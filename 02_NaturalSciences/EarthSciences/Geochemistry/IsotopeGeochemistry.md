---
aliases:
  - 同位素地球化学
  - Isotope Geochemistry
  - 同位素地质学
  - Isotopic Geology
tags:
  - earth-sciences
  - geochemistry
  - isotope-geochemistry
  - geochronology
  - paleoclimate
created: 2026-06-28
updated: 2026-06-28
---

# 同位素地球化学 (Isotope Geochemistry)

## 概述 (Overview)

同位素地球化学 (isotope geochemistry) 研究自然界中同位素 (isotopes) 的分布、分馏和衰变规律，利用同位素组成变化来揭示地球和行星系统的物质来源、演化过程和时间尺度。同位素方法是地球科学中最强大的示踪工具之一。

同位素分为两大类：
- **放射性同位素** (radiogenic isotopes)：通过放射性衰变产生，用于定年和示踪
- **稳定同位素** (stable isotopes)：不发生放射性衰变，通过质量分馏反映物理化学过程

---

## 放射性同位素定年 (Radiometric Dating)

### 基本原理

放射性衰变遵循一级动力学：

$$N(t) = N_0 e^{-\lambda t}$$

其中 $N_0$ 是初始原子数，$\lambda$ 是衰变常数 (decay constant)，$t$ 是时间。

半衰期 (half-life)：

$$t_{1/2} = \frac{\ln 2}{\lambda}$$

定年方程：

$$t = \frac{1}{\lambda} \ln\left(1 + \frac{D^*}{P}\right)$$

其中 $D^*$ 是放射成因子体同位素数目，$P$ 是母体同位素数目。

### U-Pb 定年

铀-铅定年是最精确的放射性定年方法之一：

$$^{238}\text{U} \to ^{206}\text{Pb}, \quad t_{1/2} = 4.468 \times 10^9 \text{ yr}$$
$$^{235}\text{U} \to ^{207}\text{Pb}, \quad t_{1/2} = 7.038 \times 10^8 \text{ yr}$$

**优势**：双衰变体系提供内部一致性检验 (concordia diagram)

**谐和图** (Concordia diagram)：

$$\frac{^{206}\text{Pb}}{^{238}\text{U}} = e^{\lambda_{238} t} - 1$$
$$\frac{^{207}\text{Pb}}{^{235}\text{U}} = e^{\lambda_{235} t} - 1$$

铅丢失导致数据点偏离谐和曲线 (discordia)，上下交点分别给出结晶年龄和铅丢失事件年龄。

**测定矿物**：锆石 (zircon)、独居石 (monazite)、磷灰石 (apatite)

### K-Ar 和 $^{40}$Ar/$^{39}$Ar 定年

$$^{40}\text{K} \to ^{40}\text{Ar}, \quad t_{1/2} = 1.25 \times 10^9 \text{ yr}$$

$^{40}$Ar/$^{39}$Ar 法通过中子活化将 $^{39}$K 转化为 $^{39}$Ar，实现同一样品中母体和子体的同步测定。

**应用**：火山岩定年、构造热事件、考古样品

### $^{14}$C 定年 (Radiocarbon Dating)

$$^{14}\text{C} \to ^{14}\text{N} + \beta^-, \quad t_{1/2} = 5730 \text{ yr}$$

**适用范围**：~50,000 年以内

**假设**：大气 $^{14}$C 浓度在历史上近似恒定（需树轮校正）

**应用**：考古定年、全新世地质事件、海洋环流示踪

加速器质谱 (AMS) 大大降低了样品量需求（~1 mg 碳）。

### Rb-Sr 定年

$$^{87}\text{Rb} \to ^{87}\text{Sr}, \quad t_{1/2} = 4.88 \times 10^{10} \text{ yr}$$

等时线法 (isochron method)：

$$\left(\frac{^{87}\text{Sr}}{^{86}\text{Sr}}\right) = \left(\frac{^{87}\text{Sr}}{^{86}\text{Sr}}\right)_0 + \left(\frac{^{87}\text{Rb}}{^{86}\text{Sr}}\right)(e^{\lambda t} - 1)$$

### Sm-Nd 定年

$$^{147}\text{Sm} \to ^{143}\text{Nd}, \quad t_{1/2} = 1.06 \times 10^{11} \text{ yr}$$

$\varepsilon_{\text{Nd}}$ 值用于示踪壳幔分异：

$$\varepsilon_{\text{Nd}}(t) = \left[\frac{(^{143}\text{Nd}/^{144}\text{Nd})_{\text{sample}}(t)}{(^{143}\text{Nd}/^{144}\text{Nd})_{\text{CHUR}}(t)} - 1\right] \times 10^4$$

---

## 稳定同位素 (Stable Isotopes)

### 同位素分馏 (Isotopic Fractionation)

同位素分馏由质量差异引起的物理化学性质差异导致：

- **平衡分馏** (equilibrium fractionation)：与温度相关
- **动力学分馏** (kinetic fractionation)：与反应速率相关

分馏系数 (fractionation factor)：

$$\alpha_{A-B} = \frac{R_A}{R_B}$$

$\delta$ 值表示相对于标准的千分偏差：

$$\delta (\permil) = \left(\frac{R_{\text{sample}}}{R_{\text{standard}}} - 1\right) \times 1000$$

### 氧同位素 ($\delta^{18}$O)

**标准**：V-SMOW (Vienna Standard Mean Ocean Water)

**应用**：

- **古温度计**：碳酸盐 $\delta^{18}$O 与温度的关系

$$T(°\text{C}) = 16.9 - 4.38(\delta_c - \delta_w) + 0.10(\delta_c - \delta_w)^2$$

- **冰芯记录**：反映古温度和冰量变化
- **水循环示踪**：降水 $\delta^{18}$O 与温度、降水量的关系
- **水-岩相互作用**：高温地质过程

### 碳同位素 ($\delta^{13}$C)

**标准**：V-PDB (Vienna Pee Dee Belemnite)

**分馏机制**：

- **光合作用**：$^{12}$C 优先固定，有机物富轻碳 ($\delta^{13}$C ~ -25‰)
- **C3 vs C4 植物**：C3 植物 $\delta^{13}$C ~ -27‰，C4 植物 ~ -13‰
- **碳酸盐沉淀**：海相碳酸盐 $\delta^{13}$C ~ 0‰

**应用**：碳循环、古海洋化学、食物网追踪

### 硫同位素 ($\delta^{34}$S)

- **标准**：V-CDT (Vienna Canyon Diablo Troilite)
- **硫酸盐还原菌**：产生大的负 $\delta^{34}$S 值
- **应用**：矿床成因、古海洋硫循环、大气污染示踪

---

## 同位素示踪应用 (Isotope Tracing Applications)

### 古气候重建 (Paleoclimate Reconstruction)

| 代用指标 | 同位素体系 | 反映参数 |
|---------|-----------|---------|
| 冰芯 | $\delta^{18}$O, $\delta$D | 古温度、水汽来源 |
| 珊瑚 | $\delta^{18}$O, $\delta^{13}$C | 海表温度、生产力 |
| 石笋 | $\delta^{18}$O, $\delta^{13}$C | 降水、植被变化 |
| 树轮 | $\delta^{13}$C, $\delta^{18}$O | 温度、湿度 |

### 物质来源示踪 (Source Tracing)

- **壳幔物质循环**：Sr-Nd-Pb 同位素体系区分地壳和地幔来源
- **大陆风化**：$\delta^7$Li、$\delta^{44}$Ca 示踪硅酸盐风化速率
- **污染物溯源**：Pb 同位素追踪重金属污染来源

### 地球深部过程 (Deep Earth Processes)

- **地幔不均一性**：洋岛玄武岩 (OIB) 的 Sr-Nd-Hf-Pb 同位素差异
- **俯冲带物质循环**：B、Li、N 同位素示踪俯冲板片脱水和熔融
- **核幔相互作用**：$^{182}$W/$^{184}$W 异常暗示早期地球分异

---

## 分析技术 (Analytical Techniques)

| 技术 | 精度 | 应用 |
|------|------|------|
| TIMS (热电离质谱) | ±0.001‰ (Sr) | 高精度同位素比值 |
| MC-ICP-MS (多接收电感耦合等离子体质谱) | ±0.01‰ | 非传统稳定同位素 |
| LA-MC-ICP-MS (激光剥蚀) | ±0.1‰ | 原位微区分析 |
| SIMS (二次离子质谱) | ±0.1‰ | 极小样品分析 |
| IRMS (同位素比值质谱) | ±0.05‰ | C、N、O、S、H 气体分析 |

---

## 前沿进展 (Recent Advances)

- **非传统稳定同位素** (non-traditional stable isotopes)：Fe、Cu、Zn、Mo、Cr 等金属同位素
- **团簇同位素** (clumped isotopes)：$\Delta_{47}$ 温度计，无需知道水的同位素组成
- **原位分析技术**：飞秒激光剥蚀、SIMS 纳米级分析
- **宇宙化学应用**：陨石和月球样品的同位素分析

---

## 参考与延伸阅读 (References and Further Reading)

1. *Isotope Geochemistry* — W. M. White
2. *Radiogenic Isotope Geology* — A. P. Dickin
3. *Stable Isotope Geochemistry* — J. Hoefs
4. *Geochronology and Thermochronology* — P. W. Reiners et al.
5. *Non-Traditional Stable Isotopes* — F. Z. Teng et al., Reviews in Mineralogy 82 (2017)
