# 机器人动力学

## 定义
机器人动力学是研究机器人各连杆受力与运动关系的学科。是机器人力控制和动力学参数辨识的基础。

## 研究对象
- 拉格朗日动力学方程
- 牛顿-欧拉递推法
- 动力学参数辨识
- 力控制与柔顺控制

## 核心内容

### 拉格朗日动力学方程

**拉格朗日函数**：

$$L = T - V$$

$T$ 为系统动能，$V$ 为系统势能。

**拉格朗日方程**：

$$\frac{d}{dt}\frac{\partial L}{\partial \dot{q}_i} - \frac{\partial L}{\partial q_i} = \tau_i$$

**机器人动力学方程**：

$$M(q)\ddot{q} + C(q,\dot{q})\dot{q} + g(q) = \tau$$

- $M(q)$：惯性矩阵（对称正定）
- $C(q,\dot{q})$：科氏力和离心力矩阵
- $g(q)$：重力项
- $\tau$：关节力矩

### 牛顿-欧拉递推法

**向外递推（运动学）**：

$$\omega_i = R_i^T\omega_{i-1} + \dot{q}_i z_{i-1}$$
$$\dot{\omega}_i = R_i^T\dot{\omega}_{i-1} + R_i^T\omega_{i-1} \times \dot{q}_i z_{i-1} + \ddot{q}_i z_{i-1}$$
$$\dot{v}_i = R_i^T(\dot{v}_{i-1} + \dot{\omega}_{i-1} \times r_{i-1} + \omega_{i-1} \times (\omega_{i-1} \times r_{i-1}))$$

**向内递推（动力学）**：

$$f_i = m_i\dot{v}_i + m_i\omega_i \times v_i$$
$$n_i = I_i\dot{\omega}_i + \omega_i \times I_i\omega_i$$

**关节力矩**：

$$\tau_i = f_i^T s_{i-1}$$

### 动力学参数辨识

**辨识模型**：

$$\tau = Y(q,\dot{q},\ddot{q})\pi$$

$Y$ 为回归矩阵，$\pi$ 为动力学参数向量。

**辨识方法**：
- 最小二乘法：$\hat{\pi} = (Y^TY)^{-1}Y^T\tau$
- 递推最小二乘
- 卡尔曼滤波

**辨识参数**：
- 连杆质量、质心位置
- 转动惯量
- 关节摩擦系数

### 力控制与力位混合控制

**力控制**：

$$\tau = J^T F_d + K_f(F_d - F_e)$$

$F_d$ 为期望力，$F_e$ 为实际接触力。

**力位混合控制**：
- 在约束方向：力控制
- 在自由方向：位置控制
- 选择矩阵 $S$ 控制自由度分配

### 柔顺控制

**主动柔顺**：
- 阻抗控制：$F_e = M_d(\ddot{x}_d-\ddot{x}) + D_d(\dot{x}_d-\dot{x}) + K_d(x_d-x)$
- 导纳控制：$\ddot{x} = M_d^{-1}(F_e - D_d\dot{x} - K_d x)$

**阻抗控制参数调节**：
- $M_d$：等效质量
- $D_d$：等效阻尼
- $K_d$：等效刚度

## 经典教材
- Craig《Introduction to Robotics》
- Spong《Robot Dynamics and Control》
 Lynch & Park《Modern Robotics》
- Siciliano《Robotics: Modelling, Planning and Control》

## 主要应用领域
- 机器人轨迹跟踪控制
- 力控制应用（装配、打磨）
- 协作机器人安全控制
- 动力学仿真
- 机器人结构优化设计

## 相关条目

- [[RobotKinematics]]
- [[RoboticsBasics]]
- [[ControlSystems]]
- [[ClassicalControl]]
- [[ModernControl]]
