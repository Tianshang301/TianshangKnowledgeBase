---
aliases: [HeatTransfer]
tags: ['EngineeringFundamentals', 'EngineeringThermophysics', 'HeatTransfer']
---

# 传热学

## 定义
传热学是研究热量传递规律的学科。是能源、动力、化工等领域的重要理论基础。

## 核心内容

### 三种基本传热方式对比

| 传热方式 | 物理机制 | 基本定律 | 数学形式 | 典型应用 |
|---------|---------|---------|---------|---------|
| **热传导** | 分子/电子热运动 | 傅里叶定律 | $\vec{q} = -\lambda\nabla T$ | 固体内部 |
| **热对流** | 流体宏观运动 | 牛顿冷却公式 | $q = h(T_w-T_f)$ | 流体-固体表面 |
| **热辐射** | 电磁波传递 | 斯忒藩-玻尔兹曼定律 | $E = \sigma T^4$ | 真空、高温 |

### 热传导

**傅里叶定律**：

$$\vec{q} = -\lambda\nabla T$$

**一维稳态导热**：

$$q = \lambda\frac{T_1-T_2}{\delta}$$

**导热微分方程**：

$$\rho c\frac{\partial T}{\partial t} = \nabla\cdot(\lambda\nabla T) + \dot{\Phi}$$

**典型形状的稳态导热**：

| 几何形状 | 温度分布 | 热流量公式 | 热阻表达式 |
|---------|---------|-----------|-----------|
| 平壁（面积 $A$） | 线性 $T(x)$ | $Q = \frac{\lambda A}{\delta}(T_1-T_2)$ | $R_\lambda = \frac{\delta}{\lambda A}$ |
| 圆筒壁（长度 $L$） | 对数分布 | $Q = \frac{2\pi\lambda L}{\ln(r_2/r_1)}(T_1-T_2)$ | $R_\lambda = \frac{\ln(r_2/r_1)}{2\pi\lambda L}$ |
| 球壁 | 双曲线分布 | $Q = \frac{4\pi\lambda r_1 r_2}{r_2-r_1}(T_1-T_2)$ | $R_\lambda = \frac{r_2-r_1}{4\pi\lambda r_1 r_2}$ |

**平壁导热**：

$$q = \frac{T_1-T_2}{\delta/\lambda}$$

**圆筒壁导热**：

$$q_l = \frac{2\pi\lambda (T_1-T_2)}{\ln(r_2/r_1)}$$

其中 $q_l$ 为单位长度热流量。

### 对流传热

**牛顿冷却公式**：

$$q = h(T_w-T_f)$$

$h$ 为表面传热系数。

**强迫对流**：
- 管内流动：$Nu = 0.023Re^{0.8}Pr^n$
- 平板流动：$Nu = 0.664Re^{0.5}Pr^{1/3}$

**自然对流**：
- 垂直平板：$Nu = C(Gr\cdot Pr)^n$

**典型对流关联式**：

| 流动类型 | 关联式 | 适用条件 |
|---------|--------|---------|
| 层流管内（恒壁温） | $Nu = 3.66$ | $Re < 2300$，充分发展 |
| 层流管内（恒热流） | $Nu = 4.36$ | $Re < 2300$，充分发展 |
| 湍流管内 | $Nu = 0.023 Re^{0.8} Pr^n$ | $Re > 10^4$, $0.7 < Pr < 160$ |
| 层流外掠平板 | $Nu = 0.664 Re^{0.5} Pr^{1/3}$ | $Re < 5 \times 10^5$ |
| 湍流外掠平板 | $Nu = 0.037 Re^{0.8} Pr^{1/3}$ | $Re > 5 \times 10^5$ |
| 自然对流（垂直平板） | $Nu = C(Gr \cdot Pr)^n$ | 层流 $C=0.59, n=1/4$ |

管内湍流：流体被加热时 $n=0.4$，被冷却时 $n=0.3$。

**无量纲数的物理意义**：

| 无量纲数 | 定义 | 物理意义 |
|---------|------|---------|
| **雷诺数 $Re$** | $Re = \frac{\rho v L}{\mu} = \frac{v L}{\nu}$ | 惯性力与粘性力之比，判断流态 |
| **普朗特数 $Pr$** | $Pr = \frac{\nu}{a} = \frac{\mu c_p}{\lambda}$ | 动量扩散与热量扩散能力之比 |
| **努塞尔数 $Nu$** | $Nu = \frac{h L}{\lambda}$ | 对流换热强度与纯导热强度之比 |
| **格拉晓夫数 $Gr$** | $Gr = \frac{g \beta \Delta T L^3}{\nu^2}$ | 浮升力与粘性力之比（自然对流） |
| **施密特数 $Sc$** | $Sc = \frac{\nu}{D_{AB}}$ | 动量扩散与质量扩散之比（传质） |
| **舍伍德数 $Sh$** | $Sh = \frac{h_m L}{D_{AB}}$ | 对流传质强度的无量纲形式 |

### 热辐射

**Stefan-Boltzmann定律**：

$$E = \varepsilon\sigma T^4$$

**角系数**：$X_{1,2}$

**辐射换热**：

$$Q_{12} = \varepsilon_1\sigma A_1(T_1^4-T_2^4)X_{1,2}$$

**灰体辐射换热**：

$$Q_{12} = \frac{\sigma(T_1^4-T_2^4)}{\frac{1-\varepsilon_1}{\varepsilon_1A_1}+\frac{1}{A_1X_{1,2}}+\frac{1-\varepsilon_2}{\varepsilon_2A_2}}$$

### 换热器

**平均温差法**：

$$Q = UA\Delta T_m$$

**对数平均温差**：

$$\Delta T_m = \frac{\Delta T_1-\Delta T_2}{\ln(\Delta T_1/\Delta T_2)}$$

**效能-NTU法**：

$$\varepsilon = f(NTU, C_{min}/C_{max})$$

### 传质

**Fick定律**：

$$J_A = -D_{AB}\frac{dc_A}{dx}$$

**质交换系数**：$h_m$

**热质比拟**：$Sh = f(Re, Sc)$

## 经典教材
- 杨世铭《传热学》
- 陶文铨《传热学》
- Incropera《Fundamentals of Heat and Mass Transfer》
- Holman《Heat Transfer》

## 主要应用领域
- 换热器设计
- 电子设备散热
- 建筑节能
- 发动机冷却
- 航天热防护
- 工业炉设计
