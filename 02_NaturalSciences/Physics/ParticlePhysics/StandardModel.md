---
aliases:
  - 粒子物理标准模型
  - Standard Model of Particle Physics
  - 标准模型
  - Standard Model
tags:
  - physics
  - particle-physics
  - standard-model
  - quantum-field-theory
  - fundamental-particles
created: 2026-06-28
updated: 2026-06-28
---

# 粒子物理标准模型 (Standard Model of Particle Physics)

## 概述 (Overview)

粒子物理标准模型 (Standard Model, SM) 是描述强相互作用、弱相互作用和电磁相互作用三种基本力及其所涉及基本粒子的量子场论 (quantum field theory) 框架。它是20世纪物理学最伟大的成就之一，经受了半个世纪的精密实验检验。

标准模型的拉格朗日量 (Lagrangian) 可写为：

$$\mathcal{L}_{\text{SM}} = \mathcal{L}_{\text{gauge}} + \mathcal{L}_{\text{fermion}} + \mathcal{L}_{\text{Higgs}} + \mathcal{L}_{\text{Yukawa}}$$

---

## 基本粒子 (Fundamental Particles)

### 费米子 (Fermions) — 自旋 1/2

#### 夸克 (Quarks)

| 代 | 上型夸克 | 电荷 | 下型夸克 | 电荷 |
|----|---------|------|---------|------|
| 第一代 | u (up) | +2/3 | d (down) | -1/3 |
| 第二代 | c (charm) | +2/3 | s (strange) | -1/3 |
| 第三代 | t (top) | +2/3 | b (bottom) | -1/3 |

夸克特征：
- **色荷** (color charge)：红、绿、蓝三种
- **夸克禁闭** (quark confinement)：自由状态下不可观测
- **渐近自由** (asymptotic freedom)：高能下耦合常数减小

#### 轻子 (Leptons)

| 代 | 带电轻子 | 电荷 | 中微子 | 电荷 |
|----|---------|------|--------|------|
| 第一代 | $e$ (electron) | -1 | $\nu_e$ | 0 |
| 第二代 | $\mu$ (muon) | -1 | $\nu_\mu$ | 0 |
| 第三代 | $\tau$ (tau) | -1 | $\nu_\tau$ | 0 |

轻子特征：
- 不参与强相互作用
- 中微子质量极小（中微子振荡证实有质量）

### 三代费米子 (Three Generations)

每代包含：
- 一个上型夸克（电荷 +2/3）
- 一个下型夸克（电荷 -1/3）
- 一个带电轻子（电荷 -1）
- 一个中微子（电荷 0）

$$\begin{pmatrix} \nu_e \\ e \end{pmatrix}_L, \quad e_R, \quad \begin{pmatrix} u \\ d \end{pmatrix}_L, \quad u_R, \quad d_R$$

下标 $L/R$ 表示左/右手征 (chirality)。

### 反粒子 (Antiparticles)

每个粒子都有对应的反粒子，具有相同质量但相反的所有量子数。

---

## 规范玻色子 (Gauge Bosons) — 自旋 1

### 规范对称性 (Gauge Symmetry)

标准模型基于规范群：

$$SU(3)_C \times SU(2)_L \times U(1)_Y$$

| 规范群 | 相互作用 | 规范玻色子 | 质量 | 耦合常数 |
|--------|---------|-----------|------|---------|
| $SU(3)_C$ | 强 | 8 种胶子 (gluon) | 0 | $\alpha_s \sim 0.1$ |
| $SU(2)_L$ | 弱 | $W^\pm$, $Z^0$ | 80/91 GeV | $\alpha_w \sim 0.03$ |
| $U(1)_Y$ | 超荷 | $B^0$ (混合为 $\gamma$, $Z$) | — | $g'$ |

### 电磁相互作用 (Electromagnetism)

- 光子 $\gamma$：无质量，长程力
- 量子电动力学 (QED)：$U(1)_{\text{em}}$ 规范理论
- 精细结构常数：$\alpha = e^2 / (4\pi \varepsilon_0 \hbar c) \approx 1/137$

### 弱相互作用 (Weak Interaction)

- $W^\pm$ 和 $Z^0$ 玻色子：大质量（~80-91 GeV），短程力
- **宇称不守恒** (parity violation)：弱相互作用只耦合左手费米子
- **夸克混合** (quark mixing)：CKM 矩阵

$$V_{\text{CKM}} = \begin{pmatrix} V_{ud} & V_{us} & V_{ub} \\ V_{cd} & V_{cs} & V_{cb} \\ V_{td} & V_{ts} & V_{tb} \end{pmatrix}$$

### 强相互作用 (Strong Interaction)

- 量子色动力学 (QCD)：$SU(3)_C$ 规范理论
- 8 种胶子：自耦合（非阿贝尔规范理论）
- **夸克禁闭**：色荷不能单独存在
- **渐近自由**：$\alpha_s(Q^2) \to 0$ 当 $Q^2 \to \infty$

$$\alpha_s(Q^2) = \frac{12\pi}{(33 - 2n_f)\ln(Q^2/\Lambda_{\text{QCD}}^2)}$$

---

## 希格斯机制 (Higgs Mechanism)

### 自发对称性破缺 (Spontaneous Symmetry Breaking)

希格斯场 $\phi$ 是 $SU(2)_L$ 双态复标量场：

$$V(\phi) = \mu^2 \phi^\dagger \phi + \lambda (\phi^\dagger \phi)^2$$

当 $\mu^2 < 0$ 时，势能具有非零真空期望值 (VEV)：

$$\langle\phi\rangle = \frac{1}{\sqrt{2}} \begin{pmatrix} 0 \\ v \end{pmatrix}, \quad v = \sqrt{\frac{-\mu^2}{\lambda}} \approx 246 \text{ GeV}$$

### 质量生成 (Mass Generation)

- **规范玻色子质量**：$W^\pm$ 和 $Z^0$ 通过吃掉戈德斯通玻色子 (Goldstone bosons) 获得质量
  - $m_W = \frac{gv}{2} \approx 80.4$ GeV
  - $m_Z = \frac{v\sqrt{g^2 + g'^2}}{2} \approx 91.2$ GeV
  - 光子保持无质量

- **费米子质量**：通过汤川耦合 (Yukawa coupling)
  - $\mathcal{L}_{\text{Yukawa}} = -y_f \bar{\psi}_L \phi \psi_R + \text{h.c.}$
  - $m_f = \frac{y_f v}{\sqrt{2}}$

### 希格斯玻色子 (Higgs Boson)

希格斯场的量子激发：

$$m_H = \sqrt{2\lambda} \, v \approx 125.1 \text{ GeV}$$

**发现**：2012年7月4日，ATLAS 和 CMS 实验在 LHC 上宣布发现 $m_H \approx 125$ GeV 的新粒子。

2013年 Englert 和 Higgs 获诺贝尔物理学奖。

---

## 标准模型的精密检验 (Precision Tests)

### 电弱精密测量

- **Z 玻色子参数**：$m_Z$、$\Gamma_Z$、分支比
- **W 玻色子质量**：$m_W = 80.379 \pm 0.012$ GeV
- **弱混合角**：$\sin^2\theta_W \approx 0.231$

### CKM 矩阵检验

- **幺正三角形** (unitarity triangle)：$V_{ud}V_{ub}^* + V_{cd}V_{cb}^* + V_{td}V_{tb}^* = 0$
- B 工厂 (Belle、Babar) 和 LHCb 的精确测量

### 味物理异常 (Flavor Anomalies)

近年来 B 介子衰变中的一些轻微偏差：

- $R_{D^{(*)}}$：$\tau/\mu$ 比率略高于 SM 预言
- $R_K$：$e/\mu$ 普适性可能破缺
- 需要更多数据确认是否为新物理信号

---

## 超出标准模型 (Beyond the Standard Model, BSM)

### 暗物质 (Dark Matter)

标准模型无法解释的宇宙学证据：

- 星系旋转曲线 (galaxy rotation curves)
- 引力透镜 (gravitational lensing)
- 宇宙微波背景辐射 (CMB) 各向异性

暗物质候选者：
- **WIMP** (Weakly Interacting Massive Particle)：~10-1000 GeV
- **轴子** (axion)：~$10^{-6}$-$10^{-3}$ eV
- **惰性中微子** (sterile neutrino)：~keV

### 中微子质量 (Neutrino Masses)

标准模型预言中微子无质量，但中微子振荡证实有质量：

$$\begin{pmatrix} \nu_e \\ \nu_\mu \\ \nu_\tau \end{pmatrix} = U \begin{pmatrix} \nu_1 \\ \nu_2 \\ \nu_3 \end{pmatrix}$$

PMNS 矩阵 $U$ 包含三个混合角和一个 CP 相位。

未解问题：
- 质量层级 (mass hierarchy)：正序 ($m_1 < m_2 < m_3$) 还是逆序？
- 中微子是马约拉纳粒子 (Majorana particle) 还是狄拉克粒子？
- 绝对质量标度

### 其他 BSM 物理

| 问题 | 标准模型局限 | BSM 方案 |
|------|------------|---------|
| 等级问题 (hierarchy problem) | 希格斯质量对紫外截断敏感 | 超对称 (SUSY)、复合希格斯 |
| 大统一 (grand unification) | 三种力未统一 | SU(5)、SO(10) |
| 强 CP 问题 | QCD 允许 CP 破缺项 | 轴子 (axion) |
| 引力 | 未纳入 SM | 弦理论、圈量子引力 |
| 物质-反物质不对称 | CP 破缺不足 | 轻子生成 (leptogenesis) |

---

## 实验设施 (Experimental Facilities)

| 设施 | 类型 | 主要成就 |
|------|------|---------|
| LHC (CERN) | 质子-质子对撞机 (13.6 TeV) | 发现希格斯玻色子 |
| Fermilab | 质子-反质子对撞机 | 发现 top 夸克 |
| KEK/Belle II | 电子-正电子对撞机 | B 介子 CP 破缺 |
| JUNO (中国) | 中微子振荡实验 | 质量层级 |
| LZ/XENON | 暗物质直接探测 | 限制 WIMP 截面 |

---

## 参考与延伸阅读 (References and Further Reading)

1. *Introduction to Elementary Particles* — D. Griffiths
2. *Quantum Field Theory and the Standard Model* — M. D. Schwartz
3. *The Standard Model: A Primer* — C. P. Burgess and G. D. Moore
4. *Neutrino Oscillations* — T. Kajita and A. B. McDonald, Rev. Mod. Phys. 88, 030501 (2016)
5. *Particle Physics: A Very Short Introduction* — F. Close
