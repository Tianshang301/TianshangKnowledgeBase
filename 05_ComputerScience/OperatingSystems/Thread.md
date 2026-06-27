---
aliases: [Thread]
tags: ['OperatingSystems', 'Thread']
created: 2026-05-16
updated: 2026-05-13
---

# 线程与并发 (Threads and Concurrency)

## 1. 线程概念 (Thread Concept)

线程是 CPU 调度的基本单位，是进程内的一个执行流。同一进程内的线程共享：

- 地址空间
- 全局变量
- 文件描述符
- 信号处理

### 线程独有资源

| 资源 | 说明 |
|------|------|
| Thread ID | 线程标识符 |
| Program Counter | 指令指针 |
| Register Set | CPU 寄存器 |
| Stack | 函数调用栈 |
| errno | 错误码 |
| Signal Mask | 信号掩码 |

```
┌───────────────────────────┐
│        进程 (Process)       │
│  ┌─────┬─────┬─────┐      │
│  │ T1  │ T2  │ T3  │      │
│  │Stack│Stack│Stack│      │
│  ├─────┴─────┴─────┤      │
│  │   Code + Data   │      │
│  │   Heap          │      │
│  │   Files         │      │
│  └─────────────────┘      │
└───────────────────────────┘
```

## 2. 线程 vs 进程

| 比较维度 | 进程 | 线程 |
|---------|------|------|
| 创建开销 | 大(复制地址空间) | 小(共享地址空间) |
| 上下文切换 | 慢(TLB 刷新) | 快(共享页表) |
| 通信方式 | IPC(管道/队列等) | 直接读写共享内存 |
| 同步需求 | 较少 | 多(需要加锁) |
| 独立性 | 高(独立地址空间) | 低(一个崩溃全进程挂) |
| 资源占用 | 多 | 少 |
| 安全性 | 高(隔离) | 低(共享) |
| 适用场景 | 独立任务 | 并行计算/I/O 密集型 |

## 3. 线程模型

### 3.1 用户级线程 (Many-to-One)

```
┌────────────────────┐
│    用户空间         │
│  ┌──┬──┬──┬──┐     │
│  │T1│T2│T3│T4│     │
│  └──┴──┴──┴──┘     │
│    线程库           │
├────────────────────┤
│    内核空间         │
│  ┌──────────────┐  │
│  │  单 KLT        │  │
│  └──────────────┘  │
└────────────────────┘
```

**优点:** 切换快(不涉及内核)、可移植
**缺点:** 一个线程阻塞则全部阻塞、不能利用多核

### 3.2 内核级线程 (One-to-One)

```
┌────────────────────┐
│    用户空间         │
│  ┌──┬──┬──┬──┐     │
│  │T1│T2│T3│T4│     │
│  └──┴──┴──┴──┘     │
├────────────────────┤
│    内核空间         │
│  ┌──┬──┬──┬──┐     │
│  │K1│K2│K3│K4│     │
│  └──┴──┴──┴──┘     │
└────────────────────┘
```

**优点:** 多核并行、一个阻塞不影响其他
**缺点:** 切换开销大(系统调用)、线程数限制

### 3.3 混合模型 (Many-to-Many)

```
┌────────────────────┐
│    用户空间         │
│  ┌──┬──┬──┬──┐     │
│  │T1│T2│T3│T4│     │
│  └──┴──┴──┴──┘     │
├────────────────────┤
│    内核空间         │
│  ┌──┬──┬──┬──┐     │
│  │K1│K2│K3│K4│     │
│  └──┴──┴──┴──┘     │
└────────────────────┘
       ↕ ↕
    CPU0 CPU1
```

**Solaris / IRIX 实现此模型**

## 4. POSIX 线程 (pthreads)

### 基本操作

```c
#include <pthread.h>
#include <stdio.h>

void* thread_func(void* arg) {
    int id = *(int*)arg;
    printf("线程 %d 运行中\n", id);
    return (void*)(long)(id * 2);
}

int main() {
    pthread_t threads[4];
    int args[4];

    // 创建线程
    for (int i = 0; i < 4; i++) {
        args[i] = i;
        pthread_create(&threads[i], NULL, thread_func, &args[i]);
    }

    // 等待线程结束
    void* ret;
    for (int i = 0; i < 4; i++) {
        pthread_join(threads[i], &ret);
        printf("线程 %d 返回值: %ld\n", i, (long)ret);
    }
    return 0;
}
```

编译: `gcc -pthread thread.c -o thread`

### 互斥锁 (Mutex)

```c
pthread_mutex_t mutex = PTHREAD_MUTEX_INITIALIZER;
int shared_counter = 0;

void* increment(void* arg) {
    for (int i = 0; i < 1000000; i++) {
        pthread_mutex_lock(&mutex);
        shared_counter++;
        pthread_mutex_unlock(&mutex);
    }
    return NULL;
}

int main() {
    pthread_t t1, t2;
    pthread_create(&t1, NULL, increment, NULL);
    pthread_create(&t2, NULL, increment, NULL);
    pthread_join(t1, NULL);
    pthread_join(t2, NULL);
    printf("最终值: %d (期望: 2000000)\n", shared_counter);
    pthread_mutex_destroy(&mutex);
    return 0;
}
```

### 条件变量 (Condition Variable)

```c
pthread_mutex_t mutex = PTHREAD_MUTEX_INITIALIZER;
pthread_cond_t cond = PTHREAD_COND_INITIALIZER;
int ready = 0;

void* producer(void* arg) {
    sleep(1);
    pthread_mutex_lock(&mutex);
    ready = 1;
    printf("生产者: 数据就绪\n");
    pthread_cond_signal(&cond);  // 唤醒一个等待线程
    pthread_mutex_unlock(&mutex);
    return NULL;
}

void* consumer(void* arg) {
    pthread_mutex_lock(&mutex);
    while (!ready) {
        printf("消费者: 等待数据...\n");
        pthread_cond_wait(&cond, &mutex);  // 自动释放锁, 被唤醒后重新加锁
    }
    printf("消费者: 收到数据\n");
    pthread_mutex_unlock(&mutex);
    return NULL;
}

int main() {
    pthread_t t1, t2;
    pthread_create(&t1, NULL, consumer, NULL);
    pthread_create(&t2, NULL, producer, NULL);
    pthread_join(t1, NULL);
    pthread_join(t2, NULL);
    return 0;
}
```

### 读写锁 (RWLock)

```c
pthread_rwlock_t rwlock = PTHREAD_RWLOCK_INITIALIZER;

void* reader(void* arg) {
    pthread_rwlock_rdlock(&rwlock);  // 多个读者可同时读
    printf("读者 %d: 读取数据\n", *(int*)arg);
    pthread_rwlock_unlock(&rwlock);
    return NULL;
}

void* writer(void* arg) {
    pthread_rwlock_wrlock(&rwlock);  // 写者独占
    printf("写者: 写入数据\n");
    pthread_rwlock_unlock(&rwlock);
    return NULL;
}
```

## 5. Windows 线程

```c
#include <windows.h>
#include <stdio.h>

DWORD WINAPI thread_func(LPVOID param) {
    int id = (int)(LONG_PTR)param;
    printf("Windows 线程 %d 运行中\n", id);
    return id * 2;
}

int main() {
    HANDLE threads[4];
    for (int i = 0; i < 4; i++) {
        threads[i] = CreateThread(
            NULL,               // 安全属性
            0,                  // 栈大小(0=默认)
            thread_func,        // 线程函数
            (LPVOID)(LONG_PTR)i, // 参数
            0,                  // 创建标志
            NULL                // 线程 ID
        );
    }

    // 等待所有线程
    WaitForMultipleObjects(4, threads, TRUE, INFINITE);

    // 获取退出码
    DWORD exit_code;
    GetExitCodeThread(threads[0], &exit_code);
    printf("线程0退出码: %lu\n", exit_code);

    for (int i = 0; i < 4; i++) CloseHandle(threads[i]);
    return 0;
}
```

### Windows 同步对象

| 对象 | 用途 | API |
|------|------|-----|
| Critical Section | 进程内互斥 | InitializeCriticalSection / EnterCriticalSection |
| Mutex | 跨进程互斥 | CreateMutex / WaitForSingleObject |
| Semaphore | 资源计数 | CreateSemaphore / ReleaseSemaphore |
| Event | 事件通知 | CreateEvent / SetEvent / WaitForSingleObject |
| SRWLock | 读写锁(轻量) | InitializeSRWLock / AcquireSRWLockShared |

## 6. Java 线程

```java
// 方式1: 继承 Thread
class MyThread extends Thread {
    public void run() {
        System.out.println("Thread running: " + getName());
    }
}

// 方式2: 实现 Runnable
class MyRunnable implements Runnable {
    public void run() {
        System.out.println("Runnable running: " + Thread.currentThread().getName());
    }
}

public class Main {
    public static void main(String[] args) throws Exception {
        Thread t1 = new MyThread();
        Thread t2 = new Thread(new MyRunnable());
        t1.start();
        t2.start();
        t1.join();
        t2.join();

        // 线程池
        ExecutorService pool = Executors.newFixedThreadPool(4);
        pool.submit(() -> System.out.println("Pool task"));
        pool.shutdown();
    }
}
```

## 7. 线程池 (Thread Pool)

**优势:** 避免频繁创建/销毁线程的开销、控制并发数量、任务队列管理

```c
// 简单线程池实现
#include <pthread.h>
#include <stdlib.h>

typedef struct {
    void (*function)(void*);
    void *arg;
} task_t;

typedef struct {
    task_t      *tasks;
    int         capacity;
    int         front, rear, count;
    pthread_t   *threads;
    int         thread_count;
    pthread_mutex_t lock;
    pthread_cond_t  not_empty;
    pthread_cond_t  not_full;
    int         shutdown;
} threadpool_t;

void* worker(void* arg) {
    threadpool_t *pool = (threadpool_t*)arg;
    while (1) {
        pthread_mutex_lock(&pool->lock);
        while (pool->count == 0 && !pool->shutdown)
            pthread_cond_wait(&pool->not_empty, &pool->lock);

        if (pool->shutdown) {
            pthread_mutex_unlock(&pool->lock);
            return NULL;
        }

        task_t task = pool->tasks[pool->front];
        pool->front = (pool->front + 1) % pool->capacity;
        pool->count--;

        pthread_cond_signal(&pool->not_full);
        pthread_mutex_unlock(&pool->lock);

        task.function(task.arg);  // 执行任务
    }
}
```

## 8. 竞态条件与临界区 (Race Condition & Critical Section)

**竞态条件:** 多个线程并发访问共享数据，结果取决于执行时序

**临界区:** 访问共享资源的代码段，需要互斥访问

```c
// 竞态条件示例
int counter = 0;

// 以下操作不是原子的:
// counter++ 实际是3条指令:
//   LOAD counter, R1
//   ADD R1, 1
//   STORE R1, counter

void* unsafe(void* arg) {
    for (int i = 0; i < 100000; i++) counter++;
    return NULL;
}
// 预期: 200000, 实际: 可能小于200000
```

## 9. 互斥锁 vs 信号量

| 特性 | Mutex (互斥锁) | Semaphore (信号量) |
|------|---------------|-------------------|
| 值范围 | 0或1 | 0..N |
| 用途 | 互斥访问 | 资源计数 / 同步 |
| 所有权 | 有(同一线程释放) | 无(任何线程可释放) |
| 初始状态 | 1(解锁) | N(可用资源数) |
| 典型问题 | 死锁 | 死锁 + 信号丢失 |

## 10. 死锁 (Deadlock)

### 四个必要条件

1. **互斥 (Mutual Exclusion)**: 资源一次只能一个线程使用
2. **持有并等待 (Hold and Wait)**: 线程持有资源同时等待其他资源
3. **不可剥夺 (No Preemption)**: 资源只能自愿释放
4. **循环等待 (Circular Wait)**: 存在循环等待链

```
     Thread A                    Thread B
        │                           │
    ┌───┴────┐                  ┌───┴────┐
    │ Lock X │                  │ Lock Y │
    └───┬────┘                  └───┬────┘
        │                           │
    ┌───▼────┐                  ┌───▼────┐
    │ Wait Y │                  │ Wait X │
    └───┬────┘                  └───┬────┘
        └──────────┬────────────────┘
                   │
               DEADLOCK!
```

```c
// 死锁示例
pthread_mutex_t lock1, lock2;

void* thread_a(void* arg) {
    pthread_mutex_lock(&lock1);
    sleep(1);  // 确保两个线程都拿到第一个锁
    pthread_mutex_lock(&lock2);  // 死锁!
    pthread_mutex_unlock(&lock2);
    pthread_mutex_unlock(&lock1);
    return NULL;
}

void* thread_b(void* arg) {
    pthread_mutex_lock(&lock2);
    sleep(1);
    pthread_mutex_lock(&lock1);  // 死锁!
    pthread_mutex_unlock(&lock1);
    pthread_mutex_unlock(&lock2);
    return NULL;
}
```

### 死锁处理策略

| 策略 | 方法 | 评价 |
|------|------|------|
| **预防** | 破坏四个必要条件之一 | 资源利用率低 |
| **避免** | 银行家算法 | 需预先知道最大需求 |
| **检测** | 资源分配图化简 | 检测到后手工恢复 |
| **恢复** | 终止进程/剥夺资源 | 成本高 |

### 银行家算法 (Banker's Algorithm)

```c
#define N 5  // 进程数
#define M 3  // 资源类型数

int available[M];           // 可用资源
int max[N][M];              // 最大需求
int allocation[N][M];       // 已分配
int need[N][M];             // 还需要 = max - allocation

// 安全性检查
int is_safe() {
    int work[M];
    int finish[N] = {0};
    for (int i = 0; i < M; i++) work[i] = available[i];

    for (int k = 0; k < N; k++) {
        int found = 0;
        for (int i = 0; i < N; i++) {
            if (!finish[i]) {
                int j;
                for (j = 0; j < M; j++)
                    if (need[i][j] > work[j]) break;
                if (j == M) {  // 所有 need <= work
                    for (j = 0; j < M; j++)
                        work[j] += allocation[i][j];
                    finish[i] = 1;
                    found = 1;
                    break;
                }
            }
        }
        if (!found) break;
    }

    for (int i = 0; i < N; i++)
        if (!finish[i]) return 0;
    return 1;
}
```

### 避免死锁的最佳实践

```c
// 方法1: 固定锁顺序 (破坏循环等待)
// 总是先锁 lock1再锁 lock2
void safe_thread_a() {
    pthread_mutex_lock(&lock1);
    pthread_mutex_lock(&lock2);
    // 临界区
    pthread_mutex_unlock(&lock2);
    pthread_mutex_unlock(&lock1);
}

void safe_thread_b() {
    pthread_mutex_lock(&lock1);  // 和 a 顺序一致
    pthread_mutex_lock(&lock2);
    pthread_mutex_unlock(&lock2);
    pthread_mutex_unlock(&lock1);
}

// 方法2: trylock (破坏不可剥夺)
void trylock_thread() {
    while (1) {
        pthread_mutex_lock(&lock1);
        if (pthread_mutex_trylock(&lock2) == 0) {
            break;  // 两个锁都拿到
        }
        pthread_mutex_unlock(&lock1);  // 释放已持有的锁
        // 等待后重试
    }
    // 临界区
    pthread_mutex_unlock(&lock2);
    pthread_mutex_unlock(&lock1);
}

// 方法3: 使用单个锁 + 分层
// 或使用无锁数据结构
```

## 11. 生产者-消费者问题

```c
#define BUFFER_SIZE 10
int buffer[BUFFER_SIZE];
int in = 0, out = 0, count = 0;

pthread_mutex_t mutex = PTHREAD_MUTEX_INITIALIZER;
pthread_cond_t full  = PTHREAD_COND_INITIALIZER;
pthread_cond_t empty = PTHREAD_COND_INITIALIZER;

void* producer(void* arg) {
    for (int i = 0; i < 100; i++) {
        pthread_mutex_lock(&mutex);
        while (count == BUFFER_SIZE)
            pthread_cond_wait(&empty, &mutex);
        buffer[in] = i;
        in = (in + 1) % BUFFER_SIZE;
        count++;
        pthread_cond_signal(&full);
        pthread_mutex_unlock(&mutex);
    }
    return NULL;
}

void* consumer(void* arg) {
    for (int i = 0; i < 100; i++) {
        pthread_mutex_lock(&mutex);
        while (count == 0)
            pthread_cond_wait(&full, &mutex);
        int val = buffer[out];
        out = (out + 1) % BUFFER_SIZE;
        count--;
        pthread_cond_signal(&empty);
        pthread_mutex_unlock(&mutex);
        printf("消费: %d\n", val);
    }
    return NULL;
}
```

## 12. 读者-写者问题

```c
pthread_rwlock_t rwlock = PTHREAD_RWLOCK_INITIALIZER;
int shared_data = 0;

// 读者优先策略:
// 多个读者可同时读, 写者必须等待所有读者完成
void* reader(void* arg) {
    pthread_rwlock_rdlock(&rwlock);
    printf("读取数据: %d\n", shared_data);
    pthread_rwlock_unlock(&rwlock);
    return NULL;
}

void* writer(void* arg) {
    pthread_rwlock_wrlock(&rwlock);
    shared_data++;
    printf("写入数据: %d\n", shared_data);
    pthread_rwlock_unlock(&rwlock);
    return NULL;
}
```

## 相关条目

- [[Process]]
- [[Concurrency]]
- [[死锁与并发控制]]
- [[Scheduling]]
- [[ProcessManagement]]
