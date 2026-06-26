---
aliases: [DrugDesign, 药物设计, 合理药物设计, RationalDrugDesign]
tags: ['09_MedicineAndHealth', 'Pharmacy', 'MedicinalChemistry', 'DrugDiscovery']
created: 2026-05-17
updated: 2026-06-27
---

# 药物设计

药物设计（Drug Design）是发现与优化先导化合物以开发新药的跨学科过程，融合药物化学（Medicinal Chemistry）、分子生物学（Molecular Biology）、结构生物学（Structural Biology）与计算科学（Computational Science）。药物发现从确定疾病相关的生物靶点开始，经靶点验证、先导化合物发现、先导化合物优化、临床前研究到临床试验，整个过程平均耗时 10-15 年，耗资超过 10 亿美元。

## 药物发现流程

```mermaid
graph TD
    A[疾病生物学研究] --> B[靶点识别与验证]
    B --> C{先导化合物发现}
    C --> D[高通量筛选<br/>HTS]
    C --> E[基于片段筛选<br/>FBDD]
    C --> F[虚拟筛选<br/>Virtual Screening]
    C --> G[天然产物]
    C --> H[老药新用<br/>Drug Repurposing]
    D --> I[先导化合物]
    E --> I
    F --> I
    G --> I
    H --> I
    I --> J[先导化合物优化<br/>Lead Optimization]
    J --> K[临床前研究<br/>ADME/Tox]
    K --> L[I 期临床<br/>安全性]
    L --> M[II 期临床<br/>有效性]
    M --> N[III 期临床<br/>大规模验证]
    N --> O[FDA/EMA 审批]
    O --> P[上市与 IV 期]
```

## 靶点识别与验证 （Target Identification & Validation）

生物靶点通常是蛋白质（酶、受体、离子通道、转运体）或核酸。现代靶点发现技术包括：

| 技术类型 | 方法 | 应用场景 |
|:---|:---|:---|
| 基因组学 | GWAS、CRISPR 筛选 | 基因-疾病关联 |
| 蛋白质组学 | 质谱、酵母双杂交 | 蛋白-蛋白相互作用 |
| 转录组学 | RNA-seq、单细胞测序 | 差异表达分析 |
| 化学生物学 | 亲和色谱、热位移分析 | 小分子-靶点结合 |
| 计算预测 | AlphaFold、同源建模 | 靶点三维结构 |

## 先导化合物发现 （Lead Discovery）

### 高通量筛选 （High-Throughput Screening, HTS）

使用自动化机器人平台，在 384/1536 孔板中对数十万至数百万化合物进行活性测试。典型流程：

1. 化合物库准备（多样性库 vs 定向库）
2. 检测方法开发（荧光、发光、FRET 等）
3. 初筛 → 复筛 → 剂量-响应确认
4. hit 判定标准：$IC_{50} < 10\,\mu\text{M}$，选择性 > 10 倍

### 基于片段的药物设计 （Fragment-Based Drug Design, FBDD）

筛选低分子量片段库（MW < 300 Da），通过生物物理方法（SPR、NMR、X-ray）检测弱结合片段，再通过连接（Linking）、生长（Growing）或合并（Merging）策略优化为先导化合物。

### 虚拟筛选 （Virtual Screening）

- **基于配体的虚拟筛选**（LBVS）：相似性搜索、药效团匹配、QSAR
- **基于结构的虚拟筛选**（SBVS）：分子对接（Molecular Docking）

## 合理药物设计 （Rational Drug Design）

### 基于结构的药物设计 （Structure-Based Drug Design, SBDD）

利用 X 射线晶体学、NMR 光谱或冷冻电镜（Cryo-EM）解析靶点三维结构，通过分子对接、分子动力学模拟和结合自由能计算指导分子设计。

$$ \Delta G_{\text{bind}} = RT \ln K_d = \Delta H - T\Delta S $$

结合自由能分解：

$$ \Delta G_{\text{bind}} = \Delta G_{\text{vdW}} + \Delta G_{\text{elec}} + \Delta G_{\text{solv}} + \Delta G_{\text{conf}} $$

### 基于配体的药物设计 （Ligand-Based Drug Design, LBDD）

在没有靶点三维结构时，从已知活性分子出发：

- **药效团模型**（Pharmacophore）：关键化学特征的空间排列
- **定量构效关系**（QSAR）：$ \text{活性} = f(\text{分子描述符}) $

$$ \log(1/IC_{50}) = a \cdot \log P + b \cdot \sigma + c \cdot E_s + d $$

## 计算机辅助药物设计 （CADD）

| 方法 | 输入 | 输出 | 典型软件 |
|:---|:---|:---|:---|
| 分子对接 | 靶点结构 + 配体 | 结合模式和打分 | AutoDock, Glide, Gold |
| 分子动力学 | 蛋白-配体复合物 | 轨迹和自由能 | AMBER, GROMACS, NAMD |
| 自由能微扰 | 配体系列 | $\Delta\Delta G_{\text{bind}}$ | FEP+, TIES |
| 药效团搜索 | 活性分子集合 | 三维药效团 | MOE, Phase, LigandScout |
| 生成模型 | SMILES/分子图 | 新分子结构 | REINVENT, MolDQN |

### 分子动力学模拟 （Molecular Dynamics, MD）

牛顿运动方程数值求解：

$$ m_i \frac{d^2 \mathbf{r}_i}{dt^2} = \mathbf{F}_i = -\nabla_i V(\mathbf{r}_1, \dots, \mathbf{r}_N) $$

力场（Force Field）函数形式：

$$ V = \sum_{\text{bonds}} k_b(b-b_0)^2 + \sum_{\text{angles}} k_\theta(\theta-\theta_0)^2 + \sum_{\text{dihedrals}} V_n[1+\cos(n\phi-\gamma)] + \sum_{i<j} \left( \frac{q_i q_j}{4\pi\epsilon_0 r_{ij}} + \frac{A_{ij}}{r_{ij}^{12}} - \frac{B_{ij}}{r_{ij}^6} \right) $$

## ADME/Tox 预测

早期预测药代动力学和毒性可大幅降低后期临床失败率：

| 参数 | 含义 | 理想范围 |
|:---|:---|:---:|
| $ \log P $ | 脂水分配系数 | 1-3 |
| MW | 分子量 | < 500 Da |
| HBD | 氢键供体数 | < 5 |
| HBA | 氢键受体数 | < 10 |
| $ \log D_{7.4} $ | pH 7.4 分配系数 | 1-3 |
| PSA | 极性表面积 | < 140 Å² |
| Solubility | 水溶性 | > $ 60\,\mu\text{g/mL} $ |

### Lipinski 五规则 （Rule of Five）

口服药物的类药性筛选标准：

- 分子量 ≤ 500
- log P ≤ 5
- 氢键供体 ≤ 5
- 氢键受体 ≤ 10
- 可旋转键 ≤ 10（补充规则）

## 药物代谢动力学 （Pharmacokinetics, PK）

PK 描述药物在体内的吸收（Absorption）、分布（Distribution）、代谢（Metabolism）和排泄（Excretion），即 ADME 过程。

### 关键 PK 参数

| 参数 | 符号 | 含义 | 理想范围 |
|:---|:---:|:---|:---:|
| 生物利用度 | $F$ | 口服后进入体循环的比例 | $> 30\%$ |
| 分布容积 | $V_d$ | 药物在体内理论的分布体积 | 因靶点而异 |
| 清除率 | $CL$ | 单位时间清除药物的血浆体积 | 与器官功能相关 |
| 半衰期 | $t_{1/2}$ | 血浆浓度降低一半所需时间 | 8-24 h |
| 曲线下面积 | $AUC$ | 药物暴露量的积分指标 | 越大越好 |
| 表观分布 | $V_{ss}$ | 稳态分布容积 | 反映组织结合 |

### 房室模型 （Compartment Model）

一室模型：

$$ C(t) = C_0 e^{-kt}, \quad k = \frac{CL}{V_d} $$

二室模型：

$$ C(t) = A e^{-\alpha t} + B e^{-\beta t} $$

## 药物安全性评价

毒性是药物临床失败的主要原因之一。主要毒理学评估包括：

| 毒性类型 | 评估方法 | 关键指标 |
|:---|:---|:---|
| hERG 抑制 | 膜片钳、结合实验 | $IC_{50} > 10\,\mu\text{M}$ |
| 肝毒性 | 肝细胞实验、ALT/AST | 无显著升高 |
| 遗传毒性 | Ames 试验、微核试验 | 阴性 |
| 心脏毒性 | 心电图、QT 间期 | QTc 延长 < 10 ms |
| 致癌性 | 两年啮齿类实验 | 肿瘤发生率不变 |

## 药物-靶点相互作用动力学

### 结合动力学

$$ \text{药物} + \text{靶点} \xrightleftharpoons[k_{\text{off}}]{k_{\text{on}}} \text{复合物} $$

$$ K_d = \frac{k_{\text{off}}}{k_{\text{on}}} = \frac{[\text{药物}][\text{靶点}]}{[\text{复合物}]} $$

### Residence Time

药物-靶点复合物的停留时间（Residence Time, $\tau$）是药效持续性的关键指标：

$$ \tau = \frac{1}{k_{\text{off}}} $$

延长的停留时间通常与更好的体内药效相关。

## 计算机辅助药物设计的统计学基础

### 分子描述符

分子描述符是将化学结构转换为数值特征的计算方法：

- **拓扑描述符**：Wiener 指数、分子连接性指数
- **电子描述符**：HOMO/LUMO 能级、偶极矩
- **疏水描述符**：logP、logD
- **空间描述符**：分子体积、表面积、椭圆度
- **药效团描述符**：氢键位点、电荷中心分布

### 机器学习模型评估

| 指标 | 公式 | 含义 |
|:---|:---|:---|
| $R^2$ | $1 - \frac{\sum(y_i-\hat{y}_i)^2}{\sum(y_i-\bar{y})^2}$ | 拟合优度 |
| RMSE | $\sqrt{\frac{1}{n}\sum(y_i-\hat{y}_i)^2}$ | 均方根误差 |
| MAE | $\frac{1}{n}\sum|y_i-\hat{y}_i|$ | 平均绝对误差 |
| AUC-ROC | 积分 ROC 曲线下面积 | 分类能力 |
| $Q^2$ | 交叉验证的 $R^2$ | 模型预测能力 |

## 案例：COVID-19 抗病毒药物设计

SARS-CoV-2 主要蛋白酶（M$^{\text{pro}}$）是抗 COVID-19 药物设计的关键靶点：

1. **靶点选择**：M$^{\text{pro}}$ 的晶体结构（PDB: 6LU7）在疫情初期即被解析
2. **虚拟筛选**：对已有药物库进行分子对接，发现 remdesivir 和 lopinavir 等候选
3. **共价抑制剂设计**：基于 M$^{\text{pro}}$ 的 Cys145 活性位点设计共价结合分子
4. **临床转化**：Paxlovid（nirmatrelvir + ritonavir）从发现到 EUA 仅用约 18 个月

## AI 在药物设计中的应用

- **蛋白质结构预测**：AlphaFold2/3 实现原子级精度
- **分子生成**：GANs、VAE、扩散模型生成新型分子结构
- **活性预测**：图神经网络（GNN）预测分子性质
- **逆向合成**：AI 规划有机合成路线
- **临床试验预测**：自然语言处理分析临床试验数据

```mermaid
graph LR
    A[深度学习] --> B[分子表示学习]
    A --> C[生成模型]
    A --> D[预测模型]
    B --> E[SMILES/分子图编码]
    C --> F[新分子设计]
    C --> G[逆合成分析]
    D --> H[ADME 预测]
    D --> I[毒性预测]
    D --> J[靶点亲和力预测]
```

## AI 药物发现最新进展（2024-2026）

### AlphaFold 3 与蛋白质结构预测

| 模型 | 开发商 | 发布时间 | 核心能力 |
|------|--------|---------|---------|
| **AlphaFold 3** | Google DeepMind | 2024.05 | 预测蛋白质、DNA、RNA、小分子等所有生命分子结构 |
| **AlphaFold 3 开源** | Google DeepMind | 2024.11 | 发布推理代码、模型权重和按需服务器 |
| **Boltz-1** | MIT | 2024.11 | 首个达到 AlphaFold 3 精度的开源模型 |
| **Protenix-v1** | ByteDance | 2026.02 | 全面复现 AlphaFold 3，开源代码 |
| **RhoFold+** | 社区 | 2024.11 | RNA 3D 结构预测深度学习框架 |

**AlphaFold 3 核心突破**：
- 从蛋白质扩展到所有生命分子（蛋白质、DNA、RNA、小分子、离子）
- 使用扩散模型（Diffusion Model）替代 AlphaFold 2 的结构模块
- 预测精度比 AlphaFold 2 提升 50% 以上

### AI 驱动的药物发现平台

| 平台 | 公司 | 核心技术 | 代表成果 |
|------|------|---------|---------|
| **Insilico Medicine** | Insilico | 生成化学 + 靶点发现 | 全球首个 AI 发现药物进入 II 期临床 |
| **Recursion Pharmaceuticals** | Recursion | 细胞图像分析 + 大规模表型筛选 | 收购 Cyclica 和 Valence Discovery |
| **Exscientia** | Exscientia | 精密药物设计 | 首个 AI 设计药物进入人体临床 |
| **Isomorphic Labs** | Google DeepMind | AlphaFold + 药物发现 | 与 Eli Lilly、Novartis 合作 |
| **AbSci** | AbSci | 从头设计抗体 | 使用生成式 AI 设计新抗体 |

### AI 药物发现关键里程碑

| 时间 | 事件 | 意义 |
|------|------|------|
| 2024.05 | AlphaFold 3 发布 | 扩展到所有生命分子结构预测 |
| 2024.11 | AlphaFold 3 开源 | 代码和权重公开，加速研究 |
| 2024.11 | Boltz-1 发布 | 首个开源 AlphaFold 3 级别模型 |
| 2025 | Insilico Medicine II 期临床 | 全球首个 AI 发现药物进入关键临床阶段 |
| 2026.02 | ByteDance Protenix-v1 | 字节跳动进入 AI 药物发现领域 |

### mRNA 疗法与疫苗技术

| 技术 | 应用 | 代表产品 | 状态 |
|------|------|---------|------|
| **mRNA 疫苗** | 传染病预防 | Comirnaty (Pfizer), Spikevax (Moderna) | 已获批 |
| **mRNA 癌症疫苗** | 个性化癌症治疗 | mRNA-4157 (Moderna + Merck) | III 期临床 |
| **mRNA 蛋白替代** | 罕见病治疗 | mRNA-3927 (Moderna) | 临床试验 |
| **自扩增 mRNA** | 降低剂量 | ARCT-154 (Arcturus) | 已获批（日本） |

**mRNA 技术优势**：
- 开发周期短：从序列到疫苗仅需数周
- 易于修改：快速应对病毒变异
- 无基因组整合风险：比 DNA 疗法更安全
- 可编码任何蛋白质：应用范围广泛

### 基因编辑疗法最新进展

| 疗法 | 技术 | 适应症 | 状态 |
|------|------|--------|------|
| **Casgevy** | CRISPR-Cas9 | 镰状细胞病、β-地中海贫血 | 2023年获批（全球首个） |
| **Lyfgenia** | 慢病毒载体 | 镰状细胞病 | 2023年获批 |
| **Base Editing 疗法** | 碱基编辑 | 高胆固醇血症 | 临床试验 |
| **Prime Editing 疗法** | 先导编辑 | 多种遗传病 | 临床前/早期临床 |

**CRISPR 技术演进**：
$$
\text{CRISPR-Cas9} \rightarrow \text{Base Editing} \rightarrow \text{Prime Editing} \rightarrow \text{Epigenome Editing}
$$

### GLP-1 受体激动剂革命

| 药物 | 公司 | 适应症 | 2024-2026 进展 |
|------|------|--------|---------------|
| **司美格鲁肽 (Semaglutide)** | Novo Nordisk | 糖尿病、肥胖 | 心血管获益证实，肾病适应症获批 |
| **替尔泊肽 (Tirzepatide)** | Eli Lilly | 糖尿病、肥胖 | 双靶点（GLP-1/GIP），减重效果更优 |
| **口服 GLP-1** | 多家公司 | 糖尿病、肥胖 | 口服制剂开发中 |
| **Survodutide** | Boehringer Ingelheim | 肥胖、MASH | GLP-1/胰高血糖素双靶点 |

**GLP-1 药物市场爆发**：
- 2024年全球销售额超过 500 亿美元
- 适应症从糖尿病扩展到肥胖、心血管疾病、肾病、MASH
- 被《Science》评为 2023 年度突破

### CAR-T 细胞疗法进展

| 产品 | 公司 | 适应症 | 最新进展 |
|------|------|--------|---------|
| **奕凯达 (阿基仑赛)** | 复星凯特 | 大 B 细胞淋巴瘤 | 中国首个 CAR-T 产品 |
| **倍诺达 (瑞基奥仑赛)** | 药明巨诺 | 大 B 细胞淋巴瘤 | 中国第二个 CAR-T |
| **Abecma** | BMS | 多发性骨髓瘤 | BCMA 靶点 |
| **Carvykti** | J&J | 多发性骨髓瘤 | BCMA 靶点，早期线使用 |
| **通用型 CAR-T** | 多家公司 | 多种血液肿瘤 | 异体 CAR-T，降低成本 |

## 药物设计面临的挑战

- **靶点可药性**（Druggability）：并非所有蛋白都是好靶点
- **选择性**（Selectivity）：避免脱靶效应和副作用
- **耐药性**（Drug Resistance）：突变导致药物失效
- **血脑屏障**（BBB）：中枢神经系统药物需要特殊设计
- **临床转化率**：从靶点到上市的成功率不足 10%

## 相关条目

- [[LeadDiscovery|先导化合物发现]]
- [[CADD|计算机辅助药物设计]]
- [[QSAR|定量构效关系]]
- [[MolecularDocking|分子对接]]
- [[ADMETox|ADME 与毒性预测]]
- [[Pharmacokinetics|药物代谢动力学]]
- [[MedicinalChemistry|药物化学]]
