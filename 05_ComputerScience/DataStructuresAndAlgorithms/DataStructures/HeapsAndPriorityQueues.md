---
aliases: [HeapsAndPriorityQueues]
tags: ['05_ComputerScience', 'DataStructuresAndAlgorithms', 'DataStructures']
---

# 堆与优先队列

## 概述

堆是一种特殊的完全二叉树，满足堆性质：最大堆中父节点值 ≥ 子节点值，最小堆中父节点值 ≤ 子节点值。优先队列基于堆实现。

## 操作复杂度

| 操作 | 时间复杂度 |
|------|-----------|
| 插入 | O(log n) |
| 删除最值 | O(log n) |
| 查看最值 | O(1) |
| 建堆 | O(n) |
| 堆排序 | O(n log n) |

## 应用场景

- 任务调度、Dijkstra 最短路径、Huffman 编码
- Top K 问题、中位数查找、合并 K 个有序链表

## 相关条目
- [[Heap]]
- [[Tree]]
- [[Queue]]
- [[SegmentTree]]
- [[INDEX|DataStructures 索引]]
