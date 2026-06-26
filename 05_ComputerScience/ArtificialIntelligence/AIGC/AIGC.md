---
aliases: [AIGC]
tags: ['ArtificialIntelligence', 'AIGC', 'AI 生成内容']
created: 2026-05-17
updated: 2026-06-27
---

# AIGC（AI 生成内容）

## 一、生成式 AI 概述

AIGC（AI Generated Content）指利用人工智能技术自动生成各类内容，涵盖文本、图像、音频、视频、代码等多种模态。其核心驱动力来自深度生成模型的快速发展。

### 生成模型演进

| 时期 | 代表技术 | 能力 |
|------|---------|------|
| 2014-2017 | GAN、VAE | 图像生成初步可用 |
| 2017-2020 | Transformer、BERT、GPT-2 | 文本生成突破 |
| 2020-2022 | GPT-3、DALL-E、Stable Diffusion | 多模态生成爆发 |
| 2022-2024 | GPT-4、Gemini、Sora、Claude | 通用内容生成 |
| 2024-2026 | GPT-5.5、Gemini 3.1 Pro、Claude Opus 4.7、Sora 2 | 通用 AI 代理与多模态融合 |
| 2026.06 | GPT-5.6、Claude Fable 5/Mythos 5、Ornith-1.0、GLM-5.2 | 分层推理模型、Mythos-class、开源编码突破 |

### 生成模型分类

$$
\text{生成模型} \to
\begin{cases}
\text{显式密度模型}: \text{VAE}, \text{Normalizing Flows} \\
\text{隐式密度模型}: \text{GAN} \\
\text{扩散模型}: \text{DDPM}, \text{Score-based} \\
\text{自回归模型}: \text{GPT}, \text{Transformer}
\end{cases}
$$

## 二、文本生成

### 语言模型系列

**GPT 系列**（Generative Pre-trained Transformer）：

GPT 模型使用自回归方式生成文本：

$$
P(x_1, x_2, ..., x_T) = \prod_{t=1}^T P(x_t | x_{<t}; \theta)
$$

| 模型 | 参数量 | 训练数据 | 核心能力 |
|------|--------|---------|---------|
| GPT-1 | 117M | BookCorpus | 基础语言建模 |
| GPT-2 | 1.5B | WebText | 文本生成连贯性 |
| GPT-3 | 175B | Common Crawl | 少样本学习 |
| GPT-4 | 约1.8T* | 多模态数据 | 多模态理解与生成 |
| GPT-5 | 未公开 | 大规模多模态 | 2025.08 发布，深度推理 |
| GPT-5.4 | 未公开 | 大规模多模态 | 2026.03 发布，强知识/Agent |
| GPT-5.5 | 未公开 | 大规模多模态 | 2026.04 发布，Terminal-Bench 领先 |
| GPT-5.6 | 未公开 | 大规模多模态 | 2026.06 发布，分层模型（Sol/Terra/Luna），新推理模式 |

### 提示工程技术

- **零样本提示**：直接给出任务描述
- **少样本提示**：提供若干示例引导输出
- **思维链（CoT）**：引导模型展示推理过程
- **思维树（ToT）**：多路径搜索组合
- **ReAct**：推理与行动交替执行

### 前沿大模型对比（2026春季）

截至2026年5月，前沿大模型呈现三足鼎立格局：

| 模型 | 开发商 | 综合评分 | 优势领域 | API 价格（输入/输出 per 1M tokens） |
|------|--------|---------|---------|-----------------------------------|
| **Gemini 3.1 Pro** | Google | 93 | 推理(ARC-AGI-2 77.1%)、多模态、性价比 | $2 / $12 |
| **GPT-5.5** | OpenAI | 88 | Agentic (Terminal-Bench 82.7%)、知识深度 | $5 / $30 |
| **Claude Opus 4.7** | Anthropic | 88 | SWE-Bench 93.9%、写作、长文档 | $15 / $75 |
| **Claude Mythos Preview** | Anthropic | — | USAMO 97.6%（受限发布，安全原因未公开） | 仅限安全合作方 |

### 前沿大模型对比（2026年6月更新）

2026年6月，Anthropic 推出 Mythos-class 模型，格局发生重大变化：

| 模型 | 开发商 | 综合评分 | 优势领域 | API 价格（输入/输出 per 1M tokens） |
|------|--------|---------|---------|-----------------------------------|
| **Claude Fable 5** | Anthropic | 95+ | 软件工程（Stripe 5000万行迁移）、视觉、长上下文 | $10 / $50 |
| **Claude Mythos 5** | Anthropic | 95+ | 网络安全（最强）、科学研究、基因组学 | $10 / $50（受限访问） |
| **GPT-5.6** | OpenAI | 90+ | 分层推理（Sol/Terra/Luna）、推理效率 | 未公开 |
| **Gemini 3.1 Pro** | Google | 93 | 推理(ARC-AGI-2 77.1%)、多模态、性价比 | $2 / $12 |
| **GLM-5.2** | 智谱 AI | 85+ | OpenAI 兼容 API、推理努力控制 | 未公开 |
| **Ornith-1.0** | DeepReinforce | 82.4 | SWE-Bench 82.4%、开源编码 | 开源免费 |
| **VibeThinker-3B** | 社区 | 80+ | 3B 参数匹配 DeepSeek V3.2 | 开源免费 |

核心趋势：
- **推理能力**：Gemini 3.1 Pro 在 ARC-AGI-2 上达 77.1%，是 GPT-5.4 的两倍以上
- **Agent 能力**：GPT-5.5 在 Terminal-Bench 2.0 (82.7%) 和 OSWorld (78.7%) 领先
- **编码能力**：Claude Mythos 在 SWE-Bench 达 93.9%，创历史最高
- **上下文窗口**：三大模型均支持 1M+ tokens 上下文
- **开源追赶**：DeepSeek V4、Cwen 3.6 Plus 正在缩小与闭源模型的差距
- **分层推理**：GPT-5.6 引入 Sol/Terra/Luna 三级模型，按需选择推理深度
- **Mythos-class**：Anthropic 推出 Fable 5/Mythos 5，能力超越 Opus-class
- **开源加速**：Ornith-1.0 达 82.4% SWE-Bench，VibeThinker-3B 以 3B 参数匹配大模型
- **API 标准化**：GLM-5.2 实现 OpenAI 兼容 API，降低迁移成本

### 文本生成应用

| 应用 | 描述 | 代表工具 |
|------|------|---------|
| 对话助手 | 多轮对话交互 | ChatGPT, Claude, Gemini |
| 写作辅助 | 文章、报告、创意写作 | Jasper, Copy.ai |
| 代码生成 | 根据自然语言生成代码 | GitHub Copilot, Claude Code |
| 翻译服务 | 跨语言翻译 | DeepL, GPT Translate |
| 摘要生成 | 长文本浓缩为摘要 | Claude, ChatGPT |
| 深度研究 | 自主多步研究和报告生成 | Gemini Deep Research, ChatGPT Deep Research |

## 三、图像生成

### 生成对抗网络 (GAN)

$$
\min_G \max_D V(D,G) = \mathbb{E}_{x\sim p_{\text{data}}}[\log D(x)] + \mathbb{E}_{z\sim p_z}[\log(1 - D(G(z)))]
$$

### 变分自编码器 (VAE)

$$
\log p(x) \geq \mathbb{E}_{z\sim q_\phi(z|x)}[\log p_\theta(x|z)] - D_{\text{KL}}(q_\phi(z|x) || p(z))
$$

### 扩散模型 (Diffusion Models)

**正向过程**：逐步添加噪声

$$
q(x_t | x_{t-1}) = \mathcal{N}(x_t; \sqrt{1-\beta_t} x_{t-1}, \beta_t I)
$$

**反向过程**：去噪重建

$$
p_\theta(x_{t-1} | x_t) = \mathcal{N}(x_{t-1}; \mu_\theta(x_t, t), \Sigma_\theta(x_t, t))
$$

**DDPM (Denoising Diffusion Probabilistic Models)** 损失函数：

$$
\mathcal{L}_{\text{simple}}(\theta) = \mathbb{E}_{t, x_0, \epsilon} \left[||\epsilon - \epsilon_\theta(\sqrt{\bar{\alpha}_t}x_0 + \sqrt{1-\bar{\alpha}_t}\epsilon, t)||^2\right]
$$

### 图像生成模型对比

| 模型 | 类型 | 分辨率 | 特点 |
|------|------|--------|------|
| DALL-E 2 | 扩散 + CLIP | 1024x1024 | 文本理解强 |
| DALL-E 3 | 扩散 + 改进 | 高分辨率 | 图文对齐最佳 |
| Stable Diffusion | 潜在扩散 | 512/1024 | 开源，可控性强 |
| Midjourney | 扩散模型 | 高分辨率 | 艺术风格优秀 |
| Imagen | 扩散模型 | 1024x1024 | 逼真度高 |
| Adobe Firefly | 扩散模型 | 高分辨率 | 商业安全 |

### 潜在扩散模型 (Latent Diffusion)

在潜在空间而非像素空间执行扩散过程：

$$
\mathcal{L}_{\text{LDM}} = \mathbb{E}_{\mathcal{E}(x), \epsilon, t} \left[||\epsilon - \epsilon_\theta(z_t, t, \tau_\theta(y))||^2\right]
$$

## 四、视频生成

视频生成面临时序一致性的核心挑战：

| 模型 | 特点 | 时长 |
|------|------|------|
| Sora 2 (OpenAI) | Diffusion Transformer，物理模拟+音效同步 | 20s（已停运2026.04）|
| Runway Gen-3 | 文本/图像到视频 | 约10s |
| Pika 2.0 | 简单易用，风格多样化 | 约5s |
| Stable Video Diffusion | 开源视频生成 | 约5s |
| Emu3 (Meta) | 纯 Next-Token Prediction 统一视频生成 | 可变长 |

**视频生成重大事件（2024-2026）**：
- **Sora (2024.02)**：OpenAI 首次展示，60s 高质量视频生成，被视为视频生成"GPT-1 时刻"
- **Sora Turbo (2024.12)**：更快版本，向 ChatGPT Plus/Pro 用户开放
- **Sora 2 (2025.09)**：重大改进，物理精确度大幅提升，支持音效同步生成，推出 iOS 社交应用
- **Emu3 (2026.01)**：Meta 在 Nature 发文，证明纯 Next-Token Prediction 可用于视频生成，无需扩散模型
- **Sora 停运 (2026.04)**：OpenAI 宣布关闭 Sora 产品线和 API，与迪士尼的授权协议终止
- **Sora API (2026.09)**：计划关停，Sora 品牌终结

## 五、音乐与音频生成

| 模型 | 功能 | 技术路线 |
|------|------|---------|
| MusicGen (Meta) | 文本生成音乐 | EnCodec + Transformer |
| Suno AI | 歌词+旋律生成 | 自回归 + 扩散 |
| Eleven Labs | 语音合成与克隆 | 神经网络声码器 |
| Whisper (OpenAI) | 语音识别 | Encoder-Decoder Transformer |

## 六、代码生成

### 代码大模型对比

| 模型 | 基础模型 | 训练数据 | 代码语言支持 |
|------|---------|---------|-------------|
| GitHub Copilot | Codex (GPT-3衍生) | GitHub 公开代码 | 多语言 |
| Code Llama | Llama 2 | 代码+自然语言 | Python, C++, Java 等 |
| StarCoder | 自研 | The Stack 数据集 | 80+语言 |
| DeepSeek Coder | 自研 | 87%代码+13%文本 | 多语言 |
| CodeGemma | Gemma | 代码数据 | Python, JS 等 |
| Ornith-1.0 | Gemma 4 + Qwen 3.5 | 开源代码数据 | 多语言，SWE-Bench 82.4% |

## 七、多模态生成

多模态生成模型同时处理和理解多种数据类型：

$$
P(\text{文本}, \text{图像}, \text{音频}, ...) = \text{统一生成范式}
$$

**DALL-E 3 + GPT-4**：文本理解驱动图像生成
**Gemini**：原生多模态
**Gato (DeepMind)**：单一模型处理600+任务

### 多模态统一架构（2025-2026最新进展）

| 模型 | 方法 | 特点 |
|------|------|------|
| **Emu3 (Meta 2026.01)** | 纯 Next-Token Prediction | 单一 Transformer 统一文本/图像/视频/机器人操控，发表于 Nature |
| **Nemotron 3 Nano Omni (NVIDIA 2026.04)** | 30B-A3B MoE 混合专家 | 统一视觉/音频/语言，3x 吞吐量提升，开源 |
| **Phi-4-reasoning-vision** | 15B 多模态推理 | 轻量级，数学/科学推理+UI 理解，开源权重 |
| **Vision Banana (Google 2026.04)** | 图像生成即视觉理解 | 将视觉任务视为图像生成，SOTA 分割/深度估计 |

**核心趋势**：从分离的模态专属模型走向统一架构。Emu3 证明纯 Next-Token Prediction 可以统一所有模态，Nemotron 3 Nano Omni 展示了高效的多模态 Agent 部署。

## 八、训练范式

### 预训练 + 微调 (Pre-training + Fine-tuning)

1. **预训练**：在大规模无标注数据上学习通用表示
2. **有监督微调 (SFT)**：在标注数据上适配下游任务
3. **RLHF**：基于人类反馈的强化学习

### RLHF (Reinforcement Learning from Human Feedback)

$$
\mathcal{L}_{\text{RLHF}} = \mathbb{E}_{(x,y) \sim \mathcal{D}_{\text{RL}}} [r_\phi(x, y_w) - r_\phi(x, y_l)]
$$

PPO 优化目标：

$$
\mathcal{L}^{\text{PPO}}(\theta) = \mathbb{E}_{x,y \sim \pi_{\theta_{\text{old}}}} \left[\min\left(\frac{\pi_\theta(y|x)}{\pi_{\theta_{\text{old}}}(y|x)} A(x,y), \text{clip}(\cdot) A(x,y)\right)\right]
$$

## 九、挑战与风险

| 挑战 | 描述 | 应对措施 |
|------|------|---------|
| 版权问题 | 训练数据版权、生成内容版权 | 合规数据、版权水印 |
| 真实性 | Deepfake、虚假信息传播 | 内容认证、检测技术 |
| 质量控制 | 生成内容准确性、安全性 | 内容过滤、人类审核 |
| 偏见放大 | 训练数据偏见被放大 | 偏见检测、数据平衡 |
| 能耗问题 | 大模型训练高能耗 | 模型压缩、绿色计算 |

## 十、AI Agent 与工具使用（2025-2026前沿）

2025-2026年，AI 从单纯的内容生成迈向 **Agentic AI（智能代理）** 时代：

| Agent 能力 | 代表模型/工具 | 表现 |
|-----------|-------------|------|
| 计算机操作 | GPT-5.5、Claude Code | 自主操作桌面应用、浏览器、IDE |
| 软件工程 | Claude Mythos (93.9% SWE-Bench)、Claude Fable 5 (Stripe 5000万行迁移) | 全栈开发、调试、代码审查、大规模迁移 |
| 深度研究 | Gemini Deep Research、ChatGPT Deep Research | 多步信息搜索、报告生成 |
| 多工具编排 | Gemini Antigravity、OpenAI Responses API | 函数调用、API 编排、工作流自动化 |
| 网络安全 | Claude Mythos 5 | 最强网络安全能力，Project Glasswing |
| 科学研究 | Claude Mythos 5 | 蛋白质设计加速 10x，新颖科学假设 |

**关键架构创新**：
- **Nemotron 3 Super (NVIDIA 2026.03)**：120B 参数、32B 激活的混合 Mamba-Transformer MoE，原生1M 上下文窗口，支持 Agent 多步推理
- **Multi-Token Prediction (MTP)**：一次前向传播预测多个未来 token，推理速度提升 3x
- **Hybrid Mamba-Transformer**：Mamba 层处理长序列（线性复杂度），Transformer 层保留精确检索能力

### Claude Fable 5 / Mythos 5 详细对比（2026年6月）

Anthropic 在 2026 年 6 月 9 日推出 Mythos-class 模型，代表当前最强 AI 能力：

| 属性 | Claude Fable 5 | Claude Mythos 5 | Claude Opus 4.8 |
|------|---------------|-----------------|-----------------|
| 模型层级 | Mythos-class | Mythos-class | Opus-class |
| 底层模型 | 与 Mythos 5 相同 | 与 Fable 5 相同 | Opus 4.8 |
| 可用性 | 一般可用 | 受限访问 (Project Glasswing) | 一般可用 |
| 安全分类器 | 活跃（网络安全、生物化学、蒸馏） | 网络安全限制解除 | Opus 级别安全 |
| 回退目标 | 回退至 Opus 4.8 | 不适用 | 不适用 |
| API 模型 ID | `claude-fable-5` | `claude-mythos-5` | (现有 Opus ID) |
| 上下文窗口 | 1M tokens | 1M tokens | — |
| 最大输出 | 128k tokens/请求 | 128k tokens/请求 | — |
| 定价（输入/输出 per 1M） | $10 / $50 | $10 / $50 | — |
| 思考模式 | 自适应，始终开启 | 自适应，始终开启 | 可配置 |

**Claude Fable 5 核心能力**：
- **软件工程**：Stripe 在 5000 万行 Ruby 代码库中完成代码迁移，从 2 个月缩短至 1 天
- **知识工作**：Hebbia Finance Benchmark 最高分，擅长文档推理、图表解读
- **视觉能力**：从截图重建 Web 应用源代码，视觉-only 通关 Pokémon FireRed
- **长上下文记忆**：百万 token 持续聚焦，Slay the Spire 中记忆效果提升 3x

**Claude Mythos 5 核心能力**：
- **网络安全**：当前最强网络安全能力的模型
- **科学研究**：蛋白质设计加速 10x，首次持续产生新颖科学假设
- **基因组学**：自主运行一周，训练出超越 Science 发表模型的定制模型（小 100 倍）

**安全机制**：
- Fable 5 配备分类器，检测滥用和越狱，触发时回退至 Opus 4.8
- 分类器覆盖网络安全、生物化学、蒸馏三个领域
- 触发率 <5%，>95% 的会话无回退
- 外部赏金计划 1000+ 小时未发现通用越狱

## 十一、对创意产业的影响

| 行业 | 受影响环节 | 人机协作模式 |
|------|-----------|-------------|
| 平面设计 | 素材生成、排版 | 设计师创意+AI 执行 |
| 影视制作 | 特效、分镜、场景生成 | AI 辅助预可视化 |
| 音乐创作 | 旋律生成、编曲 | 人创概念+AI 扩展 |
| 文学写作 | 大纲、草稿生成 | 作家构思+AI 润色 |
| 游戏开发 | 资产创建、NPC 对话 | AI 加速开发流程 |

## 相关条目

- [[NaturalLanguageProcessing]]
- [[ComputerVision]]
- [[05_ComputerScience/ArtificialIntelligence/MachineLearning/INDEX|MachineLearning]]
- [[AIEthics]]
- [[AIAgents]]
- [[ModelArchitectures2026]]
- [[IndustryAIApplications]]

## 参考资料

- Ho, J. et al. (2020). "Denoising Diffusion Probabilistic Models"
- Rombach, R. et al. (2022). "High-Resolution Image Synthesis with Latent Diffusion Models"
- Brown, T. B. et al. (2020). "Language Models are Few-Shot Learners"
- OpenAI. (2023). "GPT-4 Technical Report"
- Brooks, T. et al. (2024). "Video generation models as world simulators" (Sora)
- Ouyang, L. et al. (2022). "Training language models to follow instructions with human feedback"
