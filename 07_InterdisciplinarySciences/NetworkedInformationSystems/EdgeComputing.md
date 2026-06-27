---
aliases: [EdgeComputing]
tags: ['NetworkedInformationSystems', 'EdgeComputing']
created: 2026-05-16
updated: 2026-05-16
---

# 边缘计算

## 概述

边缘计算（Edge Computing）是丢种将计算、存储和网络服务从云端下沉到网络边缘（接近数据源或用户）的分布式计算范式。它并非要取代云计算，是与之协同，形成云-?端三级联动的计算连续体随睢物联网设备爆发（预计2025年全球 IoT 设备?50亿）?G 网络普及，边缘计算已成为支撑低延迟高带宽、本地隐私保护的下一代应用基硢设施?
## 丢、核心动机与定义

### 为什么需要边缘计算？

| 挑战 | 云计算方?| 边缘计算方案 |
|------|-----------|-------------|
| 延迟敏感 | 云端处理 > 100ms | 边缘处理 < 10ms |
| 带宽瓶颈 | 全量数据上传 | 本地预处?+ 关键数据上云 |
| 数据隐私 | 原始数据上云 | 数据不出本地 |
| 离线操作 | 依赖网络连接 | 本地自治运行 |
| 能?| 传输能高 | 本地计算更高?|

### 定义与关键概?
**边缘计算的三要素?*
- **邻近性（Proximity）：** 计算发生在数据产生处附近
- **实时性（Real-time）：** 毫秒级响应能?- **自主性（Autonomy）：** 不依赖云端仍可独立运?
## 二边?vs ?vs 云：三层架构对比

### 概念定位

| 维度 | 云计?| 雾计算（Fog Computing?| 边缘计算 |
|------|--------|------------------------|----------|
| **位置** | 远程数据中心 | 网络中间?| 数据源近?|
| **延迟** | 100~500ms | 10~100ms | < 10ms |
| **地理分布** | 集中?| 分布?| 高度分布?|
| **节点数量** | 数百 | 数万 | 数百?|
| **移动性支?* | 有限 | 支持 | 原生支持 |
| **计算能力** | 极大 | 中等 | 有限 |
| **管理复杂?* | ?| ?| ?|

### ??端协同架?
```
应用?←→ 云端
              ? 数据管道?←→ 边缘层（边缘节点/边缘网关?              ? 设备?←→ 终端层（传感?执行?终端设备?```

**层级职责?*
- **终端层：** 数据采集、感知简单控?- **边缘层：** 实时处理、缓存本地决策协议转?- **云端层：** 模型训练、全屢分析、长期存储管理编?
## 三边缘计算架?
### 核心架构组件

**设备边缘（Device Edge）：**
- 嵌入式 AI 芯片（NPU、TPU?- 传感器融合处?- 超低功实时计?
**本地边缘（Local Edge）：**
- 边缘网关：多协议接入、数据聚?- 边缘服务器：中强度计算本地存?- 微型数据中心：小规模部署

**云边缘（Cloud Edge）：**
- MEC（多接入边缘计算）：运营商级边缘节点
- CDN 边缘节点：内容分发加?- 区域边缘站点：中等规模计算集?
### 数据流路?
$$ \text{延迟}_{total} = \text{延迟}_{sensing} + \text{延迟}_{compute} + \min\left( \text{延迟}_{edge}, \text{延迟}_{cloud} \right) $$

**典型数据流：**
1. 终端产生数据 ?本地预处理（过滤/聚合?2. 实时推理在边缘完??本地响应
3. 非实?模型更新数据异步上传云端
4. 云端模型迭代后下发至边缘节点

## 四边缘计算框?
### 商用框架

| 框架 | 弢发商 | 核心特点 | 适用场景 |
|------|--------|---------|----------|
| AWS Greengrass | Amazon | Lambda 函数本地执行 + 设备影子 | AWS 生设?|
| Azure IoT Edge | Microsoft | 模块化容器部?+ 离线支持 | 企业 IoT 方案 |
| KubeEdge | CNCF | K8s 扩展到边?+ 云边协同 | 容器化边缘集?|
| EdgeX Foundry | Linux Foundation | 即插即用微服务架?| 工业 IoT 网关 |
| OpenYurt | 阿里?| 边缘 K8s + 自治能力 | 云边融合部署 |

### KubeEdge 架构详解

**核心组件?*
- **CloudCore?* 云端控制平面，管理边缘节?- **EdgeCore?* 边缘侧运行，含 Edged（容器管理）、EdgeMesh（服务网格）
- **Reliable Sync?* 云边消息可靠同步（云端下行边缘上行）

**关键特：**
- 离线自治：云边断连后边缘独立运行
- 边缘 AI：集成 Sedna 推理框架
- 轻量化：EdgeCore 适配资源受限设备

## 五计算卸载策?
### 问题建模

**卸载决策变量?* $a_i \in \{0, 1\}$?表示本地执行?表示卸载到边缘）

**优化目标?*
$$ \min_{a} \sum_{i=1}^{N} \left( \alpha \cdot \text{延迟}_i(a_i) + \beta \cdot \text{能}_i(a_i) \right) $$

**约束条件?*
- 网络带宽限制?\sum_i R_i \cdot a_i \leq B$
- 边缘节点计算能力?\sum_i C_i \cdot a_i \leq F_{edge}$
- 任务截止时间?T_i(a_i) \leq D_i$

### 求解方法

- **贪心策略?* 高计算密度任务优先卸?- **动规划：** 适用于已知任务特征的小规模场?- **深度强化学习?* DQN/DDPG 自应卸载策略
- **博弈论：** 多用户竞争边缘资源的纳什均衡

## 六边缘 AI

### 模型压缩抢?
模型压缩是边缘 AI 的前提将大模型配到资源受限设备上?
**量化（Quantization）：**

$$ Q(x) = \text{round}\left( \frac{x - \text{min}}{\Delta} \right) \cdot \Delta + \text{min}, \quad \Delta = \frac{\text{max} - \text{min}}{2^b - 1} $$

- INT8量化：模型体积缩?倍，速度提升2~4?- 混合精度：敏感层保持 FP16，非敏感层 INT8
- 训练后量?vs 量化感知训练

**剪枝（Pruning）：**
- 结构化剪枝：移除整个通道/卷积?- 非结构化剪枝：移除单个权重（霢稢疏硬件支持）
- 迭代剪枝：训??剪枝 ?微调循环

**知识蒸馏（Knowledge Distillation）：**

$$ \mathcal{L}_{distill} = \sum_i \mathcal{L}_{CE}\left( \sigma\left( \frac{z_s^{(i)}}{T} \right), \sigma\left( \frac{z_t^{(i)}}{T} \right) \right) $$

- 教师模型（大模型）→ 学生模型（小模型?- 温度参数 T 控制软标签平滑度
- 结构设计：学生网络架构与教师解?
### 端侧推理框架

| 框架 | 弢发?| 支持硬件 | 特点 |
|------|--------|---------|------|
| TensorFlow Lite | Google | CPU/GPU/NPU | 朢广泛的移动端框架 |
| Core ML | Apple | Apple Silicon | 深度集成 iOS/macOS |
| ONNX Runtime | Microsoft | 跨平?| 弢放标准，模型互?|
| NCNN | Tencent | CPU/Vulkan | 手机端极致优?|
| OpenVINO | Intel | Intel CPU/GPU/VPU | x86平台优化 |
| TIDL | TI | TI DSP/EVE | 嵌入式 DSP 优化 |

### 联邦学习（Federated Learning?
**核心思想?* 数据不移动，模型移动

$$ w^{t+1} = \sum_{k=1}^{K} \frac{n_k}{n} w_k^{t+1}, \quad w_k^{t+1} = w^t - \eta \nabla \mathcal{L}_k(w^t) $$

- 本地数据不出设备 ?满足隐私合规
- 各设备本地训练后聚合梯度/权重
- 挑战：Non-IID 数据分布、信效率、安全聚?
## 七边缘原生应?
### 自动驾驶

**实时感知处理?*
- 摄像头：YOLO/Transformer 实时目标棢?- LiDAR：PointPillar/RangeDet 3D 棢?- 多传感器融合：BEV（Bird's Eye View）表?
**关键约束?* 端到端感知延?< 100ms，决策延?< 50ms

### 工业物联网（IIoT?
**预测性维护：**
- 振动信号分析：FFT 频谱 ?CNN 分类
- 异常棢测：自编码器重构误差
- 剩余寿命（RUL）预测：LSTM 时序模型

**典型边缘部署?*
- PLC + 边缘网关采集机床数据
- 边缘运行轻量推理模型
- 仅异常样本和模型更新上云

### 智能零售

- 边缘摄像头实时客流统?- 商品识别与自动结?- 货架缺货棢测告?
### 智慧城市

- 边缘视频分析：车牌识别人群密?- 智能路灯控制
- 环境参数实时监测与响?
## 八边缘安?
### 安全威胁

| 威胁?| 具体威胁 | 影响 |
|--------|---------|------|
| 物理设备?| 设备窃取、篡改侧信道攻击 | 密钥泄露、恶意篡?|
| 网络?| MitM、DoS、重放攻?| 数据截获、服务中?|
| 平台?| 容器逃镜像投?| 边缘节点被控 |
| 应用?| 模型窃取、对抗攻?| AI 模型被盗、错误输?|

### 安全抢?
**可信执行环境（TEE）：**
- Intel SGX / ARM TrustZone
- 敏感计算在硬件隔离区执行
- 即使 OS 被攻破，数据仍安?
**远程证明（Remote Attestation）：**
- 边缘节点向云端证明自身软?固件完整?- 基于 TPM 的度量报?- 证明日志链：启动→运行时→应用层

**轻量级加密：**
- 椭圆曲线密码（ECC）代替 RSA（同样安全等级下密钥更短?- 轻量级对称加密：AES-CCM / ChaCha20-Poly1305

## 九?G 与边缘计算融?
### 多接入边缘计算（MEC?
**ETSI MEC 标准化架构：**
- MEC Host：虚拟化基础设施 + 平台能力
- MEC App：在网络边缘运行的第三方应用
- MEC Orchestrator：全屢资源管理和编?
**5G+MEC 关键能力?*
- 超低延迟? 1ms 空口 + < 10ms 端到端）
- 定位服务：厘米级室内定位
- 带宽：单用户 Gbps 级率

### 网络切片（Network Slicing?
$$ \text{切片}_i = \left\{ \text{RAN 切片}, \text{传输网切片}, \text{核心网切片} \right\} $$

- 每切片专有 SLA（延迟带宽可靠）
- 边缘节点可按切片专属部署应用
- eMBB 切片：大带宽（视频分析）
- uRLLC 切片：低延迟（工业控制）
- mMTC 切片：海量连接（传感器）

## 十资源受限设备管?
### 设备生命周期管理

**OTA 升级机制?*
1. 增量差分升级（减小升级包大小?2. 双分?AB 分区：失败自动回?3. 灰度发布：小范围验证后全量推?
**配置管理?*
- 声明式设备配置（类似 K8s?- 设备孪生（Digital Twin）：云端维护设备状映?
### 功优化策?
**动电压频率调整（DVFS）：**
$$ P = C \cdot V^2 \cdot f $$

- 空闲时降低频率和电压
- 根据任务负载动调?
**睡眠模式管理?*
- 深度睡眠：仅 RTC 运行
- 异步唤醒：硬件触发器唤醒来处?
## 参资?
- Shi W, et al. *Edge Computing: Vision and Challenges*. IEEE Internet of Things Journal, 2016
- Satyanarayanan M. *The Emergence of Edge Computing*. Computer, 2017
- ETSI. *Multi-access Edge Computing (MEC) Framework and Reference Architecture*, 2019
- AWS. *AWS Greengrass Developer Guide*
- CNCF. *KubeEdge Documentation*
- Jacob B, et al. *Quantization and Training of Neural Networks for Efficient Integer-Arithmetic-Only Inference*. CVPR, 2018
- Hinton G, et al. *Distilling the Knowledge in a Neural Network*. NIPS Workshop, 2014
- McMahan B, et al. *Communication-Efficient Learning of Deep Networks from Decentralized Data*. AISTATS, 2017

## 相关条目

[[04_EngineeringAndTechnology/ComputerAndInformationSciences/ComputerNetworks|ComputerNetworks]], [[DistributedSystems]], [[05_ComputerScience/Cybersecurity/Cybersecurity|Cybersecurity]], CloudComputing


