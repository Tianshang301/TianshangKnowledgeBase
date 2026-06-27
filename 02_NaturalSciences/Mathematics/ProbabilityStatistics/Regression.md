---
aliases: [Regression]
tags: ['Mathematics', 'ProbabilityStatistics', 'Regression']
created: 2026-05-16
updated: 2026-05-16
---

# 回归分析

## 一、简单线性回归

### 模型

$$y_i = \beta_0 + \beta_1 x_i + \varepsilon_i, \quad \varepsilon_i \sim N(0, \sigma^2)$$

### 最小二乘估计 (OLS)

最小化 $\sum_{i=1}^n (y_i - \beta_0 - \beta_1 x_i)^2$

$$\hat{\beta}_1 = \frac{\sum_{i=1}^n (x_i - \bar{x})(y_i - \bar{y})}{\sum_{i=1}^n (x_i - \bar{x})^2} = \frac{S_{xy}}{S_{xx}}$$

$$\hat{\beta}_0 = \bar{y} - \hat{\beta}_1 \bar{x}$$

### 拟合优度 ($R^2$)

$$R^2 = \frac{\text{SSR}}{\text{SST}} = 1 - \frac{\text{SSE}}{\text{SST}}$$

其中 SST $= \sum(y_i - \bar{y})^2$，SSR $= \sum(\hat{y}_i - \bar{y})^2$，SSE $= \sum(y_i - \hat{y}_i)^2$

## 二、多元线性回归

### 矩阵形式

$$\mathbf{y} = X\boldsymbol{\beta} + \boldsymbol{\varepsilon}$$

OLS 解：

$$\hat{\boldsymbol{\beta}} = (X^T X)^{-1} X^T \mathbf{y}$$

### ANOVA 表

| 来源 | 平方和 | 自由度 | 均方 | $F$ |
|:---|:---:|:---:|:---:|:---:|
| 回归 | SSR | $p$ | MSR $= \text{SSR}/p$ | $F = \text{MSR}/\text{MSE}$ |
| 残差 | SSE | $n-p-1$ | MSE $= \text{SSE}/(n-p-1)$ | |
| 总计 | SST | $n-1$ | | |

### 系数置信区间

$$\hat{\beta}_j \pm t_{\alpha/2, n-p-1} \cdot SE(\hat{\beta}_j)$$

**预测区间**：
$$\hat{y}_0 \pm t_{\alpha/2, n-p-1} \cdot \hat{\sigma}\sqrt{1 + x_0^T (X^T X)^{-1} x_0}$$

### 调整 $R^2$

$$R^2_{\text{adj}} = 1 - \frac{\text{SSE}/(n-p-1)}{\text{SST}/(n-1)}$$

其中 $p$ 为自变量个数。

### 整体 $F$-检验

$$F = \frac{\text{SSR}/p}{\text{SSE}/(n-p-1)} \sim F(p, n-p-1)$$

检验 $H_0: \beta_1 = \beta_2 = \cdots = \beta_p = 0$

### 多重共线性与 VIF

$$\text{VIF}_j = \frac{1}{1 - R_j^2}$$

其中 $R_j^2$ 为 $X_j$ 对其他自变量回归的 $R^2$。VIF > 10 表示严重共线性。

## 三、模型诊断

### 残差分析

- 残差 vs 拟合值图：检查线性性和同方差性
- Q-Q 图：检查正态性
- 残差 vs 时序：检查独立性

### 影响点诊断

- **杠杆值** $h_{ii}$：大杠杆值为潜在异常点
- **Cook's distance**：衡量某点对系数估计的影响

$$D_i = \frac{(\hat{y} - \hat{y}_{(i)})^T(\hat{y} - \hat{y}_{(i)})}{p \cdot \text{MSE}}$$

## 四、分类预测变量与交互项

### 虚拟变量编码

将 $k$ 类分类变量转换为 $k-1$ 个 0/1 虚拟变量。

### 交互项

$$y = \beta_0 + \beta_1 x_1 + \beta_2 x_2 + \beta_3 x_1 x_2 + \varepsilon$$

交互项 $\beta_3$ 衡量 $x_1$ 对 $y$ 的影响如何随 $x_2$ 变化。

## 五、多项式回归

$$y = \beta_0 + \beta_1 x + \beta_2 x^2 + \cdots + \beta_k x^k + \varepsilon$$

注意：多项式项间可能存在共线性，建议中心化。

## 六、逻辑回归 (Logistic Regression)

### 模型

$$\log\left(\frac{p}{1-p}\right) = \beta_0 + \beta_1 x_1 + \cdots + \beta_p x_p$$

$$p = \frac{e^{\beta_0 + \beta_1 x_1 + \cdots}}{1 + e^{\beta_0 + \beta_1 x_1 + \cdots}}$$

### 系数解释

$\exp(\beta_j)$ 为优势比 (Odds Ratio)：$x_j$ 增加一个单位，优势比乘以 $\exp(\beta_j)$。

### 模型评估

- **混淆矩阵**：TP, FP, FN, TN
- **准确率**：$\frac{TP + TN}{TP + FP + FN + TN}$
- **精确率**：$\frac{TP}{TP + FP}$
- **召回率**：$\frac{TP}{TP + FN}$
- **F1-score**：$2 \cdot \frac{\text{Precision} \cdot \text{Recall}}{\text{Precision} + \text{Recall}}$
- **ROC 曲线与 AUC**：不同阈值下的 TPR vs FPR

## 七、正则化 (Regularization)

### Ridge 回归 ($L_2$)

$$\hat{\beta}_{\text{ridge}} = \arg\min \|y - X\beta\|^2 + \lambda \|\beta\|_2^2$$

解：$\hat{\beta} = (X^T X + \lambda I)^{-1} X^T y$

### Lasso 回归 ($L_1$)

$$\hat{\beta}_{\text{lasso}} = \arg\min \|y - X\beta\|^2 + \lambda \|\beta\|_1$$

可进行特征选择（将系数压缩至 0）。

### ElasticNet

$$\hat{\beta} = \arg\min \|y - X\beta\|^2 + \lambda_1 \|\beta\|_1 + \lambda_2 \|\beta\|_2^2$$

| 方法 | 正则化项 | 特点 | 适用场景 |
|:---|:---|:---|:---|
| Ridge | $\lambda\|\beta\|_2^2$ | 系数收缩但不为零 | 多重共线性 |
| Lasso | $\lambda\|\beta\|_1$ | 系数可压缩至零 | 特征选择 |
| ElasticNet | $\lambda_1\|\beta\|_1 + \lambda_2\|\beta\|_2^2$ | 结合两者优点 | 高维数据 |

## 八、模型选择

- **AIC**：$\text{AIC} = -2\ln(L) + 2p$
- **BIC**：$\text{BIC} = -2\ln(L) + p\ln(n)$
- **交叉验证**：$k$-fold CV

```python
import numpy as np
import statsmodels.api as sm
from sklearn.linear_model import LinearRegression, LogisticRegression, Ridge, Lasso

# OLS with statsmodels
X = np.array([[1, 1], [1, 2], [1, 3]])
y = np.array([1, 2, 3])
model = sm.OLS(y, X).fit()
print(model.summary())

# LinearRegression with sklearn
lr = LinearRegression().fit(X[:, 1:], y)

# Logistic Regression
from sklearn.linear_model import LogisticRegression
clf = LogisticRegression().fit(X[:, 1:], y > 2)

# Ridge / Lasso
ridge = Ridge(alpha=1.0).fit(X[:, 1:], y)
lasso = Lasso(alpha=0.1).fit(X[:, 1:], y)

# Cross-validation
from sklearn.model_selection import cross_val_score
scores = cross_val_score(lr, X[:, 1:], y, cv=3)
```

## 相关条目

- [[07_InterdisciplinarySciences/DataScience/INDEX|DataScience]]
- [[05_ComputerScience/ArtificialIntelligence/MachineLearning/INDEX|MachineLearning]]
- [[03_HumanitiesAndSocialSciences/Economics/Econometrics/Econometrics|Econometrics]]


