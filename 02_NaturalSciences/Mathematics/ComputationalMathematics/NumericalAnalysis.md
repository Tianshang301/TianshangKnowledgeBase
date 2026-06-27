---
aliases: [NumericalAnalysis, 数值分析, ScientificComputing, 科学计算, ApproximationTheory]
tags: ['02_NaturalSciences', 'Mathematics', 'ComputationalMathematics', 'ScientificComputing']
created: 2026-05-17
updated: 2026-05-17
---

# 数值分析 Numerical Analysis

## 1. 概述 (Overview)

数值分析（Numerical Analysis）是研究用于连续数学问题数值近似解的算法。在无法获得精确解析解的情况下，数值分析提供了计算可行方法来获得高精度的近似结果，广泛应用于科学计算和工程模拟。数值分析的核心思想是将连续模型离散化（Discretization），将无限维问题转化为有限维计算问题。

## 2. 误差分析 (Error Analysis)

### 2.1 误差类型

| 误差类型 | 来源 | 特征 | 控制方法 |
|:---------|:-----|:------|:---------|
| 截断误差 (Truncation) | 无穷过程有限截断 | 可通过增加计算量减小 | 提高阶数、加密网格 |
| 舍入误差 (Rounding) | 浮点数有限精度 | 积累性、不可消除 | 使用高精度算术 |
| 测量误差 (Measurement) | 输入数据不精确 | 数据相关 | 改进测量手段 |
| 模型误差 (Modeling) | 物理模型简化 | 模型选择 | 改进数学模型 |

### 2.2 误差度量

绝对误差：$e_{\text{abs}} = |x - \hat{x}|$

相对误差：$e_{\text{rel}} = \frac{|x - \hat{x}|}{|x|}$

有效数字（Significant Digits）：与精确值一致的小数位数

**条件数**（Condition Number）衡量问题对输入误差的敏感度：

$$
\kappa(f, x) = \lim_{\varepsilon \to 0} \sup_{\|\delta x\| \leq \varepsilon} \frac{\|f(x + \delta x) - f(x)\|}{\|f(x)\|} \Big/ \frac{\|\delta x\|}{\|x\|}
$$

条件数 $\kappa$ 越大，问题越病态（Ill-conditioned）。条件数 $\kappa \approx 1$ 表示良态（Well-conditioned）。

### 2.3 算法稳定性

- **前向误差**（Forward Error）：计算结果与真实解的差距
- **后向误差**（Backward Error）：输入数据的扰动大小
- **数值稳定性**（Numerical Stability）：若后向误差小则前向误差也可控的算法

## 3. 非线性方程求根 (Nonlinear Equations)

求解 $f(x) = 0$ 的数值方法：

| 方法 | 收敛阶 | 每步计算量 | 适用条件 |
|:-----|:-------|:-----------|:---------|
| 二分法 (Bisection) | 线性 ($C=1/2$) | 1 个函数值 | $f(a)f(b) < 0$ |
| 牛顿法 (Newton) | 二次 | $f + f'$ | 函数光滑、初值接近 |
| 割线法 (Secant) | $\approx 1.618$ | 2 个函数值 | 无需导数 |
| 牛顿下山法 | 优于二次 | $f + f'$ | 牛顿法不收敛时 |

牛顿法迭代公式：

$$
x_{n+1} = x_n - \frac{f(x_n)}{f'(x_n)}
$$

牛顿法的收敛性依赖于初值选择。当 $f'(x^*) \neq 0$ 且初值足够接近根时，牛顿法具有二次收敛性。

## 4. 线性方程组求解 (Linear Systems)

### 4.1 直接法 (Direct Methods)

| 方法 | 计算量 | 特点 |
|:-----|:-------|:------|
| 高斯消元法 (Gaussian Elimination) | $O(n^3/3)$ | 基本消元过程 |
| LU 分解 (LU Decomposition) | $O(2n^3/3)$ | 一次分解多次求解 |
| Cholesky 分解 | $O(n^3/3)$ | 仅对称正定矩阵 |
| 追赶法 (Thomas Algorithm) | $O(n)$ | 仅三对角矩阵 |

LU 分解将矩阵 $A$ 分解为下三角矩阵 $L$ 和上三角矩阵 $U$：

$$
A = LU
$$

求解 $Ax = b$ 转化为 $Ly = b$（前代法）和 $Ux = y$（回代法）。

### 4.2 迭代法 (Iterative Methods)

| 方法 | 收敛条件 | 每步计算量 | 收敛速度 |
|:-----|:---------|:-----------|:---------|
| Jacobi 迭代 | 严格对角占优 | $O(n^2)$ | 慢 |
| Gauss-Seidel 迭代 | 对角占优/对称正定 | $O(n^2)$ | 优于 Jacobi |
| SOR 迭代 | $0 < \omega < 2$ | $O(n^2)$ | 最优时远优于 GS |
| 共轭梯度法 (CG) | 对称正定 | $O(n^2)$ | 超线性 |

**迭代法停止准则**：$\|r_k\| = \|b - Ax_k\| < \varepsilon$ 或 $\|x_{k+1} - x_k\| < \varepsilon$

## 5. 插值与逼近 (Interpolation & Approximation)

### 5.1 插值方法

给定数据点 $(x_i, y_i), i = 0,1,\dots,n$，构造通过所有点的函数。

| 方法 | 特点 | 误差阶 |
|:-----|:-----|:-------|
| 拉格朗日插值 (Lagrange) | 基函数构造 | $O(h^{n+1})$ |
| 牛顿插值 (Newton) | 差分形式，易于增加节点 | $O(h^{n+1})$ |
| 三次样条 (Cubic Spline) | 分段三次，$C^2$ 连续 | $O(h^4)$ |
| Hermite 插值 | 同时插值导数 | $O(h^{2n+2})$ |

拉格朗日插值多项式：

$$
P_n(x) = \sum_{i=0}^{n} y_i \prod_{\substack{j=0 \\ j \neq i}}^{n} \frac{x - x_j}{x_i - x_j}
$$

### 5.2 龙格现象 (Runge's Phenomenon)

等距节点高次多项式插值在区间端点附近会出现剧烈振荡。解决方案包括使用 Chebyshev 节点（在端点处更密集）或分段低次插值（如样条插值）。

## 6. 数值积分 (Numerical Integration)

近似计算 $I(f) = \int_a^b f(x) \, dx$。

### 6.1 Newton-Cotes 公式

| 方法 | 节点数 | 代数精度 | 误差项 |
|:-----|:-------|:---------|:-------|
| 梯形法 (Trapezoidal) | 2 | 1 次 | $-\frac{(b-a)^3}{12}f''(\xi)$ |
| Simpson 法 | 3 | 3 次 | $-\frac{(b-a)^5}{2880}f^{(4)}(\xi)$ |

复合梯形法：

$$
\int_a^b f(x)dx \approx h\left[\frac{f(a) + f(b)}{2} + \sum_{i=1}^{n-1} f(a+ih)\right], \quad h = \frac{b-a}{n}
$$

### 6.2 Gauss 求积 (Gaussian Quadrature)

Gauss 求积公式通过选择最优的节点位置和权重，对于 $2n+1$ 次多项式可以精确积分：

$$
\int_a^b f(x) w(x) dx \approx \sum_{i=1}^{n} w_i f(x_i)
$$

其中 $x_i$ 是正交多项式的零点。常见类型包括 Gauss-Legendre、Gauss-Chebyshev、Gauss-Laguerre 和 Gauss-Hermite。

## 7. 常微分方程数值解 (ODEs)

### 7.1 初值问题 (Initial Value Problems)

求解 $y' = f(t, y), \quad y(t_0) = y_0$

| 方法 | 阶数 | 稳定性 | 特点 |
|:-----|:-----|:-------|:-----|
| 向前 Euler | 1 | 条件稳定 | 显式、简单 |
| 向后 Euler | 1 | A-稳定 | 隐式、刚性适用 |
| 改进 Euler (Heun) | 2 | 条件稳定 | 预测-校正 |
| RK4 (经典龙格-库塔) | 4 | 条件稳定 | 广泛使用 |

经典四阶 Runge-Kutta 方法：

$$
\begin{aligned}
k_1 &= f(t_n, y_n) \\
k_2 &= f(t_n + \frac{h}{2}, y_n + \frac{h}{2}k_1) \\
k_3 &= f(t_n + \frac{h}{2}, y_n + \frac{h}{2}k_2) \\
k_4 &= f(t_n + h, y_n + hk_3) \\
y_{n+1} &= y_n + \frac{h}{6}(k_1 + 2k_2 + 2k_3 + k_4)
\end{aligned}
$$

### 7.2 刚性方程 (Stiff Equations)

刚性方程的特征值差异巨大，显式方法需要极小步长才能保持稳定。适用方法包括向后差分公式（Backward Differentiation Formula, BDF）和隐式 Runge-Kutta 方法。

## 8. 偏微分方程数值解 (PDEs)

| PDE 类型 | 典型方程 | 数值方法 |
|:---------|:---------|:---------|
| 椭圆型 (Elliptic) | Poisson 方程 $\nabla^2 u = f$ | 有限差分/有限元/五点法 |
| 抛物型 (Parabolic) | 热方程 $u_t = \alpha \nabla^2 u$ | Crank-Nicolson |
| 双曲型 (Hyperbolic) | 波动方程 $u_{tt} = c^2 \nabla^2 u$ | 显式格式、CFL 条件 |

**CFL 条件**（Courant-Friedrichs-Lewy Condition）是显式格式的稳定性必要条件：

$$
\Delta t \leq C \frac{\Delta x}{\max |f'(u)|}
$$

## 9. 常用软件工具 (Software Tools)

| 工具 | 特点 | 适用场景 |
|:-----|:------|:---------|
| MATLAB | 矩阵运算强大、可视化丰富 | 教学、快速原型 |
| Python (NumPy/SciPy) | 开源生态、机器学习集成 | 数据科学、大规模计算 |
| Julia | 高性能、动态类型 | 科学计算前沿研究 |
| R (base R + 包) | 统计计算强大 | 统计分析、生物信息 |
| Mathematica | 符号计算与数值计算结合 | 数学研究 |

## 10. 应用领域 (Applications)

数值分析在以下领域发挥着关键作用：
- **气象预报**（Weather Prediction）：大气方程的数值求解
- **计算流体力学**（CFD）：Navier-Stokes 方程离散求解
- **金融工程**（Financial Engineering）：期权定价、风险管理
- **量子化学**（Quantum Chemistry）：薛定谔方程数值解
- **结构分析**（Structural Analysis）：有限元分析
- **信号处理**（Signal Processing）：FFT、滤波器设计

## 相关条目

- [[02_NaturalSciences/Mathematics/AppliedMathematics|AppliedMathematics]]
- [[02_NaturalSciences/Mathematics/ComputationalMathematics|ComputationalMathematics]]
- [[05_ComputerScience/ArtificialIntelligence/MachineLearning/MachineLearning|MachineLearning]]
- [[02_NaturalSciences/Physics/Physics|Physics]]
- [[07_InterdisciplinarySciences/DataScience/DataScience|DataScience]]
- [[FluidDynamics]]
- [[OptimizationTheory]]


