---
aliases:
  - 混合专家模型
  - Mixture of Experts
  - MoE架构
tags:
  - AI/MoE
  - AI/Architecture
  - AI/LLM
created: 2026-06-28
updated: 2026-06-28
---

# 混合专家模型（MoE）

Mixture of Experts（MoE）是一种条件计算架构，通过稀疏激活实现"大参数量、低计算量"的效果。模型拥有大量参数但每次推理只激活其中一小部分，在保持推理效率的同时获得更强的模型容量。

## 稀疏MoE架构

### 基本原理

MoE层替换Transformer中的FFN层，包含多个Expert子网络和一个Router网络：

$$y = \sum_{i=1}^{N} g_i(x) \cdot E_i(x)$$

其中 $g_i$ 是Router对第i个Expert的门控权重，$E_i$ 是第i个Expert的输出。关键在于 $g_i$ 是稀疏的，大多数值为0。

### GShard（Google, 2020）

首个将MoE成功应用于大规模Transformer的工作。

- 在每隔一层的FFN位置替换为MoE层
- 使用Top-2路由：每个token选择2个Expert
- 引入容量因子（Capacity Factor）控制每个Expert处理的token数上限
- 引入辅助损失（Auxiliary Loss）促进负载均衡
- 扩展到600B参数，在多语言翻译任务上取得突破

### Switch Transformer（Google, 2021）

将Top-2简化为Top-1路由，进一步提升效率。

- **Top-1路由**：每个token只发送给1个Expert
- **简化通信**：减少Expert间的数据交换
- **精度恢复**：通过更多Expert数量弥补Top-1的信息损失
- 扩展到1.6T参数
- 训练效率相比同等计算量的稠密模型提升4-7倍

### 主流架构模式

- 替换策略：通常每隔一层替换（也有全替换方案）
- Expert数量：8-256个不等
- 总参数量可达数千亿，但每个token仅激活数十亿参数

## 路由机制

路由（Router/Gate）决定每个token分配给哪些Expert，是MoE的核心组件。

### Top-K路由

最常用的路由方式：

1. 将token表示通过线性层映射到Expert数量的logits
2. 经过softmax获取概率分布
3. 选择概率最高的K个Expert
4. 对选中Expert的权重重新归一化

Top-1简单高效但信息损失大；Top-2更稳健但计算和通信开销更大。

### Expert Choice路由（Google, 2022）

反转选择方向：由Expert选择token而非token选择Expert。

- 每个Expert从所有token中选择Top-K个最重要的token
- 天然保证负载均衡（每个Expert处理固定数量的token）
- 但可能导致部分token不被任何Expert选中
- 需要辅助机制确保所有token都被处理

### 其他路由策略

- **Soft MoE**（Google, 2023）：软分配，token的加权组合发送给Expert，避免离散路由的训练不稳定性
- **Hash路由**：基于token哈希值确定性分配，无需学习路由参数
- **随机路由**：部分Expert通过随机选择，引入探索性
- **Sinkhorn路由**：基于Sinkhorn算法的双随机矩阵路由

## 负载均衡损失

MoE训练中的核心挑战：路由器倾向于将大多数token发送给少数Expert（"赢者通吃"），导致其他Expert得不到训练。

### 辅助损失（Auxiliary Loss）

GShard和Switch Transformer引入的标准方案：

$$\mathcal{L}_{aux} = \alpha \cdot N \cdot \sum_{i=1}^{N} f_i \cdot P_i$$

其中 $f_i$ 是Expert i实际处理的token比例，$P_i$ 是Router分配给Expert i的平均概率，$N$ 是Expert数量，$\alpha$ 是系数。

该损失鼓励所有Expert被均匀使用。

### 问题与改进

- **损失系数敏感**：$\alpha$ 太大会干扰主损失，太小无法平衡
- **容量因子**：限制每个Expert的最大处理量，超出的token被丢弃
- **Z-Loss**（ST-MoE）：惩罚Router logits的绝对大小，稳定训练
- **无辅助损失方案**（DeepSeek-V2）：通过细粒度Expert和共享Expert实现自然均衡

## 代表性模型

### Mixtral 8x7B（Mistral AI, 2024）

- 8个Expert，每个token激活2个（Top-2）
- 总参数46.7B，激活参数12.9B
- 每个Expert为独立的7B FFN模块
- 在多数基准上匹配或超越LLaMA 2 70B
- 推理速度约为同等质量稠密模型的6倍

### DeepSeek-V2（DeepSeek, 2024）

创新性的MoE架构设计：

- **细粒度Expert**：将标准Expert拆分为更小的粒度（如160个小Expert）
- **共享Expert**：保留1-2个所有token都会经过的共享Expert
- **无辅助损失均衡**：通过Expert粒度和共享机制自然实现负载均衡
- **MLA注意力**：Multi-Head Latent Attention进一步压缩KV Cache
- 总参数236B，激活参数21B

### Grok（xAI, 2024）

- xAI的首个模型，采用MoE架构
- 总参数314B，激活参数约86B
- 8个Expert，Top-2路由
- 以幽默风格和较少安全限制著称

### 其他MoE模型

- **DBRX**（Databricks）：16个Expert，Top-4路由，132B总参数
- **Qwen MoE**：Qwen系列的MoE变体
- **Grok-2**：xAI的后续模型

## 训练与推理优化

### 训练优化

- **Expert并行**：不同Expert放在不同GPU上
- **数据并行 + Expert并行**：混合使用两种并行策略
- **通信优化**：All-to-All通信模式，需要专门优化
- **精度策略**：Router使用float32，Expert可使用bfloat16
- **课程学习**：逐步增加Expert数量或容量因子

### 推理优化

- **Expert Offloading**：将不活跃的Expert卸载到CPU或磁盘
- **Expert Caching**：预测即将使用的Expert并预加载
- **量化**：对Expert进行INT4/INT8量化减少内存
- **Speculative Decoding**：使用小模型预测大MoE模型的输出
- **Batch Expert Loading**：同一批次的token共享Expert加载

### 部署挑战

- 内存占用大：总参数量远超激活参数量
- 负载不均：热门Expert成为瓶颈
- 批处理效率：不同token路径不同，batch内计算不规则
- 通信开销：分布式部署时Expert间通信成本高

### 未来方向

- 更智能的路由机制（自适应、任务感知）
- 端到端训练的软硬协同优化
- MoE与其他技术的结合（如MoE + SSM）
- 更大规模的MoE模型（万亿参数级）
