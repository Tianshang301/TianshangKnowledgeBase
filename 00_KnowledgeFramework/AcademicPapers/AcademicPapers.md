---
aliases: [AcademicPapers]
tags: ['AcademicPapers', 'AcademicPapers']
---

# 学术论文写作指南

## 一、论文结构：IMRaD范式

学术论文遵循标准化的 **IMRaD** 结构，即引言（Introduction）、方法（Methods）、结果（Results）和讨论（Discussion）：

| 部分 | 功能 | 核心问题 |
|------|------|---------|
| 引言 | 确立研究背景与问题 | 为什么做这项研究？ |
| 方法 | 描述研究设计 | 如何完成研究？ |
| 结果 | 呈现研究发现 | 发现了什么？ |
| 讨论 | 解释结果含义 | 结果意味着什么？ |
| 结论 | 总结与展望 | 贡献与未来方向 |

### 1.1 标题与摘要

**标题** 应简洁、准确、信息丰富，通常控制在 10–20 字。推荐使用 **描述性标题** 或 **主副标题** 格式。

**摘要类型对比**：

| 类型 | 特征 | 适用场景 |
|------|------|---------|
| 非结构化摘要 | 一段式叙述 | 人文社科 |
| 结构化摘要 | 分节：目的、方法、结果、结论 | 生物医学、自然科学 |
| 图形化摘要 | 图示核心发现 | 高影响力期刊 |

**关键词选取原则**：选取 3–6 个核心术语，涵盖研究领域、方法、对象和结果。推荐使用 MeSH（医学主题词表）或领域标准词表。

### 1.2 引言：漏斗结构

引言采用 **倒三角（漏斗）结构**：

1. **宽泛背景**：领域大背景与重要性
2. **具体问题**：现有研究的不足与局限
3. **研究缺口**：明确指出 Gap
4. **研究贡献**：本文如何填补缺口
5. **路线图**：论文组织结构的预览

贡献陈述应具体可验证，避免模糊表述。例如："本文首次提出基于 Transformer 的 X 方法，在 Y 数据集上取得 SOTA 性能"。

### 1.3 文献综述

**系统性综述方法论**：

$$ \text{PRISMA 流程} = \text{识别} \rightarrow \text{筛选} \rightarrow \text{合格性评估} \rightarrow \text{纳入} $$

关键步骤：
- 确定检索策略（数据库、关键词、布尔逻辑）
- 设定纳入/排除标准
- 质量评估（Cochrane Risk of Bias, ROBIS）
- 数据提取与综合

**文献管理工具对比**：

| 工具 | 类型 | 优点 | 缺点 |
|------|------|------|------|
| Zotero | 开源 | 浏览器插件、免费、标签系统 | 存储空间有限 |
| EndNote | 商业 | Word 集成强、文献库大 | 价格高、学习曲线陡 |
| Mendeley | 免费+付费 | PDF 管理、社交网络、标注 | 同步慢、云存储有限 |
| JabRef | 开源 | Java 跨平台、BibTeX 原生 | 界面较旧 |
| Citavi | 商业 | 知识管理、任务规划 | 仅 Windows、价格高 |

## 二、方法部分

### 2.1 可重复性要求

方法部分必须提供足够细节，使独立研究者能够复现研究：

- 明确指出数据来源与采集方式
- 详细描述实验设备、软件版本、参数设置
- 开源代码与数据（提供 GitHub 或 Zenodo 链接）

### 2.2 统计方法

$$ \text{p-value} = P(\text{观测数据} \mid H_0 \text{为真}) $$

$$ \text{效应量 Cohen's } d = \frac{\bar{x}_1 - \bar{x}_2}{s_{\text{pooled}}} $$

| 统计概念 | 描述 | 报告要求 |
|---------|------|---------|
| p 值 | 显著性概率 | 精确值（非 p<0.05） |
| 效应量 | 差异/关联大小 | Cohen's d, η², OR |
| 置信区间 | 参数估计范围 | 95% CI 上下界 |
| 统计功效 | 检测效应能力 | > 0.80 |

### 2.3 实验设置

- 数据集划分（训练/验证/测试比例）
- 超参数调优方法（网格搜索、贝叶斯优化）
- 基线方法选择（最先进方法对比）
- 硬件环境（CPU/GPU 型号、内存）

## 三、结果呈现

### 3.1 图表选择

| 数据类型 | 推荐可视化 | 说明 |
|---------|-----------|------|
| 分类对比 | 柱状图 | 组间比较 |
| 趋势变化 | 折线图 | 时间序列、收敛曲线 |
| 分布特征 | 箱线图/直方图 | 数据分布与离群值 |
| 相关性 | 散点图 | 两变量关系 |
| 混淆矩阵 | 热力图 | 分类性能细节 |

### 3.2 统计报告规范

结果报告应遵循 APA 或 AMA 规范：

$$ t(28) = 2.45, p = 0.021, d = 0.89, 95\%\ \text{CI}\ [0.12, 1.66] $$

- 避免仅用星号表示显著性
- 报告精确 p 值（p = .003 而非 p < .01）
- 同时报告效应量与置信区间

## 四、讨论部分

### 4.1 讨论结构

1. **重申主要发现**（一句话概括）
2. **结果解释**：与假设对比，解释意外结果
3. **与文献对比**：支持或矛盾之处
4. **局限性**：方法局限、样本局限、泛化性
5. **未来工作**：后续研究方向

### 4.2 常见错误

- 过度解释结果（超出数据支持范围）
- 忽略负面结果
- 未充分讨论局限性
- 未来工作过于笼统

## 五、结论

结论应回答引言中提出的研究问题，总结 3–5 个核心贡献，并指出更广泛的影响。避免在结论中引入新数据或新论点。

## 六、参考文献与引用格式

### 6.1 主要引用格式对比

| 格式 | 学科 | 文中引用 | 文献列表示例 |
|------|------|---------|------------|
| APA 7th | 心理学、教育学 | (Author, 2020) | Author, A. (2020). *Title*. Publisher. |
| IEEE | 工程、计算机 | [1] | [1] A. Author, "Title," *Journal*, vol. 1, pp. 1–10, 2020. |
| MLA 9th | 人文学科 | (Author 45) | Author, A. *Title*. Publisher, 2020. |
| Chicago NB | 历史、艺术 | ¹ Author, *Title* (Publisher, 2020), 45. | Author, A. *Title*. Publisher, 2020. |
| GB/T 7714 | 中文期刊 | [1] | [1] 作者. 题名[J]. 刊名, 2020, 1(1): 1–10. |

### 6.2 引用管理最佳实践

- 使用文献管理工具（Zotero/EndNote/Mendeley）
- 统一引用风格（避免混合格式）
- 注意 DOI 的持久链接
- 核对参考文献的完整性

## 七、同行评审

同行评审是学术出版质量控制的基石：

| 评审类型 | 定义 | 优点 | 缺点 |
|---------|------|------|------|
| 单盲 | 审稿人匿名 | 审稿人可自由批评 | 可能偏袒/偏见 |
| 双盲 | 双方均匿名 | 减少偏见 | 难以完全匿名 |
| 开放评审 | 双方互知 | 透明、问责 | 可能影响评审 |
| 发表后评审 | 出版后公开评议 | 持续改进 | 缺少正式标准 |

## 八、期刊选择

### 8.1 关键指标

$$ \text{影响因子 (IF)} = \frac{\text{某年引用前两年文章数}}{\text{前两年可引用文章数}} $$

| 指标 | 含义 | 来源 |
|------|------|------|
| JCR 影响因子 | 期刊平均被引次数 | Web of Science |
| 中科院分区 | 期刊等级（1–4 区） | 中科院文献中心 |
| Scopus CiteScore | 期刊影响力 | Scopus |
| h-index | 期刊/学者综合指标 | Google Scholar |

### 8.2 期刊 vs 会议发表

| 维度 | 期刊论文 | 会议论文 |
|------|---------|---------|
| 审稿周期 | 3–12 个月 | 1–6 个月 |
| 篇幅 | 8–25 页 | 4–8 页 |
| 认可度 | 长周期影响力 | 快速传播 |
| 计算机领域 | 次要 | 主要（CCF 推荐） |
| 人文社科 | 主要 | 次要 |

## 九、LaTeX 论文排版

### 9.1 基本模板

```latex
\documentclass[12pt,a4paper]{article}

% 常用宏包
\usepackage{amsmath,amssymb}  % 数学公式
\usepackage{graphicx}         % 图片插入
\usepackage{natbib}           % 参考文献
\usepackage[hidelinks]{hyperref} % 超链接
\usepackage{booktabs}         % 表格美化
\usepackage{geometry}         % 页面设置
\geometry{margin=2.5cm}
```

### 9.2 常用宏包功能

| 宏包 | 功能 |
|------|------|
| amsmath / amssymb | 高级数学排版、扩展符号集 |
| graphicx | 图形插入与缩放 |
| natbib / biblatex | 参考文献管理与格式化 |
| hyperref | PDF 超链接、书签 |
| geometry | 页面边距设置 |
| booktabs | 专业表格线条 |
| algorithmic / algorithm2e | 算法伪代码 |
| tikz | 矢量图形绘制 |
| listings / minted | 源代码排版 |

## 相关条目

- [[ResearchMethodology]]
- [[ScientificCommunication]]
- [[00_KnowledgeFramework/BibTeX/INDEX|BibTeX]]
- [[AcademicWriting]]

## 参考资源

- Strunk, W., & White, E. B. (2000). *The Elements of Style* (4th ed.). Pearson.
- Booth, W. C., Colomb, G. G., & Williams, J. M. (2008). *The Craft of Research* (3rd ed.). University of Chicago Press.
- Glasman-Deal, H. (2009). *Science Research Writing for Non-Native Speakers of English*. Imperial College Press.
- Overleaf 模板库: https://www.overleaf.com/latex/templates
- Zotero 官方文档: https://www.zotero.org/support
- PRISMA 声明: https://www.prisma-statement.org
