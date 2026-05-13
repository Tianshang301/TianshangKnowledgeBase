# 知识表示

## 一、知识表示概述

知识表示（Knowledge Representation, KR）是AI中将人类知识形式化、结构化的核心问题，使得计算机能够存储、推理和运用知识。良好的知识表示应具备：

| 特性 | 描述 |
|------|------|
| 表示充分性 | 能够表达所有需要的知识类型 |
| 推理充分性 | 支持有效的推理机制 |
| 获取效率 | 便于知识的添加与更新 |
| 简洁性 | 表示形式简洁，推理高效 |

## 二、符号化表示方法

### 框架表示 (Frames)

由Minsky提出，将知识组织为结构化的框架：

```
框架: 书籍
  槽: 标题
  槽: 作者
    侧面: 默认值 (未知)
  槽: 出版年份
    侧面: 约束 (1960-2024)
  槽: 主题
    侧面: 类型 (字符串列表)
```

框架支持继承关系——子框架自动继承父框架的槽值，同时可以覆写。

### 语义网络 (Semantic Networks)

知识表示为节点（概念）与有向边（关系）组成的图：

```
[鸟] --ISA--> [动物]
[鸟] --has--> [翅膀]
[企鹅] --ISA--> [鸟]
[企鹅] --can't--> [飞]
```

缺点：缺乏形式化语义，推理易产生歧义。

### 描述逻辑 (Description Logics)

DL是语义网的本体语言基础，提供形式化语义与可判定的推理：

- **概念** (Concepts): $C \sqsubseteq D$ （概念包含）
- **角色** (Roles): $R(a,b)$ （关系断言）
- **个体** (Individuals): $C(a)$ （实例化）

推理任务：可满足性（Satisfiability）、包含关系（Subsumption）、实例检查（Instance Checking）。

## 三、谓词逻辑

### 一阶逻辑 (FOL)

FOL是表达能力最强的形式逻辑系统之一：

- **项** (Terms): 常量 $c$，变量 $x$，函数 $f(t_1,...,t_n)$
- **谓词** (Predicates): $P(t_1,...,t_n)$
- **量词** (Quantifiers): $\forall x \exists y [\text{Person}(x) \rightarrow \text{HasMother}(x,y)]$

### Horn子句

Horn子句是FOL的子集，仅包含至多一个正文字的子句：

$$
\forall x_1,...,x_k [(A_1 \land A_2 \land ... \land A_n) \rightarrow B]
$$

Horn子句支持高效的归结推理，是Prolog语言的基础。

### 归结原理 (Resolution)

归结推理的核心规则：

$$
\frac{P \lor Q, \quad \neg P \lor R}{Q \lor R}
$$

## 四、产生式规则

产生式系统由规则库、工作记忆和推理引擎组成：

$$
\text{IF } \text{条件}_1 \land \text{条件}_2 \land ... \land \text{条件}_n \text{ THEN } \text{结论/行动}
$$

| 推理方向 | 特点 | 适用场景 |
|---------|------|---------|
| 前向链 (Forward Chaining) | 数据驱动 | 监控、规划 |
| 后向链 (Backward Chaining) | 目标驱动 | 诊断、专家系统 |

## 五、本体与语义网

### 本体 (Ontology)

本体是对共享概念的形式化、显式规范：

| 层级 | 描述 | 示例 |
|------|------|------|
| 顶层本体 | 通用概念 | 时间、空间、物质 |
| 领域本体 | 特定领域 | 医学、法律、金融 |
| 任务本体 | 特定任务 | 诊断、规划 |
| 应用本体 | 具体应用 | 病例系统 |

### RDF (Resource Description Framework)

三元组表示：$\langle \text{主体, 谓词, 客体} \rangle$

```
<http://example.org/太阳> <http://example.org/是恒星> <http://example.org/恒星> .
```

### OWL (Web Ontology Language)

OWL基于描述逻辑，提供丰富的本体建模原语：
- **类公理**: $A \sqsubseteq B$，$A \equiv B$
- **属性特征**: 传递性、对称性、函数性
- **限制**: $\forall R.C$，$\exists R.C$，$= n R.C$

## 六、贝叶斯网络

贝叶斯网络是有向无环图（DAG），节点表示随机变量，边表示条件依赖关系：

$$
P(X_1, X_2, ..., X_n) = \prod_{i=1}^n P(X_i | \text{Parents}(X_i))
```

推理任务：
- **后验推断**: $P(Q | E = e)$
- **最大后验解释**: $\arg\max_q P(Q = q | E = e)$

## 七、知识图谱

### 知识图谱基础

知识图谱由实体（节点）和关系（边）构成的图结构：

$$
\mathcal{KG} = \{(h, r, t) \mid h, t \in \mathcal{E}, r \in \mathcal{R}\}
$$

### 主要知识图谱

| 知识图谱 | 规模 | 特点 |
|---------|------|------|
| Freebase | 约30亿事实 | 早期大规模KG，Google收购 |
| Wikidata | 约10亿实体声明 | 社区维护，结构化数据 |
| DBpedia | 约38亿RDF三元组 | 从Wikipedia自动提取 |
| YAGO | 约1.2亿事实 | 高精度，时间信息标注 |
| CN-DBpedia | 约9000万事实 | 中文通用知识图谱 |

### 知识图谱构建流程

$$
\text{数据采集} \rightarrow \text{实体抽取} \rightarrow \text{关系抽取} \rightarrow \text{知识融合} \rightarrow \text{质量控制}
$$

## 八、知识图谱嵌入

### 基于平移的模型

**TransE**: 将关系建模为头实体到尾实体的平移向量

$$
f(h, r, t) = -||\mathbf{h} + \mathbf{r} - \mathbf{t}||
$$

损失函数：

$$
\mathcal{L} = \sum_{(h,r,t)\in \mathcal{T}} \sum_{(h',r',t')\in \mathcal{T}'} \max(0, \gamma + f(h,r,t) - f(h',r',t'))
$$

**TransR**: 实体和关系在不同空间建模，引入投影矩阵 $\mathbf{M}_r$：

$$
f(h, r, t) = -||\mathbf{M}_r\mathbf{h} + \mathbf{r} - \mathbf{M}_r\mathbf{t}||
$$

### 其他嵌入方法

| 方法 | 核心思想 | 评分函数 |
|-----|---------|---------|
| DistMult | 对角矩阵匹配 | $\mathbf{h}^T \text{diag}(\mathbf{r}) \mathbf{t}$ |
| ComplEx | 复数空间嵌入 | $\text{Re}(\mathbf{h}^T \text{diag}(\mathbf{r}) \overline{\mathbf{t}})$ |
| RotatE | 复平面旋转 | $-||\mathbf{h} \circ \mathbf{r} - \mathbf{t}||$ |
| ConvE | 卷积特征提取 | $f(\text{vec}(\text{conv}(\overline{\mathbf{h}}, \overline{\mathbf{r}})) \mathbf{W}) \mathbf{t}$ |

## 九、应用场景

| 应用 | 描述 | 关键技术 |
|------|------|---------|
| 问答系统 | 利用KG进行事实性问答 | 实体链接、关系推理 |
| 推荐系统 | 利用KG增强推荐多样性 | 基于路径的推荐、KG嵌入 |
| 智能推理 | 基于知识的逻辑推理 | 归纳推理、类比推理 |
| 自然语言理解 | 语义解析与消歧 | 实体识别、关系抽取 |
| 药物发现 | 生物医学KG推理新药物靶点 | 图神经网络、推理 |

## 十、挑战与前沿

- **大规模推理**：百万级实体的高效推理
- **动态知识图谱**：随时间演化的知识更新
- **多模态知识图谱**：融合文本、图像、音频等多模态信息
- **神经符号系统**：深度学习和符号推理的融合
- **大语言模型与KG结合**：利用LLM增强KG构建与推理

## 相关条目

- [[SemanticWeb]]
- [[00_KnowledgeFramework/KnowledgeGraph/INDEX|KnowledgeGraph]]
- [[05_ComputerScience/ArtificialIntelligence/MachineLearning/INDEX|MachineLearning]]
- NLP

## 参考资源

- Brachman, R. & Levesque, H. (2004). *Knowledge Representation and Reasoning*
- Bordes, A. et al. (2013). "Translating Embeddings for Modeling Multi-relational Data"
- Wang, Z. et al. (2014). "Knowledge Graph Embedding by Translating on Hyperplanes"
- 刘知远等. (2016). 《知识图谱构建技术综述》
- Hogan, A. et al. (2021). "Knowledge Graphs"
