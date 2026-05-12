"""
build_packet.py — Scene Packet 编译器

职责：
1. 信息隔离：过滤 POV 不可见信息（hidden.md 不给 Writer）
2. 揭示预算：对比 reveal_ledger.yaml，裁剪 forbidden_before 内容
3. 技能路由：根据 scene_type 自动挂载 skill + 风格锚点
4. 注入规则：writer_rules.md + 3-5 条致命禁令

输入：scene_contract.yaml + 角色文件 + 世界观 + reveal_ledger
输出：packet.json
"""

import json
import os
import re
import sys
from pathlib import Path

import yaml


def load_yaml(path):
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def load_text(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def parse_chapter_number(chapter_id):
    """从 chapter_id 中提取章节数字，如 mid_ch001 -> 1"""
    m = re.search(r"ch(\d+)", chapter_id)
    return int(m.group(1)) if m else 0


def filter_reveals(secrets, current_chapter_num):
    """根据当前章节号，过滤 reveal_ledger 中的秘密"""
    allowed = []
    forbidden = []
    for secret in secrets:
        reveal_num = parse_chapter_number(str(secret.get("reveal_chapter", "ch999")))
        if current_chapter_num >= reveal_num:
            allowed.append({
                "id": secret["id"],
                "name": secret["name"],
                "status": "revealed",
            })
        else:
            allowed.extend([
                {"id": f"{secret['id']}_hint", "text": hint}
                for hint in secret.get("allowed_before", [])
            ])
            forbidden.extend([
                {"id": f"{secret['id']}_ban", "text": ban}
                for ban in secret.get("forbidden_before", [])
            ])
    return allowed, forbidden


def get_scene_skill(scene_type, skill_index_path):
    """根据 scene_type 获取对应的 skill 和风格锚点"""
    skill_index = load_yaml(skill_index_path)
    scene_skills = skill_index.get("scene_skills", {})
    if scene_type in scene_skills:
        return scene_skills[scene_type]
    return {"name": "默认", "skills": [], "style_anchor": None}


def build_packet(contract_path, project_root):
    """主函数：编译 scene packet"""
    project_root = Path(project_root)

    # 1. 读取场景合同
    contract = load_yaml(contract_path)
    chapter_id = contract.get("chapter_id", "unknown")
    scene_id = contract.get("scene_id", f"{chapter_id}_s01")
    pov = contract.get("pov", "unknown")
    scene_type = contract.get("scene_type", "dialogue")

    # 2. 读取 POV 角色的 public.md（不读 hidden.md）
    # 支持中文名：遍历所有角色目录，用 public.md 内容匹配
    char_dir = None
    characters_root = project_root / "02_characters"
    if characters_root.exists():
        for d in characters_root.iterdir():
            if not d.is_dir():
                continue
            # 方法1：目录名包含角色名（英文名）
            if pov.lower().replace(" ", "_") in d.name.lower():
                char_dir = d
                break
            # 方法2：读 public.md 检查标题是否包含角色名
            public_file = d / "public.md"
            if public_file.exists():
                with open(public_file, "r", encoding="utf-8") as f:
                    first_lines = f.read(200)
                if pov in first_lines or d.name.replace("_", " ").title() in pov:
                    char_dir = d
                    break
        # 方法3：如果还没找到，用第一个匹配 pinyin 的目录
        if char_dir is None:
            name_map = {"刘得宜": "liu_deyi", "玉之灵": "yu_zhiling", "李笑颜": "li_xiaoyan"}
            mapped = name_map.get(pov, "")
            if mapped:
                candidate = characters_root / mapped
                if candidate.exists():
                    char_dir = candidate

    public_info = ""
    voice_info = ""
    if char_dir.exists():
        public_file = char_dir / "public.md"
        voice_file = char_dir / "voice.md"
        if public_file.exists():
            public_info = load_text(public_file)
        if voice_file.exists():
            voice_info = load_text(voice_file)

    # 3. 读取 reveal_ledger
    reveal_ledger_path = project_root / "04_timeline" / "reveal_ledger.yaml"
    allowed_hints = []
    forbidden_reveals = []
    if reveal_ledger_path.exists():
        ledger = load_yaml(reveal_ledger_path)
        secrets = ledger.get("secrets", [])
        current_num = parse_chapter_number(chapter_id)
        allowed_hints, forbidden_reveals = filter_reveals(secrets, current_num)

    # 4. 获取场景技能和风格锚点
    skill_index_path = project_root / "00_rules" / "scene_skill_index.yaml"
    scene_skill = get_scene_skill(scene_type, skill_index_path)

    # 5. 读取风格锚点
    style_anchor = ""
    anchor_name = scene_skill.get("style_anchor")
    if anchor_name:
        anchor_path = project_root / "08_refs" / "samples" / anchor_name
        if anchor_path.exists():
            style_anchor = load_text(anchor_path)

    # 6. 读取 Writer 规则
    writer_rules = load_text(project_root / "00_rules" / "writer_rules.md")

    # 7. 读取全局风格规则
    global_style_path = project_root / "00_rules" / "global_style.md"
    global_style = load_text(global_style_path) if global_style_path.exists() else ""

    # 8. 组装 packet
    packet = {
        "scene_id": scene_id,
        "chapter_id": chapter_id,
        "pov": pov,
        "scene_purpose": contract.get("purpose", ""),
        "must_happen": contract.get("must_happen", []),
        "must_not_reveal": contract.get("must_not_reveal", []),
        "allowed_characters": contract.get("allowed_characters", []),
        "state_delta": contract.get("state_delta", {}),
        "scene_type": scene_type,
        "target_words": contract.get("target_words", 2000),
        "tone": contract.get("tone", ""),
        # 信息隔离：只给 public + voice，不给 hidden
        "pov_character_public": public_info,
        "pov_character_voice": voice_info,
        # 揭示预算
        "allowed_hints": allowed_hints,
        "forbidden_reveals": forbidden_reveals,
        # 技能和风格
        "scene_skills": scene_skill.get("skills", []),
        "style_anchor": style_anchor,
        # 规则
        "writer_rules": writer_rules,
        "global_style": global_style,
    }

    # 9. 输出 packet JSON
    output_dir = project_root / "06_packets"
    output_dir.mkdir(exist_ok=True)
    output_path = output_dir / f"{scene_id}.packet.json"

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(packet, f, ensure_ascii=False, indent=2)

    print(f"Packet 编译完成: {output_path}")
    print(f"  场景: {scene_id}")
    print(f"  POV: {pov}")
    print(f"  类型: {scene_type}")
    print(f"  禁止揭示: {len(forbidden_reveals)} 项")
    print(f"  风格锚点: {anchor_name or '无'}")

    return packet


def build_all_chapters(project_root):
    """为所有场景合同编译 packet"""
    project_root = Path(project_root)
    contracts_dir = project_root / "03_outline" / "contracts"

    if not contracts_dir.exists():
        print("错误: 03_outline/contracts/ 目录不存在")
        return

    contracts = list(contracts_dir.glob("*.yaml"))
    if not contracts:
        print("警告: contracts/ 目录下没有 .yaml 文件")
        return

    for contract_path in sorted(contracts):
        print(f"\n--- 编译 {contract_path.name} ---")
        try:
            build_packet(str(contract_path), str(project_root))
        except Exception as e:
            print(f"错误: {e}")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        # 编译指定合同
        contract_path = sys.argv[1]
        project_root = sys.argv[2] if len(sys.argv) > 2 else "j:/Project/小说/novel_project"
        build_packet(contract_path, project_root)
    else:
        # 编译所有合同
        project_root = "j:/Project/小说/novel_project"
        build_all_chapters(project_root)
