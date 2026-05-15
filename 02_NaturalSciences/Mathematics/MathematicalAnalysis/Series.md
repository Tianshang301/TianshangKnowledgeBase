---
aliases: [Series]
tags: ['Mathematics', 'MathematicalAnalysis', 'Series']
---

# 级数详解



## 一、数��?(Sequences)



### 极限



数列 $\{a_n\}$ 收敛��?$L$，记��?$\lim_{n \to \infty} a_n = L$，如果对任意 $\varepsilon > 0$，存��?$N \in \mathbb{N}$，使得当 $n > N$ 时有 $|a_n - L| < \varepsilon$��?

### 单调收敛定理



单调有界数列必收敛��?

## 二、级��?(Series)



### 部分和与收敛



级数 $\sum_{n=1}^\infty a_n$ 收敛当且仅当部分和序��?$\{S_n\}$ 收敛，其中：



$$S_n = \sum_{k=1}^n a_k$$



**几何级数��?* $\sum_{n=0}^\infty ar^n = \frac{a}{1-r}$，当 $|r| < 1$ 时收敛��?

**$p$-级数��?* $\sum_{n=1}^\infty \frac{1}{n^p}$ ��?$p > 1$ 时收敛，$p \leq 1$ 时发散��?

## 三、收敛性判别法



### 发散性检��?

��?$\lim_{n \to \infty} a_n \neq 0$，则 $\sum a_n$ 发散��?

### 收敛性判别法汇��?

| 判别��?| 条件 | 结论 |

|:---|:---|:---|

| 发散检��?| $\lim a_n \neq 0$ | 发散 |

| 积分��?| $f$ 连续正递减��?\int f$ 收敛 | 收敛 |

| 比较��?| $0 \le a_n \le b_n$��?\sum b_n$ 收敛 | $\sum a_n$ 收敛 |

| 比值法 | $\lim \|a_{n+1}/a_n\| = L$ | $L<1$收敛,$L>1$发散 |

| 根值法 | $\lim \sqrt[n]{\|a_n\|} = L$ | $L<1$收敛,$L>1$发散 |

| 交错级数 | $b_n$ 递减 $\to 0$ | 收敛 |

| 极限比较 | $\lim a_n/b_n = c>0$ | 同敛��?|



### 积分判别��?

��?$f$ ��?$[1, \infty)$ 上连续、正、递减，则 $\sum_{n=1}^\infty f(n)$ ��?$\int_1^\infty f(x) \, dx$ 同敛散��?

### 比较判别��?

��?$0 \leq a_n \leq b_n$ ��?$\sum b_n$ 收敛，则 $\sum a_n$ 收敛；若 $\sum a_n$ 发散，则 $\sum b_n$ 发散��?

### 极限比较判别��?

��?$\lim_{n \to \infty} \frac{a_n}{b_n} = c > 0$，则 $\sum a_n$ ��?$\sum b_n$ 同敛散��?

### 比值判别法 (Ratio Test)



$$\lim_{n \to \infty} \left|\frac{a_{n+1}}{a_n}\right| = L$$

- $L < 1$：绝对收��?- $L > 1$：发��?- $L = 1$：无法判��?

### 根值判别法 (Root Test)



$$\lim_{n \to \infty} \sqrt[n]{|a_n|} = L$$

- $L < 1$：绝对收��?- $L > 1$：发��?- $L = 1$：无法判��?

### 交错级数判别��?(Alternating Series Test)



��?$b_n$ 单调递减趋于 0，则交错级数 $\sum (-1)^{n-1} b_n$ 收敛��?

## 四、绝对收敛与条件收敛



- **绝对收敛**��?\sum |a_n|$ 收敛

- **条件收敛**��?\sum a_n$ 收敛��?$\sum |a_n|$ 发散



## 五、幂级数 (Power Series)



### 形式



$$\sum_{n=0}^\infty c_n (x - a)^n$$



### 收敛半径与收敛区��?

收敛半径 $R$ 由根值法或比值法求得��?

$$\frac{1}{R} = \limsup_{n \to \infty} \sqrt[n]{|c_n|} \quad \text{或} \quad \frac{1}{R} = \lim_{n \to \infty} \left|\frac{c_{n+1}}{c_n}\right|$$



收敛区间需检查端��?$x = a \pm R$ 处的收敛性��?

### 逐项求导与积��?

在收敛区间内��?$$\frac{d}{dx} \sum_{n=0}^\infty c_n (x-a)^n = \sum_{n=1}^\infty n c_n (x-a)^{n-1}$$

$$\int \sum_{n=0}^\infty c_n (x-a)^n \, dx = \sum_{n=0}^\infty \frac{c_n}{n+1} (x-a)^{n+1} + C$$



## 六、泰勒级数与麦克劳林级数



### 泰勒级数



$$f(x) = \sum_{n=0}^\infty \frac{f^{(n)}(a)}{n!} (x - a)^n$$



### 麦克劳林级数



$$f(x) = \sum_{n=0}^\infty \frac{f^{(n)}(0)}{n!} x^n$$



### 常见展开



$$e^x = \sum_{n=0}^\infty \frac{x^n}{n!} = 1 + x + \frac{x^2}{2!} + \frac{x^3}{3!} + \cdots, \quad x \in \mathbb{R}$$



$$\sin x = \sum_{n=0}^\infty \frac{(-1)^n x^{2n+1}}{(2n+1)!} = x - \frac{x^3}{3!} + \frac{x^5}{5!} - \cdots, \quad x \in \mathbb{R}$$



$$\cos x = \sum_{n=0}^\infty \frac{(-1)^n x^{2n}}{(2n)!} = 1 - \frac{x^2}{2!} + \frac{x^4}{4!} - \cdots, \quad x \in \mathbb{R}$$



$$\ln(1+x) = \sum_{n=1}^\infty \frac{(-1)^{n-1} x^n}{n} = x - \frac{x^2}{2} + \frac{x^3}{3} - \cdots, \quad -1 < x \leq 1$$



$$(1+x)^\alpha = \sum_{n=0}^\infty \binom{\alpha}{n} x^n = 1 + \alpha x + \frac{\alpha(\alpha-1)}{2!} x^2 + \cdots, \quad |x| < 1$$



## 七、傅里叶级数 (Fourier Series)



### 正交函数��?

函数��?$\{1, \cos(nx), \sin(nx)\}_{n=1}^\infty$ ��?$[-\pi, \pi]$ 上正交��?

### 傅里叶系��?

$$f(x) \sim \frac{a_0}{2} + \sum_{n=1}^\infty \left( a_n \cos(nx) + b_n \sin(nx) \right)$$



$$a_0 = \frac{1}{\pi} \int_{-\pi}^{\pi} f(x) \, dx$$

$$a_n = \frac{1}{\pi} \int_{-\pi}^{\pi} f(x) \cos(nx) \, dx, \ n \geq 1$$

$$b_n = \frac{1}{\pi} \int_{-\pi}^{\pi} f(x) \sin(nx) \, dx, \ n \geq 1$$



### 收敛性（狄利克雷条件��?

��?$f$ ��?$[-\pi, \pi]$ 上分段连续且分段光滑，则傅里叶级数在连续点处收敛��?$f(x)$，在跳跃间断点处收敛到左右极限的平均值��?

### 复数形式



$$f(x) = \sum_{n=-\infty}^\infty c_n e^{inx}, \quad c_n = \frac{1}{2\pi} \int_{-\pi}^{\pi} f(x) e^{-inx} \, dx$$



### Parseval定理



$$\frac{1}{2\pi} \int_{-\pi}^{\pi} |f(x)|^2 dx = \sum_{n=-\infty}^{\infty} |c_n|^2 = \frac{a_0^2}{4} + \frac{1}{2}\sum_{n=1}^{\infty} (a_n^2 + b_n^2)$$



### Cauchy乘积



两个级数的乘积：

$$\left(\sum_{n=0}^{\infty} a_n\right) \left(\sum_{n=0}^{\infty} b_n\right) = \sum_{n=0}^{\infty} c_n, \quad c_n = \sum_{k=0}^{n} a_k b_{n-k}$$



## 相关条目



[[02_NaturalSciences/Mathematics/Algebra/INDEX|Algebra]], [[02_NaturalSciences/Mathematics/DifferentialEquations/INDEX|DifferentialEquations]], [[02_NaturalSciences/Mathematics/Geometry/INDEX|Geometry]], RealAnalysis

