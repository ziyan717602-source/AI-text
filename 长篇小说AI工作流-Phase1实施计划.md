# AI 长篇小说工作流 - Phase 1 详细实施计划（v2）

> 更新时间：2026-05-12
> 更新内容：基于 5 个参考库的分析结果，调整开发内容，增加可复用资产清单

---

## 一、技术路线总览

### 核心路线

**Markdown-first + Scene Packet + 4-Agent 流水线**

| 维度 | 选择 | 理由 |
|------|------|------|
| 知识主库 | Markdown + YAML/JSON | 人类可读、Git 友好、Obsidian 原生支持 |
| 检索层 | Phase 1: SQLite FTS5 → Phase 2: + embedding | 先跑通再增强 |
| 编排器 | Claude Code (CC) | 擅长本地文件读写、状态管理 |
| 写作流 | Planner → Writer → Auditor → Patch | 写审分离，局部改写不抹平 |
| 去 AI 味 | 反向约束 + 规则检测 + 局部 Patch | 不做全章润色 |
| 防剧透 | 文件结构强制隔离 + chapter lock | 代码级过滤，不靠 prompt 自觉 |

### 为什么不用其他方案

| 方案 | 问题 |
|------|------|
| 纯 RAG 管全部真相 | 语义检索不准、plot bleed 风险、过重 |
| 一次大 prompt 成文 | 认知过载、剧情崩、AI 味重 |
| 全章润色 agent | 抹平文本、丢失锐度、更像 AI |
| 超多子 Agent + 图数据库 | Phase 1 过重，验证周期太长 |

---

## 二、当前环境

| 组件 | 状态 |
|------|------|
| Python | 3.13.9 (Anaconda, `C:\ProgramData\anaconda3`) |
| pip | 25.3 |
| anthropic SDK | 0.77.1 |
| pyyaml | 6.0.3 |
| CC 编排器 | 已就绪 |

---

## 三、参考库分析与可复用资产

已下载 5 个参考库到 `参考库/` 目录：

| 库名 | 来源 | 核心价值 |
|------|------|----------|
| ai_creator | hackiey/ai_creator | 391+ 写作 Skill（结构化 .md 格式） |
| inkos | Narcooo/inkos | 去 AI 味引擎（规则检测 + 铁律 + 反例） |
| craft-companion | qcx1919788736-collab | 5 层知识库架构 + CLAUDE.md 模板 + 双层自查 |
| novel-generator（稿匣） | mushroomfk/novel-generator | Humanize 评分 + 上下文预算 |
| AI_NovelGenerator | YILING0013/AI_NovelGenerator | 结构化 prompt 模板 + 一致性检查 |

### 3.1 ai_creator — Skill 格式

每个 skill 是一个 `.md` 文件，YAML frontmatter + 分步骤指导：

```yaml
---
slug: cinematic-scene-writing
name: "画面感场景描写"
description: "把抽象情绪改成可见的动作..."
tags: ["场景", "描写", "动作", "对话", "文风"]
---
```

**最有价值的 skill**（将复制到 `08_refs/skills/`）：
- `avoid-preachy.md` — 避免说教
- `cinematic-scene-writing.md` — 画面感场景描写
- `character-setting-card.md` — 人物设定卡
- `dialogue-rhythm-polish.md` — 对话节奏
- `chapter-pacing.md` — 章节节奏
- 约 20-30 个与去 AI 味、场景描写、角色塑造最相关的 skill

### 3.2 inkos — 去 AI 味引擎

**a) `ai-tells.ts` — 规则检测（纯代码，零 LLM 调用）**

4 个维度的结构化检测：
- 段落长度均匀性（变异系数 CV < 0.15 → AI 味）
- 套话词密度（> 3次/千字 → AI 味）
- 公式化转折词重复（同一词 ≥ 3 次）
- 列表式结构（连续 3+ 句相同开头）

→ 翻译为 Python `ai_tell_detector.py`

**b) `writer-prompts.ts` — 去 AI 味铁律（6 条）**

1. 叙述者不得替读者下结论
2. 禁止分析报告式语言（"核心动机""信息边界"等）
3. 转折/惊讶标记词全篇 ≤ 1次/3000字
4. 同一体感/意象禁止连续渲染超过两轮
5. 六步走心理分析术语只用于内部推理，不进正文
6. "不是……而是……"句式全文严禁

+ 反例→正例对照表（情绪、转折、"了"字、词汇、叙述者姿态 5 大类）

→ 整合到 `00_rules/anti_ai_iron_rules.md` 和 `00_rules/counter_examples.md`

**c) `genres/*.md` — 题材疲劳词表**

每个题材有独立的疲劳词列表（如玄幻：`["冷笑", "蝼蚁", "倒吸凉气", "瞳孔骤缩", ...]`）

→ 提取到 `00_rules/fatigue_words.yaml`

### 3.3 craft-companion — 知识库架构

**5 层知识库目录**：
- `00_核心上下文/` — 每次必读（当前状态、伏笔追踪、数值速查、文风规则）
- `01_人物档案/` — 按需加载
- `02_世界观设定/` — 按需加载
- `03_故事进展/` — 需要回溯时读
- `04_写作参考/` — 场景范例、错题集、微调意图学习库

**双层自查**：执行层自查 → 评估层复核（confirmed/disputed/dismissed 三分法）

**导入提示模板**：`导入已有小说/01-05` 可直接用于从选定小说提取角色、世界观、时间线、文风、伏笔

### 3.4 novel-generator（稿匣）— Humanize 评分

`humanize_service.py` 基于正则的 AI 味检测：
- 连接词短语（"此外"、"值得注意的是"）
- 重要性助推词（"标志着...意义"）
- 解释性语调模式
- 输出 `HumanizeTextProfile`（问题报告 + 罚分）

→ 作为 `humanize_scorer.py`

### 3.5 AI_NovelGenerator — Prompt 模板

`prompt_definitions.py` 中的结构化中文 prompt 模板，使用雪花写作法、角色弧线理论、悬念三要素模型。

→ 整合到 Writer/Auditor prompt

---

## 四、Phase 1 目标

用 **3-5 章连续剧情**跑通最小闭环，验证"防剧透"和"去 AI 味"是否有效。

### 验证标准

- [ ] 连续 3 章无明显设定冲突
- [ ] 无提前披露重大真相
- [ ] AI 黑词密度明显下降（对比一次成文基线）
- [ ] 盲读时不再像"标准 AI 说明文"

---

## 五、项目目录结构

在 `小说/` 目录下新建 `novel_project/`：

```
novel_project/
  00_rules/
    global_style.md              # 叙述人称、语体、节奏底线
    forbidden_patterns.md        # AI 黑词/黑句式清单
    scene_skill_index.yaml       # 场景类型 → 技能路由表
    anti_ai_iron_rules.md        # inkos 去 AI 味铁律（6 条）
    counter_examples.md          # inkos 反例→正例对照表
    fatigue_words.yaml           # 题材疲劳词列表

  01_world/
    setting.md                   # 世界观总设定
    factions.md                  # 势力/阵营
    places.md                    # 地点
    rules.md                     # 世界运行规则

  02_characters/
    <char>/
      public.md                  # 读者可见信息
      hidden.md                  # 仅 Planner 可读
      voice.md                   # 声纹/说话习惯
      state.json                 # 动态状态

  03_outline/
    macro.md                     # 宏纲（全书大走向）
    arc/
      arc01.md                   # 弧线级大纲
    scenes/
      ch001_s01.md               # 场景级细纲

  04_timeline/
    events.yaml                  # 已发生事件索引
    unresolved_threads.yaml      # 未回收伏笔

  05_chapters/
    ch001_draft.md               # 初稿
    ch001_final.md               # 终稿

  06_packets/
    ch001_s01.packet.json        # Scene Packet

  07_audit/
    ch001_audit.json             # 审计报告
    ai_taste_blacklist.yaml      # 实时补充的黑词
    consistency_rules.yaml       # 一致性校验规则

  08_refs/
    skills/                      # 从 ai_creator 复制的 skill 文件（20-30 个）
    samples/                     # 风格锚点（人类文本样本）
      dialogue_cold.md
      action_tension.md
      emotion_ambiguity.md
    error_patterns.md            # 错题集（写后发现的错误模式）
    micro_edit_intent.md         # 微调意图学习库（人类修改后提取意图）

  09_scripts/
    config.yaml                  # 全局配置
    build_packet.py              # Scene Packet 编译器
    run_writer.py                # Writer Agent
    run_auditor.py               # Auditor Agent
    run_patch.py                 # Patch Rewriter
    update_state.py              # 状态回写
    ai_tell_detector.py          # 规则化 AI 味检测（翻译自 inkos）
    humanize_scorer.py           # Humanize 评分（复用自稿匣）
```

---

## 六、任务清单与执行顺序

### Task 1: 建立目录结构
**内容**：创建上述所有目录和空文件
**产出**：完整的 `novel_project/` 目录树

### Task 2: 编写全局规则文件

#### `00_rules/global_style.md`
```markdown
# 全局风格规则

## 叙述人称
- 第三人称有限视角（POV 角色视角）
- 禁止全知旁白解释角色内心

## 语体
- 短句为主，长短交替
- 动作驱动，不靠形容词堆砌
- 对话带信息差，禁止角色互相解释读者已知的事

## 节奏
- 每段最多 3-4 句
- 禁止连续 3 段以上的纯描写
- 场景转换用空行分隔，不用过渡解释

## 绝对禁令
- 禁止总结性句尾（"这一刻，他明白了..."）
- 禁止空洞心理分析
- 禁止用抽象词替代动作
- 禁止全知旁白替读者理解
```

#### `00_rules/forbidden_patterns.md`
```markdown
# AI 黑词/黑句式清单

## 黑词（出现即扣分）
不禁、宛如、仿佛、某种程度上、不可否认、
深吸一口气、瞳孔骤缩、值得一提的是、
嘴角勾起一抹弧度、倒吸一口凉气、
心中暗道、目光如炬、浑身一震、
一抹、一丝、一缕、某种程度

## 黑句式
- "不是...而是..." 排比句
- "这标志着"、"这意味着" 总结性评价
- "值得注意的是" 过渡
- 每段都 "起-承-转-收" 过度工整
- 段落长度过于均匀（AI 味特征）

## 生理反应禁令
- 禁止：心脏猛地一跳、瞳孔骤缩、浑身一震
- 替代：用具体物理交互（捏碎茶杯、后退半步、手指收紧）
```

#### `00_rules/anti_ai_iron_rules.md`（整理自 inkos）
```markdown
# 去 AI 味铁律

## 铁律 1：叙述者不得替读者下结论
读者能从行为推断的意图，叙述者不得直接说出。
- ✗ 他想看陆焚能不能活
- ✓ 只写踢水囊的动作，让读者自己判断

## 铁律 2：禁止分析报告式语言
禁止"核心动机""信息边界""信息落差""核心风险""利益最大化""当前处境"等推理框架术语。
人物内心独白必须口语化、直觉化。
- ✗ 核心风险不在今晚吵赢
- ✓ 他心里转了一圈，知道今晚不是吵赢的问题

## 铁律 3：转折/惊讶标记词限制
仿佛、忽然、竟、竟然、猛地、猛然、不禁、宛如 全篇总数不超过每3000字1次。
超出时改用具体动作或感官描写传递突然性。

## 铁律 4：同一体感/意象禁止连续渲染超过两轮
第三次出现相同意象域（如"火在体内流动"）时必须切换到新信息或新动作，避免原地打转。

## 铁律 5：心理分析术语只用于内部推理
六步走心理分析中的术语（"当前处境""核心动机""信息边界""性格过滤"等）只用于 PRE_WRITE_CHECK 内部推理，绝不可出现在正文叙事中。

## 铁律 6："不是……而是……"句式全文严禁
出现即判定违规。改用直述句。
```

#### `00_rules/counter_examples.md`（整理自 inkos）
包含 5 大类反例→正例对照表：
- 情绪描写（抽象 → 身体细节）
- 转折与衔接（连接词 → 口语化/动作）
- "了"字与助词控制
- 词汇与句式
- 叙述者姿态

#### `00_rules/fatigue_words.yaml`
从 inkos `genres/*.md` 提取对应题材的疲劳词列表。

#### `00_rules/scene_skill_index.yaml`
```yaml
# 场景类型 → 技能路由
scene_skills:
  dialogue:
    name: 对话场
    load: [anti_ai_plain_spoken_cn, dialogue_subtext]
    style_anchor: dialogue_cold.md
  action:
    name: 动作/冲突场
    load: [action_short_sentences, show_dont_tell_minimal]
    style_anchor: action_tension.md
  emotion:
    name: 暧昧/情绪场
    load: [emotion_through_action, reduce_abstraction]
    style_anchor: emotion_ambiguity.md
  revelation:
    name: 信息揭示场
    load: [info_drip_not_dump, show_dont_tell_minimal]
    style_anchor: dialogue_cold.md
  atmosphere:
    name: 写景/氛围场
    load: [sensory_details, reduce_adjective_density]
    style_anchor: action_tension.md
  flashback:
    name: 回忆场
    load: [tense_shift_past, memory_not_narration]
    style_anchor: emotion_ambiguity.md
```

### Task 3: 创建测试用角色文件

选 2-3 个角色，从你选定的小说中提取信息，每人建立 4 文件：

| 文件 | 内容 | 谁能读 |
|------|------|--------|
| `public.md` | 外貌、公开身份、习惯、明面关系 | Writer + Planner |
| `hidden.md` | 身世真相、反转、伏笔真实含义 | 仅 Planner |
| `voice.md` | 常用句型、禁用词、情绪变化、动作习惯 | Writer |
| `state.json` | 当前位置、物品、关系、知道/不知道什么 | Writer + Planner |

#### state.json 示例
```json
{
  "name": "顾临",
  "current_chapter": 1,
  "current_location": "南街药铺",
  "inventory": ["旧药方"],
  "known_facts": ["沈砚懂药理", "药铺掌柜姓王"],
  "unknown_facts": ["沈砚真实身份", "五年前事件真相"],
  "relationships": {
    "沈砚": {"status": "警惕", "level": 0}
  },
  "physical_state": "健康",
  "current_goal": "治好母亲的病"
}
```

### Task 4: 从现有小说提取细纲

**流程**：
1. 你选定一本小说，告诉我书名和提取范围（建议 3 章）
2. 使用 craft-companion 的 `导入已有小说/` 提示模板辅助提取：
   - 01-提取人物信息
   - 02-提取世界观设定
   - 03-构建时间线
   - 04-分析文风特征
   - 05-识别伏笔线索
3. 归纳出场景级细纲

#### 细纲格式
```markdown
# ch001_s01 细纲

## 场景信息
- POV: 顾临
- 地点: 南街药铺
- 时间: 午后
- 在场人物: 顾临、沈砚、药铺掌柜

## 必须发生
1. 顾临进入药铺买药
2. 注意到沈砚袖口的血迹
3. 对话中试探但不点破

## 禁止发生
- 不能揭示沈砚真实身份
- 不能解释血迹来源

## 情绪弧线
顾临：目的性进入 → 起疑 → 试探 → 无果离开
```

### Task 5: 建立风格锚点库

1. 在 `08_refs/samples/` 下放入 3-5 段你认可的人类文本（300-800 字/段）
2. 从 ai_creator 的 `builtin-skills/` 中复制 20-30 个最相关的 skill 到 `08_refs/skills/`

覆盖场景：
- `dialogue_cold.md` — 冷对话/试探
- `action_tension.md` — 动作/紧张
- `emotion_ambiguity.md` — 暧昧/情绪暗流

### Task 6: 实现 Scene Packet 编译器

`09_scripts/build_packet.py`

**职责**：读取细纲 + 角色文件 + timeline，过滤未来信息，输出结构化 JSON packet

**核心逻辑**：
1. 读取 `03_outline/scenes/ch001_s01.md` 获取细纲
2. 读取出场角色的 `public.md`（过滤 `hidden.md`）
3. 读取出场角色的 `state.json`
4. 读取出场角色的 `voice.md`
5. 读取 `04_timeline/unresolved_threads.yaml`，只保留相关伏笔
6. 根据 `scene_skill_index.yaml` 确定场景类型和加载的技能
7. 读取 `global_style.md`、`forbidden_patterns.md`、`anti_ai_iron_rules.md`
8. 组装成 packet JSON（含上下文预算控制）

### Task 7: 实现 Writer Agent 脚本

`09_scripts/run_writer.py`

**职责**：读取 packet，调用 Claude 生成初稿

**Prompt 结构**（整合多源）：
```
[System] 你是小说写手。严格遵循以下约束：
- 只看 packet 提供的信息，不要自行补充设定
- 遵守 forbidden_patterns 中的所有禁令
- 遵守 anti_ai_iron_rules 中的 6 条铁律
- 参考 counter_examples 中的反例→正例对照
- 对话参考 voice.md 中的声纹描述
- 参考 style_anchor 中的样本文风

[Context] packet 内容
- scene_purpose / must_happen / must_not_happen
- known_facts_for_pov / continuity_state
- forbidden_patterns / anti_ai_iron_rules
- style_anchor 样本
- counter_examples 对照表

[Task] 根据细纲，将以下节拍扩写为完整场景正文
```

### Task 8: 实现 Auditor Agent 脚本（大幅增强）

`09_scripts/run_auditor.py`

**职责**：审查初稿，输出结构化审计报告（不改文）

**新增 2 个子模块**：
1. `09_scripts/ai_tell_detector.py` — 翻译自 inkos `ai-tells.ts`，纯规则检测（零 LLM 调用）
2. `09_scripts/humanize_scorer.py` — 复用自稿匣 `humanize_service.py`

**Auditor 检查项（7 项）**：

| # | 检查项 | 方法 | 来源 |
|---|--------|------|------|
| 1 | 设定冲突 | LLM 对比 state.json + public.md | 原设计 |
| 2 | 剧透/越界披露 | LLM 对比 forbidden_reveals | 原设计 |
| 3 | AI 黑词/黑句式 | 规则检测 + LLM 检查 | inkos + 原设计 |
| 4 | 对话声纹一致性 | LLM 对比 voice.md | 原设计 |
| 5 | 段落长度均匀性 | ai_tell_detector（CV < 0.15） | inkos ai-tells.ts |
| 6 | 套话密度 | ai_tell_detector（> 3次/千字） | inkos ai-tells.ts |
| 7 | 叙述者替读者下结论 | LLM + iron rules | inkos writer-prompts.ts |

**输出格式**：
```json
{
  "chapter": "ch001",
  "issues": [
    {
      "paragraph": 3,
      "line": 12,
      "type": "ai_blackword",
      "detail": "使用了禁词'不禁'",
      "severity": "high",
      "action": "rewrite",
      "source": "fatigue_words"
    },
    {
      "paragraph": 5,
      "line": 20,
      "type": "plot_bleed",
      "detail": "提到了'五年前事件'，该信息第15章才揭示",
      "severity": "critical",
      "action": "remove",
      "source": "forbidden_reveals"
    }
  ],
  "structural": {
    "paragraph_cv": 0.12,
    "hedge_density": 4.2,
    "repeated_transitions": ["然而×4"],
    "list_like_sentences": 3
  },
  "summary": {
    "total_issues": 2,
    "ai_taste_score": 7,
    "consistency_score": 9
  }
}
```

### Task 9: 实现 Patch Rewriter 脚本（增强）

`09_scripts/run_patch.py`

**职责**：只改 Auditor 标红的段落，不允许全章重写

**核心约束**：
- 只处理 `action: "rewrite"` 或 `action: "remove"` 的段落
- 不改剧情，只改表达
- 每次只传入一个问题段落 + 上下文，不做全章处理

**整合 inkos anti-detect 模式的 9 种改写技法**：
1. 打破句式模式
2. 口语化替换
3. 减少"了"字密度
4. 降低转折词频率
5. 情绪外化为动作
6. 删除叙述者结论
7. 群像反应具体到个人
8. 变化段落长度
9. 消除 AI 标记词

### Task 10: 实现状态回写脚本

`09_scripts/update_state.py`

**职责**：从终稿中提取状态变化，更新 state.json 和 timeline

**提取项**：
- 角色位置变化
- 物品获取/失去
- 关系变化
- 新知/未知信息变化
- 伤势/体力变化

### Task 11: 跑 Benchmark 测试

用相同的 3 章细纲，跑三条路线对比：

| 路线 | 流程 |
|------|------|
| Route A | 一次成文（Writer 直接写） |
| Route B | Planner → Writer |
| Route C | Planner → Writer → Auditor → Patch |

**评估指标**：

| 指标 | 测量方法 |
|------|----------|
| 设定冲突数 | 人工对比 state.json |
| 剧透/plot bleed 次数 | 人工检查 forbidden_reveals |
| AI 黑词密度 | ai_tell_detector 自动统计 + humanize_scorer 罚分 |
| 段落均匀性 CV | ai_tell_detector 自动计算 |
| 对话声纹可区分度 | 人工盲读判断 |
| 人类阅读体验 | 1-10 分主观评分 |

---

## 七、执行顺序

```
Step 1: 建目录结构
Step 2: 写全局规则（global_style / forbidden_patterns / anti_ai_iron_rules / counter_examples / fatigue_words）
Step 3: 复制 ai_creator skill 文件到 08_refs/skills/
Step 4: 建角色文件（你选定小说后提取）
Step 5: 从选定小说提取 3 章细纲
Step 6: 建风格锚点库（从选定小说摘取）
Step 7: 实现 ai_tell_detector.py（翻译 inkos）
Step 8: 实现 humanize_scorer.py（复用稿匣）
Step 9: 实现 build_packet.py
Step 10: 实现 run_writer.py
Step 11: 实现 run_auditor.py
Step 12: 实现 run_patch.py
Step 13: 实现 update_state.py
Step 14: 用一条细纲跑 Route A/B/C 对比
Step 15: 评估结果，调整禁令和规则
```

---

## 八、Scene Packet Schema（核心资产）

```json
{
  "scene_id": "ch001_s01",
  "chapter_id": "ch001",
  "pov": "顾临",
  "scene_purpose": "建立顾临与沈砚的第一次接触，并埋下血迹伏笔",
  "must_happen": [
    "顾临进入药铺",
    "注意到沈砚袖口的血迹",
    "对话不点破异常"
  ],
  "must_not_happen": [
    "不能揭示沈砚真实身份",
    "不能解释血迹来源"
  ],
  "allowed_characters": ["顾临", "沈砚", "药铺掌柜"],
  "allowed_places": ["南街药铺"],
  "known_facts_for_pov": [
    "顾临不认识沈砚",
    "顾临当前只觉得对方可疑"
  ],
  "continuity_state": [
    "顾临昨夜失眠",
    "身上带有旧药方"
  ],
  "style_modules": ["scene_dialogue_tension", "show_dont_tell_minimal"],
  "voice_refs": {
    "顾临": "02_characters/gu_lin/voice.md",
    "沈砚": "02_characters/shen_yan/voice.md"
  },
  "forbidden_patterns": [
    "总结升华",
    "解释性旁白过长",
    "用抽象情绪词代替动作"
  ],
  "style_anchor": "08_refs/samples/dialogue_cold.md",
  "target_length": 2000,
  "context_budget": 18000
}
```

**核心规则**：Writer 永远只吃 packet，不读原始仓库。

---

## 九、后续 Phase（Phase 1 验证通过后再做）

**Phase 2**（+2-3 周）：
- embedding + rerank
- 相似场景检索
- 对话声纹自动检查
- `08_memory/embeddings/` 目录

**Phase 3**（再往后）：
- arc 级规划
- 批量章节跑批
- 可视化状态面板
- Obsidian 插件化
