---
aliases: [TwoPointers]
tags: ['DataStructuresAndAlgorithms', 'Algorithms', 'TwoPointers']
created: 2026-05-16
updated: 2026-05-13
---

# 双指针技巧

## 概述

双指针（Two Pointers）是一种使用两个指针遍历线性数据结构的技巧。根据指针移动方向，分为三种模式：

1. **对撞指针**：两个指针从两端向中间移动
2. **快慢指针**：两个指针同向移动，速度不同
3. **滑动窗口**：两个指针维护一个区间

## 一、对撞指针 (Opposite Direction)

两个指针分别从数组首尾向中间移动。

### 1. 两数之和 II (LeetCode 167)

```python
def two_sum(numbers, target):
    """有序数组的两数之和"""
    left, right = 0, len(numbers) - 1
    while left < right:
        s = numbers[left] + numbers[right]
        if s == target:
            return [left + 1, right + 1]
        elif s < target:
            left += 1
        else:
            right -= 1
    return []
```

**时间复杂度**: O(n), **空间复杂度**: O(1)

### 2. 三数之和 (LeetCode 15)

```python
def three_sum(nums):
    """三数之和为 0"""
    nums.sort()
    result = []
    n = len(nums)
    
    for i in range(n - 2):
        if i > 0 and nums[i] == nums[i - 1]:  # 去重
            continue
        
        left, right = i + 1, n - 1
        target = -nums[i]
        
        while left < right:
            s = nums[left] + nums[right]
            if s == target:
                result.append([nums[i], nums[left], nums[right]])
                left += 1
                right -= 1
                while left < right and nums[left] == nums[left - 1]:
                    left += 1
                while left < right and nums[right] == nums[right + 1]:
                    right -= 1
            elif s < target:
                left += 1
            else:
                right -= 1
    
    return result
```

**时间复杂度**: O(n²), **空间复杂度**: O(1) 或 O(n) 排序空间

### 3. 验证回文串 (LeetCode 125)

```python
def is_palindrome(s):
    """判断是否为回文串（忽略非字母数字）"""
    left, right = 0, len(s) - 1
    while left < right:
        while left < right and not s[left].isalnum():
            left += 1
        while left < right and not s[right].isalnum():
            right -= 1
        if s[left].lower() != s[right].lower():
            return False
        left += 1
        right -= 1
    return True
```

### 4. 盛最多水的容器 (LeetCode 11)

```python
def max_area(height):
    """盛最多水的容器"""
    left, right = 0, len(height) - 1
    max_water = 0
    
    while left < right:
        area = min(height[left], height[right]) * (right - left)
        max_water = max(max_water, area)
        
        if height[left] < height[right]:
            left += 1
        else:
            right -= 1
    
    return max_water
```

**策略**: 移动较矮的那一边，因为移动较高边不会有更大面积。

## 二、快慢指针 (Same Direction)

两个指针同向移动，一个快一个慢。

### 1. 环形链表检测 (LeetCode 141/142)

```python
def has_cycle(head):
    """检测链表是否有环"""
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow == fast:
            return True
    return False

def detect_cycle(head):
    """返回环的入口"""
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow == fast:
            slow = head
            while slow != fast:
                slow = slow.next
                fast = fast.next
            return slow
    return None
```

### 2. 删除倒数第 N 个节点 (LeetCode 19)

```python
def remove_nth_from_end(head, n):
    """删除倒数第 n 个节点"""
    dummy = ListNode(0, head)
    fast = slow = dummy
    
    for _ in range(n + 1):
        fast = fast.next
    
    while fast:
        fast = fast.next
        slow = slow.next
    
    slow.next = slow.next.next
    return dummy.next
```

### 3. 链表中点

```python
def middle_node(head):
    """返回链表中间节点"""
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
    return slow
```

### 4. 寻找重复数 (LeetCode 287)

```python
def find_duplicate(nums):
    """在 O(1) 空间内找重复数（快慢指针，将值视为链表）"""
    slow = fast = nums[0]
    while True:
        slow = nums[slow]
        fast = nums[nums[fast]]
        if slow == fast:
            break
    
    slow = nums[0]
    while slow != fast:
        slow = nums[slow]
        fast = nums[fast]
    
    return slow
```

## 三、滑动窗口 (维护区间)

详见 [SlidingWindow.md](SlidingWindow.md)。

```python
def min_window(s, t):
    """最小覆盖子串 — 滑动窗口"""
    from collections import Counter
    need = Counter(t)
    missing = len(t)
    left = 0
    result = (0, float('inf'))
    
    for right, char in enumerate(s):
        if char in need:
            if need[char] > 0:
                missing -= 1
            need[char] -= 1
        
        while missing == 0:
            if right - left < result[1] - result[0]:
                result = (left, right)
            
            left_char = s[left]
            if left_char in need:
                if need[left_char] >= 0:
                    missing += 1
                need[left_char] += 1
            left += 1
    
    return s[result[0]:result[1] + 1] if result[1] != float('inf') else ""
```

## 综合对比

| 模式 | 方向 | 典型应用 | 时间复杂度 |
|-----|------|---------|-----------|
| 对撞指针 | left++, right-- | 两数之和、回文、三数之和 | O(n) / O(n²) |
| 快慢指针 | 同向不同速 | 链表环、中点、倒数第 K | O(n) |
| 滑动窗口 | 同向维护区间 | 子串、子数组 | O(n) |

## 常见问题

### 移除元素 (LeetCode 27)

```python
def remove_element(nums, val):
    """原地移除所有等于 val 的元素（快慢指针）"""
    slow = 0
    for fast in range(len(nums)):
        if nums[fast] != val:
            nums[slow] = nums[fast]
            slow += 1
    return slow
```

## 练习

| 题目 | 难度 | 指针模式 |
|------|------|---------|
| LeetCode 167. 两数之和 II | 🟢 简单 | 对撞 |
| LeetCode 125. 验证回文串 | 🟢 简单 | 对撞 |
| LeetCode 11. 盛最多水的容器 | 🟡 中等 | 对撞 |
| LeetCode 15. 三数之和 | 🟡 中等 | 对撞 |
| LeetCode 16. 最接近的三数之和 | 🟡 中等 | 对撞 |
| LeetCode 141. 环形链表 | 🟢 简单 | 快慢 |
| LeetCode 142. 环形链表 II | 🟡 中等 | 快慢 |
| LeetCode 19. 删除倒数第 N 个节点 | 🟡 中等 | 快慢 |
| LeetCode 287. 寻找重复数 | 🟡 中等 | 快慢 |
| LeetCode 26. 删除有序数组重复项 | 🟢 简单 | 快慢 |
| LeetCode 27. 移除元素 | 🟢 简单 | 快慢 |
| LeetCode 283. 移动零 | 🟢 简单 | 快慢 |
| LeetCode 88. 合并有序数组 | 🟢 简单 | 逆向双指针 |
| LeetCode 344. 反转字符串 | 🟢 简单 | 对撞 |

## 相关条目

- [[SlidingWindow]]
- [[Array]]
- [[LinkedList]]
- [[Sorting]]
- [[BinarySearch]]
