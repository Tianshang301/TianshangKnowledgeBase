---
aliases: [ModelEvaluation]
tags: ['ArtificialIntelligence', 'MachineLearning', 'ModelEvaluation', 'ModelEvaluation']
created: 2026-05-16
updated: 2026-05-13
---

# 模型评估

## 一、评估策略

### 留出法 (Holdout Method)

将数据集划分为训练集和测试集（通常70%/30%或80%/20%）：

$$
\mathcal{D} = \mathcal{D}_{\text{train}} \cup \mathcal{D}_{\text{test}},\quad \mathcal{D}_{\text{train}} \cap \mathcal{D}_{\text{test}} = \emptyset
$$

### 交叉验证

**k 折交叉验证 (k-fold Cross-Validation)**：
1. 将数据集随机分为 $k$ 个互斥子集
2. 每次取 $k-1$ 份训练，1份测试
3. 重复 $k$ 次，取平均性能

$$
\text{CV}_k = \frac{1}{k} \sum_{i=1}^k \text{Score}(\mathcal{M}_i, \mathcal{D}_{\text{test}}^{(i)})
$$

| 方法 | 特点 | 适用场景 |
|------|------|---------|
| 标准 k 折 | 简单通用 | 一般分类/回归 |
| 分层 k 折 | 保持类别比例 | 不平衡分类 |
| LOOCV | 每次留一个样本，k=n | 小样本（<100） |
| 重复 k 折 | 多次 k 折取平均 | 需要稳定估计 |

### 自助法 (Bootstrap)

有放回抽样，适用于小样本估计：

$$
P(\text{样本从未被抽中}) = \left(1 - \frac{1}{n}\right)^n \approx e^{-1} \approx 0.368
$$

Out-of-bag (OOB) 样本用于测试。

## 二、分类性能指标

### 混淆矩阵

| | 预测为正 | 预测为负 |
|--|---------|---------|
| **实际为正** | TP (真正例) | FN (假负例) |
| **实际为负** | FP (假正例) | TN (真负例) |

### 核心指标

$$
\text{准确率 (Accuracy)} = \frac{TP + TN}{TP + TN + FP + FN}
$$

$$
\text{精确率 (Precision)} = \frac{TP}{TP + FP}
$$

$$
\text{召回率 (Recall / TPR)} = \frac{TP}{TP + FN}
$$

$$
F_1 = 2 \cdot \frac{\text{Precision} \cdot \text{Recall}}{\text{Precision} + \text{Recall}}
$$

$$
\text{特异度 (Specificity)} = \frac{TN}{TN + FP}
$$

$$
F_\beta = (1 + \beta^2) \cdot \frac{\text{Precision} \cdot \text{Recall}}{\beta^2 \cdot \text{Precision} + \text{Recall}}
$$

### ROC 曲线与 AUC

ROC 曲线绘制 TPR（召回率）与 FPR（假正率）在不同阈值下的关系：

$$
\text{FPR} = \frac{FP}{FP + TN}
$$

AUC（Area Under ROC Curve）衡量模型的整体排序能力：
- AUC = 1：完美分类器
- AUC = 0.5：随机分类器

### PR 曲线

在类别不平衡时优于 ROC 曲线，关注精确率-召回率的权衡。

## 三、回归性能指标

| 指标 | 定义 | 特点 |
|------|------|------|
| MSE | $\frac{1}{n}\sum_{i=1}^n (y_i - \hat{y}_i)^2$ | 对大误差敏感 |
| RMSE | $\sqrt{\frac{1}{n}\sum_{i=1}^n (y_i - \hat{y}_i)^2}$ | 与原变量同量纲 |
| MAE | $\frac{1}{n}\sum_{i=1}^n |y_i - \hat{y}_i|$ | 鲁棒性强 |
| R² | $1 - \frac{\sum (y_i - \hat{y}_i)^2}{\sum (y_i - \bar{y})^2}$ | 解释方差比例 |
| 调整 R² | $1 - \frac{(1-R^2)(n-1)}{n-p-1}$ | 惩罚特征数量 |

$$
\text{MAPE} = \frac{100\%}{n} \sum_{i=1}^n \left|\frac{y_i - \hat{y}_i}{y_i}\right|
$$

## 四、概率预测指标

### Log Loss (交叉熵损失)

$$
\text{LogLoss} = -\frac{1}{n} \sum_{i=1}^n \sum_{j=1}^C y_{ij} \log(p_{ij})
$$

### Brier Score

$$
\text{BS} = \frac{1}{n} \sum_{i=1}^n \sum_{j=1}^C (p_{ij} - y_{ij})^2
$$

## 五、统计显著性检验

### McNemar 检验

用于比较两个分类器的配对样本检验：

$$
\chi^2 = \frac{(|n_{01} - n_{10}| - 1)^2}{n_{01} + n_{10}}
$$

其中 $n_{01}$ 为分类器1错误而分类器2正确的样本数，反之亦然。

### 配对 t 检验

对多次重复实验的评估结果进行显著性检验：

$$
t = \frac{\bar{d}}{s_d / \sqrt{n}}
$$

其中 $\bar{d}$ 为性能差异均值，$s_d$ 为标准差。

### Wilcoxon 符号秩检验

非参数配对检验，不要求正态分布假设。

## 六、偏差-方差权衡

模型总误差可分解为三个分量：

$$
\mathbb{E}[(y - \hat{f}(x))^2] = \text{Bias}(\hat{f}(x))^2 + \text{Var}(\hat{f}(x)) + \sigma^2
$$

| 模型复杂度 | 偏差 | 方差 | 总体误差 |
|-----------|------|------|---------|
| 低（欠拟合） | 高 | 低 | 高 |
| 最优 | 中 | 中 | 低 |
| 高（过拟合） | 低 | 高 | 高 |

### 过拟合检测

- 训练误差远低于验证误差
- 学习曲线：训练集性能持续提升，验证集性能开始下降
- 权重值过大
- 对噪声敏感

## 七、超参数调优

### 搜索方法对比

| 方法 | 原理 | 效率 | 适用场景 |
|------|------|------|---------|
| 网格搜索 (Grid Search) | 穷举所有组合 | 低 | 参数少、维度低 |
| 随机搜索 (Random Search) | 随机采样 | 中 | 高维参数空间 |
| 贝叶斯优化 | 基于高斯过程代理模型 | 高 | 评估代价高 |
| 遗传算法 | 进化搜索 | 中 | 非连续参数空间 |

### 贝叶斯优化

$$
P(f|\mathcal{D}) \propto P(f) \cdot P(\mathcal{D}|f)
$$

采集函数（Acquisition Function）：
- **EI (Expected Improvement)**：期望提升
- **UCB (Upper Confidence Bound)**：置信上界
- **PI (Probability of Improvement)**：提升概率

### Optuna

现代超参数优化框架特性：
- Define-by-Run API
- 剪枝机制（Pruning）
- 多目标优化
- 可视化分析

## 八、学习曲线

学习曲线绘制训练集大小与模型性能的关系：

- **高偏差**：训练和验证曲线在较高误差处收敛
- **高方差**：训练和验证曲线之间存在较大差距

## 九、模型对比框架

| 维度 | 评估方式 | 注意事项 |
|------|---------|---------|
| 预测性能 | CV + 统计检验 | 多次重复实验 |
| 计算成本 | 训练/推理时间 | 硬件环境一致 |
| 内存消耗 | 模型大小 | 部署约束 |
| 稳定性 | 多次重复的方差 | 随机种子影响 |
| 可解释性 | 特征重要性 | 业务需求 |

## 十、评估陷阱

- **数据泄露 (Data Leakage)**：测试信息意外进入训练过程
- **不恰当的划分**：时间序列数据随机划分
- **评估指标选择不当**：不平衡数据使用准确率
- **多次使用测试集**：导致过拟合测试集
- **小样本的统计不确定性**：需要置信区间

## 相关条目

- [[SupervisedLearning]]
- FeatureEngineering
- Overfitting
- CrossValidation

## 参考资源

- Bishop, C. M. (2006). *Pattern Recognition and Machine Learning*
- Hastie, T. et al. (2009). *The Elements of Statistical Learning*
- Kohavi, R. (1995). "A Study of Cross-Validation and Bootstrap for Accuracy Estimation and Model Selection"
- Bergstra, J. & Bengio, Y. (2012). "Random Search for Hyper-Parameter Optimization"
- Snoek, J. et al. (2012). "Practical Bayesian Optimization of Machine Learning Algorithms"
- Akiba, T. et al. (2019). "Optuna: A Next-generation Hyperparameter Optimization Framework"
