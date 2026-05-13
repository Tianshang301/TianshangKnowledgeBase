# 线性代数应��?
## 一、主成分分析 (PCA)

### 通过 SVD 实现

对数据中心化后的矩阵 $X$��?n$ 个样本，$d$ 个特征）��?
$$X_{\text{centered}} = X - \bar{X}$$

$$\bar{X} = \frac{1}{n} \sum_{i=1}^n X_i$$

SVD 分解��?
$$X_{\text{centered}} = U \Sigma V^T$$

- 主成分方��?= $V$ 的列（右奇异向量��?- 主成分得��?= $U \Sigma$
- 方差解释比例 = $\sigma_i^2 / \sum \sigma_j^2$

### 通过协方差矩阵实��?
$$\text{Cov}(X) = \frac{1}{n-1} X_{\text{centered}}^T X_{\text{centered}} = V \Lambda V^T$$

特征分解得到的主成分方向��?SVD 一致��?
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

## 二、线性回��?
### 正规方程

$$y = X\beta + \varepsilon$$

最小二乘解��?
$$\hat{\beta} = (X^T X)^{-1} X^T y$$

```python
import numpy as np

X = np.array([[1, 1], [1, 2], [1, 3]])  # 第一列为截距
y = np.array([1, 2, 3])
beta = np.linalg.inv(X.T @ X) @ X.T @ y
```

## 三、PageRank 算法

### 马尔可夫��?
设网页间链接矩阵 $G$，其��?$G_{ij} = 1$ 表示网页 $j$ 链接到网��?$i$��?
转移概率矩阵 $P$（归一化列）：

$$P_{ij} = \frac{G_{ij}}{\sum_k G_{kj}}$$

### PageRank 公式

$$\mathbf{r} = d P \mathbf{r} + \frac{1-d}{n} \mathbf{1}$$

其中 $d$ 为阻尼因子（通常 $d=0.85$）��?
等价于求解：

$$(I - dP) \mathbf{r} = \frac{1-d}{n} \mathbf{1}$$

### 特征向量视角

PageRank 向量是转移矩��?$M = dP + \frac{1-d}{n} \mathbf{1}\mathbf{1}^T$ 的主特征向量��?
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

## 四、图像压��?(SVD)

### SVD 近似压缩

对灰度图像矩��?$A$，取��?$k$ 个奇异值：

$$A_k = \sum_{i=1}^k \sigma_i u_i v_i^T$$

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

## 五、网络分��?
### 邻接矩阵

$A_{ij} = 1$ 若节��?$i$ ��?$j$ 相连，否则为 0��?
### 图拉普拉��?
$$L = D - A$$

其中 $D$ 为度数对角矩阵��?
### 谱聚��?
1. 计算标准化拉普拉��?$L_{\text{norm}} = D^{-1/2} L D^{-1/2}$
2. 取前 $k$ 个最小特征值对应的特征向量
3. 对特征向量组成的矩阵进行 $k$-means 聚类

## 六、计算机图形��?
### 仿射变换

$$\begin{pmatrix} x' \\ y' \\ 1 \end{pmatrix} = \begin{pmatrix} a_{11} & a_{12} & t_x \\ a_{21} & a_{22} & t_y \\ 0 & 0 & 1 \end{pmatrix} \begin{pmatrix} x \\ y \\ 1 \end{pmatrix}$$

### 齐次坐标

三维空间的点 $(x,y,z)$ 用齐次坐��?$(x,y,z,1)$ 表示，平移、旋转、缩放统一��?$4 \times 4$ 矩阵表示��?
### 旋转矩阵

��?$z$ 轴旋��?$\theta$��?
$$R_z(\theta) = \begin{pmatrix} \cos\theta & -\sin\theta & 0 & 0 \\ \sin\theta & \cos\theta & 0 & 0 \\ 0 & 0 & 1 & 0 \\ 0 & 0 & 0 & 1 \end{pmatrix}$$

## 七、错误纠正码

### 汉明��?
生成矩阵 $G$ 和校验矩��?$H$ 满足 $G H^T = 0$。接收向��?$r$，计算校正子 $s = r H^T$，定位并纠正错误��?
## 八、微分方��?
### 矩阵指数

线性系��?$\frac{d\mathbf{x}}{dt} = A\mathbf{x}$ 的解��?
$$\mathbf{x}(t) = e^{At} \mathbf{x}(0)$$

```python
import numpy as np
from scipy.linalg import expm

A = np.array([[0, 1], [-1, 0]])
x0 = np.array([1, 0])
t = 1.0
xt = expm(A * t) @ x0
```

## 相关条目

[[02_NaturalSciences/Mathematics/Geometry/INDEX|Geometry]], [[02_NaturalSciences/Mathematics/NumberTheory/INDEX|NumberTheory]], [[02_NaturalSciences/Mathematics/MathematicalAnalysis/INDEX|MathematicalAnalysis]], LinearAlgebra
