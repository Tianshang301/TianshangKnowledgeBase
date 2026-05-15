# 数据库事务与隔离详解

## 一、事务 ACID 属性

### Atomicity（原子性）

事务中的所有操作要么全部成功，要么全部回滚。InnoDB 通过 UNDO 日志实现原子性。

```sql
START TRANSACTION;
    UPDATE accounts SET balance = balance - 1000 WHERE id = 1;
    UPDATE accounts SET balance = balance + 1000 WHERE id = 2;
COMMIT;  -- 要么同时成功
-- 或
ROLLBACK;  -- 要么同时回滚
```

### Consistency（一致性）

事务执行前后，数据库必须处于一致状态。约束、触发器、级联操作确保数据完整性。

```sql
-- 一致性约束示例
ALTER TABLE orders ADD CONSTRAINT ck_positive_total CHECK (total >= 0);
```

### Isolation（隔离性）

并发执行的事务互不干扰。由锁和 MVCC 机制保证。

### Durability（持久性）

已提交的事务永久保存到数据库。InnoDB 通过 REDO 日志和 doublewrite buffer 保证。

---

## 二、隔离级别

### 四种隔离级别

| 隔离级别 | 脏读 | 不可重复读 | 幻读 | 实现机制 |
|----------|------|-----------|------|----------|
| READ UNCOMMITTED | 可能 | 可能 | 可能 | 不检查版本 |
| READ COMMITTED | 避免 | 可能 | 可能 | 每次查询生成快照 |
| REPEATABLE READ | 避免 | 避免 | InnoDB 避免 | 事务开始时生成快照 |
| SERIALIZABLE | 避免 | 避免 | 避免 | 所有操作加锁 |

### 异常现象

**脏读**：事务 A 读取了事务 B 未提交的数据，事务 B 回滚后 A 读到了不存在的数据。

```sql
-- 会话 A (隔离级别 READ UNCOMMITTED)
SET SESSION TRANSACTION ISOLATION LEVEL READ UNCOMMITTED;
START TRANSACTION;
SELECT balance FROM accounts WHERE id = 1;  -- 读到 1000

-- 会话 B
START TRANSACTION;
UPDATE accounts SET balance = 500 WHERE id = 1;  -- 未提交

-- 会话 A 再次查询，读到 500（脏读！）
SELECT balance FROM accounts WHERE id = 1;  -- 读到 500（实际 B 可能回滚）

-- 会话 B
ROLLBACK;  -- 此时 A 读到的 500 不存在
```

**不可重复读**：同一事务中，两次读取同一行数据得到不同结果（因为其他事务提交了修改）。

```sql
-- 会话 A
SET SESSION TRANSACTION ISOLATION LEVEL READ COMMITTED;
START TRANSACTION;
SELECT balance FROM accounts WHERE id = 1;  -- 读到 1000

-- 会话 B
START TRANSACTION;
UPDATE accounts SET balance = 500 WHERE id = 1;
COMMIT;

-- 会话 A 再次查询，读到 500（不可重复读！）
SELECT balance FROM accounts WHERE id = 1;  -- 读到 500
```

**幻读**：同一事务中，两次范围查询返回不同的行集合（其他事务插入了新行）。

```sql
-- 会话 A
SET SESSION TRANSACTION ISOLATION LEVEL REPEATABLE READ;
START TRANSACTION;
SELECT * FROM accounts WHERE balance > 100;  -- 返回 2 行

-- 会话 B
INSERT INTO accounts (id, balance) VALUES (3, 200);
COMMIT;

-- 会话 A 再次查询（MySQL InnoDB 下不会见到幻行）
SELECT * FROM accounts WHERE balance > 100;  -- 仍返回 2 行（MVCC 保护）
```

---

## 三、MVCC 实现原理

### InnoDB MVCC

InnoDB 中的每行数据包含两个隐藏列：

```
+----+--------+---------+-----------+
| id | name   | DB_TRX_ID | DB_ROLL_PTR |
+----+--------+---------+-----------+
| 1  | Alice  | 100     | pointer   |
+----+--------+---------+-----------+
```

- `DB_TRX_ID`：最近修改此行的事务 ID
- `DB_ROLL_PTR`：指向 UNDO 日志的指针（可找到旧版本）

### ReadView

事务在 REPEATABLE READ 级别开始时创建 ReadView：

| 组件 | 说明 |
|------|------|
| m_ids | 当前活跃的事务 ID 列表 |
| min_trx_id | 活跃事务中最小的事务 ID |
| max_trx_id | 下一个要分配的事务 ID |
| creator_trx_id | 创建此 ReadView 的事务 ID |

### 可见性判断

```
Row's trx_id == creator_trx_id → 可见（自己修改的）
Row's trx_id < min_trx_id     → 可见（已提交的旧事务）
Row's trx_id >= max_trx_id    → 不可见（未来事务修改的）
Row's trx_id IN m_ids        → 不可见（其他活跃事务修改的）
```

### PostgreSQL MVCC

PostgreSQL 使用每个元组中存储的 `xmin` 和 `xmax` 实现 MVCC：

```sql
-- PostgreSQL 元组头信息
xmin: 创建此版本的事务 ID
xmax: 删除/更新此版本的事务 ID
```

```sql
-- 查看元组版本信息
SELECT xmin, xmax, ctid, * FROM accounts;
```

**清理机制**：PostgreSQL 的 VACUUM 进程回收死元组。

---

## 四、锁机制

### 锁分类

| 粒度 | 锁类型 | 说明 |
|------|--------|------|
| 表级 | 意向共享锁 (IS) | 事务计划对某些行加 S 锁 |
| 表级 | 意向排他锁 (IX) | 事务计划对某些行加 X 锁 |
| 行级 | 共享锁 (S) | 允许其他事务读，阻止写 |
| 行级 | 排他锁 (X) | 阻止其他事务读写 |
| 行级 | 记录锁 (Record) | 锁定单条记录 |
| 行级 | 间隙锁 (Gap) | 锁定索引记录之间的间隙 |
| 行级 | Next-Key 锁 | 记录锁 + 间隙锁 |

### 锁兼容性矩阵

```
      IS    IX    S     X
IS    ✅    ✅    ✅    ❌
IX    ✅    ✅    ❌    ❌
S     ✅    ❌    ✅    ❌
X     ❌    ❌    ❌    ❌
```

### 行锁加锁 SQL

```sql
-- 共享锁
SELECT * FROM accounts WHERE id = 1 LOCK IN SHARE MODE;
SELECT * FROM accounts WHERE id = 1 FOR SHARE;  -- MySQL 8.0

-- 排他锁
SELECT * FROM accounts WHERE id = 1 FOR UPDATE;
SELECT * FROM accounts WHERE id = 1 FOR UPDATE NOWAIT;  -- 不等待，立即报错
SELECT * FROM accounts WHERE id = 1 FOR UPDATE SKIP LOCKED;  -- 跳过已锁定的行

-- 主动加表锁
LOCK TABLES accounts READ;    -- 读锁
LOCK TABLES accounts WRITE;   -- 写锁
UNLOCK TABLES;
```

### Next-Key 锁示例 (InnoDB RR 级别)

```sql
-- 假设 accounts 表在 balance 列有索引，数据行 balance 为 [10, 20, 30, 40]

-- 事务 A
START TRANSACTION;
SELECT * FROM accounts WHERE balance BETWEEN 15 AND 35 FOR UPDATE;
-- 锁定的间隙：
--   (-∞, 10) ← 间隙锁（影响到插入 balance=5）
--   (10, 20)  ← 间隙锁（影响到插入 balance=15）
--   [20]      ← 记录锁（balance=20）
--   (20, 30)  ← 间隙锁（影响到插入 balance=25）
--   [30]      ← 记录锁（balance=30）
--   (30, 40)  ← 间隙锁（影响到插入 balance=35）
--   (40, +∞)  ← 间隙锁（影响到插入 balance=50）

-- 事务 B（被阻塞）
INSERT INTO accounts (id, balance) VALUES (5, 15);  -- 被间隙锁阻塞
INSERT INTO accounts (id, balance) VALUES (6, 25);  -- 被间隙锁阻塞
```

---

## 五、死锁

### 死锁检测

InnoDB 自动检测死锁，选择一个事务回滚（选择 UNDO 量较少的那个）。

```sql
-- 死锁示例
-- 事务 A
START TRANSACTION;
UPDATE accounts SET balance = balance - 100 WHERE id = 1;  -- 锁住 id=1
-- 事务 B 此时更新 id=2
UPDATE accounts SET balance = balance - 100 WHERE id = 2;  -- 锁住 id=2
-- 事务 A 尝试锁 id=2（被 B 持有）→ 等待
UPDATE accounts SET balance = balance + 100 WHERE id = 2;  -- 等待
-- 事务 B 尝试锁 id=1（被 A 持有）→ 死锁！

-- InnoDB 检测到死锁，回滚其中一个事务
SHOW ENGINE INNODB STATUS\G  -- 查看最近死锁信息
```

### 死锁避免策略

```sql
-- 策略一：固定访问顺序
-- 事务 A 和 B 都按 id 升序更新
START TRANSACTION;
UPDATE accounts SET balance = balance - 100 WHERE id = 1;
UPDATE accounts SET balance = balance + 100 WHERE id = 2;  -- 总是先 1 后 2
COMMIT;

-- 策略二：减少锁范围
SELECT * FROM accounts WHERE id = 1 FOR UPDATE NOWAIT;  -- 不等待

-- 策略三：降低隔离级别
SET SESSION TRANSACTION ISOLATION LEVEL READ COMMITTED;

-- 策略四：设置锁等待超时
SET innodb_lock_wait_timeout = 5;  -- 5 秒超时
```

---

## 六、分布式事务

### 2PC (两阶段提交)

```
协调者             参与者1             参与者2
    │                   │                  │
    ├──── Prepare ──────▶                   │
    ├──── Prepare ──────────────────────────▶
    │◀───── Ready ──────┤                   │
    │◀─────────────────── Ready ────────────┤
    ├──── Commit ───────▶                   │
    ├──── Commit ───────────────────────────▶
    │◀───── Done ───────┤                   │
    │◀─────────────────── Done ─────────────┤
    │                                       │
```

**优点**：实现简单，强一致性
**缺点**：同步阻塞，协调者单点故障

### 3PC (三阶段提交)

在 2PC 基础上增加 CanCommit 阶段和超时机制：

1. **CanCommit**：检查各参与者是否可提交
2. **PreCommit**：执行事务（但未提交）
3. **DoCommit**：最终提交

### Saga 模式

将长事务拆分为多个本地事务，每个本地事务有对应的补偿操作：

```text
Saga: T1 → T2 → T3 → T4
补偿: C1 ← C2 ← C3 ← C4
```

**编排模式（Choreography）**：每个服务发布事件，其他服务监听并执行。

**协调模式（Orchestration）**：一个协调者告诉各个服务该做什么。

### TCC (Try-Confirm-Cancel)

| 阶段 | 操作 | 说明 |
|------|------|------|
| Try | 预留资源 | 冻结库存、冻结资金 |
| Confirm | 确认执行 | 扣减库存、扣除资金 |
| Cancel | 取消回滚 | 释放预留资源 |

```java
// TCC 示例：账户转账
public class AccountTccService {

    @Try
    public void tryTransfer(Long accountId, BigDecimal amount) {
        BigDecimal frozen = accountService.freezeBalance(accountId, amount);
        // 状态记录到事务表：状态 = TRY
    }

    @Confirm
    public void confirmTransfer(Long accountId, BigDecimal amount) {
        accountService.deductFrozen(accountId, amount);
        // 状态更新为 CONFIRM
    }

    @Cancel
    public void cancelTransfer(Long accountId, BigDecimal amount) {
        accountService.unfreezeBalance(accountId, amount);
        // 状态更新为 CANCEL
    }
}
```

### Seata 框架

Seata 是阿里巴巴开源的分布式事务解决方案：

| 模式 | 特点 |
|------|------|
| AT（自动） | 类似 TCC，自动生成反向 SQL |
| TCC | 手工编写 Try/Confirm/Cancel |
| Saga | 适合长事务 |
| XA | 基于数据库 XA 协议 |

### BASE 理论

| 缩写 | 全称 | 说明 |
|------|------|------|
| BA | Basically Available | 基本可用（允许部分功能降级）|
| S | Soft State | 软状态（允许中间状态）|
| E | Eventually Consistent | 最终一致 |

```sql
-- 最终一致性实现示例：本地消息表

-- 1. 在本地事务中同时写入业务数据和消息
START TRANSACTION;
    UPDATE accounts SET balance = balance - 1000 WHERE id = 1;
    INSERT INTO transaction_outbox (user_id, amount, target_account, status, created_at)
    VALUES (1, 1000, 2, 'PENDING', NOW());
COMMIT;

-- 2. 定时任务轮询发送
SELECT * FROM transaction_outbox WHERE status = 'PENDING' ORDER BY created_at LIMIT 10;
-- 发送到 MQ 或其他账号系统
-- 收到确认后更新状态
UPDATE transaction_outbox SET status = 'SENT' WHERE id = ?;

-- 3. 幂等处理（接收方）
INSERT INTO received_events (event_id, processed_at)
VALUES (?, NOW())
    ON CONFLICT (event_id) DO NOTHING;  -- 重复消息不做处理
```

## 相关条目

- [[查询优化与事务管理]]
- [[RelationalDatabases]]
- [[Optimization]]
- [[MySQLDeep]]
- [[PostgreSQLDeep]]
