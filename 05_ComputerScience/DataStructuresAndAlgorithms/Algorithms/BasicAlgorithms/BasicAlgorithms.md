---
aliases: [BasicAlgorithms]
tags: ['DataStructuresAndAlgorithms', 'Algorithms', 'BasicAlgorithms', 'BasicAlgorithms']
---

# Basic Algorithms - 基础算法

## 一、算法分析

### 渐进复杂度

$$ O(g(n)) = \{ f(n) \mid \exists c > 0, n_0 > 0, \forall n \geq n_0: 0 \leq f(n) \leq c \cdot g(n) \} $$

$$ \Omega(g(n)) = \{ f(n) \mid \exists c > 0, n_0 > 0, \forall n \geq n_0: 0 \leq c \cdot g(n) \leq f(n) \} $$

$$ \Theta(g(n)) = \{ f(n) \mid \exists c_1, c_2 > 0, n_0 > 0, \forall n \geq n_0: c_1 g(n) \leq f(n) \leq c_2 g(n) \} $$

| 符号 | 含义 | 类比 |
|------|------|------|
| $O$ | 上界（最坏情况） | `≤` |
| $\Omega$ | 下界（最好情况） | `≥` |
| $\Theta$ | 紧界（精确界） | `=` |
| $o$ | 非紧上界 | `<` |
| $\omega$ | 非紧下界 | `>` |

### 常见复杂度

| 复杂度 | 名称 | 示例 |
|--------|------|------|
| $O(1)$ | 常数时间 | 数组随机访问 |
| $O(\log n)$ | 对数时间 | 二分查找 |
| $O(n)$ | 线性时间 | 遍历数组 |
| $O(n \log n)$ | 线性对数时间 | 归并排序 |
| $O(n^2)$ | 平方时间 | 冒泡排序 |
| $O(2^n)$ | 指数时间 | 子集枚举 |
| $O(n!)$ | 阶乘时间 | 排列枚举 |

### 均摊分析（Amortized Analysis）

均摊分析针对一系列操作的总复杂度取平均值，而非单次操作的最坏情况。

```text
动态数组扩容：
    - 每次插入 O(1)（均摊）
    - 扩容时 O(n)，但扩容频率为 1/n → 均摊 O(1)

三种分析方法：
    - 聚合分析：总代价 / 操作次数
    - 记账法：每次操作预付额外代价
    - 势能法：定义势能函数
```

---

## 二、递归与递推关系

### 主定理（Master Theorem）

对于形如 $T(n) = aT(n/b) + f(n)$ 的递推式（$a \geq 1, b > 1$）：

$$ T(n) = \begin{cases} \Theta(n^{\log_b a}) & \text{if } f(n) = O(n^{\log_b a - \epsilon}) \\ \Theta(n^{\log_b a} \log n) & \text{if } f(n) = \Theta(n^{\log_b a}) \\ \Theta(f(n)) & \text{if } f(n) = \Omega(n^{\log_b a + \epsilon}) \text{ and } af(n/b) \leq cf(n) \end{cases} $$

```text
示例：
    T(n) = 2T(n/2) + O(n)      →  O(n log n)    （归并排序）
    T(n) = T(n/2) + O(1)       →  O(log n)      （二分查找）
    T(n) = 2T(n/2) + O(1)      →  O(n)          （树遍历）
    T(n) = 7T(n/2) + O(n²)     →  O(n^{log₂7})  （Strassen 矩阵乘法）
```

---

## 三、分治算法

### 归并排序

```python
def merge_sort(arr):
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    return merge(left, right)

def merge(left, right):
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result
```

- 时间复杂度：$O(n \log n)$（稳定）
- 空间复杂度：$O(n)$

### 快速排序

```python
def quick_sort(arr, low, high):
    if low < high:
        pivot = partition(arr, low, high)
        quick_sort(arr, low, pivot - 1)
        quick_sort(arr, pivot + 1, high)

def partition(arr, low, high):
    pivot = arr[high]  # 选择最后一个元素为 pivot
    i = low - 1
    for j in range(low, high):
        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1
```

- 时间复杂度：平均 $O(n \log n)$，最坏 $O(n^2)$
- 空间复杂度：$O(\log n)$（递归栈）
- 不稳定排序

### 二分查找

```python
def binary_search(arr, target):
    left, right = 0, len(arr) - 1
    while left <= right:
        mid = left + (right - left) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1
```

- 时间复杂度：$O(\log n)$
- 前提：数组已排序

---

## 四、暴力算法

```python
# 字符串暴力匹配
def brute_force(text, pattern):
    n, m = len(text), len(pattern)
    for i in range(n - m + 1):
        j = 0
        while j < m and text[i + j] == pattern[j]:
            j += 1
        if j == m:
            return i
    return -1  # O(nm)
```

| 算法 | 时间复杂度 | 特点 |
|------|-----------|------|
| 暴力字符串匹配 | $O(nm)$ | 实现简单，效率低 |
| 选择排序 | $O(n^2)$ | 每次找最小元素交换 |
| 冒泡排序 | $O(n^2)$ | 相邻元素比较交换 |

---

## 五、随机化算法

```python
import random

# QuickSelect — 第 k 小元素
def quick_select(arr, k):
    if len(arr) == 1:
        return arr[0]
    pivot = random.choice(arr)
    left = [x for x in arr if x < pivot]
    mid = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]

    if k <= len(left):
        return quick_select(left, k)
    elif k <= len(left) + len(mid):
        return pivot
    else:
        return quick_select(right, k - len(left) - len(mid))

# 随机化快速排序
def randomized_quicksort(arr):
    if len(arr) <= 1:
        return arr
    pivot = random.choice(arr)
    left = [x for x in arr if x < pivot]
    mid = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return randomized_quicksort(left) + mid + randomized_quicksort(right)
```

| 类型 | 特点 | 示例 |
|------|------|------|
| **Monte Carlo** | 可能出错，运行时间确定 | 素数检测（Miller-Rabin） |
| **Las Vegas** | 结果正确，运行时间随机 | 随机化快速排序 |

---

## 六、双指针技术

```python
# 两数之和 II（已排序数组）
def two_sum_sorted(numbers, target):
    left, right = 0, len(numbers) - 1
    while left < right:
        curr = numbers[left] + numbers[right]
        if curr == target:
            return [left + 1, right + 1]
        elif curr < target:
            left += 1
        else:
            right -= 1
    return [-1, -1]

# 三数之和
def three_sum(nums):
    nums.sort()
    res = []
    for i in range(len(nums) - 2):
        if i > 0 and nums[i] == nums[i - 1]:
            continue
        left, right = i + 1, len(nums) - 1
        while left < right:
            s = nums[i] + nums[left] + nums[right]
            if s == 0:
                res.append([nums[i], nums[left], nums[right]])
                while left < right and nums[left] == nums[left + 1]:
                    left += 1
                while left < right and nums[right] == nums[right - 1]:
                    right -= 1
                left += 1
                right -= 1
            elif s < 0:
                left += 1
            else:
                right -= 1
    return res
```

| 模式 | 复杂度 | 典型问题 |
|------|--------|---------|
| 对撞指针 | $O(n)$ | 两数之和、回文判断 |
| 同向指针 | $O(n)$ | 移除重复、链表环检测 |
| 快慢指针 | $O(n)$ | 链表中间节点、环入口 |

---

## 七、滑动窗口

```python
# 最小覆盖子串
def min_window(s, t):
    need = {}
    for c in t:
        need[c] = need.get(c, 0) + 1
    missing = len(t)
    left = 0
    res = (0, float('inf'))

    for right, c in enumerate(s):
        if c in need:
            need[c] -= 1
            if need[c] >= 0:
                missing -= 1

        while missing == 0:
            if right - left < res[1] - res[0]:
                res = (left, right)
            left_char = s[left]
            if left_char in need:
                need[left_char] += 1
                if need[left_char] > 0:
                    missing += 1
            left += 1

    return s[res[0]:res[1] + 1] if res[1] != float('inf') else ""
```

| 窗口类型 | 特征 |
|---------|------|
| 固定大小窗口 | 长度不变，每次右移一个单位 |
| 可变大小窗口 | 左右边界动态调整，满足条件收缩 |

---

## 八、前缀和与差分数组

```python
# 前缀和 — 区间和查询 O(1)
def prefix_sum(arr):
    n = len(arr)
    pref = [0] * (n + 1)
    for i in range(n):
        pref[i + 1] = pref[i] + arr[i]
    # 区间 [l, r] 和 = pref[r + 1] - pref[l]
    return pref

# 差分数组 — 区间更新 O(1)
def difference_array(arr):
    n = len(arr)
    diff = [0] * (n + 1)
    # 区间 [l, r] 加 val
    # diff[l] += val
    # diff[r + 1] -= val
    # 最终通过前缀和还原
    return diff
```

---

## 九、位运算

| 操作 | 运算符 | 示例 |
|------|--------|------|
| AND | `&` | `5 & 3 = 1` |
| OR | `|` | `5 | 3 = 7` |
| XOR | `^` | `5 ^ 3 = 6` |
| NOT | `~` | `~5 = -6` |
| 左移 | `<<` | `5 << 1 = 10` |
| 右移 | `>>` | `5 >> 1 = 2` |

```python
# 常用位运算技巧
x & (-x)      # 提取最低位的 1
x & (x - 1)   # 清除最低位的 1
x ^ x         # 0
x ^ 0         # x
(x >> i) & 1  # 获取第 i 位
x | (1 << i)  # 设置第 i 位为 1
x & ~(1 << i) # 清除第 i 位

# 应用：查找只出现一次的数字
def single_number(nums):
    result = 0
    for num in nums:
        result ^= num
    return result
```

---

## 十、排序基础

### 比较排序 vs 非比较排序

| 类型 | 算法 | 时间复杂度 | 空间 | 稳定 |
|------|------|-----------|------|------|
| 比较排序 | 冒泡排序 | $O(n^2)$ | $O(1)$ | ✅ |
| 比较排序 | 选择排序 | $O(n^2)$ | $O(1)$ | ❌ |
| 比较排序 | 插入排序 | $O(n^2)$ | $O(1)$ | ✅ |
| 比较排序 | 归并排序 | $O(n \log n)$ | $O(n)$ | ✅ |
| 比较排序 | 快速排序 | $O(n \log n)$ | $O(\log n)$ | ❌ |
| 比较排序 | 堆排序 | $O(n \log n)$ | $O(1)$ | ❌ |
| 非比较排序 | 计数排序 | $O(n + k)$ | $O(k)$ | ✅ |
| 非比较排序 | 基数排序 | $O(d \times (n + k))$ | $O(n + k)$ | ✅ |
| 非比较排序 | 桶排序 | $O(n + k)$ | $O(n)$ | ✅ |

### 排序算法详细对比

| 算法 | 最好情况 | 平均情况 | 最坏情况 | 空间 | 稳定 | 适用场景 |
|------|---------|---------|---------|------|------|---------|
| 冒泡排序 | $O(n)$ | $O(n^2)$ | $O(n^2)$ | $O(1)$ | ✅ | 教学演示，几乎有序数据 |
| 选择排序 | $O(n^2)$ | $O(n^2)$ | $O(n^2)$ | $O(1)$ | ❌ | 交换次数少的场景 |
| 插入排序 | $O(n)$ | $O(n^2)$ | $O(n^2)$ | $O(1)$ | ✅ | 小规模、基本有序数据 |
| 希尔排序 | $O(n \log n)$ | $O(n^{1.3})$ | $O(n^2)$ | $O(1)$ | ❌ | 中等规模数据 |
| 归并排序 | $O(n \log n)$ | $O(n \log n)$ | $O(n \log n)$ | $O(n)$ | ✅ | 外排序、需要稳定排序 |
| 快速排序 | $O(n \log n)$ | $O(n \log n)$ | $O(n^2)$ | $O(\log n)$ | ❌ | 通用最快、内存敏感 |
| 堆排序 | $O(n \log n)$ | $O(n \log n)$ | $O(n \log n)$ | $O(1)$ | ❌ | 内存受限、优先队列 |
| 计数排序 | $O(n + k)$ | $O(n + k)$ | $O(n + k)$ | $O(k)$ | ✅ | 整数、范围已知且小 |
| 基数排序 | $O(d(n+k))$ | $O(d(n+k))$ | $O(d(n+k))$ | $O(n+k)$ | ✅ | 整数、字符串、稳定 |
| 桶排序 | $O(n + k)$ | $O(n + k)$ | $O(n^2)$ | $O(n)$ | ✅ | 均匀分布浮点数 |

**排序下界**：基于比较的排序算法最坏情况时间复杂度下界为 $\Omega(n \log n)$。

排序算法核心选择标准：**数据规模、数据范围、是否稳定、空间限制**。

## 相关条目

- [[排序与搜索算法深入]]
- [[BinarySearch]]
- [[Sorting]]
- [[贪心算法证明与技巧]]
- [[DP]]

## 参考资源

- Cormen, T. H., Leiserson, C. E., Rivest, R. L., & Stein, C. (2022). Introduction to Algorithms. 4th Edition. MIT Press.
- Sedgewick, R. & Wayne, K. (2011). Algorithms. 4th Edition. Addison-Wesley.
- Kleinberg, J. & Tardos, É. (2005). Algorithm Design. Addison-Wesley.
- LeetCode. https://leetcode.com/problemset/
