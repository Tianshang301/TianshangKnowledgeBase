# 图详解

## 基本概念

图（Graph）由**顶点**（Vertex/Vertices）和**边**（Edge）组成，记为 G = (V, E)。

### 图的分类

| 类型 | 描述 | 示例 |
|------|------|------|
| 有向图 | 边有方向 | 网页链接 |
| 无向图 | 边无方向 | 社交网络 |
| 加权图 | 边有权重 | 城市间距离 |
| 无权图 | 边无权重 | 朋友关系 |
| 稀疏图 | |E| << |V|² | 社交网络 |
| 稠密图 | |E| ≈ |V|² | 完全图 |

### 术语

- **度 (Degree)**：无向图中顶点关联的边数
- **入度/出度 (In-degree/Out-degree)**：有向图中进入/离开顶点的边数
- **路径 (Path)**：顶点序列，相邻顶点间有边
- **环 (Cycle)**：起点和终点相同的路径
- **连通图 (Connected Graph)**：任意两顶点间有路径
- **强连通 (Strongly Connected)**：有向图中任意两点双向可达

## 图的表示

### 邻接矩阵 (Adjacency Matrix)

```python
class AdjacencyMatrix:
    def __init__(self, n, directed=False):
        self.n = n
        self.directed = directed
        self.matrix = [[0] * n for _ in range(n)]
    
    def add_edge(self, u, v, weight=1):
        self.matrix[u][v] = weight
        if not self.directed:
            self.matrix[v][u] = weight
    
    def has_edge(self, u, v):
        return self.matrix[u][v] != 0
    
    def get_neighbors(self, u):
        return [v for v in range(self.n) if self.matrix[u][v] != 0]
```

**空间复杂度**: O(V²)

### 邻接表 (Adjacency List)

```python
class AdjacencyList:
    def __init__(self, n, directed=False):
        self.n = n
        self.directed = directed
        self.graph = [[] for _ in range(n)]
    
    def add_edge(self, u, v, weight=1):
        self.graph[u].append((v, weight))
        if not self.directed:
            self.graph[v].append((u, weight))
    
    def get_neighbors(self, u):
        return self.graph[u]
```

**空间复杂度**: O(V + E)，适用于稀疏图

### Python dict 实现

```python
# 用 dict 表示图（适合稀疏图/动态图）
graph = {
    'A': {'B': 1, 'C': 2},
    'B': {'A': 1, 'D': 3},
    'C': {'A': 2, 'D': 4},
    'D': {'B': 3, 'C': 4}
}
```

## 图的遍历

### 深度优先搜索 (DFS)

```python
def dfs_recursive(graph, start, visited=None):
    """DFS 递归实现"""
    if visited is None:
        visited = set()
    visited.add(start)
    print(start, end=' ')
    for neighbor in graph[start]:
        if neighbor not in visited:
            dfs_recursive(graph, neighbor, visited)
    return visited

def dfs_iterative(graph, start):
    """DFS 迭代实现（栈）"""
    visited = set()
    stack = [start]
    
    while stack:
        node = stack.pop()
        if node not in visited:
            visited.add(node)
            print(node, end=' ')
            for neighbor in graph[node]:
                if neighbor not in visited:
                    stack.append(neighbor)
    
    return visited
```

### 广度优先搜索 (BFS)

```python
from collections import deque

def bfs(graph, start):
    """BFS 实现"""
    visited = {start}
    queue = deque([start])
    
    while queue:
        node = queue.popleft()
        print(node, end=' ')
        
        for neighbor in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
    
    return visited
```

### 遍历对比

| 特性 | DFS | BFS |
|-----|-----|-----|
| 数据结构 | 栈（递归/显式） | 队列 |
| 时间复杂度 | $O(V+E)$ | $O(V+E)$ |
| 空间复杂度 | $O(h)$ 递归深度 | $O(w)$ 最宽层 |
| 适用场景 | 连通分量、拓扑排序 | 最短路径、层序遍历 |
| 最短路径 | 不能（权值相等可） | 可以（无权图） |

## 连通分量

### 无向图的连通分量

```python
def connected_components(graph):
    """查找所有连通分量"""
    visited = set()
    components = []
    
    for node in graph:
        if node not in visited:
            component = set()
            dfs_recursive(graph, node, component)
            components.append(component)
            visited |= component
    
    return components
```

### 有向图的强连通分量 - Kosaraju 算法

```python
def kosaraju_scc(graph):
    """Kosaraju 算法求强连通分量"""
    n = len(graph)
    visited = [False] * n
    order = []
    
    # 第一次 DFS：记录完成顺序
    def dfs1(u):
        visited[u] = True
        for v in graph[u]:
            if not visited[v]:
                dfs1(v)
        order.append(u)
    
    for i in range(n):
        if not visited[i]:
            dfs1(i)
    
    # 反转图
    rev_graph = [[] for _ in range(n)]
    for u in range(n):
        for v in graph[u]:
            rev_graph[v].append(u)
    
    # 第二次 DFS：按逆序处理
    scc = [-1] * n
    def dfs2(u, label):
        scc[u] = label
        for v in rev_graph[u]:
            if scc[v] == -1:
                dfs2(v, label)
    
    label = 0
    for u in reversed(order):
        if scc[u] == -1:
            dfs2(u, label)
            label += 1
    
    return scc
```

## 拓扑排序 (Topological Sort)

仅适用于**有向无环图 (DAG)**。

### Kahn 算法 (BFS)

```python
from collections import deque

def topological_sort_kahn(graph):
    """Kahn 算法拓扑排序"""
    n = len(graph)
    in_degree = [0] * n
    
    for u in range(n):
        for v in graph[u]:
            in_degree[v] += 1
    
    queue = deque([i for i in range(n) if in_degree[i] == 0])
    result = []
    
    while queue:
        u = queue.popleft()
        result.append(u)
        
        for v in graph[u]:
            in_degree[v] -= 1
            if in_degree[v] == 0:
                queue.append(v)
    
    if len(result) != n:
        raise ValueError("Graph has a cycle!")
    
    return result
```

**时间复杂度**: O(V + E)

### DFS 拓扑排序

```python
def topological_sort_dfs(graph):
    """DFS 拓扑排序"""
    n = len(graph)
    visited = [0] * n  # 0=未访问, 1=访问中, 2=已处理
    result = []
    
    def dfs(u):
        if visited[u] == 1:
            raise ValueError("Graph has a cycle!")
        if visited[u] == 2:
            return
        visited[u] = 1
        for v in graph[u]:
            dfs(v)
        visited[u] = 2
        result.append(u)
    
    for i in range(n):
        if visited[i] == 0:
            dfs(i)
    
    return result[::-1]  # 逆序
```

## 环检测

```python
def has_cycle_undirected(graph):
    """无向图环检测（DFS + 父节点）"""
    n = len(graph)
    visited = [False] * n
    
    def dfs(u, parent):
        visited[u] = True
        for v in graph[u]:
            if not visited[v]:
                if dfs(v, u):
                    return True
            elif v != parent:
                return True
        return False
    
    for i in range(n):
        if not visited[i]:
            if dfs(i, -1):
                return True
    return False

def has_cycle_directed(graph):
    """有向图环检测（三色标记法）"""
    n = len(graph)
    state = [0] * n  # 0=白, 1=灰, 2=黑
    
    def dfs(u):
        state[u] = 1  # 灰色
        for v in graph[u]:
            if state[v] == 1:
                return True  # 发现反向边
            if state[v] == 0 and dfs(v):
                return True
        state[u] = 2  # 黑色
        return False
    
    for i in range(n):
        if state[i] == 0:
            if dfs(i):
                return True
    return False
```

## 最短路径

### 无权图最短路径 (BFS)

对于无权图，最短路径长度等于 BFS 的搜索深度：

$$ \delta(s, v) = \text{BFS 中从 } s \text{ 到 } v \text{ 的层数} $$

BFS 按层扩展时，$d[v] = d[u] + 1$，其中 $u$ 是 $v$ 的前驱节点。

```python
def shortest_path_unweighted(graph, start, end):
    """无权图最短路径（BFS + 路径记录）"""
    visited = {start}
    queue = deque([(start, [start])])
    
    while queue:
        node, path = queue.popleft()
        if node == end:
            return path
        for neighbor in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, path + [neighbor]))
    
    return None
```

### Dijkstra (正权图)

```python
import heapq

def dijkstra(graph, n, start):
    """Dijkstra 最短路径（堆优化）"""
    dist = [float('inf')] * n
    dist[start] = 0
    pq = [(0, start)]
    prev = [-1] * n
    
    while pq:
        d, u = heapq.heappop(pq)
        if d > dist[u]:
            continue
        
        for v, w in graph[u]:
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                prev[v] = u
                heapq.heappush(pq, (dist[v], v))
    
    return dist, prev
```

### Bellman-Ford (含负权)

```python
def bellman_ford(edges, n, start):
    """Bellman-Ford 算法（检测负环）"""
    dist = [float('inf')] * n
    dist[start] = 0
    
    for _ in range(n - 1):
        for u, v, w in edges:
            if dist[u] != float('inf') and dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
    
    # 检测负环
    for u, v, w in edges:
        if dist[u] != float('inf') and dist[u] + w < dist[v]:
            raise ValueError("Graph contains negative cycle!")
    
    return dist
```

### Floyd-Warshall (全源)

```python
def floyd_warshall(graph):
    """Floyd-Warshall 全源最短路径"""
    n = len(graph)
    dist = [[float('inf')] * n for _ in range(n)]
    
    for i in range(n):
        dist[i][i] = 0
        for j, w in graph[i]:
            dist[i][j] = w
    
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if dist[i][k] + dist[k][j] < dist[i][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]
    
    return dist
```

### 最短路径算法对比

| 算法 | 适用 | 时间复杂度 | 空间 |
|-----|------|-----------|------|
| BFS | 无权图 | O(V+E) | O(V) |
| Dijkstra | 正权图 | O((V+E)log V) | O(V) |
| Bellman-Ford | 含负权 | O(VE) | O(V) |
| Floyd-Warshall | 全源 | O(V³) | O(V²) |

## 经典问题

### 课程表 (LeetCode 207)

```python
def can_finish(num_courses, prerequisites):
    """课程表（拓扑排序检测环）"""
    graph = [[] for _ in range(num_courses)]
    in_degree = [0] * num_courses
    
    for course, prereq in prerequisites:
        graph[prereq].append(course)
        in_degree[course] += 1
    
    queue = deque([i for i in range(num_courses) if in_degree[i] == 0])
    count = 0
    
    while queue:
        node = queue.popleft()
        count += 1
        for neighbor in graph[node]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)
    
    return count == num_courses
```

### 克隆图 (LeetCode 133)

```python
def clone_graph(node):
    """DFS 克隆图"""
    if not node:
        return None
    
    visited = {}
    
    def dfs(node):
        if node in visited:
            return visited[node]
        
        clone = Node(node.val)
        visited[node] = clone
        
        for neighbor in node.neighbors:
            clone.neighbors.append(dfs(neighbor))
        
        return clone
    
    return dfs(node)
```

## 练习

| 题目 | 难度 | 核心技巧 |
|------|------|---------|
| LeetCode 200. 岛屿数量 | 🟡 中等 | DFS/BFS |
| LeetCode 207. 课程表 | 🟡 中等 | 拓扑排序 |
| LeetCode 133. 克隆图 | 🟡 中等 | DFS/BFS |
| LeetCode 210. 课程表 II | 🟡 中等 | 拓扑排序 |
| LeetCode 785. 判断二分图 | 🟡 中等 | BFS 染色 |
| LeetCode 994. 腐烂的橘子 | 🟡 中等 | BFS 多源 |
| LeetCode 743. 网络延迟时间 | 🟡 中等 | Dijkstra |
| LeetCode 787. K 站中转最便宜 | 🟡 中等 | Bellman-Ford |
| LeetCode 684. 冗余连接 | 🟡 中等 | 并查集 |
| LeetCode 329. 矩阵最长递增路径 | 🔴 困难 | DFS+记忆化 |

## 相关条目

- [[Tree]]
- [[BFS_DFS]]
- [[Dijkstra]]
- [[UnionFind]]
- [[Heap]]
