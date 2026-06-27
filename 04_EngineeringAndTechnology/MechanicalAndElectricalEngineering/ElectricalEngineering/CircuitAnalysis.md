---
aliases: [CircuitAnalysis]
tags: ['MechanicalAndElectricalEngineering', 'ElectricalEngineering', 'CircuitAnalysis']
created: 2026-05-16
updated: 2026-05-16
---

# 电路分析

## 定义
电路分析是研究集总参数电路中电压、电流及其相互关系的理论和方法。它是电气工程和电子信息工程的基础课程。

## 研究对象
- 电阻、电容、电感等基本元件
- 直流电路与交流电路
- 电路的稳态与暂态分析
- 网络函数与频率响应

## 基本元件特性对比

| 元件 | 符号 | 伏安关系 | 阻抗 $Z$ | 储能 |
|------|------|---------|---------|------|
| 电阻 $R$ | $\square\!\!-\!\!\square$ | $v = iR$ | $R$ | 无（耗能） |
| 电容 $C$ | $\shortparallel$ | $i = C\frac{dv}{dt}$ | $\frac{1}{j\omega C}$ | $\frac{1}{2}CV^2$ |
| 电感 $L$ | $\sim\!\sim$ | $v = L\frac{di}{dt}$ | $j\omega L$ | $\frac{1}{2}LI^2$ |

## 核心内容

### 基尔霍夫定律

**基尔霍夫电流定律（KCL）**：任一时刻，流入节点的电流之和等于流出节点的电流之和。

$$\sum_{k=1}^{n} i_k = 0$$

**基尔霍夫电压定律（KVL）**：沿任一闭合回路，各元件电压的代数和为零。

$$\sum_{k=1}^{n} u_k = 0$$

### 电路分析方法

**节点电压法**：
- 以节点电压为未知量
- 对每个独立节点列 KCL 方程
- 导纳矩阵形式：$\mathbf{Y}_n \mathbf{V}_n = \mathbf{I}_s$

**网孔电流法**：
- 以网孔电流为未知量
- 对每个网孔列 KVL 方程
- 阻抗矩阵形式：$\mathbf{Z}_m \mathbf{I}_m = \mathbf{V}_s$

**欧姆定律**：$V = IR$，是电路分析中最基本的定律，描述电压、电流与电阻之间的关系。

**叠加定理**：
- 线性电路中，多个电源共同作用产生的响应等于各电源单独作用产生响应的代数和
- 注意：功率不能叠加

**戴维宁定理**：
- 任何线性有源二端网络可用一个电压源 $V_{th}$ 与电阻 $R_{th}$ 串联等效
- $V_{th}$：开路电压
- $R_{th}$：将独立源置零后端口的等效电阻

**诺顿定理**：
- 线性有源二端网络可用一个电流源 $I_N$ 与电阻 $R_N$ 并联等效
- $I_N = V_{th}/R_{th}$

### RC/RL/RLC 电路分析

**RC 电路**：
- 充电过程：$u_C(t) = U_0(1-e^{-t/\tau})$，$\tau = RC$
- 放电过程：$u_C(t) = U_0 e^{-t/\tau}$
- 时间常数 $\tau$：电容充放电速度的度量

**RL 电路**：
- 电流增长：$i(t) = \frac{U}{R}(1-e^{-t/\tau})$，$\tau = L/R$
- 电流衰减：$i(t) = I_0 e^{-t/\tau}$

**RLC 串联电路**：
- 微分方程：$LC\frac{d^2u_C}{dt^2} + RC\frac{du_C}{dt} + u_C = U_s$
- 特征方程：$s^2 + \frac{R}{L}s + \frac{1}{LC} = 0$
- 阻尼比：$\zeta = \frac{R}{2}\sqrt{\frac{C}{L}}$
- 过阻尼（$\zeta>1$）、临界阻尼（$\zeta=1$）、欠阻尼（$\zeta<1$）

**串联谐振**：$\omega_0 = \frac{1}{\sqrt{LC}}$，谐振时阻抗最小 $Z = R$

**品质因数**：$Q = \frac{\omega_0 L}{R} = \frac{1}{\omega_0 RC}$，反映谐振电路的频率选择特性

**功率耗散**：电阻元件功率 $P = I^2R = \frac{V^2}{R}$

### 交流电路

**相量法**：将正弦量用复数表示

$$A\cos(\omega t + \phi) \Leftrightarrow \dot{A} = A\angle\phi$$

**阻抗**：
- 电阻：$Z_R = R$
- 电感：$Z_L = j\omega L$
- 电容：$Z_C = \frac{1}{j\omega C}$

**相量形式的欧姆定律**：$\dot{V} = Z\dot{I}$

**相量图**：直观表示电压、电流的幅值和相位关系

**功率计算**：
- 瞬时功率：$p(t) = u(t)i(t)$
- 有功功率（平均功率）：$P = VI\cos\varphi$（单位：W）
- 无功功率：$Q = VI\sin\varphi$（单位：var）
- 视在功率：$S = VI$（单位：VA）
- 功率因数：$\cos\varphi = P/S$

**复功率**：$\tilde{S} = P + jQ = \dot{V}\dot{I}^*$

**最大功率传输**：负载阻抗等于电源内阻抗的共轭时，负载获得最大功率。

$$Z_L = Z_s^*$$

### 互感与变压器

**互感电压**：$u_2 = M\frac{di_1}{dt}$，$M$ 为互感系数

**耦合系数**：$k = \frac{M}{\sqrt{L_1 L_2}}$，$0 \leq k \leq 1$

**理想变压器**：
- 电压比：$\frac{V_1}{V_2} = \frac{n_1}{n_2}$
- 电流比：$\frac{I_1}{I_2} = \frac{n_2}{n_1}$
- 阻抗变换：$Z_{in} = \left(\frac{n_1}{n_2}\right)^2 Z_L$

## 经典教材
- 邱关源《电路》
- Hayt & Kemmerly《Engineering Circuit Analysis》
- Alexander & Sadiku《Fundamentals of Electric Circuits》
- Nilsson & Riedel《Electric Circuits》

## 主要应用领域
- 电力系统分析与设计
- 电子电路设计
- 信号处理与通信系统
- 控制系统建模
- 集成电路设计
- 新能源系统（光伏逆变器、电池管理）

## 相关条目

- [[05_ComputerScience/ComputerOrganizationAndArchitecture/DigitalLogic/DigitalLogic|DigitalLogic]]
- [[05_ComputerScience/HardwareAndEmbeddedSystems/AnalogCircuits/AnalogCircuits|AnalogCircuits]]
- [[04_EngineeringAndTechnology/ElectronicsAndCommunications/SignalProcessing/INDEX|SignalProcessing]]
- [[PowerSystems]]


