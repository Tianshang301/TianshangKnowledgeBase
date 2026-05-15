---
aliases: [StatisticalLearning]
tags: ['AppliedStatistics', 'StatisticalLearning']
---

# 统计学习

## 概述

统计学习是基于统计理论构建模型来理解数据的学科。它提供了一套系统的框架，用于从数据中提取模式、做出预测和推断。统计学习是机器学习的理论基础，两者在方法上有大量重叠。

## 监督学习

### 线性回归

**简单线性回归：**
$$y = \beta_0 + \beta_1 x + \varepsilon$$

**多元线性回归：**
$$y = \beta_0 + \beta_1 x_1 + \beta_2 x_2 + \cdots + \beta_p x_p + \varepsilon$$

**参数估计（最小二乘法）：**
$$\hat{\beta} = (X^TX)^{-1}X^Ty$$

**模型诊断：**
- 残差分析：检查线性、正态性、同方差性
- 多重共线性：VIF < 10
- 影响点：Cook距离

### 逻辑回归

**模型形式：**
$$\log\left(\frac{p}{1-p}\right) = \beta_0 + \beta_1 x_1 + \cdots + \beta_p x_p$$

**概率预测：**
$$p = \frac{1}{1 + e^{-(\beta_0 + \beta_1 x_1 + \cdots + \beta_p x_p)}}$$

**参数估计（最大似然法）：**
$$L(\beta) = \prod_{i=1}^{n}p_i^{y_i}(1-p_i)^{1-y_i}$$

**应用：**
- 疾病风险预测
- 客户流失预测
- 信用评分

### 决策树

**分裂准则：**

**分类树：**
- 基尼不纯度：$Gini(D) = 1 - \sum_{k=1}^{K}p_k^2$
- 信息增益：$Gain(D,A) = H(D) - H(D|A)$

**回归树：**
- 最小化残差平方和

**树的剪枝：**
- 预剪枝：限制最大深度、最小样本数
- 后剪枝：代价复杂度剪枝

**优缺点：**
- 优点：可解释性强、处理非线性关系
- 缺点：容易过拟合、对数据敏感

### 随机森林

**原理：**
- 基于Bootstrap抽样构建多棵树
- 每次分裂随机选择特征子集
- 集成多棵树的预测结果

**参数：**
- 树的数量（n_estimators）
- 最大特征数（max_features）
- 最小样本叶节点数（min_samples_leaf）

**优势：**
- 降低过拟合风险
- 提高预测准确性
- 可评估特征重要性

### 梯度提升树（GBDT）

**原理：**
- 逐步添加弱学习器
- 每步拟合残差
- 加权求和得到最终模型

**常用算法：**
- AdaBoost
- Gradient Boosting
- XGBoost
- LightGBM
- CatBoost

## 无监督学习

### 主成分分析（PCA）

**目标：** 将高维数据投影到低维空间，保留最大方差。

**数学原理：**
- 计算协方差矩阵
- 特征值分解
- 选择前k个主成分

**方差解释率：**
$$\text{解释率} = \frac{\lambda_i}{\sum_{j=1}^{p}\lambda_j}$$

**应用：**
- 数据降维
- 特征提取
- 可视化
- 去噪

### 聚类分析

**K-Means聚类：**
1. 随机初始化k个中心点
2. 将每个样本分配到最近的中心点
3. 重新计算每个簇的中心点
4. 重复2-3直到收敛

**层次聚类：**
- 凝聚型（自底向上）
- 分裂型（自顶向下）
- 距离度量：欧氏距离、曼哈顿距离、余弦距离
- 连接准则：单连接、完全连接、平均连接

**DBSCAN：**
- 基于密度的聚类
- 参数：邻域半径ε、最小点数MinPts
- 可发现任意形状的簇
- 可识别噪声点

## 模型评估

### 交叉验证

**K折交叉验证：**
1. 将数据分成K份
2. 每次用K-1份训练，1份验证
3. 重复K次，取平均性能

**留一交叉验证（LOOCV）：**
- K等于样本量
- 偏差小，方差大
- 计算成本高

**分层交叉验证：**
- 保持各折中类别比例一致
- 适用于不平衡数据

### 分类模型评估

**混淆矩阵：**
|  | 预测正 | 预测负 |
|--|--------|--------|
| 实际正 | TP | FN |
| 实际负 | FP | TN |

**评估指标：**
- 准确率（Accuracy）：$(TP+TN)/(TP+TN+FP+FN)$
- 精确率（Precision）：$TP/(TP+FP)$
- 召回率（Recall）：$TP/(TP+FN)$
- F1分数：$2 \times \frac{Precision \times Recall}{Precision + Recall}$

### ROC曲线与AUC

**ROC曲线：**
- 横轴：假正率（FPR）= FP/(FP+TN)
- 纵轴：真正率（TPR）= TP/(TP+FN)
- 曲线越靠近左上角越好

**AUC（曲线下面积）：**
- AUC = 1：完美分类器
- AUC = 0.5：随机猜测
- AUC < 0.5：比随机猜测差

### 回归模型评估

- **均方误差（MSE）**：$\frac{1}{n}\sum_{i=1}^{n}(y_i - \hat{y}_i)^2$
- **均方根误差（RMSE）**：$\sqrt{MSE}$
- **平均绝对误差（MAE）**：$\frac{1}{n}\sum_{i=1}^{n}|y_i - \hat{y}_i|$
- **决定系数（R²）**：$1 - \frac{SS_{res}}{SS_{tot}}$

## 正则化

### Lasso回归（L1正则化）

**目标函数：**
$$\min_{\beta}\left\{\sum_{i=1}^{n}(y_i - \beta_0 - \sum_{j=1}^{p}\beta_j x_{ij})^2 + \lambda\sum_{j=1}^{p}|\beta_j|\right\}$$

**特点：**
- 可以进行特征选择（稀疏解）
- 将部分系数压缩为零
- 适用于高维数据

### Ridge回归（L2正则化）

**目标函数：**
$$\min_{\beta}\left\{\sum_{i=1}^{n}(y_i - \beta_0 - \sum_{j=1}^{p}\beta_j x_{ij})^2 + \lambda\sum_{j=1}^{p}\beta_j^2\right\}$$

**特点：**
- 缩小系数但不会压缩为零
- 处理多重共线性
- 保留所有特征

### Elastic Net

**目标函数：**
$$\min_{\beta}\left\{\|y - X\beta\|_2^2 + \lambda_1\|\beta\|_1 + \lambda_2\|\beta\|_2^2\right\}$$

**优势：**
- 结合L1和L2正则化的优点
- 可处理高维数据
- 处理高度相关的特征

### 正则化参数选择

**交叉验证选择λ：**
- 绘制λ与交叉验证误差的关系图
- 选择最小误差对应的λ（λ_min）
- 选择一倍标准误内的最大λ（λ_1se）

## 统计学习与机器学习的关系

### 核心区别

| 方面 | 统计学习 | 机器学习 |
|------|----------|----------|
| 目标 | 理解数据生成过程 | 预测准确性 |
| 模型 | 偏向参数模型 | 偏向非参数模型 |
| 推断 | 强调统计推断 | 强调预测性能 |
| 理论 | 严格的统计理论 | 经验驱动 |

### 共同基础

- 损失函数/目标函数优化
- 偏差-方差权衡
- 过拟合与欠拟合
- 模型选择与评估
- 交叉验证

### 发展趋势

- 深度学习与统计学习的融合
- 可解释机器学习
- 因果推断与机器学习结合
- 自动机器学习（AutoML）

## R语言实现

```r
# 线性回归
lm_model <- lm(y ~ x1 + x2, data = train_data)

# Lasso回归
library(glmnet)
cv_lasso <- cv.glmnet(x, y, alpha = 1)
predict(cv_lasso, s = "lambda.min", newx = x_test)

# 随机森林
library(randomForest)
rf_model <- randomForest(y ~ ., data = train_data, ntree = 500)

# 交叉验证
library(caret)
train_control <- trainControl(method = "cv", number = 10)
model <- train(y ~ ., data = train_data, method = "rf", 
               trControl = train_control)
```

## Python实现

```python
from sklearn.linear_model import LinearRegression, Lasso, Ridge
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score
from sklearn.metrics import roc_auc_score

# 线性回归
lr = LinearRegression()
lr.fit(X_train, y_train)

# Lasso回归
lasso = Lasso(alpha=0.1)
lasso.fit(X_train, y_train)

# 随机森林
rf = RandomForestClassifier(n_estimators=100)
rf.fit(X_train, y_train)

# 交叉验证
scores = cross_val_score(rf, X, y, cv=10, scoring='roc_auc')
```

## 相关条目

- [[02_NaturalSciences/Mathematics/ProbabilityStatistics/INDEX|ProbabilityStatistics]]
- [[07_InterdisciplinarySciences/DataScience/INDEX|DataScience]]
- [[Econometrics]]
- [[05_ComputerScience/ArtificialIntelligence/MachineLearning/INDEX|MachineLearning]]

## 参考资源

- Hastie T, et al. *The Elements of Statistical Learning*
- James G, et al. *An Introduction to Statistical Learning*
- 《统计学习方法》李航
- 《机器学习》周志华
