# 贪心算法详解

## 基本概念

贪心算法（Greedy Algorithm）在每一步都做出**当前最优**的选择，期望最终得到全局最优解。

### 贪心 vs DP

| 特性 | 贪心 | 动态规划 |
|-----|------|---------|
| 决策方式 | 每步选最优 | 考虑所有可能 |
| 子问题 | 一个方向 | 重叠子问题 |
| 正确性 | 需证明贪心选择性 | 基于最优子结构 |
| 适用范围 | 窄（特定问题） | 广 |
| 效率 | 通常更快 | 通常更慢 |

## 贪心算法的证明

证明贪心正确性通常需要：

1. **贪心选择性质**：全局最优解可以通过局部最优选择得到
2. **最优子结构**：子问题的最优解可以组成原问题的最优解

## 经典问题

### 1. 活动选择 (Activity Selection)

```python
def activity_selection(start, finish):
    """选择最多数量的互不重叠活动"""
    n = len(start)
    activities = sorted(zip(start, finish), key=lambda x: x[1])
    
    selected = [activities[0]]
    last_finish = activities[0][1]
    
    for i in range(1, n):
        if activities[i][0] >= last_finish:
            selected.append(activities[i])
            last_finish = activities[i][1]
    
    return selected
```

**策略**：每次选择**结束时间最早**的活动。
**时间复杂度**: O(n log n)
**正确性证明**：最早结束的活动为后续活动留出最多时间。

### 2. 零钱兑换 (LeetCode 322 — 有限制)

```python
def coin_change_greedy(coins, amount):
    """贪心策略（仅对规范硬币系统有效）"""
    coins.sort(reverse=True)
    count = 0
    
    for coin in coins:
        if amount == 0:
            break
        count += amount // coin
        amount %= coin
    
    return count if amount == 0 else -1
```

注意：普通硬币系统（如 [1, 3, 4] 凑 6）贪心会失败（4+1+1 vs 3+3）。
**规范硬币系统**（如 1, 5, 10, 25）贪心有效。

### 3. 哈夫曼编码 (Huffman Coding)

```python
import heapq

class HuffmanNode:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None
    
    def __lt__(self, other):
        return self.freq < other.freq

def huffman_encoding(chars, freqs):
    """构建哈夫曼树"""
    heap = [HuffmanNode(c, f) for c, f in zip(chars, freqs)]
    heapq.heapify(heap)
    
    while len(heap) > 1:
        left = heapq.heappop(heap)
        right = heapq.heappop(heap)
        merged = HuffmanNode(None, left.freq + right.freq)
        merged.left = left
        merged.right = right
        heapq.heappush(heap, merged)
    
    root = heap[0]
    codes = {}
    _build_codes(root, "", codes)
    return codes

def _build_codes(node, code, codes):
    if node.char:
        codes[node.char] = code
        return
    _build_codes(node.left, code + "0", codes)
    _build_codes(node.right, code + "1", codes)
```

**策略**：每次合并频率最小的两个节点。
**时间复杂度**: O(n log n)

### 4. 分数背包 (Fractional Knapsack)

```python
def fractional_knapsack(weights, values, capacity):
    """分数背包：物品可以分割"""
    items = [(v / w, w, v) for w, v in zip(weights, values)]
    items.sort(key=lambda x: x[0], reverse=True)
    
    total_value = 0
    for ratio, w, v in items:
        if capacity >= w:
            total_value += v
            capacity -= w
        else:
            total_value += ratio * capacity
            break
    
    return total_value
```

**策略**：按**单位重量价值**从高到低选取。
**时间复杂度**: O(n log n)
与 0/1 背包不同，分数背包贪心正确。

### 5. 区间调度 (Interval Scheduling)

```python
def interval_scheduling(intervals):
    """选择最多的不重叠区间"""
    intervals.sort(key=lambda x: x[1])  # 按结束时间排序
    n = len(intervals)
    count = 1
    end = intervals[0][1]
    
    for i in range(1, n):
        if intervals[i][0] >= end:
            count += 1
            end = intervals[i][1]
    
    return count
```

**策略**：按结束时间排序，选择不冲突且最早结束的。

### 6. 跳跃游戏 (LeetCode 55)

```python
def can_jump(nums):
    """判断是否能到达最后一格"""
    max_reach = 0
    for i, step in enumerate(nums):
        if i > max_reach:
            return False
        max_reach = max(max_reach, i + step)
        if max_reach >= len(nums) - 1:
            return True
    return True

def jump(nums):
    """跳到最后的最少跳跃次数 (LeetCode 45)"""
    n = len(nums)
    if n <= 1:
        return 0
    
    jumps = 0
    current_end = 0
    farthest = 0
    
    for i in range(n - 1):
        farthest = max(farthest, i + nums[i])
        if i == current_end:
            jumps += 1
            current_end = farthest
    
    return jumps
```

**策略**：维护当前能跳到的最远位置，每次到达边界时跳跃次数 +1。

### 7. 加油站 (LeetCode 134)

```python
def can_complete_circuit(gas, cost):
    """判断能否完成环路行驶"""
    total_gas = total_cost = 0
    start = 0
    curr_gas = 0
    
    for i in range(len(gas)):
        total_gas += gas[i]
        total_cost += cost[i]
        curr_gas += gas[i] - cost[i]
        
        if curr_gas < 0:
            start = i + 1
            curr_gas = 0
    
    return start if total_gas >= total_cost else -1
```

**策略**：如果从 i 到 j 无法到达，那么从 i 到 j 之间的任何起点都无法到达 j。

### 8. 分发饼干 (LeetCode 455)

```python
def find_content_children(g, s):
    """分发饼干满足最多孩子"""
    g.sort()  # 孩子胃口
    s.sort()  # 饼干尺寸
    
    child = cookie = 0
    while child < len(g) and cookie < len(s):
        if s[cookie] >= g[child]:
            child += 1
        cookie += 1
    
    return child
```

**策略**：将最小的饼干分给胃口最小的孩子。

### 9. 无重叠区间 (LeetCode 435)

```python
def erase_overlap_intervals(intervals):
    """移除最少的区间使剩余无重叠"""
    if not intervals:
        return 0
    
    intervals.sort(key=lambda x: x[1])
    end = intervals[0][1]
    keep = 1
    
    for i in range(1, len(intervals)):
        if intervals[i][0] >= end:
            keep += 1
            end = intervals[i][1]
    
    return len(intervals) - keep
```

### 10. 单调递增的数字 (LeetCode 738)

```python
def monotone_increasing_digits(n):
    """找到小于等于 n 的最大单调递增数字"""
    digits = list(str(n))
    i = 1
    while i < len(digits) and digits[i-1] <= digits[i]:
        i += 1
    
    if i < len(digits):
        while i > 0 and digits[i-1] > digits[i]:
            digits[i-1] = str(int(digits[i-1]) - 1)
            i -= 1
        for j in range(i + 1, len(digits)):
            digits[j] = '9'
    
    return int(''.join(digits))
```

## 贪心策略总结

| 问题 | 贪心策略 | 是否最优 |
|------|---------|---------|
| 活动选择 | 最早结束 | ✅ |
| 分数背包 | 最高单位价值 | ✅ |
| 哈夫曼编码 | 最小频率合并 | ✅ |
| 跳跃游戏 | 最远可达 | ✅ |
| 加油站 | 累积最低点 | ✅ |
| 分发饼干 | 最小饼干给最小胃口 | ✅ |
| 0/1 背包 | 最高单位价值 | ❌ (需 DP) |
| 找零 [1,3,4] | 最大面值优先 | ❌ |
| 图着色 | 贪心着色 | ❌ (不一定最优) |

## 练习

| 题目 | 难度 | 核心技巧 |
|------|------|---------|
| LeetCode 455. 分发饼干 | 🟢 简单 | 排序 |
| LeetCode 122. 买卖股票 II | 🟡 中等 | 贪心 |
| LeetCode 55. 跳跃游戏 | 🟡 中等 | 贪心 |
| LeetCode 45. 跳跃游戏 II | 🟡 中等 | 贪心 |
| LeetCode 134. 加油站 | 🟡 中等 | 贪心 |
| LeetCode 435. 无重叠区间 | 🟡 中等 | 区间调度 |
| LeetCode 452. 用箭爆气球 | 🟡 中等 | 区间调度 |
| LeetCode 621. 任务调度器 | 🟡 中等 | 贪心 |
| LeetCode 763. 划分字母区间 | 🟡 中等 | 贪心 |
| LeetCode 738. 单调递增数字 | 🟡 中等 | 贪心 |
| LeetCode 406. 根据身高重建队列 | 🟡 中等 | 贪心+排序 |
| LeetCode 861. 翻转矩阵后的得分 | 🟡 中等 | 逐位贪心 |

## 相关条目

- [[GreedyAlgorithms]]
- [[DP]]
- [[MST]]
- [[Backtracking]]
- [[Sorting]]
