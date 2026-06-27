---
aliases: [Applications, 代数应用, LinearAlgebraApplications]
tags: ['Mathematics', 'Algebra', 'Applications', 'LinearAlgebra']
created: 2026-05-17
updated: 2026-05-17
---

# 代数应用 (Applications of Algebra)

## 一、主成分分析 (PCA)

### 1.1 通过 SVD 实现

对数据中心化后的矩阵 $X$（$n$ 个样本，$d$ 个特征）：

$$ X_{\text{centered}} = X - \bar{X} $$

$$ \bar{X} = \frac{1}{n} \sum_{i=1}^n X_i $$

SVD 分解：

$$ X_{\text{centered}} = U \Sigma V^T $$

- 主成分方向 = $V$ 的列（右奇异向量）
- 主成分得分 = $U \Sigma$
- 方差解释比例 = $\sigma_i^2 / \sum \sigma_j^2$

### 1.2 通过协方差矩阵实现

$$ \text{Cov}(X) = \frac{1}{n-1} X_{\text{centered}}^T X_{\text{centered}} = V \Lambda V^T $$

特征分解得到的主成分方向与 SVD 一致。

```python
import numpy as np

def pca(X, n_components):
    X_center = X - X.mean(axis=0)
    U, s, Vt = np.linalg.svd(X_center, full_matrices=False)
    components = Vt[:n_components]
    projected = X_center @ components.T
    var_ratio = s[:n_components]**2 / (s**2).sum()
    return projected, components, var_ratio
```

## 二、线性回归 (Linear Regression)

### 2.1 正规方程

$$ y = X\beta + \varepsilon $$

最小二乘解：

$$ \hat{\beta} = (X^T X)^{-1} X^T y $$

```python
import numpy as np

X = np.array([[1, 1], [1, 2], [1, 3]])  # 第一列为截距
y = np.array([1, 2, 3])
beta = np.linalg.inv(X.T @ X) @ X.T @ y
```

### 2.2 岭回归 (Ridge Regression)

加入 L2 正则化项：

$$ \hat{\beta}_{\text{ridge}} = (X^T X + \lambda I)^{-1} X^T y $$

### 2.3 Lasso 回归

加入 L1 正则化项，可产生稀疏解：

$$ \hat{\beta}_{\text{lasso}} = \arg\min \|y - X\beta\|^2 + \lambda\|\beta\|_1 $$

## 三、PageRank 算法

### 3.1 马尔可夫链

设网页间链接矩阵 $G$，其中 $G_{ij} = 1$ 表示网页 $j$ 链接到网页 $i$。

转移概率矩阵 $P$（归一化列）：

$$ P_{ij} = \frac{G_{ij}}{\sum_k G_{kj}} $$

### 3.2 PageRank 公式

$$ \mathbf{r} = d P \mathbf{r} + \frac{1-d}{n} \mathbf{1} $$

其中 $d$ 为阻尼因子（通常 $d=0.85$）。

等价于求解：

$$ (I - dP) \mathbf{r} = \frac{1-d}{n} \mathbf{1} $$

### 3.3 特征向量视角

PageRank 向量是转移矩阵 $M = dP + \frac{1-d}{n} \mathbf{1}\mathbf{1}^T$ 的主特征向量。

```python
import numpy as np

def pagerank(G, d=0.85, max_iter=100):
    n = G.shape[0]
    col_sums = G.sum(axis=0)
    P = G / col_sums
    M = d * P + (1-d) / n * np.ones((n, n))
    r = np.ones(n) / n
    for _ in range(max_iter):
        r_new = M @ r
        if np.linalg.norm(r_new - r, 1) < 1e-6:
            break
        r = r_new
    return r
```

## 四、图像压缩 (SVD)

### 4.1 SVD 近似压缩

对灰度图像矩阵 $A$，取前 $k$ 个奇异值：

$$ A_k = \sum_{i=1}^k \sigma_i u_i v_i^T $$

```python
import numpy as np
from PIL import Image

def compress_svd(img_path, k):
    img = Image.open(img_path).convert('L')
    A = np.array(img, dtype=float)
    U, s, Vt = np.linalg.svd(A, full_matrices=False)
    A_compressed = U[:, :k] @ np.diag(s[:k]) @ Vt[:k, :]
    return A_compressed
```

### 4.2 压缩比分析

原始存储：$m \times n$，压缩后存储：$k(m + n + 1)$。

$$ \text{压缩比} = \frac{k(m + n + 1)}{mn} $$

## 五、网络分析 (Network Analysis)

### 5.1 邻接矩阵

$A_{ij} = 1$ 若节点 $i$ 与 $j$ 相连，否则为 0。

### 5.2 图拉普拉斯 (Graph Laplacian)

$$ L = D - A $$

其中 $D$ 为度数对角矩阵。

### 5.3 谱聚类 (Spectral Clustering)

1. 计算标准化拉普拉斯 $L_{\text{norm}} = D^{-1/2} L D^{-1/2}$
2. 取前 $k$ 个最小特征值对应的特征向量
3. 对特征向量组成的矩阵进行 $k$-means 聚类

### 5.4 社区检测 (Community Detection)

模块度 (Modularity) 衡量社区划分质量：

$$ Q = \frac{1}{2m} \sum_{ij} \left[A_{ij} - \frac{k_i k_j}{2m}\right] \delta(c_i, c_j) $$

## 六、计算机图形学 (Computer Graphics)

### 6.1 仿射变换 (Affine Transformation)

$$ \begin{pmatrix} x' \\ y' \\ 1 \end{pmatrix} = \begin{pmatrix} a_{11} & a_{12} & t_x \\ a_{21} & a_{22} & t_y \\ 0 & 0 & 1 \end{pmatrix} \begin{pmatrix} x \\ y \\ 1 \end{pmatrix} $$

### 6.2 齐次坐标 (Homogeneous Coordinates)

三维空间的点 $(x,y,z)$ 用齐次坐标 $(x,y,z,1)$ 表示，平移、旋转、缩放统一为 $4 \times 4$ 矩阵表示。

### 6.3 旋转矩阵 (Rotation Matrix)

绕 $z$ 轴旋转 $\theta$：

$$ R_z(\theta) = \begin{pmatrix} \cos\theta & -\sin\theta & 0 & 0 \\ \sin\theta & \cos\theta & 0 & 0 \\ 0 & 0 & 1 & 0 \\ 0 & 0 & 0 & 1 \end{pmatrix} $$

### 6.4 透视投影 (Perspective Projection)

$$ P_{\text{persp}} = \begin{pmatrix} \frac{1}{\tan(\text{FOV}/2) \cdot \text{aspect}} & 0 & 0 & 0 \\ 0 & \frac{1}{\tan(\text{FOV}/2)} & 0 & 0 \\ 0 & 0 & \frac{z_f}{z_f - z_n} & \frac{-z_f z_n}{z_f - z_n} \\ 0 & 0 & 1 & 0 \end{pmatrix} $$

## 七、错误纠正码 (Error-Correcting Codes)

### 7.1 汉明码 (Hamming Code)

生成矩阵 $G$ 和校验矩阵 $H$ 满足 $G H^T = 0$。接收向量 $r$，计算校正子 $s = r H^T$，定位并纠正错误。

### 7.2 线性码参数

$$ \text{码率} = \frac{k}{n}, \quad \text{最小距离} = d_{\min} $$

其中 $k$ 为信息位长度，$n$ 为码字长度，$d_{\min}$ 决定纠错能力。

## 八、微分方程 (Differential Equations)

### 8.1 矩阵指数 (Matrix Exponential)

线性系统 $\frac{d\mathbf{x}}{dt} = A\mathbf{x}$ 的解为：

$$ \mathbf{x}(t) = e^{At} \mathbf{x}(0) $$

```python
import numpy as np
from scipy.linalg import expm

A = np.array([[0, 1], [-1, 0]])
x0 = np.array([1, 0])
t = 1.0
xt = expm(A * t) @ x0
```

### 8.2 特征值分解与稳定性

$\dot{\mathbf{x}} = A\mathbf{x}$ 的稳定性由 $A$ 的特征值决定：
- 所有 $\text{Re}(\lambda_i) < 0$：稳定
- 存在 $\text{Re}(\lambda_i) > 0$：不稳定
- 存在 $\text{Re}(\lambda_i) = 0$：临界

## 九、量子力学 (Quantum Mechanics)

### 9.1 矩阵表示 (Matrix Representation)

量子态用向量表示，可观测量用厄米矩阵表示：

$$ \hat{H}|\psi\rangle = E|\psi\rangle $$

### 9.2 泡利矩阵 (Pauli Matrices)

$$ \sigma_x = \begin{pmatrix} 0 & 1 \\ 1 & 0 \end{pmatrix},\quad \sigma_y = \begin{pmatrix} 0 & -i \\ i & 0 \end{pmatrix},\quad \sigma_z = \begin{pmatrix} 1 & 0 \\ 0 & -1 \end{pmatrix} $$

## 十、密码学 (Cryptography)

### 10.1 希尔密码 (Hill Cipher)

消息向量 $m$，密钥矩阵 $K$：

$$ c = K \cdot m \mod 26 $$

解密要求 $K$ 可逆 $\mod 26$。

### 10.2 椭圆曲线密码学 (ECC)

椭圆曲线方程：

$$ y^2 = x^3 + ax + b $$

ECC 的安全性基于椭圆曲线离散对数问题 (ECDLP) 的计算困难性。

## 相关条目

[[02_NaturalSciences/Mathematics/Geometry/INDEX|Geometry]], [[02_NaturalSciences/Mathematics/NumberTheory/INDEX|NumberTheory]], [[02_NaturalSciences/Mathematics/MathematicalAnalysis/INDEX|MathematicalAnalysis]], LinearAlgebra

