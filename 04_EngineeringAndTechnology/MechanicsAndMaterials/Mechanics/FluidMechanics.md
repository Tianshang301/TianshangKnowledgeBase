# 流体力学

## 定义
流体力学是研究流体（液体和气体）在静止和运动状态下的力学行为及其与固体边界相互作用的学科。它是力学的重要分支，广泛应用于航空航天、水利工程、环境科学等领域。

## 研究对象
- 理想流体与粘性流体
- 不可压缩流体与可压缩流体
- 层流与湍流
- 多相流、非牛顿流体

### 流体分类对比

| 分类 | 定义条件 | 关键方程 | 典型应用 |
|------|---------|---------|---------|
| **理想流体** | $\mu = 0$（无粘性） | 欧拉方程、伯努利方程 | 初步气动分析 |
| **粘性流体** | $\mu > 0$ | 纳维-斯托克斯方程 | 真实流动模拟 |
| **不可压缩** | $\rho = \text{const},\; \nabla\cdot\vec{v}=0$ | $A_1v_1 = A_2v_2$ | 低速水/空气流 ($Ma < 0.3$) |
| **可压缩** | $\rho = \rho(p,T)$ | 完全气体状态方程 $p = \rho RT$ | 高速气流 ($Ma > 0.3$) |
| **牛顿流体** | $\tau = \mu\frac{du}{dy}$（线性） | N-S 方程 | 水、空气、油 |
| **非牛顿流体** | $\tau = \eta(\dot\gamma)\frac{du}{dy}$（非线性） | 广义牛顿模型 | 聚合物、血液、泥浆 |

## 核心内容

### 流体基本性质

**密度**：$\rho = \lim_{\Delta V \to 0}\frac{\Delta m}{\Delta V}$，单位 $\text{kg/m}^3$

**动力粘度**：牛顿内摩擦定律 $\tau = \mu\frac{du}{dy}$，$\mu$ 单位 $\text{Pa·s}$

**运动粘度**：$\nu = \frac{\mu}{\rho}$，单位 $\text{m}^2/\text{s}$

**体积弹性模量**：$K = -V\frac{dp}{dV}$

**表面张力**：$\sigma = \frac{F}{L}$，单位 $\text{N/m}$

### 流体静力学

**静压强分布**：$\frac{dp}{dz} = -\rho g$

**帕斯卡原理**：封闭流体中任一点压强变化等值传递到流体各处。

**液体静压强公式**：$p = p_0 + \rho g h$

**浮力（阿基米德原理）**：$F_B = \rho_f g V_{displaced}$

**静压强中心**：$y_p = y_c + \frac{I_{xc}}{y_c A}$

### 流体动力学——纳维-斯托克斯方程

**连续性方程（质量守恒）**：

$$\frac{\partial \rho}{\partial t} + \nabla \cdot (\rho \vec{v}) = 0$$

**不可压缩流动**：$\nabla \cdot \vec{v} = 0$

**纳维-斯托克斯方程（动量守恒）**：

$$\rho\left(\frac{\partial \vec{v}}{\partial t} + \vec{v}\cdot\nabla\vec{v}\right) = -\nabla p + \mu\nabla^2\vec{v} + \rho\vec{g}$$

**能量方程**：

$$\rho c_p\left(\frac{\partial T}{\partial t} + \vec{v}\cdot\nabla T\right) = k\nabla^2 T + \Phi$$

其中 $\Phi$ 为粘性耗散函数。

### 连续性方程与伯努利方程对比

| 方程 | 形式 | 物理意义 | 适用条件 |
|------|------|---------|---------|
| 质量守恒（通用） | $\dfrac{\partial \rho}{\partial t} + \nabla \cdot (\rho \vec{v}) = 0$ | 质量既不能创生也不能消灭 | 所有流动 |
| 不可压缩连续 | $A_1 v_1 = A_2 v_2$ | 体积流量守恒 | 不可压缩、定常、一维流动 |
| 可压缩连续 | $\rho_1 A_1 v_1 = \rho_2 A_2 v_2$ | 质量流量守恒 | 定常、一维流动 |
| 伯努利（理想） | $p + \frac{1}{2}\rho v^2 + \rho g z = \text{const}$ | 机械能沿流线守恒 | 无粘、不可压缩、定常 |
| 伯努利（实际） | $\frac{p_1}{\rho g} + \frac{v_1^2}{2g} + z_1 = \frac{p_2}{\rho g} + \frac{v_2^2}{2g} + z_2 + h_f$ | 含损失的能量平衡 | 粘性、不可压缩、定常 |

### 伯努利方程

**理想流体沿流线的伯努利方程**：

$$p + \frac{1}{2}\rho v^2 + \rho g z = \text{const}$$

各项物理意义：压力能 + 动能 + 势能 = 常数

**实际流体伯努利方程（含损失）**：

$$\frac{p_1}{\rho g} + \frac{v_1^2}{2g} + z_1 = \frac{p_2}{\rho g} + \frac{v_2^2}{2g} + z_2 + h_f$$

### 雷诺数与流态

**雷诺数**：$Re = \frac{\rho v L}{\mu} = \frac{vL}{\nu}$

- 管道流动：$Re < 2300$ 为层流，$Re > 4000$ 为湍流
- 平板边界层：$Re_x = 5\times10^5$ 为转捩点

**临界雷诺数**取决于流动几何形状和来流扰动水平。

### 层流与湍流对比

| 特征 | 层流 (Laminar) | 湍流 (Turbulent) |
|------|---------------|-----------------|
| 雷诺数范围 | $Re < 2300$（圆管） | $Re > 4000$（圆管） |
| 流动特征 | 流线平行、分层有序 | 涡旋随机、混沌掺混 |
| 速度分布（圆管） | 抛物线：$v(r) = \dfrac{\Delta p}{4\mu L}(R^2 - r^2)$ | 扁平：$v(r) \approx v_{\text{max}}(1 - \frac{r}{R})^{1/n}$ |
| 摩擦因子 | $f = 64/Re$ | $f = f(Re, \varepsilon/D)$ Colebrook公式 |
| 传热特性 | 导热为主 | 对流增强，传热系数高 |
| 混合程度 | 仅分子扩散 | 强烈的涡旋掺混 |
| 阻力特性 | 与速度一次方成正比 | 与速度约 1.75-2 次方成正比 |

### 边界层理论

**边界层厚度（Blasius解）**：$\delta \approx \frac{5x}{\sqrt{Re_x}}$

**位移厚度**：$\delta^* = \int_0^\infty \left(1 - \frac{u}{U}\right)dy$

**动量厚度**：$\theta = \int_0^\infty \frac{u}{U}\left(1 - \frac{u}{U}\right)dy$

**壁面摩擦系数**：$C_f = \frac{\tau_w}{\frac{1}{2}\rho U^2}$

**von Kármán动量积分方程**：

$$\frac{d\theta}{dx} + (2\theta + \delta^*)\frac{1}{U}\frac{dU}{dx} = \frac{C_f}{2}$$

### 管道流动

**Darcy-Weisbach公式**：$h_f = f\frac{L}{D}\frac{v^2}{2g}$

**Moody图**：层流时 $f = 64/Re$；湍流时 $f$ 取决于 $Re$ 和相对粗糙度 $\varepsilon/D$

**Colebrook-White公式**（湍流区）：

$$\frac{1}{\sqrt{f}} = -2\log\left(\frac{\varepsilon/D}{3.7} + \frac{2.51}{Re\sqrt{f}}\right)$$

**局部损失**：$h_j = \zeta\frac{v^2}{2g}$

## 经典教材
- 周光坰《流体力学》
- Frank M. White《流体力学》
- 吴望一《流体力学》
- Anderson Jr.《计算流体力学基础》

## 主要应用领域
- 航空航天（翼型设计、飞行器气动分析）
- 水利工程（大坝泄洪、管道输水）
- 化工过程（搅拌、混合、分离）
- 环境工程（大气扩散、河流污染）
- 生物医学（血液循环、呼吸道流动）
- 汽车工程（车身外形空气动力学优化）

## 相关条目

- [[Thermodynamics]]
- [[Aerodynamics]]
- [[Hydraulics]]
- CFD
- [[HeatTransfer]]
