# 开发进度

> 最后更新：2026-05-13
> 工作流版本：v3（轻输入 · 重编译 · 轻修补）

## 当前阶段：Phase 1 — 准备期

目标：用 3-5 章连续剧情跑通最小闭环，验证"防剧透"和"去 AI 味"是否有效。

---

## 任务总览

### 第一阶段：基础设施（不依赖小说选择）

| # | 任务 | 状态 | 说明 |
|---|------|------|------|
| T1 | 建目录结构（v3 版） | ✅ 完成 | novel_project/ 含 intents/ contracts/ reveal_ledger.yaml |
| T2 | 编写 writer_rules.md | ✅ 完成 | 5 条致命禁令 + 黑词表 |
| T3 | 编写 auditor_rules.md | ✅ 完成 | Layer 1 规则 + Layer 2 规则 |
| T4 | 编写 scene_skill_index.yaml | ✅ 完成 | 6 种场景类型路由 |
| T5 | 从 ai_creator 复制 skill 文件 | ✅ 完成 | 3 个风格锚点（dialogue/action/emotion） |
| T6 | 实现 ai_tell_detector.py | ⏭️ 跳过 | 合并入 auditor Layer 1 黑词检测 |
| T7 | 实现 humanize_scorer.py | ⏭️ 跳过 | 合并入 auditor Layer 1 段落 CV + 套话密度 |

### 第二阶段：小说素材（用户输入）

| # | 任务 | 状态 | 前置 | 说明 |
|---|------|------|------|------|
| T8 | 创建角色文件 | ✅ 完成 | T1 | 刘得宜/玉之灵/李笑颜，各 4 文件（public/hidden/voice/state） |
| T9 | 编写 reveal_ledger.yaml | ✅ 完成 | T8 | 5 个秘密，含 reveal_chapter/forbidden_before |
| T10 | 建风格锚点库 | ✅ 完成 | T1 | 间客摘取 3 段：dialogue_cold/action_tension/emotion_ambiguity |
| T11 | 提取 chapter_intent.yaml | ✅ 完成 | T8 | 风起紫罗峡 第32-34章，3 份 intent |

### 第三阶段：核心脚本

| # | 任务 | 状态 | 前置 | 说明 |
|---|------|------|------|------|
| T12 | 实现 run_planner.py | ✅ 完成 | T2-T5, T8 | Planner Agent：intent → scene_contracts |
| T13 | 实现 build_packet.py | ✅ 完成 | T4, T9, T10 | 核心编译器：信息隔离 + 揭示预算 + 技能路由 |
| T14 | 实现 run_writer.py | ✅ 完成 | T13 | Writer Agent：packet → beat_sketch → prose |
| T15 | 实现 run_auditor.py | ✅ 完成 | T6, T7, T14 | Layer 1 规则 + Layer 2 语义（按需触发） |
| T16 | 实现 run_patch.py | ✅ 完成 | T15 | span 级微创 Patch |
| T17 | 实现 update_state.py | ✅ 完成 | T14 | 状态回写 |

### 第四阶段：测试验证

| # | 任务 | 状态 | 前置 | 说明 |
|---|------|------|------|------|
| T18 | 3 章端到端流水线测试 | ✅ 完成 | T12-T17 | 3 章全流水线跑通，暴露 Patch 剧透修复缺陷 |
| T18b | Route A/B/C 对比测试 | 待开始 | T18 | 用同一条 intent 跑三条路线对比 |
| T19 | 评估结果，调整规则 | 待开始 | T18b | 人工评估 + 原文对比 |

## 执行顺序

```
第一阶段（基础设施）：
  T1 → T2, T3, T4, T5, T6, T7（并行）

第二阶段（小说素材，需用户输入）：
  T8 → T9, T11
  T10（独立）

第三阶段（核心脚本）：
  T12 → T13 → T14 → T15 → T16 → T17

第四阶段（测试）：
  T18 → T19
```

## 端到端测试记录（2026-05-12）

**测试环境**：mimo-v2.5 模型，代理 API（token-plan-cn.xiaomimimo.com）
**测试素材**：风起紫罗峡 第32-34章 chapter_intent（用户原创，非原文提取）

### 三章全流水线测试结果

| 章节 | Writer | Auditor Layer 1 | Auditor Layer 2 | Patch | 终稿状态 |
|------|--------|-----------------|-----------------|-------|----------|
| ch001 | 5104B 正文 | 1 黑词（仿佛×2） | — (未触发) | ✅ 已修复 | 1755字，无残余问题 |
| ch002 | 正文生成成功 | 4 黑词（仿佛×2、深吸一口气×1、一丝×1、一缕×1） | 2 critical（剧透×2）+ 2 medium（声纹偏移+叙述者越界） | ⚠️ 黑词已修复，剧透未修复 | 黑词清零，但2个 critical 剧透残留 |
| ch003 | 正文生成成功 | 1 黑词（一丝×2） | — (未触发) | ✅ 已修复 | 1755字，无残余问题 |

### 状态更新测试（2026-05-13）

**测试脚本**：update_state.py（修复 L001 中文目录名 bug + L006 emotional_state 类型 bug）

| 章节 | 输入 | 输出 | 状态 |
|------|------|------|------|
| ch001 | final.md + s01.yaml | state.json + events.yaml | ✅ state_history 记录 1 条 |
| ch002 | final.md + s02.yaml | state.json + events.yaml | ✅ state_history 累计 2 条 |
| ch003 | final.md + s03.yaml | state.json + events.yaml | ✅ state_history 累计 3 条 |

**局限性**：state.json 的 `emotional_state`、`current_goal`、`relationships` 等字段未更新（L006）

### Planner Agent 自动测试（2026-05-13）

**测试输入**：mid_ch001_intent.yaml
**预期输出**：2-4 个场景合同
**实际输出**：1 个合同（mid_ch001_s03.yaml），scene_id 编号幻觉

**对比评估**：

| 维度 | 手动创建 (s01) | 自动生成 (s03) |
|------|---------------|---------------|
| must_happen | 3 条，简洁直接 | 4 条，叙述层次更丰富 |
| must_not_reveal | 3 条，准确 | 3 条，同样准确 |
| tone | 棋逢对手，暗流涌动 | 更文学化，知识作为武器与盾牌 |
| state_delta | 清晰的 before→after | 更详细的转变描述 |
| scene_type | dialogue | revelation |
| 数量 | 符合预期 | ❌ 只生成 1 个（应 2-4） |
| 编号 | s01 ✅ | s03 ❌ 幻觉 |

**结论**：自动生成的合同质量不低于手动版本，但需要修复 prompt 强制多场景拆分和编号规则

### 原文对比分析（2026-05-13）

**对比素材**：风起紫罗峡 第一章~第三章（接触/觉悟/交易）
**分析方法**：原文为锚点 → chapter_intent 为中间层 → AI 最终稿为目标产物

| 章节 | 原文字数 | intent must_include | 信息密度保留 | 关键差异 |
|------|---------|---------------------|-------------|---------|
| ch001 | ~5800 | 5 条 | **低** | 丢失暗世界哲学论述（原文核心精华~1500字） |
| ch002 | ~4800 | 6 条 | **中** | reveal_ledger 冲突：intent 要求 include 但 ledger 禁止揭示 |
| ch003 | ~6800 | 8 条 | **高** | 关键节拍齐全，AI 新增意象性细节 |

**核心发现**：
1. **intent × reveal_ledger 结构性冲突**（L009）：ch002 intent 要求揭示金丹远景和核反应目标，但 reveal_ledger 禁止在 ch20/ch30 前揭示。当前工作流无自动交叉检查
2. **intent 信息密度是流水线瓶颈**（L010）：ch001 的 intent 过度精简，丢失了原文最有价值的论述段落
3. **AI writer 创造性偏差**：大部分正面（增加文学性），但 ch002 中玉之灵行为从"自发感悟"变为"被要求感悟"，改变了角色关系
4. **文风差异**：原文偏论述型（跟着角色思考），AI 偏氛围型（电影化叙事）。最大差距在信息密度

详见 `docs/comparison_analysis.md`

### 关键发现

**✅ 验证通过的能力**：
1. **信息隔离有效**：build_packet.py 正确过滤 forbidden_reveals，ch001/ch003 无剧透
2. **黑词检测可靠**：Layer 1 零 LLM 调用，精准定位所有禁词
3. **span 级 Patch 对黑词有效**：定位 + 替换一气呵成，不伤周围文本
4. **声纹检测有效**：Layer 2 捕捉到 ch002 中刘得宜回应过于平和的声纹偏移

**❌ 暴露的缺陷**：
1. **Patch 无法修复剧透问题**（critical）：当 forbidden_reveal 指向的是一大段信息性文本（如"中期目标是建立一套能够安全介入并利用核级能量反应的接口与转化机制"），`find_span_context` 无法精确定位——剧透分散在多句话中，不是单个关键词。这是架构级缺陷，需要在 Writer 阶段拦截，而非 Patch 阶段修补。
2. **ch002 Writer 忽略了 must_not_reveal 约束**：尽管 packet 中携带了禁止揭示列表，Writer 仍然生成了完整剧透。说明当前 prompt 中禁止揭示的权重不够，或者 Writer 模型（mimo-v2.5）对长列表约束的遵循能力不足。

---

## 决策日志

| 日期 | 决策 | 原因 |
|------|------|------|
| 2026-05-12 | 确认技术路线：Markdown-first + Scene Packet + 4-Agent | 5 份调研报告 + 5 个参考库分析收敛到同一路线 |
| 2026-05-12 | 测试细纲必须原创，不从已有小说提取 | 避免 LLM 凭记忆还原原文，测试结果虚高 |
| 2026-05-12 | 暂不创建 Skill，用 CLAUDE.md + docs 管理 | 项目仍在探索期，过早抽象增加维护负担 |
| 2026-05-12 | 升级到 v3 架构：轻输入 + 重编译 + 轻修补 | 人类写细纲不可持续；负向约束过多会杀死创造力 |
| 2026-05-12 | 人类输入从"场景细纲"降级为"chapter_intent" | 150-400 字的章意图替代 5000+ 字的超细纲 |
| 2026-05-12 | 新增 reveal_ledger.yaml 做代码级防剧透 | prompt 警告不可靠，信息物理隔离才可靠 |
| 2026-05-12 | Writer 约束采用 60/20/20 法则 | 负向约束过多导致"防御性写作"，正向锚定为主 |
| 2026-05-12 | Auditor 拆为 Layer 1 规则 + Layer 2 语义 | 规则检测零 LLM 调用，大幅省 token |
| 2026-05-12 | Patch 从段落级改为 span 级微创 | 整段重写会丢失原文锐度 |
| 2026-05-12 | build_packet.py 升级为核心编译器 | 承担信息隔离 + 揭示预算 + 技能路由三重职责 |
