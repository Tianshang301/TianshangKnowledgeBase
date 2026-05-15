---
aliases: [SystemModeling]
tags: ['ControlAndSystemsEngineering', 'SystemsEngineering', 'SystemModeling']
---

# 系统建模

## 定义
系统建模是建立数学模型来描述实际系统动态行为的过程。是系统分析和控制设计的基础。

## 研究对象
- 数学建模方法
- 微分方程建模
- 状态空间建模
- 系统仿真与模型验证

## 核心内容

### 数学建模方法

**机理建模**：
- 基于物理、化学定律
- 利用守恒定律（质量、能量、动量守恒）
- 适用于机理清楚的系统

**辨识建模**：
- 基于实验数据
- 输入输出关系拟合
- 适用于机理复杂的系统

**混合建模**：
- 机理+辨识结合
- 关键部分用机理，次要部分用辨识

### 微分方程建模

**建模步骤**：
1. 确定系统变量
2. 分析变量间关系
3. 列写微分方程
4. 拉普拉斯变换求传递函数

**典型系统建模**：

**质量-弹簧-阻尼系统**：

$$m\ddot{x} + c\dot{x} + kx = F(t)$$

传递函数：$G(s) = \frac{X(s)}{F(s)} = \frac{1}{ms^2+cs+k}$

**RLC电路**：

$$LC\frac{d^2u_C}{dt^2} + RC\frac{du_C}{dt} + u_C = u_s$$

传递函数：$G(s) = \frac{1/LC}{s^2+(R/L)s+1/LC}$

**热力学系统**：

$$mc_p\frac{dT}{dt} = q_{in} - \frac{T-T_{env}}{R_{th}}$$

### 状态空间建模

**从传递函数到状态空间**：

可控标准型：

$$A = \begin{bmatrix}-a_{n-1}&-a_{n-2}&\cdots&-a_0\\1&0&\cdots&0\\0&1&\cdots&0\\\vdots&\vdots&\ddots&\vdots\end{bmatrix}, \quad B = \begin{bmatrix}1\\0\\\vdots\\0\end{bmatrix}$$

可观标准型、对角标准型等。

**非线性系统建模**：

$$\dot{x} = f(x,u), \quad y = g(x,u)$$

线性化：$\dot{x} = Ax + Bu$，$A = \frac{\partial f}{\partial x}|_{x_0,u_0}$，$B = \frac{\partial f}{\partial u}|_{x_0,u_0}$

### 系统仿真（MATLAB/Simulink）

**MATLAB仿真**：
- `ode45`：Runge-Kutta法求解微分方程
- `lsim`：线性系统时域响应
- `bode`：频率响应

**Simulink仿真**：
- 模块化建模
- 多种求解器
- 子系统封装
- 参数扫描

**仿真流程**：
1. 建立数学模型
2. 搭建仿真模型
3. 设置仿真参数
4. 运行仿真
5. 分析仿真结果

### 模型验证与确认

**模型验证**：检查模型是否正确实现设计意图

**模型确认**：检查模型是否准确反映实际系统

**验证方法**：
- 比较仿真结果与实验数据
- 统计分析误差
- 灵敏度分析
- 鲁棒性分析

## 经典教材
- 王朝珠《系统建模与仿真》
- 吴重光《过程控制与仿真》
- Ogata《Modeling and Analysis of Dynamic Systems》
- Nise《Control Systems Engineering》

## 主要应用领域
- 控制系统设计
- 过程仿真与优化
- 系统性能评估
- 故障诊断
- 预测性维护
- 教学与培训

## 相关条目
- [[SystemAnalysis]]
- [[ClassicalControl]]
- [[ModernControl]]
- [[OptimalControl]]
- [[IndustrialAutomation]]
