# 踩坑经验

> 记录开发过程中遇到的问题、原因分析和解决方案。

---

## L001: 中文目录名在 Python Path 中匹配失败

**日期**：2026-05-12
**阶段**：build_packet.py
**现象**：`pov_character_public` 和 `pov_character_voice` 输出为空
**原因**：`pov.lower().replace(" ", "_")` 对中文角色名（如"刘得宜"）生成的路径无法匹配拼音目录名（如 `liu_deyi`）
**解决**：添加 `name_map` 映射表，将中文名映射到拼音目录名
**预防**：项目约定角色目录名用拼音，脚本中维护中文→拼音映射

---

## L002: reveal_ledger.yaml YAML 格式错误

**日期**：2026-05-12
**阶段**：build_packet.py
**现象**：`yaml.scanner.ScannerError: mapping values are not allowed here`
**原因**：第一条 `- id:功法_正宗性` 冒号后缺少空格
**解决**：改为 `- id: 功法_正宗性`
**预防**：YAML 冒号后必须有空格，写完用 `python -c "import yaml; yaml.safe_load(open(...))"` 验证

---

## L003: mimo-v2.5 API 返回 ThinkingBlock

**日期**：2026-05-12
**阶段**：所有脚本
**现象**：`response.content[0].text` 报错 `'ThinkingBlock' object has no attribute 'text'`
**原因**：mimo-v2.5 模型会在回复前先输出思考过程（ThinkingBlock），实际文本在 TextBlock 中
**解决**：遍历 `response.content`，找到第一个有 `text` 属性的 block
**预防**：所有 LLM 调用处统一使用 helper 函数提取文本

---

## L004: Patch Agent 无法修复剧透类问题

**日期**：2026-05-12
**阶段**：run_patch.py
**现象**：Layer 2 审计发现 2 个 critical 剧透问题（玉之灵揭示了功法中期/远期目标、提前展示了金丹雏形），Patch agent 反复报告"无法定位问题文本"
**原因**：剧透不同于黑词——黑词是精确匹配的字符串，而剧透是一大段语义信息分散在多个句子中。`find_span_context` 基于关键词定位，对"一段信息是否构成剧透"这种语义判断无能为力。
**解决**：尚未彻底解决。临时方案是降低 Layer 2 剧透类 issue 的 action 为 `flag`（仅标记不自动修复），由人工处理。
**架构启示**：防剧透的正确防线是 **Writer 阶段的信息隔离**（reveal_ledger + packet 过滤），而非事后修补。如果 Writer 生成了剧透，说明 packet 信息泄露或模型未遵循约束——应该排查上游，而不是在 Patch 层打补丁。

---

## L005: Writer 模型对长列表约束遵循能力不足

**日期**：2026-05-12
**阶段**：run_writer.py
**现象**：packet 中携带了 5 条 forbidden_reveals（包含详细的禁止内容列表），但 Writer 仍然生成了接近完整剧透的文本
**原因**：mimo-v2.5 对长约束列表的遵循能力有限。当禁止揭示内容较多时，Writer 可能"忘记"或"忽略"部分约束。60/20/20 法则中 20% 的铁律区被其他规则挤占，剧透约束权重不足。
**解决方向**：
1. 在 system prompt 中将 forbidden_reveals 放在最前、最醒目的位置
2. 将剧透约束从"列表项"改为"硬性检查"：Writer 完成后用 LLM 检查是否触犯
3. 考虑对关键剧透使用"负样本"：在 few-shot 中展示"含剧透的错误写法"和"不含剧透的正确写法"对比

---

## L006: update_state.py 只记录历史，不演进角色状态

**日期**：2026-05-12
**阶段**：update_state.py
**现象**：3 章连续更新后，state.json 的 `emotional_state`、`current_goal`、`known_facts`、`relationships` 全部不变，只有新增的 `state_history` 数组在增长
**原因**：当前实现只做 append 操作——把 state_delta 的 from/to 写入历史记录，不修改任何实际状态字段
**影响**：Writer 在后续章节中读到的 state.json 与第 1 章完全一致，跨章状态连贯性无法体现
**解决方向**：需要 LLM 介入的状态演进——读终稿 + 旧 state + delta，让 LLM 输出更新后的完整 state.json（类似 diff+merge）

---

## L007: run_planner.py YAML 解析需去除 markdown 围栏

**日期**：2026-05-12
**阶段**：run_planner.py
**现象**：LLM 输出的 YAML 被 ` ```yaml ``` ` 包裹，`re.split(r"---+")` 无法正确分割
**原因**：mimo-v2.5 在回复中习惯用 markdown 代码围栏包裹结构化内容
**解决**：在 split 前先用 `re.sub` 去除 ` ```yaml ``` ` 和 ` ```yml ``` ` 围栏
**预防**：所有 LLM 输出 YAML 的地方都应做围栏清理

---

## L008: run_planner.py 生成数量不足且场景编号幻觉

**日期**：2026-05-12
**阶段**：run_planner.py
**现象**：prompt 要求 2-4 个场景合同，但 LLM 只输出 1 个；scene_id 幻觉为 s03（而非从 s01 开始）
**对比**：手动创建的 s01 合同包含 3 条 must_happen（简洁直接），自动生成的合同包含 4 条更细致的 plot nuance
**质量评估**：自动生成的合同在"叙述者语气"和"微妙关系"方面优于手动版本，但场景拆分能力不足
**解决方向**：
1. prompt 中强调"必须拆分为至少 2 个场景"
2. 要求 LLM 先输出场景列表概览，再逐个展开
3. 强制 scene_id 编号规则：`{chapter_id}_s01`, `_s02`...

---

## L009: reveal_ledger 与 chapter_intent 存在结构性冲突

**日期**：2026-05-13
**阶段**：intent 提取 + reveal_ledger
**现象**：ch002 的 intent 要求 must_include "核反应目标"和"金丹远景"，但 reveal_ledger 禁止在 ch20/ch30 前揭示这些信息。Writer 收到矛盾约束，无法同时满足
**原因**：intent 从原文逐字提取了 must_include 内容，但未检查 reveal_ledger 的揭示时间表。原文在这些章节确实揭示了这些信息，但小说整体弧线将这些揭示安排在更后面的章节
**解决**：build_packet.py 增加 intent → reveal_ledger 交叉检查，在 packet 编译阶段自动发现冲突并报错

---

## L010: intent 提取的信息密度是整个流水线的瓶颈

**日期**：2026-05-13
**阶段**：intent 提取
**现象**：ch001 的 intent 将原文 ~5800 字压缩为 5 条 must_include，丢失了原文最有价值的暗世界哲学论述（~1500 字）。AI writer 在没有这些信息的情况下，用氛围描写填充，结果是"好看但信息密度不足"
**对比**：ch003 的 intent 有 8 条 must_include，覆盖度高，AI 输出质量最好
**结论**：输入精简是设计目标，但过度精简会丢失原文的核心竞争力（信息密度）。需要在"人类可负担的输入量"和"信息保真度"之间找到平衡
**解决方向**：intent 提取 prompt 增强——要求提取"信息密度最高"的段落作为 must_include，而非只提取情节节拍
