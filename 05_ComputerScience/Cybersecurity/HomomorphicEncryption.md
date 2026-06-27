---
aliases:
  - 同态加密
  - Homomorphic Encryption
  - HE
  - FHE
tags:
  - cryptography
  - privacy-preserving
  - homomorphic-encryption
  - cybersecurity
  - computation-on-encrypted-data
created: 2026-06-28
updated: 2026-06-28
---

# 同态加密 (Homomorphic Encryption)

## 1. 定义与核心概念

**同态加密**是一种特殊的加密方案，允许在**密文上直接进行计算**，无需解密。计算结果解密后，与在明文上执行相同操作的结果一致。

### 1.1 数学定义

对于加密函数 $E$ 和解密函数 $D$，同态加密满足：

$$D(E(a) \oplus E(b)) = a + b$$
$$D(E(a) \otimes E(b)) = a \times b$$

其中 $\oplus$ 和 $\otimes$ 分别是密文上的加法和乘法操作。

### 1.2 核心价值

- **数据隐私**：数据全程加密，计算方无法看到原始数据
- **计算外包**：将计算任务委托给不可信的第三方
- **合规性**：满足数据保护法规（GDPR、HIPAA）要求

### 1.3 历史背景

- **1978年**：Rivest 等人首次提出同态加密概念
- **2009年**：Craig Gentry 构造出第一个全同态加密方案（基于理想格）
- **2020s**：性能大幅提升，开始走向实用化

## 2. 同态加密类型

### 2.1 部分同态加密 (Partially Homomorphic Encryption, PHE)

**定义**：仅支持一种运算（加法或乘法）的无限次操作。

**代表方案**：

| 方案 | 支持运算 | 基于问题 | 特点 |
|------|---------|---------|------|
| **RSA** | 乘法 | 大整数分解 | 经典方案，效率高 |
| **ElGamal** | 乘法 | 离散对数 | 支持重随机化 |
| **Paillier** | 加法 | 复合剩余类 | 加法同态，应用广泛 |
| **Benaloh** | 加法 | 同余方程 | 小消息空间 |

**应用场景**：
- 电子投票（Paillier）
- 隐私保护的数据聚合
- 简单的统计计算

### 2.2 分级同态加密 (Leveled Homomorphic Encryption, LHE)

**定义**：支持加法和乘法，但乘法次数有上限（由电路深度决定）。

**代表方案**：
- **BGV (Brakerski-Gentry-Vaikuntanathan)**：基于 RLWE 问题
- **BFV (Brakerski/Fan-Vercauteren)**：BGV 的变体，更高效
- **CKKS (Cheon-Kim-Kim-Song)**：支持近似浮点计算

**特点**：
- 无需 Bootstrapping
- 性能优于全同态加密
- 实际应用中最常用的类型

### 2.3 全同态加密 (Fully Homomorphic Encryption, FHE)

**定义**：支持加法和乘法的无限次操作，即任意计算。

**核心技术**：
- **Bootstrapping**：对密文进行"自举"操作，降低噪声，实现无限次计算
- **密文刷新**：定期刷新密文以控制噪声增长

**代表方案**：
- **Gentry 原始方案**：基于理想格，理论突破但效率极低
- **TFHE (Fast Fully Homomorphic Encryption over the Torus)**：支持布尔电路，速度快
- **OpenFHE**：开源 FHE 库，支持多种方案

## 3. 核心方案详解

### 3.1 BGV 方案

**全称**：Brakerski-Gentry-Vaikuntanathan

**基础问题**：Ring Learning With Errors (RLWE)

**特点**：
- 支持整数运算
- 使用模切换（Modulus Switching）控制噪声
- 适合精确计算场景

**参数选择**：
- 多项式环度 $n$
- 模数 $q$
- 噪声分布参数 $\sigma$

### 3.2 BFV 方案

**全称**：Brakerski/Fan-Vercauteren

**特点**：
- BGV 的简化变体
- 使用缩放（Scaling）代替模切换
- 更易于理解和实现

**优化技术**：
- **Batching**：将多个明文打包到一个密文中（SIMD）
- **Relin**：重线性化，降低密文大小
- **Rotation**：密文元素旋转

### 3.3 CKKS 方案

**全称**：Cheon-Kim-Kim-Kong-Song

**核心创新**：支持**近似浮点数计算**

**特点**：
- 适合机器学习、科学计算等需要浮点运算的场景
- 计算结果有精度损失，但可控
- 支持 Batch 编码

**应用场景**：
- 隐私保护的机器学习推理
- 加密数据分析
- 安全的科学计算

### 3.4 TFHE 方案

**全称**：Torus Fully Homomorphic Encryption

**特点**：
- 基于布尔电路（门级操作）
- Bootstrapping 速度快（毫秒级）
- 适合逻辑运算和查找表

**核心操作**：
- **Gate Bootstrapping**：每次门操作后刷新密文
- **Programmable Bootstrapping**：支持任意函数计算

**应用场景**：
- 加密数据库查询
- 隐私保护的身份验证
- 安全的比较操作

## 4. 性能演进

### 4.1 早期方案 (2009-2015)

**Craig Gentry 的突破**：
- 2009 年博士论文：基于理想格的 FHE
- 单次操作耗时数十分钟
- 密文膨胀数万倍

**后续改进**：
- **BGV (2012)**：分级同态，性能提升
- **BFV (2012)**：进一步简化
- **GSW (2013)**：基于近似特征向量

### 4.2 中期发展 (2016-2020)

**CKKS (2017)**：近似计算，机器学习应用爆发

**TFHE (2016)**：快速 Bootstrapping，布尔电路

**性能提升**：
- 单次操作：秒级 → 毫秒级
- 密文膨胀：万倍 → 千倍

### 4.3 现代 FHE (2021-2026)

**性能提升 10000x**：
- 算法优化：更高效的 Bootstrapping
- 工程优化：SIMD、批处理、内存优化
- 硬件加速：专用芯片和指令集

**实用化里程碑**：
- 2022 年：Intel HEXL 加速库发布
- 2023 年：DARPA DPRIVE 项目原型
- 2024 年：首个商业级 FHE 应用
- 2025 年：FHE 性能达到明文计算的 100x 以内

## 5. 硬件加速

### 5.1 Intel HEXL (Homomorphic Encryption Acceleration Library)

**特点**：
- 专用指令集优化
- 支持 AVX-512 向量化
- 与 Microsoft SEAL 集成

**性能**：多项式乘法加速 3-7 倍

### 5.2 DARPA DPRIVE 项目

**全称**：Data Protection in Virtual Environments

**目标**：开发专用 FHE 加速芯片

**参与方**：
- Intel、IBM、Duality Technologies 等
- 目标：FHE 性能达到明文的 100 倍以内

**进展**：
- 2023 年：原型芯片流片
- 2025 年：性能验证，达到预期目标

### 5.3 GPU 加速

**CUDA/FHE**：
- NVIDIA GPU 并行化多项式运算
- cuFHE 库：GPU 加速的 FHE 实现
- 性能提升：10-100 倍

### 5.4 FPGA 实现

**特点**：
- 可定制的硬件流水线
- 低功耗、高吞吐
- 适合嵌入式和边缘场景

## 6. 应用场景

### 6.1 隐私保护机器学习

**加密推理**：
- 客户端加密输入数据
- 服务器在密文上执行模型推理
- 客户端解密得到预测结果

**框架**：
- **CrypTFlow2**：微软的隐私保护推理框架
- **HELR**：基于 HE 的逻辑回归
- **GAZELLE**：混合协议（HE + GC）

### 6.2 加密数据库查询

**场景**：
- 用户查询加密数据库
- 服务器在密文上执行查询
- 返回加密结果，用户解密

**技术**：
- **SQL on Encrypted Data**：加密 SQL 执行
- **PIR (Private Information Retrieval)**：隐私保护的信息检索

### 6.3 安全多方计算 (MPC)

**HE + MPC**：
- 同态加密作为 MPC 的基础组件
- 减少交互轮数
- 提高通信效率

**协议**：
- **SPDZ**：基于 HE 的预处理 MPC
- **ABY3**：三方安全计算

### 6.4 其他应用

- **电子投票**：加密投票计票
- **隐私保护统计**：加密数据分析
- **区块链隐私**：零知识证明与 HE 结合

## 7. 开源框架

### 7.1 Microsoft SEAL

**特点**：
- 支持 BFV 和 CKKS 方案
- C++ 实现，有 Python 封装
- 工业级优化

**应用**：
- Microsoft 的隐私保护 AI 服务
- 大量学术研究

### 7.2 OpenFHE

**特点**：
- 支持所有主流方案（BGV、BFV、CKKS、TFHE）
- 模块化设计，易于扩展
- 活跃的开源社区

**应用**：
- 研究和原型开发
- 教育和学习

### 7.3 Zama / Concrete

**Zama**：
- 专注于 TFHE 方案
- 开发 Concrete 框架
- 支持 Python 前端

**Concrete**：
- 将 Python 函数编译为 FHE 电路
- 自动优化参数选择
- 适合快速原型开发

### 7.4 PALISADE

**特点**：
- Lattice Cryptography 库
- 支持多种 HE 方案
- 美国政府资助项目

**注意**：PALISADE 已合并到 OpenFHE

## 8. 2025-2026 年最新进展

### 8.1 性能突破

**FHE 性能提升 10000x**：
- 算法层面：更高效的 Bootstrapping 技术
- 工程层面：SIMD、向量化、内存优化
- 硬件层面：专用加速器

**实际性能**：
- 2020 年：单次操作 ~1 秒
- 2025 年：单次操作 ~0.1 毫秒
- 2026 年：接近实用化水平

### 8.2 开源框架成熟

**Zama Concrete**：
- 2025 年发布 2.0 版本
- 支持复杂 Python 函数编译
- 性能优化显著

**OpenFHE**：
- 持续更新，支持最新算法
- 社区活跃，文档完善

**Intel HEXL 2.0**：
- 支持更多 HE 方案
- 与主流框架深度集成

### 8.3 商业化应用

**隐私保护 AI 服务**：
- 云厂商提供 FHE 加速实例
- 医疗、金融领域试点应用

**标准化进展**：
- ISO/IEC 18033-7：同态加密标准
- NIST 后量子密码标准化：部分 HE 方案入选

### 8.4 与其他技术融合

**FHE + ZKP**：
- 同态加密 + 零知识证明
- 验证计算正确性而不泄露数据

**FHE + MPC**：
- 混合协议，平衡安全性和效率
- 减少通信开销

## 9. 挑战与开放问题

### 9.1 计算开销

**现状**：FHE 仍比明文计算慢 1000 倍以上

**原因**：
- 大整数运算
- 噪声管理
- Bootstrapping 开销

**解决方向**：
- 专用硬件加速
- 算法优化
- 混合协议

### 9.2 密文膨胀

**问题**：密文大小远大于明文

**数据**：
- 明文：1 字节
- 密文：数千字节（膨胀数千倍）

**影响**：
- 存储开销
- 通信带宽
- 内存消耗

**解决方案**：
- 更高效的编码方案
- 压缩技术
- 批处理（Batching）

### 9.3 参数选择

**挑战**：
- 参数选择影响安全性和性能
- 不同应用需要不同参数
- 自动参数选择仍不成熟

**工具**：
- **HE Standard**：参数推荐
- **lattice-estimator**：安全性评估
- **自动调参**：机器学习辅助

### 9.4 编程复杂度

**问题**：
- 需要理解底层加密原理
- 算法适配困难
- 调试困难

**解决方案**：
- 高级编程接口（如 Concrete）
- 编译器优化
- 自动化工具链

## 10. 参考资源

### 10.1 经典论文

- Gentry, "Fully Homomorphic Encryption Using Ideal Lattices", STOC 2009
- Cheon et al., "Homomorphic Encryption for Arithmetic of Approximate Numbers", ASIACRYPT 2017 (CKKS)
- Chillotti et al., "TFHE: Fast Fully Homomorphic Encryption over the Torus", 2016

### 10.2 学习资源

- [HomomorphicEncryption.org](https://homomorphicencryption.org/) - 标准和资源
- [Microsoft SEAL 文档](https://github.com/microsoft/SEAL) - 实践教程
- [OpenFHE 文档](https://openfhe.org/) - 学习资源

### 10.3 开源项目

- [Microsoft SEAL](https://github.com/microsoft/SEAL) - 工业级 HE 库
- [OpenFHE](https://github.com/openfheorg/openfhe-development) - 开源 HE 库
- [Concrete](https://github.com/zama-ai/concrete) - Zama 的 FHE 框架
- [Intel HEXL](https://github.com/intel/hexl) - HE 加速库
