---
aliases:
  - 中断深入
  - Interrupt Deep Dive
  - 中断机制
  - Interrupt Handling
tags:
  - operating-system
  - interrupt
  - x86
  - arm
  - real-time
  - system-programming
created: 2026-06-27
updated: 2026-06-27
---

# 中断深入

## 1. 中断与异常分类

### 1.1 基本概念

```
中断 (Interrupt) vs 异常 (Exception):

┌─────────────────────────────────────────────────────────┐
│                    事件分类                              │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  中断 (Interrupt) - 异步事件                            │
│  ├── 硬件中断 (Hardware Interrupt / IRQ)                │
│  │   ├── 可屏蔽中断 (Maskable): 键盘, 网卡, 定时器     │
│  │   └── 不可屏蔽中断 (NMI): 硬件错误, 看门狗          │
│  └── 软件中断 (Software Interrupt / INT)                │
│      └── INT n / SYSCALL / SYSENTER                    │
│                                                         │
│  异常 (Exception) - 同步事件                            │
│  ├── 故障 (Fault): 可恢复, 重新执行指令                 │
│  │   ├── Page Fault (#PF, 14)                          │
│  │   ├── General Protection Fault (#GP, 13)            │
│  │   └── Stack Fault (#SS, 12)                         │
│  ├── 陷阱 (Trap): 可恢复, 执行下一条指令               │
│  │   ├── Breakpoint (#BP, 3)                           │
│  │   └── Overflow (#OF, 4)                             │
│  └── 终止 (Abort): 不可恢复, 进程终止                  │
│      ├── Machine Check (#MC, 18)                       │
│      └── Double Fault (#DF, 8)                         │
└─────────────────────────────────────────────────────────┘
```

### 1.2 x86-64 异常向量表

```
┌──────┬─────────────────────┬──────────┬────────────────────┐
│ 向量 │ 名称                │ 类型     │ 描述               │
├──────┼─────────────────────┼──────────┼────────────────────┤
│  0   │ #DE (Divide Error)  │ Fault    │ 除零错误           │
│  1   │ #DB (Debug)         │ Fault/TF │ 调试异常           │
│  2   │ NMI                 │ Interrupt│ 不可屏蔽中断       │
│  3   │ #BP (Breakpoint)    │ Trap     │ INT3 断点          │
│  4   │ #OF (Overflow)      │ Trap     │ INTO 溢出          │
│  5   │ #BR (Bound Range)   │ Fault    │ BOUND 越界         │
│  6   │ #UD (Invalid Opcode)│ Fault    │ 无效操作码         │
│  7   │ #NM (Device Not Avail)│ Fault  │ FPU 不可用         │
│  8   │ #DF (Double Fault)  │ Abort    │ 双重故障           │
│ 10   │ #TS (Invalid TSS)   │ Fault    │ 无效 TSS           │
│ 11   │ #NP (Segment Not P) │ Fault    │ 段不存在           │
│ 12   │ #SS (Stack Fault)   │ Fault    │ 栈段故障           │
│ 13   │ #GP (General Prot)  │ Fault    │ 一般保护故障       │
│ 14   │ #PF (Page Fault)    │ Fault    │ 页面故障           │
│ 16   │ #MF (FPU Error)     │ Fault    │ 浮点异常           │
│ 17   │ #AC (Alignment Check)│ Fault   │ 对齐检查           │
│ 18   │ #MC (Machine Check) │ Abort    │ 机器检查           │
│ 19   │ #XM (SIMD Exception)│ Fault    │ SIMD 浮点异常      │
│ 20   │ #VE (Virtualization)│ Fault    │ 虚拟化异常         │
│ 30   │ #SX (Security)      │ Fault    │ 安全异常           │
│ 32-255│ User Defined       │ Interrupt│ 外部中断/软中断    │
└──────┴─────────────────────┴──────────┴────────────────────┘
```

## 2. 中断描述符表 (IDT)

### 2.1 x86-64 IDT 结构

```
IDT (Interrupt Descriptor Table):
┌─────────────────────────────────────────────────────────┐
│  IDT 寄存器 (IDTR):                                     │
│  ┌──────────────────┬─────────────────────────────────┐ │
│  │    Limit (16-bit)│    Base Address (64-bit)        │ │
│  └──────────────────┴─────────────────────────────────┘ │
│                                                         │
│  IDT 表项 (每个 16 bytes):                              │
│  ┌─────────────────────────────────────────────────────┐│
│  │ Offset [63:48]    │ Reserved │ P │ DPL │ 0 │ Type  ││
│  ├────────────────────┼──────────┼───┼─────┼───┼───────┤│
│  │ Segment Selector   │ Offset [31:16]                 ││
│  ├────────────────────┼────────────────────────────────┤│
│  │ Offset [15:0]     │ (Reserved for 64-bit)          ││
│  └────────────────────┴────────────────────────────────┘│
│                                                         │
│  Gate Types:                                            │
│  0xE: Interrupt Gate (64-bit) - 自动清除 IF            │
│  0xF: Trap Gate (64-bit) - 不清除 IF                   │
│  0x5: Task Gate - 任务切换 (已弃用)                    │
└─────────────────────────────────────────────────────────┘

IDT Entry 详细结构:
┌─────────────────────────────────────────────────────────┐
│  Bit 127-96: Offset[63:32]                              │
│  Bit 95-80:  Reserved                                   │
│  Bit 79:     Present (P) - 是否有效                     │
│  Bit 78-77:  DPL - 特权级 (0-3)                        │
│  Bit 76:     0                                          │
│  Bit 75-72:  Gate Type (0xE=IntGate, 0xF=TrapGate)     │
│  Bit 71-64:  Reserved                                   │
│  Bit 63-48:  Offset[31:16]                              │
│  Bit 47-32:  Segment Selector (通常是内核代码段)        │
│  Bit 31-16:  Offset[15:0]                               │
│  Bit 15-0:   (保留)                                     │
└─────────────────────────────────────────────────────────┘
```

### 2.2 IDT 初始化

```c
// IDT Entry 结构 (x86-64)
struct idt_entry {
    uint16_t offset_low;     // 偏移 [15:0]
    uint16_t selector;       // 代码段选择子
    uint8_t  ist;            // IST 索引 (低3位)
    uint8_t  type_attr;      // 类型和属性
    uint16_t offset_mid;     // 偏移 [31:16]
    uint32_t offset_high;    // 偏移 [63:32]
    uint32_t reserved;       // 保留
} __attribute__((packed));

// IDT 寄存器结构
struct idt_ptr {
    uint16_t limit;          // IDT 大小 - 1
    uint64_t base;           // IDT 基地址
} __attribute__((packed));

// 设置 IDT Entry
void idt_set_gate(int vector, uint64_t handler, uint8_t flags) {
    idt[vector].offset_low  = handler & 0xFFFF;
    idt[vector].offset_mid  = (handler >> 16) & 0xFFFF;
    idt[vector].offset_high = (handler >> 32) & 0xFFFFFFFF;
    idt[vector].selector    = KERNEL_CS;
    idt[vector].ist         = 0;
    idt[vector].type_attr   = flags;
    idt[vector].reserved    = 0;
}

// 加载 IDT
void idt_load(void) {
    struct idt_ptr idtp = {
        .limit = sizeof(idt) - 1,
        .base  = (uint64_t)&idt
    };
    asm volatile("lidt %0" : : "m"(idtp));
}
```

## 3. 中断控制器

### 3.1 8259A PIC (Legacy)

```
8259A PIC (Programmable Interrupt Controller):

Master PIC (端口 0x20/0x21):
┌─────────────────────────────────────────┐
│            8259A Master                  │
│  ┌───┬───┬───┬───┬───┬───┬───┬───┐     │
│  │IRQ0│IRQ1│IRQ2│IRQ3│IRQ4│IRQ5│IRQ6│IRQ7│
│  │定时│键盘│级联│串口│串口│并口│软盘│    │
│  └───┴───┴───┴───┴───┴───┴───┴───┘     │
│         │                                │
│         ▼ (级联)                         │
│  ┌─────────────────────────────────┐    │
│  │            8259A Slave           │    │
│  │  ┌───┬───┬───┬───┬───┬───┬───┬───┐ │
│  │  │IRQ8│IRQ9│IRQ10│IRQ11│IRQ12│IRQ13│IRQ14│IRQ15│ │
│  │  │CMOS│级联│网络 │网络 │PS/2│FPU │硬盘│    │ │
│  │  └───┴───┴───┴───┴───┴───┴───┴───┘ │
│  └─────────────────────────────────┘    │
└─────────────────────────────────────────┘

中断向量重映射:
  IRQ 0-7  → INT 32-39  (Master)
  IRQ 8-15 → INT 40-47  (Slave)

8259A 编程 (ICW - Initialization Command Words):
  ICW1: 0x11 (边沿触发, 级联, 需要ICW4)
  ICW2: 0x20 (Master向量基址32)
  ICW3: 0x04 (Master: IRQ2级联)
  ICW4: 0x01 (8086模式)
```

### 3.2 APIC (Advanced PIC)

```
APIC 架构 (现代 x86):

┌─────────────────────────────────────────────────────────┐
│                    APIC 架构                             │
│                                                         │
│  ┌─────────────────────────────────────────────────┐    │
│  │              I/O APIC                            │    │
│  │  ┌───────────────────────────────────────────┐  │    │
│  │  │  Redirection Table (24 entries)           │  │    │
│  │  │  ┌─────┬─────┬─────┬─────┬─────┬─────┐  │  │    │
│  │  │  │Entry│Entry│Entry│ ... │Entry│Entry│  │  │    │
│  │  │  │  0  │  1  │  2  │     │ 22  │ 23  │  │  │    │
│  │  │  └─────┴─────┴─────┴─────┴─────┴─────┘  │  │    │
│  │  └───────────────────────────────────────────┘  │    │
│  └──────────────────────┬──────────────────────────┘    │
│                         │ (APIC Bus / Front-Side Bus)    │
│         ┌───────────────┼───────────────┐               │
│         │               │               │               │
│  ┌──────┴──────┐ ┌──────┴──────┐ ┌──────┴──────┐       │
│  │ Local APIC  │ │ Local APIC  │ │ Local APIC  │       │
│  │  (Core 0)   │ │  (Core 1)   │ │  (Core N)   │       │
│  │ ┌─────────┐ │ │ ┌─────────┐ │ │ ┌─────────┐ │       │
│  │ │ID       │ │ │ │ID       │ │ │ │ID       │ │       │
│  │ │TPR      │ │ │ │TPR      │ │ │ │TPR      │ │       │
│  │ │IRR      │ │ │ │IRR      │ │ │ │IRR      │ │       │
│  │ │ISR      │ │ │ │ISR      │ │ │ │ISR      │ │       │
│  │ │Timer    │ │ │ │Timer    │ │ │ │Timer    │ │       │
│  │ │LINT0/1  │ │ │ │LINT0/1  │ │ │ │LINT0/1  │ │       │
│  │ │Error    │ │ │ │Error    │ │ │ │Error    │ │       │
│  │ └─────────┘ │ │ └─────────┘ │ │ └─────────┘ │       │
│  └─────────────┘ └─────────────┘ └─────────────┘       │
└─────────────────────────────────────────────────────────┘

Local APIC 寄存器:
  0x020: APIC ID Register
  0x080: Task Priority Register (TPR)
  0x0B0: Arbitration Priority Register
  0x0D0: Processor Priority Register
  0x0E0: EOI Register (End of Interrupt)
  0x0F0: Remote Read Register
  0x100: Logical Destination Register
  0x200: Interrupt Command Register (ICR) [低32位]
  0x300: Interrupt Command Register (ICR) [高32位]
  0x320: LVT Timer Register
  0x340: LVT LINT0 Register
  0x350: LVT LINT1 Register
  0x370: LVT Error Register
  0x380: Initial Count Register (Timer)
  0x3E0: Divide Configuration Register (Timer)
```

### 3.3 ARM GIC (Generic Interrupt Controller)

```
ARM GICv3/v4 架构:

┌─────────────────────────────────────────────────────────┐
│                    GICv3 架构                            │
│                                                         │
│  ┌─────────────────────────────────────────────────┐    │
│  │              Distributor (GICD)                  │    │
│  │  - 全局中断分发                                  │    │
│  │  - 中断优先级管理                                │    │
│  │  - 中断路由配置                                  │    │
│  │  ┌───────────────────────────────────────────┐  │    │
│  │  │ SPI (Shared Peripheral Interrupt) 0-987   │  │    │
│  │  │ SGI (Software Generated Interrupt) 0-15   │  │    │
│  │  │ PPI (Private Peripheral Interrupt) 0-15   │  │    │
│  │  └───────────────────────────────────────────┘  │    │
│  └──────────────────────┬──────────────────────────┘    │
│                         │                               │
│         ┌───────────────┼───────────────┐               │
│         │               │               │               │
│  ┌──────┴──────┐ ┌──────┴──────┐ ┌──────┴──────┐       │
│  │ Redistributor│ │ Redistributor│ │ Redistributor│       │
│  │  (GICR)     │ │  (GICR)     │ │  (GICR)     │       │
│  │  ┌────────┐ │ │  ┌────────┐ │ │  ┌────────┐ │       │
│  │  │SGI/PPI │ │ │  │SGI/PPI │ │ │  │SGI/PPI │ │       │
│  │  └────────┘ │ │  └────────┘ │ │  └────────┘ │       │
│  └──────┬──────┘ └──────┬──────┘ └──────┬──────┘       │
│         │               │               │               │
│  ┌──────┴──────┐ ┌──────┴──────┐ ┌──────┴──────┐       │
│  │  CPU Core   │ │  CPU Core   │ │  CPU Core   │       │
│  │  ┌────────┐ │ │  ┌────────┐ │ │  ┌────────┐ │       │
│  │  │ CPU    │ │ │  │ CPU    │ │ │  │ CPU    │ │       │
│  │  │Interface│ │ │  │Interface│ │ │  │Interface│ │       │
│  │  └────────┘ │ │  └────────┘ │ │  └────────┘ │       │
│  └─────────────┘ └─────────────┘ └─────────────┘       │
└─────────────────────────────────────────────────────────┘

GIC 中断类型:
  SGI (0-15): 软件生成, 核间通信
  PPI (16-31): 私有外设中断, 每个CPU独立
  SPI (32-1019): 共享外设中断, 可路由到任意CPU
  LPI (8192+): Locality-specific, 消息信号中断
```

## 4. 中断处理流程

### 4.1 x86-64 中断处理完整流程

```
中断处理流程 (x86-64):

┌─────────────────────────────────────────────────────────┐
│  1. 中断触发                                            │
│  ┌───────────────────────────────────────────────────┐  │
│  │  硬件中断: IRQ信号 → PIC/APIC → CPU              │  │
│  │  软件中断: INT n / SYSCALL                        │  │
│  │  异常: CPU检测到错误条件                          │  │
│  └───────────────────────────────────────────────────┘  │
├─────────────────────────────────────────────────────────┤
│  2. CPU 响应 (硬件自动完成)                             │
│  ┌───────────────────────────────────────────────────┐  │
│  │  a. 保存当前状态:                                 │  │
│  │     - 保存 RIP, CS, RFLAGS, RSP, SS 到栈         │  │
│  │     - 如果特权级切换: 加载新 RSP (从 TSS)        │  │
│  │  b. 清除 TF (Trap Flag) 和 IF (Interrupt Flag)   │  │
│  │     (Interrupt Gate 清除 IF, Trap Gate 不清除)   │  │
│  │  c. 加载 IDT[n] 的段选择子到 CS                  │  │
│  │  d. 加载 IDT[n] 的偏移到 RIP                     │  │
│  └───────────────────────────────────────────────────┘  │
├─────────────────────────────────────────────────────────┤
│  3. 中断服务程序 (ISR)                                  │
│  ┌───────────────────────────────────────────────────┐  │
│  │  ; 函数序言 (保存上下文)                          │  │
│  │  push rax                                         │  │
│  │  push rbx                                         │  │
│  │  push rcx                                         │  │
│  │  push rdx                                         │  │
│  │  push rsi                                         │  │
│  │  push rdi                                         │  │
│  │  push rbp                                         │  │
│  │  push r8-r15                                      │  │
│  │  ; 保存 FPU/SSE/AVX 状态 (如果需要)              │  │
│  │  fxsave [rsp-512]                                 │  │
│  │                                                   │  │
│  │  ; 中断处理逻辑                                   │  │
│  │  ...                                              │  │
│  │                                                   │  │
│  │  ; 发送 EOI (End of Interrupt)                   │  │
│  │  mov dword [APIC_BASE + 0xB0], 0                 │  │
│  │                                                   │  │
│  │  ; 恢复上下文                                     │  │
│  │  fxrstor [rsp-512]                                │  │
│  │  pop r8-r15                                       │  │
│  │  pop rbp                                          │  │
│  │  pop rdi                                          │  │
│  │  pop rsi                                          │  │
│  │  pop rdx                                          │  │
│  │  pop rcx                                          │  │
│  │  pop rbx                                          │  │
│  │  pop rax                                          │  │
│  │                                                   │  │
│  │  ; 中断返回                                       │  │
│  │  iretq                                            │  │
│  └───────────────────────────────────────────────────┘  │
├─────────────────────────────────────────────────────────┤
│  4. IRETQ 指令                                          │
│  ┌───────────────────────────────────────────────────┐  │
│  │  - 从栈恢复 SS, RSP, RFLAGS, CS, RIP             │  │
│  │  - 如果特权级切换: 恢复旧栈                       │  │
│  │  - 恢复 IF 标志 (如果之前被清除)                  │  │
│  └───────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
```

### 4.2 栈帧布局

```
中断栈帧 (无特权级切换):
高地址
┌───────────────────────┐
│        SS             │ ← 64-bit (如果特权级切换)
├───────────────────────┤
│        RSP            │ ← 64-bit (如果特权级切换)
├───────────────────────┤
│       RFLAGS          │ ← 64-bit
├───────────────────────┤
│        CS             │ ← 64-bit
├───────────────────────┤
│        RIP            │ ← 64-bit (返回地址)
├───────────────────────┤
│   Error Code (可选)   │ ← 64-bit (某些异常)
├───────────────────────┤
│   保存的寄存器...      │
└───────────────────────┘
低地址

中断栈帧 (有特权级切换):
高地址
┌───────────────────────┐
│   用户态 SS           │
├───────────────────────┤
│   用户态 RSP          │
├───────────────────────┤
│       RFLAGS          │
├───────────────────────┤
│   用户态 CS           │
├───────────────────────┤
│   用户态 RIP          │
├───────────────────────┤
│   Error Code (可选)   │
├───────────────────────┤
│   内核态寄存器...      │
└───────────────────────┘
低地址 (内核栈)
```

## 5. 中断延迟分析

### 5.1 延迟来源

```
中断延迟分解:

┌─────────────────────────────────────────────────────────┐
│                    中断延迟组成                          │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  1. 硬件延迟 (Hardware Latency)                         │
│  ┌───────────────────────────────────────────────────┐  │
│  │  - 中断信号同步 (1-2 时钟周期)                    │  │
│  │  - APIC 延迟 (2-5 时钟周期)                       │  │
│  │  - 总线传输延迟 (取决于互连)                      │  │
│  │  总计: 5-20 时钟周期                              │  │
│  └───────────────────────────────────────────────────┘  │
│                                                         │
│  2. CPU 流水线延迟 (Pipeline Latency)                   │
│  ┌───────────────────────────────────────────────────┐  │
│  │  - 当前指令完成 (0-数十周期, 除法器最慢)          │  │
│  │  - 流水线排空 (10-20 周期)                        │  │
│  │  - 保存上下文 (10-30 周期)                        │  │
│  │  总计: 20-100+ 时钟周期                           │  │
│  └───────────────────────────────────────────────────┘  │
│                                                         │
│  3. 软件延迟 (Software Latency)                         │
│  ┌───────────────────────────────────────────────────┐  │
│  │  - IDT 查表 (缓存命中: ~10周期, 未命中: ~100)     │  │
│  │  - ISR 入口代码 (保存寄存器, 20-50 周期)          │  │
│  │  - 中断处理逻辑 (取决于实现)                      │  │
│  │  总计: 50-1000+ 时钟周期                          │  │
│  └───────────────────────────────────────────────────┘  │
│                                                         │
│  4. 仲裁延迟 (Arbitration Latency)                     │
│  ┌───────────────────────────────────────────────────┐  │
│  │  - 多中断源竞争 (APIC 优先级仲裁)                 │  │
│  │  - 更高优先级中断正在处理                         │  │
│  │  - 中断被禁用 (CLI)                               │  │
│  │  总计: 0-不确定                                   │  │
│  └───────────────────────────────────────────────────┘  │
│                                                         │
│  总中断延迟 = 硬件 + 流水线 + 软件 + 仲裁              │
│  典型值: 1-10 μs (现代 x86 @ 3GHz)                    │
│  最坏情况: 100+ μs (长指令 + 缓存未命中 + 竞争)       │
└─────────────────────────────────────────────────────────┘
```

### 5.2 WCET 分析

```
最坏执行时间 (Worst-Case Execution Time) 分析:

┌─────────────────────────────────────────────────────────┐
│  WCET = T_interrupt_disable + T_save_context +          │
│         T_ISR_logic + T_restore_context +               │
│         T_interrupt_enable                              │
│                                                         │
│  测量方法:                                              │
│  1. GPIO 翻转法:                                        │
│     中断入口: 置高 GPIO                                │
│     中断出口: 置低 GPIO                                │
│     示波器测量脉冲宽度                                 │
│                                                         │
│  2. 时间戳计数器 (TSC):                                │
│     ISR入口: rdtsc → t1                                │
│     ISR出口: rdtsc → t2                                │
│     延迟 = (t2 - t1) / CPU频率                         │
│                                                         │
│  3. 性能计数器:                                         │
│     配置 PMU 计数特定事件                              │
│     如: CPU_CLK_UNHALTED.THREAD                        │
│                                                         │
│  静态分析工具:                                          │
│  - aiT (AbsInt)                                        │
│  - Bound-T                                              │
│  - OTAWA                                               │
│  - Chronos                                             │
└─────────────────────────────────────────────────────────┘
```

## 6. 中断合并 (Interrupt Coalescing)

### 6.1 原理

```
中断合并 (减少中断频率):

无合并 (每个数据包一个中断):
时间: ─────────────────────────────────────────────────────►
中断: ↑   ↑   ↑   ↑   ↑   ↑   ↑   ↑   ↑   ↑   ↑   ↑
     pkt pkt pkt pkt pkt pkt pkt pkt pkt pkt pkt pkt
     问题: 高频中断导致 CPU 过载, 上下文切换开销大

有合并 (批量处理):
时间: ─────────────────────────────────────────────────────►
中断: ↑               ↑               ↑
     [pkt×4]         [pkt×5]         [pkt×3]
     优势: 减少中断次数, 提高吞吐量
     劣势: 增加单个数据包延迟
```

### 6.2 Linux NAPI

```
NAPI (New API) - Linux 网络中断处理:

┌─────────────────────────────────────────────────────────┐
│                    NAPI 工作流程                         │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  1. 数据包到达, 网卡产生硬件中断                        │
│     ┌───────────────────────────────────────────────┐   │
│     │  NIC → IRQ → CPU                              │   │
│     └───────────────────────────────────────────────┘   │
│                                                         │
│  2. 硬中断处理程序 (Hard IRQ Handler)                   │
│     ┌───────────────────────────────────────────────┐   │
│     │  - 禁用网卡中断 (napi_schedule)               │   │
│     │  - 将 NAPI 结构加入轮询队列                   │   │
│     │  - 触发软中断 (NET_RX_SOFTIRQ)               │   │
│     │  - 返回 IRQ_HANDLED                           │   │
│     └───────────────────────────────────────────────┘   │
│                                                         │
│  3. 软中断处理 (Polling Mode)                           │
│     ┌───────────────────────────────────────────────┐   │
│     │  - 从网卡 DMA 环形缓冲区批量取包              │   │
│     │  - 每次最多处理 budget 个数据包 (通常 64)     │   │
│     │  - 如果处理完所有包: 重新启用网卡中断         │   │
│     │  - 如果还有包: 留在轮询队列, 下次继续         │   │
│     └───────────────────────────────────────────────┘   │
│                                                         │
│  4. 状态切换:                                           │
│     ┌───────────────────────────────────────────────┐   │
│     │  中断模式 ←→ 轮询模式                         │   │
│     │  低负载: 中断模式 (低延迟)                    │   │
│     │  高负载: 轮询模式 (高吞吐)                    │   │
│     └───────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────┘

NAPI 配置参数:
  /sys/class/net/eth0/napi_defer_hard_irqs  # 延迟硬中断次数
  /sys/class/net/eth0/gro_flush_timeout      # GRO 刷新超时
  budget: 每次轮询处理的最大数据包数
```

## 7. 中断亲和性 (Interrupt Affinity)

### 7.1 配置方法

```
中断亲和性设置:

查看当前中断分布:
  $ cat /proc/interrupts
  $ cat /proc/irq/<irq_number>/smp_affinity

设置中断亲和性 (绑定到特定 CPU):
  $ echo <cpu_mask> > /proc/irq/<irq_number>/smp_affinity

CPU 掩码计算:
  CPU 0: 0x01 (0001)
  CPU 1: 0x02 (0010)
  CPU 2: 0x04 (0100)
  CPU 3: 0x08 (1000)
  CPU 0+1: 0x03 (0011)
  CPU 2+3: 0x0C (1100)

示例:
  # 将 IRQ 32 绑定到 CPU 0
  echo 1 > /proc/irq/32/smp_affinity

  # 将 IRQ 33 绑定到 CPU 1
  echo 2 > /proc/irq/33/smp_affinity

  # 将 IRQ 34 绑定到 CPU 0 和 CPU 1
  echo 3 > /proc/irq/34/smp_affinity

irqbalance 服务:
  - 自动中断负载均衡
  - 基于中断频率和 CPU 负载
  - 可配置排除特定 IRQ

  禁用 irqbalance (手动管理):
  $ systemctl stop irqbalance

  /proc/irq/default_smp_affinity: 默认亲和性掩码
```

### 7.2 性能优化

```
中断亲和性优化策略:

1. 网卡多队列 + RPS/RFS:
┌─────────────────────────────────────────────────────────┐
│  NIC Queue 0 → CPU 0 (处理流 0)                        │
│  NIC Queue 1 → CPU 1 (处理流 1)                        │
│  NIC Queue 2 → CPU 2 (处理流 2)                        │
│  NIC Queue 3 → CPU 3 (处理流 3)                        │
│                                                         │
│  RPS (Receive Packet Steering):                         │
│  - 软件级别的接收队列选择                              │
│  - 基于数据包哈希 (源IP/端口, 目的IP/端口)            │
│  - 适用于单队列网卡                                    │
│                                                         │
│  RFS (Receive Flow Steering):                           │
│  - 将数据包路由到处理该流的 CPU                        │
│  - 提高缓存命中率                                      │
└─────────────────────────────────────────────────────────┘

2. isolcpus (CPU 隔离):
   # 内核启动参数
   isolcpus=2,3

   作用: 将 CPU 2,3 从调度器中隔离
   用途: 专用中断处理 CPU, 实时任务 CPU

3. CPU 亲和性 + 中断亲和性协同:
   # 中断处理 CPU
   echo 4 > /proc/irq/32/smp_affinity  # IRQ → CPU 2

   # 应用程序 CPU
   taskset -c 3 ./my_realtime_app      # App → CPU 3

4. NUMA 感知中断分配:
   - 中断处理在设备本地 NUMA 节点
   - 减少跨节点内存访问
   - 查看: cat /proc/irq/<irq>/node
```

## 8. 实时中断

### 8.1 PREEMPT_RT

```
PREEMPT_RT (实时抢占补丁):

┌─────────────────────────────────────────────────────────┐
│                PREEMPT_RT 关键特性                       │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  1. 线程化中断 (Threaded Interrupts)                    │
│  ┌───────────────────────────────────────────────────┐  │
│  │  传统: 硬中断 → 软中断 → 处理                    │  │
│  │  RT:   硬中断 → 唤醒中断线程 → 处理              │  │
│  │                                                   │  │
│  │  中断线程:                                        │  │
│  │  - 可被更高优先级任务抢占                        │  │
│  │  - 有确定性的调度延迟                            │  │
│  │  - 优先级可配置 (默认 50)                        │  │
│  │                                                   │  │
│  │  配置:                                            │  │
│  │  echo 1 > /proc/irq/<irq>/threaded              │  │
│  │  chrt -f -p 90 <irq_thread_pid>                 │  │
│  └───────────────────────────────────────────────────┘  │
│                                                         │
│  2. 优先级继承 (Priority Inheritance)                   │
│  ┌───────────────────────────────────────────────────┐  │
│  │  - 自旋锁变为可睡眠锁 (RT_MUTEX)                 │  │
│  │  - 避免优先级反转                                │  │
│  │  - 高优先级任务等待低优先级持锁时                │  │
│  │    临时提升低优先级任务的优先级                  │  │
│  └───────────────────────────────────────────────────┘  │
│                                                         │
│  3. 完全抢占 (Full Preemption)                          │
│  ┌───────────────────────────────────────────────────┐  │
│  │  - 几乎所有内核代码都可被抢占                    │  │
│  │  - 包括临界区 (使用 RT 锁)                       │  │
│  │  - 最大化调度响应性                              │  │
│  └───────────────────────────────────────────────────┘  │
│                                                         │
│  延迟对比:                                              │
│  ┌──────────────┬────────────┬────────────┐            │
│  │ 配置         │ 平均延迟   │ 最坏延迟   │            │
│  ├──────────────┼────────────┼────────────┤            │
│  │ PREEMPT_NONE │ ~10 μs     │ ~1000 μs   │            │
│  │ PREEMPT_VOL  │ ~5 μs      │ ~100 μs    │            │
│  │ PREEMPT_FULL │ ~2 μs      │ ~50 μs     │            │
│  │ PREEMPT_RT   │ ~1 μs      │ ~10 μs     │            │
│  └──────────────┴────────────┴────────────┘            │
└─────────────────────────────────────────────────────────┘
```

### 8.2 实时中断编程

```c
// 实时中断处理示例
#include <linux/interrupt.h>
#include <linux/hrtimer.h>
#include <linux/sched/rt.h>

// 中断处理函数 (在线程化中断中执行)
static irqreturn_t my_irq_handler(int irq, void *dev_id) {
    struct my_device *dev = dev_id;

    // 读取设备状态
    uint32_t status = ioread32(dev->regs + STATUS_REG);

    if (!(status & IRQ_PENDING))
        return IRQ_NONE;

    // 清除中断
    iowrite32(IRQ_ACK, dev->regs + STATUS_REG);

    // 唤醒处理线程 (下半部)
    wake_up_process(dev->handler_thread);

    return IRQ_HANDLED;
}

// 注册线程化中断
ret = request_threaded_irq(
    dev->irq,
    my_irq_handler,      // 硬中断处理 (快速)
    my_irq_thread_fn,    // 线程化处理 (完整处理)
    IRQF_ONESHOT,        // 单次触发模式
    "my_device",
    dev
);

// 高精度定时器中断
static enum hrtimer_restart my_hrtimer_callback(struct hrtimer *timer) {
    struct my_device *dev = container_of(timer, struct my_device, timer);

    // 定时处理逻辑
    process_data(dev);

    // 重新启动定时器 (周期性)
    hrtimer_forward_now(timer, ns_to_ktime(1000000)); // 1ms
    return HRTIMER_RESTART;
}

// 设置高精度定时器
hrtimer_init(&dev->timer, CLOCK_MONOTONIC, HRTIMER_MODE_REL);
dev->timer.function = my_hrtimer_callback;
hrtimer_start(&dev->timer, ns_to_ktime(1000000), HRTIMER_MODE_REL);
```

### 8.3 中断优先级配置

```
Linux 中断优先级管理:

┌─────────────────────────────────────────────────────────┐
│  中断优先级层次:                                        │
│                                                         │
│  最高优先级:                                            │
│  ├── NMI (不可屏蔽中断)                                │
│  ├── Machine Check                                      │
│  └── Critical Hardware Faults                           │
│                                                         │
│  高优先级 (实时):                                       │
│  ├── 线程化中断 (chrt -f 90)                           │
│  ├── 高精度定时器                                      │
│  └── 关键设备中断 (网卡, 磁盘)                        │
│                                                         │
│  普通优先级:                                            │
│  ├── 普通中断线程 (默认优先级 50)                      │
│  ├── 软中断 (softirq)                                  │
│  └── 工作队列 (workqueue)                              │
│                                                         │
│  低优先级:                                              │
│  ├── 后台中断处理                                      │
│  └── 统计/监控中断                                     │
└─────────────────────────────────────────────────────────┘

实时任务优先级分配:
  SCHED_FIFO 优先级范围: 1-99 (99最高)
  推荐分配:
    中断处理: 90-95
    控制任务: 80-89
    数据采集: 70-79
    日志/监控: 50-69
    普通任务: 0 (SCHED_OTHER)

配置示例:
  # 设置中断线程优先级
  chrt -f -p 90 $(pgrep irq/32-my_dev)

  # 设置实时任务优先级
  chrt -f -p 80 ./control_task

  # CPU 隔离
  # /etc/default/grub:
  GRUB_CMDLINE_LINUX="isolcpus=2,3 nohz_full=2,3"
```
