---
aliases:
  - 汇编语言编程
  - Assembly Language Programming
  - x86-64汇编
  - ARM64汇编
tags:
  - computer-architecture
  - assembly
  - x86-64
  - arm64
  - risc-v
  - low-level-programming
created: 2026-06-27
updated: 2026-06-27
---

# 汇编语言编程实战

## 1. x86-64 寄存器体系

### 1.1 通用寄存器

x86-64 将 32 位寄存器扩展至 64 位，新增 R8-R15 八个寄存器：

```
┌─────────────────────────────────────────────────────────┐
│                    64-bit Register                       │
│  ┌─────────────────────────────────────────────────────┐│
│  │                    RAX (64-bit)                     ││
│  │  ┌─────────────────────────────────┐                ││
│  │  │          EAX (32-bit)          │                ││
│  │  │  ┌───────────────┐             │                ││
│  │  │  │   AX (16-bit) │             │                │
│  │  │  │  ┌────┬────┐  │             │                ││
│  │  │  │  │ AH │ AL │  │             │                ││
│  │  │  │  └────┴────┘  │             │                ││
│  │  │  └───────────────┘             │                ││
│  │  └─────────────────────────────────┘                ││
│  └─────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────┘
```

| 64-bit | 32-bit | 16-bit | 8-bit | 用途 |
|--------|--------|--------|-------|------|
| RAX | EAX | AX | AL/AH | 返回值、累加器 |
| RBX | EBX | BX | BL/BH | 基址（callee-saved） |
| RCX | ECX | CX | CL/CH | 计数器、第4参数 |
| RDX | EDX | DX | DL/DH | 数据、第3参数 |
| RSI | ESI | SI | SIL | 源索引、第2参数 |
| RDI | EDI | DI | DIL | 目的索引、第1参数 |
| RBP | EBP | BP | BPL | 帧指针（callee-saved） |
| RSP | ESP | SP | SPL | 栈指针 |
| R8-R15 | R8D-R15D | R8W-R15W | R8B-R15B | 扩展通用寄存器 |

### 1.2 SIMD 寄存器

```
XMM0-XMM15:   128-bit (SSE)
YMM0-YMM15:   256-bit (AVX/AVX2)
ZMM0-ZMM31:   512-bit (AVX-512)

ZMM寄存器布局:
┌───────────────────────────────────────────────────────────────┐
│                         ZMM (512-bit)                         │
│ ┌─────────────────────────────────────────┐ ┌───────────────┐ │
│ │              YMM (256-bit)              │ │               │ │
│ │ ┌───────────────────────┐ ┌───────────┐ │ │               │ │
│ │ │     XMM (128-bit)     │ │           │ │ │               │ │
│ │ └───────────────────────┘ └───────────┘ │ │               │ │
│ └─────────────────────────────────────────┘ └───────────────┘ │
└───────────────────────────────────────────────────────────────┘
```

### 1.3 指令格式

x86-64 指令编码格式：

```
┌──────────┬──────────┬──────────┬──────────┬──────────┬──────────┬──────────┐
│ Prefixes │  REX     │ Opcode   │ ModR/M   │ SIB      │ Displacement │ Immediate │
│ (0-4 B)  │  (0-1 B) │ (1-3 B)  │ (0-1 B)  │ (0-1 B)  │ (0/1/2/4 B) │ (0/1/2/4 B)│
└──────────┴──────────┴──────────┴──────────┴──────────┴──────────┴──────────┘
```

REX 前缀（64 位模式）：

```
┌───┬───┬───┬───┬───┬───┬───┬───┐
│ 0 │ 1 │ 0 │ 0 │ W │ R │ X │ B │
└───┴───┴───┴───┴───┴───┴───┴───┘
W: 1=64位操作数
R: ModR/M.reg 扩展
X: SIB.index 扩展
B: ModR/M.r/m 或 SIB.base 扩展
```

### 1.4 寻址模式

```nasm
; 立即寻址
MOV RAX, 42              ; RAX = 42

; 寄存器寻址
MOV RAX, RBX             ; RAX = RBX

; 直接寻址
MOV RAX, [0x12345678]    ; RAX = *(0x12345678)

; 寄存器间接寻址
MOV RAX, [RBX]           ; RAX = *RBX

; 基址+偏移寻址
MOV RAX, [RBX + 16]      ; RAX = *(RBX + 16)

; 基址+变址寻址
MOV RAX, [RBX + RCX]     ; RAX = *(RBX + RCX)

; 比例变址寻址 (scale = 1,2,4,8)
MOV RAX, [RBX + RCX*4 + 8]  ; RAX = *(RBX + RCX*4 + 8)

; RIP 相对寻址 (64位模式特有)
MOV RAX, [RIP + offset]  ; 位置无关代码
```

## 2. 常用指令详解

### 2.1 数据传送指令

```nasm
; MOV 指令 - 数据传送
MOV RAX, RBX             ; 寄存器 ← 寄存器
MOV RAX, [RBX]           ; 寄存器 ← 内存
MOV [RBX], RAX           ; 内存 ← 寄存器
MOV RAX, 0x1234          ; 寄存器 ← 立即数

; MOVZX - 零扩展传送
MOVZX EAX, BYTE [RBX]   ; AL → EAX, 高位补零

; MOVSX - 符号扩展传送
MOVSX RAX, DWORD [RBX]  ; 32位符号扩展到64位

; LEA - 加载有效地址（不访问内存）
LEA RAX, [RBX + RCX*4 + 8]  ; RAX = RBX + RCX*4 + 8
; 常用于算术运算
LEA RAX, [RCX + RCX*2]      ; RAX = RCX * 3
LEA RAX, [RCX*4]             ; RAX = RCX * 4

; XCHG - 交换
XCHG RAX, RBX            ; RAX ↔ RBX

; CMOV - 条件传送（无分支）
CMOVZ RAX, RBX           ; if (ZF) RAX = RBX
CMOVG RAX, RBX           ; if (SF==OF && !ZF) RAX = RBX
```

### 2.2 算术指令

```nasm
; 加法
ADD RAX, RBX             ; RAX = RAX + RBX, 设置标志位
ADC RAX, RBX             ; RAX = RAX + RBX + CF（带进位加法）
INC RAX                  ; RAX++, 不影响 CF

; 减法
SUB RAX, RBX             ; RAX = RAX - RBX
SBB RAX, RBX             ; RAX = RAX - RBX - CF（带借位减法）
DEC RAX                  ; RAX--, 不影响 CF
NEG RAX                  ; RAX = -RAX（取补）

; 乘法
IMUL RAX, RBX            ; RAX = RAX * RBX（有符号）
IMUL RAX, RBX, 10        ; RAX = RBX * 10（三操作数形式）
MUL RBX                  ; RDX:RAX = RAX * RBX（无符号64位乘法）

; 除法
IDIV RBX                 ; RAX = RDX:RAX / RBX（有符号）
                         ; RDX = RDX:RAX % RBX
DIV RBX                  ; 无符号除法

; 标志位寄存器 (RFLAGS)
; ┌───┬───┬───┬───┬───┬───┬───┬───┬───┬───┬───┐
; │CF │PF │AF │ZF │SF │OF │...│TF │IF │DF │...│
; └───┴───┴───┴───┴───┴───┴───┴───┴───┴───┴───┘
; CF: 进位标志  PF: 奇偶标志  ZF: 零标志
; SF: 符号标志  OF: 溢出标志  DF: 方向标志
```

### 2.3 控制流指令

```nasm
; 比较与跳转
CMP RAX, RBX             ; 计算 RAX - RBX, 设置标志位
JE  label                ; Jump if Equal (ZF=1)
JNE label                ; Jump if Not Equal
JG  label                ; Jump if Greater (有符号)
JL  label                ; Jump if Less (有符号)
JA  label                ; Jump if Above (无符号)
JB  label                ; Jump if Below (无符号)
JMP label                ; 无条件跳转

; 函数调用
CALL function            ; 将返回地址压栈, 跳转到 function
RET                      ; 弹出返回地址, 跳转回去

; 栈操作
PUSH RAX                 ; RSP -= 8; [RSP] = RAX
POP  RBX                 ; RBX = [RSP]; RSP += 8

; 系统调用 (Linux x86-64)
MOV RAX, 1               ; syscall number (1 = sys_write)
MOV RDI, 1               ; fd (stdout)
LEA RSI, [msg]           ; buffer address
MOV RDX, len             ; length
SYSCALL                  ; 执行系统调用
```

## 3. 调用约定

### 3.1 System V AMD64 ABI (Linux/macOS)

```
参数传递顺序:
┌─────────┬──────────┬─────────┬─────────┬─────────┬─────────┬─────────┬─────────┐
│ Param 1 │ Param 2  │ Param 3 │ Param 4 │ Param 5 │ Param 6 │ Param 7 │ ...     │
│   RDI   │   RSI    │   RDX   │   RCX   │   R8    │   R9    │  Stack  │  Stack  │
└─────────┴──────────┴─────────┴─────────┴─────────┴─────────┴─────────┴─────────┘

返回值: RAX (整数), XMM0-XMM1 (浮点)
Callee-saved: RBX, RBP, R12-R15, RSP
Caller-saved: RAX, RCX, RDX, RSI, RDI, R8-R11
```

### 3.2 Microsoft x64 (Windows)

```
参数传递顺序:
┌─────────┬─────────┬─────────┬─────────┬─────────┬─────────┐
│ Param 1 │ Param 2 │ Param 3 │ Param 4 │ Param 5 │ ...     │
│   RCX   │   RDX   │   R8    │   R9    │  Stack  │  Stack  │
└─────────┴─────────┴─────────┴─────────┴─────────┴─────────┘

Shadow space: 调用者必须预留 32 字节栈空间
Callee-saved: RBX, RBP, RDI, RSI, R12-R15, RSP, XMM6-XMM15
```

### 3.3 栈帧结构

```
高地址
┌───────────────────────┐
│    返回地址 (8B)       │  ← CALL 指令压入
├───────────────────────┤
│    旧 RBP (8B)        │  ← RBP 指向此处
├───────────────────────┤
│    局部变量            │  ← RBP - offset
├───────────────────────┤
│    callee-saved 寄存器 │
├───────────────────────┤
│    参数区域            │  ← RSP (System V)
├───────────────────────┤
│    Shadow space (32B)  │  ← RSP (Windows)
└───────────────────────┘
低地址
```

## 4. ARM64 (AArch64) 汇编

### 4.1 寄存器

```
通用寄存器:
X0-X7:    参数/返回值 (caller-saved)
X8:       间接结果寄存器
X9-X15:   临时寄存器 (caller-saved)
X16-X17:  IP0/IP1 (链接器使用)
X18:      平台保留
X19-X28:  callee-saved
X29/FP:   帧指针
X30/LR:   链接寄存器
SP:       栈指针
PC:       程序计数器
XZR:      零寄存器

SIMD/FP:
V0-V7:    参数/返回值
V8-V15:   callee-saved (低64位)
V16-V31:  临时寄存器
```

### 4.2 ARM64 指令集

```asm
; 数据传送
MOV X0, #42              ; X0 = 42
MOV X0, X1               ; X0 = X1
LDR X0, [X1]             ; X0 = *X1
LDR X0, [X1, #16]        ; X0 = *(X1 + 16)
STR X0, [X1, #16]        ; *(X1 + 16) = X0
LDP X0, X1, [SP]         ; 加载一对寄存器
STP X0, X1, [SP, #-16]!  ; 存储一对, 前索引写回

; 算术运算
ADD X0, X1, X2           ; X0 = X1 + X2
ADD X0, X1, #10          ; X0 = X1 + 10
SUB X0, X1, X2           ; X0 = X1 - X2
MUL X0, X1, X2           ; X0 = X1 * X2
SDIV X0, X1, X2          ; X0 = X1 / X2 (有符号)

; 条件标志
ADDS X0, X1, X2          ; 加法并设置标志
SUBS X0, X1, X2          ; 减法并设置标志
CMP X1, X2               ; SUBS XZR, X1, X2
CMN X1, X2               ; ADDS XZR, X1, X2

; 条件分支
BEQ label                ; 相等
BNE label                ; 不等
BGT label                ; 大于 (有符号)
BLT label                ; 小于 (有符号)
B label                  ; 无条件跳转
BL function              ; 带链接的跳转 (调用)
RET                      ; 返回 (默认使用X30)

; 条件选择
CSEL X0, X1, X2, EQ      ; if (EQ) X0=X1 else X0=X2
CSINC X0, X1, XZR, EQ    ; if (EQ) X0=X1 else X0=X2+1
```

### 4.3 条件标志 (NZCV)

```
┌───┬───┬───┬───┐
│ N │ Z │ C │ V │
└───┴───┴───┴───┘
N: 负数标志 (Negative)
Z: 零标志 (Zero)
C: 进位标志 (Carry)
V: 溢出标志 (oVerflow)
```

## 5. RISC-V 汇编

### 5.1 寄存器约定

| 寄存器 | ABI名称 | 用途 | Caller/Callee |
|--------|---------|------|---------------|
| x0 | zero | 硬连线零 | - |
| x1 | ra | 返回地址 | Caller |
| x2 | sp | 栈指针 | Callee |
| x3 | gp | 全局指针 | - |
| x4 | tp | 线程指针 | - |
| x5-x7 | t0-t2 | 临时寄存器 | Caller |
| x8 | s0/fp | 帧指针 | Callee |
| x9 | s1 | 保存寄存器 | Callee |
| x10-x11 | a0-a1 | 参数/返回值 | Caller |
| x12-x17 | a2-a7 | 参数 | Caller |
| x18-x27 | s2-s11 | 保存寄存器 | Callee |
| x28-x31 | t3-t6 | 临时寄存器 | Caller |

### 5.2 RISC-V 指令格式

```
R-type:  ┌────────┬─────┬─────┬─────┬─────┬─────────┐
         │ funct7 │ rs2 │ rs1 │funct3│ rd │ opcode  │
         │  7-bit │5-bit│5-bit│3-bit│5-bit│ 7-bit  │
         └────────┴─────┴─────┴─────┴─────┴─────────┘

I-type:  ┌─────────────┬─────┬─────┬─────┬─────────┐
         │ imm[11:0]   │ rs1 │funct3│ rd │ opcode  │
         │   12-bit    │5-bit│3-bit│5-bit│ 7-bit  │
         └─────────────┴─────┴─────┴─────┴─────────┘

S-type:  ┌───────┬─────┬─────┬─────┬──────┬─────────┐
         │imm[11:5]│ rs2 │ rs1 │funct3│imm[4:0]│ opcode │
         │  7-bit │5-bit│5-bit│3-bit │ 5-bit │ 7-bit │
         └───────┴─────┴─────┴─────┴──────┴─────────┘
```

### 5.3 RISC-V 示例代码

```asm
# 函数调用示例
# int add(int a, int b) { return a + b; }
add:
    add a0, a0, a1       # a0 = a0 + a1 (返回值)
    ret                   # 返回 (jalr zero, 0(ra))

# 数组求和
# int sum(int *arr, int n)
sum:
    addi sp, sp, -16      # 分配栈帧
    sw   ra, 12(sp)       # 保存返回地址
    sw   s0, 8(sp)        # 保存 s0
    mv   s0, a0           # s0 = arr
    li   t0, 0            # t0 = 0 (累加器)
    li   t1, 0            # t1 = 0 (索引)
loop:
    bge  t1, a1, done     # if (i >= n) goto done
    lw   t2, 0(s0)        # t2 = arr[i]
    add  t0, t0, t2       # sum += arr[i]
    addi s0, s0, 4        # arr++
    addi t1, t1, 1        # i++
    j    loop
done:
    mv   a0, t0           # 返回值 = sum
    lw   ra, 12(sp)       # 恢复返回地址
    lw   s0, 8(sp)        # 恢复 s0
    addi sp, sp, 16       # 释放栈帧
    ret
```

## 6. C/C++ 内联汇编

### 6.1 GCC 扩展内联汇编

```c
// 基本格式
asm volatile (
    "assembly template"
    : output operands    // 输出操作数
    : input operands     // 输入操作数
    : clobber list       // 被修改的寄存器/内存
);

// 示例: 原子比较交换
static inline uint64_t atomic_cmpxchg(uint64_t *ptr,
                                       uint64_t old,
                                       uint64_t new_val) {
    uint64_t result;
    asm volatile(
        "lock cmpxchg %[new_val], %[ptr]"
        : "=a"(result), [ptr] "+m"(*ptr)
        : "a"(old), [new_val] "r"(new_val)
        : "memory", "cc"
    );
    return result;
}

// 系统调用示例
static inline long syscall3(long num, long a1, long a2, long a3) {
    long ret;
    asm volatile(
        "syscall"
        : "=a"(ret)
        : "a"(num), "D"(a1), "S"(a2), "d"(a3)
        : "rcx", "r11", "memory"
    );
    return ret;
}

// 读取时间戳计数器
static inline uint64_t rdtsc(void) {
    uint32_t lo, hi;
    asm volatile(
        "rdtsc"
        : "=a"(lo), "=d"(hi)
    );
    return ((uint64_t)hi << 32) | lo;
}

// CPUID
static inline void cpuid(uint32_t leaf, uint32_t subleaf,
                          uint32_t *eax, uint32_t *ebx,
                          uint32_t *ecx, uint32_t *edx) {
    asm volatile(
        "cpuid"
        : "=a"(*eax), "=b"(*ebx), "=c"(*ecx), "=d"(*edx)
        : "a"(leaf), "c"(subleaf)
    );
}
```

### 6.2 操作数约束

```
通用约束:
  "r"  - 任意通用寄存器
  "m"  - 内存操作数
  "i"  - 立即数
  "n"  - 已知立即数
  "g"  - 通用 (寄存器/内存/立即数)

x86 特定约束:
  "a"  - RAX/EAX/AX/AL
  "b"  - RBX/EBX/BX/BL
  "c"  - RCX/ECX/CX/CL
  "d"  - RDX/EDX/DX/DL
  "S"  - RSI/ESI/SI/SIL
  "D"  - RDI/EDI/DI/DIL

修饰符:
  "="  - 只写 (覆盖原值)
  "+"  - 读写
  "&"  - earlyclobber (在输入消耗前被修改)
  "m"  - 内存引用 (volatile 常用)
```

## 7. GDB 调试汇编

### 7.1 常用命令

```bash
# 反汇编当前函数
(gdb) disassemble
(gdb) disassemble /m function_name    # 混合源码和汇编
(gdb) disassemble /r function_name    # 显示原始字节

# 单步执行汇编指令
(gdb) stepi           # si: 单步进入
(gdb) nexti           # ni: 单步跳过
(gdb) si 10           # 执行10条指令

# 查看寄存器
(gdb) info registers
(gdb) info registers rax rbx rcx
(gdb) print/x $rax    # 十六进制显示
(gdb) p/t $rax        # 二进制显示

# 设置汇编显示模式
(gdb) set disassembly-flavor intel
(gdb) display/i $pc   # 每次停止显示当前指令

# 在地址设置断点
(gdb) break *0x401000
(gdb) break *main+50

# 查看内存
(gdb) x/10gx $rsp     # 查看栈 (10个8字节十六进制)
(gdb) x/20i $pc       # 查看后续20条指令
(gdb) x/s 0x402000    # 查看字符串
```

### 7.2 调试技巧

```bash
# 查看调用栈（汇编级别）
(gdb) info frame
(gdb) backtrace
(gdb) frame 2

# 监视内存变化
(gdb) watch *(int*)0x601050
(rwatch *(int*)0x601050    # 读监视

# 查看栈帧内容
(gdb) x/30gx $rbp
# 高地址
# [rbp+8]:  返回地址
# [rbp]:    旧rbp
# [rbp-8]:  局部变量1
# [rbp-16]: 局部变量2
```

## 8. 实战示例

### 8.1 函数序言与尾声 (System V ABI)

```nasm
; void function(int a, int b, int c, int d, int e, int f, int g)
; 参数: a=RDI, b=ESI, c=RDX, d=ECX, e=R8D, f=R9D, g=[RSP+8]
function:
    ; === 序言 (Prologue) ===
    push rbp                ; 保存帧指针
    mov  rbp, rsp           ; 建立新帧指针
    sub  rsp, 64            ; 分配局部变量空间
    mov  [rbp-8], rbx       ; 保存 callee-saved 寄存器
    mov  [rbp-16], r12
    mov  [rbp-24], r13

    ; === 函数体 ===
    ; 处理参数...
    add  edi, esi           ; a + b
    mov  eax, edi           ; 返回值

    ; === 尾声 (Epilogue) ===
    mov  rbx, [rbp-8]       ; 恢复 callee-saved 寄存器
    mov  r12, [rbp-16]
    mov  r13, [rbp-24]
    mov  rsp, rbp           ; 释放局部变量
    pop  rbp                ; 恢复帧指针
    ret
```

### 8.2 数组遍历与求和

```nasm
; int64_t array_sum(const int64_t *arr, size_t count)
; RDI = arr, RSI = count
; 返回值: RAX
array_sum:
    xor  eax, eax           ; sum = 0
    test rsi, rsi           ; if (count == 0)
    jz   .done              ;   return 0
    xor  ecx, ecx           ; i = 0
.loop:
    add  rax, [rdi + rcx*8] ; sum += arr[i]
    inc  rcx                ; i++
    cmp  rcx, rsi           ; if (i < count)
    jb   .loop              ;   continue
.done:
    ret

; 向量化版本 (使用 SSE2)
array_sum_sse2:
    pxor   xmm0, xmm0       ; sum = {0, 0, 0, 0}
    test   rsi, rsi
    jz     .done
.loop:
    paddq  xmm0, [rdi]      ; 累加两个64位整数
    add    rdi, 16           ; arr += 2
    sub    rsi, 2
    ja     .loop
    ; 水平归约
    pshufd xmm1, xmm0, 0x4E ; 交换高低64位
    paddq  xmm0, xmm1       ; 相加
    movq   rax, xmm0        ; 提取结果
.done:
    ret
```

### 8.3 字符串操作

```nasm
; size_t strlen(const char *s)
; RDI = s
strlen:
    mov  rcx, -1            ; 最大计数
    xor  al, al             ; 搜索 '\0'
    repne scasb             ; 扫描直到找到零字节
    lea  rax, [rdi-1]       ; 计算长度
    sub  rax, rcx
    sub  rax, 2
    ret

; void *memcpy(void *dst, const void *src, size_t n)
; RDI = dst, RSI = src, RDX = n
memcpy_fast:
    mov  rcx, rdx
    rep  movsb              ; 逐字节复制
    mov  rax, rdi           ; 返回 dst
    ret

; 使用 AVX-512 的快速内存复制
memcpy_avx512:
    cmp  rdx, 64
    jb   .small
.loop:
    vmovdqu8 zmm0, [rsi]
    vmovdqu8 [rdi], zmm0
    add  rsi, 64
    add  rdi, 64
    sub  rdx, 64
    cmp  rdx, 64
    jae  .loop
.small:
    mov  rcx, rdx
    rep  movsb
    mov  rax, rdi
    ret
```

### 8.4 条件分支优化

```nasm
; 分支版本
max_branch:
    cmp  rdi, rsi
    jg   .greater
    mov  rax, rsi
    ret
.greater:
    mov  rax, rdi
    ret

; 无分支版本 (使用 CMOV)
max_branchless:
    mov  rax, rsi           ; 假设 rsi >= rdi
    cmp  rdi, rsi
    cmovg rax, rdi          ; 如果 rdi > rsi, 选择 rdi
    ret
```

## 9. 性能考量

### 9.1 指令延迟与吞吐量

```
典型延迟 (Skylake 级别):
┌──────────────┬────────┬──────────┐
│ 指令         │ 延迟   │ 吞吐量   │
├──────────────┼────────┼──────────┤
│ MOV reg,reg  │ 1      │ 0.25     │
│ ADD/SUB      │ 1      │ 0.25     │
│ IMUL r,r     │ 3      │ 1        │
│ IDIV r       │ 26-90  │ 26-90    │
│ LEA (simple) │ 1      │ 0.5      │
│ LEA (complex)│ 3      │ 1        │
│ FADD         │ 4      │ 0.5      │
│ FMUL         │ 4      │ 0.5      │
└──────────────┴────────┴──────────┘
```

### 9.2 常见优化技巧

```nasm
; 避免 DIV - 用乘法替代
; a / 10 → a * 0xCCCCCCCD >> 35
mov  eax, edi
mov  ecx, 0xCCCCCCCD
imul rcx, rax
shr  rcx, 35        ; 结果在 ECX

; 避免分支
; x = (a > b) ? a : b
cmp  edi, esi
setg al              ; al = (a > b) ? 1 : 0
movzx eax, al
; 或使用 CMOV

; 循环展开
; 原始: for(i=0; i<n; i++) sum += arr[i]
; 展开4次:
.loop:
    add rax, [rdi]
    add rax, [rdi+8]
    add rax, [rdi+16]
    add rax, [rdi+24]
    add rdi, 32
    sub rcx, 4
    ja  .loop
```
