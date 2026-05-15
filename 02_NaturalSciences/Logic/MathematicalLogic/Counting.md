---
aliases: [Counting]
tags: ['Logic', 'MathematicalLogic', 'Counting']
---

# 组合计数详解

## 一、基本计数原理

### 加法法则

若事件 $A$ 有 $m$ 种方式，事件 $B$ 有 $n$ 种方式，$A$ 与 $B$ 互斥，则 $A$ 或 $B$ 有 $m + n$ 种方式。

### 乘法法则

若事件 $A$ 有 $m$ 种方式，事件 $B$ 有 $n$ 种方式，则 $A$ 和 $B$ 先后发生有 $m \times n$ 种方式。

### 容斥原理

$$|A \cup B| = |A| + |B| - |A \cap B|$$
$$|A \cup B \cup C| = |A| + |B| + |C| - |A \cap B| - |A \cap C| - |B \cap C| + |A \cap B \cap C|$$

推广：
$$\left|\bigcup_{i=1}^n A_i\right| = \sum_{k=1}^n (-1)^{k+1} \sum_{1 \leq i_1 < \cdots < i_k \leq n} |A_{i_1} \cap \cdots \cap A_{i_k}|$$

## 二、排列与组合

### 排列

**无重复排列：**
$$P(n, k) = \frac{n!}{(n-k)!} = n(n-1)\cdots(n-k+1)$$

**有重复排列：** $n^k$

**圆排列：** $\frac{(n-1)!}{2}$（可翻转时）
**圆排列（不可翻转）：** $(n-1)!$

**多重集排列：** $n$ 个物体，$n_1$ 个同种、$n_2$ 个另一种、...：

$$\frac{n!}{n_1! n_2! \cdots n_k!}$$

### 组合

**无重复组合：**
$$\binom{n}{k} = \frac{n!}{k!(n-k)!}$$

**有重复组合（星与条法）：**
$$\binom{n + k - 1}{k} = \binom{n + k - 1}{n - 1}$$

**组合恒等式**：
$$\binom{n}{k} = \binom{n}{n-k} \quad \text{对称性}$$
$$\binom{n}{k} = \binom{n-1}{k-1} + \binom{n-1}{k} \quad \text{Pascal 公式}$$
$$\sum_{k=0}^n \binom{n}{k}^2 = \binom{2n}{n} \quad \text{Vandermonde 恒等式}$$

### 二项式定理

$$(x + y)^n = \sum_{k=0}^n \binom{n}{k} x^{n-k} y^k$$

### 多项式定理

$$(x_1 + x_2 + \cdots + x_m)^n = \sum_{k_1 + \cdots + k_m = n} \frac{n!}{k_1! k_2! \cdots k_m!} x_1^{k_1} x_2^{k_2} \cdots x_m^{k_m}$$

## 三、递推关系

### 斐波那契数列

$$F_n = F_{n-1} + F_{n-2}, \quad F_0 = 0, F_1 = 1$$

闭式：$F_n = \frac{1}{\sqrt{5}}\left(\phi^n - \psi^n\right)$，其中 $\phi = \frac{1+\sqrt{5}}{2}$，$\psi = \frac{1-\sqrt{5}}{2}$

### 线性递推求解

考虑 $a_n = c_1 a_{n-1} + c_2 a_{n-2} + \cdots + c_k a_{n-k}$

特征方程：$r^k - c_1 r^{k-1} - c_2 r^{k-2} - \cdots - c_k = 0$

- 不同根 $r_1, \dots, r_k$：$a_n = \alpha_1 r_1^n + \cdots + \alpha_k r_k^n$
- 重根 $r$（重数 $m$）：$\alpha_1 r^n + \alpha_2 n r^n + \cdots + \alpha_m n^{m-1} r^n$

**常用生成函数**：
$$\frac{1}{1-x} = \sum_{n=0}^\infty x^n, \quad \frac{1}{(1-x)^k} = \sum_{n=0}^\infty \binom{n+k-1}{n} x^n$$
$$\frac{1}{1-ax} = \sum_{n=0}^\infty a^n x^n, \quad e^x = \sum_{n=0}^\infty \frac{x^n}{n!}$$

### 生成函数

$$G(x) = \sum_{n=0}^\infty a_n x^n$$

利用生成函数的代数操作求解递推。

## 四、卡特兰数 (Catalan Numbers)

### 公式

$$C_n = \frac{1}{n+1} \binom{2n}{n} = \frac{(2n)!}{(n+1)!n!}$$

递推：$C_0 = 1$，$C_{n+1} = \sum_{i=0}^n C_i C_{n-i}$

前几项：$1, 1, 2, 5, 14, 42, 132, 429, 1430, \dots$

### 解释

- $n$ 对括号的正确匹配方式数
- $n+1$ 个节点的满二叉树数
- 从 $(0,0)$ 到 $(n,n)$ 不越过对角线的格路数
- $n$ 个矩阵的加括号方式数
- 凸 $(n+2)$ 边形的三角剖分数

## 五、斯特林数 (Stirling Numbers)

### 第二类斯特林数

$S(n,k)$ = 将 $n$ 个不同元素划分成 $k$ 个不可区分的非空子集的方法数。

递推：$S(n,k) = k S(n-1,k) + S(n-1,k-1)$

边界：$S(n,0) = 0 \ (n>0)$，$S(n,1) = 1$，$S(n,n) = 1$

**Bell 数**：将 $n$ 个不同元素划分成任意个非空子集的方法数：
$$B_n = \sum_{k=1}^n S(n,k), \quad B_{n+1} = \sum_{k=0}^n \binom{n}{k} B_k$$
前几项：$B_0=1, B_1=1, B_2=2, B_3=5, B_4=15, B_5=52$

### 第一类斯特林数

$c(n,k)$ = $n$ 个元素的排列中恰有 $k$ 个轮换的个数。

递推：$c(n,k) = (n-1)c(n-1,k) + c(n-1,k-1)$

## 六、Burnside 引理

群 $G$ 作用在集合 $X$ 上时，轨道数：

$$\text{轨道数} = \frac{1}{|G|} \sum_{g \in G} |\text{Fix}(g)|$$

其中 $\text{Fix}(g) = \{x \in X \mid g(x) = x\}$。

## 七、鸽巢原理

### 基本原理

若将 $n+1$ 个物体放入 $n$ 个盒子中，则至少有一个盒子包含至少 2 个物体。

### 推广

若将 $N$ 个物体放入 $k$ 个盒子中，则至少有一个盒子包含至少 $\lceil N/k \rceil$ 个物体。

**生日悖论**：$n$ 个人中至少两人生日相同的概率：
$$P(n) = 1 - \frac{365!}{365^n (365-n)!} \approx 1 - e^{-n(n-1)/(2 \cdot 365)}$$
当 $n \geq 23$ 时 $P > 0.5$，当 $n \geq 70$ 时 $P > 0.999$。

**Erdős–Szekeres 定理**：任意 $n^2+1$ 个不同实数序列中，必存在长度为 $n+1$ 的单调子序列。

**应用示例：** 在任意 6 个人中，要么有 3 人相互认识，要么有 3 人互不认识。
