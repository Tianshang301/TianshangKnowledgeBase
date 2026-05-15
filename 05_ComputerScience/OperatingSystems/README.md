---
aliases: [README]
tags: ['OperatingSystems', 'README']
---

# 操作系统知识索引

## 目录

- [进程管理](#进程管理)
- [线程与并发](#线程与并发)
- [内存管理](#内存管理)
- [文件系统](#文件系统)
- [I/O 管理](#io-管理)
- [Linux 内核基础](#linux-内核基础)

---

## 进程管理

### 进程控制块 (PCB)

```
PCB (Task Struct) 包含：
┌─────────────────────────────┐
│  进程标识符 (PID)            │
│  进程状态 (就绪/运行/阻塞)     │
│  程序计数器 (PC)             │
│  CPU 寄存器                  │
│  内存地址空间                 │
│  打开的文件描述符              │
│  CPU 调度信息 (优先级等)       │
│  统计信息 (CPU 时间等)         │
│  父子进程指针                  │
└─────────────────────────────┘
```

### 进程状态转换

```
       ┌──────┐
       │ 创建  │
       └──┬───┘
          ▼
    ┌──────────┐    调度     ┌────────┐
    │  就绪态   │───────────►│ 运行态  │
    └──────────┘            └───┬────┘
          ▲                     │ 等待 I/O
          │                     ▼
          │               ┌──────────┐
          │               │  阻塞态   │
          │               └────┬─────┘
          │     I/O 完成       │
          └────────────────────┘
```

### 调度算法

| 算法 | 策略 | 优点 | 缺点 |
|------|------|------|------|
| FCFS | 先来先服务 | 公平 | 平均等待时间长 |
| SJF | 最短作业优先 | 最小平均周转时间 | 无法预知执行时间 |
| 时间片轮转 | 固定时间片 | 响应时间好 | 上下文切换开销 |
| 优先级调度 | 按优先级 | 可区分重要程度 | 低优先级可能饿死 |
| 多级反馈队列 | 多队列+动态调整 | 兼顾响应和吞吐 | 实现复杂 |

```c
// 时间片轮转调度示意
#define TIME_QUANTUM 10  // 时间片（毫秒）

typedef struct Process {
    int pid;
    int remaining_time;  // 剩余执行时间
    struct Process *next;
} Process;

void round_robin(Process *head) {
    if (!head) return;

    Process *current = head;
    do {
        int execute_time = min(TIME_QUANTUM, current->remaining_time);
        current->remaining_time -= execute_time;
        // 执行进程...
        run_process(current, execute_time);

        if (current->remaining_time == 0) {
            terminate_process(current);
            // 从队列移除
        }
        current = current->next;
    } while (current != head);
}
```

---

## 线程与并发

### 线程模型

```
用户级线程 (N:1)
   用户空间            内核空间
  ┌────────┐
  │线程库   │          ┌────────┐
  │ T1 T2 T3│─────────►│ 一个进程 │
  │         │          │ 一个内核 │
  └────────┘          │  线程   │
                       └────────┘

内核级线程 (1:1)
   用户空间            内核空间
  ┌────────┐          ┌────────┐
  │ T1 ├─────────────►│ KPT1   │
  │ T2 ├─────────────►│ KPT2   │
  │ T3 ├─────────────►│ KPT3   │
  └────────┘          └────────┘

混合模型 (M:N)
   用户空间             内核空间
  ┌────────┐           ┌────────┐
  │ 线程库   │          │ KPT1   │
  │ T1 T2 T3├──────────┤ KPT2   │
  │ T4 T5   │          └────────┘
  └────────┘
```

### 同步互斥

```c
// 互斥锁 (Mutex)
#include <pthread.h>

pthread_mutex_t lock = PTHREAD_MUTEX_INITIALIZER;
int shared_counter = 0;

void *increment(void *arg) {
    for (int i = 0; i < 1000000; i++) {
        pthread_mutex_lock(&lock);
        shared_counter++;
        pthread_mutex_unlock(&lock);
    }
    return NULL;
}

// 信号量 (Semaphore)
#include <semaphore.h>

sem_t empty, full;
#define BUFFER_SIZE 10
int buffer[BUFFER_SIZE];

void *producer(void *arg) {
    for (int i = 0; i < 100; i++) {
        sem_wait(&empty);    // P(empty)
        buffer[in] = i;
        in = (in + 1) % BUFFER_SIZE;
        sem_post(&full);     // V(full)
    }
    return NULL;
}

void *consumer(void *arg) {
    for (int i = 0; i < 100; i++) {
        sem_wait(&full);     // P(full)
        int data = buffer[out];
        out = (out + 1) % BUFFER_SIZE;
        sem_post(&empty);    // V(empty)
        printf("消费: %d\n", data);
    }
    return NULL;
}
```

### 经典并发问题

```
1. 生产者-消费者问题
   - 缓冲区满时生产者等待 → 使用信号量 empty
   - 缓冲区空时消费者等待 → 使用信号量 full
   - 互斥访问缓冲区 → 使用 mutex

2. 读者-写者问题
   - 读者可同时读
   - 写者必须独占访问
   - 读者优先 vs 写者优先策略

3. 哲学家就餐问题
   - 5 个哲学家、5 根筷子
   - 死锁避免：同时拿起两根筷子
   - 或者：限制最多 4 人同时就餐
```

### 死锁

```
死锁的四个必要条件：
  1. 互斥：资源一次只能一个进程使用
  2. 占有并等待：进程占有资源同时等待其他资源
  3. 不可剥夺：资源不能被强制剥夺
  4. 循环等待：存在循环等待链

死锁预防：
  - 破坏占有并等待：一次性申请所有资源
  - 破坏不可剥夺：允许资源回收
  - 破坏循环等待：资源有序分配

银行家算法示例：
  可用资源: [3, 3, 2]
  进程    最大需求    已分配    还需
  P0     [7,5,3]    [0,1,0]  [7,4,3]
  P1     [3,2,2]    [2,0,0]  [1,2,2]
  P2     [9,0,2]    [3,0,2]  [6,0,0]
  P3     [2,2,2]    [2,1,1]  [0,1,1]
  P4     [4,3,3]    [0,0,2]  [4,3,1]

安全序列: P1 → P3 → P4 → P0 → P2
```

---

## 内存管理

### 分页与分段

```
分页（Paging）：
  ┌──────┬──────┬──────┬──────┐
  │ 页0  │ 页1  │ 页2  │ 页3  │  进程逻辑地址空间
  └──┬───┴──┬───┴──┬───┴──┬───┘
     │      │      │      │
     ▼      ▼      ▼      ▼
  ┌──────┬──────┬──────┬──────┬──────┬──────┐
  │ 帧0  │ 帧1  │ 帧2  │ 帧3  │ 帧4  │ 帧5  │  物理内存
  └──────┴──────┴──────┴──┬───┴──────┴──────┘
                          │
                       页2 (来自进程)

分段（Segmentation）：
  ┌──────────┐
  │  代码段   │  ├──→ 基址 0x1000, 限制 0x2000
  ├──────────┤
  │  数据段   │  ├──→ 基址 0x3000, 限制 0x1000
  ├──────────┤
  │  堆栈段   │  ├──→ 基址 0x7fff, 限制 0x1000
  └──────────┘
```

### 虚拟内存

```
虚拟地址 → 物理地址转换（x86-64 四级页表）：

虚拟地址 (48位):
┌──────┬──────┬──────┬──────┬────────┐
│ PML4 │ PDP  │  PD  │  PT  │ offset │
│ 9bit │ 9bit │ 9bit │ 9bit │ 12bit  │
└──┬───┴──┬───┴──┬───┴──┬───┴────────┘
   │      │      │      │
   ▼      ▼      ▼      ▼
┌────┐ ┌────┐ ┌────┐ ┌────┐ ┌────────┐
│PML4│→│ PDP│→│ PD │→│ PT │→│物理页框│
└────┘ └────┘ └────┘ └────┘ └────────┘
(4KB) (4KB) (4KB) (4KB)
```

### 页面置换算法

| 算法 | 策略 | 特点 |
|------|------|------|
| FIFO | 淘汰最先进入的页 | 实现简单，可能异常(Belady) |
| LRU | 淘汰最近最久未使用 | 性能好，实现成本高 |
| Clock | 近似 LRU（二次机会） | 实用折中 |
| 最优(OPT) | 淘汰未来最远使用的页 | 理论最优，不可实现 |

```c
// Clock 置换算法示意
typedef struct Page {
    int page_num;
    int referenced;  // 引用位
    struct Page *next;
} Page;

Page *clock_algorithm(Page *head, int page_num) {
    Page *current = head;
    while (1) {
        if (current->page_num == page_num) {
            current->referenced = 1;  // 命中，设置引用位
            return current;
        }

        if (current->referenced == 0) {
            // 淘汰此页
            current->page_num = page_num;
            current->referenced = 1;
            return current;
        } else {
            current->referenced = 0;  // 给第二次机会
            current = current->next;
        }
    }
}
```

---

## 文件系统

### inode 结构

```
inode (索引节点):
┌─────────────────────────────┐
│  文件类型与权限              │
│  硬链接计数                  │
│  所有者 UID / GID            │
│  文件大小                    │
│  时间戳 (access/modify/change) │
│  数据块指针:                 │
│    ├── 12 个直接块指针       │
│    ├── 1 个一级间接块指针     │
│    ├── 1 个二级间接块指针     │
│    └── 1 个三级间接块指针     │
└─────────────────────────────┘
```

### 文件系统对比

| 特性 | FAT32 | NTFS | ext4 |
|------|-------|------|------|
| 操作系统 | 跨平台 | Windows | Linux |
| 最大文件 | 4GB | 16EB | 16TB |
| 最大卷 | 2TB | 256TB | 1EB |
| 日志 | 无 | 有 | 有 |
| 压缩 | 无 | 有 | 无 |
| 加密 | 无 | EFS | 可选 |
| 硬链接 | 无 | 有 | 有 |
| 快照 | 无 | 有 | 有 |

### Linux VFS (虚拟文件系统)

```
系统调用层（open, read, write, close...）
        │
┌───────▼────────┐
│  Virtual Filesystem │
│  (VFS)              │
└───────┬────────┘
        │
  ┌─────┼─────┬──────┐
  ▼     ▼     ▼      ▼
ext4   NTFS  tmpfs  procfs
(设备)  (网盘) (内存) (/proc)
```

---

## I/O 管理

### I/O 控制方式

```
1. 程序直接控制（轮询）
   CPU 不断检查设备状态 → CPU 浪费严重

2. 中断驱动
   设备完成后发中断 → CPU 利用率高，但频繁中断

3. DMA（直接内存访问）
   流程图：
   CPU → 设置 DMA 寄存器 → DMA 控制器负责数据传输
                            ↓
   CPU 继续其他工作    ←  完成中断

4. 通道控制
   专用 I/O 处理器，可执行通道程序
```

### 缓冲技术

```
单缓冲：
  用户进程 ──→ 缓冲区 ──→ I/O 设备

双缓冲：
  用户进程 ──→ 缓冲区1 ←── I/O 设备
             └──→ 缓冲区2 ←── I/O 设备

循环缓冲：
  ┌─────┐  ┌─────┐  ┌─────┐
  │ B0  │→│ B1  │→│ B2  │→ back to B0
  └─────┘  └─────┘  └─────┘
```

### SPOOLing 技术

```
SPOOLing 系统（假脱机）：

输入进程 → 输入井（磁盘） → 内存 → 用户进程
                                              ← 输出进程 → 输出井（磁盘） → 打印机

示例：打印队列
  lpr document.pdf    # 提交打印任务
  lpq                 # 查看队列
  ┌────────────────────────┐
  │ 打印队列:               │
  │ Rank  Job   File       │
  │ 1     job1  doc1.pdf   │
  │ 2     job2  doc2.pdf   │
  │ 3     job3  photo.jpg  │
  └────────────────────────┘
```

---

## Linux 内核基础

### 内核架构

```
用户空间（Ring 3）
  ┌─────────────────────────────┐
  │  用户进程 / Shell / GUI      │
  │  (通过系统调用进入内核)       │
  ├─────────────────────────────┤
  │  系统调用接口 (syscall)       │
  ├─────────────────────────────┤
  │  进程管理    │   内存管理     │
  │  (调度器)   │   (VMA+页表)   │
  ├────────────┼───────────────┤
  │  文件系统    │    网络协议栈   │
  │  (VFS)     │   (TCP/IP)    │
  ├────────────┼───────────────┤
  │ 设备驱动 │    中断处理       │
  ├────────────┴───────────────┤
  │  硬件抽象层 (HAL)           │
  ├─────────────────────────────┤
  │         硬件                  │
  │  (CPU / 内存 / 磁盘 / 网卡)  │
  └─────────────────────────────┘
内核空间（Ring 0）
```

### 常用系统调用

```c
// 进程管理
pid_t fork(void);        // 创建子进程
pid_t wait(int *status); // 等待子进程结束
int execve(const char *path, char *const argv[], char *const envp[]);

// 文件操作
int open(const char *path, int flags, mode_t mode);
ssize_t read(int fd, void *buf, size_t count);
ssize_t write(int fd, const void *buf, size_t count);
int close(int fd);

// 内存管理
void *mmap(void *addr, size_t length, int prot, int flags, int fd, off_t offset);
int munmap(void *addr, size_t length);
void *sbrk(intptr_t increment);  // 调整堆大小

// 进程间通信
int pipe(int pipefd[2]);           // 管道
int shmget(key_t key, size_t size, int shmflg);  // 共享内存
int semget(key_t key, int nsems, int semflg);    // 信号量
int msgget(key_t key, int msgflg);               // 消息队列
```

### /proc 文件系统

```bash
# 进程信息
/proc/[pid]/status       # 进程状态
/proc/[pid]/fd/          # 文件描述符
/proc/[pid]/maps         # 内存映射
/proc/[pid]/cmdline      # 命令行参数
/proc/[pid]/environ      # 环境变量

# 系统信息
/proc/cpuinfo            # CPU 信息
/proc/meminfo            # 内存信息
/proc/version            # 内核版本
/proc/loadavg            # 系统负载
/proc/diskstats          # 磁盘 I/O 统计
```

```bash
# 查看系统负载
$ cat /proc/loadavg
2.15 1.83 1.65 3/456 12345
# 1min  5min  15min  运行/总进程 PID

# 查看内存使用
$ cat /proc/meminfo
MemTotal:       16384716 kB
MemFree:         2345678 kB
Buffers:          345678 kB
Cached:          4567890 kB
SwapTotal:       8388604 kB
SwapFree:        7345678 kB
```

---

## 相关条目

- ComputerOrganization
- [[ComputerNetworks]]
- [[05_ComputerScience/ProgrammingLanguages/INDEX|ProgrammingLanguages]]
- [[FileSystems]]

> **参考资源**：《Operating System Concepts》(Silberschatz)、《Modern Operating Systems》(Tanenbaum)、《Linux Kernel Development》、Linux 手册页
