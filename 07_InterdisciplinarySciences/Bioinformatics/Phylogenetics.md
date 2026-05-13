# 系统发育?
## 概述

系统发育学（Phylogenetics）研究物种基因或蛋白质之间的进化关系，过构建系统发育树来揭示生物演化历史。它是进化生物学、生物信息学和比较基因组学的核心工具?
## 系统发育树基本概?
### 树的拓扑结构
- **树根（Root?*：表示所有序列的共同祖先，赋予进化方?- **节点（Node?*：内部节点代表祖先类群，叶节点代表现有类?- **分支（Branch?*：连接节点的线段，长度常表示进化距离或时?- **有根?vs 无根?*：有根树具有进化方向，无根树仅表示亲疏关?
### 单系群并系群与多系群
- **单系群（Monophyly?*：包含共同祖先及其所有后?- **并系群（Paraphyly?*：包含共同祖先及其部分后?- **多系群（Polyphyly?*：不包含朢近共同祖先的群体

## 距离?
### UPGMA（Unweighted Pair Group Method with Arithmetic Mean?假设恒定进化速率（分子钟），基于遗传距离矩阵，采用算术平均聚类算法简单但假设严格?
### 邻接法（Neighbor-Joining, NJ?不假设恒定进化率，过朢小化总分支长度构建树。计算效率高，用于大数据集?
## 基于特征的方?
### 朢大简约法（Maximum Parsimony, MP?寻找霢要最少进化事件（突变、替换）的树。用于进化率较低、序列分歧较小的数据集?
### 朢大似然法（Maximum Likelihood, ML?在给定的替代模型下，寻找使观测数据概率最大的树统计理论基硢扎实，计算强度大?
### 贝叶斯推断（Bayesian Inference, BI?利用MCMC（马尔可夫链蒙特卡洛）方法对树空间进行采样，估计后验概率分布。可以整合先验信息?
- **MCMC策略**：MrBayes、BEAST等软件使用Metropolis-Hastings算法在树空间随机游走
- **后验概率（Posterior Probability?*：给定数据下拓扑结构的后验支?- **收敛诊断**：过ESS（Effective Sample Size）和潜在比例缩减因子（PSRF）判断MCMC收敛

## 替代模型

### 核苷酸替代模?- **Jukes-Cantor（JC69?*：最箢单的模型，所有替代率相等
- **Kimura 2-parameter（K80?*：区分转换和颠换速率
- **General Time Reversible（GTR?*：最通用的可逆模型，6个率参数 + 碱基频率参数
- **模型选择**：过似然比检验（LRT）AIC、BIC选择朢优模?
### 氨基酸替代模?- **PAM矩阵**：基于全球蛋白质序列比对的经验替代矩?- **BLOSUM矩阵**：基于局部比对的经验替代矩阵
- **JTT、WAG、LG**：常用的经验氨基酸替代模?
## 树评?
### 自举法（Bootstrap?从原始数据中重抽样（通常100-1000次），构建多个树，计算各分支在重抽样树中出现的频率自举?$\ge 70\%$ 通常被认为可信?
### 后验概率
贝叶斯分析中分支出现的概率，丢?$\ge 0.95$ 被认为具有统计学支持?
## 分子钟（Molecular Clock?
### 严格分子?扢有谱系的进化速率恒定，进化距离与分歧时间成正比?
### 宽松分子钟（Relaxed Molecular Clock?允许不同谱系进化速率不同，使用对数正态分布或指数分布模型描述速率变异?
## 主要软件比较

| 软件 | 方法 | 特点 |
|------|------|------|
| RAxML | ML | 支持大数据集，多线程并行 |
| MrBayes | BI | 灵活的贝叶斯分析，广泛应?|
| BEAST/BEAST2 | BI | 时间标定树，分子钟分?|
| MEGA | ML/MP/NJ | 图形界面友好，教学常?|
| IQ-TREE | ML | 自动模型选择，超快自?|

## 相关条目

ComputationalBiology, [[02_NaturalSciences/Biology/Genetics/INDEX|Genetics]], [[07_InterdisciplinarySciences/DataScience/INDEX|DataScience]], Genomics, [[02_NaturalSciences/Biology/MolecularBiology/INDEX|MolecularBiology]]
