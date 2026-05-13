# 缁熻鎺ㄦ柇

## 涓€銆佺偣浼拌 (Point Estimation)

### 鏈€澶т技鐒朵及璁?(MLE)

$$\hat{\theta}_{\text{MLE}} = \arg\max_\theta L(\theta; x) = \arg\max_\theta \prod_{i=1}^n f(x_i \mid \theta)$$

閫氬父鏈€澶у寲瀵规暟浼肩劧 $\ell(\theta) = \ln L(\theta)$銆?
### 鐭╀及璁?(Method of Moments)

浠ゆ牱鏈煩绛変簬鎬讳綋鐭╋紝瑙ｅ嚭鍙傛暟锛?
$$\frac{1}{n}\sum_{i=1}^n X_i^k = E[X^k]$$

### 浼拌閲忔€ц川

- **鏃犲亸鎬?*锛?E[\hat{\theta}] = \theta$
- **涓€鑷存€?*锛?\hat{\theta} \xrightarrow{P} \theta$锛?n \to \infty$锛?- **鏈夋晥鎬?*锛氭柟宸渶灏忕殑鏃犲亸浼拌
- **MSE**锛?\text{MSE}(\hat{\theta}) = E[(\hat{\theta} - \theta)^2] = \text{Var}(\hat{\theta}) + \text{Bias}(\hat{\theta})^2$

## 浜屻€佸尯闂翠及璁?
### 鎬讳綋鍧囧€肩殑缃俊鍖洪棿

**鏂瑰樊宸茬煡锛?z$-鍖洪棿锛夛細**
$$\bar{X} \pm z_{\alpha/2} \cdot \frac{\sigma}{\sqrt{n}}$$

**鏂瑰樊鏈煡锛?t$-鍖洪棿锛夛細**
$$\bar{X} \pm t_{\alpha/2, n-1} \cdot \frac{s}{\sqrt{n}}$$

### 鎬讳綋姣斾緥鐨勭疆淇″尯闂?
$$\hat{p} \pm z_{\alpha/2} \sqrt{\frac{\hat{p}(1-\hat{p})}{n}}$$

### 鎬讳綋鏂瑰樊鐨勭疆淇″尯闂?
$$\left( \frac{(n-1)s^2}{\chi^2_{\alpha/2, n-1}}, \frac{(n-1)s^2}{\chi^2_{1-\alpha/2, n-1}} \right)$$

## 涓夈€佸亣璁炬楠?
### 鍩烘湰姒傚康

- $H_0$锛氶浂鍋囪锛?H_1$锛氬鎷╁亣璁?- **Type I Error**锛氭嫆缁濈湡瀹?$H_0$锛?\alpha$锛?- **Type II Error**锛氭帴鍙楅敊璇?$H_0$锛?\beta$锛?- **Power**锛?1 - \beta$锛屾纭嫆缁?$H_0$ 鐨勬鐜?
### 妫€楠屾楠?
1. 鎻愬嚭 $H_0$ 鍜?$H_1$
2. 閫夋嫨妫€楠岀粺璁￠噺
3. 缁欏畾鏄捐憲鎬ф按骞?$\alpha$
4. 璁＄畻 p-value 鎴栨嫆缁濆煙
5. 鍋氬嚭缁撹

### 甯歌妫€楠?
| 妫€楠?| 鐢ㄩ€?| 缁熻閲?|
|------|------|--------|
| $z$-test | 鍗曟€讳綋鍧囧€硷紙$\sigma$ 宸茬煡锛?| $z = \frac{\bar{x} - \mu_0}{\sigma/\sqrt{n}}$ |
| $t$-test | 鍗曟€讳綋鍧囧€硷紙$\sigma$ 鏈煡锛?| $t = \frac{\bar{x} - \mu_0}{s/\sqrt{n}}$ |
| 閰嶅 $t$-test | 閰嶅鏁版嵁宸紓 | $t = \frac{\bar{d}}{s_d/\sqrt{n}}$ |
| 鍙屾牱鏈?$t$-test | 涓ゆ€讳綋鍧囧€兼瘮杈?| $t = \frac{\bar{x}_1 - \bar{x}_2}{\sqrt{s_1^2/n_1 + s_2^2/n_2}}$ |
| $\chi^2$ 妫€楠?| 鎷熷悎浼樺害/鐙珛鎬?| $\chi^2 = \sum \frac{(O_i - E_i)^2}{E_i}$ |
| $F$-test | 鏂瑰樊榻愭€?ANOVA | $F = \frac{s_1^2}{s_2^2}$ |

### ANOVA

鍗曞洜绱犳柟宸垎鏋愶細

$$F = \frac{\text{MSB}}{\text{MSW}} = \frac{\text{SSB}/(k-1)}{\text{SSW}/(n-k)}$$

鍏朵腑 SSB 涓虹粍闂村钩鏂瑰拰锛孲SW 涓虹粍鍐呭钩鏂瑰拰銆?
### p-value 瑙ｉ噴

p-value = 鍦?$H_0$ 涓虹湡鐨勬潯浠朵笅锛岃瀵熷埌褰撳墠鎴栨洿鏋佺缁撴灉鐨勬鐜囥€俻-value < $\alpha$ 鏃舵嫆缁?$H_0$銆?
## 鍥涖€侀潪鍙傛暟妫€楠?
| 妫€楠?| 鐢ㄩ€?| 瀵瑰簲鍙傛暟妫€楠?|
|------|------|--------------|
| Mann-Whitney $U$ | 涓ょ嫭绔嬫牱鏈瘮杈?| 鍙屾牱鏈?$t$-test |
| Wilcoxon 绗﹀彿绉?| 閰嶅鏍锋湰姣旇緝 | 閰嶅 $t$-test |
| Kruskal-Wallis | 澶氱粍鐙珛鏍锋湰姣旇緝 | ANOVA |
| Spearman $\rho$ | 绉╃浉鍏?| Pearson 鐩稿叧 |

## 浜斻€佸閲嶆楠屾牎姝?
### Bonferroni 鏍℃

$$\alpha_{\text{adj}} = \frac{\alpha}{m}$$

鍏朵腑 $m$ 涓烘瘮杈冩鏁般€備繚瀹堜絾绠€鍗曘€?
### FDR (False Discovery Rate)

Benjamini-Hochberg 鏂规硶锛?1. 灏?p-value 浠庡皬鍒板ぇ鎺掑簭锛?p_{(1)} \leq p_{(2)} \leq \cdots \leq p_{(m)}$
2. 鎵惧埌鏈€澶?$k$ 浣垮緱 $p_{(k)} \leq \frac{k}{m} \cdot q$
3. 鎷掔粷鎵€鏈?$H_{(i)}$锛?i = 1, \dots, k$

```python
import numpy as np
from scipy import stats

# 鍗曟牱鏈?t-test
data = np.array([2.3, 2.1, 2.5, 2.4, 2.2])
t_stat, p_val = stats.ttest_1samp(data, popmean=2.0)

# 鍙屾牱鏈?t-test
group1 = np.array([2.3, 2.1, 2.5])
group2 = np.array([3.1, 3.3, 2.9])
t_stat, p_val = stats.ttest_ind(group1, group2)

# 鍗℃柟妫€楠?from scipy.stats import chi2_contingency
obs = np.array([[10, 20], [15, 25]])
chi2, p, dof, expected = chi2_contingency(obs)

# Mann-Whitney U
u_stat, p_val = stats.mannwhitneyu(group1, group2)
```

## 鐩稿叧鏉＄洰

[[02_NaturalSciences/Mathematics/MathematicalAnalysis/INDEX|MathematicalAnalysis]], [[07_InterdisciplinarySciences/DataScience/INDEX|DataScience]], [[02_NaturalSciences/Mathematics/Algebra/INDEX|Algebra]], StatisticalInference
