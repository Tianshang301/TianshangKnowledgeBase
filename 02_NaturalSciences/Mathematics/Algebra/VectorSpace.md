# 向量空间详解

## 〇、代数结构概述

### 群(Group)
集合 $G$ 配有二元运算 $\cdot$，满足：
1. **封闭性**：$\forall a,b \in G,\ a\cdot b \in G$
2. **结合律**：$(a\cdot b)\cdot c = a\cdot(b\cdot c)$
3. **单位元**：$\exists e \in G,\ \forall a \in G,\ a\cdot e = e\cdot a = a$
4. **逆元**：$\forall a \in G,\ \exists a^{-1} \in G,\ a\cdot a^{-1} = a^{-1}\cdot a = e$

若还满足交换律 $a\cdot b = b\cdot a$，则称为 **Abel 群**。

### 环(Ring)
集合 $R$ 配有加法 $+$ 和乘法 $\cdot$，满足：
1. $(R, +)$ 是 Abel 群
2. $(R, \cdot)$ 封闭且满足结合律
3. **分配律**：$a\cdot(b+c) = a\cdot b + a\cdot c$，$(b+c)\cdot a = b\cdot a + c\cdot a$

若有乘法单位元，称为**含幺环**；若乘法交换，称为**交换环**。

### 域(Field)
集合 $\mathbb{F}$ 配有加法 $+$ 和乘法 $\cdot$，满足：
1. $(\mathbb{F}, +)$ 是 Abel 群（单位元 $0$）
2. $(\mathbb{F} \setminus \{0\}, \cdot)$ 是 Abel 群（单位元 $1$）
3. 分配律成立

**常见域**：$\mathbb{Q}$（有理数）、$\mathbb{R}$（实数）、$\mathbb{C}$（复数）、$\mathbb{Z}_p$（$p$ 为素数的模 $p$ 剩余类）

### 模(Module)与代数(Algebra)
- **模**：环上的向量空间推广
- **代数**：配有相容乘法的向量空间

## 一、向量空间的定义

### 定义

集合 $V$ 配以加法 $+$ 和数乘 $\cdot$ 构成域 $\mathbb{F}$ 上的向量空间，如果满足以下八条公理：

1. **加法封闭性**：$\forall u, v \in V, u+v \in V$
2. **加法结合律**：$(u+v)+w = u+(v+w)$
3. **加法交换律**：$u+v = v+u$
4. **零元**：$\exists \mathbf{0} \in V, \forall v \in V, v+\mathbf{0}=v$
5. **负元**：$\forall v \in V, \exists -v \in V, v+(-v)=\mathbf{0}$
6. **数乘封闭性**：$\forall c \in \mathbb{F}, v \in V, cv \in V$
7. **数乘分配律**：$c(u+v) = cu + cv$
8. **域分配律**：$(c+d)v = cv + dv$
9. **数乘结合律**：$c(dv) = (cd)v$
10. **单位元**：$1v = v$

### 常见例子

- $\mathbb{R}^n$：$n$ 维欧氏空间
- $P_n$：次数不超过 $n$ 的多项式空间
- $C[a,b]$：$[a,b]$ 上连续函数空间
- $M_{m \times n}(\mathbb{R})$：$m \times n$ 实矩阵空间

## 二、子空间 (Subspaces)

### 子空间判定
$W \subseteq V$ 是子空间当且仅当：
1. $\mathbf{0} \in W$
2. $\forall u, v \in W, u+v \in W$
3. $\forall c \in \mathbb{F}, v \in W, cv \in W$

### 重要子空间
**零空间(Null Space)**：
$$N(A) = \{x \in \mathbb{R}^n \mid Ax = 0\}$$

**列空间(Column Space)**：
$$C(A) = \text{span}\{\text{columns of } A\} \subseteq \mathbb{R}^m$$

**行空间(Row Space)**：
$$R(A) = \text{span}\{\text{rows of } A\} \subseteq \mathbb{R}^n$$

## 三、线性无关与基
### 线性无关
向量集 $\{v_1, \dots, v_k\}$ 线性无关，如果：
$$c_1 v_1 + \cdots + c_k v_k = 0 \implies c_1 = \cdots = c_k = 0$$

### 基与维数

- **基**：线性无关的生成集
- **维数**：基中向量的个数，记作 $\dim(V)$
- **标准基**：$\mathbb{R}^n$ 的标准基为 $\{e_1, \dots, e_n\}$，其中 $e_i$ 第 $i$ 分量为 1，其余为 0

### 坐标向量

向量 $v$ 在基 $\mathcal{B} = \{b_1, \dots, b_n\}$ 下的坐标 $[v]_\mathcal{B}$ 满足：
$$v = c_1 b_1 + \cdots + c_n b_n, \quad [v]_\mathcal{B} = (c_1, \dots, c_n)^T$$

### 基变换
$$\mathbf{x}_\mathcal{C} = P_{\mathcal{C} \leftarrow \mathcal{B}} \ \mathbf{x}_\mathcal{B}$$

其中 $P_{\mathcal{C} \leftarrow \mathcal{B}}$ 为从基 $\mathcal{B}$ 到基 $\mathcal{C}$ 的过渡矩阵。

## 四、线性变换
### 定义与矩阵表示
$T: V \to W$ 是线性变换，如果：
- $T(u+v) = T(u) + T(v)$
- $T(cv) = cT(v)$

在给定基下，$T$ 可由矩阵 $A$ 表示：$[T(v)]_\mathcal{C} = A[v]_\mathcal{B}$

### 核与像
- **核(Kernel)**：$\ker(T) = \{v \in V \mid T(v) = 0\}$
- **像(Image)**：$\text{Im}(T) = \{T(v) \mid v \in V\}$

**维数公式**：$\dim(\ker(T)) + \dim(\text{Im}(T)) = \dim(V)$

### 同构

若 $T$ 是双射线性变换，则 $V$ 与 $W$ 同构。有限维向量空间同构当且仅当维数相同。

## 五、内积空间
### 内积

$$\langle u, v \rangle = u \cdot v = \sum_i u_i v_i \quad (\text{标准内积})$$

### 范数

$$\|v\| = \sqrt{\langle v, v \rangle}$$

**Cauchy-Schwarz不等式**：
$$|\langle u, v \rangle| \le \|u\| \|v\|$$

**三角不等式**：
$$\|u + v\| \le \|u\| + \|v\|$$

**向量投影**：
$$\text{proj}_u(v) = \frac{\langle v, u \rangle}{\langle u, u \rangle} u$$

### 正交性
$$u \perp v \iff \langle u, v \rangle = 0$$

### 格拉姆-施密特正交化

给定线性无关集 $\{v_1, \dots, v_k\}$，
$$u_1 = v_1$$
$$u_k = v_k - \sum_{i=1}^{k-1} \frac{\langle v_k, u_i \rangle}{\langle u_i, u_i \rangle} u_i$$

正交基：$\{u_1, \dots, u_k\}$，标准正交基：$\{u_1/\|u_1\|, \dots, u_k/\|u_k\|\}$

### 正交补
$$W^\perp = \{v \in V \mid \langle v, w \rangle = 0, \forall w \in W\}$$

**基本子空间定理：** $N(A) = (R(A))^\perp$，$N(A^T) = (C(A))^\perp$

### 最小二乘法

解 $A^T A x = A^T b$（正规方程），最小化 $\|Ax - b\|^2$。
```python
import numpy as np
A = np.array([[1, 1], [1, 2], [1, 3]])
b = np.array([1, 2, 2])
x_ls = np.linalg.lstsq(A, b, rcond=None)[0]
```

## 参考资料

- Gilbert Strang, *Introduction to Linear Algebra*, Wellesley-Cambridge Press
- Sheldon Axler, *Linear Algebra Done Right*, Springer
- 北京大学数学系几何与代数教研室前代数小组, 《高等代数》, 高等教育出版社

## 相关条目

[[02_NaturalSciences/Mathematics/Geometry/INDEX|Geometry]], [[02_NaturalSciences/Mathematics/NumberTheory/INDEX|NumberTheory]], [[02_NaturalSciences/Mathematics/MathematicalAnalysis/INDEX|MathematicalAnalysis]], LinearAlgebra
