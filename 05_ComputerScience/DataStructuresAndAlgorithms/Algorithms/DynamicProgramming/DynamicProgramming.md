---
aliases: [DynamicProgramming]
tags: ['DataStructuresAndAlgorithms', 'Algorithms', 'DynamicProgramming', 'DynamicProgramming']
created: 2026-05-16
updated: 2026-05-16
---

# Dynamic Programming - 动态规划

## 一、动态规划原理

动态规划（Dynamic Programming, DP）通过将问题分解为重叠子问题并利用子问题的解来求解原问题。

### 核心要素

| 要素 | 说明 |
|------|------|
| **最优子结构** | 问题的最优解包含子问题的最优解 |
| **重叠子问题** | 子问题被重复计算多次 |
| **无后效性** | 当前状态确定后，后续决策不受之前路径影响 |

### 贝尔曼方程（Bellman Equation）

$$ V(s) = \max_{a} \left\{ R(s, a) + \gamma \sum_{s'} P(s' | s, a) V(s') \right\} $$

DP 的状态转移方程本质上是贝尔曼方程的特例：

$$ dp[i] = \min_{j < i} \{ dp[j] + cost(j, i) \} $$

### 两种实现

```python
# 自顶向下（记忆化搜索）
def fib_memo(n, memo={}):
    if n <= 1:
        return n
    if n not in memo:
        memo[n] = fib_memo(n - 1, memo) + fib_memo(n - 2, memo)
    return memo[n]

# 自底向上（填表）
def fib_tab(n):
    if n <= 1:
        return n
    dp = [0] * (n + 1)
    dp[1] = 1
    for i in range(2, n + 1):
        dp[i] = dp[i - 1] + dp[i - 2]
    return dp[n]
```

| 方式 | 优点 | 缺点 |
|------|------|------|
| 记忆化搜索 | 只计算必要子问题 | 递归栈开销 |
| 自底向上 | 无递归开销 | 可能计算无用子问题 |

---

## 二、线性 DP

### 最长递增子序列（LIS）

$$ dp[i] = 1 + \max_{j < i, \text{ nums}[j] < \text{ nums}[i]} dp[j] $$

```python
def length_of_lis(nums):
    dp = [1] * len(nums)
    for i in range(len(nums)):
        for j in range(i):
            if nums[j] < nums[i]:
                dp[i] = max(dp[i], dp[j] + 1)
    return max(dp)  # O(n²)

def length_of_lis_optimized(nums):
    """O(n log n)：贪心 + 二分"""
    tails = []
    for num in nums:
        i = bisect_left(tails, num)
        if i == len(tails):
            tails.append(num)
        else:
            tails[i] = num
    return len(tails)
```

### 最长公共子序列（LCS）

$$ dp[i][j] = \begin{cases} dp[i-1][j-1] + 1 & \text{if } a_i = b_j \\ \max(dp[i-1][j], dp[i][j-1]) & \text{otherwise} \end{cases} $$

```python
def longest_common_subsequence(text1, text2):
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

---

## 三、背包问题

### 0/1 背包

$$ dp[i][w] = \max(dp[i-1][w], dp[i-1][w-w_i] + v_i) $$

```python
def knapsack_01(weights, values, capacity):
    n = len(weights)
    dp = [0] * (capacity + 1)
    for i in range(n):
        for w in range(capacity, weights[i] - 1, -1):
            dp[w] = max(dp[w], dp[w - weights[i]] + values[i])
    return dp[capacity]
```

### 完全背包

```python
def knapsack_complete(weights, values, capacity):
    n = len(weights)
    dp = [0] * (capacity + 1)
    for i in range(n):
        for w in range(weights[i], capacity + 1):  # 正序
            dp[w] = max(dp[w], dp[w - weights[i]] + values[i])
    return dp[capacity]
```

### 多重背包

```python
def knapsack_multiple(weights, values, counts, capacity):
    """二进制优化 → 转为 0/1 背包"""
    items = []
    for i in range(len(weights)):
        k = 1
        while k <= counts[i]:
            items.append((weights[i] * k, values[i] * k))
            counts[i] -= k
            k *= 2
        if counts[i] > 0:
            items.append((weights[i] * counts[i], values[i] * counts[i]))

    dp = [0] * (capacity + 1)
    for w, v in items:
        for c in range(capacity, w - 1, -1):
            dp[c] = max(dp[c], dp[c - w] + v)
    return dp[capacity]
```

| 背包类型 | 遍历顺序 | 每个物品次数 |
|---------|---------|------------|
| 0/1 背包 | 容量逆序 | 最多 1 次 |
| 完全背包 | 容量正序 | 无限次 |
| 多重背包 | 二进制优化 | 有限次 |
| 分组背包 | 每组内 0/1 | 每组选一个 |

---

## 四、编辑距离

$$ D(i,j) = \min\begin{cases} D(i-1,j) + 1 & \text{(删除)} \\ D(i,j-1) + 1 & \text{(插入)} \\ D(i-1,j-1) + \text{cost} & \text{(替换, cost=0 如果相等, 否则 1)} \end{cases} $$

```python
def edit_distance(word1, word2):
    """Levenshtein 距离"""
    m, n = len(word1), len(word2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(m + 1):
        dp[i][0] = i
    for j in range(n + 1):
        dp[0][j] = j
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            cost = 0 if word1[i - 1] == word2[j - 1] else 1
            dp[i][j] = min(dp[i - 1][j] + 1,
                           dp[i][j - 1] + 1,
                           dp[i - 1][j - 1] + cost)
    return dp[m][n]
```

---

## 五、矩阵链乘法

$$ dp[i][j] = \min_{i \leq k < j} \{ dp[i][k] + dp[k+1][j] + d_{i-1} \times d_k \times d_j \} $$

```python
def matrix_chain_order(dims):
    """最小标量乘法次数"""
    n = len(dims) - 1
    dp = [[0] * n for _ in range(n)]
    for length in range(2, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            dp[i][j] = float('inf')
            for k in range(i, j):
                cost = dp[i][k] + dp[k + 1][j] + dims[i] * dims[k + 1] * dims[j + 1]
                dp[i][j] = min(dp[i][j], cost)
    return dp[0][n - 1]
```

时间复杂度：$O(n^3)$，空间复杂度：$O(n^2)$

---

## 六、子集和与硬币找零

### 子集和

```python
def subset_sum(nums, target):
    """判断是否能选出若干数使和为 target"""
    dp = [False] * (target + 1)
    dp[0] = True
    for num in nums:
        for s in range(target, num - 1, -1):
            if dp[s - num]:
                dp[s] = True
    return dp[target]
```

### 硬币找零

```python
def coin_change(coins, amount):
    """最少硬币数凑成 amount"""
    dp = [float('inf')] * (amount + 1)
    dp[0] = 0
    for coin in coins:
        for a in range(coin, amount + 1):
            dp[a] = min(dp[a], dp[a - coin] + 1)
    return dp[amount] if dp[amount] != float('inf') else -1

def coin_change_ways(coins, amount):
    """凑成 amount 的方法数"""
    dp = [0] * (amount + 1)
    dp[0] = 1
    for coin in coins:
        for a in range(coin, amount + 1):
            dp[a] += dp[a - coin]
    return dp[amount]
```

---

## 七、区间 DP

```python
def interval_dp_template(n, cost_func):
    """区间 DP 模板"""
    dp = [[0] * n for _ in range(n)]
    for length in range(2, n + 1):      # 区间长度
        for i in range(n - length + 1):  # 起点
            j = i + length - 1           # 终点
            dp[i][j] = float('inf')
            for k in range(i, j):        # 分割点
                dp[i][j] = min(dp[i][j],
                               dp[i][k] + dp[k + 1][j] + cost_func(i, k, j))
    return dp[0][n - 1]

# 示例：戳气球 (LeetCode 312)
def max_coins(nums):
    nums = [1] + nums + [1]
    n = len(nums)
    dp = [[0] * n for _ in range(n)]
    for length in range(2, n):
        for i in range(n - length):
            j = i + length
            for k in range(i + 1, j):
                dp[i][j] = max(dp[i][j],
                               dp[i][k] + dp[k][j] + nums[i] * nums[k] * nums[j])
    return dp[0][n - 1]
```

---

## 八、树形 DP

```python
# 树形 DP 模板（后序遍历）
def tree_dp(root):
    def dfs(node):
        if not node:
            return (0, 0)  # (选, 不选)

        left = dfs(node.left)
        right = dfs(node.right)

        # 选当前节点
        rob = node.val + left[1] + right[1]
        # 不选当前节点
        not_rob = max(left) + max(right)

        return (rob, not_rob)

    return max(dfs(root))

# 树的直径 — 最长路径
def tree_diameter(root):
    diameter = 0
    def dfs(node):
        nonlocal diameter
        if not node:
            return 0
        left = dfs(node.left)
        right = dfs(node.right)
        diameter = max(diameter, left + right)
        return max(left, right) + 1
    dfs(root)
    return diameter
```

---

## 九、状压 DP（Bitmask DP）

```python
# 旅行商问题 (TSP)
def tsp(dist):
    n = len(dist)
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

---

## 十、DP 优化技巧

| 优化 | 适用场景 | 复杂度 |
|------|---------|--------|
| **滚动数组** | $dp[i]$ 只依赖 $dp[i-1]$ | 空间 $O(1)$ |
| **KMP 优化** | DP 中字符串匹配 | $O(n)$ |
| **分治 DP** | $dp[i] = \min_{j<i} dp[j] + C(j,i)$ 且决策点单调 | $O(n \log n)$ |
| **CHT（凸壳优化）** | 转移为线性函数求极值 | $O(n)$ 或 $O(n \log n)$ |
| **四边形不等式** | 满足四边形不等式的 DP | $O(n^2) → O(n \log n)$ |
| **单调队列优化** | $\min_{j \in [i-k, i-1]} dp[j] + f(i)$ | $O(n)$ |

```python
# 单调队列优化示例
def max_sliding_window(nums, k):
    """滑动窗口最大值"""
    from collections import deque
    q = deque()
    result = []
    for i, num in enumerate(nums):
        while q and nums[q[-1]] <= num:
            q.pop()
        q.append(i)
        if q[0] <= i - k:
            q.popleft()
        if i >= k - 1:
            result.append(nums[q[0]])
    return result
```

---

## 十一、DP 问题模式速查

| 模式 | 状态定义 | 经典问题 |
|------|---------|---------|
| 一维线性 | $dp[i]$ | 爬楼梯、打家劫舍 |
| 二维线性 | $dp[i][j]$ | LCS、编辑距离 |
| 背包 | $dp[w]$ | 0/1 背包、完全背包 |
| 区间 | $dp[i][j]$ | 矩阵链乘、戳气球 |
| 树形 | $dp[node]$ | 打家劫舍 III |
| 状压 | $dp[mask][i]$ | TSP、分组问题 |
| 数位 | $dp[pos][state]$ | 数字计数、数位统计 |
| 博弈 | $dp[i][j]$ | 预测赢家、石子游戏 |

## 相关条目

- [[05_ComputerScience/DataStructuresAndAlgorithms/Algorithms/BasicAlgorithms/BasicAlgorithms|BasicAlgorithms]]
- [[05_ComputerScience/DataStructuresAndAlgorithms/Algorithms/GraphAlgorithms/GraphAlgorithms|GraphAlgorithms]]
- [[05_ComputerScience/DataStructuresAndAlgorithms/Algorithms/GreedyAlgorithms/GreedyAlgorithms|GreedyAlgorithms]]

## 参考资源

- Bellman, R. (1957). Dynamic Programming. Princeton University Press.
- Cormen, T. H. et al. (2022). Introduction to Algorithms. 4th Edition. MIT Press.
- Dasgupta, S., Papadimitriou, C. H., & Vazirani, U. (2006). Algorithms. McGraw-Hill.
- LeetCode DP Problems. https://leetcode.com/tag/dynamic-programming/


