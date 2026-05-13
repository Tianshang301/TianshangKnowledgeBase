# 机器人运动学

## 定义
机器人运动学是研究机器人各连杆之间位置、速度和加速度关系的学科。是机器人轨迹规划和控制的基础。

## 研究对象
- 坐标变换与齐次变换矩阵
- D-H参数法建模
- 正运动学与逆运动学
- 雅可比矩阵与轨迹规划

## 核心内容

### 齐次变换矩阵

**三维空间变换**：

$$T = \begin{bmatrix}R & p \\ 0 & 1\end{bmatrix} = \begin{bmatrix}r_{11}&r_{12}&r_{13}&p_x\\r_{21}&r_{22}&r_{23}&p_y\\r_{31}&r_{32}&r_{33}&p_z\\0&0&0&1\end{bmatrix}$$

$R$ 为旋转矩阵，$p$ 为平移向量。

**基本变换矩阵**：
- 绕x轴旋转：$Rot(x,\theta)$
- 绕y轴旋转：$Rot(y,\theta)$
- 绕z轴旋转：$Rot(z,\theta)$
- 沿x轴平移：$Trans(x,d)$

### D-H参数法

**Denavit-Hartenberg参数**：
- $\theta_i$：关节角（绕$z_{i-1}$轴旋转）
- $d_i$：连杆偏距（沿$z_{i-1}$轴平移）
- $a_i$：连杆长度（沿$x_i$轴平移）
- $\alpha_i$：连杆扭角（绕$x_i$轴旋转）

**变换矩阵**：

$$A_i = Rot(z_{i-1},\theta_i) \cdot Trans(0,0,d_i) \cdot Trans(a_i,0,0) \cdot Rot(x_i,\alpha_i)$$

### 正运动学

**关节空间→笛卡尔空间**：

$$T_n^0 = A_1 A_2 \cdots A_n$$

给定关节角度 $(\theta_1, \theta_2, \ldots, \theta_n)$，计算末端执行器的位姿。

**六自由度机器人正运动学示例**（Stanford手臂）：

$$T_6^0 = A_1 A_2 A_3 A_4 A_5 A_6$$

### 逆运动学

**笛卡尔空间→关节空间**：给定末端位姿，求关节角度。

**解析法**：
- 利用矩阵方程求解
- 可能得到多解（肘部上/下、腕部翻转）
- 解析解存在的条件：满足Pieper准则

**数值法**：
- 牛顿-拉夫逊法
- 雅可比矩阵伪逆法
- 迭代求解，适用于复杂结构

### 雅可比矩阵

**速度映射**：

$$\dot{x} = J(q)\dot{q}$$

$J$ 为雅可比矩阵（$6 \times n$），$\dot{x}$ 为末端速度，$\dot{q}$ 为关节速度。

**雅可比矩阵计算**：

$$J = \begin{bmatrix}J_v \\ J_\omega\end{bmatrix}$$

$J_v$ 为线速度雅可比，$J_\omega$ 为角速度雅可比。

**奇异性**：$\det(J) = 0$ 时，机器人处于奇异位形，某些方向运动受限。

### 轨迹规划

**关节空间规划**：
- 关节角度随时间变化
- 常用方法：三次多项式、五次多项式
- 优点：计算简单，关节运动平滑

**笛卡尔空间规划**：
- 末端执行器沿指定路径运动
- 需要逆运动学实时求解
- 适用于需要精确路径的任务（焊接、涂胶）

**路径规划方法**：
- 直线插补：末端沿直线运动
- 圆弧插补：末端沿圆弧运动
- 样条插值：平滑路径

## 经典教材
- 蔡自兴《机器人学》
- Craig《Introduction to Robotics》
- Lynch & Park《Modern Robotics: Mechanics, Planning, and Control》
- Siciliano《Robotics: Modelling, Planning and Control》

## 主要应用领域
- 工业机器人编程与控制
- 机械臂轨迹规划
- 仿真与离线编程
- 协作机器人安全设计
- 人形机器人步态规划

## 相关条目

- [[RobotDynamics]]
- [[RoboticsBasics]]
- [[ControlSystems]]
- [[SolidMechanics]]
- CAD/CAM
