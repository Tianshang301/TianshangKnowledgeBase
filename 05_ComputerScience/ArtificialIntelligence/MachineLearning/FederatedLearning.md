---
aliases:
  - 联邦学习
  - Federated Learning
  - FL
tags:
  - machine-learning
  - privacy-preserving
  - distributed-computing
  - federated-learning
  - AI
created: 2026-06-28
updated: 2026-06-28
---

# 联邦学习 (Federated Learning)

## 1. 定义与概述

联邦学习是一种**分布式机器学习范式**，其核心思想是"数据不动模型动"。与传统的集中式训练不同，联邦学习允许各个参与方（客户端）在本地数据上进行训练，仅将模型更新（如梯度或权重）发送到中央服务器进行聚合，从而实现**数据不出本地**的协作训练。

### 1.1 联邦学习的起源

- **2016年**：Google 首次提出 Federated Learning 概念，用于改进 Gboard 键盘预测
- **核心动机**：隐私法规（GDPR、CCPA）日益严格，数据集中存储面临合规风险
- **目标**：在保护数据隐私的同时，利用分布式数据提升模型性能

### 1.2 与传统分布式学习的区别

| 特性 | 传统分布式学习 | 联邦学习 |
|------|--------------|---------|
| 数据位置 | 集中式存储 | 分散在各客户端 |
| 数据分布 | IID（独立同分布） | Non-IID（非独立同分布） |
| 通信模式 | 高带宽、低延迟 | 低带宽、高延迟 |
| 隐私保护 | 较少考虑 | 核心设计目标 |
| 参与方 | 可信集群节点 | 不可信或半可信客户端 |

## 2. 核心流程

联邦学习的标准训练流程包含以下步骤：

### 2.1 基本流程

```
1. 服务器初始化全局模型
2. 服务器选择参与训练的客户端子集
3. 服务器将当前全局模型分发给选中的客户端
4. 各客户端在本地数据上训练模型
5. 客户端将模型更新（梯度/权重）上传至服务器
6. 服务器聚合所有客户端的更新，生成新的全局模型
7. 重复步骤 2-6 直到收敛
```

### 2.2 本地训练过程

每个客户端 $k$ 的本地目标函数为：

$$F_k(w) = \frac{1}{n_k} \sum_{i=1}^{n_k} l(w; x_i, y_i)$$

其中 $n_k$ 是客户端 $k$ 的本地样本数量，$l$ 是损失函数。

全局目标函数为：

$$F(w) = \sum_{k=1}^{K} \frac{n_k}{n} F_k(w)$$

### 2.3 通信轮次

- **Communication Round**：每一轮包含一次模型分发和一次模型上传
- **Local Epochs**：每个客户端在本地训练的轮数
- **Client Fraction**：每轮参与训练的客户端比例

## 3. 聚合算法

### 3.1 FedAvg (Federated Averaging)

**FedAvg** 是最基础的联邦学习聚合算法，由 McMahan 等人于 2017 年提出。

**聚合公式**：

$$w_{global} = \sum_{k=1}^{K} \frac{n_k}{n} w_k$$

**特点**：
- 简单高效
- 假设数据 IID 分布时效果良好
- 在 Non-IID 数据上性能下降明显

### 3.2 FedProx

**FedProx** 在 FedAvg 基础上添加了**近端项**（Proximal Term），约束本地模型不要偏离全局模型太远。

**本地目标函数**：

$$F_k^{prox}(w) = F_k(w) + \frac{\mu}{2} \|w - w_{global}\|^2$$

**优势**：
- 在 Non-IID 数据上更稳定
- 允许异构的本地计算资源

### 3.3 FedNova

**FedNova** 解决了客户端本地训练步数不一致的问题，通过**归一化平均**实现公平聚合。

**核心思想**：根据每个客户端的实际梯度更新步数进行加权，而非简单平均。

### 3.4 FedMA (Federated Matched Averaging)

**FedMA** 通过**贝叶斯非参数方法**匹配客户端模型的神经元，实现更精细的模型聚合。

**适用场景**：深度神经网络的层级聚合，尤其在处理异构模型架构时。

### 3.5 其他聚合算法

- **FedBN**：保留本地 BatchNorm 层，仅共享其他层
- **FedPer**：共享基础层 + 本地个性化层
- **FedRep**：表示学习 + 分类器分离
- **SCAFFOLD**：使用控制变量修正客户端漂移

## 4. 隐私保护机制

### 4.1 差分隐私 (Differential Privacy, DP)

**核心思想**：在模型更新中添加校准噪声，使得单个数据样本的存在与否不会显著影响输出。

**实现方式**：
- **本地差分隐私 (Local DP)**：客户端在上传前添加噪声
- **中心化差分隐私 (Central DP)**：服务器在聚合后添加噪声
- **隐私预算**：$\epsilon$-差分隐私，$\epsilon$ 越小隐私保护越强

### 4.2 安全聚合 (Secure Aggregation)

**目标**：服务器只能看到聚合后的模型更新，无法看到单个客户端的更新。

**技术方案**：
- **Secret Sharing**：将模型更新拆分为多个份额
- **Masking**：使用随机掩码加密更新
- **Secure Multi-Party Computation (MPC)**：多方安全计算

### 4.3 同态加密 (Homomorphic Encryption)

**定义**：在密文上直接进行数学运算，解密后结果与明文运算一致。

**在联邦学习中的应用**：
- 客户端加密本地模型更新
- 服务器在密文上执行聚合操作
- 解密后得到聚合结果

**挑战**：计算开销大，通信成本高。

### 4.4 可信执行环境 (TEE)

**Intel SGX / ARM TrustZone**：在硬件隔离的可信环境中执行聚合操作。

## 5. 应用场景

### 5.1 医疗数据协作

- **跨医院联合训练**：不同医院的数据无法出院，但可以联合训练诊断模型
- **案例**：COVID-19 胸部 X 光诊断、肿瘤检测
- **框架**：Intel FLARE、NVIDIA FLARE

### 5.2 金融风控

- **反欺诈模型**：多家银行联合训练，不共享客户数据
- **信用评估**：跨机构数据协作，提升风控精度
- **合规要求**：满足金融监管的数据隔离要求

### 5.3 键盘预测 (Gboard)

- **Google Gboard**：联邦学习的首个大规模商用案例
- **目标**：改进下一词预测、智能回复
- **规模**：数亿设备参与训练

### 5.4 其他应用

- **推荐系统**：跨平台用户行为建模
- **自动驾驶**：多车数据联合训练
- **物联网**：边缘设备协同学习

## 6. 主流框架

### 6.1 PySyft

- **开发者**：OpenMined
- **特点**：基于 PyTorch，支持 MPC、DP、联邦学习
- **适用场景**：研究与原型开发

### 6.2 TensorFlow Federated (TFF)

- **开发者**：Google
- **特点**：与 TensorFlow 深度集成，支持模拟和部署
- **适用场景**：生产环境部署

### 6.3 FATE (Federated AI Technology Enabler)

- **开发者**：WeBank（微众银行）
- **特点**：工业级联邦学习平台，支持横向和纵向联邦
- **适用场景**：金融、医疗等企业级应用

### 6.4 Flower

- **特点**：轻量级、框架无关、易于扩展
- **支持**：PyTorch、TensorFlow、JAX 等
- **适用场景**：快速原型开发和研究

### 6.5 NVIDIA FLARE

- **特点**：专注于医疗和企业级应用
- **集成**：与 NVIDIA Clara 医疗平台深度集成
- **适用场景**：医疗影像、药物发现

## 7. 2025-2026 年最新进展

### 7.1 联邦大模型微调

- **FedLLM**：在联邦环境中微调大型语言模型（LLM）
- **LoRA 联邦学习**：仅传输低秩适配器参数，大幅降低通信开销
- **案例**：多家医院联合微调医疗 LLM

### 7.2 跨机构协作

- **数据要素流通**：中国《数据安全法》推动联邦学习落地
- **隐私计算平台**：蚂蚁链摩斯、华控清交等商业化平台
- **标准化**：IEEE P3652.1 联邦学习标准

### 7.3 法规推动

- **EU AI Act**：要求 AI 系统具备可追溯性和隐私保护
- **中国数据出境评估**：联邦学习成为合规解决方案
- **美国 HIPAA**：医疗数据联邦学习应用加速

### 7.4 技术突破

- **异构模型联邦**：不同架构的模型也能参与联邦训练
- **联邦强化学习**：多智能体环境下的联邦学习
- **联邦持续学习**：应对数据分布随时间变化的挑战

## 8. 挑战与开放问题

### 8.1 数据异构性 (Non-IID)

- **问题**：客户端数据分布差异大，全局模型性能下降
- **表现**：标签分布偏斜、特征分布偏斜、数量不平衡
- **解决方案**：FedProx、SCAFFOLD、个性化联邦学习

### 8.2 通信开销

- **问题**：模型参数传输消耗大量带宽
- **解决方案**：
  - **梯度压缩**：Top-K 稀疏化、随机稀疏化
  - **模型量化**：低精度传输
  - **异步更新**：减少等待时间

### 8.3 拜占庭容错 (Byzantine Fault Tolerance)

- **问题**：恶意客户端发送错误的模型更新
- **攻击方式**：模型中毒、后门攻击
- **防御方案**：Krum、Median、Trimmed Mean 等鲁棒聚合算法

### 8.4 系统异构性

- **问题**：客户端计算能力、网络带宽差异大
- **解决方案**：自适应本地训练轮数、模型剪枝、异步聚合

### 8.5 激励机制

- **问题**：如何激励客户端参与联邦训练
- **方案**：基于 Shapley 值的贡献评估、数据市场定价

## 9. 参考资源

### 9.1 经典论文

- McMahan et al., "Communication-Efficient Learning of Deep Networks from Decentralized Data", AISTATS 2017
- Li et al., "Federated Optimization in Heterogeneous Networks", MLSys 2020 (FedProx)
- Kairouz et al., "Advances and Open Problems in Federated Learning", 2021

### 9.2 学习资源

- [Federated Learning Book](https://federated-learning.org/) - 综合性教材
- [Google AI Federated Learning](https://ai.google/research/pubs/?area=FederatedLearning) - Google 研究论文
- [Flower Documentation](https://flower.dev/docs/) - 实践教程

### 9.3 开源项目

- [Flower](https://github.com/adap/flower) - 联邦学习框架
- [PySyft](https://github.com/OpenMined/PySyft) - 隐私保护机器学习
- [FATE](https://github.com/FederatedAI/FATE) - 工业级联邦学习平台
