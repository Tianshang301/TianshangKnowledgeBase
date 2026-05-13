# 自然语言处理

## 一、文本预处理

自然语言处理的第一步是将原始文本转化为计算机可处理的结构化形式。

### 分词 (Tokenization)

将文本切分为最小语义单元（token）：

```
句子: "我爱自然语言处理"
分词: ["我", "爱", "自然", "语言", "处理"]
```

常见分词工具：Jieba（中文）、NLTK、spaCy、Stanford CoreNLP。

### 词形还原与词干提取

| 方法 | 描述 | 示例 |
|------|------|------|
| **词干提取 (Stemming)** | 去除词缀，不保证为合法词 | "running" → "run" |
| **词形还原 (Lemmatization)** | 基于词典将词还原为基础形式 | "better" → "good" |

### 词性标注 (POS Tagging)

为每个词标注其语法类别：
$$
P(t_1,...,t_n|w_1,...,w_n) \propto \prod_{i=1}^n P(w_i|t_i) P(t_i|t_{i-1})
$$

### 文本清洗

- 去除HTML标签、特殊符号
- 统一大小写
- 停用词过滤

## 二、语言模型

### n-gram语言模型

基于马尔可夫假设：当前词的出现仅依赖于前 $n-1$ 个词：

$$
P(w_1, w_2, ..., w_m) = \prod_{i=1}^m P(w_i | w_{i-n+1}, ..., w_{i-1})
$$

参数估计使用最大似然估计：

$$
P(w_i | w_{i-n+1}^{i-1}) = \frac{\text{Count}(w_{i-n+1}^{i})}{\text{Count}(w_{i-n+1}^{i-1})}
$$

平滑技术解决零概率问题：Laplace平滑、Kneser-Ney平滑、Good-Turing估计。

### 神经语言模型

使用神经网络替代n-gram的计数统计：

$$
P(w_t | w_{<t}) = \text{softmax}(f_\theta(w_{<t}))
$$

## 三、词嵌入

### Word2Vec

**CBOW**：根据上下文词预测中心词

$$
\mathcal{L} = -\log P(w_t | w_{t-k}, ..., w_{t-1}, w_{t+1}, ..., w_{t+k})
$$

**Skip-gram**：根据中心词预测上下文词

$$
\mathcal{L} = -\log P(w_{t+j} | w_t), \quad -k \leq j \leq k, j \neq 0
$$

### GloVe (Global Vectors)

结合全局统计矩阵和局部上下文窗口：

$$
J = \sum_{i,j=1}^V f(X_{ij}) (\mathbf{w}_i^T \tilde{\mathbf{w}}_j + b_i + \tilde{b}_j - \log X_{ij})^2
$$

### 词嵌入特性

$$
\text{vec("国王")} - \text{vec("男人")} + \text{vec("女人")} \approx \text{vec("女王")}
$$

## 四、序列模型

### RNN (Recurrent Neural Network)

$$
\mathbf{h}_t = \tanh(\mathbf{W}_{hh} \mathbf{h}_{t-1} + \mathbf{W}_{xh} \mathbf{x}_t + \mathbf{b}_h)
$$
$$
\mathbf{y}_t = \text{softmax}(\mathbf{W}_{hy} \mathbf{h}_t + \mathbf{b}_y)
$$

### LSTM (Long Short-Term Memory)

引入门控机制解决长期依赖问题：

$$
\mathbf{i}_t = \sigma(\mathbf{W}_i [\mathbf{h}_{t-1}, \mathbf{x}_t] + \mathbf{b}_i)
$$
$$
\mathbf{f}_t = \sigma(\mathbf{W}_f [\mathbf{h}_{t-1}, \mathbf{x}_t] + \mathbf{b}_f)
$$
$$
\mathbf{o}_t = \sigma(\mathbf{W}_o [\mathbf{h}_{t-1}, \mathbf{x}_t] + \mathbf{b}_o)
$$
$$
\tilde{\mathbf{C}}_t = \tanh(\mathbf{W}_C [\mathbf{h}_{t-1}, \mathbf{x}_t] + \mathbf{b}_C)
$$
$$
\mathbf{C}_t = \mathbf{f}_t \odot \mathbf{C}_{t-1} + \mathbf{i}_t \odot \tilde{\mathbf{C}}_t
$$
$$
\mathbf{h}_t = \mathbf{o}_t \odot \tanh(\mathbf{C}_t)
$$

### GRU (Gated Recurrent Unit)

LSTM的简化变体，合并遗忘门和输入门为更新门。

## 五、注意力机制与Transformer

### 注意力机制

注意力权重计算：

$$
\text{Attention}(Q, K, V) = \text{softmax}\left(\frac{QK^T}{\sqrt{d_k}}\right)V
$$

其中 $Q$ 为查询矩阵，$K$ 为键矩阵，$V$ 为值矩阵，$\sqrt{d_k}$ 为缩放因子。

### Multi-Head Attention

$$
\text{MultiHead}(Q, K, V) = \text{Concat}(\text{head}_1, ..., \text{head}_h) W^O
$$
$$
\text{head}_i = \text{Attention}(QW_i^Q, KW_i^K, VW_i^V)
$$

### Transformer架构

由编码器（Encoder）和解码器（Decoder）堆叠而成：

| 组件 | 说明 | 公式 |
|------|------|------|
| 自注意力 | 序列内部交互 | $\text{Attention}(X, X, X)$ |
| 交叉注意力 | 编码器-解码器交互 | $\text{Attention}(Y, X, X)$ |
| 前馈网络 | 非线性变换 | $\text{FFN}(x) = \max(0, xW_1 + b_1)W_2 + b_2$ |
| 层归一化 | 稳定训练 | $\text{LayerNorm}(x + \text{Sublayer}(x))$ |
| 位置编码 | 注入位置信息 | $\text{PE}_{(pos, 2i)} = \sin(pos/10000^{2i/d})$ |

## 六、预训练语言模型

| 模型 | 架构 | 预训练任务 | 特点 |
|------|------|-----------|------|
| BERT | Encoder-only | MLM + NSP | 双向上下文，理解能力强 |
| GPT | Decoder-only | 自回归语言建模 | 单向生成，文本生成强 |
| T5 | Encoder-Decoder | Span Corruption | 统一文本到文本框架 |
| RoBERTa | Encoder-only | MLM (改进) | 更优的训练策略 |
| XLNet | Encoder-only | PLM | 排列语言建模 |

### BERT

**Masked Language Model (MLM)**：随机遮盖15%的token，预测被遮盖的词

$$
\mathcal{L}_{\text{MLM}} = -\sum_{i \in M} \log P(\tilde{w}_i | w_{\setminus M})
$$

### GPT系列

自回归生成：

$$
P(\mathbf{x}) = \prod_{t=1}^T P(x_t | x_{<t})
$$

## 七、NLP核心任务

| 任务 | 输入 | 输出 | 典型方法 |
|------|------|------|---------|
| 文本分类 | 文本序列 | 类别标签 | BERT + Linear |
| 命名实体识别 (NER) | 文本 | 实体标注序列 | BERT + CRF |
| 机器翻译 | 源语言 | 目标语言 | Transformer |
| 文本摘要 | 长文本 | 简短摘要 | BART, T5 |
| 情感分析 | 文本 | 情感极性 | LSTM/BERT |
| 关系抽取 | 文本+实体对 | 关系类型 | BERT + 分类头 |
| 阅读理解 | 文章+问题 | 答案区间 | BERT + SQuAD head |

### 序列标注

使用条件随机场（CRF）建模标签间的依赖关系：

$$
P(\mathbf{y}|\mathbf{x}) = \frac{\exp\left(\sum_i f_i(\mathbf{x}, y_i) + \sum_{i,j} g_{ij}(y_i, y_j)\right)}{Z(\mathbf{x})}
$$

## 八、LLM微调与提示工程

### 微调方法

| 方法 | 原理 | 参数量 |
|------|------|--------|
| Full Fine-tuning | 更新全部参数 | 100% |
| Adapter | 插入小型适配模块 | ~3-5% |
| LoRA | 低秩矩阵分解 $\Delta W = BA$ | ~0.1-1% |
| Prompt Tuning | 学习连续prompt向量 | ~0.01% |
| Prefix Tuning | 前缀向量注入 | ~0.1% |

### 提示工程 (Prompt Engineering)

- **零样本提示**: "将以下文本翻译为英文："
- **少样本提示**: 提供示例后推理
- **思维链 (Chain-of-Thought)**: "让我们一步步思考"
- **思维树 (Tree-of-Thoughts)**: 多路径探索

## 相关条目

- [[05_ComputerScience/ArtificialIntelligence/MachineLearning/INDEX|MachineLearning]]
- SpeechRecognition
- [[ComputationalLinguistics]]
- [[AIGC]]

## 参考资源

- Jurafsky, D. & Martin, J. H. (2023). *Speech and Language Processing* (3rd ed.)
- Vaswani, A. et al. (2017). "Attention Is All You Need"
- Devlin, J. et al. (2019). "BERT: Pre-training of Deep Bidirectional Transformers"
- Brown, T. B. et al. (2020). "Language Models are Few-Shot Learners"
- Radford, A. et al. (2018). "Improving Language Understanding by Generative Pre-Training"
- Lewis, M. et al. (2020). "BART: Denoising Sequence-to-Sequence Pre-training for NLG"
