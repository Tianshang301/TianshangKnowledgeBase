# 二叉搜索树 BST

## 基本概念

二叉搜索树（Binary Search Tree, BST）是一种特殊的二叉树，满足以下性质：

1. **左子树**中所有节点的值 < 根节点的值
2. **右子树**中所有节点的值 > 根节点的值
3. 左右子树也分别是 BST

```
        8
       / \
      3   10
     / \    \
    1   6    14
       / \   /
      4   7 13
```

## 时间复杂度

| 操作 | 平均 | 最差（斜树） |
|-----|------|-------------|
| 搜索 (Search) | O(log n) | O(n) |
| 插入 (Insert) | O(log n) | O(n) |
| 删除 (Delete) | O(log n) | O(n) |
| 中序遍历 | O(n) | O(n) |

## 实现

### 节点定义

```python
class TreeNode:
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None
```

### BST 类

```python
class BST:
    def __init__(self):
        self.root = None
    
    def search(self, val):
        """搜索值"""
        return self._search(self.root, val)
    
    def _search(self, node, val):
        if not node or node.val == val:
            return node
        if val < node.val:
            return self._search(node.left, val)
        return self._search(node.right, val)
    
    def insert(self, val):
        """插入值"""
        self.root = self._insert(self.root, val)
    
    def _insert(self, node, val):
        if not node:
            return TreeNode(val)
        if val < node.val:
            node.left = self._insert(node.left, val)
        elif val > node.val:
            node.right = self._insert(node.right, val)
        # 不插入重复值
        return node
    
    def delete(self, val):
        """删除值"""
        self.root = self._delete(self.root, val)
    
    def _delete(self, node, val):
        if not node:
            return None
        
        if val < node.val:
            node.left = self._delete(node.left, val)
        elif val > node.val:
            node.right = self._delete(node.right, val)
        else:
            # 找到要删除的节点
            if not node.left:
                return node.right
            if not node.right:
                return node.left
            
            # 有两个子节点：找右子树最小节点（后继）
            min_node = self._find_min(node.right)
            node.val = min_node.val
            node.right = self._delete(node.right, min_node.val)
        
        return node
    
    def _find_min(self, node):
        while node.left:
            node = node.left
        return node
    
    def inorder(self):
        """中序遍历（得到有序序列）"""
        result = []
        self._inorder(self.root, result)
        return result
    
    def _inorder(self, node, result):
        if node:
            self._inorder(node.left, result)
            result.append(node.val)
            self._inorder(node.right, result)
```

### 迭代搜索

```python
def search_iterative(root, val):
    """迭代搜索 BST"""
    curr = root
    while curr:
        if val == curr.val:
            return curr
        elif val < curr.val:
            curr = curr.left
        else:
            curr = curr.right
    return None

def insert_iterative(root, val):
    """迭代插入"""
    if not root:
        return TreeNode(val)
    
    curr = root
    while True:
        if val < curr.val:
            if not curr.left:
                curr.left = TreeNode(val)
                break
            curr = curr.left
        else:
            if not curr.right:
                curr.right = TreeNode(val)
                break
            curr = curr.right
    return root
```

## BST 的验证 (LeetCode 98)

利用中序遍历为递增序列，或递归传值域范围。

```python
def is_valid_bst(root):
    """验证二叉搜索树（传递上下界）"""
    def validate(node, min_val, max_val):
        if not node:
            return True
        if node.val <= min_val or node.val >= max_val:
            return False
        return validate(node.left, min_val, node.val) and \
               validate(node.right, node.val, max_val)
    
    return validate(root, float('-inf'), float('inf'))

def is_valid_bst_inorder(root):
    """利用中序遍历验证"""
    prev = float('-inf')
    stack = []
    curr = root
    
    while stack or curr:
        while curr:
            stack.append(curr)
            curr = curr.left
        curr = stack.pop()
        if curr.val <= prev:
            return False
        prev = curr.val
        curr = curr.right
    
    return True
```

## 第 K 小的元素 (LeetCode 230)

```python
def kth_smallest(root, k):
    """BST 中第 K 小的元素（中序遍历）"""
    stack = []
    curr = root
    
    while stack or curr:
        while curr:
            stack.append(curr)
            curr = curr.left
        curr = stack.pop()
        k -= 1
        if k == 0:
            return curr.val
        curr = curr.right
    
    return -1
```

- 时间复杂度: O(H + k), H 为树高
- 空间复杂度: O(H)

## 将有序数组转换为 BST (LeetCode 108)

```python
def sorted_array_to_bst(nums):
    """将升序数组转换为高度平衡的 BST"""
    def build(left, right):
        if left > right:
            return None
        mid = (left + right) // 2
        node = TreeNode(nums[mid])
        node.left = build(left, mid - 1)
        node.right = build(mid + 1, right)
        return node
    
    return build(0, len(nums) - 1)
```

- 时间复杂度: O(n)
- 空间复杂度: O(log n) 递归栈

## 最近公共祖先 (LeetCode 235)

利用 BST 的特性：如果 p 和 q 在 root 的两侧，则 root 为 LCA。

```python
def lowest_common_ancestor(root, p, q):
    """BST 的最近公共祖先"""
    while root:
        if p.val < root.val and q.val < root.val:
            root = root.left
        elif p.val > root.val and q.val > root.val:
            root = root.right
        else:
            return root
    return None
```

- 时间复杂度: O(h)
- 空间复杂度: O(1)

## 前驱与后继

```python
def predecessor(root, val):
    """查找 val 的前驱（小于 val 的最大值）"""
    pred = None
    curr = root
    while curr:
        if curr.val < val:
            pred = curr
            curr = curr.right
        else:
            curr = curr.left
    return pred

def successor(root, val):
    """查找 val 的后继（大于 val 的最小值）"""
    succ = None
    curr = root
    while curr:
        if curr.val > val:
            succ = curr
            curr = curr.left
        else:
            curr = curr.right
    return succ
```

## BST 与其他树结构的对比

| 特性 | BST (不平衡) | AVL 树 | 红黑树 |
|-----|-------------|--------|--------|
| 高度 | O(n) 最差 | O(log n) 严格 | O(log n) 近似 |
| 插入/删除 | O(h) | O(log n) | O(log n) |
| 平衡机制 | 无 | 严格平衡因子 | 颜色约束 |
| 应用场景 | 教学 | 查询密集型 | 通用，语言标准库 |
| 额外空间 | O(1) | O(log n) 旋转 | O(log n) 旋转 |

## 经典问题

### 二叉搜索树的最近公共祖先 (LeetCode 235)

已在上文给出。

### 不同的二叉搜索树 (LeetCode 96)

```python
def num_trees(n):
    """计算 1...n 能构成多少个不同的 BST（卡特兰数）"""
    dp = [0] * (n + 1)
    dp[0] = dp[1] = 1
    
    for i in range(2, n + 1):
        for j in range(1, i + 1):
            dp[i] += dp[j - 1] * dp[i - j]
    
    return dp[n]
```

### 二叉搜索树迭代器 (LeetCode 173)

```python
class BSTIterator:
    def __init__(self, root):
        self.stack = []
        self._leftmost_inorder(root)
    
    def _leftmost_inorder(self, node):
        while node:
            self.stack.append(node)
            node = node.left
    
    def next(self):
        """返回下一个最小的数"""
        node = self.stack.pop()
        if node.right:
            self._leftmost_inorder(node.right)
        return node.val
    
    def has_next(self):
        return len(self.stack) > 0
```

## 练习

| 题目 | 难度 | 核心技巧 |
|------|------|---------|
| LeetCode 98. 验证二叉搜索树 | 🟡 中等 | 中序/区间法 |
| LeetCode 700. BST 搜索 | 🟢 简单 | 迭代/递归 |
| LeetCode 701. BST 插入 | 🟡 中等 | 迭代/递归 |
| LeetCode 450. 删除 BST 节点 | 🟡 中等 | 分类讨论 |
| LeetCode 230. 第 K 小的元素 | 🟡 中等 | 中序遍历 |
| LeetCode 108. 有序数组转 BST | 🟢 简单 | 二分递归 |
| LeetCode 235. BST 的 LCA | 🟢 简单 | BST 特性 |
| LeetCode 173. BST 迭代器 | 🟡 中等 | 栈模拟中序 |
| LeetCode 96. 不同的 BST | 🟡 中等 | DP/卡特兰数 |
| LeetCode 99. 恢复 BST | 🟡 中等 | Morris 遍历 |
| LeetCode 538. 转累加树 | 🟡 中等 | 逆中序 |

## 相关条目

- [[AVL]]
- [[Tree]]
- [[Heap]]
- [[Graph]]
- [[Sorting]]
