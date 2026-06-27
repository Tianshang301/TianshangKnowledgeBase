---
aliases: [DigitalSignalProcessing, DSP, 数字信号处理, 信号处理]
tags: ['04_EngineeringAndTechnology', 'ElectronicsAndCommunications', 'SignalProcessing', 'DSP']
created: 2026-05-17
updated: 2026-05-16
---

# 数字信号处理概论

数字信号处理（Digital Signal Processing, DSP）是对数字化的信号进行分析、修改和合成的技术。DSP 将模拟信号（Analog Signal）通过模数转换器（ADC）转换为数字形式，利用数学算法进行处理，再将结果通过数模转换器（DAC）转换回模拟信号，或直接提取有用信息。DSP 广泛应用于音频处理（Audio Processing）、图像处理（Image Processing）、通信系统（Communication Systems）和生物医学工程（Biomedical Engineering）等领域。

## DSP 核心流程

```mermaid
graph LR
    A[模拟信号<br/>$x_a(t)$] --> B[抗混叠滤波器<br/>Anti-Aliasing Filter]
    B --> C[采样器<br/>$T_s$ 采样周期]
    C --> D[量化器<br/>$N$ 比特]
    D --> E[编码器<br/>二进制表示]
    E --> F[数字信号<br/>$x[n]$]
    F --> G[DSP 处理器]
    G --> H[数字信号<br/>$y[n]$]
    H --> I[DAC]
    I --> J[重构滤波器<br/>Reconstruction]
    J --> K[模拟输出<br/>$y_a(t)$]
```

## 采样理论与奈奎斯特定理 （Sampling Theorem）

采样定理（Nyquist-Shannon Sampling Theorem）规定：采样频率 $f_s$ 必须至少为信号最高频率分量 $f_{\max}$ 的两倍，才能从采样信号中无损重建原始信号：

$$ f_s \geq 2f_{\max} $$

满足该条件的频率称为奈奎斯特频率（Nyquist Frequency）：$ f_N = f_s / 2 $。若采样率不足，将发生**混叠**（Aliasing）现象，高频分量被错误地映射到低频。

### 采样过程数学描述

$$ x[n] = x_a(nT_s), \quad T_s = \frac{1}{f_s} $$

理想重建（使用 sinc 插值）：

$$ x_a(t) = \sum_{n=-\infty}^{\infty} x[n] \cdot \text{sinc}\left(\frac{t - nT_s}{T_s}\right) $$

其中 $\text{sinc}(x) = \sin(\pi x) / (\pi x)$。

## 量化与编码 （Quantization & Coding）

将连续幅值映射到有限个离散电平的过程。量化误差（Quantization Error）近似为均匀分布的白噪声：

$$ \text{SNR}_Q = 6.02N + 1.76 \;\text{dB} $$

其中 $N$ 为量化比特数。

| 量化比特数 | 量化电平数 | 理论 SNR | 应用场景 |
|:---:|:---:|:---:|:---|
| 8 | 256 | 49.9 dB | 语音通信 |
| 16 | 65536 | 98.1 dB | 音频 CD |
| 24 | 16777216 | 146.3 dB | 专业录音 |
| 32 | $4.3 \times 10^9$ | 194.4 dB | 高精度音频 |

## 傅里叶变换 （Fourier Transform）

### 离散时间傅里叶变换 （DTFT）

$$ X(e^{j\omega}) = \sum_{n=-\infty}^{\infty} x[n] e^{-j\omega n} $$

### 离散傅里叶变换 （DFT）

$$ X[k] = \sum_{n=0}^{N-1} x[n] e^{-j\frac{2\pi}{N}kn}, \quad k = 0, 1, \dots, N-1 $$

### 快速傅里叶变换 （FFT）

Cooley-Tukey 算法将 DFT 的计算复杂度从 $O(N^2)$ 降至 $O(N \log_2 N)$：

$$ N\text{-点 DFT} \xrightarrow{\text{分治}} 2 \times (N/2)\text{-点 DFT} + \text{蝶形运算} $$

```mermaid
graph TD
    subgraph FFT 蝶形运算
    A[x[0]] --> C[+]
    B[x[4]] --> D[× W_N^k]
    D --> E[-]
    C --> F[X[0]]
    E --> G[X[4]]
    end
```

## Z 变换 （Z-Transform）

Z 变换是离散信号和系统的复频域分析工具：

$$ X(z) = \sum_{n=-\infty}^{\infty} x[n] z^{-n}, \quad z = re^{j\omega} $$

传递函数：

$$ H(z) = \frac{Y(z)}{X(z)} = \frac{\sum_{k=0}^{M} b_k z^{-k}}{1 + \sum_{k=1}^{N} a_k z^{-k}} $$

### 零极点与稳定性

| 极点在 z 平面位置 | 系统响应特性 | 稳定性 |
|:---|:---|:---:|
| 单位圆内 | 衰减 | 稳定 |
| 单位圆上 | 等幅振荡 | 临界稳定 |
| 单位圆外 | 发散 | 不稳定 |

## 数字滤波器 （Digital Filters）

### FIR 滤波器 （Finite Impulse Response）

- 无反馈结构，响应有限
- 线性相位特性
- 设计方法：窗函数法、频率采样法、Parks-McClellan 算法

$$ y[n] = \sum_{k=0}^{M} b_k x[n-k] $$

### IIR 滤波器 （Infinite Impulse Response）

- 含反馈结构，响应无限延续
- 非线性相位，但有更好的频率选择性
- 设计方法：从模拟原型转换（Butterworth、Chebyshev、Elliptic）

$$ y[n] = \sum_{k=0}^{M} b_k x[n-k] - \sum_{k=1}^{N} a_k y[n-k] $$

### 滤波器对比

| 特性 | FIR | IIR |
|:---|:---|:---|
| 相位特性 | 严格线性相位 | 非线性相位 |
| 稳定性 | 始终稳定 | 需保证极点都在单位圆内 |
| 阶数需求 | 高（过渡带宽） | 低（过渡带窄） |
| 计算量 | 较大 | 较小 |
| 量化效应 | 不敏感 | 敏感 |

## 卷积 （Convolution）

线性卷积定义：

$$ (x * h)[n] = \sum_{k=-\infty}^{\infty} x[k] h[n-k] $$

圆周卷积（用于 DFT）定义：

$$ (x \circledast h)[n] = \sum_{k=0}^{N-1} x[k] h[(n-k) \bmod N] $$

### 卷积定理

时域卷积等于频域乘积：

$$ x[n] * h[n] \xrightarrow{\text{DFT}} X[k] \cdot H[k] $$

这一性质使 FFT 成为快速卷积的核心——计算复杂度由 $O(N^2)$ 降至 $O(N \log N)$。

## 窗函数 （Window Functions）

窗函数用于减少频谱泄漏（Spectral Leakage）——由有限长截断引起的能量扩散：

| 窗函数 | 主瓣宽度 | 最大旁瓣（dB） | 衰减速率（dB/octave） |
|:---|:---:|:---:|:---:|
| 矩形窗 | $2/N$ | -13 | 6 |
| Hanning 窗 | $4/N$ | -32 | 18 |
| Hamming 窗 | $4/N$ | -43 | 6 |
| Blackman 窗 | $6/N$ | -58 | 18 |
| Kaiser 窗 | 可调 | 可调 | — |
| Flat Top 窗 | $10/N$ | -80 | — |

Kaiser 窗通过参数 $\beta$ 在主瓣宽度和旁瓣衰减之间权衡：

$$ w[n] = \frac{I_0\left(\beta\sqrt{1 - \left(\frac{2n}{N-1} - 1\right)^2}\right)}{I_0(\beta)}, \quad 0 \leq n \leq N-1 $$

## 多速率信号处理 （Multirate DSP）

### 降采样 （Decimation）

$$ y[n] = x[nM] $$

降采样前需经低通滤波器防止混叠。

### 升采样 （Interpolation）

$$ y[n] = \begin{cases} x[n/L], & n = 0, \pm L, \pm 2L, \dots \\ 0, & \text{其他} \end{cases} $$

升采样后需经低通滤波器平滑插值。

### 采样率转换的应用

- 音频格式转换（44.1 kHz ↔ 48 kHz）
- 子带编码（Sub-band Coding）
- 多速率滤波器组（多载波通信中的滤波器组）
- $\Sigma$-$\Delta$ ADC 中的噪声整形

## 自适应滤波 （Adaptive Filtering）

自适应滤波器通过迭代算法自动调整系数，适用于未知或时变系统。

### LMS 算法 （Least Mean Squares）

$$ w[n+1] = w[n] + \mu e[n] x[n] $$

其中 $e[n]$ 为误差信号，$\mu$ 为步长参数（控制收敛速度和稳态误差的权衡）。

### 自适应滤波应用

| 应用 | 原理 | 场景 |
|:---|:---|:---|
| 主动噪声控制 | 产生反相声波抵消噪声 | 降噪耳机 |
| 回波消除 | 估计回波路径并减去 | 电话会议 |
| 系统辨识 | 自适应估计未知系统 | 信道估计 |
| 线谱增强 | 提取正弦波 | 生物医学信号 |
| 预测编码 | 预测当前值并编码残差 | 语音编码 |

## 小波变换 （Wavelet Transform）

小波变换提供时频域的多分辨率分析，克服了短时傅里叶变换（STFT）窗口固定的局限。

### 连续小波变换 （CWT）

$$ W(a,b) = \frac{1}{\sqrt{|a|}} \int_{-\infty}^{\infty} x(t) \psi^*\left(\frac{t-b}{a}\right) dt $$

### 离散小波变换 （DWT）

Mallat 算法通过滤波器组实现快速 DWT：

```mermaid
graph LR
    A[x[n]] --> B[低通<br/>h[n]]
    A --> C[高通<br/>g[n]]
    B --> D[↓2] --> E[近似系数 cA1]
    C --> F[↓2] --> G[细节系数 cD1]
    E --> H[低通] --> I[↓2] --> J[cA2]
    E --> K[高通] --> L[↓2] --> M[cD2]
```

### 小波应用

- JPEG 2000 图像压缩标准（使用 CDF 9/7 小波）
- ECG/EEG 信号去噪
- 地震数据压缩
- 湍流分析

## 谱分析 （Spectral Analysis）

### 周期图法 （Periodogram）

$$ P_{\text{per}}(f) = \frac{1}{N} \left| \sum_{n=0}^{N-1} x[n] e^{-j2\pi fn} \right|^2 $$

### Welch 法

- 将信号分段加窗
- 计算每段周期图
- 平均谱估计，降低方差

### 现代谱估计

| 方法 | 原理 | 特点 |
|:---|:---|:---|
| AR 模型 | 自回归建模 | 高分辨率，峰检测好 |
| MUSIC | 子空间分解 | 非参数，高分辨率 |
| ESPRIT | 旋转不变子空间 | 计算效率高 |

## DSP 应用领域

| 领域 | 典型应用 | 关键算法 |
|:---|:---|:---|
| 语音处理 | 语音识别、编解码 | MFCC、LPC、VAD |
| 音频处理 | 降噪、均衡、压缩 | 自适应滤波、FFT |
| 图像处理 | JPEG 压缩、边缘检测 | DCT、小波变换 |
| 通信 | OFDM、QAM 调制 | FFT、匹配滤波 |
| 雷达/声纳 | 脉冲压缩、合成孔径 | 匹配滤波、FFT |
| 生物医学 | ECG/EEG 分析 | 小波、自适应滤波 |

## DSP 硬件平台

| 平台 | 特点 | 典型产品 |
|:---|:---|:---|
| DSP 处理器 | 哈佛架构、MAC 单元 | TI C6000, ADI SHARC |
| FPGA | 并行处理、可重构 | Xilinx, Intel/Altera |
| GPU | 大规模并行 | NVIDIA CUDA |
| ASIC | 专用、低功耗 | 手机基带芯片 |
| ARM Cortex-M | 集成 DSP 指令集 | 嵌入式应用 |

## 相关条目

- [[04_EngineeringAndTechnology/ElectronicsAndCommunications/SpeechRecognition|语音识别]]
- [[04_EngineeringAndTechnology/ElectronicsAndCommunications/WirelessNetworks|无线通信]]
- [[04_EngineeringAndTechnology/EmbeddedSystems|嵌入式系统]]
- [[05_ComputerScience/MachineLearning/DLForSignal|深度学习与信号处理]]
- [[04_EngineeringAndTechnology/ElectronicsAndCommunications/ImageProcessing|图像处理]]
