---
aliases: [IO]
tags: ['OperatingSystems', 'IO']
created: 2026-05-16
updated: 2026-05-16
---

# I/O 管理详解 (Input/Output Management)

## 1. I/O 硬件 (I/O Hardware)

### 硬件组件

```
                    CPU
                     │
               系统总线(PCIe)
                     │
        ┌────────────┼────────────┐
        │            │            │
   内存控制器     I/O 总线     DMA 控制器
        │            │            │
      内存        ┌──┴──┐      磁盘
                  │    │
              SATA/USB/PCIe 控制器
                   │
               外设(磁盘、键鼠、网卡)
```

| 组件 | 描述 |
|------|------|
| **端口 (Port)** | CPU 与设备通信的接口地址 |
| **总线 (Bus)** | 数据传输通道 (PCIe, SATA, USB) |
| **控制器 (Controller)** | 管理设备的芯片 (南桥, AHCI, NVMe) |
| **设备 (Device)** | 实际外设 (键盘、鼠标、磁盘、网卡) |

### 设备通信方式

| 方式 | 描述 | 示例 |
|------|------|------|
| **I/O 端口** | 专用指令(如 x86 `IN`/`OUT`) | 键盘(端口0x60) |
| **内存映射 I/O** | 设备寄存器映射到内存地址空间 | 显存(VRAM) |
| **混合** | 状态寄存器用端口，数据用 MMIO | 部分 PCIe 设备 |

```c
// x86 I/O 端口操作
#include <sys/io.h>

// 读取键盘状态
unsigned char status = inb(0x64);  // read byte from port 0x64
unsigned char key   = inb(0x60);  // read key data

// 输出到串口
outb('A', 0x3F8);  // write 'A' to COM1
```

## 2. 轮询 vs 中断 vs DMA

### 2.1 轮询 (Polling)

CPU 不断检查设备状态寄存器。

```c
// 轮询示例
void poll_print(char c) {
    // 等待打印机就绪
    while (!(inb(PRINTER_STATUS_PORT) & READY_BIT))
        ;  // 忙等
    outb(c, PRINTER_DATA_PORT);
}
```

**优点:** 简单、可预测
**缺点:** 浪费 CPU 周期（适合高速设备）

### 2.2 中断 (Interrupt)

设备完成操作时向 CPU 发中断信号。

```
CPU                                   设备
 │                                      │
 │ (执行其他程序)                        │
 │                                      │
 │◄───────────────────────── 中断请求 ───┤
 │                                      │
 │ 保存上下文                            │
 │ 执行中断服务程序(ISR)                  │
 │ 恢复上下文                            │
 │                                      │
```

```c
// 中断处理程序示例 (Linux 键盘驱动)
static irqreturn_t keyboard_interrupt(int irq, void *dev_id) {
    unsigned char scancode = inb(0x60);  // 读取扫描码
    // 处理按键事件
    handle_key_event(scancode);
    return IRQ_HANDLED;
}

// 注册中断
request_irq(1,                          // IRQ 1 = 键盘
            keyboard_interrupt,
            IRQF_SHARED,
            "keyboard",
            &keyboard_dev);
```

**中断类型:**
- **可屏蔽中断 (Maskable)**: 可通过`cli`/`sti`控制 (x86)
- **不可屏蔽中断 (NMI)**: 硬件错误、看门狗定时器
- **软中断 (Software Interrupt)**: 系统调用 (int 0x80 / syscall)

### 2.3 DMA (Direct Memory Access)

DMA 控制器直接在设备和内存间传输数据，无需 CPU 逐字节搬运。

```
CPU 请求 DMA 传输:                   DMA 传输过程:
┌──────────┐                     ┌──────────┐
│ CPU      │  ← 1.设置 DMA 控制     │ CPU      │
│          │                     │ (空闲)   │
└──────────┘                     └──────────┘
     │                                │
     ▼                                │
┌──────────┐                     ┌──────────┐
│ DMA Ctrl │  ← 2.开始传输       │ DMA Ctrl │ → 3.总线 → 内存
│          │                     │          │
│ 源: 磁盘 │                     │ 源: 磁盘 │
│ 目标:内存│                     │ 目标:内存│
│ 大小:4KB │                     │ 大小:4KB │
└──────────┘                     └──────────┘
                                      │
                              4.传输完成→中断
                                      │
                                      ▼
                                 ┌──────────┐
                                 │ CPU (处理)│
                                 └──────────┘
```

**DMA 模式:**
- **总线主控 (Bus Mastering)**: 设备直接控制总线

```c
// Linux DMA API (简略)
#include <linux/dma-mapping.h>

dma_addr_t dma_handle;
void *cpu_addr = dma_alloc_coherent(dev, size, &dma_handle, GFP_KERNEL);

// 启动 DMA 传输
device_start_dma(dma_handle, size, direction);

// 等待 DMA 完成(中断处理中)
dma_free_coherent(dev, size, cpu_addr, dma_handle);
```

## 3. I/O 软件层次 (I/O Software Layers)

```
┌──────────────────────────────────┐
│ 用户空间 I/O (stdio, C 库)        │
│ fopen/fread/fwrite/printf/scanf  │
├──────────────────────────────────┤
│ 设备无关操作系统层               │
│ 设备命名、保护、缓冲、缓存、分配  │
│ 通用接口(read/write/ioctl)       │
├──────────────────────────────────┤
│ 设备驱动层 (Device Drivers)      │
│ 每个设备类型对应驱动              │
│ 与设备控制器直接交互              │
├──────────────────────────────────┤
│ 中断处理程序 (Interrupt Handlers)│
│ 响应硬件中断                     │
├──────────────────────────────────┤
│ 硬件 (Hardware)                  │
│ 设备控制器、外设                  │
└──────────────────────────────────┘
```

### 系统调用流程

```
write(fd, buf, count)
        │
        ▼
    sys_write()           ← 系统调用入口 (在 kernel 中)
        │
        ▼
    vfs_write()           ← VFS 层 (文件系统无关)
        │
        ▼
    ext4_file_write()     ← 文件系统层
        │
        ▼
    generic_file_write()  ← 通用文件操作
        │
        ▼
    block layer            ← 块层 (I/O 调度器)
        │
        ▼
    SCSI/ATA 驱动           ← 驱动层
        │
        ▼
    磁盘控制器/硬件        ← 硬件层
```

## 4. 缓冲 (Buffering)

### 4.1 单缓冲 (Single Buffer)

```
设备 → 缓冲区 → 用户进程
```

**优点:** 简单
**缺点:** 处理与传输串行

### 4.2 双缓冲 (Double Buffer)

```
设备 → 缓冲区1 → 用户进程
          ↓
设备 → 缓冲区2

// 缓冲区1被处理时，设备填充缓冲区2
// 交换角色
```

### 4.3 循环缓冲 (Circular Buffer)

```
┌─────────────────────────────────┐
│  ┌──┬──┬──┬──┬──┬──┬──┬──┐     │
│  │  │  │  │  │  │  │  │  │     │
│  └──┴──┴──┴──┴──┴──┴──┴──┘     │
│     ↑          ↑                 │
│   in 指针      out 指针           │
└─────────────────────────────────┘

in: 生产者(设备)写入位置
out: 消费者(进程)读取位置

// 循环队列操作
void put(char c) {
    buffer[in] = c;
    in = (in + 1) % BUFFER_SIZE;
}

char get() {
    char c = buffer[out];
    out = (out + 1) % BUFFER_SIZE;
    return c;
}
```

### 缓冲的目的

1. **速度匹配**: 设备与内存速度差异
2. **数据聚合**: 合并多次小 I/O 为一次大 I/O
3. **解耦**: 生产者与消费者无需直接同步

## 5. 缓存 (Caching)

通常使用**页缓存 (Page Cache)**:

```
应用程序
    │
    ▼
write()
    │
    ▼
┌──────────┐    延迟写(delayed write)
│页缓存    │─────────────────────► 磁盘
│ (内存中) │
└──────────┘
    │
    ▼
read() (命中: 直接返回, 无需磁盘 I/O)

// sync 命令强制刷缓存
sync      # 刷所有缓存
fsync(fd) # 刷单个文件
```

**写策略:**

| 策略 | 描述 | 优点 | 缺点 |
|------|------|------|------|
| **Write-Through** | 同时写缓存和磁盘 | 数据安全 | 速度慢 |
| **Write-Back** | 只写缓存，延迟写磁盘 | 速度快 | 断电丢数据 |
| **Write-Around** | 绕过缓存直接写磁盘 | 不污染缓存 | 对大文件好 |

## 6. 假脱机 (Spooling)

同时在线外围操作 (Simultaneous Peripheral Operation Online)。

**打印机假脱机示例:**

```
应用程序1 → 假脱机目录/spool/printer/job1
应用程序2 → 假脱机目录/spool/printer/job2
应用程序3 → 假脱机目录/spool/printer/job3
                                    ↓
                              打印机守护进程(lpd)
                                    ↓
                                 打印机
```

```bash
# Linux 打印系统
lp file.txt              # 提交打印任务
lpq                      # 查看打印队列
lprm job_id              # 删除打印任务
lpc status               # 查看打印机状态

# 假脱机目录
ls -l /var/spool/cups/   # CUPS 打印系统假脱机目录
```

**Spooling vs 缓冲:**

| 特性 | Spooling | Buffering |
|------|----------|-----------|
| 任务数 | 多任务 | 单任务 |
| 存储 | 磁盘 | 内存 |
| 持久性 | 持久 | 临时 |
| 典型设备 | 打印机 | 键盘、磁盘 |

## 7. 磁盘结构 (Disk Structure)

### 机械硬盘 (HDD) 结构

```
             ┌──────────┐
             │  盘片     │  (platter)
             │ ┌──────┐ │
             │ │ 磁道   ││  (track)
             │ │┌────┐ ││
             │ ││扇区 ││ │  (sector, 512B 或4KB)
             │ │└────┘ ││
             │ │       ││
             │ └──────┘ │
             └──────────┘
                 │
            ┌────┴────┐
            │ 磁头    │ (read/write head)
            └─────────┘
```

**柱面 (Cylinder):** 所有盘片相同磁道编号

**磁盘地址:** CHS (Cylinder-Head-Sector) → 现代用 LBA (Logical Block Addressing)

```c
// LBA 到 CHS 转换
void lba_to_chs(int lba, int *c, int *h, int *s) {
    *s = (lba % sectors_per_track) + 1;
    *h = (lba / sectors_per_track) % heads;
    *c = lba / (sectors_per_track * heads);
}
```

## 8. SSD vs HDD 对比

| 特性 | HDD | SSD |
|------|-----|-----|
| 原理 | 磁记录 + 机械旋转 | NAND Flash 电子 |
| 随机读取 | ~100 IOPS | ~100,000 IOPS |
| 顺序读取 | ~200 MB/s | ~7,000 MB/s (PCIe 4.0) |
| 延迟 | 5-15ms | 0.01-0.1ms |
| 功耗 | 6-10W | 2-5W |
| 噪音 | 有(机械运动) | 无 |
| 抗震 | 差 | 好 |
| 寿命 | 几乎无限写入 | 有限写入次数(磨损) |
| 成本/GB | ~$0.02 | ~$0.08 |
| 数据恢复 | 可能(磁残留) | 极难 |

### SSD 特性

- **磨损均衡 (Wear Leveling)**: 均匀分配写入到所有块
- **垃圾回收 (GC)**: 后台清理无效数据块
- **TRIM**: 通知 SSD 哪些页已不再使用
- **OP (Over-Provisioning)**: 预留空间用于 GC 和磨损均衡

```bash
# Linux 查看磁盘信息
hdparm -I /dev/sda       # 查看 HDD/SSD 详细信息
smartctl -a /dev/sda      # 查看 S.M.A.R.T.信息
fstrim -v /               # 手动触发 TRIM(SSD)
```

## 9. 设备驱动程序 (Device Drivers)

### 三种设备类型

| 类型 | 特点 | 示例 | 访问接口 |
|------|------|------|---------|
| **字符设备** | 串行字节流 | 串口、键盘、鼠标 | `read/write` |
| **块设备** | 随机访问数据块 | 磁盘、SSD | `read/write + mmap` |
| **网络设备** | 数据包 | 网卡 | `socket` 接口 |

### Linux 字符设备驱动框架

```c
#include <linux/module.h>
#include <linux/fs.h>

static int my_open(struct inode *inode, struct file *file) {
    pr_info("Device opened\n");
    return 0;
}

static ssize_t my_read(struct file *file, char __user *buf,
                       size_t len, loff_t *off) {
    char data[] = "Hello from kernel!\n";
    size_t size = strlen(data);

    if (*off >= size) return 0;
    if (len > size - *off) len = size - *off;

    copy_to_user(buf, data + *off, len);
    *off += len;
    return len;
}

static struct file_operations fops = {
    .owner = THIS_MODULE,
    .open  = my_open,
    .read  = my_read,
};

static int __init my_init(void) {
    register_chrdev(0, "mydevice", &fops);
    pr_info("Module loaded\n");
    return 0;
}

static void __exit my_exit(void) {
    unregister_chrdev(MAJOR_NUM, "mydevice");
    pr_info("Module unloaded\n");
}

module_init(my_init);
module_exit(my_exit);
MODULE_LICENSE("GPL");
```

### /dev 目录

```bash
# 设备文件类型
crw-rw-rw- 1 root root 1, 3 /dev/null      # c=字符设备, 主号1, 次号3
brw-rw---- 1 root disk 8, 0 /dev/sda        # b=块设备, 主号8, 次号0
```

## 相关条目

- [[FileSystem]]
- [[05_ComputerScience/OperatingSystems/FileSystems/FileSystems|FileSystems]]
- [[Memory]]
- [[LinuxKernel]]
- [[Scheduling]]


