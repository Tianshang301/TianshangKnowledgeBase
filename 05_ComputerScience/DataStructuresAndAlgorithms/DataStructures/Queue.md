---
aliases: [Queue]
tags: ['DataStructuresAndAlgorithms', 'DataStructures', 'Queue']
created: 2026-05-16
updated: 2026-05-16
---

# 队列详解

## 基本概念

队列（Queue）是一种**先进先出**（FIFO, First In First Out）的线性数据结构。允许插入的一端称为队尾（rear），允许删除的一端称为队头（front）。

## 核心操作及时间复杂度

| 操作 | 描述 | 时间复杂度 |
|-----|------|-----------|
| enqueue(x) | 元素入队 | $O(1)$ |
| dequeue() | 队头元素出队 | $O(1)$ |
| front()/peek() | 查看队头元素 | $O(1)$ |
| is_empty() | 判断队列是否为空 | $O(1)$ |
| size() | 返回队列中元素个数 | $O(1)$ |

## 实现方式

### 1. 简单数组队列

```python
class ArrayQueue:
    def __init__(self, capacity=10):
        self.capacity = capacity
        self.data = [None] * capacity
        self.front = 0
        self.rear = 0  # 下一个插入位置
        self.size = 0
    
    def enqueue(self, val):
        if self.size == self.capacity:
            self._resize(2 * self.capacity)
        self.data[self.rear] = val
        self.rear = (self.rear + 1) % self.capacity
        self.size += 1
    
    def dequeue(self):
        if self.is_empty():
            raise IndexError("dequeue from empty queue")
        val = self.data[self.front]
        self.data[self.front] = None
        self.front = (self.front + 1) % self.capacity
        self.size -= 1
        return val
    
    def peek(self):
        if self.is_empty():
            raise IndexError("peek from empty queue")
        return self.data[self.front]
    
    def is_empty(self):
        return self.size == 0
    
    def _resize(self, new_capacity):
        new_data = [None] * new_capacity
        for i in range(self.size):
            new_data[i] = self.data[(self.front + i) % self.capacity]
        self.data = new_data
        self.front = 0
        self.rear = self.size
        self.capacity = new_capacity
```

**问题**：简单数组队列存在"假溢出"——数组前面有空位但 rear 已到末尾。解决方案是**循环队列**。

### 2. 循环队列 (Circular Queue)

```python
class CircularQueue:
    def __init__(self, k):
        """初始化大小为 k 的循环队列"""
        self.capacity = k + 1  # 多留一个空位区分空/满
        self.data = [None] * self.capacity
        self.front = 0
        self.rear = 0
    
    def enqueue(self, value):
        if self.is_full():
            return False
        self.data[self.rear] = value
        self.rear = (self.rear + 1) % self.capacity
        return True
    
    def dequeue(self):
        if self.is_empty():
            return False
        self.data[self.front] = None
        self.front = (self.front + 1) % self.capacity
        return True
    
    def front_value(self):
        if self.is_empty():
            return -1
        return self.data[self.front]
    
    def rear_value(self):
        if self.is_empty():
            return -1
        return self.data[(self.rear - 1) % self.capacity]
    
    def is_empty(self):
        return self.front == self.rear
    
    def is_full(self):
        return (self.rear + 1) % self.capacity == self.front
```

### 3. 链表队列

```python
class LinkedQueue:
    def __init__(self):
        self.head = None  # 队头
        self.tail = None  # 队尾
        self.size = 0
    
    def enqueue(self, val):
        node = ListNode(val)
        if self.tail:
            self.tail.next = node
        self.tail = node
        if not self.head:
            self.head = node
        self.size += 1
    
    def dequeue(self):
        if self.is_empty():
            raise IndexError("dequeue from empty queue")
        val = self.head.val
        self.head = self.head.next
        if not self.head:
            self.tail = None
        self.size -= 1
        return val
    
    def peek(self):
        if self.is_empty():
            raise IndexError("peek from empty queue")
        return self.head.val
    
    def is_empty(self):
        return self.size == 0
```

## Python collections.deque

`collections.deque` 是双端队列的高效实现，两端操作均为 O(1)。

```python
from collections import deque

# 创建
dq = deque()                 # 空队列
dq = deque([1, 2, 3])        # 从可迭代对象创建
dq = deque(maxlen=5)         # 限制最大长度

# 基本操作
dq.append(4)                 # 右端入队 O(1)
dq.appendleft(0)             # 左端入队 O(1)
dq.pop()                     # 右端出队 O(1)
dq.popleft()                 # 左端出队 O(1)
dq[0]                        # 索引访问 O(n)
dq.rotate(2)                 # 循环右移 2 步
```

## 优先队列 / 堆

详见 [Heap.md](Heap.md)，这里展示基本用法。

```python
import heapq

# 最小堆（默认）
pq = []
heapq.heappush(pq, 5)
heapq.heappush(pq, 2)
heapq.heappush(pq, 8)
print(heapq.heappop(pq))  # 2

# 最大堆：存入负数
max_heap = []
heapq.heappush(max_heap, -x)  # 存负值
val = -heapq.heappop(max_heap)
```

## 单调队列

单调队列常用于解决"滑动窗口最值"问题，如**滑动窗口最大值**。

### 滑动窗口最大值 (LeetCode 239)

```python
def max_sliding_window(nums, k):
    """返回每个滑动窗口的最大值"""
    from collections import deque
    result = []
    dq = deque()  # 存储下标，对应值单调递减
    
    for i, num in enumerate(nums):
        # 移除不在窗口内的元素
        if dq and dq[0] < i - k + 1:
            dq.popleft()
        
        # 维护单调递减
        while dq and nums[dq[-1]] < num:
            dq.pop()
        dq.append(i)
        
        # 窗口形成后记录结果
        if i >= k - 1:
            result.append(nums[dq[0]])
    
    return result
```

- **时间复杂度**: O(n) — 每个元素最多入队出队一次
- **空间复杂度**: O(k)

## 队列的应用

### 1. BFS (广度优先搜索)

```python
from collections import deque

def bfs(graph, start):
    """图的广度优先遍历"""
    visited = {start}
    queue = deque([start])
    
    while queue:
        node = queue.popleft()
        print(node, end=' ')
        
        for neighbor in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
```

### 2. 层次遍历二叉树

```python
def level_order(root):
    """二叉树的层序遍历"""
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

### 3. 用栈实现队列 (LeetCode 232)

```python
class MyQueue:
    def __init__(self):
        self.in_stack = []   # 入队栈
        self.out_stack = []  # 出队栈
    
    def push(self, x):
        self.in_stack.append(x)
    
    def pop(self):
        self._transfer()
        return self.out_stack.pop()
    
    def peek(self):
        self._transfer()
        return self.out_stack[-1]
    
    def empty(self):
        return not self.in_stack and not self.out_stack
    
    def _transfer(self):
        if not self.out_stack:
            while self.in_stack:
                self.out_stack.append(self.in_stack.pop())
```

### 4. 击鼓传花 / Josephus 问题

```python
def josephus(n, k):
    """n 个人，每数到 k 的人出列"""
    q = deque(range(1, n + 1))
    while len(q) > 1:
        for _ in range(k - 1):
            q.append(q.popleft())
        q.popleft()  # 第 k 个人出列
    return q[0]
```

### 5. 任务调度 / 生产者消费者

```python
from threading import Thread, Lock
from collections import deque
import time

class TaskQueue:
    def __init__(self):
        self.queue = deque()
        self.lock = Lock()
    
    def produce(self, task):
        with self.lock:
            self.queue.append(task)
            print(f"Produced: {task}")
    
    def consume(self):
        while True:
            with self.lock:
                if self.queue:
                    task = self.queue.popleft()
                    print(f"Consumed: {task}")
            time.sleep(0.1)
```

## 练习

| 题目 | 难度 | 核心技巧 |
|------|------|---------|
| LeetCode 232. 用栈实现队列 | 🟢 简单 | 双栈 |
| LeetCode 622. 设计循环队列 | 🟡 中等 | 循环数组 |
| LeetCode 641. 设计循环双端队列 | 🟡 中等 | 循环数组 |
| LeetCode 239. 滑动窗口最大值 | 🔴 困难 | 单调队列 |
| LeetCode 933. 最近的请求次数 | 🟢 简单 | 队列 |
| LeetCode 2073. 买票需要的时间 | 🟢 简单 | 队列模拟 |
| LeetCode 862. 和至少为 K 的最短子数组 | 🔴 困难 | 单调队列+前缀和 |
| LeetCode 346. 数据流中的移动平均值 | 🟢 简单 | 队列 |

## 相关条目

- [[Stack]]
- [[Array]]
- [[LinkedList]]
- [[Heap]]
- [[05_ComputerScience/DataStructuresAndAlgorithms/Algorithms/BFSDFS|BFSDFS]]


