---
aliases: [Backtracking]
tags: ['DataStructuresAndAlgorithms', 'Algorithms', 'Backtracking']
created: 2026-05-16
updated: 2026-05-13
---

# 回溯算法详解

## 基本概念

回溯算法（Backtracking）是一种通过**尝试所有可能**来解决问题的算法，核心是**选择-探索-撤销**这一循环。

### 回溯框架

```python
def backtrack(path, choices):
    if is_solution(path):
        output(path)
        return
    
    for choice in choices:
        if is_valid(choice):
            # 做选择
            make_choice(path, choice)
            
            # 递归探索
            backtrack(path, next_choices)
            
            # 撤销选择
            undo_choice(path, choice)
```

### 回溯 vs DFS

回溯是 DFS 的一种特殊形式：
- **DFS**：遍历所有节点，通常无状态回滚
- **回溯**：在搜索过程中维护状态，必须撤销选择

## 核心问题

### 1. 全排列 (LeetCode 46)

```python
def permute(nums):
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
```

**时间复杂度**: O(n × n!)
**空间复杂度**: O(n) 递归栈

### 2. 组合 (LeetCode 77)

```python
def combine(n, k):
    """从 1..n 中选 k 个数的所有组合"""
    result = []
    
    def backtrack(start, path):
        if len(path) == k:
            result.append(path[:])
            return
        
        for i in range(start, n + 1):
            path.append(i)
            backtrack(i + 1, path)
            path.pop()
    
    backtrack(1, [])
    return result
```

### 3. 子集 (LeetCode 78)

```python
def subsets(nums):
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

**时间复杂度**: O(n × 2^n)

### 4. N 皇后 (LeetCode 51)

```python
def solve_n_queens(n):
    """N 皇后问题的所有解"""
    result = []
    board = [['.'] * n for _ in range(n)]
    cols = set()
    diag1 = set()  # 主对角线: row - col
    diag2 = set()  # 副对角线: row + col
    
    def backtrack(row):
        if row == n:
            result.append([''.join(r) for r in board])
            return
        
        for col in range(n):
            if col in cols or (row - col) in diag1 or (row + col) in diag2:
                continue
            
            board[row][col] = 'Q'
            cols.add(col)
            diag1.add(row - col)
            diag2.add(row + col)
            
            backtrack(row + 1)
            
            board[row][col] = '.'
            cols.remove(col)
            diag1.remove(row - col)
            diag2.remove(row + col)
    
    backtrack(0)
    return result
```

**时间复杂度**: O(n!)

### 5. 数独求解器 (LeetCode 37)

```python
def solve_sudoku(board):
    """解数独"""
    rows = [set() for _ in range(9)]
    cols = [set() for _ in range(9)]
    boxes = [set() for _ in range(9)]
    
    for i in range(9):
        for j in range(9):
            if board[i][j] != '.':
                val = board[i][j]
                rows[i].add(val)
                cols[j].add(val)
                boxes[(i // 3) * 3 + j // 3].add(val)
    
    def backtrack(i, j):
        if i == 9:
            return True
        if j == 9:
            return backtrack(i + 1, 0)
        if board[i][j] != '.':
            return backtrack(i, j + 1)
        
        for num in map(str, range(1, 10)):
            box_idx = (i // 3) * 3 + j // 3
            if num not in rows[i] and num not in cols[j] and num not in boxes[box_idx]:
                board[i][j] = num
                rows[i].add(num)
                cols[j].add(num)
                boxes[box_idx].add(num)
                
                if backtrack(i, j + 1):
                    return True
                
                board[i][j] = '.'
                rows[i].remove(num)
                cols[j].remove(num)
                boxes[box_idx].remove(num)
        
        return False
    
    backtrack(0, 0)
    return board
```

### 6. 括号生成 (LeetCode 22)

```python
def generate_parenthesis(n):
    """生成 n 对括号的所有有效组合"""
    result = []
    
    def backtrack(s, left, right):
        if len(s) == 2 * n:
            result.append(s)
            return
        
        if left < n:
            backtrack(s + '(', left + 1, right)
        if right < left:
            backtrack(s + ')', left, right + 1)
    
    backtrack('', 0, 0)
    return result
```

### 7. 单词搜索 (LeetCode 79)

```python
def exist(board, word):
    """判断单词是否存在于网格中"""
    m, n = len(board), len(board[0])
    
    def backtrack(i, j, idx):
        if idx == len(word):
            return True
        
        if i < 0 or i >= m or j < 0 or j >= n or board[i][j] != word[idx]:
            return False
        
        temp = board[i][j]
        board[i][j] = '#'  # 标记已访问
        
        found = any(backtrack(i + di, j + dj, idx + 1)
                    for di, dj in [(0,1), (1,0), (0,-1), (-1,0)])
        
        board[i][j] = temp  # 恢复
        return found
    
    for i in range(m):
        for j in range(n):
            if backtrack(i, j, 0):
                return True
    return False
```

**剪枝优化**:
```python
def exist_optimized(board, word):
    """剪枝：反向检查、字符频率检查"""
    m, n = len(board), len(word)
    
    # 字符频率检查
    from collections import Counter
    board_counter = Counter(c for row in board for c in row)
    word_counter = Counter(word)
    for c in word_counter:
        if word_counter[c] > board_counter.get(c, 0):
            return False
    
    # 从低频端开始搜索
    if word_counter.get(word[0], 0) > word_counter.get(word[-1], 0):
        word = word[::-1]
    
    # ... 同上的 backtrack
```

### 8. 组合总和 (LeetCode 39)

```python
def combination_sum(candidates, target):
    """无重复数字，可重复使用，找和为 target 的组合"""
    result = []
    
    def backtrack(start, path, remaining):
        if remaining == 0:
            result.append(path[:])
            return
        if remaining < 0:
            return
        
        for i in range(start, len(candidates)):
            path.append(candidates[i])
            backtrack(i, path, remaining - candidates[i])
            path.pop()
    
    backtrack(0, [], target)
    return result
```

### 9. 组合总和 II (LeetCode 40)

```python
def combination_sum2(candidates, target):
    """每个数字只能用一次"""
    candidates.sort()
    result = []
    
    def backtrack(start, path, remaining):
        if remaining == 0:
            result.append(path[:])
            return
        
        for i in range(start, len(candidates)):
            if i > start and candidates[i] == candidates[i - 1]:
                continue  # 去重
            if candidates[i] > remaining:
                break    # 剪枝
            
            path.append(candidates[i])
            backtrack(i + 1, path, remaining - candidates[i])
            path.pop()
    
    backtrack(0, [], target)
    return result
```

### 10. 分割回文串 (LeetCode 131)

```python
def partition(s):
    """分割字符串使每部分都是回文"""
    result = []
    
    def is_palindrome(sub):
        return sub == sub[::-1]
    
    def backtrack(start, path):
        if start == len(s):
            result.append(path[:])
            return
        
        for end in range(start + 1, len(s) + 1):
            if is_palindrome(s[start:end]):
                path.append(s[start:end])
                backtrack(end, path)
                path.pop()
    
    backtrack(0, [])
    return result
```

## 剪枝技巧

1. **可行性剪枝**: 不满足条件的分支直接跳过
2. **最优性剪枝**: 当前已无法得到更优解
3. **重复剪枝**: 避免搜索重复状态
4. **对称剪枝**: 利用问题对称性

```python
# 剪枝示例：全排列去重
def permute_unique(nums):
    nums.sort()
    result = []
    visited = [False] * len(nums)
    
    def backtrack(path):
        if len(path) == len(nums):
            result.append(path[:])
            return
        
        for i in range(len(nums)):
            if visited[i]:
                continue
            # 去重剪枝：相同数字只选第一个未使用的
            if i > 0 and nums[i] == nums[i - 1] and not visited[i - 1]:
                continue
            
            visited[i] = True
            path.append(nums[i])
            backtrack(path)
            path.pop()
            visited[i] = False
    
    backtrack([])
    return result
```

## 时间复杂度分析

回溯的时间复杂度通常由**解空间大小 × 每次操作的时间**决定。

| 问题 | 解空间 | 时间复杂度 |
|-----|--------|-----------|
| 全排列 (n!) | n! | O(n × n!) |
| 子集 (2ⁿ) | 2ⁿ | O(n × 2ⁿ) |
| N 皇后 | n! | O(n!) |
| 数独 | 9^(空位) | 指数级（剪枝后小很多） |
| 组合 | C(n,k) | O(k × C(n,k)) |
| 括号生成 | 卡特兰数 | O(4ⁿ / √n) |

## 练习

| 题目 | 难度 | 核心技巧 |
|------|------|---------|
| LeetCode 46. 全排列 | 🟡 中等 | 基础回溯 |
| LeetCode 47. 全排列 II | 🟡 中等 | 去重剪枝 |
| LeetCode 78. 子集 | 🟡 中等 | 子集模板 |
| LeetCode 90. 子集 II | 🟡 中等 | 去重 |
| LeetCode 77. 组合 | 🟡 中等 | 组合模板 |
| LeetCode 39. 组合总和 | 🟡 中等 | 可重复选 |
| LeetCode 40. 组合总和 II | 🟡 中等 | 不可重复+去重 |
| LeetCode 22. 括号生成 | 🟡 中等 | 括号匹配 |
| LeetCode 51. N 皇后 | 🔴 困难 | 经典回溯 |
| LeetCode 37. 解数独 | 🔴 困难 | 剪枝 |
| LeetCode 79. 单词搜索 | 🟡 中等 | 网格回溯 |
| LeetCode 131. 分割回文串 | 🟡 中等 | 分割 |
| LeetCode 17. 电话号码字母组合 | 🟡 中等 | 映射+回溯 |

## 相关条目

- [[DP]]
- [[BFSDFS]]
- [[Greedy]]
- [[BitManipulation]]
- [[BasicAlgorithms]]
