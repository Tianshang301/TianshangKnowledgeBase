---
aliases:
  - RAG系统设计
  - 检索增强生成
  - Retrieval Augmented Generation
tags:
  - RAG
  - 向量数据库
  - Embedding
  - 检索系统
  - LLM应用
created: 2026-06-27
updated: 2026-06-27
---

# RAG系统设计

RAG（Retrieval Augmented Generation，检索增强生成）是将外部知识检索与大语言模型生成能力相结合的技术架构。它解决了LLM知识截止、幻觉和领域知识不足等核心问题，是构建知识密集型AI应用的基础架构。

## RAG架构演进

### Naive RAG（朴素RAG）

最基础的RAG实现：

- **流程**：文档分块 → 向量化 → 检索 → 拼接 → 生成
- **优势**：实现简单，快速验证
- **问题**：
  - 检索质量依赖embedding模型
  - 无法处理复杂查询
  - 上下文窗口限制
  - 缺乏多轮推理能力

### Advanced RAG（高级RAG）

在Naive RAG基础上引入优化策略：

- **检索前优化**：查询改写、查询扩展、假设文档嵌入（HyDE）
- **检索优化**：混合检索、重排序、元数据过滤
- **检索后优化**：上下文压缩、去重、相关性过滤

### Modular RAG（模块化RAG）

将RAG分解为可组合的模块：

- **核心模块**：Query Understanding、Retrieval、Reranking、Generation
- **可选模块**：Query Routing、Memory、Reasoning、Tool Use
- **编排层**：根据任务动态选择和组合模块

## 文档处理

### 文档解析

- **文本提取**：PDF、Word、HTML、Markdown解析
- **OCR处理**：图片、扫描件文字识别
- **表格提取**：结构化表格数据提取
- **工具选择**：Unstructured、LlamaParse、Apache Tika

### 分块策略（Chunking）

分块是RAG质量的关键影响因素：

**固定大小分块**：
- 按字符数或token数切分
- 简单但可能破坏语义完整性
- 通常设置重叠窗口（overlap）

**语义分块**：
- 基于语义相似度切分
- 保持语义完整性
- 计算成本较高

**递归分块**：
- 按层级分隔符递归切分
- Markdown按标题层级、代码按函数
- 平衡效率和质量

```python
from langchain.text_splitter import RecursiveCharacterTextSplitter

splitter = RecursiveCharacterTextSplitter(
    chunk_size=512,
    chunk_overlap=50,
    separators=["\n\n", "\n", "。", "！", "？", ".", " "]
)
chunks = splitter.split_documents(documents)
```

### 元数据提取

元数据增强检索的精确性：

- **基础元数据**：来源、时间、作者、标题
- **语义元数据**：主题、关键词、摘要
- **结构元数据**：章节、层级、引用关系

## 向量数据库

向量数据库是RAG系统的存储和检索核心：

### Milvus

- **特点**：高性能、可扩展、云原生
- **索引类型**：IVF_FLAT、IVF_SQ8、HNSW、ANNOY
- **适用场景**：大规模生产环境
- **部署方式**：Standalone、Cluster、Cloud

### Pinecone

- **特点**：全托管、Serverless、低运维
- **优势**：快速上手、自动扩展
- **适用场景**：快速原型、中小规模应用

### Weaviate

- **特点**：支持混合搜索、GraphQL API
- **优势**：内置向量化、多模态支持
- **适用场景**：需要混合搜索的场景

### Chroma

- **特点**：轻量级、嵌入式、Python原生
- **优势**：简单易用、快速原型
- **适用场景**：本地开发、小规模应用

```python
# Chroma使用示例
import chromadb

client = chromadb.Client()
collection = client.create_collection("my_docs")
collection.add(
    documents=["文档内容1", "文档内容2"],
    ids=["doc1", "doc2"]
)
results = collection.query(query_texts=["查询内容"], n_results=5)
```

### 选型建议

| 场景 | 推荐方案 |
|------|----------|
| 快速原型 | Chroma、FAISS |
| 中小规模生产 | Weaviate、Qdrant |
| 大规模生产 | Milvus、Pinecone |
| 混合搜索 | Weaviate、Elasticsearch |

## Embedding模型选择与微调

### 模型选择

- **通用模型**：text-embedding-3-small（OpenAI）、BGE、E5
- **中文优化**：BGE-zh、M3E、text2vec-chinese
- **多语言模型**：multilingual-e5-large、BGE-M3

### 评估指标

- **检索指标**：Recall@K、MRR、NDCG
- **基准测试**：MTEB、C-MTEB（中文）

### 模型微调

当通用模型无法满足特定领域需求时：

- **对比学习**：使用（query, positive, negative）三元组训练
- **数据来源**：用户点击数据、人工标注、合成数据
- **工具选择**：SentenceTransformers、FlagEmbedding

```python
from sentence_transformers import SentenceTransformer, losses, InputExample

model = SentenceTransformer('BAAI/bge-base-zh-v1.5')
train_examples = [
    InputExample(texts=["查询", "正样本", "负样本"])
]
train_loss = losses.TripletLoss(model)
model.fit(train_objectives=[(train_dataloader, train_loss)], epochs=3)
```

## 检索策略

### Dense Retrieval（稠密检索）

- **原理**：使用embedding模型将查询和文档编码为稠密向量
- **优势**：语义理解强、对同义词友好
- **劣势**：对精确匹配弱、依赖embedding质量

### Sparse Retrieval（稀疏检索）

- **原理**：基于词频的传统检索方法（BM25、TF-IDF）
- **优势**：精确匹配强、无需训练
- **劣势**：语义理解弱、词汇不匹配问题

### Hybrid Retrieval（混合检索）

- **策略**：结合Dense和Sparse检索结果
- **融合方法**：
  - RRF（Reciprocal Rank Fusion）
  - 加权线性组合
  - 学习融合权重

```python
from langchain.retrievers import EnsembleRetriever

ensemble_retriever = EnsembleRetriever(
    retrievers=[bm25_retriever, vector_retriever],
    weights=[0.4, 0.6]
)
```

## 重排序与查询改写

### Reranking（重排序）

对初步检索结果进行精排：

- **Cross-Encoder**：将query和document拼接后编码，精度高但慢
- **Bi-Encoder**：分别编码后计算相似度，快但精度略低
- **常用模型**：bge-reranker、Cohere Rerank、cross-encoder/ms-marco

```python
from sentence_transformers import CrossEncoder

reranker = CrossEncoder('BAAI/bge-reranker-base')
pairs = [[query, doc] for doc in retrieved_docs]
scores = reranker.predict(pairs)
reranked_docs = [doc for _, doc in sorted(zip(scores, retrieved_docs), reverse=True)]
```

### 查询改写（Query Rewriting）

优化用户查询以提高检索质量：

- **查询扩展**：生成多个语义相关的查询
- **查询分解**：将复杂查询分解为子查询
- **HyDE**：生成假设性答案，用答案检索
- **Step-Back Prompting**：生成更高层次的抽象查询

```python
# HyDE示例
def hyde_retrieval(query, llm, retriever):
    hypothetical_answer = llm.generate(f"请回答：{query}")
    results = retriever.retrieve(hypothetical_answer)
    return results
```

## RAG评估

### 评估维度

- **检索质量**：相关文档是否被检索到
- **生成质量**：答案是否准确、完整、流畅
- **端到端质量**：整体回答质量

### RAGAS评估框架

RAGAS提供自动化的RAG评估指标：

- **Faithfulness（忠实度）**：答案是否基于检索内容
- **Answer Relevancy（答案相关性）**：答案是否回答了问题
- **Context Precision（上下文精确度）**：检索内容是否相关
- **Context Recall（上下文召回）**：相关文档是否被检索到

```python
from ragas import evaluate
from ragas.metrics import faithfulness, answer_relevancy

result = evaluate(
    dataset=eval_dataset,
    metrics=[faithfulness, answer_relevancy],
)
```

### TruLens评估

TruLens提供可视化的RAG评估和监控：

- **反馈函数**：可自定义的评估指标
- **追踪记录**：完整的执行链路记录
- **可视化仪表板**：直观的评估结果展示

## 高级优化策略

### 上下文压缩

- **目的**：减少token使用，提高信息密度
- **方法**：LLM压缩、提取式摘要、句级过滤

### 多跳检索（Multi-hop Retrieval）

- **场景**：需要多步推理的复杂问题
- **方法**：迭代检索、自适应检索

### 自适应检索（Adaptive RAG）

- **策略**：根据查询复杂度动态选择检索策略
- **实现**：查询分类 → 策略选择 → 执行检索

## 最佳实践

1. **数据质量优先**：高质量的文档和分块是基础
2. **迭代优化**：从简单开始，逐步引入复杂策略
3. **评估驱动**：建立评估基准，量化改进效果
4. **监控生产**：监控检索质量和用户反馈
5. **成本优化**：平衡效果和成本，合理使用资源

## 总结

RAG系统是LLM应用的核心架构之一，通过将外部知识与生成能力结合，显著扩展了LLM的应用边界。构建高质量的RAG系统需要关注文档处理、检索策略、重排序和评估等每个环节。随着技术发展，RAG正在向更智能的自适应、多模态、多跳推理方向演进。
