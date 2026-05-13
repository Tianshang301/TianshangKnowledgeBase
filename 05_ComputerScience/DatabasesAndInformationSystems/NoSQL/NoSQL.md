# NoSQL Databases - NoSQL 数据库

## 一、NoSQL 概述

NoSQL（Not Only SQL）是一类非关系型数据库的统称，设计用于处理大规模、高并发的数据场景。

### 动机

| 挑战 | 关系型数据库的局限 | NoSQL 的解决方案 |
|------|-------------------|-----------------|
| 海量数据 | 垂直扩展有上限 | 水平扩展（分片） |
| 高并发 | 连接池瓶颈 | 无锁/最终一致性 |
| 灵活 Schema | 需预定义 Schema | Schema-less 设计 |
| 非结构化数据 | 不擅长大文本/JSON | 原生支持 |

---

## 二、CAP 定理

$$ \text{CAP Theorem: Consistency + Availability + Partition Tolerance → pick 2} $$

```
            CP                           AP
        ┌────────┐                  ┌────────┐
        │  HBase │                  │Cassandra│
        │  MongoDB│                 │ DynamoDB│
        │(旧版本)│                  │  Riak   │
        └────────┘                  └────────┘

            CA（实际不可行）
        ┌────────┐
        │ 传统 RDB │
        └────────┘
```

| 属性 | 说明 |
|------|------|
| **C — Consistency（一致性）** | 所有节点在同一时刻看到相同数据 |
| **A — Availability（可用性）** | 每次请求都能获得非错误的响应 |
| **P — Partition Tolerance（分区容忍性）** | 网络分区时系统仍能正常运行 |

### BASE vs ACID

| ACID | BASE |
|------|------|
| Atomicity（原子性） | Basically Available（基本可用） |
| Consistency（一致性） | Soft State（软状态） |
| Isolation（隔离性） | Eventually Consistent（最终一致性） |
| Durability（持久性） | — |

---

## 三、Key-Value 存储

### Redis

Redis 是基于内存的高性能 key-value 存储，支持丰富的数据结构。

详见 [Redis 详解](../Redis_Deep.md)。

```redis
# Redis 核心特性
SET key value                  # 字符串
LPUSH list item               # 列表
SADD set member               # 集合
ZADD sorted_set score member  # 有序集合
HSET hash field value         # 哈希

# 持久化
SAVE                          # RDB 同步快照
BGSAVE                        # RDB 异步快照
APPENDONLY yes                # AOF 日志

# 集群
CLUSTER MEET host port
CLUSTER ADDSLOTS slot
```

| 数据结构 | 底层实现 | 用途 |
|---------|---------|------|
| String | SDS（动态字符串） | 缓存、计数器、分布式锁 |
| List | 双向链表 / ZipList | 消息队列、最新列表 |
| Set | HashTable / IntSet | 标签系统、共同好友 |
| Sorted Set | SkipList + HashTable | 排行榜、延迟队列 |
| Hash | Dict / ZipList | 对象存储 |

### DynamoDB

AWS 托管的 key-value 和文档数据库。

| 特性 | 说明 |
|------|------|
| 分区键 | 决定数据分布的哈希键 |
| 排序键 | 同一分区内的排序属性 |
| 一致性 | 最终一致性（默认）/ 强一致性 |
| 扩展性 | 自动分片，无容量上限 |
| 读写容量 | 按预置容量或按需模式计费 |

---

## 四、文档存储 — MongoDB

MongoDB 是最流行的文档数据库，使用 BSON 格式存储。

### 数据模型

```javascript
// BSON 文档示例
{
    "_id": ObjectId("507f1f77bcf86cd799439011"),
    "name": "张三",
    "age": 25,
    "address": {
        "city": "北京",
        "district": "海淀"
    },
    "hobbies": ["阅读", "编程", "摄影"],
    "orders": [
        { "order_id": "ORD001", "amount": 99.9 },
        { "order_id": "ORD002", "amount": 199.0 }
    ]
}
```

### 索引

```javascript
// 索引类型
db.users.createIndex({ name: 1 })                 // 单字段索引（升序）
db.users.createIndex({ name: 1, age: -1 })        // 复合索引
db.users.createIndex({ address: "2dsphere" })     // 地理空间索引
db.users.createIndex({ tags: "text" })            // 全文索引
db.users.createIndex({ name: 1 }, { unique: true }) // 唯一索引

// 聚合管道
db.orders.aggregate([
    { $match: { status: "completed" } },
    { $group: { _id: "$customer_id", total: { $sum: "$amount" } } },
    { $sort: { total: -1 } },
    { $limit: 10 }
])
```

### 分片与复制

```
分片集群：
    mongos ──→ Config Server
       │
    Shard 1 (Replica Set) ──→ Primary ──→ Secondary ──→ Secondary
    Shard 2 (Replica Set) ──→ Primary ──→ Secondary
    Shard 3 (Replica Set) ──→ Primary ──→ Secondary ──→ Secondary
```

```javascript
// 启用分片
sh.enableSharding("mydb")
sh.shardCollection("mydb.orders", { customer_id: "hashed" })
```

### MongoDB vs RDBMS

| 概念 | MongoDB | RDBMS |
|------|---------|-------|
| 数据库 | Database | Database |
| 集合 | Collection | Table |
| 文档 | Document | Row |
| 字段 | Field | Column |
| 索引 | Index | Index |
| 引用 | Reference | Foreign Key |

---

## 五、列族存储 — Cassandra

Cassandra 是去中心化的列族数据库，提供高可用性和线性扩展。

### 数据模型

```cql
-- Cassandra Query Language (CQL)
CREATE TABLE users (
    user_id     UUID PRIMARY KEY,
    name        TEXT,
    email       TEXT,
    created_at  TIMESTAMP
);

-- 复合主键
CREATE TABLE events (
    year     INT,
    month    INT,
    event_id UUID,
    data     TEXT,
    PRIMARY KEY ((year, month), event_id)  -- 分区键 + 聚类列
);
```

| 概念 | 说明 |
|------|------|
| **Partition Key** | 决定数据分布的分区键 |
| **Clustering Columns** | 分区内的排序列 |
| **Primary Key** | = Partition Key + Clustering Columns |

### 分布式协议

**Gossip 协议**：节点间周期性交换状态信息，最终达到全局一致。

```
Node A ──gossip──→ Node B ──gossip──→ Node C
  ↑                                    │
  └──────────gossip────────────────────┘
```

**读修复（Read Repair）**：读取时发现副本数据不一致，异步修复。

**提示移交（Hinted Handoff）**：写入节点宕机时，协调节点暂存写入数据，待节点恢复后重放。

```cql
-- 一致性级别
INSERT INTO users (user_id, name) VALUES (uuid(), 'Alice')
    USING CONSISTENCY QUORUM;       -- 多数副本确认即返回

SELECT * FROM users
    WHERE user_id = 123
    USING CONSISTENCY ONE;          -- 一个副本响应即返回
```

### Cassandra vs HBase

| 特性 | Cassandra | HBase |
|------|-----------|-------|
| 架构 | 去中心化（P2P） | 主从（HMaster + RegionServer） |
| 一致性 | 可调一致性 | 强一致性（最终可调） |
| 扩展性 | 线性扩展，加节点即可 | 需管理 HMaster |
| 读写性能 | 写优化 | 随机读写均衡 |
| 适用场景 | 时序数据、IoT | 大规模结构化存储 |

---

## 六、图数据库 — Neo4j

Neo4j 是使用属性图模型的图数据库。

### 属性图模型

```
(节点:标签 {属性}) ──[:关系类型 {属性}]──→ (节点:标签 {属性})
```

```cypher
// Cypher 查询语言
CREATE (alice:Person {name: 'Alice', age: 30})
CREATE (bob:Person {name: 'Bob', age: 25})
CREATE (alice)-[:KNOWS {since: 2020}]->(bob)
CREATE (alice)-[:WORKS_AT]->(company:Company {name: 'Acme'})

// 查询
MATCH (p:Person)-[:KNOWS]->(friend)
WHERE p.name = 'Alice'
RETURN friend.name

// 最短路径
MATCH (a:Person {name: 'Alice'}), (b:Person {name: 'Bob'})
MATCH p = shortestPath((a)-[*]-(b))
RETURN p

// 推荐
MATCH (user:Person {name: 'Alice'})-[:PURCHASED]->(product)<-[:PURCHASED]-(other)-[:PURCHASED]->(rec)
WHERE NOT (user)-[:PURCHASED]->(rec)
RETURN rec, COUNT(*) AS freq
ORDER BY freq DESC
```

### 图遍历算法

| 算法 | 用途 |
|------|------|
| BFS/DFS | 连通性分析 |
| Dijkstra / A* | 最短路径 |
| PageRank | 节点重要性 |
| Betweenness Centrality | 节点中介度 |
| Community Detection (LPA) | 社群发现 |

---

## 七、NoSQL 对比总结

| 类型 | 代表 | 数据模型 | 优点 | 适用场景 |
|------|------|---------|------|---------|
| **Key-Value** | Redis, DynamoDB | 键值对 | 高性能、低延迟 | 缓存、Session、计数器 |
| **Document** | MongoDB, Couchbase | JSON/BSON 文档 | 灵活 Schema、开发效率高 | CMS、日志、实时分析 |
| **Column-Family** | Cassandra, HBase | 列族 | 高可用、水平扩展 | IoT 时序、大数据分析 |
| **Graph** | Neo4j, JanusGraph | 属性图 | 关系查询高效 | 社交网络、推荐、反欺诈 |

---

## 八、多语言持久化（Polyglot Persistence）

不同场景使用不同类型的数据库：

```text
应用系统
    ├── MySQL（用户账户、事务数据）      ← 关系型：需要 ACID
    ├── Redis（Session、缓存）           ← Key-Value：高性能读取
    ├── MongoDB（产品目录、内容管理）     ← Document：灵活 Schema
    ├── Cassandra（日志、时序数据）       ← Column-Family：高写入
    └── Neo4j（推荐关系、知识图谱）       ← Graph：关系查询
```

---

## 九、NewSQL

NewSQL 在保持 SQL 和 ACID 的同时实现水平扩展。

| 数据库 | 架构 | 特点 |
|--------|------|------|
| **CockroachDB** | 分布式 SQL，类 Spanner | 全局强一致，自动故障恢复 |
| **TiDB** | 计算存储分离（TiDB + TiKV + PD） | MySQL 兼容，HTAP 混合负载 |
| **Google Spanner** | 全球分布式，TrueTime API | 外部一致性，全球部署 |

```sql
-- TiDB 兼容 MySQL 语法
CREATE TABLE users (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255),
    email VARCHAR(255) UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- CockroachDB 分布式事务
BEGIN;
UPDATE accounts SET balance = balance - 100 WHERE id = 'A';
UPDATE accounts SET balance = balance + 100 WHERE id = 'B';
COMMIT;  -- 全局一致性，跨节点原子提交
```

## 相关条目

- [[RelationalDatabases]]
- [[BigDataTechnologies]]
- CAPTheorem
- [[DistributedSystems]]

## 参考资源

- Brewer, E. (2000). Towards Robust Distributed Systems. PODC Keynote.
- DeCandia, G. et al. (2007). Dynamo: Amazon's Highly Available Key-value Store. SOSP.
- Lakshman, A. & Malik, P. (2010). Cassandra: A Decentralized Structured Storage System. SIGOPS.
- MongoDB Documentation. https://www.mongodb.com/docs/
- Neo4j Graph Database. https://neo4j.com/docs/
- CockroachDB Documentation. https://www.cockroachlabs.com/docs/
