# 神经网络与深度学习

## 一、生物启发与理论基础

神经网络受生物神经系统启发，由大量相互连接的人工神经元组成。

### 感知机 (Perceptron)

单层感知机是最简单的神经网络单元：

$$
y = f\left(\sum_{i=1}^n w_i x_i + b\right)
$$

其中 $f$ 为激活函数，早期使用阶跃函数 $f(x) = \mathbb{1}(x > 0)$。

### 多层感知机 (MLP)

通过引入隐藏层和非线性激活函数，MLP可以学习复杂非线性映射：

$$
\mathbf{h}^{(1)} = \sigma_1(\mathbf{W}^{(1)}\mathbf{x} + \mathbf{b}^{(1)})
$$
$$
\mathbf{h}^{(2)} = \sigma_2(\mathbf{W}^{(2)}\mathbf{h}^{(1)} + \mathbf{b}^{(2)})
$$
$$
\hat{\mathbf{y}} = \sigma_L(\mathbf{W}^{(L)}\mathbf{h}^{(L-1)} + \mathbf{b}^{(L)})
$$

## 二、激活函数

| 函数 | 表达式 | 优点 | 缺点 |
|------|--------|------|------|
| Sigmoid | $\sigma(x) = \frac{1}{1+e^{-x}}$ | 平滑，输出[0,1] | 梯度消失，非零中心 |
| Tanh | $\tanh(x) = \frac{e^x - e^{-x}}{e^x + e^{-x}}$ | 零中心 | 梯度消失 |
| ReLU | $\text{ReLU}(x) = \max(0, x)$ | 简单，无梯度消失 | Dead ReLU |
| LeakyReLU | $\max(\alpha x, x), \alpha \approx 0.01$ | 缓解Dead ReLU | 超参数\alpha |
| GELU | $x \cdot \Phi(x)$ | 平滑ReLU | 计算稍复杂 |
| Swish | $x \cdot \sigma(x)$ | 自门控 | 计算代价 |

### ReLU的变体

**ELU**: 

$$
\text{ELU}(x) = \begin{cases} x & x > 0 \\ \alpha(e^x - 1) & x \leq 0 \end{cases}
$$

**PReLU**: 带可学习参数的LeakyReLU

## 三、反向传播

反向传播（Backpropagation）是训练神经网络的核心算法，基于链式法则计算梯度。

### 链式法则

对于复合函数 $L = f(g(h(x)))$：

$$
\frac{\partial L}{\partial x} = \frac{\partial L}{\partial f} \cdot \frac{\partial f}{\partial g} \cdot \frac{\partial g}{\partial h} \cdot \frac{\partial h}{\partial x}
$$

### 梯度计算

对于损失 $L$、权重 $w$、激活 $z = w^T x + b$、输出 $\hat{y} = \sigma(z)$：

$$
\frac{\partial L}{\partial w} = \frac{\partial L}{\partial \hat{y}} \cdot \frac{\partial \hat{y}}{\partial z} \cdot \frac{\partial z}{\partial w}
$$

### 梯度消失与爆炸

深层网络中梯度可能指数级衰减或增长：

$$
\frac{\partial L}{\partial \mathbf{W}^{(1)}} \propto \prod_{i=2}^L \frac{\partial \mathbf{h}^{(i)}}{\partial \mathbf{h}^{(i-1)}}
$$

缓解方法：适当的初始化（Xavier、He初始化）、Batch Normalization、残差连接。

## 四、优化器

### 梯度下降变体

| 优化器 | 更新规则 | 核心思想 |
|--------|---------|---------|
| SGD | $\theta_{t+1} = \theta_t - \eta \nabla L(\theta_t)$ | 标准梯度下降 |
| Momentum | $v_t = \gamma v_{t-1} + \eta \nabla L(\theta_t)$ | 加速收敛，冲过局部极小 |
| NAG | $v_t = \gamma v_{t-1} + \eta \nabla L(\theta_t - \gamma v_{t-1})$ | 前瞻更新 |
| AdaGrad | $\theta_{t+1} = \theta_t - \frac{\eta}{\sqrt{G_t + \epsilon}} \nabla L(\theta_t)$ | 自适应学习率 |
| RMSprop | $\theta_{t+1} = \theta_t - \frac{\eta}{\sqrt{v_t + \epsilon}} \nabla L(\theta_t)$ | 缓解AdaGrad学习率归零 |
| Adam | $m_t, v_t$ 一阶/二阶动量估计 | 最常用默认优化器 |

### Adam优化器

$$
m_t = \beta_1 m_{t-1} + (1 - \beta_1) g_t
$$
$$
v_t = \beta_2 v_{t-1} + (1 - \beta_2) g_t^2
$$
$$
\hat{m}_t = \frac{m_t}{1 - \beta_1^t}, \quad \hat{v}_t = \frac{v_t}{1 - \beta_2^t}
$$
$$
\theta_{t+1} = \theta_t - \frac{\eta}{\sqrt{\hat{v}_t} + \epsilon} \hat{m}_t
$$

## 五、正则化

### L1/L2正则化

**L2正则化**（权重衰减）：

$$
\tilde{J}(\theta) = J(\theta) + \frac{\lambda}{2} ||\mathbf{W}||_2^2
$$

**L1正则化**（稀疏性）：

$$
\tilde{J}(\theta) = J(\theta) + \lambda ||\mathbf{W}||_1
$$

### Dropout

训练时以概率 $p$ 随机丢弃神经元：

$$
\mathbf{h}_{\text{drop}} = \mathbf{h} \odot \mathbf{m}, \quad m_i \sim \text{Bernoulli}(p)
$$

测试时使用全部神经元，输出乘以 $p$ 保持期望一致。

### Batch Normalization

对每个mini-batch进行标准化：

$$
\mu_B = \frac{1}{m} \sum_{i=1}^m x_i, \quad \sigma_B^2 = \frac{1}{m} \sum_{i=1}^m (x_i - \mu_B)^2
$$
$$
\hat{x}_i = \frac{x_i - \mu_B}{\sqrt{\sigma_B^2 + \epsilon}}, \quad y_i = \gamma \hat{x}_i + \beta
$$

### 其他正则化方法

- **Early Stopping**：验证集性能不再提升时停止训练
- **数据增强 (Data Augmentation)**：随机变换增加训练数据多样性
- **Label Smoothing**：软标签替代硬标签
- **Mixup**：样本插值增强

## 六、卷积神经网络 (CNN)

### 卷积层

卷积操作提取局部空间特征：

$$
Y(i,j) = \sum_{m=0}^{K-1} \sum_{n=0}^{K-1} X(i+m, j+n) \cdot W(m,n) + b
$$

### 经典CNN架构

| 架构 | 深度 | 参数量 | 创新点 |
|------|------|--------|--------|
| LeNet-5 | 5 | 60K | 首个CNN，手写数字识别 |
| AlexNet | 8 | 60M | ReLU、Dropout、GPU并行 |
| VGG-16 | 16 | 138M | 3×3小卷积核堆叠 |
| ResNet-50 | 50 | 25.6M | 残差学习 |
| DenseNet | 121 | 8M | 密集连接 |
| EfficientNet | - | 5.3M-66M | 复合缩放 |

## 七、循环神经网络 (RNN)

### RNN

$$
\mathbf{h}_t = \tanh(\mathbf{W}_{hh} \mathbf{h}_{t-1} + \mathbf{W}_{xh} \mathbf{x}_t + \mathbf{b}_h)
$$

### LSTM (Long Short-Term Memory)

LSTM通过门控机制解决长期依赖问题：

$$
\mathbf{i}_t = \sigma(\mathbf{W}_i [\mathbf{h}_{t-1}, \mathbf{x}_t] + \mathbf{b}_i)
$$
$$
\mathbf{f}_t = \sigma(\mathbf{W}_f [\mathbf{h}_{t-1}, \mathbf{x}_t] + \mathbf{b}_f)
$$
$$
\mathbf{o}_t = \sigma(\mathbf{W}_o [\mathbf{h}_{t-1}, \mathbf{x}_t] + \mathbf{b}_o)
$$

### GRU (Gated Recurrent Unit)

简化LSTM，合并遗忘门和输入门。

## 八、注意力机制与Transformer

### Scaled Dot-Product Attention

$$
\text{Attention}(Q, K, V) = \text{softmax}\left(\frac{QK^T}{\sqrt{d_k}}\right)V
$$

### Transformer

$$
\text{MultiHead}(Q, K, V) = \text{Concat}(\text{head}_1, ..., \text{head}_h) W^O
$$

Transformer架构已成为NLP和CV领域的主流架构。

## 九、生成模型

### VAE (变分自编码器)

$$
\mathcal{L}_{\text{VAE}} = \mathbb{E}_{z \sim q_\phi(z|x)}[\log p_\theta(x|z)] - D_{\text{KL}}(q_\phi(z|x) || p(z))
$$

### GAN (生成对抗网络)

$$
\min_G \max_D V(D,G) = \mathbb{E}_{x \sim p_{\text{data}}}[\log D(x)] + \mathbb{E}_{z \sim p_z}[\log(1 - D(G(z)))]
$$

## 十、训练与部署技术

| 技术 | 描述 | 效果 |
|------|------|------|
| 混合精度训练 | FP16 + FP32混合 | 加速2-3x，显存减半 |
| 梯度累积 | 多步梯度累加 | 突破batch size限制 |
| 分布式训练 | 数据并行/模型并行 | 多GPU/多机扩展 |
| 模型量化 | INT8/FP16推理 | 加速推理，减小模型 |
| 知识蒸馏 | 大模型教小模型 | 保持性能同时压缩 |
| 剪枝 (Pruning) | 移除冗余参数 | 模型瘦身 |
| 梯度检查点 | 时间换空间 | 训练超大模型 |

### 硬件加速对比

| 硬件 | 适用场景 | 特点 |
|------|---------|------|
| GPU (NVIDIA) | 训练与推理 | CUDA生态成熟 |
| TPU (Google) | 大模型训练 | MXU矩阵加速 |
| IPU (Graphcore) | 图计算 | 灵活并行 |
| NPU (华为) | 推理加速 | 低功耗，高吞吐 |
| 神经形态芯片 | 脉冲神经网络 | 超低功耗 |

## 相关条目

- [[SupervisedLearning]]
- [[ComputerVision]]
- [[NaturalLanguageProcessing]]
- Backpropagation

## 参考资源

- Goodfellow, I. et al. (2016). *Deep Learning*
- LeCun, Y. et al. (2015). "Deep learning" (Nature)
- He, K. et al. (2016). "Deep Residual Learning for Image Recognition"
- Vaswani, A. et al. (2017). "Attention Is All You Need"
- Kingma, D. P. & Ba, J. (2015). "Adam: A Method for Stochastic Optimization"
- Ioffe, S. & Szegedy, C. (2015). "Batch Normalization: Accelerating Deep Network Training"
