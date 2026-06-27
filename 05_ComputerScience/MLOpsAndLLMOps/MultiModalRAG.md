---
aliases:
  - 多模态RAG
  - Multi-Modal RAG
  - 视觉RAG
  - 跨模态检索
tags:
  - RAG
  - 多模态
  - CLIP
  - 视觉语言模型
  - Embedding
created: 2026-06-27
updated: 2026-06-27
---

# MultiModalRAG：多模态RAG

多模态RAG将检索增强生成从纯文本扩展到图像、视频、音频等多种模态。它能够理解和检索不同类型的信息，实现跨模态的语义搜索和问答，是构建多模态AI应用的核心架构。

## Vision-Language Models（视觉语言模型）

### CLIP

CLIP（Contrastive Language-Image Pre-training）通过对比学习建立图像和文本的共享嵌入空间。

**核心原理**：
- 图像编码器（ViT/ResNet）和文本编码器（Transformer）分别编码
- 通过对比损失对齐图像和文本表示
- 支持zero-shot图像分类和跨模态检索

```python
import torch
from transformers import CLIPProcessor, CLIPModel

model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")

# 图像-文本相似度计算
inputs = processor(
    text=["一只猫", "一只狗", "一辆车"],
    images=image,
    return_tensors="pt",
    padding=True
)

outputs = model(**inputs)
logits_per_image = outputs.logits_per_image  # 图像-文本相似度
```

**局限性**：
- 分辨率限制（224x224），细节信息丢失
- 对中文支持较弱
- 复杂场景理解能力有限

### SigLIP

SigLIP（Sigmoid Loss for Language Image Pre-training）改进了CLIP的训练方式：

- **Sigmoid损失**：替代softmax，支持更大batch size
- **更好的扩展性**：在相同计算量下性能更优
- **多语言支持**：SigLIP-SO400M支持多语言文本编码

### E5-V

E5-V专为多模态检索优化：

- **统一架构**：单一模型处理图像和文本嵌入
- **检索优化**：针对检索任务微调，优于通用CLIP
- **高分辨率支持**：处理高分辨率图像，保留细节

### 模型选择建议

| 场景 | 推荐模型 |
|------|----------|
| 通用图像检索 | CLIP ViT-L/14 |
| 中文场景 | chinese-clip、E5-V |
| 高分辨率 | SigLIP-SO400M |
| 生产环境 | E5-V、SigLIP |

## Image Retrieval（图像检索）

### 视觉搜索流程

```
查询（文本/图像）→ 多模态编码器 → 向量表示 → 向量数据库检索 → 排序 → 返回结果
```

### 文本搜图

```python
def text_to_image_search(query_text, image_index, top_k=10):
    """文本查询检索相关图像"""
    # 编码文本查询
    text_embedding = clip_model.encode_text(query_text)
    
    # 向量检索
    results = image_index.search(text_embedding, top_k)
    return results
```

### 图片搜图（以图搜图）

```python
def image_to_image_search(query_image, image_index, top_k=10):
    """图像查询检索相似图像"""
    # 编码查询图像
    image_embedding = clip_model.encode_image(query_image)
    
    # 向量检索
    results = image_index.search(image_embedding, top_k)
    return results
```

### 混合检索

结合文本和图像查询：

```python
def hybrid_image_search(query_text, query_image, image_index, text_weight=0.5, image_weight=0.5):
    """混合文本和图像查询"""
    text_emb = clip_model.encode_text(query_text)
    image_emb = clip_model.encode_image(query_image)
    
    # 加权融合
    combined_emb = text_weight * text_emb + image_weight * image_emb
    return image_index.search(combined_emb)
```

## Video RAG（视频RAG）

### 关键帧提取

从视频中提取代表性帧：

```python
import cv2
from scenedetect import detect, ContentDetector

def extract_keyframes(video_path, threshold=30.0):
    """基于场景变化检测提取关键帧"""
    scene_list = detect(video_path, ContentDetector(threshold=threshold))
    
    keyframes = []
    for scene in scene_list:
        frame_num = scene[0].get_frames()
        cap = cv2.VideoCapture(video_path)
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_num)
        ret, frame = cap.read()
        if ret:
            keyframes.append(frame)
        cap.release()
    
    return keyframes
```

### 时序定位（Temporal Grounding）

定位视频中与查询相关的片段：

```python
def temporal_grounding(query, video_segments, vlm_model):
    """定位视频中与文本查询相关的时间段"""
    similarities = []
    for segment in video_segments:
        # 计算文本与视频片段的相似度
        sim = vlm_model.compute_similarity(query, segment)
        similarities.append(sim)
    
    # 返回高相似度片段
    threshold = 0.7
    relevant_segments = [
        seg for seg, sim in zip(video_segments, similarities)
        if sim > threshold
    ]
    return relevant_segments
```

### 视频问答

```python
def video_qa(query, video_path, keyframe_interval=30):
    """视频问答：提取关键帧后进行多模态问答"""
    # 提取关键帧
    keyframes = extract_keyframes(video_path)
    
    # 检索相关帧
    relevant_frames = retrieve_relevant_frames(query, keyframes)
    
    # 多模态生成
    answer = vlm_model.generate(
        query=query,
        images=relevant_frames
    )
    return answer
```

## Audio RAG（音频RAG）

### Speech-to-Text Pipeline

```python
import whisper

def audio_to_text(audio_path, model_size="medium"):
    """使用Whisper将音频转为文本"""
    model = whisper.load_model(model_size)
    result = model.transcribe(audio_path)
    
    return {
        "text": result["text"],
        "segments": result["segments"],  # 带时间戳的分段
        "language": result["language"]
    }
```

### 音频指纹

用于音频相似度匹配和重复检测：

```python
import dejavu

def audio_fingerprint(audio_path):
    """生成音频指纹"""
    djv = dejavu.Dejavu(config)
    djv.fingerprint_file(audio_path)
    
    # 识别音频
    results = djv.recognize(FileRecognizer, audio_path)
    return results
```

### 播客搜索

```python
def podcast_search(query, podcast_index):
    """在播客内容中搜索"""
    # 1. 将播客音频转为文本（预处理阶段）
    # 2. 对文本建立索引
    # 3. 检索相关片段
    results = podcast_index.search(query)
    
    # 返回文本和对应时间戳
    return [{
        "text": r.text,
        "timestamp": r.timestamp,
        "podcast_id": r.podcast_id
    } for r in results]
```

## Document RAG（文档RAG）

### PDF解析

```python
from unstructured.partition.pdf import partition_pdf

def parse_pdf(pdf_path):
    """解析PDF文档，提取文本、表格、图片"""
    elements = partition_pdf(
        pdf_path,
        strategy="hi_res",
        extract_images_in_pdf=True,
        extract_tables=True
    )
    
    result = {"text": [], "tables": [], "images": []}
    for element in elements:
        if isinstance(element, Table):
            result["tables"].append(element.metadata.text_as_html)
        elif isinstance(element, Image):
            result["images"].append(element.metadata.image_path)
        else:
            result["text"].append(str(element))
    
    return result
```

### 表格提取

```python
import camelot

def extract_tables(pdf_path):
    """从PDF中提取结构化表格"""
    tables = camelot.read_pdf(pdf_path, pages="all")
    
    structured_tables = []
    for table in tables:
        df = table.df
        structured_tables.append({
            "data": df.to_dict(orient="records"),
            "html": df.to_html(),
            "page": table.page
        })
    
    return structured_tables
```

### 图表理解

```python
def chart_understanding(chart_image, vlm_model):
    """使用VLM理解图表内容"""
    description = vlm_model.generate(
        query="请详细描述这个图表的内容，包括标题、坐标轴、数据趋势、关键数据点。",
        images=[chart_image]
    )
    return description
```

## Cross-modal Alignment（跨模态对齐）

### 共享嵌入空间

通过对比学习将不同模态映射到同一空间：

```python
class MultimodalEncoder:
    def __init__(self, clip_model):
        self.model = clip_model
    
    def encode(self, inputs):
        """统一编码不同模态"""
        if isinstance(inputs, str):
            return self.model.encode_text(inputs)
        elif isinstance(inputs, Image):
            return self.model.encode_image(inputs)
        elif isinstance(inputs, torch.Tensor) and inputs.dim() == 1:
            return inputs  # 已经是向量
```

### 对比学习训练

```python
def contrastive_loss(image_embeddings, text_embeddings, temperature=0.07):
    """对比学习损失"""
    # 计算相似度矩阵
    logits = image_embeddings @ text_embeddings.T / temperature
    
    # 对角线为正样本
    labels = torch.arange(len(logits))
    
    # 双向对比损失
    loss_i2t = F.cross_entropy(logits, labels)
    loss_t2i = F.cross_entropy(logits.T, labels)
    
    return (loss_i2t + loss_t2i) / 2
```

## Implementation（实现方案）

### 多模态向量存储

```python
import chromadb

# 创建支持多模态的集合
collection = chromadb.Collection(
    name="multimodal_docs",
    metadata={"multimodal": True}
)

# 添加图像和文本
collection.add(
    ids=["img1", "txt1"],
    images=[image_data, None],
    documents=[None, "文本内容"],
    embeddings=[image_embedding, text_embedding]
)

# 跨模态查询
results = collection.query(
    query_images=[query_image],
    n_results=10
)
```

### ColPali文档检索

ColPali是专为文档检索优化的多模态模型：

```python
from colpali_engine import ColPali, ColPaliProcessor

model = ColPali.from_pretrained("vidore/colpali-v1.2")
processor = ColPaliProcessor.from_pretrained("vidore/colpali-v1.2")

def colpali_retrieve(query, document_pages):
    """使用ColPali进行文档页面检索"""
    # 编码查询和文档页面图像
    query_emb = model.encode_query(processor(query))
    doc_embs = model.encode_documents(processor(document_pages))
    
    # 计算相似度
    scores = model.score(query_emb, doc_embs)
    return scores
```

**ColPali优势**：
- 直接处理文档页面图像，无需OCR
- 保留版面布局、表格、图表信息
- 对复杂文档结构理解更好

## Use Cases（应用场景）

### 电商视觉搜索

```
用户上传商品图片 → 图像编码 → 向量检索 → 返回相似商品
用户输入文字描述 → 文本编码 → 向量检索 → 返回匹配商品
```

- **商品检索**：以图搜图，找到相似商品
- **风格匹配**：根据描述找到符合风格的商品
- **组合推荐**：基于主商品推荐搭配商品

### 视频内容分析

- **内容搜索**：在视频库中搜索包含特定内容的视频
- **片段定位**：定位视频中出现特定人物/物体的片段
- **内容审核**：自动检测视频中的违规内容

### 医学影像

- **影像检索**：检索相似病例的医学影像
- **报告生成**：基于影像自动生成诊断报告
- **辅助诊断**：检索历史病例辅助当前诊断

```python
def medical_image_search(query_image, medical_image_db, top_k=5):
    """医学影像相似病例检索"""
    # 编码查询影像
    query_emb = medical_clip.encode_image(query_image)
    
    # 检索相似影像
    results = medical_image_db.search(query_emb, top_k)
    
    # 附带诊断报告
    return [{
        "image": r.image,
        "diagnosis": r.metadata["diagnosis"],
        "similarity": r.score
    } for r in results]
```

## 最佳实践

1. **模态选择**：根据场景选择合适的模态组合，不是所有场景都需要多模态
2. **编码器选型**：优先选择针对检索任务优化的模型（如E5-V、ColPali）
3. **索引分离**：不同模态可以建立独立索引，查询时融合
4. **质量评估**：建立跨模态检索的评估基准
5. **成本考量**：多模态模型计算成本较高，需要权衡效果和成本