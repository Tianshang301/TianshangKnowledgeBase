---
aliases: [MachineLearningBasics]
tags: ['DataScience', 'MachineLearningBasics']
created: 2026-05-16
updated: 2026-05-13
---

# 机器学习基础

## 概述

机器学习是人工智能的丢个分支，它使计算机系统能够从数据中学习和改进，无霢显式编程。过算法从数据中发现模式，机器学习可以做出预测和决策?
## ML 工作流程

### 1. 数据预处?
**数据清洗?*
- 处理缺失值：删除、填充（均中位数、众数）、插?- 处理异常值：Z-score 方法、IQR 方法
- 处理重复数据

**数据转换?*
- 标准化（Z-score）：$x' = \frac{x - \mu}{\sigma}$
- 归一化（Min-Max）：$x' = \frac{x - x_{min}}{x_{max} - x_{min}}$
- 对数变换：处理偏态数?
**数据编码?*
- 标签编码：类别转换为整数
- 独热编码：类别转换为二进制向?- 序数编码：有序类别编?
### 2. 特征工程

**特征选择?*
- 过滤法：卡方棢验互信息、方差阈?- 包装法：递归特征消除（RFE?- 嵌入法：L1正则化树模型特征重要?
**特征构建?*
- 多项式特?- 交互特征
- 分箱（Binning?- 时间特征提取

**降维?*
- PCA（主成分分析?- LDA（线性判别分析）
- t-SNE（可视化?
### 3. 模型选择

**按任务类型：**
- 分类：辑回归、SVM、决策树、随机森?- 回归：线性回归岭回归、随机森林回?- 聚类：K-Means、DBSCAN、层次聚?- 降维：PCA、t-SNE、UMAP

**按数据规模：**
- 小数据：箢单模型（线模型 SVM?- 中等数据：集成方法（随机森林、GBDT?- 大数据：深度学习、大规模线模?
### 4. 训练

**训练?验证?测试集划分：**
- 典型比例?0%/20%/20%?0%/15%/15%
- 分层抽样保持类别比例
- 时间序列数据按时间划?
**训练过程?*
- 前向传播：计算预测?- 计算损失：预测与真实值的差距
- 反向传播：计算梯?- 参数更新：梯度下?
### 5. 评估

**分类评估指标?*
- 准确率（Accuracy?- 精确率（Precision?- 召回率（Recall?- F1分数
- AUC-ROC

**回归评估指标?*
- MSE（均方误差）
- RMSE（均方根误差?- MAE（平均绝对误差）
- R²（决定系数）

### 6. 部署

**部署方式?*
- REST API 服务
- 边缘部署
- 批量预测
- 实时流处?
**监控和维护：**
- 模型性能监控
- 数据漂移棢?- 模型再训?- A/B 测试

## 监督学习算法概览

### 线模?
**线回归：**
- 连续目标变量
- 朢小二乘法求解
- 假设：线性关系独立同方差?
**逻辑回归?*
- 分类目标变量
- Sigmoid 函数映射到概?- 交叉熵损失函?
### 树模?
**决策树：**
- 递归分裂
- 可解释强
- 容易过拟?
**随机森林?*
- 多棵树集?- Bagging 减少方差
- 特征随机?
**梯度提升树：**
- 顺序添加弱学习器
- 拟合残差
- Boosting 减少偏差

### 支持向量?
**核心思想?*
- 朢大间隔分类器
- 核技巧处理非线?- 支持向量决定决策边界

**核函数：**
- 线核
- 多项式核
- RBF?
### 朴素贝叶?
**原理?*
- 贝叶斯定?- 特征条件独立假设
- 概率分类

**变体?*
- 高斯朴素贝叶?- 多项式朴素贝叶斯
- 伯努利朴素贝叶斯

## 无监督学习算法概?
### 聚类算法

**K-Means?*
- 基于距离的划?- 霢要指定 K?- 对初始中心敏?
**层次聚类?*
- 凝聚?分裂?- 不需要指定簇?- 计算复杂度高

**DBSCAN?*
- 基于密度
- 可发现任意形?- 能识别噪?
### 降维算法

**PCA?*
- 线降?- 保留朢大方?- 可解释好

**t-SNE?*
- 非线性降?- 保持屢部结?- 适合可视?
**UMAP?*
- 保持全局和局部结?- 比 t-SNE 更快
- 适合大规模数?
### 关联规则

**Apriori 算法?*
- 发现频繁项集
- 生成关联规则
- 支持度置信度

## 模型选择与调?
### 模型选择

**交叉验证?*
- K 折交叉验?- 留一交叉验证
- 分层交叉验证

**模型比较?*
- 统计棢验（t 棢验 McNemar 棢验）
- 信息准则（AIC、BIC?
### 超参数调?
**网格搜索（Grid Search）：**
- 穷举搜索扢有参数组?- 计算成本?- 适合参数空间小的情况

**随机搜索（Random Search）：**
- 随机采样参数组合
- 效率更高
- 适合参数空间大的情况

**贝叶斯优化：**
- 建立代理模型
- 平衡探索和利?- 高效找到朢优参?
### 常见超参?
**树模型：**
- max_depth：最大深?- min_samples_split：最小分裂样本数
- n_estimators：树的数?
**SVM?*
- C：正则化参数
- kernel：核函数类型
- gamma：RBF 核参?
**神经网络?*
- learning_rate：学习率
- batch_size：批大小
- epochs：训练轮?
## 过拟合与欠拟?
### 过拟合（Overfitting?
**表现?*
- 训练误差低，测试误差?- 模型复杂度过?- 记住了噪声和细节

**解决方法?*
- 增加训练数据
- 正则化（L1、L2?- 早停（Early Stopping?- Dropout（神经网络）
- 特征选择
- 降低模型复杂?
### 欠拟合（Underfitting?
**表现?*
- 训练误差和测试误差都?- 模型复杂度不?- 无法捕捉数据模式

**解决方法?*
- 增加特征
- 使用更复杂的模型
- 减少正则?- 增加训练时间

## 偏差-方差权衡

### 偏差（Bias?
- 模型预测值与真实值的系统性偏?- 高偏差导致欠拟合
- 来源于模型假设过于简?
### 方差（Variance?
- 模型对训练数据的敏感程度
- 高方差导致过拟合
- 来源于模型过于复?
### 权衡关系

$$\text{总误差} = \text{偏差}^2 + \text{方差} + \text{不可约误差}$$

**策略?*
- 箢单模型：高偏差，低方?- 复杂模型：低偏差，高方差
- 目标：找到偏差和方差的平衡点

## Python 实现示例

```python
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, roc_auc_score

# 数据划分
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y)

# 特征标准?scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# 模型训练
lr = LogisticRegression()
lr.fit(X_train_scaled, y_train)

# 交叉验证
scores = cross_val_score(lr, X_train_scaled, y_train, cv=5, scoring='roc_auc')

# 模型评估
y_pred = lr.predict(X_test_scaled)
print(f"Accuracy: {accuracy_score(y_test, y_pred):.4f}")
print(f"AUC: {roc_auc_score(y_test, lr.predict_proba(X_test_scaled)[:, 1]):.4f}")
```

## 参资?
- Mitchell TM. *Machine Learning*
- Bishop CM. *Pattern Recognition and Machine Learning*
- 《机器学习周志华
- 《统计学习方法李?- Scikit-learn 官方文档

## 相关条目

[[05_ComputerScience/ArtificialIntelligence/MachineLearning/INDEX|MachineLearning]], [[Statistics]], [[ArtificialIntelligence]], [[BigDataAnalytics]]
