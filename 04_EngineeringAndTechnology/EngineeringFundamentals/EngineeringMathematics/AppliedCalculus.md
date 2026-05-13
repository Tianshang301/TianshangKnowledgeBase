# 应用微积分

## 定义
应用微积分是研究微积分在工程问题中的应用的学科。包括一元和多元微积分、常微分方程等内容。

## 核心内容

### 极限与连续

**极限定义**：$\lim_{x \to a}f(x) = A$

**连续性**：$\lim_{x \to a}f(x) = f(a)$

### 导数与微分

**导数定义**：

$$f'(x) = \lim_{\Delta x \to 0}\frac{f(x+\Delta x)-f(x)}{\Delta x}$$

**求导法则**：
- $(uv)' = u'v+uv'$
- $(u/v)' = (u'v-uv')/v^2$
- 链式法则：$\frac{dy}{dx} = \frac{dy}{du}\cdot\frac{du}{dx}$

**应用**：
- 曲线切线
- 极值与最值
- 曲率

### 积分

**不定积分**：

$$\int f(x)dx = F(x) + C$$

**定积分**：

$$\int_a^b f(x)dx = F(b)-F(a)$$

**积分方法**：
- 换元积分法
- 分部积分法
- 有理函数积分

### 多元微积分

**偏导数**：$\frac{\partial f}{\partial x}$

**全微分**：$df = \frac{\partial f}{\partial x}dx + \frac{\partial f}{\partial y}dy$

**多重积分**：
- 二重积分：$\iint_D f(x,y)dA$
- 三重积分：$\iiint_\Omega f(x,y,z)dV$

**曲线/曲面积分**：
- 第一类曲线积分
- 第二类曲线积分
- 曲面积分

### 向量分析

**梯度**：$\nabla f = (\frac{\partial f}{\partial x}, \frac{\partial f}{\partial y}, \frac{\partial f}{\partial z})$

**散度**：$\nabla \cdot \vec{F} = \frac{\partial F_x}{\partial x}+\frac{\partial F_y}{\partial y}+\frac{\partial F_z}{\partial z}$

**旋度**：$\nabla \times \vec{F}$

**格林公式、高斯公式、斯托克斯公式**

### 常微分方程

**一阶方程**：
- 变量分离：$\frac{dy}{dx} = f(x)g(y)$
- 一阶线性：$y'+P(x)y=Q(x)$

**二阶常系数线性方程**：
- 齐次：$y''+py'+qy=0$
- 非齐次：$y''+py'+qy=f(x)$

## 经典教材
- 同济大学《高等数学》
- 同济大学《线性代数》
- Stewart《Calculus》
- Kreyszig《Advanced Engineering Mathematics》

## 主要应用领域
- 工程力学分析
- 控制系统建模
- 电路分析
- 流体力学
- 热传导分析
