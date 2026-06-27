---
aliases: [OptimalControl]
tags: ['ControlAndSystemsEngineering', 'ControlTheory', 'OptimalControl']
created: 2026-05-16
updated: 2026-05-13
---

# 最优控制

## 定义
最优控制是研究如何选择控制输入使系统性能指标达到最优的控制理论分支。是现代控制理论的重要组成部分。

## 研究对象
- 变分法基础
- 庞特里亚金极大值原理
- 动态规划
- 最优控制应用

## 核心内容

### 变分法基础

**泛函**：$J = \int_{t_0}^{t_f} F(x,\dot{x},t)dt$

**欧拉方程**：

$$\frac{\partial F}{\partial x} - \frac{d}{dt}\frac{\partial F}{\partial \dot{x}} = 0$$

**横截条件**：确定终端状态的边界条件

### 庞特里亚金极大值原理

**哈密顿函数**：

$$H = L + \lambda^T f = L + \lambda^T(Ax+Bu)$$

**极大值原理**：最优控制 $u^*$ 使 $H$ 取极小值。

$$H(x^*,u^*,\lambda^*,t) \leq H(x^*,u,\lambda^*,t), \quad \forall u \in U$$

**正则方程**：

$$\dot{x} = \frac{\partial H}{\partial \lambda}, \quad \dot{\lambda} = -\frac{\partial H}{\partial x}$$

**最优控制律**：

$$u^* = \arg\min_{u \in U} H(x^*,u,\lambda^*,t)$$

### 动态规划

**Bellman 方程**：

$$V(x,t) = \min_{u}\left\{L(x,u,t) + \frac{\partial V}{\partial x}f(x,u,t)\right\}$$

**最优性原理**：最优策略的子策略也是最优的。

**离散 Bellman 方程**：

$$V_k(x_k) = \min_{u_k}\left\{L_k(x_k,u_k) + V_{k+1}(x_{k+1})\right\}$$

### 线性二次型调节器（LQR）

**连续时间 LQR**：

$$J = \int_0^\infty (x^TQx + u^TRu)dt$$

最优控制：$u^* = -R^{-1}B^TPx$

$P$ 满足代数 Riccati 方程：$A^TP + PA - PBR^{-1}B^TP + Q = 0$

**离散时间 LQR**：

$$J = \sum_{k=0}^{\infty} (x_k^TQx_k + u_k^TRu_k)$$

最优控制：$u_k = -K_k x_k$，$K_k$ 由递推 Riccati 方程求解。

**LQR 性质**：
- 最优性：使性能指标最小
- 鲁棒性：相位裕度≥60°，增益裕度≥6dB
- 无需试凑参数

### 模型预测控制（MPC）

**基本原理**：
1. 在每个采样时刻，基于当前状态预测未来行为
2. 求解有限时域优化问题
3. 只实施第一个控制输入
4. 下一时刻重新预测和优化

**优化问题**：

$$\min_{u_0,\ldots,u_{N-1}} \sum_{k=0}^{N-1}[x_k^TQx_k + u_k^TRu_k] + x_N^TPx_N$$

**约束条件**：
- 动力学约束：$x_{k+1} = Ax_k + Bu_k$
- 状态约束：$x_{min} \leq x_k \leq x_{max}$
- 输入约束：$u_{min} \leq u_k \leq u_{max}$

**MPC 优点**：
- 处理约束能力强
- 适用于多变量系统
- 可处理非线性系统（NMPC）

### 最优控制在机器人中的应用

**轨迹优化**：
- 最小时间轨迹
- 最小能量轨迹
- 最小冲击轨迹

**力控制**：
- 最优力分配
- 阻抗控制参数优化

**运动规划**：
- 基于优化的运动规划
- 二次规划（QP）求解

## 经典教材
- 胡跃松《最优控制》
- 谢绪恺《现代控制理论》
- Kirk《Optimal Control Theory: An Introduction》
- Bryson《Applied Optimal Control》

## 主要应用领域
- 航空航天（最优制导、轨道转移）
- 机器人（轨迹优化、力控制）
- 汽车（自适应巡航、自动驾驶）
- 过程控制（最优操作条件）
- 电力系统（最优潮流）
- 经济学（最优经济增长）

## 相关条目

- [[ClassicalControl]]
- [[ModernControl]]
- [[RobotDynamics]]
- AI/ReinforcementLearning
- [[SystemModeling]]
