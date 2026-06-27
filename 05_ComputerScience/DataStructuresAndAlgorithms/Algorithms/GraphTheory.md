---
aliases: [GraphTheory, 图论, GraphAlgorithms, 图算法]
tags: ['05_ComputerScience', 'DataStructures', 'GraphAlgorithms', 'DiscreteMathematics']
created: 2026-05-17
updated: 2026-05-17
---

# 图论 Graph Theory

## 1. 概述 (Overview)

图论（Graph Theory）是数学的一个分支，研究由顶点（Vertices/Nodes）和连接顶点的边（Edges/Links）组成的图结构。图论起源于 1736 年欧拉（Leonhard Euler）解决柯尼斯堡七桥问题（Seven Bridges of Königsberg），如今已成为计算机科学、运筹学、网络科学和生物学等领域的基础工具。

图可以用来建模各种关系和结构：社交网络中的好友关系、交通网络中的道路连接、计算机网络中的路由拓扑、分子结构中的化学键等。图的通用性和表达力使其成为离散数学和计算机科学中最重要的抽象工具之一。

## 2. 基本概念 (Basic Concepts)

### 2.1 图的定义与分类

一个图 $G$ 可以表示为 $G = (V, E)$，其中 $V$ 是顶点集合，$E$ 是边集合。

| 图类型 | 定义 | 表示 | 典型应用 |
|:-------|:-----|:-----|:---------|
| 无向图 (Undirected) | 边无方向性 | $e = \{u,v\}$ | 社交网络好友关系 |
| 有向图 (Directed) | 边有方向性 | $e = (u,v)$ | Web 页面链接 |
| 加权图 (Weighted) | 边带有权重 | $w(e) \in \mathbb{R}$ | 地图距离 |
| 多重图 (Multigraph) | 顶点间多条边 | — | 运输网络 |
| 完全图 (Complete) | 每对顶点间有边 | $K_n$ | 锦标赛赛程 |
| 二分图 (Bipartite) | 顶点可分两组 | $G = (U,V,E)$ | 匹配问题 |

### 2.2 基本术语

- **度数**（Degree）：与顶点关联的边的数量。在有向图中分为入度（In-degree）和出度（Out-degree）
- **路径**（Path）：顶点序列，相邻顶点间有边相连
- **回路**（Cycle）：起点和终点相同的路径
- **连通性**（Connectivity）：图中任意两点间是否存在路径
- **子图**（Subgraph）：原图顶点和边的子集构成的图

$$
\text{握手引理: } \sum_{v \in V} \deg(v) = 2|E|
$$

### 2.3 图的表示 (Graph Representation)

```mermaid
graph LR
    subgraph 邻接矩阵 Adjacency Matrix
        direction TB
        A1[顶点数 n × n 矩阵<br/>A[i][j] = 1 if 有边<br/>空间 O(V²)]
    end
    subgraph 邻接表 Adjacency List
        direction TB
        A2[每个顶点一个链表<br/>存储相邻顶点<br/>空间 O(V+E)]
    end
    subgraph 边列表 Edge List
        direction TB
        A3[按 (u,v,w) 三元组<br/>存储所有边<br/>空间 O(E)]
    end
```

## 3. 图的遍历 (Graph Traversal)

### 3.1 广度优先搜索 (BFS)

BFS（Breadth-First Search）使用队列（Queue）实现逐层遍历，适用于寻找无权图的最短路径。

```
BFS(G, s):
    for each v in G.V:
        v.color = WHITE
        v.d = ∞
    s.color = GRAY; s.d = 0
    Q = {s}
    while Q ≠ ∅:
        u = Q.dequeue()
        for each v in G.Adj[u]:
            if v.color == WHITE:
                v.color = GRAY
                v.d = u.d + 1
                Q.enqueue(v)
        u.color = BLACK
```

时间复杂度：$O(V + E)$

### 3.2 深度优先搜索 (DFS)

DFS（Depth-First Search）使用栈（Stack）或递归实现，适用于拓扑排序、强连通分量检测等。

```
DFS(G):
    for each v in G.V:
        v.color = WHITE
    time = 0
    for each v in G.V:
        if v.color == WHITE:
            DFS-Visit(G, v)

DFS-Visit(G, u):
    time = time + 1; u.d = time
    u.color = GRAY
    for each v in G.Adj[u]:
        if v.color == WHITE:
            DFS-Visit(G, v)
    u.color = BLACK
    time = time + 1; u.f = time
```

DFS 会为每个节点记录发现时间（Discovery Time）$d[v]$ 和完成时间（Finish Time）$f[v]$，这些时间戳在多种图算法中具有重要作用。

## 4. 树与树结构 (Trees)

### 4.1 树的基本性质

树（Tree）是一种无环连通图。树具有以下等价性质：

| 性质 | 描述 |
|:-----|:------|
| 连通无环 | 任意两顶点间恰好有一条路径 |
| 边数关系 | $|E| = |V| - 1$ |
| 最小连通 | 删除任意一条边会使图不连通 |
| 最大无环 | 添加任意一条边会产生回路 |

### 4.2 生成树与最小生成树

**生成树**（Spanning Tree）是包含所有顶点的连通无环子图。**最小生成树**（Minimum Spanning Tree, MST）是所有生成树中边权总和最小的。

| 算法 | 策略 | 时间复杂度 | 特点 |
|:-----|:-----|:-----------|:-----|
| Kruskal | 按边权排序，贪心选边 | $O(E \log V)$ | 适合稀疏图 |
| Prim | 从单点扩展，选择最小邻边 | $O((V+E)\log V)$ | 适合稠密图 |
| Borůvka | 并行选择各连通分量的最小边 | $O(E \log V)$ | 适合并行计算 |

## 5. 最短路径 (Shortest Paths)

### 5.1 单源最短路径 (Single-Source)

| 算法 | 约束 | 时间复杂度 | 策略 |
|:-----|:-----|:-----------|:-----|
| Dijkstra | 非负权边 | $O((V+E)\log V)$ | 贪心+优先队列 |
| Bellman-Ford | 允许负权边 | $O(VE)$ | 动态规划 |
| SPFA | 允许负权边 | $O(VE)$ 最坏 | 队列优化 |

Dijkstra 算法的核心思想是松弛操作（Relaxation）：

$$
\text{if } d[v] > d[u] + w(u,v) \text{ then } d[v] = d[u] + w(u,v)
$$

### 5.2 全源最短路径 (All-Pairs)

| 算法 | 时间复杂度 | 特点 |
|:-----|:-----------|:-----|
| Floyd-Warshall | $O(V^3)$ | 动态规划，允许负权边 |
| Johnson | $O(V^2 \log V + VE)$ | 适用于稀疏图 |

Floyd-Warshall 算法基于递推公式：

$$
d_{ij}^{(k)} = \min\left(d_{ij}^{(k-1)}, d_{ik}^{(k-1)} + d_{kj}^{(k-1)}\right)
$$

## 6. 网络流 (Network Flow)

### 6.1 最大流问题 (Maximum Flow)

最大流问题的目标是从源点（Source）$s$ 到汇点（Sink）$t$ 在容量约束下找到最大流量的传输方案。

| 算法 | 时间复杂度 | 核心思想 |
|:-----|:-----------|:---------|
| Ford-Fulkerson | $O(E \cdot |f^*|)$ | 增广路径 |
| Edmonds-Karp | $O(VE^2)$ | BFS 找最短增广路 |
| Dinic | $O(V^2 E)$ | 分层图+阻塞流 |
| Push-Relabel | $O(V^3)$ | 预流推进 |

**最大流最小割定理**（Max-Flow Min-Cut Theorem）：

$$
\max\_\text{flow} = \min\_\text{cut\_capacity}(s,t)
$$

### 6.2 二分图匹配 (Bipartite Matching)

二分图最大匹配可以通过转化为网络流问题求解，也可以使用匈牙利算法（Hungarian Algorithm）直接解决。Kőnig 定理指出二分图中最大匹配数等于最小顶点覆盖数。

## 7. 图着色 (Graph Coloring)

### 7.1 顶点着色 (Vertex Coloring)

图着色问题要求为每个顶点分配颜色，使得相邻顶点颜色不同。**色数**（Chromatic Number）$\chi(G)$ 是所需的最小颜色数。

| 图类型 | 色数 |
|:-------|:-----|
| 二分图 | $\chi(G) \leq 2$ |
| 平面图 | $\chi(G) \leq 4$（四色定理） |
| 完全图 $K_n$ | $\chi(K_n) = n$ |

平面图的四色定理（Four Color Theorem）是图论中著名的定理，断言任何平面图都可以用四种颜色完成顶点着色，使得相邻顶点颜色不同。

### 7.2 应用

- 考试时间表安排（避免同一学生选的两门课冲突）
- 频谱分配（避免无线信号干扰）
- 寄存器分配（编译器优化）

## 8. 特殊图与高级主题 (Special Graphs & Advanced Topics)

### 8.1 平面图 (Planar Graphs)

平面图是可以画在平面上且边不相交的图。欧拉公式（Euler's Formula）对连通平面图成立：

$$
V - E + F = 2
$$

其中 $F$ 是面的数量（包括无限面）。

### 8.2 图同构 (Graph Isomorphism)

两个图 $G_1 = (V_1, E_1)$ 和 $G_2 = (V_2, E_2)$ 同构当且仅当存在双射 $f: V_1 \to V_2$，使得 $\{u,v\} \in E_1 \iff \{f(u), f(v)\} \in E_2$。图同构问题的计算复杂性至今仍是开放问题。

## 9. 应用领域 (Applications)

| 领域 | 图论应用 |
|:-----|:---------|
| 计算机网络 | 路由协议（OSPF 使用 Dijkstra）、拓扑设计 |
| 社交网络 | 影响力传播、社区发现、推荐系统 |
| 交通运输 | 最短路径导航、物流路径优化 |
| 生物信息学 | 蛋白质相互作用网络、代谢路径分析 |
| 电路设计 | PCB 布线、VLSI 布局 |
| 语言学 | 依存句法树、知识图谱 |

## 相关条目

- [[05_ComputerScience/DataStructuresAndAlgorithms/DataStructures/DataStructures|DataStructures]]
- [[Algorithms]]
- [[07_InterdisciplinarySciences/InterdisciplinaryMethodologies/NetworkScience|NetworkScience]]
- [[02_NaturalSciences/Mathematics/ComputationalMathematics|ComputationalMathematics]]
- [[02_NaturalSciences/Mathematics/DiscreteMathematics|DiscreteMathematics]]
- [[OptimizationTheory]]


