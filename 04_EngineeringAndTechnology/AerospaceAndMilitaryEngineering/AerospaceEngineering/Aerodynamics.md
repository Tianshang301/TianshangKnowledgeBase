---
aliases: [Aerodynamics]
tags: ['AerospaceAndMilitaryEngineering', 'AerospaceEngineering', 'Aerodynamics']
---

# 空气动力学

## 定义
空气动力学是研究空气与其他物体之间相互作用力及其规律的学科。是航空航天工程的理论基础。

## 核心内容

### 基本方程

**连续性方程**：$\nabla \cdot (\rho \vec{V}) = 0$

**动量方程（Euler方程）**：

$$\frac{\partial \vec{V}}{\partial t} + (\vec{V}\cdot\nabla)\vec{V} = -\frac{1}{\rho}\nabla p + \vec{g}$$

**Navier-Stokes方程**（粘性流体）：

$$\rho\left(\frac{\partial \vec{V}}{\partial t} + \vec{V}\cdot\nabla\vec{V}\right) = -\nabla p + \mu\nabla^2\vec{V} + \rho\vec{g}$$

### 升力理论

**Kutta-Joukowski定理**：$L = \rho V_\infty \Gamma$

$\Gamma$ 为环量，$L$ 为单位展长升力。

**薄翼理论**：

$$c_l = 2\pi\alpha$$

$\alpha$ 为迎角（弧度）。

**升力系数**：$C_L = \frac{L}{\frac{1}{2}\rho V_\infty^2 S}$

### 阻力理论

**摩擦阻力**：层流边界层和湍流边界层

**层流摩阻系数**（Blasius）：
$$C_f = \frac{1.328}{\sqrt{Re}}$$

**湍流摩阻系数**（1/7次方律）：
$$C_f = \frac{0.074}{Re^{1/5}}$$

**压差阻力**：由物形决定

**诱导阻力**：$C_{D,i} = \frac{C_L^2}{\pi e AR}$

$AR = b^2/S$ 为展弦比，$e$ 为Oswald效率因子。

### 可压缩流动

**马赫数**：$M = V/a$

**雷诺数**：
$$Re = \frac{\rho V L}{\mu}$$

| 流动区域 | 马赫数范围 | 特征 |
|:---:|:---:|:---|
| 亚声速 | $M < 0.8$ | 无激波，不可压缩近似 |
| 跨声速 | $0.8 \le M \le 1.2$ | 混合流动，激波开始出现 |
| 超声速 | $1.2 < M < 5.0$ | 激波主导，Prandtl-Glauert失效 |
| 高超声速 | $M \ge 5.0$ | 高温效应，化学反应显著 |

**临界马赫数**：翼面最高速度达到声速时的来流马赫数

**激波**：正激波、斜激波、膨胀波

**Prandtl-Glauert法则**：

$$C_p = \frac{C_{p,0}}{\sqrt{1-M_\infty^2}}$$

### 翼型与机翼

**NACA翼型系列**：四位数、五位数、层流翼型

**机翼平面形状**：
- 矩形翼、梯形翼、后掠翼、三角翼
- 翼尖形状影响诱导阻力

## 经典教材
- Anderson《Fundamentals of Aerodynamics》
- 高志谦《空气动力学》
- Anderson《Compressible Flow》
- 盛森裕《空气动力学实验技术》

## 主要应用领域
- 飞行器气动设计
- 风洞试验
- 计算流体力学（CFD）
- 汽车空气动力学
- 风力机气动设计

## 相关条目

- [[FlightMechanics]]
- Propulsion
- CFD
- [[FluidMechanics]]
