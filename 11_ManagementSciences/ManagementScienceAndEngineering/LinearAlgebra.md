---
aliases: [LinearAlgebra, 线性代数, 向量空间, 矩阵论]
tags: ['11_ManagementSciences', 'ManagementScienceAndEngineering', 'Mathematics']
---

# 线性代数 (Linear Algebra)

## 概述

线性代数是管理科学与工程（Management Science and Engineering）中处理多维数据和建立结构化模型的基础数学工具。向量（vector）和矩阵（matrix）作为基本数据结构，在多元回归（multiple regression）、主成分分析（PCA）和线性规划（linear programming）中大量使用。线性代数提供了描述高维空间中的变换、投影和分解的统一语言。

## 基本概念

### 向量与向量空间

向量 $\mathbf{v} \in \mathbb{R}^n$ 是 n 个有序实数的集合。向量空间（vector space）满足加法封闭性和数乘封闭性。在管理科学中，向量常用于表示：

- 一组产品的产量向量 $\mathbf{x} = (x_1, x_2, \dots, x_n)^T$
- 一组资产的价格向量 $\mathbf{p} = (p_1, p_2, \dots, p_n)^T$
- 样本观测值向量 $\mathbf{y} = (y_1, y_2, \dots, y_m)^T$

### 矩阵及其运算

矩阵 $\mathbf{A} \in \mathbb{R}^{m \times n}$ 是 m 行 n 列的数表。基本运算包括：

| 运算 | 记法 | 条件 | 结果维度 |
|------|------|------|----------|
| 加法 | $\mathbf{A} + \mathbf{B}$ | 相同维度 | $m \times n$ |
| 数乘 | $\lambda \mathbf{A}$ | 无 | $m \times n$ |
| 乘法 | $\mathbf{A}\mathbf{B}$ | $\mathbf{A}$ 列数等于 $\mathbf{B}$ 行数 | $m \times p$ |
| 转置 | $\mathbf{A}^T$ | 无 | $n \times m$ |
| 逆 | $\mathbf{A}^{-1}$ | 方阵且满秩 | $n \times n$ |

### 线性方程组

线性方程组 $\mathbf{A}\mathbf{x} = \mathbf{b}$ 的求解是管理模型的核心运算。解的存在性和唯一性取决于矩阵 $\mathbf{A}$ 的秩（rank）：

$$
\mathbf{A}\mathbf{x} = \mathbf{b} \quad \Rightarrow \quad \mathbf{x} = \mathbf{A}^{-1}\mathbf{b} \quad (\text{当 } \mathbf{A} \text{ 可逆时})
$$

```mermaid
graph TD
  A[线性方程组<br/>Ax = b] --> B{系数矩阵 A<br/>是否可逆？}
  B -->|是| C[唯一解<br/>x = A⁻¹b]
  B -->|否| D{r(A) 与 r(A|b) 的关系}
  D -->|r(A) = r(A|b) < n| E[无穷多解]
  D -->|r(A) < r(A|b)| F[无解]
  E --> G[最小二乘解<br/>x = (AᵀA)⁻¹Aᵀb]
```

投入-产出分析（Input-Output Analysis）是线性方程组在管理经济学中的经典应用：$\mathbf{x} = (\mathbf{I} - \mathbf{A})^{-1}\mathbf{d}$，其中 $\mathbf{A}$ 为直接消耗系数矩阵，$\mathbf{d}$ 为最终需求向量。

## 特征值与特征向量

特征值（eigenvalue）$\lambda$ 和特征向量（eigenvector）$\mathbf{v}$ 满足：

$$
\mathbf{A}\mathbf{v} = \lambda \mathbf{v}
$$

求解特征值即解特征方程 $\det(\mathbf{A} - \lambda \mathbf{I}) = 0$。

### 管理应用

1. **主成分分析 (PCA)**：协方差矩阵的特征值对应各主成分的方差贡献，特征向量定义投影方向。
2. **马尔可夫链稳态分析**：转移概率矩阵 $\mathbf{P}$ 的稳态分布满足 $\boldsymbol{\pi} = \boldsymbol{\pi}\mathbf{P}$，即 $\boldsymbol{\pi}$ 为 $\mathbf{P}^T$ 对应特征值 1 的特征向量。
3. **网络中心度**：邻接矩阵的主特征向量对应特征向量中心度（eigenvector centrality），PageRank 是其变体。

## 矩阵分解

| 分解方法 | 形式 | 适用场景 |
|----------|------|----------|
| LU 分解 | $\mathbf{A} = \mathbf{L}\mathbf{U}$ | 线性方程组求解 |
| QR 分解 | $\mathbf{A} = \mathbf{Q}\mathbf{R}$ | 最小二乘问题 |
| Cholesky 分解 | $\mathbf{A} = \mathbf{L}\mathbf{L}^T$ | 正定矩阵、协方差矩阵 |
| 奇异值分解 (SVD) | $\mathbf{A} = \mathbf{U}\boldsymbol{\Sigma}\mathbf{V}^T$ | 降维、推荐系统 |
| 特征分解 | $\mathbf{A} = \mathbf{V}\boldsymbol{\Lambda}\mathbf{V}^{-1}$ | PCA、谱聚类 |

奇异值分解（SVD）的表达式：

$$
\mathbf{A}_{m \times n} = \mathbf{U}_{m \times m} \boldsymbol{\Sigma}_{m \times n} \mathbf{V}^T_{n \times n}
$$

## 凸组合与凸集

凸组合（convex combination）$ \sum_{i=1}^k \theta_i \mathbf{x}_i $ 满足 $\theta_i \geq 0$ 且 $\sum \theta_i = 1$。凸集（convex set）是包含任意两点间连线上所有点的集合。

**支撑超平面定理**（Supporting Hyperplane Theorem）和 **分离定理**（Separating Hyperplane Theorem）是凸优化和拉格朗日对偶（Lagrangian duality）的理论基石。

## 正定矩阵与极值判定

正定矩阵（positive definite matrix）满足 $\mathbf{x}^T \mathbf{A} \mathbf{x} > 0$ 对所有非零 $\mathbf{x}$ 成立。黑森矩阵（Hessian matrix）的正定性用于判断多元函数的极值点性质：

- 正定 → 局部极小值
- 负定 → 局部极大值
- 不定 → 鞍点

## 最小二乘估计

普通最小二乘法（OLS）的封闭解完全建立在空间投影的几何理解之上：

$$
\hat{\boldsymbol{\beta}} = (\mathbf{X}^T \mathbf{X})^{-1} \mathbf{X}^T \mathbf{y}
```

其中 $\hat{\mathbf{y}} = \mathbf{X}\hat{\boldsymbol{\beta}}$ 是 $\mathbf{y}$ 在 $\mathbf{X}$ 列空间上的正交投影，投影矩阵 $\mathbf{P} = \mathbf{X}(\mathbf{X}^T \mathbf{X})^{-1} \mathbf{X}^T$。

## 高阶应用

管理科学中的高阶应用均以线性代数为底层运算语言：

1. **数据包络分析 (DEA)**：基于线性规划的效率评价，使用对偶变量和锥组合。
2. **社会网络分析 (SNA)**：邻接矩阵、拉普拉斯矩阵的结构属性分析。
3. **投入产出表**：Leontief 逆矩阵 $(\mathbf{I} - \mathbf{A})^{-1}$ 计算完全消耗系数。
4. **金融资产定价**：协方差矩阵用于 Markowitz 均值-方差投资组合优化。

## 相关条目

- [[OptimizationMethods|优化方法]]
- [[ProbabilityTheory|概率论]]
- [[GameTheory|博弈论]]
- [[DecisionTheory|决策理论]]
- [[DataMining|数据挖掘]]
- [[INDEX|ManagementScienceAndEngineering 索引]]
- [[../../INDEX|TianshangKnowledgeBase 索引]]
