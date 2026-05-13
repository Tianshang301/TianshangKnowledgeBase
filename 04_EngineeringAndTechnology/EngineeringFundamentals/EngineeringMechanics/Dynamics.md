# 动力学

## 定义
动力学是研究物体运动与作用力之间关系的学科。是工程力学的重要组成部分。

## 核心内容

### 质点动力学

**牛顿第二定律**：$\vec{F} = m\vec{a}$

**质点运动微分方程**：

$$m\ddot{x} = F_x, \quad m\ddot{y} = F_y, \quad m\ddot{z} = F_z$$

### 动量定理

**动量**：$\vec{P} = m\vec{v}$

**冲量**：$\vec{I} = \int\vec{F}dt$

**动量定理**：$m\vec{v}_2 - m\vec{v}_1 = \int\vec{F}dt$

**动量守恒**：$\sum\vec{F} = 0$ 时，$\vec{P} = const$

### 动量矩定理

**动量矩**：$\vec{L}_O = \vec{r} \times m\vec{v}$

**动量矩定理**：

$$\frac{d\vec{L}_O}{dt} = \vec{M}_O$$

**转动惯量**：$J = \sum m_i r_i^2$

### 动能定理

**动能**：
- 平动：$T = \frac{1}{2}mv^2$
- 转动：$T = \frac{1}{2}J\omega^2$

**功**：$W = \int\vec{F}\cdot d\vec{r}$

**动能定理**：$T_2 - T_1 = \sum W_{1\to2}$

### 达朗贝尔原理

**惯性力**：$\vec{F}_I = -m\vec{a}$

**达朗贝尔原理**：

$$\sum\vec{F} + \vec{F}_I = 0$$

**动平衡**：旋转体惯性力系的主矢和主矩均为零

### 虚位移原理

**理想约束**：约束反力虚功之和为零

**虚位移原理**：

$$\sum\vec{F}_i\cdot\delta\vec{r}_i = 0$$

### 拉格朗日方程

**拉格朗日函数**：$L = T - V$

**拉格朗日方程**：

$$\frac{d}{dt}\frac{\partial L}{\partial\dot{q}_j} - \frac{\partial L}{\partial q_j} = Q_j$$

## 经典教材
- 哈尔滨工业大学《理论力学》
- 《动力学》
- Meriam《Engineering Mechanics: Dynamics》
- Hibbeler《Engineering Mechanics: Dynamics》

## 主要应用领域
- 机械振动分析
- 车辆动力学
- 飞行器动力学
- 结构抗震分析
- 机器人动力学
