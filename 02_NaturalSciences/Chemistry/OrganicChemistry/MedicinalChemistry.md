---
aliases:
  - 药物化学
  - Medicinal Chemistry
  - Pharmaceutical Chemistry
  - Drug Design
tags:
  - chemistry
  - organic-chemistry
  - medicinal-chemistry
  - drug-design
  - pharmacology
created: 2026-06-28
updated: 2026-06-28
---

# 药物化学 (Medicinal Chemistry)

## 概述 (Overview)

药物化学 (medicinal chemistry) 是研究药物分子的设计、合成、构效关系 (structure-activity relationship, SAR) 及其与生物靶标相互作用的学科。它融合了有机化学 (organic chemistry)、生物化学 (biochemistry)、药理学 (pharmacology) 和计算化学 (computational chemistry)，是新药研发的核心学科。

现代药物化学的目标是发现和优化先导化合物 (lead compounds)，使其具有高效性、选择性和良好的药代动力学性质 (pharmacokinetics)。

---

## 药物设计策略 (Drug Design Strategies)

### 基于结构的药物设计 (Structure-Based Drug Design, SBDD)

SBDD 利用靶标蛋白的三维结构信息指导药物分子设计：

**工作流程**：

1. **靶标结构获取**：X 射线晶体学 (X-ray crystallography)、冷冻电镜 (cryo-EM) 或 NMR 解析蛋白结构
2. **结合位点分析**：识别活性口袋 (binding pocket) 的形状、电荷分布、氢键位点
3. **分子对接** (molecular docking)：预测小分子与蛋白的结合模式
4. **先导化合物优化**：基于结合模式指导结构修饰

**关键工具**：
- AutoDock、Glide、GOLD 等对接软件
- 分子动力学模拟 (molecular dynamics, MD)
- 自由能微扰 (free energy perturbation, FEP)

### 基于配体的药物设计 (Ligand-Based Drug Design, LBDD)

当靶标结构未知时，利用已知活性分子的信息：

- **药效团模型** (pharmacophore modeling)：提取活性分子的共同特征
- **定量构效关系** (QSAR)：建立分子描述符与活性的数学模型
- **分子相似性搜索** (molecular similarity search)：基于指纹或形状的虚拟筛选
- **骨架跃迁** (scaffold hopping)：保持药效团替换核心骨架

### 基于片段的药物发现 (Fragment-Based Drug Discovery, FBDD)

从小分子片段（MW < 300 Da）出发，通过筛选和结构指导拼接 (fragment growing/linking/merging) 构建高亲和力配体：

- 检测方法：热漂移 (thermal shift)、SPR、NMR、X 射线晶体学
- 代表药物：维莫非尼 (vemurafenib，首个 FBDD 上市药物)

---

## 先导化合物优化 (Lead Optimization)

### ADMET 性质优化

ADMET 是药物成药性的关键参数：

| 参数 | 含义 | 优化策略 |
|------|------|---------|
| Absorption | 吸收 | 调节 logP、增加溶解度 |
| Distribution | 分布 | 控制蛋白结合率、血脑屏障穿透 |
| Metabolism | 代谢 | 阻断代谢软位点 (metabolic soft spots) |
| Excretion | 排泄 | 调节肾清除或胆汁排泄 |
| Toxicity | 毒性 | 避免反应性基团 (reactive groups) |

### 类药五规则 (Lipinski's Rule of Five)

判断化合物口服生物利用度的经验规则：

- 分子量 (MW) ≤ 500
- 氢键供体 (HBD) ≤ 5
- 氢键受体 (HBA) ≤ 10
- 脂水分配系数 (logP) ≤ 5
- 违反两条以上规则时，口服吸收可能较差

### 可合成性与化学空间 (Synthetic Accessibility and Chemical Space)

- **药物化学空间** (drug-like chemical space)：满足类药规则的分子集合
- **多样性导向合成** (diversity-oriented synthesis, DOS)：构建结构多样的化合物库
- **天然产物启发** (natural product-inspired)：利用天然产物的结构复杂性

---

## 靶向药物 (Targeted Drugs)

### 激酶抑制剂 (Kinase Inhibitors)

蛋白激酶是最重要的药物靶标家族之一：

| 代次 | 特征 | 代表药物 |
|------|------|---------|
| 第一代 | 竞争性抑制剂 | 伊马替尼 (imatinib) |
| 第二代 | 克服耐药突变 | 达沙替尼 (dasatinib) |
| 第三代 | 靶向特定突变 | 奥希替尼 (osimertinib, T790M) |
| 第四代 | 双重/多重靶点 | 变构抑制剂 |

结合模式分类：
- **I 型**：结合活性构象的 ATP 口袋
- **II 型**：结合 DFG-out 非活性构象
- **III 型**：变构抑制剂 (allosteric inhibitor)
- **IV 型**：共价抑制剂 (covalent inhibitor)

### PROTAC (Proteolysis-Targeting Chimera)

PROTAC 是一种双功能分子，利用泛素-蛋白酶体系统 (ubiquitin-proteasome system) 降解靶标蛋白：

$$\text{PROTAC} = \text{靶标配体} - \text{连接子} - \text{E3 连接酶配体}$$

**优势**：
- 催化量起效（一个 PROTAC 分子可降解多个靶标蛋白）
- 可靶向"不可成药"靶标 (undruggable targets)
- 克服传统抑制剂的耐药性

**代表分子**：ARV-110（靶向 AR）、ARV-471（靶向 ER）

### 分子胶 (Molecular Glue)

诱导蛋白-蛋白相互作用 (protein-protein interaction, PPI) 的小分子：

- 来那度胺 (lenalidomide)：诱导 CRBN 与 IKZF1/3 结合
- 环孢菌素 A (cyclosporin A)：诱导 cyclophilin 与 calcineurin 结合

---

## 药物合成策略 (Drug Synthesis Strategies)

### 逆合成分析 (Retrosynthetic Analysis)

Corey 提出的逆合成分析方法：

1. **目标分子** → **合成子** (synthon)：识别断键位点
2. **合成子** → **合成等价物** (synthetic equivalent)：选择合适的试剂
3. 迭代至商业化可得的起始原料

### 不对称合成 (Asymmetric Synthesis)

手性药物的对映体可能具有不同药效：

- **手性催化** (chiral catalysis)：手性金属催化剂、有机催化剂
- **酶催化** (enzymatic catalysis)：转氨酶、酮还原酶
- **手性拆分** (chiral resolution)：结晶拆分、色谱分离

### 流动化学 (Flow Chemistry)

连续流动合成在药物研发中的应用：

- 传热传质效率高
- 安全性好（小体积反应）
- 易于放大 (scale-up)
- 代表：流动氢化、光化学反应

---

## 2025-2026 前沿进展 (Recent Advances)

### AI 药物发现 (AI-Driven Drug Discovery)

人工智能正在重塑药物研发流程：

- **靶标发现**：知识图谱 (knowledge graph) 和因果推断识别新靶标
- **虚拟筛选**：深度学习模型 (deep learning) 预测分子活性
- **ADMET 预测**：图神经网络 (GNN) 预测药代动力学性质
- **临床试验优化**：AI 辅助患者分层和终点预测

### 分子生成 (Molecular Generation)

生成式 AI 在分子设计中的应用：

- **变分自编码器** (VAE)：学习分子的潜在表示空间
- **生成对抗网络** (GAN)：生成具有特定性质的分子
- **扩散模型** (diffusion models)：逐步去噪生成分子结构
- **大语言模型** (LLM)：基于 Transformer 的分子生成

代表公司：Recursion、Insilico Medicine、Exscientia

### 靶向蛋白降解新方向

- **分子胶** (molecular glue) 的理性设计
- **LYTAC**：靶向溶酶体降解细胞外蛋白
- **AUTAC**：利用自噬途径降解蛋白
- **核糖体靶向嵌合体** (ribosome-targeting chimeras)

---

## 参考与延伸阅读 (References and Further Reading)

1. *An Introduction to Medicinal Chemistry* — G. L. Patrick
2. *Drug Design and Discovery* — S. E. Furness
3. *The Practice of Medicinal Chemistry* — C. G. Wermuth et al.
4. *PROTAC-Targeted Protein Degradation* — C. M. Crews, Science 367, 1314 (2020)
5. *Artificial Intelligence in Drug Discovery* — T. L. Blundell et al., Nature Reviews Drug Discovery 21, 1000 (2022)
