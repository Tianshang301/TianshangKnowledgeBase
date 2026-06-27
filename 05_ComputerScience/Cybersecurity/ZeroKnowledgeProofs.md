---
aliases:
  - 零知识证明
  - Zero-Knowledge Proofs
  - ZKP
  - ZK Proofs
tags:
  - cryptography
  - blockchain
  - privacy
  - cybersecurity
  - proof-systems
created: 2026-06-28
updated: 2026-06-28
---

# 零知识证明 (Zero-Knowledge Proofs)

## 1. 基本定义

零知识证明（Zero-Knowledge Proof, ZKP）是一种密码学协议，允许**证明者（Prover）**在不泄露任何额外信息的前提下，向**验证者（Verifier）**证明某个陈述（statement）为真。

核心思想：验证者除了"该陈述为真"这一事实外，无法获得任何其他知识。

### 1.1 直觉理解

经典比喻——阿里巴巴的洞穴：

- 洞穴内有一道需要咒语才能打开的门
- 证明者进入洞穴并从另一侧走出
- 验证者只需观察证明者能从正确方向出现，即可确信证明者知道咒语
- 全程验证者未获知咒语本身

### 1.2 形式化定义

一个零知识证明系统是一个三元组 $(P, V, S)$，其中：

- $P$ 是证明者算法
- $V$ 是验证者算法
- $S$ 是模拟器（Simulator），用于证明零知识性

## 2. 三个核心性质

### 2.1 完整性 (Completeness)

若陈述为真，且证明者诚实地执行协议，则验证者必然接受。

$$\Pr[\langle P(x,w), V(x) \rangle = 1] = 1$$

- $x$ 是公开输入
- $w$ 是秘密见证（witness）

### 2.2 可靠性 (Soundness)

若陈述为假，则任何（即使是恶意的）证明者都无法使验证者接受，除了极小概率外。

$$\Pr[\langle P^*(x), V(x) \rangle = 1] \leq \text{negl}(\lambda)$$

- $\text{negl}(\lambda)$ 是可忽略函数
- $\lambda$ 是安全参数

### 2.3 零知识性 (Zero-Knowledge)

验证者无法从交互中获得除"陈述为真"之外的任何信息。存在模拟器 $S$，使得验证者无法区分真实交互与模拟交互。

$$\text{View}_V[\langle P(x,w), V(x) \rangle] \approx_c S(x)$$

- $\approx_c$ 表示计算不可区分

## 3. 证明系统分类

### 3.1 交互式证明 (Interactive Proofs, IP)

- 证明者与验证者之间进行多轮交互
- 验证者通过随机挑战降低欺骗概率
- 经典例子：图同构的零知识证明

### 3.2 非交互式零知识证明 (NIZK)

- 证明者生成单一证明，验证者可独立验证
- 通常依赖 Common Reference String (CRS) 或 Random Oracle
- 实际应用中更高效

### 3.3 简洁非交互式知识论证 (SNARK)

- **S**uccinct：证明大小为常数或对数级
- **N**on-interactive：无需交互
- **AR**gument：计算可靠性（非信息论可靠性）
- of **K**nowledge：证明者确实拥有见证

### 3.4 可扩展透明知识论证 (STARK)

- **S**calable：证明者和验证者均为准线性时间
- **T**ransparent：无需可信设置，仅依赖随机预言机
- 抗量子计算攻击

## 4. 经典协议详解

### 4.1 Schnorr 协议

用于证明离散对数知识的 Σ-protocol：

**公共参数**：群 $G$，生成元 $g$，元素 $h = g^x$

**协议流程**：

1. **承诺**：证明者选择随机 $r$，发送 $t = g^r$
2. **挑战**：验证者发送随机挑战 $c$
3. **响应**：证明者发送 $s = r + cx \mod q$
4. **验证**：验证者检查 $g^s = t \cdot h^c$

**特点**：

- 3轮交互
- 可通过 Fiat-Shamir 变换转为非交互式
- 安全性基于离散对数假设（DL Assumption）

### 4.2 zk-SNARKs

#### 4.2.1 计算到电路的转换

1. 将计算表示为算术电路（Arithmetic Circuit）
2. 转换为 R1CS（Rank-1 Constraint System）
3. 转换为 QAP（Quadratic Arithmetic Program）

#### 4.2.2 Groth16 (2016)

- 证明大小：仅 3 个群元素（约 192 bytes）
- 验证时间：常数级，约 1ms
- 需要电路特定的可信设置（Circuit-specific CRS）
- 当前最广泛使用的 SNARK 方案

#### 4.2.3 PLONK (2019)

- 基于多项式承诺方案（Polynomial Commitment Scheme）
- 通用可信设置（Universal Trusted Setup）
- 支持自定义门（Custom Gates）和查找表（Lookup Tables）
- 证明大小约 400-500 bytes

#### 4.2.4 其他 SNARK 方案

| 方案 | 年份 | 可信设置 | 证明大小 | 特点 |
|------|------|----------|----------|------|
| Pinocchio | 2013 | Circuit-specific | ~288B | 首个实用 SNARK |
| Groth16 | 2016 | Circuit-specific | ~192B | 最小证明 |
| PLONK | 2019 | Universal | ~450B | 灵活性高 |
| Halo2 | 2021 | 无 | ~500B | 递归证明 |
| HyperPlonk | 2022 | Universal | ~400B | 高效多项式承诺 |

### 4.3 zk-STARKs

**核心特点**：

- 基于哈希函数和 FRI（Fast Reed-Solomon IOP）
- 无需可信设置（Transparent Setup）
- 证明大小较大（50-200 KB）
- 证明生成速度快于 SNARKs
- 抗量子计算攻击

**FRI 协议**：

- 多项式低度测试（Low-Degree Testing）
- 递归折叠多项式
- 基于 Reed-Solomon 纠错码

## 5. 技术演进

### 5.1 从交互式到非交互式

```
交互式证明 (IP)
    ↓ Fiat-Shamir Transform
非交互式证明 (NIZK)
    ↓ 可信设置优化
通用 SNARK (Universal SNARK)
```

### 5.2 可信设置的演进

1. **Circuit-specific CRS**：每个电路需要单独的可信设置仪式
2. **Universal CRS**：一次设置，适用于任意电路（如 PLONK 的 SRS）
3. **Transparent Setup**：无需可信设置，仅依赖公共随机性（如 STARKs）
4. **Updatable CRS**：多方参与的可更新设置（如 SONIC）

### 5.3 递归证明 (Recursive Proofs)

- 证明的证明：一个证明可以验证另一个证明
- Halo：首个无需可信设置的递归证明
- IVC（Incrementally Verifiable Computation）：增量可验证计算
- 应用：区块链轻客户端、状态压缩

## 6. 应用场景

### 6.1 区块链隐私

#### Zcash (Zcash)

- 使用 Groth16 实现屏蔽交易（Shielded Transactions）
- 隐藏发送方、接收方和交易金额
- Orchard 升级使用 Halo 2，移除可信设置

#### Tornado Cash

- 基于 Tornado Mixer 的隐私协议
- 使用 Merkle Tree + 零知识证明
- 断开存款和取款地址之间的关联
- 2022 年被美国 OFAC 制裁

#### 隐私 Layer 2

- Aztec Network：隐私 Rollup
- zk.money：隐私支付协议

### 6.2 身份认证

- **匿名凭证**：证明拥有有效凭证而不泄露身份
- **选择性披露**：仅证明属性的特定部分（如年龄 > 18）
- **去中心化身份**：DID + ZKP 实现隐私保护的身份验证

### 6.3 可验证计算

- **外包计算**：云服务器执行计算并提供 ZKP 证明结果正确
- **链下计算链上验证**：Rollup 的核心原理
- **ZK-Rollup**：zkSync、StarkNet、Polygon zkEVM

### 6.4 供应链与审计

- 证明合规性而不泄露商业秘密
- 财务审计中的隐私保护
- 供应链溯源的真实性验证

## 7. 2025-2026 年最新进展

### 7.1 FHE + ZKP 结合

全同态加密（FHE）与零知识证明的结合：

- **可验证 FHE 计算**：证明 FHE 密文上的计算正确执行
- **应用场景**：隐私保护的机器学习推理、隐私 DeFi
- **项目代表**：Zama、Fhenix

### 7.2 ZKML（零知识机器学习）

- 将机器学习推理过程转化为 ZK 电路
- 证明模型确实在特定输入上产生特定输出
- 不泄露模型权重和输入数据
- **挑战**：神经网络的非线性激活函数电路开销巨大
- **进展**：Giza、Modulus Labs、Risc Zero 的 zkML 引擎

### 7.3 ZK 协处理器

- 专用硬件加速 ZKP 证明生成
- **GPU 加速**：Ingonyama 的 ICICLE 库
- **FPGA/ASIC**：专用 ZK 芯片（如 Cysic、Ulvetanna）
- **性能提升**：10-100 倍证明速度提升

### 7.4 新型证明系统

- **Nova/SuperNova**：高效的递归证明方案
- **Plonky2/3**：结合 PLONK 和 FRI 的高效系统
- **HyperPlonk**：多元线性多项式承诺
- **Binius**：基于二进制域的高效证明系统

## 8. 性能挑战与优化

### 8.1 证明生成时间

| 系统 | 电路规模 | 证明时间 | 硬件 |
|------|----------|----------|------|
| Groth16 | 100万约束 | ~10s | CPU |
| PLONK | 100万约束 | ~30s | CPU |
| STARK | 100万约束 | ~5s | CPU |
| GPU加速 Groth16 | 100万约束 | ~1s | GPU |

### 8.2 验证成本

- SNARKs：常数级验证（3个配对运算）
- STARKs：对数级验证（$O(\log^2 n)$）
- 链上验证：Gas 成本约 200,000-500,000

### 8.3 电路复杂度优化

- **自定义门**：减少约束数量
- **查找表**：高效处理非线性运算
- **递归折叠**：分摊验证成本
- **算术化方案优化**：从 R1CS 到 Plonkish 到 AIR

## 9. 学习资源与工具

### 9.1 开发框架

- **circom**：通用 ZK 电路编程语言
- **Halo2**：Zcash 团队的 Rust 证明库
- **arkworks**：Rust 密码学工具库
- **Cairo**：StarkNet 的 ZK 语言
- **Noir**：Aztec 的通用 ZK DSL

### 9.2 推荐阅读

- Boneh & Shoup: *Graduate Course in Applied Cryptography*
- ZKP MOOC (Berkeley)
- ZK Whiteboard Sessions
- Proof Engineering (0xPARC)

## 10. 相关链接

- [[Cryptography]] - 密码学基础
- [[Blockchain]] - 区块链技术
- [[HomomorphicEncryption]] - 同态加密
- [[SecureMultiPartyComputation]] - 安全多方计算
