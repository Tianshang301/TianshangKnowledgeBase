---
aliases: [IR]
tags: ['CompilerPrinciples', 'IR']
---

# 中间代码生成

## 一、概述

中间代码（Intermediate Representation, IR）是编译器中连接前端（词法/语法/语义分析）和后端（代码生成/优化）的桥梁。IR 独立于源语言和目标机器，便于优化和代码生成。

### IR 的设计目标

1. **易于生成**：从语法树翻译简单
2. **易于优化**：支持数据流分析、控制流分析
3. **长度适中**：比高级语言更底层，比汇编更高级
4. **与机器无关**：可在不同目标架构间复用

---

## 二、三地址码 (Three-Address Code, TAC)

每条指令最多包含三个地址（两个操作数，一个结果）。

### 指令类型

| 指令 | 格式 | 示例 | 含义 |
|------|------|------|------|
| 赋值 | `x = y op z` | `t1 = a + b` | 二元运算 |
| 一元 | `x = op y` | `t1 = - a` | 一元运算 |
| 复制 | `x = y` | `t1 = a` | 值复制 |
| 无条件跳转 | `goto L` | `goto L1` | 跳转 |
| 条件跳转 | `if x relop y goto L` | `if a < b goto L1` | 条件跳转 |
| 参数传递 | `param x` | `param a` | 传递参数 |
| 函数调用 | `call f, n` | `call foo, 2` | 调用函数 |
| 函数返回 | `return x` | `return t1` | 返回值 |
| 数组访问 | `x = y[i]` / `x[i] = y` | `t1 = a[i]` | 数组读写 |
| 地址赋值 | `x = &y` / `x = *y` / `*x = y` | `t1 = &a` | 指针操作 |

### IR 示例

```c
// 源代码
int calculate(int a, int b, int c) {
    int r = (a + b) * (c - 1);
    if (r > 100)
        return r;
    else
        return 0;
}
```

```asm
// 三地址码
_calculate:
    t1 = a + b
    t2 = c - 1
    t3 = t1 * t2
    r = t3
    if r > 100 goto L1
    return 0
    goto L2
L1:
    return r
L2:
    // 函数结束
```

### 表示形式

**四元式 (Quadruples)**：

```
| op  | arg1 | arg2 | result |
|-----|------|------|--------|
| +   | a    | b    | t1     |
| -   | c    | 1    | t2     |
| *   | t1   | t2   | t3     |
| =   | t3   |      | r      |
| >   | r    | 100  | L1     |
| return | r  |      |        |
```

**三元式 (Triples)**：

```
| op  | arg1 | arg2 |
|-----|------|------|
| (0) | +    | a    | b    |
| (1) | -    | c    | 1    |
| (2) | *    | (0)  | (1)  |
| (3) | =    | (2)  | r    |
| (4) | >    | (3)  | 100  |
```

**间接三元式**：将三元式的索引独立为指令列表，便于优化（调整指令顺序时只需修改索引表）。

---

## 三、SSA 形式

SSA（Static Single Assignment）是 IR 的一种特殊形式：每个变量只被赋值一次。

```asm
// 普通三地址码
x = 1
x = x + 1
y = x * 2

// SSA 形式
x1 = 1
x2 = x1 + 1
y1 = x2 * 2
```

### φ 函数

在控制流汇合处，SSA 使用 φ（phi）函数选择正确版本。

```c
// 源代码
int f(int x) {
    int y;
    if (x > 0)
        y = 10;
    else
        y = 20;
    return y;
}
```

```asm
// SSA 形式
_f:
    if x0 > 0 goto L1
    goto L2
L1:
    y1 = 10
    goto L3
L2:
    y2 = 20
    goto L3
L3:
    y3 = φ(y1, y2)   // 选择控制流到达的版本
    return y3
```

### SSA 的优缺点

| 优点 | 缺点 |
|------|------|
| 数据流分析简化（def-use 链直观） | φ 函数增加指令数量 |
| 优化更易实现（常量传播、死代码删除） | 转回可执行代码需消除 φ |
| 便于并行化 | |

---

## 四、控制流图 (CFG)

CFG 以基本块为节点，以控制流边连接。

### 基本块

**定义**：指令序列满足以下条件：
1. **入口**：第一条指令之前无跳转目标
2. **出口**：最后一条指令之后无控制流进入
3. **连续**：块内无条件顺序执行

**划分算法**：

```
1. 找出所有 Leader：
   - 第一条指令
   - 任何跳转目标指令
   - 跳转指令的下一条指令

2. 从每个 Leader 到下一个 Leader 前为基本块
```

**示例**：

```asm
// 基本块划分
┌───────────────────────┐
│ (BB0) 入口           │
│   t1 = a + b         │
│   t2 = c - 1         │
│   t3 = t1 * t2       │
│   if t3 > 100 goto L1│───────────┐
└───────┬───────────────┘           │
        │                           │
┌───────▼───────────────┐           │
│ (BB1)                 │           │
│   return 0            │           │
│   goto L2             │           │
└───────┬───────────────┘           │
        │                           │
┌───────▼───────────────┐           │
│ (BB2) L1:             │◄──────────┘
│   return t3           │
│ (BB3) L2:             │
└───────────────────────┘
```

### 支配树 (Dominator Tree)

```
节点 d 支配节点 n：所有从入口到 n 的路径都经过 d。

直接支配者 (idom)：最接近的支配者。

支配边界：d 不能支配 n，但 d 支配 n 的某个前驱。
```

```
CFG:     Dominator Tree:
  0        0
 / \      / \
1   2   1   2
 \ /
  3
   \
    4
```

### 支配边界计算

```
算法：
1. 对 CFG 中每个节点 n 计算 idom
2. 对每个节点 n:
   for 每个 n 的后继 s:
     if idom(s) != n:
       DF(n) += {s}
3. 对 DFS 树自底向上：
   对每个子节点 c of n:
     for w in DF(c):
       if idom(w) != n:
         DF(n) += {w}
```

---

## 五、常见 IR

### LLVM IR

LLVM IR 是最流行的现代 IR，采用 SSA 形式，支持三地址码。

```llvm
; 计算阶乘
define i32 @factorial(i32 %n) {
entry:
  %cmp = icmp sle i32 %n, 1
  br i1 %cmp, label %return, label %recursive

recursive:
  %sub = sub i32 %n, 1
  %result = call i32 @factorial(i32 %sub)
  %mul = mul i32 %n, %result
  ret i32 %mul

return:
  ret i32 1
}
```

LLVM IR 三个层次：

| 层次 | 格式 | 说明 |
|------|------|------|
| .ll | 文本 | 可读的 IR |
| .bc | 二进制 | 位码格式 |
| 内存表示 | 运行时 | JIT 使用 |

### GIMPLE (GCC)

GCC 的中间表示，从 GENERIC 树转换而来：

```c
// 源代码
int f(int n) {
    int sum = 0;
    for (int i = 0; i < n; i++)
        sum += i;
    return sum;
}
```

```gimple
f (int n)
{
  int sum;
  int i;

  <bb 2> :
  sum = 0;
  i = 0;
  goto <bb 4>;

  <bb 3> :
  sum = sum + i;
  i = i + 1;

  <bb 4> :
  if (i < n)
    goto <bb 3>;
  else
    goto <bb 5>;

  <bb 5> :
  return sum;
}
```

### JVM 字节码

```java
// 源代码
public int add(int a, int b) {
    return a + b;
}
```

```bytecode
// JVM 字节码
public int add(int, int);
  Code:
   0: iload_1        // 加载局部变量 1 (a)
   1: iload_2        // 加载局部变量 2 (b)
   2: iadd           // 整数相加
   3: ireturn        // 返回结果
```

---

## 六、表达式翻译

### 算术表达式

```c
// a + b * c - d / e
```

```asm
t1 = b * c
t2 = a + t1
t3 = d / e
t4 = t2 - t3
```

### 数组访问

```c
// a[i][j]  其中 a 是 10×20 的 int 数组
// 地址 = base + (i * 20 + j) * 4
```

```asm
t1 = i * 20
t2 = t1 + j
t3 = t2 * 4
t4 = &a + t3
result = *t4
```

### 控制流语句

```c
// if-else
if (x > 0) {
    y = x * 2;
} else {
    y = -x;
}
```

```asm
    if x > 0 goto L1
    goto L2
L1:
    y = x * 2
    goto L3
L2:
    y = -x
L3:
    // continue
```

```c
// while 循环
while (i < n) {
    sum = sum + i;
    i = i + 1;
}
```

```asm
L1:
    if i < n goto L2
    goto L3
L2:
    sum = sum + i
    i = i + 1
    goto L1
L3:
    // continue
```

### 函数调用

```c
// result = foo(a, b + c);
```

```asm
param a
t1 = b + c
param t1
result = call foo, 2
```
