---
aliases:
  - RAG生产实践
  - RAG Production Patterns
  - RAG工程化
  - RAG部署
tags:
  - RAG
  - MLOps
  - 生产部署
  - 缓存
  - 监控
  - 性能优化
created: 2026-06-27
updated: 2026-06-27
---

# RAG生产实践

RAGProductionPatterns聚焦RAG系统从原型到生产的关键工程实践。涵盖缓存策略、成本优化、延迟管理、监控告警、A/B测试等生产环境必须考虑的工程问题，以及长上下文模型与RAG的取舍决策。

## Caching Strategies（缓存策略）

### 语义缓存

语义缓存根据查询的语义（而非精确匹配）判断是否命中缓存：

```python
import numpy as np
from sentence_transformers import SentenceTransformer

class SemanticCache:
    def __init__(self, similarity_threshold=0.92):
        self.encoder = SentenceTransformer("all-MiniLM-L6-v2")
        self.cache = {}  # {embedding: (query, answer, timestamp)}
        self.threshold = similarity_threshold
    
    def get(self, query):
        query_emb = self.encoder.encode(query)
        
        best_score = 0
        best_answer = None
        
        for cached_emb, (cached_query, answer, ts) in self.cache.items():
            score = np.dot(query_emb, cached_emb) / (
                np.linalg.norm(query_emb) * np.linalg.norm(cached_emb)
            )
            if score > best_score:
                best_score = score
                best_answer = answer
        
        if best_score >= self.threshold:
            return best_answer, best_score
        return None, best_score
    
    def set(self, query, answer):
        emb = tuple(self.encoder.encode(query))
        self.cache[emb] = (query, answer, time.time())
```

**语义缓存的优势**：
- 语义相似的问题共享答案（如"北京天气"和"北京今天天气怎么样"）
- 减少LLM调用，降低成本和延迟

**阈值设定**：
- 太高（>0.95）：缓存命中率低
- 太低（<0.85）：缓存错误率高
- 建议：从0.92开始，根据实际效果调整

### 精确匹配缓存

```python
from functools import lru_cache
from hashlib import md5

class ExactCache:
    def __init__(self, ttl=3600):
        self.cache = {}
        self.ttl = ttl
    
    def _key(self, query, context_hash):
        return md5(f"{query}:{context_hash}".encode()).hexdigest()
    
    def get(self, query, context_hash):
        key = self._key(query, context_hash)
        if key in self.cache:
            answer, timestamp = self.cache[key]
            if time.time() - timestamp < self.ttl:
                return answer
            del self.cache[key]
        return None
    
    def set(self, query, context_hash, answer):
        key = self._key(query, context_hash)
        self.cache[key] = (answer, time.time())
```

### Embedding缓存

避免重复计算embedding：

```python
class EmbeddingCache:
    def __init__(self, embedding_model):
        self.model = embedding_model
        self.cache = {}
    
    def encode(self, texts):
        uncached = []
        uncached_idx = []
        results = [None] * len(texts)
        
        for i, text in enumerate(texts):
            if text in self.cache:
                results[i] = self.cache[text]
            else:
                uncached.append(text)
                uncached_idx.append(i)
        
        if uncached:
            new_embeddings = self.model.encode(uncached)
            for idx, emb in zip(uncached_idx, new_embeddings):
                results[idx] = emb
                self.cache[uncached[idx - uncached_idx[0]]] = emb
        
        return results
```

### 缓存失效策略

- **TTL失效**：固定过期时间
- **LRU淘汰**：最近最少使用
- **版本失效**：数据更新时清除相关缓存
- **手动失效**：支持主动清除特定缓存

## Cost Optimization（成本优化）

### 分层检索

根据查询复杂度使用不同成本的检索策略：

```python
class TieredRetriever:
    def __init__(self):
        self.tiers = [
            {"name": "cache", "cost": 0, "retriever": semantic_cache},
            {"name": "sparse", "cost": 0.001, "retriever": bm25_retriever},
            {"name": "dense", "cost": 0.01, "retriever": vector_retriever},
            {"name": "rerank", "cost": 0.05, "retriever": reranker}
        ]
    
    def retrieve(self, query, max_cost=0.02):
        results = []
        accumulated_cost = 0
        
        for tier in self.tiers:
            if accumulated_cost + tier["cost"] > max_cost:
                break
            
            result = tier["retriever"].retrieve(query)
            accumulated_cost += tier["cost"]
            
            if self.is_sufficient(result):
                return result
            results.append(result)
        
        return self.merge_results(results)
```

### 模型路由

根据任务复杂度选择不同成本的模型：

```python
class ModelRouter:
    def __init__(self):
        self.models = {
            "cheap": {"model": "gpt-4o-mini", "cost_per_1k": 0.00015},
            "medium": {"model": "gpt-4o", "cost_per_1k": 0.005},
            "expensive": {"model": "claude-3.5-sonnet", "cost_per_1k": 0.015}
        }
    
    def route(self, query_complexity):
        if query_complexity == "simple":
            return self.models["cheap"]
        elif query_complexity == "medium":
            return self.models["medium"]
        else:
            return self.models["expensive"]
```

### 批处理优化

```python
async def batch_embed(texts, batch_size=100):
    """批量embedding，减少API调用次数"""
    all_embeddings = []
    for i in range(0, len(texts), batch_size):
        batch = texts[i:i + batch_size]
        embeddings = await embedding_model.abatch_encode(batch)
        all_embeddings.extend(embeddings)
    return all_embeddings
```

## Latency Management（延迟管理）

### 异步检索

```python
import asyncio

async def async_retrieve(query, retrievers):
    """并行执行多个检索器"""
    tasks = [retriever.aretrieve(query) for retriever in retrievers]
    results = await asyncio.gather(*tasks)
    return merge_results(results)
```

### 流式生成

```python
async def stream_rag_response(query, retriever, llm):
    """流式RAG响应"""
    # 先检索
    docs = await retriever.aretrieve(query)
    context = format_context(docs)
    
    # 流式生成
    async for chunk in llm.astream(f"基于以下信息回答：\n{context}\n问题：{query}"):
        yield chunk
```

### 预取（Pre-fetching）

```python
class PrefetchRetriever:
    def __init__(self, retriever, prediction_model):
        self.retriever = retriever
        self.predictor = prediction_model
        self.prefetch_cache = {}
    
    async def prefetch_for_user(self, user_context):
        """基于用户上下文预测可能的查询并预取"""
        predicted_queries = self.predictor.predict(user_context)
        for query in predicted_queries:
            if query not in self.prefetch_cache:
                docs = await self.retriever.aretrieve(query)
                self.prefetch_cache[query] = docs
    
    async def retrieve(self, query):
        if query in self.prefetch_cache:
            return self.prefetch_cache.pop(query)
        return await self.retriever.aretrieve(query)
```

## Monitoring（监控）

### 检索质量指标

```python
class RetrievalMetrics:
    def __init__(self):
        self.metrics = {
            "latency": [],
            "relevance_scores": [],
            "cache_hit_rate": 0,
            "total_queries": 0
        }
    
    def log_query(self, query, results, latency, relevance_score):
        self.metrics["latency"].append(latency)
        self.metrics["relevance_scores"].append(relevance_score)
        self.metrics["total_queries"] += 1
    
    def get_p95_latency(self):
        return np.percentile(self.metrics["latency"], 95)
    
    def get_avg_relevance(self):
        return np.mean(self.metrics["relevance_scores"])
```

### 漂移检测

```python
class DriftDetector:
    def __init__(self, reference_distribution):
        self.reference = reference_distribution
    
    def detect(self, current_distribution):
        """检测查询分布漂移"""
        kl_divergence = self._kl_divergence(self.reference, current_distribution)
        return kl_divergence > self.threshold
```

### 反馈循环

```python
class FeedbackCollector:
    def __init__(self, db):
        self.db = db
    
    def collect_feedback(self, query_id, feedback_type, feedback_value):
        """收集用户反馈"""
        self.db.insert({
            "query_id": query_id,
            "feedback_type": feedback_type,  # "thumbs_up", "thumbs_down", "rating"
            "feedback_value": feedback_value,
            "timestamp": datetime.now()
        })
    
    def get_negative_feedback_queries(self, limit=100):
        """获取差评查询用于分析"""
        return self.db.query(
            "feedback_type = 'thumbs_down'",
            limit=limit
        )
```

## A/B Testing

### 检索策略对比

支持策略A/B分流测试，基于用户ID分流保证一致性，评估指标包括检索质量和用户满意度。

## Long-context vs RAG

### 决策框架

| 维度 | 长上下文（128K/1M） | RAG |
|------|-------------------|-----|
| **成本** | 高（所有token计费） | 低（只检索相关片段） |
| **延迟** | 高（处理全部token） | 低（少量token） |
| **准确性** | 高（完整上下文） | 中等（依赖检索质量） |
| **适用文档量** | 少量长文档 | 大量文档 |
| **实现复杂度** | 低 | 高 |

### 何时使用长上下文

- **文档数量少**：1-5个文档，总token数在模型限制内
- **需要全局理解**：需要理解文档整体结构和逻辑
- **简单实现**：不值得构建复杂RAG系统
- **准确度要求高**：不能接受检索遗漏

### 何时使用RAG

- **文档数量大**：成千上万的文档库
- **成本敏感**：需要控制token使用成本
- **延迟敏感**：需要快速响应
- **动态文档**：文档库频繁更新

### 混合策略

根据文档总量动态选择：文档总量在上下文窗口内直接使用长上下文，否则使用RAG检索。也可结合两种方式，先用RAG缩小范围再用长上下文处理。

## Structured Data RAG（结构化数据RAG）

### Text-to-SQL

```python
class TextToSQLRAG:
    def __init__(self, llm, db_connection):
        self.llm = llm
        self.db = db_connection
    
    def query(self, natural_language_query):
        # 获取数据库schema
        schema = self.db.get_schema()
        
        # 生成SQL
        sql = self.llm.generate(f"""
        数据库Schema：{schema}
        
        将以下自然语言查询转换为SQL：
        {natural_language_query}
        
        只输出SQL语句。
        """)
        
        # 执行SQL
        results = self.db.execute(sql)
        return results
```

### 表格检索

```python
class TableRetriever:
    def __init__(self, tables_metadata, embedding_model):
        self.metadata = tables_metadata
        self.encoder = embedding_model
        self.table_embeddings = self._encode_tables()
    
    def retrieve(self, query, top_k=3):
        query_emb = self.encoder.encode(query)
        scores = self._compute_similarity(query_emb, self.table_embeddings)
        top_indices = np.argsort(scores)[-top_k:][::-1]
        return [self.metadata[i] for i in top_indices]
```

## Production Architecture（生产架构）

### RAG编排框架

使用LangChain LCEL构建可组合的RAG Chain：`retriever | format_docs` 作为上下文，配合 `prompt_template | llm | StrOutputParser` 形成完整链路。通过 `RunnableLambda` 添加监控和日志。

### 可观测性

**LangSmith集成**：设置环境变量 `LANGCHAIN_TRACING_V2=true` 和 `LANGCHAIN_API_KEY`，使用 `@traceable` 装饰器自动追踪RAG链路。

**Phoenix可观测性**：使用 `phoenix.launch_app()` 启动本地追踪，通过 `phoenix.otel.register()` 注册项目。

### 生产部署清单

1. **缓存层**：语义缓存 + 精确缓存
2. **限流**：API调用限流，防止过载
3. **降级策略**：检索失败时的fallback方案
4. **监控告警**：延迟、错误率、缓存命中率告警
5. **日志记录**：完整的查询和响应日志
6. **A/B测试框架**：支持策略对比实验
7. **反馈收集**：用户反馈机制

## 最佳实践

1. **渐进式优化**：从简单RAG开始，逐步引入缓存、分层、路由等优化
2. **监控先行**：先建立监控，再优化，用数据驱动决策
3. **成本意识**：每个优化都要评估成本收益
4. **用户反馈**：建立反馈机制，持续改进
5. **文档化**：记录架构决策和优化策略，便于团队协作