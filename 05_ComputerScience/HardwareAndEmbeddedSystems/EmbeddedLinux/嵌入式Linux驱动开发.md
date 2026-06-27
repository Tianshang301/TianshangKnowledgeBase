---
aliases: [嵌入式 Linux 驱动开发]
tags: ['HardwareAndEmbeddedSystems', 'EmbeddedLinux', '嵌入式 Linux 驱动开发']
---

# 嵌入式 Linux 驱动开发

## 一、Linux 驱动基础

Linux 驱动是内核与硬件设备之间的桥梁，负责设备管理和数据交换。

驱动类型分类：

| 类型 | 特点 | 设备文件 | 示例 |
|------|------|----------|------|
| 字符设备 | 顺序访问，流式 | /dev/xxx | 串口、GPIO |
| 块设备 | 随机访问，块操作 | /dev/xxx | SD 卡、NAND Flash |
| 网络设备 | 数据包收发 | /sys/class/net/eth0 | 以太网、WiFi |
| 杂项设备 | 简化的字符设备 | /dev/xxx | 小器件 |

设备号管理：主设备号标识驱动类型，次设备号标识具体设备。

$$
\text{设备号} = \text{主设备号} \times 256 + \text{次设备号}
$$

## 二、字符设备驱动框架

最简单的字符设备驱动结构：

```c
#include <linux/module.h>
#include <linux/fs.h>
#include <linux/uaccess.h>

#define DEVICE_NAME "my_char_dev"
#define CLASS_NAME "my_class"

static int major;
static struct class *my_class = NULL;

static int device_open(struct inode *inode, struct file *file) {
    printk(KERN_INFO "Device opened\n");
    return 0;
}

static int device_release(struct inode *inode, struct file *file) {
    printk(KERN_INFO "Device closed\n");
    return 0;
}

static ssize_t device_read(struct file *file, char __user *buffer,
                            size_t len, loff_t *offset) {
    char msg[] = "Hello from kernel!\n";
    size_t msg_len = strlen(msg);
    
    if (*offset >= msg_len) return 0;
    if (len > msg_len - *offset)
        len = msg_len - *offset;
    
    if (copy_to_user(buffer, msg + *offset, len))
        return -EFAULT;
    
    *offset += len;
    return len;
}

static ssize_t device_write(struct file *file, const char __user *buffer,
                             size_t len, loff_t *offset) {
    char kbuf[256];
    
    if (len > sizeof(kbuf)) len = sizeof(kbuf);
    
    if (copy_from_user(kbuf, buffer, len))
        return -EFAULT;
    
    kbuf[len] = '\0';
    printk(KERN_INFO "Received: %s\n", kbuf);
    return len;
}

static struct file_operations fops = {
    .owner = THIS_MODULE,
    .open = device_open,
    .release = device_release,
    .read = device_read,
    .write = device_write,
};

static int __init my_init(void) {
    major = register_chrdev(0, DEVICE_NAME, &fops);
    if (major < 0) {
        printk(KERN_ALERT "Failed to register device\n");
        return major;
    }
    
    my_class = class_create(THIS_MODULE, CLASS_NAME);
    device_create(my_class, NULL, MKDEV(major, 0), NULL, DEVICE_NAME);
    
    printk(KERN_INFO "Module loaded with major number %d\n", major);
    return 0;
}

static void __exit my_exit(void) {
    device_destroy(my_class, MKDEV(major, 0));
    class_destroy(my_class);
    unregister_chrdev(major, DEVICE_NAME);
    printk(KERN_INFO "Module unloaded\n");
}

module_init(my_init);
module_exit(my_exit);

MODULE_LICENSE("GPL");
MODULE_AUTHOR("Tianshang KB");
MODULE_DESCRIPTION("Simple character device driver");
```

## 三、设备树（Device Tree）

设备树描述硬件拓扑和资源，避免硬编码：

```dts
/dts-v1/;

/ {
    compatible = "vendor,board";
    
    cpus {
        cpu@0 {
            compatible = "arm,cortex-a7";
            clock-frequency = <1000000000>;
        };
    };
    
    memory@80000000 {
        device_type = "memory";
        reg = <0x80000000 0x10000000>;  // 256MB
    };
    
    my_device: my-device@1c00000 {
        compatible = "vendor,my-device";
        reg = <0x01c00000 0x1000>;
        interrupts = <0 31 4>;
        clocks = <&clkc 15>;
        status = "okay";
    };
    
    leds {
        compatible = "gpio-leds";
        led0 {
            gpios = <&gpio0 12 GPIO_ACTIVE_HIGH>;
            label = "user-led";
        };
    };
};
```

驱动中解析设备树：

```c
static int my_probe(struct platform_device *pdev) {
    struct resource *res;
    void __iomem *base;
    int irq;
    
    res = platform_get_resource(pdev, IORESOURCE_MEM, 0);
    base = devm_ioremap_resource(&pdev->dev, res);
    if (IS_ERR(base))
        return PTR_ERR(base);
    
    irq = platform_get_irq(pdev, 0);
    if (irq < 0)
        return irq;
    
    dev_info(&pdev->dev, "Device probed at %pR, irq=%d\n", res, irq);
    return 0;
}

static const struct of_device_id my_of_match[] = {
    { .compatible = "vendor,my-device" },
    { }
};
MODULE_DEVICE_TABLE(of, my_of_match);

static struct platform_driver my_driver = {
    .probe = my_probe,
    .remove = my_remove,
    .driver = {
        .name = "my_device",
        .of_match_table = my_of_match,
    },
};

module_platform_driver(my_driver);
```

## 四、GPIO 驱动

使用内核 GPIO 子系统：

```c
#include <linux/gpio.h>
#include <linux/gpio/consumer.h>

struct gpio_desc *gpio_led;

static int __init gpio_init(void) {
    int ret;
    
    gpio_led = gpiod_get(NULL, "user-led", GPIOD_OUT_LOW);
    if (IS_ERR(gpio_led)) {
        ret = PTR_ERR(gpio_led);
        pr_err("Failed to get GPIO: %d\n", ret);
        return ret;
    }
    
    gpiod_set_value(gpio_led, 1);  // LED 亮
    pr_info("GPIO LED initialized\n");
    return 0;
}

static void __exit gpio_exit(void) {
    gpiod_set_value(gpio_led, 0);
    gpiod_put(gpio_led);
    pr_info("GPIO LED released\n");
}
```

## 五、中断处理

注册中断处理函数：

```c
#include <linux/interrupt.h>

static irqreturn_t my_irq_handler(int irq, void *dev_id) {
    struct my_device *dev = (struct my_device *)dev_id;
    
    // 读取硬件状态
    unsigned long flags;
    spin_lock_irqsave(&dev->lock, flags);
    
    dev->irq_count++;
    // 处理中断事件
    
    spin_unlock_irqrestore(&dev->lock, flags);
    
    // 唤醒等待队列
    wake_up_interruptible(&dev->wait_queue);
    
    return IRQ_HANDLED;
}

static int request_my_irq(struct platform_device *pdev) {
    int irq, ret;
    
    irq = platform_get_irq(pdev, 0);
    if (irq < 0)
        return irq;
    
    ret = request_irq(irq, my_irq_handler,
                      IRQF_TRIGGER_RISING,
                      "my_device", pdev);
    if (ret)
        dev_err(&pdev->dev, "Failed to request IRQ\n");
    
    return ret;
}
```

## 六、内存与 DMA

DMA（Direct Memory Access）实现高速数据传输：

```c
#include <linux/dmaengine.h>
#include <linux/dma-mapping.h>

static int setup_dma(struct device *dev) {
    dma_addr_t dma_handle;
    void *cpu_addr;
    size_t size = SZ_64K;
    
    // 分配 DMA 缓冲区
    cpu_addr = dma_alloc_coherent(dev, size, &dma_handle, GFP_KERNEL);
    if (!cpu_addr)
        return -ENOMEM;
    
    dev_info(dev, "DMA buffer: cpu=%p dma=%pad size=%zu\n",
             cpu_addr, &dma_handle, size);
    return 0;
}
```

内存操作函数选择：

| 场景 | 函数 | 说明 |
|------|------|------|
| 内核内存分配 | kmalloc / kzalloc | 物理连续 |
| 大块内存 | __get_free_pages | 页对齐 |
| 虚拟连续 | vmalloc | 不保证物理连续 |
| DMA 缓冲区 | dma_alloc_coherent | 一致性内存 |
| 设备内存映射 | ioremap | MMIO 区域 |

## 七、并发与同步

并发控制机制：

```c
// 自旋锁 - 短临界区
spinlock_t my_lock;
spin_lock_init(&my_lock);
spin_lock(&my_lock);
// 临界区代码
spin_unlock(&my_lock);

// 互斥锁 - 可睡眠
struct mutex my_mutex;
mutex_init(&my_mutex);
mutex_lock(&my_mutex);
// 临界区代码
mutex_unlock(&my_mutex);

// 原子操作
atomic_t counter = ATOMIC_INIT(0);
atomic_inc(&counter);
int val = atomic_read(&counter);

// 完成量 - 等待事件完成
struct completion comp;
init_completion(&comp);
wait_for_completion(&comp);
complete(&comp);
```

## 八、驱动的编译与调试

Makefile 示例：

```makefile
obj-m += mydriver.o
mydriver-objs := main.o gpio.o irq.o

KERNEL_DIR ?= /lib/modules/$(shell uname -r)/build
PWD := $(shell pwd)

all:
    $(MAKE) -C $(KERNEL_DIR) M=$(PWD) modules

clean:
    $(MAKE) -C $(KERNEL_DIR) M=$(PWD) clean

install:
    sudo insmod mydriver.ko

remove:
    sudo rmmod mydriver

test:
    sudo dmesg -C
    sudo insmod mydriver.ko
    sudo cat /dev/my_device
    sudo rmmod mydriver
    dmesg
```

调试技巧：

```
1. printk: 内核日志输出，KERN_DEBUG/KERN_INFO/KERN_ERR
2. dev_dbg/dev_info/dev_err: 设备日志宏
3. /sys/kernel/debug: debugfs 接口
4. ftrace: 内核函数追踪
5. kgdb: 内核源码级调试
6. /proc/devices: 查看已注册的设备
7. udevadm: 监控 udev 事件
```

## 相关条目

- [[EmbeddedLinux]]
- [[05_ComputerScience/OperatingSystems/LinuxKernel|LinuxKernel]]
- [[05_ComputerScience/HardwareAndEmbeddedSystems/RaspberryPi/RaspberryPi|RaspberryPi]]
- [[05_ComputerScience/HardwareAndEmbeddedSystems/IoT/IoT|IoT]]
- [[05_ComputerScience/HardwareAndEmbeddedSystems/FPGA/FPGA|FPGA]]

## 参考资源

1. Linux 内核文档：https://www.kernel.org/doc
2. 《Linux 设备驱动程序》（第三版）O'Reilly
3. Linux Foundation 驱动开发指南
4. Bootlin 嵌入式 Linux 文档：https://bootlin.com/docs
5. Free Electron 设备树文档：https://devicetree.org
6. ELinux.org 嵌入式 Linux 维基
7. LWN.net 内核开发新闻

