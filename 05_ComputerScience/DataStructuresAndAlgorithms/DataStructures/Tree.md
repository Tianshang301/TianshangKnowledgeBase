---
aliases: [Tree]
tags: ['DataStructuresAndAlgorithms', 'DataStructures', 'Tree']
created: 2026-05-16
updated: 2026-05-13
---

# 树基础

## 基本概念

树（Tree）是一种**分层**（hierarchical）的非线性数据结构。

### 术语

| 术语 | 英文 | 描述 |
|------|------|------|
| 根节点 | Root | 没有父节点的节点 |
| 叶子节点 | Leaf | 没有子节点的节点 |
| 父节点 | Parent | 某个节点的直接前驱 |
| 子节点 | Child | 某个节点的直接后继 |
| 兄弟节点 | Sibling | 同一父节点的子节点 |
| 深度 | Depth | 从根到该节点的边数 |
| 高度 | Height | 从该节点到最远叶子的边数 |
| 层数 | Level | 深度 + 1 |
| 子树 | Subtree | 节点及其所有后代 |

```
          1          ← 根节点 (depth=0, level=1)
        /   \
       2     3       ← 2 和 3 是兄弟
      / \   / \
     4   5 6   7     ← 叶子节点 (depth=2, height=1)
```

- 节点 1 的高度 = 2（到叶子节点 4/5/6/7 的最长路径）
- 节点 2 的高度 = 1
- 叶子节点的高度 = 0

### 二叉树的性质

- 第 $i$ 层最多有 $2^{i-1}$ 个节点（$i \geq 1$）
- 深度为 $h$ 的二叉树最多有 $2^h - 1$ 个节点
- 叶节点数 = 度为 2 的节点数 + 1
- **遍历复杂度**：$O(n)$，其中 $n$ 为节点数

### 特殊二叉树

| 类型 | 定义 |
|------|------|
| 满二叉树 | 所有层都被填满 |
| 完全二叉树 | 除最后一层外全满，最后一层左对齐 |
| 平衡二叉树 | 左右子树高度差 ≤ 1 |
| 斜树 | 所有节点只有左/右子树 |

## 二叉树的实现

```python
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right
```

### 构建二叉树

```python
def build_tree_from_list(values):
    """从层序遍历列表构建二叉树（None 表示空节点）"""
    if not values:
        return None
    
    root = TreeNode(values[0])
    queue = deque([root])
    i = 1
    
    while queue and i < len(values):
        node = queue.popleft()
        
        if i < len(values) and values[i] is not None:
            node.left = TreeNode(values[i])
            queue.append(node.left)
        i += 1
        
        if i < len(values) and values[i] is not None:
            node.right = TreeNode(values[i])
            queue.append(node.right)
        i += 1
    
    return root
```

## 树的遍历

### 深度优先遍历 (DFS)

#### 前序遍历 (Pre-order): 根 → 左 → 右

```python
# 递归
def preorder_recursive(root):
    if not root:
        return []
    return [root.val] + preorder_recursive(root.left) + preorder_recursive(root.right)

# 迭代
def preorder_iterative(root):
    if not root:
        return []
    result = []
    stack = [root]
    while stack:
        node = stack.pop()
        result.append(node.val)
        if node.right:
            stack.append(node.right)
        if node.left:
            stack.append(node.left)
    return result
```

#### 中序遍历 (In-order): 左 → 根 → 右

```python
# 递归
def inorder_recursive(root):
    if not root:
        return []
    return inorder_recursive(root.left) + [root.val] + inorder_recursive(root.right)

# 迭代
def inorder_iterative(root):
    result = []
    stack = []
    curr = root
    while stack or curr:
        while curr:
            stack.append(curr)
            curr = curr.left
        curr = stack.pop()
        result.append(curr.val)
        curr = curr.right
    return result
```

#### 后序遍历 (Post-order): 左 → 右 → 根

```python
# 递归
def postorder_recursive(root):
    if not root:
        return []
    return postorder_recursive(root.left) + postorder_recursive(root.right) + [root.val]

# 迭代（双栈法）
def postorder_iterative(root):
    if not root:
        return []
    result = []
    stack = [root]
    while stack:
        node = stack.pop()
        result.append(node.val)
        if node.left:
            stack.append(node.left)
        if node.right:
            stack.append(node.right)
    return result[::-1]  # 反转 根-右-左 → 左-右-根
```

### 广度优先遍历 (BFS)

#### 层序遍历 (Level-order)

```python
from collections import deque

def level_order(root):
    """层序遍历（逐层）"""
    if not root:
        return []
    
    result = []
    queue = deque([root])
    
    while queue:
        level_size = len(queue)
        level = []
        
        for _ in range(level_size):
            node = queue.popleft()
            level.append(node.val)
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
        
        result.append(level)
    
    return result
```

### 遍历方式总结

| 遍历方式 | 顺序 | 递归 | 迭代数据结构 | 典型应用 |
|---------|------|------|-------------|---------|
| 前序 | 根→左→右 | ✅ | 栈 | 序列化、复制树 |
| 中序 | 左→根→右 | ✅ | 栈 | BST 排序输出 |
| 后序 | 左→右→根 | ✅ | 栈 | 删除树、表达式求值 |
| 层序 | 逐层 | ❌ | 队列 | BFS、最短路径 |

## 常见操作

### 树的高度

```python
def max_depth(root):
    """二叉树的最大深度"""
    if not root:
        return 0
    return 1 + max(max_depth(root.left), max_depth(root.right))
```

时间复杂度: O(n), 空间: O(h) 递归栈

### 判断平衡二叉树 (LeetCode 110)

```python
def is_balanced(root):
    """判断二叉树是否高度平衡"""
    def check_height(node):
        if not node:
            return 0
        
        left = check_height(node.left)
        if left == -1:
            return -1
        
        right = check_height(node.right)
        if right == -1:
            return -1
        
        if abs(left - right) > 1:
            return -1
        
        return 1 + max(left, right)
    
    return check_height(root) != -1
```

### 二叉树的直径 (LeetCode 543)

```python
def diameter_of_binary_tree(root):
    """二叉树中任意两节点间最长路径长度"""
    diameter = 0
    
    def depth(node):
        nonlocal diameter
        if not node:
            return 0
        left = depth(node.left)
        right = depth(node.right)
        diameter = max(diameter, left + right)
        return 1 + max(left, right)
    
    depth(root)
    return diameter
```

### 路径总和 (LeetCode 112)

```python
def has_path_sum(root, target):
    """判断是否存在根到叶子的路径和等于 target"""
    if not root:
        return False
    if not root.left and not root.right:
        return root.val == target
    return has_path_sum(root.left, target - root.val) or \
           has_path_sum(root.right, target - root.val)
```

### 最近公共祖先 (LeetCode 236)

```python
def lowest_common_ancestor(root, p, q):
    """二叉树的最近公共祖先"""
    if not root or root == p or root == q:
        return root
    
    left = lowest_common_ancestor(root.left, p, q)
    right = lowest_common_ancestor(root.right, p, q)
    
    if left and right:
        return root
    return left or right
```

## 序列化与反序列化 (LeetCode 297)

```python
def serialize(root):
    """前序遍历序列化"""
    if not root:
        return "#"
    return f"{root.val},{serialize(root.left)},{serialize(root.right)}"

def deserialize(data):
    """反序列化"""
    def dfs(vals):
        val = next(vals)
        if val == "#":
            return None
        node = TreeNode(int(val))
        node.left = dfs(vals)
        node.right = dfs(vals)
        return node
    
    vals = iter(data.split(","))
    return dfs(vals)
```

## 经典问题

### 翻转二叉树 (LeetCode 226)

```python
def invert_tree(root):
    """翻转二叉树"""
    if not root:
        return None
    root.left, root.right = root.right, root.left
    invert_tree(root.left)
    invert_tree(root.right)
    return root
```

### 对称二叉树 (LeetCode 101)

```python
def is_symmetric(root):
    """判断二叉树是否对称"""
    def check(left, right):
        if not left and not right:
            return True
        if not left or not right:
            return False
        return left.val == right.val and \
               check(left.left, right.right) and \
               check(left.right, right.left)
    
    return check(root.left, root.right) if root else True
```

### N 叉树的前序遍历 (LeetCode 589)

```python
class NTreeNode:
    def __init__(self, val=0, children=None):
        self.val = val
        self.children = children if children is not None else []

def preorder_nary(root):
    """N 叉树前序遍历"""
    if not root:
        return []
    result = [root.val]
    for child in root.children:
        result.extend(preorder_nary(child))
    return result
```

## 练习

| 题目 | 难度 | 核心技巧 |
|------|------|---------|
| LeetCode 94. 二叉树中序遍历 | 🟢 简单 | 递归/迭代 |
| LeetCode 100. 相同的树 | 🟢 简单 | 递归 |
| LeetCode 101. 对称二叉树 | 🟢 简单 | 递归/迭代 |
| LeetCode 104. 二叉树最大深度 | 🟢 简单 | DFS |
| LeetCode 110. 平衡二叉树 | 🟢 简单 | 自底向上 |
| LeetCode 111. 二叉树最小深度 | 🟢 简单 | BFS |
| LeetCode 112. 路径总和 | 🟢 简单 | DFS |
| LeetCode 226. 翻转二叉树 | 🟢 简单 | 递归 |
| LeetCode 102. 层序遍历 | 🟡 中等 | BFS |
| LeetCode 105. 从前序中序构建二叉树 | 🟡 中等 | 递归分治 |
| LeetCode 236. 最近公共祖先 | 🟡 中等 | 递归 |
| LeetCode 297. 序列化与反序列化 | 🔴 困难 | 前序/层序 |
| LeetCode 543. 二叉树的直径 | 🟢 简单 | DFS |
| LeetCode 124. 二叉树最大路径和 | 🔴 困难 | DFS 后序 |

## 相关条目

- [[BinarySearchTree]]
- [[AVL]]
- [[Graph]]
- [[BFSDFS]]
- [[Heap]]
