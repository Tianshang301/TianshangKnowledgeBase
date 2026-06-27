---
aliases: [OperationsResearch, 运筹学]
tags: ['EngineeringFundamentals', 'EngineeringMathematics', 'OperationsResearch']
created: 2026-05-17
updated: 2026-05-17
---

# 运筹学 (Operations Research)

## 定义

运筹学是应用数学方法和定量分析技术，研究系统优化决策问题的学科。其核心思想是在资源约束条件下寻找最优方案。

## 核心内容

### 线性规划 (Linear Programming, LP)

**标准形式**：

$$
\begin{aligned}
\min \quad & \mathbf{c}^T \mathbf{x} \\
\text{s.t.} \quad & \mathbf{A}\mathbf{x} = \mathbf{b} \\
& \mathbf{x} \geq 0
\end{aligned}
$$

其中 $\mathbf{x} \in \mathbb{R}^n$ 为决策变量，$\mathbf{c} \in \mathbb{R}^n$ 为目标系数，$\mathbf{A} \in \mathbb{R}^{m \times n}$ 为约束矩阵，$\mathbf{b} \in \mathbb{R}^m$ 为右端项。

**图解法 (Graphical Method)**：二维决策变量问题的几何求解。

**单纯形法 (Simplex Method)**：

```mermaid
graph TD
  A[标准形 LP] --> B[确定初始基本可行解]
  B --> C[计算检验数 $\sigma_j = c_j - c_B B^{-1} P_j$]
  C --> D{所有 $\sigma_j \leq 0$?}
  D -->|是| E[最优解找到]
  D -->|否| F[选择进基变量 $\sigma_k = \max_j \sigma_j$]
  F --> G{进基列所有 $a_{ik} \leq 0$?}
  G -->|是| H[问题无界]
  G -->|否| I[确定出基变量 $\theta = \min_i \frac{b_i}{a_{ik}}$]
  I --> J[基变换: 旋转运算]
  J --> C
```

### 对偶理论 (Duality Theory)

**原始-对偶对**：

**原始问题 (P)**：

$$
\min \mathbf{c}^T \mathbf{x}, \quad \mathbf{A}\mathbf{x} = \mathbf{b}, \quad \mathbf{x} \geq 0
$$

**对偶问题 (D)**：

$$
\max \mathbf{b}^T \mathbf{y}, \quad \mathbf{A}^T \mathbf{y} \leq \mathbf{c}
$$

**强对偶定理 (Strong Duality)**：若原始问题有最优解，则对偶问题也有最优解，且目标函数值相等：

$$
\mathbf{c}^T \mathbf{x}^* = \mathbf{b}^T \mathbf{y}^*
$$

**互补松弛条件 (Complementary Slackness)**：

$$
y_i^*(\mathbf{A}_i \mathbf{x}^* - b_i) = 0, \quad x_j^*(c_j - \mathbf{A}_j^T \mathbf{y}^*) = 0
$$

### 整数规划 (Integer Programming, IP)

**分支定界法 (Branch and Bound)**：

- 松弛整数约束→求解线性规划松弛
- 分支：选择一个分数变量 $x_j$，分为 $x_j \leq \lfloor x_j^* \rfloor$ 和 $x_j \geq \lceil x_j^* \rceil$
- 定界：更新上界（整数可行解）和下界（松弛最优解）
- 剪枝：当节点下界 ≥ 当前上界时剪枝

**割平面法 (Cutting Plane)**：

添加 Gomory 割平面缩小可行域：

$$
\sum_j (f_j - \lfloor f_j \rfloor) x_j \geq f_0 - \lfloor f_0 \rfloor
$$

**0-1 规划**：变量只能取 0 或 1，常用于选址、指派等决策问题。

### 运输问题 (Transportation Problem)

**产销平衡模型**：

$$
\min \sum_{i=1}^m \sum_{j=1}^n c_{ij} x_{ij}
$$

**约束**：

$$
\sum_{j=1}^n x_{ij} = a_i \quad (i=1,\ldots,m) \quad \text{供应约束}
$$

$$
\sum_{i=1}^m x_{ij} = b_j \quad (j=1,\ldots,n) \quad \text{需求约束}
$$

$$x_{ij} \geq 0$$

**求解方法**：西北角法、最小元素法、位势法。

### 网络优化 (Network Optimization)

**最短路径问题 (Shortest Path)**：

Dijkstra 算法（非负权）、Bellman-Ford 算法（允许负权）。

**最大流问题 (Maximum Flow)**：

Ford-Fulkerson 算法——增广路径法。

最大流-最小割定理：最大流的值等于最小割的容量。

**最小费用流 (Minimum Cost Flow)**：

$$
\min \sum_{(i,j) \in E} w_{ij} f_{ij}
$$

满足流量守恒与容量约束。

**最小生成树 (Minimum Spanning Tree)**：

Prim 算法（加点法）、Kruskal 算法（加边法）。

### 动态规划 (Dynamic Programming)

**Bellman 最优性原理**：最优决策的子决策也是最优的。

**基本递推方程**：

$$
f_i(x_i) = \min_{u_i \in U_i(x_i)} \{ c_i(x_i, u_i) + f_{i+1}(x_{i+1}) \}
$$

其中 $x_i$ 为状态变量，$u_i$ 为决策变量，$c_i$ 为阶段成本，$f_i$ 为最优值函数。

| 应用 | 状态变量 | 决策变量 | 递推方程 |
|------|---------|---------|---------|
| 资源分配 | 剩余资源 | 各项目分配量 | $f_i(s) = \max\{g_i(x) + f_{i+1}(s-x)\}$ |
| 背包问题 | 剩余容量 | 装入物品 | $f_i(w) = \max\{v_i + f_{i+1}(w-w_i), f_{i+1}(w)\}$ |

### 排队论 (Queueing Theory)

**Kendall 符号**：$A/B/c/K/N/Z$

**M/M/1 队列**（泊松到达、指数服务、单服务器）：

- 系统利用率：$\rho = \lambda / \mu$
- 平均队长：$L = \frac{\rho}{1-\rho}$
- 平均等待时间：$W = \frac{1}{\mu - \lambda}$

**Little 定律**：$L = \lambda W$

### 博弈论 (Game Theory)

**纳什均衡 (Nash Equilibrium)**：每个参与者在给定其他参与者策略的情况下没有动机单方面改变自己的策略。

**零和博弈 (Zero-Sum Game)**：一方所得等于另一方所失。

**二人零和博弈的混合策略**：

$$
\max_{\mathbf{p}} \min_{\mathbf{q}} \mathbf{p}^T \mathbf{A} \mathbf{q}
$$

## 经典教材

- 运筹学编写组《运筹学》（清华大学出版社）
- Hillier & Lieberman《Introduction to Operations Research》
- Winston《Operations Research: Applications and Algorithms》
- 胡运权《运筹学教程》

## 主要应用领域

- 生产计划与排程优化
- 物流配送与供应链管理
- 交通运输网络规划
- 金融投资组合优化
- 项目调度（关键路径法 CPM/PERT）
- 城市应急资源调配

## 相关条目

- [[NumericalMethods]]
- [[EngineeringMathematics]]
- [[04_EngineeringAndTechnology/ControlAndSystemsEngineering/SystemsEngineering/SystemAnalysis|SystemAnalysis]]
- [[ControlTheory]]


