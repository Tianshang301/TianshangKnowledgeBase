# 甯稿井鍒嗘柟绋嬭瑙?
## 涓€銆佷竴闃?ODE

### 鍙垎绂诲彉閲?
$$\frac{dy}{dx} = g(x)h(y) \implies \int \frac{dy}{h(y)} = \int g(x) \, dx + C$$

### 涓€闃剁嚎鎬ф柟绋?
$$\frac{dy}{dx} + P(x)y = Q(x)$$

绉垎鍥犲瓙锛?\mu(x) = e^{\int P(x) \, dx}$

瑙ｏ細$y(x) = \frac{1}{\mu(x)} \int \mu(x) Q(x) \, dx$

### 鎭板綋鏂圭▼

$$M(x,y) \, dx + N(x,y) \, dy = 0$$

婊¤冻 $\frac{\partial M}{\partial y} = \frac{\partial N}{\partial x}$ 鏃朵负鎭板綋鏂圭▼锛屽瓨鍦ㄥ娍鍑芥暟 $\psi(x,y)$ 浣垮緱 $d\psi = M dx + N dy$銆?
### 浼姫鍒╂柟绋?
$$\frac{dy}{dx} + P(x)y = Q(x)y^n$$

浠?$u = y^{1-n}$锛屽寲涓虹嚎鎬ф柟绋嬨€?
## 浜屻€佷簩闃剁嚎鎬?ODE

### 榻愭甯哥郴鏁版柟绋?
$$ay'' + by' + cy = 0$$

鐗瑰緛鏂圭▼锛?ar^2 + br + c = 0$

- 涓や笉鍚屽疄鏍?$r_1 \neq r_2$锛?y = c_1 e^{r_1 x} + c_2 e^{r_2 x}$
- 閲嶆牴 $r_1 = r_2 = r$锛?y = (c_1 + c_2 x) e^{rx}$
- 鍏辫江澶嶆牴 $r = \alpha \pm i\beta$锛?y = e^{\alpha x}(c_1 \cos\beta x + c_2 \sin\beta x)$

### 闈為綈娆℃柟绋?
$$ay'' + by' + cy = f(x)$$

瑙?= 榻愭瑙?+ 鐗硅В

**寰呭畾绯绘暟娉曪細**

| $f(x)$ 褰㈠紡 | 鐗硅В褰㈠紡 |
|---|---|
| $P_n(x)$ | $x^s Q_n(x)$ |
| $P_n(x) e^{\alpha x}$ | $x^s Q_n(x) e^{\alpha x}$ |
| $P_n(x) \cos\beta x$ 鎴?$P_n(x) \sin\beta x$ | $x^s [Q_n(x) \cos\beta x + R_n(x) \sin\beta x]$ |

鍏朵腑 $s$ 涓虹壒寰佹牴涓?$f(x)$ 鎸囨暟閮ㄥ垎閲嶅悎鐨勬鏁般€?
**鍙傛暟鍙樻槗娉曪細** 璁?$y_p = u_1 y_1 + u_2 y_2$锛屽叾涓?$y_1, y_2$ 涓洪綈娆¤В銆?
$$u_1' = -\frac{y_2 f}{W(y_1, y_2)}, \quad u_2' = \frac{y_1 f}{W(y_1, y_2)}$$

$W$ 涓烘湕鏂熀琛屽垪寮忋€?
### 娆ф媺-鏌タ鏂圭▼

$$ax^2 y'' + bxy' + cy = 0$$

璁?$y = x^r$锛屽緱杈呭姪鏂圭▼ $ar(r-1) + br + c = 0$銆?
## 涓夈€佺骇鏁拌В娉?
### 甯哥偣澶?
鍦?$x = x_0$ 涓哄父鐐规椂锛岃 $y = \sum_{n=0}^\infty c_n (x - x_0)^n$銆?
### 姝ｅ垯濂囩偣 - Frobenius 鏂规硶

鍦?$x = x_0$ 涓烘鍒欏鐐规椂锛岃 $y = (x - x_0)^r \sum_{n=0}^\infty c_n (x - x_0)^n$銆?
鎸囨爣鏂圭▼鐢辨渶浣庡箓娆￠」绯绘暟涓洪浂寰楀埌銆?
## 鍥涖€丱DE 绯荤粺

### 绾挎€х郴缁?
$$\mathbf{x}' = A\mathbf{x}$$

瑙ｏ細$\mathbf{x}(t) = c_1 \mathbf{v}_1 e^{\lambda_1 t} + c_2 \mathbf{v}_2 e^{\lambda_2 t}$

### 鐭╅樀鎸囨暟

$$e^{At} = I + At + \frac{A^2 t^2}{2!} + \frac{A^3 t^3}{3!} + \cdots$$

瑙ｏ細$\mathbf{x}(t) = e^{At} \mathbf{x}(0)$

**绀轰緥锛?*
$$A = \begin{pmatrix} 0 & 1 \\ -1 & 0 \end{pmatrix}, \ e^{At} = \begin{pmatrix} \cos t & \sin t \\ -\sin t & \cos t \end{pmatrix}$$

## 浜斻€佹媺鏅媺鏂彉鎹?
### 瀹氫箟

$$\mathcal{L}\{f(t)\} = F(s) = \int_0^\infty e^{-st} f(t) \, dt$$

### 閲嶈鎬ц川

$$\mathcal{L}\{f'(t)\} = sF(s) - f(0)$$
$$\mathcal{L}\{f''(t)\} = s^2 F(s) - sf(0) - f'(0)$$
$$\mathcal{L}\{e^{at} f(t)\} = F(s - a)$$
$$\mathcal{L}\{t^n\} = \frac{n!}{s^{n+1}}, \quad \mathcal{L}\{\sin at\} = \frac{a}{s^2 + a^2}, \quad \mathcal{L}\{\cos at\} = \frac{s}{s^2 + a^2}$$

### 姹傝В ODE

灏?ODE 鍙樻崲涓轰唬鏁版柟绋嬶紝瑙ｅ嚭 $Y(s)$锛屽啀姹傞€嗗彉鎹€?
## 鍏€佹暟鍊兼柟娉?
### 娆ф媺娉?
$$y_{n+1} = y_n + h f(x_n, y_n)$$

### 鍥涢樁榫欐牸-搴撳娉?(RK4)

$$y_{n+1} = y_n + \frac{h}{6}(k_1 + 2k_2 + 2k_3 + k_4)$$
$$k_1 = f(x_n, y_n)$$
$$k_2 = f(x_n + \frac{h}{2}, y_n + \frac{h}{2}k_1)$$
$$k_3 = f(x_n + \frac{h}{2}, y_n + \frac{h}{2}k_2)$$
$$k_4 = f(x_n + h, y_n + h k_3)$$

**Python 绀轰緥锛?*
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

## 鐩稿叧鏉＄洰

[[02_NaturalSciences/Mathematics/Algebra/INDEX|Algebra]], [[02_NaturalSciences/Mathematics/DifferentialEquations/INDEX|DifferentialEquations]], [[02_NaturalSciences/Mathematics/Geometry/INDEX|Geometry]], RealAnalysis
