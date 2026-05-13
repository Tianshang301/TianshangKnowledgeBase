# 强化学习

## 一、强化学习框架

强化学习（Reinforcement Learning, RL）是智能体（Agent）通过与环境的交互学习最优决策策略的机器学习范式。

### 马尔可夫决策过程 (MDP)

MDP由五元组 $\langle \mathcal{S}, \mathcal{A}, \mathcal{P}, \mathcal{R}, \gamma \rangle$ 定义：

| 元素 | 含义 | 说明 |
|------|------|------|
| $\mathcal{S}$ | 状态空间 | 环境所有可能状态的集合 |
| $\mathcal{A}$ | 动作空间 | 智能体可执行动作的集合 |
| $\mathcal{P}$ | 状态转移概率 | $P(s'|s,a)$ |
| $\mathcal{R}$ | 奖励函数 | $R(s,a)$ 或 $R(s,a,s')$ |
| $\gamma$ | 折扣因子 | $\gamma \in [0,1]$ |

### 核心概念

$$
\text{策略 } \pi(a|s): \mathcal{S} \times \mathcal{A} \rightarrow [0,1]
$$

$$
\text{回报 } G_t = \sum_{k=0}^\infty \gamma^k R_{t+k+1}
$$

## 二、贝尔曼方程

### 状态价值函数

$$
V^\pi(s) = \mathbb{E}_\pi[G_t | S_t = s]
$$

贝尔曼期望方程：

$$
V^\pi(s) = \sum_a \pi(a|s) \left[R(s,a) + \gamma \sum_{s'} P(s'|s,a) V^\pi(s')\right]
$$

### 动作价值函数

$$
Q^\pi(s,a) = \mathbb{E}_\pi[G_t | S_t = s, A_t = a]
$$

$$
Q^\pi(s,a) = R(s,a) + \gamma \sum_{s'} P(s'|s,a) \sum_{a'} \pi(a'|s') Q^\pi(s',a')
$$

### 最优价值函数

$$
V^*(s) = \max_a \left[R(s,a) + \gamma \sum_{s'} P(s'|s,a) V^*(s')\right]
$$

$$
Q^*(s,a) = R(s,a) + \gamma \sum_{s'} P(s'|s,a) \max_{a'} Q^*(s',a')
$$

## 三、动态规划

### 策略迭代

1. **策略评估**：迭代计算当前策略的价值函数
2. **策略改进**：基于价值函数贪心更新策略

$$
\pi'(s) = \arg\max_a \left[R(s,a) + \gamma \sum_{s'} P(s'|s,a) V^\pi(s')\right]
$$

### 价值迭代

$$
V_{k+1}(s) = \max_a \left[R(s,a) + \gamma \sum_{s'} P(s'|s,a) V_k(s')\right]
$$

价值迭代不显式表示策略，直接收敛到最优价值函数。

| 方法 | 收敛速度 | 计算复杂度 | 适用场景 |
|------|---------|-----------|---------|
| 策略迭代 | 较快（迭代次数少） | 每次评估代价高 | 大规模状态空间 |
| 价值迭代 | 较慢（迭代次数多） | 单步计算代价低 | 较小状态空间 |

## 四、无模型方法

无模型方法不依赖环境模型 $P(s'|s,a)$，直接从交互经验中学习。

### 蒙特卡洛方法 (MC)

基于完整episode的平均回报估计价值：

$$
V(S_t) \leftarrow V(S_t) + \alpha [G_t - V(S_t)]
$$

### 时序差分学习 (TD)

TD使用自举（bootstrap）方式，无需等待完整episode：

$$
V(S_t) \leftarrow V(S_t) + \alpha [R_{t+1} + \gamma V(S_{t+1}) - V(S_t)]
$$

**SARSA**（同策略）：

$$
Q(S_t, A_t) \leftarrow Q(S_t, A_t) + \alpha [R_{t+1} + \gamma Q(S_{t+1}, A_{t+1}) - Q(S_t, A_t)]
$$

**Q-learning**（异策略）：

$$
Q(S_t, A_t) \leftarrow Q(S_t, A_t) + \alpha \left[R_{t+1} + \gamma \max_a Q(S_{t+1}, a) - Q(S_t, A_t)\right]
$$

### SARSA与Q-learning对比

| 特性 | SARSA | Q-learning |
|------|-------|-----------|
| 策略类型 | 同策略 (On-policy) | 异策略 (Off-policy) |
| 更新目标 | 使用实际采取的动作 | 使用贪心最优动作 |
| 保守性 | 更保守（考虑实际策略） | 更激进（直接最优） |
| Cliff Walk表现 | 安全但不最优 | 最优但有风险 |

## 五、深度Q网络

### DQN (Deep Q-Network)

使用深度神经网络近似Q函数，解决高维状态空间问题：

$$
\mathcal{L}(\theta) = \mathbb{E}_{(s,a,r,s') \sim \mathcal{D}} \left[\left(r + \gamma \max_{a'} Q(s',a';\theta^-) - Q(s,a;\theta)\right)^2\right]
$$

### DQN关键技巧

- **经验回放 (Experience Replay)**：打破样本相关性
- **目标网络 (Target Network)**：$\theta^-$ 周期更新，稳定训练
- **ε-贪心探索**：平衡探索与利用

### DQN改进

| 方法                 | 改进点       | 公式                                                      |             |                    |
| ------------------ | --------- | ------------------------------------------------------- | ----------- | ------------------ |
| Double DQN         | 动作选择与评估解耦 | $r + \gamma Q(s', \arg\max_a Q(s',a;\theta); \theta^-)$ |             |                    |
| Dueling DQN        | 分离价值与优势   | $Q(s,a) = V(s) + A(s,a) - \frac{1}{                     | \mathcal{A} | }\sum_{a'}A(s,a')$ |
| Prioritized Replay | 优先级采样     | $P(i) \propto                                           | \delta_i    | ^\alpha$           |
| Rainbow            | 综合上述改进    | DQN + Double + Dueling + Prioritized + ...              |             |                    |

## 六、策略梯度方法

### REINFORCE

直接优化策略，使用蒙特卡洛估计梯度：

$$
\nabla J(\theta) = \mathbb{E}_{\pi_\theta} \left[\sum_{t=0}^T \nabla_\theta \log \pi_\theta(a_t|s_t) G_t\right]
$$

### Actor-Critic

结合策略梯度（Actor）和价值函数（Critic）：

$$
\nabla J(\theta) = \mathbb{E}_{\pi_\theta} \left[\nabla_\theta \log \pi_\theta(a|s) \cdot \delta\right]
$$

其中 $\delta = r + \gamma V(s') - V(s)$ 为TD误差。

### PPO (Proximal Policy Optimization)

通过裁剪（clipping）约束策略更新步长：

$$
\mathcal{L}^{\text{CLIP}}(\theta) = \mathbb{E}_t \left[\min\left(r_t(\theta) \hat{A}_t, \text{clip}(r_t(\theta), 1-\epsilon, 1+\epsilon) \hat{A}_t\right)\right]
$$

其中 $r_t(\theta) = \frac{\pi_\theta(a_t|s_t)}{\pi_{\theta_{\text{old}}}(a_t|s_t)}$ 为新旧策略比率。

### 方法对比

| 方法 | 特点 | 适用场景 |
|------|------|---------|
| REINFORCE | 无偏但高方差 | 简单连续控制 |
| A2C/A3C | 异步训练，方差减小 | 并行环境 |
| PPO | 稳定可靠，实现简单 | 最常用基线 |
| SAC | 最大熵框架 | 连续控制 |
| DDPG | 确定性策略 | 高维连续动作 |

## 七、探索与利用

| 策略 | 描述 | 特点 |
|------|------|------|
| ε-greedy | 以ε概率随机探索 | 简单但低效 |
| UCB | 置信上界乐观探索 | 理论保证 |
| Thompson采样 | 根据后验分布采样 | 贝叶斯最优 |
| 熵奖励 (SAC) | 最大化策略熵 | 鼓励探索 |
| 好奇心驱动 | 以预测误差为内在奖励 | 稀疏奖励场景 |

## 八、经典应用

| 应用 | 方法 | 成果 |
|------|------|------|
| AlphaGo | MCTS + DQN + 策略网络 | 击败人类围棋冠军 |
| AlphaZero | 自对弈 + MCTS | 通用棋类AI |
| Dota 2 | PPO + LSTM | 击败世界冠军（OpenAI Five） |
| 机器人控制 | SAC, PPO, DDPG | 灵巧操作、运动控制 |
| 自动驾驶 | 模仿学习 + RL | 端到端驾驶策略 |
| 推荐系统 | 多臂赌博机 | 在线广告推荐 |

## 相关条目

- [[SupervisedLearning]]
- [[04_EngineeringAndTechnology/ControlAndSystemsEngineering/ControlTheory/INDEX|ControlTheory]]
- [[Robotics]]
- GameAI

## 参考资源

- Sutton, R. S. & Barto, A. G. (2018). *Reinforcement Learning: An Introduction* (2nd ed.)
- Mnih, V. et al. (2015). "Human-level control through deep reinforcement learning"
- Schulman, J. et al. (2017). "Proximal Policy Optimization Algorithms"
- Lillicrap, T. P. et al. (2015). "Continuous control with deep reinforcement learning"
- Silver, D. et al. (2016). "Mastering the game of Go with deep neural networks and tree search"
- Haarnoja, T. et al. (2018). "Soft Actor-Critic: Off-Policy Maximum Entropy Deep RL with a Stochastic Actor"
