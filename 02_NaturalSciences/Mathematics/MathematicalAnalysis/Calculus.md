# 微积分详��?
## 一、极��?(Limits)

### ε-δ 定义

函数 $f(x)$ ��?$x \to a$ 时的极限��?$L$，记��?$\lim_{x \to a} f(x) = L$，如果对任意 $\varepsilon > 0$，存��?$\delta > 0$，使得当 $0 < |x - a| < \delta$ 时，��?$|f(x) - L| < \varepsilon$��?
$$\forall \varepsilon > 0, \ \exists \delta > 0 \ \text{s.t.} \ 0 < |x-a| < \delta \implies |f(x)-L| < \varepsilon$$

### 极限法则

��?$\lim_{x \to a} f(x) = L$��?\lim_{x \to a} g(x) = M$，则��?
$$\lim_{x \to a} [f(x) \pm g(x)] = L \pm M$$
$$\lim_{x \to a} [f(x)g(x)] = LM$$
$$\lim_{x \to a} \frac{f(x)}{g(x)} = \frac{L}{M}, \ (M \neq 0)$$
$$\lim_{x \to a} [f(x)]^n = L^n, \ n \in \mathbb{Z}^+$$

### 夹逼定��?(Squeeze Theorem)

若在 $a$ 的某去心邻域内有 $g(x) \leq f(x) \leq h(x)$，且 $\lim_{x \to a} g(x) = \lim_{x \to a} h(x) = L$，则 $\lim_{x \to a} f(x) = L$��?
**重要极限��?*

$$\lim_{x \to 0} \frac{\sin x}{x} = 1, \quad \lim_{x \to 0} \frac{1 - \cos x}{x} = 0, \quad \lim_{x \to \infty} \left(1 + \frac{1}{x}\right)^x = e$$

## 二、连续��?(Continuity)

### 定义

$f(x)$ ��?$x = a$ 处连续当且仅当：

$$\lim_{x \to a} f(x) = f(a)$$

### 间断点类��?
- **可去间断��?*��?\lim_{x \to a} f(x)$ 存在��?$\neq f(a)$ ��?$f(a)$ 未定��?- **跳跃间断��?*：左右极限存在但不相��?- **无穷间断��?*��?\lim_{x \to a} f(x) = \pm \infty$
- **振荡间断��?*：极限不存在（如 $\sin(1/x)$ ��?$x=0$��?
### 介值定��?(Intermediate Value Theorem)

��?$f$ ��?$[a,b]$ 上连续，$f(a) \neq f(b)$，则��?$f(a)$ ��?$f(b)$ 之间的任意��?$k$，存��?$c \in (a,b)$ 使得 $f(c) = k$��?
## 三、导��?(Derivatives)

### 定义

$$f'(x) = \lim_{h \to 0} \frac{f(x+h) - f(x)}{h}$$

### 求导法则

| 法则 | 公式 |
|:---|:---|
| 常数��?| $(cf)' = cf'$ |
| 和差 | $(f \pm g)' = f' \pm g'$ |
| 乘积 | $(fg)' = f'g + fg'$ |
| ��?| $\left(\frac{f}{g}\right)' = \frac{f'g - fg'}{g^2}$ |
| 链式 | $\frac{d}{dx} f(g(x)) = f'(g(x)) g'(x)$ |
| 反函��?| $(f^{-1})'(x) = \frac{1}{f'(f^{-1}(x))}$ |
| 隐函��?| ��?$F(x,y)=0$ 两边求导��?y$ 视为 $y(x)$ |

### 常用导数公式

$$\frac{d}{dx} x^n = nx^{n-1}, \quad \frac{d}{dx} e^x = e^x, \quad \frac{d}{dx} \ln x = \frac{1}{x}$$
$$\frac{d}{dx} \sin x = \cos x, \quad \frac{d}{dx} \cos x = -\sin x, \quad \frac{d}{dx} \tan x = \sec^2 x$$
$$\frac{d}{dx} \arcsin x = \frac{1}{\sqrt{1-x^2}}, \quad \frac{d}{dx} \arctan x = \frac{1}{1+x^2}$$

## 四、导数的应用

### 极值定��?(Extreme Value Theorem)

��?$f$ ��?$[a,b]$ 上连续，��?$f$ ��?$[a,b]$ 上取得最大值和最小值��?
### 中值定��?(Mean Value Theorem)

��?$f$ ��?$[a,b]$ 上连续，��?$(a,b)$ 内可导，则存��?$c \in (a,b)$ 使得��?
$$f'(c) = \frac{f(b) - f(a)}{b - a}$$

**罗尔定理��?* ��?$f(a) = f(b)$，则存在 $c \in (a,b)$ 使得 $f'(c) = 0$��?
### Taylor定理（带余项��?
$$f(x) = \sum_{k=0}^n \frac{f^{(k)}(a)}{k!}(x-a)^k + R_n(x)$$

**Lagrange余项**��?$$R_n(x) = \frac{f^{(n+1)}(\xi)}{(n+1)!}(x-a)^{n+1}, \quad \xi \in (a, x)$$

### 洛必达法��?(L'Hôpital's Rule)

��?$\lim_{x \to a} \frac{f(x)}{g(x)}$ ��?$\frac{0}{0}$ ��?$\frac{\infty}{\infty}$ 型，��?$\lim_{x \to a} \frac{f'(x)}{g'(x)}$ 存在，则��?
$$\lim_{x \to a} \frac{f(x)}{g(x)} = \lim_{x \to a} \frac{f'(x)}{g'(x)}$$

### 曲线绘制

- **临界��?*��?f'(x) = 0$ ��?$f'(x)$ 不存��?- **拐点**��?f''(x) = 0$ 且左右凹凸性改��?- **渐近��?*：水平渐近线 $\lim_{x \to \pm\infty} f(x) = L$；垂直渐近线 $\lim_{x \to a} f(x) = \pm\infty$

## 五、积��?(Integrals)

### 黎曼��?(Riemann Sum)

$$\int_a^b f(x) \, dx = \lim_{n \to \infty} \sum_{i=1}^n f(x_i^*) \Delta x, \quad \Delta x = \frac{b-a}{n}$$

### 微积分基本定��?(Fundamental Theorem of Calculus)

**FTC Part 1��?* ��?$F(x) = \int_a^x f(t) \, dt$，则 $F'(x) = f(x)$��?
$$\frac{d}{dx} \int_a^x f(t) \, dt = f(x)$$

**FTC Part 2��?* ��?$F' = f$，则��?
$$\int_a^b f(x) \, dx = F(b) - F(a)$$

### 基本积分��?
| 函数 | 原函��?|
|:---|:---|
| $x^n$ | $\frac{x^{n+1}}{n+1}+C,\ n\neq -1$ |
| $1/x$ | $\ln\|x\|+C$ |
| $e^x$ | $e^x+C$ |
| $a^x$ | $a^x/\ln a+C$ |
| $\sin x$ | $-\cos x+C$ |
| $\cos x$ | $\sin x+C$ |
| $\sec^2 x$ | $\tan x+C$ |
| $\frac{1}{\sqrt{1-x^2}}$ | $\arcsin x+C$ |
| $\frac{1}{1+x^2}$ | $\arctan x+C$ |

### 积分技��?
**换元法：**
$$\int f(g(x)) g'(x) \, dx = \int f(u) \, du, \ u = g(x)$$

**分部积分法：**
$$\int u \, dv = uv - \int v \, du$$

**部分分式分解��?* 将有理函数分解为简单分式之和再积分��?
**三角换元��?*
- $\sqrt{a^2 - x^2}$：令 $x = a\sin\theta$
- $\sqrt{a^2 + x^2}$：令 $x = a\tan\theta$
- $\sqrt{x^2 - a^2}$：令 $x = a\sec\theta$

## 六、反常积��?(Improper Integrals)

**无穷限：** $\int_a^\infty f(x) \, dx = \lim_{b \to \infty} \int_a^b f(x) \, dx$

**无界函数��?* $\int_a^b f(x) \, dx = \lim_{c \to a^+} \int_c^b f(x) \, dx$��?x=a$ 为瑕点）

## 七、积分的应用

**面积��?* $A = \int_a^b [f(x) - g(x)] \, dx$

**体积（圆盘法）：** $V = \pi \int_a^b [R(x)]^2 \, dx$

**体积（壳法）��?* $V = 2\pi \int_a^b x f(x) \, dx$

**弧长��?* $s = \int_a^b \sqrt{1 + [f'(x)]^2} \, dx$

**旋转曲面面积��?* $S = 2\pi \int_a^b f(x) \sqrt{1 + [f'(x)]^2} \, dx$

## 相关条目

[[02_NaturalSciences/Mathematics/Algebra/INDEX|Algebra]], [[02_NaturalSciences/Mathematics/DifferentialEquations/INDEX|DifferentialEquations]], [[02_NaturalSciences/Mathematics/Geometry/INDEX|Geometry]], RealAnalysis
