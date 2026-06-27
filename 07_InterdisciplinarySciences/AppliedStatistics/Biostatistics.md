---
aliases: [Biostatistics]
tags: ['AppliedStatistics', 'Biostatistics']
created: 2026-05-16
updated: 2026-05-16
---

# 生物统计?
## 概述

生物统计学是将统计学原理和方法应用于生物学和医学研究的交叉学科它为实验设计数据分析和科学推断提供定量工具，是现代生命科学研究不可或缺的方法论基础?
## 生物统计学基硢

### 假设棢?
假设棢验是生物统计学的核心方法之一，用于判断观察到的差异是否具有统计学意义?
**基本步骤?*
1. 建立原假设（H₢）和备择假设（H₁）
2. 选择显著性水平（α），通常?.05
3. 计算棢验统计量
4. 确定 P 值或临界?5. 做出统计决策

**常用棢验方法：**
- **t 棢?*：比较两组均值差异（独立样本 t 棢验配对 t 棢验）
- **方差分析（ANOVA?*：比较多组均值差?- **卡方棢?*：检验分类变量间的关联?- **非参数检?*：Wilcoxon 棢验 Kruskal-Wallis 棢验（数据不满足正态分布时使用?
**两类错误?*
- 第一类错误（α错误）：拒绝了正确的原假设（假阳性）
- 第二类错误（β错误）：接受了错误的原假设（假阴性）
- 统计功效?-β）：正确拒绝错误原假设的概率

### 常用棢验统计量公式

| 棢验方?| 棢验统计量 | 公式 | 用?|
|---------|-----------|------|------|
| **单样?t 棢?* | $t$ | $t = \dfrac{\bar{x} - \mu_0}{s/\sqrt{n}}$ | 样本均与已知总体均比?|
| **独立样本 t 棢?* | $t$ | $t = \dfrac{\bar{x}_1 - \bar{x}_2}{s_p\sqrt{\frac{1}{n_1}+\frac{1}{n_2}}}$ | 两组独立样本均比?|
| **配对 t 棢?* | $t$ | $t = \dfrac{\bar{d}}{s_d/\sqrt{n}}$ | 配对设计数据差比?|
| **单因?ANOVA** | $F$ | $F = \dfrac{MS_{\text{between}}}{MS_{\text{within}}}$ | 多组均比?|
| **卡方棢?* | $\chi^2$ | $\chi^2 = \sum \dfrac{(O_{ij} - E_{ij})^2}{E_{ij}}$ | 分类变量关联性检?|
| **F 棢验（方差齐）** | $F$ | $F = \dfrac{s_1^2}{s_2^2}$ | 两组方差是否相等 |

### 单因?ANOVA 分解

| 变异来源 | 平方?(SS) | 自由?(df) | 均方 (MS) | F ?|
|---------|------------|------------|-----------|------|
| **组间** | $SS_{\text{tr}} = \sum_{i=1}^{k} n_i(\bar{x}_i - \bar{\bar{x}})^2$ | $k-1$ | $MS_{\text{tr}} = \dfrac{SS_{\text{tr}}}{k-1}$ | $F = \dfrac{MS_{\text{tr}}}{MS_{\text{e}}}$ |
| **组内（误差）** | $SS_{\text{e}} = \sum_{i=1}^{k}\sum_{j=1}^{n_i}(x_{ij} - \bar{x}_i)^2$ | $N - k$ | $MS_{\text{e}} = \dfrac{SS_{\text{e}}}{N-k}$ | |
| **总变?* | $SS_{\text{tot}} = \sum_{i=1}^{k}\sum_{j=1}^{n_i}(x_{ij} - \bar{\bar{x}})^2$ | $N-1$ | | |

### 置信区间

置信区间提供参数估计的不确定性量化?
**均的置信区间?*
$$\bar{x} \pm t_{\alpha/2, df} \times \frac{s}{\sqrt{n}}$$

**比例的置信区间：**
$$\hat{p} \pm z_{\alpha/2} \times \sqrt{\frac{\hat{p}(1-\hat{p})}{n}}$$

**影响置信区间宽度的因素：**
- 样本量：样本量越大，区间越窄
- 变异程度：变异越大，区间越宽
- 置信水平：置信水平越高，区间越宽

## 常用实验设计

### 完全随机设计

完全随机设计（Completely Randomized Design, CRD）是朢箢单的实验设计?
**特点?*
- 试验单位随机分配到各处理?- 各处理组样本量可以相等或不等
- 适用于实验条件均匢的情?
**统计模型?*
$$y_{ij} = \mu + \tau_i + \varepsilon_{ij}$$

其中?y_{ij}$为观测，$\mu$为体均，$\tau_i$为处理效应，$\varepsilon_{ij}$为随机误差?
### 随机区组设计

随机区组设计（Randomized Block Design, RBD）过区组控制已知变异来源?
**设计原则?*
- 同一区组内试验单位尽可能相似
- 区组间允许存在差?- 每个区组内各处理随机排列

**优势?*
- 减少误差方差，提高检验功?- 可以分析区组效应
- 适用于实验材料异质较大的情况

### 析因设计

析因设计（Factorial Design）同时研究多个因素的效应及其交互作用?
**设计类型?*
- 2×2析因设计：两个因素，各两个水?- 3×3析因设计：两个因素，各三个水?- 多因素析因设计：三个及以上因?
**可分析的效应?*
- 主效应（Main Effect）：各因素的独立效应
- 交互效应（Interaction Effect）：因素间的联合效应

**应用实例?*
- 肥料×品种×密度的三因素试验
- 药物×剂量×给药时间的临床试?
## 生存分析

生存分析是研究事件发生时间数据的统计方法?
### Kaplan-Meier 曲线

Kaplan-Meier 曲线（乘积极限法）是非参数方法，用于估计生存函数?
**计算公式?*
$$S(t) = \prod_{t_i \leq t} \left(1 - \frac{d_i}{n_i}\right)$$

其中?d_i$为时?t_i$的事件数?n_i$为时?t_i$的风险人数?
**特点?*
- 可以处理删失数据
- 提供生存概率的阶梯函数估?- 可绘制生存曲线进行组间比?
### Cox 回归

Cox 比例风险模型是半参数方法，用于分析多个因素对生存时间的影响?
**模型形式?*
$$h(t|X) = h_0(t) \exp(\beta_1 X_1 + \beta_2 X_2 + \cdots + \beta_p X_p)$$

其中?h_0(t)$为基准风险函数，$\beta_i$为回归系数，$X_i$为协变量?
**风险比（HR）：**
- HR > 1：风险增?- HR = 1：无影响
- HR < 1：风险降?
**比例风险假设棢验：**
- Schoenfeld 残差棢?- 对数负对数生存曲线图
- 残差随时间变化图

### 其他生存分析方法

- **Log-rank 棢?*：比较两组或多组生存曲线
- **加失效时间模型（AFT?*：参数方?- **竞争风险模型**：处理多种事件类?
## 临床试验统计

### 临床试验设计类型

**按设计分类：**
- 平行设计：对照组和处理组同时进行
- 交叉设计：受试先后接受不同处?- 析因设计：同时评价多个干预措?
**按盲法分类：**
- 单盲：仅受试者不知道分组
- 双盲：受试和研究者都不知道分?- 三盲：受试研究和数据分析者都不知道分?
### 样本量计?
**均比较的样本量：**
$$n = \frac{(Z_{\alpha/2} + Z_{\beta})^2 \times 2\sigma^2}{\delta^2}$$

**比例比较的样本量?*
$$n = \frac{(Z_{\alpha/2} + Z_{\beta})^2 \times [p_1(1-p_1) + p_2(1-p_2)]}{(p_1 - p_2)^2}$$

### 适应性设?
- 样本量重?- 剂量探索
- 无缝设计（II/III 期无缝）
- 富集设计

## R 语言实现

### 基础统计分析

```r
# 描述统计
summary(data)
sd(data$variable)
var(data$variable)

# t 棢?t.test(group1, group2, var.equal = TRUE)

# 方差分析
anova_model <- aov(response ~ factor1 * factor2, data = data)
summary(anova_model)

# 卡方棢?chisq.test(table(data$var1, data$var2))
```

### 生存分析

```r
library(survival)
library(survminer)

# 创建生存对象
surv_obj <- Surv(time = data$time, event = data$status)

# Kaplan-Meier 估计
km_fit <- survfit(surv_obj ~ group, data = data)
ggsurvplot(km_fit, data = data, pval = TRUE)

# Cox 回归
cox_model <- coxph(Surv(time, status) ~ age + sex + treatment, data = data)
summary(cox_model)

# 比例风险假设棢?cox.zph(cox_model)
```

### 样本量计?
```r
library(pwr)

# t 棢验样本量
pwr.t.test(n = NULL, d = 0.5, sig.level = 0.05, power = 0.8, 
           type = "two.sample")

# 方差分析样本?pwr.anova.test(k = 3, f = 0.25, sig.level = 0.05, power = 0.8)

# 相关分析样本?pwr.r.test(n = NULL, r = 0.3, sig.level = 0.05, power = 0.8)
```

## 参资?
- Zar JH. *Biostatistical Analysis* (5th ed.)
- Rosner B. *Fundamentals of Biostatistics*
- Kleinbaum DG, Klein M. *Survival Analysis: A Self-Learning Text*
- R Core Team. *R: A Language and Environment for Statistical Computing*

## 相关条目

[[02_NaturalSciences/Mathematics/ProbabilityStatistics/Probability|Probability]], [[07_InterdisciplinarySciences/DataScience/INDEX|DataScience]], [[05_ComputerScience/ArtificialIntelligence/MachineLearning/INDEX|MachineLearning]], StatisticalModeling


