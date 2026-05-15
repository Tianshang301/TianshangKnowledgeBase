---
aliases: [ClassicalControl]
tags: ['ControlAndSystemsEngineering', 'ControlTheory', 'ClassicalControl']
---

# 经典控制

## 定义
经典控制理论是以传递函数为数学模型，研究单输入单输出（SISO）线性定常控制系统的分析与设计方法的理论体系。

## 研究对象
- 控制系统的传递函数模型
- 系统稳定性分析
- 根轨迹法与频率响应法
- PID控制器与校正装置设计

## 核心内容

### 传递函数模型

**传递函数定义**：零初始条件下，输出拉氏变换与输入拉氏变换之比。

$$G(s) = \frac{Y(s)}{U(s)} = \frac{b_m s^m + \cdots + b_0}{a_n s^n + \cdots + a_0}$$

**闭环传递函数**（单位负反馈）：

$$\Phi(s) = \frac{G(s)}{1+G(s)}$$

**特征方程**：$1+G(s)H(s) = 0$，决定系统稳定性。

### 方框图与信号流图

**方框图化简规则**：
- 串联：$G = G_1 G_2$
- 并联：$G = G_1 + G_2$
- 反馈：$G = \frac{G_1}{1+G_1 G_2}$

**信号流图**：
- 节点表示变量
- 支路表示传递函数
- Mason增益公式：

$$T = \frac{1}{\Delta}\sum_k P_k \Delta_k$$

### 稳定性分析方法对比

| 方法 | 数学基础 | 适用系统 | 稳定判据 | 优点 | 缺点 |
|------|---------|---------|---------|------|------|
| **Routh判据** | 代数方法 | 线性定常 | Routh表第一列全正 | 简单快速，无需绘图 | 只能判断绝对稳定性 |
| **Nyquist判据** | 复变函数 | 线性定常 | $Z = N + P = 0$ | 可判断相对稳定性，含时滞系统 | 需绘制频率特性曲线 |
| **根轨迹法** | 复平面分析 | 线性定常 | 根全在左半平面 | 直观显示参数影响 | 高阶系统绘制复杂 |
| **Lyapunov直接法** | 能量函数 | 线性/非线性 | $V(x)$正定，$\dot{V}(x)$负定 | 适用于非线性系统 | Lyapunov函数构造困难 |

**Routh判据**：
- 特征方程系数构成Routh表
- 第一列全为正→系统稳定
- 第一列变号次数→右半平面极点数

**Nyquist判据**：
- 开环频率响应 $G(j\omega)$ 绕 $(-1,j0)$ 点的圈数
- $Z = N + P$（$Z$：闭环右极点数，$N$：绕圈数，$P$：开环右极点数）
- 稳定条件：$Z = 0$

**相位裕度与增益裕度**：
- 相位裕度：$\gamma = 180^\circ + \angle G(j\omega_g)$，$\omega_g$ 为增益穿越频率
- 增益裕度：$K_g = -20\log|G(j\omega_\pi)|$ dB，$\omega_\pi$ 为相位穿越频率

**稳定性裕度与系统性能关系**：

| 相位裕度 $\gamma$ | 系统阻尼比 $\zeta$ | 超调量 $\sigma\%$ | 系统响应 |
|------------------|-------------------|-----------------|---------|
| $30^\circ \sim 60^\circ$ | $0.3 \sim 0.7$ | $5\% \sim 30\%$ | 良好 |
| $\gamma < 30^\circ$ | $\zeta < 0.3$ | $\sigma\% > 30\%$ | 振荡剧烈 |
| $\gamma > 60^\circ$ | $\zeta > 0.7$ | $\sigma\% < 5\%$ | 响应迟缓 |

### 根轨迹法

**根轨迹方程**：

$$1 + KG(s)H(s) = 0$$

**根轨迹绘制规则**：
1. 起点：$K=0$，开环极点
2. 终点：$K \to \infty$，开环零点
3. 分离点：$\frac{dK}{ds} = 0$
4. 渐近线：条数 $n-m$，角度 $\frac{(2k+1)\pi}{n-m}$
5. 与虚轴交点：令 $s=j\omega$ 求解

**根轨迹增益与开环增益的关系**：$K^* = K\frac{\text{分子首项系数}}{\text{分母首项系数}}$

### 频率响应法

**Bode图**：
- 幅频特性：$20\log|G(j\omega)|$ vs $\omega$（对数坐标）
- 相频特性：$\angle G(j\omega)$ vs $\omega$
- 渐近线近似：转折频率处斜率变化

**典型环节Bode图**：
- 比例：水平线
- 积分：斜率-20dB/dec
- 微分：斜率+20dB/dec
- 惯性：转折频率后斜率-20dB/dec

### PID控制器设计

**PID控制器**：

$$G_c(s) = K_p + \frac{K_i}{s} + K_d s = K_p\left(1+\frac{1}{T_i s}+T_d s\right)$$

**参数对系统性能的影响**：
- $K_p$：减小稳态误差，增大超调
- $K_i$：消除稳态误差，增大超调
- $K_d$：减小超调，改善动态性能

### 超前/滞后校正

**超前校正**：

$$G_c(s) = \frac{1+\alpha Ts}{1+Ts}, \quad \alpha > 1$$

- 提供正相位
- 增加相位裕度
- 改善瞬态响应

**滞后校正**：

$$G_c(s) = \frac{1+Ts}{1+\beta Ts}, \quad \beta > 1$$

- 降低高频增益
- 增加增益裕度
- 改善稳态精度

**超前-滞后校正**：同时改善动态和稳态性能

## 经典教材
- 胡寿松《自动控制原理》
- 卢京潮《自动控制原理》
- Ogata《Modern Control Engineering》
- Kuo《Automatic Control Systems》

## 主要应用领域
- 工业过程控制
- 电机调速系统
- 温度控制系统
- 液位控制系统
- 飞行控制系统
- 机器人关节控制

## 相关条目

- [[ModernControl]]
- [[Robotics]]
- [[04_EngineeringAndTechnology/ControlAndSystemsEngineering/Automation/INDEX|Automation]]
- AI/ReinforcementLearning
