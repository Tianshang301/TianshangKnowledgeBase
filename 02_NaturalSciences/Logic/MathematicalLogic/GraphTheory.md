# 图论详解

## 一、图的基本类型

### 图的定义

图 $G = (V, E)$ 由顶点集 $V$ 和边集 $E$ 组成。

**握手引理 (Handshaking Lemma)**：
$$\sum_{v \in V} \deg(v) = 2|E|$$
无向图中奇度数顶点的个数必为偶数。

### 图分类

- **无向图**：边无方向；**有向图**：边有方向
- **简单图**：无自环、无重边；**多重图**：允许重边
- **赋权图**：边有权重；**无权图**：边无权重
- **完全图 $K_n$**：每对不同顶点间恰有一条边
- **二部图 (Bipartite)**：顶点可分成两组，边只存在于不同组之间
- **正则图**：所有顶点度数相同
- **平面图**：可画在平面上无边交叉

## 二、图的表示

| 表示法 | 描述 | 空间复杂度 |
|--------|------|-----------|
| 邻接矩阵 | $A_{ij} = 1$ 若 $i$ 与 $j$ 相连 | $O(V^2)$ |
| 邻接表 | 每个顶点存相邻顶点列表 | $O(V + E)$ |
| 关联矩阵 | 行 = 顶点，列 = 边 | $O(V \times E)$ |

```python
# 邻接表表示
graph = {
    0: [1, 2],
    1: [0, 3],
    2: [0, 3],
    3: [1, 2]
}

# 邻接矩阵表示
import numpy as np
adj_matrix = np.array([
    [0, 1, 1, 0],
    [1, 0, 0, 1],
    [1, 0, 0, 1],
    [0, 1, 1, 0]
])
```

## 三、连通性

### 路与圈

- **路 (Path)**：顶点序列，相邻顶点间有边，不重复顶点
- **圈 (Cycle)**：起点 = 终点的路，其余顶点不重复
- **简单路**：不含重复顶点

### 无向图的连通性

- **连通图**：任意两顶点间存在路径
- **连通分量**：极大连通子图
- **桥 (Bridge)**：删除后增加连通分量数的边
- **割点 (Articulation Point)**：删除后增加连通分量数的顶点

### 有向图的连通性

- **强连通**：任意两顶点间双向可达
- **弱连通**：忽略方向后连通
- **强连通分量 (SCC)**：极大强连通子图

**Kosaraju 算法**：
1. 对图进行 DFS 记录完成顺序
2. 反转图
3. 按完成顺序的逆序在反转图上 DFS

**Tarjan 算法**：一次 DFS 用时间戳和 lowlink 找出 SCC。

## 四、树 (Trees)

### 树的性质

连通无环图。$n$ 个顶点的树有 $n-1$ 条边。

**Cayley 公式**：$n$ 个标号顶点的树的数量为：
$$T(n) = n^{n-2}$$
**树的基本性质**：
$$|E| = |V| - 1, \quad \sum \deg(v) = 2(|V| - 1)$$

- **生成树 (Spanning Tree)**：包含所有顶点的树子图
- **根树 (Rooted Tree)**：指定一个根节点
- **二叉树**：每个节点最多两个子节点
- **最小生成树 (MST)**：权重和最小的生成树

**Prim 算法**：从任一顶点开始，每次加入最小权边连接新顶点。$O(E \log V)$

**Kruskal 算法**：按权重从小到大加边，不形成环。$O(E \log E)$

## 五、欧拉图与哈密顿图

### 欧拉路径/回路

- **欧拉回路**：经过每条边恰好一次的回路
- **欧拉路径**：经过每条边恰好一次的路径

**判定**：
- 无向图有欧拉回路 $\iff$ 所有顶点度数为偶数
- 无向图有欧拉路径 $\iff$ 恰有 0 或 2 个奇度数顶点
- 有向图有欧拉回路 $\iff$ 每个顶点入度 = 出度

**Hierholzer 算法**：从奇度顶点开始，DFS 找回路并合并。

### 哈密顿路径/回路

- **哈密顿回路**：经过每个顶点恰好一次的回路
- **哈密顿路径**：经过每个顶点恰好一次的路径

无简单充要条件（NP-完全问题）。

**Dirac 定理**：若 $\forall v \in V, \deg(v) \geq n/2$，则图有哈密顿回路。

**Ore 定理**：若 $\forall u,v \in V, (u,v) \notin E \implies \deg(u) + \deg(v) \geq n$，则图有哈密顿回路。

**完全图 $K_n$ 中的哈密顿回路数**：
$$\frac{(n-1)!}{2} \quad (\text{不计同构})$$

## 六、二部图匹配

### 霍尔定理 (Hall's Theorem)

二部图 $G = (X \cup Y, E)$ 存在 $X$ 的完全匹配 $\iff$ $\forall S \subseteq X, |N(S)| \geq |S|$。

### 匈牙利算法

用于求二部图的最大匹配。$O(VE)$。

## 七、图着色

### 顶点着色

- **色数 $\chi(G)$**：所需最少颜色数
- **贪心着色**：按某种顺序给每个顶点涂最小的可用颜色，最多 $\Delta+1$ 种颜色
- **Brooks 定理**：若 $G$ 不是完全图或奇圈，则 $\chi(G) \leq \Delta(G)$
- **四色定理**：平面图可 4-着色，即 $\chi(G) \leq 4$（对平面图 $G$）

## 八、网络流

### 最大流

- **流网络**：有源点 $s$、汇点 $t$、容量 $c(u,v)$ 的有向图
- **可行流**：满足容量限制和流量守恒

### 最大流最小割定理

$$\max_{f} |f| = \min_{S \subset V, s \in S, t \notin S} c(S, \overline{S})$$
其中 $c(S, \overline{S}) = \sum_{u \in S} \sum_{v \notin S} c(u,v)$ 为割的容量。

### Ford-Fulkerson 算法

```python
def ford_fulkerson(graph, s, t):
    n = len(graph)
    flow = 0
    while True:
        # BFS 找增广路
        parent = [-1] * n
        parent[s] = s
        queue = [s]
        while queue and parent[t] == -1:
            u = queue.pop(0)
            for v in range(n):
                if parent[v] == -1 and graph[u][v] > 0:
                    parent[v] = u
                    queue.append(v)
        if parent[t] == -1:
            break
        # 找瓶颈容量
        v = t; bottleneck = float('inf')
        while v != s:
            u = parent[v]
            bottleneck = min(bottleneck, graph[u][v])
            v = u
        # 更新
        v = t
        while v != s:
            u = parent[v]
            graph[u][v] -= bottleneck
            graph[v][u] += bottleneck
            v = u
        flow += bottleneck
    return flow
```

**Edmonds-Karp**：Ford-Fulkerson 的 BFS 实现，$O(VE^2)$。
