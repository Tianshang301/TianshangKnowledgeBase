---
aliases: [SemiconductorPhysics]
tags: ['ElectronicsAndCommunications', 'Microelectronics', 'SemiconductorPhysics']
created: 2026-05-16
updated: 2026-05-16
---

# 半导体物理

## 定义
半导体物理是研究半导体材料的物理性质、载流子行为和半导体器件工作原理的学科。是微电子技术和光电子技术的理论基础。

## 研究对象
- 能带理论与载流子分布
- 半导体中的输运现象
- PN 结原理
- MOSFET 工作原理

## 核心内容

### 能带理论

**能带结构**：
- 导带：电子可自由运动的能带
- 价带：电子被束缚的能带
- 禁带：导带底与价带顶之间的能量间隙 $E_g$

**典型半导体禁带宽度**：
- Si：$E_g = 1.12$ eV（间接带隙）
- Ge：$E_g = 0.66$ eV（间接带隙）
- GaAs：$E_g = 1.43$ eV（直接带隙）
- SiC：$E_g = 3.26$ eV（宽禁带）

**本征载流子浓度**：

$$n_i = \sqrt{N_c N_v}\exp\left(-\frac{E_g}{2kT}\right)$$

$N_c$、$N_v$ 分别为导带和价带的有效态密度。

### 半导体中的载流子

**电子与空穴**：
- 电子：带负电的自由载流子
- 空穴：价带中电子空位等效为正电荷载流子

**载流子浓度**：
- 电中性条件：$n + N_A^- = p + N_D^+$
- 费米-狄拉克分布：$f(E) = \frac{1}{1+\exp[(E-E_F)/kT]}$

**掺杂**：
- N 型掺杂：施主杂质（P、As）提供电子
- P 型掺杂：受主杂质（B、Ga）提供空穴
- $n \approx N_D$（N 型），$p \approx N_A$（P 型）

### PN 结原理

**PN 结形成**：
- 扩散运动：载流子从高浓度向低浓度扩散
- 漂移运动：内建电场驱动载流子
- 耗尽层：载流子耗尽的空间电荷区

**内建电势**：

$$V_{bi} = \frac{kT}{q}\ln\left(\frac{N_A N_D}{n_i^2}\right)$$

**PN 结电流方程**：

$$I = I_s\left[\exp\left(\frac{qV}{nkT}\right) - 1\right]$$

$I_s$ 为反向饱和电流，$n$ 为理想因子（1~2）。

**击穿机制**：
- 雪崩击穿：高电场加速载流子→碰撞电离
- 齐纳击穿：高掺杂 PN 结的量子隧穿
- 击穿电压：$V_{BR} \propto 1/N_B^{0.75}$

### MOSFET 工作原理

**MOS 结构**：
- 金属-氧化物-半导体三层结构
- 栅极电压控制半导体表面电场

**工作模式**：
- 反型层形成：$V_{GS} > V_{th}$
- 强反型：$V_{GS} - V_{th} > 0$

**转移特性（饱和区）**：

$$I_D = \frac{1}{2}\mu_n C_{ox}\frac{W}{L}(V_{GS}-V_{th})^2$$

**输出特性**：
- 线性区：$V_{DS} < V_{GS} - V_{th}$
  $I_D = \mu_n C_{ox}\frac{W}{L}\left[(V_{GS}-V_{th})V_{DS}-\frac{V_{DS}^2}{2}\right]$
- 饱和区：$V_{DS} \geq V_{GS} - V_{th}$
  $I_D = \frac{1}{2}\mu_n C_{ox}\frac{W}{L}(V_{GS}-V_{th})^2(1+\lambda V_{DS})$

**短沟道效应**：
- 阈值电压漂移
- 载流子速度饱和
- DIBL（漏致势垒降低）
- 热载流子效应

**亚阈值区**：

$$I_D \propto \exp\left(\frac{q(V_{GS}-V_{th})}{nkT}\right)$$

## 经典教材
- 刘恩科《半导体物理学》
- Neamen《Semiconductor Physics and Devices》
- Sze《Physics of Semiconductor Devices》
- Pierret《Semiconductor Device Fundamentals》

## 主要应用领域
- 集成电路制造
- 分立器件（二极管、MOSFET）
- 功率电子器件（IGBT、SiC MOSFET）
- 光电器件（LED、激光器、太阳能电池）
- 传感器（MEMS、CMOS 图像传感器）
- 宽禁带半导体（GaN、SiC）

## 相关条目

- [[ICDesign]]
- [[04_EngineeringAndTechnology/ElectronicsAndCommunications/Electronics/AnalogElectronics|AnalogElectronics]]
- [[04_EngineeringAndTechnology/ElectronicsAndCommunications/Electronics/DigitalElectronics|DigitalElectronics]]
- SolidStatePhysics
- [[04_EngineeringAndTechnology/MechanicsAndMaterials/MaterialsScience/INDEX|MaterialsScience]]


