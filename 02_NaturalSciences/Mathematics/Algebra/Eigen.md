# 特征值与特征向量

## 一、定义与几何意义

### 定义

��?$A$ ��?$n \times n$ 矩阵，若存在非零向量 $v$ 和标��?$\lambda$ 使得��?
$$A v = \lambda v$$

��?$\lambda$ 为特征值，$v$ 为对应的特征向量��?
**几何意义��?* 特征向量��?$A$ 作用下只发生伸缩，不改变方向。伸缩倍数��?$\lambda$��?
### 特征多项��?
$$p(\lambda) = \det(A - \lambda I) = 0$$

$p(\lambda)$ ��?$n$ 次多项式，其根即为特征值��?
### Gershgorin圆盘定理

每个特征��?$\lambda$ 位于至少一个圆盘内��?$$|\lambda - a_{ii}| \le \sum_{j \neq i} |a_{ij}|$$

### Rayleigh��?
$$\lambda_{min} \le R(x) = \frac{x^T A x}{x^T x} \le \lambda_{max}$$

### 幂迭代法

$$v_{k+1} = \frac{A v_k}{\|A v_k\|}, \quad \lambda^{(k)} = v_k^T A v_k$$

收敛到模最大的特征值和对应特征向量��?
### 代数重数与几何重��?
- **代数重数**：特征值作为特征多项式根的重数
- **几何重数**��?\dim(\text{Null}(A - \lambda I))$，即对应特征空间的维��?- 几何重数 $\leq$ 代数重数

## 二、对角化 (Diagonalization)

### 可对角化条件

$A$ 可对角化 $\iff$ 对每个特征值，几何重数 = 代数重数 $\iff$ $A$ ��?$n$ 个线性无关的特征向量��?
### 对角化过��?
��?$A$ 可对角化，则存在可逆矩��?$P$ 和对角矩��?$D$ 使得��?
$$A = P D P^{-1}$$

其中 $P$ 的列��?$A$ 的特征向量，$D$ 的对角线为对应的特征值��?
**应用��?*
$$A^n = P D^n P^{-1}$$

### 特征��?(Eigenbasis)

由特征向量构成的一组基称为特征基。在特征基下，线性变换表示为对角矩阵��?
## 三、对称矩阵的谱定��?
### 实对称矩��?
��?$A = A^T$（实对称），则：
- 所有特征值为实数
- 不同特征值对应的特征向量正交
- 存在正交矩阵 $Q$��?Q^T Q = I$）使得：

$$A = Q \Lambda Q^T$$

其中 $\Lambda$ 为对角矩阵，$Q$ 的列为标准正交的特征向量��?
## 四、二次型 (Quadratic Forms)

### 定义

$$Q(x) = x^T A x = \sum_{i=1}^n \sum_{j=1}^n a_{ij} x_i x_j$$

其中 $A$ 为对称矩阵��?
### 定值��?(Definiteness)

- **正定**��?x^T A x > 0$ 对所��?$x \neq 0$；特征值全��?- **半正��?*��?x^T A x \geq 0$；特征值非��?- **负定**��?x^T A x < 0$；特征值全��?- **不定**：特征值有正有��?
### 主子式判别法

$A$ 正定 $\iff$ 所有顺序主子式 $> 0$��?
## 五、奇异值分��?(SVD)

### 定义

任意 $m \times n$ 矩阵 $A$ 可分解为��?
$$A = U \Sigma V^T$$

- $U$��?m \times m$ 正交矩阵（左奇异向量��?- $V$��?n \times n$ 正交矩阵（右奇异向量��?- $\Sigma$��?m \times n$ 对角矩阵，对角线为奇异��?$\sigma_1 \geq \sigma_2 \geq \cdots \geq \sigma_r > 0$

### 紧凑 SVD

$$A = U_r \Sigma_r V_r^T$$

其中仅保��?$r = \text{rank}(A)$ 个非零奇异值��?
### 与特征值的关系

$$\sigma_i^2 = \lambda_i(A^T A) = \lambda_i(A A^T)$$

$V$ 的列��?$A^T A$ 的特征向量，$U$ 的列��?$A A^T$ 的特征向量��?
### 矩阵近似 (Eckart-Young 定理)

保留��?$k$ 个最大奇异值得��?$A$ 的最佳秩 $k$ 近似��?
$$A_k = U_k \Sigma_k V_k^T$$

### 伪��?(Pseudoinverse)

$$A^+ = V \Sigma^+ U^T$$

其中 $\Sigma^+$ ��?$\Sigma$ 的非零对角元取倒数��?
```python
import numpy as np
from numpy.linalg import svd

A = np.array([[1, 2], [3, 4], [5, 6]], dtype=float)
U, s, Vt = svd(A)
Sigma = np.zeros((3, 2))
Sigma[:2, :2] = np.diag(s)

# 紧凑 SVD
A_approx = U[:, :2] @ np.diag(s) @ Vt[:2, :]

# ��? 近似
A_rank1 = s[0] * np.outer(U[:, 0], Vt[0, :])

# 伪��?A_pinv = Vt.T @ np.diag(1/s) @ U[:, :2].T
```

### 矩阵分解对比

| 分解 | 适用矩阵 | 形式 | 唯一��?| 用��?|
|:---|:---|:---|:---:|:---|
| LU | 方阵 | $A = LU$ | 不唯一 | 解线性方程组 |
| QR | 任意 | $A = QR$ | 唯一��?R>0$��?| 最小二��?|
| 特征分解 | 可对角化方阵 | $A = PDP^{-1}$ | 不唯一 | 矩阵幂、谱分析 |
| SVD | 任意矩阵 | $A = U\Sigma V^T$ | 唯一 | 降维、伪逆、压��?|

## 相关条目

[[02_NaturalSciences/Mathematics/Geometry/INDEX|Geometry]], [[02_NaturalSciences/Mathematics/NumberTheory/INDEX|NumberTheory]], [[02_NaturalSciences/Mathematics/MathematicalAnalysis/INDEX|MathematicalAnalysis]], LinearAlgebra
