---
aliases:
  - 知识图谱增强RAG
  - Graph RAG
  - 图检索增强生成
tags:
  - RAG
  - 知识图谱
  - Graph
  - Neo4j
  - 实体关系
  - LLM应用
created: 2026-06-27
updated: 2026-06-27
---

# GraphRAG：知识图谱增强RAG

GraphRAG是将知识图谱（Knowledge Graph）与RAG相结合的技术方案。传统RAG基于向量相似度检索文档片段，会丢失实体间的全局关系和结构化语义。GraphRAG通过构建和查询知识图谱，捕获实体间的复杂关系，实现更深层的语义理解和推理。

## 为什么需要GraphRAG

### 传统RAG的局限性

- **局部性问题**：向量检索返回语义相似的片段，但无法关联跨文档的实体关系
- **缺乏全局视角**：无法回答"整个数据集的主要主题是什么"这类全局性问题
- **推理能力弱**：多跳推理（如"A的合作伙伴的竞争对手是谁"）难以通过相似度检索实现
- **结构信息丢失**：文档中的层级、因果、时序等结构关系在向量化过程中被压缩

### GraphRAG的优势

- **关系建模**：显式建模实体间的多种关系类型
- **全局检索**：通过图结构获取数据集的全局摘要和主题
- **多跳推理**：沿图路径进行多步推理
- **结构化查询**：支持复杂的图遍历和模式匹配

## Microsoft GraphRAG

微软提出的GraphRAG框架，通过社区检测和层次化摘要实现全局检索能力。

### 核心流程

```
文档 → 文本分块 → 实体/关系提取 → 知识图谱构建 → 社区检测 → 社区摘要生成 → 索引构建
```

### 实体与关系提取

使用LLM从文本中提取实体和关系：

```python
# LLM-based实体提取prompt示例
entity_extraction_prompt = """
从以下文本中提取所有实体和它们之间的关系。

实体类型：Person, Organization, Location, Event, Concept
关系类型：works_at, located_in, participates_in, related_to

输出JSON格式：
{
  "entities": [{"name": "...", "type": "...", "description": "..."}],
  "relationships": [{"source": "...", "target": "...", "type": "...", "description": "..."}]
}

文本：{text}
"""
```

### 社区检测：Leiden算法

Leiden算法是层次化社区检测的核心，它将知识图谱划分为不同粒度的社区：

- **原理**：通过模块度优化，迭代地将节点分配到社区中
- **层次结构**：从细粒度社区到粗粒度社区，形成多级结构
- **优势**：比Louvain算法更稳定，避免病态社区划分

```python
import networkx as nx
from cdlib import algorithms

# 构建知识图谱
G = nx.Graph()
G.add_edges_from([("EntityA", "EntityB"), ("EntityB", "EntityC")])

# Leiden社区检测
communities = algorithms.leiden(G)
for community in communities.communities:
    print(f"社区成员: {community}")
```

### 社区摘要

为每个社区生成LLM摘要，作为全局检索的基础：

- **Level 0社区**：最细粒度，包含少量紧密相关的实体
- **Level 1+社区**：逐步聚合，形成更高层次的主题抽象
- **摘要内容**：社区主题、关键实体、主要关系、核心观点

### 检索模式

**Global Search（全局搜索）**：
- 适用于需要全局视角的问题
- 使用所有社区摘要的map-reduce方式
- 问题示例："这个数据集的主要发现是什么？"

**Local Search（局部搜索）**：
- 适用于特定实体相关的问题
- 从目标实体出发，扩展到相关实体和社区
- 问题示例："张三在项目中扮演什么角色？"

```python
# 全局搜索示意
def global_search(query, community_summaries):
    # Map阶段：每个社区摘要独立回答
    partial_answers = []
    for summary in community_summaries:
        answer = llm.generate(f"基于以下社区信息回答问题。\n社区摘要：{summary}\n问题：{query}")
        partial_answers.append(answer)
    
    # Reduce阶段：汇总所有部分答案
    final_answer = llm.generate(f"综合以下回答：\n{partial_answers}\n问题：{query}")
    return final_answer
```

## LightRAG

LightRAG是轻量级GraphRAG实现，采用图索引和双层检索策略。

### 图索引构建

- **实体节点**：文档中提取的命名实体
- **关系边**：实体间的语义关系，附带描述文本
- **关键词索引**：构建实体和关系的关键词倒排索引

### 双层检索

**Low-level Retrieval（底层检索）**：
- 检索具体的实体和关系
- 适用于精确查询："公司A的CEO是谁？"
- 直接从图中查找实体和关系

**High-level Retrieval（高层检索）**：
- 检索抽象主题和概念
- 适用于概括性查询："行业发展趋势是什么？"
- 使用关键词匹配相关主题簇

### 与Microsoft GraphRAG对比

| 维度 | Microsoft GraphRAG | LightRAG |
|------|-------------------|----------|
| 社区检测 | Leiden层次化 | 简单聚类 |
| 全局搜索 | 社区摘要map-reduce | 关键词主题检索 |
| 资源消耗 | 高（大量LLM调用） | 低 |
| 适用规模 | 大规模数据集 | 中小规模数据集 |

## 实体提取Pipeline

### LLM-based NER

```python
async def extract_entities(text_chunk, llm_client):
    response = await llm_client.chat(
        model="gpt-4o",
        messages=[{
            "role": "system",
            "content": "你是实体提取专家。从文本中提取所有命名实体，包括人名、组织、地点、概念、事件。"
        }, {
            "role": "user",
            "content": f"提取以下文本中的实体：\n{text_chunk}"
        }],
        response_format={"type": "json_object"}
    )
    return parse_entities(response)
```

### 关系提取

- **显式关系**：文本中明确表述的关系（"A是B的CEO"）
- **隐式关系**：需要LLM推理的关系（A和B在同一项目中出现）
- **关系合并**：跨文档的相同实体对关系合并和去重

### 图谱构建与去重

- **实体对齐**：将不同表述的同一实体合并（"苹果公司" = "Apple" = "AAPL"）
- **关系归一化**：统一关系类型表述
- **增量更新**：新文档增量添加到已有图谱

## 图存储方案

### Neo4j

- **特点**：原生图数据库，Cypher查询语言
- **优势**：成熟的图遍历优化，丰富的图算法库
- **适用**：生产环境，复杂图查询

```cypher
// Cypher查询示例：查找实体A的2跳邻居
MATCH (a:Entity {name: "实体A"})-[r*1..2]-(related)
RETURN related.name, type(r[0])
```

### NebulaGraph

- **特点**：分布式图数据库，高可用
- **优势**：水平扩展能力强，适合大规模图谱
- **适用**：超大规模知识图谱

### NetworkX（内存图）

- **特点**：Python图计算库，内存存储
- **优势**：开发便捷，与Python生态无缝集成
- **适用**：原型开发、小规模图谱、图算法研究

```python
import networkx as nx

G = nx.DiGraph()
G.add_edge("公司A", "公司B", relation="合作伙伴")
G.add_edge("公司B", "公司C", relation="竞争对手")

# 查找最短路径
path = nx.shortest_path(G, "公司A", "公司C")
```

## 检索策略

### 子图提取

- **目标实体扩展**：从查询中的实体出发，提取K跳子图
- **关系过滤**：只保留与查询相关的关系类型
- **子图摘要**：LLM对子图进行自然语言摘要

### 图遍历

- **BFS遍历**：广度优先获取相关实体，适合局部搜索
- **个性化PageRank**：计算实体重要性，用于排序
- **随机游走**：采样多样化的实体集合

### 路径推理

- **最短路径**：查找两个实体间的关系链
- **多路径分析**：发现实体间的多种关联方式
- **路径推理**：LLM沿路径进行推理

## GraphRAG vs 向量RAG vs 混合方案

| 维度 | 向量RAG | GraphRAG | 混合方案 |
|------|---------|----------|----------|
| 关系建模 | 弱 | 强 | 强 |
| 全局检索 | 弱 | 强 | 强 |
| 实现复杂度 | 低 | 高 | 中 |
| 索引构建成本 | 低 | 高 | 中 |
| 查询延迟 | 低 | 中 | 中 |
| 适用场景 | 文档QA | 关系推理 | 通用 |

### 混合方案推荐

```
用户查询 → 查询分类器
    ├─ 实体/关系查询 → GraphRAG
    ├─ 语义相似查询 → 向量RAG
    └─ 复合查询 → GraphRAG + 向量RAG → 结果融合
```

## 典型应用场景

### 法律文档分析

- **实体**：法条、案例、当事人、法院
- **关系**：引用、适用、判决
- **查询**："哪些案例引用了某法条？判决结果如何？"

### 医疗记录管理

- **实体**：患者、疾病、药物、症状
- **关系**：诊断、治疗、副作用、禁忌
- **查询**："某药物的禁忌症有哪些？哪些患者需要特别注意？"

### 金融分析

- **实体**：公司、高管、产品、事件
- **关系**：投资、竞争、供应链、监管
- **查询**："某公司的供应链上下游关系？受监管政策影响的有哪些？"

### 科学文献

- **实体**：研究者、论文、机构、方法
- **关系**：引用、合作、改进、对比
- **查询**："某方法的改进版本有哪些？哪些研究者有合作关系？"

## 性能优化

### 批量实体提取

```python
async def batch_extract_entities(text_chunks, llm_client, batch_size=10):
    """批量处理文档chunks，减少API调用"""
    all_entities = []
    all_relations = []
    
    for i in range(0, len(text_chunks), batch_size):
        batch = text_chunks[i:i + batch_size]
        tasks = [extract_entities(chunk, llm_client) for chunk in batch]
        results = await asyncio.gather(*tasks)
        
        for entities, relations in results:
            all_entities.extend(entities)
            all_relations.extend(relations)
    
    # 全局去重
    unique_entities = deduplicate_entities(all_entities)
    unique_relations = deduplicate_relations(all_relations)
    
    return unique_entities, unique_relations
```

### 增量图谱更新

```python
class IncrementalGraphBuilder:
    def __init__(self, graph_store):
        self.graph = graph_store
        self.entity_index = {}  # entity_name -> node_id
    
    def add_document(self, doc_id, entities, relations):
        """增量添加文档的实体和关系"""
        node_ids = {}
        
        for entity in entities:
            if entity.name in self.entity_index:
                # 已存在，更新属性
                node_id = self.entity_index[entity.name]
                self.graph.update_node(node_id, entity.properties)
            else:
                # 新实体，创建节点
                node_id = self.graph.add_node(entity)
                self.entity_index[entity.name] = node_id
            node_ids[entity.name] = node_id
        
        for rel in relations:
            source_id = node_ids.get(rel.source)
            target_id = node_ids.get(rel.target)
            if source_id and target_id:
                self.graph.add_edge(source_id, target_id, rel.type, rel.properties)
```

### 查询缓存

```python
class GraphQueryCache:
    def __init__(self, ttl=3600):
        self.cache = {}
        self.ttl = ttl
    
    def get_subgraph(self, entity_name, hops=2):
        cache_key = f"{entity_name}:{hops}"
        if cache_key in self.cache:
            result, timestamp = self.cache[cache_key]
            if time.time() - timestamp < self.ttl:
                return result
        
        # 缓存未命中，查询图数据库
        subgraph = self.graph.get_neighbors(entity_name, hops)
        self.cache[cache_key] = (subgraph, time.time())
        return subgraph
```

## 评估指标

### 图谱质量指标

- **覆盖率**：文档中的实体被提取的比例
- **准确率**：提取的实体和关系的正确率
- **对齐率**：同一实体的不同表述被正确合并的比例

### 检索质量指标

- **实体检索召回率**：相关实体被检索到的比例
- **关系检索准确率**：检索到的关系与查询相关的比例
- **答案忠实度**：生成答案是否基于图谱中的事实

```python
def evaluate_graph_rag(test_queries, ground_truth, graph_rag):
    """评估GraphRAG系统"""
    results = {
        "entity_recall": [],
        "relation_precision": [],
        "answer_faithfulness": []
    }
    
    for query, expected in zip(test_queries, ground_truth):
        answer, retrieved_entities, retrieved_relations = graph_rag.query(query)
        
        # 计算实体召回率
        entity_recall = len(set(retrieved_entities) & set(expected["entities"])) / len(expected["entities"])
        results["entity_recall"].append(entity_recall)
        
        # 计算关系准确率
        correct_relations = len(set(retrieved_relations) & set(expected["relations"]))
        if retrieved_relations:
            results["relation_precision"].append(correct_relations / len(retrieved_relations))
    
    return {k: np.mean(v) for k, v in results.items()}
```

## 实践建议

1. **从小开始**：先用LightRAG验证GraphRAG对场景的价值，再考虑完整方案
2. **提取质量是关键**：实体和关系提取的准确度直接影响GraphRAG效果
3. **评估驱动**：对比GraphRAG和向量RAG在具体查询上的效果差异
4. **成本意识**：GraphRAG索引构建需要大量LLM调用，需要评估成本效益
5. **增量维护**：建立增量更新机制，避免每次全量重建图谱
6. **混合使用**：GraphRAG和向量RAG不是互斥的，结合使用效果更佳