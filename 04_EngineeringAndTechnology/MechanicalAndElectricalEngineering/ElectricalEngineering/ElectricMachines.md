---
aliases: [ElectricMachines]
tags: ['MechanicalAndElectricalEngineering', 'ElectricalEngineering', 'ElectricMachines']
created: 2026-05-16
updated: 2026-05-16
---

# 电机学

## 定义
电机学是研究电机（发电机、电动机、变压器等）的工作原理、结构、性能、分析方法和运行特性的学科。

## 研究对象
- 变压器的工作原理与特性
- 直流电机的原理与控制
- 异步电机的原理与分析
- 同步电机的原理与运行

## 核心内容

### 变压器

**工作原理**：基于电磁感应定律，通过交变磁通实现能量传递。

**电压方程**：

$$\dot{V}_1 = -\dot{E}_1 + \dot{I}_1(R_1 + jX_1)$$
$$\dot{V}_2 = \dot{E}_2 - \dot{I}_2(R_2 + jX_2)$$

**等效电路（归算到一次侧）**：

$$R_2' = k^2 R_2, \quad X_2' = k^2 X_2$$

其中 $k = N_1/N_2$ 为变比。

**效率**：

$$\eta = \frac{\beta S_N \cos\varphi_2}{\beta S_N \cos\varphi_2 + P_0 + \beta^2 P_k}$$

$\beta = I_2/I_{2N}$ 为负载系数，$P_0$ 为空载损耗，$P_k$ 为短路损耗。

**最大效率条件**：$P_0 = \beta^2 P_k$

**电压调整率**：$\Delta V\% = \frac{V_{2N} - V_2}{V_{2N}} \times 100\%$，反映负载变化时输出电压的稳定性

### 直流电机

**工作原理**：载流导体在磁场中受力（$F = BIL$），同时导体切割磁力线产生感应电动势（$E = BLv$）。

**感应电动势**：

$$E = C_e \Phi n, \quad C_e = \frac{pN}{60a}$$

**电磁转矩**：

$$T = C_T \Phi I_a, \quad C_T = 9.55 C_e$$

**励磁方式**：
- 他励：励磁绕组独立供电
- 并励：励磁绕组与电枢并联
- 串励：励磁绕组与电枢串联
- 复励：并励+串励

**调速方法**：
- 调压调速：降低电枢电压
- 弱磁调速：减小励磁磁通
- 电阻调速：增大电枢回路电阻

### 异步电机（感应电机）

**旋转磁场**：

$$n_1 = \frac{60f}{p}$$

$f$ 为电源频率，$p$ 为磁极对数。

**转差率**：

$$s = \frac{n_1 - n}{n_1}$$

**感应电动势**：

$$E_1 = 4.44f_1 N_1 k_{w1} \Phi_m$$

**等效电路（T 型）**：

定子阻抗 $Z_1 = R_1 + jX_1$

励磁阻抗 $Z_m = R_m + jX_m$

转子阻抗（归算）：$Z_2' = \frac{R_2'}{s} + jX_2'$

**功率关系**：

$$P_1 = P_{Cu1} + P_{Fe} + P_{mech} + P_{Cu2} + P_{misc}$$

电磁功率：$P_{em} = 3I_2'^2 \frac{R_2'}{s}$

机械功率：$P_{mech} = (1-s)P_{em}$

**机械特性**：

$$T = \frac{3p}{2\pi f_1}\cdot\frac{U_1^2 R_2'/s}{(R_1+R_2'/s)^2+(X_1+X_2')^2}$$

最大转矩：$T_{max} \propto \frac{U_1^2}{2(X_1+X_2')}$

启动转矩：$T_{st} = \frac{3p}{2\pi f_1}\cdot\frac{U_1^2 R_2'}{(R_1+R_2')^2+(X_1+X_2')^2}$

### 同步电机

**功角特性**：

隐极机：$P = \frac{mEV}{X_d}\sin\delta$

凸极机：$P = \frac{mEV}{X_d}\sin\delta + \frac{mV^2}{2}\left(\frac{1}{X_q}-\frac{1}{X_d}\right)\sin 2\delta$

**V 形曲线**：电枢电流 $I_a$ 与励磁电流 $I_f$ 的关系
- 正常励磁：$I_a$ 最小（纯有功）
- 过励磁：输出感性无功（$I_a$ 超前 $V$）
- 欠励磁：吸收感性无功（$I_a$ 滞后 $V$）

**同步发电机运行特性**：
- 空载特性：$E_0 = f(I_f)$
- 短路特性：$I_k = f(I_f)$
- 外特性：$V = f(I)$

### 电机选型

**选型原则**：
- 功率匹配：$P_N \geq P_{load}$
- 电压等级：与电网电压一致
- 转速匹配：额定转速满足要求
- 工作环境：防护等级、绝缘等级
- 经济性：效率、维护成本

**常用电机类型对比**：

| 类型 | 功率范围 | 调速性能 | 效率 | 功率因数 | 应用 |
|------|---------|---------|------|---------|------|
| 三相异步 | 0.1kW–10MW | 差（变频可调） | 85–95% | 0.7–0.9 | 风机、泵、压缩机 |
| 三相同步 | 100kW–GW 级 | 好 | 95–98% | 1.0（可调） | 大功率、恒速 |
| 直流电机 | 0.1kW–MW 级 | 优 | 80–90% | — | 起重机、轧机 |
| 永磁同步（PMSM） | 0.1kW–MW 级 | 优 | 92–97% | 接近1.0 | 伺服系统、EV |
| 开关磁阻（SRM） | 1kW–500kW | 好 | 85–93% | — | 家电、航空 |

**功率因数**：$\cos\varphi = \frac{P}{S} = \frac{P}{\sqrt{P^2 + Q^2}}$

**电机效率**：$\eta = \frac{P_{out}}{P_{in}} = 1 - \frac{\sum P_{loss}}{P_{in}}$

## 经典教材
- 汤蕴璆《电机学》
- 陈世坤《电机设计》
- Chapman《Electric Machinery Fundamentals》
- Fitzgerald & Kingsley《Electric Machinery》

## 主要应用领域
- 工业驱动（各类机械传动）
- 电力系统（发电机、变压器）
- 交通运输（电动汽车驱动电机）
- 家用电器（空调压缩机、洗衣机）
- 航空航天（飞机发电系统）
- 新能源（风力发电机、光伏逆变器）

## 相关条目

- [[PowerSystems]]
- [[CircuitAnalysis]]
- [[04_EngineeringAndTechnology/MechanicalAndElectricalEngineering/Mechatronics/ControlSystems|ControlSystems]]
- [[04_EngineeringAndTechnology/EnergyAndNuclearEngineering/RenewableEnergy/INDEX|RenewableEnergy]]


