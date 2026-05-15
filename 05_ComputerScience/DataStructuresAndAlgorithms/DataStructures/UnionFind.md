# 并查集

## 基本概念

并查集（Union-Find / Disjoint Set Union, DSU）是一种用于处理**不相交集合**的数据结构，支持以下操作：
- **Find**: 查找元素所属集合的根
- **Union**: 合并两个元素所在的集合
- **Connected**: 判断两个元素是否属于同一集合

## 实现演进

### 1. Quick-Find (快速查找)

```python
class QuickFind:
    def __init__(self, n):
        self.root = list(range(n))  # root[i] = 元素 i 所在的集合标识
    
    def find(self, x):
        """O(1)"""
        return self.root[x]
    
    def union(self, x, y):
        """O(n) — 需要将所有属于 root[x] 的元素改标"""
        root_x = self.find(x)
        root_y = self.find(y)
        if root_x != root_y:
            for i in range(len(self.root)):
                if self.root[i] == root_x:
                    self.root[i] = root_y
    
    def connected(self, x, y):
        return self.find(x) == self.find(y)
```

| 操作 | 时间复杂度 |
|-----|-----------|
| Find | O(1) |
| Union | O(n) |

### 2. Quick-Union (快速合并)

```python
class QuickUnion:
    def __init__(self, n):
        self.parent = list(range(n))  # parent[i] = 元素 i 的父节点
    
    def find(self, x):
        """O(h) — h 为树的高度"""
        while self.parent[x] != x:
            x = self.parent[x]
        return x
    
    def union(self, x, y):
        """O(h)"""
        root_x = self.find(x)
        root_y = self.find(y)
        if root_x != root_y:
            self.parent[root_x] = root_y  # 将 x 的根指向 y 的根
    
    def connected(self, x, y):
        return self.find(x) == self.find(y)
```

| 操作 | 时间复杂度 |
|-----|-----------|
| Find | O(h) |
| Union | O(h) |

### 3. 按秩合并 (Union by Rank)

避免树退化为链表，将较矮的树合并到较高的树上。

```python
class UnionByRank:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n  # 树的高度（秩）
    
    def find(self, x):
        while self.parent[x] != x:
            x = self.parent[x]
        return x
    
    def union(self, x, y):
        root_x = self.find(x)
        root_y = self.find(y)
        
        if root_x == root_y:
            return
        
        # 按秩合并：将矮树合并到高树上
        if self.rank[root_x] < self.rank[root_y]:
            self.parent[root_x] = root_y
        elif self.rank[root_x] > self.rank[root_y]:
            self.parent[root_y] = root_x
        else:
            self.parent[root_y] = root_x
            self.rank[root_x] += 1
```

### 4. 路径压缩 (Path Compression)

在 find 过程中将路径上所有节点直接指向根。

```python
class UnionFind:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n
        self.size = [1] * n  # 可选：记录集合大小
        self.count = n       # 集合数量
    
    def find(self, x):
        """路径压缩 — 接近 O(1)"""
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]
    
    def find_iterative(self, x):
        """迭代版路径压缩"""
        root = x
        while self.parent[root] != root:
            root = self.parent[root]
        # 路径压缩
        while x != root:
            next_node = self.parent[x]
            self.parent[x] = root
            x = next_node
        return root
    
    def union(self, x, y):
        """按秩合并"""
        root_x = self.find(x)
        root_y = self.find(y)
        
        if root_x == root_y:
            return
        
        if self.rank[root_x] < self.rank[root_y]:
            self.parent[root_x] = root_y
            self.size[root_y] += self.size[root_x]
        elif self.rank[root_x] > self.rank[root_y]:
            self.parent[root_y] = root_x
            self.size[root_x] += self.size[root_y]
        else:
            self.parent[root_y] = root_x
            self.rank[root_x] += 1
            self.size[root_x] += self.size[root_y]
        
        self.count -= 1
    
    def connected(self, x, y):
        return self.find(x) == self.find(y)
    
    def get_size(self, x):
        """返回 x 所在集合的元素个数"""
        root = self.find(x)
        return self.size[root]
```

## 时间复杂度

使用**路径压缩 + 按秩合并**后：

| 操作 | 均摊时间复杂度 |
|-----|---------------|
| Find | O(α(n)) — Ackermann 反函数 |
| Union | O(α(n)) |
| 任何 M 次操作 | O(M α(n)) |

其中 α(n) ≈ 4 对于任何实际可行的大小（n ≤ 2^65536），因此可视为**近似 O(1)**。

## Python 简洁实现

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
```

## 应用场景

### 1. 连通分量

```python
def count_components(n, edges):
    """计算无向图的连通分量数"""
    dsu = UnionFind(n)
    for u, v in edges:
        dsu.union(u, v)
    return dsu.count
```

### 2. Kruskal 最小生成树

```python
def kruskal(n, edges):
    """Kruskal 算法求 MST"""
    edges.sort(key=lambda x: x[2])  # 按权重排序
    dsu = UnionFind(n)
    mst_weight = 0
    mst_edges = []
    
    for u, v, w in edges:
        if dsu.union(u, v):
            mst_weight += w
            mst_edges.append((u, v, w))
    
    return mst_weight, mst_edges
```

### 3. 岛屿数量 (LeetCode 200)

```python
def num_islands(grid):
    """并查集解法"""
    if not grid:
        return 0
    
    m, n = len(grid), len(grid[0])
    dsu = UnionFind(m * n)
    
    def idx(i, j):
        return i * n + j
    
    for i in range(m):
        for j in range(n):
            if grid[i][j] == '1':
                # 合并右边和下边
                if i + 1 < m and grid[i+1][j] == '1':
                    dsu.union(idx(i, j), idx(i+1, j))
                if j + 1 < n and grid[i][j+1] == '1':
                    dsu.union(idx(i, j), idx(i, j+1))
            else:
                dsu.count -= 1  # 水域不计
    
    return dsu.count
```

### 4. 冗余连接 (LeetCode 684)

```python
def find_redundant_connection(edges):
    """找到导致环的多余边"""
    n = len(edges)
    dsu = UnionFind(n + 1)  # 节点从 1 开始
    
    for u, v in edges:
        if dsu.connected(u, v):
            return [u, v]
        dsu.union(u, v)
    
    return []
```

### 5. 等式方程的可满足性 (LeetCode 990)

```python
def equations_possible(equations):
    """判断等式方程组是否可满足"""
    dsu = UnionFind(26)  # 26 个小写字母
    
    # 先处理所有相等关系
    for eq in equations:
        if eq[1] == '=':
            x = ord(eq[0]) - ord('a')
            y = ord(eq[3]) - ord('a')
            dsu.union(x, y)
    
    # 再检查所有不等关系
    for eq in equations:
        if eq[1] == '!':
            x = ord(eq[0]) - ord('a')
            y = ord(eq[3]) - ord('a')
            if dsu.connected(x, y):
                return False
    
    return True
```

### 6. 被围绕的区域 (LeetCode 130)

```python
def solve(board):
    """将不被 'X' 包围的 'O' 标记"""
    if not board:
        return
    
    m, n = len(board), len(board[0])
    dsu = UnionFind(m * n + 1)
    dummy = m * n  # 虚拟节点，连接所有边界 'O'
    
    for i in range(m):
        for j in range(n):
            if board[i][j] == 'O':
                if i == 0 or i == m-1 or j == 0 or j == n-1:
                    dsu.union(i * n + j, dummy)
                else:
                    for di, dj in [(0,1), (1,0), (0,-1), (-1,0)]:
                        ni, nj = i + di, j + dj
                        if board[ni][nj] == 'O':
                            dsu.union(i * n + j, ni * n + nj)
    
    for i in range(m):
        for j in range(n):
            if board[i][j] == 'O' and not dsu.connected(i * n + j, dummy):
                board[i][j] = 'X'
```

### 7. 朋友圈 (LeetCode 547)

```python
def find_circle_num(is_connected):
    """省份数量（朋友圈）"""
    n = len(is_connected)
    dsu = UnionFind(n)
    
    for i in range(n):
        for j in range(i + 1, n):
            if is_connected[i][j]:
                dsu.union(i, j)
    
    return dsu.count
```

## 练习

| 题目 | 难度 | 核心技巧 |
|------|------|---------|
| LeetCode 200. 岛屿数量 | 🟡 中等 | 并查集/DFS/BFS |
| LeetCode 547. 省份数量 | 🟡 中等 | 并查集 |
| LeetCode 684. 冗余连接 | 🟡 中等 | 并查集检测环 |
| LeetCode 990. 等式可满足性 | 🟡 中等 | 并查集 |
| LeetCode 130. 被围绕的区域 | 🟡 中等 | 并查集/虚拟节点 |
| LeetCode 128. 最长连续序列 | 🟡 中等 | 并查集/哈希 |
| LeetCode 323. 无向图连通分量 | 🟡 中等 | 并查集 |
| LeetCode 261. 图是否是树 | 🟡 中等 | 并查集 |
| LeetCode 721. 账户合并 | 🟡 中等 | 并查集 |
| LeetCode 1202. 交换字符串元素 | 🟡 中等 | 并查集 |
| LeetCode 765. 情侣牵手 | 🔴 困难 | 并查集/贪心 |

## 相关条目

- [[Graph]]
- [[BFSDFS]]
- [[MST]]
- [[SegmentTree]]
- [[HashTable]]
