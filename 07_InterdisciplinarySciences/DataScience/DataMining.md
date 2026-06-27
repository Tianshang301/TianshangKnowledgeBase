---
aliases: [DataMining]
tags: ['DataScience', 'DataMining']
created: 2026-05-16
updated: 2026-05-16
---

# 数据挖掘

## 概述

数据挖掘是从大规模数据集中自动发现有用模式和知识的过程它融合了统计学、机器学习数据库抢术和领域知识，广泛应用于商业智能、生物信息学、金融分析等领域?
## 数据挖掘流程（CRISP-DM?
CRISP-DM（Cross-Industry Standard Process for Data Mining）是业界标准的数据挖掘流程?
### 六个阶段

**1. 业务理解（Business Understanding?*
- 确定业务目标
- 评估现状
- 确定数据挖掘目标
- 制定初步计划

**2. 数据理解（Data Understanding?*
- 收集初始数据
- 描述数据
- 探索数据
- 棢验数据质?
**3. 数据准备（Data Preparation?*
- 选择数据
- 清洗数据
- 构数据（特征工程?- 整合数据
- 格式化数?
**4. 建模（Modeling?*
- 选择建模抢?- 设计测试方案
- 构建模型
- 评估模型

**5. 评估（Evaluation?*
- 评估结果
- 审视过程
- 确定下一?
**6. 部署（Deployment?*
- 计划部署
- 计划监控和维?- 生成朢终报?- 项目回顾

## 关联规则挖掘

### 基本概念

**关联规则形式?* X ?Y

**支持度（Support）：**
$$support(X \rightarrow Y) = \frac{|X \cup Y|}{|D|}$$

**置信度（Confidence）：**
$$confidence(X \rightarrow Y) = \frac{support(X \cup Y)}{support(X)}$$

**提升度（Lift）：**
$$lift(X \rightarrow Y) = \frac{confidence(X \rightarrow Y)}{support(Y)}$$

### Apriori 算法

**核心原理?*
- 先验性质：频繁项集的扢有子集也是频繁的
- 逐层搜索：从1-项集弢始，逐步发现频繁项集

**算法步骤?*
1. 扫描数据库，计算每个1-项集的支持度
2. 根据朢小支持度筛频?-项集
3. 使用频繁 k-项集生成候?k+1)-项集
4. 剪枝：删除包含非频繁子集的项?5. 扫描数据库，计算候项集支持度
6. 重复3-5直到没有新的频繁项集

**优化策略?*
- 基于哈希的项集计?- 事务压缩
- 划分方法
- 采样方法

### FP-Growth 算法

**特点?*
- 只需扫描数据库两?- 使用 FP 树结构存储频繁项信息
- 不产生项?- 效率高于 Apriori

## 分类算法

### 决策?
**ID3算法?*
- 使用信息增益选择特征
- 只能处理离散特征
- 不进行剪?
**C4.5算法?*
- 使用增益率择特征
- 可处理连续特?- 支持后剪?
**CART 算法?*
- 分类树：基尼系数
- 回归树：朢小化均方误差
- 生成二叉?
### 朴素贝叶?
**贝叶斯定理：**
$$P(C|X) = \frac{P(X|C)P(C)}{P(X)}$$

**朴素假设?* 特征条件独立
$$P(X|C) = \prod_{i=1}^{n}P(x_i|C)$$

**分类决策?*
$$\hat{C} = \arg\max_{C}P(C)\prod_{i=1}^{n}P(x_i|C)$$

**应用?*
- 垃圾邮件过滤
- 文本分类
- 情感分析

### 支持向量机（SVM?
**线可分 SVM?*
- 朢大间隔分类器
- 支持向量：距离超平面朢近的?- 优化目标?\min\frac{1}{2}\|w\|^2$

**软间隔 SVM?*
- 允许误分?- 引入松弛变量ξ
- 优化目标?\min\frac{1}{2}\|w\|^2 + C\sum\xi_i$

**核函数：**
- 线核?K(x_i,x_j) = x_i^Tx_j$
- 多项式核?K(x_i,x_j) = (x_i^Tx_j + c)^d$
- RBF 核：$K(x_i,x_j) = \exp(-\gamma\|x_i - x_j\|^2)$

## 聚类算法

### K-Means 聚类

**算法步骤?*
1. 随机初始化 K 个中心点
2. 将每个样本分配到朢近的中心
3. 重新计算每个簇的中心
4. 重复2-3直到收敛

**目标函数?*
$$J = \sum_{k=1}^{K}\sum_{x_i \in C_k}\|x_i - \mu_k\|^2$$

**选择 K 值：**
- 肘部法则（Elbow Method?- 轮廓系数（Silhouette Coefficient?- Gap Statistic

### DBSCAN

**核心概念?*
- 核心点：邻域内点数≥MinPts
- 边界点：不是核心点但在核心点邻域?- 噪声点：既不是核心点也不是边界点

**参数?*
- ε：邻域半?- MinPts：最小点?
**优势?*
- 可发现任意形状的?- 不需要预先指定簇?- 能识别噪声点

### 层次聚类

**凝聚层次聚类?*
1. 每个样本作为丢个簇
2. 合并朢相似的两个簇
3. 重复2直到只有丢个簇

**距离度量?*
- 欧氏距离
- 曼哈顿距?- 余弦距离

**连接准则?*
- 单连接：两个簇最近点的距?- 完全连接：两个簇朢远点的距?- 平均连接：两个簇扢有点对距离的平均

## 异常棢?
### 统计方法

- **Z-score 方法**?|z| > 3$为异?- **箱线图方?*：超?.5×IQR 为异?- **马氏距离**：虑变量相关性的距离度量

### 机器学习方法

**孤立森林（Isolation Forest）：**
- 基于异常点容易被隔离的原?- 随机选择特征和分割点
- 异常点的路径长度较短

**One-Class SVM?*
- 只用正常数据训练
- 学习正常数据的边?- 边界外的点为异常

**LOF（Local Outlier Factor）：**
- 基于密度的异常检?- 比较屢部密度与邻域密度
- 密度显著低于邻域的点为异?
## 数据挖掘工具

### Weka

**特点?*
- 弢源 Java 平台
- 图形用户界面友好
- 包含丰富的算?- 支持数据预处?
**主要功能?*
- Explorer：交互式数据探索
- Experimenter：实验设?- KnowledgeFlow：可视化工作?- Simple CLI：命令行接口

### RapidMiner

**特点?*
- 可视化建模环?- 拖拽式操?- 丰富的算子库
- 支持自动机器学习

**主要功能?*
- 数据加载和预处理
- 特征选择和工?- 模型训练和评?- 模型部署和监?
### Python 生系?
**主要库：**
- scikit-learn：用机器学习
- pandas：数据处?- NumPy：数值计?- Matplotlib/Seaborn：可视化

```python
from sklearn.cluster import KMeans
from sklearn.ensemble import IsolationForest
from mlxtend.frequent_patterns import apriori

# K-Means 聚类
kmeans = KMeans(n_clusters=3)
clusters = kmeans.fit_predict(data)

# 关联规则
frequent_itemsets = apriori(df, min_support=0.1, use_colnames=True)

# 异常棢?iso_forest = IsolationForest(contamination=0.1)
anomalies = iso_forest.fit_predict(data)
```

### R 语言工具

**主要包：**
- caret：机器学习统丢接口
- rpart：决策树
- e1071：SVM
- cluster：聚类分?
## 参资?
- Han J, et al. *Data Mining: Concepts and Techniques*
- Tan PN, et al. *Introduction to Data Mining*
- 《数据挖掘：概念与技术韩家炜
- 《Python 数据科学手册》Jake VanderPlas

## 相关条目

[[05_ComputerScience/ArtificialIntelligence/MachineLearning/INDEX|MachineLearning]], [[07_InterdisciplinarySciences/AppliedStatistics/Statistics|Statistics]], [[07_InterdisciplinarySciences/CognitiveScience/ArtificialIntelligence|ArtificialIntelligence]], [[BigDataAnalytics]]


