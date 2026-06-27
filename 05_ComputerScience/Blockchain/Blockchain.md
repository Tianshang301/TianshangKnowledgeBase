---
aliases: [Blockchain]
tags: ['Blockchain', 'Blockchain']
created: 2026-05-16
updated: 2026-05-16
---

# 区块链技术完全指南

## 概述

区块链是一种去中心化的分布式账本技术，通过密码学保证数据的不可篡改和可追溯性。它构成了比特币、以太坊等加密数字货币的基础，并已扩展到供应链、身份认证、投票等多个领域。

---

## 一、区块链基础

### 1.1 分布式账本

区块链的核心是一个分布式账本（Distributed Ledger），所有参与者节点都持有完整的数据副本。与传统中心化数据库不同，区块链没有单一的控制点。

```
传统账本:         区块链账本:
┌──────────┐     ┌──┐ ┌──┐ ┌──┐ ┌──┐
│  银行    │     │A │ │B │ │C │ │D │
│ 中心服务器│     │  │ │  │ │  │ │  │
└──────────┘     └──┘ └──┘ └──┘ └──┘
  单点控制         所有节点一致
```

### 1.2 区块结构

每个区块包含区块头和交易数据，通过哈希指针链接成链。

```
区块结构:
┌─────────────────────────────────┐
│ 区块头 (80 字节)                │
│  ├── 版本号 (4 字节)           │
│  ├── 前一个区块哈希 (32 字节)  │
│  ├── Merkle 根 (32 字节)       │
│  ├── 时间戳 (4 字节)           │
│  ├── 难度目标 (4 字节)         │
│  └── Nonce (4 字节)            │
├─────────────────────────────────┤
│ 交易列表 (可变大小)             │
│  ├── Coinbase 交易 (挖矿奖励)  │
│  ├── 交易 1                    │
│  ├── 交易 2                    │
│  └── ...                       │
└─────────────────────────────────┘
```

### 1.3 链式结构

```
Genesis Block ← Block 1 ← Block 2 ← Block 3
     ↓             ↓          ↓          ↓
  哈希: 0x6f   哈希: 0x8a   哈希: 0x1c   哈希: 0x3b
  上一块: 0    上一块: 0x6f 上一块: 0x8a 上一块: 0x1c
```

---

## 二、哈希函数

### 2.1 SHA-256

SHA-256（Secure Hash Algorithm 256-bit）是区块链中最核心的哈希算法。它将任意长度的输入映射为固定 256 位（32 字节）的输出。

```
SHA-256("Hello")   = 185f8db32271fe25f561a6fc938b2e264306ec304eda518007d1764826381969
SHA-256("hello")   = 2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824
SHA-256("Hello!")  = 334d016f755cd6dc58c53a86e183882f8ec14f52fb05345887c8a5edd42c87b7
                ^ 加一个字符，哈希完全变化（雪崩效应）
```

### 2.2 哈希函数的安全属性

| 属性 | 描述 | 意义 |
|------|------|------|
| 抗原像性（Preimage Resistance） | 给定 $y = H(x)$，无法反推出 $x$ | 保护私钥、交易隐私 |
| 抗第二原像性（Second Preimage Resistance） | 给定 $x$，找不到 $x' \neq x$ 使得 $H(x') = H(x)$ | 防止伪造数据 |
| 抗碰撞性（Collision Resistance） | 找不到任意 $x \neq y$ 使得 $H(x) = H(y)$ | 保证交易唯一性 |
| 雪崩效应（Avalanche Effect） | 输入微小变化 → 输出完全不同的哈希 | 保证不可预测性 |

---

## 三、Merkle 树

Merkle 树是一种二叉树数据结构，用于高效验证数据完整性。

```
Merkle 树结构:
            Root (Merkle 根)
           /                \
      H12                    H34
     /    \                 /    \
  H1      H2             H3      H4
   |       |              |       |
 Tx1     Tx2            Tx3     Tx4

Merkle 证明 (证明 Tx3 在区块中):
  只需要提供 H4 和 H12 即可
  H3' = H(Tx3)
  H34' = H(H3' || H4)
  Root' = H(H12 || H34')
  比较 Root' == Root
```

Merkle 证明的空间复杂度为 $O(\log n)$，使得轻节点（仅存储 80 字节区块头）也能验证交易是否包含在区块中。

---

## 四、共识机制

### 4.1 工作量证明 (Proof of Work)

PoW 是比特币使用的共识机制。矿工通过计算哈希找到一个 Nonce 使区块头哈希小于目标值：

$$H(\text{nonce} \parallel \text{block\_header}) < \text{target}$$

```
PoW 挖矿流程:
1. 收集交易 → 构建候选区块
2. 计算区块头哈希:
   SHA256(SHA256(version || prev_hash || merkle_root || timestamp || bits || nonce))
3. 不满足条件 → nonce++ → 重新计算
4. 找到有效 nonce → 广播区块
5. 获得区块奖励（当前 3.125 BTC）
```

**难度调整**：每 2016 个区块（约 2 周）调整一次，使得平均出块时间保持在 10 分钟。

### 4.2 权益证明 (Proof of Stake)

PoS 中，验证者（Validator）通过质押代币获得出块权，而非算力竞赛。

```
PoS 特点:
  - 验证者质押 ETH (Ethereum 要求 32 ETH)
  - 按质押比例随机选择出块者
  - 诚实出块 → 获得手续费 + 新增代币
  - 恶意行为 → 质押被罚没 (Slashing)
  - 能耗: PoW 的 ~99.95%
```

### 4.3 委托权益证明 (DPoS)

DPoS 通过投票选出少量超级节点负责出块，大幅提升效率。代表项目：EOS、TRON。

### 4.4 实用拜占庭容错 (PBFT)

PBFT 适用于联盟链场景，能够在存在恶意节点的情况下达成共识。

### 4.5 共识机制对比

| 特性 | PoW | PoS | DPoS | PBFT |
|------|-----|-----|------|------|
| 出块者 | 矿工（算力竞赛） | 验证者（质押） | 选举代表 | 所有节点 |
| 最终性 | 概率性（6 次确认） | 概率性（最终性小工具） | 概率性 | 即时最终性 |
| TPS | ~7 | ~30 (ETH) | ~1000+ | ~10000+ |
| 能耗 | 极高 | 低 | 低 | 低 |
| 去中心化程度 | 高 | 中 | 低 | 低 |
| 典型应用 | Bitcoin, Litecoin | Ethereum 2.0, Cardano | EOS, TRON | Hyperledger Fabric |
| 容错比例 | 50% 算力 | 50% 权益 | 50% 代表 | 33% 节点 |

---

## 五、Bitcoin

### 5.1 交易与 UTXO 模型

比特币使用 UTXO（Unspent Transaction Output）模型，而非账户余额模型。

```
UTXO 模型:
┌─────────────────────────────────────────────┐
│ 交易 A (TxA)                                │
│ 输入: (来自 Coinbase)                       │
│ 输出: 3.5 BTC → Bob's Address (锁定脚本)    │
│       1.5 BTC → Change Address              │
└──────────────┬──────────────────────────────┘
               ↓
┌─────────────────────────────────────────────┐
│ 交易 B (TxB: Bob → Alice)                   │
│ 输入: TxA 的输出 0 (3.5 BTC)                │
│       签名 + 公钥 (解锁脚本)                │
│ 输出: 3.0 BTC → Alice's Address             │
│       0.4 BTC → Bob's Change Address        │
│       手续费: 0.1 BTC                       │
└─────────────────────────────────────────────┘

余额计算: 遍历所有交易，累加属于你的未花费输出
```

### 5.2 挖矿与难度调整

```
难度调整公式:
  target = target_max / difficulty
  
  实际出块时间 = 10 分钟 × 2016 = 20160 分钟 (2 周)
  新难度 = 旧难度 × (实际时间 / 期望时间)
```

### 5.3 区块奖励减半 (Halving)

比特币每 210,000 个区块（约 4 年）区块奖励减半：

| 时期 | 开始年份 | 区块奖励 | 阶段 |
|------|----------|----------|------|
| 第 1 次 | 2009 | 50 BTC | 创世 |
| 第 2 次 | 2012 | 25 BTC | 第一次减半 |
| 第 3 次 | 2016 | 12.5 BTC | 第二次减半 |
| 第 4 次 | 2020 | 6.25 BTC | 第三次减半 |
| 第 5 次 | 2024 | 3.125 BTC | 第四次减半 |
| ... | 2140 | 0 BTC | 总量 2100 万全部挖完 |

---

## 六、Ethereum

### 6.1 账户模型

与比特币的 UTXO 不同，以太坊使用账户模型，类似于银行账户。

```
EOA (Externally Owned Account):
  - 由私钥控制
  - 可发起交易
  - 余额 = ETH 数量
  - nonce = 交易计数

合约账户 (Contract Account):
  - 由合约代码控制
  - 由交易触发执行
  - 存储合约状态
  - 地址由创建者地址 + nonce 哈希决定
```

### 6.2 智能合约

智能合约是以太坊上的可编程合约，用 Solidity 编写，在 EVM 中执行。

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

contract SimpleAuction {
    address public beneficiary;
    uint256 public auctionEnd;
    address public highestBidder;
    uint256 public highestBid;

    constructor(uint256 _duration) {
        beneficiary = msg.sender;
        auctionEnd = block.timestamp + _duration;
    }

    function bid() external payable {
        require(block.timestamp < auctionEnd, "拍卖已结束");
        require(msg.value > highestBid, "出价不够高");
        highestBidder = msg.sender;
        highestBid = msg.value;
    }

    function withdraw() external {
        // 将出价退回给上一个最高出价者
    }
}
```

### 6.3 Gas

Gas 是执行以太坊交易和智能合约的计算费用单位。

```
Gas 计算:
  交易费用 = Gas Used × Gas Price (Gwei)
  
  简单转账: 21,000 gas
  ERC-20 转账: ~50,000 gas
  复杂合约交互: 100,000+ gas
  
  EIP-1559 费用模型:
    总费用 = Base Fee × Gas Used + Priority Fee × Gas Used
    Base Fee: 基础费用（根据网络拥堵自动调整，销毁）
    Priority Fee: 小费（给验证者）
    Gas Limit: 用户愿意支付的最大 gas 量
```

### 6.4 EVM 与 Solidity 基础

以太坊虚拟机（EVM）是一个图灵完备的虚拟机，运行智能合约字节码。

```
Solidity → Solc 编译器 → EVM Bytecode → EVM 执行

Solidity 核心概念:
  - 状态变量 (State Variables)
  - 函数修饰符 (modifier)
  - 事件 (Event)
  - 继承 (Inheritance)
  - 接口 (Interface)
  - 库 (Library)
```

---

## 七、DeFi 与 NFT

### 7.1 DeFi（去中心化金融）

DeFi 是建立在区块链上的金融应用生态，包括：

| 类别 | 代表项目 | 功能 |
|------|----------|------|
| 去中心化交易所 (DEX) | Uniswap, SushiSwap | AMM 自动做市 |
| 借贷协议 | Aave, Compound | 超额抵押借贷 |
| 稳定币 | DAI, USDC | 锚定法币价值的代币 |
| 收益聚合器 | Yearn Finance | 自动优化收益策略 |
| 衍生品 | Synthetix | 合成资产交易 |

AMM 自动做市公式 (Constant Product):

$$x \times y = k$$

其中 $x$ 和 $y$ 是流动池中两种代币的数量，$k$ 是常数。

### 7.2 NFT（非同质化代币）

NFT 使用 ERC-721 标准，每个代币都是唯一的。ERC-1155 支持半同质化代币。

```
NFT 核心标准:
  ERC-721:   每个 Token 有独立 ID, 不可分割
  ERC-1155:  批量铸造, 支持同质化/非同质化混合

NFT 元数据:
  Token ID → Token URI → JSON 元数据 → 图片/视频 (通常存储在 IPFS)
```

---

## 八、Layer 2 扩展方案

### 8.1 Rollups

Rollups 将交易在链下执行，将压缩后的证明数据提交到主链。

| 类型 | 机制 | 安全性 | 退出周期 | 代表项目 |
|------|------|--------|----------|----------|
| Optimistic Rollup | 假设交易有效，挑战期内可质疑 | 经济安全（欺诈证明） | ~7 天 | Optimism, Arbitrum |
| ZK Rollup | 零知识证明验证交易 | 密码学安全 | 即时 | zkSync, StarkNet, Scroll |

### 8.2 状态通道

状态通道允许双方在链下进行多笔交易，只在开启和关闭时写入主链。

### 8.3 Layer 2 对比

| 方案 | TPS | 费用 | 安全模型 | 通用性 |
|------|-----|------|----------|--------|
| Optimistic Rollup | ~2000 | 低 | 经济安全 | 完全兼容 EVM |
| ZK Rollup | ~2000-10000 | 极低 | 密码学安全 | 部分兼容 EVM |
| 状态通道 | 无限 | 极低 | 签名验证 | 有限场景 |
| Plasma | ~1000 | 低 | 欺诈证明 | 有限 |

---

## 九、区块链三难困境

区块链三难困境（Blockchain Trilemma）指出，区块链系统难以同时实现三个核心属性：

```
         安全性
        /    \
       /      \
      /        \
  去中心化 ──── 可扩展性

  三角关系:
  提升可扩展性 → 降低去中心化 (如: EOS, Solana)
  提升安全性   → 降低可扩展性 (如: Bitcoin)
  提升去中心化 → 降低性能 (如: 比特币 7 TPS)
```

Layer 2 和分片技术正在尝试在不牺牲去中心化和安全性的前提下提升可扩展性。

---

## 十、应用场景

### 10.1 供应链

区块链可实现供应链的全程可追溯。从原材料到终端产品，每个环节的流转记录都不可篡改。

### 10.2 数字身份

用户自主掌控 DID（去中心化身份），通过可验证凭证（Verifiable Credential）选择性披露信息。

### 10.3 投票

区块链投票可确保投票记录的不可篡改和可审计性，同时保护投票者隐私。

---

## 相关条目

- Cryptography
- [[05_ComputerScience/Cybersecurity/Cybersecurity|Cybersecurity]]
- [[07_InterdisciplinarySciences/NetworkedInformationSystems/DistributedSystems|DistributedSystems]]
- [[03_HumanitiesAndSocialSciences/Economics/INDEX|Economics]]

## 参考资源

- Bitcoin 白皮书: Satoshi Nakamoto, "Bitcoin: A Peer-to-Peer Electronic Cash System"
- Ethereum 黄皮书: Gavin Wood, "Ethereum: A Secure Decentralized Generalised Transaction Ledger"
- 《Mastering Bitcoin》— Andreas M. Antonopoulos
- 《Mastering Ethereum》— Andreas M. Antonopoulos & Gavin Wood
- Solidity 官方文档: https://docs.soliditylang.org
- OpenZeppelin 合约库: https://www.openzeppelin.com/contracts


