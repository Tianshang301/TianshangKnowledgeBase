---
aliases: [Statics]
tags: ['EngineeringFundamentals', 'EngineeringMechanics', 'Statics']
---

# 静力学

## 定义
静力学是研究物体在力系作用下平衡条件的学科。是工程力学的基础部分。

## 核心内容

### 基本概念

**力**：物体间的相互机械作用

**力的三要素**：大小、方向、作用点

**刚体**：在外力作用下形状和大小不变的物体

### 力系简化

**力的合成**：平行四边形法则

**力偶**：等值反向平行力，$M = Fd$

**力系简化**：
- 主矢：$\vec{R} = \sum\vec{F}$
- 主矩：$\vec{M}_O = \sum\vec{r}_i \times \vec{F}_i$

### 平衡条件

**空间力系平衡**：

$$\sum F_x = 0, \sum F_y = 0, \sum F_z = 0$$
$$\sum M_x = 0, \sum M_y = 0, \sum M_z = 0$$

**平面力系平衡**：

$$\sum F_x = 0, \sum F_y = 0, \sum M_O = 0$$

### 约束与约束力

**光滑接触面**：沿法线方向

**铰链约束**：两个正交分力

**固定端约束**：两个分力+一个力偶矩

### 桁架分析

**节点法**：逐个节点列平衡方程

**截面法**：截断杆件，对截面列平衡方程

### 摩擦

**静摩擦力**：$0 \leq F \leq F_{max} = f_s N$

**动摩擦力**：$F = f_k N$

## 经典教材
- 哈尔滨工业大学《理论力学》
- 《静力学》
- Meriam《Engineering Mechanics: Statics》
- Hibbeler《Engineering Mechanics: Statics》

## 主要应用领域
- 结构受力分析
- 机械零件设计
- 起重设备设计
- 桥梁结构分析
