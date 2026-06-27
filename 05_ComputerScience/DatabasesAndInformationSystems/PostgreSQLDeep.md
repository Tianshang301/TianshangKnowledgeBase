---
aliases: [PostgreSQLDeep]
tags: ['DatabasesAndInformationSystems', 'PostgreSQLDeep']
created: 2026-05-16
updated: 2026-05-16
---

# PostgreSQL 指南

## 一、架构概览

### 进程架构

PostgreSQL 采用多进程架构（而非 MySQL 的多线程模型）：

```
┌──────────────────────────────────────────────────┐
│                  Postmaster（主进程）               │
│  监听端口（默认 5432），fork 子进程处理连接           │
├──────────────────────────────────────────────────┤
│                                                    │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐           │
│  │ Backend  │  │ Backend  │  │ Backend  │  ...     │
│  │ Process 1│  │ Process 2│  │ Process 3│          │
│  └────┬────┘  └────┬────┘  └────┬────┘           │
│       │             │             │                │
│  ┌────┴────┐  ┌────┴────┐  ┌────┴────┐           │
│  │ Shared  │  │ Shared  │  │ Shared  │           │
│  │ Buffers │  │ Buffers │  │ Buffers │           │
│  └─────────┘  └─────────┘  └─────────┘           │
├──────────────────────────────────────────────────┤
│              后台进程                              │
│  WAL Writer | Checkpointer | Autovacuum | Stats   │
│  Archiver | Logical Replication | WalReceiver     │
└──────────────────────────────────────────────────┘
```

### 共享内存

| 组件 | 说明 |
|------|------|
| Shared Buffers | 数据页缓存，类似 Oracle DB buffer cache |
| WAL Buffer | WAL 日志缓冲区 |
| Clog Buffer | 事务提交状态缓存 |

### WAL（Write-Ahead Logging）

- 事务提交前先写入 WAL 日志
- 数据文件写入延迟到检查点
- 支持 PITR（时间点恢复）
- 流式复制依赖 WAL

### 检查点 (Checkpoint)

- 将 shared buffers 中的脏页写入磁盘
- 更新控制文件
- 由 `checkpoint_timeout` 和 `max_wal_size` 控制触发

```sql
SHOW checkpoint_timeout;   -- 默认 5min
SHOW max_wal_size;         -- 默认 1GB
```

---

## 二、数据类型

### 高级数据类型

```sql
-- JSONB（推荐，支持索引）
CREATE TABLE events (
    id SERIAL PRIMARY KEY,
    payload JSONB,
    created_at TIMESTAMPTZ DEFAULT NOW()
);
CREATE INDEX idx_events_payload ON events USING GIN (payload);

-- 查询 JSONB
SELECT * FROM events WHERE payload @> '{"type": "click"}';
SELECT * FROM events WHERE payload -> 'user' ->> 'name' = 'zhangsan';

-- 数组类型
CREATE TABLE articles (
    id SERIAL PRIMARY KEY,
    title TEXT,
    tags TEXT[],
    ratings INTEGER[3]
);
INSERT INTO articles (title, tags, ratings) VALUES
    ('PG 教程', ARRAY['postgresql', 'database'], '{5, 4, 5}');

-- 数组查询
SELECT * FROM articles WHERE 'postgresql' = ANY(tags);
SELECT * FROM articles WHERE tags @> ARRAY['postgresql', 'database'];

-- hstore（键值对）
CREATE EXTENSION hstore;
CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    name TEXT,
    attributes hstore
);
INSERT INTO products VALUES (1, '笔记本电脑', 'color => silver, weight => 1.5kg');
SELECT * FROM products WHERE attributes ? 'color';

-- 枚举类型
CREATE TYPE order_status AS ENUM ('pending', 'paid', 'shipped', 'cancelled');
CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    status order_status DEFAULT 'pending'
);

-- 范围类型
CREATE TABLE reservation (
    room_id INT,
    period TSRANGE,
    EXCLUDE USING GIST (room_id WITH =, period WITH &&)
);
INSERT INTO reservation VALUES
    (101, '[2024-06-01 10:00, 2024-06-01 12:00)');

-- UUID
CREATE EXTENSION "uuid-ossp";
CREATE TABLE sessions (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    user_id INT,
    data JSONB
);

-- 几何类型
CREATE TABLE locations (
    id SERIAL PRIMARY KEY,
    name TEXT,
    coord POINT,
    area POLYGON
);
```

---

## 三、索引类型

| 索引类型 | 适用场景 | 示例 |
|----------|----------|------|
| B-tree | 等值、范围、排序 | 默认索引类型 |
| Hash | 等值查询 | `USING HASH` |
| GiST | 几何、全文搜索 | `USING GiST` |
| GIN | JSONB、数组、全文搜索 | `USING GIN` |
| SP-GiST | 空间分区、四叉树 | `USING SP-GiST` |
| BRIN | 大表、数据自然有序 | `USING BRIN` |
| 部分索引 | 特定条件查询 | `WHERE status = 'active'` |
| 表达式索引 | 函数/表达式查询 | `ON (LOWER(email))` |

```sql
-- B-tree（默认）
CREATE INDEX idx_btree ON users (username);

-- Hash（仅等值查询）
CREATE INDEX idx_hash ON users USING HASH (email);

-- GiST（范围、几何）
CREATE INDEX idx_gist ON locations USING GIST (coord);
CREATE INDEX idx_gist_range ON reservation USING GIST (period);

-- GIN（JSONB、数组、全文搜索）
CREATE INDEX idx_gin ON events USING GIN (payload jsonb_path_ops);
CREATE INDEX idx_gin_fts ON articles USING GIN (to_tsvector('english', title));

-- BRIN（适合自然有序的大表）
CREATE INDEX idx_brin ON logs USING BRIN (created_at) WITH (pages_per_range = 32);

-- 部分索引
CREATE INDEX idx_active_users ON users (id) WHERE is_active = true;

-- 表达式索引
CREATE INDEX idx_lower_email ON users (LOWER(email));
SELECT * FROM users WHERE LOWER(email) = 'test@example.com';
```

---

## 四、全文搜索

```sql
-- 创建全文搜索向量列
ALTER TABLE articles ADD COLUMN fts_vector TSVECTOR;

-- 更新向量
UPDATE articles SET fts_vector =
    setweight(to_tsvector('english', COALESCE(title, '')), 'A') ||
    setweight(to_tsvector('english', COALESCE(body, '')), 'B');

-- 创建 GIN 索引
CREATE INDEX idx_fts ON articles USING GIN (fts_vector);

-- 全文搜索查询
SELECT title, ts_rank(fts_vector, query) AS rank
FROM articles, to_tsquery('english', 'postgresql & database') query
WHERE fts_vector @@ query
ORDER BY rank DESC;

-- 高亮搜索结果
SELECT ts_headline('english', body, query, 'MaxWords=50, MinWords=20')
FROM articles, to_tsquery('english', 'postgresql') query
WHERE fts_vector @@ query;

-- 简单搜索
SELECT * FROM articles
WHERE to_tsvector('simple', title) @@ plainto_tsquery('simple', 'postgresql guide');
```

---

## 五、高级功能

### CTE 和递归查询

```sql
-- 非递归 CTE
WITH regional_sales AS (
    SELECT region, SUM(amount) AS total_sales
    FROM orders
    GROUP BY region
)
SELECT region, total_sales
FROM regional_sales
WHERE total_sales > (SELECT AVG(total_sales) FROM regional_sales);

-- 递归 CTE：查询组织树
WITH RECURSIVE org_tree AS (
    SELECT id, name, parent_id, 1 AS depth, name::TEXT AS path
    FROM departments
    WHERE parent_id IS NULL

    UNION ALL

    SELECT d.id, d.name, d.parent_id, ot.depth + 1,
           ot.path || ' -> ' || d.name
    FROM departments d
    INNER JOIN org_tree ot ON d.parent_id = ot.id
)
SELECT * FROM org_tree ORDER BY path;

-- 递归 CTE：查询地铁线路
WITH RECURSIVE route AS (
    SELECT station_id, station_name, 0 AS transfers
    FROM stations WHERE station_name = '天安门东'

    UNION

    SELECT s.station_id, s.station_name, r.transfers + 1
    FROM route r
    JOIN connections c ON r.station_id = c.station_id
    JOIN stations s ON c.next_station_id = s.station_id
    WHERE r.transfers < 20
)
SELECT * FROM route WHERE station_name = '海淀黄庄';
```

### 窗口函数

```sql
-- 排名函数
SELECT
    department, name, salary,
    ROW_NUMBER() OVER (PARTITION BY department ORDER BY salary DESC) AS rn,
    RANK()       OVER (PARTITION BY department ORDER BY salary DESC) AS rank,
    DENSE_RANK() OVER (PARTITION BY department ORDER BY salary DESC) AS dr
FROM employees;

-- 偏移与统计
SELECT
    date, revenue,
    LAG(revenue, 1) OVER (ORDER BY date) AS prev_day,
    LAG(revenue, 7) OVER (ORDER BY date) AS prev_week,
    AVG(revenue) OVER (ORDER BY date ROWS BETWEEN 6 PRECEDING AND CURRENT ROW) AS ma_7d
FROM daily_revenue;

-- 分组统计
SELECT
    department_id, employee_name, salary,
    SUM(salary) OVER (PARTITION BY department_id) AS dept_total,
    ROUND(salary * 100.0 / SUM(salary) OVER (PARTITION BY department_id), 2) AS pct
FROM employees;
```

### 表继承

```sql
CREATE TABLE person (
    id SERIAL PRIMARY KEY,
    name TEXT,
    age INT
);

CREATE TABLE student (
    student_id TEXT UNIQUE,
    grade INT
) INHERITS (person);

CREATE TABLE teacher (
    employee_id TEXT UNIQUE,
    subject TEXT
) INHERITS (person);

INSERT INTO student (name, age, student_id, grade) VALUES
    ('张三', 18, 'S001', 12);

INSERT INTO teacher (name, age, employee_id, subject) VALUES
    ('李老师', 35, 'T001', '数学');

-- 查询所有 person（包括子表数据）
SELECT * FROM ONLY person;    -- 仅父表
SELECT * FROM person;         -- 包含子表
```

### 分区表

```sql
-- 声明式分区
CREATE TABLE measurements (
    city_id INT NOT NULL,
    logdate DATE NOT NULL,
    peaktemp INT,
    unitsales INT
) PARTITION BY RANGE (logdate);

CREATE TABLE measurements_2023_q1 PARTITION OF measurements
    FOR VALUES FROM ('2023-01-01') TO ('2023-04-01');
CREATE TABLE measurements_2023_q2 PARTITION OF measurements
    FOR VALUES FROM ('2023-04-01') TO ('2023-07-01');
CREATE TABLE measurements_2023_q3 PARTITION OF measurements
    FOR VALUES FROM ('2023-07-01') TO ('2023-10-01');

-- LIST 分区
CREATE TABLE cities (
    city_id INT NOT NULL,
    city_name TEXT NOT NULL,
    country TEXT NOT NULL
) PARTITION BY LIST (country);

CREATE TABLE cities_china PARTITION OF cities FOR VALUES IN ('中国');
CREATE TABLE cities_us PARTITION OF cities FOR VALUES IN ('美国');

-- HASH 分区
CREATE TABLE users_hash PARTITION BY HASH (user_id);
CREATE TABLE users_hash_0 PARTITION OF users_hash FOR VALUES WITH (MODULUS 4, REMAINDER 0);
CREATE TABLE users_hash_1 PARTITION OF users_hash FOR VALUES WITH (MODULUS 4, REMAINDER 1);
CREATE TABLE users_hash_2 PARTITION OF users_hash FOR VALUES WITH (MODULUS 4, REMAINDER 2);
CREATE TABLE users_hash_3 PARTITION OF users_hash FOR VALUES WITH (MODULUS 4, REMAINDER 3);
```

---

## 六、PL/pgSQL

### 函数

```sql
CREATE OR REPLACE FUNCTION get_user_order_count(user_id INT)
RETURNS INT
LANGUAGE plpgsql
AS $$
DECLARE
    order_count INT;
BEGIN
    SELECT COUNT(*) INTO order_count
    FROM orders
    WHERE orders.user_id = get_user_order_count.user_id;

    RETURN order_count;
END;
$$;

-- 调用
SELECT get_user_order_count(1);
```

### 带输出参数

```sql
CREATE OR REPLACE FUNCTION get_user_stats(
    IN user_id INT,
    OUT total_orders INT,
    OUT total_spent NUMERIC,
    OUT avg_order NUMERIC
)
LANGUAGE plpgsql
AS $$
BEGIN
    SELECT COUNT(*), COALESCE(SUM(total), 0), COALESCE(AVG(total), 0)
    INTO total_orders, total_spent, avg_order
    FROM orders WHERE user_id = user_id;
END;
$$;
```

### 触发器

```sql
CREATE OR REPLACE FUNCTION audit_order_changes()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
BEGIN
    IF TG_OP = 'INSERT' THEN
        INSERT INTO audit_log(table_name, operation, new_data, changed_at)
        VALUES ('orders', 'INSERT', row_to_json(NEW), NOW());
        RETURN NEW;
    ELSIF TG_OP = 'UPDATE' THEN
        INSERT INTO audit_log(table_name, operation, old_data, new_data, changed_at)
        VALUES ('orders', 'UPDATE', row_to_json(OLD), row_to_json(NEW), NOW());
        RETURN NEW;
    ELSIF TG_OP = 'DELETE' THEN
        INSERT INTO audit_log(table_name, operation, old_data, changed_at)
        VALUES ('orders', 'DELETE', row_to_json(OLD), NOW());
        RETURN OLD;
    END IF;
END;
$$;

CREATE TRIGGER trg_audit_orders
AFTER INSERT OR UPDATE OR DELETE ON orders
FOR EACH ROW EXECUTE FUNCTION audit_order_changes();
```

### 存储过程

```sql
CREATE OR REPLACE PROCEDURE transfer_funds(
    from_account INT,
    to_account INT,
    amount NUMERIC
)
LANGUAGE plpgsql
AS $$
BEGIN
    UPDATE accounts SET balance = balance - amount WHERE id = from_account;
    IF NOT FOUND THEN
        RAISE EXCEPTION '源账户 % 不存在', from_account;
    END IF;

    UPDATE accounts SET balance = balance + amount WHERE id = to_account;
    IF NOT FOUND THEN
        RAISE EXCEPTION '目标账户 % 不存在', to_account;
    END IF;

    INSERT INTO transfer_log(from_account, to_account, amount, created_at)
    VALUES (from_account, to_account, amount, NOW());
END;
$$;

CALL transfer_funds(1, 2, 500.00);
```

---

## 七、复制

### 流式复制

```ini
# primary: postgresql.conf
wal_level = replica
max_wal_senders = 10
wal_keep_size = 1024    # MB
```

```ini
# standby: postgresql.conf
primary_conninfo = 'host=primary_host port=5432 user=repl password=xxx'
hot_standby = on
```

```bash
# standby 上执行基础备份
pg_basebackup -h primary_host -D /var/lib/pgsql/data -U repl -P -v -R
```

### 逻辑复制

```ini
# postgresql.conf
wal_level = logical
max_replication_slots = 10
```

```sql
-- Publisher
CREATE PUBLICATION my_pub FOR TABLE users, orders;
CREATE PUBLICATION all_tables FOR ALL TABLES;

-- Subscriber
CREATE SUBSCRIPTION my_sub
CONNECTION 'host=pub_host port=5432 dbname=mydb user=repl password=xxx'
PUBLICATION my_pub;
```

---

## 八、VACUUM

```sql
-- 手动 VACUUM
VACUUM;                    -- 清理死元组（不释放空间给 OS）
VACUUM FULL;               -- 彻底清理（加排他锁，重写表）
VACUUM ANALYZE;            -- 清理并更新统计信息
VACUUM VERBOSE;            -- 显示详细清理信息

-- 查看表膨胀
SELECT
    schemaname, tablename,
    n_live_tup, n_dead_tup,
    ROUND(n_dead_tup * 100.0 / NULLIF(n_live_tup + n_dead_tup, 0), 2) AS dead_pct
FROM pg_stat_user_tables
WHERE n_dead_tup > 1000
ORDER BY n_dead_tup DESC;
```

### Autovacuum 配置

```ini
autovacuum = on
autovacuum_naptime = 1min
autovacuum_vacuum_threshold = 50
autovacuum_vacuum_scale_factor = 0.2
autovacuum_analyze_threshold = 50
autovacuum_analyze_scale_factor = 0.1
```

---

## 九、监控

```sql
-- 查询当前活动会话
SELECT pid, state, query, query_start, wait_event_type, wait_event
FROM pg_stat_activity
WHERE state != 'idle'
ORDER BY query_start;

-- 查询运行最长的查询
SELECT pid, now() - pg_stat_activity.query_start AS duration, query
FROM pg_stat_activity
WHERE state = 'active'
ORDER BY duration DESC;

-- 查看表访问统计
SELECT
    schemaname, tablename,
    seq_scan, seq_tup_read,
    idx_scan, idx_tup_fetch,
    n_tup_ins, n_tup_upd, n_tup_del
FROM pg_stat_user_tables
ORDER BY seq_scan DESC;

-- 查看索引使用情况
SELECT
    schemaname, tablename, indexrelname,
    idx_scan, idx_tup_read, idx_tup_fetch
FROM pg_stat_user_indexes
ORDER BY idx_scan;

-- 查看慢查询（需要 pg_stat_statements 插件）
CREATE EXTENSION pg_stat_statements;

SELECT
    query,
    calls,
    mean_exec_time,
    total_exec_time,
    ROWS,
    shared_blks_hit,
    shared_blks_read
FROM pg_stat_statements
ORDER BY total_exec_time DESC
LIMIT 10;
```

---

## 十、vs MySQL 对比

| 特性 | PostgreSQL | MySQL |
|------|------------|-------|
| 许可证 | PostgreSQL License（类似 MIT） | GPL / 商业版 |
| 进程模型 | 多进程 | 多线程 |
| 存储引擎 | 统一存储引擎 | 插件式（InnoDB, MyISAM 等） |
| SQL 标准兼容 | 非常严格 | 宽松，有扩展 |
| JSON 支持 | JSONB（二进制，带索引） | JSON（文本存储，8.0+ 支持多值索引） |
| 索引类型 | B-tree, Hash, GiST, GIN, SP-GiST, BRIN | B-tree, Hash, Full-text, Spatial, 倒排（8.0+） |
| 全文搜索 | 内置（tsvector/tsquery） | 内置（InnoDB 5.6+） |
| MVCC | 每个元组独立版本 | UNDO 日志实现 |
| 复制 | 流式（物理 + 逻辑） | 基于 binlog 的逻辑复制 |
| 分区 | 声明式（原生） | 分区表（5.1+） |
| 并行查询 | ✅（多核并行） | ❌（8.0 部分支持） |
| 排序规则 | ICU 支持，非常丰富 | 有限 |
| 复杂查询优化 | 优秀的 CBO，支持 JOIN 重排 | 优化器较弱 |
| 写性能 | 一般（多进程、MVCC 开销大） | 较好（特别是 InnoDB） |
| GIS 空间数据 | PostGIS（最强开源地理数据库） | MySQL Spatial（功能有限） |
| 推荐场景 | 复杂查询、数据仓库、GIS、标准合规 | Web 应用、高并发简单查询、读写分离 |

## 相关条目

- [[MySQLDeep]]
- [[SQLDeep]]
- [[RelationalDatabases]]
- [[查询优化与事务管理]]
- [[Transaction]]
