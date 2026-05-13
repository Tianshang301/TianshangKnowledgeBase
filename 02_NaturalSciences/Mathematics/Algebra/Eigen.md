# 鐗瑰緛鍊间笌鐗瑰緛鍚戦噺

## 涓€銆佸畾涔変笌鍑犱綍鎰忎箟

### 瀹氫箟

璁?$A$ 涓?$n \times n$ 鐭╅樀锛岃嫢瀛樺湪闈為浂鍚戦噺 $v$ 鍜屾爣閲?$\lambda$ 浣垮緱锛?
$$A v = \lambda v$$

鍒?$\lambda$ 涓虹壒寰佸€硷紝$v$ 涓哄搴旂殑鐗瑰緛鍚戦噺銆?
**鍑犱綍鎰忎箟锛?* 鐗瑰緛鍚戦噺鍦?$A$ 浣滅敤涓嬪彧鍙戠敓浼哥缉锛屼笉鏀瑰彉鏂瑰悜銆備几缂╁€嶆暟涓?$\lambda$銆?
### 鐗瑰緛澶氶」寮?
$$p(\lambda) = \det(A - \lambda I) = 0$$

$p(\lambda)$ 涓?$n$ 娆″椤瑰紡锛屽叾鏍瑰嵆涓虹壒寰佸€笺€?
### Gershgorin鍦嗙洏瀹氱悊

姣忎釜鐗瑰緛鍊?$\lambda$ 浣嶄簬鑷冲皯涓€涓渾鐩樺唴锛?$$|\lambda - a_{ii}| \le \sum_{j \neq i} |a_{ij}|$$

### Rayleigh鍟?
$$\lambda_{min} \le R(x) = \frac{x^T A x}{x^T x} \le \lambda_{max}$$

### 骞傝凯浠ｆ硶

$$v_{k+1} = \frac{A v_k}{\|A v_k\|}, \quad \lambda^{(k)} = v_k^T A v_k$$

鏀舵暃鍒版ā鏈€澶х殑鐗瑰緛鍊煎拰瀵瑰簲鐗瑰緛鍚戦噺銆?
### 浠ｆ暟閲嶆暟涓庡嚑浣曢噸鏁?
- **浠ｆ暟閲嶆暟**锛氱壒寰佸€间綔涓虹壒寰佸椤瑰紡鏍圭殑閲嶆暟
- **鍑犱綍閲嶆暟**锛?\dim(\text{Null}(A - \lambda I))$锛屽嵆瀵瑰簲鐗瑰緛绌洪棿鐨勭淮鏁?- 鍑犱綍閲嶆暟 $\leq$ 浠ｆ暟閲嶆暟

## 浜屻€佸瑙掑寲 (Diagonalization)

### 鍙瑙掑寲鏉′欢

$A$ 鍙瑙掑寲 $\iff$ 瀵规瘡涓壒寰佸€硷紝鍑犱綍閲嶆暟 = 浠ｆ暟閲嶆暟 $\iff$ $A$ 鏈?$n$ 涓嚎鎬ф棤鍏崇殑鐗瑰緛鍚戦噺銆?
### 瀵硅鍖栬繃绋?
鑻?$A$ 鍙瑙掑寲锛屽垯瀛樺湪鍙€嗙煩闃?$P$ 鍜屽瑙掔煩闃?$D$ 浣垮緱锛?
$$A = P D P^{-1}$$

鍏朵腑 $P$ 鐨勫垪鏄?$A$ 鐨勭壒寰佸悜閲忥紝$D$ 鐨勫瑙掔嚎涓哄搴旂殑鐗瑰緛鍊笺€?
**搴旂敤锛?*
$$A^n = P D^n P^{-1}$$

### 鐗瑰緛鍩?(Eigenbasis)

鐢辩壒寰佸悜閲忔瀯鎴愮殑涓€缁勫熀绉颁负鐗瑰緛鍩恒€傚湪鐗瑰緛鍩轰笅锛岀嚎鎬у彉鎹㈣〃绀轰负瀵硅鐭╅樀銆?
## 涓夈€佸绉扮煩闃电殑璋卞畾鐞?
### 瀹炲绉扮煩闃?
鑻?$A = A^T$锛堝疄瀵圭О锛夛紝鍒欙細
- 鎵€鏈夌壒寰佸€间负瀹炴暟
- 涓嶅悓鐗瑰緛鍊煎搴旂殑鐗瑰緛鍚戦噺姝ｄ氦
- 瀛樺湪姝ｄ氦鐭╅樀 $Q$锛?Q^T Q = I$锛変娇寰楋細

$$A = Q \Lambda Q^T$$

鍏朵腑 $\Lambda$ 涓哄瑙掔煩闃碉紝$Q$ 鐨勫垪涓烘爣鍑嗘浜ょ殑鐗瑰緛鍚戦噺銆?
## 鍥涖€佷簩娆″瀷 (Quadratic Forms)

### 瀹氫箟

$$Q(x) = x^T A x = \sum_{i=1}^n \sum_{j=1}^n a_{ij} x_i x_j$$

鍏朵腑 $A$ 涓哄绉扮煩闃点€?
### 瀹氬€兼€?(Definiteness)

- **姝ｅ畾**锛?x^T A x > 0$ 瀵规墍鏈?$x \neq 0$锛涚壒寰佸€煎叏姝?- **鍗婃瀹?*锛?x^T A x \geq 0$锛涚壒寰佸€奸潪璐?- **璐熷畾**锛?x^T A x < 0$锛涚壒寰佸€煎叏璐?- **涓嶅畾**锛氱壒寰佸€兼湁姝ｆ湁璐?
### 涓诲瓙寮忓垽鍒硶

$A$ 姝ｅ畾 $\iff$ 鎵€鏈夐『搴忎富瀛愬紡 $> 0$銆?
## 浜斻€佸寮傚€煎垎瑙?(SVD)

### 瀹氫箟

浠绘剰 $m \times n$ 鐭╅樀 $A$ 鍙垎瑙ｄ负锛?
$$A = U \Sigma V^T$$

- $U$锛?m \times m$ 姝ｄ氦鐭╅樀锛堝乏濂囧紓鍚戦噺锛?- $V$锛?n \times n$ 姝ｄ氦鐭╅樀锛堝彸濂囧紓鍚戦噺锛?- $\Sigma$锛?m \times n$ 瀵硅鐭╅樀锛屽瑙掔嚎涓哄寮傚€?$\sigma_1 \geq \sigma_2 \geq \cdots \geq \sigma_r > 0$

### 绱у噾 SVD

$$A = U_r \Sigma_r V_r^T$$

鍏朵腑浠呬繚鐣?$r = \text{rank}(A)$ 涓潪闆跺寮傚€笺€?
### 涓庣壒寰佸€肩殑鍏崇郴

$$\sigma_i^2 = \lambda_i(A^T A) = \lambda_i(A A^T)$$

$V$ 鐨勫垪鏄?$A^T A$ 鐨勭壒寰佸悜閲忥紝$U$ 鐨勫垪鏄?$A A^T$ 鐨勭壒寰佸悜閲忋€?
### 鐭╅樀杩戜技 (Eckart-Young 瀹氱悊)

淇濈暀鍓?$k$ 涓渶澶у寮傚€煎緱鍒?$A$ 鐨勬渶浣崇З $k$ 杩戜技锛?
$$A_k = U_k \Sigma_k V_k^T$$

### 浼€?(Pseudoinverse)

$$A^+ = V \Sigma^+ U^T$$

鍏朵腑 $\Sigma^+$ 灏?$\Sigma$ 鐨勯潪闆跺瑙掑厓鍙栧€掓暟銆?
```python
import numpy as np
from numpy.linalg import svd

A = np.array([[1, 2], [3, 4], [5, 6]], dtype=float)
U, s, Vt = svd(A)
Sigma = np.zeros((3, 2))
Sigma[:2, :2] = np.diag(s)

# 绱у噾 SVD
A_approx = U[:, :2] @ np.diag(s) @ Vt[:2, :]

# 绉? 杩戜技
A_rank1 = s[0] * np.outer(U[:, 0], Vt[0, :])

# 浼€?A_pinv = Vt.T @ np.diag(1/s) @ U[:, :2].T
```

### 鐭╅樀鍒嗚В瀵规瘮

| 鍒嗚В | 閫傜敤鐭╅樀 | 褰㈠紡 | 鍞竴鎬?| 鐢ㄩ€?|
|:---|:---|:---|:---:|:---|
| LU | 鏂归樀 | $A = LU$ | 涓嶅敮涓€ | 瑙ｇ嚎鎬ф柟绋嬬粍 |
| QR | 浠绘剰 | $A = QR$ | 鍞竴锛?R>0$锛?| 鏈€灏忎簩涔?|
| 鐗瑰緛鍒嗚В | 鍙瑙掑寲鏂归樀 | $A = PDP^{-1}$ | 涓嶅敮涓€ | 鐭╅樀骞傘€佽氨鍒嗘瀽 |
| SVD | 浠绘剰鐭╅樀 | $A = U\Sigma V^T$ | 鍞竴 | 闄嶇淮銆佷吉閫嗐€佸帇缂?|

## 鐩稿叧鏉＄洰

[[02_NaturalSciences/Mathematics/Geometry/INDEX|Geometry]], [[02_NaturalSciences/Mathematics/NumberTheory/INDEX|NumberTheory]], [[02_NaturalSciences/Mathematics/MathematicalAnalysis/INDEX|MathematicalAnalysis]], LinearAlgebra
