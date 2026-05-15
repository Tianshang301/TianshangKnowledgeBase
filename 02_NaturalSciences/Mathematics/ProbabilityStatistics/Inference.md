---
aliases: [Inference]
tags: ['Mathematics', 'ProbabilityStatistics', 'Inference']
---

# 统计推断



## 一、点估计 (Point Estimation)



### 最大似然估��?(MLE)



$$\hat{\theta}_{\text{MLE}} = \arg\max_\theta L(\theta; x) = \arg\max_\theta \prod_{i=1}^n f(x_i \mid \theta)$$



通常最大化对数似然 $\ell(\theta) = \ln L(\theta)$��?

### 矩估��?(Method of Moments)



令样本矩等于总体矩，解出参数��?

$$\frac{1}{n}\sum_{i=1}^n X_i^k = E[X^k]$$



### 估计量性质



- **无偏��?*��?E[\hat{\theta}] = \theta$

- **一致��?*��?\hat{\theta} \xrightarrow{P} \theta$��?n \to \infty$��?- **有效��?*：方差最小的无偏估计

- **MSE**��?\text{MSE}(\hat{\theta}) = E[(\hat{\theta} - \theta)^2] = \text{Var}(\hat{\theta}) + \text{Bias}(\hat{\theta})^2$



## 二、区间估��?

### 总体均值的置信区间



**方差已知��?z$-区间）：**

$$\bar{X} \pm z_{\alpha/2} \cdot \frac{\sigma}{\sqrt{n}}$$



**方差未知��?t$-区间）：**

$$\bar{X} \pm t_{\alpha/2, n-1} \cdot \frac{s}{\sqrt{n}}$$



### 总体比例的置信区��?

$$\hat{p} \pm z_{\alpha/2} \sqrt{\frac{\hat{p}(1-\hat{p})}{n}}$$



### 总体方差的置信区��?

$$\left( \frac{(n-1)s^2}{\chi^2_{\alpha/2, n-1}}, \frac{(n-1)s^2}{\chi^2_{1-\alpha/2, n-1}} \right)$$



## 三、假设检��?

### 基本概念



- $H_0$：零假设��?H_1$：备择假��?- **Type I Error**：拒绝真��?$H_0$��?\alpha$��?- **Type II Error**：接受错��?$H_0$��?\beta$��?- **Power**��?1 - \beta$，正确拒��?$H_0$ 的概��?

### 检验步��?

1. 提出 $H_0$ ��?$H_1$

2. 选择检验统计量

3. 给定显著性水��?$\alpha$

4. 计算 p-value 或拒绝域

5. 做出结论



### 常见检��?

| 检��?| 用��?| 统计��?|

|------|------|--------|

| $z$-test | 单总体均值（$\sigma$ 已知��?| $z = \frac{\bar{x} - \mu_0}{\sigma/\sqrt{n}}$ |

| $t$-test | 单总体均值（$\sigma$ 未知��?| $t = \frac{\bar{x} - \mu_0}{s/\sqrt{n}}$ |

| 配对 $t$-test | 配对数据差异 | $t = \frac{\bar{d}}{s_d/\sqrt{n}}$ |

| 双样��?$t$-test | 两总体均值比��?| $t = \frac{\bar{x}_1 - \bar{x}_2}{\sqrt{s_1^2/n_1 + s_2^2/n_2}}$ |

| $\chi^2$ 检��?| 拟合优度/独立��?| $\chi^2 = \sum \frac{(O_i - E_i)^2}{E_i}$ |

| $F$-test | 方差齐��?ANOVA | $F = \frac{s_1^2}{s_2^2}$ |



### ANOVA



单因素方差分析：



$$F = \frac{\text{MSB}}{\text{MSW}} = \frac{\text{SSB}/(k-1)}{\text{SSW}/(n-k)}$$



其中 SSB 为组间平方和，SSW 为组内平方和��?

### p-value 解释



p-value = ��?$H_0$ 为真的条件下，观察到当前或更极端结果的概率。p-value < $\alpha$ 时拒��?$H_0$��?

## 四、非参数检��?

| 检��?| 用��?| 对应参数检��?|

|------|------|--------------|

| Mann-Whitney $U$ | 两独立样本比��?| 双样��?$t$-test |

| Wilcoxon 符号��?| 配对样本比较 | 配对 $t$-test |

| Kruskal-Wallis | 多组独立样本比较 | ANOVA |

| Spearman $\rho$ | 秩相��?| Pearson 相关 |



## 五、多重检验校��?

### Bonferroni 校正



$$\alpha_{\text{adj}} = \frac{\alpha}{m}$$



其中 $m$ 为比较次数。保守但简单��?

### FDR (False Discovery Rate)



Benjamini-Hochberg 方法��?1. ��?p-value 从小到大排序��?p_{(1)} \leq p_{(2)} \leq \cdots \leq p_{(m)}$

2. 找到最��?$k$ 使得 $p_{(k)} \leq \frac{k}{m} \cdot q$

3. 拒绝所��?$H_{(i)}$��?i = 1, \dots, k$



```python

import numpy as np

from scipy import stats



# 单样��?t-test

data = np.array([2.3, 2.1, 2.5, 2.4, 2.2])

t_stat, p_val = stats.ttest_1samp(data, popmean=2.0)



# 双样��?t-test

group1 = np.array([2.3, 2.1, 2.5])

group2 = np.array([3.1, 3.3, 2.9])

t_stat, p_val = stats.ttest_ind(group1, group2)



# 卡方检��?from scipy.stats import chi2_contingency

obs = np.array([[10, 20], [15, 25]])

chi2, p, dof, expected = chi2_contingency(obs)



# Mann-Whitney U

u_stat, p_val = stats.mannwhitneyu(group1, group2)

```



## 相关条目



[[02_NaturalSciences/Mathematics/MathematicalAnalysis/INDEX|MathematicalAnalysis]], [[07_InterdisciplinarySciences/DataScience/INDEX|DataScience]], [[02_NaturalSciences/Mathematics/Algebra/INDEX|Algebra]], StatisticalInference

