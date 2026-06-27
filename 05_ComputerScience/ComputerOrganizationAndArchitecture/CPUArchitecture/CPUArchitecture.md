---
aliases: [CPUArchitecture]
tags: ['ComputerOrganizationAndArchitecture', 'CPUArchitecture', 'CPUArchitecture']
created: 2026-05-16
updated: 2026-05-16
---

# CPU 架构 (CPU Architecture)

## 1. CPU 内部结构

### 微架构框图

```
CPU 核心 (Core):
┌─────────────────────────────────────────────┐
│  控制单元 (Control Unit)                     │
│  ┌─────────┐  ┌────────────┐  ┌──────────┐ │
│  │ 指令寄存器│  │指令译码器   │  │控制信号   │ │
│  │ (IR)    │  │ (Decoder)  │  │发生器     │ │
│  └─────────┘  └────────────┘  └──────────┘ │
├─────────────────────────────────────────────┤
│  数据通路 (Datapath)                         │
│  ┌──────────────────────────────────────┐   │
│  │  寄存器堆 (Register File)            │   │
│  │  R0 R1 R2 ... R31                   │   │
│  └────┬──────────────┬─────────────────┘   │
│       │              │                      │
│  ┌────▼────┐   ┌────▼────┐                 │
│  │  ALU    │   │ 地址计算 │                  │
│  └────┬────┘   └────┬────┘                 │
│       │              │                      │
│  ┌────▼──────────────▼─────┐                │
│  │ 数据缓存/内存接口        │                 │
│  └─────────────────────────┘                │
└─────────────────────────────────────────────┘
```

### 关键组件

| 组件 | 功能 | 说明 |
|------|------|------|
| 程序计数器 (PC) | 保存当前指令地址 | 顺序执行时自动 +4 |
| 指令寄存器 (IR) | 保存当前取出的指令 | 译码器的输入 |
| 通用寄存器堆 | 存储临时数据 | 32/64 个寄存器 |
| ALU | 算术逻辑运算 | +, -, ×, ÷, AND, OR, XOR |
| 状态寄存器 (FLAGS) | 记录运算结果特性 | Z, N, C, V 标志位 |
| 栈指针 (SP) | 指向栈顶 | 函数调用/返回 |
| 译码器 | 将指令翻译为控制信号 | 组合逻辑或微码 |

## 2. 冯·诺依曼 vs 哈佛架构

| 特性 | 冯·诺依曼 | 哈佛 | 现代改进型哈佛 |
|------|----------|------|---------------|
| 指令与数据存储器 | 统一 | 分离 | 内部分离，外部统一 |
| 总线 | 单总线 | 独立指令/数据总线 | 内部独立总线 |
| 瓶颈 | 冯·诺依曼瓶颈（总线竞争） | 无总线竞争 | 缓解瓶颈 |
| 实现复杂度 | 低 | 高 | 中 |
| 典型芯片 | x86 | 早期 DSP, ARM Cortex-M | 现代 x86/ARM (L1 分离) |

```
冯·诺依曼结构：
  CPU ──单总线── 存储器 [指令+数据]

哈佛结构：
  CPU ──指令总线── 指令存储器
  CPU ──数据总线── 数据存储器
```

## 3. RISC vs CISC

| 对比维度 | RISC | CISC |
|---------|------|------|
| 指令长度 | 固定 (32-bit) | 可变 (1-15 字节) |
| 指令数量 | 少 (~50) | 多 (~300+) |
| 寻址方式 | 少 (2-3 种) | 多 (10+ 种) |
| 寄存器数量 | 多 (32+) | 少 (8-16) |
| 访存指令 | 仅 Load/Store | 可混合运算 |
| 流水线效率 | 高 | 低（需要微码译码） |
| 代码密度 | 较低 | 高 |
| 功耗 | 低 | 高 |
| 设计周期 | 短 | 长 |
| 代表架构 | ARM, RISC-V, MIPS | x86/x64 |

### 现代趋势

```
CISC 内核实际使用 RISC 微操作：
  x86 指令 ──译码器──► μOP (微操作) ──执行引擎──► 结果
                    (类似 RISC 风格)

混合架构：
  ARMv8-A: 支持 AArch64 (64-bit RISC) + AArch32 (兼容)
  x86: 内部 μOP Cache + Out-of-Order 执行
```

## 4. 流水线基础

### 经典 5 级流水线

```
指令 1:  IF ── ID ── EX ── MEM ── WB
指令 2:    IF ── ID ── EX ── MEM ── WB
指令 3:      IF ── ID ── EX ── MEM ── WB
指令 4:        IF ── ID ── EX ── MEM ── WB

时钟周期: 1    2    3    4    5    6    7    8

理想 CPI = 1（每周期完成一条指令）
```

| 阶段 | 名称 | 操作 |
|------|------|------|
| IF | 取指 (Instruction Fetch) | 从 I-Cache 取指令，PC += 4 |
| ID | 译码 (Instruction Decode) | 译码指令，读取寄存器 |
| EX | 执行 (Execute) | ALU 运算，地址计算 |
| MEM | 访存 (Memory Access) | 数据缓存读写 (仅 Load/Store) |
| WB | 写回 (Write Back) | 结果写回寄存器堆 |

## 5. 流水线冒险 (Hazards)

### 结构冒险 (Structural Hazard)

```
冲突：同一周期两个阶段争用同一资源
例：冯·诺依曼结构 IF 取指令 + MEM 访存 → 冲突

解决：分离指令缓存和数据缓存（哈佛结构）
```

### 数据冒险 (Data Hazard)

```
三种类型：
  RAW (Read After Write)  ─── 真依赖（最常见）
  WAR (Write After Read)  ─── 反依赖（名称相关）
  WAW (Write After Write) ─── 输出依赖

例子 (RAW)：
  ADD R1, R2, R3    # R1 = R2 + R3
  SUB R4, R1, R5    # 还需要读 R1 → 冒险！
```

### 转发 (Forwarding/Bypassing)

```
无转发（会停顿）：
  ADD R1, R2, R3     IF  ID  EX  MEM  WB
  SUB R4, R1, R5         IF  ID  ---  EX  MEM  WB
                                ↑ 插入气泡

有转发：
  ADD R1, R2, R3     IF  ID  EX  MEM  WB
  SUB R4, R1, R5         IF  ID  EX  MEM  WB
                                ↑ EX 阶段从 MEM 阶段
                                  转发 R1 的值
```

### 控制冒险 (Control Hazard)

```
分支指令导致的不确定性：
  BEQ R1, R2, label   # 条件跳转
  ADD R3, R4, R5      # 可能不该执行！

解决：
  1. 分支预测 (Branch Prediction)
  2. 延迟分支 (Delayed Branch)
  3. 分支目标缓冲 (BTB)
  4. 预测失败时冲刷流水线 (Flush)
```

## 6. 分支预测 (Branch Prediction)

### 静态预测

| 策略 | 描述 | 正确率 |
|------|------|--------|
| 总是跳转 | 预测所有分支都跳转 | ~50% |
| 总是不跳转 | 预测所有分支都不跳转 | ~50% |
| 向后跳转 | 向后跳转预测为循环 → Taken | ~70% |
| 向前不跳转 | 向前跳转预测为条件 → Not Taken | ~60% |

### 动态预测

```
1-bit 预测器：
  状态: T (Taken) / N (Not Taken)
  正确率: ~80%

2-bit 饱和计数器 (更常用)：
     Taken                      Not Taken
   ┌─────┐   Not Taken    ┌─────┐
   │ 11  │◄───────────────│ 10  │
   │ 强  │                │ 弱  │
   └──┬──┘                └──┬──┘
      │  Taken                │  Taken
      ▼                       ▼
   ┌─────┐                ┌─────┐
   │ 01  │◄───────────────│ 00  │
   │ 弱  │   Not Taken    │ 强  │
   └─────┘                └─────┘
   强预测不跳转            强预测不跳转

  正确率: ~90-95%
```

### BTB (分支目标缓冲)

```
BTB 缓存分支指令的 PC 和目标地址：
  ┌──────────┬────────────┬────────┐
  │ PC       │ 目标地址    │ 历史   │
  ├──────────┼────────────┼────────┤
  │ 0x1000   │ 0x1040     │ 11     │
  │ 0x1020   │ 0x10A0     │ 10     │
  │ 0x1030   │ 0x1000     │ 00     │
  └──────────┴────────────┴────────┘

IF 阶段并行查询 BTB：
  PC → BTB → 命中 → 直接跳转（无需等待 EX 阶段）
```

## 7. 高级执行技术

### 超标量 (Superscalar)

```
单发射: [  IF  ][  ID  ][  EX  ][ MEM ][ WB ]
           每周期最多 1 条指令

多发射（超标量）:
  ┌──────┐
  │ IF   │  ← 一次取 2-6 条指令
  ├──────┤
  │ ID   │  ← 并行译码
  ├──────┤
  │ EX   │  ← 多个功能单元并行
  │ EX   │     (ALU0, ALU1, Load, Store, FP)
  ├──────┤
  │ MEM  │
  ├──────┤
  │ WB   │
  └──────┘
```

### 乱序执行 (Out-of-Order)

```
Tomasulo 算法核心：
  1. 寄存器重命名 (Register Renaming) — 解决 WAW/WAR
  2. 保留站 (Reservation Stations) — 等待操作数就绪
  3. 公共数据总线 (CDB) — 广播结果

顺序：
  ┌────┐  ┌────┐  ┌──────┐  ┌────┐  ┌────┐
  │取指│→│译码│→│发射队列 │→│执行│→│提交│
  │    │  │    │  │(乱序)  │  │    │  │(顺序)│
  └────┘  └────┘  └──────┘  └────┘  └────┘
                     ──── Tomasulo 关键
```

### SIMD（单指令多数据）

| 扩展 | 位宽 | 寄存器 | 引入年份 |
|------|------|--------|---------|
| MMX | 64-bit | MM0-MM7 | 1997 |
| SSE | 128-bit | XMM0-XMM7 | 1999 |
| SSE2 | 128-bit | XMM0-XMM15 | 2001 |
| AVX | 256-bit | YMM0-YMM15 | 2011 |
| AVX-512 | 512-bit | ZMM0-ZMM31 | 2017 |
| SVE (ARM) | 128-2048bit | 可变长度 | 2018 |

```
SIMD 加法示例：
  标量 (SISD):        SIMD (4路并行):
  a[0]+b[0]=c[0]      a[0-3]+b[0-3]=c[0-3]
  a[1]+b[1]=c[1]      ┌─────────────┐
  a[2]+b[2]=c[2]      │ +  │ +  │ +  │ +  │
  a[3]+b[3]=c[3]      └─────────────┘
```

## 8. 多核与缓存一致性

### MESI 协议

```
M — Modified (已修改): 仅本核持有，与主存不一致
E — Exclusive (独占): 仅本核持有，与主存一致
S — Shared (共享): 多核持有，与主存一致
I — Invalid (无效): 数据无效

状态转换：
              PrRd/---
              ┌────┐
              │  I  │
              └─┬──┘
     PrWr/BusRdX │ BusRd/Flush
              ┌──▼──┐
         ┌───│  E   │
         │   └──┬──┘
      BusRd    │ PrWr
         │   ┌──▼──┐
         └──►│  S  │←──BusRd──┐
             └──┬──┘         │
           BusRdX/Flush      │
            ┌──▼──┐         │
            │  M  ├──────────┘
            └─────┘ Flush
```

### 超线程 (Hyper-Threading / SMT)

```
物理核 → 逻辑核 (2个逻辑核共享一个物理核)：

物理核:
  ┌─────────────────────────┐
  │ 逻辑核0    │ 逻辑核1     │
  │ (PC, Regs) │ (PC, Regs) │
  ├─────────────────────────┤
  │  共享资源 (ALU, Cache)   │
  └─────────────────────────┘

优势：一个逻辑核停顿，另一个可继续使用执行单元
劣势：共享资源竞争，单个线程性能可能下降 ~10-20%
```

---

## 相关条目

- [[05_ComputerScience/ComputerOrganizationAndArchitecture/InstructionSet/InstructionSet|InstructionSet]]
- [[05_ComputerScience/ComputerOrganizationAndArchitecture/Pipelining/Pipelining|Pipelining]]
- [[05_ComputerScience/ComputerOrganizationAndArchitecture/MemoryHierarchy/MemoryHierarchy|MemoryHierarchy]]
- [[05_ComputerScience/ComputerOrganizationAndArchitecture/DigitalLogic/DigitalLogic|DigitalLogic]]

## 参考资源

- 《Computer Organization and Design》(Patterson & Hennessy)
- 《Computer Architecture: A Quantitative Approach》(Hennessy & Patterson)
- 《深入理解计算机系统》(CS:APP)
- Intel 64 and IA-32 Architectures Optimization Reference Manual
- ARM Architecture Reference Manual


