---
aliases: [BitManipulation]
tags: ['DataStructuresAndAlgorithms', 'Algorithms', 'BitManipulation']
---

# 位运算技巧

## 基本运算符

| 运算符 | 名称 | 示例 | 结果 |
|--------|------|------|------|
| `&` | 按位与 | `5 & 3` (101 & 011) | `1` (001) |
| `|` | 按位或 | `5 | 3` (101 | 011) | `7` (111) |
| `^` | 按位异或 | `5 ^ 3` (101 ^ 011) | `6` (110) |
| `~` | 按位取反 | `~5` (~101) | `-6` (...11111010) |
| `<<` | 左移 | `5 << 1` (101 << 1) | `10` (1010) |
| `>>` | 右移 | `5 >> 1` (101 >> 1) | `2` (10) |

## Python 位运算

```python
# 位运算符
a = 0b1100  # 12
b = 0b1010  # 10

print(a & b)   # 8  (0b1000)
print(a | b)   # 14 (0b1110)
print(a ^ b)   # 6  (0b0110)
print(~a)      # -13 (补码表示)
print(a << 1)  # 24 (0b11000)
print(a >> 1)  # 6  (0b0110)

# Python 中整数的位长度
print(a.bit_length())  # 4
print(bin(a))          # '0b1100'
```

## 常用技巧

### 1. 获取/设置/清除位

```python
# 获取第 k 位（从 0 开始）
def get_bit(num, k):
    return (num >> k) & 1

# 设置第 k 位为 1
def set_bit(num, k):
    return num | (1 << k)

# 清除第 k 位（置 0）
def clear_bit(num, k):
    return num & ~(1 << k)

# 切换第 k 位
def toggle_bit(num, k):
    return num ^ (1 << k)

# 将第 k 位设置为 val (0/1)
def update_bit(num, k, val):
    return (num & ~(1 << k)) | (val << k)
```

### 2. 常用检查

```python
# 判断奇偶
def is_odd(num):
    return num & 1  # 等价于 num % 2

# 判断是否为 2 的幂
def is_power_of_two(num):
    return num > 0 and (num & (num - 1)) == 0

# 判断两个数是否异号
def opposite_signs(a, b):
    return (a ^ b) < 0  # 符号位不同
```

### 3. 位操作

```python
# 移除最后一个 1
def remove_last_one(num):
    return num & (num - 1)

# 获取最后一个 1
def get_last_one(num):
    return num & -num  # lowbit

# 统计 1 的个数 (Brian Kernighan)
def count_bits(num):
    count = 0
    while num:
        num &= num - 1  # 移除最后一个 1
        count += 1
    return count

# 获取二进制长度
def bit_length(num):
    length = 0
    while num:
        num >>= 1
        length += 1
    return length

# 反转位
def reverse_bits(num, bits=32):
    result = 0
    for _ in range(bits):
        result = (result << 1) | (num & 1)
        num >>= 1
    return result
```

### 4. 算术技巧

```python
# 乘以 2 的幂
num << k   # num * 2^k

# 除以 2 的幂（向下取整）
num >> k   # num // 2^k

# 向上取整到 2 的幂
def next_power_of_two(num):
    if num <= 0:
        return 1
    num -= 1
    num |= num >> 1
    num |= num >> 2
    num |= num >> 4
    num |= num >> 8
    num |= num >> 16
    return num + 1

# 模 2 的幂
num & (k - 1)  # num % k, k 为 2 的幂

# 绝对值
def abs_bit(num):
    mask = num >> 31  # 负数 mask = -1, 正数 mask = 0
    return (num + mask) ^ mask

# 取最大值/最小值
def max_bit(a, b):
    return b ^ ((a ^ b) & -(a > b))

def min_bit(a, b):
    return a ^ ((a ^ b) & -(a > b))
```

## 经典应用

### 1. 只出现一次的数字 (LeetCode 136)

```python
def single_number(nums):
    """除了一个元素外，其他都出现两次"""
    result = 0
    for num in nums:
        result ^= num
    return result
```

**原理**: `a ^ a = 0`，`a ^ 0 = a`，异或满足交换律结合律。

### 2. 两个只出现一次的数字 (LeetCode 260)

```python
def single_number_iii(nums):
    """两个元素只出现一次，其他出现两次"""
    # 第一步：全部异或，得到 x ^ y
    xor_all = 0
    for num in nums:
        xor_all ^= num
    
    # 第二步：找到 x 和 y 不同的最低位
    diff_bit = xor_all & -xor_all
    
    # 第三步：按该位分组异或
    x = y = 0
    for num in nums:
        if num & diff_bit:
            x ^= num
        else:
            y ^= num
    
    return [x, y]
```

### 3. 只出现一次的数字 III — 出现三次 (LeetCode 137)

```python
def single_number_ii(nums):
    """除了一个出现一次，其他都出现三次"""
    ones = twos = 0
    for num in nums:
        ones = (ones ^ num) & ~twos
        twos = (twos ^ num) & ~ones
    return ones
```

### 4. 比特位计数 (LeetCode 338)

```python
def count_bits_dp(n):
    """0 到 n 每个数的二进制 1 的个数"""
    dp = [0] * (n + 1)
    for i in range(1, n + 1):
        # i >> 1 是 i 的一半，i & 1 判断最低位
        dp[i] = dp[i >> 1] + (i & 1)
    return dp
```

### 5. 子集枚举 (Bitmask)

```python
def subsets_bitmask(nums):
    """使用位掩码枚举所有子集"""
    n = len(nums)
    result = []
    
    for mask in range(1 << n):
        subset = []
        for i in range(n):
            if mask & (1 << i):
                subset.append(nums[i])
        result.append(subset)
    
    return result
```

### 6. 汉明距离 (LeetCode 461)

```python
def hamming_distance(x, y):
    """两个整数的二进制不同位数"""
    xor = x ^ y
    count = 0
    while xor:
        xor &= xor - 1
        count += 1
    return count
```

### 7. 位运算交换

```python
def swap(a, b):
    """不使用临时变量交换"""
    a ^= b
    b ^= a
    a ^= b
    return a, b
```

### 8. 位运算实现加法 (LeetCode 剑指 Offer 65)

```python
def add(a, b):
    """不用 + 实现加法"""
    while b:
        carry = (a & b) << 1   # 进位
        a ^= b                 # 无进位和
        b = carry              # 进位作为下一轮的加数
    return a
```

### 9. 最大单词长度乘积 (LeetCode 318)

```python
def max_product(words):
    """两个单词不含相同字母的最大长度乘积"""
    n = len(words)
    masks = [0] * n
    
    for i, word in enumerate(words):
        for c in word:
            masks[i] |= 1 << (ord(c) - ord('a'))
    
    max_prod = 0
    for i in range(n):
        for j in range(i + 1, n):
            if masks[i] & masks[j] == 0:
                max_prod = max(max_prod, len(words[i]) * len(words[j]))
    
    return max_prod
```

### 10. 状态压缩 DP (TSP 示例)

```python
def tsp_bitmask(n, dist):
    """旅行商问题（状态压缩 DP）"""
    dp = [[float('inf')] * n for _ in range(1 << n)]
    dp[1][0] = 0  # 从 0 出发，只访问了 0
    
    for mask in range(1 << n):
        for u in range(n):
            if not (mask >> u) & 1:
                continue
            if dp[mask][u] == float('inf'):
                continue
            
            for v in range(n):
                if (mask >> v) & 1:
                    continue
                new_mask = mask | (1 << v)
                dp[new_mask][v] = min(
                    dp[new_mask][v],
                    dp[mask][u] + dist[u][v]
                )
    
    full_mask = (1 << n) - 1
    return min(dp[full_mask][v] + dist[v][0] for v in range(1, n))
```

## 常见位运算技巧速查表

| 操作 | 表达式 |
|------|--------|
| 判断奇数 | `num & 1` |
| 判断 2 的幂 | `num > 0 and (num & (num-1)) == 0` |
| 移除最后一个 1 | `num & (num - 1)` |
| 获取最后一个 1 | `num & -num` |
| 统计 1 的个数 | Brian Kernighan 循环 |
| 交换两数 | `a ^= b; b ^= a; a ^= b` |
| 取绝对值 | `(num ^ (num >> 31)) - (num >> 31)` |
| 取最大值 | `b ^ ((a ^ b) & -(a > b))` |
| 两数是否异号 | `(a ^ b) < 0` |
| 乘以 2^k | `num << k` |
| 除以 2^k | `num >> k` |
| 对 2^k 取模 | `num & (k - 1)` |
| 向上取整到 2^k | 见 `next_power_of_two` |

## 练习

| 题目 | 难度 | 核心技巧 |
|------|------|---------|
| LeetCode 136. 只出现一次的数字 | 🟢 简单 | 异或 |
| LeetCode 137. 只出现一次的数字 II | 🟡 中等 | 状态机 |
| LeetCode 260. 只出现一次的数字 III | 🟡 中等 | 分组异或 |
| LeetCode 191. 位1的个数 | 🟢 简单 | Brian Kernighan |
| LeetCode 231. 2的幂 | 🟢 简单 | num & (num-1) |
| LeetCode 338. 比特位计数 | 🟢 简单 | DP |
| LeetCode 461. 汉明距离 | 🟢 简单 | 异或 |
| LeetCode 78. 子集 | 🟡 中等 | 位掩码 |
| LeetCode 201. 数字范围按位与 | 🟡 中等 | 找公共前缀 |
| LeetCode 318. 最大单词长度乘积 | 🟡 中等 | 位掩码 |
| LeetCode 371. 两整数之和 | 🟡 中等 | 位运算加法 |
| LeetCode 190. 颠倒二进制位 | 🟢 简单 | 位反转 |
| LeetCode 268. 丢失的数字 | 🟢 简单 | 异或 |
| LeetCode 389. 找不同 | 🟢 简单 | 异或 |

## 相关条目

- [[DP]]
- [[Backtracking]]
- [[Sorting]]
- [[BasicAlgorithms]]
- [[BinarySearch]]
