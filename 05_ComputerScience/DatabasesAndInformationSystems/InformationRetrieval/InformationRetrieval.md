---
aliases: [InformationRetrieval]
tags: ['DatabasesAndInformationSystems', 'InformationRetrieval', 'InformationRetrieval']
created: 2026-05-16
updated: 2026-05-13
---

# Information Retrieval - 信息检索

## 一、信息检索基础

信息检索（Information Retrieval, IR）是从大规模非结构化文档集合中找出满足用户信息需求内容的过程。

### 核心任务

| 任务类型 | 说明 | 示例 |
|---------|------|------|
| **Ad-hoc 检索** | 用户提交查询，系统返回相关文档 | 搜索引擎 |
| **过滤** | 根据用户兴趣画像推送新文档 | 推荐系统 |
| **问答** | 直接返回精确答案而非文档列表 | 智能问答 |
| **聚类** | 自动将文档分组 | 主题发现 |
| **分类** | 将文档分到预定义类别 | 垃圾邮件识别 |

---

## 二、布尔检索模型

文档表示为词项集合，查询使用布尔运算符（AND, OR, NOT）连接词项。

```
查询: "iran" AND "nuclear" AND NOT "weapon"
结果: 包含 "iran" 和 "nuclear" 但不包含 "weapon" 的文档
```

**倒排索引**（Inverted Index）是布尔检索的核心数据结构：

```
词项 → 文档列表
─────────────────
"database"  → doc1, doc3, doc5
"index"     → doc1, doc2, doc4
"search"    → doc2, doc3, doc5
"query"     → doc3, doc4
```

| 优点 | 缺点 |
|------|------|
| 简单高效，完全精确 | 无排序能力，匹配无法衡量相关性 |
| 适合结构化数据 | 查询表达受限，不支持近似匹配 |
| 响应速度快 | 长查询效率低 |

---

## 三、向量空间模型

文档和查询均表示为向量，通过余弦相似度衡量相关性。

### TF-IDF 权重

TF-IDF（词频-逆文档频率）是信息检索中最经典的权重计算方案：

$$ \text{tfidf}_{t,d} = \text{tf}_{t,d} \times \log\frac{N}{\text{df}_t} $$

其中：
- $\text{tf}_{t,d}$：词项 $t$ 在文档 $d$ 中的频率
- $\text{df}_t$：包含词项 $t$ 的文档数（文档频率）
- $N$：文档集合总数

**TF-IDF 加权变体**：

| 变体 | TF | IDF |
|------|----|-----|
| 原始 | $\text{tf}_{t,d}$ | $\log(N/\text{df}_t)$ |
| 对数 | $1 + \log(\text{tf}_{t,d})$ | $\log(N/\text{df}_t)$ |
| 归一化 | $0.5 + 0.5 \cdot \frac{\text{tf}_{t,d}}{\max_t \text{tf}_{t,d}}$ | $\log(N/\text{df}_t)$ |
| 概率 | $\text{tf}_{t,d}$ | $\log((N - \text{df}_t) / \text{df}_t)$ |

```python
import math
from collections import Counter

def compute_tfidf(documents, query):
    """计算文档集合的 TF-IDF"""
    N = len(documents)
    doc_count = Counter()
    doc_vectors = []

    for doc in documents:
        terms = doc.lower().split()
        tf = Counter(terms)
        for term in tf:
            doc_count[term] += 1

    for doc in documents:
        terms = doc.lower().split()
        tf = Counter(terms)
        vector = {}
        for term, freq in tf.items():
            idf = math.log(N / doc_count[term])
            vector[term] = freq * idf
        doc_vectors.append(vector)

    return doc_vectors
```

### 余弦相似度

$$ \cos(\vec{q},\vec{d}) = \frac{\vec{V}(q) \cdot \vec{V}(d)}{\|\vec{V}(q)\| \times \|\vec{V}(d)\|} = \frac{\sum_{t} w_{t,q} \times w_{t,d}}{\sqrt{\sum_{t} w_{t,q}^2} \times \sqrt{\sum_{t} w_{t,d}^2}} $$

其中 $w_{t,q}$ 和 $w_{t,d}$ 分别为词项 $t$ 在查询和文档中的权重。

```python
def cosine_similarity(vec_q, vec_d):
    """计算两个向量间的余弦相似度"""
    dot_product = sum(vec_q.get(t, 0) * vec_d.get(t, 0) for t in set(vec_q) | set(vec_d))
    norm_q = math.sqrt(sum(v ** 2 for v in vec_q.values()))
    norm_d = math.sqrt(sum(v ** 2 for v in vec_d.values()))
    return dot_product / (norm_q * norm_d) if norm_q and norm_d else 0
```

---

## 四、概率检索模型 — BM25

BM25 是当前最主流的检索函数之一，基于概率检索框架改进而来：

$$ \text{score}(d, q) = \sum_{t \in q} \log\frac{(r_t + 0.5)/(R - r_t + 0.5)}{(df_t - r_t + 0.5)/(N - df_t - R + r_t + 0.5)} \times \frac{(k_1 + 1) \times tf_{t,d}}{k_1 \times (1 - b + b \times \frac{|d|}{\text{avgdl}}) + tf_{t,d}} $$

其中：
- $N$：总文档数
- $df_t$：包含词项 $t$ 的文档数
- $R$：相关文档数
- $r_t$：相关文档中包含 $t$ 的文档数
- $k_1$：饱和控制参数（通常 1.2~2.0）
- $b$：长度归一化参数（通常 0.75）

| 模型 | 核心思想 | 优点 | 缺点 |
|------|---------|------|------|
| **Boolean** | 集合论 | 简洁快速 | 无排序 |
| **VSM** | 向量+余弦 | 排序好，实现简单 | 未标准化 |
| **BM25** | 概率模型 | 鲁棒性强，效果好 | 参数需调优 |

---

## 五、评估指标

### 混淆矩阵

```
              实际相关    实际不相关
检索到          TP         FP
未检索到        FN         TN
```

### 核心指标

$$ \text{Precision} = \frac{TP}{TP + FP} \quad \text{Recall} = \frac{TP}{TP + FN} $$

$$ F_1 = \frac{2 \times P \times R}{P + R} $$

| 指标 | 说明 | 公式 |
|------|------|------|
| **Precision（精确率）** | 检索结果中相关文档的比例 | TP / (TP + FP) |
| **Recall（召回率）** | 相关文档中被检索到的比例 | TP / (TP + FN) |
| **MAP** | 平均精度均值，对所有查询取平均 | $\frac{1}{Q} \sum_{q=1}^{Q} \text{AveP}(q)$ |
| **NDCG** | 归一化折损累计增益，考虑排序位置 | $\frac{DCG}{IDCG}$ |
| **RR** | 倒数排名，第一个相关结果位置的倒数 | $1 / \text{rank}_1$ |

```python
def average_precision(relevant, retrieved):
    """计算一个查询的平均精度（AP）"""
    hits = 0
    sum_precision = 0
    for i, doc in enumerate(retrieved):
        if doc in relevant:
            hits += 1
            sum_precision += hits / (i + 1)
    return sum_precision / len(relevant) if relevant else 0

def ndcg(relevance_scores, k=10):
    """计算 NDCG@k"""
    dcg = sum((2 ** rel - 1) / math.log2(i + 2)
              for i, rel in enumerate(relevance_scores[:k]))
    ideal = sorted(relevance_scores, reverse=True)
    idcg = sum((2 ** rel - 1) / math.log2(i + 2)
               for i, rel in enumerate(ideal[:k]))
    return dcg / idcg if idcg > 0 else 0
```

---

## 六、倒排索引构建与压缩

### 索引构建

```
文档集合 → Tokenization → 词项化 → 语言学处理 → 倒排索引
                                  ↓
                              Stemming/Lemmatization
```

```python
def build_inverted_index(documents):
    """构建倒排索引"""
    index = {}
    for doc_id, doc in enumerate(documents):
        terms = doc.lower().split()
        for pos, term in enumerate(terms):
            if term not in index:
                index[term] = []
            if not index[term] or index[term][-1][0] != doc_id:
                index[term].append([doc_id, []])
            index[term][-1][1].append(pos)
    return index
```

### 压缩技术

| 技术 | 方法 | 效果 |
|------|------|------|
| **变长编码** | Variable Byte Encoding | 减少空间 30~50% |
| **差分编码** | 存储 docID 差值而非绝对值 | 空间大幅降低 |
| **位图压缩** | Bitmap + Run-length Encoding | 适合稠密索引 |
| **字典压缩** | 前端编码、字典指针 | 减少词典大小 |

---

## 七、查询扩展

### Rocchio 算法

基于用户反馈调整查询向量：

$$ \vec{q}_{\text{new}} = \alpha \vec{q}_{\text{original}} + \beta \frac{1}{|D_r|} \sum_{\vec{d} \in D_r} \vec{d} - \gamma \frac{1}{|D_{nr}|} \sum_{\vec{d} \in D_{nr}} \vec{d} $$

### 伪相关反馈（Pseudo-Relevance Feedback）

1. 执行初始查询，获取 top-k 文档
2. 假设这些文档是相关的
3. 从中提取新的词项加入查询
4. 执行扩展后的查询

---

## 八、学习排序（Learning to Rank）

### 三种范式

```text
Pointwise: 将排序问题转化为回归/分类问题
   输入：单个文档特征 → 输出：相关性得分
   损失：MSE, Cross-entropy

Pairwise: 将排序问题转化为二分类（文档对）
   输入：文档对 (d_i, d_j) → 输出：哪个更相关
   损失：Pairwise loss (RankNet, RankSVM)

Listwise: 直接优化排序列表
   输入：文档列表 → 输出：排列顺序
   损失：ListMLE, LambdaRank (NDCG 优化)
```

| 方法 | 复杂度 | 排序效果 | 代表算法 |
|------|--------|---------|---------|
| Pointwise | 低 | 一般 | McRank |
| Pairwise | 中 | 较好 | RankNet, LambdaRank |
| Listwise | 高 | 最好 | ListNet, ListMLE |

---

## 九、Web 搜索

### 爬虫（Crawler）

```
URL Frontier → DNS 解析 → 下载 → 解析 → 存储 → 提取链接 → 去重 → 加入队列
                ↑                                          │
                └──────────────────────────────────────────┘
```

### PageRank 算法

$$ PR(p_i) = \frac{1-d}{N} + d \sum_{p_j \in M(p_i)} \frac{PR(p_j)}{L(p_j)} $$

其中：
- $PR(p_i)$：页面 $p_i$ 的 PageRank 值
- $d$：阻尼因子（通常 0.85）
- $M(p_i)$：链接到 $p_i$ 的页面集合
- $L(p_j)$：页面 $p_j$ 的出链数量
- $N$：总页面数

**锚文本（Anchor Text）**：指向某个页面的链接文本，为被链接页面提供重要描述信息。

```python
def pagerank(graph, d=0.85, max_iter=100, tol=1e-6):
    """PageRank 迭代计算"""
    N = len(graph)
    pr = {node: 1 / N for node in graph}
    out_degree = {node: len(neighbors) for node, neighbors in graph.items()}

    for _ in range(max_iter):
        new_pr = {}
        for node in graph:
            incoming_pr = sum(pr[src] / out_degree[src]
                             for src, neighbors in graph.items()
                             if node in neighbors)
            new_pr[node] = (1 - d) / N + d * incoming_pr

        if sum(abs(new_pr[n] - pr[n]) for n in graph) < tol:
            break
        pr = new_pr

    return pr
```

---

## 十、推荐系统

### 协同过滤（Collaborative Filtering）

```text
User-based: 找相似用户 → 推荐他们喜欢的物品
Item-based: 找相似物品 → 推荐用户喜欢的物品的同类
```

$$ \text{pred}(u, i) = \bar{r}_u + \frac{\sum_{v \in N(u)} \text{sim}(u, v) \times (r_{v,i} - \bar{r}_v)}{\sum_{v \in N(u)} |\text{sim}(u, v)|} $$

### 基于内容（Content-Based）

推荐与用户历史中喜欢的物品具有相似特征的物品。

### 混合推荐（Hybrid）

| 混合方式 | 说明 |
|---------|------|
| 加权混合 | 加权组合多个推荐结果 |
| 切换混合 | 根据场景选择不同算法 |
| 级联混合 | 一个算法的输出作为另一个的输入 |
| 特征融合 | 将不同来源的特征合并到一个模型 |

## 相关条目

- [[搜索引擎原理与实践]]
- [[RelationalDatabases]]
- [[NoSQL]]
- [[BigDataTechnologies]]
- [[流处理与实时计算]]

## 参考资源

- Manning, C. D., Raghavan, P., & Schütze, H. (2008). Introduction to Information Retrieval. Cambridge University Press.
- Brin, S. & Page, L. (1998). The Anatomy of a Large-Scale Hypertextual Web Search Engine. WWW.
- Robertson, S. & Zaragoza, H. (2009). The Probabilistic Relevance Framework: BM25 and Beyond. Foundations and Trends in IR.
- Burges, C. J. C. (2010). From RankNet to LambdaRank to LambdaMART: An Overview. MSR-TR.
- Ricci, F., Rokach, L., & Shapira, B. (2015). Recommender Systems Handbook. Springer.
