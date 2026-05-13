# 飞行力学

## 定义
飞行力学是研究飞行器运动规律和操纵稳定性的学科。是飞行器设计和飞行控制的重要理论基础。

## 核心内容

### 飞行器运动方程

**六自由度运动方程**：
- 质心运动方程（3个平动）
- 绕质心转动方程（3个转动）

**气动力与力矩**：
- 升力 $L = C_L \frac{1}{2}\rho V^2 S$
- 阻力 $D = C_D \frac{1}{2}\rho V^2 S$
- 俯仰力矩 $M = C_m \frac{1}{2}\rho V^2 S c$

**升阻比**：
$$K = \frac{L}{D} = \frac{C_L}{C_D}$$

**过载系数**：
$$n = \frac{L}{W}$$

### 静稳定性

**纵向静稳定性**：

$$\frac{dC_m}{d\alpha} < 0$$

压力中心位于重心之后，飞机具有纵向静稳定性。

**横向静稳定性**：

$$C_{l\beta} < 0$$

上反角提供横向静稳定性。

**航向静稳定性**：

$$C_{n\beta} > 0$$

垂直尾翼提供航向静稳定性。

### 动稳定性

**纵向运动模态**：
- 短周期模态：快速阻尼振荡
- 长周期模态（Phugoid）：慢速振荡

**Phugoid振荡频率**：
$$\omega_p = \sqrt{2}\frac{g}{V}$$

| 模态 | 周期 | 阻尼特性 | 主要影响因素 |
|:---|:---:|:---|:---|
| 短周期 | 1–5 s | 强阻尼 | 静稳定性、俯仰阻尼 |
| 长周期（Phugoid） | 20–100 s | 弱阻尼 | 速度稳定性、L/D |

**横航向运动模态**：
- 滚模态：单调衰减
- 螺旋模态：慢速振荡
- 荷兰滚模态：振荡运动

| 模态 | 特征根 | 典型时间常数/周期 | 主要影响因素 |
|:---|:---:|:---:|:---|
| 滚模态 | 负实根 | $\tau \approx 0.5$ s | 机翼阻尼 |
| 螺旋模态 | 小实根（正/负） | $T \approx 20$–100 s | 上反角、垂尾 |
| 荷兰滚 | 共轭复根 | $T \approx 3$–10 s | 垂尾、方向舵 |

### 机动飞行

**盘旋**：
- 盘旋半径：$R = \frac{V^2}{g\tan\phi}$
- 盘旋过载：$n = \frac{1}{\cos\phi}$

**筋斗**：
- 过载要求
- 能量管理

### 起飞与着陆

**起飞距离**：$S_T = S_1 + S_2$

**着陆距离**：$S_L = S_{flare} + S_{roll} + S_{brake}$

## 经典教材
- 方振平《飞行力学》
- Nelson《Flight Stability and Automatic Control》
- Etkin《Dynamics of Flight: Stability and Control》
- McCormick《Aerodynamics, Aeronautics, and Flight Mechanics》

## 主要应用领域
- 飞行器设计
- 飞行控制系统设计
- 飞行模拟器
- 飞行试验
- 飞行性能评估

## 相关条目
- [[Aerodynamics]]
- [[SpacecraftDesign]]
- [[ClassicalControl]]
- [[ModernControl]]
- FlightMechanics (AerospaceEngineering)
