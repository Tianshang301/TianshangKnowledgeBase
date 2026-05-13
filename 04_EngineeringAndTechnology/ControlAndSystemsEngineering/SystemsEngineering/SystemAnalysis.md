# 系统分析

## 定义
系统分析是研究控制系统性能指标及其计算方法的学科，包括时域分析、频域分析和可靠性分析。

## 研究对象
- 系统性能指标
- 时域响应分析
- 频域特性分析
- 系统可靠性

## 核心内容

### 系统性能指标

**稳定性**：系统受扰动后能否恢复平衡状态

**快速性**：系统响应速度，用上升时间、调节时间等衡量

**准确性**：系统稳态误差大小

### 时域分析

**阶跃响应性能指标**：

$$G(s) = \frac{\omega_n^2}{s^2+2\zeta\omega_n s+\omega_n^2}$$

**上升时间**（10%→90%）：

$$t_r = \frac{\pi - \beta}{\omega_d}, \quad \beta = \arccos\zeta$$

**峰值时间**：

$$t_p = \frac{\pi}{\omega_d}, \quad \omega_d = \omega_n\sqrt{1-\zeta^2}$$

**超调量**：

$$\sigma\% = e^{-\pi\zeta/\sqrt{1-\zeta^2}} \times 100\%$$

**调节时间**（2%误差带）：

$$t_s \approx \frac{4}{\zeta\omega_n}$$

**稳态误差**：

$$e_{ss} = \lim_{s\to 0}\frac{sR(s)}{1+G(s)}$$

### 频域分析

**带宽**：增益下降到-3dB时的频率

**相位裕度**：$\gamma = 180° + \angle G(j\omega_g)$

**增益裕度**：$K_g = -20\log|G(j\omega_\pi)|$ dB

**谐振峰值**：$M_r = \frac{1}{2\zeta\sqrt{1-\zeta^2}}$（$\zeta < 0.707$）

**谐振频率**：$\omega_r = \omega_n\sqrt{1-2\zeta^2}$

### 系统可靠性分析

**可靠性指标**：

**MTBF（平均故障间隔时间）**：

$$MTBF = \int_0^\infty R(t)dt$$

**失效率**：$\lambda(t) = \frac{f(t)}{R(t)}$

**指数分布**：$R(t) = e^{-\lambda t}$，$MTBF = 1/\lambda$

**串联系统可靠性**：

$$R_{sys} = R_1 \times R_2 \times \cdots \times R_n$$

**并联系统可靠性**：

$$R_{sys} = 1 - (1-R_1)(1-R_2)\cdots(1-R_n)$$

**冗余设计**：提高系统可靠性的关键方法

## 经典教材
- 胡寿松《自动控制原理》
- Ogata《Modern Control Engineering》
- Dorf《Modern Control Systems》
- Ebeling《An Introduction to Reliability and Maintainability Engineering》

## 主要应用领域
- 控制系统性能评估
- 产品质量检验
- 设备维护决策
- 安全关键系统设计
- 航空航天系统分析

## 相关条目
- [[SystemModeling]]
- [[ClassicalControl]]
- [[ModernControl]]
- [[OptimalControl]]
- [[IndustrialAutomation]]
