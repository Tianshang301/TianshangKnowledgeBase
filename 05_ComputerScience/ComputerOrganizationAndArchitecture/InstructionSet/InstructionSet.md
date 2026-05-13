# 指令集 (Instruction Set Architecture)

## 1. ISA 设计原则

### 设计权衡

| 原则 | 说明 | 影响 |
|------|------|------|
| 正交性 | 各指令可任意组合寻址方式 | 编译器友好，译码复杂 |
| 完备性 | 提供足够的指令完成所有操作 | 减少指令数 vs 简化硬件 |
| 规整性 | 指令格式统一 | 简化译码，利于流水线 |
| 兼容性 | 向后兼容 | x86 历史包袱重 |
| 可扩展性 | 预留编码空间 | RISC-V 模块化扩展 |

### ISA 分类

```
按架构类型：
  ┌──────────────────────────────────────┐
  │  堆栈架构 (Stack)       ─── JVM      │
  │  累加器架构 (Accumulator) ─── 早期CPU │
  │  寄存器-存储器架构       ─── x86     │
  │  加载-存储架构 (Load/Store) ─── ARM,  │
  │                              MIPS,   │
  │                              RISC-V  │
  └──────────────────────────────────────┘
```

## 2. 指令格式 (Instruction Formats)

### MIPS 三种格式

```
R-type (寄存器):
  ┌──────┬────┬────┬────┬──────┬──────┐
  │ OP   │ RS │ RT │ RD │ Shamt│Funct │
  │ 6bit │5bit│5bit│5bit│ 5bit │ 6bit │
  └──────┴────┴────┴────┴──────┴──────┘
  例: ADD R1, R2, R3    →  R1 = R2 + R3

I-type (立即数):
  ┌──────┬────┬────┬──────────────────┐
  │ OP   │ RS │ RT │    Immediate      │
  │ 6bit │5bit│5bit│      16bit       │
  └──────┴────┴────┴──────────────────┘
  例: ADDI R1, R2, 100  →  R1 = R2 + 100
      LW R1, 0(R2)      →  R1 = M[R2+0]

J-type (跳转):
  ┌──────┬────────────────────────────┐
  │ OP   │        Address             │
  │ 6bit │          26bit            │
  └──────┴────────────────────────────┘
  例: J 0x400000       →  PC = target
```

### x86 指令格式 (CISC 复杂)

```
x86 指令最长 15 字节：
┌────┬───┬────┬────┬────┬──────┬──────┐
│前缀 │REX│OP  │ModRM│SIB │偏移量 │立即数│
│0-4B│1B │1-3B│ 1B  │ 1B │0/1/2/4│0/1/2/4│
└────┴───┴────┴────┴────┴──────┴──────┘

ModRM 字节：
  ┌──────┬──────┬──────┐
  │ Mod  │ Reg  │ R/M  │
  │ 2bit │ 3bit │ 3bit │
  └──────┴──────┴──────┘
  Mod: 寻址模式 (寄存器/基址+偏移)
  Reg: 寄存器或操作码扩展
  R/M: 寄存器或内存地址

SIB 字节 (Scale-Index-Base)：
  ┌──────┬──────┬──────┐
  │ Scale│ Index│ Base │
  │ 2bit │ 3bit │ 3bit │
  └──────┴──────┴──────┘
  地址 = Base + Index × 2^Scale + Offset
```

## 3. 寻址方式 (Addressing Modes)

| 寻址方式 | 有效地址计算 | 示例 (MIPS/x86) |
|---------|-------------|----------------|
| 立即数寻址 | 操作数 = 指令中的立即数 | ADDI R1, 5 / MOV EAX, 5 |
| 寄存器寻址 | 操作数 = 寄存器内容 | ADD R1, R2 / MOV EAX, EBX |
| 直接寻址 | EA = 地址字段 | LW R1, addr / MOV EAX, [0x1000] |
| 寄存器间接 | EA = 寄存器值 | LW R1, (R2) / MOV EAX, [EBX] |
| 基址+偏移 | EA = 基址寄存器 + 偏移 | LW R1, 4(R2) / MOV EAX, [EBP+8] |
| 索引寻址 | EA = 基址 + (索引 × 比例) | — / MOV EAX, [EBX+ESI×4] |
| PC 相对 | EA = PC + 偏移 | BEQ R1, R2, label / JMP label |
| 自增/自减 | EA = 寄存器值, 然后增/减 | — / MOV EAX, [ESI++] |

## 4. 指令类型

### 数据传送指令

```
MIPS:
  LW R1, 0(R2)    # 加载字 (Load Word)
  SW R1, 0(R2)    # 存储字 (Store Word)
  LB / SB         # 加载/存储字节
  LBU             # 加载无符号字节

x86:
  MOV EAX, EBX    # 寄存器间传送
  MOV EAX, [mem]  # 内存加载
  MOV [mem], EAX  # 内存存储
  PUSH / POP      # 栈操作
  MOVSB           # 字符串传送
```

### 算术逻辑指令

```
MIPS:
  ADD R1, R2, R3    # 加法 (R-type)
  ADDI R1, R2, 100  # 加立即数
  SUB R1, R2, R3    # 减法
  AND / OR / XOR    # 位运算
  SLL / SRL         # 逻辑移位
  SLT R1, R2, R3    # 有符号小于 (Set Less Than)

x86:
  ADD EAX, EBX      # 加法
  SUB EAX, 5        # 减法
  IMUL EAX, EBX     # 有符号乘法
  AND / OR / XOR    # 位运算
  SHL / SHR         # 移位
  CMP EAX, EBX      # 比较（设置 FLAGS）
```

### 控制流指令

```
条件分支 (Branches):
  MIPS: BEQ R1, R2, label  # 相等则跳转
        BNE R1, R2, label  # 不等则跳转
        BLEZ, BGTZ, ...     # 与0比较

  x86:  JZ label           # 等于0跳转 (Zero Flag)
        JNZ label          # 非0跳转
        JL, JG, JLE, JGE   # 有符号比较
        JB, JA, JBE, JAE   # 无符号比较 (Below/Above)

无条件跳转:
  MIPS: J label            # 直接跳转 (J-type)
        JR R1              # 寄存器跳转 (用于函数返回)
        JAL label          # 跳转并链接 (调用函数)

  x86:  JMP label          # 无条件跳转
        CALL label         # 函数调用
        RET                # 函数返回
```

## 5. 调用约定 (Calling Conventions)

### 调用者保存 vs 被调用者保存

```
调用者保存寄存器 (Caller-saved):
  调用前由调用者压栈保存
  调用者负责恢复
  例: R1-R10 (MIPS $t0-$t9)

被调用者保存寄存器 (Callee-saved):
  被调用者可在开头保存、末尾恢复
  调用者可放心使用
  例: R11-R20 (MIPS $s0-$s7)
```

### 栈帧 (Stack Frame)

```
高地址
  ┌─────────────────────┐
  │ 调用者栈帧           │
  ├─────────────────────┤
  │ 参数 n (第7+参数)    │
  │ ...                 │
  │ 参数 7              │
  ├─────────────────────┤
  │ 返回地址             │ ← 被调用者栈帧顶部
  ├─────────────────────┤
  │ 保存的帧指针 (EBP)   │
  ├─────────────────────┤
  │ 局部变量             │
  │ ...                 │
  ├─────────────────────┤
  │ 保存的寄存器         │
  ├─────────────────────┤
  │ 临时空间             │
  └─────────────────────┘ ← ESP (栈指针)
低地址

x86-64 调用约定 (System V ABI):
  前 6 个整数参数: RDI, RSI, RDX, RCX, R8, R9
  前 8 个浮点参数: XMM0-XMM7
  返回值: RAX
```

## 6. MIPS 指令集概述

```
MIPS 核心指令 (~50 条)：

算术:      ADD, ADDI, SUB, MUL, DIV, SLT
逻辑:      AND, OR, XOR, NOR, SLL, SRL
数据传送:   LW, SW, LB, SB, LBU, SBU
分支:      BEQ, BNE, BLEZ, BGTZ, BLTZ
跳转:      J, JR, JAL, JALR
特权:      SYSCALL, BREAK, MFC0, MTC0
浮点:      ADD.S, SUB.S, MUL.S, DIV.S

寄存器约定：
  $0     ($zero)   常量 0
  $1     ($at)     汇编器临时
  $2-$3  ($v0-$v1) 函数返回值
  $4-$7  ($a0-$a3) 函数参数
  $8-$15 ($t0-$t7) 临时 (调用者保存)
  $16-$23($s0-$s7) 保存的 (被调用者保存)
  $24-$25($t8-$t9) 临时
  $26-$27($k0-$k1) 内核
  $28    ($gp)     全局指针
  $29    ($sp)     栈指针
  $30    ($fp)     帧指针
  $31    ($ra)     返回地址
```

## 7. x86/x64 指令集

### x86 演进

| 扩展 | 年份 | 说明 |
|------|------|------|
| 8086 | 1978 | 16-bit, 基础 ISA |
| 80386 | 1985 | 32-bit, 保护模式 |
| MMX | 1997 | 多媒体扩展 (64-bit) |
| SSE | 1999 | 单指令多数据 (128-bit) |
| SSE2 | 2001 | 双精度浮点 |
| x86-64 | 2003 | AMD 64-bit 扩展 |
| AVX | 2011 | 256-bit SIMD |
| AVX-512 | 2017 | 512-bit SIMD |

### x86-64 寄存器

```
64-bit 通用寄存器：
  RAX (累加器)     RCX (计数)       RDX (数据)
  RBX (基址)       RSP (栈指针)     RBP (帧指针)
  RSI (源索引)     RDI (目标索引)
  R8 - R15 (新增)

32-bit 子寄存器：
  EAX (RAX 低32位)  EBX, ECX, EDX ...

段寄存器： CS, DS, ES, FS, GS, SS
FLAGS 寄存器： ZF, CF, SF, OF, IF, DF ...
```

## 8. RISC-V ISA 基础

### 模块化设计

```
RISC-V 基础 ISA：RV32I (整数, 固定 32-bit 指令)

ISA 扩展：
  M — 乘除 (Multiply/Divide)
  F — 单精度浮点 (Float)
  D — 双精度浮点 (Double)
  C — 压缩指令 (Compressed, 16-bit)
  A — 原子操作 (Atomic)
  B — 位操作 (Bit manipulation)
  V — 向量 (Vector)
  H — 虚拟化 (Hypervisor)
  Zk — 加密 (Cryptography)

组合示例：
  RV32IMAC  ─── 嵌入式 (Arduino-like)
  RV64GC    ─── 通用计算 (Linux-capable)
    G = IMAFD
```

### RV32I 指令格式

```
R-type: [funct7(7)][rs2(5)][rs1(5)][funct3(3)][rd(5)][opcode(7)]
I-type: [imm(12)][rs1(5)][funct3(3)][rd(5)][opcode(7)]
S-type: [imm[11:5](7)][rs2(5)][rs1(5)][funct3(3)][imm[4:0](5)][opcode(7)]
B-type: [imm[12|10:5](7)][rs2(5)][rs1(5)][funct3(3)][imm[4:1|11](5)][opcode(7)]
U-type: [imm[31:12](20)][rd(5)][opcode(7)]
J-type: [imm[20|10:1|11|19:12](20)][rd(5)][opcode(7)]
```

## 9. ISA 特性对比

| 特性 | MIPS | x86-64 | ARMv8-A | RISC-V |
|------|------|--------|---------|--------|
| 架构类型 | Load/Store | Reg-Mem | Load/Store | Load/Store |
| 指令长度 | 32-bit | 1-15字节 | 32-bit (Thumb: 16/32) | 32/16-bit (C扩展) |
| 寄存器数 | 32 | 16 | 31 | 32 |
| 寻址方式 | 3种 | 10+种 | 几种 | 几种 |
| 条件执行 | 无 | 标志位 | 条件码 (大部分指令) | 无 (用分支) |
| 浮点 | 协处理器 | SSE/AVX | VFP/NEON | F/D扩展 |
| 原子操作 | LL/SC | LOCK前缀 | LL/SC/LSE | A扩展 |
| 授权 | 专有 (MIPS) | 专有 (Intel/AMD) | 授权 (ARM) | 开源 |
| 应用场景 | 教学/嵌入式 | PC/服务器 | 移动/嵌入式 | 新兴 (所有领域) |

---

## 相关条目

- [[CPUArchitecture]]
- [[Assembly]]
- RISC_V
- [[05_ComputerScience/CompilerPrinciples/INDEX|CompilerPrinciples]]

## 参考资源

- 《Computer Organization and Design》(Patterson & Hennessy)
- MIPS32 Architecture Volume I
- Intel 64 and IA-32 Architectures Manual
- RISC-V Specifications (https://riscv.org/)
- ARM Architecture Reference Manual
