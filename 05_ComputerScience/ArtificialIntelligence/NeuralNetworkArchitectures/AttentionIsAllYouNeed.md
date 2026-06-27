---
aliases:
  - Transformer
  - Attention Is All You Need
  - Self-Attention
  - Multi-Head Attention
tags:
  - deep-learning
  - transformer
  - attention-mechanism
  - nlp
  - neural-network-architecture
  - seminal-paper
created: 2026-06-27
updated: 2026-06-27
---

# Attention Is All You Need

> **论文信息**: Vaswani A, Shazeer N, Parmar N, et al. "Attention Is All You Need." *NeurIPS 2017*. arXiv:1706.03762
>
> **机构**: Google Brain / Google Research
>
> **引用量**: 120,000+ (截至2026年)

---

## 1. 历史背景与动机

### 1.1 RNN/LSTM 时代的主导地位

在 Transformer 出现之前，序列建模领域由 Recurrent Neural Network (RNN) 及其变体 Long Short-Term Memory (LSTM) 主导。这些架构在机器翻译、语言建模、语音识别等任务上取得了显著成果。

RNN 的核心思想是通过隐状态 $h_t$ 逐步处理序列：

$$h_t = \tanh(W_{hh} h_{t-1} + W_{xh} x_t)$$

然而，RNN 存在两个根本性问题：

1. **梯度消失/爆炸问题 (Vanishing/Exploding Gradients)**：在反向传播通过时间 (BPTT) 过程中，梯度需要通过多个时间步传播，导致梯度指数级衰减或增长。

2. **顺序计算瓶颈 (Sequential Computation Bottleneck)**：$h_t$ 依赖于 $h_{t-1}$，无法并行化，严重限制了训练效率。

### 1.2 Attention 机制的萌芽

Bahdanau et al. (2014) 在论文 "Neural Machine Translation by Jointly Learning to Align and Translate" (arXiv:1409.0473) 中首次引入 Attention 机制，用于解决 Seq2Seq 模型中信息瓶颈问题。

传统 Seq2Seq 模型将整个输入序列压缩为固定长度向量 $c$，而 Bahdanau Attention 允许解码器在每个时间步动态关注输入序列的不同部分：

$$\alpha_{ij} = \frac{\exp(e_{ij})}{\sum_{k=1}^{T_x} \exp(e_{ik})}$$

$$e_{ij} = a(s_{i-1}, h_j)$$

$$c_i = \sum_{j=1}^{T_x} \alpha_{ij} h_j$$

### 1.3 关键洞察：Attention 的潜力

Vaswani 等人观察到，Attention 机制本身具有强大的建模能力，**无需依赖循环结构**。这引出了一个大胆的问题：

> **能否构建一个完全基于 Attention 的架构，彻底抛弃循环和卷积？**

---

## 2. 核心创新：Scaled Dot-Product Attention

### 2.1 Query-Key-Value 框架

Transformer 的核心是将 Attention 建模为 Query (Q)、Key (K)、Value (V) 三个矩阵的交互：

- **Query (查询)**: 当前位置想要获取的信息
- **Key (键)**: 每个位置提供的索引信息
- **Value (值)**: 每个位置的实际内容

给定输入序列 $X \in \mathbb{R}^{n \times d_{model}}$，通过线性投影得到：

$$Q = XW^Q, \quad K = XW^K, \quad V = XW^V$$

其中 $W^Q \in \mathbb{R}^{d_{model} \times d_k}$，$W^K \in \mathbb{R}^{d_{model} \times d_k}$，$W^V \in \mathbb{R}^{d_{model} \times d_v}$。

### 2.2 Scaled Dot-Product Attention 公式

$$\text{Attention}(Q, K, V) = \text{softmax}\left(\frac{QK^T}{\sqrt{d_k}}\right) V$$

**计算步骤分解**：

```
输入: Q ∈ ℝ^(n×d_k), K ∈ ℝ^(m×d_k), V ∈ ℝ^(m×d_v)

步骤1: 计算相似度矩阵
    S = QK^T ∈ ℝ^(n×m)
    S_ij = q_i · k_j (点积)

步骤2: 缩放
    S_scaled = S / √d_k

步骤3: 归一化 (逐行 softmax)
    A = softmax(S_scaled) ∈ ℝ^(n×m)
    A_ij = exp(S_ij/√d_k) / Σ_j exp(S_ij/√d_k)

步骤4: 加权求和
    Output = AV ∈ ℝ^(n×d_v)
```

### 2.3 为什么需要 √d_k 缩放？

假设 $q_i$ 和 $k_j$ 的每个分量独立同分布，均值为 0，方差为 1。则点积 $q_i \cdot k_j$ 的期望为 0，方差为 $d_k$：

$$\text{Var}(q_i \cdot k_j) = \text{Var}\left(\sum_{l=1}^{d_k} q_{il} k_{jl}\right) = d_k$$

当 $d_k$ 较大时，点积的方差也较大，导致 softmax 的输入值范围过大。在极端情况下，softmax 会饱和到 one-hot 分布，梯度接近于零。

除以 $\sqrt{d_k}$ 将方差归一化为 1，确保 softmax 处于有效的工作区间。

**数学证明**：

$$\text{Var}\left(\frac{q_i \cdot k_j}{\sqrt{d_k}}\right) = \frac{d_k}{d_k} = 1$$

---

## 3. Multi-Head Attention

### 3.1 动机与设计

单一 Attention 头只能学习一种关注模式。然而，语言中存在多种不同类型的依赖关系：
- 语法依赖 (主语-谓语)
- 语义依赖 (指代消解)
- 位置依赖 (局部上下文)

**解决方案**：并行运行多个 Attention 头，每个头学习不同的投影空间。

### 3.2 数学形式

$$\text{MultiHead}(Q, K, V) = \text{Concat}(\text{head}_1, ..., \text{head}_h) W^O$$

$$\text{head}_i = \text{Attention}(QW_i^Q, KW_i^K, VW_i^V)$$

其中：
- $W_i^Q \in \mathbb{R}^{d_{model} \times d_k}$
- $W_i^K \in \mathbb{R}^{d_{model} \times d_k}$
- $W_i^V \in \mathbb{R}^{d_{model} \times d_v}$
- $W^O \in \mathbb{R}^{hd_v \times d_{model}}$

### 3.3 参数设置

原论文使用 $h = 8$ 个 Attention 头：

$$d_k = d_v = \frac{d_{model}}{h} = \frac{512}{8} = 64$$

**计算复杂度分析**：

| 操作 | 复杂度 |
|------|--------|
| 单头 Full Attention | $O(n^2 \cdot d)$ |
| 多头 Attention (h 头) | $O(n^2 \cdot d)$ (总维度不变) |
| RNN (单层) | $O(n \cdot d^2)$ |

当序列长度 $n < d$ 时，Self-Attention 比 RNN 更高效。

### 3.4 Multi-Head Attention 的可视化理解

```
输入 X (n × 512)
    │
    ├──→ W₁^Q, W₁^K, W₁^V → Head 1 (语法关系)
    ├──→ W₂^Q, W₂^K, W₂^V → Head 2 (语义关系)
    ├──→ ...
    └──→ W₈^Q, W₈^K, W₈^V → Head 8 (位置关系)
                                │
                                ▼
                        Concat → W^O → 输出
```

---

## 4. Positional Encoding (位置编码)

### 4.1 问题：Self-Attention 的位置无关性

Self-Attention 是一个 **置换等变 (permutation equivariant)** 操作：打乱输入顺序，输出也会相应打乱，但不改变相对关系。这意味着模型无法区分 "猫吃鱼" 和 "鱼吃猫"。

### 4.2 正弦位置编码

Transformer 使用固定的正弦/余弦函数编码位置信息：

$$PE_{(pos, 2i)} = \sin\left(\frac{pos}{10000^{2i/d_{model}}}\right)$$

$$PE_{(pos, 2i+1)} = \cos\left(\frac{pos}{10000^{2i/d_{model}}}\right)$$

其中 $pos$ 是位置索引，$i$ 是维度索引。

### 4.3 为什么选择正弦编码？

1. **相对位置可表示**：对于任意固定偏移 $k$，$PE_{pos+k}$ 可以表示为 $PE_{pos}$ 的线性函数：

$$\sin(pos + k) = \sin(pos)\cos(k) + \cos(pos)\sin(k)$$
$$\cos(pos + k) = \cos(pos)\cos(k) - \sin(pos)\sin(k)$$

2. **外推能力**：模型可以泛化到训练中未见过的更长序列。

3. **不同频率**：不同维度使用不同频率的正弦波，类似于傅里叶变换，能够捕捉不同尺度的位置信息。

### 4.4 位置编码的添加

$$X_{input} = X_{token} + PE_{pos}$$

位置编码与 token embedding 维度相同，直接相加。

### 4.5 Learned vs Fixed 位置编码

| 特性 | Fixed (正弦) | Learned |
|------|--------------|---------|
| 外推能力 | 较好 | 较差 |
| 训练参数 | 无额外参数 | 需要学习 |
| 实验效果 | 相当 | 相当 |

原论文实验表明两种方式效果相似，但后来的研究 (如 RoPE, ALiBi) 发展了更先进的相对位置编码方法。

---

## 5. Encoder 架构

### 5.1 整体结构

Encoder 由 $N = 6$ 个相同的层堆叠而成。每层包含两个子层：

```
输入 X
    │
    ▼
┌─────────────────────────────┐
│  Multi-Head Self-Attention   │ ← 子层 1
│  (所有位置互相可见)           │
└─────────────────────────────┘
    │
    ├── Add & LayerNorm (残差连接)
    │
    ▼
┌─────────────────────────────┐
│  Feed-Forward Network        │ ← 子层 2
│  (position-wise)             │
└─────────────────────────────┘
    │
    ├── Add & LayerNorm (残差连接)
    │
    ▼
输出 (传递到下一层)
```

### 5.2 残差连接与 Layer Normalization

每个子层的输出为：

$$\text{SubLayerOutput} = \text{LayerNorm}(x + \text{SubLayer}(x))$$

**Layer Normalization** (不同于 Batch Normalization)：

$$\text{LN}(x) = \gamma \odot \frac{x - \mu}{\sqrt{\sigma^2 + \epsilon}} + \beta$$

其中 $\mu$ 和 $\sigma^2$ 是沿特征维度计算的均值和方差。

### 5.3 Pre-LN vs Post-LN

**Post-LN** (原论文)：
$$x_{out} = \text{LN}(x + \text{SubLayer}(x))$$

**Pre-LN** (后续改进，训练更稳定)：
$$x_{out} = x + \text{SubLayer}(\text{LN}(x))$$

Pre-LN 的优势在于梯度可以直接通过残差路径传播，不需要经过 LayerNorm，训练更加稳定。

### 5.4 Encoder 的 Self-Attention

在 Encoder 的 Self-Attention 中，Q、K、V 都来自同一层的输出，每个位置可以关注序列中的所有其他位置（包括自己）。

**注意力矩阵可视化**：

```
位置:  [The] [cat] [sat] [on] [mat]
The    [0.1] [0.5] [0.2] [0.1] [0.1]  ← "The" 主要关注 "cat"
cat    [0.3] [0.2] [0.3] [0.1] [0.1]  ← "cat" 关注多个位置
sat    [0.1] [0.3] [0.2] [0.2] [0.2]  ← "sat" 分散关注
on     [0.1] [0.1] [0.2] [0.3] [0.3]  ← "on" 关注 "mat"
mat    [0.1] [0.1] [0.3] [0.3] [0.2]  ← "mat" 关注 "sat" 和 "on"
```

---

## 6. Decoder 架构

### 6.1 三个子层

Decoder 每层包含三个子层：

```
输出 Y (shifted right)
    │
    ▼
┌─────────────────────────────────┐
│  Masked Multi-Head Self-Attention│ ← 子层 1
│  (只能看到已生成的 token)        │
└─────────────────────────────────┘
    │
    ├── Add & LayerNorm
    │
    ▼
┌─────────────────────────────────┐
│  Multi-Head Cross-Attention      │ ← 子层 2
│  Q: Decoder, K/V: Encoder 输出   │
└─────────────────────────────────┘
    │
    ├── Add & LayerNorm
    │
    ▼
┌─────────────────────────────────┐
│  Feed-Forward Network            │ ← 子层 3
└─────────────────────────────────┘
    │
    ├── Add & LayerNorm
    │
    ▼
输出
```

### 6.2 Masked Self-Attention (因果掩码)

在训练时，Decoder 需要并行处理整个目标序列，但必须保证自回归性质：位置 $i$ 只能关注位置 $\leq i$。

通过下三角掩码矩阵实现：

$$\text{Mask} = \begin{bmatrix} 0 & -\infty & -\infty & -\infty \\ 0 & 0 & -\infty & -\infty \\ 0 & 0 & 0 & -\infty \\ 0 & 0 & 0 & 0 \end{bmatrix}$$

$$\text{Attention}(Q, K, V) = \text{softmax}\left(\frac{QK^T + \text{Mask}}{\sqrt{d_k}}\right) V$$

$-\infty$ 经过 softmax 后变为 0，实现了因果掩码效果。

### 6.3 Cross-Attention (交叉注意力)

在 Cross-Attention 中：
- **Query (Q)**: 来自 Decoder 的上一层输出
- **Key (K) 和 Value (V)**: 来自 Encoder 的最终输出

这使得 Decoder 在生成每个 token 时都能"查看"整个输入序列。

---

## 7. Feed-Forward Network (FFN)

### 7.1 结构

每个 Encoder/Decoder 层都包含一个 Position-wise 的全连接前馈网络：

$$\text{FFN}(x) = \max(0, xW_1 + b_1)W_2 + b_2$$

```
输入 x ∈ ℝ^d_model
    │
    ▼
Linear (d_model → d_ff = 2048)  ← 扩展维度
    │
    ▼
ReLU 激活
    │
    ▼
Linear (d_ff → d_model)  ← 恢复维度
    │
    ▼
输出
```

### 7.2 参数量分析

$$\text{FFN 参数量} = d_{model} \times d_{ff} + d_{ff} + d_{ff} \times d_{model} + d_{model}$$
$$= 512 \times 2048 + 2048 + 2048 \times 512 + 512 \approx 2.1M$$

FFN 占据了 Transformer 中约 2/3 的参数量，是模型的"记忆存储"。

### 7.3 现代变体

后续研究发展了多种 FFN 变体：
- **Gated FFN (SwiGLU)**: $\text{FFN}(x) = (\text{Swish}(xW_1)) \odot (xW_2) \cdot W_3$
- **Mixture of Experts (MoE)**: 多个 FFN 专家，稀疏激活
- **DeepSeekMoE**: 更细粒度的专家划分

---

## 8. 训练细节

### 8.1 优化器

使用 Adam 优化器 ($\beta_1 = 0.9, \beta_2 = 0.98, \epsilon = 10^{-9}$)，配合学习率预热 (warmup) 和衰减调度：

$$lr = d_{model}^{-0.5} \cdot \min(step^{-0.5}, step \cdot warmup\_steps^{-1.5})$$

```
学习率
  │
  │      /\  ← 预热阶段 (线性增长)
  │     /  \
  │    /    \
  │   /      \___________  ← 衰减阶段 (平方根衰减)
  │  /
  │ /
  └────────────────────────→ 训练步数
       warmup_steps
```

预热步数 $warmup\_steps = 4000$。

### 8.2 正则化

1. **Residual Dropout**: 每个子层的输出在残差连接前应用 dropout，$P_{drop} = 0.1$

2. **Attention Dropout**: Attention 权重的 dropout，$P_{drop} = 0.1$

3. **Label Smoothing**: $\epsilon_{ls} = 0.1$

$$\mathcal{L} = (1 - \epsilon_{ls}) \cdot \mathcal{L}_{CE} + \frac{\epsilon_{ls}}{K} \sum_{i=1}^{K} \log p(y_i)$$

Label smoothing 使得模型不会过度自信，提高泛化能力。

### 8.3 训练资源

- **硬件**: 8 NVIDIA P100 GPUs
- **训练时间**: 
  - Base 模型: 12 小时 (100K steps)
  - Big 模型: 3.5 天 (300K steps)
- **数据**: WMT 2014 EN-DE (4.5M 句对), EN-FR (36M 句对)

---

## 9. 实验结果

### 9.1 机器翻译

| 模型 | EN-DE (BLEU) | EN-FR (BLEU) | 训练成本 (FLOPs) |
|------|--------------|--------------|------------------|
| LSTM + Attention | 24.6 | 38.1 | - |
| Transformer Base | 27.3 | 38.1 | $3.3 \times 10^{18}$ |
| Transformer Big | **28.4** | **41.8** | $2.3 \times 10^{19}$ |

### 9.2 消融实验 (Ablation Study)

关键发现：
1. 减少 Attention 头数量会显著降低性能
2. $d_k$ 过大或过小都不好
3. Learned position embedding 与 Sinusoidal 效果相当
4. Dropout 对防止过拟合至关重要

---

## 10. 模型架构图 (原文 Figure 1)

```
                    ┌─────────────────────────────────────┐
                    │            Transformer              │
                    │                                     │
                    │  ┌─────────────┐  ┌─────────────┐  │
                    │  │   Encoder   │  │   Decoder    │  │
                    │  │  (×N=6)     │  │  (×N=6)     │  │
                    │  │             │  │             │  │
                    │  │ ┌─────────┐ │  │ ┌─────────┐ │  │
                    │  │ │ Multi-  │ │  │ │ Masked   │ │  │
                    │  │ │ Head    │ │  │ │ Multi-   │ │  │
                    │  │ │ Self-   │ │  │ │ Head     │ │  │
                    │  │ │ Attn    │ │  │ │ Self-Attn│ │  │
                    │  │ └────┬────┘ │  │ └────┬────┘ │  │
                    │  │      │      │  │      │      │  │
                    │  │ Add & Norm   │  │ Add & Norm   │  │
                    │  │      │      │  │      │      │  │
                    │  │ ┌────┴────┐ │  │ ┌────┴────┐ │  │
                    │  │ │  FFN    │ │  │ │ Cross-  │ │  │
                    │  │ │         │ │  │ │ Attn    │ │  │
                    │  │ └────┬────┘ │  │ └────┬────┘ │  │
                    │  │      │      │  │      │      │  │
                    │  │ Add & Norm   │  │ Add & Norm   │  │
                    │  │      │      │  │      │      │  │
                    │  └──────┼──────┘  │ ┌────┴────┐ │  │
                    │         │         │ │  FFN    │ │  │
                    │         │         │ └────┬────┘ │  │
                    │         │         │      │      │  │
                    │         │         │ Add & Norm   │  │
                    │         │         └──────┼──────┘  │
                    │         │                │         │
                    │         └────────┬───────┘         │
                    │                  │                 │
                    └──────────────────┼─────────────────┘
                                       │
                                       ▼
                                  Linear + Softmax
                                       │
                                       ▼
                                  Output Probabilities
```

---

## 11. 深层数学分析

### 11.1 Self-Attention 的信息论视角

Self-Attention 可以看作是一种 **软性键值记忆 (soft key-value memory)**：

- 每个位置存储一个键值对 $(k_j, v_j)$
- Query $q_i$ 与所有键计算相似度
- 根据相似度对值进行加权求和

这种机制类似于 **核密度估计 (Kernel Density Estimation)**：

$$\text{Attention}(q, K, V) = \sum_j \frac{K(q, k_j)}{\sum_l K(q, k_l)} v_j$$

其中核函数 $K(q, k) = \exp(q^T k / \sqrt{d_k})$ 是 softmax 核。

### 11.2 Multi-Head 的表示能力

**定理**：Multi-Head Attention 可以表示任意的序列到序列映射（给定足够的头数和维度）。

**直觉**：每个头可以专注于一种特定的模式（如相邻词、远距离依赖、语法关系等），多个头的组合提供了丰富的表示能力。

### 11.3 与图神经网络的联系

Self-Attention 可以看作是 **全连接图上的消息传递**：

- 每个 token 是图的一个节点
- 注意力权重是边权重
- Value 是消息

这种视角将 Transformer 与 Graph Neural Network (GNN) 联系起来。

---

## 12. 历史影响与遗产

### 12.1 直接后继模型

Transformer 的成功催生了一系列重要模型：

1. **BERT (2018)**: 使用 Encoder 部分，双向上下文建模
2. **GPT 系列 (2018-)**: 使用 Decoder 部分，自回归语言建模
3. **T5 (2019)**: Encoder-Decoder 结构，统一文本到文本框架
4. **ViT (2020)**: 将 Transformer 应用于计算机视觉

### 12.2 架构变体

为解决 Transformer 的 $O(n^2)$ 复杂度问题，涌现了多种高效变体：

- **Sparse Attention**: Longformer, BigBird
- **Linear Attention**: Performer, Linear Transformer
- **State Space Models**: Mamba, S4

### 12.3 Scaling Laws

Transformer 的可扩展性使其成为 Large Language Model (LLM) 的基础架构：

- **参数量**: 从 65M (Base) 到 1.8T (GPT-4 估计)
- **训练数据**: 从几 GB 到数万亿 token
- **计算资源**: 从单 GPU 到数千 GPU 集群

---

## 13. 关键贡献总结

1. **证明了纯 Attention 架构的可行性**：无需循环或卷积即可实现 SOTA 性能
2. **高度并行化**：显著提升训练效率
3. **长距离依赖建模**：任意两个位置之间的路径长度为 $O(1)$
4. **通用架构**：不仅适用于 NLP，还可扩展到视觉、语音、多模态等领域

---

## 14. 延伸阅读

- **原始论文**: [arXiv:1706.03762](https://arxiv.org/abs/1706.03762)
- **The Illustrated Transformer**: Jay Alammar 的可视化讲解
- **Harvard NLP "The Annotated Transformer"**: 代码级复现
- **Attention 前身**: Bahdanau et al. (2014) [arXiv:1409.0473](https://arxiv.org/abs/1409.0473)
- **位置编码改进**: RoPE (Su et al., 2021), ALiBi (Press et al., 2022)

---

## 15. 常见问题

### Q1: 为什么不用 CNN 替代 Self-Attention？

CNN 的感受野是局部的，需要多层堆叠才能捕捉长距离依赖。而 Self-Attention 在单层内就能建立任意两个位置之间的直接连接。

### Q2: Self-Attention 的计算复杂度是多少？

$O(n^2 \cdot d)$，其中 $n$ 是序列长度，$d$ 是特征维度。这是 Transformer 处理长序列的主要瓶颈。

### Q3: Transformer 为什么能成功？

三个关键因素：
1. **并行化能力**：充分利用 GPU 计算资源
2. **长距离依赖**：直接建模任意距离的关系
3. **可扩展性**：性能随规模稳定提升

---

*最后更新: 2026-06-27*
