# 数据库性能优化

## 一、Schema 设计优化

### 规范化与反规范化

**规范化（Normalization）**：

```sql
-- 第三范式设计
CREATE TABLE customers (
    id INT PRIMARY KEY,
    name VARCHAR(100)
);

CREATE TABLE orders (
    id INT PRIMARY KEY,
    customer_id INT,
    total DECIMAL(10,2),
    FOREIGN KEY (customer_id) REFERENCES customers(id)
);

CREATE TABLE order_items (
    id INT PRIMARY KEY,
    order_id INT,
    product_id INT,
    quantity INT,
    price DECIMAL(10,2),
    FOREIGN KEY (order_id) REFERENCES orders(id)
);
```

**反规范化**（减少 JOIN，适合读多写少场景）：

```sql
-- 在 orders 表中冗余存储 customer_name，避免 JOIN
CREATE TABLE orders_denormalized (
    id INT PRIMARY KEY,
    customer_id INT,
    customer_name VARCHAR(100),  -- 冗余字段
    total DECIMAL(10,2),
    created_at TIMESTAMP
);
```

| 方式 | 优点 | 缺点 |
|------|------|------|
| 规范化 | 数据一致性好，无冗余 | 查询需要 JOIN，可能慢 |
| 反规范化 | 查询快，减少 JOIN | 冗余数据，更新需维护一致性 |

### 数据类型选择

```sql
-- ❌ 错误：使用 VARCHAR 存储日期
CREATE TABLE bad_design (
    id INT,
    date_str VARCHAR(20)  -- 无法使用日期函数，无法索引排序
);

-- ✅ 正确：使用合适类型
CREATE TABLE good_design (
    id INT,
    event_date DATE,        -- 存储日期
    price DECIMAL(10,2),    -- 存储金额（不用 FLOAT）
    status TINYINT,         -- 状态枚举，使用最小的整数类型
    content TEXT,           -- 大文本
    is_active BOOLEAN       -- MySQL 实际用 TINYINT(1)
);
```

| 数据类型 | 存储大小 | 说明 |
|----------|----------|------|
| TINYINT | 1 字节 | 0-255 或 -128~127 |
| SMALLINT | 2 字节 | 0-65535 |
| INT | 4 字节 | 0-42亿 |
| BIGINT | 8 字节 | 大整数 |
| DECIMAL(10,2) | 变长 | 精确十进制 |
| VARCHAR(n) | 变长 | n 为最大字符数 |
| CHAR(n) | 固定 n 字节 | 定长字符串 |
| DATETIME | 8 字节 | 1000~9999 年 |
| TIMESTAMP | 4 字节 | 1970~2038 年 |

### 垂直拆分

将表的不常用字段或大字段拆分到独立表：

```sql
-- 原表
CREATE TABLE articles (
    id INT PRIMARY KEY,
    title VARCHAR(200),
    summary VARCHAR(500),
    body LONGTEXT,          -- 大字段，查询频率低
    view_count INT,
    created_at TIMESTAMP
);

-- 垂直拆分后
CREATE TABLE articles_main (
    id INT PRIMARY KEY,
    title VARCHAR(200),
    summary VARCHAR(500),
    view_count INT,
    created_at TIMESTAMP
);

CREATE TABLE articles_body (
    article_id INT PRIMARY KEY,
    body LONGTEXT,
    FOREIGN KEY (article_id) REFERENCES articles_main(id)
);
```

### 水平拆分

```sql
-- 按用户 ID 取模拆分到不同表
-- users_0, users_1, users_2, users_3
-- 应用层路由
SELECT * FROM users_{$shard_id} WHERE id = 1001;
```

---

## 二、索引策略

### 复合索引列顺序

```sql
-- 创建复合索引
CREATE INDEX idx_composite ON orders (user_id, status, created_at);
```

**最左前缀原则**：
- `WHERE user_id = ?` — ✅ 使用索引
- `WHERE user_id = ? AND status = ?` — ✅ 使用索引
- `WHERE user_id = ? AND status = ? AND created_at > ?` — ✅ 使用索引
- `WHERE status = ?` — ❌ 无法使用索引
- `WHERE created_at > ?` — ❌ 无法使用索引

**列顺序策略**：
1. 选择性高的列在前（区分度好）
2. 等值条件列在前，范围条件列在后
3. 频繁作为查询条件的列在前

```sql
-- 计算列选择性
SELECT
    COUNT(DISTINCT user_id) / COUNT(*) AS user_selectivity,
    COUNT(DISTINCT status) / COUNT(*) AS status_selectivity
FROM orders;
-- 选择性高的列优先放在复合索引前列
```

### 覆盖索引

索引包含查询的所有字段，无需回表：

```sql
-- 查询只需要 user_id, status, created_at
-- 如果索引 idx_composite 包含这三列，则实现覆盖索引
EXPLAIN SELECT user_id, status, created_at
FROM orders
WHERE user_id = 1001 AND status = 'paid';
-- Extra: Using index  ← 表示使用了覆盖索引
```

### 索引下推 (ICP)

MySQL 5.6+ 支持，在存储引擎层过滤索引数据，减少回表次数：

```sql
-- 索引 (zipcode, lastname, firstname)
SELECT * FROM users
WHERE zipcode = '100001'
  AND lastname LIKE '张%'
  AND firstname LIKE '三%';
-- 没有 ICP：根据 zipcode 查出所有记录回表再过滤 lastname, firstname
-- 有 ICP：在索引层同时过滤 zipcode, lastname, firstname
```

### 索引失效场景

```sql
-- 1. 对索引列使用函数
WHERE YEAR(created_at) = 2024;       -- ❌ 索引失效
WHERE created_at >= '2024-01-01'
  AND created_at < '2025-01-01';     -- ✅ 索引生效

-- 2. 隐式类型转换
WHERE phone = 13800138000;           -- ❌ phone 是 VARCHAR，隐式转换
WHERE phone = '13800138000';         -- ✅

-- 3. LIKE 前导通配符
WHERE name LIKE '%张%';              -- ❌ 索引失效
WHERE name LIKE '张%';               -- ✅ 索引生效

-- 4. OR 条件
WHERE id = 1 OR name = 'zhangsan';   -- ❌ 可能全表扫描
-- 改为 UNION 或用覆盖索引

-- 5. NOT IN / <>
WHERE status != 'active';            -- ❌ 索引失效
```

---

## 三、查询优化

### 使用 EXPLAIN

```sql
EXPLAIN FORMAT=JSON
SELECT u.username, COUNT(o.id) AS order_count
FROM users u
LEFT JOIN orders o ON u.id = o.user_id
WHERE u.created_at >= '2024-01-01'
GROUP BY u.id
ORDER BY order_count DESC
LIMIT 10;
```

**关注点**：
- `type`：从 system → const → eq_ref → ref → range → index → ALL（性能递减）
- `rows`：预估扫描行数（越小越好）
- `Extra`：Using filesort、Using temporary 是需要优化的信号

### 慢查询分析

```sql
-- MySQL 开启慢查询
SET GLOBAL slow_query_log = ON;
SET GLOBAL long_query_time = 1;
SET GLOBAL log_queries_not_using_indexes = ON;

-- 查看慢查询
mysqldumpslow -s t -t 10 /var/log/mysql/slow.log

-- PostgreSQL 慢查询
SELECT query, calls, total_exec_time / calls AS avg_time_ms
FROM pg_stat_statements
ORDER BY total_exec_time DESC
LIMIT 10;
```

### 查询重写技巧

```sql
-- ❌ 低效写法
SELECT * FROM orders
WHERE total - 10 > 100;

-- ✅ 高效写法（避免对索引列做运算）
SELECT * FROM orders
WHERE total > 110;

-- ❌ LIMIT 大偏移量
SELECT * FROM orders ORDER BY id LIMIT 100000, 20;
-- ✅ 基于游标的分页
SELECT * FROM orders WHERE id > 100000 ORDER BY id LIMIT 20;

-- ❌ SELECT * 多表 JOIN
SELECT * FROM users u JOIN orders o ON u.id = o.user_id;
-- ✅ 只选需要的列
SELECT u.id, u.username, o.id AS order_id, o.total
FROM users u JOIN orders o ON u.id = o.user_id;

-- ✅ 使用 EXISTS 替代 IN（大表时 EXISTS 更快）
SELECT * FROM users u
WHERE EXISTS (SELECT 1 FROM orders o WHERE o.user_id = u.id AND o.total > 1000);
```

### 批量操作

```sql
-- ❌ 逐条 INSERT
INSERT INTO logs VALUES (1, 'msg1');
INSERT INTO logs VALUES (2, 'msg2');
INSERT INTO logs VALUES (3, 'msg3');

-- ✅ 批量 INSERT
INSERT INTO logs VALUES
    (1, 'msg1'),
    (2, 'msg2'),
    (3, 'msg3');

-- ❌ 逐条 UPDATE（在循环中）
UPDATE orders SET status = 'shipped' WHERE id = 1;
UPDATE orders SET status = 'shipped' WHERE id = 2;

-- ✅ 批量 UPDATE
UPDATE orders SET status = 'shipped'
WHERE id IN (1, 2, 3, 4, 5);
```

---

## 四、缓存策略

### Redis 缓存常见模式

**Cache-Aside（旁路缓存）**：

```python
# 读取流程
def get_user(user_id):
    # 1. 尝试从缓存读取
    user = redis.get(f"user:{user_id}")
    if user:
        return user

    # 2. 缓存未命中，从数据库读取
    user = db.query("SELECT * FROM users WHERE id = ?", user_id)

    # 3. 写入缓存（设置过期时间）
    redis.setex(f"user:{user_id}", 3600, user)
    return user

# 更新流程
def update_user(user_id, data):
    # 1. 更新数据库
    db.execute("UPDATE users SET ... WHERE id = ?", user_id, data)

    # 2. 删除缓存（而非更新）
    redis.delete(f"user:{user_id}")
```

**Read-Through**：
- 应用层只通过缓存读取
- 缓存层负责从数据库加载缺失数据

**Write-Through**：
- 写入时同时更新数据库和缓存

**Write-Behind**：
- 先写入缓存，异步批量写回数据库

### 缓存问题及解决方案

| 问题 | 描述 | 解决方案 |
|------|------|----------|
| 缓存穿透 | 查询不存在的数据，每次都穿透到 DB | 缓存空值 / 布隆过滤器 |
| 缓存击穿 | 热点 key 过期，大量请求同时到 DB | 互斥锁 / 热点 key 永不过期 |
| 缓存雪崩 | 大量 key 同时过期 | 过期时间加随机值 / 多级缓存 |

### 查询缓存

```ini
# MySQL 8.0 前
query_cache_type = 1
query_cache_size = 64M
```

MySQL 8.0 已移除查询缓存，推荐使用 Redis 等外部缓存。

---

## 五、读写分离

### 架构

```
         ┌──────────────────────┐
         │    应用程序           │
         │ 读：从库 | 写：主库    │
         └───┬─────────────┬────┘
             │             │
     ┌───────▼─────┐  ┌───▼────────┐
     │   Master     │  │  Replica 1  │
     │  (读写)      │  │  (只读)      │
     └───────┬─────┘  └─────────────┘
             │              ...
             │         ┌───▼────────┐
             └────────▶│  Replica N  │
                       │  (只读)      │
                       └─────────────┘
```

### 实现方式

```python
# 应用层读写分离（Python 示例）
class DatabaseRouter:
    def __init__(self):
        self.master = create_engine("mysql://master_host/db")
        self.slaves = [
            create_engine("mysql://slave1_host/db"),
            create_engine("mysql://slave2_host/db"),
        ]
        self.slave_index = 0

    def write(self, sql, *params):
        return self.master.execute(sql, params)

    def read(self, sql, *params):
        # 轮询从库
        self.slave_index = (self.slave_index + 1) % len(self.slaves)
        return self.slaves[self.slave_index].execute(sql, params)
```

### 主从延迟问题

```sql
-- 读己之写：强制读主库
SELECT * FROM users WHERE id = 1001;  -- 高频查询走从库

-- 刚写入的数据走主库读
def create_order(user_id, product_id):
    db.master.execute("INSERT INTO orders ...")
    # 立即查询自己刚创建的订单，走主库
    return db.master.execute("SELECT * FROM orders WHERE id = LAST_INSERT_ID()")
```

---

## 六、分库分表

### 分片策略

| 策略 | 说明 | 适用场景 |
|------|------|----------|
| Hash 分片 | key % N | 数据均匀分布 |
| Range 分片 | 按 ID/时间范围 | 范围查询多 |
| List 分片 | 按枚举值 | 地域分片 |

```sql
-- Hash 分片计算
-- 分片数 N = 16
-- shard_id = user_id % 16

-- 路由到 user_0 ... user_15
SELECT * FROM user_{$shard_id} WHERE id = 1001;
```

### ShardingSphere

```yaml
# ShardingSphere 配置
rules:
  - !SHARDING
    tables:
      t_order:
        actualDataNodes: ds0.t_order_${0..1}
        tableStrategy:
          standard:
            shardingColumn: order_id
            shardingAlgorithmName: t_order_inline
        keyGenerateStrategy:
          column: order_id
          keyGeneratorName: snowflake
    shardingAlgorithms:
      t_order_inline:
        type: INLINE
        props:
          algorithm-expression: t_order_${order_id % 2}
```

---

## 七、连接池

### HikariCP 配置

```yaml
# Spring Boot 配置
spring.datasource.hikari:
  maximum-pool-size: 20
  minimum-idle: 5
  connection-timeout: 30000
  idle-timeout: 600000
  max-lifetime: 1800000
  pool-name: MyPool
```

### PgBouncer

```ini
[databases]
mydb = host=127.0.0.1 port=5432 dbname=mydb

[pgbouncer]
listen_addr = 0.0.0.0
listen_port = 6432
auth_type = md5
auth_file = /etc/pgbouncer/userlist.txt
pool_mode = transaction    # session/transaction/statement
max_client_conn = 1000
default_pool_size = 25
```

---

## 八、硬件优化

| 组件 | 建议 | 效果 |
|------|------|------|
| CPU | 高频多核（8-16核） | 复杂查询、并发连接 |
| 内存 | 尽可能大 | InnoDB buffer pool 越大越好 |
| 磁盘 | NVMe SSD | 减少 I/O 延迟 |
| 网络 | 万兆网卡 | 减少网络延迟（分布式场景） |

### 操作系统参数

```bash
# Linux 系统优化
# 调整磁盘调度器
echo noop > /sys/block/nvme0n1/queue/scheduler

# 调整虚拟内存
sysctl -w vm.swappiness=1

# 调整文件打开限制
ulimit -n 1000000

# 调整脏页回写
sysctl -w vm.dirty_background_ratio=5
sysctl -w vm.dirty_ratio=10
```

---

## 九、案例实战

### 案例 1：电商订单查询优化

**问题**：订单列表页查询耗时 > 5 秒

```sql
-- 原始查询
SELECT * FROM orders
WHERE user_id = 1001
ORDER BY created_at DESC
LIMIT 20;
```

**诊断**：`EXPLAIN` 显示 `type: ALL`，全表扫描

**优化**：
```sql
-- 1. 添加复合索引
ALTER TABLE orders ADD INDEX idx_user_time (user_id, created_at DESC);

-- 2. 避免 SELECT *
SELECT id, order_no, total, status, created_at
FROM orders
WHERE user_id = 1001
ORDER BY created_at DESC
LIMIT 20;

-- 3. 如果还需更多字段，使用覆盖索引 + JOIN
SELECT o.*, oi.product_name
FROM (
    SELECT id FROM orders
    WHERE user_id = 1001
    ORDER BY created_at DESC
    LIMIT 20
) recent
JOIN orders o ON recent.id = o.id
LEFT JOIN order_items oi ON o.id = oi.order_id;
```

**效果**：5.2 秒 → 15 毫秒

### 案例 2：大表分页优化

**问题**：翻页到深页码时越来越慢

```sql
-- 慢查询：offset 越大越慢
SELECT * FROM logs ORDER BY id LIMIT 1000000, 20;
```

**方案一：基于游标的分页**
```sql
-- 记录上一页最后一条的 id
SELECT * FROM logs
WHERE id > 上一页最后ID
ORDER BY id
LIMIT 20;
```

**方案二：延迟 JOIN**
```sql
SELECT l.*
FROM logs l
INNER JOIN (
    SELECT id FROM logs
    ORDER BY id
    LIMIT 1000000, 20
) tmp ON l.id = tmp.id;
```

### 案例 3：热点账户更新

**问题**：热门商品库存更新高频，行锁竞争严重

**方案一：库存分段**
```sql
-- 将库存拆分到多行
CREATE TABLE product_stock (
    id INT PRIMARY KEY AUTO_INCREMENT,
    product_id INT,
    segment_id INT,       -- 0 ~ 9
    stock INT
);

-- 更新时随机选择一个 segment
UPDATE product_stock
SET stock = stock - 1
WHERE product_id = 1001
  AND segment_id = FLOOR(RAND() * 10)
  AND stock > 0;

-- 查询总库存
SELECT SUM(stock) FROM product_stock WHERE product_id = 1001;
```

**方案二：Redis 扣减 + 异步同步**
```python
def deduct_stock(product_id, qty):
    # Redis 原子扣减
    remaining = redis.decrby(f"stock:{product_id}", qty)
    if remaining < 0:
        redis.incrby(f"stock:{product_id}", qty)  # 回滚
        return False
    # 异步写回数据库
    kafka.send("stock_update", {"product_id": product_id, "qty": qty})
    return True
```

## 相关条目

- [[查询优化与事务管理]]
- [[Transaction]]
- [[MySQL_Deep]]
- [[Redis_Deep]]
- [[RelationalDatabases]]
