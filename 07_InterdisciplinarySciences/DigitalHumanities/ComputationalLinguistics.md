# 计算语言?
## 概述

计算语言学是运用计算方法研究人类语言的结构意义与使用的交叉学科它在语訢学理论人工智能与自然语言处理之间架起桥梁，推动人机交互与语言抢术发展?
## 语料库语訢学（Corpus Linguistics?
### 语料库设?- **代表?*：语料库应均衡覆盖语訢变体、体裁语?- **平衡?*：各类文本按比例抽样
- **规模**：从早期的百万词级（Brown Corpus）到当今万亿词级

### 语料库标?- **词标注（POS Tagging?*：为每个词标注语法类别（名词、动词等?- **句法标注（Treebanking?*：建立句法树标注库，如Penn Treebank
- **语义标注**：语义角色命名实体共指关系等

## 句法分析（Syntactic Parsing?
### 短语结构句法 vs 依存句法
- **短语结构（Constituency?*：句子由嵌套的短语构成，用上下文无关语法（CFG）描?- **依存句法（Dependency?*：词与词之间存在直接依存关系，形成依存树

### 概率上下文无关语法（PCFG?CFG的每个产生式赋予概率，过CKY算法（Cocke-Kasami-Younger）寻找最可能的句法树。CKY算法复杂度为 $O(n^3 \cdot |G|)$?
### 基于转换的依存分析（Transition-based Dependency Parsing?- **Arc-Standard算法**：使用栈和缓冲区，过SHIFT、LEFT-ARC、RIGHT-ARC等动作步构建依存?- **分类?*：用机器学习（如神经网络）预测下丢动作
- **优势**：线性时间复杂度 $O(n)$

## 语义分析（Semantic Analysis?
### 词义消歧（Word Sense Disambiguation, WSD?根据上下文确定多义词的特定含义方法包括基于词典的Lesk算法、监督学习的特征分类器?
### 语义角色标注（Semantic Role Labeling, SRL?识别句子中谓词的论元及其语义角色（施事受事工具等）基于框架语义学（FrameNet）或动词词典（PropBank）?
## 话语分析（Discourse Analysis?- **话语结构**：修辞结构理论（RST），篇章关系（因果对比序列）
- **共指消解（Coreference Resolution?*：识别指向同丢实体的不同表述（?奥巴????- **话语连接?*：标记篇章关系的语言线索

## 机器翻译（Machine Translation, MT?
### 基于规则的方法（RBMT?依靠语言学家编写的大规模双语词典和语法规则系统构建成本高、覆盖率有限?
### 统计机器翻译（SMT?- **IBM模型**：从词对齐到短语对齐的一系列统计翻译模型。IBM Model 3引入增殖（fertility）概?- **短语翻译**：基于短语的SMT系统（如Moses），考虑屢部上下文
- **对数线模?*：整合翻译模型语訢模型、重排序模型等多个特?
### 神经机器翻译（NMT?- **编码?解码器架?*：循环神经网络（RNN）将源语訢编码为上下文向量，解码器逐词生成目标语言
- **注意力机?*（Bahdanau Attention）：解码时动态关注源语言不同位置，解决长距离依赖问题
- **Transformer架构**（Vaswani et al., 2017）：完全基于自注意力机制，并行计算效率高
- **大语訢模型**：GPT、BERT等预训练模型在机器翻译中的fine-tuning应用

## 信息抽取（Information Extraction, IE?
### 命名实体识别（NER?识别文本中的命名实体（人名地名机构名、时间等）主流方法：BiLSTM-CRF、BERT-based?
### 关系抽取（Relation Extraction?识别实体之间的语义关系（?BornIn(? 地点)"）方法包括模式匹配远程监督预训练模型微调?
### 事件抽取（Event Extraction?识别文本中描述的事件及其参与者（触发词论元角色）?
## NLP评估

### 自动评价指标
- **BLEU**：基于n-gram精确率的机器翻译评价指标
- **ROUGE**：基于n-gram召回率的自动摘要评价指标
- **F1-score**：精确率与召回率的调和平均，常用于NER、分类任?
### 评价数据?- **GLUE/SuperGLUE**：用语言理解任务?- **SQuAD**：阅读理解数据集
- **CoNLL**：共享任务数据集（NER、SRL等）

## 相关条目

[[ComputationalLinguistics]], [[07_InterdisciplinarySciences/DataScience/INDEX|DataScience]], [[TextMining]], [[CulturalAnalytics]]
