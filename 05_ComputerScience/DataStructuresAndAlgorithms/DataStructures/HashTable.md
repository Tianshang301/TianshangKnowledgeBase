# 哈希表详解

## 基本概念

哈希表（Hash Table）是一种通过**键**直接访问存储位置的数据结构，利用**哈希函数**将键映射到数组下标。理想情况下，查找、插入、删除操作的平均时间复杂度为 **O(1)**。

### 核心组件

1. **哈希函数**: 将任意大小的键映射为固定范围的整数
2. **数组**: 存储数据的实际容器
3. **冲突解决**: 处理不同键映射到同一位置的情况

## 哈希函数

好的哈希函数应满足：
- **确定性**: 相同的键必须产生相同的哈希值
- **均匀性**: 键应均匀分布在整个哈希表中
- **高效性**: 计算应快速

### 常见哈希方法

```python
# 1. 除法哈希法
def hash_div(key, table_size):
    return key % table_size

# 2. 乘法哈希法
def hash_mul(key, table_size):
    A = (5 ** 0.5 - 1) / 2  # 黄金分割比
    return int(table_size * ((key * A) % 1))

# 3. 字符串哈希
def hash_string(s, table_size):
    h = 0
    for c in s:
        h = (h * 31 + ord(c)) % table_size
    return h

# 4. Python 内置哈希
hash_value = hash("hello")  # 返回整数（但每次运行可能不同）
```

## 冲突解决

### 1. 链地址法 (Chaining)

每个桶中维护一个链表（或红黑树）。

```python
class HashTableChaining:
    def __init__(self, capacity=16):
        self.capacity = capacity
        self.size = 0
        self.table = [[] for _ in range(capacity)]
        self.load_factor = 0.75
    
    def _hash(self, key):
        return hash(key) % self.capacity
    
    def put(self, key, value):
        idx = self._hash(key)
        bucket = self.table[idx]
        
        for i, (k, v) in enumerate(bucket):
            if k == key:
                bucket[i] = (key, value)
                return
        
        bucket.append((key, value))
        self.size += 1
        
        if self.size > self.capacity * self.load_factor:
            self._resize()
    
    def get(self, key):
        idx = self._hash(key)
        bucket = self.table[idx]
        
        for k, v in bucket:
            if k == key:
                return v
        
        raise KeyError(key)
    
    def remove(self, key):
        idx = self._hash(key)
        bucket = self.table[idx]
        
        for i, (k, v) in enumerate(bucket):
            if k == key:
                bucket.pop(i)
                self.size -= 1
                return
        
        raise KeyError(key)
    
    def _resize(self):
        """扩容 2 倍并 rehash"""
        old_table = self.table
        self.capacity *= 2
        self.table = [[] for _ in range(self.capacity)]
        self.size = 0
        
        for bucket in old_table:
            for key, value in bucket:
                self.put(key, value)
```

### 2. 开放地址法 (Open Addressing)

当冲突发生时，在哈希表中寻找下一个空位。

```python
class HashTableOpenAddressing:
    def __init__(self, capacity=16):
        self.capacity = capacity
        self.table = [None] * capacity
        self.size = 0
        self.DELETED = object()  # 标记已删除
    
    def _hash(self, key):
        return hash(key) % self.capacity
    
    def _probe(self, key, i):
        """线性探测"""
        return (self._hash(key) + i) % self.capacity
    
    def put(self, key, value):
        for i in range(self.capacity):
            idx = self._probe(key, i)
            if self.table[idx] is None or self.table[idx] is self.DELETED:
                self.table[idx] = (key, value)
                self.size += 1
                return
            if self.table[idx][0] == key:
                self.table[idx] = (key, value)  # 更新
                return
        raise Exception("Hash table is full")
    
    def get(self, key):
        for i in range(self.capacity):
            idx = self._probe(key, i)
            if self.table[idx] is None:
                raise KeyError(key)
            if self.table[idx] is not self.DELETED and self.table[idx][0] == key:
                return self.table[idx][1]
        raise KeyError(key)
    
    def remove(self, key):
        for i in range(self.capacity):
            idx = self._probe(key, i)
            if self.table[idx] is None:
                raise KeyError(key)
            if self.table[idx] is not self.DELETED and self.table[idx][0] == key:
                self.table[idx] = self.DELETED
                self.size -= 1
                return
```

### 3. 双重哈希 (Double Hashing)

使用两个哈希函数，当冲突时使用第二个哈希函数计算探测步长。

```python
def _double_hash(key, i, table_size):
    h1 = hash(key) % table_size
    h2 = 1 + (hash(key) % (table_size - 1))  # 确保步长不为 0
    return (h1 + i * h2) % table_size
```

### 冲突解决对比

| 方法 | 优点 | 缺点 |
|-----|------|------|
| 链地址法 | 实现简单，支持任意多元素 | 额外指针空间，缓存不友好 |
| 线性探测 | 缓存友好 | 聚集问题影响性能 |
| 双重哈希 | 分布均匀 | 计算开销稍大 |

## 负载因子与重哈希 (Rehashing)

$$ \alpha = \frac{n}{m} $$

其中 $n$ 为已存元素数，$m$ 为哈希表总容量。

### 哈希碰撞概率

若哈希函数均匀分布，链表法中平均查找长度：

- **成功查找**：$1 + \frac{\alpha}{2}$
- **不成功查找**：$\alpha$

**生日悖论**：哈希值范围 $H$，插入 $k$ 个元素后至少一次碰撞的概率：

$$ P(\text{collision}) \approx 1 - e^{-k(k-1)/(2H)} $$

当 $k \approx \sqrt{2H}$ 时，碰撞概率超过 50%。

当负载因子超过阈值（通常 0.75）时，触发**扩容**：新建 2 倍大小的表，重新计算所有键的哈希位置。

```python
def _resize(self):
    old_table = self.table
    self.capacity *= 2
    self.table = [None] * self.capacity
    self.size = 0
    
    for entry in old_table:
        if entry is not None and entry is not self.DELETED:
            self.put(entry[0], entry[1])
```

## 哈希集合 (HashSet)

```python
class HashSet:
    def __init__(self):
        self.capacity = 16
        self.table = [[] for _ in range(self.capacity)]
        self.size = 0
    
    def add(self, key):
        idx = hash(key) % self.capacity
        if key not in self.table[idx]:
            self.table[idx].append(key)
            self.size += 1
    
    def remove(self, key):
        idx = hash(key) % self.capacity
        try:
            self.table[idx].remove(key)
            self.size -= 1
        except ValueError:
            pass
    
    def contains(self, key):
        idx = hash(key) % self.capacity
        return key in self.table[idx]
```

## Python dict 内部原理

Python 的 dict 是高度优化的哈希表。CPython 3.6+ 使用**紧凑表示法**（compact dict），保持插入顺序。

### 关键实现细节

1. **哈希值范围**: Python 的 hash() 返回 64 位整数（-2⁶³ 到 2⁶³-1）
2. **初始大小**: PyDict_MINSIZE = 8
3. **扩容时机**: 当 2/3 满时扩容，每次扩容 2x-4x
4. **冲突解决**: 伪随机探测（基于哈希值高位计算探测步长）
5. **紧凑存储**: 分离索引数组和条目数组

```python
# 实际使用
d = {}
d["key"] = "value"        # set
val = d["key"]            # get → O(1)
del d["key"]              # delete → O(1)
"key" in d                # contains → O(1)

# 常用方法
d.keys()
d.values()
d.items()
d.get("key", default)
d.setdefault("key", default)
d.update({"a": 1, "b": 2})
```

## 时间复杂度

| 操作 | 平均 | 最差 |
|-----|------|------|
| 插入 | O(1) | O(n) |
| 删除 | O(1) | O(n) |
| 查找 | O(1) | O(n) |
| 更新 | O(1) | O(n) |

**最差情况**：所有键哈希到同一位置（哈希碰撞攻击）。

## 常见应用

### 1. 计数

```python
from collections import Counter

# 频率统计
counter = Counter("hello world")
print(counter['l'])  # 3

# 手动实现
def count_chars(s):
    freq = {}
    for c in s:
        freq[c] = freq.get(c, 0) + 1
    return freq
```

### 2. 缓存 (Memoization)

```python
from functools import lru_cache

@lru_cache(maxsize=128)
def fibonacci(n):
    if n < 2:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

# 手动缓存
def memoize(f):
    cache = {}
    def wrapper(*args):
        if args not in cache:
            cache[args] = f(*args)
        return cache[args]
    return wrapper
```

### 3. 两数之和 (LeetCode 1)

```python
def two_sum(nums, target):
    seen = {}
    for i, num in enumerate(nums):
        complement = target - num
        if complement in seen:
            return [seen[complement], i]
        seen[num] = i
    return []
```

### 4. 最长连续序列 (LeetCode 128)

```python
def longest_consecutive(nums):
    """最长连续序列 O(n)"""
    num_set = set(nums)
    longest = 0
    
    for num in num_set:
        if num - 1 not in num_set:  # 只从序列起点开始
            curr = num
            length = 1
            while curr + 1 in num_set:
                curr += 1
                length += 1
            longest = max(longest, length)
    
    return longest
```

## 哈希表 vs 其他数据结构

| 数据结构 | 查找 | 插入 | 删除 | 有序 |
|---------|------|------|------|------|
| 哈希表 | O(1)* | O(1)* | O(1)* | ❌ 无序 |
| 二分搜索树 (BST) | O(log n) | O(log n) | O(log n) | ✅ |
| 有序数组 | O(log n) | O(n) | O(n) | ✅ |
| 链表 | O(n) | O(1) | O(1) | ✅ |

* 平均时间复杂度

## 练习

| 题目 | 难度 | 核心技巧 |
|------|------|---------|
| LeetCode 1. 两数之和 | 🟢 简单 | 哈希表 |
| LeetCode 217. 存在重复元素 | 🟢 简单 | 哈希集合 |
| LeetCode 242. 有效字母异位词 | 🟢 简单 | 计数 |
| LeetCode 349. 两个数组交集 | 🟢 简单 | 哈希集合 |
| LeetCode 3. 无重复字符最长子串 | 🟡 中等 | 滑动窗口+哈希 |
| LeetCode 49. 字母异位词分组 | 🟡 中等 | 排序+哈希 |
| LeetCode 128. 最长连续序列 | 🟡 中等 | 哈希集合 |
| LeetCode 146. LRU 缓存 | 🟡 中等 | 哈希+双向链表 |
| LeetCode 380. O(1) 时间插入删除和随机 | 🟡 中等 | 哈希+数组 |
| LeetCode 560. 和为 K 的子数组 | 🟡 中等 | 前缀和+哈希 |

## 相关条目

- [[Array]]
- [[LinkedList]]
- [[Trie]]
- [[BinarySearchTree]]
- [[Sorting]]
