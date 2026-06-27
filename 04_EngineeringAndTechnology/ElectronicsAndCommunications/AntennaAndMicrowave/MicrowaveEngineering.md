---
aliases: [MicrowaveEngineering]
tags: ['ElectronicsAndCommunications', 'AntennaAndMicrowave', 'MicrowaveEngineering']
created: 2026-05-16
updated: 2026-05-13
---

# 微波工程

## 定义
微波工程是研究微波频段（300MHz~300GHz）电磁波的产生、传输、放大、检测和应用的工程技术学科。

## 研究对象
- 微波传输线与波导
- 微波器件与电路
- 微波电路设计方法
- 雷达系统基础

## 核心内容

### 微波频段划分

| 频段 | 频率范围 | 波长范围 |
|------|---------|---------|
| UHF | 300MHz~3GHz | 1m~10cm |
| L 波段 | 1~2GHz | 30~15cm |
| S 波段 | 2~4GHz | 15~7.5cm |
| C 波段 | 4~8GHz | 7.5~3.75cm |
| X 波段 | 8~12GHz | 3.75~2.5cm |
| Ku 波段 | 12~18GHz | 2.5~1.67cm |
| Ka 波段 | 26.5~40GHz | 1.13~0.75cm |
| 毫米波 | 30~300GHz | 10~1mm |

### 波导

**矩形波导**：
- 主模：$TE_{10}$模
- 截止频率：$f_c = \frac{c}{2a}$（$a$ 为宽边尺寸）
- 特性阻抗：$Z_{TE} = \frac{\eta}{\sqrt{1-(f_c/f)^2}}$
- 单模工作条件：$f_c < f < 2f_c$

**圆波导**：
- 主模：$TE_{11}$模
- 旋转对称性好
- 用于旋转关节、极化器

### 微带线

**微带线结构**：
- 导带+介质基板+接地板
- 特性阻抗与介质常数、导带宽度、基板厚度有关

**特性阻抗近似公式**：

$$Z_0 = \frac{87}{\sqrt{\varepsilon_r+1.41}}\ln\left(\frac{5.98h}{0.8w+t}\right)$$

（$w/h < 1$ 时）

**有效介电常数**：

$$\varepsilon_{eff} = \frac{\varepsilon_r+1}{2} + \frac{\varepsilon_r-1}{2}\left(1+12\frac{h}{w}\right)^{-1/2}$$

### 微波器件

**环行器**：
- 多端口非互易器件
- 信号按特定方向传输
- 用于收发转换

**隔离器**：
- 二端口非互易器件
- 正向通过，反向吸收
- 保护信号源

**定向耦合器**：
- 将输入信号按一定比例分配到两个输出端口
- 参数：耦合度、方向性、隔离度

**功分器**：
- Wilkinson 功分器：等分、同相、隔离
- 耦合线功分器

### 微波电路设计

**微波滤波器**：
- 低通原型→带通/带阻变换
- 阶梯阻抗滤波器
- 耦合谐振器滤波器

**微波放大器**：
- 低噪声放大器（LNA）：位于接收前端
- 功率放大器（PA）：位于发射末端
- 稳定性设计、噪声匹配、功率匹配

**微波振荡器**：
- 介质谐振器振荡器（DRO）
- 压控振荡器（VCO）
- 锁相环频率综合器

### 雷达系统基础

**雷达方程**：

$$R_{max} = \left[\frac{P_t G^2 \lambda^2 \sigma}{(4\pi)^3 k T_s B_n (SNR)_{min}}\right]^{1/4}$$

$P_t$ 为发射功率，$G$ 为天线增益，$\sigma$ 为目标 RCS，$T_s$ 为系统噪声温度。

**雷达类型**：
- 脉冲雷达：测量距离
- 连续波雷达：测量速度
- 脉冲多普勒雷达：同时测距和测速
- 合成孔径雷达（SAR）：成像

**雷达应用**：
- 气象雷达
- 航空管制雷达
- 汽车雷达（ACC、BSD）
- 军事雷达

## 经典教材
- 高葆新《微波工程基础》
- Pozar《Microwave Engineering》
- Collin《Foundations for Microwave Engineering》
- Liao《Microwave Devices and Circuits》

## 主要应用领域
- 雷达系统（军用/民用）
- 卫星通信
- 移动通信基站
- 汽车雷达
- 微波加热（工业/家用）
- 微波遥感

## 相关条目

- [[AntennaTheory]]
- [[RFEngineering]]
- RadarSystems
- [[WirelessCommunications]]
- SatelliteCommunications
