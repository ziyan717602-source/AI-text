"""
run_writer.py — Writer Agent

职责：读取 packet，调用 Claude 生成初稿
内部两步：先 <beat_sketch>（5-8 个微观节拍）→ 再 <prose>（正文）

约束比例（60/20/20）：
- 60% 正向锚定：风格锚点 + skill
- 20% 铁律底线：3-5 条致命禁令
- 20% 边界控制：只看 packet
"""

import json
import os
import sys
from pathlib import Path

import anthropic
import yaml


def load_yaml(path):
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def build_writer_prompt(packet):
    """组装 Writer 的系统 prompt"""
    parts = []

    # 身份
    parts.append("你是顶尖小说写手。把场景合同扩写为正文。")

    # 正向锚定 60%
    parts.append("\n## 正向锚定（参考这些来写）")
    if packet.get("style_anchor"):
        parts.append(f"\n### 风格样本\n{packet['style_anchor']}")
    if packet.get("scene_skills"):
        parts.append(f"\n### 场景技能\n当前场景类型适用的写作手法：{', '.join(packet['scene_skills'])}")
    if packet.get("tone"):
        parts.append(f"\n### 气质要求\n{packet['tone']}")

    # 铁律底线 20%
    parts.append("\n## 铁律（绝对不可违反）")
    parts.append(packet.get("writer_rules", ""))

    # 边界控制 20%
    parts.append("\n## 边界")
    parts.append("- 只看下面提供的信息，不要自行补充设定")
    parts.append("- 不要写其他角色的内心活动")
    parts.append(f"- 目标字数：{packet.get('target_words', 2000)} 字")

    # 场景合同
    parts.append("\n## 场景合同")
    parts.append(f"场景目的：{packet.get('scene_purpose', '')}")
    parts.append(f"必须发生：")
    for item in packet.get("must_happen", []):
        parts.append(f"  - {item}")
    parts.append(f"禁止揭示：")
    for item in packet.get("must_not_reveal", []):
        parts.append(f"  - {item}")

    # 禁止揭示的细节（reveal_ledger）
    if packet.get("forbidden_reveals"):
        parts.append("\n### 严格禁止写出以下内容")
        for item in packet["forbidden_reveals"]:
            parts.append(f"  - {item['text']}")

    # 角色信息
    if packet.get("pov_character_public"):
        parts.append(f"\n## POV 角色公开信息\n{packet['pov_character_public']}")
    if packet.get("pov_character_voice"):
        parts.append(f"\n## POV 角色声纹\n{packet['pov_character_voice']}")

    # 全局风格
    if packet.get("global_style"):
        parts.append(f"\n## 全局风格规则\n{packet['global_style']}")

    return "\n".join(parts)


def generate_beat_sketch(client, system_prompt, packet):
    """Step 1: 生成微观节拍（不落盘）"""
    prompt = f"""根据场景合同，在心里规划 5-8 个微观节拍。
输出格式：
<beat_sketch>
1. [开场动作/环境]
2. [第一次张力点]
3. [信息传递/对话]
4. [转折/擦边点]
5. [场景结尾动作]
...（根据需要增减）
</beat_sketch>

然后立即开始写正文。

场景合同：
{json.dumps({
    'purpose': packet.get('scene_purpose'),
    'must_happen': packet.get('must_happen'),
    'must_not_reveal': packet.get('must_not_reveal'),
    'tone': packet.get('tone'),
    'target_words': packet.get('target_words'),
}, ensure_ascii=False, indent=2)}
"""

    response = client.messages.create(
        model=os.getenv("WRITER_MODEL", "mimo-v2.5"),
        max_tokens=8000,
        system=system_prompt,
        messages=[{"role": "user", "content": prompt}],
    )
    # 兼容 ThinkingBlock：提取 TextBlock 内容
    for block in response.content:
        if hasattr(block, "text"):
            return block.text
    return response.content[0].text


def run_writer(packet_path, output_dir=None):
    """主函数：运行 Writer Agent"""
    # 读取 packet
    with open(packet_path, "r", encoding="utf-8") as f:
        packet = json.load(f)

    scene_id = packet.get("scene_id", "unknown")
    chapter_id = packet.get("chapter_id", "unknown")

    print(f"Writer Agent: 正在生成 {scene_id}...")

    # 组装 prompt
    system_prompt = build_writer_prompt(packet)

    # 调用 Claude
    client = anthropic.Anthropic()

    # 生成
    raw_output = generate_beat_sketch(client, system_prompt, packet)

    # 解析 beat_sketch 和 prose
    beat_sketch = ""
    prose = raw_output

    if "<beat_sketch>" in raw_output and "</beat_sketch>" in raw_output:
        beat_sketch = raw_output.split("<beat_sketch>")[1].split("</beat_sketch>")[0].strip()
        prose = raw_output.split("</beat_sketch>")[1].strip()

    # 保存初稿
    if output_dir is None:
        output_dir = Path(packet_path).parent.parent / "05_chapters"
    else:
        output_dir = Path(output_dir)

    output_dir.mkdir(exist_ok=True)

    # 保存 beat_sketch（调试用）
    beat_path = output_dir / f"{chapter_id}_beats.md"
    with open(beat_path, "w", encoding="utf-8") as f:
        f.write(f"# {scene_id} — 微观节拍\n\n{beat_sketch}\n")

    # 保存正文
    draft_path = output_dir / f"{chapter_id}_draft.md"
    with open(draft_path, "w", encoding="utf-8") as f:
        f.write(f"# {chapter_id}\n\n{prose}\n")

    print(f"  微观节拍: {beat_path}")
    print(f"  初稿: {draft_path}")

    return {
        "beat_sketch": beat_sketch,
        "prose": prose,
        "draft_path": str(draft_path),
    }


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python run_writer.py <packet.json> [output_dir]")
        sys.exit(1)

    packet_path = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else None
    run_writer(packet_path, output_dir)
