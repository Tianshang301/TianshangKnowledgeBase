# BFS / DFS 详解

## 概述

BFS（广度优先搜索）和 DFS（深度优先搜索）是两种最基本的图遍历算法，也是许多高级算法（DP、最短路径、拓扑排序）的基础。

## 深度优先搜索 (DFS)

DFS 沿着一条路径走到底，然后回溯，使用**栈**（递归或显式）。

### 基本框架

```python
# 递归版本
def dfs_recursive(graph, node, visited):
    visited.add(node)
    process(node)  # 处理当前节点
    for neighbor in graph[node]:
        if neighbor not in visited:
            dfs_recursive(graph, neighbor, visited)

# 迭代版本（显式栈）
def dfs_iterative(graph, start):
    visited = set()
    stack = [start]
    
    while stack:
        node = stack.pop()
        if node not in visited:
            visited.add(node)
            process(node)
            for neighbor in graph[node]:
                if neighbor not in visited:
                    stack.append(neighbor)
```

### DFS 的三种顺序（二叉树）

```python
# 前序 Pre-order: 根 → 左 → 右
def preorder(node):
    if not node:
        return
    process(node)
    preorder(node.left)
    preorder(node.right)

# 中序 In-order: 左 → 根 → 右
def inorder(node):
    if not node:
        return
    inorder(node.left)
    process(node)
    inorder(node.right)

# 后序 Post-order: 左 → 右 → 根
def postorder(node):
    if not node:
        return
    postorder(node.left)
    postorder(node.right)
    process(node)
```

### 回溯 (Backtracking)

DFS 的一种特殊形式，在搜索过程中记录路径，并在回溯时撤销选择。

```python
def backtrack(path, choices):
    if is_solution(path):
        output(path)
        return
    
    for choice in choices:
        if is_valid(choice):
            make_choice(path, choice)
            backtrack(path, choices)
            undo_choice(path, choice)
```

## 广度优先搜索 (BFS)

BFS 按照距离逐层访问，使用**队列**。

### 基本框架

```python
from collections import deque

def bfs(graph, start):
    visited = {start}
    queue = deque([start])
    
    while queue:
        node = queue.popleft()
        process(node)
        
        for neighbor in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
```

### 分层 BFS

```python
def bfs_levels(graph, start):
    visited = {start}
    queue = deque([start])
    level = 0
    
    while queue:
        level_size = len(queue)
        print(f"Level {level}: ", end="")
        
        for _ in range(level_size):
            node = queue.popleft()
            print(node, end=" ")
            
            for neighbor in graph[node]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)
        
        print()  # 换行
        level += 1
```

## BFS vs DFS 对比

| 特性 | BFS | DFS |
|-----|-----|-----|
| 数据结构 | 队列 (Queue) | 栈 (Stack / 递归) |
| 空间复杂度 | O(w) — 最宽层 | O(h) — 深度 |
| 最短路径 | ✅ 无权图最短路径 | ❌ |
| 连通分量 | ✅ | ✅ |
| 拓扑排序 | ✅ (Kahn) | ✅ (DFS) |
| 回溯/排列 | ❌ | ✅ |
| 检测环 | ✅ | ✅ |
| 记忆化搜索 | ❌ | ✅ |

## 应用场景

### 1. 连通分量 — 岛屿数量 (LeetCode 200)

```python
# DFS 解法
def num_islands_dfs(grid):
    if not grid:
        return 0
    
    m, n = len(grid), len(grid[0])
    count = 0
    
    def dfs(i, j):
        if i < 0 or i >= m or j < 0 or j >= n or grid[i][j] != '1':
            return
        grid[i][j] = '0'  # 标记已访问
        for di, dj in [(0,1), (1,0), (0,-1), (-1,0)]:
            dfs(i + di, j + dj)
    
    for i in range(m):
        for j in range(n):
            if grid[i][j] == '1':
                count += 1
                dfs(i, j)
    
    return count

# BFS 解法
from collections import deque

def num_islands_bfs(grid):
    if not grid:
        return 0
    
    m, n = len(grid), len(grid[0])
    count = 0
    
    for i in range(m):
        for j in range(n):
            if grid[i][j] == '1':
                count += 1
                grid[i][j] = '0'
                queue = deque([(i, j)])
                
                while queue:
                    x, y = queue.popleft()
                    for dx, dy in [(0,1), (1,0), (0,-1), (-1,0)]:
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < m and 0 <= ny < n and grid[nx][ny] == '1':
                            grid[nx][ny] = '0'
                            queue.append((nx, ny))
    
    return count
```

### 2. 二分图检测 (LeetCode 785)

```python
def is_bipartite(graph):
    """判断是否为二分图（BFS 染色）"""
    n = len(graph)
    color = [-1] * n  # -1=未染色, 0=红色, 1=蓝色
    
    for i in range(n):
        if color[i] == -1:
            color[i] = 0
            queue = deque([i])
            
            while queue:
                node = queue.popleft()
                for neighbor in graph[node]:
                    if color[neighbor] == -1:
                        color[neighbor] = 1 - color[node]
                        queue.append(neighbor)
                    elif color[neighbor] == color[node]:
                        return False
    
    return True
```

### 3. 单词接龙 (LeetCode 127)

```python
def ladder_length(begin_word, end_word, word_list):
    """最短转换序列长度（BFS 最短路径）"""
    word_set = set(word_list)
    if end_word not in word_set:
        return 0
    
    queue = deque([(begin_word, 1)])
    visited = {begin_word}
    
    while queue:
        word, length = queue.popleft()
        if word == end_word:
            return length
        
        for i in range(len(word)):
            for c in 'abcdefghijklmnopqrstuvwxyz':
                new_word = word[:i] + c + word[i+1:]
                if new_word in word_set and new_word not in visited:
                    visited.add(new_word)
                    queue.append((new_word, length + 1))
    
    return 0
```

### 4. 拓扑排序

```python
# BFS (Kahn) 拓扑排序
def topo_sort_bfs(graph):
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
    
    return result if len(result) == n else []

# DFS 拓扑排序
def topo_sort_dfs(graph):
    n = len(graph)
    visited = [0] * n  # 0=未访, 1=访问中, 2=已处理
    result = []
    
    def dfs(u):
        if visited[u] == 1:
            raise ValueError("Cycle detected")
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
    
    return result[::-1]
```

### 5. 全排列 / 子集 (DFS + 回溯)

```python
def permute(nums):
    """全排列"""
    result = []
    visited = [False] * len(nums)
    
    def backtrack(path):
        if len(path) == len(nums):
            result.append(path[:])
            return
        
        for i in range(len(nums)):
            if not visited[i]:
                visited[i] = True
                path.append(nums[i])
                backtrack(path)
                path.pop()
                visited[i] = False
    
    backtrack([])
    return result

def subsets(nums):
    """子集"""
    result = []
    
    def backtrack(start, path):
        result.append(path[:])
        for i in range(start, len(nums)):
            path.append(nums[i])
            backtrack(i + 1, path)
            path.pop()
    
    backtrack(0, [])
    return result
```

### 6. 最短路径 (BFS 无权图)

```python
def shortest_path_bfs(graph, start, end):
    """无权图最短路径"""
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

### 7. 矩阵中的最长递增路径 (LeetCode 329)

```python
def longest_increasing_path(matrix):
    """DFS + 记忆化搜索"""
    if not matrix:
        return 0
    
    m, n = len(matrix), len(matrix[0])
    memo = [[0] * n for _ in range(m)]
    
    def dfs(i, j):
        if memo[i][j] != 0:
            return memo[i][j]
        
        longest = 1
        for di, dj in [(0,1), (1,0), (0,-1), (-1,0)]:
            ni, nj = i + di, j + dj
            if 0 <= ni < m and 0 <= nj < n and matrix[ni][nj] > matrix[i][j]:
                longest = max(longest, 1 + dfs(ni, nj))
        
        memo[i][j] = longest
        return longest
    
    return max(dfs(i, j) for i in range(m) for j in range(n))
```

## 练习

| 题目 | 难度 | 核心技巧 |
|------|------|---------|
| LeetCode 200. 岛屿数量 | 🟡 中等 | DFS/BFS |
| LeetCode 133. 克隆图 | 🟡 中等 | DFS/BFS |
| LeetCode 207. 课程表 | 🟡 中等 | 拓扑排序 (BFS/DFS) |
| LeetCode 127. 单词接龙 | 🔴 困难 | BFS 最短路径 |
| LeetCode 329. 最长递增路径 | 🔴 困难 | DFS + 记忆化 |
| LeetCode 785. 二分图 | 🟡 中等 | BFS 染色 |
| LeetCode 46. 全排列 | 🟡 中等 | DFS 回溯 |
| LeetCode 78. 子集 | 🟡 中等 | DFS 回溯 |
| LeetCode 79. 单词搜索 | 🟡 中等 | DFS 回溯 |
| LeetCode 130. 被围绕区域 | 🟡 中等 | DFS/BFS 边界 |
| LeetCode 417. 太平洋大西洋 | 🟡 中等 | DFS 双源 |
| LeetCode 695. 岛屿最大面积 | 🟡 中等 | DFS |
| LeetCode 994. 腐烂的橘子 | 🟡 中等 | BFS 多源 |

## 相关条目

- [[Graph]]
- [[Backtracking]]
- [[Dijkstra]]
- [[Tree]]
- [[UnionFind]]
