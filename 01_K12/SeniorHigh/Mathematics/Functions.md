---
aliases: [Functions, 函数]
tags: ['SeniorHigh', 'Mathematics', 'Functions']
created: 2026-05-17
updated: 2026-05-13
---

# 高中数学 · 函数（完整版）

> 涵盖：函数概念、基本性质、指数函数、对数函数、幂函数、三角函数、抽象函数、复合函数、分段函数、反函数、图像变换、函数与方程

---

## 一、函数的概念与要素

### 1. 定义

设 $A$, $B$ 是非空数集，如果按照某种确定的对应关系 $f$，使对于集合 $A$ 中的任意一个数 $x$，在集合 $B$ 中都有唯一确定的数 $f(x)$ 和它对应，那么称 $f: A \to B$ 为从集合 $A$ 到集合 $B$ 的一个函数，记作 $y = f(x)$, $x \in A$。

### 2. 三要素

| 要素 | 定义 | 说明 |
|------|------|------|
| **定义域** | $x$ 的取值范围 | 分母 $\neq 0$；偶次根号下 $\ge 0$；对数真数 $> 0$；底数 $> 0$ 且 $\neq 1$ |
| **值域** | $y$ 的取值范围 | 由定义域和对应关系决定 |
| **对应关系** | $f$ 的作用规律 | 解析式、图像、表格等形式 |

### 3. 定义域求法

**常见限制**

- 分式：分母 $\neq 0$
- 偶次根式：被开方数 $\ge 0$
- 奇次根式：被开方数 $\in \mathbb{R}$
- 对数：真数 $> 0$；底数 $> 0$ 且 $\neq 1$
- 指数：底数 $> 0$（高考一般只考底数 $> 0$ 情形）
- 正切：$x \neq \frac{\pi}{2} + k\pi, k \in \mathbb{Z}$
- 实际问题：须符合实际意义

**例**：求 $f(x) = \sqrt{x+1} + \frac{1}{x-2}$ 定义域

解：$\{x \mid x \ge -1 \text{ 且 } x \neq 2\}$

### 4. 值域求法

- 直接观察法：一次函数
- 配方法：二次函数
- 分离常数法：分式函数
- 换元法：复合函数
- 单调性法：利用增减性
- 导数法：求极值（高三）

---

## 二、函数的性质

### 1. 单调性（增减性）

**定义**：对于定义域 $I$ 内某个区间 $D$ 上的任意两个自变量的值 $x_1$, $x_2$：

- 若 $x_1 < x_2$ 且 $f(x_1) < f(x_2)$，则 $f(x)$ 在 $D$ 上 **单调递增**
- 若 $x_1 < x_2$ 且 $f(x_1) > f(x_2)$，则 $f(x)$ 在 $D$ 上 **单调递减**

**判断方法**

| 方法 | 适用 | 操作 |
|------|------|------|
| 定义法 | 一切函数 | 作差比较 $f(x_1) - f(x_2)$ 符号 |
| 图像法 | 图像已知 | 从左到右上升/下降 |
| 导数法 | 可导函数 | $f'(x) > 0 \nearrow$，$f'(x) < 0 \searrow$ |
| 复合函数 | 内外函数 | 同增异减 |

**复合函数单调性（同增异减）**

| $y = f[g(x)]$ | $g(x) \nearrow$ | $g(x) \searrow$ |
|--------------|---------------|---------------|
| $f(u) \nearrow$ | $y \nearrow$ | $y \searrow$ |
| $f(u) \searrow$ | $y \searrow$ | $y \nearrow$ |

### 2. 奇偶性

**定义**

- **偶函数**：$f(-x) = f(x)$，图像关于 $y$ 轴对称
- **奇函数**：$f(-x) = -f(x)$，图像关于原点对称

**判断步骤**：

1. 检查定义域是否关于原点对称（不对称则非奇非偶）
2. 计算 $f(-x)$ 并与 $f(x)$ 比较

**常见函数奇偶性**

| 奇函数 | 偶函数 | 非奇非偶 |
|--------|--------|----------|
| $y = x^{\text{奇数}}$ | $y = x^{\text{偶数}}$ | $y = a^x\ (a>0,a\neq1)$ |
| $y = \sin x$ | $y = \cos x$ | $y = \log_a x\ (a>0,a\neq1)$ |
| $y = \tan x$ | $y = |x|$ | $y = x + 1$ |
| $y = \frac{1}{x}$ | $y = x^2$ | |
| $y = x^3$ | | |

**奇偶性运算**：奇 $\pm$ 奇 $=$ 奇；偶 $\pm$ 偶 $=$ 偶；奇 $\times$ 奇 $=$ 偶；偶 $\times$ 偶 $=$ 偶；奇 $\times$ 偶 $=$ 奇。

### 3. 周期性

**定义**：存在非零常数 $T$，使 $f(x + T) = f(x)$ 对定义域内任意 $x$ 恒成立，$T$ 为周期。

**常见周期函数**

| 函数 | 最小正周期 |
|------|-----------|
| $\sin x$, $\cos x$ | $2\pi$ |
| $\tan x$ | $\pi$ |
| $f(x) = -f(x+a)$ | $2a$ |
| $f(x+a) = \frac{1}{f(x)}$ | $2a$ |

### 4. 对称性

**轴对称**

- $f(a + x) = f(a - x)$ 关于 $x = a$ 对称
- $f(x) = f(2a - x)$ 关于 $x = a$ 对称
- 偶函数：关于 $x = 0$ 对称

**中心对称**

- $f(a + x) = -f(a - x)$ 关于 $(a, 0)$ 对称
- $f(x) = 2b - f(2a - x)$ 关于 $(a, b)$ 对称
- 奇函数：关于 $(0, 0)$ 对称

**对称性与周期性的关系**：

- 若 $f(x)$ 有两条对称轴 $x = a$ 和 $x = b$，则周期 $T = 2|a - b|$
- 若 $f(x)$ 有两个对称中心 $(a,0)$ 和 $(b,0)$，则周期 $T = 2|a - b|$
- 若 $f(x)$ 有一条对称轴 $x = a$ 和一个对称中心 $(b,0)$，则周期 $T = 4|a - b|$

---

## 三、基本初等函数

### 1. 一次函数 $y = kx + b\ (k \neq 0)$

- 斜率 $k$，纵截距 $b$
- $k > 0$ 递增，$k < 0$ 递减
- 定义域 $\mathbb{R}$，值域 $\mathbb{R}$

### 2. 二次函数

$f(x) = ax^2 + bx + c\ (a \neq 0)$

- **图像**：抛物线
- **顶点**：$(-\frac{b}{2a}, \frac{4ac - b^2}{4a})$
- **对称轴**：$x = -\frac{b}{2a}$
- **开口**：$a > 0$ 向上，$a < 0$ 向下
- **定义域**：$\mathbb{R}$
- **值域**：$a > 0$ 时 $[f(-\frac{b}{2a}), +\infty)$，$a < 0$ 时 $(-\infty, f(-\frac{b}{2a})]$
- **$\Delta$**：$\Delta = b^2 - 4ac$
  - $\Delta > 0$：两个不等实根
  - $\Delta = 0$：一个重根
  - $\Delta < 0$：无实根

### 3. 指数函数

$y = a^x\ (a > 0 \text{ 且 } a \neq 1)$

| 性质 | $a > 1$ | $0 < a < 1$ |
|------|---------|-------------|
| 图像 | 单调上升 | 单调下降 |
| 定义域 | $\mathbb{R}$ | $\mathbb{R}$ |
| 值域 | $(0, +\infty)$ | $(0, +\infty)$ |
| 过定点 | $(0, 1)$ | $(0, 1)$ |
| 单调性 | 递增 | 递减 |
| $x \to +\infty$ | $y \to +\infty$ | $y \to 0$ |
| $x \to -\infty$ | $y \to 0$ | $y \to +\infty$ |

**运算法则**：

- $a^m \times a^n = a^{m+n}$
- $a^m \div a^n = a^{m-n}$
- $(a^m)^n = a^{mn}$
- $(ab)^n = a^n \times b^n$
- $a^0 = 1$
- $a^{-n} = \frac{1}{a^n}$
- $a^{\frac{m}{n}} = \sqrt[n]{a^m}$

**注意**：底数 $a$ 必须 $> 0$ 且 $\neq 1$

### 4. 对数函数

$y = \log_a x\ (a > 0 \text{ 且 } a \neq 1)$

**定义**：若 $a^y = x$，则 $y = \log_a x$

| 性质 | $a > 1$ | $0 < a < 1$ |
|------|---------|-------------|
| 图像 | 单调上升 | 单调下降 |
| 定义域 | $(0, +\infty)$ | $(0, +\infty)$ |
| 值域 | $\mathbb{R}$ | $\mathbb{R}$ |
| 过定点 | $(1, 0)$ | $(1, 0)$ |
| 单调性 | 递增 | 递减 |
| $x \to +\infty$ | $y \to +\infty$ | $y \to -\infty$ |
| $x \to 0^+$ | $y \to -\infty$ | $y \to +\infty$ |

**运算法则**：

- $\log_a(MN) = \log_a M + \log_a N$
- $\log_a(\frac{M}{N}) = \log_a M - \log_a N$
- $\log_a(M^n) = n \cdot \log_a M$
- $\log_a(\sqrt[n]{M}) = \frac{1}{n} \cdot \log_a M$

**换底公式**：$\log_a b = \frac{\log_c b}{\log_c a} = \frac{1}{\log_b a}$

**重要关系**

- $\log_a 1 = 0$
- $\log_a a = 1$
- $a^{\log_a N} = N$（对数恒等式）
- 常用对数：$\lg x = \log_{10} x$
- 自然对数：$\ln x = \log_e x$，$e \approx 2.71828$

### 5. 幂函数 $y = x^\alpha$（$\alpha$ 为常数）

**常见幂函数图像特征**

| $\alpha$ 取值 | 图像特征 | 举例 |
|--------------|----------|------|
| $\alpha > 1$ | 过 $(0,0),(1,1)$，在 $(0,+\infty)$ 递增 | $y = x^2$, $y = x^3$ |
| $0 < \alpha < 1$ | 过 $(0,0),(1,1)$，在 $(0,+\infty)$ 递增但较缓 | $y = \sqrt{x}$ |
| $\alpha = 0$ | $y = 1\ (x \neq 0)$，常函数 | $y = 1$ |
| $\alpha < 0$ | 过 $(1,1)$，在 $(0,+\infty)$ 递减，以两轴为渐近线 | $y = x^{-1} = \frac{1}{x}$ |

**$\alpha$ 为有理数时的定义域**

- $\alpha = \frac{p}{q}$（既约分数）
- $q$ 为奇数：定义域 $\mathbb{R}$
- $q$ 为偶数：定义域 $[0, +\infty)$

---

## 四、三角函数（完整版）

### 1. 任意角与弧度制

- **弧度与角度互化**：$\pi \text{ rad} = 180^\circ$，$1 \text{ rad} = (\frac{180}{\pi})^\circ \approx 57.3^\circ$
- **弧长公式**：$l = |\alpha| \cdot r$
- **扇形面积**：$S = \frac{1}{2} \cdot l \cdot r = \frac{1}{2} \cdot \alpha \cdot r^2$

### 2. 三角函数定义

设角 $\alpha$ 终边上一点 $P(x, y)$，$OP = r = \sqrt{x^2 + y^2}$

$\sin \alpha = \frac{y}{r}$，$\cos \alpha = \frac{x}{r}$，$\tan \alpha = \frac{y}{x}\ (x \neq 0)$

$\cot \alpha = \frac{x}{y}\ (y \neq 0)$，$\sec \alpha = \frac{r}{x}\ (x \neq 0)$，$\csc \alpha = \frac{r}{y}\ (y \neq 0)$

### 3. 特殊角三角函数值

| 角度 | $0^\circ$ | $30^\circ$ | $45^\circ$ | $60^\circ$ | $90^\circ$ | $180^\circ$ | $270^\circ$ | $360^\circ$ |
|------|-----------|------------|------------|------------|------------|-------------|-------------|-------------|
| 弧度 | $0$ | $\frac{\pi}{6}$ | $\frac{\pi}{4}$ | $\frac{\pi}{3}$ | $\frac{\pi}{2}$ | $\pi$ | $\frac{3\pi}{2}$ | $2\pi$ |
| $\sin$ | $0$ | $\frac{1}{2}$ | $\frac{\sqrt{2}}{2}$ | $\frac{\sqrt{3}}{2}$ | $1$ | $0$ | $-1$ | $0$ |
| $\cos$ | $1$ | $\frac{\sqrt{3}}{2}$ | $\frac{\sqrt{2}}{2}$ | $\frac{1}{2}$ | $0$ | $-1$ | $0$ | $1$ |
| $\tan$ | $0$ | $\frac{\sqrt{3}}{3}$ | $1$ | $\sqrt{3}$ | 不存在 | $0$ | 不存在 | $0$ |

### 4. 诱导公式（六组）

**口诀**：奇变偶不变，符号看象限

| 公式 |
|------|
| $\sin(-\alpha) = -\sin \alpha$，$\cos(-\alpha) = \cos \alpha$，$\tan(-\alpha) = -\tan \alpha$（负角公式） |
| $\sin(\pi-\alpha) = \sin \alpha$，$\cos(\pi-\alpha) = -\cos \alpha$，$\tan(\pi-\alpha) = -\tan \alpha$ |
| $\sin(\pi+\alpha) = -\sin \alpha$，$\cos(\pi+\alpha) = -\cos \alpha$，$\tan(\pi+\alpha) = \tan \alpha$ |
| $\sin(2\pi-\alpha) = -\sin \alpha$，$\cos(2\pi-\alpha) = \cos \alpha$，$\tan(2\pi-\alpha) = -\tan \alpha$ |
| $\sin(\frac{\pi}{2}-\alpha) = \cos \alpha$，$\cos(\frac{\pi}{2}-\alpha) = \sin \alpha$（互余公式） |
| $\sin(\frac{\pi}{2}+\alpha) = \cos \alpha$，$\cos(\frac{\pi}{2}+\alpha) = -\sin \alpha$ |

### 5. 三角恒等变换

**同角关系**

- $\sin^2\alpha + \cos^2\alpha = 1$
- $\tan \alpha = \frac{\sin \alpha}{\cos \alpha}$
- $1 + \tan^2\alpha = \sec^2\alpha$
- $1 + \cot^2\alpha = \csc^2\alpha$

**和差公式**：

$\sin(\alpha \pm \beta) = \sin \alpha \cos \beta \pm \cos \alpha \sin \beta$

$\cos(\alpha \pm \beta) = \cos \alpha \cos \beta \mp \sin \alpha \sin \beta$

$\tan(\alpha \pm \beta) = \frac{\tan \alpha \pm \tan \beta}{1 \mp \tan \alpha \tan \beta}$

**二倍角公式**：

$\sin 2\alpha = 2 \sin \alpha \cos \alpha$

$\cos 2\alpha = \cos^2\alpha - \sin^2\alpha = 1 - 2 \sin^2\alpha = 2 \cos^2\alpha - 1$

$\tan 2\alpha = \frac{2 \tan \alpha}{1 - \tan^2\alpha}$

**降幂公式**：

$\sin^2\alpha = \frac{1 - \cos 2\alpha}{2}$

$\cos^2\alpha = \frac{1 + \cos 2\alpha}{2}$

**辅助角公式**：

$a \sin x + b \cos x = \sqrt{a^2 + b^2} \sin(x + \varphi)$，其中 $\tan \varphi = \frac{b}{a}$

### 6. 三角函数的图像与性质

| 函数 | $y = \sin x$ | $y = \cos x$ | $y = \tan x$ |
|------|-------------|-------------|-------------|
| 定义域 | $\mathbb{R}$ | $\mathbb{R}$ | $\{x \mid x \neq \frac{\pi}{2}+k\pi\}$ |
| 值域 | $[-1, 1]$ | $[-1, 1]$ | $\mathbb{R}$ |
| 周期 | $2\pi$ | $2\pi$ | $\pi$ |
| 奇偶性 | 奇函数 | 偶函数 | 奇函数 |
| 增区间 | $[-\frac{\pi}{2}+2k\pi, \frac{\pi}{2}+2k\pi]$ | $[-\pi+2k\pi, 2k\pi]$ | $(-\frac{\pi}{2}+k\pi, \frac{\pi}{2}+k\pi)$ |
| 减区间 | $[\frac{\pi}{2}+2k\pi, \frac{3\pi}{2}+2k\pi]$ | $[2k\pi, \pi+2k\pi]$ | 无 |

### 7. 函数 $y = A \sin(\omega x + \varphi) + B$

- **振幅**：$|A|$
- **周期**：$T = \frac{2\pi}{|\omega|}$
- **频率**：$f = \frac{1}{T} = \frac{|\omega|}{2\pi}$
- **相位**：$\omega x + \varphi$
- **初相**：$\varphi$
- **平移**：$y = \sin x \to$ 平移 $|\varphi|$ 个单位 $\to$ 横坐标伸缩 $\frac{1}{|\omega|}$ $\to$ 纵坐标伸缩 $|A|$

---

## 五、抽象函数

### 定义

没有给出具体解析式的函数，只给出函数满足的某些性质（如 $f(x+y) = f(x) + f(y)$ 等）。

### 常见抽象函数模型

| 抽象条件 | 对应函数模型 |
|----------|-------------|
| $f(x+y) = f(x) + f(y)$ | 正比例函数 $f(x) = kx$ |
| $f(x+y) = f(x) \cdot f(y)$ | 指数函数 $f(x) = a^x$ |
| $f(xy) = f(x) + f(y)$ | 对数函数 $f(x) = \log_a x$ |
| $f(xy) = f(x) \cdot f(y)$ | 幂函数 $f(x) = x^\alpha$ |

### 抽象函数解题方法

1. **赋值法**：赋特殊值（$0, 1, -1$ 等）
2. **构造法**：根据条件构造具体函数
3. **性质推导**：利用单调性、奇偶性、周期性等已知性质
4. **数形结合**：画出符合性质的示意图

---

## 六、复合函数

### 定义

$y = f[g(x)]$，其中 $u = g(x)$ 是内层函数，$y = f(u)$ 是外层函数。

### 定义域

复合函数定义域 $= \{x \mid g(x) \text{ 有定义且 } g(x) \in f \text{ 的定义域}\}$

### 单调性：同增异减（见前）

---

## 七、分段函数

### 定义

用不同解析式在不同区间表示的函数。

### 处理要点

1. **分段求值**：先判断 $x$ 所在区间，再代入对应解析式
2. **分段求定义域**：各段定义域取并集
3. **分段求值域**：各段值域取并集
4. **分段求方程/不等式**：分段讨论，解集取并集

**典型形式**：

$$
f(x) = \begin{cases}
x+1, & x \le 0 \\
-x, & x > 0
\end{cases}
$$

---

## 八、反函数

### 定义

若函数 $y = f(x)$ 是一一映射，则存在反函数 $y = f^{-1}(x)$，满足：

- $f^{-1}(y) = x$ 当 $y = f(x)$
- $f[f^{-1}(x)] = x$
- 图像关于 $y = x$ 对称
- 原函数与反函数单调性相同

### 存在条件

函数必须是 **一一映射**（单调函数一定有反函数）

### 求反函数步骤

1. 由 $y = f(x)$ 解出 $x = g(y)$
2. 互换 $x, y$：$y = g(x)$
3. 注明定义域（即原函数的值域）

### 常见反函数

| 原函数 | 反函数 |
|--------|--------|
| $y = a^x\ (a>0,a\neq1)$ | $y = \log_a x$ |
| $y = \sin x\ (x\in[-\frac{\pi}{2},\frac{\pi}{2}])$ | $y = \arcsin x$ |
| $y = \cos x\ (x\in[0,\pi])$ | $y = \arccos x$ |
| $y = \tan x\ (x\in(-\frac{\pi}{2},\frac{\pi}{2}))$ | $y = \arctan x$ |

---

## 九、函数图像变换

### 1. 平移变换

| 变换 | 公式 | 口诀 |
|------|------|------|
| 左移 $a$ | $y = f(x + a)$ | 左加右减 |
| 右移 $a$ | $y = f(x - a)$ | |
| 上移 $b$ | $y = f(x) + b$ | 上加下减 |
| 下移 $b$ | $y = f(x) - b$ | |

### 2. 伸缩变换

- **横缩**：$y = f(\omega x)$，$\omega > 1$ 时横缩
- **纵伸**：$y = A \cdot f(x)$，$A > 1$ 时纵伸

### 3. 对称变换

| 变换 | 公式 |
|------|------|
| 关于 $x$ 轴对称 | $y = -f(x)$ |
| 关于 $y$ 轴对称 | $y = f(-x)$ |
| 关于原点对称 | $y = -f(-x)$ |
| 关于 $y = x$ 对称 | $x = f(y)$（反函数）|
| 保留 $x$ 轴上方 | $y = |f(x)|$ |
| 保留 $y$ 轴右侧 | $y = f(|x|)$ |

---

## 十、函数与方程

### 1. 零点

$f(x) = 0$ 的解称为 $f(x)$ 的零点（即函数图像与 $x$ 轴的交点横坐标）

### 2. 零点存在定理

若 $f(x)$ 在 $[a, b]$ 上连续，且 $f(a) \cdot f(b) < 0$，则存在 $c \in (a, b)$ 使 $f(c) = 0$

### 3. 二分法求零点

1. 确定区间 $[a, b]$ 使 $f(a) \cdot f(b) < 0$
2. 取中点 $c = \frac{a+b}{2}$
3. 若 $f(c) = 0$，则 $c$ 为零点
4. 否则根据 $f(a) \cdot f(c)$ 符号确定新区间
5. 重复直到满足精度

### 4. 一元二次方程根的分布

设 $f(x) = ax^2 + bx + c = 0\ (a > 0)$

| 根的分布 | 条件 |
|----------|------|
| 两根都 $> k$ | $\Delta \ge 0$, $-\frac{b}{2a} > k$, $f(k) > 0$ |
| 两根都 $< k$ | $\Delta \ge 0$, $-\frac{b}{2a} < k$, $f(k) > 0$ |
| 一个 $< k <$ 另一个 | $f(k) < 0$ |
| 两根在 $(m, n)$ 内 | $\Delta \ge 0$, $m < -\frac{b}{2a} < n$, $f(m) > 0$, $f(n) > 0$ |

## 相关条目

[[02_NaturalSciences/Mathematics/Algebra/INDEX|Algebra]], [[02_NaturalSciences/Mathematics/MathematicalAnalysis/INDEX|MathematicalAnalysis]], [[02_NaturalSciences/Mathematics/Geometry/INDEX|Geometry]], [[02_NaturalSciences/Mathematics/ProbabilityStatistics/INDEX|ProbabilityStatistics]]
