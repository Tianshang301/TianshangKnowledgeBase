---
aliases:
  - 质谱分析
  - Mass Spectrometry
  - MS
  - 质谱法
tags:
  - chemistry
  - analytical-chemistry
  - mass-spectrometry
  - proteomics
  - omics
created: 2026-06-28
updated: 2026-06-28
---

# 质谱分析 (Mass Spectrometry)

## 概述 (Overview)

质谱 (mass spectrometry, MS) 是通过测量离子的质荷比 (mass-to-charge ratio, $m/z$) 来鉴定和定量分析化合物的强大分析技术。现代质谱仪具有极高的灵敏度 (attomole 级别)、分辨率 (分辨率 > 200,000) 和质量精度 (< 1 ppm)，广泛应用于化学、生物、医学、环境等领域。

质谱分析的基本流程：**样品引入 → 电离 → 质量分析 → 检测 → 数据处理**

---

## 电离技术 (Ionization Techniques)

### 电喷雾电离 (Electrospray Ionization, ESI)

1984年由 Fenn 等人发展，2002年获诺贝尔化学奖：

- **原理**：在强电场下，液体通过毛细管形成带电液滴 (Taylor cone)，溶剂蒸发导致液滴库仑爆炸 (Coulomb explosion)，最终产生气相离子
- **特征**：软电离 (soft ionization)，产生多电荷离子 $[M+nH]^{n+}$
- **适用**：极性大分子（蛋白质、多肽、核酸、多糖）
- **联用**：常与液相色谱 (LC-MS) 联用

多电荷离子的优势：扩展质量范围（如 100 kDa 蛋白在 $m/z$ 1000-2000 范围内检测）

### 基质辅助激光解吸电离 (MALDI)

1985年由 Karas 和 Hillenkamp 发展：

- **原理**：分析物与基质 (matrix) 共结晶，脉冲激光 (通常 337 nm N$_2$ 激光) 激发基质分子，通过能量转移使分析物解吸电离
- **特征**：主要产生单电荷离子 $[M+H]^+$
- **基质**：CHCA（α-氰基-4-羟基肉桂酸）、SA（芥子酸）、DHB（2,5-二羟基苯甲酸）
- **适用**：多肽、蛋白质、聚合物、小分子

### 其他电离技术

| 技术 | 原理 | 应用 |
|------|------|------|
| EI (电子轰击) | 70 eV 电子束 | GC-MS，小分子 |
| CI (化学电离) | 离子-分子反应 | 软电离替代 EI |
| APCI (大气压化学电离) | 电晕放电 | 中等极性化合物 |
| APPI (大气压光电离) | 光子电离 | 非极性化合物 |
| DESI (解吸电喷雾) | 带电溶剂喷雾 | 原位分析 |
| SIMS (二次离子质谱) | 初级离子束轰击 | 表面分析 |

---

## 质量分析器 (Mass Analyzers)

### Orbitrap 质量分析器

由 Makarov 于2005年开发，是当前高分辨质谱的主流：

- **原理**：离子在外电极和中心电极之间的静电场中做轨道运动，通过傅里叶变换 (FFT) 分析离子的轴向振荡频率
- **分辨率**：> 200,000 (FWHM)
- **质量精度**：< 1 ppm
- **扫描速度**：中等（适合 UHPLC 联用）

$$m/z = \frac{k}{f^2}$$

其中 $f$ 是振荡频率，$k$ 是仪器常数。

### 飞行时间质量分析器 (Time-of-Flight, TOF)

- **原理**：相同动能的离子飞行通过漂移管，轻离子先到达检测器
- **分辨率**：10,000 - 60,000
- **优势**：扫描速度快、质量范围宽
- **反射器** (reflectron)：补偿初始能量分散，提高分辨率

$$t = L \sqrt{\frac{m}{2zV}}$$

### 四极杆质量分析器 (Quadrupole, Q)

- **原理**：四根平行电极产生的交变电场中，特定 $m/z$ 的离子稳定振荡通过
- **分辨率**：单位分辨（~1 Da）
- **应用**：定量分析（SRM/MRM 模式）

### 离子阱 (Ion Trap)

- **三维离子阱** (Paul trap) 和 **线性离子阱** (linear ion trap)
- 可进行多级质谱 (MS$^n$)
- 与 Orbitrap 或 TOF 串联使用

### 串联质谱 (Tandem Mass Spectrometry, MS/MS)

$$\text{前体离子选择} \to \text{碎裂 (CID/HCD/EThcD)} \to \text{产物离子分析}$$

碎裂技术：
- **CID** (碰撞诱导解离)：低能碰撞活化
- **HCD** (高能碰撞解离)：Orbitrap 中实现
- **EThcD**：电子转移/高能碰撞解离，保留翻译后修饰

---

## 蛋白质组学 (Proteomics)

### 自下而上蛋白质组学 (Bottom-Up Proteomics)

工作流程：

1. **样品制备**：蛋白提取、还原烷基化、酶解 (trypsin)
2. **肽段分离**：nanoLC-MS/MS
3. **数据采集**：
   - **DDA** (data-dependent acquisition)：选择强度最高的前体离子碎裂
   - **DIA** (data-independent acquisition)：如 SWATH，系统碎裂所有离子
4. **数据库搜索**：MaxQuant、Proteome Discoverer、Spectronaut
5. **统计分析**：FDR 控制 (< 1%)

### 定量蛋白质组学 (Quantitative Proteomics)

| 方法 | 类型 | 原理 |
|------|------|------|
| TMT/iTRAQ | 标记 | 同重标签，MS2/MS3 定量 |
| SILAC | 标记 | 代谢标记重/轻氨基酸 |
| Label-free | 非标记 | 前体离子强度或谱图计数 |
| DIA | 非标记 | 全离子碎裂，系统定量 |

### 翻译后修饰分析 (PTM Analysis)

- **磷酸化** (phosphorylation)：TiO$_2$ 或 IMAC 富集
- **糖基化** (glycosylation)：凝集素富集或化学酶法
- **泛素化** (ubiquitination)：K-$\varepsilon$-GG 抗体富集
- **乙酰化** (acetylation)：赖氨酸乙酰化抗体

---

## 代谢组学 (Metabolomics)

### 非靶向代谢组学 (Untargeted Metabolomics)

- **目标**：全面检测样品中的小分子代谢物 (MW < 1500 Da)
- **平台**：LC-MS、GC-MS、CE-MS
- **数据分析**：
  - 峰对齐和归一化
  - 多变量统计 (PCA、PLS-DA)
  - 代谢物鉴定 (HMDB、METLIN、mzCloud)
  - 通路富集分析 (MetaboAnalyst)

### 靶向代谢组学 (Targeted Metabolomics)

- 使用标准品建立校准曲线
- SRM/MRM 模式高灵敏度定量
- 临床应用：新生儿筛查、药物代谢监测

---

## 成像质谱 (Mass Spectrometry Imaging, MSI)

### MALDI-MSI

- **原理**：在组织切片上喷涂基质，逐点激光采集质谱
- **分辨率**：5-50 μm（取决于激光聚焦和步进）
- **应用**：药物分布、脂质组学、生物标志物发现

### DESI-MSI

- **优势**：无需基质、常压操作、保持组织形态
- **应用**：术中肿瘤边界识别（如脑瘤手术）

### SIMS-MSI

- **原理**：初级离子束 (Bi$_3^+$, Au$_3^+$) 轰击表面产生二次离子
- **分辨率**：< 1 μm（纳米级空间分辨）
- **应用**：细胞膜脂质分布、半导体分析

---

## 单细胞质谱 (Single-Cell Mass Spectrometry)

### 技术挑战

- 细胞体积小（~1 pL）
- 分子种类多（数千种代谢物）
- 浓度动态范围大

### 关键技术

- **单细胞 MALDI-MS**：直接对单个细胞进行质谱分析
- **CyTOF** (mass cytometry)：金属标签抗体，单细胞蛋白质组
- **SCoPE-MS**：单细胞蛋白质组学新方法
- **液滴微流控** (droplet microfluidics)：单细胞包裹和分析

### 应用

- 细胞异质性 (cellular heterogeneity) 研究
- 肿瘤微环境 (tumor microenvironment) 解析
- 干细胞分化轨迹 (differentiation trajectory)

---

## 前沿进展 (Recent Advances)

- **4D-蛋白质组学**：离子淌度 (ion mobility) 分离增加维度
- **空间蛋白质组学**：结合空间转录组的多组学整合
- **实时直接分析**：如 DART、REIMS，无需色谱分离
- **AI 辅助谱图解析**：深度学习预测碎裂谱和保留时间

---

## 参考与延伸阅读 (References and Further Reading)

1. *Mass Spectrometry: Principles and Applications* — E. de Hoffmann and V. Stroobant
2. *Proteomics in Practice* — R. Westermeier and T. Naven
3. *Mass Spectrometry Imaging* — R. M. Caprioli (ed.)
4. *Single-Cell Proteomics* — B. Slavov, Science 367, 512 (2020)
5. *Orbitrap Mass Spectrometry* — A. Makarov, Anal. Chem. 72, 5691 (2000)
