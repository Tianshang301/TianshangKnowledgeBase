---
aliases: [MatrixOps]
tags: ['Mathematics', 'Algebra', 'MatrixOps']
created: 2026-05-16
updated: 2026-05-13
---

# 矩阵运算详解

## 一、基本运算
### 矩阵加法与数乘
$$(A + B)_{ij} = a_{ij} + b_{ij}, \quad (cA)_{ij} = c \cdot a_{ij}$$

### 矩阵乘法

$$(AB)_{ij} = \sum_{k=1}^n a_{ik} b_{kj}$$

矩阵乘法不满足交换律，$AB \neq BA$（通常）。

### 转置

$$(A^T)_{ij} = A_{ji}$$

性质：$(AB)^T = B^T A^T, \ (A^T)^T = A$

### 共轭转置

$$A^* = \overline{A^T} = (\overline{A})^T$$

### 迹(Trace)

$$\text{tr}(A) = \sum_{i=1}^n a_{ii}$$

性质：$\text{tr}(AB) = \text{tr}(BA)$

## 二、行列式 (Determinant)

### 定义（递归）
$$\det(A) = \begin{cases} a_{11} & n=1 \\ \sum_{j=1}^n (-1)^{1+j} a_{1j} \det(M_{1j}) & n>1 \end{cases}$$

其中 $M_{ij}$ 为删除第 $i$ 行第 $j$ 列后的子矩阵。

### 分块矩阵

$$\begin{bmatrix} A & B \\ C & D \end{bmatrix} \begin{bmatrix} X \\ Y \end{bmatrix} = \begin{bmatrix} AX + BY \\ CX + DY \end{bmatrix}$$

**分块矩阵乘法**：
$$\begin{bmatrix} A_{11} & A_{12} \\ A_{21} & A_{22} \end{bmatrix} \begin{bmatrix} B_{11} & B_{12} \\ B_{21} & B_{22} \end{bmatrix} = \begin{bmatrix} A_{11}B_{11}+A_{12}B_{21} & A_{11}B_{12}+A_{12}B_{22} \\ A_{21}B_{11}+A_{22}B_{21} & A_{21}B_{12}+A_{22}B_{22} \end{bmatrix}$$

### 性质

- $\det(AB) = \det(A) \det(B)$
- $\det(A^T) = \det(A)$
- 两行互换，行列式变号
- 某行乘以 $c$，行列式乘以 $c$
- 某行加上另一行的倍数，行列式不变
- 三角矩阵的行列式等于对角线元素乘积

## 三、逆矩阵 (Inverse)

### 高斯-若尔当消元法

将 $[A \mid I]$ 通过行变换化为 $[I \mid A^{-1}]$。

### 伴随公式

$$A^{-1} = \frac{1}{\det(A)} \text{adj}(A)$$

其中 $\text{adj}(A)_{ij} = (-1)^{i+j} \det(M_{ji})$。

### 可逆矩阵定理
以下等价：
- $A$ 可逆
- $\det(A) \neq 0$
- $A$ 满秩
- $A$ 的列向量线性无关
- $A$ 的行向量线性无关
- $Ax = 0$ 只有零解

## 四、矩阵分解
### LU 分解

$$A = LU$$

其中 $L$ 为单位下三角阵，$U$ 为上三角阵。

### QR 分解

$$A = QR$$

其中 $Q$ 为正交矩阵（$Q^T Q = I$），$R$ 为上三角阵。
```python
import numpy as np
A = np.array([[1, 2], [3, 4]])
Q, R = np.linalg.qr(A)
```

## 五、矩阵范数与条件数
### 常见范数

- **谱范数**：$\|A\|_2 = \sigma_{\max}(A)$（最大奇异值）
- **Frobenius 范数**：$\|A\|_F = \sqrt{\sum_i \sum_j |a_{ij}|^2} = \sqrt{\text{tr}(A^T A)}$
- **1-范数**：$\|A\|_1 = \max_j \sum_i |a_{ij}|$（最大列和）
- **$\infty$-范数**：$\|A\|_\infty = \max_i \sum_j |a_{ij}|$（最大行和）

### 矩阵指数

$$e^{A} = \sum_{k=0}^{\infty} \frac{A^k}{k!}$$

若 $A = PDP^{-1}$，则 $e^{A} = P e^{D} P^{-1}$，其中 $e^{D} = \text{diag}(e^{\lambda_1}, \dots, e^{\lambda_n})$。

### 条件数
$$\kappa(A) = \|A\|\|A^{-1}\|$$

条件数衡量矩阵对误差的敏感程度。条件数大 → 病态矩阵。
```python
import numpy as np
A = np.array([[1, 2], [3, 4]])
cond = np.linalg.cond(A)  # 默认使用 2-范数
```

## 参考资料

- Gilbert Strang, *Introduction to Linear Algebra*, Wellesley-Cambridge Press
- Gene H. Golub & Charles F. Van Loan, *Matrix Computations*, Johns Hopkins University Press
- 张贤达, 《矩阵分析与应用》, 清华大学出版社

## 相关条目

[[02_NaturalSciences/Mathematics/Geometry/INDEX|Geometry]], [[02_NaturalSciences/Mathematics/NumberTheory/INDEX|NumberTheory]], [[02_NaturalSciences/Mathematics/MathematicalAnalysis/INDEX|MathematicalAnalysis]], LinearAlgebra
