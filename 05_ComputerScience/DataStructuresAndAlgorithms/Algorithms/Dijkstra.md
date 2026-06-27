---
aliases: [Dijkstra]
tags: ['DataStructuresAndAlgorithms', 'Algorithms', 'Dijkstra']
created: 2026-05-16
updated: 2026-05-13
---

# Dijkstra 最短路径算法

## 算法思想

Dijkstra 算法由 Edsger W. Dijkstra 于 1956 年提出，用于计算图中**单源最短路径**（一个节点到所有其他节点的最短路径）。

### 核心思想

- **贪心策略** + **BFS 思想**
- 维护一个距离数组 `dist[]`，记录从起点到每个节点的最短距离
- 每次从未处理的节点中选择距离最小的节点，松弛其所有邻接边
- **前提条件**：图中不能有负权边

### 算法步骤

```
1. 初始化：
   - dist[起点] = 0，其余 dist = ∞
   - 优先队列初始放入 (0, 起点)

2. 循环直到优先队列为空：
   a. 取出距离最小的节点 u
   b. 如果 u 已处理过（距离更大），跳过
   c. 遍历 u 的所有邻接节点 v：
      - 如果 dist[u] + w(u,v) < dist[v]：
        - 更新 dist[v]
        - 将 (dist[v], v) 加入优先队列

3. 最终 dist[] 即为起点到所有节点的最短距离
```

### 算法演示

```
     (4)     (1)
   A ─── B ─── C
   ╲    ╱     ╱
   (2) ╱(1)  ╱(5)
     ╲╱    ╱
      D ── E
       (3)

从 A 开始：
dist = {A:0, B:∞, C:∞, D:∞, E:∞}

1. 处理 A: 更新 B=4, D=2
2. 处理 D(距离2): 更新 B=min(4, 3)=3, E=5
3. 处理 B(距离3): 更新 C=min(∞, 4)=4
4. 处理 C(距离4): 更新 E=min(5, 9)=5
5. 处理 E(距离5): 无更新

结果: A→B=3, A→C=4, A→D=2, A→E=5
```

## 时间复杂度

| 实现方式 | 时间复杂度 | 说明 |
|---------|-----------|------|
| 朴素实现（邻接矩阵） | O(V²) | 每次找最小距离节点需遍历 |
| 二叉堆（优先队列） | O((V+E)log V) | 最常用实现 |
| 斐波那契堆 | O(E + V log V) | 理论最优，实现复杂 |

> V = 顶点数，E = 边数

## 代码实现

### Python 实现（优先队列优化）

```python
import heapq
from typing import List, Tuple, Dict

Graph = Dict[int, List[Tuple[int, int]]]  # 邻接表: {节点: [(邻居, 权重), ...]}

def dijkstra(graph: Graph, start: int) -> Tuple[Dict[int, float], Dict[int, int]]:
    """
    Dijkstra 最短路径算法
    
    Args:
        graph: 邻接表表示的图（非负权）
        start: 起点
    
    Returns:
        (dist, prev): 距离字典和前驱节点字典
    """
    # 初始化
    dist = {node: float('inf') for node in graph}
    prev = {node: None for node in graph}
    dist[start] = 0
    
    # 优先队列: (距离, 节点)
    pq = [(0, start)]
    visited = set()
    
    while pq:
        current_dist, u = heapq.heappop(pq)
        
        # 跳过过时的条目
        if current_dist > dist[u]:
            continue
        
        visited.add(u)
        
        # 松弛邻接边
        for v, weight in graph.get(u, []):
            if v in visited:
                continue
            
            new_dist = current_dist + weight
            if new_dist < dist[v]:
                dist[v] = new_dist
                prev[v] = u
                heapq.heappush(pq, (new_dist, v))
    
    return dist, prev


def shortest_path(prev: Dict[int, int], start: int, end: int) -> List[int]:
    """重构最短路径"""
    path = []
    current = end
    while current is not None:
        path.append(current)
        current = prev[current]
    path.reverse()
    return path if path[0] == start else []


# 使用示例
if __name__ == "__main__":
    # 无向图
    graph = {
        0: [(1, 4), (2, 1)],
        1: [(0, 4), (3, 1)],
        2: [(0, 1), (3, 5)],
        3: [(1, 1), (2, 5)],
    }
    
    dist, prev = dijkstra(graph, start=0)
    print(f"从 0 到各节点的最短距离: {dist}")
    # {0: 0, 1: 4, 2: 1, 3: 5}
    
    path = shortest_path(prev, 0, 3)
    print(f"0 → 3 的最短路径: {path}")
    # [0, 1, 3] (距离 5)
```

### C++ 实现

```cpp
#include <vector>
#include <queue>
#include <limits>
#include <algorithm>

using namespace std;

typedef pair<int, int> PII;  // (distance, node)

vector<int> dijkstra(const vector<vector<PII>>& graph, int start) {
    int n = graph.size();
    vector<int> dist(n, numeric_limits<int>::max());
    vector<bool> visited(n, false);
    dist[start] = 0;
    
    // 最小堆
    priority_queue<PII, vector<PII>, greater<PII>> pq;
    pq.push({0, start});
    
    while (!pq.empty()) {
        auto [d, u] = pq.top(); pq.pop();
        
        if (visited[u]) continue;
        visited[u] = true;
        
        for (auto [v, w] : graph[u]) {
            if (!visited[v] && dist[u] + w < dist[v]) {
                dist[v] = dist[u] + w;
                pq.push({dist[v], v});
            }
        }
    }
    
    return dist;
}
```

## 与其他算法对比

| 算法 | 适用范围 | 时间复杂度 | 能否处理负权 | 能否检测负环 |
|------|---------|-----------|------------|------------|
| **Dijkstra** | 单源、非负权 | O((V+E)log V) | ❌ | ❌ |
| **Bellman-Ford** | 单源 | O(VE) | ✅ | ✅ |
| **SPFA** | 单源 | O(VE) 平均 O(E) | ✅ | ✅ |
| **Floyd-Warshall** | 全源 | O(V³) | ✅ | ❌（可检测） |
| **Johnson** | 全源（稀疏图） | O(VE + V²log V) | ✅ | ✅ |

### Bellman-Ford 示例

```python
def bellman_ford(edges: List[Tuple[int, int, int]], n: int, start: int):
    """
    edges: (u, v, weight)
    n: 节点数量
    """
    dist = [float('inf')] * n
    dist[start] = 0
    
    # 松弛 V-1 次
    for _ in range(n - 1):
        for u, v, w in edges:
            if dist[u] != float('inf') and dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
    
    # 检测负环（第 V 次松弛仍能更新）
    for u, v, w in edges:
        if dist[u] != float('inf') and dist[u] + w < dist[v]:
            return None  # 存在负环
    
    return dist
```

### Floyd-Warshall 示例

```python
def floyd_warshall(graph: List[List[float]]) -> List[List[float]]:
    """graph[i][j] = 从 i 到 j 的直接距离（无穷大表示不直接相连）"""
    n = len(graph)
    dist = [row[:] for row in graph]
    
    for k in range(n):          # 中间节点
        for i in range(n):      # 起点
            for j in range(n):  # 终点
                if dist[i][k] + dist[k][j] < dist[i][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]
    
    return dist
```

## 应用场景

| 场景 | 说明 |
|------|------|
| **导航系统** | 地图中最短路径计算（Google Maps、高德） |
| **网络路由** | OSPF 协议使用 Dijkstra 计算最短路由 |
| **社交网络** | "六度分隔"理论中的最短路径 |
| **物流配送** | 配送路径优化 |
| **通信网络** | 数据包传输路径选择 |
| **游戏 AI** | NPC 寻路（结合网格地图） |

### 实际应用：导航简化示例

```python
def navigate(map_graph, start, end):
    """简化导航系统"""
    dist, prev = dijkstra(map_graph, start)
    
    if dist[end] == float('inf'):
        return None, "无法到达"
    
    path = shortest_path(prev, start, end)
    return path, f"总距离: {dist[end]}km"

# 城市间道路（距离单位：km）
roads = {
    "北京": [("天津", 120), ("石家庄", 280)],
    "天津": [("北京", 120), ("济南", 320)],
    "石家庄": [("北京", 280), ("郑州", 400)],
    "济南": [("天津", 320), ("南京", 600)],
    "郑州": [("石家庄", 400), ("武汉", 500)],
    "南京": [("济南", 600), ("上海", 300)],
    "武汉": [("郑州", 500), ("南京", 550)],
    "上海": [("南京", 300)],
}

path, info = navigate(roads, "北京", "上海")
print(f"路径: {' → '.join(path)}")  # 北京 → 天津 → 济南 → 南京 → 上海
print(info)  # 总距离: 1340km
```

## 优化与变种

| 变种 | 说明 | 实现要点 |
|------|------|---------|
| **双向 Dijkstra** | 同时从起点和终点搜索，相遇时停止 | 维护两个方向的 dist 和 pq |
| **A\* 算法** | 加入启发式函数（如欧几里得距离）加速 | 估计函数 h(n) 必须可采纳（admissible） |
| **多源 Dijkstra** | 多个起点同时开始 | 初始将所有起点加入 pq |
| **K 短路** | 找第 K 短路径 | Yen 算法或 Eppstein 算法 |

### A* 算法示例

```python
import heapq
import math

def a_star(graph: Graph, start: int, goal: int, 
           heuristic: Dict[int, float]) -> List[int]:
    """A* 寻路算法"""
    dist = {node: float('inf') for node in graph}
    prev = {node: None for node in graph}
    dist[start] = 0
    
    # (f_score, g_score, node)
    pq = [(heuristic[start], 0, start)]
    
    while pq:
        f, g, u = heapq.heappop(pq)
        
        if u == goal:
            break
        
        if g > dist[u]:
            continue
        
        for v, w in graph[u]:
            new_g = g + w
            if new_g < dist[v]:
                dist[v] = new_g
                prev[v] = u
                f = new_g + heuristic[v]
                heapq.heappush(pq, (f, new_g, v))
    
    return shortest_path(prev, start, goal)
```

## 常见错误与注意事项

| 错误 | 说明 | 解决方法 |
|------|------|---------|
| 处理负权边 | Dijkstra 在负权图上会给出错误结果 | 使用 Bellman-Ford 或 SPFA |
| 未使用 visited | 重复处理节点（堆优化版本可能） | 记录已确定最短路径的节点 |
| 整数溢出 | 初始化 `inf` 不够大 | 使用 `float('inf')` 或 `INT_MAX/2` |
| 堆中过时条目 | 更新距离后旧条目仍在堆中 | 检查 `current_dist > dist[u]` |
| 稠密图用堆 | 稠密图 O(V²) 可能更快 | 评估 E ≈ V² 时考虑朴素实现 |

## 相关条目

- [[Graph]]
- [[BFSDFS]]
- [[MST]]
- [[Heap]]
- [[DP]]
