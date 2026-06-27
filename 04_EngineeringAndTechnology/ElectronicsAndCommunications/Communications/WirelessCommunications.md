---
aliases: [WirelessCommunications]
tags: ['ElectronicsAndCommunications', 'Communications', 'WirelessCommunications']
created: 2026-05-16
updated: 2026-05-16
---

# 无线通信

## 定义
无线通信是利用电磁波在自由空间中传输信息的通信方式。是现代通信系统的重要组成部分，涵盖蜂窝网络、WiFi、蓝牙、卫星通信等。

## 研究对象
- 无线信道特性
- 蜂窝网络原理
- 多址接入技术
- 4G/5G 关键技术

## 核心内容

### 无线信道特性

**路径损耗**：

$$PL(d) = PL(d_0) + 10n\log_{10}\left(\frac{d}{d_0}\right) + X_\sigma$$

$n$ 为路径损耗指数（2~4），$X_\sigma$ 为阴影衰落（对数正态分布）。

**多径衰落**：
- 信号经多条路径到达接收端
- 时延扩展：$\tau_{max} - \tau_{min}$
- 相干带宽：$B_c \approx 1/\tau_{max}$
- 快衰落：瑞利分布（无直射径）或莱斯分布（有直射径）

**多普勒效应**：

$$f_d = \frac{v}{\lambda}\cos\theta = \frac{vf_c}{c}\cos\theta$$

多普勒扩展：$B_d = f_{d,max}$

### 蜂窝网络原理

**频率复用**：
- 将服务区域划分为多个小区
- 相隔一定距离的小区可复用相同频率
- 频率复用因子：$N$（$N$ 个小区组成一个簇）

**小区划分**：
- 六边形模型：覆盖无重叠无缝隙
- 三叶草模式：每基站3个扇区
- 小区分裂：缩小小区半径增加容量

**同频干扰**：$C/I = \frac{S}{\sum_{k=1}^{K}I_k}$，$K$ 为同频干扰源数量

### 多址技术

**频分多址（FDMA）**：
- 不同用户占用不同频率
- 模拟通信常用
- 代表：AMPS

**时分多址（TDMA）**：
- 不同用户占用不同时隙
- 数字通信
- 代表：GSM

**码分多址（CDMA）**：
- 不同用户使用不同扩频码
- 所有用户同时同频传输
- 代表：IS-95、WCDMA

**正交频分多址（OFDMA）**：
- 将带宽分为多个正交子载波
- 不同用户分配不同子载波组
- 代表：LTE、WiMAX

### 4G/5G 关键技术

**MIMO（多输入多输出）**：
- 发送端和接收端使用多个天线
- 空间复用：提高数据速率
- 分集增益：提高可靠性
- $y = Hx + n$

**大规模天线（Massive MIMO）**：
- 基站配置大量天线（64~256个）
- 波束成形：将能量聚焦于用户方向
- 空间分辨率提高
- 能效提升

**毫米波通信**：
- 频段：24GHz~100GHz
- 带宽大（可达数 GHz）
- 传播损耗大，覆盖距离短
- 应用：5G 热点覆盖

**5G 关键指标**：
- 峰值速率：20 Gbps
- 用户体验速率：100 Mbps
- 时延：<1 ms（URLLC）
- 连接密度：100万设备/km²

### WiFi 技术演进

**WiFi 标准**：
- 802.11b：11 Mbps（2.4GHz）
- 802.11g：54 Mbps（2.4GHz）
- 802.11n（WiFi 4）：600 Mbps
- 802.11ac（WiFi 5）：3.5 Gbps
- 802.11ax（WiFi 6）：9.6 Gbps

**WiFi 6关键技术**：
- OFDMA：多用户同时传输
- MU-MIMO：上下行多用户 MIMO
- TWT（目标唤醒时间）：省电
- 1024-QAM：更高调制阶数

## 经典教材
- Rappaport《Wireless Communications: Principles and Practice》
- Goldsmith《Wireless Communications》
- Tse & Viswanath《Fundamentals of Wireless Communication》
- 吴伟陵《移动通信原理与系统》

## 主要应用领域
- 蜂窝移动通信（4G/5G）
- 无线局域网（WiFi）
- 蓝牙（短距离通信）
- 卫星通信
- 物联网（NB-IoT、LoRa）
- 车联网（V2X）

## 相关条目

- [[CommunicationTheory]]
- [[04_EngineeringAndTechnology/ElectronicsAndCommunications/AntennaAndMicrowave/AntennaTheory|AntennaTheory]]
- [[04_EngineeringAndTechnology/ElectronicsAndCommunications/Electronics/RFEngineering|RFEngineering]]
- [[04_EngineeringAndTechnology/ElectronicsAndCommunications/SignalProcessing/DigitalSignalProcessing|DigitalSignalProcessing]]
- [[04_EngineeringAndTechnology/ElectronicsAndCommunications/AntennaAndMicrowave/MicrowaveEngineering|MicrowaveEngineering]]


