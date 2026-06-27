---
aliases: [SolidMechanics]
tags: ['MechanicsAndMaterials', 'Mechanics', 'SolidMechanics']
created: 2026-05-16
updated: 2026-05-13
---

# 固体力学

## 定义
固体力学是研究可变形固体在外力、温度变化及其他外界因素作用下的应力、应变、位移及稳定性的学科。它是力学的重要分支，为工程结构设计提供理论基础。

## 研究对象
- 弹性体、塑性体、粘弹性体等可变形固体
- 杆、板、壳、块体等典型结构构件
- 复合材料结构、多孔介质等复杂材料体系

## 核心内容

### 基本定义

**正应力（轴向拉压）：**

$$\sigma = \frac{F}{A}$$

**正应变：**

$$\varepsilon = \frac{\Delta L}{L}$$

**胡克定律（一维）：**

$$\sigma = E\varepsilon$$

### 梁弯曲

**弯曲正应力公式：**

$$\sigma = \frac{My}{I}$$

其中 $M$ 为弯矩，$y$ 为距中性轴的距离，$I$ 为截面惯性矩。

### 压杆稳定

**欧拉临界载荷：**

$$P_{cr} = \frac{\pi^2 EI}{(\mu L)^2}$$

其中 $\mu$ 为长度因数（取决于约束条件），$\mu L$ 为有效长度。

### 应力圆（莫尔圆）

莫尔圆用于图解一点处的应力状态。在 $\sigma$-$\tau$ 坐标系中，圆心为 $\left(\frac{\sigma_x + \sigma_y}{2}, 0\right)$，半径为 $\sqrt{\left(\frac{\sigma_x - \sigma_y}{2}\right)^2 + \tau_{xy}^2}$。

### 应力与应变（张量表示）

**应力张量**：物体内一点的应力状态用二阶张量表示：

$$\sigma_{ij} = \begin{pmatrix} \sigma_{xx} & \tau_{xy} & \tau_{xz} \\ \tau_{yx} & \sigma_{yy} & \tau_{yz} \\ \tau_{zx} & \tau_{zy} & \sigma_{zz} \end{pmatrix}$$

其中 $\sigma_{ii}$ 为正应力，$\tau_{ij}$ 为剪应力，且 $\tau_{ij} = \tau_{ji}$（剪应力互等定理）。

**应变张量**：小变形条件下：

$$\varepsilon_{ij} = \frac{1}{2}\left(\frac{\partial u_i}{\partial x_j} + \frac{\partial u_j}{\partial x_i}\right)$$

**主应力与主应变**：通过求解特征值问题可得主应力 $\sigma_1, \sigma_2, \sigma_3$。

**Von Mises 等效应力**：

$$\sigma_v = \sqrt{\frac{1}{2}\left[(\sigma_1-\sigma_2)^2 + (\sigma_2-\sigma_3)^2 + (\sigma_3-\sigma_1)^2\right]}$$

### 本构关系（胡克定律）

**各向同性材料广义胡克定律**：

$$\varepsilon_{ij} = \frac{1+\nu}{E}\sigma_{ij} - \frac{\nu}{E}\sigma_{kk}\delta_{ij}$$

其中 $E$ 为弹性模量，$\nu$ 为泊松比，$\delta_{ij}$ 为 Kronecker 符号。

**体积模量**：$K = \frac{E}{3(1-2\nu)}$

**剪切模量**：$G = \frac{E}{2(1+\nu)}$

### 平面应力与平面应变

**平面应力问题**（薄板受面内载荷）：
- $\sigma_{zz} = \tau_{xz} = \tau_{yz} = 0$
- 适用于薄板结构

**平面应变问题**（长柱体受横向载荷）：
- $\varepsilon_{zz} = \gamma_{xz} = \gamma_{yz} = 0$
- 适用于挡土坝、隧道等长结构

**Airy 应力函数**：平面问题可引入应力函数 $\Phi$，满足双调和方程：

$$\nabla^4 \Phi = \frac{\partial^4 \Phi}{\partial x^4} + 2\frac{\partial^4 \Phi}{\partial x^2 \partial y^2} + \frac{\partial^4 \Phi}{\partial y^4} = 0$$

### 能量方法

**应变能密度**：

$$U_0 = \frac{1}{2}\sigma_{ij}\varepsilon_{ij} = \frac{1}{2E}\left[\sigma_{xx}^2+\sigma_{yy}^2+\sigma_{zz}^2 - 2\nu(\sigma_{xx}\sigma_{yy}+\sigma_{yy}\sigma_{zz}+\sigma_{zz}\sigma_{xx})\right]$$

**卡氏第一定理**：$P_i = \frac{\partial U}{\partial \Delta_i}$

**卡氏第二定理（克罗蒂-恩格塞定理）**：线弹性体中，$\Delta_i = \frac{\partial U}{\partial P_i}$

**虚功原理**：外力虚功等于内力虚功：

$$\int_V \sigma_{ij}\delta\varepsilon_{ij}\,dV = \int_S T_i\delta u_i\,dS + \int_V f_i\delta u_i\,dV$$

**最小势能原理**：在所有满足位移边界条件的位移场中，真实位移场使总势能取极小值。

### 断裂力学基础

**应力强度因子**：

$$K_I = \lim_{r\to 0}\sigma_y(r,0)\sqrt{2\pi r}$$

**Griffith 能量准则**：

$$G = \frac{\partial}{\partial a}\left(U_{strain} - W_{external}\right)$$

**J 积分**：$J = \int_\Gamma \left(W\,dy - T_i\frac{\partial u_i}{\partial x}\,ds\right)$

**断裂判据**：$K_I \geq K_{IC}$（平面应变断裂韧性）

## 经典教材
- 刘鸿文《材料力学》
- 铁摩辛柯《材料力学》
- 徐芝纶《弹性力学》
- 郭敦仁《数学物理方法》

## 主要应用领域
- 航空航天结构强度分析
- 桥梁与建筑结构设计
- 机械零部件设计
- 汽车碰撞安全分析
- 微电子器件可靠性评估
- 生物力学（骨骼、关节分析）

## 相关条目

- 材料力学
- 弹性力学
- 断裂力学
- 有限元分析
- 结构力学
