---
aliases:
  - Spark
  - Flink
  - 大数据处理框架
  - 流处理引擎
tags:
  - data-engineering
  - apache-spark
  - apache-flink
  - stream-processing
  - batch-processing
created: 2026-06-27
updated: 2026-06-27
---

# Spark与Flink

Apache Spark和Apache Flink是当前最主流的两个大数据处理框架，分别代表了批处理和流处理的不同技术路线。

## Apache Spark架构

### 核心抽象
#### RDD（Resilient Distributed Dataset）
- **定义**：不可变、可分区、可并行操作的数据集合
- **特性**：
  - 容错性：通过血缘（Lineage）实现
  - 惰性计算：转换操作延迟执行
  - 缓存机制：支持内存和磁盘持久化
- **操作**：
  - 转换（Transformation）：map、filter、groupByKey
  - 行动（Action）：count、collect、saveAsTextFile

#### DataFrame
- **定义**：以命名列方式组织的分布式数据集合
- **优势**：
  - 结构化数据处理
  - Catalyst优化器
  - Tungsten执行引擎
- **API**：支持SQL和DSL（Domain Specific Language）

#### Dataset
- **定义**：类型安全的DataFrame
- **特点**：
  - 编译时类型检查
  - 支持函数式编程
  - 兼容DataFrame API
- **适用**：Scala/Java开发

### Spark生态系统
```
Spark Core → RDD API，任务调度
├─ Spark SQL → 结构化数据处理
├─ Spark Streaming → 微批流处理
├─ MLlib → 机器学习
└─ GraphX → 图计算
```

## Spark SQL与结构化流处理

### Spark SQL
- **Catalyst优化器**：
  - 逻辑计划优化
  - 物理计划生成
  - 代码生成（Whole-Stage Code Generation）
- **Tungsten引擎**：
  - 内存管理优化
  - 缓存感知计算
  - 二进制数据处理

### 结构化流处理（Structured Streaming）
- **编程模型**：将流数据视为无界表
- **处理模式**：
  - 微批处理（Micro-batch）：默认模式
  - 连续处理（Continuous Processing）：低延迟模式
- **输出模式**：
  - Append：只输出新行
  - Complete：输出完整结果表
  - Update：只输出变化行

### 流处理示例
```scala
// 结构化流处理示例
val inputStream = spark.readStream
  .format("kafka")
  .option("kafka.bootstrap.servers", "host:port")
  .option("subscribe", "topic")
  .load()

val query = inputStream
  .selectExpr("CAST(value AS STRING)")
  .writeStream
  .format("console")
  .start()
```

## Apache Flink架构

### 核心组件
#### DataStream API
- **定义**：处理无界和有界数据流的核心API
- **操作**：
  - 转换：map、flatMap、filter
  - 聚合：keyBy、reduce、aggregate
  - 窗口：tumbling、sliding、session窗口
  - 连接：connect、coMap、coFlatMap

#### Table API & SQL
- **定义**：声明式数据处理API
- **特点**：
  - 统一批流处理
  - 支持SQL查询
  - 与DataStream API互操作

### Flink运行时架构
```
Client → JobManager → TaskManager
├─ JobManager：作业调度，检查点协调
├─ TaskManager：执行任务，管理状态
└─ Dispatcher：作业提交入口
```

## Flink状态管理与Exactly-Once语义

### 状态管理
#### 状态类型
- **Keyed State**：基于Key的状态，自动分区
  - ValueState：单值状态
  - ListState：列表状态
  - MapState：映射状态
  - ReducingState：聚合状态
- **Operator State**：算子级别的状态

#### 状态后端
- **MemoryStateBackend**：状态存储在内存
- **FsStateBackend**：状态存储在文件系统
- **RocksDBStateBackend**：状态存储在RocksDB

### Exactly-Once语义
#### 检查点（Checkpoint）
- **原理**：分布式一致性快照
- **实现**：Chandy-Lamport算法变种
- **配置**：
  - 检查点间隔
  - 超时时间
  - 最小间隔
  - 失败容忍次数

#### 两阶段提交（2PC）
- **Sink支持**：需要支持事务的Sink
- **流程**：
  1. 预提交：数据写入临时位置
  2. 提交：确认写入最终位置
  3. 回滚：失败时清理临时数据

## 流处理语义对比

### Micro-batch vs 真正流式
```
特性 → Micro-batch（Spark） → 真正流式（Flink）
延迟 → 秒级 → 毫秒级
吞吐量 → 高 → 中等
状态管理 → 有限 → 丰富
窗口支持 → 基于处理时间 → 支持事件时间
Exactly-Once → 支持 → 支持
```

### 语义保证
- **At-Most-Once**：消息可能丢失
- **At-Least-Once**：消息可能重复
- **Exactly-Once**：消息不丢不重

### 事件时间 vs 处理时间
- **事件时间**：事件发生的时间
- **处理时间**：事件被处理的时间
- **水位线（Watermark）**：处理乱序事件的机制

## 性能调优与资源管理

### Spark调优
#### 内存管理
- **堆内存**：执行内存和存储内存
- **堆外内存**：Tungsten引擎使用
- **序列化**：Kryo序列化比Java序列化高效

#### 数据倾斜处理
- **增加分区数**：`spark.sql.shuffle.partitions`
- **广播小表**：`broadcast(df)`
- **自定义分区器**：实现`Partitioner`接口

#### 缓存策略
- **MEMORY_ONLY**：只缓存内存
- **MEMORY_AND_DISK**：内存不足时溢写磁盘
- **DISK_ONLY**：只缓存磁盘

### Flink调优
#### 状态后端选择
```
场景 → 状态后端
├─ 小状态，低延迟 → MemoryStateBackend
├─ 大状态，高吞吐 → RocksDBStateBackend
└─ 中等状态 → FsStateBackend
```

#### 检查点优化
- **检查点间隔**：平衡容错和性能
- **对齐超时**：处理反压情况
- **增量检查点**：只保存变化部分

#### 网络缓冲
- **缓冲区大小**：`taskmanager.network.memory.buffer-size`
- **缓冲区数量**：`taskmanager.network.memory.floating-buffers-per-gate`

### 资源管理
#### Spark on YARN
- **资源分配**：executor数量、核心数、内存
- **动态资源分配**：根据负载调整资源

#### Flink on Kubernetes
- **Session模式**：共享集群资源
- **Application模式**：专用资源
- **资源请求**：CPU、内存、存储

## 最佳实践

### 开发规范
1. **代码复用**：提取公共转换逻辑
2. **错误处理**：实现重试机制
3. **监控指标**：自定义业务指标
4. **测试策略**：单元测试和集成测试

### 运维建议
1. **容量规划**：基于历史数据预测资源需求
2. **监控告警**：设置关键指标阈值
3. **日志管理**：集中日志收集和分析
4. **版本管理**：控制框架版本升级

### 选型建议
```
需求 → 推荐框架
├─ 批处理为主 → Spark
├─ 低延迟流处理 → Flink
├─ 流批一体 → Flink
├─ 机器学习 → Spark MLlib
└─ 复杂事件处理 → Flink CEP
```

## 参考资料
- Apache Spark官方文档：https://spark.apache.org/docs/
- Apache Flink官方文档：https://flink.apache.org/docs/
- 《Spark: The Definitive Guide》
- 《Streaming Systems: The What, Where, When, and How of Large-Scale Data Processing》