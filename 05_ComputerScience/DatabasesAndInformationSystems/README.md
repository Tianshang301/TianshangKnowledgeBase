---
aliases: [README]
tags: ['DatabasesAndInformationSystems', 'README']
created: 2026-05-16
updated: 2026-05-16
---

# 数据库工具指南

## MySQL 常用命令

### 建库建表

```sql
-- 创建数据库
CREATE DATABASE mydb CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- 使用数据库
USE mydb;

-- 创建表
CREATE TABLE users (
    id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL,
    password_hash CHAR(60) NOT NULL,
    age TINYINT UNSIGNED DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_email (email),
    INDEX idx_age (age)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 修改表
ALTER TABLE users ADD COLUMN phone VARCHAR(20) AFTER email;
ALTER TABLE users MODIFY COLUMN age TINYINT UNSIGNED NOT NULL;
ALTER TABLE users DROP COLUMN phone;
ALTER TABLE users ADD INDEX idx_username_age (username, age);
```

### CRUD 操作

```sql
-- 插入
INSERT INTO users (username, email, password_hash, age)
VALUES ('zhangsan', 'zhangsan@example.com', 'hash123', 25);

INSERT INTO users (username, email, password_hash)
VALUES ('lisi', 'lisi@example.com', 'hash456'),
       ('wangwu', 'wangwu@example.com', 'hash789');

-- 查询
SELECT * FROM users;
SELECT id, username, age FROM users WHERE age > 18 ORDER BY age DESC LIMIT 10;

-- 聚合查询
SELECT age, COUNT(*) as count, AVG(age) as avg_age
FROM users
WHERE created_at > '2024-01-01'
GROUP BY age
HAVING count > 1
ORDER BY count DESC;

-- 更新
UPDATE users SET age = 26 WHERE username = 'zhangsan';

-- 删除
DELETE FROM users WHERE id = 3;

-- JOIN 查询
SELECT u.username, o.order_id, o.amount
FROM users u
INNER JOIN orders o ON u.id = o.user_id
WHERE o.amount > 100;

-- LEFT JOIN
SELECT u.username, COUNT(o.order_id) as order_count
FROM users u
LEFT JOIN orders o ON u.id = o.user_id
GROUP BY u.id;
```

### 索引优化

```sql
-- 查看查询执行计划
EXPLAIN SELECT * FROM users WHERE email = 'test@example.com';

-- 创建索引
CREATE INDEX idx_username ON users(username);
CREATE UNIQUE INDEX idx_email ON users(email);
CREATE FULLTEXT INDEX idx_content ON articles(content);

-- 复合索引（最左前缀原则）
CREATE INDEX idx_city_age ON users(city, age);
-- 生效: WHERE city='BJ' / WHERE city='BJ' AND age>20
-- 不生效: WHERE age>20

-- 查看索引
SHOW INDEX FROM users;

-- 删除索引
DROP INDEX idx_age ON users;

-- 慢查询日志分析
SET GLOBAL slow_query_log = ON;
SET GLOBAL long_query_time = 1;  -- 记录超过1秒的查询
```

### 查询优化技巧

```sql
-- 避免 SELECT *
SELECT id, username FROM users;

-- 使用 LIMIT 分页
SELECT * FROM users ORDER BY id LIMIT 10 OFFSET 20;

-- 优化分页（延迟关联）
SELECT * FROM users
INNER JOIN (SELECT id FROM users ORDER BY id LIMIT 1000, 10) AS tmp
ON users.id = tmp.id;

-- 使用 EXISTS 替代 IN
SELECT * FROM users u
WHERE EXISTS (SELECT 1 FROM orders o WHERE o.user_id = u.id);

-- 避免在 WHERE 中使用函数
-- 低效: WHERE DATE(created_at) = '2024-01-01'
-- 高效: WHERE created_at >= '2024-01-01' AND created_at < '2024-01-02'
```

## PostgreSQL 特色功能

### JSONB 数据类型

```sql
-- 创建 JSONB 列
CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    attributes JSONB
);

-- 插入 JSONB
INSERT INTO products (name, attributes)
VALUES ('笔记本', '{"brand": "联想", "ram": "16GB", "storage": "512GB"}');

-- JSONB 查询
SELECT * FROM products WHERE attributes @> '{"brand": "联想"}';
SELECT name, attributes->>'brand' as brand FROM products;
SELECT name, jsonb_array_elements(attributes->'tags') as tag FROM products;

-- 索引 JSONB
CREATE INDEX idx_products_attrs ON products USING GIN(attributes);
```

### 窗口函数

```sql
-- ROW_NUMBER 排名
SELECT name, salary,
       ROW_NUMBER() OVER (ORDER BY salary DESC) as rank
FROM employees;

-- 分区排名
SELECT department, name, salary,
       RANK() OVER (PARTITION BY department ORDER BY salary DESC) as dept_rank
FROM employees;

-- 移动平均
SELECT date, amount,
       AVG(amount) OVER (ORDER BY date ROWS BETWEEN 6 PRECEDING AND CURRENT ROW) as ma_7
FROM sales;

-- 累计求和
SELECT date, amount,
       SUM(amount) OVER (ORDER BY date) as running_total
FROM sales;
```

### 公共表表达式 (CTE)

```sql
-- 基础 CTE
WITH dept_salary AS (
    SELECT department, AVG(salary) as avg_salary
    FROM employees
    GROUP BY department
)
SELECT e.name, e.department, e.salary
FROM employees e
JOIN dept_salary d ON e.department = d.department
WHERE e.salary > d.avg_salary;

-- 递归 CTE（树形结构）
WITH RECURSIVE org_tree AS (
    -- 根节点
    SELECT id, name, parent_id, 1 as level
    FROM organization
    WHERE parent_id IS NULL
    UNION ALL
    -- 递归子节点
    SELECT o.id, o.name, o.parent_id, t.level + 1
    FROM organization o
    JOIN org_tree t ON o.parent_id = t.id
)
SELECT * FROM org_tree ORDER BY level, id;
```

### PostgreSQL 扩展

```sql
-- 启用扩展
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";
CREATE EXTENSION IF NOT EXISTS "postgis";

-- 使用 UUID
CREATE TABLE sessions (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    user_id INT,
    created_at TIMESTAMP DEFAULT NOW()
);

-- 模糊搜索（pg_trgm）
CREATE INDEX idx_users_name_trgm ON users USING GIN (name gin_trgm_ops);
SELECT * FROM users WHERE name % '张三';  -- 相似度搜索
```

## SQL 客户端对比

| 特性 | DBeaver | Navicat | DataGrip | TablePlus |
|------|---------|---------|----------|-----------|
| 跨平台 | ✅ | ❌ (Win/Mac) | ✅ | ✅ |
| 免费 | ✅ (社区版) | ❌ | ❌ | ❌ (基本版免费) |
| 数据库支持 | 极多 | 多 | 多 | 中 |
| ER 图 | ✅ | ✅ | ✅ | ❌ |
| SSH 隧道 | ✅ | ✅ | ✅ | ✅ |
| 代码补全 | 中 | 良 | 优 | 良 |
| 数据导出 | ✅ | ✅ | ✅ | ✅ |
| 轻量级 | 中 | 重 | 重 | ✅ |

## ORM 对比

### SQLAlchemy (Python)

```python
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True)
    email = Column(String(100))
    created_at = Column(DateTime, default=datetime.utcnow)

engine = create_engine('postgresql://user:pass@localhost/db')
Session = sessionmaker(bind=engine)
session = Session()

# CRUD
user = User(username='zhangsan', email='zhangsan@example.com')
session.add(user)
session.commit()

users = session.query(User).filter(User.username.like('%san%')).all()
```

### Prisma (Node.js/TypeScript)

```prisma
datasource db {
  provider = "postgresql"
  url      = env("DATABASE_URL")
}

model User {
  id        Int      @id @default(autoincrement())
  username  String   @unique
  email     String
  posts     Post[]
  createdAt DateTime @default(now())
}

model Post {
  id        Int      @id @default(autoincrement())
  title     String
  content   String?
  author    User     @relation(fields: [authorId], references: [id])
  authorId  Int
}
```

```typescript
const user = await prisma.user.create({
  data: { username: 'zhangsan', email: 'zhangsan@example.com' }
});

const users = await prisma.user.findMany({
  where: { username: { contains: 'san' } },
  include: { posts: true }
});
```

## 连接池配置

```python
# SQLAlchemy 连接池
engine = create_engine(
    'postgresql://user:pass@localhost/db',
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True,
    pool_recycle=3600
)
```

```yaml
# HikariCP (Java)
spring:
  datasource:
    hikari:
      maximum-pool-size: 20
      minimum-idle: 5
      connection-timeout: 30000
      idle-timeout: 600000
```

## 迁移工具

```bash
# Alembic (Python)
alembic init migrations
alembic revision --autogenerate -m "add users table"
alembic upgrade head

# Prisma Migrate
npx prisma migrate dev --name init
npx prisma migrate deploy

# Flyway (Java)
flyway migrate
flyway info
```

## SQL 格式化与调试

```bash
# sqlfluff - SQL 格式化与 Lint
pip install sqlfluff
sqlfluff lint query.sql
sqlfluff fix query.sql

# pg_stat_statements (PostgreSQL)
SELECT query, calls, total_exec_time, rows
FROM pg_stat_statements
ORDER BY total_exec_time DESC
LIMIT 10;

# MySQL Performance Schema
SELECT * FROM performance_schema.events_statements_summary_by_digest
ORDER BY sum_timer_wait DESC
LIMIT 10;

```

## 相关文件

- [[MySQLDeep]] — MySQL 深入
- [[PostgreSQLDeep]] — PostgreSQL 深入
- [[RedisDeep]] — Redis 深入
- [[MongoDBDeep]] — MongoDB 深入
- [[SQLDeep]] — SQL 深入
- [[Transaction]] — 事务
- [[Optimization]] — 查询优化
- [[05_ComputerScience/DatabasesAndInformationSystems/BigDataTechnologies/INDEX]] — 大数据技术
- [[05_ComputerScience/DatabasesAndInformationSystems/DataWarehousing/INDEX]] — 数据仓库
- [[05_ComputerScience/DatabasesAndInformationSystems/InformationRetrieval/INDEX]] — 信息检索
- [[05_ComputerScience/DatabasesAndInformationSystems/NoSQL/INDEX]] — NoSQL
- [[05_ComputerScience/DatabasesAndInformationSystems/RelationalDatabases/INDEX]] — 关系数据库

