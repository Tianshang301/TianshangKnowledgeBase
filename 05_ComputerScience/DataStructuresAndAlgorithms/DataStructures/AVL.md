---
aliases: [AVL]
tags: ['DataStructuresAndAlgorithms', 'DataStructures', 'AVL']
---

# AVL 平衡树

## 基本概念

AVL 树是**自平衡二叉搜索树**，由 Georgy Adelson-Velsky 和 Evgenii Landis 于 1962 年提出。AVL 树保证任意节点的左右子树高度差不超过 1。

### 平衡因子 (Balance Factor)

```
平衡因子 = 左子树高度 - 右子树高度
```

平衡因子取值范围：{-1, 0, 1}。若超出此范围，需要通过旋转恢复平衡。

## AVL 树节点

```python
class AVLNode:
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None
        self.height = 1  # 叶子节点高度为 1
```

## 辅助函数

```python
def get_height(node):
    return node.height if node else 0

def get_balance(node):
    """计算平衡因子"""
    return get_height(node.left) - get_height(node.right) if node else 0

def update_height(node):
    """更新节点高度"""
    node.height = 1 + max(get_height(node.left), get_height(node.right))
```

## 旋转操作

### 1. 右旋 (LL - Left-Left)

```
      y                 x
     / \               / \
    x   T3    →       T1  y
   / \                   / \
  T1  T2                T2  T3
```

适用场景：在左子树的左子节点插入导致不平衡。

```python
def right_rotate(y):
    """右旋"""
    x = y.left
    T2 = x.right
    
    # 旋转
    x.right = y
    y.left = T2
    
    # 更新高度
    update_height(y)
    update_height(x)
    
    return x
```

### 2. 左旋 (RR - Right-Right)

```
    x                     y
   / \                   / \
  T1  y       →         x   T3
     / \               / \
    T2  T3            T1  T2
```

适用场景：在右子树的右子节点插入导致不平衡。

```python
def left_rotate(x):
    """左旋"""
    y = x.right
    T2 = y.left
    
    # 旋转
    y.left = x
    x.right = T2
    
    # 更新高度
    update_height(x)
    update_height(y)
    
    return y
```

### 3. 左右旋 (LR - Left-Right)

```
    z                   z                   x
   / \                 / \                 / \
  y   T4    →         x   T4    →         y   z
 / \                 / \                 / \ / \
T1  x               y   T3              T1 T2T3 T4
   / \             / \
  T2  T3          T1  T2
```

适用场景：在左子树的右子节点插入导致不平衡。先左旋再右旋。

```python
def left_right_rotate(z):
    """左右旋"""
    z.left = left_rotate(z.left)
    return right_rotate(z)
```

### 4. 右左旋 (RL - Right-Left)

```
  z                   z                     x
 / \                 / \                   / \
T1  y       →       T1  x        →        z   y
   / \                 / \               / \ / \
  x   T4              T2  y             T1 T2T3 T4
 / \                       / \
T2  T3                    T3  T4
```

适用场景：在右子树的左子节点插入导致不平衡。先右旋再左旋。

```python
def right_left_rotate(z):
    """右左旋"""
    z.right = right_rotate(z.right)
    return left_rotate(z)
```

## 插入操作

```python
def insert(node, val):
    """AVL 树插入"""
    # 1. 标准 BST 插入
    if not node:
        return AVLNode(val)
    
    if val < node.val:
        node.left = insert(node.left, val)
    elif val > node.val:
        node.right = insert(node.right, val)
    else:
        return node  # 不插入重复值
    
    # 2. 更新高度
    update_height(node)
    
    # 3. 获取平衡因子，判断是否失衡
    balance = get_balance(node)
    
    # 4. 四种旋转情况
    # LL: 左-左
    if balance > 1 and val < node.left.val:
        return right_rotate(node)
    
    # RR: 右-右
    if balance < -1 and val > node.right.val:
        return left_rotate(node)
    
    # LR: 左-右
    if balance > 1 and val > node.left.val:
        return left_right_rotate(node)
    
    # RL: 右-左
    if balance < -1 and val < node.right.val:
        return right_left_rotate(node)
    
    return node
```

## 删除操作

```python
def delete(node, val):
    """AVL 树删除"""
    # 1. 标准 BST 删除
    if not node:
        return None
    
    if val < node.val:
        node.left = delete(node.left, val)
    elif val > node.val:
        node.right = delete(node.right, val)
    else:
        # 找到要删除的节点
        if not node.left:
            return node.right
        if not node.right:
            return node.left
        
        # 有两个子节点：找中序后继
        min_node = find_min(node.right)
        node.val = min_node.val
        node.right = delete(node.right, min_node.val)
    
    if not node:
        return None
    
    # 2. 更新高度
    update_height(node)
    
    # 3. 平衡调整
    balance = get_balance(node)
    
    # LL
    if balance > 1 and get_balance(node.left) >= 0:
        return right_rotate(node)
    
    # LR
    if balance > 1 and get_balance(node.left) < 0:
        return left_right_rotate(node)
    
    # RR
    if balance < -1 and get_balance(node.right) <= 0:
        return left_rotate(node)
    
    # RL
    if balance < -1 and get_balance(node.right) > 0:
        return right_left_rotate(node)
    
    return node

def find_min(node):
    while node.left:
        node = node.left
    return node
```

## 搜索

```python
def search(node, val):
    """AVL 搜索（同 BST）"""
    if not node or node.val == val:
        return node
    if val < node.val:
        return search(node.left, val)
    return search(node.right, val)
```

## 完整 AVL 树类

```python
class AVLTree:
    def __init__(self):
        self.root = None
    
    def insert(self, val):
        self.root = insert(self.root, val)
    
    def delete(self, val):
        self.root = delete(self.root, val)
    
    def search(self, val):
        return search(self.root, val)
    
    def inorder(self):
        result = []
        self._inorder(self.root, result)
        return result
    
    def _inorder(self, node, result):
        if node:
            self._inorder(node.left, result)
            result.append(node.val)
            self._inorder(node.right, result)
```

## 时间复杂度

| 操作 | 平均 | 最差 |
|-----|------|------|
| 搜索 | O(log n) | O(log n) |
| 插入 | O(log n) | O(log n) |
| 删除 | O(log n) | O(log n) |

## AVL 树 vs 红黑树

| 特性 | AVL 树 | 红黑树 |
|------|--------|--------|
| 平衡程度 | 严格平衡 (|BF| ≤ 1) | 近似平衡（黑高平衡） |
| 最大高度 | ≈ 1.44 log₂(n+2) | ≈ 2 log₂(n+1) |
| 搜索性能 | **更好**（更严格平衡） | 稍差 |
| 插入/删除 | 更多旋转（更频繁） | **更少旋转** |
| 额外存储 | height 或 BF | 颜色位（1 bit） |
| 实现复杂度 | 中等 | 较复杂 |
| 应用场景 | 查询密集型（数据库索引） | 通用（语言标准库、Linux 内核） |

### 如何选择？

- **查询频繁、插入删除少** → AVL 树（如数据库索引）
- **插入删除频繁** → 红黑树（如 C++ STL map/set, Java TreeMap, Linux 完全公平调度器）
- **快速实现简单平衡** → Treap 或替罪羊树

## 练习

| 题目 | 知识点 |
|------|--------|
| 实现 AVL 树的插入和删除 | 四种旋转 |
| 判断一棵树是否为 AVL 树 | 平衡因子检查 |
| 使用 AVL 树实现排序 | 中序遍历 = O(n) |
| 在 AVL 树中找第 K 小元素 | 维护子树大小 |
| 区间树 (Interval Tree) | AVL + 区间信息 |

## 相关条目

- [[BinarySearchTree]]
- [[Tree]]
- [[SegmentTree]]
- [[Heap]]
- [[HashTable]]
