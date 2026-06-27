---
aliases: [QueryOptimization]
tags: ['05_ComputerScience', 'DatabasesAndInformationSystems']
created: 2026-05-17
updated: 2026-05-17
---

# 查询优化 (Query Optimization)

## 一、概述 (Overview)

查询优化是数据库系统将 SQL 查询转换为高效执行计划（Execution Plan）的过程。优化器（Query Optimizer）在保证语义等价的前提下，选择代价最小的执行策略，是数据库性能的核心。

### 查询处理流程

```mermaid
graph LR
    SQL[SQL Query] --> PARSER[语法解析 Parser]
    PARSER --> BIND[语义绑定 Binder]
    BIND --> REWRITE[查询重写 Rewriter]
    REWRITE --> OPTIMIZER[查询优化器 Optimizer]
    OPTIMIZER --> PLAN[执行计划 Execution Plan]
    PLAN --> EXECUTOR[执行引擎 Executor]
    EXECUTOR --> RESULT[查询结果]
```

## 二、关系代数 (Relational Algebra) 基础

查询优化基于关系代数的等价变换。核心操作：

| 操作 | 符号 | SQL 对应 | 复杂度 |
|------|------|---------|--------|
| 选择 (Selection) | $\sigma_{condition}(R)$ | `WHERE` | $O(\|R\|)$ |
| 投影 (Projection) | $\pi_{columns}(R)$ | `SELECT columns` | $O(\|R\|)$ |
| 连接 (Join) | $R \bowtie_{cond} S$ | `JOIN ... ON` | $O(\|R\| \times \|S\|)$ 最坏 |
| 并 (Union) | $R \cup S$ | `UNION` | $O(\|R\| + \|S\|)$ |
| 差 (Difference) | $R - S$ | `EXCEPT` | $O(\|R\| \times \|S\|)$ 最坏 |
| 分组聚合 | $\gamma_{group, agg}(R)$ | `GROUP BY` | $O(\|R\|)$ 排序/哈希 |

### 等价变换规则 (Equivalence Rules)

```text
1. 选择合并:  σ_c1(σ_c2(R)) ≡ σ_c1∧c2(R)
2. 选择交换:  σ_c1(σ_c2(R)) ≡ σ_c2(σ_c1(R))
3. 投影合并:  π_a(π_b(R)) ≡ π_a(R)  (a ⊆ b)
4. 选择下推:  σ_c(R ⋈ S) ≡ σ_c(R) ⋈ S  (c 只涉及 R)
5. 选择与投影: π_a(σ_c(R)) ≡ σ_c(π_a(R))
6. 结合律:    (R ⋈ S) ⋈ T ≡ R ⋈ (S ⋈ T)
7. 交换律:    R ⋈ S ≡ S ⋈ R
```

## 三、连接算法 (Join Algorithms)

| 算法 | 适用场景 | 复杂度 | 内存需求 |
|------|---------|--------|---------|
| **Nested Loop Join** | 小表驱动大表 + 索引 | $O(\|R\| \times \|S\|)$ | 极低 |
| **Index Nested Loop Join** | R 小，S 有索引 | $O(\|R\| \times \log\|S\|)$ | 极低 |
| **Sort-Merge Join** | 两表已排序或结果需排序 | $O(\|R\|\log\|R\| + \|S\|\log\|S\|)$ | 低 |
| **Hash Join** | 等值连接，大表 | $O(\|R\| + \|S\|)$ | 高（需哈希表）|
| **Grace Hash Join** | 超大表（内存放不下）| $O(\|R\| + \|S\|)$ 多趟 | 磁盘 I/O 分片 |

### Hash Join 详解

```text
构建阶段 (Build): 扫描小表 R，对连接键哈希，构建哈希表
探测阶段 (Probe): 扫描大表 S，对连接键哈希，在哈希表中查找匹配

代价: 3 × (|R| + |S|) · I/O + Hash 计算
```

### 连接顺序选择

对于多表连接，连接顺序影响巨大：
$$(A \bowtie B) \bowtie C \quad \text{vs} \quad A \bowtie (B \bowtie C)$$

选择最优连接顺序是 NP-hard 问题（$n$ 表连接有 $C_{n-1}$ 种顺序）。优化器使用动态规划或启发式搜索。

$$\text{Cost}(R \bowtie S) = |R| + |S| + \text{output}_{R \bowtie S}$$

## 四、索引与访问路径 (Indexes & Access Paths)

| 索引类型 | 数据结构 | 等值查询 | 范围查询 | 排序 | 适用 |
|---------|---------|---------|---------|------|------|
| B+ 树 | B+ Tree | $O(\log n)$ | $O(\log n + k)$ | 有序输出 | 通用 |
| 哈希索引 | Hash Table | $O(1)$ | 不支持 | 不支持 | 等值查询 |
| 位图索引 (Bitmap) | Bitmap | 快 | 快（位运算）| — | 低基数列 |
| GiST | 平衡树 | $O(\log n)$ | $O(\log n + k)$ | 部分 | 空间/全文索引 |
| BRIN | 块范围索引 | 差 | 快（大范围） | — | 时序大表 |

### 索引选择原则

```text
高选择性列 (High Selectivity):  适合 B+ 树索引
低选择性列 (Low Selectivity):    适合位图索引或 BRIN
频繁排序/分组:                    B+ 树有排序顺序
频繁等值查询:                     主键/唯一键用哈希
组合查询:                         联合索引的"最左前缀"原则
```

### 最左前缀法则

对于联合索引 `INDEX(a, b, c)`：

```sql
WHERE a = 1 AND b = 2    → 使用索引 ✓
WHERE a = 1 AND c = 3    → 部分索引（仅 a）⚠
WHERE b = 2 AND c = 3    → 不使用索引 ✗
WHERE a IN (1,2) AND b = 1  → 使用索引 ✓
```

## 五、查询重写 (Query Rewriting)

优化器自动执行的等价变换：

```sql
-- 子查询展开 (Subquery Unnesting)
-- 原始
SELECT * FROM A WHERE id IN (SELECT id FROM B WHERE active = 1);
-- 重写为 JOIN
SELECT A.* FROM A JOIN B ON A.id = B.id WHERE B.active = 1;

-- 谓词下推 (Predicate Pushdown)
SELECT * FROM (SELECT * FROM orders WHERE amount > 100) AS o JOIN customers c ON o.cid = c.id;
-- → 下推选择到 orders
SELECT * FROM orders o JOIN customers c ON o.cid = c.id WHERE o.amount > 100;

-- 视图合并 (View Merging)
-- 将视图内联展开，避免物化

-- 常量折叠 (Constant Folding)
WHERE salary * 1.1 > 50000 → WHERE salary > 45454.54

-- 死代码消除
SELECT 1 WHERE false → Empty Set
```

## 六、统计信息与代价估算 (Statistics & Cost Estimation)

优化器依赖表统计信息估算每种计划的代价：

| 统计量 | 含义 | 收集方式 |
|--------|------|---------|
| $n_{tuples}$ | 表行数 | `ANALYZE` / 采样 |
| $n_{pages}$ | 数据页数 | 直接从系统表读取 |
| $n_{distinct}$ | 每列唯一值数 | 采样估计 |
| 直方图 (Histogram) | 列数据分布 | 等深/等高/最频繁值 |
| 相关性 (Correlation) | 列值排序与物理顺序关联度 | 采样 |

### 选择率估算 (Selectivity Estimation)

```text
等值查询:  sel = 1 / n_distinct
范围查询:  sel = (high - low) / (max - min)  (假设均匀分布)
AND 条件:  sel = sel1 × sel2  (假设独立)
OR 条件:   sel = sel1 + sel2 - sel1 × sel2
NOT:       sel = 1 - sel
```

### 代价模型

$$\text{Total Cost} = \text{CPU Cost} + \text{I/O Cost} + \text{Memory Cost}$$

典型 PostgreSQL 代价参数：
```text
seq_page_cost   = 1.0     (顺序读一页)
random_page_cost = 4.0    (随机读一页)
cpu_tuple_cost  = 0.01    (处理一行)
cpu_index_tuple_cost = 0.005
cpu_operator_cost = 0.0025
```

## 七、执行计划查看 (Execution Plan Analysis)

```sql
-- PostgreSQL
EXPLAIN (ANALYZE, BUFFERS, TIMING) SELECT * FROM orders WHERE status = 'paid';
                                       QUERY PLAN
-------------------------------------------------------------------------
 Seq Scan on orders  (cost=0.00..2345.10 rows=15340 width=128)
                     (actual time=0.015..12.345 rows=15200 loops=1)
   Filter: (status = 'paid'::text)
   Rows Removed by Filter: 48100
 Planning Time: 0.085 ms
 Execution Time: 13.167 ms
```

常见性能瓶颈标识：
- `Seq Scan on large_table` → 考虑索引
- `Nested Loop` 循环次数过多 → 检查连接顺序
- `Sort` 使用大量内存 → 考虑索引排序
- `Hash` build 表过大 → 确保小表为 build 表

## 七、常见优化案例分析 (Optimization Case Studies)

### 案例 1: 慢查询排查

```sql
-- 原始慢查询（全表扫描，扫描 500 万行）
SELECT * FROM orders 
WHERE customer_id = 12345 
  AND status = 'shipped'
ORDER BY created_at DESC 
LIMIT 20;

-- EXPLAIN 输出显示 Seq Scan on orders
-- 优化方案：创建联合索引
CREATE INDEX idx_orders_customer_status_created 
ON orders(customer_id, status, created_at DESC);

-- 优化后：Index Scan，扫描 < 50 行
```

### 案例 2: N+1 查询问题

```python
# N+1 问题：查询所有用户及其最近订单
users = User.objects.all()          # 1 次查询
for user in users:
    orders = user.order_set.all()    # N 次查询（每个用户 1 次）

# 优化：使用 eager loading
users = User.objects.prefetch_related('order_set').all()  # 2 次查询
```

### 案例 3: 分页优化

```sql
-- 传统 OFFSET 分页（越往后越慢）
SELECT * FROM logs ORDER BY id LIMIT 20 OFFSET 100000;
-- OFFSET 100000 需要扫描 100020 行

-- 优化：游标分页（基于索引）
SELECT * FROM logs WHERE id > 100000 ORDER BY id LIMIT 20;
-- 直接定位到 id=100000，扫描 20 行
```

## 八、查询优化器内部工作机制

```text
查询优化器决策流程:
1. 语法分析 (Parsing): SQL → Parse Tree
2. 语义分析 (Binding): Parse Tree → Query Graph (含表/列引用)
3. 查询重写 (Rewrite): 应用等价变换规则（子查询展开、视图合并等）
4. 统计信息收集: 读取表/索引统计信息
5. 候选计划生成: 枚举可能的连接顺序和访问路径
6. 代价估算: 对每个候选计划计算总代价
   Cost = I/O Cost + CPU Cost + Memory Cost
7. 最优计划选择: 选取代价最小的执行计划
8. 执行计划缓存: 缓存重复使用的计划（Prepared Statement）
```

## 九、数据库特定优化技巧 (DB-Specific Optimizations)

### PostgreSQL

```sql
-- 部分索引 (Partial Index): 只索引常用数据
CREATE INDEX idx_active_orders ON orders(status) 
WHERE status IN ('pending', 'processing');

-- 覆盖索引 (Covering Index): 包含查询所需列，避免回表
CREATE INDEX idx_order_cover ON orders(customer_id) INCLUDE (total, status);

-- 物化视图: 预计算复杂聚合
CREATE MATERIALIZED VIEW daily_sales AS
SELECT order_date, SUM(amount) as total
FROM orders GROUP BY order_date;

-- 分析表更新统计信息
ANALYZE orders;
```

### MySQL

```sql
-- 索引提示 (Index Hints)
SELECT * FROM orders FORCE INDEX (idx_customer) WHERE customer_id = 123;

-- 查询缓存 (MySQL 8 已废弃，使用 ProxySQL/Redis)
-- 使用 MRR (Multi-Range Read) 优化
SET optimizer_switch = 'mrr=on,mrr_cost_based=off';
```

### 通用查询分析

```sql
-- 慢查询日志分析
-- PostgreSQL: pg_stat_statements
SELECT query, calls, total_exec_time, mean_exec_time
FROM pg_stat_statements 
ORDER BY total_exec_time DESC 
LIMIT 10;

-- MySQL: 慢查询日志
SET GLOBAL slow_query_log = 'ON';
SET GLOBAL long_query_time = 1;  -- > 1 秒记录
```

## 十、物化视图与查询加速

物化视图 (Materialized View) 预计算并存储查询结果，适用于复杂聚合：

```sql
-- PostgreSQL 物化视图
CREATE MATERIALIZED VIEW mv_daily_sales AS
SELECT date_trunc('day', order_time) as day,
       product_id,
       SUM(quantity) as total_qty,
       SUM(amount) as total_amt
FROM orders
GROUP BY 1, 2;

-- 刷新物化视图（支持 CONCURRENTLY 减少锁）
REFRESH MATERIALIZED VIEW CONCURRENTLY mv_daily_sales;

-- 查询（不再需要扫描 orders 主表）
SELECT * FROM mv_daily_sales WHERE day = CURRENT_DATE;
```

| 优化技术 | 性能提升 | 适用场景 | 风险 |
|---------|---------|---------|------|
| 物化视图 | 10-100x | 复杂聚合、报表查询 | 数据陈旧 |
| 查询缓存 (Redis) | 100-1000x | 读多写少、数据不频繁变化 | 缓存失效风暴 |
| 列存 (Columnar Storage) | 5-10x | 分析型查询 (OLAP) | 写入性能下降 |
| 分区表 (Partitioning) | 2-5x | 时间序列、大表管理 | 分区数过多影响 |

## 相关条目
- [[ACID]]
- [[SystemDesign]]
- [[05_ComputerScience/DatabasesAndInformationSystems/INDEX]]
