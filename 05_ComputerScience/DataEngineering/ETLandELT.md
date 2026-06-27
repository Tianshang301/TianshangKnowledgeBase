---
aliases:
  - ETL
  - ELT
  - 数据抽取转换加载
  - 数据管道
tags:
  - data-engineering
  - etl
  - elt
  - data-pipeline
  - data-integration
created: 2026-06-27
updated: 2026-06-27
---

# ETL与ELT

ETL（Extract-Transform-Load）和ELT（Extract-Load-Transform）是数据集成的两种核心架构模式，广泛应用于数据仓库、数据湖和数据分析场景。

## ETL vs ELT架构对比

### ETL（Extract-Transform-Load）
- **流程**：从源系统抽取数据 → 在中间层转换 → 加载到目标系统
- **特点**：转换在加载前完成，适合传统数据仓库
- **优势**：数据质量有保障，目标系统压力小
- **劣势**：扩展性差，转换逻辑与加载耦合

### ELT（Extract-Load-Transform）
- **流程**：从源系统抽取数据 → 直接加载到目标系统 → 在目标系统内转换
- **特点**：利用目标系统（如Snowflake、BigQuery）的计算能力
- **优势**：灵活性高，支持原始数据保留
- **劣势**：对目标系统性能要求高

### 架构选择指南
```
场景 → 选择
├─ 传统数据仓库 → ETL
├─ 云数据平台 → ELT
├─ 实时处理需求 → ELT
└─ 数据湖场景 → ELT
```

## 数据抽取技术

### 全量抽取（Full Extraction）
- 每次抽取所有数据
- 适用场景：数据量小、变化不频繁
- 实现方式：`SELECT * FROM source_table`

### 增量抽取（Incremental Extraction）
- 只抽取变化的数据
- 基于时间戳：`WHERE updated_at > last_sync_time`
- 基于序列号：`WHERE id > last_max_id`
- 基于变更标记：`WHERE is_changed = 1`

### 变更数据捕获（CDC）
- **基于触发器**：数据库触发器记录变更
- **基于日志**：读取事务日志（如MySQL binlog、PostgreSQL WAL）
- **基于时间戳**：记录最后修改时间
- **工具**：Debezium、Oracle GoldenGate、AWS DMS

## 数据转换

### 数据清洗（Data Cleaning）
- **空值处理**：填充默认值、删除记录、插值
- **重复数据删除**：基于唯一键去重
- **异常值处理**：统计方法（Z-score、IQR）检测
- **格式标准化**：日期格式、地址格式统一

### 数据标准化（Data Standardization）
- **编码统一**：UTF-8编码转换
- **单位统一**：货币、度量衡转换
- **分类映射**：将不同分类体系映射到统一标准

### 数据聚合（Data Aggregation）
- **时间维度聚合**：小时、天、月汇总
- **维度钻取**：上卷（Roll-up）、下钻（Drill-down）
- **窗口函数**：ROW_NUMBER、RANK、LEAD/LAG

## 数据加载策略

### 全量覆盖（Full Overwrite）
```sql
TRUNCATE TABLE target_table;
INSERT INTO target_table SELECT * FROM staging_table;
```

### 增量更新（Incremental Update）
```sql
INSERT INTO target_table
SELECT * FROM staging_table
WHERE id NOT IN (SELECT id FROM target_table);
```

### SCD（Slowly Changing Dimensions）
- **SCD Type 1**：直接覆盖旧值
- **SCD Type 2**：保留历史记录，添加有效期字段
- **SCD Type 3**：添加新列存储旧值

## ETL工具

### Apache NiFi
- 可视化数据流设计
- 支持数据路由、转换、系统中介
- 内置数据溯源功能

### Airbyte
- 开源数据集成平台
- 支持300+连接器
- 提供标准化的连接器开发套件（CDK）

### Fivetran
- 全托管数据管道服务
- 自动化Schema管理
- 支持CDC和全量同步

### dbt（Data Build Tool）
- SQL优先的转换工具
- 版本控制的数据模型
- 自动生成文档和数据血缘

## ETL工具对比

### 工具特性对比
```
工具 → 类型 → 核心优势 → 适用场景
├─ Apache NiFi → 可视化ETL → 数据流设计复杂 → 企业级数据集成
├─ Airbyte → 开源连接器 → 连接器生态丰富 → SaaS数据集成
├─ Fivetran → 全托管服务 → 零维护 → 中小企业
├─ dbt → SQL转换 → 版本控制 → 数据仓库转换
├─ Apache Spark → 批处理引擎 → 大规模数据处理 → 大数据ETL
└─ Apache Flink → 流处理引擎 → 低延迟 → 实时ETL
```

### 工具选型指南
#### 选择Apache NiFi的场景
- 需要可视化数据流设计
- 数据源多样，格式复杂
- 需要数据路由和转换
- 企业级安全和治理需求

#### 选择Airbyte的场景
- SaaS应用数据集成
- 需要快速添加新数据源
- 预算有限，需要开源方案
- 团队SQL技能为主

#### 选择dbt的场景
- 数据仓库转换逻辑复杂
- 需要版本控制和测试
- 团队熟悉SQL
- 需要数据文档自动化

### 部署模式对比
```
模式 → 优势 → 劣势 → 适用场景
├─ 本地部署 → 数据安全 → 维护成本高 → 金融、政务
├─ 云托管 → 零维护 → 数据出境 → 互联网企业
└─ 混合部署 → 灵活性高 → 架构复杂 → 大型企业
```

## 数据质量检查框架

### 数据质量维度
1. **准确性**：数据是否正确反映现实
2. **完整性**：数据是否缺失
3. **一致性**：数据在不同系统中是否一致
4. **时效性**：数据是否及时更新
5. **唯一性**：是否存在重复数据

### 检查框架设计
```python
# 数据质量检查示例
class DataQualityChecker:
    def check_completeness(self, df, columns):
        null_counts = df[columns].isnull().sum()
        return null_counts / len(df) < 0.05  # 空值率<5%

    def check_accuracy(self, df, column, valid_range):
        return df[column].between(*valid_range).all()

    def check_timeliness(self, df, timestamp_col, max_delay_hours):
        max_timestamp = df[timestamp_col].max()
        return (datetime.now() - max_timestamp).hours < max_delay_hours

    def check_uniqueness(self, df, key_columns):
        duplicate_count = df.duplicated(subset=key_columns).sum()
        return duplicate_count / len(df) < 0.01  # 重复率<1%

    def check_consistency(self, df, column, reference_values):
        return df[column].isin(reference_values).all()
```

### Great Expectations详解
```python
import great_expectations as gx

# 创建数据上下文
context = gx.get_context()

# 定义数据源
datasource = context.sources.add_pandas("my_datasource")

# 创建数据资产
data_asset = datasource.add_dataframe_asset(name="my_data")

# 定义期望
expectation = gx.expectations.ExpectColumnValuesToNotBeNull(column="user_id")

# 运行验证
result = context.run_validation_operator(
    "action_operator",
    assets_to_validate=[data_asset],
    run_id="my_run"
)
```

### 数据质量报告
```python
class DataQualityReport:
    def __init__(self, df):
        self.df = df
        self.metrics = {}

    def calculate_metrics(self):
        # 计算基础指标
        self.metrics['row_count'] = len(self.df)
        self.metrics['column_count'] = len(self.df.columns)
        self.metrics['null_percentage'] = (self.df.isnull().sum() / len(self.df) * 100).to_dict()

        # 计算统计指标
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns
        for col in numeric_cols:
            self.metrics[f'{col}_mean'] = self.df[col].mean()
            self.metrics[f'{col}_std'] = self.df[col].std()
            self.metrics[f'{col}_min'] = self.df[col].min()
            self.metrics[f'{col}_max'] = self.df[col].max()

    def generate_report(self):
        self.calculate_metrics()
        return pd.DataFrame.from_dict(self.metrics, orient='index', columns=['Value'])
```

### 工具推荐
- **Great Expectations**：Python数据质量框架
- **Deequ**：基于Spark的数据质量库
- **Apache Griffin**：大数据数据质量解决方案
- **Monte Carlo**：数据可观测性平台
- **Ataccama**：数据质量管理平台

## 实施案例

### 电商数据集成案例
#### 业务背景
- 数据源：MySQL、MongoDB、日志文件、第三方API
- 目标：构建统一数据仓库支持BI分析

#### 技术方案
```
数据源 → Airbyte → Snowflake → dbt → BI工具
├─ MySQL订单数据 → 增量同步 → 原始层
├─ MongoDB用户数据 → 全量同步 → 清洗层
├─ 日志文件 → S3上传 → 转换层
└─ 第三方API → 定时拉取 → 应用层
```

#### 实施效果
- 数据延迟：从24小时降到1小时
- 开发效率：提升3倍
- 数据质量：问题发现时间从周级降到小时级

### 金融数据仓库案例
#### 业务背景
- 数据源：核心银行系统、风控系统、监管报送系统
- 目标：构建实时数据仓库支持风险监控

#### 技术方案
```
核心系统 → CDC(Debezium) → Kafka → Flink → Hive → 监管报表
├─ 交易数据 → 实时捕获 → 实时计算 → 风险指标
├─ 客户数据 → 增量同步 → 批量处理 → 客户画像
└─ 风控数据 → 实时推送 → 实时告警 → 风险预警
```

## 最佳实践

1. **幂等性设计**：确保管道可重复执行
2. **错误处理**：实现重试机制和死信队列
3. **监控告警**：设置数据质量指标阈值
4. **文档化**：记录数据流和转换逻辑
5. **测试覆盖**：单元测试和集成测试
6. **版本控制**：管理ETL代码和配置版本
7. **环境隔离**：开发、测试、生产环境分离

## 参考资料
- 《Data Management Body of Knowledge (DAMA-DMBOK)》
- Kimball Group 数据仓库方法论
- dbt 官方文档：https://docs.getdbt.com
- Airbyte 官方文档：https://docs.airbyte.com/
- Apache NiFi 官方文档：https://nifi.apache.org/docs/
- Great Expectations 官方文档：https://docs.greatexpectations.io/