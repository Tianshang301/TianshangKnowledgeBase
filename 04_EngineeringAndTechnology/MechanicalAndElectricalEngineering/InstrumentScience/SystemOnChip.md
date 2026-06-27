---
aliases: [SystemOnChip]
tags: ['MechanicalAndElectricalEngineering', 'InstrumentScience', 'SystemOnChip.md']
created: 2026-05-17
updated: 2026-05-17
---

---
aliases: [SystemOnChip]
tags: ['04_EngineeringAndTechnology', 'MechanicalAndElectricalEngineering', 'InstrumentScience']
---

# 片上系统 (System on Chip, SoC)

## 一、概述

SoC (System on Chip, 片上系统) 将完整电子系统集成在单个芯片 (Die) 上。
典型 SoC 包含处理器 (Processor)、存储器 (Memory)、外设接口 (Peripheral Interface)、硬件加速器 (Hardware Accelerator) 和模拟电路 (Analog Circuit)。
SoC 的核心优势：体积小 (Form Factor)、功耗低 (Power Efficiency)、可靠性高 (Reliability)、成本低 (BOM Cost)。
现代手机 SoC (如 Apple A17 Pro、Qualcomm Snapdragon 8 Gen 3) 晶体管数超过 200 亿，采用 3 nm 制程工艺。
SoC 设计是集成电路 (IC, Integrated Circuit) 设计中最复杂的一类，需要平衡性能 (Performance)、功耗 (Power)、面积 (Area, PPA) 三大指标。

## 二、处理器核心 (Processor Core)

### 2.1 应用处理器 (Application Processor)

ARM Cortex-A 系列：高性能，乱序执行 (Out-of-Order Execution) 架构，用于手机、平板和服务器。
ARM Cortex-X 系列：定制高性能核心，最大单线程性能。
ARM 大小核架构 (big.LITTLE/DynamIQ)：高性能大核 (P-core) + 能效小核 (E-core) 动态调度。

指令集架构 (ISA, Instruction Set Architecture)：
- ARMv9-A：64 位，支持 SVE2 (Scalable Vector Extension 2)
- RISC-V (RISC Five)：开源指令集，可扩展，Modular 设计 (RV64GC)
- x86 (Intel/AMD)：PC/服务器市场，向后兼容

### 2.2 实时处理器 (Real-Time Processor)

ARM Cortex-R 系列：确定性响应 (Deterministic Response)，低延迟中断处理 (<10 cycles)。
用于汽车电子 (ADAS, Advanced Driver-Assistance Systems)、工业控制 (PLC, Programmable Logic Controller)、基带处理 (Baseband Processing)。

### 2.3 微控制器 (Microcontroller)

ARM Cortex-M 系列：超低功耗 (ULP, Ultra-Low Power)，深度睡眠模式功耗 <1 uW。
M0+ (最低功耗)、M4 (DSP 指令)、M7 (高性能) 三级定位。
用于物联网 (IoT, Internet of Things) 终端、传感器节点、可穿戴设备 (Wearable)。

## 三、存储层次 (Memory Hierarchy)

### 3.1 片内缓存 (On-chip Cache)

| 缓存级别 | 容量 | 延迟 (cycles) | 关联度 (Associativity) | 技术 |
|---------|------|--------------|----------------------|------|
| L1 I-Cache | 32-64 KB | 2-4 | 4-way | SRAM |
| L1 D-Cache | 32-64 KB | 2-4 | 4-way | SRAM |
| L2 Cache | 256 KB - 1 MB | 8-15 | 8-way | SRAM |
| L3 Cache (共享) | 2-8 MB | 20-40 | 16-way | SRAM |
| SLC (System Level Cache) | 4-32 MB | 30-60 | 8-16 way | SRAM/DRAM |

**缓存一致性 (Cache Coherency)**：MESI 协议 (Modified, Exclusive, Shared, Invalid) 或 MOESI 协议。
ACE 总线 (AXI Coherency Extensions) 保证多核间数据一致性。

### 3.2 片外存储 (Off-chip Memory)

**DRAM (Dynamic Random Access Memory)**：
- LPDDR5/X (Low Power DDR5)：速率 6.4-8.5 Gbps，手机 SoC 标配
- DDR5：PC/服务器，速率 4.8-8.0 Gbps
- HBM3 (High Bandwidth Memory 3)：3D 堆叠，带宽 >800 GB/s，AI/HPC 应用

**闪存 (Flash Memory)**：
- NAND Flash：UFS 4.0 (Universal Flash Storage)，顺序读取 >4 GB/s
- eMMC 5.1：嵌入式存储，低成本

## 四、片上互连 (On-chip Interconnect)

### 4.1 AMBA 总线 (ARM Advanced Microcontroller Bus Architecture)

**AXI (Advanced eXtensible Interface)**：高性能主-从接口，支持乱序传输 (Out-of-Order Transaction) 和多个未完成交易 (Multiple Outstanding Transactions)。
**ACE (AXI Coherency Extensions)**：支持缓存一致性。
**CHI (Coherent Hub Interface)**：下一代 ARM 互连，支持网状拓扑 (Mesh Topology)。
**AHB (Advanced High-performance Bus)**：简单高性能，单次传输，用于中等带宽外设。
**APB (Advanced Peripheral Bus)**：低功耗，简单接口，用于低速外设 (UART、I2C、GPIO)。

### 4.2 NoC (Network on Chip, 片上网络)

NoC 是 SoC 多核时代的关键互连架构，提供可扩展性 (Scalability)。
**拓扑 (Topology)**：网格 (Mesh)、环 (Ring)、蝶形 (Butterfly)、层次化总线 (Hierarchical Bus)。
**路由器 (Router)**：输入缓冲 + 交叉开关 (Crossbar) + 仲裁器 (Arbiter)。
**流控 (Flow Control)**：虫洞路由 (Wormhole Routing)、虚拟通道 (Virtual Channel, VC) 防止死锁 (Deadlock)。

## 五、GPU (Graphics Processing Unit, 图形处理器)

### 5.1 移动 GPU 架构

| 架构 | 厂商 | 特点 | 最新版本 |
|------|------|------|---------|
| Mali | Arm | Valhall 架构，可变速率着色 (VRS) | Mali-G720 |
| Adreno | Qualcomm | 统一着色器，支持 Ray Tracing | Adreno 750 |
| Apple GPU | Apple | 自研架构，Tile-based Deferred Rendering (TBDR) | A17 Pro GPU |
| PowerVR | Imagination | TBDR 高效架构 | PowerVR D 系列 |

### 5.2 API 支持

**Vulkan**：跨平台低开销 (Low Overhead) 图形 API。
**OpenGL ES 3.2**：嵌入式图形标准。
**DirectX 12 Ultimate**：Windows/ 游戏主机。
**Metal**：Apple 平台专有。

## 六、NPU (Neural Processing Unit, 神经网络处理器)

### 6.1 计算核心

NPU 针对神经网络推理 (Inference) 优化，核心计算为乘累加 (MAC, Multiply-Accumulate)：
 y = \sum_{i=1}^n w_i \cdot x_i + b

**MAC 阵列 (Systolic Array, 脉动阵列)**：二维 MAC 阵列实现矩阵乘法高吞吐。
**数据流 (Dataflow)**：
- 权值固定 (Weight Stationary)：激活数据流动，权值保持
- 输出固定 (Output Stationary)：部分和累加
- 行固定 (Row Stationary)：平衡数据复用与带宽

### 6.2 性能指标

**TOPS (Tera Operations Per Second)**：NPU 性能单位，手机 NPU 5-50 TOPS。
**典型能效**：10-20 TOPS/W (7 nm)。
**精度 (Precision)**：
- INT8：推理主流，精度损失 <1%
- INT4：更高吞吐，精度损失可接受
- FP16/BF16：训练精度
- TF32：NVIDIA Ampere 架构专用

### 6.3 典型 NPU 架构

Apple Neural Engine (ANE)：16 核，35 TOPS (A17 Pro)。
Qualcomm Hexagon NPU：支持 INT8/INT16，融合 HVX 向量扩展。
MediaTek APU：多核异构，支持 INT4。

## 七、视频编解码器 (Video Codec)

### 7.1 编码标准

| 标准 | 压缩比 (vs H.264) | 特点 | SoC 支持 |
|------|-------------------|------|---------|
| H.264/AVC | 1x (基准) | 广泛兼容 | 全部 |
| H.265/HEVC | 1.5-2x | 4K/8K 主流 | 全部(2015+) |
| AV1 | 1.3x (vs HEVC) | 开源，无专利费 | 旗舰 SoC (2021+) |
| VVC/H.266 | 2x (vs HEVC) | 下一代，复杂度高 | 预计 2025+ |
| VP9 | 1.4x (vs H.264) | Google 开源 | Android 生态 |

**硬件编解码器 (Hardware Codec)**：
固定功能硬件实现，功耗比软件编解码低 100 倍。
支持 4K 60fps / 8K 30fps 实时编解码。
编码 (Encoder) 复杂度约为解码 (Decoder) 的 5-10 倍。

## 八、ISP (Image Signal Processor, 图像信号处理器)

### 8.1 ISP 流水线

**RAW 输入** → 黑电平校正 (BLC, Black Level Correction) → 去噪 (Denoising) → 去马赛克 (Demosaic) → 白平衡 (AWB, Auto White Balance) → 颜色校正矩阵 (CCM, Color Correction Matrix) → 伽马校正 (Gamma Correction) → 色调映射 (Tone Mapping) → YUV 输出。

### 8.2 计算摄影 (Computational Photography)

**多帧 HDR (High Dynamic Range)**：3-5 帧不同曝光量合成，动态范围 >120 dB。
**夜景模式 (Night Mode)**：多帧降噪 + 长曝光，信噪比 (SNR, Signal to Noise Ratio) 提升 10-20 dB。
**人像模式 (Portrait Mode)**：双摄/深度传感器 + AI 分割，实现背景虚化 (Bokeh)。
**超分 (Super Resolution)**：多帧亚像素位移重建，2x-4x 分辨率提升。

## 九、外设接口 (Peripheral Interface)

### 9.1 低速接口

| 接口 | 速率 | 用途 |
|------|------|------|
| SPI (Serial Peripheral Interface) | 10-100 Mbps | 传感器、闪存、显示 |
| I2C (Inter-Integrated Circuit) | 100 kHz - 3.4 MHz | 外设配置、传感器 |
| UART (Universal Asynchronous Receiver) | 115.2 kbps - 10 Mbps | 调试、GPS、蓝牙模块 |
| GPIO (General Purpose I/O) | 可变 | 控制信号、中断输入 |
| I3C (Improved Inter-Integrated Circuit) | 12.5 MHz | I2C 替代，更低功耗 |

### 9.2 高速接口

**USB (Universal Serial Bus)**：
- USB 2.0：480 Mbps
- USB 3.2 Gen 2x2：20 Gbps
- USB4：40 Gbps

**PCIe (Peripheral Component Interconnect Express)**：
- PCIe 4.0：16 GT/s per lane
- PCIe 5.0：32 GT/s
- PCIe 6.0：64 GT/s (PAM4 信令)

**MIPI (Mobile Industry Processor Interface)**：
- D-PHY：相机 (CSI) 和显示 (DSI)，1-2.5 Gbps/lane
- C-PHY：更高效率，2.28 Gsym/s/trio
- M-PHY：UFS 存储接口

## 十、ADC/DAC (模数/数模转换器)

### 10.1 ADC 类型

| 类型 | 分辨率 (位) | 采样率 | 特点 | 应用 |
|------|-----------|--------|------|------|
| SAR (逐次逼近) | 8-16 | 1 MSPS - 10 MSPS | 低功耗、中等速度 | 传感器、音频 |
| Pipeline (流水线) | 10-16 | 10 MSPS - 1 GSPS | 高速度、中等功耗 | 射频接收机、视频 |
| Sigma-Delta (Delta-Sigma) | 16-32 | 10 kSPS - 10 MSPS | 高精度、过采样 | 音频、精密测量 |
| Flash (全并行) | 6-8 | >10 GSPS | 超高速、高功耗 | 示波器、SerDes |
| TDC (时间-数字转换) | 10-20 ps | 可变 | 时间测量 | LiDAR、TOF |

### 10.2 ADC 性能指标

**有效位数 (ENOB, Effective Number of Bits)**：
 ENOB = \frac{SINAD - 1.76}{6.02}

SINAD 为信号-噪声-失真比 (Signal to Noise And Distortion ratio)。
**无杂散动态范围 (SFDR, Spurious Free Dynamic Range)**：dBc 或 dBFS。

## 十一、SoC 设计流程 (SoC Design Flow)

### 11.1 前端设计 (Front-end)

1. **需求定义 (Requirement Definition)**：性能目标、功耗预算、面积约束、功能需求
2. **架构设计 (Architecture Design)**：核心选择、总线拓扑、存储层次、IP 选型
3. **RTL 编码 (RTL Coding)**：Verilog/SystemVerilog HDL，模块级设计
4. **功能验证 (Functional Verification)**：仿真 (Simulation)、UVM (Universal Verification Methodology)、覆盖驱动验证 (Coverage-Driven Verification)

### 11.2 后端设计 (Back-end)

5. **逻辑综合 (Logic Synthesis)**：Design Compiler (Synopsys) / Genus (Cadence) 将 RTL 转换为门级网表 (Gate-level Netlist)
6. **形式验证 (Formal Verification)**：等效性检查 (Equivalence Checking)
7. **布局布线 (Place & Route)**：ICC2 / Innovus 将门级网表物理布局并布线
8. **静态时序分析 (STA, Static Timing Analysis)**：PrimeTime / Tempus 验证时序收敛 (Timing Closure)
9. **物理验证 (Physical Verification)**：DRC (Design Rule Check)、LVS (Layout vs Schematic)

### 11.3 流片与测试

10. **流片 (Tapeout)**：GDSII 文件交付晶圆厂
11. **ATE 测试 (Automatic Test Equipment)**：晶圆探针测试 (Wafer Probe) + 封装后最终测试 (Final Test)
12. **特征化 (Characterization)**：电压、温度、频率角点测试

## 十二、发展趋势 (Future Trends)

### 12.1 Chiplet (小芯片)

多 die 通过先进封装互联，替代单芯片大 die。
**UCIe (Universal Chiplet Interconnect Express)** 标准：PHY 层速率 16-32 GT/s。
**Die-to-Die 接口**：AIB (Intel)、BoW (Open Compute Project)。

### 12.2 3D IC

**TSV (Through Silicon Via, 硅通孔)**：垂直互连，缩短信号路径，降低功耗。
**混合键合 (Hybrid Bonding)**：Cu-Cu 直接键合，间距 <10 um，用于 HBM、CIS 堆叠。

### 12.3 CIM (Compute-In-Memory, 存算一体)

消除冯诺依曼瓶颈 (Von Neumann Bottleneck)。
SRAM 宏 (Macro) 内集成模拟/数字 MAC 运算，能效 >100 TOPS/W。
NAND Flash 阵列内计算用于 AI 大模型推理。

### 12.4 开源 SoC

**RISC-V + Chipyard (Berkeley)**：开源 SoC 生成框架。
**OpenPiton (Princeton)**：开源多核 SoC 平台。
RISC-V 碎片化风险 (Fragmentation) 与生态系统建设。

## 相关条目

- [[VHDL]]
- [[04_EngineeringAndTechnology/MechanicalAndElectricalEngineering/InstrumentScience/INDEX]]

## 十三、SoC 电源管理 (Power Management)

### 13.1 DVFS (Dynamic Voltage and Frequency Scaling, 动态电压频率调整)

根据负载动态调整核心电压 (Vdd) 和频率 (f)，降低功耗。
 P = P_{dynamic} + P_{static} = \alpha \cdot C_L \cdot V_{dd}^2 \cdot f + I_{leak} \cdot V_{dd}

**动态功耗 (Dynamic Power)**：开关活动因子 alpha * 负载电容 C_L * Vdd^2 * f。
**静态功耗 (Static Power)**：漏电流 (Leakage Current, 亚阈值漏电 + 栅漏电) * Vdd。

### 13.2 电源域 (Power Domain)

SoC 划分多个电源域，独立控制开关。
**电源门控 (Power Gating)**：关闭空闲模块电源 (Header/Footer 开关)。
**保留 (Retention)**：寄存器数据在断电前存档到 retention flop，恢复时加载。

### 13.3 低功耗模式

| 模式 | CPU 状态 | 功耗 | 唤醒延迟 | 应用场景 |
|------|---------|------|---------|---------|
| Active | 运行 | 1x | 即时 | 正常计算 |
| Sleep (WFI) | 时钟关闭 | 0.1x | 微秒级 | 短时空闲 |
| Deep Sleep | 电源关闭 (保留) | 0.01x | 毫秒级 | 待机 |
| Hibernate | 完全断电 | <0.001x | 秒级 | 深度待机 |
| Off | 断电 | 0 | 冷启动 | 关机 |

## 十四、安全性设计 (Security Design)

### 14.1 TEE (Trusted Execution Environment, 可信执行环境)

ARM TrustZone：硬件隔离的安全世界 (Secure World) 和普通世界 (Normal World)。
在安全世界运行敏感操作 (指纹验证、支付、密钥管理)。
**安全启动 (Secure Boot)**：ROM 代码验证 Bootloader 签名，链式验证 (Chain of Trust) 操作系统。

### 14.2 加密引擎 (Crypto Engine)

**对称加密**：AES (128/256-bit)，GCM/CCM 模式。
**非对称加密**：RSA (2048/4096-bit)、ECC (Elliptic Curve Cryptography, 椭圆曲线密码学)。
**哈希函数**：SHA-256/384/512。

### 14.3 PUF (Physically Unclonable Function, 物理不可克隆函数)

利用芯片制造工艺固有的变异 (Process Variation) 生成唯一指纹。
**SRAM PUF**：上电时 SRAM 单元的初始随机状态。
**环形振荡器 PUF (RO PUF)**：频率偏差生成随机数。
用于芯片身份认证 (IC Authentication) 和密钥生成。

## 十五、SoC 测试与可测性设计 (DFT, Design for Test)

### 15.1 扫描链 (Scan Chain)

寄存器替换为扫描触发器 (Scan Flip-flop)，连接形成扫描链。
ATE 通过扫描链施加测试向量 (Test Vector) 并捕获响应。
**ATPG (Automatic Test Pattern Generation)** 生成最小测试向量集，目标覆盖 >97% 的 stuck-at 故障。

### 15.2 BIST (Built-In Self-Test, 内建自测试)

**存储器 BIST (MBIST)**：片上测试 SRAM/DRAM，使用 March 算法 (March C-/March 13n)。
**逻辑 BIST (LBIST)**：片上 PRPG (Pseudo-Random Pattern Generator) 生成测试向量 + MISR (Multiple-Input Signature Register) 压缩响应。
