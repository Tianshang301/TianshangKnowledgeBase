---
aliases: [Robotics]
tags: ['HardwareAndEmbeddedSystems', 'Robotics', 'Robotics']
created: 2026-05-16
updated: 2026-05-16
---

# 机器人学 (Robotics)

## 一、机器人分类 (Robot Classification)

| 类型 | 描述 | 典型应用 |
|------|------|---------|
| **工业机器人** | 固定基座机械臂 | 焊接、喷涂、装配 |
| **服务机器人** | 辅助人类工作 | 清洁、配送、接待 |
| **移动机器人** | 可移动平台 | AGV、无人车 |
| **人形机器人** | 仿人外形 | 研究、交互、探索 |
| **协作机器人** | 人与机器人共事 | 轻工业、实验室 |
| **医疗机器人** | 医疗手术辅助 | 达芬奇手术系统 |

## 二、机器人组成 (Robot Components)

```
┌──────────────────────────────────┐
│           控制器 (Controller)      │
│  ┌─────┐  ┌────────┐  ┌──────┐  │
│  │ CPU  │  │ 实时 OS  │  │通信模块│  │
│  └─────┘  └────────┘  └──────┘  │
├──────────────────────────────────┤
│  ┌──────────┐  ┌───────────┐     │
│  │ 传感器    │  │ 执行器     │     │
│  │ (感知环境)  │  │ (执行动作) │     │
│  └──────────┘  └───────────┘     │
├──────────────────────────────────┤
│         电源 (Power Supply)       │
│    电池 / 外部供电 / 能量回收     │
└──────────────────────────────────┘
```

| 组件 | 功能 |
|------|------|
| **传感器** | 感知环境状态（位置、力、视觉等） |
| **执行器** | 产生运动（电机、液压、气动） |
| **控制器** | 处理传感器信息，生成控制指令 |
| **电源** | 提供能量 |

## 三、运动学 (Kinematics)

### 正运动学 (Forward Kinematics)

已知关节角度，求末端执行器的位姿。

$$T = \prod_{i=1}^{n} A_i$$

其中 $A_i$ 是第 $i$ 个关节的齐次变换矩阵。

```c
// 2自由度机械臂正运动学
typedef struct { double x, y, theta; } pose_t;

pose_t forward_kinematics(double theta1, double theta2,
                           double l1, double l2) {
    pose_t result;
    result.x = l1 * cos(theta1) + l2 * cos(theta1 + theta2);
    result.y = l1 * sin(theta1) + l2 * sin(theta1 + theta2);
    result.theta = theta1 + theta2;
    return result;
}
```

### 逆运动学 (Inverse Kinematics)

已知末端执行器位姿，求解关节角度。通常多解且计算复杂。

```
对于6自由度机械臂：
- 存在解析解（Pieper 准则）：连续3轴交于一点
- 不存在解析解时：使用数值迭代（如牛顿法）
```

```c
// 2自由度机械臂逆运动学
int inverse_kinematics(double x, double y,
                        double l1, double l2,
                        double *theta1, double *theta2) {
    double cos_t2 = (x*x + y*y - l1*l1 - l2*l2) / (2 * l1 * l2);
    if (fabs(cos_t2) > 1.0) return -1;  // 不可达
    
    *theta2 = acos(cos_t2);              // 肘部向上
    // *theta2 = -acos(cos_t2);          // 肘部向下（另一解）
    
    double k1 = l1 + l2 * cos(*theta2);
    double k2 = l2 * sin(*theta2);
    *theta1 = atan2(y, x) - atan2(k2, k1);
    return 0;
}
```

## 四、DH 参数 (Denavit-Hartenberg Parameters)

### 参数定义

每个关节用4个参数描述从第 $i-1$ 坐标系到第 $i$ 坐标系的变换：

| 参数 | 符号 | 描述 |
|:----:|:----:|------|
| $\theta_i$ | 关节角 | 绕 $z_{i-1}$ 轴旋转 |
| $d_i$ | 连杆偏距 | 沿 $z_{i-1}$ 轴平移 |
| $a_i$ | 连杆长度 | 沿 $x_i$ 轴平移 |
| $\alpha_i$ | 连杆扭角 | 绕 $x_i$ 轴旋转 |

### 变换矩阵

$$A_i = \begin{bmatrix}
\cos\theta_i & -\sin\theta_i\cos\alpha_i & \sin\theta_i\sin\alpha_i & a_i\cos\theta_i \\
\sin\theta_i & \cos\theta_i\cos\alpha_i & -\cos\theta_i\sin\alpha_i & a_i\sin\theta_i \\
0 & \sin\alpha_i & \cos\alpha_i & d_i \\
0 & 0 & 0 & 1
\end{bmatrix}$$

## 五、动力学 (Dynamics)

### 牛顿-欧拉法 (Newton-Euler)

递推计算力和力矩，分为外推（从基座到末端）和内推（从末端到基座）两个过程。

### 拉格朗日-欧拉法 (Lagrange-Euler)

基于能量方法：$L = K - P$（拉格朗日量 = 动能 - 势能）

$$\frac{d}{dt}\frac{\partial L}{\partial \dot{q}} - \frac{\partial L}{\partial q} = \tau$$

其中 $q$ 为广义坐标，$\tau$ 为广义力。

```c
// 单连杆动力学
double torque(double theta, double theta_dot, double theta_ddot,
              double m, double l, double g) {
    double I = (1.0/3.0) * m * l * l;  // 转动惯量
    double gravity_term = m * g * (l/2) * cos(theta);
    return I * theta_ddot + gravity_term;  // τ = I·α + mgl/2·cos(θ)
}
```

## 六、轨迹规划 (Trajectory Planning)

### 关节空间 vs 笛卡尔空间

| 方面 | 关节空间 | 笛卡尔空间 |
|------|---------|-----------|
| 规划对象 | 每个关节的角度/速度 | 末端执行器的位姿 |
| 奇异性 | 无奇异问题 | 可能需要处理奇异 |
| 计算量 | 小 | 大（需逆运动学） |
| 路径可预测性 | 末段路径不可预测 | 末端路径可预测 |

### 三次多项式插值

$$\theta(t) = a_0 + a_1 t + a_2 t^2 + a_3 t^3$$

约束：$\theta(0)=\theta_0,\ \theta(t_f)=\theta_f,\ \dot{\theta}(0)=0,\ \dot{\theta}(t_f)=0$

```c
// 三次多项式轨迹规划
void cubic_trajectory(double theta0, double thetaf,
                       double tf, double t,
                       double *pos, double *vel) {
    // 根据边界条件解系数
    double a0 = theta0;
    double a1 = 0.0;
    double a2 = 3.0 * (thetaf - theta0) / (tf * tf);
    double a3 = -2.0 * (thetaf - theta0) / (tf * tf * tf);
    
    *pos = a0 + a1*t + a2*t*t + a3*t*t*t;
    *vel = a1 + 2*a2*t + 3*a3*t*t;
}
```

### 五次多项式插值

额外约束角加速度：$\ddot{\theta}(0)=0,\ \ddot{\theta}(t_f)=0$

$$\theta(t) = a_0 + a_1 t + a_2 t^2 + a_3 t^3 + a_4 t^4 + a_5 t^5$$

## 七、控制 (Control)

### 控制方法对比

| 方法 | 描述 | 优点 | 缺点 |
|------|------|------|------|
| **PID** | 比例-积分-微分控制 | 简单、成熟 | 需调参、非线性效果差 |
| **计算力矩法** | 基于模型的前馈+反馈 | 高精度 | 依赖精确模型 |
| **阻抗控制** | 控制力/位置关系 | 适合人机交互 | 计算量大 |
| **力控制** | 直接控制接触力 | 适合装配 | 需力传感器 |

### PID 控制

```c
// PID 控制器
typedef struct {
    double Kp, Ki, Kd;  // 比例、积分、微分增益
    double integral;
    double prev_error;
} pid_t;

double pid_update(pid_t *pid, double setpoint, double actual, double dt) {
    double error = setpoint - actual;
    pid->integral += error * dt;
    double derivative = (error - pid->prev_error) / dt;
    pid->prev_error = error;
    
    return pid->Kp * error 
         - pid->Ki * pid->integral 
         - pid->Kd * derivative;
}
```

## 八、传感器 (Sensors)

| 传感器 | 测量量 | 精度 | 采样率 | 用途 |
|--------|--------|------|--------|------|
| **编码器** | 关节角度 | 高 | 高频 | 位置反馈 |
| **IMU (IMU)** | 加速度、角速度 | 中高 | 100-1000Hz | 姿态估计 |
| **LiDAR** | 距离、点云 | 高 | 10-100Hz | 建图、避障 |
| **摄像头** | 图像 | 高 | 30-120Hz | 视觉定位 |
| **力/力矩** | 接触力 | 高 | 高频 | 力控 |
| **ToF (ToF)** | 深度 | 中 | 30-60Hz | 近距离感知 |
| **超声波** | 距离 | 低 | 20-50Hz | 近距离避障 |
| **GPS** | 经纬度 | 米级 | 1-10Hz | 室外定位 |

## 九、ROS (Robot Operating System)

### 核心概念

| 概念 | 描述 |
|------|------|
| **节点 (Node)** | 可执行程序，完成单一任务 |
| **话题 (Topic)** | 发布/订阅通信（异步） |
| **服务 (Service)** | 请求/响应通信（同步） |
| **动作 (Action)** | 长时间任务（可反馈、可取消） |
| **消息 (Message)** | 数据类型定义 |
| **包 (Package)** | 组织代码的结构 |

### 发布/订阅模式

```python
# ROS2 Python 发布者
import rclpy
from std_msgs.msg import String

def main():
    rclpy.init()
    node = rclpy.create_node('talker')
    pub = node.create_publisher(String, 'chatter', 10)
    
    msg = String()
    msg.data = 'Hello ROS2!'
    pub.publish(msg)
    
    rclpy.spin_once(node, timeout_sec=0)
    node.destroy_node()
    rclpy.shutdown()
```

```python
# ROS2 Python 订阅者
import rclpy
from std_msgs.msg import String

def callback(msg):
    print(f'收到: {msg.data}')

def main():
    rclpy.init()
    node = rclpy.create_node('listener')
    sub = node.create_subscription(String, 'chatter', callback, 10)
    rclpy.spin(node)
```

## 十、移动机器人 (Mobile Robots)

### SLAM (Simultaneous Localization and Mapping)

同时定位和建图：机器人在未知环境中创建地图并确定自身位置。

```
传感器数据（LiDAR/摄像头）
      ↓
前端 (Frontend): 特征提取、数据关联
      ↓
后端 (Backend): 图优化 / 滤波器
      ↓
地图 (Map) ← → 位姿 (Pose)
```

### 定位：粒子滤波器 (Particle Filter)

```
1. 初始化：在空间均匀撒粒子
2. 预测：根据运动模型更新粒子位置
3. 更新：根据观测模型计算粒子权重
4. 重采样：按权重重新采样粒子
5. 估计：加权平均得到位置估计
```

### 路径规划

| 算法 | 描述 | 适用 |
|------|------|------|
| **Dijkstra** | 加权图最短路径 | 已知全局地图 |
| **A*** | 启发式搜索（$f = g + h$） | 已知地图，高效 |
| **RRT** | 快速随机搜索树 | 高维、未知环境 |
| **DWA** | 动态窗口法（速度空间搜索） | 局部避障 |

### A*算法

$$f(n) = g(n) + h(n)$$

| 变量 | 含义 |
|:----:|------|
| $g(n)$ | 从起点到节点 $n$ 的实际代价 |
| $h(n)$ | 从节点 $n$ 到目标的启发式估计代价 |
| $f(n)$ | 节点 $n$ 的总估计代价 |

## 相关条目

- AI
- [[04_EngineeringAndTechnology/ControlAndSystemsEngineering/ControlTheory/INDEX|ControlTheory]]
- EmbeddedSystems
- [[05_ComputerScience/ArtificialIntelligence/ComputerVision/ComputerVision|ComputerVision]]

## 参考资源

- Siciliano, B., & Khatib, O. *Springer Handbook of Robotics* (2nd ed.)
- Craig, J. J. *Introduction to Robotics: Mechanics and Control* (4th ed.)
- Corke, P. *Robotics, Vision and Control* (2nd ed.)
- Thrun, S., Burgard, W., & Fox, D. *Probabilistic Robotics*
- ROS Documentation: https://docs.ros.org/


