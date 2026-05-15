# 最小生成树

## 基本概念

最小生成树（Minimum Spanning Tree, MST）是在**加权无向连通图**中，找出一个边的子集，使得：
1. 包含所有顶点
2. 形成一棵树（无环）
3. 所有边的权重之和最小

### 性质

- **切割性质**：任何切割的**最小权重边**一定属于某个 MST
- **环性质**：任意环中的**最大权重边**一定不属于任何 MST
- 如果所有边权重互异，MST 唯一

## 算法对比

| 算法 | 思想 | 时间复杂度 | 数据结构 |
|-----|------|-----------|---------|
| Prim (朴素) | 贪心选最近顶点 | O(V²) | 数组 |
| Prim (堆) | 贪心选最近顶点 | O(E log V) | 优先队列 |
| Kruskal | 贪心选最小边 | O(E log E) | 并查集 |

## Prim 算法

从任意顶点开始，每次选择连接已在 MST 中和不在 MST 中的**最小权边**。

```python
import heapq

def prim(graph, n, start=0):
    """Prim 算法求 MST（堆优化）"""
    visited = [False] * n
    pq = [(0, start, -1)]  # (权重, 顶点, 父顶点)
    mst_weight = 0
    mst_edges = []
    
    while pq:
        w, u, parent = heapq.heappop(pq)
        if visited[u]:
            continue
        
        visited[u] = True
        mst_weight += w
        if parent != -1:
            mst_edges.append((parent, u, w))
        
        for v, weight in graph[u]:
            if not visited[v]:
                heapq.heappush(pq, (weight, v, u))
    
    if all(visited):
        return mst_weight, mst_edges
    return None  # 非连通图
```

**时间复杂度**: O(E log V) (堆优化)
**空间复杂度**: O(V + E)

### Prim 朴素实现 O(V²)

```python
def prim_naive(graph, n, start=0):
    """Prim 算法（邻接矩阵，稠密图适用）"""
    visited = [False] * n
    min_weight = [float('inf')] * n
    parent = [-1] * n
    min_weight[start] = 0
    
    for _ in range(n):
        # 找未访问中最小权重的顶点
        u = min((i for i in range(n) if not visited[i]),
                key=lambda i: min_weight[i], default=-1)
        if u == -1 or min_weight[u] == float('inf'):
            return None  # 非连通
        
        visited[u] = True
        
        for v in range(n):
            if graph[u][v] < min_weight[v] and not visited[v]:
                min_weight[v] = graph[u][v]
                parent[v] = u
    
    mst_weight = sum(min_weight)
    mst_edges = [(v, parent[v], min_weight[v]) for v in range(1, n)]
    return mst_weight, mst_edges
```

## Kruskal 算法

将所有边按权重排序，从小到大选取，若加入后不会形成环则保留。

```python
class DSU:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n
    
    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]
    
    def union(self, x, y):
        px, py = self.find(x), self.find(y)
        if px == py:
            return False
        if self.rank[px] < self.rank[py]:
            self.parent[px] = py
        elif self.rank[px] > self.rank[py]:
            self.parent[py] = px
        else:
            self.parent[py] = px
            self.rank[px] += 1
        return True

def kruskal(n, edges):
    """Kruskal 算法求 MST"""
    edges.sort(key=lambda x: x[2])  # 按权重排序
    dsu = DSU(n)
    mst_weight = 0
    mst_edges = []
    
    for u, v, w in edges:
        if dsu.union(u, v):
            mst_weight += w
            mst_edges.append((u, v, w))
    
    if len(mst_edges) != n - 1:
        return None  # 非连通图
    
    return mst_weight, mst_edges
```

**时间复杂度**: O(E log E) = O(E log V)（排序为主）
**空间复杂度**: O(V + E)

## 两个算法的比较

| 特性 | Prim | Kruskal |
|-----|------|---------|
| 策略 | 选顶点 | 选边 |
| 适用 | 稠密图 | 稀疏图 |
| 数据结构 | 堆/数组 | 并查集 |
| 边的排序 | 不需要 | 需要 |
| 是否依赖起始点 | 是 | 否 |
| 容易实现性 | 相对简单 | 简单 |

## 应用场景

### 1. 网络设计
- 铺设电缆/光缆的最小成本方案
- 水管网络规划

### 2. 聚类分析
- 单链接聚类（Single-linkage clustering）基于 MST

### 3. 近似算法
- 旅行商问题 (TSP) 的 2-近似（MST + DFS 遍历）
- Steiner 树近似

### 4. 图像分割
- 基于图的分割算法使用 MST

## TSP 近似算法

```python
def tsp_approximation(n, graph):
    """TSP 的 2-近似（基于 MST）"""
    # 1. 求 MST
    mst_weight, mst_edges = prim(graph, n)
    
    # 2. 构建 MST 邻接表
    mst_adj = [[] for _ in range(n)]
    for u, v, w in mst_edges:
        mst_adj[u].append(v)
        mst_adj[v].append(u)
    
    # 3. DFS 前序遍历得到近似 TSP 路径
    def dfs(u, visited, path):
        visited[u] = True
        path.append(u)
        for v in mst_adj[u]:
            if not visited[v]:
                dfs(v, visited, path)
    
    visited = [False] * n
    path = []
    dfs(0, visited, path)
    path.append(0)  # 回到起点
    
    # 计算路径长度
    total = 0
    for i in range(len(path) - 1):
        u, v = path[i], path[i + 1]
        for neighbor, w in graph[u]:
            if neighbor == v:
                total += w
                break
    
    return path, total
```

## 最小生成树变体

### 次小生成树 (Second MST)

```python
def second_mst(n, edges):
    """求次小生成树（替换 MST 的一条边）"""
    edges.sort(key=lambda x: x[2])
    dsu = DSU(n)
    mst_edges = []
    mst_weight = 0
    
    # 先求 MST
    for u, v, w in edges:
        if dsu.union(u, v):
            mst_edges.append((u, v, w))
            mst_weight += w
    
    if len(mst_edges) != n - 1:
        return None
    
    # 尝试删除一条 MST 边，求最小替代边
    second_min = float('inf')
    
    for i in range(len(mst_edges)):
        dsu = DSU(n)
        weight = 0
        count = 0
        
        for j, (u, v, w) in enumerate(mst_edges):
            if i != j:
                if dsu.union(u, v):
                    weight += w
                    count += 1
        
        for u, v, w in edges:
            if dsu.union(u, v):
                weight += w
                count += 1
                break
        
        if count == n - 1:
            second_min = min(second_min, weight)
    
    return second_min if second_min != float('inf') else None
```

### 最大生成树

仅需将 Kruskal 的边排序改为降序，或将 Prim 的堆改为最大堆。

```python
def kruskal_max(n, edges):
    """最大生成树"""
    edges.sort(key=lambda x: x[2], reverse=True)  # 降序
    dsu = DSU(n)
    weight = 0
    
    for u, v, w in edges:
        if dsu.union(u, v):
            weight += w
    
    return weight
```

### 最小瓶颈生成树 (Minimum Bottleneck Spanning Tree)

**性质**：任何 MST 就是最小瓶颈生成树（即最小化最大边权）。

## 练习

| 题目 | 难度 | 核心技巧 |
|------|------|---------|
| LeetCode 1584. 连接所有点的最小费用 | 🟡 中等 | Prim/Kruskal |
| LeetCode 1135. 最低成本联通所有城市 | 🟡 中等 | Prim/Kruskal |
| LeetCode 1168. 水资源分配优化 | 🔴 困难 | 虚拟节点+Kruskal |
| LeetCode 1489. 找到最小生成树的关键边 | 🔴 困难 | 关键边判断 |
| LeetCode 1631. 最小体力消耗路径 | 🟡 中等 | 并查集+排序 |
| LeetCode 778. 水位上升池中游泳 | 🔴 困难 | 并查集+排序 |
| LeetCode 261. 图是否是树 | 🟡 中等 | 并查集 |

## 相关条目

- [[Graph]]
- [[Dijkstra]]
- [[BFSDFS]]
- [[UnionFind]]
- [[Greedy]]
