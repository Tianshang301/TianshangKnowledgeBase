---
aliases: [MongoDBDeep]
tags: ['DatabasesAndInformationSystems', 'MongoDBDeep']
created: 2026-05-16
updated: 2026-05-16
---

# MongoDB NoSQL 指南

## 一、概述

MongoDB 是一个面向文档的 NoSQL 数据库，使用 BSON 格式存储数据。与关系型数据库不同，MongoDB 不使用表和行，而是使用集合（Collection）和文档（Document）。

### 核心特性

| 特性 | 说明 |
|------|------|
| 文档模型 | 数据以 BSON 文档形式存储，支持嵌套和数组 |
| Schema-less | 同一集合中的文档可以有不同的字段结构 |
| 高可用 | 副本集（Replica Set）自动故障转移 |
| 水平扩展 | 分片（Sharding）支持海量数据分布 |
| 聚合管道 | 强大的数据处理管道 |
| 二级索引 | 支持多种索引类型 |
| 地理位置 | 原生地理空间索引和查询 |
| 全文搜索 | 内置全文搜索（需要 Atlas 或 Mellisearch） |

### 术语对比

| RDBMS | MongoDB |
|-------|---------|
| Database | Database |
| Table | Collection |
| Row | Document |
| Column | Field |
| Index | Index |
| JOIN | $lookup / 嵌入式文档 |
| Primary Key | _id (ObjectId) |
| Foreign Key | Reference (DBRef / 手动引用) |

---

## 二、CRUD 操作

### Insert

```javascript
// 插入单个文档
db.users.insertOne({
    username: "zhangsan",
    email: "zhangsan@example.com",
    age: 25,
    tags: ["developer", "backend"],
    address: {
        city: "beijing",
        district: "haidian"
    },
    created_at: new Date()
})

// 插入多个文档
db.users.insertMany([
    { username: "lisi", email: "lisi@example.com", age: 30 },
    { username: "wangwu", email: "wangwu@example.com", age: 28 }
])

// 插入（如果 _id 冲突则更新）
db.users.updateOne(
    { _id: ObjectId("...") },
    { $set: { username: "zhangsan_new" } },
    { upsert: true }
)
```

### Find

```javascript
// 查询全部
db.users.find()

// 带条件查询
db.users.find({ age: { $gt: 20, $lt: 40 } })
db.users.find({ username: "zhangsan" })
db.users.find({ "address.city": "beijing" })

// 投影（只返回指定字段）
db.users.find(
    { age: { $gte: 18 } },
    { username: 1, email: 1, _id: 0 }
)

// 比较操作符
db.users.find({ age: { $in: [20, 25, 30] } })
db.users.find({ age: { $ne: 25 } })
db.users.find({ age: { $exists: true } })

// 逻辑操作符
db.users.find({
    $or: [
        { age: { $lt: 20 } },
        { age: { $gt: 60 } }
    ]
})

// 正则查询
db.users.find({ username: /zhang/i })

// 数组查询
db.users.find({ tags: "developer" })              // 包含
db.users.find({ tags: { $all: ["developer", "backend"] } })  // 全部包含
db.users.find({ tags: { $size: 3 } })              // 数组长度为3

// 排序和分页
db.users.find()
    .sort({ age: -1, username: 1 })
    .skip(20)
    .limit(10)

// 计数
db.users.countDocuments({ age: { $gte: 18 } })
```

### Update

```javascript
// 更新单个文档
db.users.updateOne(
    { username: "zhangsan" },
    { $set: { age: 26, updated_at: new Date() } }
)

// 更新多个文档
db.users.updateMany(
    { age: { $lt: 18 } },
    { $set: { status: "minor" } }
)

// 字段操作
db.users.updateOne(
    { _id: ObjectId("...") },
    {
        $set: { email: "new@example.com" },
        $unset: { old_field: "" },         // 删除字段
        $rename: { old_name: "new_name" },
        $inc: { login_count: 1 },          // 自增
        $push: { tags: "mongodb" },        // 数组追加
        $pull: { tags: "obsolete" },       // 数组移除
        $addToSet: { tags: "new_tag" }     // 不重复追加
    }
)

// 替换整个文档
db.users.replaceOne(
    { username: "zhangsan" },
    { username: "zhangsan", email: "new@example.com", age: 26 }
)
```

### Delete

```javascript
// 删除单个
db.users.deleteOne({ username: "temp_user" })

// 删除多个
db.users.deleteMany({ status: "inactive" })

// 清空集合（保留索引）
db.users.deleteMany({})

// 删除集合
db.users.drop()
```

---

## 三、聚合管道

聚合管道是 MongoDB 最强大的数据处理工具，数据依次通过多个阶段处理。

```javascript
db.orders.aggregate([
    // Stage 1: 匹配（过滤数据）
    { $match: { status: "completed", created_at: { $gte: ISODate("2024-01-01") } } },

    // Stage 2: 分组
    { $group: {
        _id: "$user_id",
        total_orders: { $sum: 1 },
        total_spent: { $sum: "$total" },
        avg_amount: { $avg: "$total" },
        first_order: { $min: "$created_at" },
        last_order: { $max: "$created_at" }
    } },

    // Stage 3: 排序
    { $sort: { total_spent: -1 } },

    // Stage 4: 限制
    { $limit: 10 },

    // Stage 5: 投影
    { $project: {
        _id: 0,
        user_id: "$_id",
        total_orders: 1,
        total_spent: { $round: ["$total_spent", 2] },
        avg_amount: { $round: ["$avg_amount", 2] }
    } }
])
```

### 常用聚合阶段

```javascript
// $lookup — 类似 JOIN
db.orders.aggregate([
    { $lookup: {
        from: "users",                    // 关联集合
        localField: "user_id",
        foreignField: "_id",
        as: "user_info"
    }},
    { $unwind: "$user_info" },           // 展开数组
    { $project: {
        order_id: "$_id",
        username: "$user_info.username",
        total: 1
    }}
])

// $unwind — 展开数组
db.articles.aggregate([
    { $unwind: "$tags" },
    { $group: { _id: "$tags", count: { $sum: 1 } } },
    { $sort: { count: -1 } }
])

// $bucket — 分组统计
db.orders.aggregate([
    { $bucket: {
        groupBy: "$total",
        boundaries: [0, 100, 500, 1000, 5000],
        default: "5000+",
        output: {
            count: { $sum: 1 },
            total: { $sum: "$total" }
        }
    }}
])

// $facet — 多维度分析
db.orders.aggregate([
    { $match: { created_at: { $gte: ISODate("2024-01-01") } } },
    { $facet: {
        "by_status": [
            { $group: { _id: "$status", count: { $sum: 1 } } }
        ],
        "by_month": [
            { $group: {
                _id: { $dateToString: { format: "%Y-%m", date: "$created_at" } },
                revenue: { $sum: "$total" }
            }},
            { $sort: { _id: 1 } }
        ],
        "stats": [
            { $group: {
                _id: null,
                avg: { $avg: "$total" },
                max: { $max: "$total" },
                min: { $min: "$total" }
            }}
        ]
    }}
])

// $addFields — 添加计算字段
db.orders.aggregate([
    { $addFields: {
        discounted: { $multiply: ["$total", 0.9] },
        order_year: { $year: "$created_at" },
        order_month: { $month: "$created_at" }
    }}
])
```

---

## 四、索引

```javascript
// 单列索引
db.users.createIndex({ email: 1 })

// 唯一索引
db.users.createIndex({ username: 1 }, { unique: true })

// 复合索引
db.orders.createIndex({ user_id: 1, created_at: -1 })

// 多键索引（数组字段）
db.articles.createIndex({ tags: 1 })

// 文本索引
db.articles.createIndex({ title: "text", body: "text" })
db.articles.find({ $text: { $search: "mongodb aggregation" } })

// 地理空间索引
db.places.createIndex({ location: "2dsphere" })
db.places.find({
    location: {
        $near: {
            $geometry: { type: "Point", coordinates: [116.40, 39.90] },
            $maxDistance: 1000   // 米
        }
    }
})

// TTL 索引（自动过期删除）
db.sessions.createIndex(
    { created_at: 1 },
    { expireAfterSeconds: 86400 }     // 24小时后自动删除
)

// 部分索引
db.users.createIndex(
    { age: 1 },
    { partialFilterExpression: { age: { $gte: 18 } } }
)

// 稀疏索引
db.products.createIndex(
    { sku: 1 },
    { sparse: true }
)

// 查看索引
db.users.getIndexes()

// 删除索引
db.users.dropIndex("email_1")
```

### 索引使用分析

```javascript
// 查询分析
db.orders.find({ user_id: 1001, created_at: { $gte: ISODate("2024-01-01") } })
    .explain("executionStats")

// 索引命中统计
db.orders.aggregate([
    { $indexStats: {} }
])
```

---

## 五、副本集

### 架构

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Primary   │────▶│  Secondary  │────▶│  Secondary  │
│  (读写)      │     │  (只读)      │     │  (只读)      │
└─────────────┘     └─────────────┘     └─────────────┘
       │                                       │
       │                                  ┌────┴────┐
       │                                  │  Arbiter │
       │                                  │ (投票用)  │
       └──────────────────────────────────┴─────────┘
```

### 配置副本集

```javascript
// 启动 mongod（每个节点）
mongod --replSet rs0 --dbpath /data/db --port 27017

// 初始化副本集
rs.initiate({
    _id: "rs0",
    members: [
        { _id: 0, host: "localhost:27017" },
        { _id: 1, host: "localhost:27018" },
        { _id: 2, host: "localhost:27019", arbiterOnly: true }
    ]
})

// 副本集管理命令
rs.status()                 // 查看状态
rs.printReplicationInfo()   // 复制信息
rs.conf()                   // 配置信息

// 读写偏好
// 主库读
db.getMongo().setReadPref("primary")
// 从库读
db.getMongo().setReadPref("secondary")
// 就近读
db.getMongo().setReadPref("nearest")
```

### 故障转移

当 Primary 宕机时，副本集自动发起选举，从 Secondary 中选出新的 Primary。选举基于 Raft 协议。

---

## 六、分片

### 架构

```
┌──────────┐
│  mongos  │  ← 路由层，应用连接 mongos
└────┬─────┘
     │
┌────┴─────┐    ┌──────────┐    ┌──────────┐
│ Config   │    │ Shard 1  │    │ Shard 2  │
│ Server   │    │ (副本集)  │    │ (副本集)  │
└──────────┘    └──────────┘    └──────────┘
```

### 分片配置

```javascript
// 启动配置服务器
mongod --configsvr --dbpath /data/config --port 27019

// 启动 mongos
mongos --configdb cfg/localhost:27019 --port 27017

// 添加分片
sh.addShard("rs1/localhost:27018")
sh.addShard("rs2/localhost:27020")

// 启用数据库分片
sh.enableSharding("mydb")

// 选择分片键
// 基于范围的分片
sh.shardCollection("mydb.users", { _id: "hashed" })

// 基于范围的分片（适合有序数据）
sh.shardCollection("mydb.orders", { created_at: 1 })
    .ensureIndex({ created_at: 1 })
```

### 分片键选择

| 策略 | 优点 | 缺点 |
|------|------|------|
| Hash 分片键 | 数据分布均匀 | 范围查询效率低 |
| Range 分片键 | 支持范围查询 | 容易产生热点 |
| 复合分片键 | 折中方案 | 复杂度高 |

---

## 七、MongoDB vs RDBMS

| 维度 | MongoDB | RDBMS (MySQL/PostgreSQL) |
|------|---------|-------------------------|
| 数据模型 | 文档型，支持嵌套 | 关系型，需规范化 |
| Schema | 动态（无模式） | 固定（需迁移） |
| JOIN | $lookup（性能不如 JOIN） | 原生 JOIN |
| 事务 | 4.0 支持多文档事务 | ACID 事务 |
| 扩展性 | 原生分片（水平扩展） | 分库分表（第三方） |
| 索引 | 丰富（2dsphere, TTL, text） | 丰富（B-tree, Hash, GiST） |
| 写入性能 | 高（无事务开销时） | 一般（取决于引擎） |
| 查询语言 | JSON-like（表达能力有限） | SQL（标准、强大） |
| 一致性 | 默认最终一致性 | 强一致性 |
| 复制 | 副本集自动故障转移 | 主从/组复制 |

### 选择建议

**使用 MongoDB 当**：
- 数据模型变化频繁，需要灵活 schema
- 需要快速开发迭代
- 数据量大，需要水平扩展
- 文档/JSON 格式的数据
- 地理位置、物联网日志、实时分析

**使用 RDBMS 当**：
- 数据关系复杂，需要 JOIN 和强一致性
- 事务要求高（金融、订单系统）
- 需要 SQL 查询和分析
- 数据结构稳定
- 需要复杂报表和统计

## 相关条目

- [[NoSQL]]
- [[RedisDeep]]
- [[分布式数据库与 NewSQL]]
- [[RelationalDatabases]]
- [[SQLDeep]]
