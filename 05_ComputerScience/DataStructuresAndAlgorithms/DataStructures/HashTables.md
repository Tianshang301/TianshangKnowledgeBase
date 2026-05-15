---
aliases: [HashTables]
tags: ['05_ComputerScience', 'DataStructuresAndAlgorithms', 'DataStructures']
---

# 哈希表

## 概述

哈希表（HashTable）通过哈希函数将键映射到数组位置，实现平均 O(1) 的插入、删除和查找操作。

## 核心概念

- **哈希函数**: 将任意大小的键映射到固定范围的索引
- **冲突解决**: 链地址法（Separate Chaining）、开放寻址法（Open Addressing）
- **负载因子**: 元素数量 / 桶数量，决定是否需要扩容
- **一致性哈希**: 分布式系统中的哈希方案

## 相关条目
- [[HashTable]]
- [[Array]]
- [[LinkedList]]
- [[Trie]]
- [[INDEX|DataStructures 索引]]
