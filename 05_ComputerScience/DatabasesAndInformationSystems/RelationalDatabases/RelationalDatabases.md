---
aliases: [RelationalDatabases]
tags: ['DatabasesAndInformationSystems', 'RelationalDatabases', 'RelationalDatabases']
created: 2026-05-16
updated: 2026-05-13
---

# Relational Databases - 关系数据库

## 一、关系模型

关系模型由 E. F. Codd 于 1970 年提出，是关系数据库的理论基础。

### 基本概念

| 术语 | 说明 | SQL 对应 |
|------|------|---------|
| **Relation（关系）** | 二维表 | Table |
| **Tuple（元组）** | 表中的一行 | Row |
| **Attribute（属性）** | 表中的一列 | Column |
| **Domain（域）** | 属性值的合法取值范围 | Data Type + Constraint |
| **Degree（度）** | 属性的个数 | 列数 |
| **Cardinality（基数）** | 元组的个数 | 行数 |
| **Schema（模式）** | 关系的结构描述 | CREATE TABLE |

### 表结构示例

```
Student Schema: Student(sid: INT, name: VARCHAR, age: INT, major: VARCHAR)

Relation Instance:
┌──────┬──────────┬─────┬──────────┐
│ sid  │  name    │ age │  major   │
├──────┼──────────┼─────┼──────────┤
│ 1001 │ 张三     │ 20  │ CS       │
│ 1002 │ 李四     │ 21  │ Math     │
│ 1003 │ 王五     │ 19  │ CS       │
└──────┴──────────┴─────┴──────────┘
```

---

## 二、键与约束

### 键的类型

| 键类型 | 定义 | 特性 |
|--------|------|------|
| **Superkey（超键）** | 能唯一标识元组的属性集 | 可能包含冗余属性 |
| **Candidate Key（候选键）** | 极小的超键 | 无冗余、唯一 |
| **Primary Key（主键）** | 选定的候选键 | 非空、唯一 |
| **Foreign Key（外键）** | 引用另一表主键的属性 | 维护引用完整性 |
| **Alternate Key（备用键）** | 未被选为主键的候选键 | 唯一非空 |
| **Composite Key（复合键）** | 由多个属性组成的键 | 联合唯一 |

```sql
CREATE TABLE student (
    sid    INT PRIMARY KEY,           -- 主键
    sname  VARCHAR(50) NOT NULL,
    email  VARCHAR(100) UNIQUE,       -- 候选键
    age    INT CHECK (age > 0 AND age < 150)
);

CREATE TABLE enrollment (
    sid    INT,
    cid    INT,
    grade  CHAR(2),
    PRIMARY KEY (sid, cid),          -- 复合主键
    FOREIGN KEY (sid) REFERENCES student(sid)
        ON DELETE CASCADE,
    FOREIGN KEY (cid) REFERENCES course(cid)
);
```

---

## 三、关系代数

关系代数是关系数据库查询语言的形式化基础。

| 操作 | 符号 | 说明 | SQL 对应 |
|------|------|------|---------|
| **选择** | $\sigma_{\text{condition}}(R)$ | 选取满足条件的元组 | WHERE |
| **投影** | $\pi_{A_1, A_2, \dots}(R)$ | 选取指定属性列 | SELECT |
| **自然连接** | $R \bowtie S$ | 相同属性上等值连接 | NATURAL JOIN |
| **笛卡尔积** | $R \times S$ | 所有元组组合 | CROSS JOIN |
| **并** | $R \cup S$ | 不重复合并 | UNION |
| **交** | $R \cap S$ | 公共元组 | INTERSECT |
| **差** | $R - S$ | 在 R 不在 S | EXCEPT |
| **重命名** | $\rho_{new}(R)$ | 重命名关系或属性 | AS |
| **除** | $R \div S$ | 包含 S 中所有值的元组 | — |

### 查询示例

```
查询：选修了所有 CS 课程的学生姓名
SQL: SELECT sname FROM student
     WHERE NOT EXISTS (
         SELECT cid FROM course WHERE dept = 'CS'
         EXCEPT
         SELECT cid FROM enrollment WHERE sid = student.sid
     )

关系代数：
    π_sname(student ⋈ (π_sid(student) − π_sid(
        (π_cid(σ_dept='CS'(course)) × π_sid(student)) − π_sid,cid(enrollment)
    )))
```

---

## 四、SQL 语言

### DDL — 数据定义语言

```sql
CREATE TABLE product (
    id        INT PRIMARY KEY,
    name      VARCHAR(200) NOT NULL,
    price     DECIMAL(10,2) CHECK (price >= 0),
    stock     INT DEFAULT 0,
    category  VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (name, category)
);

ALTER TABLE product ADD COLUMN description TEXT;
ALTER TABLE product DROP COLUMN description;
DROP TABLE product;
CREATE INDEX idx_product_category ON product(category);
```

### DML — 数据操作语言

```sql
-- INSERT
INSERT INTO product (id, name, price, category)
VALUES (1, '笔记本电脑', 5999.00, '电子产品');

-- UPDATE
UPDATE product SET price = price * 0.9 WHERE category = '电子产品';

-- DELETE
DELETE FROM product WHERE stock = 0;

-- SELECT（查询执行顺序）
SELECT p.category, COUNT(*) AS cnt, AVG(p.price) AS avg_price
FROM product p
JOIN orders o ON p.id = o.product_id
WHERE o.order_date >= '2024-01-01'
GROUP BY p.category
HAVING COUNT(*) > 10
ORDER BY avg_price DESC
LIMIT 5;
```

### DCL — 数据控制语言

```sql
CREATE USER 'app_user'@'localhost' IDENTIFIED BY 'password';
GRANT SELECT, INSERT, UPDATE ON mydb.* TO 'app_user'@'localhost';
REVOKE DELETE ON mydb.* FROM 'app_user'@'localhost';
GRANT ALL PRIVILEGES ON mydb.* TO 'admin'@'localhost' WITH GRANT OPTION;
```

---

## 五、完整性约束

| 完整性 | 说明 | SQL 实现 |
|--------|------|---------|
| **实体完整性** | 主键不能为空且唯一 | PRIMARY KEY |
| **参照完整性** | 外键值必须匹配被引用表的主键或为空 | FOREIGN KEY ... REFERENCES ... |
| **域完整性** | 属性值必须在定义域内 | CHECK, NOT NULL, DEFAULT |
| **用户定义完整性** | 业务规则约束 | CHECK, TRIGGER, ASSERTION |

---

## 六、范式与规范化

规范化是通过分解关系来减少数据冗余和更新异常的过程。

### 函数依赖

$$ \alpha \rightarrow \beta \quad (\alpha \text{ 函数决定 } \beta) $$

- **完全函数依赖**：$X \rightarrow Y$，且 $X$ 的任何真子集都不能决定 $Y$
- **部分函数依赖**：$X \rightarrow Y$，且 $X$ 的某个真子集能决定 $Y$
- **传递函数依赖**：$X \rightarrow Y$，$Y \rightarrow Z$，且 $Y \not\rightarrow X$

### 范式层级

```
1NF ──消除重复组──→ 2NF ──消除传递依赖──→ 3NF ──消除主属性对候选键的部分依赖──→ BCNF
```

| 范式 | 条件 | 解决的问题 |
|------|------|-----------|
| **1NF** | 所有属性都是原子值（不可再分） | 非原子值 |
| **2NF** | 满足 1NF，且所有非主属性完全函数依赖于候选键 | 部分依赖（冗余） |
| **3NF** | 满足 2NF，且没有非主属性传递函数依赖于候选键 | 传递依赖 |
| **BCNF** | 满足 3NF，且 $\forall \alpha \rightarrow \beta$，$\alpha$ 是超键或 $\beta \subseteq \alpha$ | 主属性对候选键的部分依赖 |
| **4NF** | 满足 BCNF，且没有非平凡多值依赖 | 多值依赖 |

**BCNF 定义**：对于所有函数依赖 $\alpha \rightarrow \beta$，必须满足：
- $\alpha \rightarrow \beta$ 是平凡依赖（$\beta \subseteq \alpha$），或者
- $\alpha$ 是超键

### Armstrong 公理

| 公理 | 规则 |
|------|------|
| **自反律** | 若 $\beta \subseteq \alpha$，则 $\alpha \rightarrow \beta$ |
| **增补律** | 若 $\alpha \rightarrow \beta$，则 $\alpha\gamma \rightarrow \beta\gamma$ |
| **传递律** | 若 $\alpha \rightarrow \beta$ 且 $\beta \rightarrow \gamma$，则 $\alpha \rightarrow \gamma$ |
| **合并律** | 若 $\alpha \rightarrow \beta$ 且 $\alpha \rightarrow \gamma$，则 $\alpha \rightarrow \beta\gamma$ |
| **分解律** | 若 $\alpha \rightarrow \beta\gamma$，则 $\alpha \rightarrow \beta$ |

---

## 七、查询处理

```
SQL Query ──→ Parser ──→ Rewriter ──→ Optimizer ──→ Executor ──→ Result
                               ↑
                        Catalog Information
```

| 阶段 | 说明 |
|------|------|
| **Parsing** | 语法分析，生成解析树 |
| **Rewriting** | 视图展开、子查询解嵌套 |
| **Optimization** | 生成等价执行计划，选择代价最小的 |
| **Execution** | 执行物理操作符（Table Scan, Index Scan, Hash Join...） |

```sql
-- 示例：优化器可能选择的执行计划

-- 计划 A：Index Scan + Nested Loop Join
-- 1. Index Seek on orders.order_date
-- 2. Index Seek on customer.id = orders.customer_id
-- 3. Nested Loop Join

-- 计划 B：Full Table Scan + Hash Join
-- 1. Table Scan on orders
-- 2. Table Scan on customer
-- 3. Hash Join on customer_id
```

---

## 八、事务与 ACID

### ACID 特性

| 特性 | 说明 | 实现机制 |
|------|------|---------|
| **Atomicity（原子性）** | 事务要么全部执行，要么全部回滚 | Undo Log |
| **Consistency（一致性）** | 事务前后数据库保持一致性状态 | 约束检查 + 应用逻辑 |
| **Isolation（隔离性）** | 并发事务互不干扰 | 锁 / MVCC |
| **Durability（持久性）** | 提交的事务永久生效 | Redo Log |

### 隔离级别

| 级别 | 脏读 | 不可重复读 | 幻读 | 实现 |
|------|------|-----------|------|------|
| **READ UNCOMMITTED** | ✅ 可能 | ✅ 可能 | ✅ 可能 | 无锁 |
| **READ COMMITTED** | ❌ 避免 | ✅ 可能 | ✅ 可能 | 行锁（写）+ MVCC（读） |
| **REPEATABLE READ** | ❌ 避免 | ❌ 避免 | ✅ 可能 | 行锁 + MVCC 快照 |
| **SERIALIZABLE** | ❌ 避免 | ❌ 避免 | ❌ 避免 | 表锁 / 谓词锁 |

---

## 九、并发控制

### 两阶段锁（2PL）

```
事务 T1:
    阶段一（扩展）：LOCK(A), LOCK(B) → 只获取不释放
    阶段二（收缩）：UNLOCK(A), UNLOCK(B) → 只释放不获取

严格 2PL（SS2PL）：在事务提交/回滚前持有所有锁
    → 保证冲突可串行化 + 无级联回滚
```

| 锁类型 | 兼容性 |
|--------|--------|
| **Shared Lock (S)** | 多个事务可同时读 |
| **Exclusive Lock (X)** | 独占，不与其他锁兼容 |
| **Intention Lock** | 表级意向锁，提高检测效率 |

### MVCC（多版本并发控制）

MVCC 通过维护数据的多个版本来实现高并发读写：

```text
事务 T1 写入 row1（版本 1）
事务 T2 读取 row1（看到版本 1）
事务 T3 写入 row1（版本 2）
事务 T2 再次读取 row1（根据隔离级别看到版本 1 或 2）
```

**可见性判断**：根据事务开始时间戳或系统版本号决定可见版本。

---

## 十、恢复机制

### ARIES 恢复算法

ARIES（Algorithm for Recovery and Isolation Exploiting Semantics）三步恢复：

```
1. Analysis Pass：扫描 Log，确定需要回滚的事务和脏页
2. Redo Pass：从找到的 checkpoint 开始重做所有已提交事务
3. Undo Pass：回滚所有未提交事务
```

### WAL（Write-Ahead Logging）

```
事务写入顺序：
    1. 写入 Redo Log（持久化）
    2. 写入数据页（缓冲池）
    3. 事务提交
    4. 在 Undo Log 中记录回滚信息

恢复：
    Redo Log ──→ 重做已提交但未刷盘的操作
    Undo Log ──→ 回滚未提交事务的操作
```

## 相关条目

- SQL
- [[NoSQL]]
- QueryOptimization
- Transactions
- DataModeling

## 参考资源

- Codd, E. F. (1970). A Relational Model of Data for Large Shared Data Banks. CACM.
- Silberschatz, A., Korth, H. F., & Sudarshan, S. (2020). Database System Concepts. 7th Edition. McGraw-Hill.
- Gray, J. & Reuter, A. (1992). Transaction Processing: Concepts and Techniques. Morgan Kaufmann.
- Mohan, C. et al. (1992). ARIES: A Transaction Recovery Method Supporting Fine-Granularity Locking and Partial Rollbacks. ACM TODS.
- PostgreSQL Documentation. https://www.postgresql.org/docs/
