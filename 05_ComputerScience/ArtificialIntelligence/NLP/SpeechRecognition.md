---
aliases: [SpeechRecognition]
tags: ['05_ComputerScience', 'AI', 'NLP']
---
# 语音识别 Speech Recognition

语音识别是将语音信号自动转录为文本的技术，也称为自动语音识别（ASR）。语音识别使计算机能够理解和处理人类语音，是智能助手（如 Siri、Alexa）、语音搜索和自动字幕等应用的核心技术。

语音识别系统通常包括声学模型、发音模型和语言模型三个核心组件。声学模型学习语音信号与音素之间的映射关系；语言模型计算词序列的概率，帮助识别器选择最可能的文本输出。特征提取（如 MFCC 梅尔频率倒谱系数）将原始音频信号转换为适合处理的向量表示。端到端深度学习模型（如 Listen-Attend-Spell、Transformer）简化了传统 ASR 流程。

语音识别面临噪声环境、说话人变化、口音差异和连续语音分割等挑战。评估指标包括词错误率（WER）和实时因子（RTF）。近年来，自监督学习（如 wav2vec、Whisper）在大规模无监督语音预训练方面取得了显著进展。语音识别在呼叫中心、医疗转录、语音控制和辅助技术等领域得到广泛应用。

## 相关条目
- [[NaturalLanguageProcessing]]
- [[MachineLearning]]
- [[DigitalSignalProcessing]]
- [[HumanComputerInteraction]]
- [[DeepLearning]]
