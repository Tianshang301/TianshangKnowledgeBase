---
aliases: [ReactionEngineering]
tags: ['ChemicalAndPharmaceuticalEngineering', 'ChemicalEngineering', 'ReactionEngineering']
created: 2026-05-16
updated: 2026-05-16
---

# 化学反应工程

## 定义
化学反应工程是研究工业规模化学反应过程的规律和反应器设计的学科。是化学工程的核心分支。

## 核心内容

### 反应动力学

**反应速率**：

$$r = kC_A^n, \quad k = A\exp\left(-\frac{E_a}{RT}\right)$$

**反应级数**：
- 零级：$r = k$
- 一级：$r = kC_A$
- 二级：$r = kC_A^2$

**转化率**：$X_A = \frac{C_{A0}-C_A}{C_{A0}}$

### 反应器类型

**间歇反应器（BR）**：
- 操作特点：分批操作，时间序列
- 设计方程：$t = C_{A0}\int_0^{X_A}\frac{dX_A}{-r_A}$

**连续搅拌反应器（CSTR）**：
- 操作特点：连续进料，稳态操作
- 设计方程：$V = \frac{F_{A0}X_A}{-r_A}$

**管式反应器（PFR）**：
- 操作特点：活塞流，沿管长转化
- 设计方程：$V = F_{A0}\int_0^{X_A}\frac{dX_A}{-r_A}$

**反应器对比**

| 特性 | 间歇（BR） | CSTR | PFR |
|------|-----------|------|-----|
| 操作方式 | 分批 | 连续 | 连续 |
| 浓度分布 | 随时间变化 | 均匀（出口浓度） | 沿管长递减 |
| 停留时间分布 | 单一 | 宽（全混流） | 窄（活塞流） |
| 转化率/体积 | — | 最低 | 最高 |
| 适用场合 | 小批量、多品种 | 液相、均相 | 气相、大量生产 |

### 反应器设计

**设计要点**：
- 反应器体积确定
- 传热设计（移热/供热）
- 搅拌与混合
- 材料选择

**停留时间分布**：
- $E(t)$ 函数：出口年龄分布
- $F(t)$ 函数：累积分布
- 平均停留时间：$\bar{t} = \int_0^\infty tE(t)dt$

**Damköhler 数**：$Da = \frac{-r_A V}{F_{A0}}$，表征反应速率与对流传输速率的比值
- $Da \ll 1$：反应器受动力学控制
- $Da \gg 1$：接近平衡

**空速**：$SV = \frac{v_0}{V}$，单位时间处理物料体积与反应器体积之比

### 气固催化反应

**反应步骤**：
1. 外扩散：反应物从气相到催化剂外表面
2. 内扩散：反应物进入催化剂孔道
3. 表面反应：在活性位上反应
4. 内扩散：产物扩散出孔道
5. 外扩散：产物扩散到气相

**效率因子**：$\eta = \frac{实际反应速率}{无内扩散时反应速率}$

## 经典教材
- 陈甘棠《化学反应工程》
- Levenspiel《Chemical Reaction Engineering》
- Fogler《Elements of Chemical Reaction Engineering》
- Froment《Chemical Reactor Analysis and Design》

## 主要应用领域
- 石油炼制（催化裂化）
- 合成氨工业
- 聚合反应工程
- 生化反应工程
- 电化学反应工程
- 环境催化

## 参考资料

- 陈甘棠, 《化学反应工程》, 化学工业出版社
- H. Scott Fogler, *Elements of Chemical Reaction Engineering*, Prentice Hall
- Octave Levenspiel, *Chemical Reaction Engineering*, Wiley

## 相关条目

- [[04_EngineeringAndTechnology/ChemicalAndPharmaceuticalEngineering/ChemicalEngineering/INDEX|ChemicalEngineering]]
- ChemicalKinetics
- Catalysis
- ProcessControl

