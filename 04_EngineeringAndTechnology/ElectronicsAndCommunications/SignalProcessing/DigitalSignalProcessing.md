---
aliases: [DigitalSignalProcessing]
tags: ['ElectronicsAndCommunications', 'SignalProcessing', 'DigitalSignalProcessing']
---

# 数字信号处理

## 定义
数字信号处理（DSP）是利用数字计算方法对离散时间信号进行分析、变换、滤波、检测和处理的理论与技术。

## 研究对象
- 采样与量化理论
- 离散时间信号与系统
- Z变换与离散傅里叶变换
- 数字滤波器设计

## 核心内容

### 采样定理

**奈奎斯特定理**：

$$f_s \geq 2f_{max}$$

$f_s$ 为采样频率，$f_{max}$ 为信号最高频率分量。

**混叠**：当 $f_s < 2f_{max}$ 时，高频分量折叠到低频区，产生失真。

**量化误差**：

$$e_q = x - Q(x), \quad |e_q| \leq \frac{\Delta}{2}$$

$\Delta = \frac{V_{pp}}{2^B}$ 为量化步长，$B$ 为量化位数。

**信噪比**：

$$SNR = 6.02B + 1.76 \text{ dB}$$

### 离散傅里叶变换（DFT/FFT）

**DFT定义**：

$$X(k) = \sum_{n=0}^{N-1} x(n)W_N^{kn}, \quad W_N = e^{-j2\pi/N}$$

**IDFT**：

$$x(n) = \frac{1}{N}\sum_{k=0}^{N-1} X(k)W_N^{-kn}$$

**FFT（快速傅里叶变换）**：
- 基2-FFT：$O(N\log_2 N)$ 复杂度
- Cooley-Tukey算法
- 应用：频谱分析、快速卷积

**频谱分辨率**：

$$\Delta f = \frac{f_s}{N}$$

### 数字滤波器

**FIR滤波器（有限脉冲响应）**：

$$y(n) = \sum_{k=0}^{M} b_k x(n-k)$$

- 线性相位：$b_k = b_{M-k}$
- 稳定性：始终稳定
- 设计方法：窗函数法、频率采样法、等波纹法

**IIR滤波器（无限脉冲响应）**：

$$y(n) = \sum_{k=0}^{M} b_k x(n-k) - \sum_{k=1}^{N} a_k y(n-k)$$

- 非线性相位
- 可能不稳定（极点在单位圆外）
- 设计方法：脉冲响应不变法、双线性变换法

**滤波器类型**：
- 低通滤波器（LPF）
- 高通滤波器（HPF）
- 带通滤波器（BPF）
- 带阻滤波器（BSF）

### Z变换

**定义**：

$$X(z) = \sum_{n=-\infty}^{\infty} x(n)z^{-n}$$

**收敛域（ROC）**：使 $X(z)$ 收敛的 $z$ 值范围

**基本性质**：
- 线性：$ax_1(n)+bx_2(n) \Leftrightarrow aX_1(z)+bX_2(z)$
- 时移：$x(n-n_0) \Leftrightarrow z^{-n_0}X(z)$
- 卷积：$x_1(n)*x_2(n) \Leftrightarrow X_1(z)X_2(z)$

**系统函数**：

$$H(z) = \frac{Y(z)}{X(z)} = \frac{\sum_{k=0}^{M} b_k z^{-k}}{1+\sum_{k=1}^{N} a_k z^{-k}}$$

### 信号频谱分析

**功率谱密度（PSD）**：

$$S_{xx}(f) = |X(f)|^2$$

**周期图法**：$\hat{S}_{xx}(f) = \frac{1}{N}|X(k)|^2$

**改进方法**：
- Bartlett法（平均周期图）
- Welch法（加窗+分段平均）

### 数字音频处理

**音频采样**：
- CD音质：44.1kHz采样，16bit量化
- 电话：8kHz采样，8bit量化

**音频编码**：
- PCM：脉冲编码调制
- ADPCM：自适应差分PCM
- MP3/AAC：感知音频编码

### 图像信号处理基础

**二维DFT**：

$$F(u,v) = \sum_{x=0}^{M-1}\sum_{y=0}^{N-1}f(x,y)e^{-j2\pi(ux/M+vy/N)}$$

**图像滤波**：
- 空间域滤波：卷积核
- 频域滤波：乘以滤波函数

## 经典教材
- 高西全《数字信号处理》
- Oppenheim《Discrete-Time Signal Processing》
- Proakis《Digital Signal Processing》
- Lyons《Understanding Digital Signal Processing》

## 主要应用领域
- 通信系统（调制解调、信道均衡）
- 音频处理（降噪、回声消除）
- 图像处理（压缩、增强）
- 雷达信号处理
- 语音识别
- 生物医学信号处理（ECG、EEG）

## 相关条目

- [[ImageProcessing]]
- [[CommunicationTheory]]
- [[AnalogElectronics]]
- [[DigitalElectronics]]
- [[ControlSystems]]
