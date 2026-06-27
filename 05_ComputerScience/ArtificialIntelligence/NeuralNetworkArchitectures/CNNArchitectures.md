---
aliases:
  - CNN
  - Convolutional Neural Network
  - LeNet
  - AlexNet
  - VGGNet
  - GoogLeNet
  - ResNet
tags:
  - deep-learning
  - cnn
  - computer-vision
  - image-classification
  - neural-network-architecture
created: 2026-06-27
updated: 2026-06-27
---

# CNN 架构演进

> **核心论文**:
> - LeCun Y, et al. "Gradient-based learning applied to document recognition." *Proceedings of the IEEE*, 1998.
> - Krizhevsky A, et al. "ImageNet Classification with Deep Convolutional Neural Networks." *NeurIPS 2012*.
> - He K, et al. "Deep Residual Learning for Image Recognition." *CVPR 2016*. arXiv:1512.03385

---

## 1. 历史背景

### 1.1 计算机视觉的挑战

计算机视觉的核心任务是让机器"看懂"图像。传统方法依赖手工特征 (如 SIFT, HOG)，存在以下问题：
- 特征工程耗时
- 泛化能力有限
- 无法处理复杂场景

### 1.2 神经网络的复兴

2012 年，AlexNet 在 ImageNet 竞赛中大幅领先传统方法，标志着深度学习在计算机视觉中的崛起。

---

## 2. 卷积操作基础

### 2.1 什么是卷积？

卷积是 CNN 的核心操作，通过滑动窗口提取局部特征：

$$(f * g)(x, y) = \sum_{i=-k}^{k} \sum_{j=-k}^{k} f(i, j) \cdot g(x-i, y-j)$$

在神经网络中，$f$ 是卷积核 (kernel)，$g$ 是输入图像。

### 2.2 卷积的关键参数

| 参数 | 说明 | 典型值 |
|------|------|--------|
| Kernel Size | 卷积核大小 | 3×3, 5×5 |
| Stride | 步长 | 1, 2 |
| Padding | 填充 | same, valid |
| Channels | 输出通道数 | 64, 128, 256 |

### 2.3 输出尺寸计算

$$\text{Output Size} = \frac{\text{Input Size} - \text{Kernel Size} + 2 \times \text{Padding}}{\text{Stride}} + 1$$

### 2.4 卷积的优势

1. **参数共享**: 同一个卷积核在整个图像上滑动
2. **局部连接**: 每个神经元只连接输入的一个局部区域
3. **平移等变性**: 物体在图像中移动，特征图相应移动

---

## 3. LeNet-5 (1998)

### 3.1 论文信息

- **作者**: Yann LeCun, Leon Bottou, Yoshua Bengio, Patrick Haffner
- **应用**: 手写数字识别 (MNIST)
- **意义**: 开创了卷积神经网络的先河

### 3.2 架构

```
输入: 32×32 灰度图像

Layer 1: Conv (5×5, 6 filters) → 28×28×6
Layer 2: AvgPool (2×2) → 14×14×6
Layer 3: Conv (5×5, 16 filters) → 10×10×16
Layer 4: AvgPool (2×2) → 5×5×16
Layer 5: FC (120)
Layer 6: FC (84)
Layer 7: Output (10, softmax)
```

### 3.3 关键创新

1. **卷积 + 池化**: 奠定了 CNN 的基本范式
2. **参数共享**: 大幅减少参数量
3. **局部感受野**: 模拟生物视觉系统

### 3.4 局限性

- 仅适用于小尺寸灰度图像
- 网络较浅 (7 层)
- 计算资源有限

---

## 4. AlexNet (2012)

### 4.1 论文信息

- **作者**: Alex Krizhevsky, Ilya Sutskever, Geoffrey Hinton
- **成就**: ImageNet 2012 冠军，top-5 错误率从 26% 降至 15.3%
- **意义**: 开启了深度学习时代

### 4.2 架构

```
输入: 224×224×3 RGB 图像

Layer 1: Conv (11×11, 96 filters, stride 4) → 55×55×96
         ReLU → MaxPool (3×3, stride 2) → 27×27×96

Layer 2: Conv (5×5, 256 filters, padding 2) → 27×27×256
         ReLU → MaxPool (3×3, stride 2) → 13×13×256

Layer 3: Conv (3×3, 384 filters, padding 1) → 13×13×384
         ReLU

Layer 4: Conv (3×3, 384 filters, padding 1) → 13×13×384
         ReLU

Layer 5: Conv (3×3, 256 filters, padding 1) → 13×13×256
         ReLU → MaxPool (3×3, stride 2) → 6×6×256

FC 1: 4096 neurons + ReLU + Dropout (0.5)
FC 2: 4096 neurons + ReLU + Dropout (0.5)
FC 3: 1000 neurons (softmax)
```

### 4.3 关键创新

1. **ReLU 激活函数**: 替代 tanh/sigmoid，解决梯度消失问题
$$\text{ReLU}(x) = \max(0, x)$$

2. **Dropout**: 随机丢弃神经元，防止过拟合
$$\text{Dropout}(x) = \begin{cases} 0 & \text{with probability } p \\ x/(1-p) & \text{otherwise} \end{cases}$$

3. **数据增强**: 水平翻转、随机裁剪、颜色抖动

4. **GPU 训练**: 使用两块 GTX 580 GPU 并行训练

5. **Local Response Normalization (LRN)**: 后来被 Batch Normalization 取代

### 4.4 历史意义

AlexNet 的成功证明了：
1. 深度神经网络的有效性
2. GPU 计算的潜力
3. 大规模数据的重要性
4. 深度学习时代正式开始

---

## 5. VGGNet (2014)

### 5.1 论文信息

- **作者**: Karen Simonyan, Andrew Zisserman
- **成就**: ImageNet 2014 亚军
- **意义**: 证明了网络深度的重要性

### 5.2 核心思想

使用多个 3×3 小卷积核替代大卷积核：

```
两个 3×3 卷积的感受野 = 一个 5×5 卷积
三个 3×3 卷积的感受野 = 一个 7×7 卷积
```

**优势**:
- 更多非线性层，更强的表示能力
- 更少的参数: $3 \times (3^2 C^2) < 7^2 C^2$

### 5.3 VGG-16 架构

```
输入: 224×224×3

Block 1:
  Conv3-64 × 2 → MaxPool → 112×112×64

Block 2:
  Conv3-128 × 2 → MaxPool → 56×56×128

Block 3:
  Conv3-256 × 3 → MaxPool → 28×28×256

Block 4:
  Conv3-512 × 3 → MaxPool → 14×14×512

Block 5:
  Conv3-512 × 3 → MaxPool → 7×7×512

FC 1: 4096 + ReLU + Dropout
FC 2: 4096 + ReLU + Dropout
FC 3: 1000 (softmax)
```

### 5.4 VGG-16 vs VGG-19

| 模型 | 层数 | 参数量 | Top-5 错误率 |
|------|------|--------|--------------|
| VGG-16 | 16 | 138M | 7.3% |
| VGG-19 | 19 | 144M | 7.3% |

更深的网络不一定带来显著提升，但 VGG 证明了可以训练很深的网络。

### 5.5 影响

1. **小卷积核成为标准**: 3×3 卷积成为主流
2. **模块化设计**: 网络由重复的 block 组成
3. **特征提取器**: VGG 的预训练模型广泛用于迁移学习

---

## 6. GoogLeNet / Inception (2014)

### 6.1 论文信息

- **作者**: Christian Szegedy et al. (Google)
- **成就**: ImageNet 2014 冠军
- **创新**: Inception 模块，更高效的网络结构

### 6.2 Inception 模块

核心思想：在同一层中并行使用不同大小的卷积核：

```
输入
  │
  ├── 1×1 Conv ─────────────────────┐
  │                                 │
  ├── 1×1 Conv → 3×3 Conv ─────────┤
  │                                 │
  ├── 1×1 Conv → 5×5 Conv ─────────┤
  │                                 │
  └── 3×3 MaxPool → 1×1 Conv ──────┤
                                    │
                                    ▼
                              Concat (沿通道维度)
```

### 6.3 1×1 卷积的作用

1×1 卷积看似无用，实则关键：

1. **降维/升维**: 改变通道数
2. **增加非线性**: 后接 ReLU 激活
3. **跨通道交互**: 融合不同通道的信息

**计算量对比**:
- 不使用 1×1 卷积: $C_{in} \times 5^2 \times C_{out}$
- 使用 1×1 卷积降维: $C_{in} \times 1^2 \times C_{mid} + C_{mid} \times 5^2 \times C_{out}$

当 $C_{mid} \ll C_{in}$ 时，计算量大幅减少。

### 6.4 GoogLeNet 架构

```
输入: 224×224×3

Conv 7×7 (64) → MaxPool → 112×112×64
Conv 1×1 (64) + Conv 3×3 (192) → MaxPool → 56×56×192

Inception 3a → 28×28×256
Inception 3b → 28×28×480
MaxPool → 14×14×480

Inception 4a → 14×14×512
Inception 4b → 14×14×512
Inception 4c → 14×14×512
Inception 4d → 14×14×528
Inception 4e → 14×14×832
MaxPool → 7×7×832

Inception 5a → 7×7×832
Inception 5b → 7×7×1024

Global Average Pool → 1×1×1024
FC → 1000 (softmax)
```

### 6.5 关键创新

1. **Network in Network**: 多尺度特征提取
2. **1×1 卷积**: 降维减少计算量
3. **Global Average Pooling**: 替代全连接层，减少参数
4. **辅助分类器**: 缓解梯度消失问题

### 6.6 参数效率

| 模型 | 参数量 | Top-5 错误率 |
|------|--------|--------------|
| AlexNet | 60M | 15.3% |
| VGG-16 | 138M | 7.3% |
| GoogLeNet | **6.8M** | 6.7% |

GoogLeNet 的参数量仅为 VGG 的 1/20，性能更好！

---

## 7. ResNet (2015)

### 7.1 论文信息

- **作者**: Kaiming He, Xiangyu Zhang, Shaoqing Ren, Jian Sun (Microsoft Research)
- **成就**: ImageNet 2015 冠军，top-3.57% 错误率
- **意义**: 解决了深度网络的退化问题，使得训练超深网络成为可能

### 7.2 退化问题 (Degradation Problem)

理论上，更深的网络应该至少不比浅网络差（多出来的层可以学习恒等映射）。但实际上：

```
网络深度增加 → 训练误差先降后升
                    ↑
            这不是过拟合！
            (训练误差也上升)
```

**问题本质**: 优化困难，不是过拟合。

### 7.3 残差学习 (Residual Learning)

**核心思想**: 让网络学习残差函数 $F(x) = H(x) - x$，而非直接学习 $H(x)$。

$$H(x) = F(x) + x$$

**直觉**: 学习恒等映射 $F(x) = 0$ 比学习 $H(x) = x$ 更容易。

### 7.4 Skip Connection (跳跃连接)

```
输入 x
  │
  ├────────────────────────┐
  │                        │
  ▼                        │
  Conv → BN → ReLU         │
  │                        │
  ▼                        │
  Conv → BN                │
  │                        │
  ▼                        │
  + ← ────────────────────┘ (残差连接)
  │
  ▼
  ReLU
  │
  ▼
输出
```

### 7.5 残差块 (Residual Block)

**Basic Block** (用于 ResNet-18, ResNet-34):

$$y = F(x, \{W_i\}) + x$$

$$F = W_2 \sigma(W_1 x)$$

其中 $\sigma$ 是 ReLU，$W_1, W_2$ 是卷积层。

**Bottleneck Block** (用于 ResNet-50, ResNet-101, ResNet-152):

```
输入 (256-d)
  │
  ├────────────────────────────┐
  │                            │
  ▼                            │
  1×1 Conv (64) → BN → ReLU   │
  │                            │
  ▼                            │
  3×3 Conv (64) → BN → ReLU   │
  │                            │
  ▼                            │
  1×1 Conv (256) → BN          │
  │                            │
  ▼                            │
  + ← ────────────────────────┘
  │
  ▼
  ReLU
```

**参数量对比**:
- Basic Block: $2 \times 3^2 \times C^2 = 18C^2$
- Bottleneck Block: $1^2 \times C \times C/4 + 3^2 \times (C/4)^2 + 1^2 \times C/4 \times C \approx 12.5C^2$

### 7.6 ResNet 架构

| 模型 | 层数 | 结构 | 参数量 |
|------|------|------|--------|
| ResNet-18 | 18 | [2,2,2,2] Basic | 11.7M |
| ResNet-34 | 34 | [3,4,6,3] Basic | 21.8M |
| ResNet-50 | 50 | [3,4,6,3] Bottleneck | 25.6M |
| ResNet-101 | 101 | [3,4,23,3] Bottleneck | 44.5M |
| ResNet-152 | 152 | [3,8,36,3] Bottleneck | 60.2M |

### 7.7 为什么 ResNet 能训练很深的网络？

**数学分析**:

对于 L 层 ResNet:

$$x_L = x_0 + \sum_{i=0}^{L-1} F(x_i)$$

梯度从第 L 层传到第 l 层:

$$\frac{\partial \mathcal{L}}{\partial x_l} = \frac{\partial \mathcal{L}}{\partial x_L} \cdot \left(1 + \frac{\partial}{\partial x_l} \sum_{i=l}^{L-1} F(x_i)\right)$$

关键点: 梯度中始终有一个 "1"，确保梯度不会消失！

### 7.8 ResNet 的影响

1. **深度突破**: 从几十层扩展到上千层
2. **残差学习成为标准**: 几乎所有现代网络都使用
3. **迁移学习**: ResNet 预训练模型广泛使用
4. **启发了后续工作**: DenseNet, EfficientNet 等

---

## 8. 其他重要 CNN 架构

### 8.1 Batch Normalization (Ioffe & Szegedy, 2015)

对每个 mini-batch 进行归一化:

$$\hat{x}_i = \frac{x_i - \mu_B}{\sqrt{\sigma_B^2 + \epsilon}}$$

$$y_i = \gamma \hat{x}_i + \beta$$

**效果**:
- 加速训练
- 允许更大的学习率
- 有一定的正则化效果

### 8.2 DenseNet (2017)

每层与前面所有层连接:

$$x_l = H_l([x_0, x_1, ..., x_{l-1}])$$

**优势**: 特征复用，缓解梯度消失

### 8.3 MobileNet (2017)

使用 Depthwise Separable Convolution:

```
标准卷积: D_K × D_K × M × N 参数
Depthwise Separable: D_K × D_K × M + M × N 参数

计算量减少: 1/N + 1/D_K^2
```

### 8.4 EfficientNet (2019)

使用 Neural Architecture Search 找到最优的复合缩放:

$$\text{depth}: d = \alpha^\phi$$
$$\text{width}: w = \beta^\phi$$
$$\text{resolution}: r = \gamma^\phi$$

约束: $\alpha \cdot \beta^2 \cdot \gamma^2 \approx 2$

---

## 9. CNN 在其他视觉任务中的应用

### 9.1 目标检测

**Two-stage Detectors**:
- **R-CNN (2014)**: Region proposals + CNN features
- **Fast R-CNN (2015)**: Shared feature maps
- **Faster R-CNN (2015)**: Region Proposal Network (RPN)

**One-stage Detectors**:
- **YOLO (2016)**: You Only Look Once，实时检测
- **SSD (2016)**: Multi-scale feature maps

### 9.2 语义分割

**FCN (2015)**: 全卷积网络，端到端像素级分类

**U-Net (2015)**: Encoder-Decoder + Skip Connections

```
Encoder (下采样):          Decoder (上采样):
┌─────────────┐           ┌─────────────┐
│ Conv Block  │           │ UpConv      │
│     ↓       │   skip    │     ↓       │
│ Conv Block  │ ────────→ │ Concat      │
│     ↓       │           │     ↓       │
│ Conv Block  │ ────────→ │ Conv Block  │
│     ↓       │           │     ↓       │
│ Conv Block  │ ────────→ │ Conv Block  │
└─────────────┘           └─────────────┘
```

### 9.3 图像生成

**GAN (2014)**: Generator + Discriminator 都使用 CNN

**StyleGAN (2019)**: 高质量人脸生成

### 9.4 图像分割

**Mask R-CNN (2017)**: 在 Faster R-CNN 基础上增加 mask 分支

---

## 10. CNN 的数学基础

### 10.1 卷积定理

时域卷积 = 频域乘积:

$$\mathcal{F}\{f * g\} = \mathcal{F}\{f\} \cdot \mathcal{F}\{g\}$$

这使得可以通过 FFT 加速卷积计算。

### 10.2 感受野计算

第 l 层的感受野:

$$RF_l = RF_{l-1} + (k_l - 1) \times \prod_{i=1}^{l-1} s_i$$

其中 $k_l$ 是卷积核大小，$s_i$ 是步长。

### 10.3 参数量计算

对于卷积层:

$$\text{Params} = C_{in} \times C_{out} \times K_h \times K_w + C_{out}$$

对于全连接层:

$$\text{Params} = C_{in} \times C_{out} + C_{out}$$

---

## 11. CNN vs Vision Transformer

### 11.1 对比

| 特性 | CNN | ViT |
|------|-----|-----|
| 归纳偏置 | 局部性、平移等变性 | 无（需大数据学习） |
| 数据效率 | 小数据表现好 | 需要大规模预训练 |
| 计算复杂度 | $O(n \cdot k^2 \cdot c^2)$ | $O(n^2 \cdot d)$ |
| 长距离依赖 | 需要多层堆叠 | 单层即可 |

### 11.2 融合趋势

现代架构结合了 CNN 和 Transformer 的优点:
- **ConvNeXt**: 将 CNN "现代化"
- **Swin Transformer**: 局部窗口注意力
- **CoAtNet**: CNN + Transformer 混合

---

## 12. 关键论文列表

1. **LeCun Y, et al. (1998)**: LeNet-5，CNN 的奠基之作
2. **Krizhevsky A, et al. (2012)**: AlexNet，深度学习革命
3. **Simonyan K, Zisserman A (2014)**: VGGNet，深度很重要
4. **Szegedy C, et al. (2014)**: GoogLeNet，Inception 模块
5. **He K, et al. (2015)**: ResNet，残差学习
6. **Ioffe S, Szegedy C (2015)**: Batch Normalization
7. **Huang G, et al. (2017)**: DenseNet
8. **Howard A, et al. (2017)**: MobileNet
9. **Tan M, Le Q (2019)**: EfficientNet
10. **Dosovitskiy A, et al. (2020)**: Vision Transformer (ViT)

---

## 13. 总结

CNN 架构的演进历史:

```
LeNet (1998) → AlexNet (2012) → VGGNet (2014) → GoogLeNet (2014) → ResNet (2015) → ...
    │              │                │                │                │
    ↓              ↓                ↓                ↓                ↓
  开创者         突破者          深度化           效率化           残差学习
```

**核心趋势**:
1. **网络越来越深**: 从 7 层到 1000+ 层
2. **模块化设计**: 重复的 building block
3. **效率优化**: 1×1 卷积、深度可分离卷积
4. **归一化技术**: Batch Normalization
5. **残差连接**: 解决退化问题

CNN 的发展为计算机视觉带来了革命性变化，也为后来的 Vision Transformer 奠定了基础。

---

*最后更新: 2026-06-27*
