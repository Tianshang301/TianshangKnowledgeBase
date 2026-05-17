---
aliases:
  - Transport Phenomena
  - 传递过程
  - 化工原理
tags:
  - transport
  - momentum-transfer
  - heat-transfer
  - mass-transfer
  - fluid-mechanics
---

# 传递现象 (Transport Phenomena)

传递现象研究动量、热量和质量在物质中的传递规律。这三大传递过程具有相似的数学结构，是化学工程的物理基础。

## 通用传递方程 (General Transport Equations)

三种传递过程都可以用通用方程描述：

$$
\frac{\partial \Phi}{\partial t} + \nabla \cdot \mathbf{J} = S
$$

其中 $\Phi$ 为传递量，$\mathbf{J}$ 为通量，$S$ 为源项。

| 传递类型 | 传递量 $\Phi$ | 通量 $\mathbf{J}$ | 源项 $S$ |
|---------|--------------|-------------------|----------|
| 动量传递 | $\rho \mathbf{v}$ | $\mathbf{\tau}$ | $-\nabla p + \rho \mathbf{g}$ |
| 热量传递 | $\rho c_p T$ | $-k \nabla T$ | $\dot{q}$ |
| 质量传递 | $c_i$ | $-D \nabla c_i$ | $r_i$ |

## 动量传递 (Momentum Transfer)

动量传递研究流体的运动规律，即流体力学。

### 连续性方程 (Continuity Equation)

$$
\frac{\partial \rho}{\partial t} + \nabla \cdot (\rho \mathbf{v}) = 0
$$

对于不可压缩流体：

$$
\nabla \cdot \mathbf{v} = 0
$$

### 纳维-斯托克斯方程 (Navier-Stokes Equations)

$$
\rho \left(\frac{\partial \mathbf{v}}{\partial t} + \mathbf{v} \cdot \nabla \mathbf{v}\right) = -\nabla p + \mu \nabla^2 \mathbf{v} + \rho \mathbf{g}
$$

各项含义：
- 左边：局部加速度 + 对流加速度
- 右边：压力梯度 + 粘性力 + 体积力

### 雷诺数 (Reynolds Number)

无量纲数，表征流动状态：

$$
Re = \frac{\rho v D}{\mu} = \frac{v D}{\nu}
$$

| 流动状态 | Re 范围 | 特征 |
|---------|--------|------|
| 层流 (Laminar) | $Re < 2100$ | 流线平行，粘性主导 |
| 过渡流 (Transitional) | $2100 < Re < 4000$ | 不稳定 |
| 湍流 (Turbulent) | $Re > 4000$ | 涡流，惯性主导 |

### 圆管层流

对于圆管内充分发展的层流，速度分布为抛物线：

$$
v(r) = v_{max}\left(1 - \frac{r^2}{R^2}\right)
$$

最大速度：

$$
v_{max} = \frac{\Delta P R^2}{4 \mu L}
$$

平均速度：

$$
v_{avg} = \frac{v_{max}}{2} = \frac{\Delta P R^2}{8 \mu L}
$$

压降（Hagen-Poiseuille 方程）：

$$
\Delta P = \frac{32 \mu L v_{avg}}{D^2}
$$

## 热量传递 (Heat Transfer)

热量传递包括三种基本机制：传导、对流和辐射。

### 热传导 (Conduction)

傅里叶定律：

$$
\mathbf{q} = -k \nabla T
$$

其中 $k$ 为导热系数 $[W/(m \cdot K)]$。

一维稳态热传导：

$$
q = \frac{k A}{L}(T_1 - T_2)
$$

### 对流传热 (Convection)

牛顿冷却定律：

$$
q = h A (T_s - T_\infty)
$$

其中 $h$ 为对流传热系数 $[W/(m^2 \cdot K)]$。

### 传热系数关联式

| 几何形状 | 关联式 | 适用条件 |
|----------|--------|----------|
| 管内强制对流 | Dittus-Boelter | $Re > 10^4$, $Pr = 0.7-160$ |
| 管外横掠 | Churchill-Bernstein | 单管绕流 |
| 自然对流 | 各种 Grashof 数关联 | 浮力驱动 |

努塞尔数定义：

$$
Nu = \frac{h L}{k}
$$

### 换热器设计 (Heat Exchanger Design)

对数平均温差法 (LMTD)：

$$
\Delta T_{lm} = \frac{\Delta T_1 - \Delta T_2}{\ln(\Delta T_1 / \Delta T_2)}
$$

传热方程：

$$
Q = U A \Delta T_{lm}
$$

总传热系数：

$$
\frac{1}{U} = \frac{1}{h_i} + \frac{\Delta x}{k} + \frac{1}{h_o} + R_f
$$

其中 $R_f$ 为污垢热阻。

## 质量传递 (Mass Transfer)

质量传递是组分在浓度梯度驱动下的迁移。

### 菲克定律 (Fick's Law)

$$
\mathbf{J}_A = -D_{AB} \nabla c_A
$$

其中 $D_{AB}$ 为扩散系数 $[m^2/s]$。

### 扩散方程

对于无化学反应的一维非稳态扩散：

$$
\frac{\partial c_A}{\partial t} = D_{AB} \frac{\partial^2 c_A}{\partial z^2}
$$

### 对流传质 (Convective Mass Transfer)

传质通量：

$$
N_A = k_c A (c_{A,s} - c_{A,\infty})
$$其中 $k_c$ 为传质系数 $[m/s]$。

舍伍德数：

$$
Sh = \frac{k_c L}{D_{AB}}
$$

### 传质与传热的类比

| 无量纲数 | 动量传递 | 热量传递 | 质量传递 |
|---------|---------|---------|---------|
| 通量系数 | 摩擦因子 $f$ | 努塞尔数 $Nu$ | 舍伍德数 $Sh$ |
| 扩散系数 | 运动粘度 $\nu$ | 热扩散率 $\alpha$ | 扩散系数 $D$ |
| 比值 | Prandtl $Pr = \nu/\alpha$ | | Schmidt $Sc = \nu/D$ |

Chilton-Colburn 类比：

$$
\frac{f}{2} = j_H = j_D
$$

## 边界层理论 (Boundary Layer Theory)

边界层是固体表面附近流体性质剧烈变化的薄层。

### 速度边界层

```mermaid
graph LR
    A[层流边界层<br/>Laminar<br/>Boundary Layer] --> B[转捩点<br/>Transition<br/>Point]
    B --> C[湍流边界层<br/>Turbulent<br/>Boundary Layer]
    C --> D[粘性底层<br/>Viscous<br/>Sublayer]
```

边界层厚度：

$$
\delta(x) \approx \frac{5x}{\sqrt{Re_x}}
$$

### 热边界层与浓度边界层

热边界层厚度与速度边界层的关系：

$$
\frac{\delta_t}{\delta} \approx Pr^{-1/3}
$$

浓度边界层厚度：

$$
\frac{\delta_c}{\delta} \approx Sc^{-1/3}
$$

## 多组分系统 (Multicomponent Systems)

### 麦克斯韦-斯蒂芬方程

对于多组分扩散：

$$
\nabla x_i = \sum_{j \neq i} \frac{x_i x_j}{D_{ij}} (\mathbf{v}_j - \mathbf{v}_i)
$$

### 有效扩散系数

对于稀溶液，组分 $A$ 在混合物中的有效扩散系数：

$$
D_{A,m} = \left(\sum_{j \neq A} \frac{x_j}{D_{Aj}}\right)^{-1}
$$

## 传递现象的工程应用

| 应用领域 | 传递类型 | 典型设备 |
|---------|---------|----------|
| 反应器设计 | 动量、热量、质量 | 搅拌釜、固定床 |
| 蒸馏塔 | 热量、质量 | 板式塔、填料塔 |
| 换热器 | 热量 | 管壳式、板式 |
| 吸收塔 | 质量 | 填料塔、喷淋塔 |
| 膜分离 | 质量 | 膜组件 |

## 参考资料 (References)

- Bird, R.B. et al. *Transport Phenomena*
- Incropera, F.P. et al. *Fundamentals of Heat and Mass Transfer*
- Cussler, E.L. *Diffusion: Mass Transfer in Fluid Systems*
