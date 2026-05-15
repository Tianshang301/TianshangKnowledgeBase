---
aliases: [LinkedLists]
tags: ['05_ComputerScience', 'DataStructuresAndAlgorithms', 'DataStructures']
---

# 链表

## 概述

链表由一系列节点组成，每个节点包含数据和指向下一个节点的指针。链表支持高效的插入和删除操作。

## 类型

| 类型 | 特点 |
|------|------|
| 单向链表 | 每个节点只有 next 指针 |
| 双向链表 | 每个节点有 prev 和 next 指针 |
| 循环链表 | 尾节点指向头节点 |
| 双向循环链表 | 头尾相连的双向链表 |

## 操作复杂度

| 操作 | 单向链表 | 双向链表 |
|------|---------|---------|
| 头部插入 | O(1) | O(1) |
| 尾部插入 | O(n) | O(1) |
| 查找 | O(n) | O(n) |
| 删除已知节点 | O(1)（在首部） | O(1) |

## 相关条目
- [[LinkedList]]
- [[Array]]
- [[Stack]]
- [[Queue]]
- [[HashTable]]
