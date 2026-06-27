---
aliases: [SensorTechnology]
tags: ['MechanicalAndElectricalEngineering', 'InstrumentScience', 'SensorTechnology']
created: 2026-05-16
updated: 2026-05-16
---

# 传感器技术

## 定义
传感器是能感受被测量并按照一定规律转换成可用输出信号（通常为电信号）的器件或装置。传感器技术是信息获取的核心技术。

## 研究对象
- 传感器的工作原理与分类
- 各类物理量传感器的结构与特性
- 传感器信号调理电路
- 智能传感器与物联网

## 核心内容

### 传感器分类

**按工作原理分类**：
- 电阻式：电阻应变片、热敏电阻、压敏电阻
- 电容式：变极距型、变面积型、变介质型
- 电感式：自感式、互感式（差动变压器）
- 压电式：石英晶体、压电陶瓷
- 热电式：热电偶、热敏电阻
- 光电式：光敏电阻、光电二极管、CCD

**按被测量分类**：
- 位移、速度、加速度传感器
- 力、压力、扭矩传感器
- 温度、湿度传感器
- 流量、液位传感器
- 气体、化学传感器

### 温度传感器

**热电偶**：
- 原理：塞贝克效应（温差电势）
- 热电势：$E = S(T_1 - T_2)$，$S$ 为塞贝克系数
- 常用类型：K 型（镍铬-镍硅）、J 型（铁-铜镍）、T 型（铜-铜镍）、S 型（铂铑-铂）
- 测温范围：-200°C ~ 1800°C
- 特点：测温范围宽、响应快、可远传

**热敏电阻**：
- NTC（负温度系数）：电阻随温度升高而降低
  - $R = R_0 \exp\left[B\left(\frac{1}{T}-\frac{1}{T_0}\right)\right]$
- PTC（正温度系数）：电阻随温度升高而增加
- 特点：灵敏度高、体积小、响应快

**RTD（热电阻）**：
- 铂电阻（Pt100、Pt1000）：精度高、稳定性好
- 铜电阻（Cu50、Cu100）：成本低
- 线性度好，但灵敏度较低

### 压力传感器

**应变式压力传感器**：
- 电阻应变片粘贴在弹性体上
- 灵敏系数：$K = \frac{\Delta R/R}{\varepsilon}$
- 惠斯通电桥输出：$\frac{\Delta V}{V} = \frac{K\varepsilon}{4}$

**压阻式压力传感器**：
- 半导体压阻效应
- 灵敏度高（比金属应变片高50~100倍）
- 温度稳定性较差

**电容式压力传感器**：
- $C = \frac{\varepsilon A}{d}$，压力改变 $d$ 或 $A$
- 灵敏度高、功耗低
- 适用于微压测量

### 位移传感器

**电感式（LVDT）**：
- 线性可变差动变压器
- 输出电压与位移成线性关系
- 分辨率高、抗干扰能力强

**电容式位移传感器**：
- 非接触测量
- 分辨率可达纳米级
- 适合精密测量

**光栅尺**：
- 莫尔条纹原理
- 数字输出，精度高
- 分辨率：0.1μm ~ 1μm

**编码器**：
- 光电编码器：增量式/绝对式
- 旋转编码器：测角位移
- 直线编码器：测线位移

### 传感器信号调理

**放大电路**：
- 仪表放大器：高共模抑制比（CMRR > 100dB）
- 低噪声放大

**滤波电路**：
- 低通滤波：去除高频噪声
- 陷波滤波：去除50Hz 工频干扰

**A/D 转换**：
- 分辨率：12位、16位、24位
- 采样定理：$f_s \geq 2f_{max}$
- 过采样技术提高分辨率

**线性化**：
- 查表法
- 多项式拟合
- 数字线性化

### 智能传感器与物联网

**智能传感器特点**：
- 内置微处理器
- 自诊断、自校准
- 数字输出（SPI、I²C、UART）
- 数据存储与预处理

**物联网（IoT）传感器**：
- 无线传感网络（WSN）
- 低功耗设计（μA 级）
- 通信协议：Zigbee、LoRa、NB-IoT
- 边缘计算与云平台集成

**MEMS 传感器**：
- 微机电系统技术
- 加速度计、陀螺仪、压力传感器
- 体积小、成本低、批量生产

## 经典教材
- 刘迎春《传感器原理与应用》
- 贾伯年《传感器技术》
- Fraden《Handbook of Modern Sensors》
- Webster《Measurement, Instrumentation and Sensors Handbook》

## 主要应用领域
- 工业自动化（过程控制、质量检测）
- 汽车电子（ABS、安全气囊、胎压监测）
- 医疗器械（体温、血压、血氧监测）
- 智能家居（温湿度、烟雾、人体感应）
- 环境监测（PM2.5、水质、噪声）
- 航空航天（惯性导航、姿态测量）

## 相关条目

- [[MeasurementTheory]]
- [[04_EngineeringAndTechnology/MechanicalAndElectricalEngineering/Mechatronics/ControlSystems|ControlSystems]]
- [[04_EngineeringAndTechnology/MechanicalAndElectricalEngineering/Mechatronics/RoboticsBasics|RoboticsBasics]]
- [[04_EngineeringAndTechnology/ElectronicsAndCommunications/SignalProcessing/INDEX|SignalProcessing]]
- [[04_EngineeringAndTechnology/MechanicalAndElectricalEngineering/Mechatronics/PLCProgramming|PLCProgramming]]


