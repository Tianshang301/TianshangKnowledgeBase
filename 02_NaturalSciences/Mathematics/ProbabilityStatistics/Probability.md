# 概率论基础

## 一、基本概��?
### 样本空间与事��?
- **样本空间 $\Omega$**：所有可能结果的集合
- **事件**��?\Omega$ 的子��?
### 概率公理

1. $P(A) \geq 0$（非负性）
2. $P(\Omega) = 1$（规范性）
3. ��?$A_1, A_2, \dots$ 互斥，则 $P(\bigcup_i A_i) = \sum_i P(A_i)$（可列可加性）

### 条件概率

$$P(A \mid B) = \frac{P(A \cap B)}{P(B)}, \quad P(B) > 0$$

### 全概率公��?
��?$\{B_i\}$ ��?$\Omega$ 的一个划分，则：

$$P(A) = \sum_i P(A \mid B_i) P(B_i)$$

### 贝叶斯定��?
**简单形��?*��?$$P(A \mid B) = \frac{P(B \mid A) P(A)}{P(B)}$$

**全概率展开形式**��?$$P(B_i \mid A) = \frac{P(A \mid B_i) P(B_i)}{\sum_j P(A \mid B_j) P(B_j)}$$

### 独立��?
$A$ ��?$B$ 独立 $\iff$ $P(A \cap B) = P(A) P(B)$

## 二、随机变��?
### 离散随机变量

**概率质量函数 (PMF)��?* $p_X(x) = P(X = x)$

**累积分布函数 (CDF)��?* $F_X(x) = P(X \leq x) = \sum_{t \leq x} p_X(t)$

### 连续随机变量

**概率密度函数 (PDF)��?* $f_X(x)$，满��?$\int_{-\infty}^\infty f_X(x) \, dx = 1$

$$P(a \leq X \leq b) = \int_a^b f_X(x) \, dx$$

**CDF��?* $F_X(x) = \int_{-\infty}^x f_X(t) \, dt$

$$f_X(x) = \frac{d}{dx} F_X(x)$$

## 三、期望与��?
### 期望

离散��?E[X] = \sum_x x p_X(x)$
连续��?E[X] = \int_{-\infty}^\infty x f_X(x) \, dx$

### 方差

$$\text{Var}(X) = E[(X - \mu)^2] = E[X^2] - (E[X])^2$$

### 协方差与相关系数

$$\text{Cov}(X, Y) = E[(X - \mu_X)(Y - \mu_Y)] = E[XY] - E[X]E[Y]$$

$$\rho_{XY} = \frac{\text{Cov}(X, Y)}{\sigma_X \sigma_Y} \in [-1, 1]$$

### 矩母函数 (MGF)

$$M_X(t) = E[e^{tX}]$$

性质��?E[X^n] = M_X^{(n)}(0)$

## 四、常见离散分��?
| 分布 | PMF | $E[X]$ | $\text{Var}(X)$ |
|------|-----|--------|-----------------|
| Bernoulli$(p)$ | $p^x (1-p)^{1-x}$ | $p$ | $p(1-p)$ |
| Binomial$(n,p)$ | $\binom{n}{x} p^x (1-p)^{n-x}$ | $np$ | $np(1-p)$ |
| Geometric$(p)$ | $(1-p)^{x-1}p$ | $1/p$ | $(1-p)/p^2$ |
| Poisson$(\lambda)$ | $e^{-\lambda} \lambda^x / x!$ | $\lambda$ | $\lambda$ |
| Uniform$(N)$ | $1/N$ | $(N+1)/2$ | $(N^2-1)/12$ |

## 五、常见连续分��?
| 分布 | PDF | $E[X]$ | $\text{Var}(X)$ |
|------|-----|--------|-----------------|
| Uniform$(a,b)$ | $1/(b-a)$ | $(a+b)/2$ | $(b-a)^2/12$ |
| Normal$(\mu,\sigma^2)$ | $\frac{1}{\sigma\sqrt{2\pi}} e^{-(x-\mu)^2/(2\sigma^2)}$ | $\mu$ | $\sigma^2$ |
| Exponential$(\lambda)$ | $\lambda e^{-\lambda x}$ | $1/\lambda$ | $1/\lambda^2$ |
| Gamma$(\alpha,\beta)$ | $\frac{\beta^\alpha}{\Gamma(\alpha)} x^{\alpha-1} e^{-\beta x}$ | $\alpha/\beta$ | $\alpha/\beta^2$ |
| Beta$(\alpha,\beta)$ | $\frac{\Gamma(\alpha+\beta)}{\Gamma(\alpha)\Gamma(\beta)} x^{\alpha-1}(1-x)^{\beta-1}$ | $\frac{\alpha}{\alpha+\beta}$ | $\frac{\alpha\beta}{(\alpha+\beta)^2(\alpha+\beta+1)}$ |

### 正态分��?
标准正��?PDF��?\phi(z) = \frac{1}{\sqrt{2\pi}} e^{-z^2/2}$

标准化：$Z = \frac{X - \mu}{\sigma} \sim N(0,1)$

### 卡方分布

��?$Z_i \sim N(0,1)$ 独立，则 $\sum_{i=1}^k Z_i^2 \sim \chi^2(k)$

### $t$-分布

$$T = \frac{Z}{\sqrt{Y/k}} \sim t(k)$$

其中 $Z \sim N(0,1)$��?Y \sim \chi^2(k)$ 独立��?
## 六、极限定��?
### 大数定律 (LLN)

样本均��?$\bar{X}_n = \frac{1}{n}\sum_{i=1}^n X_i$ 依概率收敛于 $\mu$��?
$$\bar{X}_n \xrightarrow{P} \mu$$

### 中心极限定理 (CLT)

$$\frac{\bar{X}_n - \mu}{\sigma/\sqrt{n}} \xrightarrow{d} N(0,1)$$

即样本均值的分布��?$n$ 增大趋近于正态分布��?

## 相关条目

[[02_NaturalSciences/Mathematics/MathematicalAnalysis/INDEX|MathematicalAnalysis]], [[07_InterdisciplinarySciences/DataScience/INDEX|DataScience]], [[02_NaturalSciences/Mathematics/Algebra/INDEX|Algebra]], StatisticalInference
