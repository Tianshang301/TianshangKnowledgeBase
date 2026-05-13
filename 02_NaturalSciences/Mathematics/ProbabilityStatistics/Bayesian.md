# 璐濆彾鏂粺璁?
## 涓€銆佽礉鍙舵柉鎺ㄦ柇鍩虹

### 璐濆彾鏂畾鐞?
$$p(\theta \mid y) = \frac{p(y \mid \theta) p(\theta)}{p(y)} = \frac{p(y \mid \theta) p(\theta)}{\int p(y \mid \theta) p(\theta) \, d\theta}$$

- $p(\theta)$锛氬厛楠屽垎甯?(Prior)
- $p(y \mid \theta)$锛氫技鐒?(Likelihood)
- $p(\theta \mid y)$锛氬悗楠屽垎甯?(Posterior)
- $p(y)$锛氳竟闄呬技鐒?(Evidence)

### 鍏辫江鍏堥獙

| 浼肩劧 | 鍏辫江鍏堥獙 | 鍚庨獙 |
|------|----------|------|
| Bernoulli$(p)$ | Beta$(\alpha, \beta)$ | Beta$(\alpha + \sum y_i, \beta + n - \sum y_i)$ |
| Poisson$(\lambda)$ | Gamma$(\alpha, \beta)$ | Gamma$(\alpha + \sum y_i, \beta + n)$ |
| Normal$(\mu, \sigma^2)$锛?\sigma^2$ 宸茬煡锛?| Normal$(\mu_0, \sigma_0^2)$ | Normal$(\frac{\mu_0/\sigma_0^2 + n\bar{y}/\sigma^2}{1/\sigma_0^2 + n/\sigma^2}, \frac{1}{1/\sigma_0^2 + n/\sigma^2})$ |

### 璐濆彾鏂?vs 棰戠巼瀛︽淳

| 鏂归潰 | 棰戠巼瀛︽淳 | 璐濆彾鏂?|
|------|---------|--------|
| 鍙傛暟 $\theta$ | 鍥哄畾鏈煡甯告暟 | 闅忔満鍙橀噺 |
| 姒傜巼鍚箟 | 闀挎湡棰戠巼 | 淇″康绋嬪害 |
| 鎺ㄦ柇渚濇嵁 | 浼肩劧 | 鍚庨獙鍒嗗竷 |
| 鍖洪棿浼拌 | 缃俊鍖洪棿 | 鍙俊鍖洪棿 |

## 浜屻€佽礉鍙舵柉绾挎€у洖褰?
### 妯″瀷

$$y \sim N(X\beta, \sigma^2 I)$$
$$\beta \sim N(0, \tau^2 I)$$

### 鍚庨獙

$$\beta \mid y \sim N\left( \frac{1}{\sigma^2} \Sigma X^T y, \ \Sigma \right)$$

鍏朵腑 $\Sigma = \left( \frac{1}{\sigma^2} X^T X + \frac{1}{\tau^2} I \right)^{-1}$

璐濆彾鏂嚎鎬у洖褰掔殑 MAP 浼拌绛変环浜?Ridge 鍥炲綊銆?
## 涓夈€佸彲淇″尯闂?vs 缃俊鍖洪棿

- **Credible Interval**锛?P(\theta \in [a,b] \mid y) = 1 - \alpha$锛屽弬鏁版槸闅忔満鐨勶紝鍖洪棿鍥哄畾
- **Confidence Interval**锛?P(\text{鍖洪棿鍖呭惈 } \theta) = 1 - \alpha$锛屽弬鏁板浐瀹氾紝鍖洪棿闅忔満

## 鍥涖€侀┈灏斿彲澶摼钂欑壒鍗℃礇 (MCMC)

### 涓轰粈涔堥渶瑕?MCMC

褰撳悗楠屽垎甯冩棤闂紡瑙ｆ椂锛岀敤閲囨牱杩戜技鍚庨獙銆?
### Metropolis-Hastings 绠楁硶

1. 浠庡綋鍓嶇姸鎬?$\theta^{(t)}$ 寮€濮?2. 浠庢彁璁垎甯?$q(\theta^* \mid \theta^{(t)})$ 閲囨牱鍊欓€?$\theta^*$
3. 璁＄畻鎺ュ彈姒傜巼锛?
$$\alpha = \min\left(1, \frac{p(\theta^* \mid y) q(\theta^{(t)} \mid \theta^*)}{p(\theta^{(t)} \mid y) q(\theta^* \mid \theta^{(t)})}\right)$$

4. 浠ユ鐜?$\alpha$ 鎺ュ彈 $\theta^{(t+1)} = \theta^*$锛屽惁鍒?$\theta^{(t+1)} = \theta^{(t)}$

### Gibbs 閲囨牱

姣忔浠庝竴涓潯浠跺悗楠屽垎甯冧腑閲囨牱锛?
$$\theta_1^{(t+1)} \sim p(\theta_1 \mid \theta_2^{(t)}, \theta_3^{(t)}, \dots, y)$$
$$\theta_2^{(t+1)} \sim p(\theta_2 \mid \theta_1^{(t+1)}, \theta_3^{(t)}, \dots, y)$$
$$\vdots$$

```python
import numpy as np
import pymc as pm

# PyMC 绀轰緥锛氳礉鍙舵柉绾挎€у洖褰?data = np.random.randn(100)
y = 2 * data + 1 + np.random.randn(100) * 0.5

with pm.Model():
    # 鍏堥獙
    alpha = pm.Normal('alpha', mu=0, sigma=10)
    beta = pm.Normal('beta', mu=0, sigma=10)
    sigma = pm.HalfNormal('sigma', sigma=1)
    
    # 浼肩劧
    mu = alpha + beta * data
    y_obs = pm.Normal('y_obs', mu=mu, sigma=sigma, observed=y)
    
    # MCMC 閲囨牱
    trace = pm.sample(1000, tune=500)
    
    # 鍚庨獙鎽樿
    print(pm.summary(trace))
```

## 浜斻€佽礉鍙舵柉璁＄畻宸ュ叿

### PyMC

- 鐢?Python 瀹炵幇鐨勬鐜囩紪绋嬫鏋?- 鏀寔鑷姩 MCMC锛圢UTS 閲囨牱鍣級
- 閫傚悎涓皬瑙勬ā妯″瀷

### Stan

- 鐙珛鐨勬鐜囩紪绋嬭瑷€
- 浣跨敤 HMC/NUTS 楂樻晥閲囨牱
- Python 鎺ュ彛锛歅yStan锛圕mdStanPy锛?- 閫傚悎澶嶆潅妯″瀷

## 鍏€佸簲鐢?
- **A/B 娴嬭瘯**锛氳礉鍙舵柉鏂规硶鎻愪緵 $P(\text{A 浼樹簬 B})$ 鐨勭洿鎺ユ鐜?- **璐濆彾鏂垎灞傛ā鍨?*锛氬鐞嗗垎缁勬暟鎹紙濡備笉鍚屽鏍＄殑鑰冭瘯鎴愮哗锛?- **璐濆彾鏂紭鍖?*锛氳秴鍙傛暟璋冧紭锛圙aussian Process + acquisition function锛?- **璐濆彾鏂椂闂村簭鍒?*锛氱粨鏋勬椂闂村簭鍒楁ā鍨?

## 鐩稿叧鏉＄洰

[[02_NaturalSciences/Mathematics/MathematicalAnalysis/INDEX|MathematicalAnalysis]], [[07_InterdisciplinarySciences/DataScience/INDEX|DataScience]], [[02_NaturalSciences/Mathematics/Algebra/INDEX|Algebra]], StatisticalInference
