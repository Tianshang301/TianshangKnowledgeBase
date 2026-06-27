---
aliases: [序列建模与 Transformer]
tags: ['ArtificialIntelligence', 'NaturalLanguageProcessing', '序列建模与 Transformer']
---

# 序列建模与 Transformer

## 一、序列建模问题定义

序列建模是自然语言处理的核心任务，涉及对输入序列 $X = (x_1, x_2, \ldots, x_T)$ 进行编码、解码或转换。任务类型包括序列分类、序列标注、序列到序列生成等。序列建模面临的核心挑战包括：变长输入的处理、长距离依赖的捕获和序列内部结构关系的建模。

传统序列模型采用马尔可夫假设简化概率分解：

$$
P(x_1, x_2, \ldots, x_T) = \prod_{t=1}^T P(x_t | x_{t-1}, \ldots, x_{t-k})
$$

然而，固定阶数的马尔可夫假设无法捕获超过窗口 $k$ 的长距离依赖关系。

## 二、循环神经网络(RNN)

### 2.1 标准 RNN 架构

RNN 通过隐藏状态持续传递序列信息：

$$
h_t = \sigma(W_{xh}x_t + W_{hh}h_{t-1} + b_h)
$$

$$
y_t = \text{softmax}(W_{hy}h_t + b_y)
$$

其中 $h_t$ 是时间步 $t$ 的隐藏状态，编码了截至当前步的序列信息。RNN 的输出仅依赖于前序信息，形成因果结构。

### 2.2 梯度消失与爆炸

RNN 训练面临严重的梯度不稳定问题。时间反向传播(BPTT)计算梯度：

$$
\frac{\partial \mathcal{L}_T}{\partial \theta} = \sum_{t=1}^T \frac{\partial \mathcal{L}_T}{\partial h_T} \left( \prod_{k=t+1}^T \frac{\partial h_k}{\partial h_{k-1}} \right) \frac{\partial h_t}{\partial \theta}
$$

当时间步间隔增大时，连乘项中 $\frac{\partial h_k}{\partial h_{k-1}}$ 的谱半径若小于1则梯度消失，若大于1则梯度爆炸。

### 2.3 LSTM 与 GRU

LSTM 通过门控机制缓解梯度问题：

- **遗忘门** $f_t = \sigma(W_f \cdot [h_{t-1}, x_t] + b_f)$
- **输入门** $i_t = \sigma(W_i \cdot [h_{t-1}, x_t] + b_i)$
- **候选状态** $\tilde{C}_t = \tanh(W_C \cdot [h_{t-1}, x_t] + b_C)$
- **细胞状态更新** $C_t = f_t \odot C_{t-1} + i_t \odot \tilde{C}_t$
- **输出门** $o_t = \sigma(W_o \cdot [h_{t-1}, x_t] + b_o)$
- **隐藏状态** $h_t = o_t \odot \tanh(C_t)$

GRU 将遗忘门和输入门合并为更新门，结构更简洁。

| 组件 | RNN | LSTM | GRU | Transformer |
|------|-----|------|-----|-------------|
| 并行性 | 无 | 无 | 无 | 完全 |
| 长程依赖 | 差 | 良好 | 良好 | 优秀 |
| 参数量 | 最少 | 较多 | 中等 | 最多 |
| 训练速度 | 慢 | 慢 | 慢 | 快(可并行) |

## 三、注意力机制

### 3.1 Bahdanau 注意力

在编码器-解码器框架中引入注意力，使解码器能在每个时间步关注编码器的不同位置：

$$
e_{ij} = v_a^T \tanh(W_a s_{i-1} + U_a h_j)
$$

$$
\alpha_{ij} = \frac{\exp(e_{ij})}{\sum_{k=1}^{T_x} \exp(e_{ik})}
$$

$$
c_i = \sum_{j=1}^{T_x} \alpha_{ij} h_j
$$

其中 $s_{i-1}$ 是解码器前一时刻状态，$h_j$ 是编码器第 $j$ 时刻状态。

### 3.2 Luong 注意力

Luong 提出了两种更高效的计算方式：

- **全局注意力**：对所有编码器状态计算注意力分布
- **局部注意力**：先预测对齐位置，再在窗口内计算注意力

评分函数包括：$\text{score}(s_t, h_i) = s_t^T h_i$ (点积), $s_t^T W_a h_i$ (一般), $v_a^T \tanh(W_a[s_t; h_i])$ (拼接)

## 四、Transformer 架构

### 4.1 缩放点积注意力

$$
\text{Attention}(Q, K, V) = \text{softmax}\left(\frac{QK^T}{\sqrt{d_k}}\right)V
$$

缩放因子 $\sqrt{d_k}$ 防止点积结果随维度增长过大导致 softmax 梯度消失。

### 4.2 多头注意力

多头机制允许模型在不同子空间捕获不同类型的依赖关系：

$$
\text{MultiHead}(Q, K, V) = \text{Concat}(\text{head}_1, \ldots, \text{head}_h)W^O
$$

$$
\text{head}_i = \text{Attention}(QW_i^Q, KW_i^K, VW_i^V)
$$

### 4.3 位置编码

由于自注意力运算不包含位置信息，Transformer 通过位置编码注入位置信号：

**正弦位置编码**：
$$
PE_{(pos, 2i)} = \sin\left(\frac{pos}{10000^{2i/d_{\text{model}}}}\right)
$$
$$
PE_{(pos, 2i+1)} = \cos\left(\frac{pos}{10000^{2i/d_{\text{model}}}}\right)
$$

**可学习位置编码**：将位置索引映射为可训练嵌入向量，灵活性更好。

### 4.4 编码器-解码器结构

**编码器层**包含多头自注意力和前馈网络，每个子层后接残差连接和层归一化：

$$
\text{FFN}(x) = \max(0, xW_1 + b_1)W_2 + b_2
$$

**解码器层**在编码器结构基础上增加遮蔽多头自注意力(防止看到未来信息)和交叉注意力(关注编码器输出)。

## 五、Transformer 的扩展与变体

### 5.1 高效注意力

标准自注意力的复杂度为 $O(T^2)$，限制了长序列处理。改进方法包括：

- **稀疏注意力**：如 Longformer 的滑动窗口+全局注意力模式
- **线性注意力**：使用核方法将复杂度降至 $O(T)$
- **FlashAttention**：通过 IO 感知的精确注意力计算，利用分块和重计算减少显存占用

### 5.2 预训练 Transformer

| 模型 | 架构 | 预训练任务 | 特点 |
|------|------|-----------|------|
| BERT | 编码器 | MLM + NSP | 双向上下文 |
| GPT | 解码器 | 自回归 LM | 生成能力强 |
| T5 | 编码器-解码器 | Span Corruption | 统一框架 |
| RoBERTa | 编码器 | MLM(改进) | 更充分训练 |
| XLNet | 编码器 | PLM | 自回归+双向 |

## 六、前沿发展

Transformer 架构的最新进展包括：混合专家(MoE)层以在扩大参数规模时控制计算成本、FlashAttention 系列提升训练和推理效率、以及状态空间模型(Mamba)等替代架构的出现。旋转位置编码(RoPE)和分组查询注意力(GQA)已成为大语言模型的标准配置。

## 相关条目

- RNN
- Attention
- Transformer
- BERT
- GPT

## 参考资源

1. Hochreiter, S., Schmidhuber, J. "Long Short-Term Memory." Neural Computation, 1997.
2. Bahdanau, D., et al. "Neural Machine Translation by Jointly Learning to Align and Translate." ICLR, 2015.
3. Vaswani, A., et al. "Attention Is All You Need." NeurIPS, 2017.
4. Devlin, J., et al. "BERT: Pre-training of Deep Bidirectional Transformers." NAACL, 2019.
5. Radford, A., et al. "Improving Language Understanding by Generative Pre-Training." 2018.
6. Raffel, C., et al. "Exploring the Limits of Transfer Learning with a Unified Text-to-Text Transformer." JMLR, 2020.
7. Brown, T., et al. "Language Models are Few-Shot Learners." NeurIPS, 2020.
8. Dao, T., et al. "FlashAttention: Fast and Memory-Efficient Exact Attention." NeurIPS, 2022.
