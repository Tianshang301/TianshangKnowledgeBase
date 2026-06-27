---
aliases: [DataWarehousing]
tags: ['DatabasesAndInformationSystems', 'DataWarehousing', 'DataWarehousing']
created: 2026-05-16
updated: 2026-05-16
---

# Data Warehousing - 数据仓库

## 一、数据仓库定义

数据仓库（Data Warehouse）是一个面向主题的、集成的、非易失的、随时间变化的数据集合，用于支持管理决策。

### Inmon vs Kimball 方法论

| 维度 | Inmon（企业信息工厂） | Kimball（维度建模） |
|------|---------------------|-------------------|
| 架构 | 自上而下：EDW → 数据集市 | 自下而上：数据集市 → 总线架构 |
| 建模 | 第三范式（3NF） | 星型/雪花型维度建模 |
| 开发周期 | 较长（需先建企业模型） | 较短（按业务过程迭代） |
| 一致性 | 数据从中心向外辐射 | 通过一致性维度保证 |
| 适用 | 大型企业、复杂集成 | 敏捷开发、部门级需求 |

---

## 二、维度建模

### 星型模式（Star Schema）

事实表与多个维度表直接相连，形成星型结构：

```
$$ \text{Fact} \bowtie \text{Dim}_1 \bowtie \text{Dim}_2 \bowtie \text{Dim}_3 \bowtie \dots $$

                 ┌──────────┐
                 │ Dim_Date │
                 ├──────────┤
                 │ date_key │──┐
                 │  year    │  │
                 │  month   │  │
                 └──────────┘  │
                               ▼
┌──────────┐          ┌────────────────┐          ┌──────────┐
│ Dim_Product│         │   Fact_Sales   │          │ Dim_Store│
├──────────┤          ├────────────────┤          ├──────────┤
│ prod_key │─────────→│ date_key (FK)  │←─────────│ store_key│
│ prod_name│          │ prod_key (FK)  │          │ city     │
│ category │          │ store_key (FK) │          │ region   │
└──────────┘          │  units_sold    │          └──────────┘
                      │  revenue       │
                      │  cost          │
                      └────────────────┘

```

| 元素 | 说明 |
|------|------|
| **事实表** | 存储业务过程的度量值，包含外键和数值型指标 |
| **维度表** | 存储描述性属性，提供上下文 |
| **粒度** | 事实表中一行所代表的业务事件级别 |

### 雪花模式（Snowflake Schema）

维度表进一步规范化，分解为子维度表：

```
Fact_Sales
  ├── Dim_Product → Product_Category
  ├── Dim_Store → Dim_Region
  └── Dim_Date
```

- 优点：减少数据冗余，节省存储
- 缺点：查询需要更多 JOIN，性能下降

### 事实星座（Fact Constellation）

多个事实表共享一致维度：

```
Fact_Sales ──→ Dim_Date ←── Fact_Inventory
Fact_Sales ──→ Dim_Product ←── Fact_Inventory
Fact_Sales ──→ Dim_Store ←── Fact_Promotion
```

---

## 三、ETL 过程

```
┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐
│  提取     │ → │  转换     │ → │  清洗     │ → │  加载     │
│ (Extract)│    │(Transform)│    │(Cleanse) │    │ (Load)   │
└──────────┘    └──────────┘    └──────────┘    └──────────┘
```

| 阶段 | 任务 | 工具/技术 |
|------|------|----------|
| **Extract** | 从源系统获取数据 | JDBC, API, FTP, 日志采集 |
| **Transform** | 数据格式转换、字段映射、计算衍生值 | SQL, Python, Spark |
| **Cleanse** | 去重、空值处理、异常值修正 | 规则引擎、数据质量工具 |
| **Load** | 写入目标数据仓库 | 批量 INSERT, COPY, UPSERT |

```sql
-- ETL 示例：增量加载
MERGE INTO dwd_sales AS target
USING (
    SELECT
        order_id,
        product_id,
        customer_id,
        amount,
        order_date
    FROM ods_orders
    WHERE order_date >= '2024-01-01'
) AS source
ON target.order_id = source.order_id
WHEN MATCHED THEN UPDATE SET
    amount = source.amount
WHEN NOT MATCHED THEN INSERT
    (order_id, product_id, customer_id, amount, order_date)
VALUES (source.order_id, source.product_id, source.customer_id,
        source.amount, source.order_date);
```

---

## 四、OLAP 操作

OLAP（联机分析处理）支持多维数据分析。

| 操作 | 说明 | 示例 |
|------|------|------|
| **Roll-up** | 上卷，沿维度层次聚合 | 从「日」聚合到「月」 |
| **Drill-down** | 下钻，查看更细粒度数据 | 从「年」下钻到「季度」 |
| **Slice** | 切片，选择单一维度值 | 只查看 2024 年数据 |
| **Dice** | 切块，选择多个维度子集 | 2024 年华北区数据 |
| **Pivot** | 旋转，重新排列维度 | 行列互换展示 |

### 数据立方体（Data Cube）

数据立方体是多维数组，每个维度代表一个分析角度：

```
$$ \text{Cube}[time][product][location] = \text{measure} $$

                   location
                    ▲
                    │
              ┌─────┼─────┐
              │     │     │
              ├─────┼─────┤
              │     │     │
              ├─────┼─────┤
              │     │     │
product ◄─────┼─────┼─────┼───► time
              │     │     │
              └─────┴─────┘
```

**CUBE 运算符**：

```sql
SELECT
    COALESCE(year, 'ALL') AS year,
    COALESCE(region, 'ALL') AS region,
    COALESCE(product, 'ALL') AS product,
    SUM(revenue) AS total_revenue
FROM sales_fact
JOIN dim_date USING (date_key)
JOIN dim_region USING (region_key)
JOIN dim_product USING (product_key)
GROUP BY CUBE (year, region, product);
```

---

## 五、物化视图（Materialized View）

物化视图是预先计算并存储的查询结果，用于加速 OLAP 查询。

```sql
CREATE MATERIALIZED VIEW mv_monthly_sales AS
SELECT
    year,
    month,
    product_id,
    SUM(units_sold) AS total_units,
    SUM(revenue) AS total_revenue,
    COUNT(*) AS transaction_count
FROM sales_fact
JOIN dim_date USING (date_key)
GROUP BY year, month, product_id;

-- 查询重写：优化器自动使用物化视图
SELECT year, month, SUM(total_revenue)
FROM mv_monthly_sales
GROUP BY year, month;
```

| 策略 | 说明 | 权衡 |
|------|------|------|
| **立即刷新** | 源表变更后立即更新 | 实时性高，开销大 |
| **延迟刷新** | 定期更新（如每天） | 性能好，数据有延迟 |
| **按需刷新** | 查询时检查并更新 | 查询可能变慢 |

---

## 六、缓慢变化维度（Slowly Changing Dimensions, SCD）

维度属性随时间变化，需要不同的处理策略。

| 类型 | 策略 | 示例（员工部门变更） |
|------|------|-------------------|
| **SCD Type 1** | 直接覆盖旧值 | 部门改为新值，历史丢失 |
| **SCD Type 2** | 新增记录，标记有效期 | 旧记录 end_date=昨日，新记录 start_date=今日 |
| **SCD Type 3** | 增加新列保存之前的值 | 增加 previous_department 列 |

```sql
-- SCD Type 2 实现
CREATE TABLE dim_customer (
    customer_sk   INT PRIMARY KEY,    -- 代理键
    customer_id   INT,                -- 业务键
    name          VARCHAR(100),
    address       VARCHAR(200),
    effective_date DATE,
    end_date       DATE DEFAULT '9999-12-31',
    is_current    BOOLEAN DEFAULT TRUE
);

-- 插入新版本
UPDATE dim_customer
SET end_date = '2024-06-01', is_current = FALSE
WHERE customer_id = 123 AND is_current = TRUE;

INSERT INTO dim_customer (customer_sk, customer_id, name, address,
                          effective_date, end_date, is_current)
VALUES (nextval('seq_customer_sk'), 123, '张三', '新地址',
        '2024-06-02', '9999-12-31', TRUE);
```

---

## 七、数据集市（Data Mart）

数据集市是面向特定部门或业务线的数据仓库子集。

| 特性 | 企业数据仓库（EDW） | 数据集市 |
|------|-------------------|----------|
| 范围 | 企业级 | 部门级 |
| 主题 | 多主题集成 | 单一主题 |
| 粒度 | 明细数据 | 汇总数据 |
| 建设周期 | 长 | 短 |
| 用户 | 全企业 | 特定部门 |

---

## 八、数据湖与湖仓一体

### 数据湖仓库对比

| 维度 | 数据仓库 | 数据湖 | 湖仓一体 |
|------|---------|--------|---------|
| 数据格式 | 结构化 | 结构化+半结构化+非结构化 | 所有格式 |
| Schema | Schema-on-Write | Schema-on-Read | Schema-on-Write + Read |
| ACID | ✅ 完整支持 | ❌ 有限 | ✅ |
| 性能 | 高（预优化） | 低（需转换） | 中高 |
| 成本 | 高 | 低 | 中 |

### Delta Lake

```python
# Delta Lake 操作
from delta.tables import DeltaTable

# 写入
(spark.readStream
     .format("kafka")
     .load()
     .writeStream
     .format("delta")
     .option("checkpointLocation", "/checkpoints")
     .start("/data/delta/events"))

# 时间旅行
df = spark.read.format("delta") \
    .option("versionAsOf", 42) \
    .load("/data/delta/events")

# 更新
delta_table = DeltaTable.forPath(spark, "/data/delta/events")
delta_table.update(
    condition = "event_type = 'click'",
    set = { "count": "count + 1" }
)
```

### Apache Iceberg

```sql
-- Iceberg 表操作
CREATE TABLE iceberg_catalog.nyc.taxis (
    vendor_id BIGINT,
    trip_id BIGINT,
    fare_amount DOUBLE,
    ts TIMESTAMP
) USING iceberg
PARTITIONED BY (hours(ts));

-- 时间旅行
SELECT * FROM iceberg_catalog.nyc.taxis
    FOR SYSTEM_TIME AS OF '2024-01-01 10:00:00';

-- 增量读取
SELECT * FROM iceberg_catalog.nyc.taxis
    FOR SYSTEM_VERSION AS OF 42;
```

---

## 九、维度建模最佳实践

| 原则 | 说明 |
|------|------|
| **一致性维度** | 多个数据集市共享相同维度的定义和值 |
| **退化维度** | 将无属性的维度合并到事实表 |
| **垃圾维度** | 将低频标志位组合为单一维度 |
| **缓慢变化维度** | 根据业务需求选择合适的 SCD 类型 |
| **事实表粒度** | 明确每行代表的业务事件级别 |
| **代理键** | 使用无业务含义的代理键作为主键 |
| **避免过度规范化** | 星型模式牺牲一定的规范化换取查询性能 |

## 相关条目

- OLAP
- ETL
- [[05_ComputerScience/DatabasesAndInformationSystems/BigDataTechnologies/BigDataTechnologies|BigDataTechnologies]]
- BusinessIntelligence

## 参考资源

- Kimball, R. & Ross, M. (2013). The Data Warehouse Toolkit: The Definitive Guide to Dimensional Modeling. 3rd Edition. Wiley.
- Inmon, W. H. (2005). Building the Data Warehouse. 4th Edition. Wiley.
- Armbrust, M. et al. (2021). Lakehouse: A New Generation of Open Platforms that Unify Data Warehousing and Advanced Analytics. CIDR.
- Apache Iceberg Documentation. https://iceberg.apache.org/docs/latest/
- Delta Lake Documentation. https://docs.delta.io/latest/


