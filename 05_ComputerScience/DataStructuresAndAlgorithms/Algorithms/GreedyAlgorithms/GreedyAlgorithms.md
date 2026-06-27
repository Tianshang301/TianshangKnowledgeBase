---
aliases: [GreedyAlgorithms]
tags: ['DataStructuresAndAlgorithms', 'Algorithms', 'GreedyAlgorithms', 'GreedyAlgorithms']
created: 2026-05-16
updated: 2026-05-13
---

# Greedy Algorithms - 贪心算法

## 一、贪心算法原理

贪心算法在每一步选择中都做出**当前最优**的决定，期望最终得到全局最优解。

### 贪心 vs 动态规划

| 特性 | 贪心 | 动态规划 |
|------|------|---------|
| 决策方式 | 每步选最优，不回退 | 考虑所有可能，记录最优 |
| 子问题关系 | 单一方向递进 | 重叠子问题 |
| 正确性证明 | 需要贪心选择性质 | 基于最优子结构 |
| 适用范围 | 窄（需满足特定性质） | 广 |
| 效率 | 通常更快 | 通常更慢 |

### 贪心算法正确的条件

1. **贪心选择性质**：全局最优解可以通过局部最优选择得到
2. **最优子结构**：子问题的最优解能组成原问题的最优解

### 证明方法

| 方法 | 说明 | 示例 |
|------|------|------|
| **交换论证** | 假设最优解与贪心解不同，可以通过交换操作将最优解转化为贪心解而不变差 | 活动选择 |
| **贪心领先** | 证明贪心选择的每一步都不比最优解差 | 跳跃游戏 |

---

## 二、活动选择

**问题**：选择最多数量的互不重叠的活动。

**策略**：每次选择**结束时间最早**的活动。

```python
def activity_selection(start, finish):
    """选择最多互不重叠活动"""
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

**正确性证明（交换论证）**：设 $S$ 为最优解，$G$ 为贪心解。若 $S$ 第一个活动不是最早结束的，可替换为最早结束的活动，结果不会变差。依此类推。

| 指标 | 值 |
|------|----|
| 时间复杂度 | $O(n \log n)$（排序） |
| 空间复杂度 | $O(n)$ |
| 贪心策略 | 最早结束时间优先 |

---

## 三、哈夫曼编码

**问题**：为字符集合构造最优前缀码，使编码总长度最短。

$$ B(T) = \sum_{c \in C} f(c) \cdot d_T(c) $$

其中 $f(c)$ 为字符 $c$ 的频率，$d_T(c)$ 为 $c$ 在树 $T$ 中的深度。

**信息熵**：最优前缀码的理论下界

$$ H = -\sum_{i=1}^{n} p_i \log_2 p_i $$

其中 $p_i = f(c_i) / \sum f(c)$ 为字符 $c_i$ 出现的概率，香农熵 $H$ 给出了平均编码位数的最小可能值。

**策略**：每次合并频率最小的两个节点。

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
    """构建哈夫曼树并生成编码"""
    heap = [HuffmanNode(c, f) for c, f in zip(chars, freqs)]
    heapq.heapify(heap)

    while len(heap) > 1:
        left = heapq.heappop(heap)
        right = heapq.heappop(heap)
        merged = HuffmanNode(None, left.freq + right.freq)
        merged.left = left
        merged.right = right
        heapq.heappush(heap, merged)

    codes = {}
    _build_codes(heap[0], "", codes)
    return codes

def _build_codes(node, code, codes):
    if node.char:
        codes[node.char] = code
        return
    _build_codes(node.left, code + "0", codes)
    _build_codes(node.right, code + "1", codes)
```

```text
示例：
字符:  A  B  C  D  E
频率:  45  13  12  16  9

哈夫曼树构建过程：
    Step 1: 合并 E(9) + C(12) = 21
    Step 2: 合并 B(13) + D(16) = 29
    Step 3: 合并 21 + 29 = 50
    Step 4: 合并 A(45) + 50 = 95

编码结果：
    A: 0        (1位)
    B: 111      (3位)
    C: 110      (3位)
    D: 101      (3位)
    E: 100      (3位)

平均编码长度: 45×1 + 13×3 + 12×3 + 16×3 + 9×3  /  95 = 2.13
```

| 指标 | 值 |
|------|----|
| 时间复杂度 | $O(n \log n)$ |
| 空间复杂度 | $O(n)$ |
| 正确性 | 前缀码性质 + 贪心选择保持最优 |

---

## 四、分数背包（Fractional Knapsack）

**问题**：物品可分割，在容量限制内最大化总价值。

**策略**：按**单位重量价值**从高到低选取。

$$ \text{最大化 } \sum_{i=1}^{n} v_i x_i \quad \text{s.t. } \sum_{i=1}^{n} w_i x_i \leq C,\; 0 \leq x_i \leq 1 $$

其中 $x_i$ 为物品 $i$ 被选取的比例。

```python
def fractional_knapsack(weights, values, capacity):
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

| 特性 | 分数背包 | 0/1 背包 |
|------|---------|----------|
| 物品可分割 | ✅ | ❌ |
| 贪心最优 | ✅ | ❌（需 DP） |
| 时间复杂度 | $O(n \log n)$ | $O(nC)$ |

---

## 五、区间调度

**问题**：选择最多的不重叠区间。

```python
def interval_scheduling(intervals):
    """intervals: [(start, end), ...]"""
    intervals.sort(key=lambda x: x[1])  # 按结束时间排序
    count = 0
    end = float('-inf')

    for s, e in intervals:
        if s >= end:
            count += 1
            end = e

    return count


# 区间分组：最少需要多少组使所有区间不重叠
def min_interval_groups(intervals):
    intervals.sort(key=lambda x: x[0])
    heap = []  # 存储每组的结束时间
    for s, e in intervals:
        if heap and heap[0] <= s:
            heapq.heappop(heap)
        heapq.heappush(heap, e)
    return len(heap)
```

---

## 六、任务调度与截止时间

### 作业排序（Job Sequencing with Deadlines）

**问题**：每个作业有截止时间和利润，在同一时间只能执行一个作业，最大化总利润。

**策略**：按利润降序排序，将每个作业安排在最靠近截止时间的空闲时间槽。

```python
def job_sequencing(jobs, max_deadline):
    """jobs: [(deadline, profit), ...]"""
    jobs.sort(key=lambda x: x[1], reverse=True)
    slots = [-1] * (max_deadline + 1)
    total_profit = 0

    for deadline, profit in jobs:
        for t in range(min(deadline, max_deadline), 0, -1):
            if slots[t] == -1:
                slots[t] = profit
                total_profit += profit
                break

    return total_profit
```

---

## 七、Dijkstra 算法

**问题**：非负权图单源最短路径。

**策略**：每次从尚未确定最短距离的顶点中选择距离最小的顶点。

```python
import heapq

def dijkstra(graph, start):
    dist = {v: float('inf') for v in graph}
    dist[start] = 0
    pq = [(0, start)]

    while pq:
        d, u = heapq.heappop(pq)
        if d > dist[u]:
            continue
        for v, w in graph[u]:
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                heapq.heappush(pq, (dist[v], v))

    return dist
```

**正确性**：假设当前选择的 $u$ 的 $dist[u]$ 是最小的。因为所有边权非负，不可能有另一条路径以更小的距离到达 $u$。

---

## 八、贪心不起作用的场景

### 0/1 背包的反例

```text
物品:   物品1    物品2    物品3
重量:    10       20       30
价值:    60      100      120
单位价值: 6        5        4
容量:    50

贪心按单位价值选：物品1(60) + 物品2(100) = 160
最优解：物品2(100) + 物品3(120) = 220 ❌ 贪心失败
```

### 零钱兑换的反例

```text
硬币面额: [1, 3, 4]
目标金额: 6

贪心：4 + 1 + 1 = 3枚
最优：3 + 3 = 2枚 ← 贪心失败

硬币面额: [1, 5, 10, 25]
目标金额: 30
贪心：25 + 5 = 2枚 ← 成功（规范硬币系统）
```

### 贪心适用范围总结

| 问题 | 贪心最优？ | 正确策略 |
|------|-----------|---------|
| 活动选择 | ✅ | 最早结束 |
| 哈夫曼编码 | ✅ | 最小频率合并 |
| 分数背包 | ✅ | 最高单位价值 |
| Dijkstra | ✅ | 最小距离优先 |
| Prim/Kruskal (MST) | ✅ | 最小边/点扩展 |
| 区间调度 | ✅ | 最早结束 |
| 0/1 背包 | ❌ | DP |
| 普通零钱 | ❌ | DP |
| 旅行商 (TSP) | ❌ | 近似/DP |
| 图着色 | ❌ | 回溯/贪心近似 |

---

## 九、拟阵理论（Matroid Theory）

拟阵为贪心算法提供了理论基础：

$$ \text{Matroid } M = (S, I) $$

其中 $S$ 是有限集，$I$ 是独立集族，满足：
1. **空集独立**：$\emptyset \in I$
2. **继承性**：若 $A \in I$ 且 $B \subseteq A$，则 $B \in I$
3. **交换性**：若 $A, B \in I$ 且 $|A| < |B|$，则 $\exists x \in B \setminus A$ 使 $A \cup \{x\} \in I$

**定理**：在拟阵上，贪心算法总能找到最大权值独立集。

$$ \text{贪心选择性质：} \max_{A \in I} \sum_{x \in A} w(x) \text{ 可通过每步选择最大权值可行元素得到} $$

```text
图拟阵示例：
    S = 图的边集
    I = 无环的边集（森林）
    贪心 = Kruskal 算法
```

---

## 十、贪心算法速查表

| 问题 | 贪心策略 | 证明方法 | 复杂度 |
|------|---------|---------|--------|
| 活动选择 | 最早结束 | 交换论证 | $O(n \log n)$ |
| 哈夫曼编码 | 最小频率合并 | 贪心领先 | $O(n \log n)$ |
| 分数背包 | 最高单位价值 | 交换论证 | $O(n \log n)$ |
| 区间调度 | 最早结束 | 交换论证 | $O(n \log n)$ |
| 作业排序 | 利润降序+最晚可用 | 交换论证 | $O(n \cdot m)$ |
| Dijkstra | 最小距离优先 | 贪心领先 | $O((V+E)\log V)$ |
| Prim MST | 最小权边扩展 | 割性质 | $O((V+E)\log V)$ |
| Kruskal MST | 最小权边（无环） | 割性质 | $O(E \log E)$ |
| 跳跃游戏 II | 最远可达 | 贪心领先 | $O(n)$ |
| 分发饼干 | 最小饼干给最小胃口 | 交换论证 | $O(n \log n)$ |

## 相关条目

- [[贪心算法证明与技巧]]
- [[DynamicProgramming]]
- [[BasicAlgorithms]]
- [[MST]]
- [[GraphAlgorithms]]

## 参考资源

- Cormen, T. H. et al. (2022). Introduction to Algorithms. 4th Edition. MIT Press.
- Kleinberg, J. & Tardos, É. (2005). Algorithm Design. Addison-Wesley.
- Edmonds, J. (1971). Matroids and the Greedy Algorithm. Mathematical Programming.
- Oxley, J. (2011). Matroid Theory. 2nd Edition. Oxford University Press.
