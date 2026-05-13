# 绾挎€т唬鏁板簲鐢?
## 涓€銆佷富鎴愬垎鍒嗘瀽 (PCA)

### 閫氳繃 SVD 瀹炵幇

瀵规暟鎹腑蹇冨寲鍚庣殑鐭╅樀 $X$锛?n$ 涓牱鏈紝$d$ 涓壒寰侊級锛?
$$X_{\text{centered}} = X - \bar{X}$$

$$\bar{X} = \frac{1}{n} \sum_{i=1}^n X_i$$

SVD 鍒嗚В锛?
$$X_{\text{centered}} = U \Sigma V^T$$

- 涓绘垚鍒嗘柟鍚?= $V$ 鐨勫垪锛堝彸濂囧紓鍚戦噺锛?- 涓绘垚鍒嗗緱鍒?= $U \Sigma$
- 鏂瑰樊瑙ｉ噴姣斾緥 = $\sigma_i^2 / \sum \sigma_j^2$

### 閫氳繃鍗忔柟宸煩闃靛疄鐜?
$$\text{Cov}(X) = \frac{1}{n-1} X_{\text{centered}}^T X_{\text{centered}} = V \Lambda V^T$$

鐗瑰緛鍒嗚В寰楀埌鐨勪富鎴愬垎鏂瑰悜涓?SVD 涓€鑷淬€?
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

## 浜屻€佺嚎鎬у洖褰?
### 姝ｈ鏂圭▼

$$y = X\beta + \varepsilon$$

鏈€灏忎簩涔樿В锛?
$$\hat{\beta} = (X^T X)^{-1} X^T y$$

```python
import numpy as np

X = np.array([[1, 1], [1, 2], [1, 3]])  # 绗竴鍒椾负鎴窛
y = np.array([1, 2, 3])
beta = np.linalg.inv(X.T @ X) @ X.T @ y
```

## 涓夈€丳ageRank 绠楁硶

### 椹皵鍙か閾?
璁剧綉椤甸棿閾炬帴鐭╅樀 $G$锛屽叾涓?$G_{ij} = 1$ 琛ㄧず缃戦〉 $j$ 閾炬帴鍒扮綉椤?$i$銆?
杞Щ姒傜巼鐭╅樀 $P$锛堝綊涓€鍖栧垪锛夛細

$$P_{ij} = \frac{G_{ij}}{\sum_k G_{kj}}$$

### PageRank 鍏紡

$$\mathbf{r} = d P \mathbf{r} + \frac{1-d}{n} \mathbf{1}$$

鍏朵腑 $d$ 涓洪樆灏煎洜瀛愶紙閫氬父 $d=0.85$锛夈€?
绛変环浜庢眰瑙ｏ細

$$(I - dP) \mathbf{r} = \frac{1-d}{n} \mathbf{1}$$

### 鐗瑰緛鍚戦噺瑙嗚

PageRank 鍚戦噺鏄浆绉荤煩闃?$M = dP + \frac{1-d}{n} \mathbf{1}\mathbf{1}^T$ 鐨勪富鐗瑰緛鍚戦噺銆?
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

## 鍥涖€佸浘鍍忓帇缂?(SVD)

### SVD 杩戜技鍘嬬缉

瀵圭伆搴﹀浘鍍忕煩闃?$A$锛屽彇鍓?$k$ 涓寮傚€硷細

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

## 浜斻€佺綉缁滃垎鏋?
### 閭绘帴鐭╅樀

$A_{ij} = 1$ 鑻ヨ妭鐐?$i$ 涓?$j$ 鐩歌繛锛屽惁鍒欎负 0銆?
### 鍥炬媺鏅媺鏂?
$$L = D - A$$

鍏朵腑 $D$ 涓哄害鏁板瑙掔煩闃点€?
### 璋辫仛绫?
1. 璁＄畻鏍囧噯鍖栨媺鏅媺鏂?$L_{\text{norm}} = D^{-1/2} L D^{-1/2}$
2. 鍙栧墠 $k$ 涓渶灏忕壒寰佸€煎搴旂殑鐗瑰緛鍚戦噺
3. 瀵圭壒寰佸悜閲忕粍鎴愮殑鐭╅樀杩涜 $k$-means 鑱氱被

## 鍏€佽绠楁満鍥惧舰瀛?
### 浠垮皠鍙樻崲

$$\begin{pmatrix} x' \\ y' \\ 1 \end{pmatrix} = \begin{pmatrix} a_{11} & a_{12} & t_x \\ a_{21} & a_{22} & t_y \\ 0 & 0 & 1 \end{pmatrix} \begin{pmatrix} x \\ y \\ 1 \end{pmatrix}$$

### 榻愭鍧愭爣

涓夌淮绌洪棿鐨勭偣 $(x,y,z)$ 鐢ㄩ綈娆″潗鏍?$(x,y,z,1)$ 琛ㄧず锛屽钩绉汇€佹棆杞€佺缉鏀剧粺涓€鐢?$4 \times 4$ 鐭╅樀琛ㄧず銆?
### 鏃嬭浆鐭╅樀

缁?$z$ 杞存棆杞?$\theta$锛?
$$R_z(\theta) = \begin{pmatrix} \cos\theta & -\sin\theta & 0 & 0 \\ \sin\theta & \cos\theta & 0 & 0 \\ 0 & 0 & 1 & 0 \\ 0 & 0 & 0 & 1 \end{pmatrix}$$

## 涓冦€侀敊璇籂姝ｇ爜

### 姹夋槑鐮?
鐢熸垚鐭╅樀 $G$ 鍜屾牎楠岀煩闃?$H$ 婊¤冻 $G H^T = 0$銆傛帴鏀跺悜閲?$r$锛岃绠楁牎姝ｅ瓙 $s = r H^T$锛屽畾浣嶅苟绾犳閿欒銆?
## 鍏€佸井鍒嗘柟绋?
### 鐭╅樀鎸囨暟

绾挎€х郴缁?$\frac{d\mathbf{x}}{dt} = A\mathbf{x}$ 鐨勮В锛?
$$\mathbf{x}(t) = e^{At} \mathbf{x}(0)$$

```python
import numpy as np
from scipy.linalg import expm

A = np.array([[0, 1], [-1, 0]])
x0 = np.array([1, 0])
t = 1.0
xt = expm(A * t) @ x0
```

## 鐩稿叧鏉＄洰

[[02_NaturalSciences/Mathematics/Geometry/INDEX|Geometry]], [[02_NaturalSciences/Mathematics/NumberTheory/INDEX|NumberTheory]], [[02_NaturalSciences/Mathematics/MathematicalAnalysis/INDEX|MathematicalAnalysis]], LinearAlgebra
