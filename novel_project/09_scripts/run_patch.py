"""
run_patch.py — Patch Agent（span 级微创手术）

职责：只改 Auditor 标红的 hard_fail 问题，不碰全文
输入：审计报告 + 初稿 + packet
输出：修正后的终稿
"""

import json
import os
import re
import sys
from pathlib import Path

import anthropic


def find_span_context(text, target, context_chars=100):
    """在文本中定位问题 span，并提取前后上下文"""
    idx = text.find(target)
    if idx == -1:
        # 尝试模糊匹配（去掉空格和标点后比较）
        clean_target = re.sub(r"\s+", "", target)
        for i in range(len(text) - len(clean_target)):
            segment = re.sub(r"\s+", "", text[i:i + len(clean_target) * 2])
            if clean_target in segment:
                idx = i
                break

    if idx == -1:
        return None

    start = max(0, idx - context_chars)
    end = min(len(text), idx + len(target) + context_chars)
    before = text[start:idx]
    span = text[idx:idx + len(target)]
    after = text[idx + len(target):end]

    return {
        "before": before,
        "span": span,
        "after": after,
        "full_context": text[start:end],
    }


def build_patch_prompt(span_info, issue, writer_rules):
    """构建 Patch 的 prompt"""
    parts = []
    parts.append("你是小说微编辑。只修改下面标出的问题句，不要重写其他部分。")
    parts.append(f"\n## 铁律\n{writer_rules}")
    parts.append(f"\n## 问题")
    parts.append(f"类型: {issue.get('type')}")
    parts.append(f"详情: {issue.get('detail')}")
    parts.append(f"\n## 需要修改的句子（只改这句）")
    parts.append(f"前文: ...{span_info['before']}...")
    parts.append(f"问题句: {span_info['span']}")
    parts.append(f"后文: {span_info['after']}...")
    parts.append(f"\n## 要求")
    parts.append("- 只替换问题句，保持上下文衔接无缝")
    parts.append("- 不要重写前后文")
    parts.append("- 保持原文风格和节奏")
    parts.append(f"- 建议改法: {issue.get('suggestion', '自行判断')}")

    return "\n".join(parts)


def run_patch(draft_path, audit_report_path, packet_path, output_dir=None):
    """主函数：运行 Patch Agent"""
    # 读取初稿
    with open(draft_path, "r", encoding="utf-8") as f:
        text = f.read()

    # 读取审计报告
    with open(audit_report_path, "r", encoding="utf-8") as f:
        report = json.load(f)

    # 读取 packet
    with open(packet_path, "r", encoding="utf-8") as f:
        packet = json.load(f)

    # 读取 writer rules
    rules_path = Path(packet_path).parent.parent / "00_rules" / "writer_rules.md"
    writer_rules = ""
    if rules_path.exists():
        with open(rules_path, "r", encoding="utf-8") as f:
            writer_rules = f.read()

    scene_id = report.get("scene_id", "unknown")
    print(f"Patch Agent: 正在修复 {scene_id}...")

    # 收集需要 patch 的问题（只处理 hard_fail: rewrite）
    issues_to_patch = []
    for issue in report.get("layer1_issues", []):
        if issue.get("action") == "rewrite":
            issues_to_patch.append(issue)
    for issue in report.get("layer2_issues", []):
        if issue.get("action") == "rewrite":
            issues_to_patch.append(issue)

    if not issues_to_patch:
        print("  无需修复的问题")
        # 直接复制初稿为终稿
        if output_dir is None:
            output_dir = Path(draft_path).parent
        final_path = Path(output_dir) / Path(draft_path).name.replace("_draft", "_final")
        with open(final_path, "w", encoding="utf-8") as f:
            f.write(text)
        print(f"  终稿（无修改）: {final_path}")
        return text

    print(f"  需修复 {len(issues_to_patch)} 个问题")

    # 逐个修复
    modified_text = text
    client = anthropic.Anthropic()

    for i, issue in enumerate(issues_to_patch):
        # 从 detail 中提取问题句
        detail = issue.get("detail", "")
        # 尝试从 detail 中提取引号内的内容
        quoted = re.findall(r"['「](.+?)['」]", detail)
        target = quoted[0] if quoted else detail

        span_info = find_span_context(modified_text, target)
        if not span_info:
            print(f"  [{i+1}] 无法定位: {target[:30]}...")
            continue

        prompt = build_patch_prompt(span_info, issue, writer_rules)

        try:
            response = client.messages.create(
                model=os.getenv("PATCH_MODEL", "mimo-v2.5"),
                max_tokens=1000,
                messages=[{"role": "user", "content": prompt}],
            )
            # 兼容 ThinkingBlock
            replacement = ""
            for block in response.content:
                if hasattr(block, "text"):
                    replacement = block.text.strip()
                    break
            if not replacement:
                replacement = response.content[0].text.strip()

            # 替换
            modified_text = modified_text.replace(span_info["span"], replacement, 1)
            print(f"  [{i+1}] 已修复: {issue.get('type')} — {issue.get('detail', '')[:40]}...")
        except Exception as e:
            print(f"  [{i+1}] 修复失败: {e}")

    # 保存终稿
    if output_dir is None:
        output_dir = Path(draft_path).parent
    final_path = Path(output_dir) / Path(draft_path).name.replace("_draft", "_final")

    with open(final_path, "w", encoding="utf-8") as f:
        f.write(modified_text)

    print(f"  终稿: {final_path}")
    return modified_text


if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("用法: python run_patch.py <draft.md> <audit_report.json> <packet.json>")
        sys.exit(1)

    run_patch(sys.argv[1], sys.argv[2], sys.argv[3])
