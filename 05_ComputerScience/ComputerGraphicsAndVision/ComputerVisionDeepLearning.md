---
aliases: [ComputerVisionDeepLearning]
tags: ['ComputerGraphicsAndVision', 'ComputerVisionDeepLearning']
created: 2026-05-16
updated: 2026-05-16
---

# 深度学习计算机视觉

## 概述

深度学习极大地推动了计算机视觉的发展。从 AlexNet 在 2012 年 ImageNet 上的突破开始，CNN 架构不断演进，Transformer 架构的引入更是开启了视觉领域的新时代。本章系统梳理图像分类、目标检测、分割、生成等核心任务及其代表性方法。

---

## 一、图像分类

### 1.1 CNN 架构演进

| 模型 | 年份 | 参数量 | Top-1 准确率 (ImageNet) | 核心创新 |
|------|------|--------|------------------------|----------|
| AlexNet | 2012 | 60M | 56.5% | ReLU, Dropout, GPU 训练 |
| VGG-16 | 2014 | 138M | 71.6% | 小卷积核堆叠 (3×3) |
| Inception v3 | 2015 | 24M | 78.1% | Inception 模块并行卷积 |
| ResNet-50 | 2015 | 25.6M | 76.0% | 残差连接 (Skip Connection) |
| DenseNet-121 | 2017 | 8M | 75.0% | 密集连接重用特征 |
| ResNeXt-101 | 2017 | 83.5M | 79.3% | 分组卷积 (Cardinality) |
| EfficientNet-B7 | 2019 | 66M | 84.4% | NAS 搜索复合缩放 |
| ConvNeXt | 2022 | 89M | 85.1% | 现代化纯 CNN 设计 |
| ViT-H | 2021 | 632M | 85.2% | 纯 Transformer |
| Swin-B | 2021 | 88M | 85.2% | 层级化窗口注意力 |

### 1.2 关键技术

```
残差连接:
  y = F(x) + x
  解决深层网络退化问题，使 100+ 层网络可训练

批归一化 (BatchNorm):
  ŷ = (x - μ) / √(σ² + ε) · γ + β
  加速收敛，允许更高学习率

注意力机制:
  Attention(Q, K, V) = softmax(QKᵀ / √d) V
  捕获全局依赖，CNN 替代或补充

数据增强:
  Random Crop, Flip, Rotation, Color Jitter
  Mixup, CutMix, RandAugment
```

---

## 二、目标检测

### 2.1 两阶段检测器 (Two-Stage)

```
R-CNN 系列演进:

R-CNN (2014):
  候选区域 (Selective Search) → 分类器 (SVM) → 框回归
  速度慢: 每张图 2000 个候选框

Fast R-CNN (2015):
  整图 CNN → RoI Pooling → 分类 + 回归
  速度显著提升

Faster R-CNN (2016):
  Region Proposal Network (RPN) 共享特征 → 端到端
  速度: 7 FPS

Mask R-CNN (2017):
  Faster R-CNN + RoI Align (双线性插值) + 分割分支
  同时做检测 + 实例分割
```

### 2.2 单阶段检测器 (One-Stage)

| 模型 | 年份 | 骨干 | mAP (COCO) | 特点 |
|------|------|------|-----------|------|
| YOLOv1 | 2016 | Darknet | — | 直接回归框 + 类别 |
| YOLOv3 | 2018 | Darknet-53 | 33.0 | 多尺度预测 + FPN |
| YOLOv5 | 2020 | CSPDarknet | 50.7 | 工程化最佳 |
| YOLOv8 | 2023 | CSPDarknet | 53.9 | 统一框架 (检测/分割/姿态) |
| SSD | 2016 | VGG | 31.2 | 多特征图预测 |
| RetinaNet | 2017 | ResNet+FPN | 40.8 | Focal Loss 解决正负样本不均衡 |

YOLO 核心思想：

```
输入图像 → 特征提取网络 → S×S 网格 → 每个网格预测 B 个框 + C 个类概率

损失函数:
  L = λ_box · L_box + λ_obj · L_obj + λ_cls · L_cls
  L_box: GIoU / CIoU 损失
  L_obj: 目标置信度损失 (BCE)
  L_cls: 类别损失 (BCE)
```

### 2.3 基于 Transformer 的检测

| 模型 | 方法 | mAP (COCO) | 特点 |
|------|------|-----------|------|
| DETR (2020) | Transformer Encoder-Decoder | 44.9 | 去除了 NMS 和 Anchor |
| Deformable DETR (2021) | 可变形注意力 | 46.9 | 收敛更快 |
| DINO (2022) | 对比去噪训练 | 52.1 | SOTA Transformer 检测器 |

---

## 三、语义分割

### 3.1 分割方法对比

| 方法 | 类型 | 核心思路 | mIoU (Cityscapes) |
|------|------|----------|-------------------|
| FCN (2015) | 全卷积 | 全卷积 + 跳跃连接 | 65.3 |
| U-Net (2015) | 编码-解码 | 对称编解码 + Skip Connection | 医学图像 SOTA |
| DeepLab v3+ (2018) | 空洞卷积 | Atrous Spatial Pyramid Pooling | 82.1 |
| PSPNet (2017) | 金字塔池化 | 多尺度池化融合 | 81.2 |
| SegFormer (2021) | Transformer | 层级 Transformer + MLP 解码器 | 84.0 |

U-Net 架构示意：

```
编码器 (下采样)              解码器 (上采样)
  ┌─────┐  ┌─────┐  ┌─────┐  ┌─────┐
  │ Conv │  │ Conv │  │ Conv │  │ Conv │
  │ ↓ 2×  │  │ ↓ 2×  │  │ ↑ 2×  │  │ ↑ 2×  │
  └──┬──┘  └──┬──┘  └──┬──┘  └──┬──┘
     └────────┼────────┘
          Skip Connection (特征拼接)
```

---

## 四、实例分割与姿态估计

### 4.1 实例分割

| 模型 | 方法 | 骨干 | mAP (COCO) |
|------|------|------|-----------|
| Mask R-CNN | Mask Head + Faster R-CNN | ResNeXt-101 | 38.9 |
| YOLACT | 单阶段 + Mask 原型 | ResNet-101 | 31.2 |
| SOLOv2 | 动态卷积 Mask | ResNeXt-101 | 39.7 |

### 4.2 姿态估计

| 类型 | 方法 | 核心思路 | 指标 |
|------|------|----------|------|
| 自顶向下 | Mask R-CNN + Keypoint Head | 先检测后估计 | AP 67.8 (COCO) |
| 自底向上 | OpenPose | 检测关键点 + 关联 PAF | AP 61.8 |
| 自顶向下 | HRNet | 高分辨率特征保持 | AP 77.0 |
| 回归方法 | RLE | 残差似然估计 | AP 75.4 |

OpenPose 核心：

```
PAF (Part Affinity Fields):
  编码肢体的方向和位置
  通过积分计算关键点关联概率
  二分图匹配 (匈牙利算法) 将关键点分配到个人
```

---

## 五、目标跟踪

| 方法 | 类型 | 核心思路 | 速度 |
|------|------|----------|------|
| SiamRPN | 孪生网络 | 模板匹配 + 区域提议 | 实时光 |
| SiamMask | 孪生网络 | 跟踪 + 分割 | 实时光 |
| TransT | Transformer | 特征融合代替互相关 | 实时光 |
| DeepSORT | 跟踪 + 重识别 | Kalman 滤波 + 匈牙利匹配 | 实时光 |

**多目标跟踪 (MOT) 流程：**

```
检测 (Detection) → 特征提取 (ReID) → 数据关联 (匈牙利/图匹配) → 轨迹更新 (Kalman)

评价指标:
  MOTA: 多目标跟踪准确率
  IDF1: 身份 F1 分数
  HOTA: 高阶跟踪准确率
```

---

## 六、视觉生成模型

### 6.1 生成对抗网络 (GAN)

| GAN 模型 | 年份 | 核心改进 |
|----------|------|----------|
| DCGAN | 2015 | 全卷积判别器/生成器 |
| Pix2Pix | 2017 | 条件 GAN + 图像翻译 |
| CycleGAN | 2017 | 循环一致性损失（无配对） |
| StyleGAN | 2019 | 风格解耦 + AdaIN，高质量人脸 |
| StyleGAN3 | 2021 | 等变改进，消除纹理伪影 |

### 6.2 扩散模型 (Diffusion Models)

Diffusion 模型通过正向加噪和逆向去噪生成图像：

```
正向过程 (Forward): x₀ → x₁ → ... → x_T (逐步加噪)
逆向过程 (Reverse): x_T → x_{T-1} → ... → x₀ (逐步去噪)

训练目标:
  L = E_{t, x₀, ε}[‖ε - ε_θ(x_t, t)‖²]

采样:
  DDPM: 逐步去噪 T 步
  DDIM: 加速采样 (跳步)
```

| 模型 | 年份 | 类别 | 特点 |
|------|------|------|------|
| DDPM | 2020 | 扩散模型 | 高斯加噪，高质量生成 |
| Stable Diffusion | 2022 | 潜在扩散模型 | 在潜空间扩散，高效 |
| DALL-E 3 | 2023 | 文本到图像 | 精确的文本理解 |
| Imagen | 2022 | 文本到图像 | 级联扩散 |

---

## 七、自监督学习 (Self-Supervised Learning)

| 方法 | 类型 | 核心思路 | 骨干 |
|------|------|----------|------|
| SimCLR | 对比学习 | 正负样本对比 (NT-Xent loss) | ResNet-50 |
| MoCo v3 | 对比学习 | 动量编码器 + 队列 | ViT |
| BYOL | 非对比 | 预测目标网络表示 (无需负样本) | ResNet-50 |
| MAE | 掩码重建 | 随机掩码 75% patches → 重建 | ViT |
| DINO | 知识蒸馏 | 自蒸馏 + 教师/学生 ViT | ViT |

**SimCLR 对比损失：**

$$L = -\log \frac{\exp(\text{sim}(z_i, z_j) / \tau)}{\sum_{k=1}^{2N} \mathbb{1}_{[k \neq i]} \exp(\text{sim}(z_i, z_k) / \tau)}$$

其中 $\text{sim}$ 为余弦相似度，$\tau$ 为温度系数。

---

## 八、视频理解

| 方法 | 架构 | 计算量 | 准确率 (Kinetics-400) |
|------|------|--------|---------------------|
| C3D | 3D Conv | 高 | 82.3 |
| I3D | 2D Conv + 光流 | 中 | 84.5 |
| SlowFast | 双路径 (Slow+Fast) | 中 | 87.0 |
| Video Swin Transformer | 3D Swin | 高 | 88.3 |
| TimeSformer | 时空分离注意力 | 高 | 86.5 |

**动作识别常用技巧：**

```
TSN (Temporal Segment Networks):
  将视频均匀分段 → 每段随机采样 → 分段预测 → 融合

TSM (Temporal Shift Module):
  沿时间维度移位通道 → 零额外计算实现时间建模
```

---

## 九、模型压缩与部署

| 技术 | 描述 | 效果 |
|------|------|------|
| 量化 (Quantization) | FP32 → INT8 | 4× 存储压缩，2-3× 加速 |
| 剪枝 (Pruning) | 移除不重要权重/通道 | 50%-90% 参数减少 |
| 知识蒸馏 (Distillation) | 教师模型指导学生模型 | 小模型接近大模型精度 |
| NAS | 自动搜索网络结构 | 自动优化速度-精度平衡 |

**部署框架：**

| 框架 | 支持平台 | 特点 |
|------|----------|------|
| TensorRT | NVIDIA GPU | FP16/INT8 优化，推理加速 |
| ONNX Runtime | CPU/GPU/移动端 | 跨框架互操作 |
| OpenVINO | Intel CPU/GPU/VPU | Intel 平台优化 |
| CoreML | Apple 设备 | iOS/macOS 优化 |
| NCNN | 移动端 CPU | 腾讯开源，轻量级 |

---

## 相关条目

- [[05_ComputerScience/ArtificialIntelligence/ComputerVision/ComputerVision|ComputerVision]]
- DeepLearning
- [[04_EngineeringAndTechnology/ElectronicsAndCommunications/SignalProcessing/ImageProcessing|ImageProcessing]]
- NeuralNetworks

## 参考资源

- 《Deep Learning》— Goodfellow, Bengio, Courville（第 9 章 CNN，第 12 章应用）
- 《动手学深度学习》— 李沐等
- CS231n: Convolutional Neural Networks for Visual Recognition (Stanford)
- Papers With Code (CV): https://paperswithcode.com/area/computer-vision
- PyTorch 官方 CV 教程: https://pytorch.org/tutorials/intermediate/torchvision_tutorial.html
- MMDetection: https://github.com/open-mmlab/mmdetection
- OpenCV 文档: https://docs.opencv.org


