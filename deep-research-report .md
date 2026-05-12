# CC/Codex+LLM 长篇小说工作流最佳建议

## 核心判断

如果你这里的 CC 指的是 Claude Code，那么我给你的最佳建议可以收敛成一句话：**把 CC/Codex 当成“编排器、检索器、状态更新器和验证器”，而不是直接承担最终正文风格的“作者”；把长篇小说系统做成“人类可编辑知识库 + 机器可校验状态层 + 按需检索 + 分阶段写作闭环”**。来自 entity["company","Anthropic","ai company"] 的 urlClaude Code 文档turn18view0 和来自 entity["company","OpenAI","ai company"] 的 urlCodex CLI 文档turn29view0 都把这类工具定义为能读项目、改文件、跑命令、接工具的 coding agent；你提供的几条开源路线里，真正提高长篇稳定性的也都不是“一条神 prompt”，而是结构化知识、阶段化流程和审计闭环。citeturn18view0turn29view0turn37search0turn14view0turn8view0turn12view0

直接回答你的四个问题：一，**信息管理不是纯 RAG，也不是纯 Markdown，而是“Markdown 为主、结构化状态为准、RAG 为辅”**；二，**渐进式 skills 非常值得做，但必须保证技能按需加载、描述互斥、优先级清楚，不要把 300 条写作规范一起塞进主 prompt**；三，**不要追求一次成文，也不要把“去 AI 味”全部押给最后一个润色 agent，而是用“章纲/场景 → 初稿 → 审计 → 定向修订 → 状态回写”的闭环**；四，**验证不要只测一段，而要测至少 3–5 个连续章节**，因为连续性、伏笔、状态漂移和文风失真都要跨章才会暴露。citeturn27view0turn14view0turn18view2turn19view1turn33view3turn37search0

还有一个很关键但常被忽略的点：**不要把 agent 自带 memory 当成小说事实库**。Claude Code 的 auto memory 只会在会话开始时装载 `MEMORY.md` 的前 200 行或 25KB，Codex 官方也明确说，必须始终生效的规则应该放在 `AGENTS.md` 或项目文档里，而不是 Memories 里。对长篇小说来说，memory 更适合存“偏好”和“经验”，不适合存“世界真相”。citeturn18view1turn30search2turn19view2turn35search4

## 从现有开源路线里真正该继承什么

你给的几个仓库，其实已经把路线图勾勒得很清楚了。

- urlCraft Companionturn9view0 最值得借的是它的 **Harness 思路**：入口分流、结构化知识库、五阶段工作流，以及对 Codex / Claude Code 的首推定位。它的目标不是“让 AI 一把写完”，而是让 AI 在稳定约束下协作，并把“执行层—评估层—仲裁层”拆开。citeturn10view0turn37search0
- urlInkOSturn13view0 最值得借的是 **真相文件 + JSON delta + 审计修订闭环**。它把长期记忆拆成 7 个 canonical truth files，又把权威来源从 Markdown 迁到 `story/state/*.json`，由代码层做 schema 校验和 immutable apply；同时把本章的 `intent`、`context`、`rule-stack`、`trace` 做成运行时产物。这条路线最接近“可工程化的长篇系统”。citeturn14view0turn32search2turn32search3
- urlAI Creatorturn11view0 最值得借的是 **世界观→小说→章节** 的层级、双层记忆，以及“主创作 agent 不直接搜 skills，而由独立推荐 agent 推荐技能”的分工。这恰好能避免主写作 agent 在正文创作时被技能选择噪音拖偏。citeturn12view0
- url稿匣turn7view0 最值得借的是 **本地优先**、`SQLite / FTS5 + embedding + rerank` 的混合检索路线，以及“计划—执行—预览—写回—历史”的可追溯链路。它说明长篇创作系统不需要把检索理解成“纯向量数据库”，关键词检索、结构化索引、rerank 完全应该共存。citeturn8view0
- urlAI_NovelGeneratorturn16view0 代表的是一条经典且依旧有价值的基线：**设定 → 目录 → 草稿 → 定稿 → 更新 summary / character state / vector store**。这条路线适合做最小闭环验证。但它当前 `dev` 分支的 README 也明确写着仍在重构、尚未完成，不应视为稳定版本，所以更适合作为“最小原型的参照”，不适合作为你最终架构的上限。citeturn17view0turn15view0

我的结论是：**你应该抄“模式”，不要抄“全家桶实现”**。最值得融合的，是 Craft Companion 的流程 discipline、InkOS 的事实层设计、稿匣的本地混合检索、AI Creator 的技能分治；最不该直接照搬的，是把所有能力一次性做成全功能桌面端。citeturn10view0turn14view0turn8view0turn12view0

## 小说信息管理的最优解

在 entity["company","Obsidian","note-taking software"] 的 url帮助文档turn27view3 里，properties 本质上就是文件顶部的 YAML，支持文本、列表、内部链接；内部链接既支持 wikilink 也支持 Markdown link，重命名时还能自动更新；Bases 又能直接基于本地 Markdown 和 properties 提供数据库式视图。所以，**用 Obsidian 的 `.md` 来做人类可编辑的知识管理层，是完全正确而且很适合你的路线**。它天然适合角色卡、地点卡、设定条目、章节摘要、关系网、伏笔板、作者意图等“要被人读、被人改、被链接”的内容。citeturn27view0turn27view1turn27view2turn28search4turn28search0

但我不建议把 `.md` 直接当成**唯一事实源**。最佳做法是四层分离：**第一层**是 Obsidian Markdown，给人看、给你手改；**第二层**是结构化 state，例如 `current_state.json`、`open_hooks.json`、`relationship_graph.json`、`resource_ledger.json`，作为机器唯一信源；**第三层**是检索层，用 FTS + embedding + rerank 去“找到要读什么”；**第四层**是本章 runtime package，只把当前章真正需要的事实、当前 POV 可知的信息、未闭合钩子、风格约束和局部示例编译到 `context.json` 里。这个分层和 InkOS 的 truth files / runtime artifacts、以及 Codex/Claude 对短而稳定的项目文档建议，是一致的。citeturn14view0turn32search2turn19view2turn18view1turn31search1turn31search0

你担心 `.md` 会提前披露未来信息，这个风险是真实存在的，但**不是 Markdown 的问题，而是“同一个文件同时承载现在态和未来态”的问题**。我的建议是把每个角色至少拆成三部分：`profile.md` 只写稳定信息和当前已知事实；`state.json` 只写机器要校验的当前状态；`future_arc.md` 只写作者知道但当前章节不该暴露的未来弧线。写第 N 章时，Writer 只能读 `revealed_until <= N` 的内容；Planner 可以有更高权限；Auditor 可以读全量，但只输出问题，不直接覆盖正文。这个访问控制可以通过 Codex / Claude Code hooks 在 agent 生命周期里做 deterministic 检查。citeturn18view3turn35search0turn35search5turn10view0turn14view0

所以我对“要不要 RAG”的答案是：**要，但 RAG 只做访问层，不做真相层**。而且不建议你把原始章节按固定 500–1000 token 生硬切块后直接向量检索；研究对比显示，长上下文和 RAG 各有 trade-off，**摘要式 retrieval 往往比 raw chunk retrieval 更接近长上下文效果，而 chunk-based retrieval 明显偏弱**；另一些研究还说明，哪怕 retrieval 是完美的，输入一旦太长，性能也会显著下降。更贴近长篇小说的检索单元应该是：**章节摘要、场景摘要、角色状态变化、关系边、未闭合伏笔、资源账本、POV 已知信息**，而不是原始大段正文。citeturn24view2turn34view2turn34view0turn25search0turn33view1turn33view2turn8view0

这也是为什么我不建议依赖“超长上下文把所有资料一次塞进去”。现在两条主流路线都已经提供了很长的窗口，但一方面，Claude 对 200k 以上输入有 long context pricing，GPT-5.4 对 272k 以上输入也会加价；另一方面，研究已经表明**上下文变长本身就可能伤害性能**。因此，长上下文应该被当成“兜底容量”，不是默认工作模式。真正省 token、也更稳的做法，是让静态前缀固定、动态内容后置，并利用两家的 prompt caching。citeturn23view5turn23view4turn36view0turn24view3turn34view0

一个足够稳的项目骨架，大概应该长这样：

```text
novel/
  AGENTS.md 或 CLAUDE.md
  bible/
    author_intent.md
    current_focus.md
    style_bible.md
    characters/
    locations/
    factions/
  state/
    current_state.json
    open_hooks.json
    relationship_graph.json
    resource_ledger.json
  chapters/
    ch001.md
    ch002.md
  summaries/
    chapter_summaries.md
    scene_summaries/
  runtime/
    ch012.intent.md
    ch012.context.json
    ch012.rule-stack.yaml
    ch012.trace.json
```

这个结构本质上是在吸收 InkOS 的 truth/runtime 分层、Craft Companion 的项目骨架，以及 Obsidian 的本地 Markdown 协作方式。citeturn14view0turn10view0turn27view0turn28search4

## 降低 AI 味的真正抓手

你提出的“skills 渐进式披露”方向，我认为是对的，而且和两家的官方能力非常对齐：Claude Code 和 Codex 都支持 skills，且都强调按需加载；Codex 还明确说明技能列表只会先放 name / description / path，完整 `SKILL.md` 只有在被选中时才加载，以避免把上下文挤爆；如果技能太多，初始列表甚至会被截断或省略一部分。换句话说，**渐进式披露不是可选项，而是必须的工程约束**。citeturn18view2turn19view1turn35search6

但你还没说出的隐患也很明确：**第一，技能描述重叠会导致路由歧义；第二，技能粒度太细会导致选择成本上升；第三，主 prompt 太长、太过程化，会把 prose 写得很机械**。OpenAI 的最新 prompt guidance 明确提醒，新的大模型更适合“短、结果导向、少流程噪音”的提示；把旧时代那种超长 process stack 原封不动搬过来，反而会让文本显得过度规整、机械、像模板。对小说来说，这正是“AI 味”的重要来源之一。citeturn24view5turn24view1turn19view1

所以，真正有效的去 AI 味，不是做一个泛化的“人味润色器”，而是做三层约束。**最上层**是非常短的 `style_bible.md`，只保留 5–15 条真正影响成文气质的硬规则，比如叙述视角、句长分布倾向、允许/禁用词域、比喻密度、对话的口语程度。**中间层**是场景技能，比如“写争执对话”“写压迫感空间”“写动作交代”“写冷幽默反应”，一次只加载一个。**最下层**是本场景局部证据：当前 POV、此刻已知事实、前一场景余波、1–2 段你认可的示例片段。这样模型面对的是“窄而具体”的风格任务，而不是“以统一笔法覆盖一切”。citeturn18view2turn19view1turn24view5turn14view0

另一个很关键的经验是：**技能应该更多地约束“写作决策”，而不是堆砌“华丽词藻要求”**。从你给的项目里看，AI Creator 把技能推荐从主写作 agent 里拆了出去，InkOS 把写作规则体系做成通用规则 + 题材规则 + 书级规则 + 当前任务意图的堆叠；这都说明成熟路线并不依赖一个“文采增强 prompt”，而是依赖更清楚的规则优先级。我的建议优先级是：**事实层与 POV 边界 > 本章意图 > 场景技能 > 语言风格 > 润色**。只要优先级反过来，AI 味几乎一定会变重。citeturn12view0turn14view0

最后，**去 AI 味最有效的不是“全文重写”，而是“定向修订”**。`Self-Refine` 这类工作已经说明，LLM 的“先出稿、再给反馈、再迭代修订”通常优于一遍成文。对小说来说，最合适的修订器不是一个“大润色 agent”，而是 3–5 个很窄的 reviser：只抓“抽象总结过多”“对话人声不分”“感官细节脱离 POV”“段落节奏过齐”“情绪只说不演”。这类局部修订既更稳，也不容易把文本洗成同一种腔调。citeturn33view3

## 我建议的写作流水线

我不建议你在正文生成时追求“一次成文”；也不建议你只让写作 agent 负责把细纲写成文，再交给一个大而全的润色 agent 统一去 AI 味。**最佳路线是“多阶段但不多余”的最短闭环**：

1. **章级规划**：输入卷纲、当前焦点、未闭合伏笔、本章 must-keep / must-avoid，生成 `intent.md` 和 3–7 个 scene beats。  
2. **上下文编译**：从 state、summary、hook、角色关系、POV 已知边界里检索，生成紧凑的 `context.json`，不要把整部书灌进 prompt。  
3. **分场景初稿**：一次只写一个 scene，而不是一口气写整章；每个 scene 完成后立即做局部自查。  
4. **事实抽取与状态回写**：让 Observer/Updater 输出 JSON delta，而不是重写整份角色档案。  
5. **连续性审计**：对照 canonical state、open hooks、chapter summaries 和 POV 边界，标记 `confirmed / disputed / dismissed`。  
6. **定向修订**：只修 disputed 段落；关键问题清零后再决定是否做轻量风格 polish。  
7. **人工门控**：确认后写回章节、更新摘要、更新索引。  

这套流程本质上融合了 Craft Companion 的五阶段协作、InkOS 的审计/修订/状态更新，以及 AI_NovelGenerator 的“定稿时更新 summary / state / vector store”的经典 baseline。对于机器输出的 state，我建议直接用 Structured Outputs 保 schema，不要靠 prompt 祈祷它 JSON 永远合法。citeturn37search0turn14view0turn17view0turn31search1turn31search0

真正落实到 CC/Codex+LLM 的分工上，我建议这样切：**CC/Codex 负责读文件、跑脚本、编排子任务、触发 hooks、更新状态、做批量检查；Writer 模型负责 scene prose；Auditor 模型负责逻辑、连续性、信息边界；State Updater 只负责结构化 delta；人类保留最终 gate**。这样你就把“写得好”和“写得对”拆开了。前者是 prose quality，后者是 system quality；这两者如果交给同一个 agent 同一轮 prompt，同步完成的稳定性通常不高。citeturn18view0turn29view0turn14view0turn19view4

在控制面上，项目级 `AGENTS.md` / `CLAUDE.md` 要尽量短，只放稳定约束、目录说明、状态层定义、写作阶段协议和禁令；细分的写人/写事/写景/动作/悬念/群像/对白等规范，全部下沉到 skills。Codex 官方建议 `AGENTS.md` 保持简洁，Claude 也强调 skills 的正文只在使用时加载；同时，Codex 和 Claude Code 都支持 hooks，因此你完全可以在 PreToolUse 或等价阶段做“防剧透读文件检查”“schema 校验”“只允许写当前章节”“禁止直接覆盖未来弧线文件”等确定性策略。citeturn19view2turn35search4turn18view2turn18view3turn35search0turn35search5

在 token 和成本上，我建议三条硬原则。第一，**静态前缀前置，动态信息后置**，让 prompt caching 真正生效；两家的官方文档都强调缓存命中依赖稳定前缀。第二，**默认用 summary/state/hook 做检索单位，不拿 raw chapter 做主检索单位**。第三，**subagents 只用于研究、审计和批量检查，不要每写一个 scene 都并行起一堆子代理**，因为 Codex 官方明确写了 subagent 会消耗更多 token。citeturn24view3turn36view0turn19view0turn34view0turn34view2

## 路线验证与最终取舍

验证阶段，我更建议你先拿**已有风格、已有事实边界的材料**做，而不是从全新脑洞直接开跑。原因很简单：如果从零开始，你测出来的是“创意生成 + 设定搭建 + 长篇连贯性”的混合结果，变量太多；如果你拿一段自己认可的细纲，或者拿 3–5 个连续章节做导入，你就能更准确地测“系统有没有稳住事实、节奏和文风”。Craft Companion 已经把“从零开始”和“导入已有小说”视为两条入口；AI_NovelGenerator 也提供了非常清晰的阶段式基线，因此你完全可以把“导入已有材料做连续章节验证”当成第一性测试。citeturn37search0turn17view0

具体比较时，不要只看“这段是不是好看”，而要看三类指标：**连续性指标**，比如人物认知边界是否穿帮、物品状态是否对得上、伏笔有没有被错误关闭；**文本指标**，比如抽象叙述占比、重复句式、相邻段落节奏同构、对话区分度；**生产指标**，比如每章 token、每次人工改动比例、每章 debug 次数。拿这三类指标去比较三条管线：一遍出稿；出稿后整章大润色；以及我上面推荐的“规划—上下文编译—分场景初稿—审计—定向修订”。如果你的目标是“减少 AI 味，同时保住长篇稳定性”，第三条路线大概率会是总体最优。这个判断既符合现有开源项目的收敛，也符合迭代修订优于单步生成的研究结论。citeturn14view0turn33view3turn37search0

最终取舍上，我的建议非常明确：**最佳路线不是更大的 prompt，而是更窄的运行时上下文；不是更重的 RAG，而是更硬的 canonical state；不是更万能的“润色 agent”，而是更细的缺陷审计与定向修订；不是把 CC/Codex 当作者，而是把它们当长篇系统的控制台。** 你真正要做出来的，不是“会写小说的聊天框”，而是“能长期维护小说真相、逐章稳定输出、并且允许你随时接管”的创作工作流。citeturn18view0turn29view0turn14view0turn10view0turn8view0