---
aliases: [ODE]
tags: ['Mathematics', 'MathematicalAnalysis', 'ODE']
---

# 常微分方程详��?

## 一、一��?ODE



### 可分离变��?

$$\frac{dy}{dx} = g(x)h(y) \implies \int \frac{dy}{h(y)} = \int g(x) \, dx + C$$



### 一阶线性方��?

$$\frac{dy}{dx} + P(x)y = Q(x)$$



积分因子��?\mu(x) = e^{\int P(x) \, dx}$



解：$y(x) = \frac{1}{\mu(x)} \int \mu(x) Q(x) \, dx$



### 恰当方程



$$M(x,y) \, dx + N(x,y) \, dy = 0$$



满足 $\frac{\partial M}{\partial y} = \frac{\partial N}{\partial x}$ 时为恰当方程，存在势函数 $\psi(x,y)$ 使得 $d\psi = M dx + N dy$��?

### 伯努利方��?

$$\frac{dy}{dx} + P(x)y = Q(x)y^n$$



��?$u = y^{1-n}$，化为线性方程��?

## 二、二阶线��?ODE



### 齐次常系数方��?

$$ay'' + by' + cy = 0$$



特征方程��?ar^2 + br + c = 0$



- 两不同实��?$r_1 \neq r_2$��?y = c_1 e^{r_1 x} + c_2 e^{r_2 x}$

- 重根 $r_1 = r_2 = r$��?y = (c_1 + c_2 x) e^{rx}$

- 共轭复根 $r = \alpha \pm i\beta$��?y = e^{\alpha x}(c_1 \cos\beta x + c_2 \sin\beta x)$



### 非齐次方��?

$$ay'' + by' + cy = f(x)$$



��?= 齐次��?+ 特解



**待定系数法：**



| $f(x)$ 形式 | 特解形式 |

|---|---|

| $P_n(x)$ | $x^s Q_n(x)$ |

| $P_n(x) e^{\alpha x}$ | $x^s Q_n(x) e^{\alpha x}$ |

| $P_n(x) \cos\beta x$ ��?$P_n(x) \sin\beta x$ | $x^s [Q_n(x) \cos\beta x + R_n(x) \sin\beta x]$ |



其中 $s$ 为特征根��?$f(x)$ 指数部分重合的次数��?

**参数变易法：** ��?$y_p = u_1 y_1 + u_2 y_2$，其��?$y_1, y_2$ 为齐次解��?

$$u_1' = -\frac{y_2 f}{W(y_1, y_2)}, \quad u_2' = \frac{y_1 f}{W(y_1, y_2)}$$



$W$ 为朗斯基行列式��?

### 欧拉-柯西方程



$$ax^2 y'' + bxy' + cy = 0$$



��?$y = x^r$，得辅助方程 $ar(r-1) + br + c = 0$��?

## 三、级数解��?

### 常点��?

��?$x = x_0$ 为常点时，设 $y = \sum_{n=0}^\infty c_n (x - x_0)^n$��?

### 正则奇点 - Frobenius 方法



��?$x = x_0$ 为正则奇点时，设 $y = (x - x_0)^r \sum_{n=0}^\infty c_n (x - x_0)^n$��?

指标方程由最低幂次项系数为零得到��?

## 四、ODE 系统



### 线性系��?

$$\mathbf{x}' = A\mathbf{x}$$



解：$\mathbf{x}(t) = c_1 \mathbf{v}_1 e^{\lambda_1 t} + c_2 \mathbf{v}_2 e^{\lambda_2 t}$



### 矩阵指数



$$e^{At} = I + At + \frac{A^2 t^2}{2!} + \frac{A^3 t^3}{3!} + \cdots$$



解：$\mathbf{x}(t) = e^{At} \mathbf{x}(0)$



**示例��?*

$$A = \begin{pmatrix} 0 & 1 \\ -1 & 0 \end{pmatrix}, \ e^{At} = \begin{pmatrix} \cos t & \sin t \\ -\sin t & \cos t \end{pmatrix}$$



## 五、拉普拉斯变��?

### 定义



$$\mathcal{L}\{f(t)\} = F(s) = \int_0^\infty e^{-st} f(t) \, dt$$



### 重要性质



$$\mathcal{L}\{f'(t)\} = sF(s) - f(0)$$

$$\mathcal{L}\{f''(t)\} = s^2 F(s) - sf(0) - f'(0)$$

$$\mathcal{L}\{e^{at} f(t)\} = F(s - a)$$

$$\mathcal{L}\{t^n\} = \frac{n!}{s^{n+1}}, \quad \mathcal{L}\{\sin at\} = \frac{a}{s^2 + a^2}, \quad \mathcal{L}\{\cos at\} = \frac{s}{s^2 + a^2}$$



### 求解 ODE



��?ODE 变换为代数方程，解出 $Y(s)$，再求逆变捃6�9�?

## 六、数值方��?

### 欧拉��?

$$y_{n+1} = y_n + h f(x_n, y_n)$$



### 四阶龙格-库塔��?(RK4)



$$y_{n+1} = y_n + \frac{h}{6}(k_1 + 2k_2 + 2k_3 + k_4)$$

$$k_1 = f(x_n, y_n)$$

$$k_2 = f(x_n + \frac{h}{2}, y_n + \frac{h}{2}k_1)$$

$$k_3 = f(x_n + \frac{h}{2}, y_n + \frac{h}{2}k_2)$$

$$k_4 = f(x_n + h, y_n + h k_3)$$



**Python 示例��?*

```python

def rk4(f, x0, y0, h, n):

    x, y = x0, y0

    xs, ys = [x], [y]

    for _ in range(n):

        k1 = f(x, y)

        k2 = f(x + h/2, y + h/2 * k1)

        k3 = f(x + h/2, y + h/2 * k2)

        k4 = f(x + h, y + h * k3)

        y = y + h/6 * (k1 + 2*k2 + 2*k3 + k4)

        x = x + h

        xs.append(x); ys.append(y)

    return xs, ys

```



## 相关条目



[[02_NaturalSciences/Mathematics/Algebra/INDEX|Algebra]], [[02_NaturalSciences/Mathematics/DifferentialEquations/INDEX|DifferentialEquations]], [[02_NaturalSciences/Mathematics/Geometry/INDEX|Geometry]], RealAnalysis

