---
aliases: [LinkedList]
tags: ['DataStructuresAndAlgorithms', 'DataStructures', 'LinkedList']
created: 2026-05-16
updated: 2026-05-13
---

# 链表详解

## 基本概念

链表（LinkedList）是一种线性数据结构，元素通过指针链接，不需要连续内存。每个节点包含数据域和指针域。

## 链表类型

### 单向链表 (Singly Linked List)

```
head → [data|next] → [data|next] → [data|next] → None
```

```python
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

class SinglyLinkedList:
    def __init__(self):
        self.head = None
        self.size = 0
    
    def get(self, index):
        """获取第 index 个节点的值"""
        if index < 0 or index >= self.size:
            return -1
        curr = self.head
        for _ in range(index):
            curr = curr.next
        return curr.val
    
    def add_at_head(self, val):
        """头插法"""
        self.head = ListNode(val, self.head)
        self.size += 1
    
    def add_at_tail(self, val):
        """尾插法"""
        if not self.head:
            self.head = ListNode(val)
        else:
            curr = self.head
            while curr.next:
                curr = curr.next
            curr.next = ListNode(val)
        self.size += 1
    
    def add_at_index(self, index, val):
        """在指定位置插入"""
        if index < 0 or index > self.size:
            return
        if index == 0:
            self.add_at_head(val)
        else:
            prev = self.head
            for _ in range(index - 1):
                prev = prev.next
            prev.next = ListNode(val, prev.next)
            self.size += 1
    
    def delete_at_index(self, index):
        """删除指定位置节点"""
        if index < 0 or index >= self.size:
            return
        if index == 0:
            self.head = self.head.next
        else:
            prev = self.head
            for _ in range(index - 1):
                prev = prev.next
            prev.next = prev.next.next
        self.size -= 1
```

### 双向链表 (Doubly Linked List)

```
None ← [prev|data|next] ↔ [prev|data|next] ↔ [prev|data|next] → None
```

```python
class DListNode:
    def __init__(self, val=0, prev=None, next=None):
        self.val = val
        self.prev = prev
        self.next = next
```

优势：双向遍历，删除节点无需查找前驱。

### 循环链表 (Circular Linked List)

```
head → [data|next] → [data|next] → [data|next] → head
```

最后一个节点的 next 指向 head，适用于约瑟夫环问题。

## 时间复杂度

| 操作 | 单向链表 | 双向链表 |
|-----|---------|---------|
| 访问 (Access) | O(n) | O(n) |
| 搜索 (Search) | O(n) | O(n) |
| 头插/头删 | O(1) | O(1) |
| 尾插（无尾指针） | O(n) | O(1) |
| 尾插（有尾指针） | O(1) | O(1) |
| 中间插入 | O(n) | O(n) |
| 删除给定节点 | O(n) | O(1) |

## 核心技巧

### 1. 哑节点 (Dummy Node)

哑节点（哨兵节点）简化边界情况处理。

```python
def merge_two_lists(l1, l2):
    """合并两个有序链表"""
    dummy = ListNode(0)
    curr = dummy
    while l1 and l2:
        if l1.val < l2.val:
            curr.next = l1
            l1 = l1.next
        else:
            curr.next = l2
            l2 = l2.next
        curr = curr.next
    curr.next = l1 or l2
    return dummy.next
```

### 2. 快慢指针 (Fast & Slow Pointer)

```python
def middle_node(head):
    """返回链表中间节点（快慢指针法）"""
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
    return slow

def has_cycle(head):
    """检测链表是否有环（Floyd 判圈算法）"""
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow == fast:
            return True
    return False

def detect_cycle_start(head):
    """返回环的入口节点"""
    slow = fast = head
    has_cycle = False
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow == fast:
            has_cycle = True
            break
    if not has_cycle:
        return None
    # 头节点到环入口 = 相遇点到环入口
    slow = head
    while slow != fast:
        slow = slow.next
        fast = fast.next
    return slow
```

**Floyd 算法原理**：快指针每次走 2 步，慢指针每次走 1 步。若存在环，必在环内相遇。相遇后，将一个指针重置到 head，两者同速移动，再次相遇处即为环入口。

### 3. 反转链表

```python
def reverse_list(head):
    """迭代反转链表"""
    prev = None
    curr = head
    while curr:
        next_temp = curr.next
        curr.next = prev
        prev = curr
        curr = next_temp
    return prev

def reverse_list_recursive(head):
    """递归反转链表"""
    if not head or not head.next:
        return head
    new_head = reverse_list_recursive(head.next)
    head.next.next = head
    head.next = None
    return new_head
```

### 4. 删除节点

```python
def delete_node(node):
    """删除给定的节点（非尾节点），O(1)"""
    node.val = node.next.val
    node.next = node.next.next

def remove_nth_from_end(head, n):
    """删除倒数第 n 个节点"""
    dummy = ListNode(0, head)
    fast = slow = dummy
    # fast 先走 n+1 步
    for _ in range(n + 1):
        fast = fast.next
    while fast:
        slow = slow.next
        fast = fast.next
    slow.next = slow.next.next
    return dummy.next
```

## 经典问题

### LRU 缓存 (LeetCode 146)

使用**哈希表 + 双向链表**实现 O(1) 的 get 和 put。

```python
class LRUCache:
    def __init__(self, capacity):
        self.capacity = capacity
        self.cache = {}  # key -> node
        # 哨兵节点
        self.head = DListNode()
        self.tail = DListNode()
        self.head.next = self.tail
        self.tail.prev = self.head
    
    def _remove(self, node):
        """从链表中移除节点"""
        node.prev.next = node.next
        node.next.prev = node.prev
    
    def _add_to_head(self, node):
        """将节点添加到头部"""
        node.next = self.head.next
        node.prev = self.head
        self.head.next.prev = node
        self.head.next = node
    
    def get(self, key):
        if key not in self.cache:
            return -1
        node = self.cache[key]
        self._remove(node)
        self._add_to_head(node)
        return node.val
    
    def put(self, key, value):
        if key in self.cache:
            node = self.cache[key]
            node.val = value
            self._remove(node)
            self._add_to_head(node)
        else:
            if len(self.cache) >= self.capacity:
                # 淘汰尾部节点
                lru = self.tail.prev
                self._remove(lru)
                del self.cache[lru.key]
            node = DListNode(key, value)
            self.cache[key] = node
            self._add_to_head(node)
```

### 合并 K 个升序链表 (LeetCode 23)

```python
import heapq

def merge_k_lists(lists):
    """使用优先队列合并 K 个有序链表"""
    dummy = ListNode(0)
    curr = dummy
    heap = []
    
    for i, lst in enumerate(lists):
        if lst:
            heapq.heappush(heap, (lst.val, i, lst))
    
    while heap:
        val, i, node = heapq.heappop(heap)
        curr.next = node
        curr = curr.next
        if node.next:
            heapq.heappush(heap, (node.next.val, i, node.next))
    
    return dummy.next
```

- **时间复杂度**: O(N log K)，N 为总节点数，K 为链表数
- **空间复杂度**: O(K)

### 回文链表 (LeetCode 234)

```python
def is_palindrome(head):
    """判断链表是否为回文"""
    if not head or not head.next:
        return True
    
    # 1. 找中点
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
    
    # 2. 反转后半部分
    second = reverse_list(slow)
    first = head
    
    # 3. 比较
    while second:
        if first.val != second.val:
            return False
        first = first.next
        second = second.next
    
    return True
```

### 两数相加 (LeetCode 2)

```python
def add_two_numbers(l1, l2):
    """两个链表表示的数相加"""
    dummy = ListNode(0)
    curr = dummy
    carry = 0
    
    while l1 or l2 or carry:
        v1 = l1.val if l1 else 0
        v2 = l2.val if l2 else 0
        total = v1 + v2 + carry
        carry = total // 10
        curr.next = ListNode(total % 10)
        curr = curr.next
        if l1: l1 = l1.next
        if l2: l2 = l2.next
    
    return dummy.next
```

## 练习

| 题目 | 难度 | 核心技巧 |
|------|------|---------|
| LeetCode 206. 反转链表 | 🟢 简单 | 迭代/递归 |
| LeetCode 21. 合并两个有序链表 | 🟢 简单 | 哑节点 |
| LeetCode 141. 环形链表 | 🟢 简单 | 快慢指针 |
| LeetCode 160. 相交链表 | 🟢 简单 | 双指针 |
| LeetCode 203. 移除链表元素 | 🟢 简单 | 哑节点 |
| LeetCode 83. 删除排序链表重复 | 🟢 简单 | 遍历 |
| LeetCode 19. 删除倒数第 N 个 | 🟡 中等 | 快慢指针 |
| LeetCode 2. 两数相加 | 🟡 中等 | 模拟加法 |
| LeetCode 142. 环形链表 II | 🟡 中等 | Floyd |
| LeetCode 148. 排序链表 | 🟡 中等 | 归并排序 |
| LeetCode 234. 回文链表 | 🟡 中等 | 快慢+反转 |
| LeetCode 146. LRU 缓存 | 🟡 中等 | 哈希+双向链表 |
| LeetCode 23. 合并 K 个升序链表 | 🔴 困难 | 优先队列 |
| LeetCode 25. K 个一组翻转链表 | 🔴 困难 | 递归 |

## 相关条目

- [[Array]]
- [[Stack]]
- [[Queue]]
- [[HashTable]]
- [[Tree]]
