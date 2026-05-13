# 计算机视觉

## 一、图像形成与表示

数字图像在计算机中以矩阵形式表示。对于灰度图像，每个像素的强度值 $I(x,y)$ 构成二维矩阵；对于彩色图像，通常采用RGB三通道表示：

$$
I(x,y) = [R(x,y), G(x,y), B(x,y)]^T
$$

图像分辨率表示为 $H \times W \times C$，其中 $H$ 为高度，$W$ 为宽度，$C$ 为通道数。

### 图像采样与量化

- **空间采样**：决定图像分辨率
- **灰度量化**：决定每个像素的灰度级数（通常8 bit，即256级）

## 二、图像滤波

### 卷积操作

图像滤波通过卷积核（kernel）与图像进行卷积运算：

$$
(f * g)(x,y) = \sum_{i=-a}^{a} \sum_{j=-b}^{b} f(x-i, y-j) \cdot g(i,j)
$$

### 常见滤波器

| 滤波器 | 核 | 用途 |
|-------|-----|------|
| 高斯滤波 (Gaussian) | $\frac{1}{2\pi\sigma^2}e^{-\frac{x^2+y^2}{2\sigma^2}}$ | 去噪、平滑 |
| 均值滤波 | $\frac{1}{k^2}\mathbf{1}_{k\times k}$ | 平滑 |
| 中值滤波 | 排序取中值 | 去椒盐噪声 |

### 边缘检测

**Sobel算子**：计算图像梯度近似值

$$
G_x = \begin{bmatrix} -1 & 0 & 1 \\ -2 & 0 & 2 \\ -1 & 0 & 1 \end{bmatrix} * I, \quad
G_y = \begin{bmatrix} -1 & -2 & -1 \\ 0 & 0 & 0 \\ 1 & 2 & 1 \end{bmatrix} * I
$$

$$
G = \sqrt{G_x^2 + G_y^2}, \quad \theta = \arctan\left(\frac{G_y}{G_x}\right)
$$

**Canny边缘检测**流程：
1. 高斯滤波去噪
2. 计算梯度幅值与方向
3. 非极大值抑制（NMS）
4. 双阈值检测（高阈值/低阈值）
5. 边缘连接（滞后阈值跟踪）

## 三、特征提取

### SIFT (Scale-Invariant Feature Transform)

步骤：
1. 尺度空间极值检测：$L(x,y,\sigma) = G(x,y,\sigma) * I(x,y)$
2. 关键点定位
3. 方向分配
4. 局部描述子生成（128维向量）

### HOG (Histogram of Oriented Gradients)

将图像划分为cells，每个cell计算梯度方向直方图，多个cells组合成block并归一化：

$$
v_{\text{norm}} = \frac{v}{\sqrt{||v||_2^2 + \epsilon^2}}
$$

## 四、图像分类与CNN

### 卷积神经网络核心组件

**卷积层**：使用可学习卷积核提取特征

$$
Y(i,j) = \sum_{m} \sum_{n} X(i+m, j+n) \cdot W(m,n) + b
$$

**池化层**：降低空间维度，保持平移不变性
- 最大池化：$Y(i,j) = \max_{m,n} X(i \cdot s + m, j \cdot s + n)$
- 平均池化：$Y(i,j) = \frac{1}{k^2} \sum_{m,n} X(i \cdot s + m, j \cdot s + n)$

**全连接层**：将提取的特征映射到输出类别

### 经典架构对比

| 架构 | 提出年份 | 特点 | 关键创新 |
|-----|---------|------|---------|
| AlexNet | 2012 | 5 conv + 3 FC | ReLU、Dropout、GPU训练 |
| VGG | 2014 | 16/19层 | 小卷积核（3×3）堆叠 |
| ResNet | 2015 | 152层 | 残差连接 $F(x) + x$ |
| Inception | 2014 | 并行多尺度 | Inception模块 |
| MobileNet | 2017 | 轻量级 | 深度可分离卷积 |

### 残差连接

ResNet的核心思想：学习残差映射而非直接映射

$$
\mathcal{F}(x) = \mathcal{H}(x) - x \quad \Rightarrow \quad \mathcal{H}(x) = \mathcal{F}(x) + x
$$

## 五、目标检测

### 两阶段检测器 (R-CNN系列)

1. **R-CNN**：Selective Search生成候选区域 → CNN提取特征 → SVM分类
2. **Fast R-CNN**：整图CNN + RoI Pooling
3. **Faster R-CNN**：RPN (Region Proposal Network) 端到端训练

### 单阶段检测器

**YOLO (You Only Look Once)**：将检测视为回归问题

$$
\text{输出张量} = S \times S \times (B \times 5 + C)
$$

其中 $S$ 为网格数，$B$ 为边界框数，$C$ 为类别数。

**SSD (Single Shot Multibox Detector)**：
- 多尺度特征图检测
- 预定义默认框（default boxes）
- 速度较快但小目标检测精度低于两阶段方法

### 损失函数

$$
\mathcal{L} = \mathcal{L}_{\text{cls}} + \lambda \mathcal{L}_{\text{loc}}
$$

$$
\mathcal{L}_{\text{loc}} = \sum_{i \in \text{pos}} \text{smooth}_{L1}(t_i - t_i^*)
$$

## 六、语义分割

### FCN (Fully Convolutional Network)

将CNN的全连接层替换为卷积层，实现像素级分类：

$$
\text{FCN-32s} \rightarrow \text{FCN-16s} \rightarrow \text{FCN-8s} \ (\text{逐步细化})
$$

### U-Net

对称的编码器-解码器结构，跳跃连接保留空间信息：

$$
\text{特征图尺寸: } H \times W \xrightarrow{\text{下采样}} \frac{H}{2} \times \frac{W}{2} \xrightarrow{\text{上采样}} H \times W
$$

## 七、生成模型

### 生成对抗网络 (GAN)

生成器 $G$ 与判别器 $D$ 的极小极大博弈：

$$
\min_G \max_D V(D,G) = \mathbb{E}_{x \sim p_{\text{data}}}[\log D(x)] + \mathbb{E}_{z \sim p_z}[\log(1 - D(G(z)))]
$$

### 图像生成应用

- **DCGAN**：CNN架构的GAN
- **Pix2Pix**：条件GAN用于图像翻译
- **CycleGAN**：无配对图像翻译
- **StyleGAN**：高质量人脸生成

## 八、三维视觉

### 立体匹配

通过左右视图的视差计算深度：

$$
\text{视差 } d = x_L - x_R, \quad \text{深度 } Z = \frac{f \cdot B}{d}
$$

其中 $f$ 为焦距，$B$ 为基线距离。

### 运动恢复结构 (Structure from Motion)

从多视图图像序列同时恢复3D结构和相机位姿：
1. 特征匹配（SIFT）
2. 本质矩阵估计
3. 三角化
4. 全局优化（Bundle Adjustment）

## 九、应用场景

| 应用领域 | 具体任务 | 代表技术 |
|---------|---------|---------|
| 自动驾驶 | 目标检测、车道线检测、语义分割 | YOLO、FCN |
| 医学影像 | 病灶检测、器官分割、病理分析 | U-Net、ResNet |
| 工业质检 | 缺陷检测、尺寸测量 | CNN分类、分割 |
| 安防监控 | 人脸识别、行人重识别 | FaceNet、ResNet |
| 增强现实 | SLAM、姿态估计 | ORB-SLAM、PnP |
| 遥感分析 | 地物分类、变化检测 | 语义分割、Transformer |

## 十一、GPT Image 2（2026前沿图像生成模型）

### 11.1 概述

GPT Image 2 是 OpenAI 于2026年4月发布的第二代专用图像生成模型（模型ID：`gpt-image-2`），是 `gpt-image-1` 的直接继任者，也是 ChatGPT "Images 2.0" 功能背后的核心模型。与 DALL-E 3 和 GPT-5 的图像生成能力不同，GPT Image 2 是一个专用、可嵌入工作流的图像生成模型。

### 11.2 核心能力

| 能力 | 说明 |
|------|------|
| **多语言文字渲染** | 近乎完美地在图像中渲染英文、中文、日文、韩文等文本 |
| **1K-4K 输出** | 支持 1K、2K、4K 三档分辨率，横屏/竖屏/超宽屏多比例 |
| **参考图像编辑** | 支持最多 16 张参考图像的上下文感知编辑 |
| **推理前置** | 生成前先进行简短推理，减少提示工程需求 |
| **高保真输入** | 自动对所有输入图像保持高保真处理 |

### 11.3 技术规格

| 参数 | 值 |
|------|-----|
| 发布日 | 2026-04-21 |
| 模型 ID | `gpt-image-2` |
| 输入 | 文本（提示语）+ 图像（可选） |
| 输出 | 图像 |
| API端点 | `/v1/images/generations`、`/v1/responses` |
| 分辨率 | 1K、2K、4K（方形/横屏/竖屏/超宽屏） |
| 参考图像上限 | 16 张 |
| 快照版本 | `gpt-image-2-2026-04-21` |

**定价**（2026年4月官方）：

| 项目 | 价格 |
|------|------|
| 文本输入 | $5.00 / 1M tokens |
| 图像输入 | $8.00 / 1M tokens |
| 图像输出 | $30.00 / 1M tokens |
| 缓存文本输入 | $1.25 / 1M tokens |
| 缓存图像输入 | $2.00 / 1M tokens |

按质量与尺寸估算单张价格：
| 质量 | 1K | 2K | 4K |
|------|-----|-----|-----|
| 低 | $0.006 | $0.005 | $0.005 |
| 中 | $0.053 | $0.041 | $0.041 |
| 高 | $0.211 | $0.165 | $0.165 |

### 11.4 与 DALL-E 3、GPT-5 图像生成的对比

| 维度 | GPT Image 2 | DALL-E 3 | GPT-5 图像生成 |
|------|-------------|----------|---------------|
| 模型定位 | 专用生成模型 | 旧代文本到图像 | 多模态对话生成 |
| 文本渲染 | 近乎完美（含CJK） | 较差（文字扭曲） | 较好 |
| 分辨率 | 最高4K | 最高1792×1024 | 取决于对话上下文 |
| 编辑能力 | 16张参考图像编辑 | 基础编辑 | 多轮对话编辑 |
| 适用场景 | 生产型工作流 | 快速创意生成 | 多轮对话式创作 |

## 相关条目

- [[ImageProcessing]]
- [[05_ComputerScience/ArtificialIntelligence/MachineLearning/INDEX|MachineLearning]]
- [[ComputerGraphics]]
- [[Robotics]]

## 参考资源

- Goodfellow, I. et al. (2016). *Deep Learning* (Chapter 9: Convolutional Networks)
- Szeliski, R. (2010). *Computer Vision: Algorithms and Applications*
- Krizhevsky, A. et al. (2012). "ImageNet Classification with Deep Convolutional Neural Networks"
- He, K. et al. (2016). "Deep Residual Learning for Image Recognition"
- Ren, S. et al. (2015). "Faster R-CNN: Towards Real-Time Object Detection with Region Proposal Networks"
- Redmon, J. et al. (2016). "You Only Look Once: Unified, Real-Time Object Detection"
