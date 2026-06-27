---
aliases: [Heap]
tags: ['DataStructuresAndAlgorithms', 'DataStructures', 'Heap']
created: 2026-05-16
updated: 2026-05-13
---

# 堆详解

## 基本概念

堆（Heap）是一种**完全二叉树**，满足堆性质：
- **最大堆（大根堆）**：每个节点的值 ≥ 其子节点的值，根为最大值
- **最小堆（小根堆）**：每个节点的值 ≤ 其子节点的值，根为最小值

### 完全二叉树的数组表示

```
        3
       / \
      5   8        → 数组： [3, 5, 8, 7, 6]
     / \
    7   6

index:  0  1  2  3  4
        [3, 5, 8, 7, 6]

节点 i 的：
- 左子节点: 2*i + 1
- 右子节点: 2*i + 2
- 父节点:   (i-1) // 2
```

## 核心操作及时间复杂度

| 操作 | 描述 | 时间复杂度（二叉堆） | 时间复杂度（斐波那契堆） |
|-----|------|--------------------|----------------------|
| push(heap, x) | 插入元素 | O(log n) | O(1) |
| pop(heap) | 弹出堆顶 | O(log n) | O(log n) |
| heapify(arr) | 数组建堆 | O(n) | — |
| peek() | 查看堆顶 | O(1) | O(1) |
| decrease_key | 减小键值 | O(log n) | O(1) 摊还 |
| merge | 合并两个堆 | O(n) | O(1) |

### 建堆复杂度证明

建堆 $O(n)$ 的证明：从最后一个非叶节点开始下沉，每个节点下沉代价与其高度成正比：

$$ T(n) = \sum_{h=0}^{\lfloor \log_2 n \rfloor} \left\lceil \frac{n}{2^{h+1}} \right\rceil \cdot O(h) = O(n) $$

## 最小堆实现

```python
class MinHeap:
    def __init__(self):
        self.data = []
    
    def push(self, val):
        """插入元素"""
        self.data.append(val)
        self._sift_up(len(self.data) - 1)
    
    def pop(self):
        """弹出最小值"""
        if not self.data:
            raise IndexError("pop from empty heap")
        if len(self.data) == 1:
            return self.data.pop()
        
        min_val = self.data[0]
        self.data[0] = self.data.pop()
        self._sift_down(0)
        return min_val
    
    def peek(self):
        if not self.data:
            raise IndexError("peek from empty heap")
        return self.data[0]
    
    def size(self):
        return len(self.data)
    
    def _sift_up(self, i):
        """上浮"""
        parent = (i - 1) // 2
        while i > 0 and self.data[i] < self.data[parent]:
            self.data[i], self.data[parent] = self.data[parent], self.data[i]
            i = parent
            parent = (i - 1) // 2
    
    def _sift_down(self, i):
        """下沉"""
        size = len(self.data)
        while True:
            smallest = i
            left = 2 * i + 1
            right = 2 * i + 2
            
            if left < size and self.data[left] < self.data[smallest]:
                smallest = left
            if right < size and self.data[right] < self.data[smallest]:
                smallest = right
            
            if smallest == i:
                break
            
            self.data[i], self.data[smallest] = self.data[smallest], self.data[i]
            i = smallest
    
    @staticmethod
    def heapify(arr):
        """数组建堆 O(n)"""
        h = MinHeap()
        h.data = arr[:]
        # 从最后一个非叶节点开始下沉
        for i in range(len(arr) // 2 - 1, -1, -1):
            h._sift_down(i)
        return h
```

## 最大堆实现

```python
class MaxHeap:
    def __init__(self):
        self.data = []
    
    def push(self, val):
        self.data.append(val)
        self._sift_up(len(self.data) - 1)
    
    def pop(self):
        if not self.data:
            raise IndexError("pop from empty heap")
        if len(self.data) == 1:
            return self.data.pop()
        
        max_val = self.data[0]
        self.data[0] = self.data.pop()
        self._sift_down(0)
        return max_val
    
    def _sift_up(self, i):
        parent = (i - 1) // 2
        while i > 0 and self.data[i] > self.data[parent]:
            self.data[i], self.data[parent] = self.data[parent], self.data[i]
            i = parent
            parent = (i - 1) // 2
    
    def _sift_down(self, i):
        size = len(self.data)
        while True:
            largest = i
            left = 2 * i + 1
            right = 2 * i + 2
            
            if left < size and self.data[left] > self.data[largest]:
                largest = left
            if right < size and self.data[right] > self.data[largest]:
                largest = right
            
            if largest == i:
                break
            
            self.data[i], self.data[largest] = self.data[largest], self.data[i]
            i = largest
```

## Python heapq 模块

Python 内置的 `heapq` 实现的是**最小堆**。

```python
import heapq

heap = []
heapq.heappush(heap, 5)   # 插入
heapq.heappush(heap, 2)
heapq.heappush(heap, 8)
print(heap[0])             # 查看堆顶: 2

val = heapq.heappop(heap)  # 弹出: 2
print(val)

# 数组建堆 O(n)
arr = [3, 1, 4, 1, 5, 9]
heapq.heapify(arr)

# 弹出并插入新元素
val = heapq.heapreplace(heap, 10)  # pop then push

# 插入后弹出
val = heapq.heappushpop(heap, 0)

# nlargest / nsmallest
largest = heapq.nlargest(3, [1, 3, 5, 2, 4])  # [5, 4, 3]
smallest = heapq.nsmallest(3, [1, 3, 5, 2, 4])  # [1, 2, 3]
```

### 实现最大堆

```python
# 方法1：存负数
import heapq
max_heap = []
heapq.heappush(max_heap, -5)
heapq.heappush(max_heap, -2)
max_val = -heapq.heappop(max_heap)  # 5

# 方法2：包装类
class MaxHeapObj:
    def __init__(self, val):
        self.val = val
    def __lt__(self, other):
        return self.val > other.val  # 反转比较

max_heap = []
heapq.heappush(max_heap, MaxHeapObj(5))
```

## 堆排序 (Heap Sort)

```python
def heap_sort(arr):
    """堆排序 O(n log n)"""
    n = len(arr)
    
    # 建堆 O(n)
    for i in range(n // 2 - 1, -1, -1):
        _sift_down(arr, n, i)
    
    # 排序 O(n log n)
    for i in range(n - 1, 0, -1):
        arr[0], arr[i] = arr[i], arr[0]  # 将堆顶移到末尾
        _sift_down(arr, i, 0)            # 调整堆
    
    return arr

def _sift_down(arr, n, i):
    """下沉（用于最大堆）"""
    largest = i
    left = 2 * i + 1
    right = 2 * i + 2
    
    if left < n and arr[left] > arr[largest]:
        largest = left
    if right < n and arr[right] > arr[largest]:
        largest = right
    
    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]
        _sift_down(arr, n, largest)
```

- **时间复杂度**: O(n log n)
- **空间复杂度**: O(1) 原地排序
- **稳定性**: 不稳定

## 应用场景

### 1. Top K 问题

```python
def find_kth_largest(nums, k):
    """数组中第 K 大的元素（最小堆）"""
    heap = nums[:k]
    heapq.heapify(heap)  # 大小为 k 的最小堆
    
    for num in nums[k:]:
        if num > heap[0]:
            heapq.heappop(heap)
            heapq.heappush(heap, num)
    
    return heap[0]

def top_k_frequent(nums, k):
    """出现频率最高的 K 个元素"""
    from collections import Counter
    counter = Counter(nums)
    
    # 最小堆，按频率排序
    heap = []
    for num, freq in counter.items():
        heapq.heappush(heap, (freq, num))
        if len(heap) > k:
            heapq.heappop(heap)
    
    return [num for _, num in heap]
```

### 2. 数据流中的中位数 (LeetCode 295)

```python
class MedianFinder:
    """用两个堆维护数据流中位数"""
    def __init__(self):
        self.small = []  # 最大堆（存负数）
        self.large = []  # 最小堆
    
    def add_num(self, num):
        if len(self.small) == len(self.large):
            # 先放入 small，再平衡到 large
            heapq.heappush(self.small, -num)
            heapq.heappush(self.large, -heapq.heappop(self.small))
        else:
            heapq.heappush(self.large, num)
            heapq.heappush(self.small, -heapq.heappop(self.large))
    
    def find_median(self):
        if len(self.small) == len(self.large):
            return (-self.small[0] + self.large[0]) / 2
        return self.large[0]
```

- **时间复杂度**: add_num O(log n), find_median O(1)
- **空间复杂度**: O(n)

### 3. Dijkstra 最短路径

```python
def dijkstra(graph, start):
    """Dijkstra 最短路径算法（堆优化）"""
    n = len(graph)
    dist = [float('inf')] * n
    dist[start] = 0
    pq = [(0, start)]  # (距离, 节点)
    
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

- **时间复杂度**: O((V+E) log V)
- **空间复杂度**: O(V)

### 4. 合并 K 个有序数组

```python
def merge_k_sorted(arrays):
    """合并 K 个有序数组"""
    heap = []
    result = []
    
    for i, arr in enumerate(arrays):
        if arr:
            heapq.heappush(heap, (arr[0], i, 0))
    
    while heap:
        val, arr_idx, elem_idx = heapq.heappop(heap)
        result.append(val)
        
        if elem_idx + 1 < len(arrays[arr_idx]):
            next_val = arrays[arr_idx][elem_idx + 1]
            heapq.heappush(heap, (next_val, arr_idx, elem_idx + 1))
    
    return result
```

### 5. 任务调度器 (LeetCode 621)

```python
def least_interval(tasks, n):
    """CPU 任务调度最短时间"""
    from collections import Counter
    
    freq = list(Counter(tasks).values())
    max_freq = max(freq)
    max_count = freq.count(max_freq)
    
    # 公式：max(len(tasks), (max_freq - 1) * (n + 1) + max_count)
    return max(len(tasks), (max_freq - 1) * (n + 1) + max_count)
```

## 练习

| 题目 | 难度 | 核心技巧 |
|------|------|---------|
| LeetCode 215. 第 K 大元素 | 🟡 中等 | 堆/快速选择 |
| LeetCode 347. 前 K 高频元素 | 🟡 中等 | 最小堆 |
| LeetCode 295. 数据流中位数 | 🔴 困难 | 双堆 |
| LeetCode 23. 合并 K 个链表 | 🔴 困难 | 堆 |
| LeetCode 378. 有序矩阵第 K 小 | 🟡 中等 | 堆/二分 |
| LeetCode 703. 数据流第 K 大 | 🟢 简单 | 最小堆 |
| LeetCode 1046. 最后一块石头重量 | 🟢 简单 | 最大堆 |
| LeetCode 239. 滑动窗口最大值 | 🔴 困难 | 堆/单调队列 |
| LeetCode 973. 最接近原点的 K 个点 | 🟡 中等 | 最大堆 |
| LeetCode 692. 前 K 高频单词 | 🟡 中等 | 堆+排序 |

## 相关条目

- [[Queue]]
- [[Tree]]
- [[Sorting]]
- [[SegmentTree]]
- [[BinarySearch]]
