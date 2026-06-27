---
aliases: [Dynamics, 动力学]
tags: ['EngineeringFundamentals', 'EngineeringMechanics', 'Dynamics']
created: 2026-05-17
updated: 2026-05-13
---

# 动力学 (Dynamics)

## 定义

动力学是研究物体运动与作用力之间关系的学科。工程动力学主要分析力、质量与加速度之间的因果关系，是机械、航空、土木等工程领域的基础。

## 核心内容

### 质点动力学 (Particle Dynamics)

**牛顿第二定律**：

$$
\vec{F} = m\vec{a}
$$

**质点运动微分方程**——直角坐标形式：

$$
m\ddot{x} = \sum F_x, \quad m\ddot{y} = \sum F_y, \quad m\ddot{z} = \sum F_z
$$

**自然坐标形式**（切向与法向）：

$$
F_t = m\frac{dv}{dt} = ma_t, \quad F_n = m\frac{v^2}{\rho} = ma_n
$$

**极坐标形式**（径向与横向）：

$$
F_r = m(\ddot{r} - r\dot{\theta}^2), \quad F_\theta = m(r\ddot{\theta} + 2\dot{r}\dot{\theta})
$$

### 动量定理 (Impulse-Momentum Principle)

**动量 (Linear Momentum)**：

$$
\vec{P} = m\vec{v}
$$

**冲量 (Impulse)**：

$$
\vec{I} = \int_{t_1}^{t_2} \vec{F} \, dt
$$

**动量定理**：

$$
m\vec{v}_2 - m\vec{v}_1 = \int_{t_1}^{t_2} \vec{F} \, dt
$$

**动量守恒**：当 $\sum \vec{F} = 0$ 时：

$$
\vec{P} = m\vec{v} = \text{常数}
$$

### 动量矩定理 (Angular Momentum Principle)

**动量矩 (Angular Momentum)**——对固定点 O：

$$
\vec{L}_O = \vec{r} \times m\vec{v}
$$

**动量矩定理**：

$$
\frac{d\vec{L}_O}{dt} = \vec{M}_O
$$

其中 $\vec{M}_O = \vec{r} \times \vec{F}$ 为外力对 O 点的主矩。

**动量矩守恒**：当 $\vec{M}_O = 0$ 时：

$$
\vec{L}_O = \text{常数}
$$

### 动能定理 (Work-Energy Principle)

**功 (Work)**：

$$
W = \int_{s_1}^{s_2} \vec{F} \cdot d\vec{r} = \int_{s_1}^{s_2} F\cos\theta \, ds
$$

**动能 (Kinetic Energy)**：

- 平动：$T = \frac{1}{2}mv^2$
- 转动：$T = \frac{1}{2}J\omega^2$
- 平面运动：$T = \frac{1}{2}mv_C^2 + \frac{1}{2}J_C\omega^2$

**动能定理**：

$$
T_2 - T_1 = \sum W_{1 \to 2}
$$

**机械能守恒**（保守力系）：

$$
T_1 + V_1 = T_2 + V_2
$$

### 达朗贝尔原理 (D'Alembert's Principle)

**惯性力 (Inertial Force)**：

$$
\vec{F}_I = -m\vec{a}
$$

**达朗贝尔原理**——将动力学问题化为静力学平衡：

$$
\sum \vec{F} + \vec{F}_I = 0
$$

**质点系的达朗贝尔原理**：

$$
\sum(\vec{F}_i + \vec{F}_{Ii}) = 0, \quad \sum(\vec{M}_{O_i} + \vec{M}_{OI_i}) = 0
$$

### 虚位移原理与拉格朗日方程

**理想约束**：约束反力在虚位移上所作虚功之和为零。

**虚位移原理 (Principle of Virtual Work)**：

$$
\sum \vec{F}_i \cdot \delta\vec{r}_i = 0
$$

**拉格朗日方程 (Lagrange's Equations)**：

$$
\frac{d}{dt}\left(\frac{\partial L}{\partial \dot{q}_j}\right) - \frac{\partial L}{\partial q_j} = Q_j
$$

其中 $L = T - V$ 为拉格朗日函数，$q_j$ 为广义坐标，$Q_j$ 为非有势力对应的广义力。

### 刚体动力学 (Rigid Body Dynamics)

**刚体平面运动微分方程**：

$$
\sum F_x = ma_{Cx}, \quad \sum F_y = ma_{Cy}, \quad \sum M_C = J_C\alpha
$$

**转动惯量 (Moment of Inertia)**：

- 细杆绕中心：$J = \frac{1}{12}ml^2$
- 细杆绕端点：$J = \frac{1}{3}ml^2$
- 圆盘：$J = \frac{1}{2}mR^2$
- 圆环：$J = mR^2$

**平行轴定理 (Parallel Axis Theorem)**：

$$
J = J_C + md^2
$$

### 机械振动 (Mechanical Vibrations)

**单自由度系统的自由振动**：

$$
m\ddot{x} + kx = 0
$$

固有频率：$\omega_n = \sqrt{k/m}$

**受迫振动**：

$$
m\ddot{x} + c\dot{x} + kx = F_0\sin(\omega t)
$$

稳态解振幅：

$$
X = \frac{F_0/k}{\sqrt{(1-r^2)^2 + (2\zeta r)^2}}
$$

其中 $r = \omega/\omega_n$ 为频率比，$\zeta = c/(2\sqrt{mk})$ 为阻尼比。

### 动力学普遍定理总结

| 定理 | 矢量/标量 | 守恒条件 |
|------|-----------|---------|
| 动量定理 | 矢量 | $\sum\vec{F}=0$ |
| 动量矩定理 | 矢量 | $\sum\vec{M}_O=0$ |
| 动能定理 | 标量 | 保守系统机械能守恒 |

## 经典教材

- 哈尔滨工业大学《理论力学（下）》
- Meriam & Kraige《Engineering Mechanics: Dynamics》
- Hibbeler《Engineering Mechanics: Dynamics》
- 张雄《理论力学》

## 主要应用领域

- 机械系统动力学分析
- 车辆行驶动力学
- 飞行器飞行动力学
- 结构抗震与抗风
- 机器人运动控制
- 多体系统仿真

## 相关条目

- [[Statics]]
- [[EngineeringMechanics]]
- [[StructuralAnalysis]]
- [[VibrationAnalysis]]
