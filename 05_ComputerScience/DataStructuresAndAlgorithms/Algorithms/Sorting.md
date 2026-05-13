# 排序算法大全

## 概述

排序是将一组数据按特定顺序排列的操作，是计算机科学中最基础的算法之一。

## 比较排序 (O(n²))

### 冒泡排序 (Bubble Sort)

```python
def bubble_sort(arr):
    n = len(arr)
    for i in range(n - 1):
        swapped = False
        for j in range(n - 1 - i):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
        if not swapped:  # 优化：已有序提前退出
            break
    return arr
```

| 指标 | 值 |
|-----|----|
| 时间复杂度 | O(n²) 平均/最差, O(n) 最好 |
| 空间复杂度 | O(1) |
| 稳定性 | 稳定 |

### 选择排序 (Selection Sort)

```python
def selection_sort(arr):
    n = len(arr)
    for i in range(n - 1):
        min_idx = i
        for j in range(i + 1, n):
            if arr[j] < arr[min_idx]:
                min_idx = j
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
    return arr
```

| 指标 | 值 |
|-----|----|
| 时间复杂度 | O(n²) 全部情况 |
| 空间复杂度 | O(1) |
| 稳定性 | 不稳定 |

### 插入排序 (Insertion Sort)

```python
def insertion_sort(arr):
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
    return arr
```

| 指标 | 值 |
|-----|----|
| 时间复杂度 | O(n²) 平均/最差, O(n) 最好 |
| 空间复杂度 | O(1) |
| 稳定性 | 稳定 |

### 希尔排序 (Shell Sort)

```python
def shell_sort(arr):
    n = len(arr)
    gap = n // 2
    while gap > 0:
        for i in range(gap, n):
            temp = arr[i]
            j = i
            while j >= gap and arr[j - gap] > temp:
                arr[j] = arr[j - gap]
                j -= gap
            arr[j] = temp
        gap //= 2
    return arr
```

| 指标 | 值 |
|-----|----|
| 时间复杂度 | O(n log² n) 平均, O(n²) 最差 |
| 空间复杂度 | O(1) |
| 稳定性 | 不稳定 |

## 高效排序 (O(n log n))

### 归并排序 (Merge Sort)

分治思想：将数组分成两半，分别排序后合并。

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

# 原地归并排序（优化空间）
def merge_sort_inplace(arr, left=0, right=None):
    if right is None:
        right = len(arr) - 1
    if left >= right:
        return
    
    mid = (left + right) // 2
    merge_sort_inplace(arr, left, mid)
    merge_sort_inplace(arr, mid + 1, right)
    _merge_inplace(arr, left, mid, right)

def _merge_inplace(arr, left, mid, right):
    left_part = arr[left:mid + 1]
    right_part = arr[mid + 1:right + 1]
    i = j = 0
    k = left
    while i < len(left_part) and j < len(right_part):
        if left_part[i] <= right_part[j]:
            arr[k] = left_part[i]
            i += 1
        else:
            arr[k] = right_part[j]
            j += 1
        k += 1
    arr[k:right + 1] = left_part[i:] or right_part[j:]
```

| 指标 | 值 |
|-----|----|
| 时间复杂度 | O(n log n) 全部情况 |
| 空间复杂度 | O(n) |
| 稳定性 | 稳定 |

### 快速排序 (Quick Sort)

分治思想：选择 pivot（基准），将数组分为小于和大于 pivot 的两部分，递归排序。

```python
def quick_sort(arr, left=0, right=None):
    if right is None:
        right = len(arr) - 1
    if left < right:
        pivot_idx = partition(arr, left, right)
        quick_sort(arr, left, pivot_idx - 1)
        quick_sort(arr, pivot_idx + 1, right)
    return arr

def partition(arr, left, right):
    """Lomuto 分区方案"""
    pivot = arr[right]  # 选最后一个元素为 pivot
    i = left - 1
    for j in range(left, right):
        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
    arr[i + 1], arr[right] = arr[right], arr[i + 1]
    return i + 1

# Hoare 分区方案（更高效）
def partition_hoare(arr, left, right):
    pivot = arr[(left + right) // 2]
    i, j = left - 1, right + 1
    while True:
        i += 1
        while arr[i] < pivot:
            i += 1
        j -= 1
        while arr[j] > pivot:
            j -= 1
        if i >= j:
            return j
        arr[i], arr[j] = arr[j], arr[i]

# 随机化快排（避免最差情况）
import random

def quick_sort_random(arr, left=0, right=None):
    if right is None:
        right = len(arr) - 1
    if left < right:
        # 随机选择 pivot
        rand_idx = random.randint(left, right)
        arr[rand_idx], arr[right] = arr[right], arr[rand_idx]
        pivot_idx = partition(arr, left, right)
        quick_sort_random(arr, left, pivot_idx - 1)
        quick_sort_random(arr, pivot_idx + 1, right)
    return arr
```

| 指标 | 值 |
|-----|----|
| 时间复杂度 | O(n log n) 平均, O(n²) 最差 |
| 空间复杂度 | O(log n) 递归栈 |
| 稳定性 | 不稳定 |

### 堆排序 (Heap Sort)

利用最大堆进行排序（详见 [Heap.md](DataStructures/Heap.md)）。

```python
def heap_sort(arr):
    n = len(arr)
    
    # 建堆 O(n)
    for i in range(n // 2 - 1, -1, -1):
        _heapify(arr, n, i)
    
    # 排序 O(n log n)
    for i in range(n - 1, 0, -1):
        arr[0], arr[i] = arr[i], arr[0]
        _heapify(arr, i, 0)
    
    return arr

def _heapify(arr, n, i):
    largest = i
    left = 2 * i + 1
    right = 2 * i + 2
    
    if left < n and arr[left] > arr[largest]:
        largest = left
    if right < n and arr[right] > arr[largest]:
        largest = right
    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]
        _heapify(arr, n, largest)
```

| 指标 | 值 |
|-----|----|
| 时间复杂度 | O(n log n) 全部情况 |
| 空间复杂度 | O(1) |
| 稳定性 | 不稳定 |

## 线性时间排序

### 计数排序 (Counting Sort)

适用于整数排序，范围较小的情况。

```python
def counting_sort(arr):
    if not arr:
        return arr
    
    max_val = max(arr)
    min_val = min(arr)
    range_size = max_val - min_val + 1
    
    # 计数
    count = [0] * range_size
    for num in arr:
        count[num - min_val] += 1
    
    # 累计
    for i in range(1, len(count)):
        count[i] += count[i - 1]
    
    # 构建输出
    output = [0] * len(arr)
    for num in reversed(arr):
        idx = count[num - min_val] - 1
        output[idx] = num
        count[num - min_val] -= 1
    
    return output
```

| 指标 | 值 |
|-----|----|
| 时间复杂度 | O(n + k)，k 为值域范围 |
| 空间复杂度 | O(k) |
| 稳定性 | 稳定 |

### 基数排序 (Radix Sort)

按位进行排序，从最低位到最高位。

```python
def radix_sort(arr):
    if not arr:
        return arr
    
    max_val = max(arr)
    exp = 1
    
    while max_val // exp > 0:
        counting_sort_by_digit(arr, exp)
        exp *= 10
    
    return arr

def counting_sort_by_digit(arr, exp):
    n = len(arr)
    output = [0] * n
    count = [0] * 10
    
    for num in arr:
        digit = (num // exp) % 10
        count[digit] += 1
    
    for i in range(1, 10):
        count[i] += count[i - 1]
    
    for num in reversed(arr):
        digit = (num // exp) % 10
        output[count[digit] - 1] = num
        count[digit] -= 1
    
    arr[:] = output
```

| 指标 | 值 |
|-----|----|
| 时间复杂度 | O(d × (n + k))，d 为位数，k=10 |
| 空间复杂度 | O(n + k) |
| 稳定性 | 稳定 |

### 桶排序 (Bucket Sort)

将元素分配到桶中，桶内排序后合并。

```python
def bucket_sort(arr, bucket_size=5):
    if not arr:
        return arr
    
    min_val, max_val = min(arr), max(arr)
    bucket_count = (max_val - min_val) // bucket_size + 1
    buckets = [[] for _ in range(bucket_count)]
    
    for num in arr:
        idx = (num - min_val) // bucket_size
        buckets[idx].append(num)
    
    result = []
    for bucket in buckets:
        result.extend(sorted(bucket))  # 桶内可用插入排序
    
    return result
```

| 指标 | 值 |
|-----|----|
| 时间复杂度 | O(n + k) 平均, O(n²) 最差 |
| 空间复杂度 | O(n + k) |
| 稳定性 | 取决于桶内排序 |

## 排序算法对比表

| 算法 | 平均时间 | 最差时间 | 最好时间 | 空间 | 稳定 | 原地 |
|-----|---------|---------|---------|------|------|------|
| 冒泡排序 | O(n²) | O(n²) | O(n) | O(1) | ✅ | ✅ |
| 选择排序 | O(n²) | O(n²) | O(n²) | O(1) | ❌ | ✅ |
| 插入排序 | O(n²) | O(n²) | O(n) | O(1) | ✅ | ✅ |
| 希尔排序 | O(n log² n) | O(n²) | O(n log n) | O(1) | ❌ | ✅ |
| 归并排序 | O(n log n) | O(n log n) | O(n log n) | O(n) | ✅ | ❌ |
| 快速排序 | O(n log n) | O(n²) | O(n log n) | O(log n) | ❌ | ✅ |
| 堆排序 | O(n log n) | O(n log n) | O(n log n) | O(1) | ❌ | ✅ |
| 计数排序 | O(n+k) | O(n+k) | O(n+k) | O(k) | ✅ | ❌ |
| 基数排序 | O(d(n+k)) | O(d(n+k)) | O(d(n+k)) | O(n+k) | ✅ | ❌ |
| 桶排序 | O(n+k) | O(n²) | O(n+k) | O(n+k) | ✅ | ❌ |

## Python 内置排序

```python
# Timsort — 混合排序（归并 + 插入）
arr = [3, 1, 4, 1, 5, 9]

# 原地排序
arr.sort()              # 升序
arr.sort(reverse=True)  # 降序
arr.sort(key=lambda x: -x)

# 返回新列表
sorted_arr = sorted(arr)
sorted_arr = sorted(arr, reverse=True)
sorted_arr = sorted(arr, key=lambda x: x % 2)  # 按模 2 排序
```

Python 的 Timsort 时间复杂度 O(n log n)，最差 O(n log n)，空间 O(n)，稳定排序。

## 常见面试题

### 第 K 大元素 (LeetCode 215)

```python
def find_kth_largest(nums, k):
    """快速选择 (QuickSelect)"""
    def quick_select(left, right, k_smallest):
        if left == right:
            return nums[left]
        
        pivot_idx = partition(nums, left, right)
        
        if k_smallest == pivot_idx:
            return nums[pivot_idx]
        elif k_smallest < pivot_idx:
            return quick_select(left, pivot_idx - 1, k_smallest)
        else:
            return quick_select(pivot_idx + 1, right, k_smallest)
    
    n = len(nums)
    return quick_select(0, n - 1, n - k)
```

### 颜色分类 (LeetCode 75)

```python
def sort_colors(nums):
    """荷兰国旗问题（三路快排）"""
    left = curr = 0
    right = len(nums) - 1
    
    while curr <= right:
        if nums[curr] == 0:
            nums[left], nums[curr] = nums[curr], nums[left]
            left += 1
            curr += 1
        elif nums[curr] == 2:
            nums[curr], nums[right] = nums[right], nums[curr]
            right -= 1
        else:
            curr += 1
```

## 练习

| 题目 | 难度 | 核心技巧 |
|------|------|---------|
| LeetCode 912. 排序数组 | 🟡 中等 | 实现任意排序 |
| LeetCode 75. 颜色分类 | 🟡 中等 | 三路快排 |
| LeetCode 215. 第 K 大元素 | 🟡 中等 | 快速选择/堆 |
| LeetCode 148. 排序链表 | 🟡 中等 | 归并排序 |
| LeetCode 179. 最大数 | 🟡 中等 | 自定义排序 |
| LeetCode 56. 合并区间 | 🟡 中等 | 排序 |
| LeetCode 164. 最大间距 | 🔴 困难 | 基数排序/桶排序 |
| LeetCode 493. 翻转对 | 🔴 困难 | 归并排序 |

## 相关条目

- [[BinarySearch]]
- [[BasicAlgorithms]]
- [[TwoPointers]]
- [[Heap]]
- [[Array]]
