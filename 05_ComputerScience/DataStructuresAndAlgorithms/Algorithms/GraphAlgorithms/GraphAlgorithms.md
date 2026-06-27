---
aliases: [GraphAlgorithms]
tags: ['DataStructuresAndAlgorithms', 'Algorithms', 'GraphAlgorithms', 'GraphAlgorithms']
created: 2026-05-16
updated: 2026-05-16
---

# Graph Algorithms - 图算法

## 一、图的表示

### 三种基本表示

| 表示法 | 空间 | 判断边存在 | 遍历邻居 | 适用场景 |
|--------|------|-----------|---------|---------|
| **邻接矩阵** | $O(V^2)$ | $O(1)$ | $O(V)$ | 稠密图 |
| **邻接表** | $O(V+E)$ | $O(\deg(v))$ | $O(\deg(v))$ | 稀疏图 |
| **边列表** | $O(E)$ | $O(E)$ | $O(E)$ | Kruskal 算法 |

```python
# 邻接矩阵
graph = [[0, 1, 1, 0],
         [1, 0, 0, 1],
         [1, 0, 0, 1],
         [0, 1, 1, 0]]

# 邻接表
graph = {
    'A': ['B', 'C'],
    'B': ['A', 'D'],
    'C': ['A', 'D'],
    'D': ['B', 'C']
}
```

---

## 二、图遍历

### BFS（广度优先搜索）

BFS 使用队列，逐层遍历，用于求无权图的最短路径。

```python
from collections import deque

def bfs(graph, start):
    visited = set([start])
    queue = deque([start])
    distance = {start: 0}

    while queue:
        node = queue.popleft()
        for neighbor in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                distance[neighbor] = distance[node] + 1
                queue.append(neighbor)

    return distance
```

- 时间复杂度：$O(V + E)$
- 空间复杂度：$O(V)$
- 应用：最短路径、连通分量、二分图检测

### DFS（深度优先搜索）

DFS 使用栈（递归或显式），用于拓扑排序、连通分量、环检测。

```python
def dfs(graph, start):
    visited = set()
    result = []

    def _dfs(node):
        visited.add(node)
        result.append(node)
        for neighbor in graph[node]:
            if neighbor not in visited:
                _dfs(neighbor)

    _dfs(start)
    return result
```

**拓扑排序**（有向无环图）：

```python
def topological_sort(graph):
    visited = set()
    order = []

    def dfs(node):
        visited.add(node)
        for neighbor in graph[node]:
            if neighbor not in visited:
                dfs(neighbor)
        order.append(node)  # 后序加入

    for node in graph:
        if node not in visited:
            dfs(node)

    return order[::-1]  # 逆序即为拓扑序
```

| 特性 | BFS | DFS |
|------|-----|-----|
| 数据结构 | 队列 | 栈 |
| 最短路径（无权图） | ✅ | ❌ |
| 拓扑排序 | ❌（Kahn 算法除外） | ✅ |
| 连通分量 | ✅ | ✅ |
| 二分图检测 | ✅ | ✅ |

---

## 三、最短路径

### Dijkstra 算法

适用于**非负权图**，单源最短路径。

$$ \text{Dijkstra: } O((V+E)\log V) $$

$$ d[v] = \min(d[v], d[u] + w(u,v)) \quad \text{(松弛操作)} $$

```python
import heapq

def dijkstra(graph, start):
    """graph: {node: [(neighbor, weight),...]}"""
    dist = {node: float('inf') for node in graph}
    dist[start] = 0
    pq = [(0, start)]

    while pq:
        d, u = heapq.heappop(pq)
        if d > dist[u]:
            continue
        for v, w in graph[u]:
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                heapq.heappush(pq, (dist[v], v))

    return dist
```

**正确性**：贪心选择当前距离最小的顶点，因为所有边权非负，不可能通过其他路径得到更小距离。

### Bellman-Ford 算法

适用于**含负权边**的图，可检测负权环。

$$ \text{Bellman-Ford: } O(VE) $$

$$ d[v] = \min_{(u,v) \in E} (d[u] + w(u,v)), \quad \text{重复 } V-1 \text{ 次} $$

```python
def bellman_ford(edges, V, start):
    """edges: [(u, v, w),...]"""
    dist = [float('inf')] * V
    dist[start] = 0

    # 松弛 V-1 次
    for _ in range(V - 1):
        for u, v, w in edges:
            if dist[u] != float('inf') and dist[u] + w < dist[v]:
                dist[v] = dist[u] + w

    # 检测负权环
    for u, v, w in edges:
        if dist[u] != float('inf') and dist[u] + w < dist[v]:
            return None  # 存在负权环

    return dist
```

### Floyd-Warshall 算法

**全源最短路径**，动态规划思想。

$$ \text{Floyd-Warshall: } O(V^3) $$

$$ dp[k][i][j] = \min(dp[k-1][i][j], dp[k-1][i][k] + dp[k-1][k][j]) $$

即 $d_{ij}^{(k)} = \min(d_{ij}^{(k-1)}, d_{ik}^{(k-1)} + d_{kj}^{(k-1)})$，其中 $d_{ij}^{(k)}$ 表示从 $i$ 到 $j$ 且中间顶点仅取自 $\{1,\dots,k\}$ 的最短路径长度。

```python
def floyd_warshall(graph):
    V = len(graph)
    dist = [[float('inf')] * V for _ in range(V)]

    for i in range(V):
        dist[i][i] = 0
        for j, w in graph[i]:
            dist[i][j] = w

    for k in range(V):
        for i in range(V):
            for j in range(V):
                if dist[i][k] + dist[k][j] < dist[i][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]

    return dist
```

### A* 算法

启发式搜索，结合 Dijkstra 和贪心：

$$ f(n) = g(n) + h(n) $$

其中 $g(n)$ 是从起点到 $n$ 的实际代价，$h(n)$ 是启发式函数（如欧几里得距离、曼哈顿距离）。

| 算法 | 时间复杂度 | 负权 | 负环 | 单源/全源 |
|------|-----------|------|------|----------|
| Dijkstra | $O((V+E)\log V)$ | ❌ | ❌ | 单源 |
| Bellman-Ford | $O(VE)$ | ✅ | ✅ 检测 | 单源 |
| Floyd-Warshall | $O(V^3)$ | ✅ | ✅ 检测 | 全源 |
| A* | $O(E)$（平均） | ❌ | ❌ | 单源（启发式） |

---

## 四、最小生成树

### Prim 算法

从任意一个节点出发，贪心地扩展最小权值边。

$$ \text{Prim: } O((V+E)\log V) \text{ 二叉堆优化} $$

```python
def prim(graph, start=0):
    """graph: {node: [(neighbor, weight),...]}"""
    visited = set([start])
    edges = [(w, start, v) for v, w in graph[start]]
    heapq.heapify(edges)
    mst = []

    while edges and len(visited) < len(graph):
        w, u, v = heapq.heappop(edges)
        if v in visited:
            continue
        visited.add(v)
        mst.append((u, v, w))
        for x, w2 in graph[v]:
            if x not in visited:
                heapq.heappush(edges, (w2, v, x))

    return mst
```

### Kruskal 算法

将所有边按权排序，依次选权值最小且不形成环的边。

$$ \text{Kruskal: } O(E \log E) $$

```python
class UnionFind:
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

def kruskal(edges, V):
    """edges: [(w, u, v),...]"""
    edges.sort()
    uf = UnionFind(V)
    mst = []
    for w, u, v in edges:
        if uf.union(u, v):
            mst.append((u, v, w))
    return mst
```

| 算法 | 策略 | 数据结构 | 适用 |
|------|------|---------|------|
| Prim | 点扩展 | 优先队列 | 稠密图 |
| Kruskal | 边选择 | 并查集 | 稀疏图 |

**割性质 (Cut Property)**：对于任意割 $(S, V\setminus S)$，权值最小的跨越边一定属于某棵最小生成树。

**环性质 (Cycle Property)**：对于任意环，权值最大的边一定不属于任何最小生成树。

---

## 五、最大流

### 最大流最小割定理

$$ \max |f| = \min_{S \subset V,\; s \in S,\; t \notin S} c(S,T) $$

网络中的最大流值等于最小割的容量。对于任意割 $(S,T)$，有 $f(S,T) \leq c(S,T)$，且最大流等价于最小割。

### Ford-Fulkerson 方法

```python
def ford_fulkerson(graph, source, sink):
    """graph: 邻接矩阵，graph[u][v] = 容量"""
    V = len(graph)
    residual = [row[:] for row in graph]
    max_flow = 0

    def bfs(s, t, parent):
        visited = [False] * V
        queue = deque([s])
        visited[s] = True
        while queue:
            u = queue.popleft()
            for v in range(V):
                if not visited[v] and residual[u][v] > 0:
                    parent[v] = u
                    visited[v] = True
                    if v == t:
                        return True
                    queue.append(v)
        return False

    parent = [-1] * V
    while bfs(source, sink, parent):
        path_flow = float('inf')
        v = sink
        while v != source:
            u = parent[v]
            path_flow = min(path_flow, residual[u][v])
            v = u
        v = sink
        while v != source:
            u = parent[v]
            residual[u][v] -= path_flow
            residual[v][u] += path_flow
            v = u
        max_flow += path_flow

    return max_flow
```

**Dinic 算法**（时间复杂度 $O(EV^2)$）：

```text
1. 使用 BFS 构建分层图（Level Graph）
2. 使用 DFS 沿分层图发送阻塞流
3. 重复直到源点无法到达汇点
```

| 算法 | 时间复杂度 | 特点 |
|------|-----------|------|
| Ford-Fulkerson | $O(E \cdot |f|)$ | 依赖容量值 |
| Edmonds-Karp | $O(VE^2)$ | BFS 找增广路 |
| Dinic | $O(EV^2)$ | 分层图+阻塞流 |
| Push-Relabel | $O(V^3)$ | 预流推进 |

---

## 六、强连通分量

### Kosaraju 算法

```python
def kosaraju(graph, V):
    """返回强连通分量列表"""
    visited = [False] * V
    order = []

    def dfs1(u):
        visited[u] = True
        for v in graph[u]:
            if not visited[v]:
                dfs1(v)
        order.append(u)

    for i in range(V):
        if not visited[i]:
            dfs1(i)

    # 构建反向图
    rev_graph = [[] for _ in range(V)]
    for u in range(V):
        for v in graph[u]:
            rev_graph[v].append(u)

    # 按完成时间逆序遍历反向图
    sccs = []
    visited = [False] * V

    def dfs2(u, component):
        visited[u] = True
        component.append(u)
        for v in rev_graph[u]:
            if not visited[v]:
                dfs2(v, component)

    for u in reversed(order):
        if not visited[u]:
            component = []
            dfs2(u, component)
            sccs.append(component)

    return sccs
```

### Tarjan 算法

一次 DFS 完成，基于 `dfn`（访问时间）和 `low`（回溯最低时间）：

$$ \text{low}[u] = \min(\text{dfn}[u], \text{dfn}[v] \text{ for back edge}, \text{low}[v] \text{ for child}) $$

| 算法 | 时间复杂度 | 特点 |
|------|-----------|------|
| Kosaraju | $O(V+E)$ | 两次 DFS，实现简单 |
| Tarjan | $O(V+E)$ | 一次 DFS，需维护栈 |

---

## 七、二分图与匹配

### 二分图检测

```python
def is_bipartite(graph):
    color = {}
    for node in graph:
        if node not in color:
            color[node] = 0
            queue = deque([node])
            while queue:
                u = queue.popleft()
                for v in graph[u]:
                    if v not in color:
                        color[v] = color[u] ^ 1
                        queue.append(v)
                    elif color[v] == color[u]:
                        return False, None
    return True, color
```

### 匈牙利算法（最大匹配）

```python
def hungarian(graph, n_left, n_right):
    """graph[left] = [right_neighbors...]"""
    match_right = [-1] * n_right

    def dfs(u, visited):
        for v in graph[u]:
            if not visited[v]:
                visited[v] = True
                if match_right[v] == -1 or dfs(match_right[v], visited):
                    match_right[v] = u
                    return True
        return False

    result = 0
    for u in range(n_left):
        visited = [False] * n_right
        if dfs(u, visited):
            result += 1
    return result
```

---

## 八、欧拉路径与哈密顿路径

| 类型 | 定义 | 判定条件 |
|------|------|---------|
| **欧拉路径** | 经过每条边恰好一次 | 无向图：0 或 2 个奇度顶点 |
| **欧拉回路** | 欧拉路径 + 起点=终点 | 无向图：所有顶点度为偶数 |
| **哈密顿路径** | 经过每个顶点恰好一次 | NP-完全 |
| **哈密顿回路** | 哈密顿路径 + 起点=终点 | NP-完全 |

```python
# Fleury 算法（找欧拉路径）
def fleury(graph):
    """graph: 邻接表"""
    def dfs(u, visited_edges):
        visited_edges.add(u)
        for v in graph[u]:
            edge = (min(u, v), max(u, v))
            if edge not in visited_edges:
                dfs(v, visited_edges)

    # 检查度条件...
    pass
```

---

## 九、图着色

图着色问题是给每个顶点分配颜色，使相邻顶点颜色不同。

- **贪心着色**：按某种顺序，每个顶点使用可用的最小颜色
- **Welsh-Powell 算法**：按度降序排列后贪心着色
- **四色定理**：任何平面图可用 4 种颜色着色

| 问题 | 复杂度 |
|------|--------|
| 判断 2-着色 | $O(V+E)$（二分图检测） |
| 判断 3-着色 | NP-完全 |
| 最小着色数 | NP-困难 |

## 相关条目

- [[网络流与匹配算法]]
- [[05_ComputerScience/DataStructuresAndAlgorithms/DataStructures/Graph|Graph]]
- [[05_ComputerScience/DataStructuresAndAlgorithms/Algorithms/BFSDFS|BFSDFS]]
- [[05_ComputerScience/DataStructuresAndAlgorithms/Algorithms/Dijkstra|Dijkstra]]
- [[05_ComputerScience/DataStructuresAndAlgorithms/Algorithms/MST|MST]]

## 参考资源

- Cormen, T. H. et al. (2022). Introduction to Algorithms. 4th Edition. MIT Press.
- Sedgewick, R. & Wayne, K. (2011). Algorithms. 4th Edition. Addison-Wesley.
- Tarjan, R. (1972). Depth-First Search and Linear Graph Algorithms. SIAM Journal on Computing.
- Dinic, E. A. (1970). Algorithm for Solution of a Problem of Maximum Flow in a Network. Soviet Math. Doklady.


