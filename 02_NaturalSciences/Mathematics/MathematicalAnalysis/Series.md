---
aliases:
  - 级数
  - Series
  - 无穷级数
  - Infinite Series
  - 幂级数
  - Power Series
  - 傅里叶级数
  - Fourier Series
  - 泰勒级数
tags:
  - mathematics
  - series
  - convergence
  - Fourier
  - power series
  - Taylor
  - analysis
---

# 级数 (Series)

## 概述 (Overview)

级数是无穷数列之和，是分析学中研究函数逼近和表示的重要工具。主要类型包括数项级数 (numerical series)、幂级数 (power series) 和傅里叶级数 (Fourier series)。级数理论在信号处理、数值分析、微分方程和量子力学中有核心地位。通过级数展开，可以将复杂函数表示为简单函数的无穷和，从而进行分析和计算。

```mermaid
graph TD
  A[级数 Series] --> B[数项级数 Numerical]
  A --> C[函数项级数 Functional]
  B --> D[正项级数 Positive Term]
  B --> E[交错级数 Alternating]
  B --> F[任意项级数 General Term]
  C --> G[幂级数 Power Series<br/>Σ c_n(x-a)^n]
  C --> H[傅里叶级数 Fourier Series<br/>三角级数]
  C --> I[泰勒级数 Taylor Series]
  D --> J[比较判别法 Comparison]
  D --> K[比值判别法 Ratio Test]
  D --> L[根值判别法 Root Test]
  D --> M[积分判别法 Integral Test]
  D --> N[p-级数 p-Series<br/>Σ 1/n^p]
  E --> O[莱布尼茨判别法 Leibniz]
  G --> P[收敛半径 Radius R]
  G --> Q[逐项求导与积分]
  G --> R[和函数 Sum Function]
  H --> S[傅里叶系数 Fourier Coeff]
  H --> T[收敛定理 Dirichlet]
  I --> U[余项估计 Remainder]
```

## 数项级数 (Numerical Series)

### 基本概念 (Basic Concepts)

级数 $\sum_{n=1}^\infty a_n$ 的部分和 $S_N = \sum_{n=1}^N a_n$。级数收敛当且仅当 $\lim_{N \to \infty} S_N$ 存在有限。

### 收敛的必要条件 (Necessary Condition)

若 $\sum a_n$ 收敛，则 $\lim_{n \to \infty} a_n = 0$。反之不真（调和级数 $\sum 1/n$ 发散但通项趋于 0）。

### 正项级数判别法 (Tests for Positive Series)

#### 比较判别法 (Comparison Test)

若 $0 \leq a_n \leq b_n$ 且 $\sum b_n$ 收敛，则 $\sum a_n$ 收敛。若 $a_n \geq b_n \geq 0$ 且 $\sum b_n$ 发散，则 $\sum a_n$ 发散。

#### 极限比较法 (Limit Comparison Test)

若 $\lim_{n \to \infty} a_n / b_n = c > 0$，则 $\sum a_n$ 与 $\sum b_n$ 同敛散。

#### 比值判别法 (Ratio Test, d'Alembert)

$$
\rho = \lim_{n \to \infty} \left| \frac{a_{n+1}}{a_n} \right|
$$

$\rho < 1$ 绝对收敛，$\rho > 1$ 发散，$\rho = 1$ 无法判断。

#### 根值判别法 (Root Test, Cauchy)

$$
\rho = \lim_{n \to \infty} \sqrt[n]{|a_n|}
$$

$\rho < 1$ 绝对收敛，$\rho > 1$ 发散，$\rho = 1$ 无法判断。

#### 积分判别法 (Integral Test)

若 $a_n = f(n)$，$f$ 在 $[1, \infty)$ 上连续正递减，则 $\sum a_n$ 收敛当且仅当 $\int_1^\infty f(x) \, dx$ 收敛。

| 判别法 | 适用类型 | 优点 | 局限 |
|---|---|---|---|
| 比较 | 正项级数 | 灵活 | 需已知参照级数 |
| 极限比较 | 正项级数 | 不需不等式 | 极限需存在非零 |
| 比值 | 含阶乘 $n!$ 或指数 $a^n$ | 简单易算 | 对 p-级数无效 |
| 根值 | 含 $n$ 次幂 $[f(n)]^n$ | 通用 | 有时极限难求 |
| 积分 | $a_n = f(n)$ 形式 | 精确 | $f$ 需可积 |

#### 常用参照级数 (Reference Series)

- **p-级数**：$\sum 1/n^p$ 收敛当且仅当 $p > 1$
- **几何级数**：$\sum a r^n$ 收敛当且仅当 $|r| < 1$，和为 $\frac{a}{1 - r}$
- **调和级数**：$\sum 1/n$ 发散（$p = 1$ 的情形）

### 交错级数与绝对收敛 (Alternating Series and Absolute Convergence)

#### 莱布尼茨判别法 (Leibniz Test for Alternating Series)

若 $a_n$ 单调递减趋于 $0$，则 $\sum (-1)^{n} a_n$ 收敛。余项估计：$|R_N| = |S - S_N| \leq a_{N+1}$。

#### 绝对收敛 (Absolute Convergence)

若 $\sum |a_n|$ 收敛，则 $\sum a_n$ 绝对收敛，且 $\sum a_n$ 必收敛。

#### 条件收敛 (Conditional Convergence)

$\sum a_n$ 收敛但 $\sum |a_n|$ 发散时称为条件收敛。例如 $\sum (-1)^n / n$。

**黎曼重排定理 (Riemann Rearrangement Theorem)**：条件收敛级数可通过重排得到任意和（包括发散）。

## 幂级数 (Power Series)

### 定义 (Definition)

$$
\sum_{n=0}^\infty c_n (x - a)^n
$$

### 收敛半径 (Radius of Convergence)

$$
R = \frac{1}{\limsup_{n \to \infty} \sqrt[n]{|c_n|}} \quad \text{或} \quad R = \lim_{n \to \infty} \left| \frac{c_n}{c_{n+1}} \right|
$$

收敛区间为 $(a - R, a + R)$，端点 $x = a \pm R$ 需单独检验。

### 幂级数的运算 (Operations)

在收敛区间 $(a - R, a + R)$ 内可逐项求导和逐项积分，且收敛半径不变：

$$
\frac{d}{dx} \sum_{n=0}^\infty c_n x^n = \sum_{n=1}^\infty n c_n x^{n-1},\quad \int \sum_{n=0}^\infty c_n x^n \, dx = \sum_{n=0}^\infty \frac{c_n}{n+1} x^{n+1} + C
$$

## 泰勒展开 (Taylor Expansion)

### 泰勒定理 (Taylor's Theorem with Remainder)

$$
f(x) = \sum_{k=0}^n \frac{f^{(k)}(a)}{k!} (x - a)^k + R_n(x)
$$

**拉格朗日余项 (Lagrange Remainder)**：

$$
R_n(x) = \frac{f^{(n+1)}(\xi)}{(n+1)!} (x - a)^{n+1},\quad \xi \in (a, x)
$$

### 常用麦克劳林展开 (Common Maclaurin Series)

| 函数 | 展开式 | 收敛域 |
|---|---|---|
| $\displaystyle \frac{1}{1 - x}$ | $\displaystyle \sum_{n=0}^\infty x^n$ | $|x| < 1$ |
| $e^x$ | $\displaystyle \sum_{n=0}^\infty \frac{x^n}{n!}$ | $\mathbb{R}$ |
| $\sin x$ | $\displaystyle \sum_{n=0}^\infty \frac{(-1)^n x^{2n+1}}{(2n+1)!}$ | $\mathbb{R}$ |
| $\cos x$ | $\displaystyle \sum_{n=0}^\infty \frac{(-1)^n x^{2n}}{(2n)!}$ | $\mathbb{R}$ |
| $\ln(1 + x)$ | $\displaystyle \sum_{n=1}^\infty \frac{(-1)^{n-1} x^n}{n}$ | $(-1, 1]$ |
| $\arctan x$ | $\displaystyle \sum_{n=0}^\infty \frac{(-1)^n x^{2n+1}}{2n+1}$ | $[-1, 1]$ |
| $(1 + x)^\alpha$ | $\displaystyle \sum_{n=0}^\infty \binom{\alpha}{n} x^n$ | $|x| < 1$ |

## 傅里叶级数 (Fourier Series)

周期 $2L$ 的函数 $f(x)$：

$$
f(x) \sim \frac{a_0}{2} + \sum_{n=1}^\infty \left[ a_n \cos\left(\frac{n\pi x}{L}\right) + b_n \sin\left(\frac{n\pi x}{L}\right) \right]
$$

**傅里叶系数**：

$$
a_n = \frac{1}{L} \int_{-L}^L f(x) \cos\left(\frac{n\pi x}{L}\right) dx,\ b_n = \frac{1}{L} \int_{-L}^L f(x) \sin\left(\frac{n\pi x}{L}\right) dx
$$

**收敛定理 (Dirichlet)**：分段光滑函数的傅里叶级数逐点收敛到 $\frac{f(x^+) + f(x^-)}{2}$。

## 应用 (Applications)

| 领域 | 级数类型 | 说明 |
|---|---|---|
| 函数近似 | 泰勒级数 | 多项式逼近 |
| 信号处理 | 傅里叶级数 | 谐波分解与滤波 |
| 数值积分 | 幂级数 | 逐项积分 |
| ODE 求解 | 幂级数法 | 解析解展开 |
| 量子力学 | 傅里叶级数 | 波函数展开 |
| 图像压缩 | 余弦级数 | JPEG DCT |

### 函数项级数的一致收敛 (Uniform Convergence of Functional Series)

函数项级数 $\sum u_n(x)$ 在区间 $I$ 上一致收敛 (uniformly convergent) 到 $S(x)$ 当且仅当 $\lim_{n\to\infty} \sup_{x\in I} |S_n(x) - S(x)| = 0$。**魏尔斯特拉斯 M-判别法 (Weierstrass M-test)**：若 $|u_n(x)| \leq M_n$ 且 $\sum M_n$ 收敛，则 $\sum u_n(x)$ 一致收敛。

一致收敛保持了连续性、可积性和可微性（在适当条件下），是分析中函数项级数运算的理论基础。

### 幂级数的应用：求解微分方程 (Power Series Solution of ODEs)

在常点 $x_0$ 附近，$y'' + p(x) y' + q(x) y = 0$ 有幂级数解 $y = \sum c_n (x - x_0)^n$，代入后递推得到系数。在正则奇点处需使用**弗罗贝尼乌斯方法 (Frobenius Method)**，设 $y = (x - x_0)^r \sum c_n (x - x_0)^n$，由指标方程 (indicial equation) 确定 $r$。
