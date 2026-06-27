---
aliases: [SatelliteGeodesy]
tags: ['SurveyingAndMappingScience', 'Geodesy', 'SatelliteGeodesy']
created: 2026-05-17
updated: 2026-05-13
---

# 卫星大地测量 (Satellite Geodesy)

## 概述

卫星大地测量 (Satellite Geodesy) 是利用人造地球卫星进行地球形状、大小、重力场及地壳运动等大地测量学任务的科学与技术。它是现代大地测量的核心分支，彻底改变了传统地面测量的工作模式，实现了从局部到全球、从静态到动态、从二维到三维的跨越。

卫星大地测量的发展历程可分为三个阶段：
- **几何卫星大地测量**：通过观测卫星轨道几何关系确定地面点位置
- **动力卫星大地测量**：利用卫星轨道摄动反演地球重力场
- **空间大地测量**：以全球导航卫星系统 (GNSS) 为代表，实现全天候、实时、高精度定位

## 核心技术与系统

### 全球导航卫星系统 (GNSS)

GNSS 是现代卫星大地测量的基石，目前主要有四大全球系统：

| 系统名称 | 国家/地区 | 卫星数量 | 轨道类型 | 服务精度 |
|---------|----------|---------|---------|---------|
| GPS | 美国 | 24+ | MEO | 民用 3~5m |
| GLONASS | 俄罗斯 | 24 | MEO | 民用 2.5~5m |
| Galileo | 欧盟 | 30 | MEO | 民用 1m 以内 |
| 北斗 (BDS) | 中国 | 35 | GEO+IGSO+MEO | 民用 3.6m，亚太优于 1m |

**北斗系统特色**：北斗三号 (BDS-3) 采用混合星座设计，具备短报文通信、精密单点定位 (PPP)、国际搜救等特色服务。

### GNSS 定位原理

#### 伪距定位 (Pseudorange Positioning)

卫星向地面广播测距信号，接收机测量信号传播时间：

$$\rho = c \cdot \Delta t + c \cdot (\delta t_r - \delta t_s) + I + T + \varepsilon$$

其中：
- $\rho$ 为伪距观测值
- $c$ 为光速
- $\delta t_r$, $\delta t_s$ 分别为接收机和卫星钟差
- $I$ 为电离层延迟
- $T$ 为对流层延迟
- $\varepsilon$ 为多路径和观测噪声

#### 载波相位定位 (Carrier Phase Positioning)

载波相位观测方程：

$$\Phi = \rho + c(\delta t_r - \delta t_s) - \lambda N + I - T + \varepsilon$$

其中 $\lambda$ 为载波波长，$N$ 为整周模糊度 (Integer Ambiguity)。载波相位定位的关键在于准确解算整周模糊度。

### 精密定位技术

| 技术名称 | 英文 | 精度 | 实时性 | 适用场景 |
|---------|------|------|--------|---------|
| 实时动态定位 | RTK (Real-Time Kinematic) | cm 级 | 实时 | 工程测量、自动驾驶 |
| 后处理动态定位 | PPK (Post-Processed Kinematic) | cm 级 | 事后 | 航空摄影、无人机测绘 |
| 精密单点定位 | PPP (Precise Point Positioning) | cm~dm 级 | 实时/事后 | 海洋测量、精密农业 |
| 网络 RTK | NRTK / CORS | cm 级 | 实时 | 区域精密定位服务 |

**差分定位原理**：通过双差观测消除或削弱公共误差项。

- 单差：站间差分，消除卫星钟差
- 双差：站间星间差分，消除接收机钟差
- 三差：历元间差分，消除整周模糊度参数

### 卫星激光测距 (SLR)

SLR 是测定卫星轨道和地球参考框架最高精度的技术之一。

**测距方程**：

$$R = \frac{c \cdot \Delta t}{2} + \Delta_{\text{atm}} + \Delta_{\text{rel}} + \Delta_{\text{CG}}$$

其中 $\Delta t$ 为激光脉冲往返时间，$\Delta_{\text{atm}}$ 为大气延迟改正，$\Delta_{\text{rel}}$ 为相对论效应改正，$\Delta_{\text{CG}}$ 为质心改正。

**精度指标**：
- 单次测距精度：1~3 mm
- 轨道确定精度：亚 cm 级
- 地心坐标精度：mm 级

### 卫星测高 (Satellite Altimetry)

卫星测高利用星载雷达或激光高度计，通过测量雷达脉冲往返时间确定卫星到海面的距离。

**海面高计算**：

$$h_{\text{sea}} = h_{\text{sat}} - R - \sum \Delta$$

其中 $h_{\text{sat}}$ 为卫星轨道高度，$R$ 为观测距离，$\Delta$ 为各项改正（干/湿对流层、电离层、固体潮、极潮等）。

**主要应用**：
- 平均海面高 (MSL) 与大地水准面确定
- 海洋重力场反演
- 海平面变化监测（精度达 mm/yr）
- 海洋环流研究

### 合成孔径雷达干涉测量 (InSAR)

InSAR 利用两幅或多幅 SAR 图像的相位差获取地表形变信息。

**干涉相位方程**：

$$\Delta\phi = \frac{4\pi}{\lambda}\Delta r + \frac{4\pi}{\lambda}B_{\perp}\frac{\Delta z}{r\sin\theta} + \phi_{\text{atm}} + \phi_{\text{noise}}$$

其中 $\Delta r$ 为地表形变引起的距离变化，$B_{\perp}$ 为垂直基线，$\Delta z$ 为地形误差。

**差分 InSAR (D-InSAR)**：通过消除地形相位，提取纯粹的地表形变信息。对于形变监测，距离向形变与相位的关系为：

$$\Delta r = \frac{\lambda}{4\pi} \Delta\phi$$

**时序 InSAR 技术**：
- PS-InSAR：利用永久散射体进行长时间序列监测
- SBAS-InSAR：短基线集时序分析
- 精度可达 mm 级

## 轨道确定与动力学

### 卫星轨道力学

开普勒轨道六要素描述卫星在空间中的运动状态：
- 半长轴 $a$
- 偏心率 $e$
- 轨道倾角 $i$
- 升交点赤经 $\Omega$
- 近地点幅角 $\omega$
- 平近点角 $M$

受地球非球形引力摄动、日月引力、太阳光压、大气阻力等因素影响，实际轨道为受摄轨道。卫星运动方程：

$$\ddot{\mathbf{r}} = -\frac{GM}{r^3}\mathbf{r} + \mathbf{a}_{\text{non-central}}$$

### 精密定轨方法

| 定轨方法 | 观测数据 | 精度 | 应用 |
|---------|---------|------|------|
| 动力学定轨 | 伪距 + 载波相位 | 2~5 cm | GNSS 卫星定轨 |
| 简化动力学定轨 | 相位 + 伪距 + 先验力模型 | 1~3 cm | LEO 卫星定轨 |
| 运动学定轨 | 纯 GNSS 相位 | 亚 cm 级 | 高分辨率遥感 |
| SLR 联合定轨 | SLR + GNSS | mm 级 | 地球参考框架维持 |

## 参考框架与时间系统

### 国际地球参考框架 (ITRF)

ITRF 是卫星大地测量的空间基准，由 VLBI、SLR、GNSS 和 DORIS 四种空间大地测量技术综合解算。

**最新版本 ITRF2020** 特点：
- 原点精度：mm 级
- 尺度精度：$10^{-9}$ 量级
- 包含测站坐标和速度场
- 顾及非线性运动（周期性负荷位移、地震共震位移）

### 时间系统

| 时间系统 | 英文 | 定义 | 应用 |
|---------|------|------|------|
| 世界时 | UT1 | 基于地球自转 | 天文导航 |
| 协调世界时 | UTC | 原子时 + 闰秒 | 民用时间 |
| GPS 时 | GPST | 连续原子时 | GPS 系统 |
| 北斗时 | BDT | 连续原子时 | BDS 系统 |

## 应用领域

### 地壳运动与形变监测

GNSS 连续运行参考站 (CORS) 网络可监测板块运动、断层活动、火山形变等。中国大陆构造环境监测网络 (CMONOC) 包含 260 余个连续观测站，为地震预测提供基础数据。

### 精密工程测量

- 桥梁、大坝、高层建筑变形监测
- 高速铁路轨道几何状态检测
- 地铁隧道掘进导向
- 精度要求通常优于 mm 级

### 大气与气象学

GNSS 气象学 (GNSS Meteorology) 利用 GNSS 信号反演大气水汽含量：

$$PWV = \Pi \cdot ZTD_{\text{wet}}$$

其中 $PWV$ 为可降水量，$\Pi$ 为转换系数，$ZTD_{\text{wet}}$ 为湿延迟分量。该技术已广泛应用于数值天气预报和气候研究。

### 海洋学应用

- 卫星测高确定全球平均海面高
- 反演海洋重力异常和海底地形
- 监测全球海平面上升（约 3.3 mm/yr）

## 经典教材与规范

- 魏子卿《卫星大地测量学》
- 许其凤《GPS 卫星导航与精密定位》
- Hofmann-Wellenhof《GNSS: Theory and Practice》
- Teunissen《GNSS Data Processing》
- 《全球定位系统测量规范》GB/T 18314
- 《卫星定位测量规范》CH/T 2009

## 相关条目

- [[Geodesy]]
- [[GNSS]]
- [[ReferenceFrame]]
- [[RemoteSensing]]
- [[INDEX|SurveyingAndMappingScience 索引]]
