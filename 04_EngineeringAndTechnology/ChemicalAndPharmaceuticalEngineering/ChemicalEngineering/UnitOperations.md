---
aliases: [UnitOperations]
tags: ['ChemicalAndPharmaceuticalEngineering', 'ChemicalEngineering', 'UnitOperations']
created: 2026-05-16
updated: 2026-05-13
---

# 化工单元操作

## 定义
化工单元操作是化工生产中具有共同物理变化规律的基本操作过程。是化学工程的核心基础。

## 核心内容

### 流体流动与输送

**伯努利方程**：

$$\frac{p_1}{\rho} + \frac{u_1^2}{2} + gz_1 = \frac{p_2}{\rho} + \frac{u_2^2}{2} + gz_2 + h_f$$

**管路计算**：
- 直管阻力：$h_f = \lambda\frac{l}{d}\frac{u^2}{2}$
- 局部阻力：$h_j = \zeta\frac{u^2}{2}$

**泵的选择**：
- 离心泵：$Q-H$ 特性曲线
- 扬程与流量匹配

### 传热

**热传导**：$q = -\lambda\frac{dT}{dx}$

**对流传热**：$q = h(T_s - T_f)$

**辐射传热**：$q = \varepsilon\sigma(T_1^4 - T_2^4)$

**换热器设计**：
- 管壳式换热器
- 板式换热器
- 传热方程：$Q = UA\Delta T_m$

### 蒸馏

**气液平衡**：
- 拉乌尔定律：$p_i = x_i p_i^*$
- 相对挥发度：$\alpha = \frac{y_A/x_A}{y_B/x_B}$

**精馏塔计算**：
- 物料衡算
- 理论板数计算（图解法、逐板计算法）
- 最小回流比

**芬斯克方程（全回流最少理论板数）**：$N_{min} = \frac{\ln\left[\frac{x_D(1-x_W)}{x_W(1-x_D)}\right]}{\ln\alpha}$

**最小回流比（Underwood 法）**：$\sum\frac{\alpha_i x_{F,i}}{\alpha_i - \theta} = 1 - q$

## 分离方法对比

| 方法 | 分离原理 | 适用物系 | 产品相态 | 能耗 |
|------|---------|---------|---------|------|
| 蒸馏 | 挥发度/沸点差 | 液体混合物 | 液+气 | 高（需汽化） |
| 吸收 | 溶解度差 | 气-液体系 | 液 | 中 |
| 萃取 | 分配系数差 | 液-液体系 | 液 | 中 |
| 吸附 | 亲和力差 | 气/液-固 | 气/液 | 低 |
| 膜分离 | 分子大小/电荷 | 液/气 | 液 | 低 |
| 结晶 | 溶解度-温度 | 溶液 | 固 | 中 |

### 吸收

**气液平衡**：亨利定律 $p = Ex$

**吸收速率**：$N_A = K_y a (y-y^*)$

**总传质系数**：$\frac{1}{K_y} = \frac{1}{k_y} + \frac{m}{k_x}$

**填料塔设计**：
- 填料选型
- 塔径计算
- 填料高度

### 干燥

**干燥速率**：$N = \frac{dW}{Ad\tau}$

**平衡含水量**：物料与干燥介质达到平衡时的含水量

**干燥器类型**：厢式干燥器、转筒干燥器、喷雾干燥器

## 经典教材
- 柯葵兴《化工原理》
- McCabe《Unit Operations of Chemical Engineering》
- Geankoplis《Transport Processes and Unit Operations》
- Perry's Chemical Engineers' Handbook

## 主要应用领域
- 石油化工
- 精细化工
- 制药工程
- 食品工程
- 环境工程
- 新材料制备

## 相关条目
- [[ProcessDesign]]
- [[ReactionEngineering]]
- [[FineChemicals]]
- [[Thermodynamics]]
- [[FluidMechanics]]
