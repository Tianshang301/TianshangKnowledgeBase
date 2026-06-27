---
aliases: [SQLDeep]
tags: ['DatabasesAndInformationSystems', 'SQLDeep']
created: 2026-05-16
updated: 2026-05-16
---

# SQL 完全指南

## 概述

SQL（Structured Query Language）是操作关系型数据库的标准语言。本指南覆盖 SQL 的核心概念和常用操作。

---

## 1. DDL — 数据定义语言

DDL 用于定义数据库结构：创建、修改、删除表、索引等。

### CREATE TABLE

```sql
CREATE TABLE users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL,
    age INT CHECK (age >= 0 AND age <= 150),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE orders (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    total DECIMAL(10, 2) NOT NULL DEFAULT 0.00,
    status ENUM('pending', 'paid', 'shipped', 'cancelled') DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);
```

### ALTER TABLE

```sql
-- 添加列
ALTER TABLE users ADD COLUMN phone VARCHAR(20) AFTER email;

-- 修改列类型
ALTER TABLE users MODIFY COLUMN phone VARCHAR(30);

-- 重命名列
ALTER TABLE users CHANGE COLUMN phone mobile VARCHAR(20);

-- 添加索引
ALTER TABLE users ADD INDEX idx_email (email);

-- 添加外键
ALTER TABLE orders ADD CONSTRAINT fk_user FOREIGN KEY (user_id) REFERENCES users(id);

-- 删除列
ALTER TABLE users DROP COLUMN mobile;
```

### DROP TABLE

```sql
DROP TABLE IF EXISTS temp_data;
TRUNCATE TABLE logs;  -- 快速清空表，不可回滚
```

---

## 2. DML — 数据操作语言

### INSERT

```sql
-- 插入单行
INSERT INTO users (username, email, age) VALUES ('zhangsan', 'zhangsan@example.com', 25);

-- 插入多行
INSERT INTO users (username, email, age) VALUES
    ('lisi', 'lisi@example.com', 30),
    ('wangwu', 'wangwu@example.com', 28);

-- 从查询结果插入
INSERT INTO user_backup (id, username, email)
SELECT id, username, email FROM users WHERE deleted_at IS NOT NULL;

-- INSERT ... ON DUPLICATE KEY UPDATE (MySQL)
INSERT INTO users (id, username, email) VALUES (1, 'zhangsan', 'new@example.com')
ON DUPLICATE KEY UPDATE email = VALUES(email);
```

### UPDATE

```sql
UPDATE users SET age = 26 WHERE username = 'zhangsan';

UPDATE orders
SET status = 'shipped', updated_at = NOW()
WHERE id = 1001;
```

### DELETE

```sql
DELETE FROM users WHERE id = 10;

-- 删除所有行（保留表结构）
DELETE FROM temp_logs;
```

### SELECT — 查询

```sql
-- 基础查询
SELECT id, username, email FROM users;

-- 别名
SELECT u.username AS name, u.email FROM users u;

-- 去重
SELECT DISTINCT status FROM orders;

-- 计算字段
SELECT id, total * 0.9 AS discounted_total FROM orders;

-- 限制结果
SELECT * FROM users LIMIT 10 OFFSET 20;
```

---

## 3. 过滤条件

### WHERE 子句

```sql
-- 等于
SELECT * FROM users WHERE username = 'zhangsan';

-- 不等于
SELECT * FROM users WHERE age != 30;

-- 比较
SELECT * FROM products WHERE price > 100;
SELECT * FROM products WHERE price BETWEEN 50 AND 200;

-- LIKE 模糊匹配
SELECT * FROM users WHERE username LIKE 'zhang%';   -- 以 zhang 开头
SELECT * FROM users WHERE email LIKE '%@example.com'; -- 特定域名
SELECT * FROM users WHERE phone LIKE '138________';   -- 138 开头的手机号

-- IN 列表
SELECT * FROM users WHERE age IN (18, 25, 30, 35);

-- IS NULL
SELECT * FROM users WHERE deleted_at IS NULL;
SELECT * FROM users WHERE deleted_at IS NOT NULL;

-- 组合条件
SELECT * FROM orders
WHERE status = 'pending'
  AND total > 100
  AND (created_at >= '2024-01-01' OR user_id IN (1, 2, 3));
```

---

## 4. JOIN 连接

### INNER JOIN

返回两表中满足连接条件的匹配行。

```sql
SELECT u.username, o.id AS order_id, o.total, o.status
FROM users u
INNER JOIN orders o ON u.id = o.user_id;
```

### LEFT JOIN

返回左表所有行，右表无匹配时填充 NULL。

```sql
SELECT u.username, COUNT(o.id) AS order_count
FROM users u
LEFT JOIN orders o ON u.id = o.user_id
GROUP BY u.id;
```

### RIGHT JOIN

返回右表所有行，左表无匹配时填充 NULL。

```sql
SELECT o.id AS order_id, u.username
FROM users u
RIGHT JOIN orders o ON u.id = o.user_id;
```

### FULL OUTER JOIN

返回两表所有行，不匹配的一侧填充 NULL（MySQL 不支持，用 UNION 模拟）。

```sql
-- MySQL 模拟 FULL OUTER JOIN
SELECT u.username, o.id AS order_id
FROM users u
LEFT JOIN orders o ON u.id = o.user_id
UNION
SELECT u.username, o.id AS order_id
FROM users u
RIGHT JOIN orders o ON u.id = o.user_id;
```

### CROSS JOIN

笛卡尔积，每行与另一表每行组合。

```sql
SELECT colors.name, sizes.name
FROM colors
CROSS JOIN sizes;
```

### Self-Join

表与自身连接。

```sql
-- 查找员工及其管理者
SELECT e.name AS employee, m.name AS manager
FROM employees e
LEFT JOIN employees m ON e.manager_id = m.id;
```

---

## 5. 分组与聚合

### 聚合函数

```sql
SELECT
    COUNT(*) AS total_users,
    COUNT(email) AS users_with_email,  -- 不统计 NULL
    AVG(age) AS avg_age,
    MAX(age) AS max_age,
    MIN(age) AS min_age,
    SUM(orders.total) AS revenue
FROM users
LEFT JOIN orders ON users.id = orders.user_id;
```

### GROUP_CONCAT (MySQL)

```sql
SELECT user_id, GROUP_CONCAT(product_name ORDER BY created_at SEPARATOR ', ') AS products
FROM order_items
GROUP BY user_id;
```

### GROUP BY + HAVING

```sql
-- 每个用户的订单数，只显示订单数 > 3 的用户
SELECT user_id, COUNT(*) AS order_count, SUM(total) AS total_spent
FROM orders
GROUP BY user_id
HAVING order_count > 3
ORDER BY total_spent DESC;

-- 每个月订单统计
SELECT
    DATE_FORMAT(created_at, '%Y-%m') AS month,
    COUNT(*) AS order_count,
    SUM(total) AS revenue
FROM orders
WHERE created_at >= '2024-01-01'
GROUP BY month
ORDER BY month;
```

---

## 6. 排序

```sql
-- 单列排序
SELECT * FROM products ORDER BY price DESC;

-- 多列排序
SELECT * FROM orders ORDER BY status ASC, created_at DESC;

-- 按表达式排序
SELECT *, (price * quantity) AS total FROM order_items
ORDER BY total DESC;

-- 按聚合结果排序
SELECT user_id, COUNT(*) cnt FROM orders
GROUP BY user_id ORDER BY cnt DESC;
```

---

## 7. 子查询

### 非关联子查询

子查询独立执行，结果用于外层查询。

```sql
-- 标量子查询
SELECT username, (SELECT COUNT(*) FROM orders WHERE user_id = users.id) AS order_count
FROM users;

-- 行子查询
SELECT * FROM products
WHERE price > (SELECT AVG(price) FROM products);

-- 存在性检查
SELECT * FROM users u
WHERE EXISTS (SELECT 1 FROM orders o WHERE o.user_id = u.id AND o.total > 1000);

-- IN 子查询
SELECT * FROM users
WHERE id IN (SELECT user_id FROM orders WHERE total > 500);

-- FROM 子句子查询
SELECT avg_order.avg_total, users.username
FROM users
JOIN (SELECT user_id, AVG(total) AS avg_total FROM orders GROUP BY user_id) avg_order
ON users.id = avg_order.user_id;
```

### 关联子查询

子查询引用外层查询的列，逐行执行。

```sql
-- 查找超过用户平均订单金额的订单
SELECT o.*
FROM orders o
WHERE o.total > (SELECT AVG(total) FROM orders WHERE user_id = o.user_id);

-- 查询最新订单
SELECT o.*
FROM orders o
WHERE o.created_at = (SELECT MAX(created_at) FROM orders WHERE user_id = o.user_id);
```

---

## 8. 集合操作

```sql
-- UNION（去重合并）
SELECT username FROM users_2023
UNION
SELECT username FROM users_2024;

-- UNION ALL（全部合并，不去重）
SELECT city FROM address_beijing
UNION ALL
SELECT city FROM address_shanghai;

-- INTERSECT（交集，MySQL 不支持）
SELECT user_id FROM orders_2023
INTERSECT
SELECT user_id FROM orders_2024;

-- EXCEPT（差集，MySQL 不支持）
SELECT user_id FROM all_users
EXCEPT
SELECT user_id FROM blacklist;
```

MySQL 模拟 INTERSECT：

```sql
SELECT DISTINCT a.user_id
FROM orders_2023 a
INNER JOIN orders_2024 b ON a.user_id = b.user_id;
```

---

## 9. CTE — 公用表表达式

### 基础 CTE

```sql
WITH user_orders AS (
    SELECT user_id, COUNT(*) AS order_count, SUM(total) AS total_spent
    FROM orders
    GROUP BY user_id
)
SELECT u.username, uo.order_count, uo.total_spent
FROM users u
JOIN user_orders uo ON u.id = uo.user_id
ORDER BY uo.total_spent DESC;
```

### 递归 CTE

```sql
-- 生成数字序列
WITH RECURSIVE numbers(n) AS (
    SELECT 1
    UNION ALL
    SELECT n + 1 FROM numbers WHERE n < 100
)
SELECT n FROM numbers;

-- 查询组织树
WITH RECURSIVE org_tree AS (
    -- 基础情况：顶层节点
    SELECT id, name, parent_id, 1 AS level
    FROM departments
    WHERE parent_id IS NULL

    UNION ALL

    -- 递归：子节点
    SELECT d.id, d.name, d.parent_id, ot.level + 1
    FROM departments d
    JOIN org_tree ot ON d.parent_id = ot.id
)
SELECT * FROM org_tree ORDER BY level, id;
```

---

## 10. 窗口函数

### 排名函数

```sql
SELECT
    id,
    user_id,
    total,
    ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY created_at DESC) AS rn,
    RANK()       OVER (ORDER BY total DESC) AS rank,
    DENSE_RANK() OVER (ORDER BY total DESC) AS dense_rank,
    NTILE(4)     OVER (ORDER BY total DESC) AS quartile
FROM orders;
```

### 偏移函数

```sql
SELECT
    id, user_id, total, created_at,
    LAG(total)  OVER (PARTITION BY user_id ORDER BY created_at) AS prev_order_total,
    LEAD(total) OVER (PARTITION BY user_id ORDER BY created_at) AS next_order_total
FROM orders;
```

### 聚合窗口函数

```sql
SELECT
    id, user_id, total, created_at,
    SUM(total)       OVER (PARTITION BY user_id ORDER BY created_at) AS running_total,
    AVG(total)       OVER (PARTITION BY user_id) AS avg_order_total,
    total - AVG(total) OVER (PARTITION BY user_id) AS diff_from_avg
FROM orders;
```

---

## 11. 约束

```sql
CREATE TABLE employees (
    id          INT PRIMARY KEY AUTO_INCREMENT,      -- 主键约束
    emp_no      VARCHAR(20) NOT NULL UNIQUE,          -- 非空 + 唯一约束
    name        VARCHAR(50) NOT NULL,
    email       VARCHAR(100) UNIQUE,                  -- 唯一约束
    age         INT CHECK (age >= 18),               -- 检查约束
    department  VARCHAR(50) DEFAULT '未分配',          -- 默认约束
    manager_id  INT,
    created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (manager_id) REFERENCES employees(id) -- 外键约束
);
```

---

## 12. 索引

```sql
-- 单列索引
CREATE INDEX idx_name ON employees(name);

-- 唯一索引
CREATE UNIQUE INDEX idx_email ON employees(email);

-- 复合索引（最左前缀原则）
CREATE INDEX idx_dept_age ON employees(department, age);

-- 全文索引
CREATE FULLTEXT INDEX idx_content ON articles(title, body);

-- 删除索引
DROP INDEX idx_name ON employees;

-- 查看索引
SHOW INDEX FROM employees;
```

### 索引使用原则

| 原则 | 说明 |
|------|------|
| 最左前缀 | 复合索引 (a,b,c)，查询条件需从 a 开始 |
| 高选择性 | 选择度高的列在前（如 ID，email），选择性低的在后（如性别） |
| 覆盖索引 | 索引包含所有查询字段，避免回表 |
| 避免冗余 | 已有 (a,b) 索引时，(a) 索引是冗余的 |
| LIKE 优化 | LIKE 'abc%' 可用索引，LIKE '%abc' 不能 |

## 相关条目

- [[MySQLDeep]]
- [[PostgreSQLDeep]]
- [[RelationalDatabases]]
- [[查询优化与事务管理]]
- [[Transaction]]
