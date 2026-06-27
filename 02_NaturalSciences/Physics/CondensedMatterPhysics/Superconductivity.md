---
aliases:
  - 超导物理
  - Superconductivity Physics
  - 超导电性
  - Superconductivity
tags:
  - physics
  - condensed-matter
  - superconductivity
  - quantum-materials
  - bcs-theory
created: 2026-06-28
updated: 2026-06-28
---

# 超导物理 (Superconductivity Physics)

## 概述 (Overview)

超导 (superconductivity) 是指某些材料在低于临界温度 $T_c$ 时电阻完全消失并表现出完全抗磁性 (perfect diamagnetism) 的量子现象。自1911年翁纳斯 (Kamerlingh Onnes) 在汞中发现超导以来，这一领域已发展出丰富的理论体系和广泛的技术应用。

超导研究的核心问题包括：寻找更高 $T_c$ 的超导材料、理解非常规超导配对机制、以及开发超导技术应用。

---

## BCS 理论 (BCS Theory)

### 库珀对 (Cooper Pairs)

BCS 理论的核心是电子通过电声子相互作用 (electron-phonon interaction) 形成库珀对。费米面附近动量相反、自旋相反的两个电子通过交换虚声子形成束缚态：

$$|\Psi\rangle = \sum_k g_k c_{k\uparrow}^\dagger c_{-k\downarrow}^\dagger |0\rangle$$

库珀对的特征：
- 总动量为零：$\vec{k}_{\uparrow} + (-\vec{k})_{\downarrow} = 0$
- 自旋单态 (spin singlet)：$S = 0$
- 对称性：$s$-波配对（各向同性）

### 能隙函数 (Energy Gap Function)

BCS 超导体在费米能级处存在能隙 $\Delta$：

$$\Delta(T) \approx 1.74 \, \Delta(0) \sqrt{1 - \frac{T}{T_c}} \quad (T \to T_c)$$

零温能隙与临界温度的关系：

$$\frac{\Delta(0)}{k_B T_c} \approx 1.764$$

### BCS 基态与激发谱 (BCS Ground State and Excitation Spectrum)

BCS 基态波函数：

$$|\text{BCS}\rangle = \prod_k (u_k + v_k c_{k\uparrow}^\dagger c_{-k\downarrow}^\dagger) |0\rangle$$

准粒子激发能量：

$$E_k = \sqrt{\xi_k^2 + |\Delta_k|^2}$$

其中 $\xi_k = \varepsilon_k - \mu$ 是相对于费米能的动能。

---

## 超导体的分类 (Classification of Superconductors)

### 第一类超导体 (Type-I Superconductors)

- 完全迈斯纳效应直到单一临界磁场 $H_c$
- 伦敦穿透深度 $\lambda_L \ll$ 相干长度 $\xi$
- 典型材料：纯金属 Pb、Hg、Sn、Al、In

### 第二类超导体 (Type-II Superconductors)

- 存在下临界磁场 $H_{c1}$ 和上临界磁场 $H_{c2}$
- 混合态 (mixed state)：磁通涡旋 (flux vortex) 穿透材料
- $\lambda_L \gg \xi$，GL 参数 $\kappa = \lambda_L / \xi > 1/\sqrt{2}$

| 参数 | 第一类 | 第二类 |
|------|--------|--------|
| 临界磁场 | 单一 $H_c$ | $H_{c1}$, $H_{c2}$ |
| GL 参数 $\kappa$ | $< 1/\sqrt{2}$ | $> 1/\sqrt{2}$ |
| 磁通穿透 | 阶跃式 | 渐进式（混合态） |
| 典型材料 | 纯金属 | 合金、化合物 |

---

## 高温超导体 (High-Temperature Superconductors)

### 铜氧化物超导体 (Cuprate Superconductors)

1986年柏诺兹和缪勒发现 La-Ba-Cu-O 体系超导，掀起高温超导研究热潮：

| 材料 | 化学式 | $T_c$ (K) | 发现年份 |
|------|--------|-----------|---------|
| 镧系 | La$_{2-x}$Ba$_x$CuO$_4$ | ~35 | 1986 |
| 钇系 | YBa$_2$Cu$_3$O$_{7-\delta}$ | ~92 | 1987 |
| 铋系 | Bi$_2$Sr$_2$CaCu$_2$O$_{8+\delta}$ | ~108 | 1988 |
| 铊系 | Tl$_2$Ba$_2$Ca$_2$Cu$_3$O$_{10}$ | ~125 | 1988 |
| 汞系 | HgBa$_2$Ca$_2$Cu$_3$O$_{8+\delta}$ | ~134 | 1993 |

铜氧化物超导体的特征：
- 层状结构：CuO$_2$ 平面是超导发生的关键层
- $d$-波配对对称性：$\Delta_k \propto \cos k_x - \cos k_y$
- 赝能隙 (pseudogap)：$T^*$ 温度以上出现的部分能隙
- 强关联电子体系：不能用传统费米液体理论描述

### 铁基超导体 (Iron-Based Superconductors)

2008年细野秀雄发现 LaFeAsO$_{1-x}$F$_x$ 在 $T_c \approx 26$ K 超导：

- 五大体系：1111、122、111、11、42622
- 最高 $T_c$：SmFeAsO$_{1-x}$F$_x$ (~55 K)
- 配对对称性：可能的 $s^\pm$-波（符号反转的 $s$-波）
- 反铁磁涨落驱动配对

---

## 室温超导争议 (Room-Temperature Superconductivity Controversies)

### LK-99 事件 (2023)

2023年韩国团队声称在改性铅磷灰石 (Pb$_{10}$(PO$_4$)$_6$O，命名为 LK-99) 中发现室温常压超导：

- 声称 $T_c > 123°\text{C}$（396 K）
- 引发全球关注和大量重复实验
- 最终被否定：观测到的"超导"行为源于 Cu$_2$S 杂质的相变
- 教训：科学声明需要严格的同行评审和独立验证

### 其他室温超导声明

- 2020年 Dias 团队：碳质氢化物在 288 K（15°C）、267 GPa 下超导
- 2022年被 Nature 撤稿，数据处理存在争议
- 高压氢化物超导仍是最有希望实现室温超导的路径之一

---

## 超导理论框架 (Theoretical Frameworks)

### 金兹堡-朗道理论 (Ginzburg-Landau Theory)

唯象理论，引入序参量 (order parameter) $\psi$：

$$F = F_n + \alpha |\psi|^2 + \frac{\beta}{2} |\psi|^4 + \frac{1}{2m^*} \left| \left(-i\hbar\nabla - \frac{e^*}{c}\vec{A}\right) \psi \right|^2 + \frac{h^2}{8\pi}$$

相干长度 $\xi$ 和穿透深度 $\lambda$：

$$\xi = \sqrt{\frac{\hbar^2}{2m^* |\alpha|}}, \quad \lambda = \sqrt{\frac{m^* c^2}{4\pi n_s (e^*)^2}}$$

### 伊利阿什伯格理论 (Eliashberg Theory)

超越 BCS 的强耦合理论，考虑声子谱 $\alpha^2 F(\omega)$：

$$Z(i\omega_n) = 1 + \frac{\pi T}{\omega_n} \sum_m \lambda(i\omega_n - i\omega_m) \frac{\omega_m}{\sqrt{\omega_m^2 + \Delta_m^2}}$$

---

## 超导应用 (Applications)

### 磁悬浮 (Magnetic Levitation)

- 高温超导体的磁通钉扎 (flux pinning) 实现稳定悬浮
- 超导磁悬浮列车：日本 JR 磁悬浮（L0 系列，时速 603 km/h）
- 轴向磁悬浮轴承

### SQUID (Superconducting Quantum Interference Device)

超导量子干涉仪利用约瑟夫森效应 (Josephson effect) 测量极微弱磁场：

- 灵敏度：~$10^{-15}$ T（飞特斯拉量级）
- 应用：脑磁图 (MEG)、地质勘探、暗物质探测

### 超导量子比特 (Superconducting Qubits)

| 类型 | 代表 | 特征 |
|------|------|------|
| 电荷量子比特 | Cooper pair box | 对电荷敏感 |
| 通量量子比特 | Flux qubit | 对磁通敏感 |
| 相位量子比特 | Phase qubit | 对相位敏感 |
| Transmon | IBM/Google | 对电荷噪声不敏感 |

IBM 和 Google 的量子处理器基于 Transmon 量子比特，已实现数百量子比特规模。

### 其他应用

- **核磁共振** (NMR) 和 **磁共振成像** (MRI) 超导磁体
- 粒子加速器超导射频腔 (superconducting RF cavity)
- 超导电缆和电力传输
- 超导数字电路 (RSFQ 逻辑)

---

## 前沿与展望 (Frontiers and Outlook)

- **室温超导探索**：高压氢化物、新型材料体系
- **拓扑超导体**：马约拉纳费米子与容错量子计算
- **非常规配对机制**：铜氧化物和铁基超导的微观理论
- **超导量子计算**：从 NISQ 到容错量子计算

---

## 参考与延伸阅读 (References and Further Reading)

1. *Introduction to Superconductivity* — M. Tinkham
2. *BCS: 50 Years* — L. N. Cooper and D. Feldman (eds.)
3. *High-Temperature Superconductors* — J. G. Bednorz and K. A. Müller
4. *Iron-Based Superconductors* — P. C. Canfield and S. L. Bud'ko
5. *Superconductivity of Metals and Alloys* — P. G. de Gennes
