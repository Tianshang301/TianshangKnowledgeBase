---
aliases: [EngineeringStatistics]
tags: ['EngineeringFundamentals', 'EngineeringMathematics', 'EngineeringStatistics.md']
created: 2026-05-17
updated: 2026-05-17
---

---
aliases: [EngineeringStatistics]
tags: ['04_EngineeringAndTechnology', 'EngineeringFundamentals', 'EngineeringMathematics']
---

# 工程统计学 (Engineering Statistics)

## 一、概述

工程统计学 (Engineering Statistics) 是应用统计方法解决工程问题的学科，涵盖数据收集与整理 (Data Collection)、概率建模 (Probability Modeling)、统计推断 (Statistical Inference)、实验设计 (Design of Experiments, DOE) 和质量控制 (Quality Control)。
工程师使用统计方法分析实验数据、评估产品可靠性 (Reliability)、监控生产过程 (Process Monitoring) 和进行科学决策。
统计思维 (Statistical Thinking) 是连接理论与实践的定量工具，在六西格玛 (Six Sigma)、SPC (Statistical Process Control, 统计过程控制) 和 DOE 中具有核心地位。
数据驱动的工程决策越来越依赖于统计学方法。

## 二、描述性统计 (Descriptive Statistics)

### 2.1 集中趋势 (Central Tendency)

均值 (Mean)：$\bar{x} = \frac{1}{n}\sum_{i=1}^n x_i$
中位数 (Median)：排序后中间值 (或两中间值平均)，对偏态分布 (Skewed Distribution) 稳健。
众数 (Mode)：最高频率值 (Highest Frequency)。
几何均值 (Geometric Mean)：$\bar{x}_g = \sqrt[n]{\prod x_i}$，适用于比率数据和增长率计算。

### 2.2 离散程度 (Dispersion)

方差 (Variance)：$s^2 = \frac{1}{n-1}\sum(x_i-\bar{x})^2$
标准差 (Standard Deviation)：$s = \sqrt{s^2}$
极差 (Range)：$R = x_{max} - x_{min}$
四分位距 (Interquartile Range, IQR)：$IQR = Q_3 - Q_1$
变异系数 (Coefficient of Variation, CV)：$CV = \frac{s}{\bar{x}} \times 100\%$

### 2.3 可视化 (Visualization)

```mermaid
graph TD
    A[可视化] --> B[数值型 Numerical]
    A --> C[分类型 Categorical]
    B --> D[直方图 Histogram]
    B --> E[箱线图 Box Plot]
    B --> F[散点图 Scatter Plot]
    B --> G[Q-Q 图 (正态概率图)]
    C --> H[条形图 Bar Chart]
    C --> I[帕累托图 Pareto Chart]
```

箱线图异常值 (Outlier) 判定：$< Q_1 - 1.5 IQR$ 或 $> Q_3 + 1.5 IQR$ (Tukey's Rule)。

## 三、概率基础 (Probability Fundamentals)

### 3.1 概率公理 (Axioms)

$P(A) \geq 0$，$P(\Omega) = 1$ (样本空间, Sample Space)，$P(A\cup B) = P(A)+P(B)-P(A\cap B)$

### 3.2 条件概率与贝叶斯 (Conditional Probability & Bayes)

$P(A|B) = \frac{P(A\cap B)}{P(B)}$ (条件概率)
全概率公式 (Law of Total Probability)：$P(B) = \sum P(B|A_i)P(A_i)$
贝叶斯定理 (Bayes' Theorem)：$P(A_i|B) = \frac{P(B|A_i)P(A_i)}{\sum P(B|A_j)P(A_j)}$

### 3.3 常见概率分布 (Common Probability Distributions)

**离散分布 (Discrete Distributions)**：

| 分布 | PMF (概率质量函数) | $E[X]$ | $Var$ | 应用 |
|------|-----|--------|-------|------|
| 二项分布 $B(n,p)$ | $\binom{n}{k}p^k(1-p)^{n-k}$ | $np$ | $np(1-p)$ | 次品数 (Defects) |
| Poisson 分布 $P(\lambda)$ | $\frac{e^{-\lambda}\lambda^k}{k!}$ | $\lambda$ | $\lambda$ | 故障次数 (Failures) |
| 几何分布 $G(p)$ | $(1-p)^{k-1}p$ | $1/p$ | $(1-p)/p^2$ | 首次成功时间 |
| 超几何分布 | $\frac{\binom{K}{k}\binom{N-K}{n-k}}{\binom{N}{n}}$ | $nK/N$ | - | 不放回抽样 (Without Replacement) |

**连续分布 (Continuous Distributions)**：

| 分布 | PDF (概率密度函数) | 均值 | 方差 |
|------|-----|------|------|
| 正态分布 $N(\mu,\sigma^2)$ | $\frac{1}{\sigma\sqrt{2\pi}}e^{-\frac{(x-\mu)^2}{2\sigma^2}}$ | $\mu$ | $\sigma^2$ |
| 指数分布 $Exp(\lambda)$ | $\lambda e^{-\lambda x}$ | $1/\lambda$ | $1/\lambda^2$ |
| 均匀分布 $U(a,b)$ | $1/(b-a)$ | $(a+b)/2$ | $(b-a)^2/12$ |
| Weibull 分布 $W(k,\lambda)$ | $\frac{k}{\lambda}(\frac{x}{\lambda})^{k-1}e^{-(x/\lambda)^k}$ | $\lambda\Gamma(1+1/k)$ | - |
| $t$ 分布 $t(\nu)$ | $\frac{\Gamma(\frac{\nu+1}{2})}{\sqrt{\nu\pi}\Gamma(\frac{\nu}{2})}(1+\frac{t^2}{\nu})^{-(\nu+1)/2}$ | 0 (对称) | $\frac{\nu}{\nu-2}$ |

### 3.4 中心极限定理 (Central Limit Theorem, CLT)

$$\bar{X} \sim N(\mu, \sigma^2/n) \ \text{当} \ n \to \infty$$

$n \geq 30$ 近似足够 (Rule of Thumb)，但偏态分布 (Highly Skewed) 需更大样本量。CLT 是统计推断的基石——即使总体分布未知，样本均值的抽样分布仍近似正态。

## 四、参数估计 (Parameter Estimation)

### 4.1 点估计 (Point Estimation)

矩估计法 (MOM, Method of Moments)：令样本矩 (Sample Moments) = 总体矩 (Population Moments)。
最大似然估计 (MLE, Maximum Likelihood Estimation)：$\hat{\theta}_{MLE} = \arg\max \prod f(x_i|\theta)$

正态分布 MLE：$\hat{\mu} = \bar{x}$，$\hat{\sigma}^2_{MLE} = \frac{1}{n}\sum(x_i-\bar{x})^2$

### 4.2 区间估计 (Interval Estimation)

均值 (方差已知, $z$)：$\bar{x} \pm z_{\alpha/2} \cdot \sigma/\sqrt{n}$
均值 (方差未知, $t$)：$\bar{x} \pm t_{\alpha/2,n-1} \cdot s/\sqrt{n}$
方差：$\left(\frac{(n-1)s^2}{\chi^2_{\alpha/2}}, \frac{(n-1)s^2}{\chi^2_{1-\alpha/2}}\right)$

## 五、假设检验 (Hypothesis Testing)

### 5.1 基本步骤

$H_0$ (原假设, Null Hypothesis) vs $H_1$ (备择假设, Alternative Hypothesis) → $\alpha$ (显著性水平) → 检验统计量 → $p$ 值 → 决策。

第 I 类错误 (Type I Error) $\alpha$ (拒真, False Positive)，第 II 类错误 (Type II Error) $\beta$ (纳伪, False Negative)。检验功效 (Power) $1-\beta$。

### 5.2 常用检验

| 检验 | 统计量 | $H_0$ |
|------|--------|-------|
| $z$ 单样本 | $z = \frac{\bar{x}-\mu_0}{\sigma/\sqrt{n}}$ | $\mu = \mu_0$ |
| $t$ 单样本 | $t = \frac{\bar{x}-\mu_0}{s/\sqrt{n}}$ | $\mu = \mu_0$ |
| 两样本 $t$ (独立) | $t = \frac{\bar{x}_1-\bar{x}_2}{s_p\sqrt{1/n_1+1/n_2}}$ | $\mu_1 = \mu_2$ |
| 配对 $t$ (Paired) | $t = \frac{\bar{d}}{s_d/\sqrt{n}}$ | $\mu_d = 0$ |
| $\chi^2$ 方差 | $\chi^2 = \frac{(n-1)s^2}{\sigma_0^2}$ | $\sigma^2 = \sigma_0^2$ |
| $F$ 方差比 | $F = \frac{s_1^2}{s_2^2}$ | $\sigma_1^2 = \sigma_2^2$ |
| $\chi^2$ 独立性 | $\chi^2 = \sum\frac{(O-E)^2}{E}$ | 两变量独立 |

### 5.3 $p$ 值 (P-Value)

$p$ 值 = $P($数据或更极端 $| H_0)$。$p < \alpha$ 拒绝 $H_0$。$p$ 值越小证据越强，但不应机械地使用 $p<0.05$ 阈值。

## 六、方差分析 (ANOVA, Analysis of Variance)

### 6.1 单因素 ANOVA (One-Way)

$SS_T = SS_{Tr} + SS_E$ (总平方和 = 处理平方和 + 误差平方和)
$F = \frac{MS_{Tr}}{MS_E} = \frac{SS_{Tr}/(k-1)}{SS_E/(n-k)}$

### 6.2 双因素 ANOVA (Two-Way, 含交互作用)

$SS_T = SS_A + SS_B + SS_{AB} + SS_E$
事后多重比较 (Post-Hoc Tests)：Tukey HSD (Honestly Significant Difference)、Bonferroni、Scheffe。

## 七、回归分析 (Regression Analysis)

### 7.1 简单线性回归 (Simple Linear)

$y_i = \beta_0 + \beta_1 x_i + \varepsilon_i$
$\hat{\beta}_1 = \frac{S_{xy}}{S_{xx}}$，$\hat{\beta}_0 = \bar{y} - \hat{\beta}_1 \bar{x}$
决定系数 (Coefficient of Determination)：$R^2 = \frac{SS_R}{SS_T} = 1 - \frac{SS_E}{SS_T}$

### 7.2 多元线性回归 (Multiple Linear)

$\mathbf{y} = \mathbf{X}\boldsymbol{\beta} + \boldsymbol{\varepsilon}$
$\hat{\boldsymbol{\beta}} = (\mathbf{X}^T\mathbf{X})^{-1}\mathbf{X}^T\mathbf{y}$

调整 $R^2$ (Adjusted $R^2$)：$R^2_{adj} = 1 - \frac{SS_E/(n-p-1)}{SS_T/(n-1)}$
VIF (Variance Inflation Factor, 方差膨胀因子) $= 1/(1-R_j^2)$，VIF > 10 表示严重多重共线性 (Multicollinearity)。

### 7.3 回归诊断 (Regression Diagnostics)

残差 vs 拟合值图 (Residuals vs Fitted)、Q-Q 图 (正态性检验)、Cook's D (强影响点诊断)、Durbin-Watson (自相关检验)。

## 八、统计过程控制 (SPC, Statistical Process Control)

$\bar{x}$ 图 (均值控制图)：$UCL = \bar{\bar{x}} + A_2\bar{R}$，$LCL = \bar{\bar{x}} - A_2\bar{R}$
$R$ 图 (极差控制图)：$UCL = D_4\bar{R}$，$LCL = D_3\bar{R}$
$p$ 图 (不合格品率控制图)：$UCL = \bar{p} + 3\sqrt{\frac{\bar{p}(1-\bar{p})}{n}}$

过程能力指数 (Process Capability Indices)：
$$C_p = \frac{USL-LSL}{6\sigma}, \quad C_{pk} = \min\left(\frac{USL-\bar{x}}{3\sigma}, \frac{\bar{x}-LSL}{3\sigma}\right)$$

$C_{pk} \geq 1.33$ 充足 (Capable)，$C_{pk} \geq 1.67$ 优秀 (Excellent)，$C_{pk} \geq 2.0$ 六西格玛水平。

## 九、实验设计 (DOE, Design of Experiments)

基本原理：随机化 (Randomization)、重复 (Replication)、区组化 (Blocking)。
$2^k$ 全因子设计 (Full Factorial)，$2^{k-p}$ 部分因子设计 (Fractional Factorial)，用于筛选重要因子。
响应面法 (RSM, Response Surface Methodology)：二阶模型寻优 (Optimization)。中心复合设计 (CCD, Central Composite Design) 和 Box-Behnken 设计是常用 RSM 设计。

## 十、非参数统计 (Nonparametric Statistics)

Wilcoxon 符号秩检验 (Wilcoxon Signed-Rank, 配对/单样本)、Mann-Whitney U 检验 (两独立样本)、Kruskal-Wallis 检验 (多组独立样本)、Spearman 秩相关系数 $\rho$ (Spearman Rank Correlation)。非参数方法不依赖总体分布假设。

## 十一、贝叶斯统计 (Bayesian Statistics)

后验 $\propto$ 似然 $\times$ 先验：$p(\theta|x) = \frac{p(x|\theta)p(\theta)}{p(x)}$
MCMC (Markov Chain Monte Carlo, 马尔可夫链蒙特卡洛, Gibbs/Metropolis-Hastings) 用于计算复杂后验分布。

## 相关条目

- [[INDEX|当前目录索引]]
- [[04_EngineeringAndTechnology/EngineeringFundamentals/EngineeringMathematics/INDEX]]

## 十二、贝叶斯统计 (Bayesian Statistics)

### 12.1 贝叶斯推断框架

贝叶斯定理将先验信息与样本数据结合：
 p(\theta | \mathbf{x}) = \frac{p(\mathbf{x} | \theta) \cdot p(\theta)}{p(\mathbf{x})} \propto \mathcal{L}(\theta | \mathbf{x}) \cdot p(\theta)

先验分布 (\theta)$ 反映参数 $\theta$ 的已知信息（无信息先验 Jeffreys Prior 或共轭先验 Conjugate Prior）。
似然函数 $\mathcal{L}(\theta | \mathbf{x})$ 由数据分布决定。
后验分布 (\theta | \mathbf{x})$ 是贝叶斯推断的核心输出。

**共轭先验 (Conjugate Prior)**：

| 似然分布 | 共轭先验 | 后验参数 |
|---------|---------|---------|
| 正态 (\mu, \sigma^2)$ (已知 $\sigma$) | 正态 (\mu_0, \sigma_0^2)$ | $\mu_n = \frac{\mu_0/\sigma_0^2 + n\bar{x}/\sigma^2}{1/\sigma_0^2 + n/\sigma^2}$ |
| 二项 (n, p)$ | Beta (\alpha, \beta)$ | (\alpha + k, \beta + n - k)$ |
| Poisson (\lambda)$ | Gamma (\alpha, \beta)$ | (\alpha + \sum x_i, \beta + n)$ |

### 12.2 MCMC 方法 (Markov Chain Monte Carlo)

后验分布复杂时无法解析求解，使用数值采样：

**Metropolis-Hastings 算法**：
1. 从提议分布 (Proposal Distribution) (\theta^* | \theta^{(t)})$ 生成候选参数 $\theta^*$
2. 计算接受概率 (Acceptance Probability)：$\alpha = \min\left(1, \frac{p(\theta^* | \mathbf{x}) q(\theta^{(t)} | \theta^*)}{p(\theta^{(t)} | \mathbf{x}) q(\theta^* | \theta^{(t)})}\right)$
3. 以概率 $\alpha$ 接受 $\theta^*$，否则保持 $\theta^{(t)}$

**Gibbs 采样 (Gibbs Sampling)**：从条件后验分布依次采样每个参数，无拒绝步骤。

**收敛诊断 (Convergence Diagnostics)**：Gelman-Rubin 统计量 $\hat{R}$、有效样本量 (ESS, Effective Sample Size)。

### 12.3 贝叶斯预测 (Bayesian Prediction)

后验预测分布 (Posterior Predictive Distribution)：
 p(\tilde{x} | \mathbf{x}) = \int p(\tilde{x} | \theta) \cdot p(\theta | \mathbf{x}) d\theta

贝叶斯预测自动考虑参数不确定性，预测区间比经典方法更宽但更准确。

## 十三、统计学习简介 (Statistical Learning)

### 13.1 偏差-方差权衡 (Bias-Variance Tradeoff)

 E[(y - \hat{f}(x))^2] = Bias[\hat{f}(x)]^2 + Var[\hat{f}(x)] + \sigma^2

- **高偏差 (High Bias)**：模型过于简单 (欠拟合, Underfitting)，如线性回归拟合非线性数据
- **高方差 (High Variance)**：模型过于复杂 (过拟合, Overfitting)，如高阶多项式
- **目标**：选择模型复杂度使测试误差 (Test Error) 最小化

### 13.2 交叉验证 (Cross-Validation)

**k 折交叉验证 (k-Fold CV)**：数据随机分为 k 个等份，k-1 份训练、1 份验证，轮流 k 次取平均误差。
**留一法 (LOOCV, Leave-One-Out Cross-Validation)**：n 个样本逐个留出验证，计算量大但无偏。

### 13.3 正则化 (Regularization)

**岭回归 (Ridge Regression, L2)**：
 \hat{\boldsymbol{\beta}}_{ridge} = \arg\min \left\{ \sum_{i=1}^n (y_i - \mathbf{x}_i^T \boldsymbol{\beta})^2 + \lambda \sum_{j=1}^p \beta_j^2 \right\}

**Lasso 回归 (L1)**：
 \hat{\boldsymbol{\beta}}_{lasso} = \arg\min \left\{ \sum_{i=1}^n (y_i - \mathbf{x}_i^T \boldsymbol{\beta})^2 + \lambda \sum_{j=1}^p |\beta_j| \right\}

Lasso 自动进行变量选择 (Variable Selection)，使部分系数收缩至零。

## 十四、时间序列分析 (Time Series Analysis)

### 14.1 平稳性 (Stationarity)

弱平稳 (Weak Stationarity)：均值 $\mu_t = \mu$ 为常数，自协方差 $\gamma(t, t+h) = \gamma(h)$ 仅与滞后阶数有关。

**ADF 检验 (Augmented Dickey-Fuller Test)**：$：序列存在单位根 (Unit Root, 非平稳)。 < 0.05$ 拒绝 $。

### 14.2 ARIMA 模型 (Autoregressive Integrated Moving Average)

**AR(p)**： = c + \phi_1 y_{t-1} + \phi_2 y_{t-2} + \cdots + \phi_p y_{t-p} + \varepsilon_t$
**MA(q)**： = c + \varepsilon_t + \theta_1 \varepsilon_{t-1} + \cdots + \theta_q \varepsilon_{t-q}$
**ARIMA(p,d,q)**：AR + 差分 (d 次) + MA

**模型选择**：AIC (Akaike Information Criterion) $= 2k - 2\ln(\hat{L})$ 或 BIC，选择 AIC/BIC 最小者。

## 十五、多元统计分析 (Multivariate Analysis)

### 15.1 主成分分析 (PCA, Principal Component Analysis)

降维 (Dimensionality Reduction)：寻找新坐标系使方差最大化。
主成分 (PC) 由协方差矩阵的特征向量 (Eigenvector) 决定。
**解释方差比例 (PVE, Proportion of Variance Explained)**：选择前 k 个 PC 使 PVE > 80%。

### 15.2 聚类分析 (Cluster Analysis)

**k-means 聚类**：最小化类内平方和 (WCSS)。需要预设聚类数 k，肘部法 (Elbow Method) 确定最优 k。
**层次聚类 (Hierarchical Clustering)**：自底向上凝聚 (Agglomerative) 或自顶向下分裂 (Divisive)，树状图 (Dendrogram) 展示聚类层次。

## 十六、工程应用案例

### 16.1 六西格玛 DMAIC 流程

**D (Define)**：定义项目目标和客户 CTQ (Critical to Quality)。
**M (Measure)**：测量当前过程性能基线 (Baseline Performance)。
**A (Analyze)**：统计分析找出根本原因 (Root Cause)。
**I (Improve)**：实施改进方案，DOE 验证。
**C (Control)**：SPC 控制图监控，维持改进成果。

### 16.2 可靠性工程中的统计方法

**Weibull 分析 (Weibull Analysis)**：产品寿命建模，估计特征寿命 (Characteristic Life) $\eta$ 和形状参数 $\beta$。

 R(t) = e^{-(t/\eta)^\beta}

$\beta < 1$：早期失效 (Infant Mortality)，$\beta = 1$：随机失效 (Random Failure, 指数分布)，$\beta > 1$：磨损失效 (Wear-out)。

**加速寿命试验 (ALT, Accelerated Life Testing)**：Arrhenius 模型 (温度加速)、逆幂律模型 (电压加速)。

 \text{AF} = e^{\frac{E_a}{k}\left(\frac{1}{T_{use}} - \frac{1}{T_{stress}}\right)}

### 16.3 测量系统分析 (MSA, Measurement System Analysis)

**Gage R&R (量具重复性与再现性)**：
 \sigma_{total}^2 = \sigma_{part}^2 + \sigma_{gage}^2 + \sigma_{appraiser}^2

GRR < 10% 可接受，10-30% 有条件接受，>30% 不可接受。

## 十七、工程统计软件与实现

### 17.1 常用统计软件比较

| 软件 | 特点 | 适用领域 | 价格 |
|------|------|---------|------|
| Minitab | 六西格玛和 DOE 专用，操作简便 | 质量控制、DOE、SPC | 商业软件 |
| JMP (SAS) | 交互式探索性分析，可视化强 | 研发实验设计 | 商业软件 |
| R | 开源，包丰富 (CRAN 2万+)，社区活跃 | 学术研究、高级分析 | 免费开源 |
| Python (SciPy/StatsModels) | 编程灵活，与 ML/深度学习集成 | 数据科学、机器学习 | 免费开源 |
| SPSS (IBM) | 社会学/医学统计专用 | 市场调研、问卷调查 | 商业软件 |
| MATLAB Statistics TB | 矩阵运算集成，工具箱丰富 | 工程计算、蒙特卡洛 | 商业软件 |

### 17.2 R/Python 实用代码示例

**Python 正态性检验 (Shapiro-Wilk Test)**：
`python
from scipy import stats
stat, p_value = stats.shapiro(data)
print(f'Statistic={stat:.4f}, p-value={p_value:.4f}')
if p_value > 0.05: print('Data looks Gaussian')
else: print('Data does not look Gaussian')
`

**R 线性回归诊断**：
`
model <- lm(y ~ x1 + x2, data = df)
summary(model)
plot(model)
vif(model)
`

### 17.3 统计结果报告规范

科学统计报告应包含：
- 样本量 $ 和缺失数据 (Missing Data) 说明
- 描述统计量 (均值±标准差，中位数[IQR])
- 检验统计量、自由度 (df) 和精确 $ 值
- 效应量 (Effect Size)：Cohen's d、$\eta^2$、^2$ 调整值
- 置信区间 (CI, Confidence Interval, 通常 95%)

**APA 格式示例**："A significant difference was found, (28) = 2.45$,  = .021$,  = 0.87$, 95% CI [0.14, 1.60]."

## 十八、统计陷阱与注意事项

### 18.1 常见统计错误

1. **多重比较问题 (Multiple Comparison Problem)**：多次检验不校正，增加 I 类错误。校正方法：Bonferroni、Holm-Bonferroni、FDR (Benjamini-Hochberg)。
2. **p-hacking**：反复分析数据直到找到显著结果，违背科学诚信。
3. **忽略假设条件**：t 检验要求正态性和方差齐性 (Homogeneity of Variance, Levene's Test)。不满足时使用 Welch's t 检验或非参数替代。
4. **异常值处理不当**：随意删除异常值 (Outlier) 可能导致偏差。应使用稳健统计方法或敏感性分析。
5. **混淆变量 (Confounding Variable)**：未控制第三变量导致虚假相关 (Spurious Correlation)。使用多变量回归或因果推断方法。

### 18.2 统计思维 (Statistical Thinking)

统计思维是工程师的基本素养：用数据而非直觉做决策，理解变异性 (Variability) 是自然现象，使用概率而非确定性语言表达不确定性。

**六西格玛统计思维核心**：
- 所有工作都是过程 (Process)
- 所有过程都有变异 (Variation)
- 所有变异都有原因 (Root Cause)
- 过程改进需要理解并控制变异源
