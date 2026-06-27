---
aliases: [ICDesign]
tags: ['ElectronicsAndCommunications', 'Microelectronics', 'ICDesign']
created: 2026-05-16
updated: 2026-05-16
---

# 集成电路设计

## 定义
集成电路设计是利用 EDA 工具设计和验证集成电路芯片的过程，包括数字 IC 设计、模拟 IC 设计和混合信号 IC 设计。

## 研究对象
- CMOS 工艺基础
- 数字 IC 设计流程
- 模拟 IC 设计方法
- FPGA 设计与 ASIC 对比

## 核心内容

### CMOS 工艺基础

**CMOS 反相器**：
- PMOS 上拉网络 + NMOS 下拉网络
- 静态功耗极低
- 噪声容限高

**CMOS 工艺节点**：
- 180nm → 130nm → 90nm → 65nm → 40nm → 28nm → 14nm → 7nm → 5nm
- 节点缩小→速度提高、功耗降低、集成度提高

**工艺参数**：
- 阈值电压 $V_{th}$
- 迁移率 $\mu$
- 栅氧化层厚度 $t_{ox}$
- 电源电压 $V_{DD}$

### 数字 IC 设计流程

**RTL 设计**：
- Verilog/VHDL 编写 RTL 代码
- 功能仿真验证
- 代码覆盖率分析

**逻辑综合**：
- RTL→门级网表
- 工具：Design Compiler（Synopsys）
- 约束：时序、面积、功耗
- 工艺库：.lib 文件

**布局布线（P&R）**：
- 布局规划（Floorplan）
- 布线（Place & Route）
- 工具：ICC2（Synopsys）、Innovus（Cadence）
- 物理验证：DRC、LVS、ERC

**时序分析**：
- 静态时序分析（STA）
- 建立时间约束：$T_{clk} > T_{cq} + T_{logic} + T_{setup}$
- 保持时间约束：$T_{hold} < T_{cq} + T_{logic}$

### 模拟 IC 设计

**运算放大器设计**：
- 折叠共源共栅运放
- 增益提高技术
- 轨到轨输入/输出
- 增益带宽积（GBW）

**ADC 设计**：
- 逐次逼近型（SAR）：中速中精度
- 流水线型（Pipeline）：高速高精度
- Σ-Δ型：低速高精度
- 性能指标：ENOB、SNDR、SFDR

**DAC 设计**：
- 电阻串型
- 电荷再分配型
- 电流舵型
- 性能指标：INL、DNL

**PLL（锁相环）**：
- 组成：鉴相器（PD）→环路滤波器（LF）→压控振荡器（VCO）
- 锁定条件：$f_{out} = N \cdot f_{ref}$
- 应用：时钟生成、频率综合

### FPGA 设计

**FPGA 结构**：
- 可配置逻辑块（CLB）
- 布线资源
- I/O 块
- 嵌入式 RAM/DSP

**设计流程**：
- RTL 设计 → 功能仿真 → 综合 → 仿真 → 布局布线 → 时序分析 → 下载配置

**HDL 语言**：
- Verilog：C 风格语法
- VHDL：Ada 风格语法
- SystemVerilog：面向验证

### ASIC 与 FPGA 对比

| 特性 | ASIC | FPGA |
|------|------|------|
| 开发成本 | 高（百万美元级） | 低（几千~几万美元） |
| 开发周期 | 6~18个月 | 几天~几周 |
| 性能 | 高 | 中等 |
| 功耗 | 低 | 较高 |
| 量产成本 | 低 | 高 |
| 灵活性 | 不可修改 | 可重配置 |
| 适用场景 | 大批量产品 | 原型验证、小批量 |

## 经典教材
- 西门·哈德《CMOS VLSI Design: A Circuits and Systems Perspective》
- Razavi《Design of Analog CMOS Integrated Circuits》
- 刘雷波《数字集成电路设计》
- Rabaey《Digital Integrated Circuits: A Design Perspective》

## 主要应用领域
- 处理器芯片（CPU、GPU、DSP）
- 存储器芯片（DRAM、NAND Flash）
- 通信芯片（基带、射频）
- 消费电子芯片（手机 SoC）
- 汽车电子芯片（MCU、传感器）
- AI 芯片（NPU、TPU）

## 相关条目

- [[SemiconductorPhysics]]
- [[DigitalElectronics]]
- [[AnalogElectronics]]
- [[ComputerArchitecture]]
- [[DigitalSignalProcessing]]
