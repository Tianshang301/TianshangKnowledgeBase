---
aliases: [MySQLDeep]
tags: ['DatabasesAndInformationSystems', 'MySQLDeep']
created: 2026-05-16
updated: 2026-05-16
---

# MySQL 深入指南

## 一、MySQL 架构

### 整体架构分层

MySQL 服务器从上到下分为以下几个层次：

```
┌─────────────────────────────────────────────────┐
│                 客户端连接                         │
│   (MySQL Client, Navicat, JDBC, Python Driver)    │
├─────────────────────────────────────────────────┤
│            Connection / Thread Pool               │
│   (连接管理、认证、SSL、线程复用)                    │
├─────────────────────────────────────────────────┤
│                查询缓存 (Query Cache)              │
│   (MySQL 8.0 已移除，之前用于缓存 SELECT 结果)        │
├─────────────────────────────────────────────────┤
│              SQL 接口 (SQL Interface)              │
│   (DDL, DML, 存储过程, 视图, 触发器)                │
├─────────────────────────────────────────────────┤
│              解析器 (Parser)                       │
│   (词法分析 → 语法分析 → 生成解析树)                  │
├─────────────────────────────────────────────────┤
│              优化器 (Optimizer)                    │
│   (查询重写、成本估算、执行计划选择)                   │
├─────────────────────────────────────────────────┤
│              执行器 (Executor)                     │
│   (调用存储引擎 API，返回结果)                       │
├─────────────────────────────────────────────────┤
│             存储引擎层 (Storage Engines)            │
│   (InnoDB, MyISAM, Memory, CSV, Archive...)       │
└─────────────────────────────────────────────────┘
```

### 各组件详解

**连接层**：
- 每个客户端连接对应一个线程
- `max_connections` 控制最大连接数
- `thread_cache_size` 控制线程缓存

**查询缓存（8.0 前）**：
- 缓存完整的 SELECT 结果
- 表数据变更时自动失效
- 高并发写入场景下命中率低，MySQL 8.0 彻底移除

**解析器**：
- 词法分析：将 SQL 拆分为 token
- 语法分析：根据语法规则构建解析树
- 验证表名、列名是否存在

**优化器**：
- 选择最优执行计划
- 可选择的执行路径：全表扫描、索引扫描、临时表、连接顺序
- 通过 `EXPLAIN` 查看优化器选择的计划

---

## 二、存储引擎

### 存储引擎对比

| 特性 | InnoDB | MyISAM | Memory |
|------|--------|--------|--------|
| 事务支持 | ✅ ACID | ❌ | ❌ |
| 外键 | ✅ | ❌ | ❌ |
| 行级锁 | ✅ | ❌（表级锁） | ❌（表级锁） |
| MVCC | ✅ | ❌ | ❌ |
| 崩溃恢复 | ✅ | ❌ | ❌ |
| B+树索引 | ✅ | ✅ | ✅（Hash 索引） |
| 全文索引 | ✅（5.6+） | ✅ | ❌ |
| 聚簇索引 | ✅ | ❌ | ❌ |
| 压缩 | ✅ | ✅ | ❌ |
| 适用场景 | OLTP，事务 | 只读，报表 | 临时表，缓存 |

### 存储引擎操作

```sql
-- 查看支持的存储引擎
SHOW ENGINES;

-- 查看表使用的存储引擎
SHOW TABLE STATUS WHERE Name = 'users';

-- 修改表的存储引擎
ALTER TABLE users ENGINE = InnoDB;

-- 建表时指定存储引擎
CREATE TABLE logs (
    id INT PRIMARY KEY AUTO_INCREMENT,
    message TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE = MyISAM;
```

---

## 三、InnoDB 内部机制

### B+ 树索引

InnoDB 使用 B+ 树作为索引结构，特点：

| 特性 | 说明 |
|------|------|
| 非叶子节点 | 仅存储键值和指针，不存储数据 |
| 叶子节点 | 存储完整数据（聚簇索引）或主键值（二级索引） |
| 叶子节点链表 | 叶子节点之间形成双向链表，支持范围扫描 |
| 扇出度 | 通常为几百到上千（取决于页大小和键大小） |
| 树高 | 通常为 2-4 层（千万级数据量） |

### 聚簇索引 vs 二级索引

```sql
CREATE TABLE employee (
    id INT PRIMARY KEY,        -- 聚簇索引：叶子节点存储整行数据
    name VARCHAR(50),
    age INT,
    dept_id INT,
    INDEX idx_name (name),     -- 二级索引：叶子节点存储主键值
    INDEX idx_dept_age (dept_id, age)  -- 复合二级索引
);
```

**聚簇索引**：
- 表数据物理顺序与索引顺序一致
- 每张表只能有一个聚簇索引
- 没有定义主键时，InnoDB 自动选择唯一非空列或生成隐藏的 ROW_ID

**二级索引（回表）**：
- 通过二级索引找到主键值
- 再通过主键聚簇索引找到完整行数据
- **覆盖索引**：二级索引包含所有查询字段则无需回表

### 自适应哈希索引 (AHI)

- InnoDB 自动优化：监控索引页的查找模式
- 为热数据在 B+ 树之上建立哈希索引
- 等值查询可 O(1) 完成
- 由 `innodb_adaptive_hash_index` 参数控制

### Change Buffer

- 对二级索引的变更（INSERT/UPDATE/DELETE）不立即合并到磁盘
- 缓存变更，在后续读取或合并操作时统一应用
- 大幅减少随机 I/O
- `innodb_change_buffer_max_size` 控制最大大小（默认 25%）

### Doublewrite Buffer

- 解决部分页面写入问题（torn page）
- 写入前先将数据拷贝到 doublewrite buffer
- 写入共享表空间的两个连续区
- 再同步到实际数据文件
- 崩溃恢复时可从此缓冲区恢复

```sql
-- 查看 doublewrite buffer 状态
SHOW GLOBAL STATUS LIKE 'Innodb_dblwr%';

-- 配置
innodb_doublewrite = ON
```

---

## 四、事务与 ACID

### 事务控制

```sql
START TRANSACTION;
    UPDATE accounts SET balance = balance - 1000 WHERE id = 1;
    UPDATE accounts SET balance = balance + 1000 WHERE id = 2;
COMMIT;

-- 自动提交控制
SET autocommit = 0;  -- 关闭自动提交

-- 保存点
START TRANSACTION;
    INSERT INTO logs VALUES (1, 'start');
    SAVEPOINT sp1;
    INSERT INTO logs VALUES (2, 'point1');
    ROLLBACK TO sp1;  -- 回滚到保存点，保留第一个插入
COMMIT;
```

### REDO 日志

- 记录已提交事务对数据页的物理修改
- 保证 Durability（持久性）— 已提交事务不会丢失
- WAL（Write-Ahead Logging）：REDO 日志先于数据写入磁盘
- `innodb_log_file_size` 和 `innodb_log_files_in_group` 控制 REDO 日志大小

```sql
SHOW VARIABLES LIKE 'innodb_log%';
```

### UNDO 日志

- 记录事务修改前的数据版本（逻辑日志）
- 实现 MVCC 和事务回滚
- 存储在 undo 表空间
- 事务隔离级别不同，UNDO 保留时间不同

### MVCC (Multi-Version Concurrency Control)

MVCC 的实现依赖 UNDO 日志和快照读：

```sql
-- 当前读（加锁）
SELECT * FROM users WHERE id = 1 FOR UPDATE;    -- 排他锁
SELECT * FROM users WHERE id = 1 LOCK IN SHARE MODE;  -- 共享锁

-- 快照读（不加锁）
SELECT * FROM users WHERE id = 1;  -- MVCC 读，不上锁
```

**MVCC 工作原理**：

每个事务开始时获得一个事务 ID (trx_id)，每行数据有两个隐藏列：
- `DB_TRX_ID`：最后修改此行的事务 ID
- `DB_ROLL_PTR`：指向 UNDO 日志的指针

- REPEATABLE READ 级别：事务开始时创建一致性视图 (ReadView)
- 查询只读取在该视图创建前已提交的事务版本

### 隔离级别

```sql
-- 设置当前会话隔离级别
SET SESSION TRANSACTION ISOLATION LEVEL READ COMMITTED;
SET SESSION TRANSACTION ISOLATION LEVEL REPEATABLE READ;

-- 设置全局隔离级别
SET GLOBAL TRANSACTION ISOLATION LEVEL READ COMMITTED;
```

| 隔离级别 | 脏读 | 不可重复读 | 幻读 |
|----------|------|-----------|------|
| READ UNCOMMITTED | ✅ | ✅ | ✅ |
| READ COMMITTED | ❌ | ✅ | ✅ |
| REPEATABLE READ（MySQL 默认） | ❌ | ❌ | ✅（InnoDB 解决了） |
| SERIALIZABLE | ❌ | ❌ | ❌ |

---

## 五、锁机制

### 锁类型

| 锁类型 | 说明 |
|--------|------|
| 共享锁 (S) | 允许多个事务读取，阻塞写 |
| 排他锁 (X) | 阻塞其他事务读写 |
| 意向共享锁 (IS) | 表级锁，标识事务打算加行级 S 锁 |
| 意向排他锁 (IX) | 表级锁，标识事务打算加行级 X 锁 |
| 记录锁 (Record Lock) | 锁定单条记录 |
| 间隙锁 (Gap Lock) | 锁定记录之间的间隙（防止幻读） |
| Next-Key Lock | 记录锁 + 间隙锁的组合（RR 级别默认） |
| 插入意向锁 | INSERT 时的特殊间隙锁 |

### 行锁示例

```sql
-- 会话 A
START TRANSACTION;
SELECT * FROM users WHERE id = 1 FOR UPDATE;
-- 持有 id=1 的行锁

-- 会话 B 被阻塞，直到会话 A 提交
UPDATE users SET name = 'test' WHERE id = 1;
```

### Next-Key 锁示例

在 REPEATABLE READ 级别，InnoDB 对范围查询使用 Next-Key 锁：

```sql
-- 假设 age 列有索引，数据为 [10, 20, 30, 40]
START TRANSACTION;
SELECT * FROM users WHERE age BETWEEN 20 AND 30 FOR UPDATE;
-- 锁定区间：(10, 20], (20, 30], (30, 40)
-- 阻止其他事务在 age=25 插入数据（防止幻读）
```

### 死锁检测

```sql
-- 查看最近死锁
SHOW ENGINE INNODB STATUS;

-- 查看当前等待锁的事务
SELECT * FROM performance_schema.data_lock_waits;

-- 死锁超时设置
SET innodb_lock_wait_timeout = 50;  -- 默认 50 秒
```

---

## 六、复制

### 复制架构

```
Master → Binlog → Slave I/O Thread → Relay Log → Slave SQL Thread
```

### 基于二进制日志的复制

```ini
# my.cnf - Master 配置
[mysqld]
server_id = 1
log_bin = mysql-bin
binlog_format = ROW
expire_logs_days = 7
```

```ini
# my.cnf - Slave 配置
[mysqld]
server_id = 2
relay_log = mysql-relay-bin
read_only = 1
```

```sql
-- Master 创建复制用户
CREATE USER 'repl'@'%' IDENTIFIED BY 'password';
GRANT REPLICATION SLAVE ON *.* TO 'repl'@'%';

-- Slave 配置复制
CHANGE MASTER TO
    MASTER_HOST='master_host',
    MASTER_USER='repl',
    MASTER_PASSWORD='password',
    MASTER_LOG_FILE='mysql-bin.000001',
    MASTER_LOG_POS=0;

START SLAVE;

-- 查看复制状态
SHOW SLAVE STATUS\G;
```

### GTID 复制

```ini
[mysqld]
gtid_mode = ON
enforce_gtid_consistency = ON
```

```sql
CHANGE MASTER TO
    MASTER_HOST='master_host',
    MASTER_USER='repl',
    MASTER_PASSWORD='password',
    MASTER_AUTO_POSITION=1;

START SLAVE;
```

### 同步 vs 半同步

```sql
-- 半同步复制插件
INSTALL PLUGIN rpl_semi_sync_master SONAME 'semisync_master.so';
SET GLOBAL rpl_semi_sync_master_enabled = 1;
SET GLOBAL rpl_semi_sync_slave_enabled = 1;
```

| 复制模式 | 优点 | 缺点 |
|----------|------|------|
| 异步（默认） | 性能好，不影响主库 | 主库宕机可能丢数据 |
| 半同步 | 至少一个从库确认，减少数据丢失 | 增加提交延迟 |
| 全同步（组复制） | 强一致性 | 性能损失大 |

---

## 七、分区

```sql
-- RANGE 分区
CREATE TABLE orders_partitioned (
    id INT,
    user_id INT,
    total DECIMAL(10,2),
    created_at DATE
) PARTITION BY RANGE (YEAR(created_at)) (
    PARTITION p2022 VALUES LESS THAN (2023),
    PARTITION p2023 VALUES LESS THAN (2024),
    PARTITION p2024 VALUES LESS THAN (2025),
    PARTITION p_future VALUES LESS THAN MAXVALUE
);

-- HASH 分区
CREATE TABLE logs_hash (
    id INT,
    level VARCHAR(10),
    message TEXT
) PARTITION BY HASH (id) PARTITIONS 8;

-- LIST 分区
CREATE TABLE employees_by_region (
    id INT,
    name VARCHAR(50),
    region ENUM('north', 'south', 'east', 'west')
) PARTITION BY LIST COLUMNS(region) (
    PARTITION p_north VALUES IN ('north'),
    PARTITION p_south VALUES IN ('south'),
    PARTITION p_east VALUES IN ('east'),
    PARTITION p_west VALUES IN ('west')
);
```

## 八、性能优化

### EXPLAIN 解读

```sql
EXPLAIN SELECT u.username, COUNT(o.id) AS order_count
FROM users u
LEFT JOIN orders o ON u.id = o.user_id
WHERE u.created_at >= '2024-01-01'
GROUP BY u.id
ORDER BY order_count DESC
LIMIT 10;
```

| 列名 | 说明 |
|------|------|
| id | 查询标识符（数字越大越先执行） |
| select_type | SIMPLE / PRIMARY / SUBQUERY / DERIVED / UNION |
| table | 访问的表 |
| type | ALL（全表）/ index（全索引）/ range（范围）/ ref（等值）/ eq_ref / const / system（性能从差到好） |
| possible_keys | 可能使用的索引 |
| key | 实际使用的索引 |
| key_len | 使用的索引长度（越短越好） |
| ref | 索引的参照列 |
| rows | 预计扫描行数（估算值） |
| Extra | Using Index（覆盖索引）/ Using Where / Using Temporary / Using Filesort |

### 慢查询日志

```ini
[mysqld]
slow_query_log = ON
slow_query_log_file = /var/log/mysql/slow.log
long_query_time = 2     # 超过 2 秒记录
log_queries_not_using_indexes = ON
```

```sql
-- 手动分析慢查询
mysqldumpslow -s t -t 10 /var/log/mysql/slow.log
```

### 索引优化策略

```sql
-- 查看索引使用情况
SELECT
    index_name,
    cardinality,
    (cardinality / (SELECT COUNT(*) FROM orders)) AS selectivity
FROM information_schema.statistics
WHERE table_name = 'orders';

-- 强制使用索引
SELECT * FROM users FORCE INDEX (idx_email) WHERE email = 'test@example.com';

-- 忽略索引
SELECT * FROM users IGNORE INDEX (idx_email) WHERE email = 'test@example.com';
```

### 常用性能参数

```ini
[mysqld]
# 缓冲池 - InnoDB 最重要的性能参数
innodb_buffer_pool_size = 4G         # 设置为可用内存的 60-80%
innodb_buffer_pool_instances = 4     # 减少锁争用

# 日志相关
innodb_log_file_size = 1G            # REDO 日志大小
innodb_log_buffer_size = 64M         # REDO 日志缓冲区

# I/O 相关
innodb_io_capacity = 1000            # SSD 可设更高
innodb_flush_method = O_DIRECT       # 绕过 OS 缓存，直接写入磁盘

# 连接
max_connections = 500
thread_cache_size = 100

# 临时表
tmp_table_size = 64M
max_heap_table_size = 64M
```

### 性能问题诊断

```sql
-- 查看当前正在运行的事务
SELECT * FROM information_schema.INNODB_TRX\G

-- 查看锁等待
SELECT * FROM sys.innodb_lock_waits;

-- 索引使用统计
SELECT * FROM sys.schema_index_statistics WHERE table_schema = 'mydb';

-- 查看表 IO
SELECT * FROM sys.io_global_by_file_by_bytes ORDER BY total DESC LIMIT 10;

-- 查询长时间运行的事务
SELECT trx_id, trx_started, TIMEDIFF(NOW(), trx_started) AS duration,
       trx_state, trx_mysql_thread_id
FROM information_schema.INNODB_TRX
HAVING duration > '00:00:05';
```

## 相关条目

- [[PostgreSQLDeep]]
- [[SQLDeep]]
- [[RelationalDatabases]]
- [[查询优化与事务管理]]
- [[Optimization]]
