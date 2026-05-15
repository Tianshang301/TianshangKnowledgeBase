---
aliases: [超参数调优与AutoML]
tags: ['ArtificialIntelligence', 'MachineLearning', 'ModelEvaluation', '超参数调优与AutoML']
---

# 超参数调优与AutoML

## 一、超参数调优概述

超参数是在模型训练开始前设置的参数，其取值直接影响模型性能和训练行为。与模型参数(通过训练自动学习)不同，超参数需要人工或自动化方法确定。常见的超参数包括：学习率、批量大小、网络层数、隐藏单元数、正则化系数、Dropout比例等。

超参数优化的目标是找到一组超参数配置 $\lambda^*$，使得模型在验证集上的性能度量 $\mathcal{M}$ 达到最优：

$$
\lambda^* = \arg\max_{\lambda \in \Lambda} \mathcal{M}(\mathcal{A}_\lambda, \mathcal{D}_{\text{train}}, \mathcal{D}_{\text{val}})
$$

其中 $\mathcal{A}_\lambda$ 是由超参数 $\lambda$ 参数化的学习算法。

## 二、手动与网格调参方法

### 2.1 手动调参

手动调参依赖经验和直觉，通过观察训练曲线调整超参数。常用策略包括：先粗调确定合理范围再细调、先确定学习率再调整其他参数。手动调参虽然灵活，但缺乏可重复性且效率低下。

### 2.2 网格搜索

网格搜索在预设的超参数网格上枚举所有组合：

$$
\Lambda_{\text{grid}} = \{\lambda^{(1,1,\ldots)} \mid \lambda_i \in \{\lambda_{i1}, \lambda_{i2}, \ldots, \lambda_{ik_i}\}\}
$$

总组合数为 $\prod_i k_i$，随着超参数数量增加呈指数增长。网格搜索在低维空间有效，但在高维空间不切实际。

### 2.3 随机搜索

随机搜索从超参数分布中随机采样配置：

$$
\lambda \sim P(\Lambda)
$$

Bergstra和Bengio(2012)的理论分析表明，随机搜索在大多数情况下优于网格搜索。对于维度为 $d$ 的超参数空间，当只有少数维度起主导作用时，随机搜索以更高概率探索到有效配置。

| 方法 | 搜索效率 | 并行性 | 适用场景 |
|------|----------|--------|----------|
| 手动调参 | 低 | 低 | 简单模型、经验丰富时 |
| 网格搜索 | 中(低维) | 高 | 低维超参空间 |
| 随机搜索 | 中 | 高 | 通用方法 |
| 贝叶斯优化 | 高 | 中 | 昂贵评估任务 |
| 遗传算法 | 中 | 高 | 离散/组合超参 |

## 三、贝叶斯优化

### 3.1 基本原理

贝叶斯优化通过概率代理模型拟合目标函数，利用采集函数指导搜索。代理模型通常使用高斯过程(GP)：

$$
f(\lambda) \sim \mathcal{GP}(\mu(\lambda), k(\lambda, \lambda'))
$$

给定观测数据 $\mathcal{D} = \{(\lambda_i, y_i)\}_{i=1}^n$，在任意新点 $\lambda$ 的后验分布为：

$$
p(f(\lambda)|\mathcal{D}) = \mathcal{N}(\mu_n(\lambda), \sigma_n^2(\lambda))
$$

### 3.2 采集函数

- **期望改进(EI)**：$EI(\lambda) = \mathbb{E}[\max(0, f(\lambda) - f(\lambda^+))]$
- **置信上界(UCB)**：$UCB(\lambda) = \mu_n(\lambda) + \kappa \sigma_n(\lambda)$
- **概率改进(PI)**：$PI(\lambda) = \Phi\left(\frac{\mu_n(\lambda) - f(\lambda^+)}{\sigma_n(\lambda)}\right)$

### 3.3 树结构Parzen估计(TPE)

TPE是贝叶斯优化的替代方案，通过核密度估计分别建模好配置和差配置的分布：

$$
p(\lambda|y < \gamma^*) \quad \text{vs} \quad p(\lambda|y \geq \gamma^*)
$$

采集函数定义为似然比 $EI(\lambda) \propto \frac{p(\lambda|y < \gamma^*)}{p(\lambda|y \geq \gamma^*)}$。

## 四、自动化机器学习(AutoML)

### 4.1 神经架构搜索(NAS)

NAS自动搜索最优网络架构。搜索空间定义包括：操作类型(卷积、池化、全连接)、连接模式和超参数(核大小、通道数)。

**搜索策略**：
1. **强化学习**：控制器RNN生成架构描述，验证准确率作为奖励信号
2. **进化算法**：对架构种群进行变异和交叉操作
3. **梯度方法(DARTS)**：将离散架构选择松弛为连续的可微形式：
   $$
   \bar{o}^{(i,j)}(x) = \sum_{o \in \mathcal{O}} \frac{\exp(\alpha_o^{(i,j)})}{\sum_{o' \in \mathcal{O}} \exp(\alpha_{o'}^{(i,j)})} \cdot o(x)
   $$

### 4.2 元学习与迁移学习

元学习为AutoML提供了加速手段：

- **学习曲线外推**：在训练早期预测最优配置，提前终止低潜力尝试
- **多任务贝叶斯优化**：利用历史任务数据构建先验知识
- **温启动**：使用迁移学习初始化新任务的搜索

### 4.3 完整AutoML流水线

```python
from auto_ml import AutomatedML

# 定义搜索空间
search_space = {
    'model': ['rf', 'xgboost', 'lightgbm'],
    'max_depth': (3, 15),
    'learning_rate': (0.01, 0.3, 'log-uniform'),
    'n_estimators': (50, 500),
    'subsample': (0.6, 1.0)
}

# 执行自动化搜索
automl = AutomatedML(
    search_space=search_space,
    optimization_method='bayesian',
    max_trials=100,
    early_stopping=True
)
automl.fit(X_train, y_train)
best_model = automl.best_estimator_
```

## 五、超参数优化的挑战

### 5.1 资源效率

每次训练都是一次昂贵的计算。加速策略包括：

- **早停(early stopping)**：当验证性能长时间无改善时终止训练
- **成功率放大(successive halving)**：动态分配资源，淘汰表现差的配置
- **异步并行**：异步贝叶斯优化和并行配置评估

### 5.2 超参数的重要性分析

不同超参数对性能的影响差异很大。fANOVA框架通过分析随机森林模型分解方差：

$$
\text{Var}[y] = \sum_{i} V_i + \sum_{i<j} V_{ij} + \ldots
$$

其中 $V_i = \text{Var}_{\lambda_i}[\mathbb{E}[y|\lambda_i]]$ 表示单变量重要性。

研究表明，学习率和批量大小通常是最敏感的超参数，而优化器选择对最终性能的影响相对较小。

## 六、自动化调参工具

| 工具 | 优化方法 | 特性 |
|------|----------|------|
| Optuna | TPE, CMA-ES | 动态构建搜索空间，剪枝 |
| Hyperopt | TPE, 随机搜索 | 分布式支持 |
| Ray Tune | 多种 | 扩展性强，支持深度学习 |
| SMAC | 随机森林+BO | 处理条件超参数 |
| AutoGluon | 集成+多阶段 | 端到端AutoML |

## 相关条目

- [[ModelEvaluation]]
- [[SupervisedLearning]]
- [[NeuralNetworksAndDeepLearning]]
- [[05_ComputerScience/ArtificialIntelligence/MachineLearning/INDEX|MachineLearning]]

## 参考资源

1. Bergstra, J., Bengio, Y. "Random Search for Hyper-Parameter Optimization." JMLR, 2012.
2. Snoek, J., et al. "Practical Bayesian Optimization of Machine Learning Algorithms." NeurIPS, 2012.
3. Bergstra, J., et al. "Algorithms for Hyper-Parameter Optimization." NeurIPS, 2011.
4. Zoph, B., Le, Q. "Neural Architecture Search with Reinforcement Learning." ICLR, 2017.
5. Liu, H., et al. "DARTS: Differentiable Architecture Search." ICLR, 2019.
6. Falkner, S., et al. "BOHB: Robust and Efficient Hyperparameter Optimization at Scale." ICML, 2018.
7. Hutter, F., et al. "Automated Machine Learning: Methods, Systems, Challenges." Springer, 2019.
