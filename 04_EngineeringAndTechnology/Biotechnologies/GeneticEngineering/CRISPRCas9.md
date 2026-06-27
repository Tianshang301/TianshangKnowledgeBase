---
aliases: [CRISPRCas9]
tags: ['Biotechnologies', 'GeneticEngineering', 'CRISPRCas9']
created: 2026-05-16
updated: 2026-05-16
---

# CRISPR-Cas9基因编辑

## 定义
CRISPR-Cas9是一种革命性的基因编辑技术，利用 RNA 引导的核酸酶对基因组进行精确修改。

## 核心内容

### CRISPR 系统原理

**CRISPR 序列**：Clustered Regularly Interspaced Short Palindromic Repeats（成簇的规律间隔短回文重复序列）

**Cas9蛋白**：具有 DNA 切割活性的核酸酶

**sgRNA**：单向导 RNA，由 crRNA 和 tracrRNA 融合而成

**工作原理**：
1. sgRNA 与目标 DNA 互补配对
2. Cas9蛋白切割目标 DNA 双链
3. 细胞修复机制修复断裂

### 基因编辑策略

| 策略 | 修复机制 | 模板需求 | 产物 | 效率 | 应用 |
|:---|:---|:---:|:---|:---:|:---|
| 基因敲除 | NHEJ | 无 | 插入/缺失 | 高 | 基因功能丧失 |
| 基因敲入 | HDR | 供体模板 | 精确序列插入 | 低–中 | 点突变、标签 |
| CRISPRi | dCas9+抑制域 | 无 | 转录抑制 | 高 | 基因沉默 |
| CRISPRa | dCas9+激活域 | 无 | 转录激活 | 中–高 | 基因过表达 |

**基因敲除**：
- NHEJ（非同源末端连接）→产生插入/缺失突变
- 导致移码突变→基因失活

**基因敲入**：
- HDR（同源定向修复）
- 提供供体模板
- 精确插入目标序列

**基因调控**：
- dCas9（死亡 Cas9）：失去切割活性
- CRISPRi：基因沉默
- CRISPRa：基因激活

### sgRNA 设计

**靶序列选择**：
- 20bp 目标序列
- PAM 序列：NGG（SpCas9）
- 脱靶预测

**靶向效率评分**：
$$S = w_{GC} \cdot f(G\%) + w_{pos} \cdot \sum_{i} p_i$$

其中 $f(G\%)$ 为 GC 含量评分（40–60%最优），$p_i$ 为位置依赖性权重因子。

| 脱靶类型 | 错配容忍度 | 风险评估 | 检测方法 |
|:---|:---:|:---|:---|
| 种子区错配（8–12 bp 近 PAM） | 低 | 高 | GUIDE-seq |
| 远端错配（>12 bp 离 PAM） | 高 | 中低 | CIRCLE-seq |
| PAM 远端突出 | 高 | 低 | Digenome-seq |

**设计工具**：
- Benchling
- CHOPCHOP
- CRISPOR

### 递送方法

**物理方法**：
- 显微注射
- 电穿孔
- 基因枪

**化学方法**：
- 脂质体
- 聚合物纳米颗粒
- 病毒载体（AAV、慢病毒）

### 脱靶效应

**检测方法**：
- GUIDE-seq
- CIRCLE-seq
- Digenome-seq

**降低脱靶**：
- 优化 sgRNA
- 使用高保真 Cas9变体
- 控制递送剂量

### 应用

**疾病治疗**：
- 镰刀型细胞贫血症
- β-地中海贫血
- 肿瘤免疫治疗

**农业应用**：
- 抗病作物
- 高产品种
- 营养强化

## 经典教材
- 《CRISPR-Cas9基因编辑技术》
- Doudna《A Crack in Creation》
- Jinek《CRISPR-Cas9: A Tutorial》
- 《基因编辑技术与应用》

## 主要应用领域
- 基因功能研究
- 疾病模型构建
- 基因治疗
- 作物育种
- 基因驱动
- 合成生物学

## 相关条目

- [[02_NaturalSciences/Biology/MolecularBiology/INDEX|MolecularBiology]]
- [[02_NaturalSciences/Biology/Genetics/INDEX|Genetics]]
- [[04_EngineeringAndTechnology/Biotechnologies/BiomedicalEngineering/INDEX|BiomedicalEngineering]]
- Bioethics
