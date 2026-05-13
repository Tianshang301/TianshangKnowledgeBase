# 工程力学

## 定义
工程力学是将力学基本原理应用于工程实际问题的学科，主要包括静力学、运动学和动力学三大部分。它是机械、土木、航空航天等工程学科的理论基础。

## 研究对象
- 刚体与质点系的力学行为
- 工程结构的受力分析与运动分析
- 机械系统的动力响应

## 核心内容

### 静力学

**力的基本性质**：力的三要素（大小、方向、作用点），力的合成与分解。

**力的平衡方程**：

$$\sum \vec{F} = 0, \quad \sum \vec{M}_O = 0$$

三维空间中展开为六个标量方程：

$$\sum F_x = 0, \quad \sum F_y = 0, \quad \sum F_z = 0$$
$$\sum M_x = 0, \quad \sum M_y = 0, \quad \sum M_z = 0$$

**力矩**：$\vec{M}_O = \vec{r} \times \vec{F}$，大小 $M = rF\sin\theta$

**力偶**：$\vec{M} = \vec{r}_{AB} \times \vec{F}$，力偶矩为自由矢量。

**约束与约束反力**：
- 固定铰支座：两个反力分量
- 可动铰支座：一个垂直于支承面的反力
- 固定端：三个反力分量 + 三个反力偶矩
- 光滑接触面：沿法线方向的反力

**桁架分析**：
- 节点法：逐个节点列平衡方程
- 截面法：用截面截断桁架，对截断杆件列平衡方程

### 运动学

**点的运动学**：
- 自然法：$v = \dot{s}$，$a_t = \ddot{s}$，$a_n = \frac{v^2}{\rho}$
- 直角坐标法：$\vec{r} = x\hat{i} + y\hat{j} + z\hat{k}$
- 极坐标法：$v_r = \dot{r}$，$v_\theta = r\dot{\theta}$

**刚体平面运动**：
- 速度瞬心法：$v = \omega \cdot r$（绕瞬心转动）
- 基点法：$\vec{v}_B = \vec{v}_A + \vec{\omega} \times \vec{r}_{AB}$
- 加速度分析：$\vec{a}_B = \vec{a}_A + \vec{\alpha} \times \vec{r}_{AB} + \vec{\omega} \times (\vec{\omega} \times \vec{r}_{AB})$

**刚体定点运动**：
- 欧拉角描述：进动角 $\psi$、章动角 $\theta$、自转角 $\varphi$
- 欧拉动力学方程

### 动力学

**牛顿第二定律**：$\vec{F} = m\vec{a}$

**质点系动量定理**：

$$\frac{d\vec{P}}{dt} = \sum \vec{F}^{(e)}$$

其中 $\vec{P} = m\vec{v}_C$，$\vec{v}_C$ 为质心速度。

**动量矩定理**：

$$\frac{d\vec{L}_O}{dt} = \sum \vec{M}_O^{(e)}$$

**刚体绕定轴转动**：$M_z = J_z \alpha$，其中 $J_z$ 为转动惯量。

**动能定理**：

$$T_2 - T_1 = \sum W_{1\to2}$$

平动动能：$T = \frac{1}{2}mv^2$

转动动能：$T = \frac{1}{2}J\omega^2$

**达朗贝尔原理**：在运动物体上施加惯性力 $-m\vec{a}$，则可用静力学方法求解动力学问题。

$$\sum \vec{F} + (-m\vec{a}) = 0$$

**虚位移原理**：$\sum \vec{F}_i \cdot \delta\vec{r}_i = 0$（理想约束下）

**拉格朗日方程**：

$$\frac{d}{dt}\frac{\partial L}{\partial \dot{q}_j} - \frac{\partial L}{\partial q_j} = Q_j$$

其中 $L = T - V$ 为拉格朗日函数，$q_j$ 为广义坐标。

## 经典教材
- 哈尔滨工业大学理论力学教研室《理论力学》
- 刘鸿文《材料力学》
- Meriam & Kraige《Engineering Mechanics: Statics/Dynamics》
- Beer & Johnston《Vector Mechanics for Engineers》

## 主要应用领域
- 机械设计与制造
- 土木工程结构分析
- 航空航天器设计
- 汽车工程（碰撞分析、振动控制）
- 机器人运动规划
- 桥梁与建筑抗震分析

## 相关条目

- [[SolidMechanics]]
- [[FluidMechanics]]
- [[StructuralAnalysis]]
- [[MachineDesign]]
- [[Dynamics]]
