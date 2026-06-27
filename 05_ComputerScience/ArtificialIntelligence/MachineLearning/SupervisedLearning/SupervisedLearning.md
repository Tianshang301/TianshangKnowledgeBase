---
aliases: [SupervisedLearning]
tags: ['ArtificialIntelligence', 'MachineLearning', 'SupervisedLearning', 'SupervisedLearning']
created: 2026-05-16
updated: 2026-05-13
---

# 监督学习

## 一、监督学习概述

监督学习从标注数据 $\mathcal{D} = \{(x_i, y_i)\}_{i=1}^N$ 中学习从输入 $x$ 到输出 $y$ 的映射函数 $f: \mathcal{X} \rightarrow \mathcal{Y}$。

### 问题分类

| 类型 | 输出空间 $\mathcal{Y}$ | 示例 |
|------|----------------------|------|
| 回归 (Regression) | 连续值 | 房价预测 |
| 二分类 (Binary Classification) | $\{0, 1\}$ 或 $\{-1, +1\}$ | 垃圾邮件检测 |
| 多分类 (Multi-class) | $\{1, 2, ..., K\}$ | 手写数字识别 |
| 多标签分类 (Multi-label) | 标签子集 | 图像标注 |

### 经验风险最小化

$$
\hat{f} = \arg\min_{f \in \mathcal{F}} \frac{1}{N} \sum_{i=1}^N \mathcal{L}(y_i, f(x_i)) + \lambda \Omega(f)
$$

## 二、线性回归

### 普通最小二乘法 (OLS)

$$
\hat{y} = \mathbf{w}^T \mathbf{x} + b
$$

$$
\mathcal{L}(\mathbf{w}) = \frac{1}{2} \sum_{i=1}^N (y_i - \mathbf{w}^T \mathbf{x}_i)^2
$$

闭式解：

$$
\hat{\mathbf{w}} = (\mathbf{X}^T \mathbf{X})^{-1} \mathbf{X}^T \mathbf{y}
$$

### 岭回归 (Ridge Regression)

加入 L2正则化：

$$
\mathcal{L}(\mathbf{w}) = \frac{1}{2} \sum_{i=1}^N (y_i - \mathbf{w}^T \mathbf{x}_i)^2 + \frac{\lambda}{2} ||\mathbf{w}||_2^2
$$

$$
\hat{\mathbf{w}} = (\mathbf{X}^T \mathbf{X} + \lambda \mathbf{I})^{-1} \mathbf{X}^T \mathbf{y}
$$

### Lasso 回归

加入 L1正则化，产生稀疏解：

$$
\mathcal{L}(\mathbf{w}) = \frac{1}{2} \sum_{i=1}^N (y_i - \mathbf{w}^T \mathbf{x}_i)^2 + \lambda ||\mathbf{w}||_1
$$

| 方法 | 正则化 | 特性 |
|------|--------|------|
| OLS | 无 | 无偏但高方差 |
| Ridge | L2 | 收缩系数，不稀疏 |
| Lasso | L1 | 系数稀疏，特征选择 |
| Elastic Net | L1 + L2 | 结合两者优点 |

## 三、逻辑回归

逻辑回归用于分类任务，通过 sigmoid 函数将线性输出映射到概率：

$$
P(y=1|x) = \sigma(\mathbf{w}^T \mathbf{x} + b) = \frac{1}{1 + e^{-(\mathbf{w}^T \mathbf{x} + b)}}
$$

### 损失函数（交叉熵）

$$
\mathcal{L}(\mathbf{w}) = -\frac{1}{N} \sum_{i=1}^N [y_i \log(\hat{y}_i) + (1-y_i) \log(1 - \hat{y}_i)]
$$

### 多分类：Softmax 回归

$$
P(y=k|x) = \frac{e^{\mathbf{w}_k^T \mathbf{x}}}{\sum_{j=1}^K e^{\mathbf{w}_j^T \mathbf{x}}}
$$

## 四、决策树

| 算法 | 分裂准则 | 特点 |
|------|---------|------|
| ID3 | 信息增益 | 偏好取值多的属性 |
| C4.5 | 信息增益率 | 处理连续值、缺失值 |
| CART | 基尼系数 / MSE | 二叉分裂，可回归 |

### 信息增益

$$
\text{Gain}(D, A) = H(D) - \sum_{v \in \text{Values}(A)} \frac{|D_v|}{|D|} H(D_v)
$$

### 基尼系数

$$
\text{Gini}(D) = 1 - \sum_{k=1}^K p_k^2
$$

### 剪枝 (Pruning)

- **预剪枝**：在树生长过程中提前停止
- **后剪枝**：树完全生长后自底向上剪枝

## 五、支持向量机 (SVM)

### 最大间隔分类

SVM 寻找最大间隔超平面：

$$
\max_{\mathbf{w}, b} \frac{2}{||\mathbf{w}||} \quad \text{s.t.} \quad y_i(\mathbf{w}^T \mathbf{x}_i + b) \geq 1
$$

等价于：

$$
\min_{\mathbf{w}, b} \frac{1}{2} ||\mathbf{w}||^2 \quad \text{s.t.} \quad y_i(\mathbf{w}^T \mathbf{x}_i + b) \geq 1, \forall i
$$

### 对偶问题

$$
\max_{\alpha} \sum_{i=1}^N \alpha_i - \frac{1}{2} \sum_{i,j} \alpha_i \alpha_j y_i y_j \mathbf{x}_i^T \mathbf{x}_j
$$
$$
\text{s.t.} \quad \sum_{i=1}^N \alpha_i y_i = 0, \quad \alpha_i \geq 0
$$

### 核技巧 (Kernel Trick)

通过核函数将数据映射到高维空间：

| 核函数 | 表达式 | 参数 |
|--------|--------|------|
| 线性核 | $K(x_i, x_j) = x_i^T x_j$ | 无 |
| 多项式核 | $K(x_i, x_j) = (x_i^T x_j + c)^d$ | $c, d$ |
| RBF 核 | $K(x_i, x_j) = \exp(-\gamma ||x_i - x_j||^2)$ | $\gamma$ |
| Sigmoid 核 | $K(x_i, x_j) = \tanh(\alpha x_i^T x_j + c)$ | $\alpha, c$ |

### 软间隔 (Soft Margin)

容忍噪声和不可分情况：

$$
\min_{\mathbf{w}, b, \xi} \frac{1}{2} ||\mathbf{w}||^2 + C \sum_{i=1}^N \xi_i
$$
$$
\text{s.t.} \quad y_i(\mathbf{w}^T \mathbf{x}_i + b) \geq 1 - \xi_i, \quad \xi_i \geq 0
$$

## 六、集成学习

### Bagging

通过自助采样（Bootstrap）生成多个子模型，平均投票：

**随机森林 (Random Forest)**：
- 样本随机：Bootstrap 采样
- 特征随机：每棵树随机选择特征子集
- 结果聚合：分类投票，回归平均

### Boosting

串行训练弱学习器，每个新模型重点关注前序模型错误样本：

**AdaBoost**：

$$
\alpha_t = \frac{1}{2} \ln\left(\frac{1 - \epsilon_t}{\epsilon_t}\right)
$$

**GBDT (Gradient Boosting Decision Tree)**：

$$
F_m(x) = F_{m-1}(x) + \eta \cdot h_m(x)
$$

其中 $h_m$ 拟合负梯度：

$$
h_m = \arg\min_h \sum_{i=1}^N \left[-\frac{\partial L(y_i, F_{m-1}(x_i))}{\partial F_{m-1}(x_i)} - h(x_i)\right]^2
$$

### 主流 Boosting 框架对比

| 框架 | 基学习器 | 特点 | 速度 |
|------|---------|------|------|
| XGBoost | 决策树 | 二阶梯度、正则化、列抽样 | 快 |
| LightGBM | 决策树 | GOSS + EFB，叶子生长 | 最快 |
| CatBoost | 对称决策树 | 原生类别特征处理 | 中等 |
| AdaBoost | 决策桩 | 自适应权重更新 | 一般 |

### Stacking

使用元学习器融合多个基学习器的预测：

$$
\hat{y} = \mathcal{M}_{\text{meta}}(f_1(x), f_2(x), ..., f_K(x))
$$

## 七、其他监督学习算法

### k-近邻 (k-NN)

基于样本空间距离的惰性学习：

$$
\hat{y}(x) = \frac{1}{k} \sum_{x_i \in \mathcal{N}_k(x)} y_i \quad (\text{回归})
$$
$$
\hat{y}(x) = \text{majority}(\{y_i: x_i \in \mathcal{N}_k(x)\}) \quad (\text{分类})
$$

### 朴素贝叶斯

基于特征条件独立假设：

$$
P(y|x_1,...,x_n) \propto P(y) \prod_{i=1}^n P(x_i|y)
$$

## 八、特征工程与数据预处理

| 技术 | 描述 | 适用场景 |
|------|------|---------|
| 标准化 | $x' = (x - \mu)/\sigma$ | 距离/梯度类模型 |
| 归一化 | $x' = (x - x_{\min})/(x_{\max} - x_{\min})$ | 范围敏感模型 |
| 独热编码 | 类别变量转为二进制向量 | 无序类别特征 |
| 特征交叉 | 特征组合生成新特征 | 线性模型表达能力 |
| 多项式特征 | 特征升维 | 非线性拟合 |
| 特征选择 | 过滤/包裹/嵌入法 | 降维、去冗余 |

## 九、不平衡数据处理

| 方法 | 原理 | 特点 |
|------|------|------|
| 随机过采样 | 复制少数类样本 | 简单但易过拟合 |
| 随机欠采样 | 删除多数类样本 | 可能丢失重要信息 |
| SMOTE | 插值生成新样本 | $x_{\text{new}} = x_i + \lambda (x_{zi} - x_i)$ |
| ADASYN | 自适应合成采样 | 关注难分样本 |
| 代价敏感学习 | 为少数类赋予更高权重 | 不改变数据分布 |
| 异常检测视角 | 将少数类视为异常 | 适用于极端不平衡 |

## 十、模型选择与调优

| 步骤 | 方法 | 目标 |
|------|------|------|
| 交叉验证 | k-fold CV | 稳定评估模型性能 |
| 超参数搜索 | Grid/Random/Bayesian | 寻找最优参数 |
| 学习曲线分析 | 训练/验证误差曲线 | 诊断偏差-方差 |
| 特征重要性分析 | 树模型/置换重要性 | 理解特征贡献 |
| 误差分析 | 混淆矩阵/错误样本 | 定位改进方向 |

## 相关条目

- [[UnsupervisedLearning]]
- [[ReinforcementLearning]]
- [[ModelEvaluation]]
- NeuralNetworks

## 参考资源

- Hastie, T. et al. (2009). *The Elements of Statistical Learning*
- Bishop, C. M. (2006). *Pattern Recognition and Machine Learning*
- Breiman, L. (2001). "Random Forests"
- Chen, T. & Guestrin, C. (2016). "XGBoost: A Scalable Tree Boosting System"
- Ke, G. et al. (2017). "LightGBM: A Highly Efficient Gradient Boosting Decision Tree"
- Cortes, C. & Vapnik, V. (1995). "Support-vector networks"
