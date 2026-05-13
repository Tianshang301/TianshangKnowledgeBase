# 嵌入式 Linux

## 一、嵌入式 Linux 概述

嵌入式 Linux 是将 Linux 内核移植到资源受限的嵌入式设备上的操作系统解决方案。

| 对比维度 | 桌面 Linux | 嵌入式 Linux | RTOS |
|---------|-----------|-------------|------|
| 硬件资源 | 充足（GB 级内存） | 有限（MB 级内存） | 极少（KB 级） |
| 实时性 | 非实时 | 可配置（PREEMPT_RT） | 硬实时 |
| 文件系统 | 完整 | 精简（squashfs, UBIFS） | 通常无 |
| 用户界面 | GUI 桌面 | 可选（Qt, LVGL） | 无或简单 |
| 启动时间 | 数十秒 | 秒级 | 毫秒级 |
| 典型硬件 | x86 PC | ARM, RISC-V, MIPS | MCU |

## 二、构建系统

### Yocto Project

Yocto 是高度可定制的嵌入式 Linux 构建系统，使用 BitBake 构建引擎。

核心概念：
- **Recipe**（`.bb`）：描述如何构建软件包
- **Layer**：组织 recipe 的层级结构
- **Poky**：Yocto 的参考发行版
- **Machine**：目标硬件配置

```
meta-myboard/
├── conf/
│   ├── machine/myboard.conf
│   └── layer.conf
├── recipes-example/
│   └── hello/
│       └── hello_1.0.bb
└── recipes-core/
    └── images/
        └── my-image.bb
```

### Buildroot

Buildroot 使用 Kconfig 配置系统，通过 Makefile 构建。

| 特性 | Yocto | Buildroot |
|------|-------|-----------|
| 学习曲线 | 陡峭 | 较平缓 |
| 构建时间 | 很长（数小时） | 较短（数十分钟） |
| 可定制性 | 极高 | 中等 |
| 包数量 | 10000+ | 2000+ |
| 二进制包支持 | 有限 | 支持 |
| 企业使用 | 广泛 | 中小项目 |

## 三、启动流程

```
Boot ROM → Bootloader (U-Boot) → Kernel → Device Tree → init → Application
```

### 1. Bootloader - U-Boot

U-Boot 是嵌入式 Linux 最常用的 bootloader，支持多种架构和存储介质。

```
# U-Boot 常用命令
bootm          # 启动内核
tftp           # TFTP 下载
ext4load       # 从 ext4 文件系统加载
setenv/printenv # 环境变量
bootargs       # 内核启动参数
```

### 2. 内核

内核从 bootloader 接收设备树和启动参数，完成硬件初始化、驱动加载、挂载根文件系统。

### 3. 设备树（Device Tree）

设备树描述硬件信息，使内核与硬件配置解耦。

**DTS（Device Tree Source）** $\to$ **DTC（编译器）** $\to$ **DTB（Device Tree Blob）**

```dts
/dts-v1/;
/ {
    model = "MyBoard";
    compatible = "vendor,myboard";

    memory@80000000 {
        device_type = "memory";
        reg = <0x80000000 0x10000000>;
    };

    uart0: serial@10000000 {
        compatible = "ns16550a";
        reg = <0x10000000 0x100>;
        interrupts = <0 33 4>;
        clock-frequency = <24000000>;
    };
};
```

### 4. init 系统

| init 系统 | 特点 | 适用场景 |
|-----------|------|---------|
| BusyBox init | 轻量、简单 | 极小系统 |
| systemd | 功能丰富、并行启动 | 功能完整的系统 |

## 四、内核配置

```bash
make menuconfig          # 交互式配置内核
make modules             # 编译内核模块
make zImage              # 编译压缩内核
make dtbs                # 编译设备树
```

**内核模块**：动态加载的驱动，使用 `insmod`/`rmmod`/`modprobe` 管理。

### 驱动开发

```c
// 字符设备驱动模板
static struct file_operations fops = {
    .open = my_open,
    .read = my_read,
    .write = my_write,
    .release = my_release,
};

static int __init my_init(void) {
    register_chrdev(major, "mydev", &fops);
    return 0;
}

module_init(my_init);
module_exit(my_exit);
MODULE_LICENSE("GPL");
```

## 五、根文件系统

| 文件系统类型 | 特点 | 适用场景 |
|------------|------|---------|
| SquashFS | 只读、高压缩比 | 根文件系统 |
| UBIFS | 闪存优化、磨损均衡 | NAND Flash |
| ext4 | 功能完整 | SD 卡、eMMC |
| JFFS2 | 闪存文件系统 | 旧版 NAND |
| initramfs | 内存文件系统 | 早期启动 |

**C 库选择**：

| C 库 | 大小 | 性能 | 兼容性 |
|------|------|------|--------|
| glibc | 大 | 高 | 最好 |
| musl | 小 | 中 | 好 |
| uClibc-ng | 极小 | 中 | 部分受限 |

## 六、交叉编译

嵌入式开发通常在 x86 主机上编译目标平台的 ARM/RISC-V 代码。

```bash
# 使用 Linaro 工具链
export CROSS_COMPILE=aarch64-linux-gnu-
export CC=${CROSS_COMPILE}gcc
export ARCH=arm64

${CC} -o hello hello.c
```

### CMake 交叉编译工具链文件

```cmake
set(CMAKE_SYSTEM_NAME Linux)
set(CMAKE_SYSTEM_PROCESSOR arm)
set(CMAKE_C_COMPILER arm-linux-gnueabihf-gcc)
set(CMAKE_FIND_ROOT_PATH /path/to/sysroot)
set(CMAKE_FIND_ROOT_PATH_MODE_PROGRAM NEVER)
```

**Sysroot** 包含目标系统的库和头文件，确保编译链接使用正确的版本。

## 七、实时性

标准 Linux 的调度延迟不可预测。**PREEMPT_RT** 补丁将 Linux 变为硬实时系统。

| 特性 | 标准内核 | PREEMPT_RT |
|------|---------|------------|
| 抢占点 | 有限 | 几乎所有内核代码 |
| 中断线程化 | 部分 | 全部 |
| 自旋锁 | 不可抢占 | 可抢占 |
| 最坏延迟 | ~10 ms | ~50 $\mu$s |
| 适用场景 | 通用 | 工业控制、音频 |

## 八、调试工具

| 工具 | 用途 | 层级 |
|------|------|------|
| JTAG | 硬件调试、单步执行 | 硬件 |
| gdb/gdbserver | 远程软件调试 | 应用 |
| kgdb | 内核调试 | 内核 |
| strace | 系统调用追踪 | 应用 |
| perf | 性能分析、采样 | 内核/应用 |
| ftrace | 内核函数追踪 | 内核 |
| dmesg | 内核日志 | 内核 |
| Valgrind | 内存检测 | 应用 |

```bash
# strace 追踪程序系统调用
strace -p PID
strace -e open,read ./program

# perf 采样分析
perf record -a -g sleep 10
perf report

# ftrace 追踪内核函数
echo function > /sys/kernel/debug/tracing/current_tracer
echo do_sys_open > /sys/kernel/debug/tracing/set_ftrace_filter
cat /sys/kernel/debug/tracing/trace
```

## 相关条目

- [[05_ComputerScience/OperatingSystems/Linux/INDEX|Linux]]
- [[RTOS]]
- [[Arduino]]
- [[RaspberryPi]]
- DeviceDrivers

## 参考资源

- [Yocto Project 文档](https://docs.yoctoproject.org/)
- [Buildroot 用户手册](https://buildroot.org/docs.html)
- 《Mastering Embedded Linux Programming》（Chris Simmonds）
- [Linux 内核文档 - Device Tree](https://www.kernel.org/doc/html/latest/devicetree/)
- [Bootlin ELinux 文档](https://bootlin.com/docs/)
