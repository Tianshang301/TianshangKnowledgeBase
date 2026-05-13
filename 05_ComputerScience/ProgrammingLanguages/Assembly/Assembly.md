# 汇编语言

## 一、汇编语言基础

汇编语言是机器码的符号化表示，每条汇编指令对应一条机器指令。程序由以下元素组成：

| 元素 | 说明 | 示例 |
|------|------|------|
| 标签（Label） | 地址的符号名 | `start:` |
| 指令（Mnemonic） | 操作码 | `mov, add, sub` |
| 操作数（Operand） | 指令的操作对象 | `eax, 42` |
| 伪指令（Directive） | 给汇编器的指示 | `db, dw, resb` |
| 注释（Comment） | 说明信息 | `; 注释` |

## 二、x86 架构

### 寄存器

| 寄存器 | 32 位 | 16 位 | 8 位高/低 | 用途 |
|--------|-------|-------|-----------|------|
| 累加器 | EAX | AX | AH/AL | 算术、I/O |
| 基址 | EBX | BX | BH/BL | 基址寻址 |
| 计数 | ECX | CX | CH/CL | 循环、移位 |
| 数据 | EDX | DX | DH/DL | I/O、乘法 |
| 源变址 | ESI | SI | — | 字符串操作源 |
| 目的变址 | EDI | DI | — | 字符串操作目标 |
| 基址指针 | EBP | BP | — | 栈帧基址 |
| 栈指针 | ESP | SP | — | 栈顶指针 |
| 指令指针 | EIP | IP | — | 程序计数器 |
| 标志 | EFLAGS | FLAGS | — | 状态标志 |

### 标志寄存器

| 标志位 | 名称 | 作用 |
|--------|------|------|
| ZF | 零标志 | 结果为 0 置位 |
| CF | 进位标志 | 算术进位/借位 |
| SF | 符号标志 | 结果为负置位 |
| OF | 溢出标志 | 有符号溢出 |
| PF | 奇偶标志 | 低 8 位 1 的个数为偶 |
| IF | 中断使能 | 允许/禁止可屏蔽中断 |

### 内存分段

| 段 | 用途 | 默认寄存器 |
|----|------|-----------|
| 代码段 (CS) | 存放指令 | EIP |
| 数据段 (DS) | 存放数据 | EAX, EBX, ECX, EDX |
| 栈段 (SS) | 栈操作 | ESP, EBP |
| 附加段 (ES/FS/GS) | 额外数据 | 变址寄存器 |

## 三、指令集

### 数据传送

```assembly
mov  eax, 42        ; 立即数 → 寄存器
mov  eax, ebx       ; 寄存器 → 寄存器
mov  eax, [ebx]     ; 内存 → 寄存器（间接寻址）
mov  [eax], ebx     ; 寄存器 → 内存
xchg eax, ebx       ; 交换
push eax            ; 压栈
pop  eax            ; 出栈
lea  eax, [ebx+ecx] ; 加载有效地址
```

### 算术运算

```assembly
add  eax, ebx       ; eax = eax + ebx
sub  eax, ebx       ; eax = eax - ebx
inc  eax            ; eax++
dec  eax            ; eax--
mul  ebx            ; edx:eax = eax * ebx (无符号)
div  ebx            ; eax = edx:eax / ebx, edx = 余数
imul eax, ebx       ; eax = eax * ebx (有符号)
```

### 逻辑与移位

```assembly
and  eax, ebx       ; 按位与
or   eax, ebx       ; 按位或
xor  eax, ebx       ; 按位异或
not  eax            ; 按位取反

shl  eax, 1         ; 左移 1 位（乘以 2）
shr  eax, 1         ; 右移 1 位（除以 2）
sal  eax, cl        ; 算术左移 cl 位
sar  eax, cl        ; 算术右移 cl 位
```

### 控制转移

```assembly
jmp  label          ; 无条件跳转
je   label          ; ZF=1 则跳转
jne  label          ; ZF=0 则跳转
jg   label          ; 大于（有符号）
jl   label          ; 小于（有符号）
jge  label          ; 大于等于
jle  label          ; 小于等于
ja   label          ; 大于（无符号，CF=0 且 ZF=0）
jb   label          ; 小于（无符号，CF=1）

call func           ; 调用函数
ret                 ; 返回
ret  8              ; 返回并清理 8 字节参数
```

## 四、寻址模式

| 寻址模式 | 示例 | 有效地址 |
|---------|------|---------|
| 立即数 | `mov eax, 42` | 42（值本身） |
| 寄存器 | `mov eax, ebx` | EBX |
| 直接 | `mov eax, [0x1000]` | 0x1000 |
| 基址变址 | `mov eax, [ebx+ecx]` | EBX + ECX |
| 比例变址 | `mov eax, [ebx+ecx*4]` | EBX + ECX × 4 |
| 基址比例变址位移 | `mov eax, [ebx+ecx*4+8]` | EBX + ECX × 4 + 8 |

通用格式：`[base + index × scale + displacement]`

## 五、栈操作与函数调用

### 调用约定

| 约定 | 参数传递 | 清理者 | 返回值 |
|------|---------|--------|--------|
| cdecl | 从右到左压栈 | 调用者 | EAX |
| stdcall | 从右到左压栈 | 被调者 | EAX |
| fastcall | ECX/EDX 传前两个参数，其余压栈 | 被调者 | EAX |

```assembly
; cdecl 调用示例
push  dword 3       ; 参数 2
push  dword 2       ; 参数 1
call  add_func
add   esp, 8        ; 调用者清理栈

; 函数定义
add_func:
    push ebp
    mov  ebp, esp       ; 建立栈帧
    mov  eax, [ebp+8]   ; 参数 1
    add  eax, [ebp+12]  ; 参数 2
    pop  ebp
    ret                 ; cdecl: 调用者清理
```

## 六、中断

```assembly
; Linux 系统调用 (int 0x80)
mov  eax, 4         ; sys_write
mov  ebx, 1         ; stdout
mov  ecx, msg       ; 字符串地址
mov  edx, len       ; 长度
int  0x80           ; 调用内核

; DOS 系统调用 (int 21h)
mov  ah, 09h        ; 显示字符串
mov  dx, msg        ; 字符串地址
int  21h
```

## 七、x86-64 差异

| 特性 | x86 (32 位) | x86-64 |
|------|------------|--------|
| 通用寄存器 | 8 个 (EAX-EDX, ESI, EDI, EBP, ESP) | 16 个 (RAX-RDX, RSI, RDI, RBP, RSP, R8-R15) |
| 寄存器宽度 | 32 位 | 64 位 |
| 地址空间 | 4 GB | 64 TB (实际) |
| 指令指针 | EIP | RIP |
| 相对寻址 | — | RIP-relative 寻址 |

### 调用约定差异

| 平台 | 参数传递方式 | 说明 |
|------|-------------|------|
| Linux (System V AMD64) | RDI, RSI, RDX, RCX, R8, R9, 然后栈 | 前 6 个整数参数用寄存器 |
| Windows x64 | RCX, RDX, R8, R9, 然后栈 | 前 4 个参数用寄存器 |

## 八、NASM vs MASM

| 特性 | NASM | MASM |
|------|------|------|
| 平台 | 跨平台 | Windows |
| 大小写 | 区分 | 不区分 |
| 内存引用 | `[eax]` | `[eax]` 或 `eax` |
| 立即数前缀 | 无 | 无（`42`） |
| 变量定义 | `var db 42` | `var db 42` |
| 段定义 | `SECTION .text` | `.code` |
| 宏 | `%define` | `EQU`/`TEXTEQU` |

## 九、内联汇编

### GCC 扩展内联汇编

```c
int result;
int a = 10, b = 20;

asm volatile (
    "addl %1, %0"
    : "=r" (result)    // 输出操作数
    : "r" (a), "0" (b) // 输入操作数
    : "cc"             // 影响的资源
);

// 带 clobber 的 syscall
asm volatile (
    "int $0x80"
    : "=a" (result)
    : "a" (4), "b" (1), "c" (msg), "d" (len)
);
```

### MSVC 内联汇编 (x86 限定)

```c
int result;
__asm {
    mov eax, 10
    add eax, 20
    mov result, eax
}
```

## 十、逆向工程基础

逆向工程通过反汇编和调试分析程序行为和协议：

- **静态分析**：使用 IDA Pro、Ghidra、radare2 反汇编
- **动态调试**：使用 GDB、x64dbg、OllyDbg 单步执行
- **常见分析目标**：验证算法、协议逆向、恶意软件分析、漏洞挖掘

```bash
# Linux 反汇编
objdump -d program    # 反汇编可执行文件
gdb ./program         # 调试
(gdb) disas main      # 反汇编 main 函数

# 查看实际机器码
xxd program.bin | head -20
```

## 相关条目

- ComputerOrganization
- [[05_ComputerScience/CompilerPrinciples/INDEX|CompilerPrinciples]]
- ReverseEngineering
- EmbeddedSystems

## 参考资源

- 《汇编语言》（王爽）— 经典入门教材
- 《x86 Assembly Language and C Fundamentals》（Joseph Cavanagh）
- Intel 64 and IA-32 Architectures Software Developer Manuals
- [NASM 文档](https://www.nasm.us/doc/)
- [x86-64 System V ABI](https://github.com/hjl-tools/x86-psABI/wiki/X86-psABI)
- [Ghidra 逆向工程工具](https://ghidra-sre.org/)
