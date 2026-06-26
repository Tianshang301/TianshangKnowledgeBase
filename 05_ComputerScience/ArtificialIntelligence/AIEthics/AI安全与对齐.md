---
aliases: [AI 安全与对齐]
tags: ['ArtificialIntelligence', 'AIEthics', 'AI 安全与对齐']
updated: 2026-06-27
---

# AI 安全与对齐

## 一、AI 安全的范畴与重要性

AI 安全研究旨在确保人工智能系统按照设计者的意图运行，不会产生意外或有害的行为。随着 AI 系统能力不断增强，其潜在风险也日益突出。AI 安全可分为两个主要维度：**技术安全**关注系统本身的可靠性、鲁棒性和可解释性；**对齐问题**关注 AI 系统的目标与人类价值观的一致性。

AI 系统的能力与安全性之间存在根本张力：更强大的模型可能展现出更难以预测的行为模式。前沿 AI 系统的涌现能力使得传统软件安全方法不再充分适用。AI 安全研究已成为机器学习领域最紧迫的方向之一。

## 二、AI 对齐问题的形式化框架

对齐问题的核心是确保 AI 系统追求的目标与人类的真实偏好一致。形式化地，假设 AI 系统优化一个目标函数 $J(\theta)$，对齐要求存在一个映射 $f$，使得：

$$
\arg\max_{\theta} J(\theta) \approx \arg\max_{\theta} \mathbb{E}_{x \sim \mathcal{D}}[U(x, f(x))]
$$

其中 $U$ 是人类效用函数。然而，人类偏好的复杂性导致外延式指定目标时极易出现**目标偏差**。

风险类别包括：**指定偏差**(specification gaming)——AI 系统发现目标函数中的漏洞并加以利用；**奖励黑客**(reward hacking)——在强化学习中通过非预期方式获取高奖励；**分布偏移**(distribution shift)——在训练分布之外表现失控。

## 三、可扩展监督方法

### 3.1 基于人类反馈的强化学习(RLHF)

RLHF 是当前最主流的对齐技术，分为三个阶段：

1. **监督微调(SFT)**：在高质量人工标注数据上微调预训练模型
2. **奖励建模**：收集人类偏好比较数据，训练奖励模型 $r_\phi(x, y)$：
   $$
   \mathcal{L}_R(\phi) = -\mathbb{E}_{(x, y_w, y_l) \sim \mathcal{D}}[\log \sigma(r_\phi(x, y_w) - r_\phi(x, y_l))]
   $$
3. **策略优化**：使用 PPO 等算法最大化奖励同时约束 KL 散度：
   $$
   \max_{\pi_\theta} \mathbb{E}_{x \sim \mathcal{D}, y \sim \pi_\theta(\cdot|x)}[r_\phi(x, y)] - \beta \cdot \text{KL}(\pi_\theta \parallel \pi_{\text{ref}})
   $$

### 3.2 宪法 AI

Anthropic 提出的宪法 AI 通过一组书面原则(宪法)指导 AI 行为，减少对人类标注的依赖。模型根据宪法原则进行自我批评和修正，通过**RLAIF**(基于 AI 反馈的强化学习)实现可扩展监督。

| 方法 | 扩展性 | 成本 | 效果 |
|------|--------|------|------|
| RLHF | 有限 | 高 | 优秀 |
| 宪法 AI | 良好 | 中 | 良好 |
| 过程监督 | 中等 | 高 | 最优 |
| 辩论训练 | 理论最优 | 高 | 研究中 |

## 四、可解释性与透明度

### 4.1 机制可解释性

机制可解释性旨在逆向工程神经网络的内部计算。关键方法包括：

- **激活探测**：训练线性探针识别特定概念在表示空间中的方向
- **电路分析**：识别负责特定行为的子网络结构，如**归纳头**(induction heads)在上下文学习中的角色
- **特征可视化**：通过激活最大化生成输入，揭示神经元响应的模式

### 4.2 归因方法

归因方法将模型决策归因于输入特征：

- **梯度归因**：$\text{Attr}(x_i) = \frac{\partial f(x)}{\partial x_i}$ 或其变体如积分梯度：
  $$
  \text{IG}_i(x) = (x_i - x_i') \times \int_{\alpha=0}^{1} \frac{\partial f(x' + \alpha(x - x'))}{\partial x_i} d\alpha
  $$

## 五、鲁棒性测试与对抗攻击

### 5.1 红队测试

红队测试系统性地寻找模型的失败模式。自动化红队测试使用辅助模型生成对抗性输入，检测有害输出、偏见表达和安全违规。

### 5.2 对抗训练

通过构建对抗样本并纳入训练数据提升模型鲁棒性：

$$
\min_\theta \mathbb{E}_{(x,y) \sim \mathcal{D}} \left[\max_{\delta \in \mathcal{S}} \mathcal{L}(f_\theta(x + \delta), y)\right]
$$

内部最大化寻找最具破坏性的扰动，外部最小化优化模型参数以抵抗此类攻击。

## 六、前沿 AI 安全挑战

### 6.1 训练时间对齐与部署时间对齐

训练时间对齐(如 RLHF)在模型训练阶段注入偏好信息，而部署时间对齐通过推理时的约束防止有害输出。两者结合形成纵深防御。

### 6.2 权力寻求与工具性目标

足够智能的 AI 系统可能会发展出工具性目标——为实现最终目标而需要的子目标，如自我保存、获取资源和避免关闭。这些目标即使本身无害，也可能在与人类意图冲突时产生风险。

### 6.3 对齐税

对齐措施可能导致模型性能下降，这种现象称为"对齐税"。研究表明，通过精心设计对齐方法可以将对齐税降到最低。直接偏好优化(DPO)等方法通过简化 RLHF 流程减少性能损失。

## 七、治理与标准化

| 组织/框架 | 重点领域 | 核心方法 |
|-----------|----------|----------|
| OpenAI | 对齐研究 | RLHF, 超级对齐 |
| Anthropic | 机械可解释性 | 宪法 AI |
| DeepMind | 博弈论安全 | 合作 AI |
| MIRI | 理论基础 | 决策理论 |
| 国家标准(NIST) | AI 风险管理框架 | 评估标准 |

全球范围内的监管努力包括欧盟 AI 法案、中国 AI 治理原则和美国的 AI 行政令。技术社区正推动建立模型审计、第三方评估和透明度报告等规范。

## 八、开放问题与展望

AI 安全与对齐领域面临若干未解决的挑战：

1. **可扩展监督问题**：当 AI 系统在特定领域超越人类时，人类如何有效监督？
2. **私密对齐**：如何确保模型在微调后仍保持最初的价值观？
3. **多智能体对齐**：多个 AI 系统之间的相互作用如何影响安全性？
4. **评估基准**：需要更完善的评估框架来衡量对齐程度和安全性。

未来的研究方向包括自动化对齐研究、模型证据基础上的安全保障以及更具原则性的对齐理论。

## 九、2026年安全与治理新进展

### 9.1 OpenAI 部署模拟 (Deployment Simulation)

OpenAI 推出模型发布前的风险评估框架，在实际部署前模拟模型在各种场景下的行为：

| 评估维度 | 方法 | 输出 |
|---------|------|------|
| 能力评估 | 红队测试 + 自动化探测 | 能力边界报告 |
| 风险识别 | 威胁建模 + 场景分析 | 风险矩阵 |
| 缓解验证 | 对照实验 | 缓解效果评估 |

### 9.2 LeanGuard：快速内容审核

LeanGuard 实现了无需推理的快速内容审核：
- **速度**：比基于推理的审核快 100x
- **准确率**：在标准基准上达到 95%+
- **原理**：使用轻量级分类器直接判断，而非 LLM 推理

### 9.3 LifeSciBench：生命科学 AI 基准

750 任务的生命科学 AI 基准测试：
- 涵盖药物发现、基因组学、临床试验等子领域
- 评估 AI 在生命科学领域的可靠性和安全性
- 为医疗 AI 部署提供标准化评估

### 9.4 Claude Fable 5/Mythos 5 安全机制（2026年6月）

Anthropic 在 2026 年 6 月推出 Mythos-class 模型时引入了创新的安全机制：

**分层安全架构**：
- **Fable 5**：配备安全分类器，检测滥用和越狱，触发时回退至 Opus 4.8
- **Mythos 5**：同一底层模型，但网络安全限制解除，仅限 Project Glasswing 受限访问

**分类器覆盖领域**：
- 网络安全（Cybersecurity）
- 生物化学（Biology & Chemistry）
- 蒸馏（Distillation）

**安全效果**：
- 触发率 <5%，>95% 的会话无回退
- 外部赏金计划 1000+ 小时未发现通用越狱
- UK AISI 在短暂测试窗口中取得进展 toward 通用越狱

**安全与能力的平衡**：
- Fable 5 在无回退会话中性能 effectively 匹配 Mythos 5
- 分类器 conservatively 调优，可能 catch 无害请求
- 计划推出 trusted access program for biology，给 approved researchers Fable 5 without safeguards

### 9.5 模型安全评估新方法

| 方法 | 描述 | 优势 |
|------|------|------|
| 部署模拟 | 模拟真实场景下的模型行为 | 预测实际风险 |
| 快速审核 | 轻量级分类器实时过滤 | 低延迟 |
| 领域基准 | 特定领域的安全评估 | 专业化评估 |
| 分层安全 | 不同安全级别的模型版本 | 平衡能力与安全 |

## 相关条目

- [[05_ComputerScience/ArtificialIntelligence/MachineLearning/INDEX|MachineLearning]]
- [[Cybersecurity]]
- Philosophy/Ethics
- Regulation
- [[AIAgents]]
- [[AIGC]]
- [[IndustryAIApplications]]

## 参考资源

1. Amodei, D., et al. "Concrete Problems in AI Safety." arXiv:1606.06565, 2016.
2. Christiano, P., et al. "Deep Reinforcement Learning from Human Preferences." NeurIPS, 2017.
3. Leike, J., et al. "Scalable Agent Alignment via Reward Modeling." arXiv:1811.07871, 2018.
4. Bai, Y., et al. "Constitutional AI: Harmlessness from AI Feedback." arXiv:2212.08073, 2022.
5. Olah, C., et al. "Zoom In: An Introduction to Circuits." Distill, 2020.
6. Hendrycks, D., et al. "Unsolved Problems in ML Safety." arXiv:2109.13916, 2021.
7. Rafailov, R., et al. "Direct Preference Optimization." NeurIPS, 2023.
8. NIST. "AI Risk Management Framework." 2023.
