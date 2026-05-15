---
aliases: [Aerodynamics]
tags: ['AerospaceAndMilitaryEngineering', 'Aerodynamics', 'Aerodynamics']
---

# 空气动力学

## 一、基本概念

### 1.1 流体与连续介质假设

空气动力学研究气体（特别是空气）在运动中的力学行为。**连续介质假设**将流体视为连续分布的介质，忽略分子热运动的离散性，使得流场物理量（密度、压力、速度等）可用连续函数描述。有效性的判定依据为Knudsen数：$Kn = \lambda / L < 0.01$，其中$\lambda$为分子平均自由程，$L$为特征长度。

### 1.2 可压缩性与黏性

- **可压缩性**：流体密度随压力变化的性质。马赫数 $Ma = v/a$ 表征可压缩性程度，$Ma < 0.3$ 时密度变化小于5%，通常视为不可压缩。
- **黏性**：流体抵抗剪切变形的性质，由牛顿内摩擦定律 $\tau = \mu \frac{du}{dy}$ 描述，$\mu$为动力黏度。运动黏度 $\nu = \mu / \rho$。

### 1.3 流动分类

| 分类依据 | 类别 | 特征 |
|---------|------|------|
| 黏性 | 无黏流 / 黏性流 | 是否考虑黏性力 |
| 压缩性 | 不可压缩 / 可压缩 | 密度是否变化 |
| 时间 | 定常 / 非定常 | 物理量是否随时间变化 |
| 状态 | 层流 / 湍流 | 流动的有序程度 |
| 速度 | 亚声速(Ma<0.8) / 跨声速(0.8-1.2) / 超声速(1.2-5) / 高超声速(Ma>5) | 马赫数范围 |

### 1.4 流体物性参数

| 参数 | 符号 | 定义 | 物理意义 |
|------|------|------|---------|
| 密度 | $\rho$ | 单位体积质量 | 流体惯性 |
| 压力 | $p$ | 单位面积法向力 | 压缩效应 |
| 温度 | $T$ | 分子平均动能度量 | 热状态 |
| 声速 | $a = \sqrt{\gamma RT}$ | 小扰动传播速度 | 压缩波速 |
| 比热比 | $\gamma = c_p/c_v$ | 定压/定容比热容之比 | 绝热指数（空气$\gamma=1.4$） |

## 二、控制方程

### 2.1 连续性方程

质量守恒定律。积分形式：

$$ \frac{\partial}{\partial t} \iiint_V \rho dV + \iint_S \rho \mathbf{v} \cdot \mathbf{n} dS = 0 $$

微分形式：

$$ \frac{\partial\rho}{\partial t} + \nabla \cdot (\rho\mathbf{v}) = 0 $$

不可压缩时简化为 $\nabla \cdot \mathbf{v} = 0$。

### 2.2 动量方程

Navier-Stokes方程（牛顿第二定律在流体中的表达）：

$$ \rho\frac{D\mathbf{v}}{Dt} = -\nabla p + \mu\nabla^2\mathbf{v} + \rho\mathbf{g} $$

其中$\frac{D}{Dt} = \frac{\partial}{\partial t} + \mathbf{v} \cdot \nabla$为物质导数，左边为惯性力项，右边依次为压力项、黏性项和体积力项。

**欧拉方程**：忽略黏性的无黏流动动量方程：$\rho\frac{D\mathbf{v}}{Dt} = -\nabla p + \rho\mathbf{g}$。

### 2.3 能量方程

热力学第一定律在流体中的表达：

$$ \rho\frac{Dh}{Dt} = \frac{Dp}{Dt} + \nabla \cdot (k\nabla T) + \Phi $$

其中$h$为比焓，$k$为热导率，$\Phi$为耗散函数（黏性耗散转化为热能的速率）。

### 2.4 边界层方程

Prandtl于1904年提出边界层概念，将流场分为边界层（黏性起主导作用的薄层）和外部无黏流区域。量级分析简化N-S方程：

$$ u\frac{\partial u}{\partial x} + v\frac{\partial u}{\partial y} = -\frac{1}{\rho}\frac{dp}{dx} + \nu\frac{\partial^2 u}{\partial y^2} $$

$$ \frac{\partial u}{\partial x} + \frac{\partial v}{\partial y} = 0 $$

## 三、无黏流动

### 3.1 伯努利方程

沿流线成立的能量守恒关系。不可压缩无黏定常流动：

$$ p + \frac{1}{2}\rho v^2 + \rho gh = \text{常数} $$

三项分别代表静压、动压和位势压头。皮托管测速基于此原理。

### 3.2 势流理论

无旋流动（$\nabla \times \mathbf{v} = 0$）引入速度势$\phi$，满足Laplace方程$\nabla^2\phi = 0$。叠加原理可组合基本解：

| 基本解 | 势函数$\phi$ | 流函数$\psi$ | 应用 |
|-------|-------------|-------------|------|
| 均匀流 | $V_\infty x$ | $V_\infty y$ | 自由来流 |
| 源/汇 | $\frac{Q}{2\pi}\ln r$ | $\frac{Q}{2\pi}\theta$ | 半体绕流 |
| 偶极子 | $-\frac{\kappa}{2\pi}\frac{\cos\theta}{r}$ | $\frac{\kappa}{2\pi}\frac{\sin\theta}{r}$ | 圆柱绕流 |
| 点涡 | $\frac{\Gamma}{2\pi}\theta$ | $-\frac{\Gamma}{2\pi}\ln r$ | 升力产生 |

## 四、边界层理论

### 4.1 层流与湍流边界层

转捩由雷诺数决定：$Re_x = \rho V_\infty x / \mu$，临界值约$5\times10^5$。

| 特性 | 层流边界层 | 湍流边界层 |
|------|-----------|-----------|
| 速度剖面 | 抛物线形 | 更饱满 |
| 壁面摩擦阻力 | 小 | 大 |
| 厚度增长 | $\delta \propto x^{1/2}$ | $\delta \propto x^{4/5}$ |
| 传热系数 | 小 | 大 |
| 抗分离能力 | 弱 | 强 |

**布拉修斯解**：平板层流边界层精确解，壁面摩擦系数$C_f = 0.664 / \sqrt{Re_x}$。

### 4.2 边界层分离

逆压梯度导致壁面附近流体速度减为零甚至反向，边界层从壁面分离。后果：压差阻力增大、升力下降、尾流扩大、失速（大迎角时机翼升力骤降）。

控制分离方法：涡流发生器、附面层吹吸、翼型优化设计、前缘缝翼、后缘襟翼。

## 五、升力与阻力

### 5.1 翼型理论

**库塔-儒科夫斯基定理**：

$$ L' = \rho V_\infty \Gamma $$

环量$\Gamma$由库塔条件（后缘光滑脱体条件）确定。

**薄翼型理论**：小迎角时升力系数与迎角线性关系：$C_l = 2\pi\alpha$（$\alpha$为弧度迎角）。

### 5.2 有限翼展理论

三维机翼的翼尖涡产生**诱导阻力**：

$$ C_{Di} = \frac{C_L^2}{\pi AR e} $$

$AR = b^2/S$为展弦比，$e$为奥斯瓦尔德效率因子。展弦比越大诱导阻力越小。椭圆环量分布具有最小诱导阻力。

### 5.3 阻力分类

| 阻力类型 | 来源 | 特点 |
|---------|------|------|
| 摩擦阻力 | 壁面黏性剪切应力 | 与表面积成正比 |
| 压差阻力 | 前后压力分布不对称 | 与物体形状相关 |
| 诱导阻力 | 三维机翼翼尖涡 | 与$C_L^2$成正比 |
| 激波阻力 | 超声速激波 | Ma>1时出现 |
| 干扰阻力 | 部件间相互干扰 | 叠加效应 |

**阻力极曲线**：$C_D$随$C_L$变化曲线，评估飞行器气动效率。升阻比$L/D$为关键指标。

## 六、跨声速与超声速流动

### 6.1 激波

当流动速度超过声速时形成激波，流动参数发生突变：

$$ \frac{p_2}{p_1} = 1 + \frac{2\gamma}{\gamma+1}(Ma_1^2 - 1) \quad \frac{\rho_2}{\rho_1} = \frac{(\gamma+1)Ma_1^2}{2+(\gamma-1)Ma_1^2} $$

正激波：波面垂直来流，总压损失最大。斜激波：波面有角度，损失较小。

**激波角$\beta$与偏转角$\theta$关系**：$\tan\theta = 2\cot\beta\frac{Ma_1^2\sin^2\beta - 1}{Ma_1^2(\gamma+\cos2\beta)+2}$

### 6.2 膨胀波

超声速气流绕外凸角形成普朗特-迈耶膨胀波，等熵加速降压。偏转角与马赫数关系：

$$ \theta = \sqrt{\frac{\gamma+1}{\gamma-1}}\arctan\sqrt{\frac{\gamma-1}{\gamma+1}(Ma^2-1)} - \arctan\sqrt{Ma^2-1} $$

### 6.3 面积-马赫数关系

喷管/风洞中一维等熵流动：

$$ \frac{A}{A^*} = \frac{1}{Ma}\left[\left(\frac{2}{\gamma+1}\right)\left(1+\frac{\gamma-1}{2}Ma^2\right)\right]^{\frac{\gamma+1}{2(\gamma-1)}} $$

$A^*$为声速喉部面积。亚声速时面积减小速度增加，超声速时面积增大速度增加。

## 七、计算流体力学基础

**基本流程**：前处理（几何建模+网格生成）→ 求解（数值格式+边界条件）→ 后处理（流场可视化+力/力矩计算）

**网格类型**：结构化网格（计算精度高）、非结构化网格（适应复杂几何）、混合网格。

**数值方法**：FVM（有限体积法，最常用，守恒性好）、FDM（有限差分法）、FEM（有限元法，固体力学为主）。

**湍流模型**：
| 模型 | 方程数 | 特点 |
|------|--------|------|
| Spalart-Allmaras | 1 | 航空工程常用，计算量小 |
| $k-\varepsilon$ | 2 | 标准模型，远场好 |
| $k-\omega$ SST | 2 | 近壁面精度高 |
| LES | - | 大涡模拟，计算量大 |
| DNS | - | 直接数值模拟，计算量极大 |

## 八、气动实验

### 8.1 风洞类型

低速（Ma<0.3，开口/闭口回路）、跨声速（多孔壁减少反射）、超声速（拉瓦尔喷管）、高超声速（激波风洞、电弧加热风洞）。

**相似准则**：雷诺数（黏性力）、马赫数（压缩性）、弗劳德数（重力）、斯特劳哈尔数（非定常）。

### 8.2 测量技术

- **压力**：压力传感器（点测量）、压力敏感涂料PSP（全场压力分布）
- **速度**：皮托管（点）、热线风速仪（高频响应）、粒子图像测速PIV（全场瞬态）
- **力**：应变式天平（三分量/六分量）
- **流动显示**：烟线法、纹影法（密度梯度）、油流法（壁面流线示踪）

## 参考资源

1. Anderson J D. Fundamentals of Aerodynamics. 6th ed. McGraw-Hill, 2017.
2. Bertin J J, Cummings R M. Aerodynamics for Engineers. 6th ed. Pearson, 2013.
3. Pope A, Barlow J B, Rae W H. Low-Speed Wind Tunnel Testing. 3rd ed. Wiley, 1999.
4. 庄逢甘, 张涵信. 空气动力学. 科学出版社, 2014.
5. Ferziger J H, Peric M, Street R L. Computational Methods for Fluid Dynamics. 4th ed. Springer, 2020.

## 相关条目
- [[FlightMechanics]]
- [[计算流体力学基础]]
- [[SpacecraftDesign]]
- [[FluidMechanics]]
