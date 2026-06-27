---
aliases: [分布式数据库与 NewSQL]
tags: ['DatabasesAndInformationSystems', 'NoSQL', '分布式数据库与 NewSQL']
---

# 分布式数据库与 NewSQL

## 一、分布式数据库概述

分布式数据库将数据分布在多个物理节点上，通过网络连接构成统一的数据库系统。随着互联网应用的规模增长，单机数据库在容量、吞吐和可用性方面面临瓶颈，分布式架构成为必然选择。

分布式数据库的设计面临 CAP 理论约束：一致性(Consistency)、可用性(Availability)和分区容忍性(Partition tolerance)三者不可同时完美满足。不同系统在一致性模型上做出不同取舍——从强一致到最终一致存在连续谱。

## 二、数据分区策略

### 2.1 水平分区

水平分片(horizontal sharding)将表的行分布在不同节点上。常见策略包括：

- **范围分区**：按主键或分区键值的连续范围分配。范围查询效率高，但可能产生热点。
- **哈希分区**：对分区键计算哈希值取模分配，数据分布均匀但范围查询需广播。
- **列表分区**：按枚举值显式指定分区。

### 2.2 一致性哈希

一致性哈希在节点增减时最小化数据迁移量。哈希环上的每个节点负责顺时针方向到下一节点之间的数据范围。虚拟节点技术改善数据分布不均问题。

```
哈希环：
   [N1] ← 数据范围 [N3, N1)
  /      \
[N2]     [N4] ← 数据范围 [N1, N4)
  \      /
   [N3] ← 数据范围 [N4, N2)
```

### 2.3 分区键选择

分区键选择直接影响系统性能。良好分区键应满足：数据分布均匀、查询时尽量在单分区完成、减少跨分区事务。常见选择包括用户 ID、订单 ID 和地理位置哈希。

## 三、复制与一致性

### 3.1 复制协议

| 协议 | 一致性 | 性能 | 容错 | 典型代表 |
|------|--------|------|------|----------|
| 主从异步 | 弱 | 高 | 主故障有损 | MySQL Replication |
| 半同步 | 最终一致 | 中 | 至少一从确认 | MySQL Semi-Sync |
| 同步(2PC) | 强 | 低 | 阻塞 | 传统分布式 DB |
| Paxos/Raft | 强 | 中 | 最多 N/2故障 | Spanner, TiDB |
| 最终一致(Gossip) | 弱 | 极高 | 好 | Cassandra |

### 3.2 Raft 协议

Raft 是一种易于理解的一致性算法，通过选主实现共识：

1. **领导者选举**：Follower→Candidate→Leader，需要获得多数票
2. **日志复制**：Leader 将日志条目复制到大多数节点后提交
3. **安全性**：保证已提交的条目不会被后续领导者覆盖

Raft 的 Term(任期)机制保证时间上的全局顺序，每条日志条目都被赋予一个 term 编号。

### 3.3 分布式事务

**两阶段提交(2PC)**是经典分布式事务协议：

- 阶段1(准备)：协调者向所有参与者发送 prepare 请求
- 阶段2(提交)：所有参与者 prepare 成功则提交，否则中止

2PC 的阻塞问题——协调者故障时参与者可能无限等待。**三阶段提交(3PC)**通过引入预提交状态减少阻塞窗口。

## 四、NewSQL 体系

### 4.1 NewSQL 定义

NewSQL 是一类兼具 NoSQL 扩展性和传统 SQL ACID 事务保证的数据库系统，旨在解决分布式环境下的规模化 OLTP 问题。

NewSQL 的三种实现路径：
1. **全新架构**：Spanner, CockroachDB, TiDB—重新设计分布式存储+计算
2. **透明分片中间件**：Vitess—在单机数据库之上提供分片和路由
3. **云原生数据库**：Aurora, PolarDB—计算存储分离

### 4.2 Spanner 架构(Google)

Spanner 是现代 NewSQL 的始祖级系统，关键创新：

- **TrueTime API**：使用 GPS 和原子钟提供全局精确时间戳，实现外部一致性
- **Paxos 复制**：每个 Paxos 组管理一个数据分片，保证强一致
- **可串行化隔离**：通过时间戳排序实现快照隔离级别上的可串行化

TrueTime 的不确定性窗口 $\epsilon$ 大约为1-7 ms，Spanner 通过等待 $\epsilon$ 时间确保时间戳不会与未来冲突。

### 4.3 TiDB 架构

TiDB 是开源的 NewSQL 数据库，采用计算与存储分离架构：

- **TiDB Server**：无状态 SQL 层，处理协议兼容、查询解析和优化
- **TiKV**：分布式键值存储引擎，使用 Raft 协议复制数据
- **PD**：调度中心，管理元数据和负载均衡

```sql
-- TiDB 与传统 MySQL 协议兼容
CREATE TABLE orders (
    order_id BIGINT PRIMARY KEY CLUSTERED,
    user_id BIGINT NOT NULL,
    amount DECIMAL(10, 2),
    created_at DATETIME
) PARTITION BY HASH (user_id) PARTITIONS 16;
```

### 4.4 CockroachDB

CockroachDB 使用 Paxos 协议，通过混合逻辑时钟(HLC)替代 TrueTime 实现串行化隔离。自动数据再均衡无需人工干预。

## 五、分布式 SQL 引擎

### 5.1 分布式查询执行

SQL 查询在多节点上并行执行，通过数据交换算子(Exchange)在节点间传输数据。Join 操作在分布式环境中的实现：

- **Broadcast Join**：将小表广播到所有节点
- **Hash Join(分桶)**：按 Join 键哈希将数据重分布
- **Sort Merge Join**：适用于已排序的大数据量

### 5.2 全局索引

全局索引维护数据在多个分片上的分布信息，支持非分区键的高效查询。二级全局索引的实现需要在所有分片上查找，通常通过"索引表"或"Scatter-Gather"模式实现。

## 六、挑战与展望

| 挑战 | 描述 | 解决方案 |
|------|------|----------|
| 分布式死锁 | 跨节点事务循环等待 | 超时+死锁检测 |
| 时钟偏差 | 节点间时间不同步 | TrueTime, HLC, 混合时钟 |
| 分布式 Join | 跨分片连接性能 | 数据本地性优化，Colocation |
| 在线 DDL | 不停机修改表结构 | Gh-ost, Online Schema Change |
| 备份恢复 | 大规模数据备份 | 快照备份+增量恢复 |

未来方向包括：Serverless 数据库(按需计费，自动弹性)、HTAP(混合事务分析处理)和 AI 增强的数据库自治管理。

## 相关条目

- [[NoSQL]]
- [[RelationalDatabases]]
- [[Transaction]]
- [[MongoDBDeep]]
- [[流处理与实时计算]]

## 参考资源

1. Corbett, J. C., et al. "Spanner: Google's Globally-Distributed Database." OSDI, 2012.
2. Ongaro, D., Ousterhout, J. "In Search of an Understandable Consensus Algorithm." USENIX ATC, 2014.
3. Huang, D., et al. "TiDB: A Raft-based HTAP Database." VLDB, 2020.
4. Baker, J., et al. "CockroachDB: The Resilient Geo-Distributed SQL Database." SIGMOD, 2020.
5. DeCandia, G., et al. "Dynamo: Amazon's Highly Available Key-Value Store." SOSP, 2007.
6. Gilbert, S., Lynch, N. "Brewer's Conjecture and the Feasibility of Consistent, Available, Partition-Tolerant Web Services." ACM SIGACT News, 2002.
7. Stonebraker, M. "NewSQL: An Alternative to NoSQL and Old SQL for New OLTP Apps." Communications of the ACM, 2012.
