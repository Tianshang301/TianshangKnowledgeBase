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

## Contextual Retrieval（上下文检索）

Anthropic提出的上下文检索方案，通过为每个chunk添加上下文信息，解决传统分块丢失上下文的问题。

### 核心思想

传统分块将文档切分为独立片段，丢失了片段间的关联信息。Contextual Retrieval在分块时为每个chunk生成上下文描述，保留其在原文中的语境。

### Contextual Chunking

```python
def contextual_chunking(document, llm):
    """为每个chunk添加上下文前缀"""
    chunks = split_document(document)
    
    contextualized_chunks = []
    for chunk in chunks:
        # 使用LLM生成上下文描述
        context = llm.generate(f"""
        文档内容：{document[:2000]}...
        
        请为以下片段生成简短的上下文说明，解释它在文档中的位置和作用：
        片段：{chunk}
        
        输出格式："这段内容来自...，主要讨论..."
        """)
        
        # 将上下文添加到chunk前面
        contextualized_chunk = f"{context}\n\n{chunk}"
        contextualized_chunks.append(contextualized_chunk)
    
    return contextualized_chunks
```

### 上下文保留策略

- **文档级上下文**：chunk所在文档的主题和背景
- **章节级上下文**：chunk所在章节的核心观点
- **段落级上下文**：前后段落的逻辑关系
- **实体上下文**：chunk中提及实体的定义和背景

### 效果对比

| 方法 | 检索准确率 | 实现复杂度 |
|------|-----------|-----------|
| 传统分块 | 基准 | 低 |
| Contextual Retrieval | +35% | 中 |
| Contextual + BM25 | +49% | 中 |

## Late Chunking（延迟分块）

延迟分块是一种改进的分块策略，先对整个文档进行编码，再进行分块，以获得更好的chunk边界。

### 传统分块的问题

- **边界切割**：在语义完整的内容中间切分
- **上下文丢失**：chunk脱离原文语境
- **嵌入质量差**：短chunk的embedding信息量不足

### Late Chunking流程

```python
def late_chunking(document, chunk_size=512):
    """先编码整个文档，再基于token位置分块"""
    # 1. 对整个文档进行token级编码
    token_embeddings = model.encode_tokens(document)  # [seq_len, dim]
    
    # 2. 基于语义边界确定分块位置
    boundaries = find_semantic_boundaries(document)
    
    # 3. 按边界提取embedding并聚合
    chunks = []
    for start, end in boundaries:
        chunk_emb = token_embeddings[start:end].mean(axis=0)
        chunk_text = document[start:end]
        chunks.append({"text": chunk_text, "embedding": chunk_emb})
    
    return chunks

def find_semantic_boundaries(document):
    """基于语义变化检测分块边界"""
    # 句子级embedding差异
    sentences = split_sentences(document)
    embeddings = model.encode(sentences)
    
    boundaries = [0]
    for i in range(1, len(embeddings)):
        similarity = cosine_similarity(embeddings[i-1], embeddings[i])
        if similarity < 0.5:  # 语义变化阈值
            boundaries.append(i)
    boundaries.append(len(sentences))
    
    return boundaries
```

### 优势

- **完整上下文**：编码时考虑整个文档的语义
- **自然边界**：基于语义变化而非固定长度切分
- **更好的embedding**：长距离依赖被编码到chunk embedding中

## RAG vs Fine-tuning vs Long-context：决策框架

三种扩展LLM知识的方法各有适用场景，需要根据具体需求选择。

### 对比分析

| 维度 | RAG | Fine-tuning | Long-context |
|------|-----|-------------|--------------|
| **知识更新** | 实时（更新文档） | 需要重新训练 | 实时（更新输入） |
| **成本** | 中等 | 高（训练+推理） | 高（长token计费） |
| **延迟** | 低-中 | 低 | 高 |
| **准确性** | 依赖检索质量 | 高（内化知识） | 高（完整上下文） |
| **可解释性** | 高（可追溯来源） | 低 | 中 |
| **适用规模** | 大规模知识库 | 小规模专业领域 | 少量长文档 |

### 决策流程

```
知识量大（>1000文档）→ RAG
需要实时更新 → RAG
需要可追溯来源 → RAG
专业领域且知识稳定 → Fine-tuning
文档少且需要全局理解 → Long-context
预算充足且延迟不敏感 → Long-context
```

### 混合策略

- **RAG + Fine-tuning**：RAG提供外部知识，Fine-tuning提升领域理解
- **RAG + Long-context**：检索到的chunk用长上下文模型处理
- **Fine-tuning + Long-context**：微调模型支持长上下文输入

## RAG 2.0 Patterns（下一代RAG模式）

### Speculative RAG

Speculative RAG借鉴speculative decoding的思想，使用多个轻量级RAG系统并行生成候选答案，然后由主模型选择最优答案。

```python
def speculative_rag(query, main_llm, rag_workers):
    """多个RAG worker并行生成，主模型选择"""
    # 并行执行多个RAG worker
    candidate_answers = []
    for worker in rag_workers:
        docs = worker.retriever.retrieve(query)
        answer = worker.llm.generate(query, docs)
        candidate_answers.append(answer)
    
    # 主模型选择最优答案
    final_answer = main_llm.generate(f"""
    问题：{query}
    
    候选答案：
    {format_candidates(candidate_answers)}
    
    选择最准确、最完整的答案，或综合多个答案。
    """)
    
    return final_answer
```

**优势**：
- 提高答案可靠性
- 并行执行，延迟可控
- 综合多个检索源的结果

### RAG-Fusion

RAG-Fusion通过查询改写和结果融合，提高检索的召回率和多样性。

```python
def rag_fusion(query, llm, retriever, top_k=5):
    """查询改写 + 多路检索 + RRF融合"""
    # 1. 生成多个相关查询
    related_queries = llm.generate(f"""
    为以下查询生成3-5个相关但不同角度的查询：
    原始查询：{query}
    """)
    all_queries = [query] + related_queries
    
    # 2. 对每个查询执行检索
    all_results = []
    for q in all_queries:
        results = retriever.retrieve(q, top_k=top_k)
        all_results.append(results)
    
    # 3. RRF融合排序
    fused_results = reciprocal_rank_fusion(all_results)
    return fused_results[:top_k]

def reciprocal_rank_fusion(result_lists, k=60):
    """RRF融合多个排序列表"""
    scores = {}
    for results in result_lists:
        for rank, doc in enumerate(results):
            if doc.id not in scores:
                scores[doc.id] = 0
            scores[doc.id] += 1 / (k + rank + 1)
    
    return sorted(scores.items(), key=lambda x: x[1], reverse=True)
```

### HyDE（Hypothetical Document Embeddings）

HyDE先让LLM生成假设性答案，然后用这个答案进行检索，而不是直接用用户查询检索。

```python
def hyde_retrieval(query, llm, retriever):
    """生成假设文档 → 编码 → 检索"""
    # 1. 生成假设性答案
    hypothetical_doc = llm.generate(f"""
    请回答以下问题（即使你不确定，也请给出最可能的答案）：
    问题：{query}
    """)
    
    # 2. 用假设答案进行检索
    results = retriever.retrieve(hypothetical_doc)
    
    # 3. 用检索结果生成最终答案
    final_answer = llm.generate(f"""
    基于以下信息回答问题。
    信息：{format_docs(results)}
    问题：{query}
    """)
    
    return final_answer
```

**HyDE的原理**：
- 用户查询通常简短、模糊
- 假设答案更接近文档的表述方式
- 用假设答案检索可以提高语义匹配度

**适用场景**：
- 查询简短或模糊
- 用户不确定如何描述问题
- 需要探索性检索

### 各模式对比

| 模式 | 核心思想 | 优势 | 劣势 |
|------|----------|------|------|
| Speculative RAG | 多worker并行 | 答案可靠性高 | 成本高 |
| RAG-Fusion | 查询改写+融合 | 召回率高 | 多次检索 |
| HyDE | 假设文档检索 | 语义匹配好 | 依赖LLM质量 |

## 总结

RAG系统是LLM应用的核心架构之一，通过将外部知识与生成能力结合，显著扩展了LLM的应用边界。构建高质量的RAG系统需要关注文档处理、检索策略、重排序和评估等每个环节。随着技术发展，RAG正在向更智能的自适应、多模态、多跳推理方向演进。Contextual Retrieval、Late Chunking等新方法不断涌现，Speculative RAG、RAG-Fusion、HyDE等RAG 2.0模式进一步提升了系统能力。在实际应用中，需要根据具体场景在RAG、Fine-tuning和Long-context之间做出合理选择，或采用混合策略以获得最佳效果。
