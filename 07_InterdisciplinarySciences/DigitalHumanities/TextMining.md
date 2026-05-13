# 文本挖掘（数字人文）

## 概述

文本挖掘是利用自然语訢处理和机器学习技术从大量文本中提取有价信息的方法。在数字人文领域，文本挖掘为历史文献研究、文学分析文化遗产保护等提供了新的研究范式?
## 文本预处?
### 中文分词

**分词方法?*
- 基于词典：最大匹配法、向朢大匹?- 基于统计：隐马尔可夫模型、条件随机场
- 基于深度学习：BiLSTM-CRF、BERT

**常用工具?*
- jieba：Python中文分词
- HanLP：多语言NLP工具
- pkuseg：北京大学分?
```python
import jieba

# 精确模式
text = "数字人文是跨学科的研究领?
words = jieba.lcut(text)

# 添加自定义词?jieba.add_word("数字人文")
```

### 去除停用?
**停用词类型：**
- 语气词：啊呢、吗
- 连词：和、与、及
- 介词：在、从、向
- 代词：这、那、他

**停用词表?*
- 哈工大停用词?- 百度停用词表
- 自定义停用词?
```python
def remove_stopwords(words, stopwords):
    return [w for w in words if w not in stopwords and len(w) > 1]
```

### 词标?
**标注集：**
- 名词（n）动词（v）形容词（a?- 副词（d）介词（p）连词（c?
**工具?*
- jieba.posseg
- HanLP词标?- LTP词标?
## 词频分析

### 词频统计

**基本统计?*
- 词频列表
- 词频分布
- TF-IDF权重

**TF-IDF计算?*
$$TF-IDF(t,d) = TF(t,d) \times IDF(t)$$

$$IDF(t) = \log\frac{N}{DF(t)}$$

### 词云

**制作工具?*
- WordCloud（Python?- 微词?- 图悦

**设计要点?*
- 词频映射到大?- 颜色选择
- 形状设计

```python
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# 生成词云
wc = WordCloud(font_path='simhei.ttf', 
               width=800, height=400,
               max_words=200)
wc.generate(text)

# 显示词云
plt.imshow(wc)
plt.axis('off')
plt.show()
```

### 词频分析应用

**文献计量?*
- 研究热点分析
- 学科发展趋势
- 作关键词分析

**历史文献?*
- 历史术语演变
- 概念史研?- 文本风格分析

## 主题模型

### LDA（Latent Dirichlet Allocation?
**基本原理?*
- 文档-主题-词三层结?- 每个文档是主题的混合
- 每个主题是词的分?
**概率模型?*
$$P(w|d) = \sum_{k=1}^{K}P(w|z=k)P(z=k|d)$$

**参数估计?*
- 变分推断
- Gibbs采样
- 在线学习

### LDA应用

**参数设置?*
- 主题数K：困惑度、一致?- 超参数：α（文?主题）β（主题-词）

**结果解释?*
- 主题词列?- 文档-主题分布
- 主题可视?
```python
from gensim import corpora, models

# 创建词典和语料库
dictionary = corpora.Dictionary(texts)
corpus = [dictionary.doc2bow(text) for text in texts]

# 训练LDA模型
lda = models.LdaModel(corpus, num_topics=5, 
                       id2word=dictionary,
                       passes=15)

# 输出主题
for topic in lda.print_topics():
    print(topic)
```

### 其他主题模型

- **NMF**：非负矩阵分?- **pLSA**：概率潜在语义分?- **动主题模?*：时序主题演?- **层次主题模型**：主题层次结?
## 情感分析

### 情感词典方法

**词典构建?*
- 知网HowNet情感词典
- 台湾大学NTUSD
- 大连理工大学情感词汇本体

**情感计算?*
$$Sentiment = \sum_{i=1}^{n}w_i \times score(word_i)$$

### 机器学习方法

**特征工程?*
- 词袋模型
- TF-IDF
- 词嵌?
**常用算法?*
- 朴素贝叶?- SVM
- 随机森林
- 深度学习（LSTM、BERT?
```python
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB

# 特征提取
vectorizer = TfidfVectorizer()
X_train = vectorizer.fit_transform(train_texts)

# 训练模型
clf = MultinomialNB()
clf.fit(X_train, train_labels)

# 预测
X_test = vectorizer.transform(test_texts)
predictions = clf.predict(X_test)
```

### 深度学习情感分析

**BERT微调?*
```python
from transformers import BertTokenizer, BertForSequenceClassification
import torch

# 加载模型
tokenizer = BertTokenizer.from_pretrained('bert-base-chinese')
model = BertForSequenceClassification.from_pretrained('bert-base-chinese')

# 编码
inputs = tokenizer(text, return_tensors='pt', padding=True, truncation=True)
outputs = model(**inputs)
```

## 命名实体识别（NER?
### 定义

识别文本中的人名、地名机构名、时间等实体?
### 标注体系

**BIO标注?*
- B：实体开?- I：实体内?- O：非实体

**示例?*
```
北京/nr ?v 中国/ns ?uj 首都/n
```

### NER方法

**基于规则?*
- 正则表达?- 词典匹配
- 模板匹配

**基于统计?*
- HMM
- CRF
- BiLSTM-CRF

**基于预训练模型：**
- BERT-NER
- RoBERTa-NER

```python
from transformers import BertTokenizer, TokenClassificationPipeline

# 加载NER模型
tokenizer = BertTokenizer.from_pretrained('bert-base-chinese')
pipeline = TokenClassificationPipeline(model=model, tokenizer=tokenizer)

# 识别实体
result = pipeline("北京大学是中国著名高等学?)
```

## 文本挖掘在历史文献中的应?
### 历史文献数字?
**OCR抢术：**
- 古籍文字识别
- 手写体识?- 多字体处?
**数字化工具：**
- Tesseract OCR
- 百度OCR
- ABBYY FineReader

### 历史文本分析

**人物关系网络?*
- 人名识别
- 关系抽取
- 社会网络分析

**历史事件分析?*
- 事件抽取
- 时间线构?- 因果关系分析

**思想史研究：**
- 概念演变
- 思潮分析
- 影响力评?
### 案例研究

**《红楼梦》文本分析：**
- 人物词频
- 情感分析
- 风格分析

**《史记研究：**
- 人物关系网络
- 时间分布
- 地理分布

### 工具平台

- **MARKUS**：历史文献标?- **DocuSky**：台湾数位人?- **CBDB**：中国历代人物传记数据库
- **CTEXT**：中国哲学书电子化计?
## 参资?
- 《数字人文导论?- 《文本挖掘与分析?- 《Python自然语言处理?- 《数字人文研究期?

## 相关条目

[[ComputationalLinguistics]], [[07_InterdisciplinarySciences/DataScience/INDEX|DataScience]], [[TextMining]], [[CulturalAnalytics]]
