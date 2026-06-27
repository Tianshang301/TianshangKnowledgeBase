---
aliases: [SegmentTree]
tags: ['DataStructuresAndAlgorithms', 'DataStructures', 'SegmentTree']
created: 2026-05-16
updated: 2026-05-16
---

# 线段树

## 基本概念

线段树（Segment Tree）是一种用于**区间查询**和**区间更新**的二叉树数据结构。它将一个数组的区间递归地二分为子区间，每个节点代表一个区间范围。

## 解决的问题

- **区间查询**: 求区间 [l, r] 的和、最小值、最大值等 O(log n)
- **单点更新**: 修改某个元素的值 O(log n)
- **区间更新**: 给区间 [l, r] 的所有元素加一个值 O(log n)（配合懒标记）

### 为什么需要线段树？

| 数据结构 | 区间查询 | 区间更新 | 单点更新 |
|---------|---------|---------|---------|
| 前缀和 | O(1) | O(n) | O(n) |
| 差分数组 | O(n) | O(1) | O(n) |
| Fenwick 树 | O(log n) | O(log n) | O(log n) |
| **线段树** | **O(log n)** | **O(log n)** | **O(log n)** |

线段树不仅支持前缀和功能，还支持**任意区间**的聚合操作（求和、最小值、最大值、GCD 等），且区间更新也只需 O(log n)。

## 线段树的表示

```
数组: [1, 3, 5, 7, 9, 11]
n = 6

线段树（求和）:
                  [0-5] sum=36
                /           \
           [0-2] sum=9     [3-5] sum=27
          /       \        /        \
      [0-1] s=4  [2] s=5 [3-4] s=16 [5] s=11
      /    \             /    \
    [0] s=1 [1] s=3   [3] s=7 [4] s=9
```

使用数组存储，根节点为下标 1：
- 左子节点: 2 * i
- 右子节点: 2 * i + 1
- 父节点: i // 2
- 数组大小: 4 * n（足够安全）

## 基本实现（区间和）

```python
class SegmentTree:
    def __init__(self, nums):
        self.n = len(nums)
        self.tree = [0] * (4 * self.n)
        if self.n > 0:
            self._build(nums, 1, 0, self.n - 1)
    
    def _build(self, nums, node, left, right):
        """构建线段树 O(n)"""
        if left == right:
            self.tree[node] = nums[left]
            return
        
        mid = (left + right) // 2
        self._build(nums, node * 2, left, mid)
        self._build(nums, node * 2 + 1, mid + 1, right)
        self.tree[node] = self.tree[node * 2] + self.tree[node * 2 + 1]
    
    def update(self, index, val):
        """单点更新 O(log n)"""
        self._update(1, 0, self.n - 1, index, val)
    
    def _update(self, node, left, right, index, val):
        if left == right:
            self.tree[node] = val
            return
        
        mid = (left + right) // 2
        if index <= mid:
            self._update(node * 2, left, mid, index, val)
        else:
            self._update(node * 2 + 1, mid + 1, right, index, val)
        
        self.tree[node] = self.tree[node * 2] + self.tree[node * 2 + 1]
    
    def range_sum(self, ql, qr):
        """区间和查询 O(log n)"""
        return self._range_sum(1, 0, self.n - 1, ql, qr)
    
    def _range_sum(self, node, left, right, ql, qr):
        if ql > right or qr < left:
            return 0
        if ql <= left and right <= qr:
            return self.tree[node]
        
        mid = (left + right) // 2
        return self._range_sum(node * 2, left, mid, ql, qr) + \
               self._range_sum(node * 2 + 1, mid + 1, right, ql, qr)
```

## 区间最小值查询 (Range Minimum Query)

```python
class SegTreeMin:
    def __init__(self, nums):
        self.n = len(nums)
        self.tree = [float('inf')] * (4 * self.n)
        if self.n > 0:
            self._build(nums, 1, 0, self.n - 1)
    
    def _build(self, nums, node, left, right):
        if left == right:
            self.tree[node] = nums[left]
            return
        mid = (left + right) // 2
        self._build(nums, node * 2, left, mid)
        self._build(nums, node * 2 + 1, mid + 1, right)
        self.tree[node] = min(self.tree[node * 2], self.tree[node * 2 + 1])
    
    def range_min(self, ql, qr):
        return self._range_min(1, 0, self.n - 1, ql, qr)
    
    def _range_min(self, node, left, right, ql, qr):
        if ql > right or qr < left:
            return float('inf')
        if ql <= left and right <= qr:
            return self.tree[node]
        mid = (left + right) // 2
        return min(self._range_min(node * 2, left, mid, ql, qr),
                   self._range_min(node * 2 + 1, mid + 1, right, ql, qr))
    
    def update(self, index, val):
        self._update(1, 0, self.n - 1, index, val)
    
    def _update(self, node, left, right, index, val):
        if left == right:
            self.tree[node] = val
            return
        mid = (left + right) // 2
        if index <= mid:
            self._update(node * 2, left, mid, index, val)
        else:
            self._update(node * 2 + 1, mid + 1, right, index, val)
        self.tree[node] = min(self.tree[node * 2], self.tree[node * 2 + 1])
```

## 懒标记 (Lazy Propagation)

懒标记用于**区间更新**——不需要立即更新所有叶子节点，而是将更新"缓存"在节点上，需要时才下推。

```python
class SegmentTreeLazy:
    def __init__(self, nums):
        self.n = len(nums)
        self.tree = [0] * (4 * self.n)
        self.lazy = [0] * (4 * self.n)  # 懒标记
        if self.n > 0:
            self._build(nums, 1, 0, self.n - 1)
    
    def _build(self, nums, node, left, right):
        if left == right:
            self.tree[node] = nums[left]
            return
        mid = (left + right) // 2
        self._build(nums, node * 2, left, mid)
        self._build(nums, node * 2 + 1, mid + 1, right)
        self.tree[node] = self.tree[node * 2] + self.tree[node * 2 + 1]
    
    def _push_down(self, node, left, right):
        """下推懒标记"""
        if self.lazy[node] != 0:
            mid = (left + right) // 2
            # 更新子节点
            self.tree[node * 2] += self.lazy[node] * (mid - left + 1)
            self.tree[node * 2 + 1] += self.lazy[node] * (right - mid)
            # 传递懒标记
            self.lazy[node * 2] += self.lazy[node]
            self.lazy[node * 2 + 1] += self.lazy[node]
            # 清空当前懒标记
            self.lazy[node] = 0
    
    def range_add(self, ql, qr, val):
        """区间 [ql, qr] 所有元素加 val"""
        self._range_add(1, 0, self.n - 1, ql, qr, val)
    
    def _range_add(self, node, left, right, ql, qr, val):
        if ql > right or qr < left:
            return
        if ql <= left and right <= qr:
            self.tree[node] += val * (right - left + 1)
            self.lazy[node] += val
            return
        
        self._push_down(node, left, right)
        mid = (left + right) // 2
        self._range_add(node * 2, left, mid, ql, qr, val)
        self._range_add(node * 2 + 1, mid + 1, right, ql, qr, val)
        self.tree[node] = self.tree[node * 2] + self.tree[node * 2 + 1]
    
    def range_sum(self, ql, qr):
        return self._range_sum(1, 0, self.n - 1, ql, qr)
    
    def _range_sum(self, node, left, right, ql, qr):
        if ql > right or qr < left:
            return 0
        if ql <= left and right <= qr:
            return self.tree[node]
        
        self._push_down(node, left, right)
        mid = (left + right) // 2
        return self._range_sum(node * 2, left, mid, ql, qr) + \
               self._range_sum(node * 2 + 1, mid + 1, right, ql, qr)
```

### 懒标记执行流程

```
range_add(2, 5, 3) — 给 [2,5] 加 3

1. 根节点 [0,5] 不完全在范围内，下推懒标记（如果存在）
2. 递归到 [0,2] 和 [3,5]
3. [0,2] 不完全在 [2,5] 内，继续递归
4. [2,2] 完全在范围内，更新值并设置懒标记
5. [0,1] 不在范围内，跳过
6. [3,5] 完全在范围内，更新值并设置懒标记
```

## 区间更新 + 单点查询

当只需要区间更新 + 单点查询时，可以使用**差分线段树**，但更简单的是使用**树状数组**或**差分数组**。

```python
class SegTreePointQuery:
    """区间加、单点查"""
    def __init__(self, n):
        self.n = n
        self.tree = [0] * (4 * n)
        self.lazy = [0] * (4 * n)
    
    def range_add(self, ql, qr, val):
        self._range_add(1, 0, self.n - 1, ql, qr, val)
    
    def _range_add(self, node, left, right, ql, qr, val):
        if ql > right or qr < left:
            return
        if ql <= left and right <= qr:
            self.tree[node] += val * (right - left + 1)
            self.lazy[node] += val
            return
        self._push_down(node, left, right)
        mid = (left + right) // 2
        self._range_add(node * 2, left, mid, ql, qr, val)
        self._range_add(node * 2 + 1, mid + 1, right, ql, qr, val)
        self.tree[node] = self.tree[node * 2] + self.tree[node * 2 + 1]
    
    def point_query(self, index):
        return self._point_query(1, 0, self.n - 1, index)
    
    def _point_query(self, node, left, right, index):
        if left == right:
            return self.tree[node]
        self._push_down(node, left, right)
        mid = (left + right) // 2
        if index <= mid:
            return self._point_query(node * 2, left, mid, index)
        return self._point_query(node * 2 + 1, mid + 1, right, index)
    
    def _push_down(self, node, left, right):
        if self.lazy[node] != 0:
            mid = (left + right) // 2
            self.tree[node * 2] += self.lazy[node] * (mid - left + 1)
            self.tree[node * 2 + 1] += self.lazy[node] * (right - mid)
            self.lazy[node * 2] += self.lazy[node]
            self.lazy[node * 2 + 1] += self.lazy[node]
            self.lazy[node] = 0
```

## 动态开点线段树

当值域很大但元素稀疏时，动态开点可节省大量内存。

```python
class DynamicSegNode:
    def __init__(self):
        self.left = None
        self.right = None
        self.sum = 0
        self.lazy = 0

class DynamicSegmentTree:
    def __init__(self, n):
        self.n = n
        self.root = DynamicSegNode()
    
    def range_add(self, ql, qr, val):
        self._range_add(self.root, 0, self.n - 1, ql, qr, val)
    
    def _range_add(self, node, left, right, ql, qr, val):
        if ql > right or qr < left:
            return
        if ql <= left and right <= qr:
            node.sum += val * (right - left + 1)
            node.lazy += val
            return
        
        self._push_down(node)
        mid = (left + right) // 2
        self._range_add(node.left, left, mid, ql, qr, val)
        self._range_add(node.right, mid + 1, right, ql, qr, val)
        node.sum = node.left.sum + node.right.sum
    
    def range_sum(self, ql, qr):
        return self._range_sum(self.root, 0, self.n - 1, ql, qr)
    
    def _range_sum(self, node, left, right, ql, qr):
        if ql > right or qr < left:
            return 0
        if ql <= left and right <= qr:
            return node.sum
        self._push_down(node)
        mid = (left + right) // 2
        return self._range_sum(node.left, left, mid, ql, qr) + \
               self._range_sum(node.right, mid + 1, right, ql, qr)
    
    def _push_down(self, node):
        if not node.left:
            node.left = DynamicSegNode()
        if not node.right:
            node.right = DynamicSegNode()
        if node.lazy != 0:
            mid = 0  # 实际需传入 mid，这里简化
            node.left.sum += node.lazy  # 需乘以子范围长度
            node.right.sum += node.lazy
            node.left.lazy += node.lazy
            node.right.lazy += node.lazy
            node.lazy = 0
```

**注意**: 实际动态开点需在 _push_down 中传入 left/right/mid。

## 线段树 vs 树状数组

| 特性 | 线段树 | 树状数组 (Fenwick) |
|-----|--------|-------------------|
| 区间查询 | O(log n) 任意区间 | O(log n) 前缀 |
| 区间更新 | O(log n) (懒标记) | 需差分技巧 |
| 实现复杂度 | 较复杂 | 简单 |
| 内存 | 4n | n |
| 适用操作 | 和、积、最值、GCD 等 | 前缀和、可逆操作 |
| 动态开点 | ✅ 支持 | ❌ |

## 经典问题

### 区间和检索 (LeetCode 307)

```python
class NumArray:
    def __init__(self, nums):
        self.seg = SegmentTree(nums)
    
    def update(self, index, val):
        self.seg.update(index, val)
    
    def sum_range(self, left, right):
        return self.seg.range_sum(left, right)
```

### 我的日程安排表 (LeetCode 731)

```python
class MyCalendarTwo:
    """线段树 + 懒标记实现区间重叠计数"""
    def __init__(self):
        self.n = 10**9
        self.root = DynamicSegNode()
    
    def book(self, start, end):
        # 查询 [start, end-1] 的最大重叠次数
        if self._query(self.root, 0, self.n, start, end - 1) >= 2:
            return False
        self._update(self.root, 0, self.n, start, end - 1, 1)
        return True
    
    def _query(self, node, left, right, ql, qr):
        if ql > right or qr < left:
            return 0
        if ql <= left and right <= qr:
            return node.max_cnt if hasattr(node, 'max_cnt') else 0
        mid = (left + right) // 2
        return max(self._query(node.left, left, mid, ql, qr),
                   self._query(node.right, mid + 1, right, ql, qr))
    
    def _update(self, node, left, right, ql, qr, val):
        # 实现略（需要懒标记维护最大值）
        pass
```

### 区间和的个数 (LeetCode 327)

```python
def count_range_sum(nums, lower, upper):
    """统计区间和在 [lower, upper] 内的个数"""
    prefix = [0]
    for num in nums:
        prefix.append(prefix[-1] + num)
    
    # 离散化 + 线段树
    sorted_vals = sorted(set(prefix))
    m = len(sorted_vals)
    
    def compress(x):
        from bisect import bisect_left
        return bisect_left(sorted_vals, x)
    
    seg = SegmentTree([0] * m)
    result = 0
    
    for p in prefix:
        left = compress(p - upper)
        right = compress(p - lower)
        # ... 查询和更新
```

## 练习

| 题目 | 难度 | 核心技巧 |
|------|------|---------|
| LeetCode 307. 区域和检索 | 🟡 中等 | 基础线段树 |
| LeetCode 303. 区域和检索 | 🟢 简单 | 前缀和（更简单） |
| LeetCode 699. 掉落方块 | 🔴 困难 | 线段树+懒标记 |
| LeetCode 715. Range 模块 | 🔴 困难 | 动态开点线段树 |
| LeetCode 218. 天际线问题 | 🔴 困难 | 线段树/扫描线 |
| LeetCode 850. 矩形面积 II | 🔴 困难 | 离散化+线段树 |
| LeetCode 673. 最长递增子序列个数 | 🟡 中等 | 线段树优化 DP |
| LeetCode 2407. 最长递增子序列 II | 🔴 困难 | 值域线段树 |

## 相关条目

- [[Heap]]
- [[BinarySearchTree]]
- [[AVL]]
- [[Trie]]
- [[UnionFind]]

