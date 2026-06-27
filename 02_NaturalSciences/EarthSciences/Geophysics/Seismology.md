---
aliases:
  - 地震学
  - Seismology
  - 地震波
  - Seismic Waves
tags:
  - earth-sciences
  - geophysics
  - seismology
  - earthquakes
  - geodynamics
created: 2026-06-28
updated: 2026-06-28
---

# 地震学 (Seismology)

## 概述 (Overview)

地震学 (seismology) 是研究地震 (earthquake) 及其相关现象的学科，通过分析地震波 (seismic waves) 在地球内部的传播来探测地球内部结构、震源过程和构造活动。地震学是地球物理学 (geophysics) 的核心分支，也是理解地球动力学的关键工具。

全球每年记录约50万次地震，其中约10万次可被仪器检测到，约100次造成显著破坏。

---

## 地震波 (Seismic Waves)

### 体波 (Body Waves)

#### P 波 (Primary Waves)

- **类型**：纵波 (longitudinal wave)，压缩波 (compressional wave)
- **质点运动**：平行于传播方向
- **速度**：最快，$v_P = \sqrt{\frac{K + \frac{4}{3}G}{\rho}}$
- **传播介质**：固体和液体
- **典型速度**：地壳中 5-7 km/s，地幔顶部 ~8 km/s

#### S 波 (Secondary Waves)

- **类型**：横波 (transverse wave)，剪切波 (shear wave)
- **质点运动**：垂直于传播方向
- **速度**：$v_S = \sqrt{\frac{G}{\rho}}$
- **传播介质**：仅固体（液体中 $G = 0$）
- **典型速度**：地壳中 3-4 km/s

**P 波和 S 波速度比**：

$$\frac{v_P}{v_S} = \sqrt{\frac{K + \frac{4}{3}G}{G}} = \sqrt{\frac{4}{3} + \frac{K}{G}}$$

### 面波 (Surface Waves)

面波沿地球表面传播，振幅随深度指数衰减：

#### 瑞利波 (Rayleigh Waves)

- 质点做逆进椭圆运动
- 速度：$v_R \approx 0.92 v_S$
- 类似海浪运动

#### 勒夫波 (Love Waves)

- 质点水平横向运动
- 仅在层状介质中存在
- 速度介于上下层 S 波速度之间

#### 面波频散 (Surface Wave Dispersion)

不同频率的面波穿透深度不同，导致传播速度随频率变化：

$$c(\omega) = c_{\text{phase}}(\omega)$$

频散曲线 (dispersion curve) 用于反演地壳和上地幔结构。

---

## 地震仪与地震台网 (Seismometers and Networks)

### 地震仪原理

**短周期地震仪** (short-period seismometer)：
- 自然频率 > 1 Hz
- 灵敏于近震和高频信号

**宽频带地震仪** (broadband seismometer)：
- 频率范围：0.001-100 Hz
- 记录远震和地球自由振荡

### 全球地震台网

| 台网 | 机构 | 特征 |
|------|------|------|
| GSN (Global Seismographic Network) | IRIS/USGS | ~150 个宽频带台站 |
| GEOSCOPE | IPGP (法国) | 全球覆盖 |
| F-net | NIED (日本) | 日本密集台网 |
| China Seismic Network | CEA (中国) | ~2000 个台站 |

---

## 震源参数与震级 (Source Parameters and Magnitude)

### 震源参数

- **震中** (epicenter)：震源在地表的投影
- **震源深度** (focal depth)：震源到地表的距离
- **发震时刻** (origin time)

### 震级标度

| 震级 | 符号 | 适用范围 | 测量参数 |
|------|------|---------|---------|
| 里氏震级 | $M_L$ | 近震 | 最大振幅 |
| 体波震级 | $m_b$ | 远震 | P 波振幅 |
| 面波震级 | $M_s$ | 远震 | 面波振幅 |
| 矩震级 | $M_w$ | 所有 | 地震矩 |

**矩震级** (moment magnitude)：

$$M_w = \frac{2}{3} \log_{10} M_0 - 10.7$$

其中地震矩 $M_0 = \mu A \bar{D}$（$\mu$ 为剪切模量，$A$ 为断层面积，$\bar{D}$ 为平均滑动量）。

---

## 震源机制 (Focal Mechanisms)

### 断层面解 (Fault Plane Solution)

P 波初动 (first motion) 分析确定断层面参数：

- **走向** (strike)：断层面与水平面交线的方向
- **倾角** (dip)：断层面与水平面的夹角
- **滑动角** (rake)：滑动方向与走向的夹角

### 震源球 (Focal Sphere / Beach Ball)

用沙滩球图 (beach ball diagram) 表示震源机制：

- **黑色区域**：压缩区 (P 波初动向上)
- **白色区域**：膨胀区 (P 波初动向下)
- **节面** (nodal planes)：两个正交平面，一个是断层面

### 矩张量 (Moment Tensor)

地震矩张量 $M_{ij}$ 完整描述震源辐射模式：

$$M = \begin{pmatrix} M_{xx} & M_{xy} & M_{xz} \\ M_{yx} & M_{yy} & M_{yz} \\ M_{zx} & M_{zy} & M_{zz} \end{pmatrix}$$

可分解为各向同性 (isotropic)、补偿线性矢量偶极 (CLVD) 和双力偶 (double-couple) 分量。

---

## 地震层析成像 (Seismic Tomography)

### 基本原理

利用地震波走时 (travel time) 反演地球内部的三维速度结构：

$$\delta t = \int_{\text{ray}} \frac{\delta v}{v^2} \, ds$$

### 方法分类

- **体波层析成像**：利用 P 波和 S 波走时残差
- **面波层析成像**：利用面波频散
- **全波形层析成像** (full waveform inversion)：利用完整波形信息

### 主要发现

- **俯冲板片** (subducting slab)：高速异常
- **地幔柱** (mantle plume)：低速异常
- **大型低剪切速度省** (LLSVP)：非洲和太平洋下方的巨型结构
- **岩石圈厚度变化**：克拉通 (craton) 下方厚岩石圈

---

## 地震预警系统 (Earthquake Early Warning, EEW)

### 基本原理

利用 P 波与 S 波的速度差和电磁波与地震波的速度差：

$$\Delta t = \frac{d}{v_S} - \frac{d}{v_P}$$

P 波到达后数秒至数十秒内发出警报。

### 主要系统

| 系统 | 国家 | 特征 |
|------|------|------|
| ShakeAlert | 美国 | 加州、俄勒冈、华盛顿 |
| J-Alert | 日本 | 全国覆盖，秒级预警 |
| EEWS | 中国 | 四川、首都圈等区域 |
| SAS | 墨西哥城 | 基于海岸台站 |

### 预警时间

- 距震中 10 km：~2 秒
- 距震中 50 km：~10 秒
- 距震中 100 km：~20 秒

---

## 强震动与地震工程 (Strong Motion and Earthquake Engineering)

### 强震动记录

- **加速度峰值** (PGA)：地面最大加速度
- **反应谱** (response spectrum)：单自由度系统的最大响应
- **持续时间** (duration)：强震动的时间长度

### 地震灾害评估

- **烈度** (intensity)：MMI (Modified Mercalli Intensity)、中国烈度表
- **地震危险性分析** (seismic hazard analysis)：概率性 (PSHA) 和确定性
- **场地效应** (site effect)：盆地效应、共振

---

## 前沿进展 (Recent Advances)

- **机器学习地震检测**：深度学习自动识别和定位地震
- **分布式光纤传感** (DAS)：利用光纤作为密集地震仪阵列
- **诱发地震** (induced seismicity)：页岩气开采和废水注入引发的地震
- **地震周期** (seismic cycle)：从间震期到同震期的完整过程

---

## 参考与延伸阅读 (References and Further Reading)

1. *An Introduction to Seismology, Earthquakes, and Earth Structure* — S. Stein and M. Wysession
2. *Modern Global Seismology* — T. Lay and T. C. Wallace
3. *Quantitative Seismology* — K. Aki and P. G. Richards
4. *Seismic Tomography* — G. Nolet (ed.)
5. *Earthquake Early Warning* — M. Böse et al., Springer (2014)
