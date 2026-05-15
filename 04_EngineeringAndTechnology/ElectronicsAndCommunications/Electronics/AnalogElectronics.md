---
aliases: [AnalogElectronics]
tags: ['ElectronicsAndCommunications', 'Electronics', 'AnalogElectronics']
---

# 模拟电子

## 定义
模拟电子技术是研究模拟信号（连续变化的电信号）的产生、放大、处理和变换的学科。是电子信息工程的基础课程。

## 研究对象
- 半导体器件（二极管、三极管、场效应管）
- 基本放大电路
- 运算放大器及其应用
- 反馈放大电路

## 核心内容

### 半导体基础

**PN结**：
- P型半导体（空穴多数载流子）与N型半导体（电子多数载流子）接触形成PN结
- 扩散运动：载流子从高浓度向低浓度扩散
- 漂移运动：载流子在电场作用下定向运动
- 耗尽层：PN结附近载流子被耗尽的区域

**二极管**：
- 伏安特性：$I = I_s(e^{V/V_T}-1)$
- $V_T = kT/q \approx 26mV$（室温）
- 正向导通压降：硅0.7V，锗0.3V
- 反向击穿：稳压二极管利用此特性

### 三极管放大电路

**三极管（BJT）工作原理**：
- 电流关系：$I_C = \beta I_B$，$I_E = (1+\beta)I_B$
- 三种工作区：放大区、饱和区、截止区

**共射放大电路**：
- 电压增益：$A_v = -\beta\frac{R_C}{r_{be}}$
- 输入电阻：$r_{be} = r_{bb'} + (1+\beta)\frac{V_T}{I_E}$
- 输出电阻：$R_o \approx R_C$
- 特点：增益大，输入输出反相

**共集电极放大电路（射极跟随器）**：
- 电压增益：$A_v \approx 1$（小于1但接近1）
- 输入电阻高：$R_i \approx \beta(R_E//R_L)$
- 输出电阻低：$R_o \approx \frac{r_{be}+R_S}{\beta}$
- 特点：缓冲、阻抗变换

**共基极放大电路**：
- 电压增益：$A_v = g_m R_C$
- 输入电阻低
- 频率响应好
- 特点：高频放大

### 场效应管放大电路

**MOSFET工作原理**：
- 通过栅极电压控制漏极电流
- 转移特性（饱和区）：$I_D = \frac{1}{2}k_n'(W/L)(V_{GS}-V_{th})^2$
- 输出特性：$V_{DS} \geq V_{GS} - V_{th}$（饱和区）

**共源放大电路**：
- 电压增益：$A_v = -g_m(R_D//R_L)$
- 输入电阻极高（$10^{10}\Omega$以上）
- 噪声低
- 特点：高输入阻抗放大

### 运算放大器

**理想运放特性**：
- 开环增益：$A_{vo} = \infty$
- 输入电阻：$R_i = \infty$
- 输出电阻：$R_o = 0$
- 带宽：$BW = \infty$

**虚短**：$v_+ = v_-$（两输入端电压相等）

**虚断**：$i_+ = i_- = 0$（输入电流为零）

**基本运放电路**：
- 反相比例：$A_v = -\frac{R_f}{R_1}$
- 同相比例：$A_v = 1 + \frac{R_f}{R_1}$
- 电压跟随器：$A_v = 1$
- 反相加法器：$v_o = -R_f(\frac{v_1}{R_1}+\frac{v_2}{R_2})$
- 积分器：$v_o = -\frac{1}{RC}\int v_i\,dt$
- 微分器：$v_o = -RC\frac{dv_i}{dt}$

### 负反馈放大电路

**反馈类型**：
- 电压串联负反馈：稳定输出电压
- 电流串联负反馈：稳定输出电流
- 电压并联负反馈：降低输出电阻
- 电流并联负反馈：提高输出电阻

**反馈对性能的影响**：
- 增益稳定性提高：$\frac{dA_f}{A_f} = \frac{1}{1+AF}\cdot\frac{dA}{A}$
- 带宽增大：$BW_f = (1+AF)\cdot BW$
- 非线性失真减小
- 输入输出电阻改变

### 功率放大电路

**甲类（A类）**：导通角360°，效率低（≤25%）
**乙类（B类）**：导通角180°，效率高（≤78.5%），有交越失真
**甲乙类（AB类）**：导通角略大于180°，兼顾效率和失真
**D类**：开关工作方式，效率最高（>90%）

**OCL电路**：双电源供电，输出电容耦合
**OTL电路**：单电源供电，输出电容耦合

## 经典教材
- 童诗白《模拟电子技术基础》
- 康华光《电子技术基础（模拟部分）》
- Sedra & Smith《Microelectronic Circuits》
- Razavi《Design of Analog CMOS Integrated Circuits》

## 主要应用领域
- 信号放大与调理
- 传感器接口电路
- 音频放大器
- 电源管理电路
- 数据采集系统（ADC/DAC前端）
- 射频通信电路

## 相关条目

- ComputerEngineering
- [[04_EngineeringAndTechnology/ElectronicsAndCommunications/SignalProcessing/INDEX|SignalProcessing]]
- EmbeddedSystems
