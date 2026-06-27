---
aliases:
  - Agent记忆系统
  - Agent Memory System
  - LLM记忆机制
tags:
  - AI/Agent
  - AI/Memory
  - AI/LLM
created: 2026-06-28
updated: 2026-06-28
---

# Agent记忆系统

Agent记忆系统是AI Agent架构中的核心组件，决定了Agent能否在多轮交互中保持上下文连贯性、积累经验并持续学习。记忆系统的设计直接关系到Agent的智能水平和实用价值。

## 短期记忆（上下文窗口）

短期记忆对应LLM的Context Window，是模型在单次推理中能直接访问的信息范围。

### 工作原理

- 输入的token序列在注意力机制中被全局关注
- 窗口大小决定了"即时记忆"的容量：GPT-4o 128K tokens、Claude 3.5 200K tokens、Gemini 1.5 1M+ tokens
- 超出窗口的信息将被截断，无法被模型感知

### 限制与挑战

- **上下文长度瓶颈**：即使窗口扩大，长对话中早期信息仍可能被"遗忘"
- **注意力稀释**：过长上下文导致模型对关键信息的注意力分散
- **成本问题**：输入token数直接影响推理成本（API计费）
- **"大海捞针"问题**：长上下文中准确定位特定信息的能力仍有限

### 扩展策略

- 对话摘要（Conversation Summary）：定期压缩历史对话
- 滑动窗口（Sliding Window）：保留最近N轮对话
- 重要性筛选：基于相关性评分保留关键信息

## 长期记忆

长期记忆用于持久化存储Agent积累的知识和经验，突破上下文窗口限制。

### 向量数据库

将文本通过Embedding模型转化为高维向量，存储在专门的向量数据库中进行相似性检索。

- **常用方案**：Pinecone、Weaviate、Qdrant、ChromaDB、Milvus
- **检索方式**：基于Cosine Similarity或L2距离的近似最近邻（ANN）搜索
- **索引算法**：HNSW、IVF、PQ（Product Quantization）
- **典型流程**：文本分块 → Embedding → 存储 → 查询时Embedding → 相似性检索 → 返回Top-K结果

### 知识图谱

以结构化的图形式存储实体及其关系，适合需要推理的场景。

- **表示方式**：三元组（Subject, Predicate, Object）
- **常用框架**：Neo4j、ArangoDB、NetworkX
- **与RAG结合**：GraphRAG将图谱结构融入检索增强生成
- **优势**：支持多跳推理、关系查询、因果链追踪

### 混合方案

实际系统中常将向量检索与知识图谱结合使用，向量检索处理语义相似性，知识图谱处理结构化推理。

## 工作记忆（Scratchpad、思维链）

工作记忆是Agent在执行任务过程中临时使用的"草稿纸"，用于中间推理和信息组织。

### Scratchpad

- 在提示词中显式开辟一段空间用于记录中间步骤
- 可包含任务分解、中间计算结果、备选方案比较
- 与Chain of Thought结合使用效果更佳

### 思维链（Chain of Thought）

- 通过提示"Let's think step by step"引导模型逐步推理
- 将复杂问题分解为可管理的子步骤
- 扩展形式：Tree of Thought（树状探索）、Graph of Thought（图状探索）、ReAct（推理+行动交替）

### 自我反思（Reflection）

- Agent执行后对结果进行评估和反思
- 将反思结论存入记忆，避免重复犯错
- Reflexion框架：尝试 → 评估 → 反思 → 重试

## 记忆检索与压缩

### 检索策略

- **语义检索**：基于Embedding相似度
- **关键词检索**：BM25等传统IR方法
- **时间衰减**：近期记忆权重更高
- **重要性评分**：基于LLM评估信息重要性
- **混合检索**：结合多种信号的综合排序

### 记忆压缩

- **摘要压缩**：用LLM对长文本生成摘要
- **关键信息提取**：提取实体、关系、关键事实
- **选择性遗忘**：丢弃低价值或过时信息
- **分层压缩**：原始记录 → 摘要 → 关键词，逐层压缩

### 记忆更新

- **去重**：避免重复存储相同信息
- **冲突检测**：新旧信息矛盾时的处理策略
- **版本管理**：跟踪信息的演变历史

## MemGPT、Generative Agents

### MemGPT

受操作系统虚拟内存启发的分层记忆管理框架。

- **核心思想**：将LLM的Context Window类比为"主内存"，外部存储类比为"磁盘"
- **分层架构**：Main Context（工作记忆） ↔ External Storage（长期记忆）
- **自主管理**：Agent通过函数调用自主决定何时读写记忆
- **操作原语**：`core_memory_append`、`core_memory_replace`、`archival_memory_insert`、`archival_memory_search`
- **应用场景**：无限长度对话、文档分析、持续学习

### Generative Agents

斯坦福大学提出的生成式Agent架构（"小镇"实验）。

- **记忆流（Memory Stream）**：记录Agent所有经历的时序列表
- **检索函数**：综合近期性（Recency）、重要性（Importance）、相关性（Relevance）三个维度
- **反思机制**：定期从具体经历中提炼高层抽象见解
- **规划机制**：基于记忆和反思生成每日计划并动态调整
- **涌现行为**：多个Agent之间自发形成社交关系、组织活动、传播信息

### 其他重要框架

- **AutoGen**：微软的多Agent对话框架，支持灵活的记忆共享
- **CrewAI**：角色扮演Agent框架，内置记忆管理
- **LangChain Memory**：提供ConversationBufferMemory、ConversationSummaryMemory等多种记忆组件
- **LlamaIndex**：提供丰富的索引和检索模式，可作为长期记忆后端

## 设计原则与实践建议

1. **按需设计**：不是所有Agent都需要完整的记忆系统，简单任务用短对话即可
2. **分层存储**：热数据放Context，温数据放向量库，冷数据放持久化存储
3. **评估记忆质量**：定期测试Agent对历史信息的召回准确率
4. **隐私与安全**：敏感信息的存储和访问需要严格的权限控制
5. **成本权衡**：更丰富的记忆意味着更高的存储和检索成本
