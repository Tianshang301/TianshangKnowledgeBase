# 无监督学习

## 一、无监督学习概述

无监督学习从不含标签的数据 $\mathcal{D} = \{\mathbf{x}_i\}_{i=1}^N$ 中发现隐藏的结构、模式和分布。与监督学习不同，没有目标变量 $y$ 指导学习过程。

### 主要任务

| 任务 | 目标 | 典型应用 |
|------|------|---------|
| 聚类 (Clustering) | 将样本分组为内在类别 | 客户分群 |
| 降维 (Dimensionality Reduction) | 低维表示保留关键信息 | 数据可视化 |
| 密度估计 | 估计数据分布 $p(\mathbf{x})$ | 异常检测 |
| 关联分析 | 发现特征间共现模式 | 购物篮分析 |

## 二、聚类算法

### K-means

目标：最小化样本到所属簇中心的距离平方和：

$$
J = \sum_{i=1}^k \sum_{\mathbf{x} \in C_i} ||\mathbf{x} - \boldsymbol{\mu}_i||^2
$$

**算法步骤**：
1. 随机初始化 $k$ 个簇中心 $\boldsymbol{\mu}_1, ..., \boldsymbol{\mu}_k$
2. 分配：每个样本分配到最近的簇中心
3. 更新：重新计算每个簇的均值作为新中心
4. 重复步骤2-3直到收敛

**局限性**：
- 需预设 $k$ 值
- 对初始中心敏感
- 假设球形簇
- 对异常值敏感

### DBSCAN (Density-Based Spatial Clustering)

基于密度的聚类，不需要预设簇数量：

| 概念 | 定义 |
|------|------|
| $\epsilon$-邻域 | $N_\epsilon(p) = \{q \in D | \text{dist}(p,q) \leq \epsilon\}$ |
| 核心点 | $\vert N_\epsilon(p)\vert \geq \text{MinPts}$ |
| 边界点 | 非核心点但属于某个核心点的邻域 |
| 噪声点 | 既非核心也非边界 |

**优点**：发现任意形状簇，自动识别噪声

### 层次聚类

| 类型 | 方法 | 特点 |
|------|------|------|
| 凝聚式 (AGNES) | 自底向上合并 | 最常用 |
| 分裂式 (DIANA) | 自顶向下分裂 | 较少使用 |

**簇间距离度量**：
- **单链 (Single-link)**：$\min\{d(x,y): x \in C_i, y \in C_j\}$
- **全链 (Complete-link)**：$\max\{d(x,y): x \in C_i, y \in C_j\}$
- **平均链 (Average-link)**：$\frac{1}{|C_i||C_j|} \sum_{x \in C_i} \sum_{y \in C_j} d(x,y)$
- **Ward法**：合并使簇内方差增量最小

### 高斯混合模型 (GMM)

GMM假设数据由 $k$ 个高斯分布混合生成：

$$
p(\mathbf{x}) = \sum_{i=1}^k \pi_i \mathcal{N}(\mathbf{x} | \boldsymbol{\mu}_i, \boldsymbol{\Sigma}_i)
$$

**EM算法**求解参数：

**E步**：计算样本属于各高斯成分的后验概率

$$
\gamma_{ij} = \frac{\pi_j \mathcal{N}(\mathbf{x}_i | \boldsymbol{\mu}_j, \boldsymbol{\Sigma}_j)}{\sum_{l=1}^k \pi_l \mathcal{N}(\mathbf{x}_i | \boldsymbol{\mu}_l, \boldsymbol{\Sigma}_l)}
$$

**M步**：更新参数

$$
\boldsymbol{\mu}_j^{\text{new}} = \frac{\sum_{i=1}^N \gamma_{ij} \mathbf{x}_i}{\sum_{i=1}^N \gamma_{ij}}
$$
$$
\boldsymbol{\Sigma}_j^{\text{new}} = \frac{\sum_{i=1}^N \gamma_{ij} (\mathbf{x}_i - \boldsymbol{\mu}_j^{\text{new}})(\mathbf{x}_i - \boldsymbol{\mu}_j^{\text{new}})^T}{\sum_{i=1}^N \gamma_{ij}}
$$
$$
\pi_j^{\text{new}} = \frac{1}{N} \sum_{i=1}^N \gamma_{ij}
$$

### 聚类算法对比

| 算法 | 簇形状 | 需预设k | 对噪声 | 可扩展性 |
|------|--------|---------|--------|---------|
| K-means | 球形 | 是 | 敏感 | 好 |
| DBSCAN | 任意 | 否 | 鲁棒 | 中等 |
| 层次聚类 | 任意 | 否 | 敏感 | 差 |
| GMM | 椭球形 | 是 | 较鲁棒 | 中等 |
| Spectral | 任意 | 是 | 较鲁棒 | 差 |

## 三、降维

### PCA (主成分分析)

PCA寻找方差最大的投影方向：

**目标**：最大化投影方差

$$
\max_{\mathbf{w}} \mathbf{w}^T \boldsymbol{\Sigma} \mathbf{w} \quad \text{s.t.} \quad ||\mathbf{w}|| = 1
$$

**求解**：协方差矩阵的特征值分解

$$
\boldsymbol{\Sigma} \mathbf{w}_i = \lambda_i \mathbf{w}_i
$$

**降维**：选择前 $d$ 个最大特征值对应的特征向量

$$
X' = X W_d
$$

主成分保留的方差比例：

$$
\text{Explained Variance} = \frac{\sum_{i=1}^d \lambda_i}{\sum_{i=1}^D \lambda_i}
$$

### t-SNE (t-distributed Stochastic Neighbor Embedding)

用于高维数据可视化的非线性降维方法：

**高维空间相似度**：

$$
p_{j|i} = \frac{\exp(-||x_i - x_j||^2 / 2\sigma_i^2)}{\sum_{k \neq i} \exp(-||x_i - x_k||^2 / 2\sigma_i^2)}
$$

**低维空间相似度**（t分布）：

$$
q_{ij} = \frac{(1 + ||y_i - y_j||^2)^{-1}}{\sum_{k \neq l} (1 + ||y_k - y_l||^2)^{-1}}
$$

**KL散度优化**：

$$
\text{KL}(P||Q) = \sum_i \sum_j p_{ij} \log \frac{p_{ij}}{q_{ij}}
$$

### UMAP (Uniform Manifold Approximation and Projection)

基于流形学习的降维方法，比t-SNE更快，全局结构保留更好。

### 降维方法对比

| 方法 | 线性/非线性 | 速度 | 适用场景 |
|------|------------|------|---------|
| PCA | 线性 | 快 | 数据压缩、去相关 |
| t-SNE | 非线性 | 慢 | 可视化（局部结构） |
| UMAP | 非线性 | 中等 | 可视化（局部+全局） |
| Isomap | 非线性 | 中等 | 流形学习 |
| LLE | 非线性 | 中等 | 局部线性结构 |
| Autoencoder | 非线性 | 慢 | 特征学习 |

## 四、异常检测

### 孤立森林 (Isolation Forest)

通过随机划分快速隔离异常点，异常点更容易被隔离（路径更短）：

$$
s(x, n) = 2^{-\frac{E(h(x))}{c(n)}}
$$

其中 $E(h(x))$ 为样本 $x$ 的平均路径长度，$c(n)$ 为归一化因子。

### LOF (Local Outlier Factor)

基于局部密度：

$$
\text{LOF}_k(p) = \frac{\frac{1}{k} \sum_{o \in N_k(p)} \text{lrd}_k(o)}{\text{lrd}_k(p)}
$$

其中 $\text{lrd}_k(p)$ 为局部可达密度。LOF > 1 表示异常。

### 其他异常检测方法

| 方法 | 核心思想 | 适用场景 |
|------|---------|---------|
| One-Class SVM | 学习数据边界 | 高维异常检测 |
| Elliptic Envelope | 假设高斯分布 | 全局异常检测 |
| Autoencoder | 重构误差 | 复杂数据异常 |

## 五、关联规则挖掘

### 基本概念

| 概念 | 定义 | 公式 |
|------|------|------|
| 支持度 (Support) | 项集出现频率 | $\text{Supp}(A) = \frac{\text{count}(A)}{N}$ |
| 置信度 (Confidence) | 条件概率 | $\text{Conf}(A \Rightarrow B) = \frac{\text{Supp}(A \cup B)}{\text{Supp}(A)}$ |
| 提升度 (Lift) | 相关性度量 | $\text{Lift}(A \Rightarrow B) = \frac{\text{Conf}(A \Rightarrow B)}{\text{Supp}(B)}$ |

### Apriori算法

利用先验性质（频繁项集的所有非空子集也必须是频繁的）剪枝：

1. 生成候选 $k$-项集
2. 剪枝：移除非频繁子集
3. 计数：扫描数据库计算支持度
4. 生成频繁 $k$-项集
5. 重复直到无新频繁项集

### FP-Growth

基于FP-tree的频繁模式挖掘，无需生成候选集，效率远高于Apriori。

## 六、自监督学习

自监督学习（Self-Supervised Learning）通过设计预文任务（pretext task）从无标签数据中学习表示：

### 对比学习 (Contrastive Learning)

**SimCLR**：

$$
\mathcal{L} = -\log \frac{\exp(\text{sim}(z_i, z_j)/\tau)}{\sum_{k=1}^{2N} \mathbb{1}_{[k \neq i]} \exp(\text{sim}(z_i, z_k)/\tau)}
$$

**MoCo (Momentum Contrast)**：
- 使用动量编码器维护负样本队列
- 动态字典机制

**对比学习目标**：拉近正样本对，推开负样本对

## 七、聚类评估

### 内部评估指标

| 指标 | 公式 | 最优值 |
|------|------|--------|
| 轮廓系数 (Silhouette) | $s(i) = \frac{b(i) - a(i)}{\max(a(i), b(i))}$ | 接近1 |
| Davies-Bouldin指数 | $\text{DB} = \frac{1}{k} \sum_{i=1}^k \max_{j \neq i} \frac{\sigma_i + \sigma_j}{d(\mu_i, \mu_j)}$ | 越小越好 |
| Calinski-Harabasz | $\frac{\text{tr}(B_k)}{\text{tr}(W_k)} \times \frac{N-k}{k-1}$ | 越大越好 |

### 外部评估指标

| 指标 | 描述 |
|------|------|
| 调整兰德指数 (ARI) | 调整后的聚类与真实标签一致性 |
| 互信息 (NMI) | 归一化互信息 |
| 同质性/完整性 | Homogeneity vs Completeness |

## 八、应用场景

| 领域 | 应用 | 常用方法 |
|------|------|---------|
| 客户分群 | 市场细分、个性化推荐 | K-means, DBSCAN |
| 异常检测 | 欺诈检测、网络入侵 | Isolation Forest, LOF |
| 生物信息学 | 基因表达聚类、蛋白质分类 | 层次聚类, t-SNE |
| 图像处理 | 图像分割、特征学习 | GMM, Autoencoder |
| 推荐系统 | 用户行为聚类、物品关联 | Apriori, K-means |
| 自然语言处理 | 词嵌入、文档主题建模 | PCA, t-SNE |

## 相关条目

- [[SupervisedLearning]]
- DimensionalityReduction
- Clustering
- [[ModelEvaluation]]

## 参考资源

- Bishop, C. M. (2006). *Pattern Recognition and Machine Learning* (Chapter 9: Mixture Models and EM)
- MacQueen, J. (1967). "Some methods for classification and analysis of multivariate observations"
- Ester, M. et al. (1996). "A density-based algorithm for discovering clusters in large spatial databases"
- van der Maaten, L. & Hinton, G. (2008). "Visualizing Data using t-SNE"
- McInnes, L. et al. (2018). "UMAP: Uniform Manifold Approximation and Projection"
- Chen, T. et al. (2020). "A Simple Framework for Contrastive Learning of Visual Representations"
