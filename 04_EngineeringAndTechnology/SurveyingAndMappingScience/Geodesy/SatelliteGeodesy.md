---
aliases: [SatelliteGeodesy]
tags: ['SurveyingAndMappingScience', 'Geodesy', 'SatelliteGeodesy']
---

# 卫星大地测量

## 定义
卫星大地测量是利用人造卫星进行大地测量的技术。包括GNSS测量、卫星激光测距、卫星测高等。

## 核心内容

### GNSS系统

**系统组成**：
- GPS（美国）：24颗卫星
- GLONASS（俄罗斯）：24颗卫星
- Galileo（欧盟）：30颗卫星
- 北斗（中国）：35颗卫星（GEO+IGSO+MEO）

**定位原理**：
- 伪距观测：$\rho = c \cdot \Delta t$
- 载波相位观测：$\Phi = N + \frac{\phi}{2\pi}$

**差分定位**：
- 单差：消除卫星钟差
- 双差：消除接收机钟差
- 三差：消除整周模糊度

**精密定位技术**：
- RTK：实时动态定位，精度cm级
- PPK：后处理动态定位
- PPP：精密单点定位，精度cm~dm级

### 卫星激光测距（SLR）

**原理**：测量激光脉冲往返时间

$$R = \frac{c \cdot \Delta t}{2}$$

**精度**：1~3mm

### 卫星测高

**原理**：卫星向海面发射雷达脉冲，测量回波时间

**应用**：
- 海面地形测定
- 海洋重力场反演
- 海平面变化监测

### InSAR技术

**原理**：利用两幅SAR图像的相位差获取地表形变

**差分InSAR（D-InSAR）**：

$$\Delta\phi = \frac{4\pi}{\lambda}\Delta r$$

**应用**：地表沉降监测、地震形变、滑坡监测

## 经典教材
- 魏子卿《卫星大地测量学》
- Hofmann-Wellenhof《GNSS: Theory and Practice》
- 《全球定位系统测量规范》
- 《卫星定位测量规范》

## 主要应用领域
- GNSS控制测量
- 精密工程测量
- 地壳运动监测
- 气象探测（GNSS气象学）
- 自动驾驶定位
