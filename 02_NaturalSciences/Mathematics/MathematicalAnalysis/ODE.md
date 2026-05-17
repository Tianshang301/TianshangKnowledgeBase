---
aliases:
  - 常微分方程
  - Ordinary Differential Equations
  - ODE
  - 微分方程
  - 一阶 ODE
  - 拉普拉斯变换
tags:
  - mathematics
  - ODE
  - differential equations
  - Laplace transform
  - dynamical systems
  - first-order
---

# 常微分方程 (Ordinary Differential Equations)

## 概述 (Overview)

常微分方程 (ODE) 描述一个自变量下函数与其导数之间的关系。ODE 在物理、工程、生物、经济等领域有广泛应用，是建模动态系统的核心工具。本笔记覆盖从一阶 ODE 到线性系统、拉普拉斯变换方法以及数值解法，包含完整的求解流程和典型应用模型。

```mermaid
graph TD
  A[常微分方程 ODE] --> B[一阶 ODE First-Order]
  A --> C[高阶 ODE Higher-Order]
  A --> D[方程组 Systems]
  A --> E[拉普拉斯变换 Laplace]
  A --> F[数值方法 Numerical]
  B --> G[可分离 Separable<br/>dy/dx = g(x)h(y)]
  B --> H[线性 Linear<br/>y'+P(x)y = Q(x)]
  B --> I[恰当 Exact<br/>M dx + N dy = 0]
  B --> J[伯努利 Bernoulli<br/>y'+Py = Qy^n]
  B --> K[齐次型 Homogeneous<br/>y' = φ(y/x)]
  C --> L[常系数 Constant Coeff<br/>特征方程法]
  C --> M[变系数 Variable Coeff]
  C --> N[欧拉-柯西 Euler-Cauchy<br/>x^r 代入法]
  D --> O[线性系统 Linear Systems<br/>x'=Ax+f]
  D --> P[相平面 Phase Plane<br/>稳定性分析]
  E --> Q[变换表 Transform Table]
  E --> R[卷积 Convolution]
  E --> S[逆变换 Partial Fractions]
  F --> T[欧拉法 Euler<br/>O(h)]
  F --> U[龙格-库塔 RK4<br/>O(h^4)]
```

## 一阶常微分方程 (First-Order ODEs)

### 一般形式 (General Form)

$$
\frac{dy}{dx} = f(x, y)
$$

或写成微分形式：

$$
M(x, y) \, dx + N(x, y) \, dy = 0
$$

### 可分离方程 (Separable Equations)

形如 $dy/dx = g(x) \, h(y)$ 或 $M(x)N(y) dx + P(x)Q(y) dy = 0$：

$$
\int \frac{dy}{h(y)} = \int g(x) \, dx + C
$$

### 一阶线性方程 (First-Order Linear ODEs)

标准形式：

$$
\frac{dy}{dx} + P(x) y = Q(x)
$$

**积分因子 (Integrating Factor)**：

$$
\mu(x) = e^{\int P(x) \, dx}
$$

通解公式：

$$
y = \frac{1}{\mu(x)} \int \mu(x) Q(x) \, dx
$$

### 恰当方程 (Exact Equations)

若 $M(x, y) \, dx + N(x, y) \, dy = 0$ 满足 $\frac{\partial M}{\partial y} = \frac{\partial N}{\partial x}$，则存在势函数 $\psi(x, y)$ 使得 $d\psi = M \, dx + N \, dy$，通解为 $\psi(x, y) = C$。势函数可通过线积分求出：$\psi(x, y) = \int M \, dx + \int \left(N - \frac{\partial}{\partial y} \int M \, dx\right) dy$。

若方程不恰当，可寻找**积分因子** $\mu(x)$ 或 $\mu(y)$ 使其恰当。常见情况：

- 若 $\frac{M_y - N_x}{N}$ 仅为 $x$ 的函数，则 $\mu(x) = e^{\int \frac{M_y - N_x}{N} dx}$
- 若 $\frac{N_x - M_y}{M}$ 仅为 $y$ 的函数，则 $\mu(y) = e^{\int \frac{N_x - M_y}{M} dy}$

### 伯努利方程 (Bernoulli Equation)

$$
\frac{dy}{dx} + P(x) y = Q(x) y^n,\quad n \neq 0, 1
$$

令 $u = y^{1-n}$，则 $\frac{du}{dx} + (1 - n) P(x) u = (1 - n) Q(x)$，化为线性方程。

### 齐次方程 (Homogeneous Equations)

若 $f(x, y) = \phi(y/x)$，令 $u = y/x$，则 $y = ux$，$dy/dx = u + x \, du/dx$，化为可分离方程。

## 二阶常系数线性方程 (Second-Order Linear with Constant Coefficients)

### 齐次方程 (Homogeneous Equation)

$$
a y'' + b y' + c y = 0
$$

特征方程 $a r^2 + b r + c = 0$：

| 判别式 $\Delta$ | 根的情况 | 通解形式 |
|---|---|---|
| $\Delta > 0$ | 两个不等实根 $r_1 \neq r_2$ | $y = C_1 e^{r_1 x} + C_2 e^{r_2 x}$ |
| $\Delta = 0$ | 重根 $r_1 = r_2 = r$ | $y = (C_1 + C_2 x) e^{r x}$ |
| $\Delta < 0$ | 共轭复根 $r = \alpha \pm i\beta$ | $y = e^{\alpha x}(C_1 \cos \beta x + C_2 \sin \beta x)$ |

### 非齐次方程 (Nonhomogeneous Equation)

$$
a y'' + b y' + c y = f(x)
$$

通解 = 齐次解 + 特解。

**待定系数法 (Undetermined Coefficients)**：

| $f(x)$ | 特解形式 |
|---|---|
| $P_n(x)$ | $x^s Q_n(x)$ |
| $P_n(x) e^{\alpha x}$ | $x^s Q_n(x) e^{\alpha x}$ |
| $P_n(x) e^{\alpha x} \sin \beta x$ | $x^s e^{\alpha x}[Q_n(x) \cos \beta x + R_n(x) \sin \beta x]$ |

其中 $s$ 为使特解不与齐次解线性相关的重数（0, 1, 或 2）。

**参数变易法 (Variation of Parameters)**：

$$
y_p = -y_1 \int \frac{y_2 f}{W} \, dx + y_2 \int \frac{y_1 f}{W} \, dx,\quad W = y_1 y_2' - y_2 y_1'
$$

## 常微分方程组 (Systems of ODEs)

### 线性系统 (Linear Systems)

齐次系统 $\mathbf{x}' = A \mathbf{x}$ 的解由特征值和特征向量决定：

- 相异实特征值：$\mathbf{x} = c_1 \mathbf{v}_1 e^{\lambda_1 t} + \cdots + c_n \mathbf{v}_n e^{\lambda_n t}$
- 重特征值：需要广义特征向量 (generalized eigenvectors)

### 相平面分析 (Phase Plane Analysis)

| 特征值 | 平衡点类型 | 稳定性 |
|---|---|---|
| 两负实根 | 稳定结点 (Stable Node) | 渐近稳定 |
| 两正实根 | 不稳定结点 (Unstable Node) | 不稳定 |
| 一正一负 | 鞍点 (Saddle Point) | 不稳定 |
| 负实部复根 | 稳定焦点 (Stable Spiral) | 渐近稳定 |
| 正实部复根 | 不稳定焦点 (Unstable Spiral) | 不稳定 |
| 纯虚根 | 中心 (Center) | 稳定（非渐近） |

## 拉普拉斯变换 (Laplace Transform)

### 定义 (Definition)

$$
\mathcal{L}\{f(t)\} = F(s) = \int_0^\infty e^{-st} f(t) \, dt
$$

### 重要变换表 (Important Transforms)

| $f(t)$ | $F(s)$ | 收敛域 |
|---|---|---|
| $1$ | $\frac{1}{s}$ | $\operatorname{Re}(s) > 0$ |
| $t^n$ | $\frac{n!}{s^{n+1}}$ | $\operatorname{Re}(s) > 0$ |
| $e^{at}$ | $\frac{1}{s - a}$ | $\operatorname{Re}(s) > a$ |
| $\sin(at)$ | $\frac{a}{s^2 + a^2}$ | $\operatorname{Re}(s) > 0$ |
| $\cos(at)$ | $\frac{s}{s^2 + a^2}$ | $\operatorname{Re}(s) > 0$ |
| $t^n e^{at}$ | $\frac{n!}{(s - a)^{n+1}}$ | $\operatorname{Re}(s) > a$ |
| $\delta(t - a)$ | $e^{-as}$ | 全平面 |
| $u(t - a)$ | $\frac{e^{-as}}{s}$ | $\operatorname{Re}(s) > 0$ |
| $\sinh(at)$ | $\frac{a}{s^2 - a^2}$ | $\operatorname{Re}(s) > |a|$ |
| $\cosh(at)$ | $\frac{s}{s^2 - a^2}$ | $\operatorname{Re}(s) > |a|$ |
| $e^{at} \sin(bt)$ | $\frac{b}{(s - a)^2 + b^2}$ | $\operatorname{Re}(s) > a$ |
| $e^{at} \cos(bt)$ | $\frac{s - a}{(s - a)^2 + b^2}$ | $\operatorname{Re}(s) > a$ |

### 导数变换 (Derivative Transforms)

$$
\mathcal{L}\{f'(t)\} = sF(s) - f(0),\quad \mathcal{L}\{f''(t)\} = s^2 F(s) - s f(0) - f'(0)
$$

### 卷积 (Convolution)

$$
(f * g)(t) = \int_0^t f(\tau) g(t - \tau) \, d\tau,\quad \mathcal{L}\{f * g\} = F(s) G(s)
$$

## 数值方法 (Numerical Methods)

| 方法 | 公式 | 局部截断误差 |
|---|---|---|
| 欧拉法 (Euler) | $y_{n+1} = y_n + h f(x_n, y_n)$ | $O(h^2)$ |
| 改进欧拉 (Heun) | $y_{n+1} = y_n + \frac{h}{2}(k_1 + k_2)$ | $O(h^3)$ |
| 经典 RK4 | $y_{n+1} = y_n + \frac{h}{6}(k_1 + 2k_2 + 2k_3 + k_4)$ | $O(h^5)$ |

## 应用 (Applications)

| 模型 | 方程 | 参数 |
|---|---|---|
| 牛顿冷却 (Newton's Law of Cooling) | $dT/dt = -k(T - T_e)$ | $k$: 冷却系数 |
| RC 电路 | $R dQ/dt + Q/C = V(t)$ | $R$: 电阻, $C$: 电容 |
| 简谐振动 (Simple Harmonic Motion) | $m x'' + k x = 0$ | $m$: 质量, $k$: 劲度系数 |
| 受迫振动 (Forced Oscillation) | $m x'' + c x' + k x = F_0 \cos \omega t$ | $c$: 阻尼系数 |
| Logistic 增长 | $dP/dt = rP(1 - P/K)$ | $r$: 增长率, $K$: 环境容量 |
| RLC 电路 | $L I'' + R I' + I/C = V'(t)$ | $L$: 电感, $R$: 电阻 |
