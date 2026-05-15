---
aliases: [Process]
tags: ['OperatingSystems', 'Process']
---

# 进程管理详解 (Process Management)

## 1. 进程概念 (Process Concept)

进程是正在执行的程序的实例。进程是操作系统资源分配的基本单位，包含：

- **代码段 (Text Section)**: 可执行代码
- **数据段 (Data Section)**: 全局变量
- **堆 (Heap)**: 动态分配的内存
- **栈 (Stack)**: 函数调用、局部变量、返回地址

### 程序 vs 进程

| 特性 | 程序 | 进程 |
|------|------|------|
| 本质 | 静态文件(磁盘) | 动态执行(内存) |
| 生命周期 | 永久存在 | 创建到终止 |
| 资源 | 占用磁盘空间 | 占用CPU、内存等 |
| 唯一性 | 一个程序可多个进程 | 每个进程有唯一PID |

## 2. 进程控制块 (Process Control Block, PCB)

PCB是操作系统管理进程的核心数据结构，存储在内核空间。每个进程有唯一PCB。

**PCB主要内容:**

```
Process ID (PID)
Program Counter (PC)
CPU Registers
CPU Scheduling Info (priority, queue pointers)
Memory Management Info (page table, segment table)
Accounting Info (CPU time, time limits)
I/O Status (open files, devices allocated)
```

**Linux task_struct 关键字段 (include/linux/sched.h):**

```c
struct task_struct {
    pid_t                 pid;
    pid_t                 tgid;
    struct task_struct    *parent;
    struct list_head      children;
    struct mm_struct      *mm;
    struct files_struct   *files;
    struct fs_struct      *fs;
    struct signal_struct  *signal;
    unsigned int          flags;
    struct list_head      tasks;
    /* 调度相关 */
    int                   prio;
    int                   static_prio;
    unsigned int          time_slice;
    /* 状态 */
    volatile long         state;
};
```

## 3. 进程状态 (Process States)

### 五状态模型

```
                ┌─────────────┐
                │    New      │ (进程创建)
                └──────┬──────┘
                       │ admit
                       ▼
    ┌──────────┐  dispatch  ┌──────────┐  I/O或event   ┌──────────┐
    │  Ready   │───────────►│ Running  │──────────────►│ Waiting  │
    └──────────┘            └──────────┘               └──────────┘
          ▲                      │                           │
          │                    exit                          │
          │                  I/O完成                         │ I/O完成
          │                      ▼                           │ or event
          │               ┌─────────────┐                    │
          │               │ Terminated  │◄───────────────────┘
          │               └─────────────┘
          └──────────────────────────────────────────────────┘
                        (timer interrupt: preempt)
```

| 状态 | 描述 |
|------|------|
| **New** | 进程正在被创建 |
| **Ready** | 进程已在内存中，等待CPU调度 |
| **Running** | 进程正在CPU上执行 |
| **Waiting (Blocked)** | 进程等待I/O或事件完成 |
| **Terminated** | 进程已完成执行 |

### Linux进程状态

```c
#define TASK_RUNNING        0   // R (可运行或正在运行)
#define TASK_INTERRUPTIBLE  1   // S (可中断睡眠)
#define TASK_UNINTERRUPTIBLE 2  // D (不可中断睡眠)
#define __TASK_STOPPED      4   // T (停止)
#define __TASK_TRACED       8   // t (被跟踪)
#define EXIT_DEAD           16  // X (死亡)
#define EXIT_ZOMBIE         32  // Z (僵尸)
```

## 4. 上下文切换 (Context Switch)

当CPU切换到另一个进程时，系统保存当前进程的状态(PCB)并加载新进程的保存状态。

**切换开销:**
- 保存/恢复寄存器(PC, SP, 通用寄存器)
- TLB刷新
- Cache污染
- 页表切换(CR3寄存器)

```c
// 上下文切换伪代码
void context_switch(struct task_struct *prev, struct task_struct *next) {
    // 保存prev的CPU状态
    save_processor_state(prev);
    // 更新内存管理(切换页表)
    switch_mm(prev->active_mm, next->active_mm);
    // 切换寄存器状态
    switch_to(prev, next);
    // 恢复next的CPU状态
    restore_processor_state(next);
}
```

## 5. 进程创建 (Process Creation)

### Linux: fork() / exec() / wait()

```c
#include <stdio.h>
#include <unistd.h>
#include <sys/wait.h>

int main() {
    pid_t pid = fork();  // 创建子进程

    if (pid < 0) {
        // fork失败
        perror("fork failed");
        return 1;
    } else if (pid == 0) {
        // 子进程
        printf("子进程: PID=%d, 父PID=%d\n", getpid(), getppid());
        execlp("/bin/ls", "ls", "-l", NULL);  // 替换进程映像
        perror("execlp failed");
        return 1;
    } else {
        // 父进程
        printf("父进程: 子PID=%d\n", pid);
        int status;
        waitpid(pid, &status, 0);  // 等待子进程结束
        printf("子进程退出状态: %d\n", WEXITSTATUS(status));
    }
    return 0;
}
```

**exec家族:**

| 函数 | 描述 |
|------|------|
| execlp | 参数列表 + PATH搜索 |
| execvp | 参数数组 + PATH搜索 |
| execle | 参数列表 + 环境变量 |
| execve | 参数数组 + 环境变量 (系统调用) |

### Windows: CreateProcess()

```c
#include <windows.h>
#include <stdio.h>

int main() {
    STARTUPINFO si;
    PROCESS_INFORMATION pi;
    ZeroMemory(&si, sizeof(si));
    ZeroMemory(&pi, sizeof(pi));
    si.cb = sizeof(si);

    // 创建记事本进程
    if (!CreateProcess(
            "C:\\Windows\\System32\\notepad.exe",  // 可执行文件
            NULL,           // 命令行参数
            NULL, NULL,     // 安全属性
            FALSE,          // 句柄继承
            0,              // 创建标志
            NULL,           // 环境变量
            NULL,           // 工作目录
            &si,            // STARTUPINFO
            &pi)) {         // PROCESS_INFORMATION
        printf("CreateProcess失败: %lu\n", GetLastError());
        return 1;
    }

    printf("进程句柄: %p, 线程句柄: %p\n", pi.hProcess, pi.hThread);
    printf("进程ID: %lu, 线程ID: %lu\n", pi.dwProcessId, pi.dwThreadId);

    // 等待进程结束
    WaitForSingleObject(pi.hProcess, INFINITE);
    CloseHandle(pi.hProcess);
    CloseHandle(pi.hThread);
    return 0;
}
```

## 6. 进程终止 (Process Termination)

### 正常终止
- `exit()` / `_exit()` — 请求系统调用
- main函数return
- `ExitProcess()` (Windows)

### 异常终止
- `abort()` — SIGABRT信号
- 段错误 (SIGSEGV)
- 被其他进程杀死 (`kill()`)

### 僵尸进程 (Zombie Process)

子进程已终止，但其PCB尚未被父进程回收(wait)。

```c
// 制造僵尸进程
int main() {
    pid_t pid = fork();
    if (pid == 0) {
        printf("子进程退出\n");
        exit(0);  // 子进程退出，变为僵尸
    }
    sleep(10);  // 父进程sleep期间，子进程是僵尸
    // 此时 ps aux 可看到 <defunct> 或 Z
    wait(NULL);  // 回收僵尸
    return 0;
}
```

### 孤儿进程 (Orphan Process)

父进程先于子进程终止，子进程被init(PID=1)收养。

```c
// 制造孤儿进程
int main() {
    pid_t pid = fork();
    if (pid == 0) {
        sleep(5);  // 父进程先退出
        printf("子进程(孤儿) PPID=%d\n", getppid());  // PPID变为1
        sleep(5);
    } else {
        printf("父进程退出\n");
        exit(0);
    }
    return 0;
}
```

### 守护进程 (Daemon Process)

后台运行、无控制终端的进程。

```c
// 守护进程创建步骤
void create_daemon() {
    pid_t pid = fork();
    if (pid > 0) exit(0);           // 父进程退出

    setsid();                        // 创建新会话
    chdir("/");                      // 更改工作目录
    umask(0);                        // 重置文件掩码

    close(STDIN_FILENO);             // 关闭标准I/O
    close(STDOUT_FILENO);
    close(STDERR_FILENO);

    while (1) {
        // 守护进程工作循环
        sleep(1);
    }
}
```

## 7. 进程间通信 (Inter-Process Communication, IPC)

### 7.1 管道 (Pipe)

**匿名管道:** 仅用于父子/兄弟进程

```c
int main() {
    int fd[2];
    pipe(fd);  // fd[0]读端, fd[1]写端

    if (fork() == 0) {
        close(fd[1]);           // 关闭写端
        char buf[256];
        read(fd[0], buf, sizeof(buf));
        printf("子进程收到: %s", buf);
        close(fd[0]);
    } else {
        close(fd[0]);           // 关闭读端
        write(fd[1], "Hello from parent!\n", 19);
        close(fd[1]);
        wait(NULL);
    }
    return 0;
}
```

### 7.2 FIFO (命名管道)

允许无亲缘关系进程通信。

```c
// Server
int main() {
    mkfifo("/tmp/myfifo", 0666);
    int fd = open("/tmp/myfifo", O_RDONLY);
    char buf[256];
    read(fd, buf, sizeof(buf));
    printf("收到: %s\n", buf);
    close(fd);
    unlink("/tmp/myfifo");
    return 0;
}

// Client
int main() {
    int fd = open("/tmp/myfifo", O_WRONLY);
    write(fd, "Hello via FIFO!", 16);
    close(fd);
    return 0;
}
```

### 7.3 共享内存 (Shared Memory)

最高效的IPC方式，需要同步机制。

```c
// Server
#include <sys/shm.h>
int main() {
    key_t key = ftok("shmfile", 65);
    int shmid = shmget(key, 1024, 0666 | IPC_CREAT);
    char *data = (char*)shmat(shmid, NULL, 0);
    strcpy(data, "Shared memory data!");
    printf("写入共享内存: %s\n", data);
    shmdt(data);
    return 0;
}

// Client
int main() {
    key_t key = ftok("shmfile", 65);
    int shmid = shmget(key, 1024, 0666);
    char *data = (char*)shmat(shmid, NULL, 0);
    printf("读取共享内存: %s\n", data);
    shmdt(data);
    shmctl(shmid, IPC_RMID, NULL);  // 删除共享内存
    return 0;
}
```

### 7.4 消息队列 (Message Queue)

```c
// 发送
struct msgbuf { long mtype; char mtext[100]; };
int main() {
    key_t key = ftok("msgq", 65);
    int msgid = msgget(key, 0666 | IPC_CREAT);
    struct msgbuf msg = {1, "Message Queue Hello!"};
    msgsnd(msgid, &msg, sizeof(msg.mtext), 0);
    printf("消息已发送\n");
    return 0;
}

// 接收
int main() {
    struct msgbuf msg;
    key_t key = ftok("msgq", 65);
    int msgid = msgget(key, 0666);
    msgrcv(msgid, &msg, sizeof(msg.mtext), 1, 0);
    printf("收到消息: %s\n", msg.mtext);
    msgctl(msgid, IPC_RMID, NULL);
    return 0;
}
```

### 7.5 信号 (Signal)

```c
void handler(int sig) {
    printf("收到信号: %d (SIGINT)\n", sig);
    exit(0);
}

int main() {
    signal(SIGINT, handler);  // Ctrl+C触发
    while (1) {
        printf("运行中...\n");
        sleep(1);
    }
    return 0;
}
```

**常用信号:**

| 信号 | 值 | 默认行为 | 描述 |
|------|-----|---------|------|
| SIGHUP | 1 | Term | 终端挂断 |
| SIGINT | 2 | Term | 键盘中断(Ctrl+C) |
| SIGQUIT | 3 | Core | 键盘退出(Ctrl+\\) |
| SIGKILL | 9 | Term | 强制终止(不可捕获) |
| SIGSEGV | 11 | Core | 段错误 |
| SIGTERM | 15 | Term | 终止信号 |
| SIGCHLD | 17 | Ign | 子进程状态改变 |

### 7.6 套接字 (Socket)

跨主机进程间通信。

```c
// TCP Server
int main() {
    int sockfd = socket(AF_INET, SOCK_STREAM, 0);
    struct sockaddr_in addr = {
        .sin_family = AF_INET,
        .sin_port = htons(8080),
        .sin_addr.s_addr = INADDR_ANY
    };
    bind(sockfd, (struct sockaddr*)&addr, sizeof(addr));
    listen(sockfd, 5);

    int client = accept(sockfd, NULL, NULL);
    char buf[1024];
    read(client, buf, sizeof(buf));
    printf("收到: %s\n", buf);
    write(client, "HTTP/1.1 200 OK\r\nContent-Length: 12\r\n\r\nHello World!", 50);
    close(client);
    close(sockfd);
    return 0;
}
```

## IPC方式对比

| 方式 | 速度 | 适用场景 | 支持网络 | 内核参与 |
|------|------|---------|---------|---------|
| 管道 | 慢 | 父子进程 | 否 | 是 |
| FIFO | 慢 | 本机任意进程 | 否 | 是 |
| 共享内存 | 最快 | 大数据量 | 否 | 仅初始化 |
| 消息队列 | 中 | 结构化消息 | 否 | 是 |
| 信号 | 慢 | 事件通知 | 否 | 是 |
| Socket | 中 | 任意(含网络) | 是 | 是 |
| 信号量 | N/A | 同步控制 | 否 | 是 |

## 相关条目

- [[Thread]]
- [[Concurrency]]
- [[死锁与并发控制]]
- [[Scheduling]]
- [[ProcessManagement]]
