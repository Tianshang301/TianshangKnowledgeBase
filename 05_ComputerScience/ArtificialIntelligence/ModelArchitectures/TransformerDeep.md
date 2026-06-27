---
aliases:
  - Transformer深度解析
  - Transformer架构详解
  - Self-Attention机制
tags:
  - AI/Transformer
  - AI/Architecture
  - AI/DeepLearning
created: 2026-06-28
updated: 2026-06-28
---

# Transformer深度解析

Transformer是2017年Google在"Attention Is All You Need"中提出的架构，彻底改变了NLP乃至整个深度学习领域。本文深入剖析其核心组件和现代优化技术。

## 自注意力机制数学推导

### 基本公式

给定输入序列 $X \in \mathbb{R}^{n \times d}$，通过三个权重矩阵生成Query、Key、Value：

$$Q = XW^Q, \quad K = XW^K, \quad V = XW^V$$

其中 $W^Q, W^K \in \mathbb{R}^{d \times d_k}$，$W^V \in \mathbb{R}^{d \times d_v}$。

注意力计算：

$$\text{Attention}(Q, K, V) = \text{softmax}\left(\frac{QK^T}{\sqrt{d_k}}\right)V$$

### 缩放因子

$\sqrt{d_k}$ 的作用：当 $d_k$ 较大时，$QK^T$ 的方差为 $d_k$，导致softmax输出趋向one-hot分布，梯度消失。除以 $\sqrt{d_k}$ 将方差稳定在1附近。

### 多头注意力

$$\text{MultiHead}(Q, K, V) = \text{Concat}(\text{head}_1, ..., \text{head}_h)W^O$$

$$\text{head}_i = \text{Attention}(QW_i^Q, KW_i^K, VW_i^V)$$

多头机制允许模型同时关注不同位置和不同语义子空间的信息。

### 复杂度分析

- 时间复杂度：$O(n^2 d)$，n为序列长度
- 空间复杂度：$O(n^2)$（存储注意力矩阵）
- 这是长序列处理的主要瓶颈

## 位置编码

Transformer本身不具备位置感知能力，需要额外的位置编码。

### 正弦位置编码（Sinusoidal）

原始Transformer使用固定的正弦函数：

$$PE_{(pos, 2i)} = \sin(pos / 10000^{2i/d})$$
$$PE_{(pos, 2i+1)} = \cos(pos / 10000^{2i/d})$$

- 优点：无需训练，可泛化到更长序列
- 缺点：表达能力有限，相对位置信息隐式

### RoPE（Rotary Position Embedding）

将位置信息编码为旋转矩阵，对Query和Key施加旋转变换：

$$f(q, m) = R_m q, \quad f(k, n) = R_n k$$

其中 $R_m$ 是按位置m构造的旋转矩阵。核心优势：$\langle f(q,m), f(k,n) \rangle$ 仅依赖于相对位置 $m-n$。

- 被LLaMA、Qwen、Mistral等主流模型广泛采用
- 支持通过NTK-aware插值等方法扩展到训练长度之外

### ALiBi（Attention with Linear Biases）

直接在注意力分数上加一个与距离成正比的线性偏置：

$$\text{softmax}(q_i k_j^T - m \cdot |i-j|)$$

- 无需修改输入Embedding
- 不同注意力头使用不同的斜率m
- 训练短推理长的外推性好
- 被BLOOM、MPT等模型采用

## 前馈网络（FFN）

### 标准FFN

$$\text{FFN}(x) = \text{ReLU}(xW_1 + b_1)W_2 + b_2$$

中间维度通常是隐藏维度的4倍。

### GLU变体（Gated Linear Unit）

引入门控机制：

$$\text{GLU}(x) = (\sigma(xW_g) \odot xW_1)W_2$$

### SwiGLU

将sigmoid替换为SiLU/Swish激活函数：

$$\text{SwiGLU}(x) = (\text{Swish}(xW_g) \odot xW_1)W_2$$

- LLaMA、PaLM等模型采用
- 通常将中间维度调整为 $\frac{8}{3}d$ 以保持参数量不变
- 实验表明比ReLU和标准GLU效果更好

### GeGLU

使用GELU激活的门控变体：

$$\text{GeGLU}(x) = (\text{GELU}(xW_g) \odot xW_1)W_2$$

## 归一化

### LayerNorm

$$\text{LN}(x) = \gamma \odot \frac{x - \mu}{\sqrt{\sigma^2 + \epsilon}} + \beta$$

对每个样本的所有特征维度计算均值和方差。

### RMSNorm

省略均值中心化，仅做缩放归一化：

$$\text{RMSNorm}(x) = \frac{x}{\sqrt{\frac{1}{d}\sum_{i=1}^{d}x_i^2 + \epsilon}} \odot \gamma$$

- 计算更快（省略均值计算）
- 被LLaMA、Qwen、Gemma等采用
- 实验表明效果与LayerNorm相当

### Pre-Norm vs Post-Norm

- **Post-Norm**（原始Transformer）：归一化在残差连接之后
- **Pre-Norm**：归一化在子层之前，训练更稳定
- 现代大模型普遍采用Pre-Norm + RMSNorm

## 优化技术

### FlashAttention

通过IO感知的分块计算优化注意力的内存访问模式。

- **核心问题**：标准注意力需要将 $n \times n$ 的注意力矩阵完整写入HBM（高带宽内存）
- **解决方案**：将Q、K、V分块，在SRAM（片上内存）中完成计算，避免完整矩阵存储
- **效果**：速度提升2-4倍，内存从 $O(n^2)$ 降至 $O(n)$
- **FlashAttention-2**：进一步优化并行度和工作分区
- **FlashAttention-3**：利用异步性和低精度技术

### KV Cache

自回归生成时缓存已计算的Key和Value，避免重复计算。

- 每生成一个新token只需计算其Q与所有缓存K、V的注意力
- 内存占用：$2 \times n_{layers} \times n_{heads} \times d_{head} \times seq\_len \times batch\_size \times dtype\_size$
- 长序列下KV Cache成为主要内存瓶颈

### GQA（Grouped-Query Attention）

多个Query头共享同一组Key-Value头，减少KV Cache大小。

- **MHA**：每个Q头对应独立的K、V头
- **MQA**：所有Q头共享一组K、V（极端情况）
- **GQA**：每g个Q头共享一组K、V头（折中方案）
- LLaMA 2 70B、Qwen2等采用GQA
- 在质量损失极小的情况下显著减少推理内存和延迟

### 其他优化

- **PagedAttention**（vLLM）：类似操作系统虚拟内存的KV Cache管理
- **Sliding Window Attention**：限制注意力范围为局部窗口
- **Sparse Attention**：仅计算部分注意力对（如Longformer的dilated attention）
- **Multi-Query Latent Attention**（MLA）：DeepSeek-V2提出的低秩压缩方案
