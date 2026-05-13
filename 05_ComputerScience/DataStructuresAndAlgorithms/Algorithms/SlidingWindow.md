# 滑动窗口详解

## 基本概念

滑动窗口（Sliding Window）是双指针技巧的一种，维护一个**动态区间**，通过移动窗口的左右边界来解决问题。

### 适用场景

- 连续子数组/子串问题
- 需要 O(n) 时间复杂度的场景
- 窗口大小固定或可变

### 基本框架

```python
def sliding_window(s):
    """滑动窗口通用框架"""
    from collections import defaultdict
    window = defaultdict(int)
    left = right = 0
    result = []
    
    while right < len(s):
        # 扩大窗口
        c = s[right]
        right += 1
        # 更新窗口内数据
        process_char_in(c)
        
        # 缩小窗口条件
        while shoud_shrink():
            d = s[left]
            left += 1
            # 更新窗口内数据
            process_char_out(d)
        
        # 记录结果（窗口满足条件时）
        update_result()
```

## 固定窗口大小

### 1. 大小为 K 的最大子数组和

```python
def max_sum_subarray(arr, k):
    """固定长度为 k 的最大子数组和"""
    window_sum = sum(arr[:k])
    max_sum = window_sum
    
    for i in range(k, len(arr)):
        window_sum += arr[i] - arr[i - k]
        max_sum = max(max_sum, window_sum)
    
    return max_sum
```

**时间复杂度**: O(n), **空间复杂度**: O(1)

### 2. 存在重复元素 II (LeetCode 219)

```python
def contains_nearby_duplicate(nums, k):
    """是否存在距离 ≤ k 的相同元素"""
    window = set()
    
    for i, num in enumerate(nums):
        if num in window:
            return True
        
        window.add(num)
        if len(window) > k:
            window.remove(nums[i - k])
    
    return False
```

### 3. 滑动窗口最大值 (LeetCode 239)

```python
from collections import deque

def max_sliding_window(nums, k):
    """每个滑动窗口的最大值（单调队列）"""
    dq = deque()  # 存储下标，对应值单调递减
    result = []
    
    for i, num in enumerate(nums):
        # 移除窗口外的元素
        if dq and dq[0] < i - k + 1:
            dq.popleft()
        
        # 维护单调递减队列
        while dq and nums[dq[-1]] < num:
            dq.pop()
        dq.append(i)
        
        # 窗口形成后记录结果
        if i >= k - 1:
            result.append(nums[dq[0]])
    
    return result
```

## 可变窗口大小

### 1. 无重复字符的最长子串 (LeetCode 3)

```python
def length_of_longest_substring(s):
    """最长无重复字符子串"""
    from collections import defaultdict
    window = defaultdict(int)
    left = max_len = 0
    
    for right, c in enumerate(s):
        window[c] += 1
        
        while window[c] > 1:  # 有重复，缩小窗口
            window[s[left]] -= 1
            left += 1
        
        max_len = max(max_len, right - left + 1)
    
    return max_len
```

**时间复杂度**: O(n), **空间复杂度**: O(min(m, n)) — m 为字符集大小

### 2. 最小覆盖子串 (LeetCode 76)

```python
def min_window(s, t):
    """包含 t 中所有字符的最小子串"""
    from collections import Counter
    need = Counter(t)
    missing = len(t)
    left = 0
    result = (0, float('inf'))
    
    for right, c in enumerate(s):
        if c in need:
            if need[c] > 0:
                missing -= 1
            need[c] -= 1
        
        while missing == 0:  # 已完全覆盖
            if right - left < result[1] - result[0]:
                result = (left, right)
            
            left_c = s[left]
            if left_c in need:
                if need[left_c] >= 0:
                    missing += 1
                need[left_c] += 1
            left += 1
    
    return s[result[0]:result[1] + 1] if result[1] != float('inf') else ""
```

### 3. 字符串排列 (LeetCode 567)

```python
def check_inclusion(s1, s2):
    """s2 是否包含 s1 的排列"""
    from collections import Counter
    need = Counter(s1)
    missing = len(s1)
    left = 0
    
    for right, c in enumerate(s2):
        if c in need:
            if need[c] > 0:
                missing -= 1
            need[c] -= 1
        
        while missing == 0:
            if right - left + 1 == len(s1):
                return True
            
            left_c = s2[left]
            if left_c in need:
                if need[left_c] >= 0:
                    missing += 1
                need[left_c] += 1
            left += 1
    
    return False
```

### 4. 最长重复字符替换 (LeetCode 424)

```python
def character_replacement(s, k):
    """最多替换 k 个字符使最长重复子串"""
    from collections import defaultdict
    window = defaultdict(int)
    max_freq = 0
    left = 0
    
    for right, c in enumerate(s):
        window[c] += 1
        max_freq = max(max_freq, window[c])
        
        # 窗口长度 - 最大频率 > k 时需要缩小
        if right - left + 1 - max_freq > k:
            window[s[left]] -= 1
            left += 1
    
    return len(s) - left
```

### 5. 和至少为 K 的最短子数组 (LeetCode 862)

```python
def shortest_subarray(nums, k):
    """和至少为 K 的最短非空子数组长度"""
    from collections import deque
    n = len(nums)
    prefix = [0] * (n + 1)
    for i in range(n):
        prefix[i + 1] = prefix[i] + nums[i]
    
    dq = deque()
    min_len = float('inf')
    
    for i in range(n + 1):
        while dq and prefix[i] - prefix[dq[0]] >= k:
            min_len = min(min_len, i - dq.popleft())
        
        while dq and prefix[i] <= prefix[dq[-1]]:
            dq.pop()
        
        dq.append(i)
    
    return min_len if min_len != float('inf') else -1
```

## 滑动窗口常见问题总结

### 缩小窗口的时机

| 问题类型 | 缩小条件 | 窗口属性 |
|---------|---------|---------|
| 无重复子串 | 窗口内有重复 | 不重复 |
| 最小覆盖子串 | 已包含全部目标字符 | 包含目标 |
| 字符串排列 | 窗口长度 == len(s1) | 字符频率匹配 |
| 最长重复替换 | 窗口长度 - 最大频率 > k | 可替换 ≤ k |

### 模板应用示例

```python
def sliding_window_template(s, condition_fn):
    """滑动窗口通用模板"""
    from collections import defaultdict
    window = defaultdict(int)
    left = 0
    result = 0
    
    for right, c in enumerate(s):
        # 加入右边界
        window[c] += 1
        
        # 调整左边界直到满足条件
        while condition_fn(window, left, right, s):
            window[s[left]] -= 1
            if window[s[left]] == 0:
                del window[s[left]]
            left += 1
        
        # 更新结果
        result = max(result, right - left + 1)
    
    return result
```

## 滑动窗口 vs 动态规划

| 特性 | 滑动窗口 | 动态规划 |
|-----|---------|---------|
| 适用场景 | 连续子串/子数组 | 各种最优化问题 |
| 时间复杂度 | 通常 O(n) | 通常 O(n²) 或更高 |
| 空间复杂度 | 通常 O(1) | 通常 O(n) |
| 思路 | 维护区间 | 状态转移 |

## 练习

| 题目 | 难度 | 窗口类型 |
|------|------|---------|
| LeetCode 3. 无重复字符最长子串 | 🟡 中等 | 可变 |
| LeetCode 76. 最小覆盖子串 | 🔴 困难 | 可变 |
| LeetCode 239. 滑动窗口最大值 | 🔴 困难 | 固定 + 单调队列 |
| LeetCode 424. 最长重复字符替换 | 🟡 中等 | 可变 |
| LeetCode 567. 字符串排列 | 🟡 中等 | 固定 |
| LeetCode 438. 找到字符串所有异位词 | 🟡 中等 | 固定 |
| LeetCode 209. 长度最小的子数组 | 🟡 中等 | 可变 |
| LeetCode 862. 和至少为 K 的最短子数组 | 🔴 困难 | 可变 + 单调队列 |
| LeetCode 904. 水果成篮 | 🟡 中等 | 可变 |
| LeetCode 1004. 最大连续1的个数 III | 🟡 中等 | 可变 |
| LeetCode 480. 滑动窗口中位数 | 🔴 困难 | 固定 + 双堆 |
| LeetCode 995. K 连续位的最小翻转次数 | 🔴 困难 | 滑动窗口 |

## 相关条目

- [[TwoPointers]]
- [[BasicAlgorithms]]
- [[Array]]
- [[StringAlgorithms]]
- [[HashTable]]
