---
aliases: [RelationalDatabases]
tags: ['05_ComputerScience', 'DatabasesAndInformationSystems']
---

# 关系数据库

关系数据库（Relational Database）是建立在关系模型（Relational Model）基础上的数据库系统，由 E. F. Codd 于 1970 年提出。关系模型的核心是将数据组织为二维表（关系），通过元组（行）和属性（列）来存储数据，并使用集合论与一阶谓词逻辑作为理论基础。Codd 提出了著名的 **12 条规则**来定义关系数据库系统的完整性标准。SQL（Structured Query Language）是操作关系数据库的标准语言，分为 DDL（数据定义语言）、DML（数据操纵语言）和 DCL（数据控制语言）三大子集。

关系数据库通过 **范式理论**（Normalization）来减少数据冗余和避免更新异常，从 1NF 到 5NF 及 BCNF 逐级递进。事务管理保证了数据库操作的 **ACID** 特性（原子性、一致性、隔离性、持久性），通过锁机制和 MVCC（多版本并发控制）实现并发控制。索引是提升查询性能的核心手段，B+ 树索引适用于范围查询，哈希索引适用于等值查询。查询优化器负责将 SQL 语句转化为高效的执行计划，涉及代价估算、连接算法选择、索引利用等优化策略。

## 相关条目

- [[SQL]] 
- [[ACID]] 
- [[Index]] 
- [[QueryOptimization]] 
- [[NoSQL]]