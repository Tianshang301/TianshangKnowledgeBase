---
aliases: [DP]
tags: ['DataStructuresAndAlgorithms', 'Algorithms', 'DP']
---

# 动态规划详解

## 基本概念

动态规划（Dynamic Programming, DP）是一种通过将问题分解为重叠子问题来求解的算法思想。

### 核心要素

1. **最优子结构 (Optimal Substructure)**：问题的最优解包含子问题的最优解
2. **重叠子问题 (Overlapping Subproblems)**：子问题被重复计算多次
3. **无后效性**：当前状态确定后，后续决策不受之前路径影响

### 两种实现方式

| 方式 | 方法 | 特点 |
|-----|------|------|
| **自顶向下 (Top-down)** | 递归 + 记忆化 | 不计算无用子问题，有递归栈开销 |
| **自底向上 (Bottom-up)** | 迭代填表 | 没有递归开销，可能计算无用子问题 |

```python
# 自顶向下：递归 + 记忆化
def fib_memo(n, memo=None):
    if memo is None:
        memo = {}
    if n <= 1:
        return n
    if n not in memo:
        memo[n] = fib_memo(n - 1, memo) + fib_memo(n - 2, memo)
    return memo[n]

# 自底向上：迭代
def fib_dp(n):
    if n <= 1:
        return n
    dp = [0] * (n + 1)
    dp[1] = 1
    for i in range(2, n + 1):
        dp[i] = dp[i - 1] + dp[i - 2]
    return dp[n]

# 空间优化
def fib_optimized(n):
    if n <= 1:
        return n
    prev2, prev1 = 0, 1
    for _ in range(2, n + 1):
        curr = prev1 + prev2
        prev2, prev1 = prev1, curr
    return prev1
```

## DP 解题框架

```
1. 定义状态：dp[i] / dp[i][j] 表示什么？
2. 确定状态转移方程：dp[i] = f(dp[i-1], dp[i-2], ...)
3. 初始化：边界条件
4. 遍历顺序：正序/逆序
5. 返回结果：dp[n] / max(dp)
```

## 经典问题

### 1. 爬楼梯 (LeetCode 70)

```python
def climb_stairs(n):
    """每次爬 1 或 2 阶，到达楼顶的方法数"""
    if n <= 2:
        return n
    dp = [0] * (n + 1)
    dp[1], dp[2] = 1, 2
    for i in range(3, n + 1):
        dp[i] = dp[i - 1] + dp[i - 2]
    return dp[n]
```

- 状态定义：dp[i] = 爬到第 i 阶的方法数
- 转移方程：dp[i] = dp[i-1] + dp[i-2]
- 时间/空间：O(n) / O(1) 优化后

### 2. 0/1  背包问题

```python
def knapsack_01(weights, values, capacity):
    """0/1 背包：每个物品最多选一次"""
    n = len(weights)
    dp = [0] * (capacity + 1)
    
    for i in range(n):
        for w in range(capacity, weights[i] - 1, -1):
            dp[w] = max(dp[w], dp[w - weights[i]] + values[i])
    
    return dp[capacity]
```

- 状态定义：dp[w] = 容量 w 时的最大价值
- 转移方程：dp[w] = max(dp[w], dp[w-wi] + vi)
- 时间复杂度：O(n × C)
- 空间复杂度：O(C)

#### 完全背包

```python
def knapsack_complete(weights, values, capacity):
    """完全背包：每个物品无限次使用"""
    n = len(weights)
    dp = [0] * (capacity + 1)
    
    for i in range(n):
        for w in range(weights[i], capacity + 1):
            dp[w] = max(dp[w], dp[w - weights[i]] + values[i])
    
    return dp[capacity]
```

注意 0/1 背包逆序遍历容量，完全背包**正序**遍历。

### 3. 零钱兑换 (LeetCode 322)

```python
def coin_change(coins, amount):
    """凑成 amount 所需的最少硬币数"""
    dp = [float('inf')] * (amount + 1)
    dp[0] = 0
    
    for coin in coins:
        for a in range(coin, amount + 1):
            dp[a] = min(dp[a], dp[a - coin] + 1)
    
    return dp[amount] if dp[amount] != float('inf') else -1
```

- 状态定义：dp[a] = 凑成金额 a 的最少硬币数
- 转移方程：dp[a] = min(dp[a], dp[a - coin] + 1)

### 4. 最长公共子序列 (LeetCode 1143)

```python
def longest_common_subsequence(text1, text2):
    """LCS — 最长公共子序列"""
    m, n = len(text1), len(text2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if text1[i - 1] == text2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
    
    return dp[m][n]
```

- 状态定义：dp[i][j] = text1[0..i-1] 和 text2[0..j-1] 的 LCS 长度
- 转移方程：
  - 如果 text1[i-1] == text2[j-1]: dp[i][j] = dp[i-1][j-1] + 1
  - 否则: dp[i][j] = max(dp[i-1][j], dp[i][j-1])
- 时间/空间：O(mn)

### 5. 最长递增子序列 (LeetCode 300)

```python
def length_of_lis(nums):
    """LIS — O(n²) DP"""
    if not nums:
        return 0
    
    dp = [1] * len(nums)
    for i in range(len(nums)):
        for j in range(i):
            if nums[j] < nums[i]:
                dp[i] = max(dp[i], dp[j] + 1)
    
    return max(dp)

def length_of_lis_optimized(nums):
    """LIS — O(n log n) 贪心 + 二分"""
    import bisect
    piles = []
    for num in nums:
        idx = bisect.bisect_left(piles, num)
        if idx == len(piles):
            piles.append(num)
        else:
            piles[idx] = num
    return len(piles)
```

- O(n²) DP：dp[i] = 以 nums[i] 结尾的 LIS 长度
- O(n log n)：维护每个长度的最小末尾值

### 6. 编辑距离 (LeetCode 72)

```python
def min_distance(word1, word2):
    """编辑距离：插入/删除/替换"""
    m, n = len(word1), len(word2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    
    for i in range(m + 1):
        dp[i][0] = i
    for j in range(n + 1):
        dp[0][j] = j
    
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if word1[i - 1] == word2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = 1 + min(
                    dp[i - 1][j],      # 删除
                    dp[i][j - 1],      # 插入
                    dp[i - 1][j - 1]   # 替换
                )
    
    return dp[m][n]
```

### 7. 最大子数组和 (LeetCode 53)

```python
def max_subarray(nums):
    """Kadane 算法"""
    max_ending_here = max_so_far = nums[0]
    for num in nums[1:]:
        max_ending_here = max(num, max_ending_here + num)
        max_so_far = max(max_so_far, max_ending_here)
    return max_so_far
```

- 状态定义：dp[i] = 以 nums[i] 结尾的最大子数组和
- 转移：dp[i] = max(nums[i], dp[i-1] + nums[i])
- 空间优化：O(1)

### 8. 矩阵链乘法

```python
def matrix_chain_order(dims):
    """最小标量乘法次数"""
    n = len(dims) - 1
    dp = [[0] * n for _ in range(n)]
    
    for length in range(2, n + 1):  # 链长度
        for i in range(n - length + 1):
            j = i + length - 1
            dp[i][j] = float('inf')
            for k in range(i, j):
                cost = dp[i][k] + dp[k + 1][j] + dims[i] * dims[k + 1] * dims[j + 1]
                dp[i][j] = min(dp[i][j], cost)
    
    return dp[0][n - 1]
```

- 时间复杂度：O(n³)
- 空间复杂度：O(n²)

### 9. 打家劫舍 (LeetCode 198)

```python
def rob(nums):
    """相邻不能偷的最大金额"""
    if not nums:
        return 0
    if len(nums) == 1:
        return nums[0]
    
    dp = [0] * len(nums)
    dp[0] = nums[0]
    dp[1] = max(nums[0], nums[1])
    
    for i in range(2, len(nums)):
        dp[i] = max(dp[i - 1], dp[i - 2] + nums[i])
    
    return dp[-1]

def rob_optimized(nums):
    prev = curr = 0
    for num in nums:
        prev, curr = curr, max(curr, prev + num)
    return curr
```

### 10. 股票买卖 (LeetCode 121/122/123/188/309/714)

```python
def max_profit_k_transactions(prices, k):
    """买卖股票的最佳时机（最多 k 次交易）"""
    n = len(prices)
    if n < 2 or k == 0:
        return 0
    
    if k >= n // 2:
        # 无限次交易
        profit = 0
        for i in range(1, n):
            if prices[i] > prices[i - 1]:
                profit += prices[i] - prices[i - 1]
        return profit
    
    dp = [[0] * n for _ in range(k + 1)]
    
    for t in range(1, k + 1):
        max_diff = -prices[0]
        for i in range(1, n):
            dp[t][i] = max(dp[t][i - 1], prices[i] + max_diff)
            max_diff = max(max_diff, dp[t - 1][i] - prices[i])
    
    return dp[k][n - 1]
```

## DP 常见模式

### 线性 DP
- 一维 DP：爬楼梯、最大子数组和
- 二维 DP：LCS、编辑距离、背包

### 区间 DP
```python
# 区间 DP 模板
for length in range(2, n + 1):
    for i in range(n - length + 1):
        j = i + length - 1
        for k in range(i, j):
            dp[i][j] = min(dp[i][j], dp[i][k] + dp[k+1][j] + cost)
```

### 树形 DP
```python
# 树形 DP 模板（后序遍历）
def dfs(node):
    if not node:
        return 0
    left = dfs(node.left)
    right = dfs(node.right)
    # 状态转移
    dp[node] = max(left, right) + 1  # 举例
    return dp[node]
```

### 状态压缩 DP (Bitmask)
```python
def tsp(dist, n):
    """旅行商问题 — 状态压缩 DP"""
    dp = [[float('inf')] * n for _ in range(1 << n)]
    dp[1][0] = 0  # 从 0 出发，只访问了 0
    
    for mask in range(1 << n):
        for u in range(n):
            if not (mask & (1 << u)):
                continue
            if dp[mask][u] == float('inf'):
                continue
            for v in range(n):
                if mask & (1 << v):
                    continue
                new_mask = mask | (1 << v)
                dp[new_mask][v] = min(dp[new_mask][v],
                                      dp[mask][u] + dist[u][v])
    
    return min(dp[(1 << n) - 1][v] + dist[v][0] for v in range(1, n))
```

## 练习

| 题目 | 难度 | DP 类型 |
|------|------|---------|
| LeetCode 70. 爬楼梯 | 🟢 简单 | 一维 |
| LeetCode 53. 最大子数组和 | 🟢 简单 | Kadane |
| LeetCode 121. 买卖股票最佳时机 | 🟢 简单 | 状态机 |
| LeetCode 198. 打家劫舍 | 🟡 中等 | 一维 |
| LeetCode 300. 最长递增子序列 | 🟡 中等 | 一维/二分 |
| LeetCode 322. 零钱兑换 | 🟡 中等 | 完全背包 |
| LeetCode 1143. 最长公共子序列 | 🟡 中等 | 二维 |
| LeetCode 72. 编辑距离 | 🟡 中等 | 二维 |
| LeetCode 416. 分割等和子集 | 🟡 中等 | 0/1 背包 |
| LeetCode 5. 最长回文子串 | 🟡 中等 | 区间 DP |
| LeetCode 312. 戳气球 | 🔴 困难 | 区间 DP |
| LeetCode 337. 打家劫舍 III | 🟡 中等 | 树形 DP |
| LeetCode 10. 正则表达式匹配 | 🔴 困难 | 二维 DP |
| LeetCode 887. 鸡蛋掉落 | 🔴 困难 | 二分优化 DP |

## 相关条目

- [[DynamicProgramming]]
- [[区间与状态压缩DP]]
- [[Backtracking]]
- [[Greedy]]
- [[BFSDFS]]
