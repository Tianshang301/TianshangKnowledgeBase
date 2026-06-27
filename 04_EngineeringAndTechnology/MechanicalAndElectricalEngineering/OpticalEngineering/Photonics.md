---
aliases: [Photonics]
tags: ['MechanicalAndElectricalEngineering', 'OpticalEngineering', 'Photonics.md']
created: 2026-05-17
updated: 2026-05-17
---

---
aliases: [Photonics]
tags: ['04_EngineeringAndTechnology', 'MechanicalAndElectricalEngineering', 'OpticalEngineering']
---

# 光子学 (Photonics)

## 一、概述

光子学 (Photonics) 研究光子的产生、传输、操控和检测。
光子作为信息载体具有速度快 (光速 3e8 m/s)、带宽大 (THz 量级)、抗干扰 (EMI Immunity) 等核心优势。
涵盖集成光子学 (Integrated Photonics)、非线性光学 (Nonlinear Optics)、量子光学 (Quantum Optics)、等离激元 (Plasmonics) 等前沿方向。
光子学与电子学互补发展，形成了光电融合 (Optoelectronic Convergence) 的技术趋势。
全球光子学市场规模超过 5000 亿美元，年增长 6-8%。

## 二、光波导理论 (Optical Waveguide Theory)

### 2.1 平板波导 (Slab Waveguide)

三层结构：芯层 (Core, n1) + 包层 (Cladding, n2)，n1 > n2。

**本征方程 (Eigenvalue Equation, TE 模式)**：
kappa * d = m*pi + arctan(gamma/kappa) + arctan(delta/kappa)

kappa = sqrt(k0^2 * n1^2 - beta^2)，gamma = sqrt(beta^2 - k0^2 * n2^2)。
beta = n_eff * k0 为传播常数，n_eff 为有效折射率 (Effective Index)。

**单模条件 (Single-Mode Condition)**：
V = (2*pi/lambda) * d * sqrt(n1^2 - n2^2) < pi/2

V 为归一化频率 (Normalized Frequency)。

### 2.2 脊波导和条波导

脊波导 (Rib Waveguide) 通过刻蚀部分芯层形成横向限制，适用于激光器、调制器。
条波导 (Strip/Channel Waveguide) 在横向和纵向均受限，用于无源光路互联。

## 三、无源光子器件 (Passive Photonic Devices)

### 3.1 分束器 (Beam Splitter)

**Y 分支 (Y-Branch)**：对称分束，50:50 功率分配。
**定向耦合器 (Directional Coupler, DC)**：
P2 = P0 * sin^2(kappa * L)，P3 = P0 * cos^2(kappa * L)

kappa 为耦合系数 (Coupling Coefficient)，L 为耦合长度。精确调节 L 实现任意分束比。

**MMI (Multimode Interference, 多模干涉)** 耦合器：基于自映像原理 (Self-Imaging Principle)，N x N 分束。
1x2 MMI 的 3dB 带宽超过 100 nm，工艺容差大 (Fabrication Tolerance)。

### 3.2 滤波器 (Filter)

**环形谐振腔 (Microring Resonator, MRR)**：
FSR = lambda^2 / (2*pi*R*n_g)，F = FSR / FWHM

R 为环半径，n_g 为群折射率 (Group Index)，FSR 为自由光谱范围 (Free Spectral Range)，F 为精细度 (Finesse)。

**阵列波导光栅 (AWG, Arrayed Waveguide Grating)**：罗兰圆 (Rowland Circle) 结构，相邻波导长度差 dL 产生相位差。
AWG 解复用 (DeMUX) 通道数 16-256，间隔 50/100 GHz。

### 3.3 复用器 (Mux/Demux)

**模式复用器 (Mode Mux)**：基于非对称定向耦合器 (ADC, Asymmetric Directional Coupler) 实现模式转换和复用。

## 四、硅光子技术 (Silicon Photonics)

### 4.1 SOI 平台优势

SOI (Silicon-on-Insulator) 结构：Si 芯层 (220 nm) + SiO2 埋氧层 (BOX, 2-3 um) + Si 衬底。
高折射率差 dn 约等于 2.0，可实现超紧凑弯曲半径 R > 3 um，集成度达百万器件/cm2。

### 4.2 调制器 (Modulator)

载流子色散效应 (Carrier Plasma Dispersion, Soref Equation)：
dn = -8.8e-22 * dNe - 8.5e-18 * (dNh)^0.8
d_alpha = 8.5e-20 * dNe + 6.0e-20 * dNh

载流子耗尽型 (Carrier Depletion) PN 结马赫-曾德调制器 (MZM)：带宽 >50 GHz，Vpi*L < 2 V·cm。

### 4.3 探测器 (Photodetector)

锗 (Ge) 外延在 Si 上，Ge 在 1.31/1.55 um 有良好吸收。
**波导集成 Ge PD**：响应度 >0.8 A/W，暗电流 <1 uA，带宽 >50 GHz。

### 4.4 光源集成挑战 (Laser Integration)

硅是间接带隙，不能高效发光。
**异质集成 (Heterogeneous Integration)**：III-V 量子点激光器 (QD Laser) 通过 BCB 键合或直接外延在 Si 上。
**片上外腔激光器**：Si 波导谐振腔 + III-V 增益芯片。线宽 <10 kHz。

## 五、非线性光学 (Nonlinear Optics)

### 5.1 非线性极化

极化强度 (Polarization) 展开：
P = epsilon0 * (chi1 * E + chi2 * E^2 + chi3 * E^3 + ...)

chi1 线性极化 (折射率)，chi2 二阶非线性，chi3 三阶非线性。
Si 和 SiO2 中心对称 (chi2 = 0)，SiN 和 LiNbO3 非中心对称 (chi2 != 0)。

### 5.2 二阶非线性过程

**SHG (Second Harmonic Generation, 二次谐波/倍频)**：w_out = 2 * w_in。
**SFG (Sum-Frequency Generation, 和频)**：w3 = w1 + w2。
**DFG (Difference-Frequency Generation, 差频)**：w3 = w1 - w2 (参量放大 OPA/参量振荡 OPO)。

**相位匹配条件 (Phase Matching)**：
dk = k3 - k1 - k2 = 0

准相位匹配 (QPM, Quasi-Phase Matching)：周期性极化铌酸锂 (PPLN, Periodically Poled LiNbO3)，周期 Lambda = 2*pi/|dk|。

### 5.3 三阶非线性过程

**SPM (Self-Phase Modulation, 自相位调制)**：dphi_SPM = gamma * P0 * L_eff。
**XPM (Cross-Phase Modulation, 交叉相位调制)**。
**FWM (Four-Wave Mixing, 四波混频)**：w4 = w1 + w2 - w3，用于波长转换 (Wavelength Conversion)。
**SRS (Stimulated Raman Scattering, 受激拉曼散射)**：Si 中 SRS 增益系数 g_R 约 20e-10 cm/W。

### 5.4 超连续谱产生 (Supercontinuum Generation)

飞秒脉冲在非线性介质中传播，通过 SPM、XPM、FWM 等效应展宽光谱。
非线性薛定谔方程 (NLSE, Nonlinear Schrödinger Equation) 描述脉冲在光纤中的非线性传播。

## 六、超快光学 (Ultrafast Optics)

### 6.1 锁模激光器 (Mode-Locked Laser)

锁模 (Mode Locking) 使多纵模相位同步，产生飞秒脉冲序列。
**被动锁模**：可饱和吸收体 (SESAM, Semiconductor Saturable Absorber Mirror)。
**钛宝石激光器 (Ti:Sapphire Laser)**：<10 fs 脉冲，中心波长 800 nm，克尔透镜锁模 (KLM)。

### 6.2 飞秒脉冲测量

**自相关仪 (Autocorrelator)**：二阶自相关测量脉冲宽度。
**FROG (Frequency-Resolved Optical Gating, 频率分辨光学开关)**：同时测量脉冲幅度和相位。
**SPIDER (Spectral Phase Interferometry for Direct Electric-field Reconstruction)**。

### 6.3 泵浦-探测技术 (Pump-Probe Technique)

泵浦光 (Pump) 激发样品，探测光 (Probe) 以可调延迟测量瞬态变化。
时间分辨率由脉冲宽度决定 (<10 fs)。用于研究载流子动力学 (Carrier Dynamics)、声子 (Phonon) 弛豫。

## 七、量子光学 (Quantum Optics)

### 7.1 非经典光场

**Fock 态 (光子数态)** |n>：确定光子数。
**压缩态 (Squeezed State)**：正交振幅或相位分量的量子噪声低于散粒噪声极限 (Shot Noise Limit)。
**纠缠态 (Entangled State)**：双光子态 (Bell 态)。

### 7.2 纠缠光子产生

**SPDC (Spontaneous Parametric Down-Conversion, 自发参量下转换)**：泵浦光子在 chi2 晶体中分裂为信号光 (Signal) 和闲频光 (Idler)。
PPKTP 是常用 SPDC 晶体。

### 7.3 单光子源与探测器

| 类型 | 纯度 g2(0) | 温度 | 特点 |
|------|-----------|------|------|
| 量子点 QD | <0.01 | 4 K | 确定性产生，纯度最高 |
| 色心 NV/SiV in Diamond | <0.1 | RT | 可室温，自旋-光子纠缠 |
| SPDC HBT 触发 | <0.1 | RT | 概率性 (Probabilistic) |
| 原子/离子囚禁 | <0.01 | 低温 | 确定性，系统复杂 |

**SNSPD (超导纳米线单光子探测器)**：NbTiN 纳米线，探测效率 >98%，暗计数 <1 cps，时间抖动 <3 ps。
**SPAD (单光子雪崩二极管)**：Si (400-900 nm) / InGaAs (1.3-1.55 um)。

## 八、等离激元光子学 (Plasmonics)

### 8.1 SPP (Surface Plasmon Polariton, 表面等离激元极化激元)

SPP 是光子和金属表面自由电子集体振荡 (Plasmon) 的耦合激发。
SPP 将光场约束在亚波长尺度 (<lambda/10)，突破衍射极限 (Diffraction Limit)。

**色散关系 (Dispersion Relation)**：
k_SPP = (w/c) * sqrt(em * ed / (em + ed))

em 为金属介电常数 (Drude 模型)，ed 为介质介电常数。

### 8.2 应用

**SERS (Surface-Enhanced Raman Scattering, 表面增强拉曼散射)**：探针分子吸附在金属纳米结构表面，拉曼信号增强百万到万亿倍。
**等离激元波导 (Plasmonic Waveguide)**：金属-绝缘体-金属 (MIM) 结构，传播长度 10-100 um。

## 九、应用系统 (Application Systems)

### 9.1 DWDM 光纤通信

C-band 80 通道 x 100 Gbps = 8 Tbps 单纤。
Nyquist WDM 和 Superchannel 进一步提高频谱效率。

### 9.2 共封装光学 (CPO, Co-Packaged Optics)

光引擎与交换芯片 3D 封装在同一基板，消除可插拔模块电接口功耗 (每通道省 1-2 W)。
CPO 是 51.2 Tbps 交换芯片的关键互连方案。

### 9.3 LiDAR (激光雷达)

FMCW (调频连续波) LiDAR 基于相干探测 (Coherent Detection)，同时测量距离和速度，抗干扰能力强。
OPA (Optical Phased Array, 光学相控阵) LiDAR 采用 SiPh 移相器阵列电控光束偏转。

### 9.4 OCT (Optical Coherence Tomography, 光学相干断层扫描)

利用低相干干涉 (Low-Coherence Interferometry) 获得生物组织深部微米级分辨率图像。
扫频源 OCT (SS-OCT) 使用 1.3 um 扫频激光器。

## 相关条目

- [[Optoelectronics]]
- [[FiberOptics]]
- [[04_EngineeringAndTechnology/MechanicalAndElectricalEngineering/OpticalEngineering/INDEX]]

## 十、光子计算 (Photonic Computing)

### 10.1 光子神经网络 (Photonic Neural Network)

利用 MZI (Mach-Zehnder Interferometer) 网格实现矩阵-向量乘加 (Matrix-Vector Multiplication)。
Reck 分解：任意 N x N 酉矩阵 (Unitary Matrix) 可由 N(N-1)/2 个 MZI 实现。
光子处理器速度比电子处理器快 100 倍，功耗低 1000 倍。

### 10.2 光互连 (Optical Interconnect)

芯片级光互连 (On-chip Optical Interconnect) 替代电互连，突破 IO 带宽瓶颈 (I/O Bandwidth Wall)。
微环谐振器 (MRR) 作为 WDM 调制器可实现 >1 Tbps/通道的数据速率。
片上激光器阵列 + SiPh 路由网络组成光网络-on-chip (ONoC, Optical Network-on-Chip)。

### 10.3 光计算 (Optical Computing)

**光学逻辑门 (Optical Logic Gate)**：基于 Sagnac 干涉仪、非线性光环镜 (NOLM, Nonlinear Optical Loop Mirror)。
**光学存储 (Optical Buffer)**：慢光 (Slow Light) 在光子晶体波导或 EIT (Electromagnetically Induced Transparency, 电磁感应透明) 介质中实现。

## 十一、材料与工艺

### 11.1 核心材料对比

| 材料 | 折射率 n | 带宽 (nm) | 损耗 (dB/cm) | 电光系数 | 主要应用 |
|------|---------|----------|-------------|---------|---------|
| Si (SOI) | 3.48 | 1200-7000 | 1-3 | 无 (载流子色散) | 调制器、无源光路 |
| Si3N4 (SiN) | 2.00 | 400-2350 | 0.1-0.5 | 无 | 超低损耗滤波器 |
| SiO2 | 1.44 | UV-IR | <0.1 | 无 | 光纤、包层 |
| LiNbO3 (TFLN) | 2.21 | 400-5000 | 0.2-0.5 | 很强 (r33=30) | 高速调制器 |
| InP | 3.17 | 900-1600 | 2-5 | 中等 | 有源集成 (激光器) |
| Al2O3 | 1.65 | 200-5000 | <0.1 | 掺杂后 | 放大器 (EDFA 波导) |

### 11.2 制造工艺

**CMOS 兼容工艺**：深紫外光刻 (DUV, 193 nm) / 极紫外光刻 (EUV, 13.5 nm) 定义波导。
**电子束光刻 (EBL, Electron Beam Lithography)**：nm 级精度，用于原型验证。
**刻蚀 (Etching)**：ICP-RIE (电感耦合等离子反应离子刻蚀) 各向异性刻蚀 Si/SiN。
**原子层沉积 (ALD, Atomic Layer Deposition)**：精确控制薄膜厚度 (<nm 级) 用于保形涂层。
**键合 (Bonding)**：晶圆键合 (Wafer Bonding, SiO2/SiO2 熔融键合)、BCB 粘合键合、金属热压键合。

## 十二、测试与表征

### 12.1 基本测量

**端面耦合效率 (Fiber-to-Chip Coupling)**：光栅耦合器 (Grating Coupler, GC) 效率 -2 到 -5 dB，端面耦合 (Edge Coupler, 倒锥 Inverse Taper) 效率 -1 到 -3 dB。
**传播损耗测量**：切回法 (Cut-back Method) 测量不同长度波导的透射率。
**色散测量**：白光干涉法 (White Light Interferometry) 测量群折射率 n_g。

### 12.2 频域/时域测试

**光矢量网络分析 (OVNA, Optical Vector Network Analyzer)**：测量器件幅度和相位响应。
**光采样示波器 (Optical Sampling Oscilloscope)**：测量高速光信号眼图 (Eye Diagram)。
**误码率测试 (BERT, Bit Error Rate Test)**：PRBS (伪随机二进制序列) 测试通信链路质量。
 BER = \frac{\text{错误比特数}}{\text{总比特数}} < 10^{-12} \text{(通信标准)}

## 十三、产业与市场 (Industry & Market)

### 13.1 光子学产业链

上游：衬底 (Substrate, SOI/SiN/LiNbO3 晶圆)、气体 (Gas, SiH4/N2/Ar)、光刻胶 (Photoresist)。
中游：器件设计 (Design, EDA 工具 Lumerical/Ansys)、晶圆制造 (Foundry, AIM Photonics/TowerJazz)、封装测试 (Packaging & Test)。
下游：光通信设备商 (Cisco/Huawei)、数据中心 (AWS/Google/Meta)、激光雷达 (Luminar/RoboSense)、消费电子 (Apple 3D Sensing)。

### 13.2 主要光子学 Foundry

| Foundry | 平台 | 工艺节点 | PDK 支持 |
|---------|------|---------|---------|
| AIM Photonics (USA) | SiPh | 300 nm | Process Design Kit |
| TowerJazz (Israel) | SiPh | 250 nm | 完整光/电 PDK |
| IMEC (Belgium) | SiPh/SiN | 193 nm DUV | 多项目晶圆 MPW |
| VTT (Finland) | SiN | 193 nm | 超低损耗 SiN |
| LioniX (Netherlands) | TriPleX (SiN) | 定制 | 低损耗氮化硅 |
| CSMC/Huali (China) | SiPh | 180 nm | 国内供应链 |

## 十四、未来展望 (Future Outlook)

### 14.1 片上光互连 (On-chip Optical Interconnect)

以光代电解决芯片级数据带宽瓶颈。
片上 WDM 链路：微环调制器阵列 + 波导路由 + 锗探测接收。
每通道速率 25-50 Gbps，64 通道实现 1.6-3.2 Tbps 单向带宽。
功耗 <1 pJ/bit (电互连 >5 pJ/bit)。

### 14.2 量子光子芯片 (Quantum Photonic Chip)

片上纠缠光子对产生、量子门操作、波导分束器实现量子计算。
SiN + SPDC 晶体集成实现 Chip-scale 量子密钥分发 (QKD) 终端。

### 14.3 生物光子传感 (Biophotonic Sensing)

片上微型光谱仪 (Micro-spectrometer, AWG 阵列探测器)。
生化传感 (Biochemical Sensing, 倏逝波 Evanescent Wave 传感 + 微流控 Microfluidics)。

### 14.4 光子学与 AI 交叉

光计算加速 AI 推理 (Matrix-Vector 加速)。
AI 辅助光子器件设计 (Inverse Design, 拓扑优化 Topology Optimization)。
