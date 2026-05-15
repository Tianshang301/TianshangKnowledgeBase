---
aliases: [BigDataTechnologies]
tags: ['DatabasesAndInformationSystems', 'BigDataTechnologies', 'BigDataTechnologies']
---

# Big Data Technologies - 大数据技术

## 一、大数据概述

大数据是指无法用传统数据处理工具处理的**海量、高速、多样**的数据集合。

### 4V 特征

| 特征 | 说明 | 技术挑战 |
|------|------|---------|
| **Volume（大量）** | 数据量级从 TB 到 PB 乃至 EB | 分布式存储与计算 |
| **Velocity（高速）** | 数据产生和处理的速率极高 | 实时/流式处理 |
| **Variety（多样）** | 结构化、半结构化、非结构化数据 | 多源异构数据整合 |
| **Veracity（真实性）** | 数据的质量与可信度 | 数据清洗与质量管理 |

### 批处理 vs 流处理

| 维度 | 批处理 | 流处理 |
|------|--------|--------|
| 数据范围 | 全部/大批量数据 | 实时到达的数据 |
| 延迟 | 分钟到小时级 | 毫秒到秒级 |
| 处理方式 | 定期作业 | 持续不断 |
| 典型框架 | Hadoop MapReduce, Spark | Flink, Spark Streaming |
| 场景 | 离线报表、ETL | 实时监控、 fraud detection |

---

## 二、Hadoop 生态系统

Hadoop 是大数据技术的基石，核心组件包括 HDFS、MapReduce 和 YARN。

### HDFS — 分布式文件系统

**架构**：

```
Client ──→ NameNode (元数据)
              │
              ▼
DataNode 1 ──→ DataNode 2 ──→ DataNode 3 ...
（块存储）    （块存储）      （块存储）
```

| 组件 | 职责 |
|------|------|
| **NameNode** | 管理文件系统命名空间和元数据，记录文件到块的映射 |
| **DataNode** | 存储实际数据块，执行读写请求 |
| **Secondary NameNode** | 辅助合并 edit logs，非热备 |

**数据复制**：

```
块复制因子（默认 3）：
┌──────────┬──────────┬──────────┐
│  副本 1   │  副本 2   │  副本 3   │
│ (节点 A)  │ (节点 B)  │ (节点 C)  │
│同一机架   │不同机架   │同一机架   │
└──────────┴──────────┴──────────┘
```

### MapReduce — 分布式计算模型

**计算范式**：

$$ \text{Map}:\; (k_1, v_1) \to \text{List}(k_2, v_2) $$
$$ \text{Reduce}:\; (k_2, \text{List}(v_2)) \to \text{List}(k_3, v_3) $$

```
Input → Split → Map → Shuffle & Sort → Reduce → Output
```

- **Map 阶段**：将输入数据拆分为键值对，并行处理
- **Shuffle 阶段**：按 key 分区、排序、合并，将结果发送到 Reducer
- **Reduce 阶段**：对每个 key 对应的 value 列表进行聚合处理

```java
// WordCount 示例 — Mapper
public static class TokenizerMapper
    extends Mapper<Object, Text, Text, IntWritable> {
    private final static IntWritable one = new IntWritable(1);
    private Text word = new Text();

    public void map(Object key, Text value, Context context) {
        StringTokenizer itr = new StringTokenizer(value.toString());
        while (itr.hasMoreTokens()) {
            word.set(itr.nextToken());
            context.write(word, one);
        }
        // 输出: (word, 1)
    }
}

// Reducer
public static class IntSumReducer
    extends Reducer<Text, IntWritable, Text, IntWritable> {
    private IntWritable result = new IntWritable();

    public void reduce(Text key, Iterable<IntWritable> values, Context context) {
        int sum = 0;
        for (IntWritable val : values)
            sum += val.get();
        result.set(sum);
        context.write(key, result);
        // 输出: (word, count)
    }
}
```

### YARN — 资源管理

```
ResourceManager
    ├── Scheduler（调度器）
    └── ApplicationManager（应用管理器）
            │
    NodeManager ──→ Container
    NodeManager ──→ Container
    NodeManager ──→ Container
```

| 组件 | 功能 |
|------|------|
| **ResourceManager** | 全局资源管理和调度 |
| **NodeManager** | 每个节点上的代理，管理容器 |
| **ApplicationMaster** | 每个应用一个，协调任务执行 |
| **Container** | 资源抽象（CPU + 内存） |

---

## 三、Spark

Spark 是基于内存计算的统一分析引擎，比 Hadoop MapReduce 快 100 倍以上。

### 核心抽象

**RDD（Resilient Distributed Dataset）**：

```
RDD ──→ Partition 1 ──→ Partition 2 ──→ ...
   ↓              ↓              ↓
各分区可独立并行计算，自动容错
```

```python
# RDD 操作
rdd = sc.textFile("hdfs://data/logs")
errors = rdd.filter(lambda line: "ERROR" in line)
error_count = errors.count()

# Transformation（惰性求值）：map, filter, flatMap, reduceByKey, join
# Action（触发计算）：count, collect, saveAsTextFile, reduce
```

**DataFrame / Dataset**：

```python
# DataFrame API（比 RDD 更高级）
df = spark.read.json("data/people.json")
df.filter(df.age > 20).groupBy("gender").count().show()
# Spark SQL 优化器 Catalyst Optimizer 自动优化执行计划
```

**DAG 执行引擎**：

```
RDD A ─→ map ─→ RDD B ─→ filter ─→ RDD C
  │                                │
  └──────── join ──────────────────┘
                        │
                   RDD D ─→ action → 结果
```

DAG Scheduler 将计算图划分为 Stage，每个 Stage 内执行流水线式的任务。

### Spark 组件

| 组件 | 用途 |
|------|------|
| **Spark SQL** | 结构化数据处理，支持 SQL 查询 |
| **Spark Streaming** | 微批处理流计算（DStream） |
| **MLlib** | 分布式机器学习库 |
| **GraphX** | 图计算引擎 |

```python
# Spark Streaming — 微批处理
stream = SparkStreamingContext(spark, batch_interval=1)
lines = stream.socketTextStream("host", port)
words = lines.flatMap(lambda line: line.split(" "))
word_counts = words.map(lambda w: (w, 1)).reduceByKey(lambda a, b: a + b)
word_counts.pprint()
stream.start()
stream.awaitTermination()
```

---

## 四、Flink

Flink 是专为**流处理**设计的分布式计算引擎，支持真正的逐条事件处理。

### 核心概念

| 概念 | 说明 |
|------|------|
| **DataStream** | 无限数据流抽象 |
| **Event Time** | 事件实际发生的时间（vs Processing Time） |
| **Watermark** | 用于处理乱序事件的机制 |
| **Checkpoint** | 分布式快照，实现 exactly-once |

```java
// Flink 流处理
StreamExecutionEnvironment env = StreamExecutionEnvironment.getExecutionEnvironment();
env.setStreamTimeCharacteristic(TimeCharacteristic.EventTime);

DataStream<Event> stream = env.addSource(new FlinkKafkaConsumer<>("topic", ...));
stream
    .keyBy(event -> event.getUserId())
    .window(TumblingEventTimeWindows.of(Time.minutes(1)))
    .aggregate(new CountAggregate())
    .print();
```

**Exactly-Once 语义**：

```
Source ─→ Checkpoint ─→ Operator ─→ Checkpoint ─→ Sink
            │                             │
    Barrier n                      Barrier n
```

Flink 通过 checkpoint 中的 barrier 机制对齐快照，确保故障恢复后每个记录恰好处理一次。

### 流处理 vs 微批处理

| 特性 | Flink（真流） | Spark Streaming（微批） |
|------|-------------|----------------------|
| 延迟 | 毫秒级 | 秒级（取决于 batch interval） |
| 窗口 | 天然支持事件时间窗口 | 基于微批的窗口 |
| 状态管理 | 内置状态后端 | 需要外部状态存储 |
| 一致性 | 原生 exactly-once | 配合 Kafka 实现 |

---

## 五、Kafka

Kafka 是分布式**发布-订阅消息系统**，广泛用于日志收集、流处理数据管道。

### 架构

```
Producer ──→ Topic (Partition 0) ──→ Consumer Group A
              Topic (Partition 1) ──→ Consumer Group B
              Topic (Partition 2) ──→ ...
```

| 概念 | 说明 |
|------|------|
| **Topic** | 消息的逻辑分类 |
| **Partition** | 分区，实现并行和水平扩展 |
| **Offset** | 分区内消息的唯一标识 |
| **Consumer Group** | 消费组内成员共同消费一个 topic |
| **Broker** | Kafka 集群中的每个服务器节点 |

```java
// Kafka Producer
Properties props = new Properties();
props.put("bootstrap.servers", "localhost:9092");
props.put("key.serializer", "org.apache.kafka.common.serialization.StringSerializer");
props.put("value.serializer", "org.apache.kafka.common.serialization.StringSerializer");

Producer<String, String> producer = new KafkaProducer<>(props);
producer.send(new ProducerRecord<>("my-topic", "key", "value"));
```

**分区与消费组**：

```
Topic "orders" (3 partitions)
    Part-0 ──→ Consumer A（组 G1）
    Part-1 ──→ Consumer B（组 G1）
    Part-2 ──→ Consumer C（组 G1）
同一分区内消息有序，不同分区无法保证全局有序
```

---

## 六、HBase

HBase 是构建在 HDFS 之上的**列族存储**数据库。

### 数据模型

```
Table
  └── Row Key ──→ Column Family 1 ──→ Column Family 2
                      │                      │
                   Qualifier             Qualifier
                      │                      │
                   Value (Timestamped)    Value (Timestamped)
```

```shell
# HBase Shell 操作
create 'users', 'info', 'orders'
put 'users', 'row1', 'info:name', 'zhangsan'
put 'users', 'row1', 'info:age', '25'
put 'users', 'row1', 'orders:order_id', 'ORD001'
get 'users', 'row1'
scan 'users', {COLUMNS => ['info']}
```

**Region Server 架构**：

```
HMaster ──→ RegionServer 1 ──→ Region A, Region B
             RegionServer 2 ──→ Region C, Region D
             RegionServer 3 ──→ Region E, Region F
```

---

## 七、Hive

Hive 是基于 Hadoop 的**数据仓库基础设施**，将 SQL 转换为 MapReduce/Tez/Spark 作业。

```sql
-- HQL 示例
CREATE TABLE page_views (
    user_id   STRING,
    page_url  STRING,
    view_time TIMESTAMP
)
PARTITIONED BY (dt STRING)
STORED AS PARQUET;

INSERT OVERWRITE TABLE page_views PARTITION (dt='2024-01-01')
SELECT user_id, page_url, view_time
FROM raw_logs
WHERE dt = '2024-01-01';
```

---

## 八、数据湖 vs 数据仓库

| 维度 | 数据仓库 | 数据湖 |
|------|---------|--------|
| 数据格式 | 结构化（Schema-on-Write） | 所有格式（Schema-on-Read） |
| 处理方式 | ETL → 存储 | ELT → 存储后转换 |
| 存储成本 | 高（需预处理） | 低（原始数据存储） |
| 数据质量 | 高（经过清洗） | 原始（可能需处理） |
| 典型技术 | Hive, Snowflake | Delta Lake, Iceberg, Hudi |

### 湖仓一体（Lakehouse）

Delta Lake 和 Apache Iceberg 为数据湖添加了事务、版本管理、ACID 特性：

| 特性 | Delta Lake | Apache Iceberg |
|------|-----------|---------------|
| ACID 事务 | ✅ 支持 | ✅ 支持 |
| 时间旅行 | ✅ | ✅ |
| Schema 演化 | ✅ | ✅ |
| 分区演化 | 需重写 | ✅ 自动 |
| 隐藏分区 | ❌ | ✅ |
| 文件格式 | Parquet | Parquet / Avro / ORC |

---

## 九、Lambda 架构

Lambda 架构同时运行批处理和流处理两条路径，合并结果：

```
                      ┌──────────────┐
                      │  实时层 (Speed) │
所有数据 ──→ 消息队列 ─→├──────────────┤
           (Kafka)   │  流处理 (Flink) │──→ 实时视图
                      └──────────────┘
                           │
                      ┌──────────────┐
                      │  批处理层 (Batch)│
                      ├──────────────┤
                      │  HDFS + Spark │──→ 批视图
                      └──────────────┘
                           │
                      ┌──────────────┐
                      │  服务层 (Serving)│
                      ├──────────────┤
                      │  合并结果输出  │──→ 最终查询
                      └──────────────┘
```

Kappa 架构（简化）：仅使用流处理，将批处理视为流处理的特例。

---

## 十、大数据存储格式

| 格式 | 特点 | 适用场景 |
|------|------|---------|
| **Parquet** | 列式存储，高压缩率 | OLAP、分析查询 |
| **ORC** | 列式，Hive 深度优化 | Hive 查询 |
| **Avro** | 行式，Schema 演化好 | 数据管道、序列化 |
| **Arrow** | 内存列式格式，零拷贝 | 跨系统数据交换 |

---

## 十一、CAP 定理与一致性模型

### CAP 定理

$$ \text{CAP: 一致性 (Consistency)} \land \text{可用性 (Availability)} \land \text{分区容错 (Partition Tolerance)} $$

分布式系统最多同时满足其中两个：

| 系统类型 | 放弃 | 说明 | 典型系统 |
|---------|------|------|---------|
| **CA** | 分区容错 | 不允许网络分区，实际很少见 | 单机数据库 |
| **CP** | 可用性 | 分区时拒绝请求保证一致 | HBase, ZooKeeper, MongoDB |
| **AP** | 一致性 | 分区时允许不一致，最终一致 | Cassandra, DynamoDB, CouchDB |

### 一致性模型对比

| 模型 | 描述 | 延迟 | 适用场景 |
|------|------|------|---------|
| **强一致性** | 写入后立即可见 | 高 | 银行交易 |
| **最终一致性** | 无更新后最终一致 | 低 | DNS, CDN |
| **因果一致性** | 有因果关系的操作按序可见 | 中 | 社交网络 |
| **读己之写** | 写后自己的读可见 | 中 | 用户设置 |
| **单调读** | 不会读到更早版本 | 中 | 日志查询 |

## 相关条目

- MapReduce
- Hadoop
- Spark
- [[NoSQL]]
- [[DataWarehousing]]

## 参考资源

- Dean, J. & Ghemawat, S. (2004). MapReduce: Simplified Data Processing on Large Clusters. OSDI.
- Zaharia, M. et al. (2012). Resilient Distributed Datasets: A Fault-Tolerant Abstraction for In-Memory Cluster Computing. NSDI.
- Carbone, P. et al. (2015). Apache Flink: Stream and Batch Processing in a Single Engine. IEEE Data Engineering Bulletin.
- Kreps, J. et al. (2011). Kafka: A Distributed Messaging System for Log Processing. NetDB.
- Apache Hadoop Documentation. https://hadoop.apache.org/docs/
- Apache Spark Documentation. https://spark.apache.org/docs/latest/
