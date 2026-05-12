"""
run_auditor.py — Auditor Agent（双层检测）

Layer 1: 规则检测（零 LLM 调用，纯代码）
  - 黑词扫描
  - 段落长度均匀性 CV
  - 转折词重复
  - 套话密度
  - humanize_scorer

Layer 2: 语义审计（按需触发 LLM）
  - 设定冲突
  - 剧透/越界披露
  - 对话声纹一致性
  - 叙述者替读者下结论

输出：audit report JSON
"""

import json
import os
import re
import sys
from pathlib import Path

import yaml


# === Layer 1: 规则检测 ===

BLACKLIST_WORDS = [
    "不禁", "宛如", "仿佛", "某种程度上", "不可否认",
    "深吸一口气", "瞳孔骤缩", "值得一提的是",
    "嘴角勾起一抹弧度", "倒吸一口凉气",
    "心中暗道", "目光如炬", "浑身一震",
    "一抹", "一丝", "一缕", "某种程度",
]

PHYSICAL_REACTIONS = [
    "心脏猛地一跳", "瞳孔骤缩", "浑身一震",
]

TRANSITION_WORDS = ["然而", "但是", "不过", "忽然", "竟然", "猛然"]

HEDGE_WORDS = ["此外", "值得注意的是", "需要指出", "从某种意义上", "不可否认"]


def split_paragraphs(text):
    """按空行分割段落"""
    paragraphs = re.split(r"\n\s*\n", text)
    return [p.strip() for p in paragraphs if p.strip()]


def count_chars(text):
    """统计中文字符数"""
    return len(re.findall(r"[一-鿿]", text))


def detect_blackwords(text):
    """检测黑词"""
    issues = []
    for word in BLACKLIST_WORDS:
        count = text.count(word)
        if count > 0:
            issues.append({
                "type": "blackword",
                "detail": f"使用了禁词'{word}' × {count}",
                "severity": "high",
                "action": "rewrite",
            })
    return issues


def detect_physical_reactions(text):
    """检测生理反应禁令"""
    issues = []
    for reaction in PHYSICAL_REACTIONS:
        if reaction in text:
            issues.append({
                "type": "physical_reaction",
                "detail": f"使用了禁用生理反应'{reaction}'",
                "severity": "high",
                "action": "rewrite",
            })
    return issues


def detect_paragraph_cv(text):
    """检测段落长度均匀性"""
    paragraphs = split_paragraphs(text)
    if len(paragraphs) < 3:
        return []

    lengths = [count_chars(p) for p in paragraphs]
    mean = sum(lengths) / len(lengths)
    if mean == 0:
        return []

    variance = sum((l - mean) ** 2 for l in lengths) / len(lengths)
    cv = (variance ** 0.5) / mean

    if cv < 0.15:
        return [{
            "type": "paragraph_cv",
            "detail": f"段落长度变异系数 CV={cv:.3f}（<0.15），AI 味嫌疑",
            "severity": "medium",
            "action": "flag",
        }]
    return []


def detect_transition_repetition(text):
    """检测转折词重复"""
    issues = []
    char_count = count_chars(text)
    if char_count == 0:
        return issues

    for word in TRANSITION_WORDS:
        count = text.count(word)
        density = count / (char_count / 1000)
        if density > 3:
            issues.append({
                "type": "transition_repetition",
                "detail": f"转折词'{word}'出现 {count} 次（密度 {density:.1f}/千字 > 3）",
                "severity": "medium",
                "action": "flag",
            })
    return issues


def detect_hedge_density(text):
    """检测套话密度"""
    char_count = count_chars(text)
    if char_count == 0:
        return []

    total = sum(text.count(w) for w in HEDGE_WORDS)
    density = total / (char_count / 1000)

    if density > 3:
        return [{
            "type": "hedge_density",
            "detail": f"套话密度 {density:.1f}/千字（> 3）",
            "severity": "medium",
            "action": "flag",
        }]
    return []


def detect_banned_patterns(text):
    """检测黑句式"""
    issues = []
    # "不是...而是..." 句式
    if re.search(r"不是[^。，]{2,}而是", text):
        issues.append({
            "type": "banned_pattern",
            "detail": "使用了'不是……而是……'句式",
            "severity": "critical",
            "action": "rewrite",
        })
    # 总结性句尾
    summary_patterns = [
        r"这一刻.{0,10}明白了",
        r"他终于意识到",
        r"这标志着",
        r"这意味着",
    ]
    for pattern in summary_patterns:
        if re.search(pattern, text):
            issues.append({
                "type": "banned_pattern",
                "detail": f"使用了总结性句式: {pattern}",
                "severity": "high",
                "action": "rewrite",
            })
    return issues


def run_layer1(text):
    """Layer 1: 规则检测"""
    all_issues = []
    all_issues.extend(detect_blackwords(text))
    all_issues.extend(detect_physical_reactions(text))
    all_issues.extend(detect_paragraph_cv(text))
    all_issues.extend(detect_transition_repetition(text))
    all_issues.extend(detect_hedge_density(text))
    all_issues.extend(detect_banned_patterns(text))
    return all_issues


# === Layer 2: 语义审计（需要 LLM） ===

def build_semantic_prompt(text, packet):
    """构建 Layer 2 语义审计的 prompt"""
    parts = []
    parts.append("你是小说审计员。检查以下初稿是否存在问题。")
    parts.append("\n## 检查项")
    parts.append("1. 设定冲突：角色行为是否与已知设定矛盾？")
    parts.append("2. 剧透/越界披露：是否提前揭示了禁止揭示的信息？")
    parts.append("3. 对话声纹：角色对话是否符合其声纹特征？")
    parts.append("4. 叙述者越界：是否有叙述者替读者下结论的句子？")

    parts.append("\n## 禁止揭示的信息")
    for item in packet.get("forbidden_reveals", []):
        parts.append(f"  - {item['text']}")

    parts.append("\n## 角色声纹")
    if packet.get("pov_character_voice"):
        parts.append(packet["pov_character_voice"])

    parts.append(f"\n## 初稿\n{text[:6000]}")  # 截断防止超长

    parts.append("\n## 输出格式")
    parts.append("""返回 JSON 数组，每个问题：
[
  {
    "type": "设定冲突|剧透|声纹偏移|叙述者越界",
    "detail": "具体问题描述",
    "severity": "critical|high|medium",
    "action": "rewrite|flag",
    "line_hint": "问题出现的大致位置"
  }
]
如果没有问题，返回空数组 []。""")

    return "\n".join(parts)


def run_auditor(draft_path, packet_path, project_root=None):
    """主函数：运行双层审计"""
    # 读取初稿
    with open(draft_path, "r", encoding="utf-8") as f:
        text = f.read()

    # 读取 packet
    with open(packet_path, "r", encoding="utf-8") as f:
        packet = json.load(f)

    scene_id = packet.get("scene_id", "unknown")
    print(f"Auditor: 正在审计 {scene_id}...")

    # Layer 1: 规则检测
    layer1_issues = run_layer1(text)
    print(f"  Layer 1 检测到 {len(layer1_issues)} 个问题")

    # Layer 2: 语义审计（按需触发）
    layer2_issues = []
    threshold = 3  # Layer 1 问题数 ≥ 此值时触发 Layer 2
    if len(layer1_issues) >= threshold:
        print(f"  Layer 1 问题数 ≥ {threshold}，触发 Layer 2 语义审计...")
        try:
            import anthropic
            client = anthropic.Anthropic()
            prompt = build_semantic_prompt(text, packet)
            response = client.messages.create(
                model=os.getenv("AUDITOR_MODEL", "mimo-v2.5"),
                max_tokens=4000,
                messages=[{"role": "user", "content": prompt}],
            )
            # 兼容 ThinkingBlock
            result_text = ""
            for block in response.content:
                if hasattr(block, "text"):
                    result_text = block.text
                    break
            if not result_text:
                result_text = response.content[0].text
            # 尝试解析 JSON
            json_match = re.search(r"\[.*\]", result_text, re.DOTALL)
            if json_match:
                layer2_issues = json.loads(json_match.group())
        except Exception as e:
            print(f"  Layer 2 审计失败: {e}")

    # 组装报告
    report = {
        "scene_id": scene_id,
        "chapter_id": packet.get("chapter_id"),
        "layer1_issues": layer1_issues,
        "layer2_issues": layer2_issues,
        "summary": {
            "total_layer1": len(layer1_issues),
            "total_layer2": len(layer2_issues),
            "total_critical": sum(
                1 for i in layer1_issues + layer2_issues
                if i.get("severity") == "critical"
            ),
        },
    }

    # 保存报告
    output_dir = Path(packet_path).parent.parent / "07_audit"
    output_dir.mkdir(exist_ok=True)
    report_path = output_dir / f"{scene_id}_audit.json"

    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)

    print(f"  审计报告: {report_path}")
    print(f"  总问题数: {report['summary']['total_layer1'] + report['summary']['total_layer2']}")
    print(f"  严重问题: {report['summary']['total_critical']}")

    return report


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("用法: python run_auditor.py <draft.md> <packet.json>")
        sys.exit(1)

    draft_path = sys.argv[1]
    packet_path = sys.argv[2]
    run_auditor(draft_path, packet_path)
