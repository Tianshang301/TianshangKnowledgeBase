---
aliases: [Optoelectronics]
tags: ['04_EngineeringAndTechnology', 'MechanicalAndElectricalEngineering', 'OpticalEngineering']
---

# 光电子学 (Optoelectronics)

## 一、概述

光电子学 (Optoelectronics) 研究光与电子 (Photon-Electron) 的相互作用和能量转换。
核心物理机制包括光的产生、探测、调制和放大。
理论基础是半导体能带理论 (Energy Band Theory) 和量子力学 (Quantum Mechanics)。
光电子器件广泛应用于光纤通信 (Fiber Communication)、显示 (Display)、光伏 (Photovoltaics)、传感 (Sensing) 和量子技术 (Quantum Technology)。
光电子产业规模超过 5000 亿美元，是信息时代的关键支撑技术。
光电子学与微电子学 (Microelectronics) 协同发展，形成了光电集成 (Optoelectronic Integration) 技术方向。

## 二、光与物质相互作用 (Light-Matter Interaction)

### 2.1 三种基本过程

`mermaid
graph LR
    A[光子入射] --> B{能量条件}
    B -->|hv > Eg| C[吸收 Absorption]
    B -->|导带电子| D[自发辐射 Spontaneous]
    B -->|光子激励| E[受激辐射 Stimulated]
    D --> F[随机相位 Random]
    E --> G[同频同相同方向 Coherent]
`

**吸收 (Absorption)**：电子 (Electron) 吸收光子能量从价带 (Valence Band) 跃迁到导带 (Conduction Band)。
吸收系数 $\alpha(h\nu) \propto (h\nu - E_g)^{1/2}$ (直接带隙, Direct Bandgap)。

**自发辐射 (Spontaneous Emission)**：导带电子随机跃迁回价带，发射光子。
光子相位 (Phase) 和方向随机，是非相干光 (Incoherent Light) 的来源。

**受激辐射 (Stimulated Emission)**：入射光子激励导带电子跃迁，发射同频率、同相位、同方向的光子。
受激辐射是激光 (LASER, Light Amplification by Stimulated Emission of Radiation) 放大的物理基础。

**爱因斯坦系数 (Einstein Coefficients)**：
 A_{21} = \frac{8\pi h\nu^3}{c^3} B_{21}, \quad B_{12} = \frac{g_2}{g_1} B_{21} 

{21}$ 为自发辐射速率，{21}$ 为受激辐射系数，{12}$ 为吸收系数。$、$ 为能级简并度 (Degeneracy)。

### 2.2 半导体能带结构

直接带隙 (Direct Bandgap, GaAs, InP)：导带底和价带顶位于相同 $ 空间位置，辐射复合效率高。
间接带隙 (Indirect Bandgap, Si, Ge)：需要声子 (Phonon) 辅助，辐射复合效率低 3-6 个数量级。
发光器件必须采用直接带隙半导体材料。

## 三、LED (Light Emitting Diode, 发光二极管)

### 3.1 工作原理

LED 利用电致发光 (Electroluminescence) 原理——正向偏置 (Forward Bias) 下，电子和空穴在 PN 结耗尽区辐射复合 (Radiative Recombination) 发光。
发光波长 (Emission Wavelength)：
 \lambda = \frac{hc}{E_g} \approx \frac{1240}{E_g (\text{eV})} \ \text{nm} 

### 3.2 材料体系

| 材料 | 禁带宽度 (eV) | 发光波长 | 应用 |
|------|-------------|---------|------|
| AlGaInP | 1.9-2.2 | 红-黄 (620-590 nm) | 指示灯、显示屏 |
| InGaN | 2.2-3.4 | 绿-紫 (530-365 nm) | 照明、背光 |
| AlGaN | 3.4-6.2 | UV (365-200 nm) | 紫外杀菌 |
| GaAsP | 1.4-2.0 | 红-橙 | 早期 LED |

**蓝光 LED**：中村修二 (Shuji Nakamura) 发明 InGaN/GaN 蓝光 LED，获 2014 年诺贝尔物理学奖。
蓝光 LED + 黄色荧光粉 (YAG:Ce) → 白光 LED，彻底改变了照明产业。

### 3.3 效率指标

**内量子效率 (IQE, Internal Quantum Efficiency)**：
 \eta_{IQE} = \frac{\text{辐射复合速率}}{\text{总复合速率}} = \frac{Bnp}{Bnp + A_{SRH}n + C_{Auger}n^3} 

$ 为辐射复合系数，{SRH}$ 为 Shockley-Read-Hall 非辐射复合系数，{Auger}$ 为俄歇复合 (Auger Recombination) 系数。

**外量子效率 (EQE, External Quantum Efficiency)**：
 \eta_{EQE} = \eta_{IQE} \times \eta_{extraction} 

提取效率 (Extraction Efficiency) 受全内反射 (TIR, Total Internal Reflection) 限制：$ \eta_{extraction} \approx \frac{1}{4n^2} \approx 2\text{-}4\% $ (n≈2.5，无结构优化)。
提高方法：表面粗化 (Surface Texturing)、DBR (Distributed Bragg Reflector, 分布式布拉格反射镜)、倒装芯片 (Flip-Chip)、光子晶体 (Photonic Crystal)。

### 3.4 LED 照明特性

**光效 (Luminous Efficacy)**：单位电功率产生的光通量 (lm/W)。当前白光 LED 光效 150-200 lm/W，超过荧光灯 (80-100 lm/W) 和白炽灯 (15 lm/W)。
**显色指数 (CRI, Color Rendering Index)**：Ra > 80 为一般照明，Ra > 90 为高显色。
**色温 (CCT, Correlated Color Temperature)**：暖白 2700-3500K，中性 4000-4500K，冷白 5000-6500K。

## 四、半导体激光器 (Semiconductor Laser Diode)

### 4.1 激光原理

激光器三个要素：增益介质 (Gain Medium)、谐振腔 (Resonant Cavity)、粒子数反转 (Population Inversion)。

**阈值条件 (Threshold Condition)**：
 \Gamma g_{th} = \alpha_i + \frac{1}{2L}\ln\frac{1}{R_1R_2} 

$\Gamma$ 为光限制因子 (Confinement Factor)，{th}$ 为阈值增益，$\alpha_i$ 为内损耗 (Internal Loss)，$ 为腔长，$、$ 为端面反射率。

**速率方程 (Rate Equations)**：
 \frac{dN}{dt} = \frac{I}{qV} - \frac{N}{\tau_s} - v_g g(N)S 
 \frac{dS}{dt} = \Gamma v_g g(N)S + \Gamma\beta\frac{N}{\tau_s} - \frac{S}{\tau_p} 

$ 为载流子密度，$ 为光子密度，$ 为群速度，$\tau_s$ 为载流子寿命，$\tau_p$ 为光子寿命。

### 4.2 激光器类型

| 类型 | 结构 | 特点 | 应用 |
|------|------|------|------|
| FP LD (Fabry-Perot) | 解理面谐振腔 | 多纵模、低成本 | 短距离通信 |
| DFB LD (Distributed Feedback) | 布拉格光栅 | 单纵模、稳频 | 长距离 DWDM |
| VCSEL (Vertical Cavity) | 垂直腔、DBR 反射镜 | 低阈值、圆光束 | 数据中心、3D 传感 |
| EEL (Edge Emitting) | 边发射条形结构 | 高功率 | 泵浦源、加工 |
| QCL (Quantum Cascade) | 量子阱子带跃迁 | 中远红外 | 气体传感 |

**VCSEL (Vertical-Cavity Surface-Emitting Laser, 垂直腔面发射激光器)**：有源区厚度约 $\lambda/n$，上下 DBR 反射率 >99%，阈值电流低至亚毫安级。
广泛应用于 Face ID、LiDAR 和短距离光互连。

### 4.3 调制特性

直接调制 (Direct Modulation) 带宽受弛豫振荡频率 (Relaxation Oscillation Frequency) 限制：
 f_{3dB} \approx \frac{1}{2\pi}\sqrt{\frac{v_g g_0 S_0}{\tau_p}} 

$ 为微分增益 (Differential Gain)，$ 为稳态光子密度。
直调激光器 3dB 带宽已达 50 GHz (InP EAM-DFB 集成)。

## 五、光电探测器 (Photodetector)

### 5.1 工作原理

光电探测器将光信号转换为电信号，核心是光生载流子 (Photogenerated Carrier) 产生光电流 (Photocurrent)。

**响应度 (Responsivity)**：
 R = \frac{I_{ph}}{P_{opt}} = \frac{\eta q}{h\nu} \ \text{(A/W)} 

**量子效率 (Quantum Efficiency)**：
 \eta = \frac{\text{光生电子数}}{\text{入射光子数}} = (1-R)(1-e^{-\alpha d}) 

$ 为表面反射率，$\alpha$ 为吸收系数，$ 为吸收层厚度。

### 5.2 探测器类型对比

| 类型 | 增益 | 响应速度 | 噪声 | 应用 |
|------|------|---------|------|------|
| PIN PD | 1 | 高速 (GHz-THz) | 低 | 光纤通信 |
| APD (Avalanche Photodiode) | 10-1000 | 高速 | 中 (倍增噪声) | 长距离光通信 |
| MSM (Metal-Semiconductor-Metal) | 1 | 超高速 | 暗电流大 | 片上光互连 |
| UTC-PD (Uni-Traveling Carrier) | 1 | >100 GHz | 低 | 太赫兹 (THz) |
| SiPM (Silicon Photomultiplier) | 10^6 | 中 | 单光子级 | 闪烁体探测 |

**APD 雪崩增益 (Avalanche Gain)**：
 M = \frac{1}{1 - \int_0^W \alpha_{ion}(x) dx} 

$\alpha_{ion}$ 为电离系数 (Impact Ionization Coefficient)。InGaAs APD 在 1.55 $\mu 波段广泛使用，增益可达 10-30。

## 六、电光调制器 (Electro-Optic Modulator)

### 6.1 马赫-曾德调制器 (MZM, Mach-Zehnder Modulator)

利用 LiNbO$ (铌酸锂) 或 Si (载流子色散效应) 的 Pockels 效应 (Pockels Effect):
折射率变化 $\Delta n \propto E_{applied}$。

**半波电压 (Half-Wave Voltage)**：
 V_\pi = \frac{\lambda d}{n^3 r_{33} L \Gamma} 

{33}$ 为电光系数 (LiNbO$：30.8 pm/V)，$ 为电极长度，$ 为电极间距。

**调制带宽**受 RC 时间常数和行波电极 (Traveling-Wave Electrode) 速度匹配限制。
薄膜铌酸锂 (TFLN, Thin-Film Lithium Niobate) 调制器带宽 >100 GHz，半波电压 <1 V。

### 6.2 电吸收调制器 (EAM, Electro-Absorption Modulator)

基于量子约束斯塔克效应 (QCSE, Quantum-Confined Stark Effect)：外加电场使吸收边红移 (Red Shift)。
EAM 体积小 (<100 $\mu)，可集成在 DFB 激光器同一芯片上 (EML, Electro-absorption Modulated Laser)。

## 七、太阳能电池 (Solar Cell)

### 7.1 I-V 特性

 I = I_{ph} - I_0 \left[\exp\left(\frac{q(V + IR_s)}{nkT}\right) - 1\right] - \frac{V + IR_s}{R_{sh}} 

{ph}$ 为光生电流，$ 为暗饱和电流，$ 为理想因子，$ 为串联电阻，{sh}$ 为并联电阻。

**填充因子 (FF, Fill Factor)**：
 FF = \frac{P_{max}}{V_{oc} \times I_{sc}} = \frac{V_{mp} \times I_{mp}}{V_{oc} \times I_{sc}} 

典型 FF 0.75-0.85 (单晶硅)。

### 7.2 效率记录

| 电池类型 | 实验室效率 | 特点 |
|---------|-----------|------|
| 单晶硅 (c-Si) | 27.6% (SHJ-IBC) | 成熟，占市场 95% |
| 钙钛矿 (Perovskite) | 26.1% | 溶液法低成本，稳定性待提高 |
| GaAs 单结 | 29.1% | 高效率昂贵，航天应用 |
| 多结叠层 (III-V) | 47.1% (6结) | 最高效率，聚光 CPV |
| 有机光伏 (OPV) | 19.2% | 柔性可印刷 |

**Shockley-Queisser 极限**：单结太阳能电池最大效率 ~33.7% (带隙 1.34 eV)。

## 八、图像传感器 (Image Sensor)

### 8.1 CCD vs CMOS

CCD (Charge-Coupled Device, 电荷耦合器件)：低噪声 (<3 e-$ rms)、高满阱容量 (Full Well Capacity)，但功耗高、读出速度慢、不适合集成。

CMOS Image Sensor (CIS)：像素级放大器 (Per-pixel Amplifier)，低功耗、高集成度、高速读出 (>1000 fps)。当前主流 (>90% 市场)。

**BSI (Backside Illumination, 背面照明)** 和 Stacked (堆叠式) 结构提高量子效率和填充因子。

### 8.2 新型探测器

**SPAD (Single-Photon Avalanche Diode, 单光子雪崩二极管)**：盖革模式 (Geiger Mode) 下单光子探测，用于 LiDAR、量子成像和荧光寿命测量 (FLIM)。
**SiPM (Silicon Photomultiplier)**：SPAD 阵列，输出模拟信号，用于 PET (正电子发射断层扫描) 和辐射探测。

## 九、光子集成 (Photonic Integration)

### 9.1 集成平台

| 平台 | 折射率差 | 传播损耗 | 有源功能 | CMOS 兼容 |
|------|---------|---------|---------|----------|
| InP | ~0.3 | 2-3 dB/cm | 激光器+调制器+探测 | 否 |
| SiPh (SOI) | ~2.0 | 1-2 dB/cm | 调制+探测 (Ge) | 是 |
| SiN | ~0.5 | 0.1 dB/cm | 无电光效应 | 是 |
| TFLN | ~0.2 | 0.3 dB/cm | 高速调制 | 有限 |

### 9.2 硅光子 (Silicon Photonics)

利用 CMOS 工艺在 SOI (Silicon-on-Insulator) 衬底上制造光子器件。
集成度已达数百万器件/芯片，数据中心光互连 (400G/800G FR4) 主流方案。
**关键挑战**：硅是间接带隙，无法高效发光。解决方案：III-V 异质集成 (Heterogeneous Integration) 或锗硅量子点激光器。

### 9.3 共封装光学 (CPO, Co-Packaged Optics)

将光收发引擎 (Optical Engine) 与交换芯片 (Switch ASIC) 封装在同一基板上。
消除可插拔模块 (Pluggable Module) 的电-光接口功耗和延迟。
CPO 是下一代数据中心互连的关键技术，可降低功耗 50%。

## 相关条目

- [[04_EngineeringAndTechnology/MechanicalAndElectricalEngineering/OpticalEngineering/INDEX]]
- [[Photonics]]
- [[FiberOptics]]

## 十、显示技术 (Display Technology)

### 10.1 LCD (Liquid Crystal Display, 液晶显示)

液晶分子在外加电场下旋转，改变偏振光 (Polarized Light) 通过率。
**TFT (Thin Film Transistor, 薄膜晶体管)** 像素驱动。
LED 背光 (Backlight) + 彩色滤光片 (Color Filter) + 液晶层 + 偏光片。

**主要性能参数**：
- 对比度 (Contrast Ratio)：1000:1 - 5000:1
- 响应时间 (Response Time)：1-5 ms (灰阶 GTG)
- 色域 (Color Gamut)：sRGB 100%、DCI-P3 95%、BT.2020 70%
- 刷新率 (Refresh Rate)：60-360 Hz

### 10.2 OLED (Organic LED, 有机发光二极管)

自发光 (Self-Emissive)，无需背光，结构简单。
**RGB OLED**：红绿蓝子像素独立发光。
**WOLED (白光 OLED + 彩色滤光片)**：LG 方案。
**QD-OLED**：蓝光 OLED + 量子点 (Quantum Dot) 色转换。

OLED 优势：无限对比度 (真黑)、广视角 (>170°)、可柔性 (Flexible) 折叠 (Foldable)。
劣势：烧屏 (Burn-in)、蓝色子像素寿命短 (LT95 < 20000h)、成本高于 LCD。

### 10.3 MicroLED

MicroLED (<100 $\mu) 直接作为像素，无机材料 (GaN) 发光。
优势：高亮度 (>5000 nits)、长寿命、低功耗、快速响应 (<ns)。
挑战：巨量转移 (Mass Transfer) 良率 (<99.9999%)、修复成本高。

### 10.4 量子点显示 (Quantum Dot Display)

量子点 (QD) 尺寸决定发光波长，窄半峰宽 (FWHM < 30 nm)。
**QD-LCD** (光致发光, Photoluminescence)：QD 膜 + 蓝光 LED 背光，色域 DCI-P3 100%+。
**QLED** (电致发光, Electroluminescence)：QD 直接发光，尚未量产。

## 十一、光通信应用 (Optical Communication Applications)

### 11.1 光纤通信链路

光发射机 (Tx, 激光器 + 调制器) → 光纤 (Fiber, SMF/MMF) → 光接收机 (Rx, 探测器 + TIA) → DSP。

**传输窗口 (Transmission Window)**：
- O-band (1260-1360 nm)：零色散，短距离
- C-band (1530-1565 nm)：最低损耗 (0.2 dB/km)，长距离 DWDM
- L-band (1565-1625 nm)：扩展波段

**DWDM (密集波分复用)**：通道间隔 50/100 GHz，单纤容量 >30 Tbps。

### 11.2 高速光模块

| 标准 | 速率 | 调制格式 | 传输距离 | 应用 |
|------|------|---------|---------|------|
| SFP28 | 25 Gbps | NRZ | 10 km | 数据中心接入 |
| QSFP28 | 100 Gbps | NRZ 4λ | 2-10 km | 数据中心汇聚 |
| QSFP56-DD | 400 Gbps | PAM4 8λ | 500 m-10 km | 数据中心核心 |
| OSFP/QSFP-DD800 | 800 Gbps | PAM4 8λ | 2 km | AI集群互联 |
| CFP2-DCO | 400G+ | DP-16QAM | >1000 km | 长途相干 |

**相干通信 (Coherent Communication, DP-QPSK/DP-16QAM)**：结合数字信号处理 (DSP) 和 IQ 调制器、本振激光器 (Local Oscillator)，支持长距离高速传输。

## 十二、光电传感应用

### 12.1 LiDAR (激光雷达)

**飞行时间法 (ToF, Time of Flight)**：发射激光脉冲，测量反射回波时间：
 d = \frac{c \cdot \Delta t}{2} 

| 类型 | 波长 | 光源 | 扫描方式 | 特点 |
|------|------|------|---------|------|
| 机械旋转 | 905/1550 nm | EEL/VCSEL | 旋转镜 | 360° FOV，成本高 |
| MEMS 微振镜 | 905 nm | VCSEL | 单轴/双轴振镜 | 固态化，中等成本 |
| Flash | 905 nm | VCSEL 阵列 | 无扫描 | 瞬时成像，距离近 |
| OPA (Optical Phased Array) | 1550 nm | SiPh | 电控移相 | 全固态，无运动部件 |
| FMCW | 1550 nm | DFB+Lo | 相干测距 | 抗干扰，速度同时测量 |

**1550 nm LiDAR**：人眼安全 (Eye-Safe)，大气传输衰减低，适用于长距离 >200 m。

### 12.2 光纤传感 (Fiber Optic Sensing)

**FBG (Fiber Bragg Grating, 光纤布拉格光栅)** 传感：
 \lambda_B = 2n_{eff}\Lambda 

温度和应变使 $\lambda_B$ 漂移：
 \frac{\Delta \lambda_B}{\lambda_B} = (\alpha + \xi)\Delta T + (1 - p_e)\varepsilon 

**分布传感 (Distributed Sensing)**：基于布里渊散射 (Brillouin Scattering, BOTDA) 或拉曼散射 (Raman Scattering, ROTDR)，实现 km 级温度和应变分布式测量。

## 十三、发展趋势

**片上光互连 (On-chip Optical Interconnect)**：利用 SiPh 在芯片级替代电互连，突破 IO 带宽瓶颈 (I/O Bandwidth Wall)。
**微波光子学 (Microwave Photonics)**：光生太赫兹 (THz Photonics)、光子 ADC、光控相控阵天线。
**量子光学芯片 (Quantum Photonic Chip)**：片上纠缠光子源、量子门操作、量子密钥分发 (QKD) 芯片。
**神经形态光子学 (Neuromorphic Photonics)**：光子神经网络 (Photonic Neural Network)，光子处理器实现矩阵乘加运算，速度比电子处理器快 100 倍。
