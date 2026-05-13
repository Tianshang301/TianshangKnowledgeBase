# 区间与状态压缩DP

## 一、动态规划基础回顾

动态规划(DP)通过将原问题分解为重叠子问题，利用最优子结构性质避免重复计算。DP问题满足两个关键性质：**最优子结构**(问题的最优解包含子问题的最优解)和**重叠子问题**(不同路径求解相同子问题)。DP的求解范式包括状态定义、状态转移方程和初始条件与边界处理。

## 二、区间DP

### 2.1 区间DP的定义

区间DP处理的问题涉及对序列的连续区间进行操作，状态通常定义为 $dp[l][r]$，表示处理子数组 $A[l..r]$ 的最优解。区间DP的转移通常枚举区间内的分割点 $k$：

$$
dp[l][r] = \min_{k \in [l, r]} (dp[l][k] + dp[k+1][r] + \text{cost}(l, k, r))
$$

### 2.2 石子合并问题

经典的区间DP问题：合并堆石子，每次合并相邻两堆，代价为两堆石子数之和，求最小总代价。

```python
def stone_merge(stones):
    n = len(stones)
    prefix = [0] * (n + 1)
    for i in range(n):
        prefix[i+1] = prefix[i] + stones[i]

    dp = [[0] * n for _ in range(n)]
    for length in range(2, n + 1):
        for l in range(n - length + 1):
            r = l + length - 1
            dp[l][r] = float('inf')
            for k in range(l, r):
                cost = dp[l][k] + dp[k+1][r] + prefix[r+1] - prefix[l]
                dp[l][r] = min(dp[l][r], cost)

    return dp[0][n-1]
```

### 2.3 四边形不等式优化

当cost函数满足**四边形不等式**和**单调性**时，DP的枚举范围可以缩小：

$$
\text{opt}[l][r-1] \leq \text{opt}[l][r] \leq \text{opt}[l+1][r]
$$

其中 $\text{opt}[l][r]$ 是使 $dp[l][r]$ 取最小值的分割点。此优化将区间DP的时间复杂度从 $O(n^3)$ 降低到 $O(n^2)$。

### 2.4 回文相关DP

最长回文子序列：

$$
dp[i][j] = \begin{cases}
dp[i+1][j-1] + 2 & s[i] = s[j] \\
\max(dp[i+1][j], dp[i][j-1]) & s[i] \neq s[j]
\end{cases}
$$

最少插入次数使字符串成为回文串：
$$
dp[i][j] = \begin{cases}
dp[i+1][j-1] & s[i] = s[j] \\
1 + \min(dp[i+1][j], dp[i][j-1]) & s[i] \neq s[j]
\end{cases}
$$

## 三、状态压缩DP

### 3.1 位运算基础

状态压缩DP使用整数的二进制位表示集合状态。设共有 $n$ 个元素，一个子集可表示为位掩码 $mask = 0b1101$，表示元素集合 $\{0, 2, 3\}$。

常用位运算技巧：

```python
mask | (1 << i)       # 添加元素i
mask & ~(1 << i)      # 移除元素i
mask & (1 << i)       # 检查元素i是否存在
mask & -mask          # 获取最低位的1
mask & (mask - 1)     # 移除最低位的1
```

### 3.2 旅行商问题(TSP)

TSP是状态压缩DP的经典问题：从起点出发，经过所有城市恰好一次后回到起点，求最短路径：

```python
def tsp(dist):
    n = len(dist)
    dp = [[float('inf')] * n for _ in range(1 << n)]
    dp[1][0] = 0  # 从城市0出发

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

    full_mask = (1 << n) - 1
    ans = float('inf')
    for u in range(1, n):
        ans = min(ans, dp[full_mask][u] + dist[u][0])
    return ans
```

复杂度 $O(2^n \cdot n^2)$，状态数 $2^n \cdot n$。

### 3.3 任务分配与匹配

将n个任务分配给n个人，每个人只能做一个任务，求最大价值：

```python
def assignment(profit, n):
    dp = [-float('inf')] * (1 << n)
    dp[0] = 0
    for mask in range(1 << n):
        i = bin(mask).count('1')  # 当前处理第i个人
        for j in range(n):
            if not (mask & (1 << j)):
                dp[mask | (1 << j)] = max(
                    dp[mask | (1 << j)],
                    dp[mask] + profit[i][j]
                )
    return dp[(1 << n) - 1]
```

### 3.4 子集DP与子集枚举

子集枚举的复杂度优化：枚举所有掩码的每个子集，可通过对子掩码进行递减操作实现 $O(3^n)$ 而非 $O(4^n)$：

```python
sub = mask
while sub:
    # 处理子集sub
    sub = (sub - 1) & mask
```

## 四、经典问题对比

| 问题 | DP类型 | 状态维度 | 时间复杂度 | 空间复杂度 |
|------|--------|----------|-----------|-----------|
| 石子合并 | 区间DP | $O(n^2)$ | $O(n^3)/O(n^2)$ | $O(n^2)$ |
| 回文子序列 | 区间DP | $O(n^2)$ | $O(n^2)$ | $O(n^2)$ |
| TSP | 状态压缩DP | $O(2^n \cdot n)$ | $O(2^n \cdot n^2)$ | $O(2^n \cdot n)$ |
| 任务分配 | 状态压缩DP | $O(2^n)$ | $O(n \cdot 2^n)$ | $O(2^n)$ |
| 独立集计数 | 状态压缩DP | $O(2^n)$ | $O(2^n)$ | $O(2^n)$ |

## 五、高级技巧

### 5.1 轮廓线DP

轮廓线DP(也称插头DP)处理网格上的连通性问题，状态记录当前扫描线的状态。适用于哈密顿路径、骨牌覆盖等问题。

### 5.2 子集卷积

子集卷积计算 $f[U] = \sum_{T \subseteq U} g[T] \cdot h[U \setminus T]$，通过快速泽塔变换在 $O(n \cdot 2^n)$ 内完成。

### 5.3 动态规划的状态压缩优化

对于某些DP问题，当前状态仅依赖于前几行/前几个状态，可通过滚动数组压缩空间。状态压缩DP还可配合Meet-in-the-Middle将问题拆分为两个规模减半的子问题。

## 六、状态压缩DP的n取值参考

| n | 状态数 $2^n$ | 状态数 $2^n \cdot n$ | 可行性 |
|---|-------------|---------------------|--------|
| 10 | 1,024 | 10,240 | 瞬间 |
| 15 | 32,768 | 491,520 | 瞬间 |
| 20 | 1,048,576 | 20,971,520 | 可行 |
| 24 | 16,777,216 | 402,653,184 | 较大内存 |
| 30 | 1,073,741,824 | 32G | 不可行 |

在实践中，n超过20-24时通常需要搜索优化或启发式方法。

## 相关条目

- [[DynamicProgramming]]
- [[DP]]
- [[贪心算法证明与技巧]]
- [[Backtracking]]
- [[BasicAlgorithms]]

## 参考资源

1. Cormen, T. H., et al. "Introduction to Algorithms." 4th ed., MIT Press, 2022.
2. Kleinberg, J., Tardos, E. "Algorithm Design." Addison-Wesley, 2005.
3. Tardos, E. "Approximation Schemes for Scheduling and Related Problems." FOCS, 1997.
4. Held, M., Karp, R. M. "A Dynamic Programming Approach to Sequencing Problems." JSIAM, 1962.
5. Yao, F. F. "Efficient Dynamic Programming Using Quadrangle Inequalities." SODA, 1980.
6. Dasgupta, S., et al. "Algorithms." McGraw-Hill, 2006.
7. Skiena, S. S. "The Algorithm Design Manual." 3rd ed., Springer, 2020.
