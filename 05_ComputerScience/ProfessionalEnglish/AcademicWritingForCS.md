---
aliases:
  - CS学术论文写作
  - 学术论文写作
  - Academic Writing for CS
tags:
  - AcademicWriting
  - Paper
  - Conference
created: 2026-06-28
updated: 2026-06-28
---

# CS学术论文写作

计算机科学领域的学术论文写作是研究成果传播的核心方式。高质量的写作不仅需要清晰的技术内容，还需要规范的结构、准确的表达和专业的图表设计。

## 论文结构

### Title（标题）

- 简洁准确，通常10-15个词
- 包含核心贡献的关键词
- 避免缩写和不常见的术语
- 好的标题示例："FlashAttention: Fast and Memory-Efficient Exact Attention with IO-Awareness"
- 避免："A Novel Method for Something"（过于泛泛）

### Abstract（摘要）

150-250词，包含四个关键要素：

1. **问题**（1-2句）：研究的问题是什么，为什么重要
2. **方法**（2-3句）：提出了什么方法，核心思想是什么
3. **结果**（1-2句）：主要实验结果和优势
4. **意义**（1句）：贡献和影响

常用句式：
- "We propose [method], a novel approach to [problem]."
- "Extensive experiments on [dataset] demonstrate that our method achieves [result]."
- "To the best of knowledge, this is the first [contribution]."

### Introduction（引言）

通常1-1.5页，结构化写作：

1. **背景与动机**（2-3段）：研究领域的大背景，为什么这个问题重要
2. **现有方法的不足**（1-2段）：现有方法的具体局限
3. **本文贡献**（1段）：用编号列表明确列出贡献点
4. **论文组织**（1段）：各节内容简介（可选）

贡献点写法示例：
- "We propose X, which achieves Y by Z."
- "We conduct extensive experiments showing that X outperforms Y by Z%."
- "We provide theoretical analysis of X, showing Y."

### Related Work（相关工作）

- 按主题分组而非时间顺序
- 与本文方法的异同要明确说明
- 引用要准确全面，避免遗漏重要工作
- 客观评价，避免贬低他人工作

### Method（方法）

核心部分，需要足够详细以便复现：

1. **问题定义**：形式化定义输入、输出、目标
2. **总体框架**：系统架构图 + 概述
3. **详细设计**：每个组件的详细描述
4. **理论分析**：复杂度分析、收敛性证明（如适用）

写作要点：
- 使用一致的数学符号
- 每个公式前有文字说明
- 关键设计选择要有理由
- 使用图表辅助说明

### Experiment（实验）

1. **实验设置**：数据集、基线方法、评价指标、实现细节
2. **主实验**：与SOTA方法的对比，包含定量表格
3. **消融实验**：验证各组件的贡献
4. **分析实验**：参数敏感性、案例分析、可视化
5. **讨论**：方法的局限性和适用范围

实验表格规范：
- 最佳结果**加粗**，次优下划线
- 报告均值和标准差（多次运行）
- 使用统一的评价指标和数据划分

### Conclusion（结论）

- 总结核心贡献（2-3句）
- 强调主要实验发现（1-2句）
- 指出局限性和未来工作（1-2句）
- 避免引入新信息

## 常用句式与表达

### 引出问题

- "Despite significant progress in [area], [problem] remains challenging."
- "A major limitation of existing approaches is [limitation]."
- "However, these methods fail to [problem] when [condition]."

### 描述方法

- "The key insight of our method is [insight]."
- "Specifically, we [action] by [method]."
- "Formally, we define [concept] as [definition]."
- "As illustrated in Figure X, [description]."

### 报告结果

- "Our method achieves [result] on [dataset], outperforming [baseline] by [margin]."
- "As shown in Table X, [observation]."
- "Notably, [method] consistently outperforms [baseline] across all metrics."
- "The results demonstrate that [conclusion]."

### 讨论局限

- "One limitation of our approach is [limitation]."
- "Our method assumes [assumption], which may not hold in [scenario]."
- "We leave [future work] for future investigation."

### 避免的表达

- ❌ "Our method is the best." → ✅ "Our method achieves state-of-the-art performance."
- ❌ "Obviously" / "Clearly" → 删除或用 "It can be shown that"
- ❌ "We believe" → ✅ "Our results suggest" / "This indicates"
- ❌ "Novel" 重复使用 → 用 "proposed" / "presented" 替换

## 图表设计规范

### 通用原则

- 使用矢量格式（PDF/SVG），避免位图模糊
- 字号不小于8pt（打印后可读）
- 颜色使用色盲友好的调色板（如ColorBrewer）
- 图表标题完整，包含足够的信息使其可独立理解
- 保持一致的视觉风格

### 架构图

- 使用方框表示模块，箭头表示数据流
- 标注输入输出的维度和类型
- 使用颜色区分不同类型的组件
- 工具推荐：draw.io、TikZ、OmniGraffle

### 结果图表

- 折线图：展示趋势变化
- 柱状图：展示方法对比
- 热力图：展示相关性或注意力权重
- 表格：精确数值对比
- 误差棒：展示结果的稳定性

### 表格规范

- 顶部和底部使用粗线，中间使用细线
- 列名清晰，包含单位和评价指标方向（↑/↓）
- 对齐方式：数字右对齐，文字左对齐
- 使用三线表（top、header、bottom）

## 顶级会议投稿指南

### 主要会议

**AI/ML领域**：
- **ICML**：International Conference on Machine Learning，每年7月
- **NeurIPS**：Neural Information Processing Systems，每年12月
- **ICLR**：International Conference on Learning Representations，每年5月
- **AAAI**：Association for the Advancement of Artificial Intelligence，每年2月
- **IJCAI**：International Joint Conference on Artificial Intelligence

**CV领域**：
- **CVPR**：Computer Vision and Pattern Recognition，每年6月
- **ICCV**：International Conference on Computer Vision，奇数年10月
- **ECCV**：European Conference on Computer Vision，偶数年

**NLP领域**：
- **ACL**：Association for Computational Linguistics
- **EMNLP**：Empirical Methods in Natural Language Processing
- **NAACL**：North American Chapter of ACL

**系统领域**：
- **OSDI**：Operating Systems Design and Implementation
- **SOSP**：Symposium on Operating Systems Principles
- **SIGCOMM**：Special Interest Group on Data Communication
- **NSDI**：Networked Systems Design and Implementation

### 投稿流程

1. **准备阶段**（截止前2-3个月）：确定核心贡献、完成实验、撰写初稿
2. **写作阶段**（截止前1个月）：完善论文、团队内部审阅
3. **修改阶段**（截止前1-2周）：根据反馈修改、检查格式
4. **提交**：通过CMT/OpenReview提交，检查PDF合规性
5. **Rebuttal**：回复审稿人意见（2-3周后）
6. **最终决定**：接收/拒绝（1-2月后）

### 常见拒稿原因

- 贡献不清晰或增量改进
- 实验不充分（缺少基线、数据集少、无消融实验）
- 写作质量差（结构混乱、语言不清晰）
- 与现有工作区分度不够
- 方法假设过强或适用范围过窄
- 缺乏理论支撑或实验验证

### 提高接收率的建议

1. 明确定位贡献，突出创新点
2. 充分的实验对比和消融分析
3. 清晰的写作和专业的图表
4. 理论分析与实验验证相结合
5. 认真对待Rebuttal，逐条回复审稿人
6. 提前让同行预审，获取外部反馈
