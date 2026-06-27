---
aliases: [Optimization]
tags: ['CompilerPrinciples', 'Optimization']
created: 2026-05-16
updated: 2026-05-13
---

# 编译优化

## 一、概述

编译优化在保持程序语义的前提下，通过分析和变换 IR，使生成的目标代码执行更快、占用空间更小。

### 优化分类

| 分类 | 范围 | 示例 |
|------|------|------|
| 局部优化 | 单个基本块内 | 常量折叠、公共子表达式删除 |
| 全局优化 | 单个函数内跨基本块 | 循环不变代码外提 |
| 过程间优化 | 跨函数 | 内联、常量传播 |
| 机器相关优化 | 特定架构 | 指令调度、寄存器分配 |

---

## 二、局部优化

### 常量折叠 (Constant Folding)

编译时计算常量表达式的值。

```asm
// 优化前
t1 = 3 + 5
t2 = t1 * 2

// 优化后
t2 = 16
```

```c
// C 语言级别
int x = 2 * 3 * 4;   // 编译时直接计算为 24
```

### 代数简化 (Algebraic Simplification)

```asm
// 优化前              优化后
t1 = 0 + x           // x
t1 = x * 1           // x
t1 = x * 0           // 0
t1 = x + 0           // x
t1 = x - 0           // x
t1 = x - x           // 0
t1 = x / 1           // x
t1 = x * 2           // x << 1
t1 = x / 2           // x >> 1 (无符号或有符号正)
t1 = x * 2 + x       // x * 3 (强度削弱)
```

### 死代码删除 (Dead Code Elimination)

删除结果不被使用且无副作用的指令。

```asm
// 优化前
t1 = a + b
t2 = c + d
t3 = t2 * a      // t3 从未使用
t4 = t2 * b
result = t1 + t4

// 优化后
t1 = a + b
t2 = c + d
t4 = t2 * b
result = t1 + t4
```

### 公共子表达式删除 (Common Subexpression Elimination, CSE)

```asm
// 优化前
t1 = a + b
t2 = a - 1
t3 = a + b        // 重复计算
t4 = t3 * t2

// 优化后
t1 = a + b
t2 = a - 1
t4 = t1 * t2      // 复用 t1
```

### 复制传播 (Copy Propagation)

```asm
// 优化前
t1 = x
t2 = t1 + 1
t3 = x
t4 = t2 * t3

// 优化后（复制传播 + 死代码删除）
t2 = x + 1
t4 = t2 * x
```

---

## 三、全局优化

### 循环不变代码外提 (Loop Invariant Code Motion)

将循环内不随迭代变化的表达式外提到循环前。

```asm
// 优化前（每次循环都计算）
L1:
    t1 = 3 * 7          // 循环不变
    t2 = a[i] + t1
    a[i] = t2
    i = i + 1
    if i < n goto L1

// 优化后
t1 = 3 * 7              // 提到循环前
L1:
    t2 = a[i] + t1
    a[i] = t2
    i = i + 1
    if i < n goto L1
```

### 归纳变量删除 (Induction Variable Elimination)

```asm
// 优化前
L1:
    t1 = i * 4
    a[t1] = 0
    i = i + 1
    if i < n goto L1

// 优化后（用地址递增替代乘法）
t1 = &a                 // 数组基址
L1:
    *t1 = 0
    t1 = t1 + 4         // 步进 4 字节
    i = i + 1
    if i < n goto L1
```

### 强度削弱 (Strength Reduction)

将昂贵运算替换为廉价运算。

```asm
// 乘法 → 加法
// 优化前
t1 = i * 4

// 优化后（循环内）
// 每次迭代递增 4 而不是重新计算乘法

// 乘法 → 移位
t1 = x * 8    →  t1 = x << 3
t1 = x / 4    →  t1 = x >> 2  (仅无符号)
```

### 循环展开 (Loop Unrolling)

减少循环控制开销。

```asm
// 原始循环
L1:
    a[i] = 0
    i = i + 1
    if i < n goto L1

// 展开 4 次
L1:
    a[i]   = 0
    a[i+1] = 0
    a[i+2] = 0
    a[i+3] = 0
    i = i + 4
    if i < n goto L1

// 处理剩余元素
L2:
    if i >= n goto L3
    a[i] = 0
    i = i + 1
    goto L2
L3:
```

### 内联 (Inlining)

将函数调用替换为函数体本身。

```c
// 优化前
int min(int a, int b) { return a < b ? a : b; }

int f(int x, int y) {
    return min(x * 2, y * 3);
}

// 优化后（内联展开）
int f(int x, int y) {
    return (x * 2) < (y * 3) ? (x * 2) : (y * 3);
}
```

---

## 四、数据流分析

### 到达定值 (Reaching Definitions)

定义：变量 x 的定值 d 到达程序点 p 如果存在一条从 d 到 p 的路径，该路径上 x 未被重定义。

```
方程：
  IN[B]  = ∪(OUT[P]) for P in predecessors(B)
  OUT[B] = GEN[B] ∪ (IN[B] - KILL[B])

  GEN[B]: B 中生成的定值（被定义的变量）
  KILL[B]: B 中变量的其他定值
```

```asm
// 分析示例
BB0:
  a = 1         // def a1
  b = 2         // def b1

BB1:
  a = a + b     // def a2（杀死 a1）
  c = a + b     // def c1

BB2:
  if a > 0 goto BB1
```

### 活跃变量分析 (Live Variable Analysis)

定义：变量 v 在程序点 p 是活跃的，如果存在一条从 p 开始的路径使用了 v 的值。

```
方程：
  OUT[B] = ∪(IN[S]) for S in successors(B)
  IN[B]  = USE[B] ∪ (OUT[B] - DEF[B])

  USE[B]: B 中使用但之前未定义的变量
  DEF[B]: B 中定义的变量
```

```asm
// 活跃变量分析用于寄存器分配
BB0:
  a = 1         // 活跃变量: ε
  b = 2         // 活跃变量: a
  c = a + b     // 活跃变量: a, b → 生成 c 后 a,b 不再活跃
```

### 可用表达式 (Available Expressions)

定义：表达式 e 在程序点 p 是可用的，如果所有到达 p 的路径都计算过 e 且之后未修改操作数。

```
方程：
  IN[B]  = ∩(OUT[P]) for P in predecessors(B)
  OUT[B] = GEN[B] ∪ (IN[B] - KILL[B])

  GEN[B]: B 中计算的表达式
  KILL[B]: 被 B 修改了操作数的表达式
```

---

## 五、寄存器分配

### 图着色算法

```
1. 构建干涉图 (Interference Graph):
   - 节点 = 变量（虚拟寄存器）
   - 边 = 两个变量在同一时刻活跃，不能分配同一物理寄存器

2. 着色（K 种颜色，K = 物理寄存器数）:
   - 如果节点数 ≤ K，直接可着色
   - 否则选择一个节点溢出 (spill) 到内存
```

```asm
// 寄存器分配示例
// 物理寄存器: eax, ebx, ecx, edx

// 优化前（假设只有 2 个物理寄存器）
t1 = a + b       // t1 → eax
t2 = c + d       // t2 → ebx（需要溢出 t1）
t3 = t1 * t2     // t3 → eax（t1 从内存恢复）

// 如果干涉图中 t1, t2, t3 都互相干涉，需要 3 个寄存器
// 但只有 2 个，则选择一个溢出
```

### 线性扫描

更高效的寄存器分配算法，适合 JIT 编译器：

```
1. 计算每个变量的活跃区间 [start, end]
2. 按 start 排序
3. 扫描区间：
   - 当新区间开始时：
     - 释放已结束的区间
     - 如果有空闲寄存器，分配
     - 否则，选择一个区间溢出
```

### 寄存器分配策略

| 策略 | 说明 |
|------|------|
| 直接分配 | 固定使用特定寄存器（如 eax 作累加器） |
| 图着色 | 全局优化，效果好但较慢 |
| 线性扫描 | 快速，效果接近图着色 |
| 优先寄存器 | 频繁使用的变量优先分配寄存器 |
| 多核优化 | 使用 SIMD 寄存器进行向量化 |

---

## 六、优化等级

| GCC 等级 | 说明 |
|----------|------|
| -O0 | 无优化，编译最快 |
| -O1 | 基本优化（时间-空间折中） |
| -O2 | 大多数优化，不包括空间-时间折中 |
| -O3 | 所有优化（包括循环展开、函数内联） |
| -Os | 优化空间大小 |
| -Ofast | -O3 + 忽略严格标准合规（可能不精确） |

### GCC -O2 启用的优化

```
auto-inc-dec
branch-probabilities
combine-stack-adjustments
common-subexpression-elimination
constant-propagation
dead-code-elimination
div-mod-transform
dominator-optimization
dse
forward-propagate
function-cse
gcse
global-var
if-conversion
inline-simple
ipa-pure-const
loop-invariant-motion
loop-optimizations
merge-constants
move-loop-invariants
peephole
peephole2
reassociate
regmove
reorder-blocks
sched-interblock
sched-spec
store-forwarding
strength-reduce
tree-builtin-call-dce
tree-copy-prop
tree-dce
tree-dominator-opts
tree-forwprop
tree-fre
tree-loop-im
tree-loop-ivcanon
tree-phiprop
tree-pta
tree-sra
tree-ssa-ccp
tree-ssa-copyrename
tree-ssa-dce
tree-ssa-dom
tree-ssa-forwprop
tree-ssa-live
tree-ssa-phiopt
tree-ssa-pre
tree-ssa-reassoc
tree-ssa-sccvn
tree-tail-merge
unit-at-a-time
```

### 优化与调试的权衡

```
-O0：调试体验最好，变量可查看，单步跟踪精准
-O1：大部分变量可看，局部信息保留
-O2：部分变量优化掉，行号信息可能偏移
-O3：函数可能内联消失，调试困难
```
