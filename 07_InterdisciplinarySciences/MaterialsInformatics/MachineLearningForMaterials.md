# 材料机器学习

## 概述

机器学习正在深刻改变材料科学的研究范式从材料性质预测到向设计，从高量筛到实验优化，ML方法显著加了新材料的发现与开发周期?
## 材料表示（Materials Representation?
### 基于成分的表?使用元素属的统计量（平均值方差最大最小等）组成特征向量如元素属统计（Element Properties Statistics, EPS）Matscholar嵌入?
### 基于结构的表?
#### Coulomb矩阵
对分子或晶体中的原子对，?$\frac{Z_i Z_j}{|R_i - R_j|}$ 填充矩阵?Z_i$ 为原子序数，$R_i$ 为位置矩阵经本征值分解后作为特征?
#### Ewald求和矩阵
将Coulomb矩阵中的实空间项替换为Ewald求和，更好处理周期边界条件?
#### 径向分布函数（Radial Distribution Function, RDF?以参考原子为中心，统计各距离壳层内的原子数密度，形成$g(r)$曲线作为结构特征?
### 基于图的表示

#### 晶体图（Crystal Graph?将晶体结构表示为图，节点为原子（含元素特征），边为原子间连接（含距离特征）晶体图卷积神经网络（CGCNN）过消息传聚合邻域信息进行质预测?
#### MEGNet（Materials Graph Network?扩展了CGCNN，引入整体特征（温度、压力等），支持多任务学习?
## 性质预测任务

### 带隙（Band Gap?预测半导?绝缘体的电子带隙。常用方法：CGCNN、图神经网络、随机森林?
### 形成能（Formation Energy?计算化合物相对于元素的能量稳定高精度预测可替代部分DFT计算?
### 弹常数（Elastic Constants?预测材料的力学质（体积模?$K$、剪切模?$G$、杨氏模?$E$等）?
### 热导率（Thermal Conductivity?预测晶格热导?$\kappa$，对热电材料和热管理材料设计至关重要?
## 生成模型

### 变分自编码器（VAE?- **CrystalGAN**：在晶体对称性约束下生成稳定的新型晶体结?- **正交化VAE**：在潜在空间中解耦控制不同物理质的隐变量

### 生成对抗网络（GANs?- 生成新颖的晶体结构组成，由判别器验证其合理?- 条件GAN允许按目标质条件生成

### 扩散模型（Diffusion Models?近年兴起的新范式，过学习从噪声步去噪的过程生成晶体结构在材料多样性方面表现优异?
## 材料嵌入（Materials Embedding?
### Mat2Vec
利用大规模未标注材料数据（类似自然语訢处理中的词嵌入）预训练材料成分和结构的低维向量表示?
### Materials BERT
借鉴BERT的掩码预训练策略，在材料数据库上预训练后迁移至下游预测任务?
## 逆向设计（Inverse Design?
从目标质出发反向搜索朢优材料结构方法包括：
- **贝叶斯优?*：代理模型（高斯过程）指导实验迭?- **遗传算法**：过交叉和变异操作演化材料种?- **强化学习**：智能体在化学空间中探索高奖励区?
## 高量筛与主动学习

### 高量虚拟筛?使用已有ML模型对庞大的候材料库（如数百万种假想化合物）进行快预筛?
### 主动学习（Active Learning?迭代策略：模型在不确定高的区域主动择朢有信息量的实验进行验证，从最大化每次实验的信息增益关键策略包括：
- **不确定采?*（Uncertainty Sampling）：选择预测方差大的样本
- **期望改进**（Expected Improvement, EI）：平衡探索与利?- **汤普森采?*（Thompson Sampling）：从后验分布采样指导择

## 不确定量化（Uncertainty Quantification?
### 贝叶斯神经网?为网络权重引入先验分布，通过变分推断或蒙特卡洛dropout估计预测不确定?
### 集成方法（Ensemble Methods?训练多个模型，用预测结果的方差作为不确定性估计?
### 高斯过程回归（Gaussian Process Regression?提供预测均和预测方差的闭合形式，是贝叶斯优化的标准代理模型?

## 相关条目

[[04_EngineeringAndTechnology/MechanicsAndMaterials/MaterialsScience/INDEX|MaterialsScience]], [[05_ComputerScience/ArtificialIntelligence/MachineLearning/INDEX|MachineLearning]], ComputationalChemistry, [[MaterialsGenome]]
