---
aliases:
  - RNN
  - LSTM
  - GRU
  - Recurrent Neural Network
  - Long Short-Term Memory
tags:
  - deep-learning
  - rnn
  - lstm
  - sequence-modeling
  - neural-network-architecture
  - pre-transformer
created: 2026-06-27
updated: 2026-06-27
---

# RNN 与 LSTM 架构

> **核心论文**:
> - Hochreiter S, Schmidhuber J. "Long Short-Term Memory." *Neural Computation*, 1997.
> - Cho K, et al. "Learning Phrase Representations using RNN Encoder-Decoder for Statistical Machine Translation." *EMNLP 2014*. arXiv:1406.1078

---

## 1. 历史背景

### 1.1 序列建模的需求

自然语言、语音、时间序列等数据本质上是序列化的。传统的前馈神经网络 (Feed-Forward Neural Network) 无法处理变长序列，也无法捕捉序列中的时序依赖关系。

### 1.2 早期尝试

- **Jordan Network (1986)**: 将输出反馈到输入
- **Elman Network (1990)**: 将隐状态反馈到输入

这些早期循环网络奠定了 Recurrent Neural Network 的基础。

---

## 2. Vanilla RNN

### 2.1 基本结构

Vanilla RNN 通过隐状态 (hidden state) $h_t$ 在时间步之间传递信息：

$$h_t = \tanh(W_{hh} h_{t-1} + W_{xh} x_t + b_h)$$

$$y_t = W_{hy} h_t + b_y$$

其中：
- $x_t \in \mathbb{R}^{d_x}$: 时间步 $t$ 的输入
- $h_t \in \mathbb{R}^{d_h}$: 时间步 $t$ 的隐状态
- $y_t \in \mathbb{R}^{d_y}$: 时间步 $t$ 的输出
- $W_{hh} \in \mathbb{R}^{d_h \times d_h}$: 隐状态到隐状态的权重
- $W_{xh} \in \mathbb{R}^{d_h \times d_x}$: 输入到隐状态的权重
- $W_{hy} \in \mathbb{R}^{d_y \times d_h}$: 隐状态到输出的权重

### 2.2 计算图展开

```
时间步:   t-1          t           t+1
          │            │            │
          ▼            ▼            ▼
        ┌───┐        ┌───┐        ┌───┐
h_{t-1}→│   │  h_t   →│   │ h_{t+1}→│   │
        │ RNN│────────│RNN│────────│RNN│
        │Cell│        │Cell│        │Cell│
        └───┘        └───┘        └───┘
          ▲            ▲            ▲
          │            │            │
        x_{t-1}      x_t         x_{t+1}
```

### 2.3 参数共享

RNN 在所有时间步共享相同的参数 ($W_{hh}, W_{xh}, W_{hy}$)，这使得：
1. 模型可以处理任意长度的序列
2. 参数量与序列长度无关
3. 在不同位置学习相同的模式

### 2.4 通过时间的反向传播 (BPTT)

训练 RNN 使用 BPTT 算法。对于损失函数 $\mathcal{L} = \sum_{t=1}^{T} \mathcal{L}_t$：

$$\frac{\partial \mathcal{L}}{\partial W_{hh}} = \sum_{t=1}^{T} \frac{\partial \mathcal{L}_t}{\partial W_{hh}}$$

关键的梯度链：

$$\frac{\partial h_t}{\partial h_{t-1}} = \text{diag}(1 - h_t^2) W_{hh}$$

从时间步 $t$ 到时间步 $k$ 的梯度：

$$\frac{\partial h_t}{\partial h_k} = \prod_{i=k+1}^{t} \frac{\partial h_i}{\partial h_{i-1}} = \prod_{i=k+1}^{t} \text{diag}(1 - h_i^2) W_{hh}$$

---

## 3. 梯度消失与爆炸问题

### 3.1 问题分析

由于梯度是矩阵乘积的连乘，设 $\|W_{hh}\| = \lambda$：

$$\left\|\frac{\partial h_t}{\partial h_k}\right\| \approx \lambda^{t-k}$$

- 当 $\lambda > 1$：梯度指数增长 → **梯度爆炸**
- 当 $\lambda < 1$：梯度指数衰减 → **梯度消失**

### 3.2 直观理解

```
梯度流动:

时间步 1 ──→ 时间步 2 ──→ ... ──→ 时间步 100
   │            │                      │
   └────────────┴──────────────────────┘
        梯度需要经过 99 次矩阵乘法
        
如果每次乘法使梯度缩小 0.9:
最终梯度 = 0.9^99 ≈ 0.00005 (几乎为零)
```

### 3.3 后果

1. **长距离依赖无法学习**: 模型只能学习短期模式
2. **训练不稳定**: 梯度爆炸导致参数更新过大
3. **收敛困难**: 优化景观极其复杂

### 3.4 解决方案 (LSTM 之前)

1. **梯度裁剪 (Gradient Clipping)**:
$$g \leftarrow \frac{g}{\|g\|} \cdot \text{threshold} \quad \text{if } \|g\| > \text{threshold}$$

2. **小心初始化**: 正交初始化、稀疏初始化

3. **ReLU 激活**: 避免 tanh 的饱和区

这些方法只能缓解，无法根本解决问题。

---

## 4. LSTM (Long Short-Term Memory)

### 4.1 核心设计思想

Hochreiter 和 Schmidhuber 在 1997 年提出了 LSTM，其核心创新是引入 **Cell State (细胞状态)** $c_t$ 作为信息的"高速公路"。

**关键洞察**：通过加法操作（而非乘法操作）传递梯度，避免梯度消失。

### 4.2 LSTM 的三个门

LSTM 使用三个门来控制信息流：

1. **Forget Gate (遗忘门)**: 决定丢弃哪些旧信息
2. **Input Gate (输入门)**: 决定存储哪些新信息
3. **Output Gate (输出门)**: 决定输出哪些信息

### 4.3 完整数学公式

**Forget Gate**:
$$f_t = \sigma(W_f \cdot [h_{t-1}, x_t] + b_f)$$

**Input Gate**:
$$i_t = \sigma(W_i \cdot [h_{t-1}, x_t] + b_i)$$

**候选细胞状态**:
$$\tilde{c}_t = \tanh(W_c \cdot [h_{t-1}, x_t] + b_c)$$

**Cell State 更新** (核心):
$$c_t = f_t \odot c_{t-1} + i_t \odot \tilde{c}_t$$

**Output Gate**:
$$o_t = \sigma(W_o \cdot [h_{t-1}, x_t] + b_o)$$

**Hidden State 输出**:
$$h_t = o_t \odot \tanh(c_t)$$

其中 $\odot$ 表示逐元素乘法 (Hadamard product)，$\sigma$ 是 sigmoid 函数。

### 4.4 LSTM 结构图

```
        ┌───────────────────────────────────────────────────┐
        │                    Cell State                      │
        │                     c_{t-1}                        │
        │                       │                            │
        │          ┌────────────┼────────────┐              │
        │          │    ×       │            │              │
        │          │ (forget)   │            │              │
        │          │            │            │              │
        │          │            ▼            │              │
        │          │      ┌─────────┐       │              │
        │          │      │   +     │       │              │
        │          │      └────┬────┘       │              │
        │          │           │            │              │
        │          │           ▼            │              │
        │          │         c_t            │              │
        │          │           │            │              │
        │          │      ┌────┴────┐       │              │
        │          │      │  tanh   │       │              │
        │          │      └────┬────┘       │              │
        │          │           │            │              │
        │          │      × (output)        │              │
        │          │           │            │              │
        │          │           ▼            │              │
        │          │         h_t            │              │
        └──────────┴───────────┴────────────┘              │
                                                           │
    输入: x_t ─┬───────────────────────────────────────────┘
               │
        ┌──────┼──────┬──────┐
        │      │      │      │
        ▼      ▼      ▼      ▼
      forget  input  candidate output
       gate    gate    tanh    gate
        │      │      │       │
        ▼      ▼      ▼       ▼
       f_t    i_t    c̃_t     o_t
```

### 4.5 为什么 LSTM 能解决梯度消失？

Cell State 的更新是 **加法操作**：

$$c_t = f_t \odot c_{t-1} + i_t \odot \tilde{c}_t$$

梯度通过 Cell State 传播时：

$$\frac{\partial c_t}{\partial c_{t-1}} = f_t$$

当 $f_t \approx 1$ 时，梯度可以无损传播！这与 Vanilla RNN 的矩阵乘法形成鲜明对比。

**数学证明**：

从时间步 $t$ 到时间步 $k$：

$$\frac{\partial c_t}{\partial c_k} = \prod_{i=k+1}^{t} f_i$$

只要 forget gate 保持接近 1，梯度就不会消失。

### 4.6 LSTM 的门控直觉

| 门 | 值范围 | 作用 | 直觉 |
|----|--------|------|------|
| Forget Gate $f_t$ | (0, 1) | 控制旧信息保留程度 | "忘记不重要的历史" |
| Input Gate $i_t$ | (0, 1) | 控制新信息写入程度 | "记住重要的新信息" |
| Output Gate $o_t$ | (0, 1) | 控制信息输出程度 | "输出相关的信息" |

---

## 5. GRU (Gated Recurrent Unit)

### 5.1 设计动机

Cho et al. (2014) 提出 GRU 作为 LSTM 的简化版本，减少参数量的同时保持性能。

### 5.2 GRU 的数学公式

**Update Gate (更新门)**:
$$z_t = \sigma(W_z \cdot [h_{t-1}, x_t] + b_z)$$

**Reset Gate (重置门)**:
$$r_t = \sigma(W_r \cdot [h_{t-1}, x_t] + b_r)$$

**候选隐状态**:
$$\tilde{h}_t = \tanh(W \cdot [r_t \odot h_{t-1}, x_t] + b)$$

**隐状态更新**:
$$h_t = (1 - z_t) \odot h_{t-1} + z_t \odot \tilde{h}_t$$

### 5.3 GRU 结构图

```
输入: x_t, h_{t-1}
         │
    ┌────┼────┐
    │    │    │
    ▼    ▼    ▼
  reset update │
   gate  gate  │
    │    │    │
    ▼    ▼    ▼
   r_t  z_t   │
    │    │    │
    │    │    ▼
    │    │  candidate h̃_t
    │    │    │
    │    └────┼────┐
    │         │    │
    ▼         ▼    ▼
  (1-z)⊙h_{t-1}  z⊙h̃_t
         │         │
         └────┬────┘
              │
              ▼
            h_t
```

### 5.4 LSTM vs GRU 对比

| 特性 | LSTM | GRU |
|------|------|-----|
| 门的数量 | 3 (forget, input, output) | 2 (update, reset) |
| 参数量 | $12 \cdot d_h^2$ (近似) | $9 \cdot d_h^2$ (近似) |
| Cell State | 显式 $c_t$ | 隐式 (与 $h_t$ 合并) |
| 性能 | 长序列表现更好 | 短序列相当 |
| 训练速度 | 较慢 | 较快 |

### 5.5 选择建议

- **长序列 (>100 步)**: 优先选择 LSTM
- **短序列或资源受限**: 优先选择 GRU
- **实际应用**: 差异通常不大，需要实验验证

---

## 6. RNN 的变体与扩展

### 6.1 Bidirectional RNN (双向 RNN)

单向 RNN 只能看到过去的信息，但在很多任务中，未来的信息同样重要。

**结构**:
```
前向 RNN:  x_1 → h_1 → h_2 → ... → h_T
后向 RNN:  x_T ← h_T ← h_{T-1} ← ... ← h_1

输出: y_t = [h_t_forward; h_t_backward]
```

**数学形式**:
$$\vec{h}_t = \text{RNN}_{forward}(x_t, \vec{h}_{t-1})$$
$$\overleftarrow{h}_t = \text{RNN}_{backward}(x_t, \overleftarrow{h}_{t+1})$$
$$h_t = [\vec{h}_t; \overleftarrow{h}_t]$$

**应用**: 命名实体识别、情感分析、BERT 的前身

### 6.2 Deep RNN (深层 RNN)

堆叠多个 RNN 层，每层的输出作为下一层的输入：

$$h_t^{(l)} = \text{RNN}^{(l)}(h_t^{(l-1)}, h_{t-1}^{(l)})$$

```
层 3:  h_t^(3) ←→ h_{t+1}^(3)
          ↑
层 2:  h_t^(2) ←→ h_{t+1}^(2)
          ↑
层 1:  h_t^(1) ←→ h_{t+1}^(1)
          ↑
输入:   x_t       x_{t+1}
```

通常使用残差连接防止梯度消失：

$$h_t^{(l)} = \text{RNN}^{(l)}(h_t^{(l-1)}, h_{t-1}^{(l)}) + h_t^{(l-1)}$$

### 6.3 Encoder-Decoder 架构

Sutskever et al. (2014) 提出的 Seq2Seq 架构：

```
Encoder (编码器):
┌─────────────────────────────────────┐
│ RNN 逐步处理输入序列                │
│ x_1 → x_2 → ... → x_n              │
│                ↓                    │
│              context vector c       │
└─────────────────────────────────────┘
                    │
                    ▼
Decoder (解码器):
┌─────────────────────────────────────┐
│ 以 c 为初始状态，逐步生成输出        │
│ c → y_1 → y_2 → ... → y_m          │
└─────────────────────────────────────┘
```

**数学形式**:
- Encoder: $h_n = \text{RNN}_{enc}(x_1, x_2, ..., x_n)$
- Decoder: $y_t = \text{RNN}_{dec}(y_{t-1}, s_{t-1}, c)$，其中 $c = h_n$

**信息瓶颈问题**: 整个输入序列被压缩到固定长度的向量 $c$ 中，这是后来 Attention 机制出现的直接动机。

---

## 7. RNN 的训练技巧

### 7.1 梯度裁剪

防止梯度爆炸的常用方法：

```python
# 按范数裁剪
if torch.norm(grad) > threshold:
    grad = grad * threshold / torch.norm(grad)
```

### 7.2 梯度裁剪的数学形式

$$g \leftarrow \begin{cases} g & \text{if } \|g\| \leq \theta \\ \frac{\theta}{\|g\|} g & \text{if } \|g\| > \theta \end{cases}$$

### 7.3 Teacher Forcing

训练时使用真实标签作为下一步输入，而非模型预测：

$$\hat{y}_t = \text{Decoder}(y_{t-1}^{*}, s_t)$$

其中 $y_{t-1}^{*}$ 是真实标签。

**问题**: 训练和推理时的输入分布不一致 (Exposure Bias)。

### 7.4 Dropout 策略

RNN 的 Dropout 不能直接应用于时间维度，常用方法：

1. **Variational Dropout**: 所有时间步使用相同的 Dropout mask
2. **Recurrent Dropout**: 只在非循环连接上应用

---

## 8. RNN 的应用

### 8.1 语言模型

预测下一个词的概率：

$$P(x_t | x_1, ..., x_{t-1}) = \text{softmax}(W_h h_t + b)$$

### 8.2 机器翻译 (Seq2Seq)

Encoder-Decoder 架构 + Attention 机制 (Bahdanau et al., 2014)

### 8.3 语音识别

Deep Bidirectional LSTM + CTC Loss

### 8.4 时间序列预测

股票价格、天气、传感器数据等

---

## 9. RNN 的局限性

### 9.1 顺序计算瓶颈

```
Vanilla RNN:
时间步 1 → 时间步 2 → 时间步 3 → ... → 时间步 T
   ↑           ↑           ↑              ↑
必须顺序计算，无法并行
```

这使得 RNN 无法充分利用 GPU 的并行计算能力。

### 9.2 长距离依赖

即使 LSTM 缓解了梯度消失问题，对于非常长的序列 (>1000 步)，仍然难以学习远距离依赖。

### 9.3 与 Transformer 的对比

| 特性 | RNN/LSTM | Transformer |
|------|----------|-------------|
| 并行性 | 低 (顺序计算) | 高 (并行计算) |
| 长距离依赖 | 困难 | 容易 ($O(1)$ 路径) |
| 内存 | $O(1)$ (隐状态) | $O(n)$ (所有位置) |
| 训练效率 | 慢 | 快 |
| 推理效率 | $O(1)$ 每步 | $O(n)$ 每步 |

---

## 10. 关键论文列表

1. **Elman J L. "Finding structure in time." *Cognitive Science*, 1990.**
   - 提出 Elman Network，奠定了 RNN 的基础

2. **Hochreiter S, Schmidhuber J. "Long Short-Term Memory." *Neural Computation*, 1997.**
   - 提出 LSTM，解决梯度消失问题

3. **Cho K, et al. "Learning Phrase Representations using RNN Encoder-Decoder for Statistical Machine Translation." *EMNLP 2014*.**
   - 提出 GRU 和 Encoder-Decoder 架构

4. **Bahdanau D, et al. "Neural Machine Translation by Jointly Learning to Align and Translate." *ICLR 2015*.**
   - 引入 Attention 机制

5. **Sutskever I, et al. "Sequence to Sequence Learning with Neural Networks." *NeurIPS 2014*.**
   - 提出 Seq2Seq 架构

6. **Graves A. "Generating Sequences with Recurrent Neural Networks." *arXiv:1308.0850*, 2013.**
   - RNN 在序列生成中的应用

---

## 11. 从 RNN 到 Transformer

### 11.1 Attention 机制的萌芽

Bahdanau Attention (2014) 引入了注意力机制，但仍依赖 RNN 作为基础架构。

### 11.2 Self-Attention 的出现

2016-2017 年，研究者开始探索 Self-Attention 作为 RNN 的替代：
- **Parikh et al. (2016)**: Decomposable Attention Model
- **Cheng et al. (2016)**: Long Short-Term Memory-Networks

### 11.3 Transformer 的革命

Vaswani et al. (2017) 的 "Attention Is All You Need" 证明了：
1. 纯 Attention 架构可行
2. 性能优于 RNN
3. 训练效率大幅提升

### 11.4 历史意义

RNN/LSTM 是深度学习历史上的重要里程碑：
1. 证明了神经网络可以处理序列数据
2. 开创了 NLP 的深度学习时代
3. Attention 机制的前身
4. 为 Transformer 的出现奠定了基础

---

## 12. 现代应用中的 RNN

虽然 Transformer 已成为主流，但 RNN 仍在某些场景中使用：

1. **实时流处理**: RNN 可以逐 token 处理，无需缓存整个序列
2. **资源受限环境**: RNN 参数量更小
3. **时间序列**: 某些时间序列任务中 RNN 表现仍然良好

State Space Models (如 Mamba) 结合了 RNN 和 Transformer 的优点，是当前的研究热点。

---

*最后更新: 2026-06-27*
