---
aliases: [BinarySearch]
tags: ['DataStructuresAndAlgorithms', 'Algorithms', 'BinarySearch']
created: 2026-05-16
updated: 2026-05-16
---

# 二分查找完全指南

## 算法思想

二分查找（Binary Search）是一种在**有序数组**中查找特定元素的高效算法。其核心思想是每次将搜索范围缩小一半：

1. 取数组中间元素与目标值比较
2. 如果相等，返回索引
3. 如果目标值小于中间元素，在左半部分继续查找
4. 如果目标值大于中间元素，在右半部分继续查找
5. 重复直到找到或搜索范围为空

```
搜索 7 在 [1, 3, 5, 7, 9, 11, 13] 中：

[1, 3, 5, 7, 9, 11, 13]  mid=7, 7==7 ✓ 找到！
 ^        ^         ^
left     mid      right
```

## 时间复杂度

| 维度 | 值 |
|------|-----|
| 最坏时间复杂度 | O(log n) |
| 最优时间复杂度 | O(1) |
| 平均时间复杂度 | O(log n) |
| 空间复杂度 | O(1)（迭代） / O(log n)（递归） |

n=100 万时，最坏只需 log₂(1,000,000) ≈ 20 次比较。

## 实现细节

### 标准二分查找

```python
def binary_search(arr: list[int], target: int) -> int:
    """标准二分查找，返回目标索引，未找到返回 -1"""
    left, right = 0, len(arr) - 1
    
    while left <= right:
        mid = left + (right - left) // 2  # 防止溢出
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    
    return -1
```

```cpp
int binarySearch(vector<int>& arr, int target) {
    int left = 0, right = arr.size() - 1;
    
    while (left <= right) {
        int mid = left + (right - left) / 2;  // 防止 (left+right) 溢出
        if (arr[mid] == target)
            return mid;
        else if (arr[mid] < target)
            left = mid + 1;
        else
            right = mid - 1;
    }
    
    return -1;
}
```

### mid 计算防溢出

```python
# 不推荐（可能溢出，当 left + right > 2³¹-1）
mid = (left + right) // 2

# 推荐（不会溢出）
mid = left + (right - left) // 2

# 或位运算（更快）
mid = (left + right) >> 1
```

### 边界处理细节

| 条件 | left 更新 | right 更新 | 循环条件 | 返回值 |
|------|-----------|-----------|---------|--------|
| `left <= right` | `mid + 1` | `mid - 1` | 区间 [left, right] | 找到返回 mid，否则 -1 |
| `left < right` | `mid + 1` | `mid` | 区间 [left, right) | 收缩到 left=right 退出 |

## 变体

### 查找左边界（第一个等于 target 的位置）

```python
def find_left_boundary(arr: list[int], target: int) -> int:
    """返回第一个 >= target 的索引"""
    left, right = 0, len(arr)
    
    while left < right:
        mid = left + (right - left) // 2
        if arr[mid] >= target:
            right = mid
        else:
            left = mid + 1
    
    return left

# 示例
# arr = [1, 2, 2, 2, 3, 4], target = 2
# find_left_boundary(arr, 2) → 1
```

### 查找右边界（最后一个等于 target 的位置）

```python
def find_right_boundary(arr: list[int], target: int) -> int:
    """返回第一个 > target 的索引 - 1"""
    left, right = 0, len(arr)
    
    while left < right:
        mid = left + (right - left) // 2
        if arr[mid] > target:
            right = mid
        else:
            left = mid + 1
    
    return left - 1

# 示例
# arr = [1, 2, 2, 2, 3, 4], target = 2
# find_right_boundary(arr, 2) → 3
```

### 查找最接近元素

```python
def find_closest(arr: list[int], target: int) -> int:
    """返回最接近 target 的元素索引"""
    left, right = 0, len(arr) - 1
    
    if target <= arr[left]:
        return left
    if target >= arr[right]:
        return right
    
    while left <= right:
        mid = left + (right - left) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    
    # left > right，检查相邻两个哪个更接近
    if abs(arr[left] - target) < abs(arr[right] - target):
        return left
    return right
```

## 应用场景

### 1. 有序数组查找

```python
# 标准二分查找，最基本的应用
index = binary_search([1, 3, 5, 7, 9, 11, 13], 7)
```

### 2. 旋转数组查找

```python
def search_rotated(nums: list[int], target: int) -> int:
    """在旋转排序数组中查找（如 [4,5,6,7,0,1,2]）"""
    left, right = 0, len(nums) - 1
    
    while left <= right:
        mid = left + (right - left) // 2
        if nums[mid] == target:
            return mid
        
        # 左半部分有序
        if nums[left] <= nums[mid]:
            if nums[left] <= target < nums[mid]:
                right = mid - 1
            else:
                left = mid + 1
        # 右半部分有序
        else:
            if nums[mid] < target <= nums[right]:
                left = mid + 1
            else:
                right = mid - 1
    
    return -1
```

### 3. 二分答案

```python
def sqrt_approx(x: float, epsilon: float = 1e-10) -> float:
    """二分法求平方根近似值"""
    if x < 0:
        raise ValueError("Cannot compute sqrt of negative number")
    if x == 0 or x == 1:
        return x
    
    left, right = (0, x) if x > 1 else (x, 1)
    
    while right - left > epsilon:
        mid = (left + right) / 2
        if mid * mid > x:
            right = mid
        else:
            left = mid
    
    return (left + right) / 2
```

### 常见二分答案场景

| 场景 | 问题 | check 函数 |
|------|------|-----------|
| 分割数组 | 将数组分成 m 段，使最大值最小 | 判断能否在 ≤mid 下分成 m 段 |
| 木材切割 | 将木材切成 k 段等长，求最大长度 | 判断能否切出 k 段 ≥mid 的木材 |
| 运输问题 | 在 D 天内运完货物，求最小运力 | 判断能否 ≤mid 运力在 D 天内运完 |
| Koko 吃香蕉 | 每小时吃 K 根，求最小 K | 判断能否在 H 小时内吃完 |

```python
def min_eating_speed(piles: list[int], h: int) -> int:
    """Koko 吃香蕉 - 二分答案经典题"""
    def can_eat(speed: int) -> bool:
        hours = 0
        for p in piles:
            hours += (p + speed - 1) // speed  # 向上取整
        return hours <= h
    
    left, right = 1, max(piles)
    
    while left < right:
        mid = left + (right - left) // 2
        if can_eat(mid):
            right = mid
        else:
            left = mid + 1
    
    return left
```

## 二分查找模板总结

```python
def binary_search_template(arr, target):
    """通用二分查找模板"""
    left, right = 0, len(arr)  # [left, right) 左闭右开
    
    while left < right:
        mid = left + (right - left) // 2
        
        if arr[mid] == target:
            return mid  # 找到返回
        elif arr[mid] < target:
            left = mid + 1  # 右移
        else:
            right = mid  # 左移
    
    return left  # 返回插入位置（或 -1 表示未找到）

# 不同需求的返回值：
# - 标准查找：找到返回 mid，否则 -1
# - 左边界：返回 left（第一个 >= 的位置）
# - 右边界：返回 left - 1（最后一个 <= 的位置）
# - 插入位置：返回 left（应插入的索引）
```

## 相关条目

- [[Sorting]]
- [[05_ComputerScience/DataStructuresAndAlgorithms/Algorithms/BasicAlgorithms/BasicAlgorithms|BasicAlgorithms]]
- [[TwoPointers]]
- [[05_ComputerScience/DataStructuresAndAlgorithms/DataStructures/Array|Array]]
- [[05_ComputerScience/DataStructuresAndAlgorithms/DataStructures/Tree|Tree]]


