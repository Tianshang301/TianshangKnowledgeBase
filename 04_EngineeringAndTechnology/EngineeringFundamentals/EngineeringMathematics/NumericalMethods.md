---
aliases: [NumericalMethods, 数值方法]
tags: ['EngineeringFundamentals', 'EngineeringMathematics', 'NumericalMethods']
created: 2026-05-17
updated: 2026-05-17
---

# 工程数值方法 (Numerical Methods in Engineering)

## 定义

数值方法研究如何利用计算机求解工程与科学问题中的数学近似解。它包括算法设计、误差分析、收敛性证明与应用实现，是连接数学理论与工程实践的桥梁。

## 核心内容

### 数值误差 (Numerical Errors)

**误差分类**：

- **截断误差 (Truncation Error)**：用有限项近似无穷过程
- **舍入误差 (Round-off Error)**：浮点数有限精度表示

**误差传播与条件数 (Condition Number)**：

$$
\frac{|\delta x|}{|x|} \leq \kappa(A) \frac{|\delta b|}{|b|}
$$

其中 $\kappa(A) = \|A\| \|A^{-1}\|$ 为矩阵条件数。

### 非线性方程求根 (Root Finding)

**二分法 (Bisection Method)**：在区间 $[a,b]$ 上 $f(a) \cdot f(b) < 0$，逐步对分。

**Newton 法**：

$$
x_{n+1} = x_n - \frac{f(x_n)}{f'(x_n)}
$$

**割线法 (Secant Method)**：

$$
x_{n+1} = x_n - f(x_n) \frac{x_n - x_{n-1}}{f(x_n) - f(x_{n-1})}
$$

**收敛阶数对比**：

| 方法 | 收敛阶 | 每次迭代函数计算次数 |
|------|--------|-------------------|
| 二分法 | 线性 | 1 |
| Newton 法 | 二阶 | 2 |
| 割线法 | 超线性 ($\approx 1.618$) | 1 |

### 线性方程组求解 (Linear Systems)

**直接法 (Direct Methods)**：

- **Gauss 消去法 (Gaussian Elimination)**

  $$A = LU$$

- **LU 分解**：$A\mathbf{x} = \mathbf{b} \to L\mathbf{y} = \mathbf{b}, U\mathbf{x} = \mathbf{y}$
- **Cholesky 分解**：对称正定矩阵 $A = LL^T$
- **追赶法 (Thomas Algorithm)**：三对角矩阵特殊情形

**迭代法 (Iterative Methods)**：

**Jacobi 迭代**：

$$
x_i^{(k+1)} = \frac{1}{a_{ii}} \left( b_i - \sum_{j \neq i} a_{ij} x_j^{(k)} \right)
$$

**Gauss-Seidel 迭代**：

$$
x_i^{(k+1)} = \frac{1}{a_{ii}} \left( b_i - \sum_{j < i} a_{ij} x_j^{(k+1)} - \sum_{j > i} a_{ij} x_j^{(k)} \right)
$$

**SOR 迭代 (Successive Over-Relaxation)**：

$$
x_i^{(k+1)} = (1-\omega)x_i^{(k)} + \omega \cdot x_{i,GS}^{(k+1)}
$$

其中 $\omega \in (0, 2)$ 为松弛因子，最优值 $\omega_{opt} = 2/(1+\sqrt{1-\rho^2})$。

### 插值与拟合 (Interpolation & Curve Fitting)

**Lagrange 插值**：

$$
L_n(x) = \sum_{i=0}^n y_i \ell_i(x), \quad \ell_i(x) = \prod_{j\neq i} \frac{x - x_j}{x_i - x_j}
$$

**Newton 插值**（差商形式）：

$$
N_n(x) = f[x_0] + f[x_0,x_1](x-x_0) + \cdots + f[x_0,\ldots,x_n](x-x_0)\cdots(x-x_{n-1})
$$

**三次样条插值 (Cubic Spline)**：分段三次多项式，$C^2$ 连续。

**最小二乘拟合 (Least Squares)**：

$$
\min_{\mathbf{a}} \sum_{i=1}^n \left[ y_i - f(x_i, \mathbf{a}) \right]^2
$$

线性最小二乘的法方程：$(X^T X) \mathbf{a} = X^T \mathbf{y}$

### 数值积分 (Numerical Integration)

**Newton-Cotes 公式**：

| 方法 | 公式 | 误差阶 |
|------|------|--------|
| 梯形法则 | $\int_a^b f(x)dx \approx \frac{h}{2}[f(a) + f(b)]$ | $O(h^2)$ |
| Simpson 法则 | $\int_a^b f(x)dx \approx \frac{h}{3}[f(a) + 4f(m) + f(b)]$ | $O(h^4)$ |

**复合求积公式**：将区间划分为 $n$ 个子区间。

**Gauss 求积 (Gaussian Quadrature)**：

$$
\int_{-1}^1 f(x) dx \approx \sum_{i=1}^n w_i f(x_i)
$$

其中 $x_i$ 为 Legendre 多项式 $P_n(x)$ 的根，$w_i$ 为权重。

**Romberg 求积**：Richardson 外推加速。

### 常微分方程数值解 (ODE Solvers)

**初值问题 (IVP)**：$y' = f(t, y), \quad y(t_0) = y_0$

**单步法**：

| 方法 | 公式 | 局部截断误差 |
|------|------|-------------|
| Euler 法 | $y_{n+1} = y_n + h f(t_n, y_n)$ | $O(h^2)$ |
| 改进 Euler 法 | $k_1 = f(t_n, y_n), k_2 = f(t_n + h, y_n + hk_1)$ | $O(h^3)$ |
| 四阶 RK | 四级加权平均 | $O(h^5)$ |

**经典四阶 Runge-Kutta 方法**：

$$
\begin{aligned}
k_1 &= h f(t_n, y_n) \\
k_2 &= h f(t_n + h/2, y_n + k_1/2) \\
k_3 &= h f(t_n + h/2, y_n + k_2/2) \\
k_4 &= h f(t_n + h, y_n + k_3)
\end{aligned}
$$

$$
y_{n+1} = y_n + \frac{1}{6}(k_1 + 2k_2 + 2k_3 + k_4)
$$

**多步法**：

Adams-Bashforth 显式公式、Adams-Moulton 隐式公式（预测-校正系统）。

### 偏微分方程数值解 (PDE Solvers)

**有限差分法 (Finite Difference Method, FDM)**：

**扩散方程** $\frac{\partial u}{\partial t} = \alpha \frac{\partial^2 u}{\partial x^2}$ 的差分离散：

**向前 Euler 显式格式**：

$$
\frac{u_i^{n+1} - u_i^n}{\Delta t} = \alpha \frac{u_{i+1}^n - 2u_i^n + u_{i-1}^n}{\Delta x^2}
$$

**稳定性条件** (CFL 条件)：

$$
r = \frac{\alpha \Delta t}{\Delta x^2} \leq \frac{1}{2}
$$

**有限元法 (Finite Element Method, FEM)**：

**基本步骤**：

1. 将连续域离散为有限个单元
2. 选择形函数 (Shape Functions) 插值
3. 建立单元刚度矩阵 $K^e$
4. 组装总体刚度矩阵 $K$
5. 引入边界条件，求解 $K\mathbf{u} = \mathbf{f}$

## 经典教材

- 李庆扬《数值分析》
- 同济大学《数值方法》
- Burden & Faires《Numerical Analysis》
- Atkinson《An Introduction to Numerical Analysis》

## 主要应用领域

- 计算流体动力学 (CFD) 数值模拟
- 结构有限元分析 (FEA)
- 电磁场数值计算
- 多物理场耦合仿真
- 工程数据拟合与预报
- 最优控制数值求解

## 相关条目

- [[OperationsResearch]]
- [[EngineeringMathematics]]
- [[ComputationalFluidDynamics]]
- [[FiniteElementAnalysis]]
- [[11_ManagementSciences/ManagementScienceAndEngineering/OptimizationMethods|OptimizationMethods]]


