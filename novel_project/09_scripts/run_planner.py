"""
run_planner.py — Planner Agent

职责：读取 chapter_intent.yaml，生成 scene_contracts/*.yaml
输入：chapter_intent.yaml + 角色文件 + 世界观
输出：scene_contracts/chXXX_s01.yaml, chXXX_s02.yaml, ...
"""

import json
import os
import re
import sys
from pathlib import Path

import anthropic
import yaml


def build_planner_prompt(intent, world_info="", character_info=""):
    """构建 Planner 的 prompt"""
    parts = []
    parts.append("你是小说结构师。根据章意图，拆分为 2-4 个场景合同。")
    parts.append("\n## 输出格式")
    parts.append("""每个场景输出一个 YAML 文件，格式如下：
scene_id: ch001_s01
chapter_id: ch001
pov: 视角角色
purpose: 这个场景要完成什么（1-2 句话）
must_happen:
  - 事件1
  - 事件2
must_not_reveal:
  - 禁区1
scene_type: dialogue|action|emotion|revelation|atmosphere|flashback
target_words: 1200
tone: 这个场景的气质（1 句话）
allowed_characters:
  - 角色1
  - 角色2
state_delta:
  character: 主要角色
  before: 场景开始时的状态
  after: 场景结束时的状态
""")

    parts.append("\n## 章意图")
    parts.append(json.dumps(intent, ensure_ascii=False, indent=2))

    if world_info:
        parts.append(f"\n## 世界观（参考，不要泄露）\n{world_info[:2000]}")
    if character_info:
        parts.append(f"\n## 角色信息（参考）\n{character_info[:2000]}")

    parts.append("\n## 注意事项")
    parts.append("- 不要在场景合同中写写作指导（如'用短句'、'用动作代替'等）")
    parts.append("- 场景合同只管结构，不管文风")
    parts.append("- 每个场景的 state_delta 要连贯：上一个的 after 是下一个的 before")
    parts.append("- must_not_reveal 要递进：后续场景可以比前面暗示更多")
    parts.append("- scene_type 只能是：dialogue, action, emotion, revelation, atmosphere, flashback")

    return "\n".join(parts)


def run_planner(intent_path, project_root=None):
    """主函数：运行 Planner Agent"""
    project_root = Path(project_root) if project_root else Path(intent_path).parent.parent.parent

    # 读取章意图
    with open(intent_path, "r", encoding="utf-8") as f:
        intent = yaml.safe_load(f)

    chapter_id = intent.get("chapter_id", "unknown")
    print(f"Planner Agent: 正在为 {chapter_id} 生成场景合同...")

    # 读取世界观（可选）
    world_path = project_root / "01_world" / "setting.md"
    world_info = ""
    if world_path.exists():
        with open(world_path, "r", encoding="utf-8") as f:
            world_info = f.read()

    # 读取角色信息（可选）
    pov = intent.get("pov", "")
    char_info = ""
    char_dir = project_root / "02_characters"
    if char_dir.exists():
        for d in char_dir.iterdir():
            if d.is_dir() and pov in d.name:
                public_file = d / "public.md"
                if public_file.exists():
                    with open(public_file, "r", encoding="utf-8") as f:
                        char_info = f.read()
                break

    # 调用 Claude
    client = anthropic.Anthropic()
    prompt = build_planner_prompt(intent, world_info, char_info)

    response = client.messages.create(
        model=os.getenv("PLANNER_MODEL", "mimo-v2.5"),
        max_tokens=4000,
        messages=[{"role": "user", "content": prompt}],
    )

    # 兼容 ThinkingBlock
    raw_output = ""
    for block in response.content:
        if hasattr(block, "text"):
            raw_output = block.text
            break
    if not raw_output:
        raw_output = response.content[0].text

    # 解析输出：提取多个 YAML 块
    # 先去除 markdown 代码围栏
    raw_output = re.sub(r"```(?:yaml|yml)?\s*\n?", "", raw_output)
    raw_output = re.sub(r"```\s*$", "", raw_output, flags=re.MULTILINE)
    yaml_blocks = re.split(r"---+\n?", raw_output)
    yaml_blocks = [b.strip() for b in yaml_blocks if b.strip() and not b.strip().startswith("#")]

    contracts = []
    output_dir = project_root / "03_outline" / "contracts"
    output_dir.mkdir(parents=True, exist_ok=True)

    for i, block in enumerate(yaml_blocks):
        try:
            contract = yaml.safe_load(block)
            if contract and "scene_id" in contract:
                scene_id = contract["scene_id"]
                output_path = output_dir / f"{scene_id}.yaml"
                with open(output_path, "w", encoding="utf-8") as f:
                    yaml.dump(contract, f, allow_unicode=True, default_flow_style=False)
                contracts.append(contract)
                print(f"  已生成: {output_path}")
        except yaml.YAMLError as e:
            print(f"  YAML 解析失败 (block {i}): {e}")

    print(f"  共生成 {len(contracts)} 个场景合同")
    return contracts


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python run_planner.py <intent.yaml> [project_root]")
        sys.exit(1)

    intent_path = sys.argv[1]
    project_root = sys.argv[2] if len(sys.argv) > 2 else None
    run_planner(intent_path, project_root)
