# 数值方法

## 定义
数值方法是研究用计算机求解数学问题近似解的理论和方法的学科。

## 核心内容

### 数值误差

**误差类型**：
- 舍入误差：计算机浮点运算产生
- 截断误差：用近似公式代替精确公式

**误差传播**：条件数分析

### 方程求根

**二分法**：$[a,b]$ 区间逐步对分

**牛顿法**：

$$x_{n+1} = x_n - \frac{f(x_n)}{f'(x_n)}$$

**割线法**：用差商代替导数

### 线性方程组求解

**直接法**：
- 高斯消去法
- LU分解：$A = LU$
- Cholesky分解：$A = LL^T$

**迭代法**：
- Jacobi迭代
- Gauss-Seidel迭代
- SOR迭代

### 插值与拟合

**多项式插值**：
- Lagrange插值
- Newton插值
- Hermite插值

**样条插值**：三次样条

**最小二乘拟合**：

$$\min\sum_{i=1}^{n}[y_i-f(x_i)]^2$$

### 数值积分

**Newton-Cotes公式**：
- 梯形公式：$\int_a^b f(x)dx \approx \frac{b-a}{2}[f(a)+f(b)]$
- Simpson公式：$\int_a^b f(x)dx \approx \frac{b-a}{6}[f(a)+4f(m)+f(b)]$

**Gauss求积**：$\int_{-1}^{1}f(x)dx \approx \sum_{i=1}^{n}w_i f(x_i)$

### 常微分方程数值解

**Euler方法**：$y_{n+1} = y_n + hf(x_n,y_n)$

**Runge-Kutta方法**：$k_1, k_2, k_3, k_4$ 加权平均

**Adams方法**：多步法

### 偏微分方程数值解

**有限差分法**：
- 离散化网格
- 差分格式
- 稳定性分析

**有限元法**：
- 单元划分
- 形函数
- 刚度矩阵

## 经典教材
- 李庆扬《数值分析》
- 同济大学《数值方法》
- Burden《Numerical Analysis》
- Atkinson《An Introduction to Numerical Analysis》

## 主要应用领域
- 工程仿真计算
- 流体力学数值模拟
- 结构有限元分析
- 电磁场计算
- 数据分析与拟合
