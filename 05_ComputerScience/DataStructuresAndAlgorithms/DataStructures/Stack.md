---
aliases: [Stack]
tags: ['DataStructuresAndAlgorithms', 'DataStructures', 'Stack']
created: 2026-05-16
updated: 2026-05-13
---

# 栈详解

## 基本概念

栈（Stack）是一种**后进先出**（LIFO, Last In First Out）的线性数据结构。允许操作的一端称为栈顶（top），另一端称为栈底（bottom）。

## 核心操作及时间复杂度

| 操作 | 描述 | 时间复杂度 |
|-----|------|-----------|
| push(x) | 元素入栈 | O(1) |
| pop() | 弹出栈顶元素 | O(1) |
| top()/peek() | 查看栈顶元素 | O(1) |
| is_empty() | 判断栈是否为空 | O(1) |
| size() | 返回栈中元素个数 | O(1) |

## 实现方式

### 基于动态数组实现

```python
class ArrayStack:
    def __init__(self, capacity=10):
        self.capacity = capacity
        self.data = [None] * capacity
        self.top = -1
    
    def push(self, val):
        if self.top == self.capacity - 1:
            self._resize(2 * self.capacity)
        self.top += 1
        self.data[self.top] = val
    
    def pop(self):
        if self.is_empty():
            raise IndexError("pop from empty stack")
        val = self.data[self.top]
        self.data[self.top] = None
        self.top -= 1
        return val
    
    def peek(self):
        if self.is_empty():
            raise IndexError("peek from empty stack")
        return self.data[self.top]
    
    def is_empty(self):
        return self.top == -1
    
    def _resize(self, new_capacity):
        new_data = [None] * new_capacity
        for i in range(self.top + 1):
            new_data[i] = self.data[i]
        self.data = new_data
        self.capacity = new_capacity
```

### 基于链表实现

```python
class LinkedStack:
    def __init__(self):
        self.head = None  # 栈顶
        self.size = 0
    
    def push(self, val):
        self.head = ListNode(val, self.head)
        self.size += 1
    
    def pop(self):
        if self.is_empty():
            raise IndexError("pop from empty stack")
        val = self.head.val
        self.head = self.head.next
        self.size -= 1
        return val
    
    def peek(self):
        if self.is_empty():
            raise IndexError("peek from empty stack")
        return self.head.val
    
    def is_empty(self):
        return self.size == 0
```

### Python 内置栈

```python
# 使用 list 模拟栈
stack = []
stack.append(1)    # push
stack.append(2)
top = stack[-1]    # peek
val = stack.pop()  # pop
print(len(stack))  # size
print(not stack)   # is_empty
```

## 单调栈 (Monotonic Stack)

单调栈是栈中元素保持单调递增或递减的特殊栈，用于解决"下一个更大/更小元素"类问题。

### 单调递增栈

栈中元素从栈底到栈顶单调递增（即栈顶最小），用于找**下一个更小元素**。

### 单调递减栈

栈中元素从栈底到栈顶单调递减（即栈顶最大），用于找**下一个更大元素**。

```python
def next_greater_element(nums):
    """下一个更大元素（单调递减栈）"""
    n = len(nums)
    result = [-1] * n
    stack = []  # 存放下标
    
    for i in range(n):
        while stack and nums[i] > nums[stack[-1]]:
            idx = stack.pop()
            result[idx] = nums[i]
        stack.append(i)
    
    return result
```

## 经典应用

### 1. 有效的括号 (LeetCode 20)

```python
def is_valid(s):
    """判断括号字符串是否有效"""
    mapping = {')': '(', ']': '[', '}': '{'}
    stack = []
    
    for char in s:
        if char in mapping:
            top = stack.pop() if stack else '#'
            if mapping[char] != top:
                return False
        else:
            stack.append(char)
    
    return not stack
```

- **时间复杂度**: O(n)
- **空间复杂度**: O(n)

### 2. 最小栈 (LeetCode 155)

在 O(1) 时间内获取栈中最小值。

```python
class MinStack:
    def __init__(self):
        self.stack = []
        self.min_stack = []  # 辅助栈，栈顶为当前最小值
    
    def push(self, val):
        self.stack.append(val)
        if not self.min_stack or val <= self.min_stack[-1]:
            self.min_stack.append(val)
    
    def pop(self):
        if self.stack:
            val = self.stack.pop()
            if val == self.min_stack[-1]:
                self.min_stack.pop()
    
    def top(self):
        return self.stack[-1]
    
    def get_min(self):
        return self.min_stack[-1]
```

- 各操作时间复杂度: O(1)
- 空间复杂度: O(n)

### 3. 每日温度 (LeetCode 739)

```python
def daily_temperatures(temperatures):
    """计算需要等多少天才有更高温度（单调栈）"""
    n = len(temperatures)
    answer = [0] * n
    stack = []  # 存放下标，栈顶到栈底递减
    
    for i in range(n):
        while stack and temperatures[i] > temperatures[stack[-1]]:
            prev = stack.pop()
            answer[prev] = i - prev
        stack.append(i)
    
    return answer
```

### 4. 表达式求值

#### 中缀转后缀（逆波兰表达式）

```python
def infix_to_postfix(expression):
    """中缀表达式转后缀表达式"""
    precedence = {'+': 1, '-': 1, '*': 2, '/': 2}
    output = []
    stack = []
    
    for token in expression.split():
        if token.isdigit():
            output.append(token)
        elif token == '(':
            stack.append(token)
        elif token == ')':
            while stack and stack[-1] != '(':
                output.append(stack.pop())
            stack.pop()  # 移除 '('
        else:  # 运算符
            while stack and stack[-1] != '(' and precedence.get(stack[-1], 0) >= precedence[token]:
                output.append(stack.pop())
            stack.append(token)
    
    while stack:
        output.append(stack.pop())
    
    return ' '.join(output)

def eval_rpn(tokens):
    """计算逆波兰表达式"""
    stack = []
    for token in tokens:
        if token in {'+', '-', '*', '/'}:
            b = stack.pop()
            a = stack.pop()
            if token == '+':
                stack.append(a + b)
            elif token == '-':
                stack.append(a - b)
            elif token == '*':
                stack.append(a * b)
            else:  # /
                stack.append(int(a / b))  # 向零取整
        else:
            stack.append(int(token))
    return stack[0]
```

### 5. 浏览器历史

```python
class BrowserHistory:
    def __init__(self, homepage):
        self.back_stack = [homepage]   # 后退栈
        self.forward_stack = []        # 前进栈
    
    def visit(self, url):
        self.back_stack.append(url)
        self.forward_stack.clear()     # 新访问清除前进历史
    
    def back(self, steps):
        while steps > 0 and len(self.back_stack) > 1:
            self.forward_stack.append(self.back_stack.pop())
            steps -= 1
        return self.back_stack[-1]
    
    def forward(self, steps):
        while steps > 0 and self.forward_stack:
            self.back_stack.append(self.forward_stack.pop())
            steps -= 1
        return self.back_stack[-1]
```

### 6. 直方图最大矩形 (LeetCode 84)

```python
def largest_rectangle_area(heights):
    """计算直方图中最大矩形面积"""
    stack = []  # 单调递增栈，存放下标
    max_area = 0
    heights.append(0)  # 哨兵
    
    for i in range(len(heights)):
        while stack and heights[i] < heights[stack[-1]]:
            h = heights[stack.pop()]
            left = stack[-1] if stack else -1
            width = i - left - 1
            max_area = max(max_area, h * width)
        stack.append(i)
    
    heights.pop()  # 移除哨兵
    return max_area
```

### 动态数组的均摊分析

动态数组每次扩容 2 倍，$n$ 次 push 操作的均摊时间复杂度：

$$ T(n) = \frac{n \cdot O(1) + (1 + 2 + 4 + \cdots + 2^{\lfloor \log_2 n \rfloor})}{n} = O(1) $$

即每次 push 的**均摊复杂度为 $O(1)$**。

| 操作 | 最坏 | 均摊 |
|-----|------|------|
| push | $O(n)$（扩容时） | $O(1)$ |
| pop | $O(1)$ | $O(1)$ |
| peek | $O(1)$ | $O(1)$ |

## 调用栈与递归

递归函数的本质就是栈的使用——每次函数调用将返回地址和局部变量压入**调用栈**，返回时弹出。

```python
def factorial(n):
    """递归计算阶乘（调用栈深度 O(n)）"""
    if n <= 1:
        return 1
    return n * factorial(n - 1)
```

## 比较：Stack vs 其他数据结构

| 特性 | Stack | Queue | Deque |
|-----|-------|-------|-------|
| 存取顺序 | LIFO | FIFO | 两端均可 |
| 主要操作 | push/pop | enqueue/dequeue | append/pop 两端 |
| 典型应用 | DFS, 括号匹配 | BFS, 缓冲 | 滑动窗口 |

## 练习

| 题目 | 难度 | 核心技巧 |
|------|------|---------|
| LeetCode 20. 有效的括号 | 🟢 简单 | 栈匹配 |
| LeetCode 155. 最小栈 | 🟡 中等 | 辅助栈 |
| LeetCode 232. 用栈实现队列 | 🟢 简单 | 双栈 |
| LeetCode 225. 用队列实现栈 | 🟢 简单 | 双队列 |
| LeetCode 739. 每日温度 | 🟡 中等 | 单调栈 |
| LeetCode 84. 柱状图最大矩形 | 🔴 困难 | 单调栈 |
| LeetCode 42. 接雨水 | 🔴 困难 | 单调栈/双指针 |
| LeetCode 150. 逆波兰表达式 | 🟡 中等 | 栈计算 |
| LeetCode 227. 基本计算器 II | 🟡 中等 | 栈 |
| LeetCode 394. 字符串解码 | 🟡 中等 | 栈 |
| LeetCode 503. 下一个更大元素 II | 🟡 中等 | 单调栈+循环 |

## 相关条目

- [[Queue]]
- [[Array]]
- [[LinkedList]]
- [[Tree]]
- [[BFSDFS]]
