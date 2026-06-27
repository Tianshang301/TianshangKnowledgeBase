---
aliases: [DistributedStorage]
tags: ['CloudComputingAndDistributedSystems', 'DistributedStorage']
created: 2026-05-16
updated: 2026-05-16
---

# 分布式存储

## 概述

分布式存储系统将数据分散存储在多台独立机器上，通过网络互联构成统一的存储资源池。它解决单机存储的容量、性能和可用性瓶颈，是现代云计算和大数据基础设施的核心。

---

## 一、分布式存储基础理论

### 1.1 CAP 定理

分布式系统在一致性（Consistency）、可用性（Availability）、分区容错性（Partition Tolerance）三者中只能同时满足两个。

```
         一致性 (C)
          /   \
         /     \
        /       \
       /         \
  可用性 (A) ──── 分区容错性 (P)

  CP: etcd, ZooKeeper, HBase
  AP: Cassandra, DynamoDB, CouchDB
  CA: 实际分布式系统中不可实现（分区必然存在）
```

### 1.2 一致性模型

| 模型 | 描述 | 强度 | 性能影响 | 典型系统 |
|------|------|------|----------|----------|
| 线性一致性 (Linearizability) | 操作瞬间生效，全局顺序 | 最强 | 高延迟 | etcd, ZooKeeper |
| 顺序一致性 (Sequential) | 每个节点内部顺序一致 | 强 | 中等 | 分布式锁 |
| 因果一致性 (Causal) | 有因果关系的事件有序 | 中等 | 较低 | COPS, 部分 CRDT |
| 最终一致性 (Eventual) | 无更新后最终一致 | 弱 | 低 | DNS, Cassandra |
| 读己写 (Read-Your-Writes) | 用户总能看到自己的写入 | 会话级 | 低 | 用户偏好设置 |
| 单调读 (Monotonic Read) | 后续读版本 ≥ 之前读版本 | 会话级 | 低 | 社交动态 |

### 1.3 数据分布策略

| 策略 | 描述 | 优点 | 缺点 |
|------|------|------|------|
| 哈希分区 (Consistent Hashing) | 哈希环映射 | 增减节点影响小 | 查询需知道 key |
| 范围分区 (Range Partitioning) | 按 key 范围分段 | 范围查询高效 | 热点数据倾斜 |
| 轮询 (Round Robin) | 依次分布 | 实现简单 | 无局部性 |
| 列表分区 (List Partitioning) | 显式指定映射 | 灵活 | 扩展性差 |

---

## 二、分布式文件系统

### 2.1 HDFS (Hadoop Distributed File System)

```
HDFS 架构:
  ┌──────────────┐
  │  NameNode    │←── 元数据 (内存中)
  │  (Active/Standby) │  文件 → Block → Datanode
  └──────┬───────┘
         │
    ┌────┼────┐
    │    │    │
  ┌─┴─┐ ┌─┴─┐ ┌─┴─┐
  │DN │ │DN │ │DN │  三副本: Rack-1 2个, Rack-2 1个
  └───┘ └───┘ └───┘
```

| 组件 | 功能 | 特性 |
|------|------|------|
| NameNode | 管理文件系统命名空间和块映射 | 单点故障（HA 需 QJM 和 Standby） |
| DataNode | 存储实际数据块 | 定期向 NameNode 发送心跳和块报告 |
| Secondary NameNode | 合并编辑日志 | 非热备，仅用于 checkpoint |

**副本放置策略：**

```
机架感知副本放置:
  副本 1: 客户端所在节点（或随机节点）
  副本 2: 不同机架的随机节点
  副本 3: 与副本 2 同机架的不同节点
  更多副本: 随机放置（限制跨机架数量）

可靠性: 默认 3 副本 → 容忍 2 个副本丢失
块大小: 默认 128MB（可配置）
```

### 2.2 Ceph

```
Ceph 架构:
  ┌──────────┐  ┌──────────┐  ┌──────────┐
  │   MON    │  │   MON    │  │   MON    │  监视器: 集群状态, Paxos
  └────┬─────┘  └────┬─────┘  └────┬─────┘
       │              │              │
  ┌────┴──────────────┴──────────────┴────┐
  │            CRUSH 算法                  │  可控哈希, 数据分布
  └──────────────────┬───────────────────┘
                      │
       ┌──────────────┼──────────────┐
   ┌───┴───┐     ┌───┴───┐     ┌───┴───┐
   │  OSD  │ ... │  OSD  │ ... │  OSD  │  对象存储守护进程
   └───────┘     └───────┘     └───────┘
       │
   ┌───┴───┐
   │  MDS  │  元数据服务器 (CephFS 需要)
   └───────┘
```

| 组件 | 全称 | 功能 |
|------|------|------|
| MON | Monitor | 维护集群状态映射（OSD Map、PG Map、CRUSH Map） |
| OSD | Object Storage Daemon | 存储数据、处理复制和恢复 |
| MDS | Metadata Server | 为 CephFS 管理文件元数据 |
| RGW | RADOS Gateway | 提供 S3/Swift 兼容对象存储接口 |

**CRUSH 算法：**

```
CRUSH (Controlled Replication Under Scalable Hashing):
  输入: (对象 o, 规则 rule)
  输出: n 个 OSD

  无需中心化映射表，客户端可直接计算数据位置
  支持多种故障域: 盘 → 主机 → 机架 → 机房

  PG (Placement Group): 对象的逻辑分组
  对象 → PG → OSD (通过 CRUSH)
  默认每 OSD 100 PG
```

---

## 三、对象存储

### 3.1 S3 API 与 MinIO

S3 (Simple Storage Service) 是 AWS 提出的对象存储标准接口：

| 概念 | 说明 |
|------|------|
| Bucket | 存储桶（全局唯一名称） |
| Object | 对象（数据 + 元数据 + 唯一 key） |
| Versioning | 对象版本控制 |
| Lifecycle Policy | 存储生命周期管理（自动沉降/删除） |
| Multipart Upload | 大文件分片上传 |

```bash
# MinIO CLI (mc) 使用示例
mc alias set myminio http://localhost:9000 accessKey secretKey
mc mb myminio/my-bucket
mc cp file.pdf myminio/my-bucket/
mc cat myminio/my-bucket/file.pdf
```

### 3.2 Cassandra

```
Cassandra 数据分布:

  Consistent Hashing Ring:
      ┌────── Node D ──────┐
      │                     │
  Node C                     Node A
      │                     │
      └────── Node B ──────┘

  vnodes (虚拟节点): 每个物理节点对应多个 Token 范围
  默认: 每个节点 256 个 vnodes
```

| 特性 | 描述 |
|------|------|
| Partition Key | 决定数据所在节点（哈希） |
| Clustering Columns | 同一分区内的排序和唯一性 |
| Hinted Handoff | 节点宕机时，协调节点代写日志 |
| Read Repair | 读取时检测不一致并修复 |
| Gossip Protocol | 节点间交换状态信息 |
| Tombstone | 删除标记，GC 后清理 |
| Compaction | SSTable 合并，清理墓碑和过时数据 |

**Gossip 协议：**

```
每个节点每秒与 1-3 个随机节点通信:
  1. 交换自身和已知节点的状态
  2. 包含: 心跳计数、生成时间、负载等
  3. 收敛时间: O(log N) 轮

同步 vs 异步修复:
  读修复 (Read Repair): 读路径上检测不一致
  反熵 (Anti-Entropy): Merkle Tree 比较差异
  修复 (Repair): nodetool repair 手动触发
```

---

## 四、键值存储

### 4.1 etcd

etcd 是分布式可靠的键值存储，核心是基于 Raft 的强一致性：

```
etcd 架构:
  Client ──▶ gRPC API ──▶ etcd Server (Raft 节点)
                              │
                    ┌─────────┼─────────┐
                    │         │         │
                 Leader    Follower  Follower
                    │         │         │
                    └─────────┼─────────┘
                              │
                            WAL (磁盘日志) + Snapshot
```

| 特性 | 说明 |
|------|------|
| API | gRPC + v3 API（基于 Revision 的多版本并发控制） |
| 存储 | BoltDB (bbolt) 底层存储引擎 |
| 租约 (Lease) | 带 TTL 的键，用于分布式锁和服务发现 |
| Watch | 监听键的变化事件 |
| 事务 | 支持 if-then-else 事务（比较-交换） |
| 快照 | 自动/手动 snapshot 压缩 WAL |

### 4.2 ZooKeeper

```
ZooKeeper 架构:
  ┌─────────────────────────────────┐
  │        ZooKeeper Service         │
  │  ┌──────┐ ┌──────┐ ┌──────┐     │
  │  │Leader│ │Follower│ │Follower│  │
  │  └──┬───┘ └──┬───┘ └──┬───┘     │
  │     └────────┼─────────┘         │
  │        Zab 原子广播协议           │
  └─────────────────────────────────┘
```

| 特性 | 说明 |
|------|------|
| Znode | 数据节点（持久/临时/顺序） |
| Watches | 一次性触发器（数据变化通知） |
| Zab | Zookeeper Atomic Broadcast，类 Paxos 共识 |
| Session | 客户端连接会话（临时 zn ode 随 session 结束而删除） |
| 典型应用 | 服务发现、配置管理、分布式锁、Leader 选举 |

**etcd vs ZooKeeper 对比：**

| 特性 | etcd | ZooKeeper |
|------|------|-----------|
| 共识协议 | Raft | Zab |
| 数据模型 | 扁平键值 | 层级树（Znode） |
| Watch | 支持 | 支持（一次性） |
| API | gRPC + JSON | 自定义 TCP 协议 |
| 多版本并发控制 | 支持（Revision） | 不支持 |
| 社区生态 | Kubernetes 原生 | Hadoop、Kafka 生态 |

---

## 五、分布式数据库

### 5.1 Spanner (Google)

Spanner 是全球分布的关系型数据库，核心创新是 TrueTime：

```
Spanner 架构:
  Universe → Zone → SpanServer
  每个 Zone 包含数千个 SpanServer

  TrueTime API:
    TT.now() 返回 [earliest, latest]
    保证外部一致性 (External Consistency)
    基于 GPS + 原子钟

  Paxos 组（每个 Tablet）:
    数据被分割为 Directory → Paxos 组
    支持 Paxos 组间的分布式事务 (2PC)
```

### 5.2 TiDB

TiDB 是兼容 MySQL 协议的分布式 NewSQL 数据库：

```
TiDB 架构:
  ┌───────────┐      ┌───────────┐      ┌───────────┐
  │   TiDB   │      │   TiDB   │      │   TiDB   │  SQL 层 (无状态)
  │  (SQL)   │      │  (SQL)   │      │  (SQL)   │
  └─────┬─────┘      └─────┬─────┘      └─────┬─────┘
        │                  │                  │
  ┌─────┴──────────────────┴──────────────────┴─────┐
  │              PD (Placement Driver)               │  元数据 + 调度
  │         (etcd 存储元数据 + Raft)                  │
  └─────┬──────────────────┬──────────────────┬─────┘
        │                  │                  │
  ┌─────┴─────┐      ┌─────┴─────┐      ┌─────┴─────┐
  │   TiKV   │      │   TiKV   │      │   TiKV   │  存储层 (Raft)
  │ (Raft)    │      │ (Raft)    │      │ (Raft)    │
  └───────────┘      └───────────┘      └───────────┘
```

| 层 | 组件 | 功能 |
|------|------|------|
| 计算层 | TiDB | MySQL 协议兼容，SQL 解析优化 |
| 调度层 | PD | 元数据管理、时间戳分配、调度决策 |
| 存储层 | TiKV | 分布式 KV 存储（Raft + RocksDB） |
| 列存引擎 | TiFlash | Raft Learner 异步复制，列式存储 |

**Percolator 事务模型：**

```
Percolator 两阶段提交:
  1. Prewrite: 写入数据并加锁
  2. Commit: 提交主锁 → 清理次级锁

  冲突检测: 锁冲突时回滚
  时间戳: PD 分配全局单调递增 TSO
```

---

## 六、一致性与复制

### 6.1 Quorum 机制

$$W + R > N$$

其中 $N$ 是副本数，$W$ 是写需确认数，$R$ 是读需确认数。

| 配置 | 特点 |
|------|------|
| $W=N, R=1$ | 强一致写，读最快 |
| $W=1, R=N$ | 强一致读，写最快 |
| $W=Quorum, R=Quorum$ | 折中（Dynamo 默认 $N=3, W=2, R=2$） |
| $W=R=1$ | 最终一致 |

### 6.2 复制策略对比

| 策略 | 描述 | 优点 | 缺点 | 代表系统 |
|------|------|------|------|----------|
| 主从复制 | 单主写入，异步/同步复制 | 写一致性简单 | 主节点瓶颈 | MySQL, PostgreSQL |
| 多主复制 | 多节点写入，冲突检测 | 多机房写入 | 冲突处理复杂 | MySQL Cluster |
| 无主复制 (Leaderless) | 任何副本可写，读时协调 | 高可用 | 读取延迟高 | Cassandra, Dynamo |

### 6.3 冲突解决

| 方法 | 描述 | 适用场景 |
|------|------|----------|
| Last-Write-Wins (LWW) | 时间戳最大的写入生效 | 可接受丢失更新的场景 |
| CRDT (Conflict-free Replicated Data Type) | 合并操作无冲突 | 协作编辑、计数器 |
| 应用层合并 | 应用自行解决冲突 | 需要业务语义的场景 |
| 向量时钟 | 检测冲突由客户端处理 | Amazon Dynamo |

---

## 相关条目

- CloudComputing
- [[ConsensusAndCoordination]]
- [[05_ComputerScience/DatabasesAndInformationSystems/BigDataTechnologies/BigDataTechnologies|BigDataTechnologies]]
- [[05_ComputerScience/DatabasesAndInformationSystems/NoSQL/NoSQL|NoSQL]]

## 参考资源

- 《Designing Data-Intensive Applications》— Martin Kleppmann
- 《分布式存储系统：原理、架构与实现》— 杨传辉
- HDFS 架构文档: https://hadoop.apache.org/docs/stable/hadoop-project-dist/hadoop-hdfs/HdfsDesign.html
- Ceph 文档: https://docs.ceph.com
- Cassandra 文档: https://cassandra.apache.org/doc/latest
- etcd 文档: https://etcd.io/docs
- TiDB 文档: https://docs.pingcap.com/zh/tidb/stable


