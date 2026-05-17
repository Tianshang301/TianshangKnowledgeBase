---
aliases: [MappingsAndIndices, 映射与索引, ClassificationMappings, IndexingTechniques]
tags: ['ClassificationMappings', 'MappingsAndIndices', 'Indexing', 'InformationRetrieval', 'KnowledgeOrganization']
---

# 映射与索引技术指南（Mappings and Indices）

本文涵盖信息检索、数据库索引、知识映射和图索引四大领域，系统梳理索引构建、压缩、匹配与检索的核心技术。

## 一、索引基础

### 1.1 信息检索索引

**倒排索引（Inverted Index）** 是信息检索系统的核心数据结构，将文档集合映射为词项 → 文档列表的映射关系。

$$ \text{倒排索引}: \text{词项 } t \rightarrow \{\langle d_1, \text{pos}_{1,1}, \text{pos}_{1,2}, \ldots \rangle, \langle d_2, \ldots \rangle, \ldots\} $$

| 组件 | 描述 | 示例 |
|------|------|------|
| 词典（Dictionary） | 所有词项的集合 | {apple, banana, cat, ...} |
| 倒排列表（Posting List） | 每个词项对应的文档列表 | apple → [doc1, doc3, doc7] |
| 跳跃指针（Skip Pointers） | 加速列表合并的索引指针 | doc1 → 跳至 doc5 |

**倒排索引构建**：

```
文档集 → 分词(Tokenization) → 词项归一化(Normalization)
    → 词项-文档ID对 → 排序 → 合并 → 写入磁盘
```

### 1.2 索引构建算法

| 算法 | 原理 | 内存需求 | 磁盘 I/O | 适用场景 |
|:----:|------|:--------:|:--------:|---------|
| BSBI | 块排序，分块排序后合并 | 可控（块大小） | 高 | 大规模静态集合 |
| SPIMI | 单遍内存索引，词项按 ID 排序 | 灵活 | 中 | 大规模流式处理 |
| MapReduce | 分布式 map + reduce | 分布式 | 网络 I/O | TB/PB 级数据 |

**BSBI（Blocked Sort-Based Indexing）**：

1. 将文档集分割为大小相等的块
2. 每块在内存中构建倒排索引并排序
3. 将排序后的倒排列表写入临时文件
4. 多路合并临时文件为最终索引

$$ \text{BSBI 时间复杂度 } O(T \log T), \quad T = \text{词项-文档对总数} $$

**SPIMI（Single-Pass In-Memory Indexing）**：

1. 逐块处理文档，在内存中维护词项 → 倒排列表映射
2. 词典使用哈希表或 Trie，无需全局排序
3. 每块达到阈值后写入临时文件
4. 最终合并时按词项 ID 排序合并

### 1.3 索引压缩技术

**词典压缩**：

| 方法 | 原理 | 压缩率 | 解码速度 |
|:----:|------|:------:|:--------:|
| 前端编码（Front Coding） | 共享前缀压缩 | 高（20-30%） | 慢 |
| 阻塞（Blocking） | 按块存储，块内无分隔 | 中 | 中 |
| 字典编码（Dictionary Encoding） | Token → 整数映射 | 高 | 快 |

**倒排列表压缩**：

| 编码 | 原理 | 压缩率 | 解码速度 | 适用场景 |
|:----:|------|:------:|:--------:|---------|
| 可变字节编码（VByte） | 每个字节 7 位数据 + 1 位标记 | 中 | 快 | 通用 |
| Gamma 编码 | 一元码 + 二进制，小整数高效 | 高 | 中 | 小文档间距 |
| Rice 编码 | 参数化的 Golomb 编码 | 高 | 中 | 已知分布 |
| PForDelta | 打包 FOR 差分解码 | 极高 | 快 | 大规模搜索索引 |

$$ \text{VByte 编码}: n \rightarrow \text{每 7 位分组, 末字节最高位为 1} $$

$$ \text{Gamma 编码: } \text{G}(n) = \underbrace{111\ldots 10}_{\lfloor \log_2 n \rfloor + 1 \text{ 位}}\ \underbrace{xxxxxx}_{\lfloor \log_2 n \rfloor \text{ 位}} $$

## 二、索引类型

### 2.1 数据库索引类型（PostgreSQL）

| 索引类型 | 数据结构 | 适用操作 | 适用数据类型 |
|---------|---------|---------|-------------|
| B-tree | 平衡树 | =, <, >, BETWEEN, LIKE | 通用 |
| Hash | 哈希表 | = | 等值查询 |
| GiST | 广义搜索树 | 全文搜索、几何 | 多维、自定义 |
| GIN | 广义倒排索引 | 数组、JSONB、全文 | 复合值 |
| BRIN | 块范围索引 | 顺序相关数据 | 时间序列、日志 |
| SP-GiST | 空间分区 GiST | 空间、网络 | 分层结构 |

### 2.2 索引类型对比

| 维度 | 聚簇索引 | 非聚簇索引 | 主索引 | 辅助索引 |
|:----:|---------|-----------|:------:|:--------:|
| 数据排序 | 按索引键排序 | 独立于数据 | 按键排序 | 独立 |
| 表数据位置 | 叶子节点存储 | 叶子存指针 | 主键排序 | 任意 |
| 回表需求 | 无 | 需要回表 | 无 | 需要 |
| 数量限制 | 1 个 | 多个 | 1 个 | 多个 |

### 2.3 空间索引

**R-tree** 及其变体是空间索引的核心结构：

| 索引 | 特点 | 插入策略 | 分裂策略 | 查询性能 |
|:----:|------|---------|---------|:--------:|
| R-tree | 最小边界矩形（MBR）嵌套 | ChooseSubtree | 最小面积 | 中 |
| R*-tree | 改进插入/分裂 | 强制重插入 | 最小重叠优先 | 好 |
| STR-tree | 排序行递归打包 | 批量加载 | — | 好（静态） |

$$ \text{R-tree 搜索 } O(\log N) \text{（平均, 点查询）}, \quad N = \text{条目数} $$

## 三、知识映射

### 3.1 概念图（Concept Map）

由 Joseph Novak 基于 Ausubel 同化理论开发，用于表示知识结构。

| 元素 | 定义 | 示例 |
|------|------|------|
| 概念节点 | 感知到的规律性，用标签标记 | "光合作用" |
| 连接线 | 节点间的关系线 | 箭头 |
| 连接词 | 连接线上的关系描述 | "需要", "产生" |
| 层级结构 | 从上到下，从一般到具体 | 最一般概念在顶部 |
| 交叉连接 | 不同层级间的连接 | 跨领域关联 |
| 具体示例 | 概念的具体实例 | "菠菜"→叶绿体 |

**概念图评估**：Novak 提出依据层级、交叉连接和示例数量量化评估。

### 3.2 思维导图（Mind Map）

由 Tony Buzan 推广的放射式笔记方法：

| 特征 | 概念图 | 思维导图 |
|:----:|--------|---------|
| 结构 | 层级 + 交叉连接 | 放射树状 |
| 根节点 | 中心问题 | 中心主题 |
| 连接词 | 需要标记 | 通常不需 |
| 方向性 | 有向 | 无向 |
| 认知基础 | 同化理论 | 放射性思维 |

### 3.3 论辩图（Argument Map）

将论证结构可视化的工具：

```
结论
    ├── 支持 Premise 1
    │     ├── 证据 1.1
    │     └── 证据 1.2
    ├── 支持 Premise 2
    └── 反对 Objection 1
          └── 反驳 Rebuttal 1
```

### 3.4 主题图（Topic Maps）

ISO 标准（ISO/IEC 13250），基于 XTM（XML Topic Maps）语法：

| 核心概念 | 说明 |
|---------|------|
| 主题（Topic） | 任何可被标识的事物 |
| 关联（Association） | 主题之间的关系 |
| 外观（Occurrence） | 主题相关的信息资源 |

## 四、本体映射

### 4.1 模式匹配

| 方法 | 类别 | 技术 | 示例 |
|:----:|:----:|------|------|
| 基于字符串 | 元素级 | Levenshtein 编辑距离 | "Name" → "FullName" |
| 基于语言 | 元素级 | WordNet 同义词 | "Car" → "Vehicle" |
| 基于结构 | 结构级 | 图同构、邻域相似度 | 两个本体的结构对齐 |
| 基于约束 | 元素级 | 数据类型/基数匹配 | int → integer |
| 基于实例 | 结构级 | 实例重叠度计算 | 实例交集 |

$$ \text{编辑距离: } \text{lev}(a, b) = \frac{\text{最小编辑次数}}{\max(|a|, |b|)} $$

$$ \text{WordNet 相似度 } \text{sim}(c_1, c_2) = \frac{2 \times \text{depth(lcs)}}{\text{depth}(c_1) + \text{depth}(c_2)} $$

### 4.2 实例匹配

**实体解析（Entity Resolution）** 的核心挑战是确定两个记录是否指向同一实体：

| 方法 | 原理 | 准确率 | 效率 |
|:----:|------|:------:|:----:|
| 精确匹配 | 完全一致 | 低 | 高 |
| 模糊匹配 | 编辑距离/Jaro-Winkler | 中 | 中 |
| 基于规则 | 手工规则 + 阈值 | 高 | 中 |
| 机器学习 | 分类器（随机森林/XGBoost） | 高 | 中 |
| 深度学习 | Ditto, DeepER | 最高 | 低 |
| 众包 | 人工标注 + 聚合 | 最高 | 极低 |

**阻塞方法（Blocking）**：将候选记录分组到块中，只在块内进行比较，避免全对全比较：

$$ O(N^2) \rightarrow O(B \times (N/B)^2) = O(N^2 / B) $$

## 五、图索引

### 5.1 可达性索引

| 索引 | 原理 | 查询时间 | 更新时间 | 空间 |
|:----:|------|:--------:|:--------:|:----:|
| 传递闭包 | 预计算所有可达对 | $O(1)$ | $O(N^2)$ | $O(N^2)$ |
| 2-hop 覆盖 | 中心节点集 | $O(d)$ | $O(N^3)$ | $O(N \sqrt{M})$ |
| Dual-labeling | 树 + 非树边标签 | $O(\alpha(N))$ | 高 | $O(N)$ |
| PLL | 剪枝标签 | $O(1)$ | 高 | 中 |
| GraphQL | 邻域匹配 | $O(d^k)$ | 低 | $O(N)$ |

### 5.2 子图匹配

| 算法 | 策略 | 适用图规模 | 特点 |
|:----:|------|:---------:|------|
| VF2 | 回溯 + 可行性规则 | 中小（10K） | 精确匹配 |
| GraphQL | 邻域探索 + 索引 | 中大 | 基于图数据库 |
| TurboISO | 查询图聚类 | 中 | 候选过滤优化 |
| QuickSI | 查询排序 | 中 | 最小编号边优先 |
| RI | 路径探索 | 大 | 分布式 |

## 六、文本索引结构

### 6.1 后缀结构

| 结构 | 构建时间 | 空间 | 支持操作 |
|:----:|:--------:|:----:|---------|
| 后缀数组（SA） | $O(N \log N)$ | $4N$ 字节 | 子串搜索、LCP |
| 后缀树（ST） | $O(N)$ | $20N$ 字节 | 所有子串操作 |
| FM-index | $O(N)$ | $0.5N-2N$ | 压缩全文索引 |
| BWT | $O(N)$ | $N$ 字节 | 数据压缩 + 索引 |

**Burrows-Wheeler Transform（BWT）** 是压缩索引的核心：

1. 循环移位矩阵的所有行
2. 按字典序排序
3. 取最后一列作为 BWT 输出

$$ \text{BWT}(T) = \text{最后一列(循环移位矩阵的排序结果)} $$

**FM-index** 结合 BWT 和辅助数据结构（rank/select 操作），在压缩空间内实现高效子串搜索：

$$ \text{count}(P) = \text{使用 LF-mapping 在 BWT 上定位模式 } P $$

### 6.2 比较总结

| 结构 | 空间开销 | 搜索速度 | 支持动态 | 压缩 |
|:----:|:--------:|:--------:|:--------:|:----:|
| 后缀数组 | $O(N \log N)$ | $O(|P| + \log N)$ | 难 | 可压缩 |
| 后缀树 | $O(N \sigma)$ | $O(|P|)$ | 难 | 不可 |
| FM-index | $O(N H_k)$ | $O(|P| \log \sigma)$ | 难 | 高度压缩 |
| BWT+SA | $O(N)$ 文本 + $O(N \log N)$ 索引 | $O(|P|)$ | 难 | 中间 |

## 七、知识图谱索引

### 7.1 知识图谱存储索引

| 索引类型 | 作用 | 实现 | 查询加速 |
|---------|------|------|---------|
| SPO 索引 | 主-谓-宾全序排列 | 六种排列组合 | 任意三元组模式 |
| Value 索引 | 字面值范围查询 | B-tree | 过滤/排序 |
| 全文索引 | 文本属性 | 倒排索引 | 实体搜索 |
| 邻接索引 | 一跳邻居快速访问 | 邻接表 | 图遍历 |
| 路径索引 | 预计算路径 | 传递闭包 | 长路径查询 |

### 7.2 标签约束可达性

$$ \text{标签约束可达性查询: 从 } v_s \text{ 沿标签 } l_1, l_2, \ldots, l_k \text{ 能否到达 } v_t $$

| 方法 | 预处理 | 查询时间 | 更新支持 |
|:----:|:------:|:--------:|:--------:|
| BFS/DFS | $O(1)$ | $O(N + M)$ | ✅ |
| 标签传递闭包 | $O(N^3 L)$ | $O(1)$ | ❌ |
| 2-hop 标签覆盖 | $O(N^3)$ | $O(k)$ | ❌ |

## 参考资源

- Manning, C. D., Raghavan, P., & Schutze, H. (2008). *Introduction to Information Retrieval*. Cambridge University Press.
- Witten, I. H., Moffat, A., & Bell, T. C. (1999). *Managing Gigabytes* (2nd ed.). Morgan Kaufmann.
- Zobel, J., & Moffat, A. (2006). Inverted Files for Text Search Engines. *ACM Computing Surveys*, 38(2), 6.
- Samet, H. (2006). *Foundations of Multidimensional and Metric Data Structures*. Morgan Kaufmann.
- PostgreSQL 索引文档: https://www.postgresql.org/docs/current/indexes.html
- FM-index: Ferragina, P., & Manzini, P. (2005). Indexing Compressed Text. *JACM*, 52(4), 552-581.

## 相关条目

[[00_KnowledgeFramework/KnowledgeGraph/INDEX|KnowledgeGraph]], [[CrossDisciplinaryLinks]], InformationArchitecture, Taxonomy
