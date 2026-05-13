# 材料力学

## 定义
材料力学是研究变形固体在外力作用下的内力、应力、变形和稳定性问题的学科。

## 核心内容

### 内力分析

**轴力**：$N$（拉力为正）

**剪力**：$Q$（使隔离体顺时针转动为正）

**弯矩**：$M$（使梁下凹为正）

**扭矩**：$T$（右手螺旋指向外为正）

### 应力分析

**正应力**：$\sigma = \frac{N}{A}$（轴向拉压）

**剪应力**：$\tau = \frac{Q}{A}$（剪切）

**弯曲正应力**：

$$\sigma = \frac{My}{I}$$

**弯曲剪应力**：$\tau = \frac{QI^*}{Ib}$

**扭转剪应力**：$\tau = \frac{Tr}{I_p}$

### 变形分析

**轴向变形**：$\Delta l = \frac{NL}{EA}$

**扭转变形**：$\varphi = \frac{TL}{GI_p}$

**弯曲挠度**：利用积分法或叠加法求解

### 强度条件

**拉压强度**：$\sigma_{max} \leq [\sigma]$

**剪切强度**：$\tau_{max} \leq [\tau]$

**弯曲强度**：$\sigma_{max} = \frac{M_{max}}{W} \leq [\sigma]$

**扭转强度**：$\tau_{max} = \frac{T_{max}}{W_p} \leq [\tau]$

**组合变形强度**：利用强度理论

### 强度理论

**第一强度理论**（最大拉应力）：$\sigma_1 \leq [\sigma]$

**第三强度理论**（最大剪应力）：$\sigma_1-\sigma_3 \leq [\sigma]$

**第四强度理论**（最大畸变能）：

$$\sqrt{\frac{1}{2}[(\sigma_1-\sigma_2)^2+(\sigma_2-\sigma_3)^2+(\sigma_3-\sigma_1)^2]} \leq [\sigma]$$

### 压杆稳定

**欧拉公式**：

$$P_{cr} = \frac{\pi^2 EI}{(\mu l)^2}$$

**柔度**：$\lambda = \frac{\mu l}{i}$

**稳定条件**：$P \leq P_{cr}/n_{st}$

## 经典教材
- 刘鸿文《材料力学》
- 聂毓琴《材料力学》
- Beer & Johnston《Mechanics of Materials》
- Gere《Mechanics of Materials》

## 主要应用领域
- 结构强度设计
- 机械零件设计
- 轴的设计
- 压杆稳定分析
- 疲劳强度分析
