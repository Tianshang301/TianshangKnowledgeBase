---
aliases: [NuclearPhysics]
tags: ['EnergyAndNuclearEngineering', 'NuclearEngineering', 'NuclearPhysics']
created: 2026-05-16
updated: 2026-05-16
---

# 核物理学

## 定义
核物理学是研究原子核的结构、性质、反应和衰变规律的物理学分支。是核能工程的理论基础。

## 核心内容

### 原子核结构

**核素**：$^A_ZX$（$Z$ 质子数，$A$ 质量数）

**核力**：强相互作用，短程力（~10⁻¹⁵m）

**核结合能**：

$$B = [Zm_p + (A-Z)m_n - M]c^2$$

**比结合能**：$\varepsilon = B/A$

**比结合能曲线**：轻核聚变和重核裂变都能释放能量

### 液滴模型

Weizsäcker 半经验质量公式：
$$B = a_V A - a_S A^{2/3} - a_C \frac{Z(Z-1)}{A^{1/3}} - a_A \frac{(A-2Z)^2}{A} + \delta(A, Z)$$

| 项 | 符号 | 物理意义 | 经验值 |
|---|------|---------|-------|
| 体积能 | $a_V A$ | 核力饱和，与体积成正比 | $a_V \approx 15.75$ MeV |
| 表面能 | $-a_S A^{2/3}$ | 表面核子受核力较少 | $a_S \approx 17.80$ MeV |
| 库仑能 | $-a_C Z(Z-1)/A^{1/3}$ | 质子间静电排斥 | $a_C \approx 0.711$ MeV |
| 对称能 | $-a_A (A-2Z)^2/A$ | 中子质子数平衡 | $a_A \approx 23.70$ MeV |
| 对能 | $\delta(A, Z)$ | 核子配对效应 | $a_P \approx \pm 11.18/\sqrt{A}$ MeV |

**对能项**：
$$\delta(A, Z) =
\begin{cases}
+a_P A^{-1/2}, & Z, N \text{ 均为偶（偶偶核）} \\
0, & A \text{ 为奇（奇核）} \\
-a_P A^{-1/2}, & Z, N \text{ 均为奇（奇奇核）}
\end{cases}$$

液滴模型成功解释了结合能系统性和核裂变机制，但无法解释幻数等精细结构。

### 壳层模型

**幻数**：$2, 8, 20, 28, 50, 82, 126$

具有幻数中子或质子的核特别稳定（类似惰性气体电子壳层）。

**自旋-轨道耦合势**：$V(r) + V_{LS}(r)(\mathbf{L}\cdot\mathbf{S})$

**能级顺序**（在自旋-轨道耦合下重新排列）：
$$1s_{1/2},\ 1p_{3/2},\ 1p_{1/2},\ 1d_{5/2},\ 2s_{1/2},\ 1d_{3/2},\ 1f_{7/2},\ \dots$$

**核自旋与宇称**：奇 $A$ 核的自旋与宇称由最后一个奇核子决定。

壳层模型成功解释了幻数、核自旋、核磁矩等性质。

### 放射性衰变

**放射性衰变类型对比**：

| 衰变类型 | 衰变前 | 衰变后 | 粒子 | 穿透能力 | 本质 |
|---------|--------|--------|------|---------|------|
| **α衰变** | $^A_ZX$ | $^{A-4}_{Z-2}Y$ | $^4_2\text{He}^{2+}$ | 弱（纸可阻挡） | 强相互作用隧道效应 |
| **β⁻衰变** | $^A_ZX$ | $^A_{Z+1}Y$ | $e^-, \bar{\nu}_e$ | 中等（铝板阻挡） | 弱相互作用 |
| **β⁺衰变** | $^A_ZX$ | $^A_{Z-1}Y$ | $e^+, \nu_e$ | 中等 | 弱相互作用 |
| **电子俘获** | $^A_ZX$ | $^A_{Z-1}Y$ | $\nu_e, \text{Auger 电子/X 射线}$ | — | 内层电子被俘获 |
| **γ衰变** | $^A_ZX^*$ | $^A_ZX$ | $\gamma$ 光子 | 强（铅板阻挡） | 电磁相互作用 |

**α衰变**：$^A_ZX \to ^{A-4}_{Z-2}Y + ^4_2\text{He}$

**β⁻衰变**：$^A_ZX \to ^A_{Z+1}Y + e^- + \bar{\nu}_e$

**β⁺衰变**：$^A_ZX \to ^A_{Z-1}Y + e^+ + \nu_e$

**γ衰变**：激发态核退激辐射γ光子

**衰变规律相关量关系**：

$$\lambda = \frac{\ln 2}{t_{1/2}}, \quad \tau = \frac{1}{\lambda} = \frac{t_{1/2}}{\ln 2}$$

其中 $\lambda$ 为衰变常数，$t_{1/2}$ 为半衰期，$\tau$ 为平均寿命。

**衰变规律**：$N(t) = N_0 e^{-\lambda t}$

**半衰期**：$t_{1/2} = \frac{\ln 2}{\lambda}$

### 放射性衰变链

**衰变链**：放射性核素连续衰变最终到达稳定核素。

**铀镭系**（$^{238}\text{U}$ → $^{206}\text{Pb}$，半衰期 $4.47 \times 10^9$ 年）：
$$^{238}\text{U} \xrightarrow{\alpha} ^{234}\text{Th} \xrightarrow{\beta^-} ^{234}\text{Pa} \xrightarrow{\beta^-} ^{234}\text{U} \xrightarrow{\alpha} ^{230}\text{Th} \xrightarrow{\alpha} ^{226}\text{Ra} \xrightarrow{\alpha} ^{222}\text{Rn} \xrightarrow{\alpha} ^{218}\text{Po} \xrightarrow{\alpha} ^{214}\text{Pb} \xrightarrow{\beta^-} ^{214}\text{Bi} \xrightarrow{\beta^-} ^{214}\text{Po} \xrightarrow{\alpha} ^{210}\text{Pb} \xrightarrow{\beta^-} ^{210}\text{Bi} \xrightarrow{\beta^-} ^{210}\text{Po} \xrightarrow{\alpha} ^{206}\text{Pb}$$

**钍系**（$^{232}\text{Th}$ → $^{208}\text{Pb}$，半衰期 $1.41 \times 10^{10}$ 年）：
$$^{232}\text{Th} \xrightarrow{\alpha} ^{228}\text{Ra} \xrightarrow{\beta^-} ^{228}\text{Ac} \xrightarrow{\beta^-} ^{228}\text{Th} \xrightarrow{\alpha} ^{224}\text{Ra} \xrightarrow{\alpha} ^{220}\text{Rn} \xrightarrow{\alpha} ^{216}\text{Po} \xrightarrow{\alpha} ^{212}\text{Pb} \xrightarrow{\beta^-} ^{212}\text{Bi} \xrightarrow{\beta^-} ^{212}\text{Po} \xrightarrow{\alpha} ^{208}\text{Pb}$$

**长期平衡条件**（母核半衰期远大于子核）：
$$\lambda_1 N_1 = \lambda_2 N_2 = \cdots = \lambda_k N_k$$

此时各代核素的活度相等：$A_1 = A_2 = \cdots = A_k$。

### 核反应

**核裂变**：

$$^{235}_{92}U + n \to ^{141}_{56}Ba + ^{92}_{36}Kr + 3n + \text{能量}$$

每次裂变释放约200MeV 能量，能量分布：

| 裂变产物 | 能量份额 |
|---------|---------|
| 裂变碎片动能 | ~168 MeV |
| 瞬发γ射线 | ~8 MeV |
| 裂变中子动能 | ~5 MeV |
| β衰变 | ~7 MeV |
| 缓发γ射线 | ~7 MeV |
| 中微子 | ~12 MeV |

**核聚变**：

$$^2_1\text{H} + ^3_1\text{H} \to ^4_2\text{He} + n + 17.6\,\text{MeV}$$

**裂变与聚变对比**：

| 特性 | 核裂变 | 核聚变 |
|------|--------|--------|
| 核燃料 | $^{235}\text{U}, ^{239}\text{Pu}$ | 氘、氚（$^2\text{H}, ^3\text{H}$） |
| 燃料储量 | 有限（铀矿约可使用数百年） | 几乎无限（海水中含氘） |
| 单位质量能量 | ~1 MeV/核子 | ~3.5 MeV/核子 |
| 放射性废物 | 高放、长寿命（千年~万年） | 低放、短寿命（氚半衰期12.3年） |
| 临界安全 | 有临界事故风险 | 无临界风险（事故即停止） |
| 技术成熟度 | 已商业化运行70年 | 实验阶段（ITER 在建） |
| 主要污染风险 | 核泄漏、乏燃料 | 氚放射性、中子活化 |

**反应截面**：$\sigma$（靶恩，b = $10^{-24}$ cm²）

**中子按能量分类**：

| 中子类型 | 能量范围 | 特点 |
|---------|---------|------|
| 热中子 | ~0.025 eV | 与慢化剂热平衡，可引发 $^{235}\text{U}$ 裂变 |
| 慢中子 | 1 eV ~ 100 eV | 共振吸收区 |
| 中能中子 | 100 eV ~ 100 keV | 共振区 |
| 快中子 | > 100 keV | 裂变产生的原始中子，需慢化 |

### 中子物理学

**中子慢化**：快中子→热中子

**慢化过程**：快中子通过与慢化剂原子核的弹性碰撞损失能量。每次弹性碰撞的平均对数能降：

$$\xi = 1 + \frac{(A-1)^2}{2A} \ln\frac{A-1}{A+1}$$

其中 $A$ 为原子核质量数。对于氢核（$A=1$），$\xi = 1$，一次碰撞可损失全部能量。

**慢化剂性能对比**：

| 慢化剂 | 慢化能力 $\xi \Sigma_s$ | 慢化比 $\xi \Sigma_s / \Sigma_a$ | 吸收截面 | 反应堆类型 |
|--------|----------------------|-------------------------------|---------|-----------|
| 轻水 $\text{H}_2\text{O}$ | 高 | 较低 (~70) | 较高 | PWR, BWR |
| 重水 $\text{D}_2\text{O}$ | 中 | 很高 (~2100) | 极低 | CANDU |
| 石墨 $\text{C}$ | 低 | 高 (~200) | 很低 | Magnox, AGR |
| 铍 $\text{Be}$ | 中 | 高 | 低 | 研究堆 |

**中子扩散**：$J = -D\nabla\phi$，其中 $\phi$ 为中子通量，$D$ 为扩散系数。

**四因子公式**：无限增殖系数 $k_{\infty} = \eta f p \varepsilon$

| 因子 | 符号 | 物理意义 |
|------|------|---------|
| 快中子裂变因子 | $\varepsilon$ | 每次吸收产生的所有裂变中子数 |
| 逃脱共振吸收概率 | $p$ | 慢化过程中未被共振吸收的概率 |
| 热利用系数 | $f$ | 热中子被燃料吸收的比例 |
| 再生因子 | $\eta$ | 每次燃料吸收产生的裂变中子数 |

有效增殖系数：$k_{\text{eff}} = k_{\infty} P_{NL} P_{NL}'$，考虑中子泄漏。

反应堆状态：
- $k_{\text{eff}} = 1$：临界（稳定功率）
- $k_{\text{eff}} > 1$：超临界（功率上升）
- $k_{\text{eff}} < 1$：次临界（功率下降）

## 经典教材
- 胡仲森《核反应堆物理》
- 谢仲生《核反应堆物理分析》
- Krane《Introductory Nuclear Physics》
- Lamarsh《Introduction to Nuclear Engineering》

## 主要应用领域
- 核电站
- 核武器
- 核医学
- 核探测
- 核技术应用

## 相关条目

- [[NuclearPhysics]]
- [[12_SportsScience/ExercisePhysiology/EnergySystems|EnergySystems]]
- RadiationProtection
- ThermalEngineering


