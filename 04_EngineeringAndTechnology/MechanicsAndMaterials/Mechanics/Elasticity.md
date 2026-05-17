---
aliases: [Elasticity]
tags: ['04_EngineeringAndTechnology', 'MechanicsAndMaterials', 'Mechanics', 'Elasticity']
---

# 弹性力学

## 一、概述

弹性力学（Theory of Elasticity）研究弹性体在外力（体力和面力）作用下所产生的应力（Stress）、应变（Strain）和位移（Displacement）分布规律的学科。它是固体力学（Solid Mechanics）的基础分支，也是材料力学（Mechanics of Materials）的深化和推广。

## 二、基本假设

弹性力学的基本假设（经典线弹性理论）：

1. **连续性假设**（Continuum）：物质无间隙充满整个空间
2. **均匀性假设**（Homogeneity）：各点力学性质相同
3. **各向同性假设**（Isotropy）：各方向力学性质相同（各向异性理论另论）
4. **小变形假设**（Small Deformation）：变形远小于物体尺寸，应变 $\ll 1$
5. **线弹性假设**（Linear Elasticity）：应力-应变成正比，卸载后可完全恢复

## 三、应力分析

### 3.1 应力张量（Stress Tensor）

空间一点的应力状态由二阶对称张量 $\boldsymbol{\sigma}$ 描述：

$$
\boldsymbol{\sigma} = \begin{bmatrix}
\sigma_{xx} & \tau_{xy} & \tau_{xz} \\
\tau_{yx} & \sigma_{yy} & \tau_{yz} \\
\tau_{zx} & \tau_{zy} & \sigma_{zz}
\end{bmatrix}
$$

由于剪应力互等定理（Reciprocity of Shear Stresses）：

$$
\tau_{xy} = \tau_{yx}, \quad \tau_{yz} = \tau_{zy}, \quad \tau_{zx} = \tau_{xz}
$$

因此独立应力分量共 6 个。

### 3.2 主应力与应力不变量

主应力（Principal Stresses）$\sigma_1, \sigma_2, \sigma_3$ 是特征值问题：

$$
\det(\boldsymbol{\sigma} - \sigma \mathbf{I}) = 0
$$

应力不变量（Stress Invariants）：

$$
I_1 = \sigma_{xx} + \sigma_{yy} + \sigma_{zz} = \sigma_1 + \sigma_2 + \sigma_3
$$

$$
I_2 = \sigma_{xx}\sigma_{yy} + \sigma_{yy}\sigma_{zz} + \sigma_{zz}\sigma_{xx} - \tau_{xy}^2 - \tau_{yz}^2 - \tau_{zx}^2
$$

$$
I_3 = \det(\boldsymbol{\sigma})
$$

## 四、应变分析

### 4.1 应变张量

小变形条件下的应变张量（几何方程 / Cauchy 应变）：

$$
\varepsilon_{ij} = \frac{1}{2} \left( \frac{\partial u_i}{\partial x_j} + \frac{\partial u_j}{\partial x_i} \right)
$$

展开为（$u, v, w$ 分别为 $x, y, z$ 方向的位移）：

$$
\varepsilon_{xx} = \frac{\partial u}{\partial x}, \quad \varepsilon_{yy} = \frac{\partial v}{\partial y}, \quad \varepsilon_{zz} = \frac{\partial w}{\partial z}
$$

$$
\gamma_{xy} = 2\varepsilon_{xy} = \frac{\partial u}{\partial y} + \frac{\partial v}{\partial x}
$$

$$
\gamma_{yz} = 2\varepsilon_{yz} = \frac{\partial v}{\partial z} + \frac{\partial w}{\partial y}
$$

$$
\gamma_{zx} = 2\varepsilon_{zx} = \frac{\partial w}{\partial x} + \frac{\partial u}{\partial z}
$$

### 4.2 应变协调方程（Compatibility Equations）

为了保证位移场的单值连续，6 个应变分量必须满足 St. Venant 协调方程：

$$
\frac{\partial^2 \varepsilon_{xx}}{\partial y^2} + \frac{\partial^2 \varepsilon_{yy}}{\partial x^2} = \frac{\partial^2 \gamma_{xy}}{\partial x \partial y}
$$

（以及另外四个类似方程）

## 五、本构关系

### 5.1 广义胡克定律（Generalized Hooke's Law）

对各向同性线弹性材料，应力-应变关系为：

$$
\varepsilon_{xx} = \frac{1}{E} \left[ \sigma_{xx} - \nu (\sigma_{yy} + \sigma_{zz}) \right]
$$

$$
\varepsilon_{yy} = \frac{1}{E} \left[ \sigma_{yy} - \nu (\sigma_{zz} + \sigma_{xx}) \right]
$$

$$
\varepsilon_{zz} = \frac{1}{E} \left[ \sigma_{zz} - \nu (\sigma_{xx} + \sigma_{yy}) \right]
$$

$$
\gamma_{xy} = \frac{\tau_{xy}}{G}, \quad \gamma_{yz} = \frac{\tau_{yz}}{G}, \quad \gamma_{zx} = \frac{\tau_{zx}}{G}
$$

其中 $E$ 为弹性模量（Young's Modulus），$\nu$ 为泊松比（Poisson's Ratio），$G$ 为剪切模量（Shear Modulus），三者满足：

$$
G = \frac{E}{2(1+\nu)}
$$

### 5.2 Lamé 常数

各向同性弹性体可完全由两个 Lamé 常数 $\lambda$ 和 $\mu$ 描述：

$$
\sigma_{ij} = \lambda \delta_{ij} \varepsilon_{kk} + 2\mu \varepsilon_{ij}
$$

其中 $\mu = G$，$\lambda = \frac{E\nu}{(1+\nu)(1-2\nu)}$，$\varepsilon_{kk} = \varepsilon_{xx} + \varepsilon_{yy} + \varepsilon_{zz}$ 为体积应变。

## 六、平衡方程与边界条件

### 6.1 平衡方程（Equilibrium Equations）

$$
\frac{\partial \sigma_{xx}}{\partial x} + \frac{\partial \tau_{xy}}{\partial y} + \frac{\partial \tau_{xz}}{\partial z} + F_x = 0
$$

$$
\frac{\partial \tau_{xy}}{\partial x} + \frac{\partial \sigma_{yy}}{\partial y} + \frac{\partial \tau_{yz}}{\partial z} + F_y = 0
$$

$$
\frac{\partial \tau_{xz}}{\partial x} + \frac{\partial \tau_{yz}}{\partial y} + \frac{\partial \sigma_{zz}}{\partial z} + F_z = 0
$$

### 6.2 边界条件

应力边界条件（Cauchy 公式）：

$$
T_i^{(n)} = \sigma_{ji} n_j
$$

位移边界条件：

$$
u_i = \bar{u}_i \quad \text{on } S_u
$$

### 6.3 Navier 位移方程

将本构关系和几何关系代入平衡方程，得到以位移表示的控制方程：

$$
\mu \nabla^2 \mathbf{u} + (\lambda + \mu) \nabla (\nabla \cdot \mathbf{u}) + \mathbf{F} = 0
$$

## 七、平面问题

### 7.1 平面应力（Plane Stress）

薄板受力，$\sigma_{zz} = \tau_{xz} = \tau_{yz} = 0$：

$$
\begin{bmatrix}
\sigma_{xx} \\
\sigma_{yy} \\
\tau_{xy}
\end{bmatrix} = \frac{E}{1-\nu^2} \begin{bmatrix}
1 & \nu & 0 \\
\nu & 1 & 0 \\
0 & 0 & \frac{1-\nu}{2}
\end{bmatrix} \begin{bmatrix}
\varepsilon_{xx} \\
\varepsilon_{yy} \\
\gamma_{xy}
\end{bmatrix}
$$

### 7.2 平面应变（Plane Strain）

长柱形物体受横向力作用，$\varepsilon_{zz} = \gamma_{xz} = \gamma_{yz} = 0$：

$$
\begin{bmatrix}
\sigma_{xx} \\
\sigma_{yy} \\
\tau_{xy}
\end{bmatrix} = \frac{E}{(1+\nu)(1-2\nu)} \begin{bmatrix}
1-\nu & \nu & 0 \\
\nu & 1-\nu & 0 \\
0 & 0 & \frac{1-2\nu}{2}
\end{bmatrix} \begin{bmatrix}
\varepsilon_{xx} \\
\varepsilon_{yy} \\
\gamma_{xy}
\end{bmatrix}
$$

### 7.3 应力函数（Airy Stress Function）

在没有体力时，可用 Airy 应力函数 $\Phi(x,y)$ 自动满足平衡方程：

$$
\sigma_{xx} = \frac{\partial^2 \Phi}{\partial y^2}, \quad \sigma_{yy} = \frac{\partial^2 \Phi}{\partial x^2}, \quad \tau_{xy} = -\frac{\partial^2 \Phi}{\partial x \partial y}
$$

代入协调方程得到双调和方程：

$$
\nabla^4 \Phi = \frac{\partial^4 \Phi}{\partial x^4} + 2\frac{\partial^4 \Phi}{\partial x^2 \partial y^2} + \frac{\partial^4 \Phi}{\partial y^4} = 0
$$

## 八、能量法

### 8.1 应变能（Strain Energy）

应变能密度：

$$
U_0 = \frac{1}{2} \sigma_{ij} \varepsilon_{ij} = \frac{1}{2E} \left[ \sigma_{xx}^2 + \sigma_{yy}^2 + \sigma_{zz}^2 - 2\nu(\sigma_{xx}\sigma_{yy} + \sigma_{yy}\sigma_{zz} + \sigma_{zz}\sigma_{xx}) \right] + \frac{1}{2G} (\tau_{xy}^2 + \tau_{yz}^2 + \tau_{zx}^2)
$$

### 8.2 最小势能原理（Minimum Potential Energy Principle）

在所有满足位移边界条件的可能位移场中，真实位移场使总势能 $\Pi = U - W$ 取最小值。

$$\delta \Pi = 0$$

### 8.3 虚功原理（Principle of Virtual Work）

在平衡状态下，外力在虚位移上的虚功等于内力在虚应变上的虚应变能：

$$
\int_V \sigma_{ij} \delta \varepsilon_{ij} dV = \int_V F_i \delta u_i dV + \int_S T_i \delta u_i dS
$$

## 九、求解方法

| 方法 | 基本未知量 | 适用范围 |
|------|-----------|---------|
| 位移法 | 位移分量 | 通用（FEM） |
| 应力法 | 应力分量 | 静定/超静定问题 |
| 混合法 | 位移+应力 | 接触问题、弹塑性 |
| 数值方法 | 数值近似 | 复杂形状（FEM、BEM） |

## 十二、各向异性弹性

### 12.1 复合材料弹性

正交各向异性材料的广义胡克定律（9 个独立常数）：

$$
\begin{bmatrix}
\sigma_{11}\\\sigma_{22}\\\sigma_{33}\\\tau_{23}\\\tau_{13}\\\tau_{12}
\end{bmatrix} =
\begin{bmatrix}
C_{11}&C_{12}&C_{13}&0&0&0\\
C_{12}&C_{22}&C_{23}&0&0&0\\
C_{13}&C_{23}&C_{33}&0&0&0\\
0&0&0&C_{44}&0&0\\
0&0&0&0&C_{55}&0\\
0&0&0&0&0&C_{66}
\end{bmatrix}
\begin{bmatrix}
\varepsilon_{11}\\\varepsilon_{22}\\\varepsilon_{33}\\\gamma_{23}\\\gamma_{13}\\\gamma_{12}
\end{bmatrix}
$$

### 12.2 热弹性

温度变化引起的热应力：$\boldsymbol{\sigma} = \mathbf{C}(\boldsymbol{\varepsilon} - \boldsymbol{\alpha}\Delta T)$

## 相关条目
- [[04_EngineeringAndTechnology/MechanicsAndMaterials/Mechanics/INDEX|当前目录索引]]
- [[Plasticity]]
- [[FractureMechanics]]
- [[Nanomaterials]]
