---
aliases: [ConsensusAndCoordination]
tags: ['CloudComputingAndDistributedSystems', 'ConsensusAndCoordination']
created: 2026-05-16
updated: 2026-05-13
---

# 分布式一致性与协调

## 概述

分布式协调是分布式系统的核心挑战：如何在不可靠的网络和可能故障的节点间达成一致，实现全局有序的操作。Lamport 时钟、Paxos、Raft、2PC 等算法构成了分布式系统一致性的理论基础。

---

## 一、分布式协调的基础挑战

| 挑战 | 描述 | 常见解决方案 |
|------|------|-------------|
| 全序 (Total Order) | 所有节点对事件顺序达成一致 | 共识算法 (Paxos/Raft) |
| 互斥 (Mutual Exclusion) | 同一时刻只有一个节点访问资源 | 分布式锁 (etcd/ZK) |
| Leader 选举 | 从多个节点选出一个协调者 | Bully 算法, Raft 选举 |
| 组内成员 (Group Membership) | 维护当前活跃节点列表 | Gossip + SWIM |
| 配置管理 | 动态分发配置文件 | etcd Watch, ZK Watches |

---

## 二、逻辑时钟

### 2.1 Lamport 时钟

Lamport 时钟为分布式系统中的事件提供偏序关系（因果关系）。

**定义：**

每个节点 $i$ 维护一个计数器 $C_i$，初始为 0。

```
规则 1: 节点执行事件时，C_i = C_i + 1
规则 2: 节点发送消息 m 时，附上 C_i
规则 3: 节点接收消息 m 时，C_j = max(C_j, C_msg) + 1
```

**性质：**

$$a \to b \implies C(a) < C(b)$$

其中 $\to$ 表示 "happens-before"（因果关系）。注意逆命题不成立：$C(a) < C(b)$ 不一定意味着 $a \to b$。

### 2.2 向量时钟

向量时钟解决 Lamport 时钟无法检测并发（冲突）的问题。

**定义：**

每个节点 $i$ 维护一个向量 $V_i = [V_i[1], V_i[2], ..., V_i[n]]$，$n$ 为节点数。

```
规则 1: 节点 i 执行事件时，V_i[i] = V_i[i] + 1
规则 2: 发送消息时，附上 V_i 向量
规则 3: 接收消息时，V_j[k] = max(V_j[k], V_msg[k]) 对所有 k；然后 V_j[j] = V_j[j] + 1
```

**比较：**

| 比较 | 含义 |
|------|------|
| $V_a = V_b$ | 同一事件 |
| $V_a < V_b$（所有分量 ≤） | a 导致 b（因果关系） |
| $V_a \parallel V_b$（互不 ≤） | a 和 b 并发（冲突） |

**Lamport 时钟 vs 向量时钟：**

| 特性 | Lamport 时钟 | 向量时钟 |
|------|-------------|----------|
| 空间复杂度 | $O(1)$ | $O(n)$ |
| 因果关系检测 | 仅单向（happens-before） | 双向检测 |
| 冲突检测 | 无法检测并发 | 可检测并发事件 |
| 应用场景 | 全局排序要求不严格 | 版本冲突检测（Dynamo 式 KV） |

---

## 三、共识算法

### 3.1 Paxos

Paxos 是 Leslie Lamport 提出的共识算法族，是分布式共识的理论基石。

**Basic Paxos 角色：**

| 角色 | 职责 |
|------|------|
| Proposer (提议者) | 提出提案，包含提案编号和值 |
| Acceptor (接受者) | 接收提案，决定是否接受 |
| Learner (学习者) | 学习已达成共识的提案 |

**Basic Paxos 两阶段流程：**

```
阶段 1 (Prepare):
  Proposer → 多数 Accepters: Prepare(n)
  Accepter: 如果 n > 已承诺的最大编号 → 承诺不再接受 < n 的提案，返回已接受的最大编号提案 (如果有)

阶段 2 (Accept):
  Proposer → 多数 Accepters: Accept(n, value)
    value: 如果有返回提案则取其值，否则使用自己的值
  Accepter: 如果 n ≥ 已承诺的最大编号 → 接受提案

达成共识: 多数 Accepter 接受同一提案
```

**Multi-Paxos：**

```
优化:
  - 选举一个 Proposer 作为 Leader
  - Leader 可以跳过 Prepare 阶段直接 Accept
  - 多个提案在同一个 Leader 任期内连续提交

Paxos 问题:
  - 理解难度大 (Lamport 原论文抽象晦涩)
  - 实现中的活锁问题
  - 无强 Leader 概念，多数派切换可能导致延迟
```

### 3.2 Raft

Raft 将共识分解为三个子问题：Leader 选举、日志复制、安全性。目标是可理解性。

**节点状态：**

```
          ┌──────────┐
          │ Follower │
          └────┬─────┘
               │ 选举超时
               ▼
          ┌──────────┐
          │ Candidate│──────── 获得多数票 ──────▶ ┌────────┐
          └────┬─────┘                              │ Leader │
               │                                    └────────┘
               │ 发现更高 Term                          │
               ▼ 或 Leader 心跳超时                      │ 心跳重置
          ┌──────────┐                                  │
          │ Follower │◄──────────────────────────────────┘
          └──────────┘
```

**Leader 选举：**

```
1. Follower 收不到心跳 → 增加 Term → 转为 Candidate
2. 给自己投票 + 请求其他节点投票
3. 获得多数票 (N/2 + 1) → 成为 Leader
4. Leader 发送心跳 (AppendEntries RPC) 维持权威
5. 选举超时随机化 (150-300ms) 避免平局
```

**日志复制：**

```
Client → Leader: 接收写入请求
Leader → Follower: 并行 AppendEntries RPC

日志条目:
  ┌─────┬─────┬─────┬─────┬─────┐
  │ 1   │ 2   │ 3   │ 4   │ 5   │  ← Term
  ├─────┼─────┼─────┼─────┼─────┤
  │ x=3 │ y=1 │ x=5 │ z=2 │ x=7 │  ← 操作
  └─────┴─────┴─────┴─────┴─────┘
  ↑                     ↑
  commitIndex         lastApplied

提交条件: Leader 将日志复制到多数节点后提交
```

**安全性保证：**

| 规则 | 说明 |
|------|------|
| Leader Completeness | 被选举的 Leader 拥有所有已提交的日志 |
| Log Matching | 两节点日志在相同 index 和 term 上必然相同 |
| State Machine Safety | 节点按相同顺序应用已提交条目 |
| Committed Entry Persistence | 一旦提交，必定被后续 Leader 包含 |

**Raft vs Paxos 对比：**

| 维度 | Raft | Paxos |
|------|------|-------|
| 理解难度 | 低（可理解性优先） | 高（理论抽象） |
| 强 Leader | 是（Leader 主导一切） | 否（Multi-Paxos 可选出 Leader） |
| 日志连续性 | 强制连续（空洞必须填满） | 允许空洞 |
| 集群成员变更 | 两阶段联合共识 (Joint Consensus) | 需独立机制 |
| 流行实现 | etcd, Consul, TiKV | Google Chubby |
| 网络分区处理 | 老 Leader 隔离，新 Leader 接手 | 类似 |

### 3.3 Zab (Zookeeper Atomic Broadcast)

Zab 是 ZooKeeper 使用的共识协议，与 Raft 类似但有差异：

```
Zab 协议:
  - 类 Paxos 确保 Leader 提案被原子广播
  - 全局有序 (FIFO) 广播
  - 崩溃恢复:
    阶段 1: Leader 选举
    阶段 2: 恢复 (Discovery + Sync)
    阶段 3: 广播

Zab vs Raft:
  - Zab 不要求日志连续
  - Zab 的恢复阶段是 (epoch, zxid) 确定最新数据
  - Raft 的 Log Matching 更严格
```

### 3.4 PBFT (Practical Byzantine Fault Tolerance)

PBFT 是第一个实用的拜占庭容错算法，容忍 $f$ 个恶意节点需要 $3f+1$ 个节点。

```
PBFT 三阶段:
  1. Pre-Prepare: 主节点分配序列号
  2. Prepare: 节点间广播准备消息，收集 2f+1 个
  3. Commit: 节点间广播提交消息，收集 2f+1+1 个

View-Change (视图变更):
  当主节点故障时，所有节点发起 View-Change
  新主节点从 Checkpoint 恢复处理

性能: O(n²) 通信复杂度
适用: 联盟链 (Hyperledger Fabric)、RBFT
```

---

## 四、分布式事务

### 4.1 2PC (两阶段提交)

```
协调者 (Coordinator)                    参与者 (Participants)
     │                                       │
     │──── Prepare ────────────────────────▶ │
     │                                       │
     │◀───────── Yes/No ─────────────────── │
     │                                       │
     │──── Commit (如果全部 Yes) / Abort ──▶ │
     │                                       │
     │◀───────── Ack ────────────────────── │
```

| 阶段 | 动作 | 状态变更 |
|------|------|----------|
| Phase 1 (Prepare) | 协调者询问参与者是否可以提交 | 参与者写入 UNDO/REDO 日志，锁定资源 |
| Phase 2 (Commit/Abort) | 全 Yes → Commit；任一 No → Abort | 参与者释放资源 |

**2PC 问题：**

| 问题 | 描述 |
|------|------|
| 阻塞 (Blocking) | 协调者故障时，参与者阻塞等待（持有锁） |
| 单点故障 | 协调者宕机导致整个事务挂起 |
| 脑裂 | 网络分区时部分收到 Commit 部分未收到 |

### 4.2 3PC (三阶段提交)

3PC 在 2PC 基础上增加 CanCommit 阶段和非阻塞机制：

```
CanCommit (询问是否可提交) → PreCommit (预提交) → DoCommit (执行提交)

三阶段:
  1. CanCommit: 检查是否可提交（不写日志）
  2. PreCommit: 写入 UNDO/REDO 日志，锁定资源
  3. DoCommit: 实际提交

超时处理: 参与者在 PreCommit 后超时会自动提交（避免阻塞）
限制: 仍然无法完全解决网络分区的问题
```

### 4.3 SAGA

SAGA 是长事务的替代方案，将事务分解为多个子事务，每个子事务有对应的补偿操作：

```
SAGA 事务:
  T1 → T2 → T3 → ... → Tn

  失败时:
  T1 → T2 → T3 → ✗ → C3 → C2 → C1

  其中 Ci 是 Ti 的补偿事务 (Compensation)
```

**实现模式：**

| 模式 | 描述 | 适用场景 |
|------|------|----------|
| Choreography (编排) | 每个服务发布事件，监听执行下一步 | 简单链路，事件驱动 |
| Orchestration (编排) | 协调者中心化控制事务流程 | 复杂流程，需要集中管控 |

**事务方案对比：**

| 方案 | 一致性 | 可用性 | 隔离性 | 适用场景 |
|------|--------|--------|--------|----------|
| 2PC | 强一致 | 低（阻塞） | 高 | 短事务、高一致性需求 |
| 3PC | 弱于 2PC | 中（超时自动提交） | 中 | 需要避免阻塞 |
| SAGA | 最终一致 | 高 | 低 | 长事务、微服务 |
| TCC | 最终一致 | 高 | 可定制 | 需要预留资源的场景 |
| BASE | 最终一致 | 高 | 级别可设 | 互联网高并发 |

---

## 五、分布式锁

### 5.1 基于 etcd 的锁

```go
// etcd 分布式锁原理
lease := client.Grant(ctx, 10)        // 创建租约 (10s TTL)
txn := client.Txn(ctx).
  If(client.Compare(client.CreateRevision("/lock"), "=", 0)).
  Then(client.OpPut("/lock", "owner-1", client.WithLease(lease.ID)))
resp, _ := txn.Commit()
if resp.Succeeded {
  // 获得锁
  defer client.Revoke(ctx, lease.ID)   // 释放锁
}
```

### 5.2 Redlock (Redis 分布式锁)

```
Redlock 算法:
  1. 获取当前时间 T1
  2. 依次向 N 个 Redis 节点尝试加锁 (N=5, 超时短)
  3. 计算获取锁的时间: elapsed = now - T1
  4. 如果成功锁定 ≥ N/2 + 1 个节点 且 elapsed < TTL → 锁成立
  5. 否则 → 解锁所有已加锁节点

问题:
  - 依赖时钟同步
  - 无法保证强一致性 (Redis 异步复制)
  - Martin Kleppmann 曾撰文批评: 不安全的分布式锁
```

---

## 六、分布式 ID 生成

| 方案 | 结构 | 特点 | 缺点 |
|------|------|------|------|
| Snowflake | 41bit 时间戳 + 10bit 机器 + 12bit 序列号 | 全局唯一、趋势递增 | 时钟回拨问题 |
| UUID v4 | 128bit 随机 | 无需协调 | 无序、索引效率低 |
| UUID v7 | 48bit 时间戳 + 74bit 随机 | 有序、适合数据库索引 | 需一定随机性 |
| 数据库自增 | AUTO_INCREMENT | 实现简单 | 单点瓶颈、扩展性差 |
| Redis INCR | INCR key | 高性能 | 持久化问题 |

**Snowflake ID 结构：**

```
Snowflake 64bit:
  0 | 41bit timestamp | 10bit worker | 12bit sequence
  ↑    ↑               ↑              ↑
  符号位 毫秒级时间戳    机器标识       同一毫秒内的序列号

  时间戳: 自定义 epoch 以来的毫秒数 (支持 ~69 年)
  机器标识: 数据中心 (5bit) + 机器 (5bit) 或直接 10bit
  序列号: 每毫秒 4096 个 ID

时钟回拨处理:
  1. 记录上次最大时间
  2. 发现回拨 → 等待或报错
  3. 使用 ZooKeeper/etcd 保持机器 ID 唯一
```

---

## 相关条目

- [[DistributedSystems]]
- [[ConsensusMechanisms]]
- [[Blockchain]]
- CAPTheorem

## 参考资源

- 《分布式系统：概念与设计》— Coulouris 等
- 《Designing Data-Intensive Applications》— Martin Kleppmann
- Paxos Made Simple — Leslie Lamport
- In Search of an Understandable Consensus Algorithm (Raft) — Diego Ongaro
- ZAB: High-performance broadcast for primary-backup systems
- Practical Byzantine Fault Tolerance — Miguel Castro & Barbara Liskov
- etcd Raft 库: https://github.com/etcd-io/raft
