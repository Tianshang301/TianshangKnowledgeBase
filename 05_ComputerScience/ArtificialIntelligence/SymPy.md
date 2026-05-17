---
aliases: [SymPy]
tags: ['05_ComputerScience', 'ArtificialIntelligence']
---

# SymPy — Python 符号数学库

## 一、概述 (Overview)

SymPy 是 Python 的符号数学计算库（Symbolic Mathematics），进行代数运算、微积分、方程求解、矩阵运算等符号计算，而非数值近似。与数值计算库（NumPy）不同，SymPy 保持精确的数学表达式。

### SymPy 的特点

- **纯 Python**：无外部依赖，易于安装和嵌入
- **符号计算**：精确数学运算，无浮点误差
- **LaTeX 输出**：$\LaTeX$ 格式打印数学表达式
- **扩展性**：支持自定义函数和表达式变换
- **交互式**：Jupyter Notebook 集成良好

## 二、核心功能 (Core Features)

### 符号定义与基础运算

```python
import sympy as sp

# 符号定义
x, y, z = sp.symbols('x y z')
a, b, c = sp.symbols('a b c', real=True, positive=True)
n = sp.symbols('n', integer=True, nonnegative=True)

# 代数展开与化简
expr = (x + y)**3
expanded = sp.expand(expr)   # x^3 + 3*x^2*y + 3*x*y^2 + y^3
simplified = sp.simplify(expanded)

# 因式分解
sp.factor(x**2 - 5*x + 6)    # (x - 2)*(x - 3)

# 部分分式分解
sp.apart(1/(x*(x+1)), x)     # 1/x - 1/(x+1)
```

### 微积分 (Calculus)

```python
# 导数 (Differentiation)
sp.diff(sp.sin(x), x)              # cos(x)
sp.diff(x**3 * sp.exp(x), x)       # x**3*exp(x) + 3*x**2*exp(x)

# 高阶导数
sp.diff(x**5, x, 3)                # 60*x**2

# 不定积分
sp.integrate(sp.sin(x), x)         # -cos(x)

# 定积分
sp.integrate(sp.exp(-x), (x, 0, sp.oo))  # 1

# 极限
sp.limit(sp.sin(x)/x, x, 0)        # 1

# 泰勒展开
sp.series(sp.sin(x), x, 0, 6)      # x - x**3/6 + x**5/120 + O(x**6)

# 级数求和
sp.summation(1/n**2, (n, 1, sp.oo))  # pi**2/6
```

### 方程求解 (Equation Solving)

```python
# 代数方程
sp.solve(x**2 - 5*x + 6, x)        # [2, 3]
sp.solve([x + y - 1, x - y - 3], [x, y])  # {x: 2, y: -1}

# 微分方程
f = sp.Function('f')
eq = sp.Eq(sp.diff(f(x), x, 2) + f(x), 0)
sp.dsolve(eq, f(x))                # Eq(f(x), C1*sin(x) + C2*cos(x))

# 特征值问题
M = sp.Matrix([[1, 2], [3, 4]])
M.eigenvals()                      # {5/2 - sqrt(33)/2: 1, 5/2 + sqrt(33)/2: 1}
M.eigenvects()                     # 特征向量
```

### 矩阵运算 (Matrix Operations)

```python
# 矩阵创建
A = sp.Matrix([[1, 2], [3, 4]])
B = sp.Matrix([[5, 6], [7, 8]])

# 基础运算
A + B, A * B, A**2
A.inv()                            # 逆矩阵
A.det()                            # 行列式: -2
A.rank()                           # 秩: 2
A.LUdecomposition()                # LU 分解

# 标准化矩阵形式
λ = sp.symbols('λ')
(A - λ * sp.eye(2)).det()          # 特征多项式: λ^2 - 5*λ - 2
```

### 逻辑与集合 (Logic & Sets)

```python
# 逻辑运算
x, y = sp.symbols('x y')
sp.simplify(sp.Implies(x, y))      # ~x | y

# 集合运算
A = sp.Interval(0, 5)
B = sp.Interval(3, 8)
A.intersect(B)                     # [3, 5]
A.union(B)                         # [0, 8]
A - B                              # [0, 3)
```

## 三、高等数学应用 (Advanced Mathematics)

### 拉普拉斯变换 (Laplace Transform)

```python
s, t = sp.symbols('s t')
sp.laplace_transform(sp.sin(t), t, s)  # (1/(s**2 + 1), 0, True)
sp.inverse_laplace_transform(1/(s**2 + 1), s, t)  # sin(t)*Heaviside(t)
```

### 傅里叶变换 (Fourier Transform)

```python
ω = sp.symbols('ω')
sp.fourier_transform(sp.exp(-t**2), t, ω)  # sqrt(pi)*exp(-omega**2/4)
```

### 概率与统计 (Probability & Statistics)

```python
# 概率分布
from sympy.stats import Normal, density, E, variance
X = Normal('X', 0, 1)            # N(0, 1)
density(X)(x)                    # exp(-x**2/2)/sqrt(2*pi)
E(X**2)                          # 1
variance(X)                      # 1
```

## 四、公式美化输出 (Pretty Printing)

```python
# LaTeX 输出
sp.init_printing()
expr = sp.Integral(sp.exp(-x**2), (x, -sp.oo, sp.oo))
sp.latex(expr)  # $$\\int_{-\\infty}^{\\infty} e^{- x^{2}}\\, dx$$

# Unicode 美打印
sp.pprint(expr)
# ∞
# ⌠
# ⎮    2
# ⎮  -x
# ⎮ ℯ   dx
# ⌡
# -∞
```

### 公式代换 (Substitution)

```python
expr = sp.sin(x) + sp.cos(x)
expr.subs(x, sp.pi/2)             # 1
expr.subs(x, sp.Symbol('t'))      # sin(t) + cos(t)

# 多项代换
expr.subs({sp.sin(x): 'S', sp.cos(x): 'C'})  # C + S

# 数值计算
expr_n = sp.lambdify(x, expr, 'numpy')
import numpy as np
expr_n(np.array([0, np.pi/2]))    # array([1., 1.])
```

## 五、自动微分与 SymPy

SymPy 的符号微分（Symbolic Diff）与自动微分（AD）不同：

```text
符号微分: 直接操作数学表达式得到导数公式
  输入: sin(x) * cos(x)
  输出: -sin(x)^2 + cos(x)^2

自动微分: 在数值执行时使用链式法则
  输入: 函数 + 数值
  输出: 数值梯度（非公式）
```

SymPy 可用于推导机器学习中的梯度公式，然后通过 `lambdify` 转换为 NumPy 计算：

```python
x = sp.symbols('x')
loss = sp.log(1 + sp.exp(-x))
gradient = sp.diff(loss, x)       # -exp(-x)/(1 + exp(-x))
grad_numeric = sp.lambdify(x, gradient, 'numpy')
```

## 六、集成与应用场景 (Integration & Applications)

| 场景 | SymPy 角色 | 配合库 |
|------|-----------|--------|
| 公式推导验证 | 检查手推导数/积分 | — |
| 科学研究 | 符号推导后转数值 | NumPy, SciPy |
| 控制系统分析 | 传递函数、根轨迹 | Control |
| 物理学计算 | 量子力学、相对论 | — |
| 教育/教学 | 数学公式可视化 | Jupyter, `sympy.plotting` |
| 自动梯度生成 | 辅助深度学习梯度推导 | PyTorch, JAX |

## 六、符号计算 vs 数值计算 (Symbolic vs Numeric)

| 特性 | SymPy (符号) | NumPy (数值) |
|------|-------------|-------------|
| 精度 | **精确**（无舍入误差） | 有限精度（float64） |
| 速度 | 慢（符号操作） | 快（向量化 C/Fortran） |
| 适用 | 公式推导、精确验证 | 大规模数值计算 |
| 内存 | 表达式膨胀 | 固定大小数组 |
| 微分 | 精确导数公式 | 自动微分/数值近似 |
| 最佳实践 | SymPy 推导公式 → `lambdify` 转 NumPy 计算 | — |

### SymPy → NumPy 转换流水线

```python
# 1. 符号推导
x = sp.symbols('x')
f = sp.sin(x) * sp.exp(-x**2)
df = sp.diff(f, x)        # 符号导数

# 2. 转 NumPy 函数
f_np = sp.lambdify(x, f, 'numpy')
df_np = sp.lambdify(x, df, 'numpy')

# 3. 高速数值计算
import numpy as np
xs = np.linspace(-3, 3, 10000)
ys = f_np(xs)
dys = df_np(xs)
```

## 七、常见应用模式 (Common Patterns)

### 线性代数最佳实践

```python
# 符号矩阵运算
A = sp.Matrix([[1, 2, 3], [4, 5, 6], [7, 8, 10]])
b = sp.Matrix([1, 2, 3])

# 求解 Ax = b
x = A.LUsolve(b)
print(x)  # Matrix([[-2/3], [1/3], [1]])

# 特征值分解
A.eigenvals()    # 特征值
A.eigenvects()   # 特征向量（含几何重数）

# 奇异值分解 (SVD)
U, S, V = A.singular_value_decomposition()
```

### 符号积分和变换

```python
# 傅里叶级数
n = sp.symbols('n', integer=True, positive=True)
x = sp.symbols('x')
f = sp.Piecewise((0, x < -sp.pi/2), (1, x < sp.pi/2), (0, True))
# 计算傅里叶系数
an = (1/sp.pi) * sp.integrate(f * sp.cos(n*x), (x, -sp.pi, sp.pi))
bn = (1/sp.pi) * sp.integrate(f * sp.sin(n*x), (x, -sp.pi, sp.pi))
```

SymPy 与 Latex 输出结合在 Jupyter Notebook 中最为高效，适合数学教学和论文公式推导验证。

## 相关条目
- [[AutomaticDifferentiation]]
- [[InformationTheory]]
- [[05_ComputerScience/ArtificialIntelligence/INDEX]]
