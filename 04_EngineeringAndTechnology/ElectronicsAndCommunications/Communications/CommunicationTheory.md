---
aliases: [CommunicationTheory]
tags: ['ElectronicsAndCommunications', 'Communications', 'CommunicationTheory']
---

# 通信原理

## 定义
通信原理是研究信息传输基本理论和方法的学科，包括模拟通信和数字通信的原理、系统组成、性能分析和设计方法。

## 研究对象
- 通信系统模型与性能指标
- 模拟调制与解调技术
- 数字调制与解调技术
- 信道容量与编码理论

## 核心内容

### 通信系统模型

**基本模型**：信源→编码→调制→信道→解调→译码→信宿

**模拟通信系统**：信源输出连续信号，直接调制传输

**数字通信系统**：信源输出离散符号，经编码、调制后传输

**通信系统性能指标**：
- 有效性：频带利用率 $\eta = R_b/B$ (b/s/Hz)
- 可靠性：误码率 $P_e$、误比特率 $P_b$

### 模拟调制

**幅度调制（AM）**：

$$s_{AM}(t) = [A_0 + m(t)]\cos(2\pi f_c t)$$

- 包络检波：$m(t)$ 的包络
- 调制度：$m_a = \max|m(t)|/A_0$
- 带宽：$B_{AM} = 2W$（$W$ 为基带信号带宽）

**抑制载波双边带（DSB-SC）**：

$$s_{DSB}(t) = m(t)\cos(2\pi f_c t)$$

- 需要相干解调
- 带宽：$B_{DSB} = 2W$

**单边带调制（SSB）**：

$$s_{SSB}(t) = \frac{1}{2}m(t)\cos(2\pi f_c t) \mp \frac{1}{2}\hat{m}(t)\sin(2\pi f_c t)$$

$\hat{m}(t)$ 为 $m(t)$ 的希尔伯特变换。

- 带宽：$B_{SSB} = W$
- 频带利用率最高

**频率调制（FM）**：

$$s_{FM}(t) = A_c\cos\left[2\pi f_c t + 2\pi k_f\int_0^t m(\tau)d\tau\right]$$

- 瞬时频率：$f_i = f_c + k_f m(t)$
- 卡森公式：$B_{FM} = 2(\Delta f + W)$
- 调频指数：$m_f = \Delta f/W$

### 数字调制

**幅移键控（ASK）**：
- $s_{ASK}(t) = A\cos(2\pi f_c t)$（发送1）
- 误码率：$P_e = \frac{1}{2}\text{erfc}(\sqrt{r/2})$（相干检测）
- $r = E_b/N_0$ 为信噪比

**频移键控（FSK）**：
- $s_1(t) = A\cos(2\pi f_1 t)$（发送1）
- $s_0(t) = A\cos(2\pi f_2 t)$（发送0）
- 误码率优于ASK

**相移键控（PSK）**：
- BPSK：$s_1 = A\cos(2\pi f_c t)$，$s_0 = -A\cos(2\pi f_c t)$
- 误码率：$P_e = \frac{1}{2}\text{erfc}(\sqrt{r})$
- 抗噪声性能最好

**正交幅度调制（QAM）**：
- 同时调制幅度和相位
- 16-QAM、64-QAM、256-QAM
- 频谱效率高
- 需要更大的信噪比

### 信道容量

**香农定理**：

$$C = B\log_2\left(1+\frac{S}{N}\right) = B\log_2(1+\text{SNR})$$

$C$ 为信道容量（b/s），$B$ 为带宽（Hz），$S/N$ 为信噪比。

**物理意义**：
- 给定带宽和信噪比，信息传输速率存在上限
- 提高带宽或信噪比可增加容量
- 当 $SNR \to \infty$ 时，$C/B \to \infty$；但实际中 $SNR$ 有限

**带宽与信噪比的互换**：带宽可与信噪比互换，用带宽换取信噪比

### 差错控制编码

**汉明码**：
- 线性分组码
- 能纠正1位错误
- 参数：$(2^m-1, 2^m-1-m)$，最小距离 $d_{min}=3$

**卷积码**：
- 编码器有记忆
- $(n, k, K)$：$n$ 个输出，$k$ 个输入，约束长度 $K$
- 维特比译码：最大似然译码

**LDPC码**：
- 低密度奇偶校验码
- 稀疏校验矩阵
- 近香农限性能
- 应用：5G、Wi-Fi 6

**Turbo码**：
- 并行级联卷积码
- 交织器+两个分量码
- 迭代译码
- 应用：3G/4G

## 经典教材
- 曹志刚《现代通信原理》
- 樊昌信《通信原理》
- Haykin《Communication Systems》
- Proakis《Digital Communications》

## 主要应用领域
- 移动通信（4G/5G）
- 卫星通信
- 光纤通信
- 无线局域网（WiFi）
- 广播电视
- 军事通信

## 相关条目

- [[04_EngineeringAndTechnology/ElectronicsAndCommunications/SignalProcessing/INDEX|SignalProcessing]]
- [[ComputerNetworks]]
- [[WirelessNetworks]]
- InformationTheory
