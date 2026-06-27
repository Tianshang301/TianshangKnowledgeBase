---
aliases:
  - GPT
  - GPT-1
  - GPT-2
  - GPT-3
  - GPT-4
  - Scaling Laws
  - Large Language Model
  - LLM
tags:
  - deep-learning
  - gpt
  - llm
  - scaling-laws
  - transformer
  - neural-network-architecture
created: 2026-06-27
updated: 2026-06-27
---

# GPT 系列与 Scaling Laws

> **核心论文**:
> - Radford A, et al. "Improving Language Understanding by Generative Pre-Training." *OpenAI*, 2018. (GPT-1)
> - Radford A, et al. "Language Models are Unsupervised Multitask Learners." *OpenAI*, 2019. (GPT-2)
> - Brown T, et al. "Language Models are Few-Shot Learners." *NeurIPS 2020*. arXiv:2005.14165 (GPT-3)
> - Kaplan J, et al. "Scaling Laws for Neural Language Models." *arXiv:2001.08361*, 2020.

---

## 1. 历史背景

### 1.1 预训练的兴起

2018 年前后，NLP 领域出现了两种预训练范式：

1. **判别式预训练**: ELMo, BERT 等，学习上下文表示
2. **生成式预训练**: GPT 系列，学习语言模型

### 1.2 GPT 的设计哲学

OpenAI 的 GPT 系列坚持一个核心信念：

> **通过预测下一个词 (next token prediction)，模型可以学习到世界的知识。**

这种简洁的目标函数，配合大规模数据和计算，催生了强大的语言模型。

---

## 2. GPT-1 (2018)

### 2.1 论文信息

- **标题**: "Improving Language Understanding by Generative Pre-Training"
- **作者**: Alec Radford, Karthik Narasimhan, Tim Salimans, Ilya Sutskever
- **机构**: OpenAI

### 2.2 核心思想

**两阶段训练范式**:

```
阶段 1: 无监督预训练 (Unsupervised Pre-training)
    ↓
使用大规模无标注文本训练语言模型
    ↓
阶段 2: 有监督微调 (Supervised Fine-tuning)
    ↓
使用下游任务标注数据微调
```

### 2.3 预训练目标

标准的语言模型目标：

$$\mathcal{L}_{PT}(\theta) = \sum_{i} \log P(u_i | u_{i-k}, ..., u_{i-1}; \theta)$$

其中 $u_i$ 是文本序列中的第 i 个 token，$k$ 是上下文窗口大小。

### 2.4 模型架构

GPT-1 使用 Transformer Decoder (12 层):

```
参数量: 117M
层数: 12
隐藏维度: 768
Attention 头数: 12
上下文长度: 512 tokens
词汇表大小: 40,000 (BPE)
```

**架构细节**:
- 使用 Masked Multi-Head Self-Attention (因果掩码)
- Feed-Forward Network: 768 → 3072 → 768
- 激活函数: GELU (Gaussian Error Linear Unit)

$$\text{GELU}(x) = x \cdot \Phi(x) \approx 0.5x\left(1 + \tanh\left[\sqrt{2/\pi}(x + 0.044715x^3)\right]\right)$$

### 2.5 微调策略

在预训练模型顶部添加任务特定的分类头：

```
输入: [START] token_1 token_2 ... token_n [EXTRACT]
                │
                ▼
        Transformer Decoder (12层)
                │
                ▼
        取 [EXTRACT] 位置的隐藏状态 h_n
                │
                ▼
        线性分类器: P(y|h_n) = softmax(W_y h_n + b_y)
```

**微调损失**:

$$\mathcal{L}_{FT}(\theta) = \mathcal{L}_{PT}(\theta) + \lambda \cdot \mathcal{L}_{CLF}(\theta)$$

其中 $\lambda$ 是辅助语言模型损失的权重。

### 2.6 实验结果

在 12 个 NLP 基准测试中，GPT-1 在 9 个上取得了 SOTA：

| 任务 | 数据集 | GPT-1 结果 |
|------|--------|-----------|
| 自然语言推理 | MNLI | 82.1% |
| 问答 | RACE | 72.8% |
| 语义相似度 | QQP | 70.3% |
| 文本分类 | SST-2 | 91.3% |

### 2.7 历史意义

GPT-1 证明了：
1. 无监督预训练可以学习通用语言表示
2. Transformer Decoder 是有效的预训练架构
3. 预训练 + 微调范式的成功

---

## 3. GPT-2 (2019)

### 3.1 论文信息

- **标题**: "Language Models are Unsupervised Multitask Learners"
- **作者**: Alec Radford, Jeffrey Wu, Rewon Child, David Luan, Dario Amodei, Ilya Sutskever
- **机构**: OpenAI
- **争议**: "Too dangerous to release"

### 3.2 核心创新：Zero-shot Learning

GPT-2 的关键洞察：

> **语言模型已经在做多任务学习！**

例如，翻译任务可以表示为：

```
输入: "translate English to French: cheese =>"
期望输出: "fromage"
```

模型无需显式微调，只需通过适当的 prompt 格式化，就能执行各种任务。

### 3.3 模型规模

GPT-2 有四个版本：

| 版本 | 参数量 | 层数 | 隐藏维度 | 上下文长度 |
|------|--------|------|----------|-----------|
| Small | 117M | 12 | 768 | 1024 |
| Medium | 345M | 24 | 1024 | 1024 |
| Large | 762M | 36 | 1280 | 1024 |
| XL | 1.5B | 48 | 1600 | 1024 |

### 3.4 训练数据：WebText

- 从 Reddit 抓取高质量网页 (≥3 karma)
- 约 40GB 文本
- 800 万个网页
- 覆盖多种领域和任务格式

### 3.5 架构改进

1. **Pre-Layer Normalization**: 将 Layer Normalization 移到每个子层的输入处

$$x_{out} = x + \text{SubLayer}(\text{LN}(x))$$

2. **残差路径初始化**: 缩放残差层权重 $1/\sqrt{N}$，其中 N 是层数

3. **更大的词汇表**: 50,257 tokens (BPE)

### 3.6 Zero-shot 能力

GPT-2 在没有微调的情况下，通过适当的 prompt 实现了多种任务：

| 任务 | Prompt 格式 | 性能 |
|------|------------|------|
| 翻译 | "translate English to French: X =>" | 接近有监督 |
| 问答 | "Q: ... A:" | 合理 |
| 摘要 | "Article: ... TL;DR:" | 有意义 |
| 生成 | 任意前缀 | 流畅 |

### 3.7 伦理争议

OpenAI 最初决定不公开完整模型，理由是：
- 可能被用于生成虚假新闻
- 可能被用于垃圾邮件生成
- 滥用风险

这一决定引发了关于 AI 开放性的广泛讨论。

---

## 4. GPT-3 (2020)

### 4.1 论文信息

- **标题**: "Language Models are Few-Shot Learners"
- **作者**: Tom Brown et al.
- **机构**: OpenAI
- **发表**: NeurIPS 2020
- **引用量**: 30,000+

### 4.2 核心创新：In-context Learning

GPT-3 引入了 **In-context Learning** 的概念：

```
Zero-shot:  只给任务描述
One-shot:   任务描述 + 1 个示例
Few-shot:   任务描述 + 几个示例

示例 (Few-shot):
    Translate English to French:
    sea otter => loutre de mer
    peppermint => menthe poivrée
    cheese => [模型生成: fromage]
```

**关键发现**: 不需要更新参数，只需在 prompt 中提供示例，模型就能"学习"新任务。

### 4.3 模型规模

GPT-3 有多个版本，最大版本参数量达到 175B：

| 版本 | 参数量 | 层数 | 隐藏维度 | 注意力头数 | 上下文长度 |
|------|--------|------|----------|-----------|-----------|
| Small | 125M | 12 | 768 | 12 | 2048 |
| Medium | 350M | 24 | 1024 | 16 | 2048 |
| Large | 760M | 24 | 1536 | 16 | 2048 |
| XL | 1.3B | 24 | 2048 | 32 | 2048 |
| 2.7B | 2.7B | 32 | 2560 | 32 | 2048 |
| 6.7B | 6.7B | 32 | 4096 | 32 | 2048 |
| 13B | 13B | 40 | 5140 | 40 | 2048 |
| **175B** | **175B** | 96 | 12288 | 96 | 2048 |

### 4.4 训练细节

**数据集**:
- Common Crawl (60%)
- WebText2 (22%)
- Books1 (8%)
- Books3 (8%)
- Wikipedia (3%)

总 token 数: 约 300B tokens

**训练资源**:
- 硬件: 数千个 V100 GPU
- 训练时间: 约 3-4 周
- 训练成本: 估计 $4.6M - $12M

**优化器**: Adam ($\beta_1 = 0.9, \beta_2 = 0.95$)

**学习率调度**:
$$lr = \begin{cases} lr_{max} \cdot \frac{step}{warmup} & \text{if } step < warmup \\ lr_{max} \cdot \frac{1}{\sqrt{step}} & \text{otherwise} \end{cases}$$

### 4.5 In-context Learning 的形式化

给定 k 个示例 $(x_1, y_1), ..., (x_k, y_k)$ 和查询 $x_{query}$:

$$P(y_{query} | x_1, y_1, ..., x_k, y_k, x_{query})$$

模型通过条件概率隐式地"学习"了任务。

### 4.6 涌现能力 (Emergent Abilities)

随着模型规模增大，出现了小模型不具备的能力：

1. **多步推理**: 复杂逻辑推理
2. **代码生成**: 生成可执行代码
3. **数学**: 解决数学问题
4. **翻译**: 高质量机器翻译
5. **问答**: 开放域问答

### 4.7 Few-shot 性能

GPT-3 在多个基准测试上的表现：

| 任务 | Zero-shot | One-shot | Few-shot | 微调 SOTA |
|------|-----------|----------|----------|-----------|
| TriviaQA | 64.3% | 68.0% | 71.2% | 72.5% |
| HellaSwag | 78.1% | 78.6% | 79.3% | 85.6% |
| LAMBADA | 76.2% | 80.7% | 86.4% | 68.0% |
| StoryCloze | 77.2% | 77.7% | 83.2% | 84.7% |

### 4.8 局限性

1. **重复生成**: 长文本生成时容易重复
2. **常识推理**: 仍然存在困难
3. **事实准确性**: 会产生"幻觉"
4. **计算成本**: 推理成本高昂

---

## 5. Scaling Laws (2020)

### 5.1 论文信息

- **标题**: "Scaling Laws for Neural Language Models"
- **作者**: Jared Kaplan, Sam McCandlish, Tom Henighan et al.
- **机构**: OpenAI
- **意义**: 为 LLM 的发展提供了理论指导

### 5.2 核心发现

**幂律关系**: 模型性能 (loss) 与模型规模、数据量、计算量呈幂律关系。

$$L(N) = \left(\frac{N_c}{N}\right)^{\alpha_N}, \quad \alpha_N \approx 0.076$$

$$L(D) = \left(\frac{D_c}{D}\right)^{\alpha_D}, \quad \alpha_D \approx 0.095$$

$$L(C) = \left(\frac{C_c}{C}\right)^{\alpha_C}, \quad \alpha_C \approx 0.050$$

其中：
- $N$: 模型参数量
- $D$: 数据量 (tokens)
- $C$: 计算量 (FLOPs)
- $L$: 交叉熵损失 (nats/token)

### 5.3 Scaling Laws 的三个维度

```
        计算预算 C 固定
              │
    ┌─────────┼─────────┐
    │         │         │
    ▼         ▼         ▼
增加 N    增加 D    平衡增加
(参数)    (数据)    (两者)

最优分配: N ∝ C^0.73, D ∝ C^0.27
```

### 5.4 Compute-Optimal Training

**问题**: 给定固定的计算预算 C，如何最优地分配给 N 和 D？

**Kaplan et al. (2020) 的结论**:
- 优先增加模型参数量 N
- 数据量 D 的增加回报递减
- 最优关系: $N \propto C^{0.73}$, $D \propto C^{0.27}$

### 5.5 Chinchilla Scaling Laws (2022)

**Hoffmann et al. (2022)** 的研究挑战了 Kaplan 的结论：

> **论文**: "Training Compute-Optimal Large Language Models" (Chinchilla)

**核心发现**:
- 数据和模型应该等比例缩放
- 最优关系: $N \propto C^{0.50}$, $D \propto C^{0.50}$
- 规则: **参数量 × 20 = 最优训练 token 数**

**Chinchilla vs Gopher**:

| 模型 | 参数量 | 训练 tokens | 性能 |
|------|--------|------------|------|
| Gopher | 280B | 300B | 基准 |
| Chinchilla | 70B | 1.4T | **更优** |

Chinchilla 用更少的参数和更多的数据，实现了更好的性能！

### 5.6 Scaling Laws 的意义

1. **指导资源分配**: 如何最优地使用计算预算
2. **预测性能**: 根据规模预测模型能力
3. **推动规模扩展**: 为更大的模型提供理论依据

---

## 6. InstructGPT 与 RLHF

### 6.1 问题：对齐 (Alignment)

GPT-3 虽然强大，但存在对齐问题：
- 不遵循用户指令
- 生成有害内容
- 编造事实

### 6.2 InstructGPT (2022)

**论文**: "Training language models to follow instructions with human feedback"

**三阶段训练**:

```
阶段 1: 监督微调 (SFT)
    ↓
使用人工标注的指令-回答对微调
    ↓
阶段 2: 训练奖励模型 (RM)
    ↓
使用人类偏好数据训练奖励模型
    ↓
阶段 3: 强化学习优化 (PPO)
    ↓
使用 RL 算法优化策略
```

### 6.3 RLHF (Reinforcement Learning from Human Feedback)

**奖励模型训练**:

给定 prompt $x$ 和两个回答 $y_1, y_2$，人类偏好 $y_1 > y_2$：

$$\mathcal{L}_{RM} = -\log\sigma(r_\theta(x, y_1) - r_\theta(x, y_2))$$

**PPO 优化目标**:

$$\mathcal{L}_{PPO} = \mathbb{E}_{x,y \sim \pi_\theta} \left[ r_\phi(x, y) - \beta \cdot D_{KL}(\pi_\theta || \pi_{ref}) \right]$$

其中 $\pi_\theta$ 是当前策略，$\pi_{ref}$ 是参考策略 (SFT 模型)。

### 6.4 效果

InstructGPT (1.3B) 在人类评估中优于 GPT-3 (175B)：
- 更遵循指令
- 更少有害输出
- 更真实

---

## 7. 从 GPT-4 到现代

### 7.1 GPT-4 (2023)

**关键创新**:
1. **多模态**: 支持图像和文本输入
2. **更大的规模**: 估计 1.8T 参数 (8×220B MoE)
3. **更强的能力**: 在专业考试中达到人类水平

**GPT-4 的成就**:
- 通过律师资格考试 (前 10%)
- 通过 SAT 数学 (700/800)
- 通过 AP 多门考试 (5/5)

### 7.2 Mixture of Experts (MoE)

**架构**: 多个专家网络，稀疏激活

```
输入 x
    │
    ▼
┌─────────────┐
│ Gate Network │ → 选择 Top-K 专家
└─────────────┘
    │
    ├──→ Expert 1 (FFN)
    ├──→ Expert 2 (FFN)
    ├──→ ...
    └──→ Expert N (FFN)
           │
           ▼
    加权组合选中的专家输出
```

**数学形式**:

$$y = \sum_{i=1}^{N} g_i(x) \cdot E_i(x)$$

$$g(x) = \text{TopK}(\text{softmax}(W_g x))$$

**优势**: 在保持计算效率的同时增加模型容量。

### 7.3 现代 LLM 的共同特征

1. **Transformer 架构**: 基础架构
2. **大规模预训练**: 数万亿 tokens
3. **指令微调**: 遵循人类指令
4. **RLHF/DPO**: 人类偏好对齐
5. **MoE**: 稀疏激活提高效率
6. **长上下文**: 128K+ tokens
7. **多模态**: 文本、图像、音频、视频

---

## 8. Scaling 的经济学

### 8.1 训练成本

| 模型 | 参数量 | 估计训练成本 |
|------|--------|-------------|
| GPT-3 | 175B | $4.6M - $12M |
| GPT-4 | 1.8T (估计) | $100M+ |
| Claude 3 | 未公开 | $100M+ |
| Gemini Ultra | 未公开 | $100M+ |

### 8.2 推理成本

$$\text{推理成本} \propto \text{参数量} \times \text{序列长度}$$

MoE 架构通过稀疏激活降低推理成本。

### 8.3 能源消耗

训练一个大型 LLM 的碳排放:
- GPT-3: 约 552 吨 CO2
- 相当于 5 辆汽车终身排放

---

## 9. 未来方向

### 9.1 Scaling 的极限

**问题**: Scaling Laws 会一直有效吗？

**可能的极限**:
1. **数据瓶颈**: 高质量文本数据有限
2. **计算瓶颈**: 训练成本过高
3. **架构瓶颈**: 可能需要新的架构创新

### 9.2 新兴范式

1. **Test-time Compute**: 在推理时增加计算 (如 o1)
2. **合成数据**: 使用模型生成训练数据
3. **多模态 Scaling**: 联合扩展文本、图像、视频
4. **Agent**: 使用 LLM 作为智能代理

### 9.3 开源 vs 闭源

| 模型 | 类型 | 参数量 | 许可 |
|------|------|--------|------|
| GPT-4 | 闭源 | 1.8T | API |
| Claude 3 | 闭源 | 未公开 | API |
| LLaMA 3 | 开源 | 70B/405B | 开放 |
| Mistral | 开源 | 7B/8×7B | Apache 2.0 |
| Qwen 2 | 开源 | 72B | 开放 |

开源模型正在缩小与闭源模型的差距。

---

## 10. 关键论文列表

1. **Radford et al. (2018)**: GPT-1 - 生成式预训练
2. **Radford et al. (2019)**: GPT-2 - 无监督多任务学习
3. **Brown et al. (2020)**: GPT-3 - Few-shot learning
4. **Kaplan et al. (2020)**: Scaling Laws
5. **Hoffmann et al. (2022)**: Chinchilla Scaling Laws
6. **Ouyang et al. (2022)**: InstructGPT - RLHF
7. **OpenAI (2023)**: GPT-4 Technical Report

---

## 11. 技术细节补充

### 11.1 Tokenization

GPT 系列使用 **Byte Pair Encoding (BPE)**:

```
初始: 每个字符作为一个 token
合并: 统计最常见的相邻字符对
重复: 直到达到目标词汇表大小

示例:
"low" → ['l', 'o', 'w']
"lower" → ['low', 'e', 'r']  (如果 'low' 已合并)
```

### 11.2 位置编码

GPT 系列使用 **Learned Position Embedding**:

$$\text{Input} = \text{TokenEmbed}(x) + \text{PosEmbed}(pos)$$

现代模型 (如 GPT-4) 可能使用 RoPE (Rotary Position Embedding)。

### 11.3 激活函数演进

| 模型 | 激活函数 |
|------|---------|
| GPT-1/2 | GELU |
| GPT-3 | GELU |
| LLaMA | SwiGLU |
| GPT-4 | SwiGLU (估计) |

**SwiGLU**:
$$\text{SwiGLU}(x) = \text{Swish}(xW_1) \odot (xW_2)$$

$$\text{Swish}(x) = x \cdot \sigma(x)$$

### 11.4 混合精度训练

使用 FP16/BF16 减少内存和计算成本:

```
前向传播: FP16
梯度计算: FP16
权重更新: FP32 (主权重)
损失缩放: 动态 loss scaling
```

---

## 12. 总结

### GPT 系列的演进

```
GPT-1 (2018)     GPT-2 (2019)     GPT-3 (2020)     GPT-4 (2023)
    │                │                │                │
    ▼                ▼                ▼                ▼
预训练+微调       Zero-shot       Few-shot        多模态+MoE
  117M             1.5B            175B            1.8T (est.)
```

### 核心洞察

1. **规模很重要**: 更大的模型、更多的数据、更多的计算
2. **简洁目标**: Next token prediction 就够了
3. **涌现能力**: 规模带来质变
4. **对齐关键**: RLHF 使模型更有用、更安全
5. **Scaling Laws**: 指导资源分配的理论基础

### 未来展望

GPT 系列和 Scaling Laws 深刻影响了 AI 的发展方向。未来的关键问题包括：
- Scaling 的极限在哪里？
- 如何更高效地训练和推理？
- 如何实现真正的通用人工智能 (AGI)？

---

*最后更新: 2026-06-27*
