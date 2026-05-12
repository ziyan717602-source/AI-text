# AI 长篇小说工作流

## 项目目标

用 Claude Code 编排流水线，实现 Markdown-first + Scene Packet 架构的长篇小说创作工作流。

Phase 1 验证标准：连续 3 章无设定冲突、无剧透、AI 黑词密度显著下降、盲读不像 AI 说明文。

## 核心哲学

- **轻输入**：人类只写章意图（150-400 字），不写细纲
- **重编译**：build_packet.py 做信息隔离 + 揭示预算 + 技能路由
- **轻修补**：Patch 只做 span 级微创，不碰整段

## 技术路线（v3，已确认）

- 知识主库：Markdown + YAML/JSON
- 编排器：Claude Code
- 写作流：chapter_intent → Planner → Human Checkpoint → build_packet → Writer → 规则检测 → 语义审计 → span 级 Patch → update_state
- 去 AI 味：Writer 正向锚定 60% + 铁律 20% + 边界 20%（60/20/20 法则）
- 防剧透：reveal_ledger.yaml 代码级信息隔离（不靠 prompt 警告）
- 约束分层：Writer 只看 3-5 条致命禁令，其余交给 Auditor 检测

## 目录结构

```
novel_project/
  00_rules/
    writer_rules.md              # Writer 前置层（3-5 条致命禁令）
    auditor_rules.md             # Auditor 检测层（黑词、黑句式、密度等）
    learning/
      counter_examples.md        # 反例→正例对照（仅供 Patch 参考）
      error_patterns.md          # 错题集
      micro_edit_intent.md       # 微调意图学习库
    fatigue_words.yaml           # 疲劳词表（Auditor 用）
    scene_skill_index.yaml       # 场景类型 → 技能路由（build_packet 用）

  01_world/                      # 世界观设定
  02_characters/                 # 角色档案（public/hidden/voice/state 四件套）
  03_outline/
    macro.md                     # 宏纲
    arc/                         # 弧线级大纲
    intents/                     # ★ 人类写的章意图（ch001_intent.yaml）
    contracts/                   # ★ Planner 生成的场景合同
  04_timeline/
    events.yaml                  # 已发生事件索引
    unresolved_threads.yaml      # 未回收伏笔
    reveal_ledger.yaml           # ★ 揭示账本（秘密 → 最早揭示章节 → 允许暗示 → 禁止写出）
  05_chapters/                   # 正文（draft + final）
  06_packets/                    # Scene Packet（JSON）
  07_audit/                      # 规则检测报告 + 语义审计报告
  08_refs/                       # 技能库 + 风格锚点 + 错题集
  09_scripts/                    # Python 脚本
```

## 关键约束

- **Writer 永远只吃 packet，不读原始仓库**。packet 由 build_packet.py 编译。
- **Writer 约束 60/20/20**：正向锚定 60%（few-shot + skill）/ 铁律 20%（3-5 条）/ 边界 20%。
- **Writer 内部两步**：先 <beat_sketch>（5-8 个微观节拍）再 <prose>（正文）。
- **Auditor 分两层**：Layer 1 规则检测（零 LLM）+ Layer 2 语义审计（按需触发）。
- **Patch 只改 span**：不传全章不传整段，只传问题句 + 上下文。
- **防剧透靠代码隔离**：reveal_ledger.yaml + build_packet 信息过滤，不靠 prompt 警告。
- **Human Checkpoint**：Planner 产出场景合同后，人类扫 30 秒确认结构无跑偏。
- **测试细纲必须原创**。不能从已有小说提取细纲做测试。

## 执行原则

- 螺旋上升：先跑通最小闭环，再迭代增强
- 文档同步：每次决策/踩坑都更新 docs/ 下对应文件
- 进度跟踪：用 TodoWrite 跟踪当前会话任务，用 docs/progress.md 跟踪跨会话进度

## 参考库（只读）

| 库名 | 核心价值 | 复用方式 |
|------|----------|----------|
| ai_creator | 391+ 写作 Skill | 复制 20-30 个到 08_refs/skills/ |
| inkos | 去 AI 味引擎 | 翻译 ai-tells.ts → ai_tell_detector.py；整合铁律 |
| craft-companion | 知识库架构 | 借鉴 5 层目录 + 双层自查 |
| novel-generator | Humanize 评分 | 复用 humanize_service.py → humanize_scorer.py |
| AI_NovelGenerator | Prompt 模板 | 整合到 Writer/Auditor prompt |

## 深入文档

- 技术方案（v1）：`长篇小说AI工作流-Phase1实施计划.md`
- 开发进度：`docs/progress.md`
- 已知问题：`docs/issues.md`
- 踩坑经验：`docs/lessons.md`
- 决策依据：`调研文档/决策汇总.md`
