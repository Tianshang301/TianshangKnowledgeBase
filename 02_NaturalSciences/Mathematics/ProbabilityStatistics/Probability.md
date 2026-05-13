# 姒傜巼璁哄熀纭€

## 涓€銆佸熀鏈蹇?
### 鏍锋湰绌洪棿涓庝簨浠?
- **鏍锋湰绌洪棿 $\Omega$**锛氭墍鏈夊彲鑳界粨鏋滅殑闆嗗悎
- **浜嬩欢**锛?\Omega$ 鐨勫瓙闆?
### 姒傜巼鍏悊

1. $P(A) \geq 0$锛堥潪璐熸€э級
2. $P(\Omega) = 1$锛堣鑼冩€э級
3. 鑻?$A_1, A_2, \dots$ 浜掓枼锛屽垯 $P(\bigcup_i A_i) = \sum_i P(A_i)$锛堝彲鍒楀彲鍔犳€э級

### 鏉′欢姒傜巼

$$P(A \mid B) = \frac{P(A \cap B)}{P(B)}, \quad P(B) > 0$$

### 鍏ㄦ鐜囧叕寮?
鑻?$\{B_i\}$ 涓?$\Omega$ 鐨勪竴涓垝鍒嗭紝鍒欙細

$$P(A) = \sum_i P(A \mid B_i) P(B_i)$$

### 璐濆彾鏂畾鐞?
**绠€鍗曞舰寮?*锛?$$P(A \mid B) = \frac{P(B \mid A) P(A)}{P(B)}$$

**鍏ㄦ鐜囧睍寮€褰㈠紡**锛?$$P(B_i \mid A) = \frac{P(A \mid B_i) P(B_i)}{\sum_j P(A \mid B_j) P(B_j)}$$

### 鐙珛鎬?
$A$ 涓?$B$ 鐙珛 $\iff$ $P(A \cap B) = P(A) P(B)$

## 浜屻€侀殢鏈哄彉閲?
### 绂绘暎闅忔満鍙橀噺

**姒傜巼璐ㄩ噺鍑芥暟 (PMF)锛?* $p_X(x) = P(X = x)$

**绱Н鍒嗗竷鍑芥暟 (CDF)锛?* $F_X(x) = P(X \leq x) = \sum_{t \leq x} p_X(t)$

### 杩炵画闅忔満鍙橀噺

**姒傜巼瀵嗗害鍑芥暟 (PDF)锛?* $f_X(x)$锛屾弧瓒?$\int_{-\infty}^\infty f_X(x) \, dx = 1$

$$P(a \leq X \leq b) = \int_a^b f_X(x) \, dx$$

**CDF锛?* $F_X(x) = \int_{-\infty}^x f_X(t) \, dt$

$$f_X(x) = \frac{d}{dx} F_X(x)$$

## 涓夈€佹湡鏈涗笌鐭?
### 鏈熸湜

绂绘暎锛?E[X] = \sum_x x p_X(x)$
杩炵画锛?E[X] = \int_{-\infty}^\infty x f_X(x) \, dx$

### 鏂瑰樊

$$\text{Var}(X) = E[(X - \mu)^2] = E[X^2] - (E[X])^2$$

### 鍗忔柟宸笌鐩稿叧绯绘暟

$$\text{Cov}(X, Y) = E[(X - \mu_X)(Y - \mu_Y)] = E[XY] - E[X]E[Y]$$

$$\rho_{XY} = \frac{\text{Cov}(X, Y)}{\sigma_X \sigma_Y} \in [-1, 1]$$

### 鐭╂瘝鍑芥暟 (MGF)

$$M_X(t) = E[e^{tX}]$$

鎬ц川锛?E[X^n] = M_X^{(n)}(0)$

## 鍥涖€佸父瑙佺鏁ｅ垎甯?
| 鍒嗗竷 | PMF | $E[X]$ | $\text{Var}(X)$ |
|------|-----|--------|-----------------|
| Bernoulli$(p)$ | $p^x (1-p)^{1-x}$ | $p$ | $p(1-p)$ |
| Binomial$(n,p)$ | $\binom{n}{x} p^x (1-p)^{n-x}$ | $np$ | $np(1-p)$ |
| Geometric$(p)$ | $(1-p)^{x-1}p$ | $1/p$ | $(1-p)/p^2$ |
| Poisson$(\lambda)$ | $e^{-\lambda} \lambda^x / x!$ | $\lambda$ | $\lambda$ |
| Uniform$(N)$ | $1/N$ | $(N+1)/2$ | $(N^2-1)/12$ |

## 浜斻€佸父瑙佽繛缁垎甯?
| 鍒嗗竷 | PDF | $E[X]$ | $\text{Var}(X)$ |
|------|-----|--------|-----------------|
| Uniform$(a,b)$ | $1/(b-a)$ | $(a+b)/2$ | $(b-a)^2/12$ |
| Normal$(\mu,\sigma^2)$ | $\frac{1}{\sigma\sqrt{2\pi}} e^{-(x-\mu)^2/(2\sigma^2)}$ | $\mu$ | $\sigma^2$ |
| Exponential$(\lambda)$ | $\lambda e^{-\lambda x}$ | $1/\lambda$ | $1/\lambda^2$ |
| Gamma$(\alpha,\beta)$ | $\frac{\beta^\alpha}{\Gamma(\alpha)} x^{\alpha-1} e^{-\beta x}$ | $\alpha/\beta$ | $\alpha/\beta^2$ |
| Beta$(\alpha,\beta)$ | $\frac{\Gamma(\alpha+\beta)}{\Gamma(\alpha)\Gamma(\beta)} x^{\alpha-1}(1-x)^{\beta-1}$ | $\frac{\alpha}{\alpha+\beta}$ | $\frac{\alpha\beta}{(\alpha+\beta)^2(\alpha+\beta+1)}$ |

### 姝ｆ€佸垎甯?
鏍囧噯姝ｆ€?PDF锛?\phi(z) = \frac{1}{\sqrt{2\pi}} e^{-z^2/2}$

鏍囧噯鍖栵細$Z = \frac{X - \mu}{\sigma} \sim N(0,1)$

### 鍗℃柟鍒嗗竷

鑻?$Z_i \sim N(0,1)$ 鐙珛锛屽垯 $\sum_{i=1}^k Z_i^2 \sim \chi^2(k)$

### $t$-鍒嗗竷

$$T = \frac{Z}{\sqrt{Y/k}} \sim t(k)$$

鍏朵腑 $Z \sim N(0,1)$锛?Y \sim \chi^2(k)$ 鐙珛銆?
## 鍏€佹瀬闄愬畾鐞?
### 澶ф暟瀹氬緥 (LLN)

鏍锋湰鍧囧€?$\bar{X}_n = \frac{1}{n}\sum_{i=1}^n X_i$ 渚濇鐜囨敹鏁涗簬 $\mu$锛?
$$\bar{X}_n \xrightarrow{P} \mu$$

### 涓績鏋侀檺瀹氱悊 (CLT)

$$\frac{\bar{X}_n - \mu}{\sigma/\sqrt{n}} \xrightarrow{d} N(0,1)$$

鍗虫牱鏈潎鍊肩殑鍒嗗竷闅?$n$ 澧炲ぇ瓒嬭繎浜庢鎬佸垎甯冦€?

## 鐩稿叧鏉＄洰

[[02_NaturalSciences/Mathematics/MathematicalAnalysis/INDEX|MathematicalAnalysis]], [[07_InterdisciplinarySciences/DataScience/INDEX|DataScience]], [[02_NaturalSciences/Mathematics/Algebra/INDEX|Algebra]], StatisticalInference
