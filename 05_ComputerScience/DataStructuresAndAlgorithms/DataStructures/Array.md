---
aliases: [Array]
tags: ['DataStructuresAndAlgorithms', 'DataStructures', 'Array']
---

# 数组详解

## 基本概念

数组（Array）是一种线性数据结构，用连续的内存空间存储相同类型的数据。数组的特点是支持**随机访问**，即通过下标可以在 O(1) 时间内访问任意元素。

### 静态数组 vs 动态数组

| 特性 | 静态数组 (Static Array) | 动态数组 (Dynamic Array) |
|------|------------------------|-------------------------|
| 大小 | 创建时固定 | 可动态增长 |
| 内存分配 | 栈或静态区 | 堆上分配 |
| 扩容 | 不支持 | 满时自动扩容（通常 1.5x-2x） |
| 语言示例 | C++ `int arr[10]` | Python `list`, C++ `std::vector` |

## 时间复杂度

| 操作 | 静态数组 | 动态数组（均摊） |
|-----|---------|----------------|
| 访问 (Access) | O(1) | O(1) |
| 搜索 (Search) | O(n) | O(n) |
| 插入 (Insert) | O(n) | O(n) |
| 删除 (Delete) | O(n) | O(n) |
| 末尾添加 | — | O(1) 均摊 |

### Python 中的数组

```python
# Python list - 动态数组
arr = [1, 2, 3, 4, 5]
arr.append(6)               # O(1) 均摊
arr.insert(2, 99)           # O(n)
arr.pop()                   # O(1)
arr.pop(2)                  # O(n)
arr[3]                      # O(1) 随机访问
len(arr)                    # O(1)

# array 模块 - 类型化数组
from array import array
int_arr = array('i', [1, 2, 3])  # 'i' = signed int

# NumPy 数组 - 高效数值运算
import numpy as np
np_arr = np.array([1, 2, 3, 4, 5])
np_arr_2d = np.zeros((3, 4))     # 3x4 零矩阵
```

### C++ 数组

```cpp
#include <vector>
#include <array>

// 静态数组
int arr[5] = {1, 2, 3, 4, 5};

// STL 动态数组
std::vector<int> vec = {1, 2, 3};
vec.push_back(4);        // O(1) 均摊
vec.insert(vec.begin() + 2, 99);  // O(n)
```

## 二维数组

二维数组本质上是"数组的数组"，内存中按行优先（row-major）存储。

```python
# 创建一个 3x4 的二维数组
matrix = [[0] * 4 for _ in range(3)]

# 按行遍历
for i in range(len(matrix)):
    for j in range(len(matrix[0])):
        print(matrix[i][j], end=' ')

# 矩阵转置
transposed = list(zip(*matrix))
```

## 常见技巧

### 前缀和 (Prefix Sum)

前缀和可以在 O(1) 时间内计算任意子数组的和。

```python
def prefix_sum(arr):
    """构建前缀和数组"""
    n = len(arr)
    pref = [0] * (n + 1)
    for i in range(n):
        pref[i + 1] = pref[i] + arr[i]
    return pref

def range_sum(pref, l, r):
    """计算 arr[l..r] 的和，包含两端"""
    return pref[r + 1] - pref[l]

# 使用
arr = [1, 2, 3, 4, 5]
pref = prefix_sum(arr)
print(range_sum(pref, 1, 3))  # 2+3+4 = 9
```

**时间复杂度**: 构建 O(n), 查询 O(1)
**空间复杂度**: O(n)

### 差分数组 (Difference Array)

差分数组用于快速进行区间增减操作。

```python
def difference_array(arr):
    """构建差分数组"""
    n = len(arr)
    diff = [0] * (n + 1)
    diff[0] = arr[0]
    for i in range(1, n):
        diff[i] = arr[i] - arr[i - 1]
    return diff

def add_range(diff, l, r, val):
    """给 arr[l..r] 所有元素加 val"""
    diff[l] += val
    diff[r + 1] -= val

def restore(diff):
    """从差分数组恢复原数组"""
    n = len(diff) - 1
    arr = [0] * n
    arr[0] = diff[0]
    for i in range(1, n):
        arr[i] = arr[i - 1] + diff[i]
    return arr
```

## 常见模式

### 双指针 (Two Pointers)

```python
def two_sum_sorted(arr, target):
    """有序数组的两数之和"""
    left, right = 0, len(arr) - 1
    while left < right:
        s = arr[left] + arr[right]
        if s == target:
            return [left, right]
        elif s < target:
            left += 1
        else:
            right -= 1
    return []
```

### 滑动窗口 (Sliding Window)

```python
def max_sum_subarray(arr, k):
    """固定长度 k 的最大子数组和"""
    window_sum = sum(arr[:k])
    max_sum = window_sum
    for i in range(k, len(arr)):
        window_sum += arr[i] - arr[i - k]
        max_sum = max(max_sum, window_sum)
    return max_sum
```

## 经典问题

### 两数之和 (LeetCode 1)

```python
def two_sum(nums, target):
    """使用哈希表，O(n) 时间"""
    seen = {}
    for i, num in enumerate(nums):
        complement = target - num
        if complement in seen:
            return [seen[complement], i]
        seen[num] = i
    return []
```

- **时间复杂度**: O(n)
- **空间复杂度**: O(n)

### 接雨水 (LeetCode 42)

```python
def trap(height):
    """双指针法计算能接的雨水量"""
    left, right = 0, len(height) - 1
    left_max = right_max = 0
    water = 0
    
    while left < right:
        if height[left] < height[right]:
            if height[left] >= left_max:
                left_max = height[left]
            else:
                water += left_max - height[left]
            left += 1
        else:
            if height[right] >= right_max:
                right_max = height[right]
            else:
                water += right_max - height[right]
            right -= 1
    
    return water
```

- **时间复杂度**: O(n)
- **空间复杂度**: O(1)

### 螺旋矩阵 (LeetCode 54)

```python
def spiral_order(matrix):
    """按螺旋顺序返回矩阵元素"""
    if not matrix or not matrix[0]:
        return []
    
    res = []
    top, bottom = 0, len(matrix) - 1
    left, right = 0, len(matrix[0]) - 1
    
    while top <= bottom and left <= right:
        # 从左到右
        for j in range(left, right + 1):
            res.append(matrix[top][j])
        top += 1
        
        # 从上到下
        for i in range(top, bottom + 1):
            res.append(matrix[i][right])
        right -= 1
        
        if top <= bottom:
            # 从右到左
            for j in range(right, left - 1, -1):
                res.append(matrix[bottom][j])
            bottom -= 1
        
        if left <= right:
            # 从下到上
            for i in range(bottom, top - 1, -1):
                res.append(matrix[i][left])
            left += 1
    
    return res
```

- **时间复杂度**: O(m × n)
- **空间复杂度**: O(1) 不含输出

## 数组旋转

```python
def rotate(arr, k):
    """将数组右旋 k 步"""
    n = len(arr)
    k %= n
    # 三步反转法
    reverse(arr, 0, n - 1)
    reverse(arr, 0, k - 1)
    reverse(arr, k, n - 1)

def reverse(arr, l, r):
    while l < r:
        arr[l], arr[r] = arr[r], arr[l]
        l += 1
        r -= 1
```

- **时间复杂度**: O(n)
- **空间复杂度**: O(1)

## 练习

| 题目 | 难度 | 核心技巧 |
|------|------|---------|
| LeetCode 1. 两数之和 | 🟢 简单 | 哈希表 |
| LeetCode 26. 删除有序数组重复项 | 🟢 简单 | 双指针 |
| LeetCode 27. 移除元素 | 🟢 简单 | 双指针 |
| LeetCode 53. 最大子数组和 | 🟢 简单 | Kadane 算法 |
| LeetCode 88. 合并两个有序数组 | 🟢 简单 | 双指针从后 |
| LeetCode 189. 旋转数组 | 🟢 简单 | 三步反转 |
| LeetCode 283. 移动零 | 🟢 简单 | 双指针 |
| LeetCode 15. 三数之和 | 🟡 中等 | 排序+双指针 |
| LeetCode 42. 接雨水 | 🔴 困难 | 双指针/单调栈 |
| LeetCode 54. 螺旋矩阵 | 🟡 中等 | 边界收缩 |
| LeetCode 56. 合并区间 | 🟡 中等 | 排序 |
| LeetCode 238. 除自身以外乘积 | 🟡 中等 | 前缀积 |
| LeetCode 4. 寻找两个正序数组的中位数 | 🔴 困难 | 二分查找 |

## 相关条目

- [[LinkedList]]
- [[Stack]]
- [[Queue]]
- [[HashTable]]
- [[Sorting]]
