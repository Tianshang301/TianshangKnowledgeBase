---
aliases:
  - 内存一致性与排序
  - Memory Consistency and Ordering
  - 内存模型
  - Memory Model
  - 缓存一致性
tags:
  - computer-architecture
  - memory-consistency
  - memory-ordering
  - cache-coherence
  - concurrency
  - lock-free
created: 2026-06-27
updated: 2026-06-27
---

# 内存一致性与排序

## 1. 基本概念

### 1.1 一致性 vs 排序

```
Memory Coherence (缓存一致性) vs Memory Consistency (内存一致性):

┌─────────────────────────────────────────────────────────┐
│  缓存一致性 (Cache Coherence):                          │
│  ┌───────────────────────────────────────────────────┐  │
│  │  问题: 多个处理器缓存同一内存位置时              │  │
│  │        如何保证所有处理器看到一致的值?            │  │
│  │                                                   │  │
│  │  定义: 对于单个内存位置 X                         │  │
│  │  - 所有处理器对 X 的写操作最终对所有处理器可见   │  │
│  │  - 对 X 的读操作返回最近的写入值                 │  │
│  │  - 写操作是串行化的 (所有处理器看到相同顺序)     │  │
│  │                                                   │  │
│  │  协议: MESI, MOESI, MOESIF, MESIF                │  │
│  └───────────────────────────────────────────────────┘  │
│                                                         │
│  内存一致性 (Memory Consistency):                       │
│  ┌───────────────────────────────────────────────────┐  │
│  │  问题: 多个内存位置的读写操作顺序如何?           │  │
│  │        处理器看到的操作顺序是否一致?              │  │
│  │                                                   │  │
│  │  定义: 对于多个内存位置 X, Y, Z...               │  │
│  │  - 不同处理器看到的读写顺序是否相同?             │  │
│  │  - 允许哪些重排序?                               │  │
│  │  - 需要什么屏障来强制顺序?                       │  │
│  │                                                   │  │
│  │  模型: SC, TSO, PSO, Relaxed (ARM, POWER)        │  │
│  └───────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘

类比:
  一致性 = "所有人看到同一份报纸的相同内容"
  一致性 = "报纸的出版顺序是否所有人都能看到"
```

### 1.2 操作重排序

```
处理器和编译器可能重排序操作:

┌─────────────────────────────────────────────────────────┐
│  重排序类型:                                            │
│                                                         │
│  1. 编译器重排序:                                       │
│     源代码:     a = 1; b = 2;                           │
│     编译后:     b = 2; a = 1;  ← 编译器优化           │
│                                                         │
│  2. 处理器乱序执行:                                     │
│     程序顺序:   LOAD a; ADD b; STORE c                 │
│     执行顺序:   LOAD a; STORE c; ADD b                 │
│                                                         │
│  3. Store Buffer 重排序:                                │
│     处理器写入 Store Buffer, 稍后写入缓存              │
│     其他处理器可能看到旧值                             │
│                                                         │
│  4. 缓存延迟:                                           │
│     写操作需要时间传播到其他处理器                     │
│                                                         │
│  允许的重排序 (x86 TSO):                               │
│  ┌───────────────────────────────────────────────────┐  │
│  │  ✓ Load-Load:     不允许重排序 (保序)            │  │
│  │  ✓ Load-Store:    不允许重排序 (保序)            │  │
│  │  ✓ Store-Load:    允许重排序! ← TSO唯一放松     │  │
│  │  ✓ Store-Store:   不允许重排序 (保序)            │  │
│  └───────────────────────────────────────────────────┘  │
│                                                         │
│  ARM/POWER (更宽松):                                   │
│  ┌───────────────────────────────────────────────────┐  │
│  │  ✓ Load-Load:     可能重排序 (需要屏障)          │  │
│  │  ✓ Load-Store:    可能重排序 (需要屏障)          │  │
│  │  ✓ Store-Load:    可能重排序 (需要屏障)          │  │
│  │  ✓ Store-Store:   可能重排序 (需要屏障)          │  │
│  └───────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
```

## 2. Sequential Consistency (SC)

### 2.1 Lamport 定义

```
Sequential Consistency (顺序一致性):

┌─────────────────────────────────────────────────────────┐
│  Lamport (1979) 定义:                                   │
│  "A multiprocessor is sequentially consistent if        │
│   the result of any execution is the same as if         │
│   the operations of all the processors were executed    │
│   in some sequential order, and the operations of       │
│   each individual processor appear in this sequence     │
│   in the order specified by its program."               │
│                                                         │
│  两个条件:                                              │
│  1. 所有处理器的操作存在一个全局顺序                   │
│  2. 每个处理器的程序顺序在这个全局顺序中保持           │
│                                                         │
│  示例:                                                  │
│  ┌───────────────────────────────────────────────────┐  │
│  │  P0: a = 1; if (b == 0) ...                      │  │
│  │  P1: b = 1; if (a == 0) ...                      │  │
│  │                                                   │  │
│  │  SC 保证: 不可能同时看到 a=0 和 b=0              │  │
│  │  因为: 全局顺序必须是 a=1 → b=1 或 b=1 → a=1   │  │
│  └───────────────────────────────────────────────────┘  │
│                                                         │
│  SC 实现:                                               │
│  ┌───────────────────────────────────────────────────┐  │
│  │  - 所有操作按程序顺序执行                         │  │
│  │  - 写操作立即对所有处理器可见                     │  │
│  │  - 禁止所有重排序                                │  │
│  │                                                   │  │
│  │  性能代价: 极高!                                 │  │
│  │  - 无法使用 Store Buffer                         │  │
│  │  - 无法乱序执行                                  │  │
│  │  - 无法写缓冲                                    │  │
│  └───────────────────────────────────────────────────┘  │
│                                                         │
│  SC 性能问题:                                           │
│  延迟 = L1访问 + 总线仲裁 + 所有缓存同步              │
│  每次写操作都需要等待所有处理器确认                    │
│  实际系统不使用纯 SC!                                  │
└─────────────────────────────────────────────────────────┘
```

## 3. Total Store Order (TSO)

### 3.1 x86 TSO 模型

```
x86 TSO (Total Store Order) 模型:

┌─────────────────────────────────────────────────────────┐
│  TSO 是 x86 架构的内存一致性模型                       │
│  比 SC 宽松, 允许一种重排序                            │
│                                                         │
│  允许的重排序:                                          │
│  ┌───────────────────────────────────────────────────┐  │
│  │  Store-Load 重排序:                               │  │
│  │                                                   │  │
│  │  P0: store X = 1     ← 写入 Store Buffer        │  │
│  │      load Y          ← 读取 Y (可能读到旧值)    │  │
│  │                                                   │  │
│  │  P1: store Y = 1     ← 写入 Store Buffer        │  │
│  │      load X          ← 读取 X (可能读到旧值)    │  │
│  │                                                   │  │
│  │  结果: 可能 X=0, Y=0! (Store Buffer 导致)       │  │
│  └───────────────────────────────────────────────────┘  │
│                                                         │
│  Store Buffer 导致的重排序:                            │
│  ┌───────────────────────────────────────────────────┐  │
│  │                                                   │  │
│  │  ┌─────┐    ┌──────────────┐    ┌──────────┐    │  │
│  │  │ CPU │───►│ Store Buffer │───►│  Cache   │    │  │
│  │  └─────┘    └──────────────┘    └──────────┘    │  │
│  │                  │                               │  │
│  │  写操作先进入 SB, 稍后才写入 Cache              │  │
│  │  但 load 可能从 Cache 读取 (旧值)              │  │
│  │                                                   │  │
│  │  解决: Store Buffer Forwarding                  │  │
│  │  - load 检查 SB 是否有对应地址                 │  │
│  │  - 如果有, 直接从 SB 读取 (新值)              │  │
│  │  - 但其他处理器的 load 无法看到!              │  │
│  └───────────────────────────────────────────────────┘  │
│                                                         │
│  TSO 保证:                                              │
│  ┌───────────────────────────────────────────────────┐  │
│  │  ✓ Load-Load 保序: load 不能越过前面的 load     │  │
│  │  ✓ Load-Store 保序: load 不能越过前面的 store   │  │
│  │  ✓ Store-Store 保序: store 不能越过前面的 store │  │
│  │  ✗ Store-Load 可重排序: store 可能延迟对其他   │  │
│  │    处理器可见 (通过 Store Buffer)               │  │
│  └───────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
```

### 3.2 x86 MFENCE

```
x86 内存屏障指令:

┌─────────────────────────────────────────────────────────┐
│  MFENCE (Memory Fence):                                 │
│  ┌───────────────────────────────────────────────────┐  │
│  │  - 完全内存屏障                                   │  │
│  │  - 阻止所有重排序                                │  │
│  │  - 等待所有挂起的内存操作完成                    │  │
│  │  - 包括 Store Buffer 排空                       │  │
│  └───────────────────────────────────────────────────┘  │
│                                                         │
│  LFENCE (Load Fence):                                   │
│  ┌───────────────────────────────────────────────────┐  │
│  │  - 加载屏障 (x86 实际上是序列化指令)            │  │
│  │  - 阻止 load-load 重排序                        │  │
│  │  - 也用于 Spectre 缓解 (序列化流水线)           │  │
│  └───────────────────────────────────────────────────┘  │
│                                                         │
│  SFENCE (Store Fence):                                  │
│  ┌───────────────────────────────────────────────────┐  │
│  │  - 存储屏障                                      │  │
│  │  - 阻止 store-store 重排序                      │  │
│  │  - 排空 Store Buffer                            │  │
│  └───────────────────────────────────────────────────┘  │
│                                                         │
│  使用示例:                                              │
│  ┌───────────────────────────────────────────────────┐  │
│  │  // 确保写入对其他处理器立即可见                 │  │
│  │  mov [flag], 1       // 设置标志                 │  │
│  │  mfence              // 完全屏障                 │  │
│  │  mov eax, [data]     // 读取数据                 │  │
│  │                                                   │  │
│  │  // 等价于 acquire-release 语义                  │  │
│  │  mov [flag], 1       // release                  │  │
│  │  // (x86 store 自带 release 语义)               │  │
│  │  mov eax, [flag]     // acquire                  │  │
│  │  // (x86 load 自带 acquire 语义)                │  │
│  └───────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
```

## 4. Partial Store Order (PSO)

### 4.1 SPARC PSO 模型

```
SPARC PSO (Partial Store Order):

┌─────────────────────────────────────────────────────────┐
│  PSO 比 TSO 更宽松:                                    │
│  允许 Store-Store 重排序!                              │
│                                                         │
│  允许的重排序:                                          │
│  ┌───────────────────────────────────────────────────┐  │
│  │  Store-Load:  允许 (同 TSO)                      │  │
│  │  Store-Store: 允许! ← PSO特有                    │  │
│  │  Load-Load:   不允许 (保序)                      │  │
│  │  Load-Store:  不允许 (保序)                      │  │
│  └───────────────────────────────────────────────────┘  │
│                                                         │
│  Store-Store 重排序示例:                               │
│  ┌───────────────────────────────────────────────────┐  │
│  │  P0:                     P1:                      │  │
│  │  data = 42;              while (flag == 0);      │  │
│  │  flag = 1;               print(data);            │  │
│  │                                                   │  │
│  │  PSO: P1 可能打印 0!                            │  │
│  │  因为 flag=1 可能在 data=42 之前可见            │  │
│  └───────────────────────────────────────────────────┘  │
│                                                         │
│  解决: STBAR 指令 (Store Barrier)                      │
│  ┌───────────────────────────────────────────────────┐  │
│  │  data = 42;                                       │  │
│  │  stbar;              // 强制 store-store 保序    │  │
│  │  flag = 1;                                       │  │
│  └───────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
```

## 5. Relaxed Memory Models

### 5.1 ARM/POWER 宽松模型

```
ARM 和 POWER 的宽松内存模型:

┌─────────────────────────────────────────────────────────┐
│  特点: 允许几乎所有类型的重排序                        │
│                                                         │
│  允许的重排序:                                          │
│  ┌───────────────────────────────────────────────────┐  │
│  │  Load-Load:   允许重排序                         │  │
│  │  Load-Store:  允许重排序                         │  │
│  │  Store-Load:  允许重排序                         │  │
│  │  Store-Store: 允许重排序                         │  │
│  └───────────────────────────────────────────────────┘  │
│                                                         │
│  仅保证:                                                │
│  ┌───────────────────────────────────────────────────┐  │
│  │  - 数据依赖保序: 如果 B 依赖 A 的结果           │  │
│  │    则 A 一定在 B 之前执行                        │  │
│  │  - 单处理器内的因果关系保序                     │  │
│  └───────────────────────────────────────────────────┘  │
│                                                         │
│  ARM 示例问题:                                          │
│  ┌───────────────────────────────────────────────────┐  │
│  │  P0:                 P1:                          │  │
│  │  STR X1, [X0]       LDR X2, [X0]                │  │
│  │  STR X3, [X4]       LDR X5, [X4]                │  │
│  │                                                   │  │
│  │  ARM 允许: X2=新值, X5=旧值!                    │  │
│  │  (Load-Load 重排序)                              │  │
│  └───────────────────────────────────────────────────┘  │
│                                                         │
│  为什么需要这么宽松?                                   │
│  ┌───────────────────────────────────────────────────┐  │
│  │  1. 性能: 允许更多优化                           │  │
│  │     - 乱序执行                                   │  │
│  │     - 写合并 (Write Combining)                   │  │
│  │     - Store Buffer 优化                          │  │
│  │                                                   │  │
│  │  2. 功耗: 减少不必要的同步                       │  │
│  │     - 仅在需要时使用屏障                         │  │
│  │     - 移动设备特别重要                           │  │
│  │                                                   │  │
│  │  3. 可扩展性: 适合大规模多核                     │  │
│  │     - 减少一致性流量                             │  │
│  └───────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
```

### 5.2 ARM 内存屏障

```
ARM 内存屏障指令:

┌─────────────────────────────────────────────────────────┐
│  DMB (Data Memory Barrier):                             │
│  ┌───────────────────────────────────────────────────┐  │
│  │  - 数据内存屏障                                  │  │
│  │  - 保证屏障前的内存访问在屏障后的访问之前完成    │  │
│  │  - 不影响指令执行顺序                            │  │
│  │                                                   │  │
│  │  DMB SY   ; 系统级全屏障                         │  │
│  │  DMB ISH  ; 内部共享域 (同一CPU集群)            │  │
│  │  DMB ISHST; 内部共享域, 仅store                 │  │
│  │  DMB ISHLD; 内部共享域, 仅load                  │  │
│  └───────────────────────────────────────────────────┘  │
│                                                         │
│  DSB (Data Synchronization Barrier):                    │
│  ┌───────────────────────────────────────────────────┐  │
│  │  - 数据同步屏障                                  │  │
│  │  - 比 DMB 更强: 等待所有内存访问完成            │  │
│  │  - 包括缓存维护操作                              │  │
│  │  - 后续指令等待 DSB 完成                        │  │
│  └───────────────────────────────────────────────────┘  │
│                                                         │
│  ISB (Instruction Synchronization Barrier):             │
│  ┌───────────────────────────────────────────────────┐  │
│  │  - 指令同步屏障                                  │  │
│  │  - 刷新流水线                                    │  │
│  │  - 确保后续指令从缓存/内存重新获取              │  │
│  │  - 用于修改代码后或页表修改后                   │  │
│  └───────────────────────────────────────────────────┘  │
│                                                         │
│  使用示例 (消息传递):                                   │
│  ┌───────────────────────────────────────────────────┐  │
│  │  // P0: 生产者                                    │  │
│  │  STR X1, [data]      // 写入数据                 │  │
│  │  DMB ISH             // 数据屏障                 │  │
│  │  MOV X2, #1                                     │  │
│  │  STR X2, [flag]      // 设置标志                 │  │
│  │                                                   │  │
│  │  // P1: 消费者                                    │  │
│  │  LDR X3, [flag]      // 读取标志                 │  │
│  │  CMP X3, #1                                     │  │
│  │  B.ne wait                                      │  │
│  │  DMB ISH             // 数据屏障                 │  │
│  │  LDR X4, [data]      // 读取数据                 │  │
│  │  // 保证看到 X1 的值!                           │  │
│  └───────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
```

## 6. C++ 内存模型

### 6.1 C++11 Memory Order

```
C++11 原子操作内存顺序:

┌─────────────────────────────────────────────────────────┐
│  std::memory_order 枚举:                                │
│                                                         │
│  1. memory_order_relaxed:                               │
│  ┌───────────────────────────────────────────────────┐  │
│  │  - 最宽松: 仅保证原子性                          │  │
│  │  - 不保证顺序                                    │  │
│  │  - 适合: 计数器, 统计数据                        │  │
│  └───────────────────────────────────────────────────┘  │
│                                                         │
│  2. memory_order_acquire:                               │
│  ┌───────────────────────────────────────────────────┐  │
│  │  - 获取语义: load-acquire                        │  │
│  │  - 后续读写不能重排序到此操作之前               │  │
│  │  - 对应: x86 load (自动), ARM LDAR              │  │
│  └───────────────────────────────────────────────────┘  │
│                                                         │
│  3. memory_order_release:                               │
│  ┌───────────────────────────────────────────────────┐  │
│  │  - 释放语义: store-release                       │  │
│  │  - 前面的读写不能重排序到此操作之后             │  │
│  │  - 对应: x86 store (自动), ARM STLR             │  │
│  └───────────────────────────────────────────────────┘  │
│                                                         │
│  4. memory_order_acq_rel:                               │
│  ┌───────────────────────────────────────────────────┐  │
│  │  - 获取-释放语义: 同时具有 acquire 和 release   │  │
│  │  - 适合: 读-改-写操作 (CAS)                     │  │
│  └───────────────────────────────────────────────────┘  │
│                                                         │
│  5. memory_order_seq_cst:                               │
│  ┌───────────────────────────────────────────────────┐  │
│  │  - 顺序一致性 (默认)                            │  │
│  │  - 最强保证: 全局顺序一致                       │  │
│  │  - 性能最差                                      │  │
│  └───────────────────────────────────────────────────┘  │
│                                                         │
│  6. memory_order_consume:                               │
│  ┌───────────────────────────────────────────────────┐  │
│  │  - 消费语义: 依赖保序                            │  │
│  │  - 仅保证数据依赖的操作保序                     │  │
│  │  - 比 acquire 弱, 但更高效                      │  │
│  │  - 目前编译器大多实现为 acquire                 │  │
│  └───────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
```

### 6.2 Acquire-Release 编程

```cpp
// Acquire-Release 语义示例

#include <atomic>
#include <thread>

std::atomic<int> data{0};
std::atomic<bool> ready{false};

// 生产者线程
void producer() {
    data.store(42, std::memory_order_relaxed);
    // release 语义: 保证 data 的写入在 ready 之前可见
    ready.store(true, std::memory_order_release);
}

// 消费者线程
void consumer() {
    // acquire 语义: 保证 ready 之后的读取能看到 data 的值
    while (!ready.load(std::memory_order_acquire)) {
        // 自旋等待
    }
    // 保证看到 data == 42
    assert(data.load(std::memory_order_relaxed) == 42);
}

// 实现一个简单的自旋锁
class SpinLock {
    std::atomic_flag flag = ATOMIC_FLAG_INIT;
public:
    void lock() {
        // test-and-set with acquire
        while (flag.test_and_set(std::memory_order_acquire)) {
            // 自旋
        }
    }

    void unlock() {
        // clear with release
        flag.clear(std::memory_order_release);
    }
};

// 使用示例
SpinLock mutex;
int shared_data = 0;

void increment() {
    std::lock_guard<SpinLock> lock(mutex);
    shared_data++;
}

// 双重检查锁定 (Double-Checked Locking)
class Singleton {
    static std::atomic<Singleton*> instance;
    static std::mutex mtx;

public:
    static Singleton* get_instance() {
        Singleton* tmp = instance.load(std::memory_order_acquire);
        if (tmp == nullptr) {
            std::lock_guard<std::mutex> lock(mtx);
            tmp = instance.load(std::memory_order_relaxed);
            if (tmp == nullptr) {
                tmp = new Singleton();
                instance.store(tmp, std::memory_order_release);
            }
        }
        return tmp;
    }
};
```

## 7. 无锁数据结构

### 7.1 CAS 操作

```
Compare-And-Swap (CAS) 原子操作:

┌─────────────────────────────────────────────────────────┐
│  CAS 伪代码:                                            │
│  ┌───────────────────────────────────────────────────┐  │
│  │  bool CAS(addr, expected, desired) {              │  │
│  │      atomic {                                     │  │
│  │          if (*addr == expected) {                 │  │
│  │              *addr = desired;                     │  │
│  │              return true;                         │  │
│  │          }                                        │  │
│  │          return false;                            │  │
│  │      }                                            │  │
│  │  }                                                │  │
│  └───────────────────────────────────────────────────┘  │
│                                                         │
│  x86 实现 (CMPXCHG):                                   │
│  ┌───────────────────────────────────────────────────┐  │
│  │  ; 原子比较交换                                   │  │
│  │  lock cmpxchg [mem], new_val                      │  │
│  │  ; EAX = 期望值                                   │  │
│  │  ; 如果 [mem] == EAX:                             │  │
│  │  ;     [mem] = new_val, ZF=1                     │  │
│  │  ; 否则:                                          │  │
│  │  ;     EAX = [mem], ZF=0                         │  │
│  └───────────────────────────────────────────────────┘  │
│                                                         │
│  ARM 实现 (LL/SC):                                      │  │
│  ┌───────────────────────────────────────────────────┐  │
│  │  // Load-Linked / Store-Conditional               │  │
│  │  retry:                                           │  │
│  │      ldxr x0, [addr]     // Load-Linked          │  │
│  │      cmp x0, expected                           │  │
│  │      b.ne fail                                   │  │
│  │      stxr w1, desired, [addr] // Store-Cond      │  │
│  │      cbnz w1, retry     // 如果失败, 重试        │  │
│  │  fail:                                            │  │
│  │      // CAS 失败                                 │  │
│  └───────────────────────────────────────────────────┘  │
│                                                         │
│  CAS 循环模式:                                          │
│  ┌───────────────────────────────────────────────────┐  │
│  │  do {                                             │  │
│  │      old_val = *addr;                             │  │
│  │      new_val = compute(old_val);                 │  │
│  │  } while (!CAS(addr, old_val, new_val));         │  │
│  │                                                   │  │
│  │  // 适用于: 原子累加, 原子更新等                 │  │
│  └───────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
```

### 7.2 ABA 问题

```
ABA 问题:

┌─────────────────────────────────────────────────────────┐
│  问题描述:                                              │
│  ┌───────────────────────────────────────────────────┐  │
│  │  初始状态: addr → A → B → C                      │  │
│  │                                                   │  │
│  │  线程1: 读取 A, 计划将 A 替换为 D               │  │
│  │          被抢占...                               │  │
│  │                                                   │  │
│  │  线程2: 删除 A, 删除 B, 分配新节点 E            │  │
│  │          再次分配新节点 (地址恰好是 A!)          │  │
│  │          addr → A → E → C                        │  │
│  │                                                   │  │
│  │  线程1: 恢复执行, CAS(addr, A, D)               │  │
│  │          成功! 但链表已被破坏                    │  │
│  │          addr → D → B → C (B已被删除!)          │  │
│  └───────────────────────────────────────────────────┘  │
│                                                         │
│  解决方案:                                              │
│  ┌───────────────────────────────────────────────────┐  │
│  │  1. 使用带版本号的指针 (Tagged Pointer)          │  │
│  │     struct TaggedPtr {                            │  │
│  │         Node* ptr;                                │  │
│  │         uint64_t version;  // 单调递增           │  │
│  │     };                                            │  │
│  │     CAS: 同时比较 ptr 和 version                │  │
│  │                                                   │  │
│  │  2. 使用 Hazard Pointers                         │  │
│  │     - 每个线程维护"危险指针"列表                │  │
│  │     - 删除前检查是否被其他线程引用              │  │
│  │                                                   │  │
│  │  3. 使用 RCU (Read-Copy-Update)                  │  │
│  │     - 读取时无锁                                 │  │
│  │     - 更新时复制修改                             │  │
│  │     - 延迟回收旧版本                             │  │
│  └───────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
```

### 7.3 无锁栈

```cpp
// 无锁栈 (Lock-Free Stack) 实现

#include <atomic>
#include <memory>

template<typename T>
class LockFreeStack {
    struct Node {
        T data;
        Node* next;
        Node(const T& val) : data(val), next(nullptr) {}
    };

    std::atomic<Node*> head{nullptr};

public:
    void push(const T& val) {
        Node* new_node = new Node(val);
        Node* old_head = head.load(std::memory_order_relaxed);

        do {
            new_node->next = old_head;
        } while (!head.compare_exchange_weak(
            old_head,
            new_node,
            std::memory_order_release,
            std::memory_order_relaxed
        ));
    }

    bool pop(T& result) {
        Node* old_head = head.load(std::memory_order_acquire);

        do {
            if (old_head == nullptr)
                return false;
        } while (!head.compare_exchange_weak(
            old_head,
            old_head->next,
            std::memory_order_acquire,
            std::memory_order_relaxed
        ));

        result = old_head->data;
        // 注意: 这里存在 ABA 问题!
        // 延迟删除 old_head 可以解决
        delete old_head;
        return true;
    }
};

// 带版本号的无锁栈 (解决 ABA 问题)
template<typename T>
class TaggedLockFreeStack {
    struct Node {
        T data;
        Node* next;
    };

    struct TaggedPtr {
        Node* ptr;
        uint64_t tag;  // 版本号
    };

    std::atomic<TaggedPtr> head;

public:
    void push(const T& val) {
        Node* new_node = new Node{val, nullptr};
        TaggedPtr old_head = head.load(std::memory_order_relaxed);

        do {
            new_node->next = old_head.ptr;
            TaggedPtr new_head = {new_node, old_head.tag + 1};
        } while (!head.compare_exchange_weak(
            old_head,
            new_head,
            std::memory_order_release,
            std::memory_order_relaxed
        ));
    }

    bool pop(T& result) {
        TaggedPtr old_head = head.load(std::memory_order_acquire);

        do {
            if (old_head.ptr == nullptr)
                return false;
            TaggedPtr new_head = {old_head.ptr->next, old_head.tag + 1};
        } while (!head.compare_exchange_weak(
            old_head,
            new_head,
            std::memory_order_acquire,
            std::memory_order_relaxed
        ));

        result = old_head.ptr->data;
        delete old_head.ptr;
        return true;
    }
};
```

## 8. 实践应用

### 8.1 消息传递模式

```cpp
// 生产者-消费者消息传递

#include <atomic>
#include <array>

template<typename T, size_t Size>
class LockFreeQueue {
    std::array<T, Size> buffer;
    std::atomic<size_t> write_idx{0};
    std::atomic<size_t> read_idx{0};

public:
    bool push(const T& val) {
        size_t current_write = write_idx.load(std::memory_order_relaxed);
        size_t next_write = (current_write + 1) % Size;

        // 检查是否满
        if (next_write == read_idx.load(std::memory_order_acquire))
            return false;

        buffer[current_write] = val;

        // release 语义: 保证数据写入在索引更新之前可见
        write_idx.store(next_write, std::memory_order_release);
        return true;
    }

    bool pop(T& val) {
        size_t current_read = read_idx.load(std::memory_order_relaxed);

        // 检查是否空
        if (current_read == write_idx.load(std::memory_order_acquire))
            return false;

        val = buffer[current_read];

        // release 语义: 保证读取完成在索引更新之前
        read_idx.store((current_read + 1) % Size, std::memory_order_release);
        return true;
    }
};

// 使用示例
LockFreeQueue<int, 1024> queue;

void producer_thread() {
    for (int i = 0; i < 1000000; i++) {
        while (!queue.push(i)) {
            // 队列满, 等待
        }
    }
}

void consumer_thread() {
    int val;
    int count = 0;
    while (count < 1000000) {
        if (queue.pop(val)) {
            // 处理 val
            count++;
        }
    }
}
```

### 8.2 性能对比

```
内存序性能对比 (x86-64, 1000万次操作):

┌─────────────────────────────────────────────────────────┐
│  操作                    │ 相对耗时 │ 备注             │
├─────────────────────────┼──────────┼──────────────────┤
│  memory_order_relaxed    │ 1.0x     │ 最快             │
│  memory_order_acquire    │ 1.0x     │ x86 自动保序     │
│  memory_order_release    │ 1.0x     │ x86 自动保序     │
│  memory_order_acq_rel    │ 1.0x     │ x86 自动保序     │
│  memory_order_seq_cst    │ 1.2-1.5x │ 需要 MFENCE      │
├─────────────────────────┼──────────┼──────────────────┤
│  std::mutex (lock/unlock)│ 20-50x   │ 需要系统调用     │
│  std::atomic_flag (spin) │ 1.5x     │ 自旋锁           │
└─────────────────────────┴──────────┴──────────────────┘

x86 vs ARM 性能差异:
┌─────────────────────────────────────────────────────────┐
│  在 x86 上:                                             │
│  - acquire/release 与 relaxed 性能几乎相同              │
│  - 因为 x86 TSO 已经保证了大部分顺序                   │
│  - 仅 seq_cst 需要额外 MFENCE                          │
│                                                         │
│  在 ARM 上:                                             │
│  - acquire/release 比 relaxed 慢 20-50%                │
│  - 因为 ARM 需要额外的 LDAR/STLR 指令                 │
│  - seq_cst 更慢 (需要 DMB)                             │
│                                                         │
│  建议:                                                  │
│  - 优先使用 acquire/release (足够安全且高效)           │
│  - 仅在必要时使用 seq_cst                              │
│  - 计数器/统计可用 relaxed                             │
│  - 关键同步点用 acquire/release                        │
└─────────────────────────────────────────────────────────┘
```
