---
aliases: [Concurrency]
tags: ['OperatingSystems', 'Concurrency', 'Concurrency']
created: 2026-05-16
updated: 2026-05-16
---

# 并发详解 (Concurrency)

## 一、进程与线程 (Processes vs Threads)

| 特性 | 进程 (Process) | 线程 (Thread) |
|------|---------------|--------------|
| 地址空间 | 独立地址空间 | 共享进程地址空间 |
| 资源开销 | 大（独立 PCB、内存、文件） | 小（共享堆、代码、文件） |
| 通信方式 | IPC（管道、消息队列等） | 直接读写共享内存 |
| 切换开销 | 大（页表切换、TLB 刷新） | 小（仅保存寄存器） |
| 独立性 | 一个进程崩溃不影响其他 | 一个线程崩溃可能导致进程崩溃 |
| 创建速度 | 慢 | 快（轻量级） |

每个进程至少包含一个线程，线程是 CPU 调度的基本单位。

## 二、并发与并行 (Concurrency vs Parallelism)

- **并发 (Concurrency)**: 多个任务在同一时间段内交替执行（单核也可实现）
- **并行 (Parallelism)**: 多个任务在同一时刻同时执行（需要多核）

```
并发（单核）：   ┌─A─┐ ┌─B─┐ ┌─A─┐ ┌─B─┐
并行（多核）：   ┌─A──────────────────┐
                ┌─B──────────────────┐
```

并发关注程序结构，并行关注执行效率。

## 三、竞态条件 (Race Condition)

多个线程同时访问共享数据且至少一个是写操作，结果取决于执行顺序。

```c
// 竞态条件示例：counter++
int counter = 0;

// 等价于三条指令：
// LOAD  counter, R1
// ADD   R1, 1
// STORE R1, counter

// 线程 A 和 B 同时执行时可能：
// A: LOAD counter(0) → A: ADD(1) → B: LOAD counter(0) → A: STORE(1) → B: ADD(1) → B: STORE(1)
// 结果：counter = 1  （丢失一次递增！）
```

## 四、临界区问题 (Critical Section Problem)

临界区是访问共享资源的代码段，需满足三个要求：

| 要求 | 描述 |
|------|------|
| **互斥 (Mutual Exclusion)** | 同一时刻最多一个进程在临界区 |
| **前进 (Progress)** | 无进程在临界区时，只有不待在剩余区的进程可参与选择 |
| **有限等待 (Bounded Waiting)** | 每个进程在发出请求后有限时间内进入临界区 |

### 软件解决方案：Peterson 算法

```c
// Peterson 算法（适用于两个进程）
int flag[2] = {0, 0};
int turn = 0;

// 进程 i (另一个为 j = 1 - i)
void enter_critical_section(int i) {
    int j = 1 - i;
    flag[i] = 1;       // 表示想进入
    turn = j;          // 让给对方
    while (flag[j] && turn == j)
        ;              // 忙等待
}

void leave_critical_section(int i) {
    flag[i] = 0;       // 表示退出
}
```

## 五、锁 (Locks)

### 5.1 互斥锁 (Mutex)

```c
#include <pthread.h>

pthread_mutex_t mutex = PTHREAD_MUTEX_INITIALIZER;

void *thread_func(void *arg) {
    pthread_mutex_lock(&mutex);
    // 临界区
    pthread_mutex_unlock(&mutex);
    return NULL;
}
```

### 5.2 自旋锁 (Spinlock)

忙等待的锁，适合短临界区。不会让出 CPU。

```c
// 自旋锁实现（基于 TAS 指令）
void spin_lock(volatile int *lock) {
    while (__sync_lock_test_and_set(lock, 1))
        ;  // 忙等待
}

void spin_unlock(volatile int *lock) {
    __sync_lock_release(lock);
}
```

### 5.3 读写锁 (Read-Write Lock)

| 场景 | 并发度 |
|------|--------|
| 多读一写 | 读可并发，写互斥 |
| 读多写少 | 性能优于互斥锁 |

```c
pthread_rwlock_t rwlock = PTHREAD_RWLOCK_INITIALIZER;

void reader() {
    pthread_rwlock_rdlock(&rwlock);
    // 读操作（可多个读者同时进入）
    pthread_rwlock_unlock(&rwlock);
}

void writer() {
    pthread_rwlock_wrlock(&rwlock);
    // 写操作（独占）
    pthread_rwlock_unlock(&rwlock);
}
```

### 锁对比

| 类型 | 等待方式 | 适用场景 | 开销 |
|------|---------|---------|------|
| Mutex | 睡眠（上下文切换） | 临界区长 | 中 |
| Spinlock | 忙等待（循环） | 临界区极短 | 小 |
| RW Lock | 读共享/写互斥 | 读多写少 | 中 |

## 六、信号量 (Semaphore)

信号量是一个整型变量 $S$，仅通过两个原子操作访问：

### 基本操作

```
wait(S):   while (S <= 0) ;  S--
signal(S): S++
```

**信号量不变量**：$S \geq 0$ 始终成立且 $S = S_0 + \text{signal} - \text{wait}$，其中 $\text{signal}$ 和 $\text{wait}$ 是已完成的信号量操作次数。

### 计数信号量 vs 二进制信号量

| 类型 | 取值范围 | 用途 |
|------|---------|------|
| **计数信号量** | 任意非负整数 | 管理多个同类型资源 |
| **二进制信号量** | 0 或 1 | 互斥锁、同步 |

### 用信号量解决同步问题

```c
// 生产者-消费者（有界缓冲区）
sem_t empty, full, mutex;
// empty = N（缓冲区容量）
// full = 0
// mutex = 1

void *producer(void *arg) {
    while (1) {
        // 生产数据
        sem_wait(&empty);    // 有空位？
        sem_wait(&mutex);    // 互斥访问缓冲区
        // 放入缓冲区
        sem_post(&mutex);
        sem_post(&full);     // 增加已满项数
    }
}

void *consumer(void *arg) {
    while (1) {
        sem_wait(&full);     // 有数据？
        sem_wait(&mutex);    // 互斥访问缓冲区
        // 取出数据
        sem_post(&mutex);
        sem_post(&empty);    // 增加空位
        // 消费数据
    }
}
```

## 七、管程 (Monitor)

管程是高级同步抽象，将共享变量和操作封装在一起，保证同一时刻只有一个进程在管程内活动。

### 条件变量 (Condition Variable)

```c
pthread_mutex_t mutex = PTHREAD_MUTEX_INITIALIZER;
pthread_cond_t cond = PTHREAD_COND_INITIALIZER;

void *waiter(void *arg) {
    pthread_mutex_lock(&mutex);
    while (!condition)
        pthread_cond_wait(&cond, &mutex);  // 等待并释放锁
    // 条件满足，继续执行
    pthread_mutex_unlock(&mutex);
}

void *signaler(void *arg) {
    pthread_mutex_lock(&mutex);
    condition = 1;
    pthread_cond_signal(&cond);  // 唤醒等待线程
    pthread_mutex_unlock(&mutex);
}
```

### Hoare vs Mesa 语义

| 特性 | Hoare | Mesa |
|------|-------|------|
| signal 后谁执行 | 被唤醒进程立即执行 | signaler 继续执行 |
| 被唤醒进程 | 获得 CPU 和锁 | 重新竞争锁 |
| 实现复杂度 | 高（需特殊调度） | 低（更常用） |
| 需重新检查条件 | 否 | 是（while 循环） |

## 八、死锁 (Deadlock)

### 4个必要条件

| 条件 | 符号 | 描述 |
|------|------|------|
| **互斥 (Mutual Exclusion)** | $C_1$ | 资源一次只能被一个进程使用 |
| **持有并等待 (Hold and Wait)** | $C_2$ | 进程持有资源并等待其他资源 |
| **不可剥夺 (No Preemption)** | $C_3$ | 资源不能被强制剥夺 |
| **循环等待 (Circular Wait)** | $C_4$ | 存在进程-资源循环链 |

死锁发生当且仅当四个条件同时成立：$\text{Deadlock} \iff C_1 \land C_2 \land C_3 \land C_4$

### 死锁预防

破坏四个条件之一：

| 策略 | 方法 | 代价 |
|------|------|------|
| 破坏互斥 | 使用共享资源（读） | 不适用于写 |
| 破坏持有并等待 | 一次性申请所有资源 | 资源利用率低 |
| 破坏不可剥夺 | 申请失败时释放已持有资源 | 实现复杂 |
| 破坏循环等待 | 资源按序分配 | 需确定全局顺序 |

### 死锁避免：银行家算法 (Banker's Algorithm)

$$ \text{Available} = \text{资源总量} - \sum_{i} \text{Allocation}_i $$
$$ \text{Need}_i = \text{Max}_i - \text{Allocation}_i $$
$$ \text{安全状态} \iff \exists \text{序列 } \langle P_1, P_2, \dots, P_n \rangle \text{ 满足 } \forall i,\; \text{Need}_i \leq \text{Available} + \sum_{j < i} \text{Allocation}_j $$

```
Available: 可用资源向量
Max:       每个进程最大需求
Allocation:已分配资源
Need:      剩余需求 = Max - Allocation

安全性检查：
1. Work = Available
2. 找 Need[i] <= Work 且未完成的进程
3. 若找到: Work += Allocation[i], 标记完成, 回到2
4. 若所有进程完成 → 安全状态
```

### 死锁检测与恢复

```
检测：
等待图 (Wait-for Graph) 中有环 → 死锁

恢复方法：
1. 终止所有死锁进程
2. 逐个终止直到环消失
3. 剥夺资源
4. 回滚到安全状态
```

## 九、经典同步问题

### 9.1 哲学家就餐问题

```c
// 每位哲学家：思考 → 拿左叉 → 拿右叉 → 吃 → 放叉 → 思考
sem_t chopstick[5];  // 每根叉子是信号量

void philosopher(int i) {
    while (1) {
        think();
        sem_wait(&chopstick[i]);           // 拿左
        sem_wait(&chopstick[(i+1) % 5]);   // 拿右
        eat();
        sem_post(&chopstick[i]);           // 放左
        sem_post(&chopstick[(i+1) % 5]);   // 放右
    }
}
// 问题：所有哲学家同时拿左叉 → 死锁
// 解法：奇数号先左后右，偶数号先右后左；或最多4人同时吃
```

### 9.2 读者-写者问题

| 方案 | 读者优先级 | 写者优先级 |
|------|-----------|-----------|
| 第一读者-写者 | 读者优先（写者可能饥饿） | 低 |
| 第二读者-写者 | 写者优先（读者可能饥饿） | 高 |

```c
// 读者优先实现
sem_t rw_mutex = 1;  // 读写互斥
sem_t mutex = 1;     // 保护 read_count
int read_count = 0;

void reader() {
    sem_wait(&mutex);
    read_count++;
    if (read_count == 1)
        sem_wait(&rw_mutex);  // 第一个读者锁住写者
    sem_post(&mutex);
    
    // 读操作
    
    sem_wait(&mutex);
    read_count--;
    if (read_count == 0)
        sem_post(&rw_mutex);  // 最后一个读者释放
    sem_post(&mutex);
}

void writer() {
    sem_wait(&rw_mutex);
    // 写操作
    sem_post(&rw_mutex);
}
```

## 十、无锁编程 (Lock-Free Programming)

### CAS (Compare-And-Swap)

```c
int compare_and_swap(int *ptr, int expected, int new_val) {
    int actual = *ptr;
    if (actual == expected)
        *ptr = new_val;
    return actual;  // 返回旧值
}

// 无锁计数器
void atomic_increment(int *counter) {
    int old;
    do {
        old = *counter;
    } while (CAS(counter, old, old + 1) != old);
}
```

### 原子操作

| 操作 | 描述 |
|------|------|
| `atomic_read` | 原子读 |
| `atomic_set` | 原子写 |
| `atomic_add` | 原子加 |
| `atomic_sub` | 原子减 |
| `atomic_xchg` | 原子交换 |
| `atomic_cmpxchg` | CAS |

### ABA 问题

CAS 的陷阱：值从 A 变为 B 又变回 A，CAS 误认为未改变。

解法：使用带版本号的指针（如 `atomic_ref` 或双字 CAS）。

## 十一、内存模型 (Memory Model)

### 顺序一致性 (Sequential Consistency)

所有线程的执行结果如同按某种顺序交错执行，且每个线程内指令顺序不变。

```
线程1: store X=1, load Y
线程2: store Y=1, load X

顺序一致性下，(X=1, Y=1), (X=1, Y=0), (X=0, Y=1) 都合法
(X=0, Y=0) 不可能
```

### Happens-Before 关系

若操作 A happens-before 操作 B，则 A 的结果对 B 可见。

| 规则 | 说明 |
|------|------|
| 程序顺序 | 同一线程内，前面的操作 happens-before 后面的 |
| 监视器锁 | 解锁 happens-before 后续加锁 |
| volatile | 对 volatile 变量的写 happens-before 后续读 |
| 传递性 | A happens-before B, B happens-before C → A happens-before C |

### 内存栅栏 (Memory Barrier)

```c
// 防止编译器/CPU 重排序
asm volatile("mfence" ::: "memory");  // x86 全屏障
asm volatile("lfence" ::: "memory");  // 读屏障
asm volatile("sfence" ::: "memory");  // 写屏障
```

## 十二、Amdahl 定律

系统加速比受限于不能并行化的部分：

$$S = \frac{1}{(1-p) + p/n}$$

| $p$（并行比例） | $n$（处理器数） | 加速比 $S$ |
|:--------------:|:---------------:|:----------:|
| 0.5 | 2 | 1.33 |
| 0.5 | 16 | 1.88 |
| 0.9 | 2 | 1.82 |
| 0.9 | 16 | 6.40 |
| 0.99 | 16 | 13.9 |
| 0.99 | 1024 | 91.7 |

即使并行比例达到99%，理论最大加速比也仅为100。

## 相关条目

- [[05_ComputerScience/OperatingSystems/ProcessManagement/ProcessManagement|ProcessManagement]]
- Synchronization
- Deadlock
- [[05_ComputerScience/HardwareAndEmbeddedSystems/RTOS/RTOS|RTOS]]

## 参考资源

- Silberschatz, A., Galvin, P. B., & Gagne, G. *Operating System Concepts* (10th ed.)
- Herlihy, M., & Shavit, N. *The Art of Multiprocessor Programming*
- Tanenbaum, A. S., & Bos, H. *Modern Operating Systems* (4th ed.)
- Intel 64 and IA-32 Architectures Software Developer's Manual


