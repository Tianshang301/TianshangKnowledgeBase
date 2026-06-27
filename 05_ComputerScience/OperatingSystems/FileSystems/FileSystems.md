---
aliases: [FileSystems]
tags: ['OperatingSystems', 'FileSystems', 'FileSystems']
created: 2026-05-16
updated: 2026-05-13
---

# 文件系统详解 (File System)

## 一、文件概念 (File Concepts)

文件是操作系统中信息存储的基本逻辑单元。

### 文件属性与操作

| 属性 | 含义 |
|------|------|
| **Name** | 文件名，供用户使用 |
| **Path** | 文件路径，定位文件位置 |
| **Identifier** | 文件系统唯一标识（如 inode 号） |
| **Attributes** | 权限、时间戳、大小等 |
| **Operations** | create, open, read, write, close, delete |

### 文件路径

| 路径类型 | 示例 | 说明 |
|---------|------|------|
| **绝对路径** | `/home/user/doc.txt` | 从根目录开始 |
| **相对路径** | `../doc.txt` | 相对于当前工作目录 |
| **硬链接** | 同一 inode 的不同文件名 | 不能跨文件系统 |
| **符号链接** | 指向另一路径的指针 | 可跨文件系统，可指向目录 |

## 二、目录结构 (Directory Structures)

| 结构 | 描述 | 优点 | 缺点 |
|------|------|------|------|
| **单级** | 所有文件在同一目录 | 简单 | 命名冲突，无法分组 |
| **两级** | 每个用户独立目录 | 隔离用户 | 用户内仍无法分组 |
| **树形** | 递归嵌套目录 | 分组能力强 | 共享不便 |
| **无环图** | 目录+链接 | 支持共享 | 需管理引用计数 |
| **通用图** | 任意链接 | 最灵活 | 需检测循环 |

```
树形目录示例：
/
├── bin/
│   ├── bash
│   └── ls
├── home/
│   ├── user1/
│   │   ├── docs/
│   │   └── projects/
│   └── user2/
├── etc/
│   ├── passwd
│   └── fstab
└── usr/
    ├── lib/
    └── local/
```

## 三、文件分配方法 (File Allocation Methods)

### 3.1 连续分配 (Contiguous)

```
文件 A: 逻辑块0-3 → 物理块100-103
文件 B: 逻辑块0-1 → 物理块104-105

┌─────────────────────────────────────┐
│ A0 │ A1 │ A2 │ A3 │ B0 │ B1 │ ... │
└─────────────────────────────────────┘
 100  101  102  103  104  105
```

**缺点**：外部碎片，文件难扩展。

### 3.2 链接分配 (Linked)

目录项仅存起始块指针，每块指向下一块。

| 优点 | 缺点 |
|------|------|
| 无外部碎片 | 随机访问慢（需遍历） |
| 易扩展 | 指针占用数据空间 |
| **FAT 表改进**：所有指针集中到 FAT 表 | FAT 表需常驻内存 |

### 3.3 索引分配 (Indexed)

文件的所有块指针集中在一个索引块中。

```
文件 A 索引块:
┌────┬────┬────┬────┬────┐
│ 40 │ 72 │ 15 │ 63 │EOF │
└─┬──┴──┬─┴──┬─┴──┬─┴────┘
  ↓     ↓    ↓    ↓
数据块 数据块 数据块 数据块
```

### 3.4 混合方式对比

| 方法 | 随机访问 | 空间效率 | 扩展性 |
|------|---------|---------|--------|
| 连续 | $O(1)$ | 无元数据开销 | 差 |
| 链接 | $O(n)$ | 极小指针开销 | 好 |
| FAT | $O(1)$（FAT 在内存） | FAT 表开销 | 好 |
| 索引 | $O(1)$ | 索引块开销 | 好 |
| Extent | $O(\log n)$ | 对连续块极高效 | 好 |

## 四、空闲空间管理 (Free Space Management)

| 方法 | 原理 | 空间效率 | 适用场景 |
|------|------|---------|---------|
| **位图 (Bitmap)** | 每块1位标记空闲/已用 | 高（1/4096） | 通用 |
| **空闲链表 (Free List)** | 链表串联空闲块 | 中 | 简单系统 |
| **组链接 (Group Chain)** | 组式空闲块管理 | 高 | Unix FFS |
| **B 树** | 用 B 树索引空闲区间 | 很高 | ext4, XFS |

```c
// 位图操作示例
#define BLOCK_SIZE 4096
#define BLOCKS 1048576  // 4GB 磁盘

unsigned char bitmap[BLOCKS / 8];  // 128KB 位图

int find_free_block() {
    for (int i = 0; i < BLOCKS / 8; i++) {
        if (bitmap[i] != 0xFF) {  // 有0位
            for (int j = 0; j < 8; j++) {
                if (!(bitmap[i] & (1 << j))) {
                    int block = i * 8 + j;
                    bitmap[i] |= (1 << j);  // 标记已用
                    return block;
                }
            }
        }
    }
    return -1;  // 无空闲块
}
```

## 五、磁盘调度 (Disk Scheduling)

### 调度算法对比

磁盘寻道时间模型：

$$ T_{\text{seek}}(d) = a + b \cdot d $$

其中 $a$ 为启动时间，$b$ 为每磁道移动时间，$d$ 为磁道数。总访问时间 = $T_{\text{seek}} + T_{\text{rotation}} + T_{\text{transfer}}$。

| 算法 | 描述 | 平均寻道 | 优缺点 |
|------|------|---------|--------|
| **FCFS** | 按请求顺序 | 高 | 公平但寻道距离大 |
| **SSTF** | 选最近请求 | 较低 | 快但可能饥饿 |
| **SCAN (电梯)** | 单向扫描到边缘 | 中等 | 两端等待不均 |
| **C-SCAN** | 单向到边缘后返回 | 中等 | 等待时间更均匀 |
| **LOOK** | SCAN 改进，到最后一个请求即转向 | 较低 | 减少无效扫描 |
| **C-LOOK** | C-SCAN+LOOK | 最低 | 综合最优 |

```
请求队列: 98, 183, 37, 122, 14, 124, 65, 67
起始位置: 53

FCFS: 53→98→183→37→122→14→124→65→67  (640磁道)
SSTF: 53→65→67→37→14→98→122→124→183 (236磁道)
SCAN(↑): 53→65→67→98→122→124→183→199→37→14→0 (345磁道)
C-SCAN(↑): 53→65→67→98→122→124→183→199→0→14→37 (382磁道)
LOOK(↑): 53→65→67→98→122→124→183→37→14 (299磁道)
```

## 六、RAID 级别 (RAID Levels)

| 级别 | 最少磁盘 | 冗余 | 容量利用率 | 读性能 | 写性能 | 容错 |
|------|---------|------|-----------|-------|-------|------|
| **RAID 0** | 2 | 无 | 100% | 高 | 高 | 无 |
| **RAID 1** | 2 | 镜像 | 50% | 高 | 中 | 1盘 |
| **RAID 5** | 3 | 奇偶校验 | $(N-1)/N$ | 高 | 中 | 1盘 |
| **RAID 6** | 4 | 双重校验 | $(N-2)/N$ | 高 | 低 | 2盘 |
| **RAID 10** | 4 | 镜像+条带 | 50% | 最高 | 最高 | 每组1盘 |

```
RAID 0 (条带):         RAID 1 (镜像):         RAID 5 (分布式奇偶校验):
Disk0  Disk1           Disk0  Disk1           Disk0 Disk1 Disk2
┌────┬────┐            ┌────┬────┐            ┌────┬────┬────┐
│ A0 │ A1 │            │ A0 │ A0 │            │ A0 │ A1 │ P0 │
├────┼────┤            ├────┼────┤            ├────┼────┼────┤
│ A2 │ A3 │            │ A1 │ A1 │            │ B0 │ P1 │ B1 │
├────┼────┤            ├────┼────┤            ├────┼────┼────┤
│ A4 │ A5 │            │ A2 │ A2 │            │ P2 │ C0 │ C1 │
└────┴────┘            └────┴────┘            └────┴────┴────┘
```

## 七、文件系统类型 (File System Types)

| 特性 | FAT32 | NTFS | ext4 | APFS | ZFS |
|------|-------|------|------|------|-----|
| 最大文件 | 4GB | 16EB | 16TB | 8EB | 16EB |
| 最大卷 | 2TB | 256TB | 1EB | 大量 | 256ZB |
| 日志 | ✗ | ✓ | ✓ | ✓ | ✓ (CoW) |
| 压缩 | ✗ | ✓ | ✗ | ✓ | ✓ |
| 快照 | ✗ | ✗ | ✗ | ✓ | ✓ |
| 校验和 | ✗ | ✗ | ✗ | ✓ | ✓ |
| 跨平台 | 优 | Windows | Linux | macOS | 跨平台 |

## 八、Inode 结构

inode 是文件系统元数据的核心，存储文件属性而非文件名。

$$ \text{inode} = \langle \text{权限, 大小, 时间戳, 块指针, } \dots \rangle $$

- 文件名存储在目录项中，目录项通过 inode 号指向 inode
- 支持直接块、间接块、二级间接块、三级间接块

```c
struct ext4_inode {
    __u16  i_mode;         // 文件类型和权限
    __u16  i_uid;
    __u32  i_size_lo;      // 文件大小低位
    __u32  i_atime;        // 访问时间
    __u32  i_ctime;        // 状态变更时间
    __u32  i_mtime;        // 修改时间
    __u32  i_dtime;        // 删除时间
    __u16  i_gid;
    __u16  i_links_count;  // 硬链接计数
    __u32  i_blocks_lo;    // 512字节块数
    __u32  i_flags;
    __u32  i_block[15];    // extent 树根节点或块指针
    // ...
};
```

### ext4 extent 树

```
inode.i_block[0..3] → extent header + 4个 extent 条目
每个 extent: 逻辑起始块, 物理起始块, 长度(连续块数)

extent header (12 bytes):
  eh_magic, eh_entries, eh_max, eh_depth

extent 条目 (12 bytes each):
  ee_block (逻辑块号), ee_len (块数), ee_start_hi, ee_start_lo
```

## 九、日志 (Journaling)

### 写前日志 (Write-Ahead Logging)

在写入数据前先将操作记录到日志，崩溃后恢复。

```
日志记录格式：
[JFS_COMMIT | 事务 ID | 元数据块 | 校验和]
```

### ext3/4 日志模式

| 模式 | 日志内容 | 安全性 | 性能 |
|------|---------|-------|------|
| **writeback** | 仅元数据（数据可能乱序） | 低 | 最快 |
| **ordered** | 仅元数据，但数据先写入磁盘 | 中 | 较快 |
| **data** | 元数据+数据都写入日志 | 高 | 最慢 |

## 十、VFS 与 FUSE

### VFS (Virtual File System)

```
系统调用接口 (open, read, write...)
        ↓
    VFS 层 (统一文件模型)
        ↓
   ┌───┼───┬───┐
   │   │   │   │
  ext4 NTFS FAT32 FUSE
```

VFS 定义通用文件模型（超级块、inode、目录项、文件对象），具体文件系统实现这些接口。

### FUSE (Filesystem in Userspace)

```c
// FUSE 用户态文件系统示例
static int hello_getattr(const char *path, struct stat *stbuf) {
    memset(stbuf, 0, sizeof(struct stat));
    if (strcmp(path, "/") == 0) {
        stbuf->st_mode = S_IFDIR | 0755;
        stbuf->st_nlink = 2;
    } else if (strcmp(path, "/hello.txt") == 0) {
        stbuf->st_mode = S_IFREG | 0444;
        stbuf->st_nlink = 1;
        stbuf->st_size = 13;
    } else {
        return -ENOENT;
    }
    return 0;
}
```

## 十一、存储层次 (Storage Hierarchy)

```
寄存器 (1ns, 1KB)
   ↓
L1 Cache (2ns, 32KB)
   ↓
L2 Cache (10ns, 256KB)
   ↓
L3 Cache (20ns, 8MB)
   ↓
内存 (100ns, 16-512GB)
   ↓
SSD (10μs-100μs, 256GB-2TB)
   ↓
HDD (10ms, 1-20TB)
   ↓
磁带/云存储 (秒级, PB 级)
```

## 相关条目

- Storage
- DiskScheduling
- Inode
- VFS
- Journaling

## 参考资源

- Silberschatz, A., Galvin, P. B., & Gagne, G. *Operating System Concepts* (10th ed.)
- Tanenbaum, A. S., & Bos, H. *Modern Operating Systems* (4th ed.)
- ext4 Wiki: https://ext4.wiki.kernel.org/
- Oracle Solaris ZFS Administration Guide
