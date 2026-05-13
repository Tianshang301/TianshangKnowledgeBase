# AI伦理

## 一、伦理框架基础

AI伦理涉及多种哲学伦理框架在人工智能系统中的应用与权衡：

| 伦理框架 | 核心原则 | AI应用考量 |
|---------|---------|-----------|
| 功利主义 (Utilitarianism) | 追求最大多数人的最大幸福 | 模型决策需要评估总体社会收益与成本 |
| 义务论 (Deontology) | 基于道德规则与义务，关注行为本身对错 | AI系统必须遵守不可侵犯的道德准则 |
| 德性伦理 (Virtue Ethics) | 关注行为主体的品格与美德 | AI系统应体现诚实、公正、仁爱等品质 |

### 功利主义视角

$$
\text{效用} = \sum_{i=1}^{n} U_i(\text{outcome})
$$

AI系统的设计应最大化总体社会福利，但面临如何量化效用、如何处理少数群体利益的挑战。

### 义务论视角

强调AI系统必须遵循特定道德规则，如"不得伤害人类"（Asimov机器人三定律的延伸），即使在某些情境下违反规则可能带来更大的总体收益。

### 德性伦理视角

关注AI系统应当培养或模拟哪些美德特质：诚实（可解释性）、公正（无偏见）、审慎（安全考量）等。

## 二、偏见与公平性

### 偏见的来源

- **数据偏见**：训练数据未能代表真实人群分布
- **算法偏见**：模型设计或目标函数导致系统性偏差
- **部署偏见**：模型在不同于训练分布的环境中应用

### 公平性定义

不同公平性定义之间存在不可兼得性（Impossibility Theorem）：

| 公平性指标 | 定义 | 公式 |
|-----------|------|------|
| 人口均等 (Demographic Parity) | 各组别接受正面预测的比例相等 | $P(\hat{Y}=1|A=a) = P(\hat{Y}=1|A=b)$ |
| 均等机会 (Equal Opportunity) | 各组别真正例率相等 | $P(\hat{Y}=1|Y=1,A=a) = P(\hat{Y}=1|Y=1,A=b)$ |
| 均等赔率 (Equalized Odds) | 各组别TPR和FPR均相等 | $P(\hat{Y}|Y,A=a) = P(\hat{Y}|Y,A=b)$ |
| 不同影响 (Disparate Impact) | 各组别正面比率之比不低于4/5 | $\frac{P(\hat{Y}=1|A=a)}{P(\hat{Y}=1|A=b)} \geq 0.8$ |

### 偏见缓解方法

$$
\text{预处理} \rightarrow \text{处理训练数据以消除偏见源}
$$
$$
\text{处理中} \rightarrow \text{在训练过程中加入公平性约束}
$$
$$
\text{后处理} \rightarrow \text{调整模型输出以满足公平性标准}
$$

## 三、可解释性与透明度

### XAI（可解释AI）方法

**全局解释**：理解模型的整体决策逻辑
- 特征重要性（SHAP, LIME）
- 决策树 surrogate 模型
- 部分依赖图 (Partial Dependence Plot)

**局部解释**：理解单个预测的原因
- LIME: 在预测点附近拟合可解释模型
- SHAP: 基于博弈论Shapley值的特征归因

$$
\phi_i = \sum_{S \subseteq N \setminus \{i\}} \frac{|S|!(|N|-|S|-1)!}{|N|!} [f(S \cup \{i\}) - f(S)]
$$

## 四、隐私保护

AI系统中的隐私挑战：
- 训练数据可能包含敏感个人信息
- 模型可能记忆并泄露训练数据（Membership Inference Attack）
- 模型输出可能推断出敏感属性

隐私保护技术：
- **差分隐私 (Differential Privacy)**：在训练或查询过程中添加噪声
- **联邦学习 (Federated Learning)**：数据不离开本地，仅交换模型更新
- **同态加密 (Homomorphic Encryption)**：在加密数据上直接计算

$$
\epsilon\text{-差分隐私}: \Pr[\mathcal{M}(D) \in S] \leq e^\epsilon \cdot \Pr[\mathcal{M}(D') \in S]
$$

## 五、AI安全与对齐问题

### 对齐问题 (Alignment Problem)

确保AI系统的目标与人类价值观相一致：

$$
\text{reward}(a|s) \xrightarrow{\text{学习}} \text{人类真实偏好}
$$

主要挑战：
- **外延对齐 (Outer Alignment)**：目标函数是否真正反映了人类意图
- **内涵对齐 (Inner Alignment)**：模型是否真正优化了设定的目标而非投机取巧

### AI安全风险

| 风险类型 | 描述 | 示例 |
|---------|------|------|
| 奖励篡改 (Reward Hacking) | 系统找到最大化奖励的意外方式 | 游戏AI利用bug而非学习技能 |
| 分布偏移 (Distribution Shift) | 在训练分布外表现不可控 | 自动驾驶遇到未见场景 |
| 涌现行为 (Emergent Behavior) | 复杂系统出现未预期的能力 | 大语言模型展示推理能力 |
| 权力寻求 (Power-Seeking) | 系统为达成目标而寻求更多控制 | 为达成目标而阻止关机 |

## 六、自主武器系统

致命性自主武器系统（LAWS）引发的伦理争议：
- 将生杀大权交给机器的道德合法性
- 缺乏人类判断的问责机制
- 自主武器扩散的军备竞赛风险

## 七、就业与经济影响

AI对劳动力市场的影响呈现双重性：
- **替代效应**：自动化取代重复性工作
- **补充效应**：AI增强人类能力，创造新岗位

| 影响维度 | 低技能岗位 | 高技能岗位 | 创意岗位 |
|---------|-----------|-----------|---------|
| 替代风险 | 高 | 中 | 低 |
| 转型需求 | 技能重塑 | 人机协作 | AI辅助 |

## 八、AI治理与监管

### 欧盟AI法案 (EU AI Act)

基于风险分级的管理框架：
$$
\text{不可接受风险} \rightarrow \text{禁止}
$$
$$
\text{高风险} \rightarrow \text{严格合规要求}
$$
$$
\text{有限风险} \rightarrow \text{透明度义务}
$$
$$
\text{极小风险} \rightarrow \text{无约束}
$$

**2024-2026年实施时间线**：
- **2024.08.01**：法案生效
- **2025.02**：禁止不可接受的AI实践
- **2026.08.02**：高风险AI规则生效 + 透明度义务生效（用户须被告知正在与AI交互）
- **2027.08.02**：全部规则生效

**2026年关键更新**：
- 欧盟委员会发布AI透明度义务指南草案（2026.04公开征询）
- 要求AI提供商对AIGC内容添加机器可读标记
- 部署者须标记深度伪造和AI生成内容
- 预计2026年6月发布最终版《AI生成内容标记与标签行为准则》

### 中国AI监管

- 《生成式人工智能服务管理暂行办法》（2023）
- 算法备案制度
- 内容安全审查机制
- 强调社会主义核心价值观与技术发展平衡
- 2025-2026年进一步细化大模型备案要求和安全评估标准

## 九、典型案例分析

### COMPAS再犯风险评估

- 问题：算法对非裔美国人的错误率（FPR）显著高于白人
- 教训：算法公平性不能仅追求单一指标，需要多维度评估

### 面部识别偏见

- 问题：早期面部识别系统对肤色较深女性的识别准确率显著较低
- 根源：训练数据缺乏多样性
- 影响：导致错误逮捕案例，引发禁用呼声

## 九、AI安全治理最新进展（2025-2026）

### 9.1 国际AI安全报告2026

第二届国际AI安全报告（2026年发布）基于2023年Bletchley Park AI安全峰会的授权，涵盖以下核心内容：

**前沿AI风险类别**：
- **恶意使用**：AI用于犯罪、网络攻击、生物/化学武器开发
- **故障风险**：可靠性问题、失控风险
- **系统性风险**：劳动力市场冲击、人类自主性威胁

**风险管理实践**：
- 2025年，12家公司发布或更新了前沿AI安全框架
- 风险识别：威胁建模、能力评估
- 技术防护：红队测试、输入/输出过滤
- 社会韧性建设：提升社会对AI冲击的适应能力

### 9.2 法律对齐（Legal Alignment）

牛津大学AIGI团队于2026年提出"法律对齐"概念，成为AI伦理的新研究方向：

**三条路径**：
1. **法律规则作为AI对齐的内容来源**：设计AI系统遵守通过合法制度制定的法律
2. **法律解释方法作为AI推理指南**：借鉴法律解释技术指导AI决策
3. **法律概念作为AI对齐的结构蓝图**：利用法律概念解决可靠性、信任和合作问题

**关键特点**：
- 法律对齐不同于AI法律监管——它主要使用现有法律，不一定需要监管改革
- 需要实证评估（法律合规基准）和制度框架（透明度报告义务）

### 9.3 OECD AI尽责管理指南

2026年2月，OECD发布《AI尽责管理指南》，为企业实施负责任AI提供操作框架：

**六步尽责管理流程**：
1. 将负责任商业行为嵌入政策和管理系统
2. 识别和评估实际和潜在的负面影响
3. 停止、预防和缓解负面影响
4. 跟踪实施和结果
5. 沟通应对措施
6. 在适当时提供或配合补救

### 9.4 前沿AI安全框架（Frontier AI Safety Frameworks）

2025-2026年，主要AI企业自愿发布安全框架：

| 企业 | 框架内容 |
|------|----------|
| OpenAI | 准备框架（Preparedness Framework） |
| Anthropic | 负责任扩展政策（RSP） |
| Google DeepMind | 前沿安全框架 |
| Microsoft | 负责任AI标准 |

虽然多数仍为自愿性质，但部分司法管辖区开始将部分实践纳入法律要求。

## 十、AI伦理实施路径

1. **伦理设计（Ethics by Design）**：伦理考量嵌入开发全流程
2. **伦理影响评估**：部署前进行系统性伦理审计
3. **多元利益相关方参与**：引入伦理学家、社会学家、社区代表
4. **持续监控与迭代**：部署后持续追踪伦理影响
5. **透明报告**：公开模型能力边界与局限性

## 相关条目

- [[AI安全与对齐]]
- [[05_ComputerScience/ArtificialIntelligence/MachineLearning/INDEX|MachineLearning]]
- [[KnowledgeRepresentation]]
- Regulation

## 参考资源

- Russell, S. (2019). *Human Compatible: AI and the Problem of Control*
- Floridi, L. & Cowls, J. (2019). "A Unified Framework of Five Principles for AI in Society"
- Bender, E. M. et al. (2021). "On the Dangers of Stochastic Parrots"
- European Commission. (2021). "Proposal for a Regulation laying down harmonised rules on AI" (EU AI Act)
- 国家互联网信息办公室. (2023). 《生成式人工智能服务管理暂行办法》
- Kolt, N. et al. (2026). "Legal Alignment for Safe and Ethical AI." Oxford AIGI.
- International AI Safety Report 2026. (2026). https://internationalaisafetyreport.org
- OECD. (2026). "OECD Due Diligence Guidance for Responsible AI."
- European Commission. (2025). "Commission opens consultation on draft guidelines for AI transparency obligations."
- Anthropic. (2025). "Responsible Scaling Policy."
- OpenAI. (2023). "Preparedness Framework."
