---
aliases:
  - Go运行时
  - Go Runtime
  - GMP调度模型
tags:
  - Go/Runtime
  - Go/GC
  - Go/Goroutine
created: 2026-06-28
updated: 2026-06-28
---

# Go运行时

Go运行时（runtime）是Go程序执行的基础层，负责goroutine调度、内存分配和垃圾回收等核心功能。理解运行时机制对于编写高性能Go程序至关重要。

## GMP调度模型详解

### 核心组件

- **G（Goroutine）**：Go协程，轻量级用户态线程
  - 初始栈大小仅2KB（可动态增长）
  - 包含栈、程序计数器、状态、关联的M等信息
  - 状态：_Gidle → _Grunnable → _Grunning → _Gwaiting → _Gdead

- **M（Machine）**：操作系统线程
  - 最多10000个（默认，可通过runtime/debug.SetMaxThreads调整）
  - 实际运行goroutine的执行单元
  - 通过系统调用与内核交互

- **P（Processor）**：逻辑处理器
  - 数量默认等于CPU核心数（GOMAXPROCS）
  - 持有本地运行队列和mcache（内存缓存）
  - 是G和M之间的桥梁

### 调度流程

1. **获取G**：M先从P的本地队列获取G，若为空则从全局队列获取
2. **偷取机制（Work Stealing）**：本地和全局队列都为空时，从其他P的队列偷取一半的G
3. **执行G**：M绑定G并执行
4. **阻塞处理**：
   - 系统调用阻塞：M与P解绑，P找新的M继续执行其他G
   - 网络I/O阻塞：G被挂起，M继续执行其他G（netpoller异步通知）
   - channel/mutex阻塞：G被放入等待队列，M继续执行其他G

### 调度器调度点

- 函数调用时检查栈空间和抢占标志
- 系统调用进入和退出时
- channel操作、mutex操作、time.Sleep等主动让出
- GC STW（Stop The World）阶段

### 抢占调度

Go 1.14引入基于信号的异步抢占：

- **协作式抢占**：函数调用时检查抢占标志（preempt）
- **异步抢占**：向M发送SIGURG信号，强制中断正在执行的goroutine
- 解决了没有函数调用的死循环goroutine无法被抢占的问题
- 抢占是为了让GC的STW阶段能及时停止所有goroutine

### sysmon监控线程

独立运行的监控线程，不绑定P：

- 检测长时间运行的goroutine并发起抢占
- 回收长时间未使用的syscall阻塞的P
- 触发GC
- 网络轮询（netpoll）

## 内存分配器

Go的内存分配器基于TCMalloc（Thread-Caching Malloc）的变体设计。

### 多级缓存结构

```
mcache (per-P) → mcentral (per-sizeclass) → mheap (全局)
```

- **mcache**：每个P的本地缓存，分配小对象无需加锁
- **mcentral**：按大小分类的全局缓存，需要加锁
- **mheap**：全局堆管理器，管理大块内存

### 对象大小分类

- **Tiny对象**：< 16字节，多个对象共享一个16字节块
- **Small对象**：16B - 32KB，按size class分配（67个等级）
- **Large对象**：> 32KB，直接从mheap分配

### span管理

内存以page（8KB）为单位，多个page组成span：

- **mspan**：连续的page组成的内存块
- 每个span有特定的size class和元素数量
- 使用bitmap标记span中每个slot的使用状态
- 空闲span通过链表和树结构管理

### 分配流程

1. 根据对象大小确定size class
2. 从mcache获取对应size class的span
3. 从span中找到空闲slot分配
4. mcache中没有可用span时，从mcentral获取
5. mcentral也没有时，从mheap申请新的span
6. 大对象直接从mheap分配

### 内存归还

- GC标记后，未使用的span被归还给mheap
- 长时间未使用的内存通过madvise归还给操作系统
- Go 1.12+使用更积极的归还策略（scavenging）

## 垃圾回收器

Go使用并发三色标记清除垃圾回收器，目标是低延迟。

### 三色标记法

- **白色**：未被扫描的对象，GC结束后白色对象被回收
- **灰色**：已被扫描但其引用的对象尚未扫描
- **黑色**：已被扫描且其引用的对象也已扫描

标记过程：
1. 从根对象（goroutine栈、全局变量等）开始，标记为灰色
2. 从灰色集合取出对象，扫描其引用，将引用标记为灰色，自身标记为黑色
3. 重复直到灰色集合为空
4. 所有白色对象为垃圾

### 写屏障（Write Barrier）

并发GC需要写屏障保证正确性：

- **插入写屏障**：在指针赋值时，将新指向的对象标灰
- **删除写屏障**：在指针赋值时，将旧指向的对象标灰
- **混合写屏障**（Go 1.8+）：结合两者，避免栈重新扫描

混合写屏障规则：
- 指针赋值时，将旧值和新值都标灰（如果在堆上）
- 栈上新分配的对象直接标黑

### GC阶段

1. **STW Mark Setup**：开启写屏障，初始化标记任务（极短，通常<1ms）
2. **Concurrent Mark**：与用户goroutine并发执行标记
3. **STW Mark Termination**：关闭写屏障，完成剩余标记（极短）
4. **Concurrent Sweep**：并发清除白色对象

### GC触发条件

- 堆大小增长到GOGC阈值（默认100%，即堆翻倍时触发）
- 超过2分钟未GC则强制触发
- 手动调用runtime.GC()

### GOGC调优

- **GOGC=100**（默认）：堆增长100%时触发GC
- **GOGC=200**：更少的GC频率，更大的内存占用
- **GOGC=off**：禁用GC（仅适用于短生命周期程序）
- **GOMEMLIMIT**（Go 1.19+）：设置软内存上限，自动调整GC频率

## 栈管理

### 分段栈（Segmented Stacks，Go < 1.3）

- 每个goroutine的栈由多个不连续的栈段组成
- 栈空间不足时分配新的栈段，链接到旧栈
- 问题："hot split"——在栈边界反复增长/缩小导致性能抖动

### 连续栈（Contiguous Stacks，Go >= 1.3）

- goroutine使用连续的内存块作为栈
- 栈空间不足时：
  1. 分配一个2倍大小的新栈
  2. 将旧栈内容完整复制到新栈
  3. 调整所有指向旧栈的指针
  4. 释放旧栈
- 初始大小2KB，最大可增长到1GB
- 栈缩小：GC时检测栈使用率，过低则缩栈

### 栈增长检查

- 函数序言（prologue）中检查栈空间是否充足
- 编译器在每个函数入口插入检查代码
- 栈空间不足时调用runtime.morestack
- 检查是协作式的，与抢占调度配合

### 栈大小演变

- 初始栈：2KB（Go 1.4+）
- 最大栈：1GB（可配置）
- 增长策略：不够时翻倍
- 缩小策略：使用率不足1/4时缩半
