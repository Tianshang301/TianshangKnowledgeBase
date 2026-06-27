---
aliases: [ProcessManagement]
tags: ['OperatingSystems', 'ProcessManagement', 'ProcessManagement']
created: 2026-05-16
updated: 2026-05-16
---

# 进程管理详解 (Process Management)

## 一、进程概念 (Process Concept)

进程是正在执行的程序实例，是操作系统资源分配的基本单位。

```
进程内存布局：
┌──────────────────┐
│ 代码段 (Text)    │ 可执行指令（只读）
├──────────────────┤
│ 数据段 (Data)    │ 全局变量
├──────────────────┤
│ 堆 (Heap)        │ 动态分配（向上增长）
├──────────────────┤
│                  │
│    空闲空间       │
│                  │
├──────────────────┤
│ 栈 (Stack)       │ 局部变量（向下增长）
└──────────────────┘
```

### 进程 vs 程序

| 特性 | 程序 | 进程 |
|------|------|------|
| 本质 | 静态文件 | 动态执行 |
| 存储 | 磁盘 | 内存 |
| 生命周期 | 永久 | 创建→终止 |
| 对应关系 | 1个程序可对应多进程 | 唯一 PID |

## 二、进程状态 (Process States)

### 五状态模型

```
         ┌──────┐
         │ New  │
         └──┬───┘
            │ admit
            ▼
   ┌────┐  dispatch  ┌───────┐  I/O 请求  ┌───────┐
   │Ready│───────────►│Running│──────────►│Waiting│
   └─────┘            └───┬───┘           └───┬───┘
        ▲                 │                    │
        │              timeout                 │ I/O 完成
        │                 │                    │
        │                 ▼                    │
        │            ┌───────┐                 │
        └────────────┤ Term  │◄────────────────┘
                     └───────┘
```

| 状态 | 说明 |
|------|------|
| **New (新建)** | 进程正在创建 |
| **Ready (就绪)** | 在内存中，等待 CPU 调度 |
| **Running (运行)** | 占用 CPU 执行 |
| **Waiting (等待/阻塞)** | 等待 I/O 或事件 |
| **Terminated (终止)** | 执行完毕 |

### Linux 进程状态

| 状态 | 内核宏 | 描述 |
|------|--------|------|
| R | TASK_RUNNING | 运行或可运行 |
| S | TASK_INTERRUPTIBLE | 可中断睡眠 |
| D | TASK_UNINTERRUPTIBLE | 不可中断睡眠 |
| T | __TASK_STOPPED | 停止 |
| Z | EXIT_ZOMBIE | 僵尸进程 |

## 三、进程控制块 (Process Control Block)

PCB 是内核管理进程的数据结构，每个进程一个。

### PCB 关键内容

```
┌─────────────────────────┐
│ PID (进程标识符)         │
├─────────────────────────┤
│ 程序计数器 (PC)          │
├─────────────────────────┤
│ CPU 寄存器              │
├─────────────────────────┤
│ 调度信息 (优先级、队列)    │
├─────────────────────────┤
│ 内存管理信息 (页表)       │
├─────────────────────────┤
│ I/O 状态 (打开的文件)      │
├─────────────────────────┤
│ 记账信息 (CPU 时间等)     │
└─────────────────────────┘
```

### Linux task_struct

```c
struct task_struct {
    pid_t pid;
    volatile long state;
    unsigned int flags;
    struct task_struct *parent;
    struct list_head children;
    struct mm_struct *mm;        // 内存管理
    struct files_struct *files;  // 打开文件
    struct fs_struct *fs;        // 文件系统
    struct signal_struct *signal;
    const struct sched_class *sched_class;
    struct sched_entity se;      // 调度实体
};
```

## 四、上下文切换 (Context Switch)

CPU 从一进程切换到另一进程时的操作。

### 切换开销

| 开销类型 | 说明 |
|---------|------|
| 寄存器保存/恢复 | PC, SP, 通用寄存器等 |
| 页表切换 | TLB 刷新 |
| Cache 污染 | 新进程需重新加载 cache |
| 内核栈切换 | 需切换到内核栈 |

```c
// 上下文切换伪代码
void context_switch(struct task_struct *prev, struct task_struct *next) {
    switch_mm(prev->active_mm, next->active_mm);
    switch_to(prev, next);
}
```

## 五、进程创建 (Process Creation)

### fork() 系统调用

```c
#include <stdio.h>
#include <unistd.h>
#include <sys/wait.h>

int main() {
    pid_t pid = fork();

    if (pid < 0) {
        perror("fork failed");
        return 1;
    } else if (pid == 0) {
        // 子进程
        printf("子进程: PID=%d, 父 PID=%d\n", getpid(), getppid());
        execlp("/bin/ls", "ls", "-l", NULL);
        perror("execlp");
        return 1;
    } else {
        // 父进程
        printf("父进程: 子 PID=%d\n", pid);
        wait(NULL);  // 回收子进程
    }
    return 0;
}
```

| fork 返回值 | 说明 |
|-----------|------|
| `pid > 0` | 父进程，返回子 PID |
| `pid == 0` | 子进程 |
| `pid < 0` | 创建失败 |

### exec 家族

| 函数 | 路径搜索 | 参数格式 | 环境变量 |
|------|---------|---------|---------|
| `execlp` | PATH 搜索 | 列表 | 继承 |
| `execvp` | PATH 搜索 | 数组 | 继承 |
| `execle` | 精确路径 | 列表 | 自定义 |
| `execve` | 精确路径 | 数组 | 自定义（系统调用） |

### 僵尸进程 vs 孤儿进程

| 类型 | 父进程 | 子进程 | 影响 |
|------|--------|--------|------|
| **僵尸 (Zombie)** | 未调用 wait | 已终止 | 占用 PCB，泄漏资源 |
| **孤儿 (Orphan)** | 先终止 | 仍在运行 | 被 init(PID=1)收养 |

```c
// 避免僵尸：信号处理
void sigchld_handler(int sig) {
    while (waitpid(-1, NULL, WNOHANG) > 0)
        ;
}

int main() {
    signal(SIGCHLD, sigchld_handler);
    // ... fork 子进程
}
```

## 六、进程间通信 (IPC)

### IPC 方式对比

| 方式 | 速度 | 网络支持 | 适用场景 |
|------|------|---------|---------|
| **共享内存** | 最快 | 否 | 大数据量 |
| **消息队列** | 中 | 否 | 结构化消息 |
| **管道 (Pipe)** | 慢 | 否 | 父子进程 |
| **命名管道 (FIFO)** | 慢 | 否 | 本机任意进程 |
| **信号 (Signal)** | 慢 | 否 | 事件通知 |
| **套接字 (Socket)** | 中 | 是 | 跨主机通信 |

### 共享内存示例

```c
// 共享内存 (System V)
int shmid = shmget(IPC_PRIVATE, 4096, IPC_CREAT | 0666);
void *data = shmat(shmid, NULL, 0);
strcpy(data, "Hello");
shmdt(data);
```

### 管道示例

```c
int fd[2];
pipe(fd);  // fd[0]=读端, fd[1]=写端

if (fork() == 0) {
    close(fd[1]);
    read(fd[0], buf, sizeof(buf));
} else {
    close(fd[0]);
    write(fd[1], "data", 4);
}
```

## 七、CPU 调度 (CPU Scheduling)

### 调度目标

| 指标 | 定义 | 目标 |
|------|------|------|
| **吞吐量** | 单位时间完成的进程数 | 最大化 |
| **周转时间** | 进程从提交到完成的时间 | 最小化 |
| **等待时间** | 进程在就绪队列中等待总和 | 最小化 |
| **响应时间** | 从提交到首次响应的时间 | 最小化 |
| **CPU 利用率** | CPU 忙碌时间比例 | 最大化 |
| **公平性** | 各进程分配 CPU 公平程度 | 均衡 |

### 调度算法对比

| 算法 | 描述 | 抢占 | 饥饿 | 适用 |
|------|------|------|------|------|
| **FCFS** | 先来先服务 | ✗ | ✗ | 批处理 |
| **SJF** | 最短作业优先 | ✗ | ✓ | 批处理 |
| **SRTF** | 最短剩余时间优先 | ✓ | ✓ | 批处理 |
| **优先级** | 优先级高的先执行 | 可选 | ✓ | 通用 |
| **RR** | 时间片轮转 | ✓ | ✗ | 分时系统 |
| **多级队列** | 多队列不同算法 | ✓ | 可能 | 通用 |
| **多级反馈队列** | 动态调整队列 | ✓ | ✗ | 通用 OS |

### Round Robin 时间片选择

```
时间片太大 → 退化为 FCFS
时间片太小 → 上下文切换开销过大

经验值：10-100ms（切换开销约0.1-1ms，占1%以内）
```

### Linux CFS (Completely Fair Scheduler)

```c
// CFS 核心思想：用红黑树维护进程，选择 vruntime 最小的进程
// vruntime = 实际运行时间 × (nice_0_weight / process_weight)

// 调度延迟
// sched_latency_ns = 6ms (默认)
// 每个进程至少运行 min_granularity = 0.75ms

// CFS 时间片 = sched_latency / 进程数
// 进程数 > sched_latency / min_granularity → 使用 min_granularity
```

### 实时调度

| 算法 | 描述 | 可调度性判断 |
|------|------|-------------|
| **RM (Rate-Monotonic)** | 周期越短优先级越高 | $\sum_{i=1}^{n} \frac{C_i}{T_i} \leq n(2^{1/n} - 1)$ |
| **EDF (Earliest Deadline First)** | 截止时间越早优先级越高 | $\sum_{i=1}^{n} \frac{C_i}{T_i} \leq 1$ |

## 相关条目

- [[05_ComputerScience/ProgrammingLanguages/Go/Concurrency|Concurrency]]
- [[05_ComputerScience/OperatingSystems/MemoryManagement/MemoryManagement|MemoryManagement]]
- [[05_ComputerScience/OperatingSystems/Scheduling|Scheduling]]
- IPC

## 参考资源

- Silberschatz, A., Galvin, P. B., & Gagne, G. *Operating System Concepts* (10th ed.)
- Tanenbaum, A. S., & Bos, H. *Modern Operating Systems* (4th ed.)
- Love, R. *Linux Kernel Development* (3rd ed.)
- Linux kernel source: https://kernel.org/


