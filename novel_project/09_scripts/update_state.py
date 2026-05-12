"""
update_state.py — 状态回写

职责：从终稿中提取状态变化，更新 state.json 和 timeline
输入：终稿 + 场景合同
输出：更新后的 state.json
"""

import json
import re
import sys
from pathlib import Path

import yaml


NAME_MAP = {"刘得宜": "liu_deyi", "玉之灵": "yu_zhiling", "李笑颜": "li_xiaoyan"}


def run_update_state(final_path, contract_path, project_root=None):
    """主函数：从终稿提取状态变化并更新"""
    project_root = Path(project_root) if project_root else Path(contract_path).parent.parent.parent

    # 读取终稿
    with open(final_path, "r", encoding="utf-8") as f:
        text = f.read()

    # 读取场景合同
    with open(contract_path, "r", encoding="utf-8") as f:
        contract = yaml.safe_load(f)

    chapter_id = contract.get("chapter_id", "unknown")
    pov = contract.get("pov", "unknown")

    print(f"update_state: 正在处理 {chapter_id}...")

    # 提取状态变化（从合同中的 state_delta）
    state_delta = contract.get("state_delta", {})

    if not state_delta:
        print("  场景合同中没有 state_delta，跳过状态更新")
        return

    # 读取当前 state.json（多方法查找目录）
    char_dir = project_root / "02_characters" / NAME_MAP.get(pov, pov.lower().replace(" ", "_"))
    if not char_dir.exists():
        for d in (project_root / "02_characters").iterdir():
            if d.is_dir() and pov in d.name:
                char_dir = d
                break

    state_path = char_dir / "state.json"
    if state_path.exists():
        with open(state_path, "r", encoding="utf-8") as f:
            state = json.load(f)
    else:
        state = {"name": pov}

    # 更新状态
    state["current_chapter"] = chapter_id
    if "before" in state_delta and "after" in state_delta:
        # 记录状态变化历史
        if "state_history" not in state:
            state["state_history"] = []
        state["state_history"].append({
            "chapter": chapter_id,
            "from": state_delta.get("before", ""),
            "to": state_delta.get("after", ""),
        })

    # 保存更新后的 state.json
    with open(state_path, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)

    print(f"  已更新: {state_path}")

    # 更新 events.yaml
    events_path = project_root / "04_timeline" / "events.yaml"
    if events_path.exists():
        with open(events_path, "r", encoding="utf-8") as f:
            events = yaml.safe_load(f) or {"events": []}
    else:
        events = {"events": []}

    events["events"].append({
        "chapter": chapter_id,
        "description": state_delta.get("after", ""),
        "character": pov,
    })

    with open(events_path, "w", encoding="utf-8") as f:
        yaml.dump(events, f, allow_unicode=True, default_flow_style=False)

    print(f"  已更新: {events_path}")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("用法: python update_state.py <final.md> <contract.yaml> [project_root]")
        sys.exit(1)

    project_root = sys.argv[3] if len(sys.argv) > 3 else None
    run_update_state(sys.argv[1], sys.argv[2], project_root)
