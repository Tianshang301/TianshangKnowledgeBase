# 数据集资源指南
## 一、数据集类型

### 1.1 按数据类型分类
| 类型 | 特征 | 典型维度 | 存储格式 |
|------|------|---------|---------|
| 表格数据 | 结构化行-列 | 样本 × 特征 | CSV, Parquet |
| 图像数据 | 像素矩阵 | H × W × C | JPEG, PNG, TFRecord |
| 文本数据 | 自然语言序列 | 文档 × 词数 | TXT, JSONL |
| 音频数据 | 时序信号 | 采样点 × 通道 | WAV, MP3, FLAC |
| 视频数据 | 帧序列 | T × H × W × C | MP4, AVI |
| 时间序列 | 有序观测 | 时间步 × 变量 | CSV, TSV |
| 图数据 | 节点-边结构 | 节点 × 邻接矩阵 | GraphML, GEXF |

### 1.2 按学习范式分类
- **监督学习**：带标签数据集（分类、回归）
- **无监督学习**：无标签数据集（聚类、降维）
- **半监督学习**：少量标签 + 大量无标签
- **自监督学习**：自动生成伪标签
- **强化学习**：环境交互序列（Atari, MuJoCo）
## 二、公开数据集资源库

### 2.1 综合平台

| 平台 | 规模 | 特点 | 访问 |
|------|------|------|------|
| Kaggle | 50,000+ | 竞赛 + 社区 + Kernel | kaggle.com/datasets |
| UCI ML Repository | 600+ | 经典数据集、学术起源 | archive.ics.uci.edu |
| Hugging Face Datasets | 5,000+ | NLP 为主、多模态扩展 | huggingface.co/datasets |
| Google Dataset Search | 25,000,000+ | 跨库搜索引擘 | datasetsearch.research.google.com |
| Papers with Code | 5,000+ | 论文 + 数据集 + SOTA | paperswithcode.com/datasets |
| Zenodo | 200,000+ | 学术数据、CERN 托管 | zenodo.org |
| Figshare | 1,000,000+ | 通用学术数据 | figshare.com |

### 2.2 领域特定数据集
**计算机视觉**：
| 数据集 | 任务 | 规模 | 年份 |
|--------|------|------|------|
| ImageNet | 分类 | 14M 图像, 21K 类别 | 2009 |
| MS COCO | 检测/分割/描述 | 330K 图像, 80 类别 | 2014 |
| CIFAR-10/100 | 分类 | 60K 图像, 10/100 类别 | 2009 |
| MNIST | 手写数字识别 | 70K 图像, 10 类别 | 1998 |
| Open Images | 检测/分割 | 9M 图像, 600 类别 | 2016 |

**自然语言处理**：
| 数据集 | 任务 | 规模 | 指标 |
|--------|------|------|------|
| GLUE | 多任务理解 | 9 个子任务 | 综合得分 |
| SuperGLUE | 进阶理解 | 8 个子任务 | 综合得分 |
| SQuAD 2.0 | 阅读理解 | 150K 问答对 | EM / F1 |
| Common Crawl | 网页文本 | PB 级 | — |
| BookCorpus | 书籍文本 | 11K 本书 | — |

**音频与语音**：
| 数据集 | 任务 | 规模 | 语言 |
|--------|------|------|------|
| LibriSpeech | 语音识别 | 1000 小时 | 英语 |
| AudioSet | 音频事件 | 2M 片段, 527 类 | — |
| VoxCeleb | 说话人识别 | 7000+ 说话人 | 多语种 |

**医学领域**：
| 数据集 | 任务 | 规模 | 类型 |
|--------|------|------|------|
| MIMIC-III | 临床记录 | 40K 患者 | EHR |
| CheXpert | 胸部 X 光 | 224K 图像 | 影像 |
| NIH ChestX-ray | 胸部 X 光 | 112K 图像 | 影像 |
| TCGA | 癌症基因组 | 11K 样本 | 组学 |

## 三、数据质量评估
### 3.1 质量维度

$$ \text{Data Quality} = f(\text{Completeness}, \text{Consistency}, \text{Accuracy}, \text{Timeliness}, \text{Uniqueness}) $$

| 维度 | 定义 | 评估方法 |
|------|------|---------|
| 完整性（Completeness）| 数据是否缺失 | 缺失率统计 |
| 一致性（Consistency）| 数据是否矛盾 | 逻辑约束验证 |
| 准确性（Accuracy）| 数据是否正确 | 抽样核查 |
| 时效性（Timeliness）| 数据是否过时 | 时间戳检查 |
| 独特性（Uniqueness）| 是否存在重复 | 重复检测 |

### 3.2 数据偏差审计

- **采样偏差**：样本不能代表总体
- **标注偏差**：标注者之间的不一致
- **标签偏差**：标签定义模糊或错误
- **时间偏差**：数据采集时间影响结果
- **报告偏差**：选择性报告正面结果
## 四、数据标注方法
| 方法 | 成本 | 质量 | 速度 | 适用场景 |
|------|------|------|------|---------|
| 专家标注 | 高 | 最高 | 慢 | 医学、法律 |
| 众包标注 | 低 | 中等 | 快 | 通用标注 |
| 主动学习 | 中等 | 高 | 中等 | 标签稀疏 |
| 半监督 | 低 | 中等 | 很快 | 大量无标签数据 |
| 自动标注 | 极低 | 取决于模型 | 极快 | 预标注 |

### 4.1 Amazon Mechanical Turk 工作流
1. 设计 HIT（Human Intelligence Task）
2. 设定资格要求（批准率 > 95%，任务数 > 500）
3. 创建黄金标准问题（质量检查）
4. 多数投票或 EM 算法聚合标注
5. 标注者一致性评估（Cohen's kappa）
$$ \kappa = \frac{p_o - p_e}{1 - p_e} $$

## 五、数据预处理

### 5.1 常见预处理操作
| 操作 | 描述 | 适用场景 |
|------|------|---------|
| 去重 | 移除重复样本 | 所有类型 |
| 缺失值处理 | 删除/填充/插值 | 表格数据 |
| 标准化 | Z-score: $x' = \frac{x - \mu}{\sigma}$ | 数值特征 |
| 归一化 | Min-Max: $x' = \frac{x - x_{\min}}{x_{\max} - x_{\min}}$ | 有界特征 |
| 数据增强 | 旋转变换/噪声添加 | 图像、音频 |
| 分词 | Tokenization | 文本 |
| 重采样 | 上采样/下采样 | 不平衡分类 |

### 5.2 数据增强技术
$$ \text{增强图像} = T_{\theta}(I), \quad T \in \{\text{旋转, 翻转, 裁剪, 色彩抖动}\} $$

- **图像**：Random Crop, Flip, Rotation, Color Jitter, CutMix, MixUp
- **文本**：回译（Back Translation）、同义词替换、随机插入
- **音频**：SpecAugment（频率/时间掩码）、噪声添加
- **表格**：SMOTE（合成少数类过采样）

## 六、数据版本控制
| 工具 | 类型 | 优点 | 缺点 |
|------|------|------|------|
| DVC | 数据版本管理 | Git 集成、S3/GCS 兼容 | 学习曲线 |
| Git LFS | 大文件存储 | Git 原生 | 存储限制 |
| Hugging Face Datasets | 数据集版本管理 | 缓存/流式加载 | 主要支持 HF |
| Quilt | 数据包管理 | Pythonic API | 社区较小 |

## 七、数据文档

### 7.1 Datasheets for Datasets 模板

推荐的文档结构：

1. **动机**：为何创建此数据集？
2. **组成**：数据来源、格式、规模
3. **收集过程**：采集方法、时间、地点
4. **预处理**：清洗/过滤/标注流程
5. **用途**：适合的任务、已知限制
6. **分布**：数据的统计摘要（类别分布等）
7. **伦理**：隐私、同意、偏见
8. **维护**：版本更新、联系人

### 7.2 数据卡（Data Cards）
Hugging Face 和 Google 推动的标准化文档格式，包含模型卡和数据卡，促进负责任的数据使用。
## 八、数据许可
| 许可证 | 缩写 | 允许商业使用 | 要求署名 | 要求相同方式共享 |
|--------|------|:----------:|:--------:|:--------------:|
| CC0 | 公共领域 | ✓ | ✗ | ✗ |
| CC BY 4.0 | 署名 | ✓ | ✓ | ✗ |
| CC BY-SA 4.0 | 署名-相同方式共享 | ✓ | ✓ | ✓ |
| ODC-BY | Open Data Commons 署名 | ✓ | ✓ | ✗ |
| ODbL | Open Database License | ✓ | ✓ | ✓ |
| ODC PDDL | 公共领域 | ✓ | ✗ | ✗ |

## 九、合成数据生成
### 9.1 生成方法

$$ G(z) \rightarrow x_{\text{synthetic}}, \quad z \sim \mathcal{N}(0, I) $$

| 方法 | 原理 | 应用场景 |
|------|------|---------|
| GANs | 对抗训练生成器+判别器 | 图像、表格 |
| 扩散模型 | 逐步去噪生成 | 图像（SOTA）|
| VAE | 变分自编码器 | 连续潜在空间 |
| 基于规则 | 手工定义分布 | 简单表格 |
| 数据扰动 | 添加噪声/交换值 | 隐私保护 |

## 十、数据存储格式对比
| 格式 | 类型 | 压缩率 | 读性能 | 写性能 | 生态支持 |
|------|------|:------:|:------:|:------:|:--------:|
| CSV | 文本 | 低 | 中 | 高 | 通用 |
| Parquet | 列式二进制 | 高 | 高 | 中 | Pandas, Spark |
| TFRecord | 二进制 | 中 | 中 | 低 | TensorFlow |
| HDF5 | 层级二进制 | 中 | 高 | 中 | NumPy, MATLAB |
| LMDB | 键值二进制 | 低 | 极高 | 高 | 深度学习 |
| Feather | 二进制 | 中 | 极高 | 高 | R/Python 互操作 |

## 参考资料
- Gebru, T., et al. (2021). Datasheets for Datasets. *Communications of the ACM*, 64(12), 86-92.
- Mitchell, M., et al. (2019). Model Cards for Model Reporting. *FAccT*.
- Kaggle 数据集: https://www.kaggle.com/datasets
- Hugging Face Datasets: https://huggingface.co/datasets
- DVC 官方文档: https://dvc.org/doc
- Google Dataset Search: https://datasetsearch.research.google.com

## 相关条目

[[07_InterdisciplinarySciences/DataScience/INDEX|DataScience]], OpenData, [[ResearchMethods]], DataManagement
