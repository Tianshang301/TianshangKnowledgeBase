# Linux 内核基础 (Linux Kernel Fundamentals)

## 1. 内核架构 (Kernel Architecture)

### 单内核 vs 微内核

```
单内核 (Monolithic Kernel)         微内核 (Microkernel)
┌──────────────────────┐          ┌──────────────────────┐
│     用户空间          │          │     用户空间          │
├──────────────────────┤          ├──────────────────────┤
│  ┌────────────────┐  │          │  ┌────────────────┐  │
│  │   系统调用接口   │  │          │  │  IPC客户端      │  │
│  ├────────────────┤  │          │  ├────────────────┤  │
│  │ 文件系统       │  │          │  │ 文件系统(用户)   │  │
│  │ 内存管理       │  │          │  ├────────────────┤  │
│  │ 进程调度       │  │          │  │ 设备驱动(用户)   │  │
│  │ 设备驱动       │  │          │  ├────────────────┤  │
│  │ 网络栈         │  │          │  │  ...           │  │
│  │ ...            │  │          └──┴───────┬────────┘  │
│  └────────────────┘  │                     │ IPC       │
│      内核空间        │          ┌──────────┴────────┐  │
└──────────────────────┘          │ 微内核(最小化)     │   │
                                  │ 调度、IPC、VM      │  │
                                  └───────────────────┘  │
                                       内核空间           │
                                  └──────────────────────┘
```

| 特性 | Linux (单内核) | Minix (微内核) |
|------|---------------|----------------|
| 性能 | 高(函数调用) | 低(IPC通信) |
| 模块化 | 可加载模块 | 天生模块化 |
| 调试 | 难(大内核) | 易(各组件独立) |
| 稳定性 | 驱动崩溃→内核崩溃 | 驱动崩溃→可重启 |
| 代码量 | ~3千万行 | ~1万行 |

### Linux 内核模块 (LKM)

```c
// hello.c - 最简单的内核模块
#include <linux/module.h>
#include <linux/kernel.h>
#include <linux/init.h>

static int __init hello_init(void) {
    printk(KERN_INFO "Hello, Kernel!\n");
    return 0;
}

static void __exit hello_exit(void) {
    printk(KERN_INFO "Goodbye, Kernel!\n");
}

module_init(hello_init);
module_exit(hello_exit);
MODULE_LICENSE("GPL");
MODULE_DESCRIPTION("A simple kernel module");
```

```bash
make -C /lib/modules/$(uname -r)/build M=$(pwd) modules
insmod hello.ko
rmmod hello
lsmod | grep hello
modinfo hello.ko
```

## 2. 内核空间 vs 用户空间

### 地址空间划分 (x86-64)

```
0xFFFFFFFFFFFFFFFF
    ┌──────────────────┐
    │  内核空间        │
    │  内核代码+数据   │
0xFFFF800000000000
    ├──────────────────┤
0x00007FFFFFFFFFFF
    ├──────────────────┤
    │  用户空间        │
    │  代码+数据+堆    │
    │  栈+环境变量     │
0x0000000000000000
    └──────────────────┘
```

### 系统调用流程

```c
// 用户空间:
ssize_t write(int fd, const void *buf, size_t count) {
    return syscall(SYS_write, fd, buf, count);
}

// 内核空间 - 系统调用表
// arch/x86/entry/syscalls/syscall_64.tbl
// 0   common  read     sys_read
// 1   common  write    sys_write
// 2   common  open     sys_open
// 59  common  execve   sys_execve

// x86-64 syscall 指令流程:
//   mov rax, SYS_write   ; 系统调用号
//   mov rdi, 1           ; fd = stdout
//   mov rsi, buf
//   mov rdx, count
//   syscall              ; → entry_SYSCALL_64 → sys_call_table[rax]
```

## 3. 进程管理

### task_struct 关键字段

```c
// include/linux/sched.h (简化)
struct task_struct {
    pid_t                   pid;            // 进程ID
    pid_t                   tgid;           // 线程组ID
    struct task_struct      *real_parent;
    struct task_struct      *parent;
    struct list_head        children;
    struct list_head        sibling;

    struct sched_entity     se;             // CFS调度实体
    unsigned int            policy;
    int                     prio;
    int                     static_prio;

    volatile long           state;          // TASK_RUNNING等
    int                     exit_state;

    struct mm_struct        *mm;            // 用户地址空间
    struct mm_struct        *active_mm;
    struct fs_struct        *fs;
    struct files_struct     *files;
    struct signal_struct    *signal;

    const struct cred       *cred;
    struct nsproxy          *nsproxy;

    u64                     utime;
    u64                     stime;
};
```

### do_fork() 流程

```c
long do_fork(unsigned long clone_flags, unsigned long stack_start,
             unsigned long stack_size, int __user *parent_tidptr,
             int __user *child_tidptr) {
    struct task_struct *p;

    p = dup_task_struct(current);           // 分配task_struct
    if (clone_flags & CLONE_VM)
        p->mm = current->mm;               // 共享地址空间(线程)
    else
        copy_mm(clone_flags, p);           // 写时复制

    sched_fork(clone_flags, p);
    copy_thread_tls(clone_flags, stack_start, stack_size, p, tls);
    wake_up_new_task(p);
    return p->pid;
}
```

**clone_flags:**

| 标志 | 含义 | fork | vfork | pthread |
|------|------|------|-------|---------|
| CLONE_VM | 共享地址空间 | ✗ | ✗ | ✓ |
| CLONE_FILES | 共享文件描述符 | ✗ | ✓ | ✓ |
| CLONE_SIGHAND | 共享信号处理 | ✗ | ✗ | ✓ |
| CLONE_THREAD | 同线程组 | ✗ | ✗ | ✓ |

## 4. 内存管理

### 4.1 伙伴系统 (Buddy System)

```c
// mm/page_alloc.c
struct page *alloc_pages(gfp_t gfp_mask, unsigned int order);
// order=0→4KB, order=1→8KB, ..., order=10→4MB

void free_pages(struct page *page, unsigned int order);
```

**机制:**
- 空闲块按2^order页分组到free_area[order]链表
- 分配: 从free_area[order]取, 若无则从上级分裂
- 释放: 检查伙伴是否空闲, 是则合并

```
分配2页(order=1):
free_area[0]: [页0] [页2]    free_area[1]: []
free_area[2]: [页0-3]

从order=2分裂出order=1: 页0-1返回, 页2-3加入free_area[1]
```

### 4.2 SLUB 分配器

```c
// 系统预定义slab缓存 (cat /proc/slabinfo)
// task_struct ~3KB  |  mm_struct ~1KB
// inode_cache ~1KB  |  dentry_cache ~200B

void *kmalloc(size_t size, gfp_t flags);
void kfree(const void *objp);

struct kmem_cache *kmem_cache_create(const char *name, size_t size, ...);
void *kmem_cache_alloc(struct kmem_cache *s, gfp_t flags);
```

### 4.3 VMA (Virtual Memory Area)

```
进程地址空间:
┌─────────────────┐ 0x00000000
│  代码段 (.text)  │  VMA: [r-xp]
├─────────────────┤
│  数据段 (.data)  │  VMA: [rw-p]
├─────────────────┤
│  堆 (heap)      │  VMA: [rw-p]
├─────────────────┤
│  mmap区域       │  VMA: [rw-p] (共享库)
├─────────────────┤
│  栈 (stack)     │  VMA: [rw-p]
├─────────────────┤
│  内核空间       │  (用户态不可访问)
└─────────────────┘ 0xFFFFFFFFFFFFFFFF
```

```c
// include/linux/mm_types.h
struct vm_area_struct {
    unsigned long           vm_start;
    unsigned long           vm_end;
    struct mm_struct        *vm_mm;
    pgprot_t                vm_page_prot;
    unsigned long           vm_flags;
    struct rb_node          vm_rb;
    struct file             *vm_file;
    unsigned long           vm_pgoff;
};
```

**缺页处理流程:**
```
do_page_fault()
    ├── 地址在VMA内?  → 继续, 否则 → SIGSEGV
    ├── 页表项=0?     → demand paging
    ├── 写保护页?     → copy-on-write
    └── 匿名页?       → 分配零页
```

## 5. 文件系统

### 5.1 VFS (Virtual File System)

```
系统调用 ↓
┌─────────────────────────────────────┐
│ VFS 层                              │
│ struct super_block / inode / dentry │
│ / file                              │
├─────────────────────────────────────┤
│ ext4    btrfs    xfs    tmpfs       │
├─────────────────────────────────────┤
│ 块层 (Block Layer)                  │
├─────────────────────────────────────┤
│ 设备驱动                            │
└─────────────────────────────────────┘
```

### 5.2 VFS 关键数据结构

```c
struct super_block {
    dev_t               s_dev;
    unsigned long       s_blocksize;
    struct file_system_type *s_type;
    struct dentry       *s_root;
    void                *s_fs_info;
};

struct inode {
    umode_t             i_mode;
    uid_t               i_uid;
    gid_t               i_gid;
    loff_t              i_size;
    struct timespec64   i_atime, i_mtime, i_ctime;
    unsigned long       i_ino;
    unsigned int        i_nlink;
};

struct file {
    struct path         f_path;
    struct inode        *f_inode;
    const struct file_operations *f_op;
    loff_t              f_pos;
    unsigned int        f_flags;
};

struct dentry {
    struct qstr         d_name;
    struct inode        *d_inode;
    struct dentry       *d_parent;
    struct list_head    d_subdirs;
};
```

### 5.3 procfs & sysfs

```bash
# /proc - 进程和内核信息
cat /proc/cpuinfo
cat /proc/meminfo
cat /proc/version
cat /proc/1/maps

# /sys - 设备和驱动信息
ls /sys/class/
cat /sys/block/sda/size
cat /sys/class/net/eth0/address
```

## 6. 设备驱动

### 三种设备类型

| 类型 | 文件类型 | 操作接口 |
|------|---------|---------|
| 字符设备 | c | open/read/write/ioctl |
| 块设备 | b | open/read/write/mmap |
| 网络设备 | 无 | socket/send/recv |

### 字符设备驱动框架

```c
#include <linux/module.h>
#include <linux/fs.h>
#include <linux/cdev.h>
#include <linux/slab.h>
#include <linux/uaccess.h>

#define DEVICE_NAME "chardev"
#define BUFFER_SIZE 1024

struct chardev_dev {
    struct cdev cdev;
    char buffer[BUFFER_SIZE];
    size_t size;
};

static struct chardev_dev *devp;
static int major;

static int chardev_open(struct inode *inode, struct file *file) {
    struct chardev_dev *dev = container_of(inode->i_cdev,
                              struct chardev_dev, cdev);
    file->private_data = dev;
    return 0;
}

static ssize_t chardev_read(struct file *file, char __user *buf,
                            size_t count, loff_t *ppos) {
    struct chardev_dev *dev = file->private_data;
    if (*ppos >= dev->size) return 0;
    if (count > dev->size - *ppos) count = dev->size - *ppos;
    if (copy_to_user(buf, dev->buffer + *ppos, count))
        return -EFAULT;
    *ppos += count;
    return count;
}

static ssize_t chardev_write(struct file *file, const char __user *buf,
                             size_t count, loff_t *ppos) {
    struct chardev_dev *dev = file->private_data;
    if (count > BUFFER_SIZE - *ppos) count = BUFFER_SIZE - *ppos;
    if (copy_from_user(dev->buffer + *ppos, buf, count))
        return -EFAULT;
    *ppos += count;
    if (dev->size < *ppos) dev->size = *ppos;
    return count;
}

static const struct file_operations fops = {
    .owner   = THIS_MODULE,
    .open    = chardev_open,
    .read    = chardev_read,
    .write   = chardev_write,
};

static int __init chardev_init(void) {
    dev_t dev_num;
    alloc_chrdev_region(&dev_num, 0, 1, DEVICE_NAME);
    major = MAJOR(dev_num);
    devp = kzalloc(sizeof(struct chardev_dev), GFP_KERNEL);
    cdev_init(&devp->cdev, &fops);
    devp->cdev.owner = THIS_MODULE;
    cdev_add(&devp->cdev, dev_num, 1);
    pr_info("chardev: registered, major=%d\n", major);
    return 0;
}

static void __exit chardev_exit(void) {
    dev_t dev_num = MKDEV(major, 0);
    cdev_del(&devp->cdev);
    kfree(devp);
    unregister_chrdev_region(dev_num, 1);
    pr_info("chardev: unregistered\n");
}

module_init(chardev_init);
module_exit(chardev_exit);
MODULE_LICENSE("GPL");
```

```bash
mknod /dev/chardev c 240 0
echo "Hello" > /dev/chardev
cat /dev/chardev
```

## 7. 内核调试

### 7.1 printk

```c
#define KERN_EMERG    "<0>"   // 系统不可用
#define KERN_ALERT    "<1>"   // 必须立即处理
#define KERN_CRIT     "<2>"   // 严重错误
#define KERN_ERR      "<3>"   // 错误
#define KERN_WARNING  "<4>"   // 警告
#define KERN_NOTICE   "<5>"   // 普通但重要
#define KERN_INFO     "<6>"   // 信息
#define KERN_DEBUG    "<7>"   // 调试

printk(KERN_INFO "PID %d: file opened\n", current->pid);
pr_info("Module loaded\n");
pr_err("Error occurred: %d\n", ret);
pr_debug("Debug info\n");   // 需定义DEBUG
```

```bash
dmesg -w                     # 实时查看内核日志
dmesg | tail -20             # 查看最后20条
echo 8 > /proc/sys/kernel/printk  # 设置日志级别
```

### 7.2 ftrace (Function Tracer)

```bash
# 挂载tracefs
mount -t tracefs tracefs /sys/kernel/tracing

# 启用函数跟踪
echo function > /sys/kernel/tracing/current_tracer
echo do_fork > /sys/kernel/tracing/set_ftrace_filter
echo 1 > /sys/kernel/tracing/tracing_on
# 执行操作...
cat /sys/kernel/tracing/trace   # 查看跟踪结果

# 关闭
echo 0 > /sys/kernel/tracing/tracing_on
```

### 7.3 kgdb (Kernel GDB)

```bash
# 内核配置 (需编译)
CONFIG_KGDB=y
CONFIG_KGDB_SERIAL_CONSOLE=y

# 启动时启用
kgdboc=ttyS0,115200 kgdbwait

# 在另一台机器上
gdb vmlinux
(gdb) target remote /dev/ttyS0
(gdb) continue
```

### 7.4 其他调试方法

| 方法 | 用途 | 命令/工具 |
|------|------|-----------|
| oops/panic | 内核崩溃分析 | kdump + crash |
| perf | 性能分析 | perf top / perf record |
| strace | 跟踪系统调用 | strace -p PID |
| ltrace | 跟踪库函数 | ltrace ./program |
| SystemTap | 动态跟踪 | stap script.stp |
| eBPF | 可编程内核观测 | bpftrace, bcc |

## 8. 内核编译

```bash
# 下载内核源码
wget https://cdn.kernel.org/pub/linux/kernel/v6.x/linux-6.7.tar.xz
tar xf linux-6.7.tar.xz
cd linux-6.7

# 配置
make menuconfig           # 基于ncurses的配置界面
make defconfig            # 默认配置
make localmodconfig       # 基于当前系统模块的最小配置

# 编译
make -j$(nproc)           # 编译内核和模块
make modules              # 仅编译模块

# 安装
make modules_install      # 安装模块到 /lib/modules/
make install              # 安装内核到 /boot/

# 更新grub
update-grub               # Debian/Ubuntu
grub2-mkconfig -o /boot/grub2/grub.cfg  # RHEL/CentOS
```

**内核源码目录结构:**

| 目录 | 内容 |
|------|------|
| arch/ | 体系结构相关 (x86, arm, riscv...) |
| block/ | 块设备层 |
| crypto/ | 加密API |
| drivers/ | 设备驱动 |
| fs/ | 文件系统 |
| include/ | 头文件 |
| init/ | 初始化代码 |
| ipc/ | 进程间通信 |
| kernel/ | 核心功能(调度、信号、时间...) |
| lib/ | 库函数 |
| mm/ | 内存管理 |
| net/ | 网络协议栈 |
| scripts/ | 编译脚本 |
| security/ | 安全模块(SELinux, AppArmor) |
| sound/ | 音频子系统 |
| tools/ | 用户空间工具 |
| usr/ | initramfs生成 |
| virt/ | KVM虚拟化 |

## 相关条目

- [[ProcessManagement]]
- [[MemoryManagement]]
- [[FileSystems]]
- [[IO]]
- [[Scheduling]]
