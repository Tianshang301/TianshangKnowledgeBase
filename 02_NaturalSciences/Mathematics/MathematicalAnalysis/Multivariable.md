# 多元微积分详��?
## 一、多元函��?
### 偏导��?
$$f_x(x,y) = \frac{\partial f}{\partial x} = \lim_{h \to 0} \frac{f(x+h, y) - f(x, y)}{h}$$
$$f_y(x,y) = \frac{\partial f}{\partial y} = \lim_{h \to 0} \frac{f(x, y+h) - f(x, y)}{h}$$

### 克莱罗定��?(Clairaut's Theorem)

��?$f_{xy}$ ��?$f_{yx}$ 在点 $(a,b)$ 附近连续，则��?
$$\frac{\partial^2 f}{\partial x \partial y} = \frac{\partial^2 f}{\partial y \partial x}$$

### Hessian矩阵

$$H_f = \begin{bmatrix} 
\frac{\partial^2 f}{\partial x_1^2} & \frac{\partial^2 f}{\partial x_1\partial x_2} & \cdots \\
\frac{\partial^2 f}{\partial x_2\partial x_1} & \frac{\partial^2 f}{\partial x_2^2} & \cdots \\
\vdots & \vdots & \ddots
\end{bmatrix}$$

$H_f$ 正定 $\implies$ 局部极小；$H_f$ 负定 $\implies$ 局部极大��?
### 多元Taylor展开

$$f(x) = f(a) + \nabla f(a)^T(x-a) + \frac{1}{2}(x-a)^T H_f(a)(x-a) + \cdots$$

### 梯度 (Gradient)

$$\nabla f = \left\langle \frac{\partial f}{\partial x}, \frac{\partial f}{\partial y}, \frac{\partial f}{\partial z} \right\rangle$$

梯度方向为函数增长最快的方向，其模为最大方向导数��?
### 方向导数

$$D_{\mathbf{u}} f = \nabla f \cdot \mathbf{u}$$

其中 $\mathbf{u}$ 为单位向量��?
### 切平��?
对曲��?$z = f(x,y)$，在 $(x_0, y_0, z_0)$ 处的切平面为��?
$$z - z_0 = f_x(x_0, y_0)(x - x_0) + f_y(x_0, y_0)(y - y_0)$$

## 二、拉格朗日乘数法

��?$f(x,y,z)$ 在约��?$g(x,y,z) = 0$ 下的极值：

$$\nabla f = \lambda \nabla g$$

即解方程组：
$$f_x = \lambda g_x, \quad f_y = \lambda g_y, \quad f_z = \lambda g_z, \quad g = 0$$

## 三、多重积��?
### 二重积分

$$\iint_R f(x,y) \, dA = \iint_R f(x,y) \, dx \, dy$$

### 累次积分

$$\iint_R f(x,y) \, dA = \int_a^b \int_{g_1(x)}^{g_2(x)} f(x,y) \, dy \, dx = \int_c^d \int_{h_1(y)}^{h_2(y)} f(x,y) \, dx \, dy$$

### 极坐标变��?
$$x = r\cos\theta, \quad y = r\sin\theta, \quad dA = r \, dr \, d\theta$$

$$\iint_R f(x,y) \, dA = \iint_S f(r\cos\theta, r\sin\theta) \, r \, dr \, d\theta$$

### 三重积分

$$\iiint_E f(x,y,z) \, dV$$

**柱坐标：**
$$x = r\cos\theta, \ y = r\sin\theta, \ z = z, \ dV = r \, dr \, d\theta \, dz$$

**球坐标：**
$$x = \rho\sin\phi\cos\theta, \ y = \rho\sin\phi\sin\theta, \ z = \rho\cos\phi, \ dV = \rho^2\sin\phi \, d\rho \, d\phi \, d\theta$$

### 变量替换与雅可比行列��?
$$\iint_R f(x,y) \, dA = \iint_S f(x(u,v), y(u,v)) \, |J| \, du \, dv$$

其中雅可比行列式��?
$$J = \frac{\partial(x,y)}{\partial(u,v)} = \begin{vmatrix} \frac{\partial x}{\partial u} & \frac{\partial x}{\partial v} \\ \frac{\partial y}{\partial u} & \frac{\partial y}{\partial v} \end{vmatrix}$$

## 四、向量微积分

### 向量��?
$$\mathbf{F}(x,y,z) = P\mathbf{i} + Q\mathbf{j} + R\mathbf{k}$$

### 散度 (Divergence)

$$\text{div} \ \mathbf{F} = \nabla \cdot \mathbf{F} = \frac{\partial P}{\partial x} + \frac{\partial Q}{\partial y} + \frac{\partial R}{\partial z}$$

### 旋度 (Curl)

$$\text{curl} \ \mathbf{F} = \nabla \times \mathbf{F} = \begin{vmatrix} \mathbf{i} & \mathbf{j} & \mathbf{k} \\ \frac{\partial}{\partial x} & \frac{\partial}{\partial y} & \frac{\partial}{\partial z} \\ P & Q & R \end{vmatrix}$$

### Laplace算子

$$\Delta f = \nabla^2 f = \frac{\partial^2 f}{\partial x^2} + \frac{\partial^2 f}{\partial y^2} + \frac{\partial^2 f}{\partial z^2}$$

### 线积��?
$$\int_C \mathbf{F} \cdot d\mathbf{r} = \int_a^b \mathbf{F}(\mathbf{r}(t)) \cdot \mathbf{r}'(t) \, dt$$

��?$\mathbf{F} = \nabla f$（保守场），��?$\int_C \mathbf{F} \cdot d\mathbf{r} = f(\mathbf{r}(b)) - f(\mathbf{r}(a))$��?
### 格林定理 (Green's Theorem)

$$\oint_C P \, dx + Q \, dy = \iint_D \left( \frac{\partial Q}{\partial x} - \frac{\partial P}{\partial y} \right) \, dA$$

### 面积��?
$$\iint_S \mathbf{F} \cdot d\mathbf{S} = \iint_D \mathbf{F} \cdot (\mathbf{r}_u \times \mathbf{r}_v) \, du \, dv$$

### 斯托克斯定理 (Stokes' Theorem)

$$\oint_C \mathbf{F} \cdot d\mathbf{r} = \iint_S (\nabla \times \mathbf{F}) \cdot d\mathbf{S}$$

### 散度定理 (高斯定理)

$$\iint_S \mathbf{F} \cdot d\mathbf{S} = \iiint_E (\nabla \cdot \mathbf{F}) \, dV$$

## 五、应��?
- **曲面面积**��?A(S) = \iint_D |\mathbf{r}_u \times \mathbf{r}_v| \, du \, dv$
- **通量**��?\iint_S \mathbf{F} \cdot \mathbf{n} \, dS$（散度定理计算）
- **环量**��?\oint_C \mathbf{F} \cdot d\mathbf{r}$（斯托克斯定理计算）

## 相关条目

[[02_NaturalSciences/Mathematics/Algebra/INDEX|Algebra]], [[02_NaturalSciences/Mathematics/DifferentialEquations/INDEX|DifferentialEquations]], [[02_NaturalSciences/Mathematics/Geometry/INDEX|Geometry]], RealAnalysis
