---
aliases:
  - LLM微调技术
  - 大语言模型微调
  - Fine-Tuning
tags:
  - LLM
  - 微调
  - PEFT
  - LoRA
  - RLHF
  - 指令微调
created: 2026-06-27
updated: 2026-06-27
---

# LLM微调技术

大语言模型（LLM）微调是在预训练模型基础上，使用特定领域或任务数据进行二次训练，使模型更好地适应目标应用场景。微调是连接通用基座模型与垂直领域应用的关键桥梁。

## 微调策略选择

### 全参数微调（Full Fine-Tuning）

- **原理**：更新模型所有参数
- **优势**：理论上能达到最佳性能
- **劣势**：计算资源需求大、易过拟合、存储成本高
- **适用场景**：数据充足、资源充裕、追求极致性能

### 参数高效微调（PEFT）

- **核心思想**：只更新少量参数，冻结大部分预训练权重
- **优势**：训练速度快、显存占用低、易于存储和切换
- **主流方法**：LoRA、Adapter、Prompt Tuning

## LoRA/QLoRA

### LoRA（Low-Rank Adaptation）

LoRA是目前最流行的参数高效微调方法：

- **核心原理**：
  - 假设模型更新矩阵是低秩的
  - 将权重更新分解为两个低秩矩阵：ΔW = BA
  - 其中 B ∈ R^(d×r)，A ∈ R^(r×k)，r << min(d,k)
  - 训练时冻结原始权重，只训练A和B

- **超参数选择**：
  - rank（r）：通常选择8-64，任务越复杂选择越大
  - alpha（α）：缩放因子，通常设置为rank的2倍
  - target_modules：应用LoRA的层，通常是attention层

```python
from peft import LoraConfig, get_peft_model

config = LoraConfig(
    r=16,
    lora_alpha=32,
    target_modules=["q_proj", "v_proj", "k_proj", "o_proj"],
    lora_dropout=0.05,
    bias="none",
    task_type="CAUSAL_LM"
)
model = get_peft_model(base_model, config)
```

### QLoRA（Quantized LoRA）

QLoRA在LoRA基础上引入量化，进一步降低显存需求：

- **核心技术**：
  - 4-bit NormalFloat（NF4）量化
  - 双重量化（Double Quantization）
  - 分页优化器（Paged Optimizer）

- **显存对比**：
  - 7B模型全参数微调：约60GB显存
  - 7B模型LoRA：约16GB显存
  - 7B模型QLoRA：约6GB显存

```python
from transformers import BitsAndBytesConfig

bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.bfloat16,
    bnb_4bit_use_double_quant=True,
)
model = AutoModelForCausalLM.from_pretrained(
    model_name, quantization_config=bnb_config
)
```

## Adapter Tuning

### 原理

- 在Transformer层之间插入小型Adapter模块
- Adapter通常包含下投影→非线性激活→上投影
- 训练时只更新Adapter参数

### 结构

```
原始层输出 → LayerNorm → Down-Projection → Activation → Up-Projection → Residual Connection
```

### 变体

- **AdapterFusion**：组合多个Adapter
- **AdapterSoup**：加权平均多个Adapter
- **MAD-X**：语言和任务Adapter分离

## Prompt Tuning与P-Tuning

### Prompt Tuning

- **方法**：在输入前添加可学习的soft prompt
- **特点**：参数量极少（通常几百到几千个参数）
- **适用**：大模型（>10B参数）效果接近全参数微调

### P-Tuning v1

- **方法**：使用LSTM或MLP编码prompt embeddings
- **改进**：prompt token可以不连续，更灵活

### P-Tuning v2

- **方法**：在每一层都添加prefix tokens
- **优势**：在小模型上也能取得好效果
- **参数量**：约0.1%-1%的模型参数

```python
from peft import PrefixTuningConfig, get_peft_model

config = PrefixTuningConfig(
    task_type="CAUSAL_LM",
    num_virtual_tokens=20,
    prefix_projection=True
)
model = get_peft_model(base_model, config)
```

## 指令微调（Instruction Tuning）

### 核心思想

- 使用"指令-输入-输出"格式的数据训练模型
- 让模型学会理解和遵循人类指令
- 提升模型的zero-shot和few-shot能力

### 数据格式

```json
{
  "instruction": "将以下英文翻译成中文",
  "input": "Hello, how are you?",
  "output": "你好，你好吗？"
}
```

### 数据质量要求

- **多样性**：覆盖多种任务类型和领域
- **准确性**：输出必须正确、高质量
- **一致性**：格式统一、风格一致
- **规模**：通常需要数千到数万条高质量数据

### 主流数据集

- **Alpaca**：斯坦福发布的52K指令数据
- **ShareGPT**：用户分享的对话数据
- **BELLE**：中文指令数据集
- **OpenAssistant**：开源助手对话数据

## 对齐技术

### RLHF（Reinforcement Learning from Human Feedback）

RLHF是让模型输出更符合人类偏好的关键技术：

**三阶段流程**：

1. **监督微调（SFT）**：使用高质量数据微调基座模型
2. **奖励模型训练**：训练一个模型来预测人类偏好
3. **PPO优化**：使用强化学习优化模型策略

```python
# 简化的RLHF流程
from trl import PPOTrainer, PPOConfig

config = PPOConfig(
    model_name="sft_model",
    learning_rate=1.41e-5,
    batch_size=64,
)
ppo_trainer = PPOTrainer(config, model, ref_model, tokenizer)
```

### DPO（Direct Preference Optimization）

DPO直接从偏好数据学习，无需训练奖励模型：

- **优势**：更简单、更稳定、计算成本更低
- **原理**：将RLHF目标转化为分类损失
- **实现**：只需要偏好对数据（chosen vs rejected）

```python
from trl import DPOTrainer

trainer = DPOTrainer(
    model=model,
    ref_model=ref_model,
    tokenizer=tokenizer,
    train_dataset=dataset,
    beta=0.1,
)
trainer.train()
```

### RLAIF（RL from AI Feedback）

- **思想**：使用AI模型代替人类提供反馈
- **优势**：可扩展、成本低、一致性好
- **实践**：使用强模型（如GPT-4）评估弱模型输出

## 微调数据准备与质量控制

### 数据收集

- **人工标注**：质量最高，成本也最高
- **模型生成**：使用强模型生成，人工筛选
- **开源数据集**：Hugging Face Hub上的公开数据集

### 数据清洗

- **去重**：移除重复或近似重复的样本
- **过滤**：移除低质量、有害、错误的样本
- **标准化**：统一格式、修正错误

### 数据配比

- **任务配比**：不同任务类型的比例平衡
- **难度配比**：简单、中等、困难样本的合理分布
- **领域配比**：不同领域数据的平衡

### 质量评估

- **人工抽检**：随机抽样人工评估
- **自动评估**：使用指标（如困惑度、BLEU）评估
- **对比评估**：与基线模型对比评估

## 训练最佳实践

### 超参数选择

- **学习率**：通常比预训练小1-2个数量级（1e-5到5e-5）
- **批大小**：根据显存调整，通常8-32
- **训练轮数**：1-3轮，避免过拟合
- **Warmup**：总步数的5-10%

### 防止过拟合

- **Early Stopping**：监控验证集损失
- **Dropout**：在LoRA中使用dropout
- **数据增强**：同义词替换、回译等
- **正则化**：L2正则化、权重衰减

### 评估策略

- **自动评估**：困惑度、BLEU、ROUGE等指标
- **人工评估**：输出质量、相关性、安全性
- **任务评估**：特定任务的基准测试（如MMLU、C-Eval）

## 工具与框架

### 训练框架

- **Hugging Face Transformers**：最流行的训练框架
- **LLaMA-Factory**：一站式LLM微调工具
- **Axolotl**：简化的微调配置
- **XTuner**：支持多种微调算法

### 评估工具

- **lm-evaluation-harness**：标准化评估框架
- **OpenCompass**：中文LLM评估平台
- **AlpacaEval**：指令跟随能力评估

## 总结

LLM微调技术正在快速发展，从全参数微调向参数高效微调演进，从单一监督学习向多阶段对齐发展。选择合适的微调策略需要综合考虑数据量、计算资源、任务需求和性能要求。高质量的训练数据是微调成功的关键因素，投入足够精力在数据准备上往往比选择算法更重要。
