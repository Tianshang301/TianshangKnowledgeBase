# 人工智能 / 机器学习知识索引

## 目录

- [ML 基础](#ml-基础)
- [经典算法](#经典算法)
- [深度学习](#深度学习)
- [自然语言处理 (NLP)](#自然语言处理-nlp)
- [计算机视觉 (CV)](#计算机视觉-cv)
- [框架对比](#框架对比)
- [MLOps 基础](#mlops-基础)

---

## ML 基础

### 学习范式

```
监督学习（Supervised Learning）
  输入 X → 模型 → 输出 Y
  需要标注数据 (X, Y)
  分类 / 回归

  无监督学习（Unsupervised Learning）
  输入 X → 模型 → 隐藏结构
  不需要标注数据
  聚类 / 降维 / 密度估计

  强化学习（Reinforcement Learning）
  状态 S → 动作 A → 奖励 R
  智能体与环境交互学习策略
  游戏 / 机器人 / 自动驾驶

  半监督学习
  少量标注 + 大量未标注数据

  自监督学习
  从数据自身构造监督信号（BERT、MAE）
```

### 评估指标

```python
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score,
    f1_score, confusion_matrix, roc_auc_score,
    mean_squared_error, r2_score
)

# 分类指标
y_true = [0, 1, 1, 0, 1, 1, 0, 0]
y_pred = [0, 1, 0, 0, 1, 1, 1, 0]

print(f"准确率: {accuracy_score(y_true, y_pred):.3f}")
print(f"精确率: {precision_score(y_true, y_pred):.3f}")
print(f"召回率: {recall_score(y_true, y_pred):.3f}")
print(f"F1分数: {f1_score(y_true, y_pred):.3f}")
print(f"混淆矩阵:\n{confusion_matrix(y_true, y_pred)}")

# 回归指标
y_true_reg = [1.0, 2.0, 3.0, 4.0]
y_pred_reg = [1.1, 1.9, 3.2, 3.8]
print(f"MSE: {mean_squared_error(y_true_reg, y_pred_reg):.3f}")
print(f"R²: {r2_score(y_true_reg, y_pred_reg):.3f}")
```

| 指标 | 公式 | 说明 |
|------|------|------|
| 准确率 | (TP+TN)/(TP+TN+FP+FN) | 整体正确率 |
| 精确率 | TP/(TP+FP) | 查准率，预测为正样本的准确度 |
| 召回率 | TP/(TP+FN) | 查全率，正样本被找到的比例 |
| F1 | 2×P×R/(P+R) | 精确率和召回率的调和平均 |
| AUC | — | ROC 曲线下面积 |
| MSE | Σ(y-ŷ)²/n | 均方误差 |
| R² | 1 - SSres/SStot | 拟合优度 |

---

## 经典算法

### 线性回归

```python
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures

# 简单线性回归
X = np.array([[1], [2], [3], [4], [5]])
y = np.array([2, 4, 5, 4, 6])

model = LinearRegression()
model.fit(X, y)
print(f"系数: {model.coef_[0]:.2f}, 截距: {model.intercept_:.2f}")

# 多项式回归
poly = PolynomialFeatures(degree=2)
X_poly = poly.fit_transform(X)
model_poly = LinearRegression()
model_poly.fit(X_poly, y)
```

### 决策树

```python
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.ensemble import RandomForestClassifier
import matplotlib.pyplot as plt

# 决策树
dt = DecisionTreeClassifier(
    max_depth=5,
    min_samples_split=10,
    min_samples_leaf=5,
    criterion='gini'
)
dt.fit(X_train, y_train)

# 可视化树
plt.figure(figsize=(20, 10))
plot_tree(dt, filled=True, feature_names=feature_names)
plt.show()

# 随机森林
rf = RandomForestClassifier(
    n_estimators=100,
    max_depth=10,
    random_state=42
)
rf.fit(X_train, y_train)
print(f"特征重要性: {rf.feature_importances_}")
```

### SVM

```python
from sklearn.svm import SVC
from sklearn.preprocessing import StandardScaler

# 数据标准化（SVM 对尺度敏感）
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# SVM 分类器
svm = SVC(
    kernel='rbf',       # 线性/poly/rbf/sigmoid
    C=1.0,              # 正则化参数
    gamma='scale',      # RBF 核参数
    probability=True    # 输出概率
)
svm.fit(X_train_scaled, y_train)
print(f"SVM 准确率: {svm.score(X_test_scaled, y_test):.3f}")
```

### KNN

```python
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import cross_val_score

# 寻找最优 K 值
k_range = range(1, 31)
k_scores = []

for k in k_range:
    knn = KNeighborsClassifier(n_neighbors=k)
    scores = cross_val_score(knn, X_train, y_train, cv=5)
    k_scores.append(scores.mean())

best_k = k_range[np.argmax(k_scores)]
print(f"最优 K 值: {best_k}")

knn = KNeighborsClassifier(n_neighbors=best_k)
knn.fit(X_train, y_train)
```

### K-Means 聚类

```python
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA

# 肘部法确定 K 值
inertias = []
for k in range(1, 11):
    kmeans = KMeans(n_clusters=k, random_state=42)
    kmeans.fit(X)
    inertias.append(kmeans.inertia_)

# 选择拐点处的 K 值
kmeans = KMeans(n_clusters=3, random_state=42)
labels = kmeans.fit_predict(X)

# 可视化（使用 PCA 降维到 2D）
pca = PCA(n_components=2)
X_2d = pca.fit_transform(X)
plt.scatter(X_2d[:, 0], X_2d[:, 1], c=labels, cmap='viridis')
plt.scatter(kmeans.cluster_centers_[:, 0], kmeans.cluster_centers_[:, 1],
            marker='x', s=200, linewidths=3, color='red')
```

### 算法对比总结

| 算法 | 类型 | 优点 | 缺点 |
|------|------|------|------|
| 线性回归 | 回归 | 简单、可解释强 | 只能处理线性关系 |
| 逻辑回归 | 分类 | 输出概率、可解释 | 决策边界线性 |
| 决策树 | 分类/回归 | 可解释、无需归一化 | 易过拟合 |
| 随机森林 | 分类/回归 | 高精度、抗过拟合 | 模型大、慢 |
| SVM | 分类/回归 | 核技巧、高维有效 | 大数据集慢 |
| KNN | 分类/回归 | 无需训练 | 计算量大、维度灾难 |
| K-Means | 聚类 | 简单、高效 | 需指定K、球形簇假设 |
| 朴素贝叶斯 | 分类 | 极快、小数据有效 | 特征独立假设 |

---

## 深度学习

### 神经网络基础

```python
import torch
import torch.nn as nn
import torch.optim as optim

# PyTorch 定义 MLP
class MLP(nn.Module):
    def __init__(self, input_dim, hidden_dim, output_dim):
        super().__init__()
        self.network = nn.Sequential(
            nn.Linear(input_dim, hidden_dim),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(hidden_dim, hidden_dim),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(hidden_dim, output_dim)
        )

    def forward(self, x):
        return self.network(x)

model = MLP(input_dim=784, hidden_dim=256, output_dim=10)
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

# 训练循环
for epoch in range(10):
    for batch_x, batch_y in dataloader:
        optimizer.zero_grad()
        outputs = model(batch_x)
        loss = criterion(outputs, batch_y)
        loss.backward()
        optimizer.step()
    print(f"Epoch {epoch}, Loss: {loss.item():.4f}")
```

### CNN（卷积神经网络）

```python
# PyTorch 卷积神经网络
class CNN(nn.Module):
    def __init__(self, num_classes=10):
        super().__init__()
        self.features = nn.Sequential(
            nn.Conv2d(3, 32, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2),
            nn.Conv2d(32, 64, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2),
            nn.Conv2d(64, 128, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.AdaptiveAvgPool2d(1)
        )
        self.classifier = nn.Sequential(
            nn.Linear(128, 256),
            nn.ReLU(),
            nn.Dropout(0.5),
            nn.Linear(256, num_classes)
        )

    def forward(self, x):
        x = self.features(x)
        x = x.view(x.size(0), -1)
        return self.classifier(x)
```

### RNN / LSTM

```python
class LSTMModel(nn.Module):
    def __init__(self, vocab_size, embedding_dim, hidden_dim, num_layers):
        super().__init__()
        self.embedding = nn.Embedding(vocab_size, embedding_dim)
        self.lstm = nn.LSTM(
            embedding_dim,
            hidden_dim,
            num_layers,
            batch_first=True,
            bidirectional=True,
            dropout=0.3
        )
        self.classifier = nn.Linear(hidden_dim * 2, num_classes)  # 双向

    def forward(self, x):
        embedded = self.embedding(x)
        lstm_out, (hidden, cell) = self.lstm(embedded)
        # 使用最后一个时间步的输出
        last_hidden = torch.cat((hidden[-2], hidden[-1]), dim=1)
        return self.classifier(last_hidden)
```

### Transformer

```python
import torch.nn.functional as F

class MultiHeadAttention(nn.Module):
    def __init__(self, d_model, num_heads):
        super().__init__()
        self.num_heads = num_heads
        self.d_k = d_model // num_heads

        self.W_q = nn.Linear(d_model, d_model)
        self.W_k = nn.Linear(d_model, d_model)
        self.W_v = nn.Linear(d_model, d_model)
        self.W_o = nn.Linear(d_model, d_model)

    def forward(self, query, key, value, mask=None):
        batch_size = query.size(0)

        # 线性变换并分头
        Q = self.W_q(query).view(batch_size, -1, self.num_heads, self.d_k).transpose(1, 2)
        K = self.W_k(key).view(batch_size, -1, self.num_heads, self.d_k).transpose(1, 2)
        V = self.W_v(value).view(batch_size, -1, self.num_heads, self.d_k).transpose(1, 2)

        # Scaled Dot-Product Attention
        scores = torch.matmul(Q, K.transpose(-2, -1)) / (self.d_k ** 0.5)
        if mask is not None:
            scores = scores.masked_fill(mask == 0, -1e9)

        attn = F.softmax(scores, dim=-1)
        context = torch.matmul(attn, V)

        # 合并头
        context = context.transpose(1, 2).contiguous().view(
            batch_size, -1, self.num_heads * self.d_k
        )
        return self.W_o(context)

class TransformerBlock(nn.Module):
    def __init__(self, d_model, num_heads, d_ff, dropout=0.1):
        super().__init__()
        self.attention = MultiHeadAttention(d_model, num_heads)
        self.norm1 = nn.LayerNorm(d_model)
        self.norm2 = nn.LayerNorm(d_model)
        self.ffn = nn.Sequential(
            nn.Linear(d_model, d_ff),
            nn.ReLU(),
            nn.Dropout(dropout),
            nn.Linear(d_ff, d_model)
        )
        self.dropout = nn.Dropout(dropout)

    def forward(self, x, mask=None):
        # 多头自注意力 + 残差连接 + LayerNorm
        attn_out = self.attention(x, x, x, mask)
        x = self.norm1(x + self.dropout(attn_out))

        # 前馈网络 + 残差连接 + LayerNorm
        ffn_out = self.ffn(x)
        x = self.norm2(x + self.dropout(ffn_out))
        return x
```

---

## 自然语言处理 (NLP)

### 词嵌入

```python
# Word2Vec (CBOW + Skip-gram)
from gensim.models import Word2Vec

sentences = [["我", "喜欢", "机器学习"], ["深度学习", "是", "机器学习的", "子集"]]
model = Word2Vec(sentences, vector_size=100, window=5, min_count=1, sg=0)  # sg=0: CBOW, sg=1: Skip-gram

# 词向量相似度
similar_words = model.wv.most_similar("机器学习", topn=5)
print(f"与「机器学习」最相似的词: {similar_words}")

# GloVe (预训练词向量)
# 下载预训练 GloVe 向量，使用 spacy 或 torchtext 加载
```

### BERT

```python
from transformers import BertTokenizer, BertModel
import torch

# 加载预训练 BERT
tokenizer = BertTokenizer.from_pretrained('bert-base-chinese')
model = BertModel.from_pretrained('bert-base-chinese')

# 编码文本
text = "今天天气真好"
inputs = tokenizer(text, return_tensors='pt', padding=True, truncation=True)

# 获取表示
with torch.no_grad():
    outputs = model(**inputs)

# 获取 [CLS] 向量（可用于分类）
cls_embedding = outputs.last_hidden_state[:, 0, :]

# 获取所有 token 向量
token_embeddings = outputs.last_hidden_state

# 使用 BertForSequenceClassification 进行微调
from transformers import BertForSequenceClassification, Trainer, TrainingArguments

model = BertForSequenceClassification.from_pretrained(
    'bert-base-chinese',
    num_labels=2  # 二分类
)

training_args = TrainingArguments(
    output_dir='./results',
    per_device_train_batch_size=16,
    num_train_epochs=3,
    learning_rate=2e-5,
    warmup_ratio=0.1,
    logging_dir='./logs',
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=eval_dataset,
)
trainer.train()
```

### GPT

```python
from transformers import GPT2LMHeadModel, GPT2Tokenizer

# 加载 GPT-2
tokenizer = GPT2Tokenizer.from_pretrained('gpt2')
model = GPT2LMHeadModel.from_pretrained('gpt2')

# 文本生成
prompt = "人工智能的未来是"
inputs = tokenizer(prompt, return_tensors='pt')

# 生成
outputs = model.generate(
    **inputs,
    max_length=100,
    temperature=0.7,
    top_k=50,
    top_p=0.9,
    do_sample=True,
    num_return_sequences=3
)

for i, output in enumerate(outputs):
    text = tokenizer.decode(output, skip_special_tokens=True)
    print(f"生成 {i+1}: {text}")
```

### NLP 任务概览

| 任务 | 说明 | 典型模型 |
|------|------|----------|
| 文本分类 | 情感分析、垃圾检测 | BERT、TextCNN |
| 命名实体识别 (NER) | 识别人名、地名等 | BERT-CRF |
| 关系抽取 | 实体间关系 | BILSTM + Attention |
| 机器翻译 | 语言转换 | Transformer |
| 文本摘要 | 长文压缩 | BART、Pegasus |
| 问答系统 | 基于文档问答 | BERT QA、T5 |
| 文本生成 | 续写、创作 | GPT、LLaMA |

---

## 计算机视觉 (CV)

### 图像分类

```python
import torchvision.models as models

# 使用预训练 ResNet
resnet = models.resnet50(weights='IMAGENET1K_V2')
# 替换最后一层适配自定义类别数
resnet.fc = nn.Linear(2048, num_classes)

# 数据增强
from torchvision import transforms

train_transform = transforms.Compose([
    transforms.RandomResizedCrop(224),
    transforms.RandomHorizontalFlip(),
    transforms.ColorJitter(brightness=0.2, contrast=0.2),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])
```

### 目标检测

```
经典目标检测框架：

Two-Stage（两阶段检测器）：
  R-CNN → Fast R-CNN → Faster R-CNN → Mask R-CNN
  流程：提议区域 → 分类 + 回归

One-Stage（单阶段检测器）：
  YOLO (v1-v8) — 实时检测
  SSD — 多尺度特征
  RetinaNet — Focal Loss 解决类别不平衡

Anchor-Free（无锚点）：
  CenterNet、FCOS
```

### 图像分割

```python
# U-Net 结构（医学图像分割经典）
class UNet(nn.Module):
    def __init__(self, in_channels=3, out_channels=1):
        super().__init__()
        # 编码器（下采样）
        self.enc1 = self.conv_block(in_channels, 64)
        self.enc2 = self.conv_block(64, 128)
        self.enc3 = self.conv_block(128, 256)
        self.pool = nn.MaxPool2d(2)

        # 瓶颈
        self.bottleneck = self.conv_block(256, 512)

        # 解码器（上采样）
        self.up3 = nn.ConvTranspose2d(512, 256, 2, stride=2)
        self.dec3 = self.conv_block(512, 256)
        self.up2 = nn.ConvTranspose2d(256, 128, 2, stride=2)
        self.dec2 = self.conv_block(256, 128)
        self.up1 = nn.ConvTranspose2d(128, 64, 2, stride=2)
        self.dec1 = self.conv_block(128, 64)

        self.out = nn.Conv2d(64, out_channels, 1)

    def conv_block(self, in_c, out_c):
        return nn.Sequential(
            nn.Conv2d(in_c, out_c, 3, padding=1),
            nn.BatchNorm2d(out_c),
            nn.ReLU(),
            nn.Conv2d(out_c, out_c, 3, padding=1),
            nn.BatchNorm2d(out_c),
            nn.ReLU()
        )

    def forward(self, x):
        e1 = self.enc1(x)
        e2 = self.enc2(self.pool(e1))
        e3 = self.enc3(self.pool(e2))
        b = self.bottleneck(self.pool(e3))
        d3 = self.dec3(torch.cat([self.up3(b), e3], dim=1))
        d2 = self.dec2(torch.cat([self.up2(d3), e2], dim=1))
        d1 = self.dec1(torch.cat([self.up1(d2), e1], dim=1))
        return self.out(d1)
```

---

## 框架对比

| 特性 | PyTorch | TensorFlow |
|------|---------|------------|
| 动态图 | 原生（Eager） | 2.x Eager，静态图也可 |
| 调试 | Python 原生（pdb） | 较复杂（tf.print/回调） |
| 生产部署 | TorchScript / ONNX | TF Serving / TFLite |
| 分布式训练 | DDP / FSDP | MirroredStrategy / TPU |
| 社区生态 | HuggingFace、学术界 | TF Hub、Keras |
| 学习曲线 | 相对平缓 | 相对陡峭 |
| 推荐项目 | NLP / 科研 | 生产部署 / 移动端 |

---

## MLOps 基础

### ML 工作流

```
数据收集 → 数据清洗 → 特征工程 → 模型训练 → 模型评估 → 部署上线 → 监控
  ↑                                                                   │
  └────────────────────────── 持续迭代 ────────────────────────────────┘
```

### 关键工具

```yaml
# MLflow 实验追踪
MLflow Tracking: 记录参数、指标、模型、artifact
MLflow Registry: 模型版本管理
MLflow Serving: 模型部署

# DVC (Data Version Control)
dvc init
dvc add data/raw_dataset.csv
git add data/raw_dataset.csv.dvc .gitignore
git commit -m "add dataset"
dvc remote add myremote s3://mybucket/data
dvc push
```

```python
# MLflow 示例
import mlflow
import mlflow.sklearn

mlflow.set_experiment("iris_classifier")

with mlflow.start_run():
    # 记录参数
    mlflow.log_param("model_type", "RandomForest")
    mlflow.log_param("n_estimators", 100)

    # 训练模型
    model = RandomForestClassifier(n_estimators=100)
    model.fit(X_train, y_train)

    # 记录指标
    acc = accuracy_score(y_test, model.predict(X_test))
    mlflow.log_metric("accuracy", acc)

    # 记录模型
    mlflow.sklearn.log_model(model, "model")

    # 记录重要文件
    mlflow.log_artifact("feature_importance.png")
```

---

> **参考资源**：scikit-learn 文档、PyTorch 官方教程、HuggingFace 文档、《Deep Learning》(Goodfellow)、CS231n / CS224n

---

## 相关文件

- [[05_ComputerScience/ArtificialIntelligence/AIEthics/AIEthics]] — AI 伦理
- [[05_ComputerScience/ArtificialIntelligence/AIEthics/AI安全与对齐]] — AI 安全与对齐
- [[05_ComputerScience/ArtificialIntelligence/AIGC/AIGC]] — AIGC 概述
- [[05_ComputerScience/ArtificialIntelligence/AIGC/AIGC模型架构与应用]] — AIGC 模型架构
- [[05_ComputerScience/ArtificialIntelligence/ComputerVision/ComputerVision]] — 计算机视觉
- [[05_ComputerScience/ArtificialIntelligence/ComputerVision/图像处理与特征提取]] — 图像处理与特征提取
- [[05_ComputerScience/ArtificialIntelligence/KnowledgeRepresentation/KnowledgeRepresentation]] — 知识表示
- [[05_ComputerScience/ArtificialIntelligence/KnowledgeRepresentation/知识图谱构建技术]] — 知识图谱构建技术
- [[05_ComputerScience/ArtificialIntelligence/MachineLearning/SupervisedLearning/INDEX]] — 监督学习
- [[05_ComputerScience/ArtificialIntelligence/MachineLearning/UnsupervisedLearning/INDEX]] — 无监督学习
- [[05_ComputerScience/ArtificialIntelligence/MachineLearning/ReinforcementLearning/INDEX]] — 强化学习
- [[05_ComputerScience/ArtificialIntelligence/MachineLearning/NeuralNetworksAndDeepLearning/INDEX]] — 神经网络与深度学习
- [[05_ComputerScience/ArtificialIntelligence/MachineLearning/ModelEvaluation/INDEX]] — 模型评估
- [[05_ComputerScience/ArtificialIntelligence/NaturalLanguageProcessing/NaturalLanguageProcessing]] — 自然语言处理
- [[05_ComputerScience/ArtificialIntelligence/NaturalLanguageProcessing/序列建模与Transformer]] — 序列建模与 Transformer
