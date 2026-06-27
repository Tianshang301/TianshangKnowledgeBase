---
aliases: [DiscreteMathematics]
tags: ['Mathematics', 'DiscreteMathematics']
created: 2026-05-16
updated: 2026-05-13
---

# 离散数学

## 学科定义
离散数学研究离散对象的结构与性质，是计算机科学的数学基础。包括数理逻辑、集合论、组合数学、图论、代数结构等。

## 一、组合数学

### 计数原理
**加法原理**：若事件 $A$ 有 $m$ 种方式，事件 $B$ 有 $n$ 种方式，$A$ 与 $B$ 互斥，则 $A$ 或 $B$ 有 $m + n$ 种方式。

**乘法原理**：若事件 $A$ 有 $m$ 种方式，事件 $B$ 有 $n$ 种方式，则 $A$ 与 $B$ 依次发生有 $m \times n$ 种方式。

### 排列与组合
**排列**：$P(n, k) = \frac{n!}{(n-k)!}$

**组合**：$\binom{n}{k} = C(n, k) = \frac{n!}{k!(n-k)!}$

**多重集排列**：$\frac{n!}{n_1! n_2! \cdots n_k!}$

**组合恒等式**：
- $\binom{n}{k} = \binom{n}{n-k}$
- $\binom{n}{k} = \binom{n-1}{k} + \binom{n-1}{k-1}$（Pascal 恒等式）
- $\sum_{k=0}^n \binom{n}{k} = 2^n$
- $\binom{m+n}{k} = \sum_{i=0}^k \binom{m}{i}\binom{n}{k-i}$（Vandermonde 卷积）

### 鸽笼原理
若将 $n+1$ 个物品放入 $n$ 个盒子，则至少有一个盒子包含至少两个物品。

## 二、递推关系

### 常系数线性递推
$$a_n = c_1 a_{n-1} + c_2 a_{n-2} + \cdots + c_k a_{n-k} + f(n)$$

**特征方程**：$r^k - c_1 r^{k-1} - c_2 r^{k-2} - \cdots - c_k = 0$

**齐次解**：
- 单根 $r$：$a_n^{(h)} = C r^n$
- $m$ 重根 $r$：$a_n^{(h)} = (C_0 + C_1 n + \cdots + C_{m-1} n^{m-1}) r^n$

**常见递推**：

| 递推关系                                  | 通解                                                                                                               |
| ------------------------------------- | ---------------------------------------------------------------------------------------------------------------- |
| $a_n = a_{n-1} + d$                   | $a_n = a_0 + nd$                                                                                                 |
| $a_n = r a_{n-1}$                     | $a_n = a_0 r^n$                                                                                                  |
| $a_n = a_{n-1} + a_{n-2}$ (Fibonacci) | $a_n = \frac{1}{\sqrt{5}}\left[\left(\frac{1+\sqrt{5}}{2}\right)^n - \left(\frac{1-\sqrt{5}}{2}\right)^n\right]$ |

### 生成函数
**普通生成函数 (OGF)**：
$$F(x) = \sum_{n=0}^\infty a_n x^n$$

**指数生成函数 (EGF)**：
$$E(x) = \sum_{n=0}^\infty a_n \frac{x^n}{n!}$$

**常用生成函数**：

| 序列 | OGF |
|------|-----|
| $1, 1, 1, \dots$ | $\frac{1}{1-x}$ |
| $1, c, c^2, \dots$ | $\frac{1}{1-cx}$ |
| $\binom{n}{k}$ 对 $n$ | $\frac{x^k}{(1-x)^{k+1}}$ |
| Fibonacci $F_n$ | $\frac{x}{1-x-x^2}$ |

## 三、图论

### 基本概念
**图** $G = (V, E)$，$|V| = n$ 为顶点数，$|E| = m$ 为边数。

**握手定理**：$\sum_{v \in V} \deg(v) = 2m$

**完全图** $K_n$：$m = \binom{n}{2}$

**二分图**：顶点集可划分为 $V_1, V_2$，所有边连接 $V_1$ 与 $V_2$ 中的顶点。

### 路径与连通性
**Euler 路径**：经过每条边恰好一次的路径。存在条件：恰有 0 或 2 个奇度顶点。

**Hamilton 路径**：经过每个顶点恰好一次的路径。

### 树
**树**：连通无环图。$n$ 个顶点的树有 $m = n-1$ 条边。

**生成树计数**（Cayley 公式）：$K_n$ 有 $n^{n-2}$ 棵生成树。

**最小生成树**：Kruskal 算法（$O(m\log m)$），Prim 算法（$O(m\log n)$）

### 平面图
**Euler 公式**：$n - m + f = 2$（$f$ 为面数）

推论：若 $G$ 是简单平面图且 $n \ge 3$，则 $m \le 3n - 6$

### 图着色
**四色定理**：任何平面图可用 4 种颜色正常着色。

**色数** $\chi(G)$：着色所需最少颜色数。

### 匹配
**二分图最大匹配**：匈牙利算法

**Hall 定理**：二分图 $G = (V_1 \cup V_2, E)$ 存在饱和 $V_1$ 的匹配 $\iff$ 对任意 $S \subseteq V_1$，$|N(S)| \ge |S|$

## 四、数理逻辑

### 命题逻辑
**联结词**：$\neg$（非）、$\land$（与）、$\lor$（或）、$\to$（蕴含）、$\leftrightarrow$（等价）

**真值表**：

| $p$ | $q$ | $p \land q$ | $p \lor q$ | $p \to q$ | $p \leftrightarrow q$ |
|-----|-----|------------|------------|-----------|----------------------|
| T | T | T | T | T | T |
| T | F | F | T | F | F |
| F | T | F | T | T | F |
| F | F | F | F | T | T |

### 谓词逻辑
**量词**：$\forall$（全称量词）、$\exists$（存在量词）

**推理规则**：Modus Ponens（$p \land (p \to q) \Rightarrow q$）、Modus Tollens（$\neg q \land (p \to q) \Rightarrow \neg p$）

## 五、代数结构
- **半群**：封闭 + 结合律
- **群**：半群 + 单位元 + 逆元
- **环**：两个二元运算（加法 Abel 群 + 乘法半群）
- **域**：两个二元运算（加法 Abel 群 + 乘法 Abel 群）

## 经典教材
- Rosen《Discrete Mathematics and Its Applications》
- 左孝凌《离散数学》
- Knuth《The Art of Computer Programming》

## 主要应用领域
- 算法设计与分析
- 密码学
- 计算机网络
- 数据库系统
- 编译原理
- 人工智能

## 相关条目

- [[GraphTheory]]
- Combinatorics
- ComputerScience
- [[Logic]]
