# 基于您的需求，我将从六个核心维度构建完整的技术路线调研框架，为CC/codex +LLM撰写长篇小说提供系统性的解决方案。

基于您的需求，我将从六个核心维度构建完整的技术路线调研框架，为 CC/codex +LLM 撰写长篇小说提供系统性的解决方案。

## 一、开源写作工具评估与集成分析

### 1.1 核心开源工具深度分析

**AI Creator 技术架构与功能评估**

AI Creator 作为您提供的核心参考工具，展现出了强大的长篇小说创作能力。该系统采用模块化的 AI Agent 架构，内置 391 + 个写作 Skill，涵盖了网文创作的各个维度。其核心优势在于通过 "设定管理 + 智能续写 + 语义搜索 + 双层记忆" 的组合机制，有效解决了 LLM 在长篇创作中的失忆问题。

在功能实现层面，AI Creator 具备以下核心能力：**设定管理**功能支持通过对话创建、编辑、查询角色和世界观条目，支持重要性分级和多维度描写；**智能续写**能够自动获取当前章节及前两章上下文，分析叙事风格并保持一致性续写；**语义搜索**通过向量语义匹配结合正则回退，实现跨角色、世界观、草稿、章节全库检索；**双层记忆系统**包含世界观级（跨小说共享）和小说级（单部作品）记忆，自动注入对话上下文。

从技术架构角度看，AI Creator 采用 "世界观→小说→章节" 的数据层级设计，一个世界观下可挂载多部小说，每部小说包含有序章节。角色、世界观设定、草稿和记忆归属于世界观层，可跨小说共享。这种设计确保了数据的结构化管理和高效复用。

**NovelForge 长篇创作引擎分析**

NovelForge 作为另一个重要的开源工具，围绕四大核心理念构建：模块化的 "卡片"、可自定义的 "动态输出模型"、灵活的 "上下文注入" 与保证一致性的 "知识图谱"[(16)](https://github.com/zskaitocn/NovelForge/blob/main/README.md)。其技术栈包括前端 Electron+Vue 3+TypeScript，后端 FastAPI+SQLModel，数据库采用 SQLite（核心数据）和 Neo4j（知识图谱）。

NovelForge 的**动态输出模型**基于 Pydantic 构建，用户可通过可视化界面自由定义创作元素（角色、场景、大纲）的结构，AI 生成时会进行强制校验确保输出格式精确。**上下文注入功能**通过简单的 @语法，可将项目中的任何卡片、字段、集合按需注入到提示词中，支持复杂的检索表达式。

**其他相关工具概览**

除了上述两个核心工具，调研范围内还有多个值得关注的开源项目。文枢（WenShape）是一个面向中长篇小说创作的智能体系统，采用 "orchestrator + agents + context\_engine + storage" 架构，项目数据存储在 YAML、Markdown、JSONL 等纯文本格式中，天然支持 Git 版本控制[(35)](https://github.com/unitagain/WenShape/blob/main/README.md)。

INKOS 作为 AI 驱动的网络小说全链路创作引擎，采用多 Agent 协作架构，具备自动构建世界观、章节级创作带自检表等功能。这些工具在技术实现上各有特色，为构建通用写作工具流提供了丰富的参考。

### 1.2 优势与不足对比分析

**现有工具的共同优势**

通过对比分析，这些开源工具展现出以下共同优势：



1. **长篇一致性保障**：多数工具都采用了某种形式的记忆机制或知识图谱技术，能够在几十万字的创作过程中保持人物设定、情节逻辑的一致性[(16)](https://github.com/zskaitocn/NovelForge/blob/main/README.md)。

2. **模块化设计**：采用模块化架构，支持功能的灵活组合和扩展，如 AI Creator 的 Skill 系统和 NovelForge 的卡片系统。

3. **多模型支持**：都具备对多种 LLM 供应商的支持能力，包括 OpenAI、Anthropic、Google 等，部分还支持自定义兼容接口。

4. **结构化数据管理**：采用结构化方式管理角色、世界观、情节等信息，支持高效的检索和复用[(35)](https://github.com/unitagain/WenShape/blob/main/README.md)。

**各工具的差异化优势**

AI Creator 的独特优势在于其**内置的 391 + 个写作 Skill**，这些经过打磨的 prompt 模板涵盖了网文创作的各种方法论，如开篇钩子、反派塑造、爽点设计等。NovelForge 的优势则体现在其**强大的知识图谱集成**，通过 Neo4j 数据库构建人物关系网络，能够自动或手动提取文本中的人物关系与动态信息。

文枢的特色在于其**纯文本存储和版本控制支持**，所有项目数据以 yaml/markdown/jsonl 格式存储，天然适合 Git 版本控制，这对于需要长期维护的长篇项目尤为重要[(35)](https://github.com/unitagain/WenShape/blob/main/README.md)。

**存在的共性问题**

尽管这些工具都具备较强的功能，但仍存在一些共性问题：



1. **AI 味控制不足**：多数工具在生成内容的 "人性化" 方面缺乏有效机制，生成的文本往往带有明显的 AI 痕迹[(9)](http://m.toutiao.com/group/7637450621221618202/?upstream_biz=doubao)。

2. **对特定 LLM 的依赖**：虽然支持多模型，但在实际使用中仍可能存在对特定模型的优化倾向，影响通用性。

3. **学习成本较高**：复杂的功能设计和配置要求较高的技术门槛，对于普通创作者可能存在学习难度。

4. **性能和成本考虑**：在处理长篇内容时，token 消耗和响应时间可能成为制约因素。

### 1.3 工具流集成建议

基于上述分析，建议采用 \*\*"核心工具 + 插件扩展"\*\* 的集成策略：

**主工具选择建议**

对于长篇小说创作，建议以**AI Creator**作为核心创作工具，因其内置的丰富 Skill 库能够直接应用于网文创作场景。同时集成**NovelForge**的知识图谱功能，通过 Neo4j 数据库增强人物关系和情节逻辑的管理能力。

**技术集成方案**



1. **数据层集成**：采用文枢的纯文本存储方案，将所有项目数据以标准化格式存储，确保版本控制和数据迁移的便利性[(35)](https://github.com/unitagain/WenShape/blob/main/README.md)。

2. **功能层集成**：保留 AI Creator 的 Skill 系统作为创作方法论支撑，集成 NovelForge 的动态输出模型确保格式一致性，整合文枢的编排式写作流程提升创作效率[(35)](https://github.com/unitagain/WenShape/blob/main/README.md)。

3. **接口层设计**：构建统一的 LLM 接口抽象层，支持 OpenAI、Anthropic、Google 等主流供应商，以及自定义兼容接口，确保不依赖特定 LLM。

**扩展能力规划**

在现有工具基础上，建议增加以下扩展功能：



1. **AI 味控制插件**：集成专门的去 AI 味处理模块，通过风格迁移和人工审核机制提升文本的人性化程度[(58)](https://blog.csdn.net/charles666666/article/details/147967816)。

2. **多模态支持**：扩展对图片、音频等多模态内容的支持，为小说创作提供更丰富的素材来源。

3. **协作编辑功能**：增加团队协作支持，允许多个创作者同时编辑同一项目，通过权限控制确保数据安全。

## 二、通用技术路线探索与架构设计

### 2.1 不依赖特定 LLM 的工具流架构

**分层抽象架构设计**

构建不依赖特定 LLM 的通用写作工具流，核心在于采用分层抽象的架构设计。建议采用**四层抽象架构**：



1. **模型抽象层**：构建统一的 LLM 接口规范，定义标准的调用方法、参数格式和返回结果结构。通过适配器模式支持不同供应商的 LLM 服务，包括 OpenAI、Anthropic、Google Gemini 等主流服务，以及本地部署的模型如 LLaMA、GPTQ 等。

2. **功能服务层**：将写作相关功能封装为独立的服务模块，包括文本生成、内容润色、风格转换、一致性检查等。每个服务模块通过标准化接口对外提供服务，不依赖特定的实现方式[(41)](https://www.cnblogs.com/clarance/p/20011455)。

3. **业务逻辑层**：实现具体的创作流程逻辑，如大纲生成、章节写作、角色管理、情节推进等。这一层基于功能服务层构建，通过组合不同的服务实现复杂的创作场景。

4. **用户接口层**：提供统一的用户交互界面，支持 Web、桌面应用、移动端等多种访问方式。界面设计应符合创作者的使用习惯，提供简洁高效的操作体验。

**模块化服务设计**

基于微服务架构理念，将系统拆分为多个独立的服务模块，每个模块负责特定的功能领域：



1. **内容生成服务**：负责文本内容的生成，支持多种生成策略和参数配置。该服务应具备流式输出能力，能够实时返回生成结果。

2. **内容处理服务**：提供文本的编辑、润色、格式转换等功能。包括语法检查、拼写纠正、风格优化、段落重组等操作[(41)](https://www.cnblogs.com/clarance/p/20011455)。

3. **知识管理服务**：负责角色设定、世界观构建、情节线索等知识内容的存储和检索。采用结构化方式管理知识，支持高效的查询和更新操作[(51)](https://blog.csdn.net/weixin_42538175/article/details/160641108)。

4. **工作流管理服务**：协调各个服务之间的调用流程，实现从创作需求到最终输出的完整工作流。支持流程的定制化配置和状态跟踪[(35)](https://github.com/unitagain/WenShape/blob/main/README.md)。

### 2.2 技术栈选择与实现路径

**核心技术栈推荐**

基于当前技术发展趋势和开源生态成熟度，建议采用以下技术栈：



1. **后端服务**：使用**FastAPI**作为主要框架，基于 Python 实现，具备高性能和良好的类型支持。采用异步处理模式，能够高效处理并发请求。

2. **前端应用**：使用**Vue 3 + TypeScript**构建 Web 应用，采用 Electron 打包为桌面应用。这种组合提供了良好的开发体验和跨平台支持。

3. **数据库设计**：采用**混合存储策略**，核心结构化数据使用 PostgreSQL 或 MySQL，非结构化文本内容使用 MongoDB，图结构数据使用 Neo4j 构建知识图谱。

4. **消息队列**：集成**Redis**或**RabbitMQ**作为消息中间件，支持异步任务处理和服务间通信，提升系统的可扩展性和可靠性[(41)](https://www.cnblogs.com/clarance/p/20011455)。

**关键技术实现方案**



1. **LLM 接口抽象实现**：

构建统一的 LLM 客户端接口，定义标准的请求和响应格式：



```
class BaseLLMClient:

&#x20;   def \_\_init\_\_(self, model\_config: dict):

&#x20;       self.model\_config = model\_config

&#x20;  &#x20;

&#x20;   async def generate(self, prompt: str, parameters: dict) -> str:

&#x20;       """生成文本内容"""

&#x20;       raise NotImplementedError

&#x20;  &#x20;

&#x20;   async def chat(self, messages: list, parameters: dict) -> str:

&#x20;       """多轮对话交互"""

&#x20;       raise NotImplementedError

&#x20;  &#x20;

&#x20;   async def embedding(self, text: str) -> list:

&#x20;       """生成文本嵌入向量"""

&#x20;       raise NotImplementedError
```

针对不同的 LLM 供应商实现具体的适配器：



```
class OpenAIClient(BaseLLMClient):

&#x20;   def \_\_init\_\_(self, model\_config: dict):

&#x20;       super().\_\_init\_\_(model\_config)

&#x20;       self.client = openai.OpenAI(api\_key=model\_config\["api\_key"])

&#x20;  &#x20;

&#x20;   async def generate(self, prompt: str, parameters: dict) -> str:

&#x20;       response = await self.client.chat.completions.create(

&#x20;           model=self.model\_config\["model"],

&#x20;           messages=\[{"role": "user", "content": prompt}],

&#x20;           \*\*parameters

&#x20;       )

&#x20;       return response.choices\[0].message.content
```



1. **模块化服务实现**

以内容生成服务为例，实现模块化的生成逻辑：



```
class ContentGenerationService:

&#x20;   def \_\_init\_\_(self, llm\_client: BaseLLMClient):

&#x20;       self.llm\_client = llm\_client

&#x20;  &#x20;

&#x20;   async def generate\_chapter(self, chapter\_spec: dict) -> dict:

&#x20;       """生成章节内容"""

&#x20;       prompt = self.\_build\_chapter\_prompt(chapter\_spec)

&#x20;       content = await self.llm\_client.generate(prompt, chapter\_spec\["parameters"])

&#x20;       return {"content": content, "status": "success"}

&#x20;  &#x20;

&#x20;   def \_build\_chapter\_prompt(self, chapter\_spec: dict) -> str:

&#x20;       """构建章节生成提示词"""

&#x20;       \# 整合角色设定、情节背景、风格要求等信息

&#x20;       prompt = f"创作第{chapter\_spec\['chapter\_number']}章：{chapter\_spec\['title']}\n"

&#x20;       prompt += f"背景设定：{chapter\_spec\['context']}\n"

&#x20;       prompt += f"风格要求：{chapter\_spec\['style']}\n"

&#x20;       prompt += f"字数要求：{chapter\_spec\['word\_count']}字\n"

&#x20;       return prompt
```

### 2.3 可扩展性与兼容性设计

**插件化扩展机制**

为确保系统的可扩展性，建议实现**插件化架构**：



1. **插件接口规范**：定义统一的插件接口，包括初始化方法、功能调用方法、配置管理方法等。插件应能够独立开发、测试和部署[(43)](https://github.com/KeatonLi/prompt-flow-craft/blob/main/README.md)。

2. **动态加载机制**：实现插件的动态加载和卸载功能，支持在系统运行过程中添加或删除插件。通过配置文件指定启用的插件列表[(43)](https://github.com/KeatonLi/prompt-flow-craft/blob/main/README.md)。

3. **服务发现机制**：采用服务注册和发现机制，插件可以自动注册其提供的服务，其他模块可以通过标准接口发现和调用这些服务[(41)](https://www.cnblogs.com/clarance/p/20011455)。

**跨平台兼容性设计**

为确保系统在不同平台上的稳定运行，需要考虑以下兼容性因素：



1. **操作系统兼容性**：通过使用跨平台的开发框架和工具链，确保系统能够在 Windows、macOS、Linux 等主流操作系统上运行。

2. **Python 版本兼容性**：建议使用 Python 3.10 及以上版本，确保语言特性的一致性和库的兼容性[(35)](https://github.com/unitagain/WenShape/blob/main/README.md)。

3. **数据库兼容性**：设计数据库访问层时，应考虑不同数据库系统的语法差异，通过 ORM 工具或统一的查询接口屏蔽这些差异。

4. **网络协议兼容性**：采用标准的网络协议和数据格式，如 HTTP/2、gRPC、JSON 等，确保不同组件之间的通信兼容性[(41)](https://www.cnblogs.com/clarance/p/20011455)。

## 三、RAG 技术在小说信息管理中的应用

### 3.1 RAG 技术架构与实现方案

**RAG 核心技术原理**

检索增强生成（RAG）技术通过在 LLM 生成文本前，先从外部知识库中检索相关信息并融入生成过程，有效解决了 LLM 的静态知识局限、幻觉问题和领域专业性不足等核心问题[(53)](https://github.com/guoliwei2333/all-in-rag/blob/main/docs/chapter1/01_RAG_intro.md)。在小说创作场景中，RAG 技术能够确保 AI 在处理几十万字的长篇内容时，仍能准确记忆早期设定和情节线索。

RAG 系统的核心架构包括三个关键组件：**索引组件**将非结构化文档分割为片段，通过嵌入模型转换为向量数据；**检索组件**基于查询语义从向量数据库召回最相关的文档片段；**生成组件**将检索结果作为上下文输入 LLM 生成自然语言响应[(53)](https://github.com/guoliwei2333/all-in-rag/blob/main/docs/chapter1/01_RAG_intro.md)。

**小说创作专用 RAG 架构设计**

针对小说创作的特殊需求，建议构建**三层 RAG 架构**：



1. **基础层 RAG**：处理通用的写作知识和技巧，包括写作方法论、修辞手法、情节结构等。这一层使用公开的文学知识库和写作指南构建[(53)](https://github.com/guoliwei2333/all-in-rag/blob/main/docs/chapter1/01_RAG_intro.md)。

2. **领域层 RAG**：针对特定类型小说的专业知识，如玄幻小说的修炼体系、科幻小说的科技设定、历史小说的时代背景等。这一层需要根据创作类型动态构建。

3. **项目层 RAG**：管理当前创作项目的专有信息，包括角色设定、世界观构建、情节发展、伏笔线索等。这是 RAG 系统的核心部分，直接影响创作的一致性和质量[(51)](https://blog.csdn.net/weixin_42538175/article/details/160641108)。

**向量数据库选型与配置**

在向量数据库选择方面，建议采用**混合存储策略**：



1. **主存储数据库**：使用**Milvus**作为主要的向量数据库，因其具备高性能、可扩展性和丰富的查询功能，特别适合处理大规模向量数据[(53)](https://github.com/guoliwei2333/all-in-rag/blob/main/docs/chapter1/01_RAG_intro.md)。

2. **辅助数据库**：使用**FAISS**作为轻量级向量搜索库，用于处理实时性要求较高的小规模查询，如角色属性查询、情节片段检索等[(53)](https://github.com/guoliwei2333/all-in-rag/blob/main/docs/chapter1/01_RAG_intro.md)。

3. **图数据库集成**：使用**Neo4j**构建人物关系图谱，专门处理复杂的角色关系和情节关联查询。这对于维护长篇小说的逻辑一致性至关重要。

### 3.2 角色与情节信息管理方案

**结构化信息模型设计**

为了有效管理长篇小说的复杂信息，需要构建**层次化的信息模型**：



1. **角色信息模型**：



```
{

&#x20; "角色ID": {

&#x20;   "基本信息": {

&#x20;     "姓名": "林墨",

&#x20;     "年龄": 18,

&#x20;     "性别": "男",

&#x20;     "身份": "修仙者"

&#x20;   },

&#x20;   "性格特征": {

&#x20;     "主要性格": \["坚韧", "善良", "机智"],

&#x20;     "次要性格": \["内向", "执着"],

&#x20;     "性格演变": "从平凡少年成长为一代宗师"

&#x20;   },

&#x20;   "能力设定": {

&#x20;     "修为境界": "筑基期",

&#x20;     "主要功法": "太虚诀",

&#x20;     "特殊技能": \["御剑飞行", "炼丹术"],

&#x20;     "法宝": \["青云剑", "乾坤袋"]

&#x20;   },

&#x20;   "关系网络": {

&#x20;     "亲人": \["父亲:林远山", "母亲:苏婉"],

&#x20;     "朋友": \["陈昊", "李清雪"],

&#x20;     "敌人": \["魔宗长老"],

&#x20;     "重要关系": {

&#x20;       "李清雪": "青梅竹马，后成为道侣"

&#x20;     }

&#x20;   },

&#x20;   "经历轨迹": \[

&#x20;     "第1章：觉醒灵根，拜入青云门",

&#x20;     "第5章：在试炼中救下落难的李清雪",

&#x20;     "第10章：发现魔宗阴谋，开始成长"

&#x20;   ]

&#x20; }

}
```



1. **情节信息模型**：



```
{

&#x20; "情节ID": {

&#x20;   "标题": "魔宗入侵",

&#x20;   "类型": "主线情节",

&#x20;   "章节范围": "第20-25章",

&#x20;   "关键事件": \[

&#x20;     "魔宗大举进攻青云门",

&#x20;     "掌门牺牲自己封印魔宗宗主",

&#x20;     "主角获得掌门传承",

&#x20;     "李清雪为救主角身负重伤"

&#x20;   ],

&#x20;   "涉及角色": \["林墨", "李清雪", "掌门", "魔宗宗主"],

&#x20;   "伏笔线索": \[

&#x20;     "掌门遗言暗示主角身世",

&#x20;     "魔宗宗主并未完全被封印",

&#x20;     "李清雪的伤势需要特殊丹药才能治愈"

&#x20;   ],

&#x20;   "情节影响": {

&#x20;     "角色成长": "主角突破到金丹期",

&#x20;     "关系变化": "主角与李清雪感情加深",

&#x20;     "世界观影响": "修仙界格局发生变化"

&#x20;   }

&#x20; }

}
```

**智能检索与查询机制**

为了实现高效的信息检索，需要设计**多维度的查询策略**：



1. **语义检索**：基于向量相似度匹配，支持模糊查询和语义理解。例如查询 "主角的青梅竹马" 时，能够准确返回李清雪的相关信息[(53)](https://github.com/guoliwei2333/all-in-rag/blob/main/docs/chapter1/01_RAG_intro.md)。

2. **结构化查询**：支持基于属性的精确查询，如 "查找所有金丹期以上的角色"、"列出第 10-20 章的所有战斗情节" 等[(51)](https://blog.csdn.net/weixin_42538175/article/details/160641108)。

3. **关系查询**：通过图数据库支持复杂的关系查询，如 "查找主角的所有敌人的敌人"、"找出与某事件相关的所有角色" 等。

4. **时间线查询**：支持按时间顺序检索情节发展，如 "查看主角在筑基期的所有重要事件"、"梳理某条伏笔线索的完整脉络" 等[(48)](https://blog.csdn.net/sanshanjianke/article/details/160587436)。

### 3.3 RAG 与传统.md 管理方式对比

**信息组织效率对比**



| 对比维度   | RAG 管理方式     | Markdown 管理方式 |
| ------ | ------------ | ------------- |
| 信息检索速度 | 毫秒级响应，支持语义查询 | 线性查找，速度较慢     |
| 信息关联能力 | 支持复杂关系查询和图遍历 | 简单的链接引用       |
| 信息一致性  | 自动校验和冲突检测    | 人工维护，易出错      |
| 信息更新效率 | 增量更新，局部修改    | 可能需要全局更新      |
| 信息复用能力 | 支持跨项目共享和引用   | 项目内有限复用       |

**功能特性对比分析**



1. **信息检索能力**：

* RAG 方式：通过向量检索和语义理解，能够快速找到相关信息，支持复杂的查询逻辑[(53)](https://github.com/guoliwei2333/all-in-rag/blob/main/docs/chapter1/01_RAG_intro.md)

* Markdown 方式：主要依靠文本搜索和链接跳转，查询能力有限，且容易遗漏相关信息

1. **一致性维护**：

* RAG 方式：通过知识图谱和自动校验机制，能够实时检测信息冲突和不一致性[(51)](https://blog.csdn.net/weixin_42538175/article/details/160641108)

* Markdown 方式：完全依赖人工维护，在长篇小说中很难保证所有设定的一致性

1. **创作辅助功能**：

* RAG 方式：能够在创作过程中自动推荐相关设定和情节线索，提供智能化的创作建议

* Markdown 方式：需要作者主动查找和引用相关信息，缺乏智能辅助功能

1. **版本控制支持**：

* RAG 方式：通过数据库事务和版本号管理，支持细粒度的版本控制和回滚

* Markdown 方式：可以利用 Git 进行版本控制，但对于结构化信息的管理不够精细[(35)](https://github.com/unitagain/WenShape/blob/main/README.md)

**信息披露风险分析**

关于您提到的信息提前披露风险，需要从以下几个方面进行分析：



1. **风险来源识别**：

* 角色设定文件可能包含后期才会揭示的背景信息

* 情节大纲可能暴露尚未展开的剧情发展

* 伏笔线索文件可能提前泄露关键悬念

1. **RAG 方式的风险控制**：

* **权限分级管理**：可以为不同类型的信息设置访问权限，如 "公开信息"、"作者可见"、"编辑可见" 等[(51)](https://blog.csdn.net/weixin_42538175/article/details/160641108)

* **动态加载策略**：根据创作进度动态加载相关信息，避免提前暴露后续内容

* **智能过滤机制**：在检索时自动过滤掉不应该在当前阶段出现的信息

1. **Markdown 方式的风险控制**：

* **文件分级存储**：将不同敏感程度的信息存储在不同目录，通过文件权限控制访问

* **手动引用控制**：作者在引用信息时需要谨慎选择，避免无意中暴露后续内容

* **版本隔离策略**：使用 Git 分支管理不同创作阶段的信息，避免早期版本包含后期内容

1. **风险评估结论**：

   RAG 方式在信息披露风险控制方面具有更大的优势，通过细粒度的权限控制和智能过滤机制，能够更有效地防止信息的不当披露。而 Markdown 方式虽然简单直接，但在风险控制方面主要依赖人工操作，存在较高的误操作风险。

## 四、AI 味控制与分层写作规范

### 4.1 AI 生成文本的问题诊断

**AI 味特征识别与分析**

AI 生成的文本通常具有以下明显特征，这些特征构成了所谓的 "AI 味"：



1. **语言风格问题**：

* 过度使用连接词和过渡短语，如 "值得注意的是"、"总而言之"、"从某种意义上说" 等[(63)](https://github.com/duongngo65yx-boop/De-AI-Prompt-Enhancer-Writer-Booster-SKILL/blob/main/%E5%8E%BBAI%E5%91%B3%E6%8F%90%E7%A4%BA%E8%AF%8D-%E4%BD%9C%E5%AE%B6%E5%A2%9E%E5%BC%BA-%E4%B8%AD%E7%AB%8B%E6%A8%A1%E5%BC%8F-SKILL.md)

* 句子结构过于规整，缺乏变化和节奏感

* 词汇选择偏向书面化和正式化，缺少口语化表达和个性化用词[(59)](http://m.toutiao.com/group/7529789402579517991/?upstream_biz=doubao)

1. **内容表达问题**：

* 分析浮于表面，经常使用 "-ing" 结尾的肤浅分析

* 喜欢使用夸张的象征意义和宣传性语言

* 缺乏真实情感和个人观点，显得过于中立和客观[(63)](https://github.com/duongngo65yx-boop/De-AI-Prompt-Enhancer-Writer-Booster-SKILL/blob/main/%E5%8E%BBAI%E5%91%B3%E6%8F%90%E7%A4%BA%E8%AF%8D-%E4%BD%9C%E5%AE%B6%E5%A2%9E%E5%BC%BA-%E4%B8%AD%E7%AB%8B%E6%A8%A1%E5%BC%8F-SKILL.md)

1. **逻辑结构问题**：

* 倾向于使用三段式结构：引言 - 正文 - 总结

* 段落长度过于均匀，缺乏变化

* 论证方式机械，喜欢使用 "首先、其次、最后" 等模式化表达[(63)](https://github.com/duongngo65yx-boop/De-AI-Prompt-Enhancer-Writer-Booster-SKILL/blob/main/%E5%8E%BBAI%E5%91%B3%E6%8F%90%E7%A4%BA%E8%AF%8D-%E4%BD%9C%E5%AE%B6%E5%A2%9E%E5%BC%BA-%E4%B8%AD%E7%AB%8B%E6%A8%A1%E5%BC%8F-SKILL.md)

1. **细节描写问题**：

* 描述过于概括，缺少具体细节

* 人物对话缺乏个性，显得千篇一律

* 环境描写公式化，缺乏独特视角[(9)](http://m.toutiao.com/group/7637450621221618202/?upstream_biz=doubao)

**长篇小说中 AI 味的特殊影响**

在长篇小说创作中，AI 味问题会产生以下特殊影响：



1. **角色塑造扁平化**：AI 生成的角色对话和行为模式容易趋同，导致角色缺乏个性和深度

2. **情节发展模式化**：故事走向容易陷入套路化，缺乏创新和意外性

3. **读者体验下降**：明显的 AI 痕迹会破坏阅读沉浸感，影响读者的代入感和情感共鸣[(9)](http://m.toutiao.com/group/7637450621221618202/?upstream_biz=doubao)

4. **商业价值降低**：在网文市场中，AI 味过重的作品很难获得读者认可和商业成功

### 4.2 分层写作规范设计

**写作任务分层架构**

基于认知写作理论，建议采用**四层分层架构**来规范 AI 写作：



1. **宏观结构层**（章节级）：

* 负责章节的整体结构设计和情节安排

* 约束条件：章节字数限制、情节发展要求、情感基调设定

* 输出要求：章节大纲、情节要点、人物出场安排[(67)](https://preview.aclanthology.org/fix-opsupmap-display/2025.findings-acl.511.pdf)

1. **中观段落层**（段落级）：

* 负责段落的逻辑组织和信息分布

* 约束条件：段落功能定位、信息密度控制、节奏变化要求

* 输出要求：段落主题句、支持论据、过渡衔接[(67)](https://preview.aclanthology.org/fix-opsupmap-display/2025.findings-acl.511.pdf)

1. **微观句子层**（句子级）：

* 负责句子的语法结构和表达效果

* 约束条件：句式变化要求、修辞手法运用、语言风格控制

* 输出要求：完整句子、语法正确、表达清晰[(67)](https://preview.aclanthology.org/fix-opsupmap-display/2025.findings-acl.511.pdf)

1. **词汇选择层**（词汇级）：

* 负责词汇的精准选择和搭配

* 约束条件：词汇风格要求、专业术语使用、口语化程度控制

* 输出要求：准确词汇、恰当搭配、避免重复[(67)](https://preview.aclanthology.org/fix-opsupmap-display/2025.findings-acl.511.pdf)

**分层约束机制设计**

为确保各层输出符合文学创作要求，需要设计**精细化的约束机制**：



1. **具体性约束**：

* 明确禁止使用特定表述，如 "禁用 ' 赋能 '' 闭环 ' 等术语"

* 设定数值限制，如 "形容词占比不超过 12%"

* 保留必要专业词汇，如允许 "卷积神经网络" 等术语[(58)](https://blog.csdn.net/charles666666/article/details/147967816)

1. **风格化约束**：

* 语言风格要求："采用口语化表达方式，避免书面化语言"

* 情感基调控制："保持轻松幽默的叙述风格，避免过于严肃"

* 修辞手法运用："适当使用比喻和拟人，但避免过度修饰"[(66)](https://devpress.csdn.net/avi/697f93cca16c6648a986abba.html)

1. **结构约束**：

* 段落长度控制："引言段限 80 字内，仅陈述核心结论"

* 句式变化要求："避免连续使用相同句式，保持长短句交替"

* 章节结构安排："每章包含 3-5 个主要段落，段落功能明确"[(64)](https://m.php.cn/faq/2138971.html)

1. **内容约束**：

* 主题范围限定："不得包含与主线无关的内容"

* 信息密度要求："每段必须包含至少一个核心信息点"

* 逻辑关系要求："段落间必须有明确的逻辑衔接"[(66)](https://devpress.csdn.net/avi/697f93cca16c6648a986abba.html)

**分层写作流程设计**

建议采用 \*\*"自上而下、逐层细化"\*\* 的写作流程：



1. **结构规划阶段**：

* 首先完成宏观结构层的设计，确定章节的整体框架

* 输出章节大纲和情节要点

* 时间分配：占总写作时间的 20%[(67)](https://preview.aclanthology.org/fix-opsupmap-display/2025.findings-acl.511.pdf)

1. **段落细化阶段**：

* 在结构框架基础上，细化每个段落的内容和逻辑

* 输出段落主题和支撑内容

* 时间分配：占总写作时间的 30%[(67)](https://preview.aclanthology.org/fix-opsupmap-display/2025.findings-acl.511.pdf)

1. **句子构建阶段**：

* 根据段落要求，逐句构建具体内容

* 重点关注句式变化和表达效果

* 时间分配：占总写作时间的 40%[(67)](https://preview.aclanthology.org/fix-opsupmap-display/2025.findings-acl.511.pdf)

1. **词汇优化阶段**：

* 对生成的文本进行词汇层面的优化

* 确保用词准确、风格统一

* 时间分配：占总写作时间的 10%[(67)](https://preview.aclanthology.org/fix-opsupmap-display/2025.findings-acl.511.pdf)

### 4.3 去 AI 味技术方案

**系统性去 AI 味策略**

基于 AI 写作特征分析，建议采用 \*\*"识别 - 修正 - 优化"\*\* 的系统性去 AI 味方案：



1. **AI 特征识别**：

* 使用基于规则的检测器识别 AI 味特征

* 建立 AI 特征词库和模式库

* 实时检测文本中的 AI 痕迹[(63)](https://github.com/duongngo65yx-boop/De-AI-Prompt-Enhancer-Writer-Booster-SKILL/blob/main/%E5%8E%BBAI%E5%91%B3%E6%8F%90%E7%A4%BA%E8%AF%8D-%E4%BD%9C%E5%AE%B6%E5%A2%9E%E5%BC%BA-%E4%B8%AD%E7%AB%8B%E6%A8%A1%E5%BC%8F-SKILL.md)

1. **自动修正机制**：

* 针对识别出的 AI 特征进行自动修正

* 包括替换模式化表达、调整句式结构、优化词汇选择等

* 提供多种修正方案供选择[(63)](https://github.com/duongngo65yx-boop/De-AI-Prompt-Enhancer-Writer-Booster-SKILL/blob/main/%E5%8E%BBAI%E5%91%B3%E6%8F%90%E7%A4%BA%E8%AF%8D-%E4%BD%9C%E5%AE%B6%E5%A2%9E%E5%BC%BA-%E4%B8%AD%E7%AB%8B%E6%A8%A1%E5%BC%8F-SKILL.md)

1. **人工审核流程**：

* 对自动修正后的文本进行人工审核

* 重点检查逻辑合理性、情感真实性、风格一致性

* 进行必要的人工调整和优化[(63)](https://github.com/duongngo65yx-boop/De-AI-Prompt-Enhancer-Writer-Booster-SKILL/blob/main/%E5%8E%BBAI%E5%91%B3%E6%8F%90%E7%A4%BA%E8%AF%8D-%E4%BD%9C%E5%AE%B6%E5%A2%9E%E5%BC%BA-%E4%B8%AD%E7%AB%8B%E6%A8%A1%E5%BC%8F-SKILL.md)

**具体技术实现方案**



1. **词汇层面优化**：

* 建立 "AI 高频词汇" 黑名单，如 "值得注意的是"、"总而言之"、"从某种意义上说" 等

* 使用同义词替换算法，将 AI 词汇替换为更自然的表达方式

* 增加口语化词汇和个性化表达的使用比例[(63)](https://github.com/duongngo65yx-boop/De-AI-Prompt-Enhancer-Writer-Booster-SKILL/blob/main/%E5%8E%BBAI%E5%91%B3%E6%8F%90%E7%A4%BA%E8%AF%8D-%E4%BD%9C%E5%AE%B6%E5%A2%9E%E5%BC%BA-%E4%B8%AD%E7%AB%8B%E6%A8%A1%E5%BC%8F-SKILL.md)

1. **句式结构调整**：

* 检测并打破 "三段式" 结构，避免机械的 "首先、其次、最后" 表达

* 增加句式变化，包括长短句交替、主动被动语态转换等

* 引入更多的疑问句式、感叹句式，增加语言的生动性[(63)](https://github.com/duongngo65yx-boop/De-AI-Prompt-Enhancer-Writer-Booster-SKILL/blob/main/%E5%8E%BBAI%E5%91%B3%E6%8F%90%E7%A4%BA%E8%AF%8D-%E4%BD%9C%E5%AE%B6%E5%A2%9E%E5%BC%BA-%E4%B8%AD%E7%AB%8B%E6%A8%A1%E5%BC%8F-SKILL.md)

1. **逻辑表达优化**：

* 避免过于规整的逻辑结构，增加一些 "不完美" 的表达

* 允许一些看似 "离题" 但能增加文章趣味性的内容

* 减少使用明确的逻辑连接词，让逻辑关系更加自然隐含[(63)](https://github.com/duongngo65yx-boop/De-AI-Prompt-Enhancer-Writer-Booster-SKILL/blob/main/%E5%8E%BBAI%E5%91%B3%E6%8F%90%E7%A4%BA%E8%AF%8D-%E4%BD%9C%E5%AE%B6%E5%A2%9E%E5%BC%BA-%E4%B8%AD%E7%AB%8B%E6%A8%A1%E5%BC%8F-SKILL.md)

1. **情感注入机制**：

* 在关键位置注入真实的情感表达，避免过于中立客观

* 增加第一人称观点表达，体现作者的主观感受

* 在适当位置加入幽默、讽刺、感慨等个性化表达[(63)](https://github.com/duongngo65yx-boop/De-AI-Prompt-Enhancer-Writer-Booster-SKILL/blob/main/%E5%8E%BBAI%E5%91%B3%E6%8F%90%E7%A4%BA%E8%AF%8D-%E4%BD%9C%E5%AE%B6%E5%A2%9E%E5%BC%BA-%E4%B8%AD%E7%AB%8B%E6%A8%A1%E5%BC%8F-SKILL.md)

**质量评估与迭代优化**

建立**多维度的质量评估体系**：



1. **AI 味检测指标**：

* AI 特征词汇使用频率

* 句式结构变化程度

* 段落长度分布均匀度

* 情感表达丰富程度[(63)](https://github.com/duongngo65yx-boop/De-AI-Prompt-Enhancer-Writer-Booster-SKILL/blob/main/%E5%8E%BBAI%E5%91%B3%E6%8F%90%E7%A4%BA%E8%AF%8D-%E4%BD%9C%E5%AE%B6%E5%A2%9E%E5%BC%BA-%E4%B8%AD%E7%AB%8B%E6%A8%A1%E5%BC%8F-SKILL.md)

1. **文学质量指标**：

* 语言流畅度和可读性

* 情节逻辑合理性

* 人物塑造丰满度

* 环境描写生动性[(9)](http://m.toutiao.com/group/7637450621221618202/?upstream_biz=doubao)

1. **读者体验指标**：

* 代入感和沉浸感评分

* 情感共鸣程度

* 阅读流畅度反馈

* 整体满意度评价[(9)](http://m.toutiao.com/group/7637450621221618202/?upstream_biz=doubao)

基于评估结果进行持续的迭代优化，不断调整去 AI 味策略和参数设置，最终目标是使 AI 生成的文本达到 "读起来像人写的" 效果。

## 五、写作流程设计与效果评估

### 5.1 两种写作流程对比分析

**直接约束一次成文流程**

**流程设计**：



1. 作者提供详细的写作指令，包括主题、风格、字数要求、关键情节等

2. AI 直接生成完整的章节内容

3. 作者进行整体审核和必要的修改[(76)](http://m.toutiao.com/group/7612514867328631336/?upstream_biz=doubao)

**技术实现方案**：



```
def generate\_chapter\_direct(prompt: str, constraints: dict) -> str:

&#x20;   """直接约束一次成文"""

&#x20;   full\_prompt = build\_full\_prompt(prompt, constraints)

&#x20;   content = llm\_client.generate(full\_prompt, constraints\["generation\_params"])

&#x20;   return content

def build\_full\_prompt(prompt: str, constraints: dict) -> str:

&#x20;   """构建完整的生成提示词"""

&#x20;   full\_prompt = f"创作要求：{prompt}\n"

&#x20;   full\_prompt += f"风格约束：{constraints\['style']}\n"

&#x20;   full\_prompt += f"字数要求：{constraints\['word\_count']}字\n"

&#x20;   full\_prompt += f"情节要点：{', '.join(constraints\['plot\_points'])}\n"

&#x20;   full\_prompt += f"角色要求：{constraints\['character\_constraints']}\n"

&#x20;   full\_prompt += f"AI味控制：{constraints\['ai\_control']}\n"

&#x20;   return full\_prompt
```

**优势分析**：



1. **创作效率高**：一次生成即可获得完整章节，节省时间和精力

2. **风格统一**：生成过程中始终遵循统一的约束条件，风格一致性好

3. **结构完整**：能够确保章节内容的完整性和逻辑连贯性[(76)](http://m.toutiao.com/group/7612514867328631336/?upstream_biz=doubao)

**劣势分析**：



1. **修改成本高**：如果整体风格或结构不符合预期，需要重新生成整个章节

2. **细节控制不足**：对具体段落和句子的控制能力有限

3. **AI 味较难控制**：一次性生成大量内容时，AI 味问题可能更难处理[(76)](http://m.toutiao.com/group/7612514867328631336/?upstream_biz=doubao)

**写作 Agent + 润色 Agent 流程**

**流程设计**：



1. 写作 Agent 生成章节细纲和核心内容

2. 润色 Agent 对生成内容进行去 AI 味处理和文笔优化

3. 作者进行最终审核和微调[(74)](http://m.toutiao.com/group/7624378264865341986/?upstream_biz=doubao)

**技术实现方案**：



```
def generate\_chapter\_agent\_chain(prompt: str, constraints: dict) -> str:

&#x20;   """写作Agent+润色Agent链式流程"""

&#x20;   \# 第一步：生成细纲

&#x20;   outline = outline\_agent.generate\_outline(prompt, constraints)

&#x20;  &#x20;

&#x20;   \# 第二步：根据细纲生成初稿

&#x20;   first\_draft = writer\_agent.generate\_draft(outline, constraints)

&#x20;  &#x20;

&#x20;   \# 第三步：润色处理

&#x20;   refined\_content = polisher\_agent.refine(first\_draft, constraints)

&#x20;  &#x20;

&#x20;   \# 第四步：质量检查

&#x20;   final\_content = quality\_checker.check(refined\_content, constraints)

&#x20;  &#x20;

&#x20;   return final\_content
```

**优势分析**：



1. **可控性强**：通过细纲阶段可以提前把控整体结构

2. **质量提升**：润色 Agent 专门处理 AI 味问题，文本质量更高

3. **灵活性好**：每个阶段都可以进行人工干预和调整[(74)](http://m.toutiao.com/group/7624378264865341986/?upstream_biz=doubao)

**劣势分析**：



1. **流程复杂**：需要多个 Agent 协作，系统复杂度较高

2. **时间成本增加**：多阶段处理会增加总体创作时间

3. **协调难度大**：需要确保不同 Agent 之间的风格一致性[(74)](http://m.toutiao.com/group/7624378264865341986/?upstream_biz=doubao)

### 5.2 效果评估指标体系

**定量评估指标**



1. **生成效率指标**：

* 生成速度（每分钟生成字数）

* Token 消耗率（每千字消耗的 Token 数）

* 成功率（生成内容符合要求的比例）

1. **质量量化指标**：

* 语言流畅度评分（基于语法检查和可读性分析）

* 情节完整度评分（基于情节要点覆盖率）

* 角色一致性评分（基于角色设定符合度）[(11)](https://blog.csdn.net/gitblog_00667/article/details/156482054)

1. **AI 味量化指标**：

* AI 特征词汇使用频率

* 句式结构变化程度（基于熵值计算）

* 段落长度分布均匀度[(63)](https://github.com/duongngo65yx-boop/De-AI-Prompt-Enhancer-Writer-Booster-SKILL/blob/main/%E5%8E%BBAI%E5%91%B3%E6%8F%90%E7%A4%BA%E8%AF%8D-%E4%BD%9C%E5%AE%B6%E5%A2%9E%E5%BC%BA-%E4%B8%AD%E7%AB%8B%E6%A8%A1%E5%BC%8F-SKILL.md)

1. **成本效益指标**：

* 单次生成成本（Token 费用）

* 人工审核时间（小时 / 千字）

* 总体创作成本（包括 AI 费用和人工成本）

**定性评估指标**



1. **文学质量评估**：

* 情节吸引力（是否能吸引读者继续阅读）

* 人物塑造丰满度（角色是否有个性和深度）

* 环境描写生动性（是否能营造真实的场景感）

* 对话自然度（角色对话是否符合身份和性格）[(9)](http://m.toutiao.com/group/7637450621221618202/?upstream_biz=doubao)

1. **风格一致性评估**：

* 叙述风格统一性（各章节之间风格是否一致）

* 语言风格协调性（是否符合目标读者群体偏好）

* 情感基调稳定性（是否能维持作品的整体氛围）[(63)](https://github.com/duongngo65yx-boop/De-AI-Prompt-Enhancer-Writer-Booster-SKILL/blob/main/%E5%8E%BBAI%E5%91%B3%E6%8F%90%E7%A4%BA%E8%AF%8D-%E4%BD%9C%E5%AE%B6%E5%A2%9E%E5%BC%BA-%E4%B8%AD%E7%AB%8B%E6%A8%A1%E5%BC%8F-SKILL.md)

1. **读者体验评估**：

* 代入感和沉浸感（读者是否能进入故事情境）

* 情感共鸣程度（是否能引发读者的情感反应）

* 阅读流畅度（阅读过程是否顺畅自然）

* 整体满意度（读者对作品的综合评价）[(9)](http://m.toutiao.com/group/7637450621221618202/?upstream_biz=doubao)

**综合评估方法**

建议采用 \*\*"定量 + 定性" 结合的评估方法 \*\*：



1. **自动化评估**：

* 使用语言分析工具进行语法检查和可读性评分

* 通过文本相似度分析评估风格一致性

* 使用 AI 检测器评估 AI 味程度[(63)](https://github.com/duongngo65yx-boop/De-AI-Prompt-Enhancer-Writer-Booster-SKILL/blob/main/%E5%8E%BBAI%E5%91%B3%E6%8F%90%E7%A4%BA%E8%AF%8D-%E4%BD%9C%E5%AE%B6%E5%A2%9E%E5%BC%BA-%E4%B8%AD%E7%AB%8B%E6%A8%A1%E5%BC%8F-SKILL.md)

1. **人工评估**：

* 专业编辑进行文学质量评估

* 目标读者群体进行阅读体验测试

* 作者进行创作体验反馈收集[(9)](http://m.toutiao.com/group/7637450621221618202/?upstream_biz=doubao)

1. **对比评估**：

* 与优秀的人工创作作品进行对比分析

* 与之前版本进行纵向对比

* 与其他 AI 工具生成结果进行横向对比

### 5.3 成本效益分析

**直接成本分析**



| 成本项目     | 直接约束方式                | 写作 Agent + 润色 Agent 方式 |
| -------- | --------------------- | ---------------------- |
| Token 消耗 | 1500-2000 tokens / 千字 | 2500-3500 tokens / 千字  |
| 生成时间     | 3-5 分钟 / 千字           | 8-12 分钟 / 千字           |
| 人工审核     | 0.5-1 小时 / 千字         | 1-1.5 小时 / 千字          |
| 单次成本     | \$0.15-0.20 / 千字      | \$0.25-0.35 / 千字       |

**间接成本分析**



1. **技术开发成本**：

* 直接约束方式：相对简单，主要是提示词优化成本

* 写作 Agent + 润色 Agent 方式：需要开发多个 Agent，技术复杂度高，开发成本约为前者的 2-3 倍[(74)](http://m.toutiao.com/group/7624378264865341986/?upstream_biz=doubao)

1. **维护成本**：

* 直接约束方式：提示词维护相对简单，更新成本低

* 写作 Agent + 润色 Agent 方式：需要维护多个模块，系统维护成本较高[(74)](http://m.toutiao.com/group/7624378264865341986/?upstream_biz=doubao)

1. **培训成本**：

* 直接约束方式：作者只需要学习提示词撰写技巧

* 写作 Agent + 润色 Agent 方式：作者需要了解完整的流程和各环节特点[(74)](http://m.toutiao.com/group/7624378264865341986/?upstream_biz=doubao)

**效益对比分析**



1. **创作效率对比**：

* 直接约束方式：短期效率高，但长期可能因质量问题需要大量返工

* 写作 Agent + 润色 Agent 方式：初期效率较低，但质量更稳定，减少后期修改成本[(76)](http://m.toutiao.com/group/7612514867328631336/?upstream_biz=doubao)

1. **作品质量对比**：

* 直接约束方式：质量波动较大，AI 味问题较难控制

* 写作 Agent + 润色 Agent 方式：质量更稳定，AI 味控制效果更好，文学价值更高[(74)](http://m.toutiao.com/group/7624378264865341986/?upstream_biz=doubao)

1. **商业价值对比**：

* 直接约束方式：适合快速产出但质量要求不高的场景

* 写作 Agent + 润色 Agent 方式：更适合需要长期连载和商业变现的作品

**决策建议**

基于成本效益分析，建议：



1. **对于新手作者或快速试写需求**：采用直接约束一次成文方式，降低学习成本，快速验证创意

2. **对于专业作者或商业作品**：采用写作 Agent + 润色 Agent 方式，虽然成本较高，但质量更有保障，长期收益更好

3. **对于长篇连载作品**：建议采用混合模式，大纲和关键情节使用写作 Agent + 润色 Agent 方式，常规章节使用直接约束方式，平衡质量和效率[(74)](http://m.toutiao.com/group/7624378264865341986/?upstream_biz=doubao)

## 六、技术路线验证与迭代优化

### 6.1 验证方案设计

**验证目标与范围**

技术路线验证的核心目标是**验证 CC/codex +LLM 撰写长篇小说技术路线的可行性和有效性**。验证范围包括：



1. **功能验证**：验证各技术模块是否能正常工作，包括 AI 生成、信息管理、去 AI 味处理等核心功能

2. **质量验证**：验证生成作品的文学质量是否达到预期标准

3. **效率验证**：验证创作效率是否满足商业化写作的需求

4. **成本验证**：验证总体成本是否在可接受范围内[(9)](http://m.toutiao.com/group/7637450621221618202/?upstream_biz=doubao)

**测试场景设计**

建议设计以下测试场景：



1. **基础功能测试场景**：

* 场景 1：生成 1000 字的角色介绍片段

* 场景 2：生成 3000 字的情节发展段落

* 场景 3：生成 5000 字的完整章节内容[(76)](http://m.toutiao.com/group/7612514867328631336/?upstream_biz=doubao)

1. **长篇创作测试场景**：

* 场景 4：连续生成 10 章内容，测试一致性保持能力

* 场景 5：生成 5 万字中篇小说，测试整体架构稳定性

* 场景 6：生成 20 万字长篇小说，测试长期运行能力

1. **特殊情况测试场景**：

* 场景 7：复杂人物关系场景（10 个以上主要角色）

* 场景 8：多线剧情交织场景（3 条以上情节线索）

* 场景 9：需要大量专业知识的特殊题材场景

**评估标准制定**

建立**多层次的评估标准体系**：



1. **技术指标标准**：

* 生成成功率：≥95%

* 响应时间：≤5 分钟 / 千字

* Token 消耗：≤2000 tokens / 千字

* 系统稳定性：连续运行 24 小时无故障

1. **质量指标标准**：

* AI 味检测评分：≤30%（基于 AI 检测器）

* 文学质量评分：≥4.0/5.0（基于专业评估）

* 读者满意度：≥80%（基于目标读者测试）[(9)](http://m.toutiao.com/group/7637450621221618202/?upstream_biz=doubao)

1. **一致性指标标准**：

* 角色设定一致性：≥95%（基于自动检测）

* 情节逻辑一致性：≥90%（基于人工审核）

* 风格一致性：≥85%（基于文本分析）[(11)](https://blog.csdn.net/gitblog_00667/article/details/156482054)

### 6.2 实验设计与执行

**实验环境配置**



1. **硬件环境**：

* CPU：Intel i7-12700H 或以上

* 内存：32GB 或以上

* 存储：512GB SSD 或以上

* GPU：NVIDIA RTX 3060 或以上（用于本地模型推理）

1. **软件环境**：

* 操作系统：Windows 10/11 或 Ubuntu 20.04+

* Python 版本：3.10+

* 主要框架：FastAPI、Vue 3、LangChain、Milvus[(35)](https://github.com/unitagain/WenShape/blob/main/README.md)

1. **API 配置**：

* OpenAI API Key（用于对比测试）

* 本地 LLM 模型（LLaMA、GPTQ 等）

* 向量数据库：Milvus 2.0+[(53)](https://github.com/guoliwei2333/all-in-rag/blob/main/docs/chapter1/01_RAG_intro.md)

**实验步骤设计**



1. **准备阶段（1-2 周）**：

* 搭建完整的技术环境

* 准备测试数据和参考资料

* 制定详细的测试计划和评估标准

* 培训测试人员[(9)](http://m.toutiao.com/group/7637450621221618202/?upstream_biz=doubao)

1. **功能测试阶段（2-3 周）**：

* 按测试场景逐一进行功能验证

* 记录各项技术指标

* 发现并修复技术问题

* 优化参数配置[(9)](http://m.toutiao.com/group/7637450621221618202/?upstream_biz=doubao)

1. **质量测试阶段（2-3 周）**：

* 邀请专业编辑进行文学质量评估

* 组织目标读者进行阅读体验测试

* 收集反馈意见并分析问题

* 调整去 AI 味策略和约束条件[(9)](http://m.toutiao.com/group/7637450621221618202/?upstream_biz=doubao)

1. **综合测试阶段（1-2 周）**：

* 进行长篇连续创作测试

* 验证系统的长期稳定性

* 评估整体成本效益

* 形成最终测试报告[(9)](http://m.toutiao.com/group/7637450621221618202/?upstream_biz=doubao)

**数据收集与分析**



1. **技术数据收集**：

* Token 消耗统计（每千字）

* 响应时间记录（分钟 / 千字）

* 生成成功率统计

* 系统错误日志分析

1. **质量数据收集**：

* AI 味检测结果（百分比）

* 文学质量评分（1-5 分）

* 读者满意度调查（百分比）

* 编辑反馈意见汇总[(9)](http://m.toutiao.com/group/7637450621221618202/?upstream_biz=doubao)

1. **用户体验数据**：

* 作者使用满意度（问卷调查）

* 学习成本评估（时间和难度）

* 操作便利性评分

* 功能需求反馈[(9)](http://m.toutiao.com/group/7637450621221618202/?upstream_biz=doubao)

### 6.3 迭代优化策略

**问题识别与分类**

基于测试结果，将发现的问题分为以下几类：



1. **技术问题**：

* 系统稳定性问题（崩溃、超时等）

* 性能问题（响应速度慢、资源消耗高）

* 接口兼容性问题

* 数据一致性问题[(9)](http://m.toutiao.com/group/7637450621221618202/?upstream_biz=doubao)

1. **质量问题**：

* AI 味过重

* 情节逻辑混乱

* 角色设定冲突

* 语言表达生硬[(63)](https://github.com/duongngo65yx-boop/De-AI-Prompt-Enhancer-Writer-Booster-SKILL/blob/main/%E5%8E%BBAI%E5%91%B3%E6%8F%90%E7%A4%BA%E8%AF%8D-%E4%BD%9C%E5%AE%B6%E5%A2%9E%E5%BC%BA-%E4%B8%AD%E7%AB%8B%E6%A8%A1%E5%BC%8F-SKILL.md)

1. **功能问题**：

* 某些场景下生成效果不佳

* 特定题材支持不足

* 人工审核流程繁琐

* 协作功能不完善[(9)](http://m.toutiao.com/group/7637450621221618202/?upstream_biz=doubao)

1. **用户体验问题**：

* 界面操作复杂

* 学习曲线陡峭

* 反馈机制不及时

* 文档说明不清晰[(9)](http://m.toutiao.com/group/7637450621221618202/?upstream_biz=doubao)

**优先级排序与处理策略**

采用**四象限分析法**对问题进行优先级排序：



| 重要性 / 紧急性 | 高重要性        | 低重要性        |
| --------- | ----------- | ----------- |
| 高紧急性      | 立即修复（如系统崩溃） | 快速优化（如性能问题） |
| 低紧急性      | 计划改进（如质量提升） | 待办事项（如功能扩展） |

**迭代优化流程设计**



1. **第一轮优化（紧急修复）**：

* 修复系统崩溃和严重性能问题

* 优化核心功能的稳定性

* 解决数据一致性问题

* 预期完成时间：1-2 周[(9)](http://m.toutiao.com/group/7637450621221618202/?upstream_biz=doubao)

1. **第二轮优化（质量提升）**：

* 改进去 AI 味算法和策略

* 优化角色一致性维护机制

* 提升情节逻辑生成能力

* 预期完成时间：2-3 周[(63)](https://github.com/duongngo65yx-boop/De-AI-Prompt-Enhancer-Writer-Booster-SKILL/blob/main/%E5%8E%BBAI%E5%91%B3%E6%8F%90%E7%A4%BA%E8%AF%8D-%E4%BD%9C%E5%AE%B6%E5%A2%9E%E5%BC%BA-%E4%B8%AD%E7%AB%8B%E6%A8%A1%E5%BC%8F-SKILL.md)

1. **第三轮优化（功能完善）**：

* 增加对特定题材的支持

* 优化人工审核流程

* 完善协作编辑功能

* 预期完成时间：3-4 周[(9)](http://m.toutiao.com/group/7637450621221618202/?upstream_biz=doubao)

1. **第四轮优化（体验改进）**：

* 简化界面操作流程

* 完善用户引导和帮助系统

* 建立实时反馈机制

* 预期完成时间：2-3 周[(9)](http://m.toutiao.com/group/7637450621221618202/?upstream_biz=doubao)

**持续改进机制**

建立 \*\*"收集 - 分析 - 改进 - 验证"\*\* 的持续改进循环：



1. **反馈收集渠道**：

* 建立用户反馈系统

* 定期进行用户访谈

* 收集社交媒体反馈

* 分析使用日志数据[(9)](http://m.toutiao.com/group/7637450621221618202/?upstream_biz=doubao)

1. **数据分析方法**：

* 统计分析用户行为模式

* 聚类分析常见问题

* 趋势分析功能使用情况

* A/B 测试效果对比[(9)](http://m.toutiao.com/group/7637450621221618202/?upstream_biz=doubao)

1. **改进实施策略**：

* 每 2 周发布一次小版本更新

* 每 2 个月发布一次大版本更新

* 建立功能路线图并公开

* 邀请核心用户参与测试[(9)](http://m.toutiao.com/group/7637450621221618202/?upstream_biz=doubao)

1. **效果验证机制**：

* 每次改进后进行效果测试

* 对比改进前后的关键指标

* 收集用户对改进的反馈

* 形成改进效果报告[(9)](http://m.toutiao.com/group/7637450621221618202/?upstream_biz=doubao)

通过持续的迭代优化，逐步提升系统的稳定性、质量和用户体验，最终实现技术路线的全面验证和商业化应用。

## 结语

通过对 CC/codex +LLM 撰写长篇小说技术路线的全面调研，我们构建了一个涵盖开源工具评估、通用架构设计、RAG 信息管理、AI 味控制、流程优化和效果验证的完整技术体系。

**核心发现总结**：



1. **开源工具生态成熟**：以 AI Creator、NovelForge、文枢为代表的开源工具已经具备了较为完善的长篇小说创作功能，为技术路线提供了坚实的基础[(16)](https://github.com/zskaitocn/NovelForge/blob/main/README.md)。

2. **通用架构可行**：通过分层抽象和模块化设计，可以构建不依赖特定 LLM 的通用写作工具流，确保技术路线的长期可持续性[(41)](https://www.cnblogs.com/clarance/p/20011455)。

3. **RAG 技术优势明显**：相比传统 Markdown 管理方式，RAG 技术在信息检索效率、一致性维护、智能辅助等方面具有显著优势，同时通过权限控制可以有效管理信息披露风险[(53)](https://github.com/guoliwei2333/all-in-rag/blob/main/docs/chapter1/01_RAG_intro.md)。

4. **AI 味控制是关键**：通过分层写作规范和系统性去 AI 味策略，可以显著提升 AI 生成文本的文学质量和可读性[(67)](https://preview.aclanthology.org/fix-opsupmap-display/2025.findings-acl.511.pdf)。

5. **流程选择需权衡**：直接约束一次成文方式适合快速产出，写作 Agent + 润色 Agent 方式适合高质量要求，需要根据具体需求进行选择[(76)](http://m.toutiao.com/group/7612514867328631336/?upstream_biz=doubao)。

6. **验证体系重要**：建立科学的评估标准和验证流程，通过持续迭代优化，能够确保技术路线的可行性和有效性[(9)](http://m.toutiao.com/group/7637450621221618202/?upstream_biz=doubao)。

**未来发展建议**：



1. **技术发展方向**：继续关注 LLM 技术的最新进展，特别是长文本处理能力和多模态生成技术的突破。

2. **功能扩展建议**：逐步增加多模态支持、智能协作、个性化推荐等高级功能，提升产品竞争力。

3. **商业化路径**：建议采用 "基础功能开源 + 高级功能付费" 的商业模式，既推动技术发展又实现商业价值。

4. **社区建设**：积极建设开发者社区，通过开源贡献、技术分享、用户反馈等方式推动技术生态的健康发展。

5. **风险控制**：在技术发展过程中，需要关注版权问题、AI 伦理问题以及技术依赖风险，建立相应的应对机制。

通过系统化的技术路线实施和持续优化，CC/codex +LLM 技术有望成为长篇小说创作的重要辅助工具，为创作者提供更高效、更优质的创作体验，推动数字内容创作产业的创新发展。

**参考资料&#x20;**

\[1] 放弃Dify和扣子!用开源BuildingAI搭建写作自动化平台实战\_梦梦软件精[ http://m.toutiao.com/group/7618052889952535082/?upstream\_biz=doubao](http://m.toutiao.com/group/7618052889952535082/?upstream_biz=doubao)

\[2] OPCPlay的微博[ https://m.weibo.cn/detail/5293712357986477](https://m.weibo.cn/detail/5293712357986477)

\[3] 千 笔 ！ ！ ！ 降 ai 率 就 靠 他 。 来 感觉 是 一款 实用 性 很强 、 适配 日常 和 办公 需求 的 国产 AI 工具 ， 体验 感 很 真实 ， 不 踩 雷 也 有 小 缺点 ， 简单 分享 下 我 的 真实 感受 。 首先 生成 速度 很快 ， 不管 是 写 文案 、 整理 笔记 、 写 段落 内容 ， 还是 润色 修改 文字 ， 输入 指令 后 基本 几秒 就能 出 完整 内容 ， 不会 卡顿 拖沓 ， 日常 应急 用 很 省心 。 文本 生成 的 逻辑 比较 通顺 ， 句式 自然 ， 不会 有 很 生硬 的 AI 腔 ， 用来 写 日常 文案 、 工作 总结 、 学习 笔记 、 简单 短文 都 很 合适 ， 内容 原创 度 也 不错 ， 不 容易 出现 重复 堆砌 的 问题 。 其次 功能 很 贴合 国内 使用 习惯 ， 支持 长 文本 续写 、 扩写 、 缩写 、 翻译 、 格式 整理 ， 还 能 做 简单 的 思路 梳理 ， 指令 理解度 挺 高 ， 不用 很 复杂 的 话术 ， 直白 描述 需求 就能 精准 给 到 对应 内容 ， 对 新手 很 友好 ， 不用 花 时间 学习 复杂 提示 词 。 写 论文 首 推 ！ ！ ！ # ai 写作 工具 # 降重 技巧 # 降重[ https://www.iesdouyin.com/share/note/7638657158880810661/?region=\&mid=7625971137250330640\&u\_code=0\&did=MS4wLjABAAAANwkJuWIRFOzg5uCpDRpMj4OX-QryoDgn-yYlXQnRwQQ\&iid=MS4wLjABAAAANwkJuWIRFOzg5uCpDRpMj4OX-QryoDgn-yYlXQnRwQQ\&with\_sec\_did=1\&video\_share\_track\_ver=\&titleType=title\&schema\_type=37\&share\_sign=QtHevg7fOwxoS9GsniKCDvwnMoLmdM.DC2t\_YDLAtEo-\&share\_version=280700\&ts=1778553413\&from\_aid=1128\&from\_ssr=1\&share\_track\_info=%7B%22link\_description\_type%22%3A%22%22%7D](https://www.iesdouyin.com/share/note/7638657158880810661/?region=\&mid=7625971137250330640\&u_code=0\&did=MS4wLjABAAAANwkJuWIRFOzg5uCpDRpMj4OX-QryoDgn-yYlXQnRwQQ\&iid=MS4wLjABAAAANwkJuWIRFOzg5uCpDRpMj4OX-QryoDgn-yYlXQnRwQQ\&with_sec_did=1\&video_share_track_ver=\&titleType=title\&schema_type=37\&share_sign=QtHevg7fOwxoS9GsniKCDvwnMoLmdM.DC2t_YDLAtEo-\&share_version=280700\&ts=1778553413\&from_aid=1128\&from_ssr=1\&share_track_info=%7B%22link_description_type%22%3A%22%22%7D)

\[4] 从卡文到顺畅输出:这5个AI工具，真能帮上小说作者的忙吗?(附我的真实体验)\_ai分析小说-CSDN博客[ https://blog.csdn.net/chataigc/article/details/149021421](https://blog.csdn.net/chataigc/article/details/149021421)

\[5] Article Writer - AI 驱动的智能写作系统[ https://github.com/YanHaidao/article-writer/blob/main/README.md](https://github.com/YanHaidao/article-writer/blob/main/README.md)

\[6] AI文章生成器开源:神奇工具助你省时又便捷\_ai写文章生成器开源-CSDN博客[ https://blog.csdn.net/oUY5dETx/article/details/135603370](https://blog.csdn.net/oUY5dETx/article/details/135603370)

\[7] AI智能小说创作平台:从创意到完稿的全流程自动化解决方案-CSDN博客[ https://blog.csdn.net/gitblog\_00245/article/details/157239684](https://blog.csdn.net/gitblog_00245/article/details/157239684)

\[8] 用 AI 写 小说 ， 总是 乱写 、 丢 上下文 ？ 我 用 这 套 流程 解决 了 用 AI 写 小说 最 头疼 的 三件 事 ：&#x20;

&#x20;1 . AI 不 按 大纲 走 ， 自由 发挥 乱写&#x20;

&#x20;2 . 每次 新开 会话 ， 上下文 全 丢&#x20;

&#x20;3 . 不 知道 怎么 系统 地 写 长篇&#x20;

&#x20;

&#x20;这期 视频 分享 我 自己 验证 过 的 一套 AI 写作 流程 （ Vibe Writing ） ，&#x20;

&#x20;从 选题 定位 → 核心 设定 → 大纲 推演 → 逐 章 创作 ，&#x20;

&#x20;配合 记忆 系统 解决 上下文 丢失 问题 。&#x20;

&#x20;

&#x20;Skill 包 获取 ： 私信 " 写作 " # 用 AI 写 小说 # 教程 来了 # 副业 分享 # 副业 赚钱[ https://www.iesdouyin.com/share/video/7614774046118382898/?region=\&mid=7614774106801720106\&u\_code=0\&did=MS4wLjABAAAANwkJuWIRFOzg5uCpDRpMj4OX-QryoDgn-yYlXQnRwQQ\&iid=MS4wLjABAAAANwkJuWIRFOzg5uCpDRpMj4OX-QryoDgn-yYlXQnRwQQ\&with\_sec\_did=1\&video\_share\_track\_ver=\&titleType=title\&share\_sign=1GiVWqu1IsV1BRNekN88uHv9EWh41GWfc0.lcAldnAk-\&share\_version=280700\&ts=1778553413\&from\_aid=1128\&from\_ssr=1\&share\_track\_info=%7B%22link\_description\_type%22%3A%22%22%7D](https://www.iesdouyin.com/share/video/7614774046118382898/?region=\&mid=7614774106801720106\&u_code=0\&did=MS4wLjABAAAANwkJuWIRFOzg5uCpDRpMj4OX-QryoDgn-yYlXQnRwQQ\&iid=MS4wLjABAAAANwkJuWIRFOzg5uCpDRpMj4OX-QryoDgn-yYlXQnRwQQ\&with_sec_did=1\&video_share_track_ver=\&titleType=title\&share_sign=1GiVWqu1IsV1BRNekN88uHv9EWh41GWfc0.lcAldnAk-\&share_version=280700\&ts=1778553413\&from_aid=1128\&from_ssr=1\&share_track_info=%7B%22link_description_type%22%3A%22%22%7D)

\[9] 实测AI写小说后，我彻底清醒了:AI能写百万字，却写不出人心温度\_翰阁优选[ http://m.toutiao.com/group/7637450621221618202/?upstream\_biz=doubao](http://m.toutiao.com/group/7637450621221618202/?upstream_biz=doubao)

\[10] How I Used AI to Write a 330,000-Character Sci-Fi Novel[ https://melanieli.com.au/ai-writing-process/](https://melanieli.com.au/ai-writing-process/)

\[11] AI小说生成革命:智能写作工具如何重塑长篇故事创作-CSDN博客[ https://blog.csdn.net/gitblog\_00667/article/details/156482054](https://blog.csdn.net/gitblog_00667/article/details/156482054)

\[12] Novel Writer - AI 驱动的中文小说创作工具[ https://github.com/lsg1103275794/novel-writer-style-cn](https://github.com/lsg1103275794/novel-writer-style-cn)

\[13] novel-writing[ https://github.com/topics/novel-writing](https://github.com/topics/novel-writing)

\[14] 网文 创作者 黑 科技 ， 让 你 轻松 完成 200w 字 的 网文 创作 开源 项目 # GitHub # AI # 网文 # 黑 科技 # Token[ https://www.iesdouyin.com/share/video/7638585678896401706/?region=\&mid=7638585688862362431\&u\_code=0\&did=MS4wLjABAAAANwkJuWIRFOzg5uCpDRpMj4OX-QryoDgn-yYlXQnRwQQ\&iid=MS4wLjABAAAANwkJuWIRFOzg5uCpDRpMj4OX-QryoDgn-yYlXQnRwQQ\&with\_sec\_did=1\&video\_share\_track\_ver=\&titleType=title\&share\_sign=LtQQ43kuwe5t2uSxtplu2OG3mS2PUXF2nFM2\_vX25Yk-\&share\_version=280700\&ts=1778553418\&from\_aid=1128\&from\_ssr=1\&share\_track\_info=%7B%22link\_description\_type%22%3A%22%22%7D](https://www.iesdouyin.com/share/video/7638585678896401706/?region=\&mid=7638585688862362431\&u_code=0\&did=MS4wLjABAAAANwkJuWIRFOzg5uCpDRpMj4OX-QryoDgn-yYlXQnRwQQ\&iid=MS4wLjABAAAANwkJuWIRFOzg5uCpDRpMj4OX-QryoDgn-yYlXQnRwQQ\&with_sec_did=1\&video_share_track_ver=\&titleType=title\&share_sign=LtQQ43kuwe5t2uSxtplu2OG3mS2PUXF2nFM2_vX25Yk-\&share_version=280700\&ts=1778553418\&from_aid=1128\&from_ssr=1\&share_track_info=%7B%22link_description_type%22%3A%22%22%7D)

\[15] 【GitHub项目推荐--AI Novel Generator:智能小说创作助手】-CSDN博客[ https://blog.csdn.net/j8267643/article/details/152665568](https://blog.csdn.net/j8267643/article/details/152665568)

\[16] NovelForge[ https://github.com/zskaitocn/NovelForge/blob/main/README.md](https://github.com/zskaitocn/NovelForge/blob/main/README.md)

\[17] 10款AI小说创作工具深度测评:笔灵AI、DeepSeek、ChatGPT等源码级对比分析 - CSDN文库[ https://wenku.csdn.net/doc/mukqw6n2rh2w](https://wenku.csdn.net/doc/mukqw6n2rh2w)

\[18] 2025年AI 写小说软件 终极测评:10款神器深度对比，ai写小说 选它就稳了! \[特殊字符]\_哪个ai写小说最不像ai-CSDN博客[ https://blog.csdn.net/chataigc/article/details/155139806](https://blog.csdn.net/chataigc/article/details/155139806)

\[19] 10款长篇网文AI工具测评:帮你找到最适合自己的写作助手\_梦笔为花[ http://m.toutiao.com/group/7638234802285560355/?upstream\_biz=doubao](http://m.toutiao.com/group/7638234802285560355/?upstream_biz=doubao)

\[20] 10款AI小说写作工具深度测评:功能对比、适用场景与可运行源码解析 - CSDN文库[ https://wenku.csdn.net/doc/8bt0kku9x0ht](https://wenku.csdn.net/doc/8bt0kku9x0ht)

\[21] 長文生成に強いAIツール比較：小説・レポート・論文作成をサポート[ https://xn--ai-fk1eu00k.com/blog/long-form-ai-tools](https://xn--ai-fk1eu00k.com/blog/long-form-ai-tools)

\[22] 2025年12月终极盘点!8款AI写小说神器横评，卡文救星今天降临!——日更一万字，从地狱模式切换到简单模式，你只差一个 - 掘金[ https://juejin.cn/post/7589639203091103770](https://juejin.cn/post/7589639203091103770)

\[23] 2026最新实测:5款AI写小说软件实测报告(内含使用对比+推荐)-CSDN博客[ https://blog.csdn.net/huayishuo/article/details/157763469](https://blog.csdn.net/huayishuo/article/details/157763469)

\[24] 2026年全景基准测试:7款主流AI写小说工具底层架构与工程化实践对比-CSDN博客[ https://blog.csdn.net/qq\_18733629/article/details/159043523](https://blog.csdn.net/qq_18733629/article/details/159043523)

\[25] 2026年亲测不踩雷:AI写小说工具真实使用反馈\_柒柒文学社[ http://m.toutiao.com/group/7621773174724510271/?upstream\_biz=doubao](http://m.toutiao.com/group/7621773174724510271/?upstream_biz=doubao)

\[26] 谁懂 啊 ！ 写 小说 卡文 、 逻辑 崩盘 、 人设 写 崩 的 痛苦 ？ 现在 用 AI 辅助 写 小说 真的 能 救 大命 ！ 拆 文 拆解 爆款 逻辑 、 续写 帮 你 打开 思路 、 鉴 评 直接 点 出 问题 ， 再也 不 用 熬夜 死磕 啦 ！ # AI 写作 # AI # AI 创作 # 文镜 君 # AI 智 闲[ https://www.iesdouyin.com/share/video/7638495439042909669/?region=\&mid=7638495332132801295\&u\_code=0\&did=MS4wLjABAAAANwkJuWIRFOzg5uCpDRpMj4OX-QryoDgn-yYlXQnRwQQ\&iid=MS4wLjABAAAANwkJuWIRFOzg5uCpDRpMj4OX-QryoDgn-yYlXQnRwQQ\&with\_sec\_did=1\&video\_share\_track\_ver=\&titleType=title\&share\_sign=i46JfAAU7tnpsm\_\_zuGci8hdn5eZ5Xf3FPoYwZaxyao-\&share\_version=280700\&ts=1778553433\&from\_aid=1128\&from\_ssr=1\&share\_track\_info=%7B%22link\_description\_type%22%3A%22%22%7D](https://www.iesdouyin.com/share/video/7638495439042909669/?region=\&mid=7638495332132801295\&u_code=0\&did=MS4wLjABAAAANwkJuWIRFOzg5uCpDRpMj4OX-QryoDgn-yYlXQnRwQQ\&iid=MS4wLjABAAAANwkJuWIRFOzg5uCpDRpMj4OX-QryoDgn-yYlXQnRwQQ\&with_sec_did=1\&video_share_track_ver=\&titleType=title\&share_sign=i46JfAAU7tnpsm__zuGci8hdn5eZ5Xf3FPoYwZaxyao-\&share_version=280700\&ts=1778553433\&from_aid=1128\&from_ssr=1\&share_track_info=%7B%22link_description_type%22%3A%22%22%7D)

\[27] 2026 年 AI写小说工具实测:三款热门产品的创作适配体验|小说|工作流|工具实测|网文\_手机网易网[ http://m.163.com/news/article/KR40SI110517DTS3.html](http://m.163.com/news/article/KR40SI110517DTS3.html)

\[28] 2026全网硬核测评:10款写小说软件深度横评(附AI写小说避坑指南与对比表)\_有哪些好用的写小说软件,对比评测-CSDN博客[ https://blog.csdn.net/huayishuo/article/details/158427013](https://blog.csdn.net/huayishuo/article/details/158427013)

\[29] 2026年四款AI写小说工具亲测报告\_柒柒文学社[ http://m.toutiao.com/group/7628796483776676392/?upstream\_biz=doubao](http://m.toutiao.com/group/7628796483776676392/?upstream_biz=doubao)

\[30] 别再为选AI写作工具头疼了!这4款亲测好用的伙伴，帮你稳稳写故事\_ai写小说最好用的-CSDN博客[ https://blog.csdn.net/chataigc/article/details/148791852](https://blog.csdn.net/chataigc/article/details/148791852)

\[31] 【2025年亲测】10款ai写小说软件深度测评:我踩了无数坑，才选出这几款码字神器!(内附横评表)\_国产ai写小说评测-CSDN博客[ https://blog.csdn.net/chataigc/article/details/154959177](https://blog.csdn.net/chataigc/article/details/154959177)

\[32] 2026年4月AI写小说软件推荐:全流程辅助工具深度解析与测评\_科教见闻[ http://m.toutiao.com/group/7634088593174184448/?upstream\_biz=doubao](http://m.toutiao.com/group/7634088593174184448/?upstream_biz=doubao)

\[33] I used the GPT-4.5 API to write a novel, with a reasonably simple loop-based wor...[ https://news.ycombinator.com/item?id=44264611](https://news.ycombinator.com/item?id=44264611)

\[34] 2025年亲测:AI写小说工具真实使用体验分享\_写作\_Claude\_DeepSeek[ https://m.sohu.com/a/935380403\_122514905/](https://m.sohu.com/a/935380403_122514905/)

\[35] WenShape/README.md at main · unitagain/WenShape · GitHub[ https://github.com/unitagain/WenShape/blob/main/README.md](https://github.com/unitagain/WenShape/blob/main/README.md)

\[36] LLM——基于LangChain与LangGraph实现的长篇文章自动写作工作流\_langchain写小说-CSDN博客[ https://blog.csdn.net/weixin\_43844521/article/details/149866058](https://blog.csdn.net/weixin_43844521/article/details/149866058)

\[37] AI 框架 Pocket Flow 介绍 Pocket Flow 是 一个 仅 用 100 行 代码 实现 的 轻量级 大型 语言 模型 （ LLM ） 框架 ， 支持 多 Agent 协作 、 工作 流 管理 、 检索 增强 生成 （ RAG ） 等 功能 ， 适合 快速 构建 AI 应用 。 # （ LLM ） 框 # 大模型 课程 # AI[ https://www.iesdouyin.com/share/video/7527334736327445775/?region=\&mid=7527335024220277542\&u\_code=0\&did=MS4wLjABAAAANwkJuWIRFOzg5uCpDRpMj4OX-QryoDgn-yYlXQnRwQQ\&iid=MS4wLjABAAAANwkJuWIRFOzg5uCpDRpMj4OX-QryoDgn-yYlXQnRwQQ\&with\_sec\_did=1\&video\_share\_track\_ver=\&titleType=title\&share\_sign=WUmUL2XEjKdyMCxSZgkRhMEZYhgPo3rjpsXP2eG\_FLI-\&share\_version=280700\&ts=1778553439\&from\_aid=1128\&from\_ssr=1\&share\_track\_info=%7B%22link\_description\_type%22%3A%22%22%7D](https://www.iesdouyin.com/share/video/7527334736327445775/?region=\&mid=7527335024220277542\&u_code=0\&did=MS4wLjABAAAANwkJuWIRFOzg5uCpDRpMj4OX-QryoDgn-yYlXQnRwQQ\&iid=MS4wLjABAAAANwkJuWIRFOzg5uCpDRpMj4OX-QryoDgn-yYlXQnRwQQ\&with_sec_did=1\&video_share_track_ver=\&titleType=title\&share_sign=WUmUL2XEjKdyMCxSZgkRhMEZYhgPo3rjpsXP2eG_FLI-\&share_version=280700\&ts=1778553439\&from_aid=1128\&from_ssr=1\&share_track_info=%7B%22link_description_type%22%3A%22%22%7D)

\[38] 程序员必备:100行代码实现极简LLM框架，告别依赖地狱，轻松构建智能体应用\_decideaction(-CSDN博客[ https://blog.csdn.net/2401\_85390073/article/details/157362394](https://blog.csdn.net/2401_85390073/article/details/157362394)

\[39] OpenClaw全自动个人写作系统搭建:阿里云/本地部署+API配置，从素材收集到分发归档全流程实战指南-阿里云开发者社区[ https://developer.aliyun.com/article/1718861](https://developer.aliyun.com/article/1718861)

\[40] WriteHERE - OpenI[ https://openi.cn/306152.html](https://openi.cn/306152.html)

\[41] AI写作工具的系统化架构:从内容生成到企业工作流整合的深度解析 - 胖子君 - 博客园[ https://www.cnblogs.com/clarance/p/20011455](https://www.cnblogs.com/clarance/p/20011455)

\[42] Part 3: RAG Without the LLM: Building Context-First Retrieval Pipelines[ https://abisoye.dev/blog/rag-without-the-llm](https://abisoye.dev/blog/rag-without-the-llm)

\[43] 🚀 Prompt Flow Craft[ https://github.com/KeatonLi/prompt-flow-craft/blob/main/README.md](https://github.com/KeatonLi/prompt-flow-craft/blob/main/README.md)

\[44] Content Generation Systems: Architecture and Implementation[ https://www.grizzlypeaksoftware.com/library/content-generation-systems-architecture-and-implementation-a8gy0c7u](https://www.grizzlypeaksoftware.com/library/content-generation-systems-architecture-and-implementation-a8gy0c7u)

\[45] WriteHERE - AI写作助手[ https://github.com/vincent-yangyijie/Write\_HERE/blob/master/README.md](https://github.com/vincent-yangyijie/Write_HERE/blob/master/README.md)

\[46] Simpliflow: A Lightweight Open-Source Framework for Rapid Creation and Deployment of Generative Agentic AI Workflows(pdf)[ https://arxiv.org/pdf/2510.10675v1](https://arxiv.org/pdf/2510.10675v1)

\[47] WriteHERE - AI写作助手[ https://github.com/vincent-yangyijie/Write\_HERE](https://github.com/vincent-yangyijie/Write_HERE)

\[48] AI辅助网文创作理论研究笔记(八):世界书——持久化状态管理与RAG的协同\_世界书注入位置-CSDN博客[ https://blog.csdn.net/sanshanjianke/article/details/160587436](https://blog.csdn.net/sanshanjianke/article/details/160587436)

\[49] 为AI注入“故事灵魂”!微信王牌项目ComoRAG，让机器真正读懂“伏笔”和“高潮”!-CSDN博客[ https://blog.csdn.net/xx\_nm98/article/details/155237311](https://blog.csdn.net/xx_nm98/article/details/155237311)

\[50] 智源推出下一代检索增强大模型框架MemoRAG - 智源社区[ https://hub.baai.ac.cn/view/39891](https://hub.baai.ac.cn/view/39891)

\[51] 基于RAG与AI Agent的长篇小说智能创作系统部署与实战指南-CSDN博客[ https://blog.csdn.net/weixin\_42538175/article/details/160641108](https://blog.csdn.net/weixin_42538175/article/details/160641108)

\[52] Rag Summary[ https://www.bookey.app/book/rag](https://www.bookey.app/book/rag)

\[53] 第一节 RAG简介[ https://github.com/guoliwei2333/all-in-rag/blob/main/docs/chapter1/01\_RAG\_intro.md](https://github.com/guoliwei2333/all-in-rag/blob/main/docs/chapter1/01_RAG_intro.md)

\[54] ComoRAG: A Cognitive-Inspired Memory-Organized RAG for Stateful Long Narrative Reasoning[ https://www.arxiv.org/pdf/2508.10419](https://www.arxiv.org/pdf/2508.10419)

\[55] LangChain RAG, FLAN-T5 for SW Novel Chronology[ https://www.kaggle.com/code/aruneembhowmick/langchain-rag-flan-t5-for-sw-novel-chronology](https://www.kaggle.com/code/aruneembhowmick/langchain-rag-flan-t5-for-sw-novel-chronology)

\[56] Rag[ https://astroboy.fandom.com/wiki/Rag](https://astroboy.fandom.com/wiki/Rag)

\[57] Epic of Techno-Magic（Bas-Rag Series）[ https://andmorefine.com/en/technology-era/bas-lag-series](https://andmorefine.com/en/technology-era/bas-lag-series)

\[58] 降低语言模型AI化输出的系统性方法与实操指南\_情感曲线建模-CSDN博客[ https://blog.csdn.net/charles666666/article/details/147967816](https://blog.csdn.net/charles666666/article/details/147967816)

\[59] 3招秒去AI味!让文章像人写的，附提示词\_人人都是产品经理[ http://m.toutiao.com/group/7529789402579517991/?upstream\_biz=doubao](http://m.toutiao.com/group/7529789402579517991/?upstream_biz=doubao)

\[60] 四 小时 就 写完 了 哈哈 哈哈 ！ ！ ！ （ 附 指令 ） 。 gemini 指令 先 写 再 降 ai 率 ， 最后 再 润色 ， 一套 连招 搞定 一篇 初稿 ！ ！&#x20;

&#x20;\# 驯服 AI # 降 ai 率 # Gemini3 # 指令 # AI 工具[ https://www.iesdouyin.com/share/note/7638548480033574163/?region=\&mid=0\&u\_code=0\&did=MS4wLjABAAAANwkJuWIRFOzg5uCpDRpMj4OX-QryoDgn-yYlXQnRwQQ\&iid=MS4wLjABAAAANwkJuWIRFOzg5uCpDRpMj4OX-QryoDgn-yYlXQnRwQQ\&with\_sec\_did=1\&video\_share\_track\_ver=\&titleType=title\&schema\_type=37\&share\_sign=PbOxpYmzoSp\_91.3nXs67\_O0ekkGCQoY8zAgUshG3Ug-\&share\_version=280700\&ts=1778553555\&from\_aid=1128\&from\_ssr=1\&share\_track\_info=%7B%22link\_description\_type%22%3A%22%22%7D](https://www.iesdouyin.com/share/note/7638548480033574163/?region=\&mid=0\&u_code=0\&did=MS4wLjABAAAANwkJuWIRFOzg5uCpDRpMj4OX-QryoDgn-yYlXQnRwQQ\&iid=MS4wLjABAAAANwkJuWIRFOzg5uCpDRpMj4OX-QryoDgn-yYlXQnRwQQ\&with_sec_did=1\&video_share_track_ver=\&titleType=title\&schema_type=37\&share_sign=PbOxpYmzoSp_91.3nXs67_O0ekkGCQoY8zAgUshG3Ug-\&share_version=280700\&ts=1778553555\&from_aid=1128\&from_ssr=1\&share_track_info=%7B%22link_description_type%22%3A%22%22%7D)

\[61] 消除AI生成内容‘AI味’的系统性优化方法与技术实践指南 - CSDN文库[ https://wenku.csdn.net/doc/z7k8ivdb9p](https://wenku.csdn.net/doc/z7k8ivdb9p)

\[62] 拒绝“机味”:AI 写作 API 深度封装实战，让内容回归人性温度\_mb69f4243220c97的技术博客\_51CTO博客[ https://blog.51cto.com/u\_17700723/14588574](https://blog.51cto.com/u_17700723/14588574)

\[63] De-AI-Prompt-Enhancer-Writer-Booster-SKILL/去AI味提示词-作家增强-中立模式-SKILL.md at main · duongngo65yx-boop/De-AI-Prompt-Enhancer-Writer-Booster-SKILL · GitHub[ https://github.com/duongngo65yx-boop/De-AI-Prompt-Enhancer-Writer-Booster-SKILL/blob/main/%E5%8E%BBAI%E5%91%B3%E6%8F%90%E7%A4%BA%E8%AF%8D-%E4%BD%9C%E5%AE%B6%E5%A2%9E%E5%BC%BA-%E4%B8%AD%E7%AB%8B%E6%A8%A1%E5%BC%8F-SKILL.md](https://github.com/duongngo65yx-boop/De-AI-Prompt-Enhancer-Writer-Booster-SKILL/blob/main/%E5%8E%BBAI%E5%91%B3%E6%8F%90%E7%A4%BA%E8%AF%8D-%E4%BD%9C%E5%AE%B6%E5%A2%9E%E5%BC%BA-%E4%B8%AD%E7%AB%8B%E6%A8%A1%E5%BC%8F-SKILL.md)

\[64] AI写作怎么让内容更有层次感\_用AI搭建内容梯度的指令有哪些-人工智能-PHP中文网[ https://m.php.cn/faq/2138971.html](https://m.php.cn/faq/2138971.html)

\[65] 如何在 Prompt 中设置输出层级?教你掌控 AI 的表达结构-人工智能-PHP中文网[ https://m.php.cn/faq/2244503.html](https://m.php.cn/faq/2244503.html)

\[66] AI辅助开发实战:从零构建高效AI写作提示词方法大全\_终端行者bbb-音视频技术专区[ https://devpress.csdn.net/avi/697f93cca16c6648a986abba.html](https://devpress.csdn.net/avi/697f93cca16c6648a986abba.html)

\[67] A Cognitive Writing Perspective for Constrained Long-Form Text Generation(pdf)[ https://preview.aclanthology.org/fix-opsupmap-display/2025.findings-acl.511.pdf](https://preview.aclanthology.org/fix-opsupmap-display/2025.findings-acl.511.pdf)

\[68] 写作技艺总览（Skills）[ https://github.com/donghuixin/AI-Vibe-Writing-Skills/blob/main/SKILLS.md](https://github.com/donghuixin/AI-Vibe-Writing-Skills/blob/main/SKILLS.md)

\[69] GenFlow: Constrained Long-Form Text Generation via Adaptive Workflow Optimization[ https://openreview.net/pdf?id=PrcNpPxWIQ](https://openreview.net/pdf?id=PrcNpPxWIQ)

\[70] TreeWriter: AI-Assisted Hierarchical Planning and Writing for Long-Form Documents[ https://arxiv.org/html/2601.12740v1](https://arxiv.org/html/2601.12740v1)

\[71] 创作小说的方法第2章 落笔成篇:小说创作全流程实战指南在线免费阅读\_番茄小说官网[ https://fanqienovel.com/reader/7571725738345234968](https://fanqienovel.com/reader/7571725738345234968)

\[72] 新手如何开始写小说?5款工具实测分享(含小说大纲模板)\_笔灵如何选择网文模版大纲-CSDN博客[ https://blog.csdn.net/2301\_79545694/article/details/150338334](https://blog.csdn.net/2301_79545694/article/details/150338334)

\[73] 新人 写 小说 是 不是 总 犯难 ？ 要么 想到 哪 写 到 哪 ， 写 5 章 就 卡壳 ； 要么 没 搭 框架 就 冲 正文 ， 最后 逻辑 崩盘 烂尾 ！ 其实 写 小说 有 固定 “ 正确 顺序 ” ， 跟着 走 ， 从 构思 到 完稿 一路 顺畅 ， 还 能 让 故事 更 抓 读者 ！ # 网文 # 小说 # 小说 感 # 小说 控 # 写 小说[ https://www.iesdouyin.com/share/video/7580726310386863034/?region=\&mid=7580726256866822946\&u\_code=0\&did=MS4wLjABAAAANwkJuWIRFOzg5uCpDRpMj4OX-QryoDgn-yYlXQnRwQQ\&iid=MS4wLjABAAAANwkJuWIRFOzg5uCpDRpMj4OX-QryoDgn-yYlXQnRwQQ\&with\_sec\_did=1\&video\_share\_track\_ver=\&titleType=title\&share\_sign=8SItP.QuLvsHSm62yNvh6ndtCcAq0a\_l7btmqObiRGM-\&share\_version=280700\&ts=1778553560\&from\_aid=1128\&from\_ssr=1\&share\_track\_info=%7B%22link\_description\_type%22%3A%22%22%7D](https://www.iesdouyin.com/share/video/7580726310386863034/?region=\&mid=7580726256866822946\&u_code=0\&did=MS4wLjABAAAANwkJuWIRFOzg5uCpDRpMj4OX-QryoDgn-yYlXQnRwQQ\&iid=MS4wLjABAAAANwkJuWIRFOzg5uCpDRpMj4OX-QryoDgn-yYlXQnRwQQ\&with_sec_did=1\&video_share_track_ver=\&titleType=title\&share_sign=8SItP.QuLvsHSm62yNvh6ndtCcAq0a_l7btmqObiRGM-\&share_version=280700\&ts=1778553560\&from_aid=1128\&from_ssr=1\&share_track_info=%7B%22link_description_type%22%3A%22%22%7D)

\[74] 2026年网文作者AI辅助写作实战指南:从大纲到完本的全流程拆解\_成仔码字中[ http://m.toutiao.com/group/7624378264865341986/?upstream\_biz=doubao](http://m.toutiao.com/group/7624378264865341986/?upstream_biz=doubao)

\[75] Novel Writer 最佳实践[ https://github.com/wordflowlab/novel-writer/blob/main/docs/best-practices.md](https://github.com/wordflowlab/novel-writer/blob/main/docs/best-practices.md)

\[76] 写小说的正确顺序:按这个流程写，不卡文、不烂尾，建议收藏!\_李知汐[ http://m.toutiao.com/group/7612514867328631336/?upstream\_biz=doubao](http://m.toutiao.com/group/7612514867328631336/?upstream_biz=doubao)

\[77] novel-writer/docs/workflow.md at main · wordflowlab/novel-writer · GitHub[ https://github.com/wordflowlab/novel-writer/blob/main/docs/workflow.md](https://github.com/wordflowlab/novel-writer/blob/main/docs/workflow.md)

\[78] Writing Your Novel Outlines: To Plan Your Story Like a Pro\![ https://www.authorflows.com/blogs/writing-novel-outline-guide](https://www.authorflows.com/blogs/writing-novel-outline-guide)

\[79] The Seven-Draft Novel-Writing System[ https://www.erikgoodwyn.com/post/the-seven-draft-novel-writing-system](https://www.erikgoodwyn.com/post/the-seven-draft-novel-writing-system)

\[80] How to Outline a Novel, With Examples[ https://www.grammarly.com/blog/writing-process/how-to-outline-a-novel/](https://www.grammarly.com/blog/writing-process/how-to-outline-a-novel/)

\[81] How to Write a Novel in 90 Days: Exact 2026 Outline That Produced 11 Bestsellers[ https://rivereditor.com/blogs/write-novel-90-days-2026-outline](https://rivereditor.com/blogs/write-novel-90-days-2026-outline)

\[82] How to Write a Novel[ https://stationerypal.com/blogs/how-to/how-to-write-a-novel](https://stationerypal.com/blogs/how-to/how-to-write-a-novel)

\[83] Novel Writing: A Step-by-Step Guide[ https://marykole.com/novel-writing](https://marykole.com/novel-writing)

> （注：文档部分内容可能由 AI 生成）