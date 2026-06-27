---
aliases: [Statics, 静力学]
tags: ['EngineeringFundamentals', 'EngineeringMechanics', 'Statics']
created: 2026-05-17
updated: 2026-05-17
---

# 静力学 (Statics)

## 定义

静力学是研究物体在力系作用下处于平衡条件的科学。它是工程力学的基础，为结构分析、机械设计等提供核心理论支撑。

## 核心内容

### 基本概念与公理

**力的三要素**：大小、方向、作用点。

**静力学公理**：

1. **二力平衡公理**：作用在同一刚体上的两个力使物体平衡的充要条件是等值、反向、共线。
2. **加减平衡力系公理**：在力系上加上或减去平衡力系，不改变原力系对刚体的效应。
3. **力的平行四边形法则**：作用于同一点的两个力，其合力由平行四边形对角线表示。
4. **作用与反作用定律**：两物体间的作用力与反作用力等值、反向、共线。

$$
\vec{F}_{AB} = -\vec{F}_{BA}
$$

### 力系简化 (Reduction of Force Systems)

**力在轴上的投影**：

$$
F_x = F\cos\alpha, \quad F_y = F\cos\beta, \quad F_z = F\cos\gamma
$$

**力对点的矩 (Moment about a Point)**：

$$
\vec{M}_O(\vec{F}) = \vec{r} \times \vec{F}
$$

**力对轴的矩 (Moment about an Axis)**：

$$
M_z(\vec{F}) = M_O(\vec{F}_{xy})
$$

**力偶 (Couple)**：等值、反向、不共线的平行力。

力偶矩：$M = F \cdot d$（$d$ 为力偶臂）

**力系简化结果**：

- **主矢**：$\vec{R} = \sum \vec{F}_i$
- **主矩**：$\vec{M}_O = \sum (\vec{r}_i \times \vec{F}_i)$

### 平衡条件 (Equilibrium Conditions)

**空间一般力系平衡方程**（六个独立方程）：

$$
\sum F_x = 0, \quad \sum F_y = 0, \quad \sum F_z = 0
$$

$$
\sum M_x = 0, \quad \sum M_y = 0, \quad \sum M_z = 0
$$

**平面一般力系平衡方程**（三个独立方程）：

$$
\sum F_x = 0, \quad \sum F_y = 0, \quad \sum M_O = 0
$$

**平面汇交力系**（两个独立方程）：

$$
\sum F_x = 0, \quad \sum F_y = 0
$$

**平面平行力系**（两个独立方程）：

$$
\sum F_y = 0, \quad \sum M_O = 0
$$

### 约束与约束力 (Constraints & Reactions)

| 约束类型 | 约束特征 | 未知数 | 约束力表示 |
|---------|---------|--------|-----------|
| 光滑接触面 | 沿法线方向 | 1 | $N$ |
| 柔软绳索 | 沿绳索方向受拉 | 1 | $T$ |
| 光滑圆柱铰链 | 两个正交分力 | 2 | $F_x, F_y$ |
| 固定铰支座 | 两个正交分力 | 2 | $F_x, F_y$ |
| 可动铰支座 | 沿法线方向 | 1 | $F_y$ |
| 固定端 | 两个分力+一个力偶 | 3 | $F_x, F_y, M$ |
| 球形铰链 | 三个正交分力 | 3 | $F_x, F_y, F_z$ |

### 桁架分析 (Truss Analysis)

**基本假设**：所有杆件均为二力杆，节点为光滑铰链，荷载作用于节点。

**节点法 (Method of Joints)**：

逐节点建立平衡方程求解杆件内力。平面桁架每个节点提供两个方程：

$$
\sum F_x = 0, \quad \sum F_y = 0
$$

**截面法 (Method of Sections)**：

用截面截断桁架，取部分为隔离体，建立平衡方程直接求解特定杆件内力。

**零力杆判别规则**：

- 两杆节点无外力：两杆均为零力杆
- 三杆节点无外力，两杆共线：第三杆为零力杆

### 摩擦 (Friction)

**静摩擦 (Static Friction)**：

$$
0 \leq F \leq F_{max} = \mu_s N
$$

**动摩擦 (Kinetic Friction)**：

$$
F = \mu_k N
$$

**摩擦角 (Angle of Friction)**：

$$
\tan\phi = \frac{F_{max}}{N} = \mu_s
$$

**自锁现象 (Self-Locking)**：当主动力作用线位于摩擦锥内时，无论力多大物体均保持静止。

### 重心与形心 (Centroids & Centers of Gravity)

**重心坐标**：

$$
x_C = \frac{\int x \, dW}{\int dW}, \quad y_C = \frac{\int y \, dW}{\int dW}, \quad z_C = \frac{\int z \, dW}{\int dW}
$$

**形心坐标**（均质物体）：

$$
x_C = \frac{\int x \, dA}{\int dA}, \quad y_C = \frac{\int y \, dA}{\int dA}
$$

**组合体的形心**：

$$
x_C = \frac{\sum A_i x_{Ci}}{\sum A_i}, \quad y_C = \frac{\sum A_i y_{Ci}}{\sum A_i}
$$

### 惯性矩 (Moment of Inertia)

**定义**：

$$
I_x = \int y^2 \, dA, \quad I_y = \int x^2 \, dA
$$

**极惯性矩 (Polar Moment of Inertia)**：

$$
J_O = I_x + I_y = \int (x^2 + y^2) \, dA
$$

**平行轴定理 (Parallel Axis Theorem)**：

$$
I_x = I_{xC} + A d_y^2, \quad I_y = I_{yC} + A d_x^2
$$

**常见截面的惯性矩**：

| 截面形状 | $I_x$ | $I_y$ |
|---------|-------|-------|
| 矩形 $b \times h$ | $bh^3/12$ | $hb^3/12$ |
| 圆形 $d$ | $\pi d^4/64$ | $\pi d^4/64$ |
| 圆环 $D, d$ | $\pi(D^4-d^4)/64$ | $\pi(D^4-d^4)/64$ |
| 三角形 $b \times h$ | $bh^3/36$ | — |

## 经典教材

- 哈尔滨工业大学《理论力学（上）》
- Meriam & Kraige《Engineering Mechanics: Statics》
- Hibbeler《Engineering Mechanics: Statics》
- 同济大学《静力学》

## 主要应用领域

- 建筑与桥梁结构受力分析
- 机械系统构件的强度设计
- 起重设备与工程机械设计
- 航空航天结构静力计算
- 船舶与海洋结构稳性分析

## 相关条目

- [[Dynamics]]
- [[04_EngineeringAndTechnology/MechanicsAndMaterials/Mechanics/EngineeringMechanics|EngineeringMechanics]]
- [[04_EngineeringAndTechnology/CivilEngineering/StructuralEngineering/StructuralAnalysis|StructuralAnalysis]]
- [[MechanicsOfMaterials]]
- [[04_EngineeringAndTechnology/CivilEngineering/GeotechnicalEngineering/SoilMechanics|SoilMechanics]]


