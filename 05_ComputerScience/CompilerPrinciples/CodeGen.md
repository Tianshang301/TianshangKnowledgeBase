# 目标代码生成

## 一、概述

代码生成是编译器的最后阶段，将优化后的中间代码（IR）转换为目标机器的汇编代码或机器码。

### 代码生成面临的问题

1. **指令选择**：选择合适的目标指令序列
2. **寄存器分配**：管理有限的物理寄存器
3. **指令调度**：重排指令以利用流水线
4. **调用约定**：函数调用的参数传递、栈帧管理

---

## 二、指令选择

### 树模式匹配 (Tree Pattern Matching)

将 IR 表示成树，用树重写规则匹配目标指令。

```text
IR 树：
        +
       / \
      a   *
         / \
        b   c

目标指令：
add r1, r2, r3    // r1 = r2 + r3
mul r1, r2, r3    // r1 = r2 * r3

匹配结果：
mul t1, b, c
add t2, a, t1
```

### 平铺 (Tiling)

将 IR 平铺成指令序列，每个图块对应一条目标指令。

```asm
// IR: a + b * c
// 方法1（简单平铺）
mov t1, b
mul t1, c
mov t2, a
add t2, t1

// 方法2（更好的平铺，利用 x86 的复杂指令）
mov t1, a
add t1, b * c    // 一条指令完成乘加（如果目标支持）
```

### 指令选择示例

```c
// 源代码
int f(int a, int b, int c) {
    return a + b * c;
}
```

**x86-64 汇编**：

```asm
f:
    imull   %edx, %esi      ; b * c → esi (Intel: esi = esi * edx)
    leal    (%rdi, %rsi), %eax  ; a + (b*c) → eax
    ret
```

**ARM64 汇编**：

```asm
f:
    mul     w1, w1, w2      ; b * c → w1
    add     w0, w0, w1      ; a + (b*c) → w0
    ret
```

**RISC-V 汇编**：

```asm
f:
    mul     t0, a1, a2      ; b * c → t0
    add     a0, a0, t0      ; a + (b*c) → a0
    ret
```

---

## 三、寄存器分配

### 寄存器溢出 (Register Spilling)

当物理寄存器不足时，将变量临时存储到内存（栈）。

```asm
// 假设只有 2 个可用寄存器：r0, r1
// 需要处理 4 个变量：a, b, c, d

// 溢出策略：
mov r0, a        // a → r0
mov r1, b        // b → r1
add r0, r0, r1   // r0 = a + b

// 需要 c 和 d，但寄存器已满
// 将 a+b 的结果溢出到栈
store r0, [sp+0] // 保存临时结果

mov r0, c        // c → r0
mov r1, d        // d → r1
add r1, r0, r1   // r1 = c + d

// 恢复之前的结果
load r0, [sp+0]  // 恢复 a+b
add r0, r0, r1   // r0 = (a+b) + (c+d)
```

### 调用约定 (Calling Convention)

**x86-64 System V ABI（Linux, macOS）**：

```asm
// 参数传递：
//   整数/指针: rdi, rsi, rdx, rcx, r8, r9
//   浮点数:    xmm0-xmm7
//   额外参数:  栈（从右到左压栈）

// 返回值：
//   整数/指针: rax
//   浮点数:    xmm0

// 被调用者保存：rbx, rbp, r12-r15
// 调用者保存：其他寄存器

// 示例：int f(int a, int b, int c, int d)
// a → rdi, b → rsi, c → rdx, d → rcx
f:
    push    rbp           ; 保存栈帧基址
    mov     rbp, rsp      ; 设置栈帧
    mov     eax, edi      ; a
    add     eax, esi      ; + b
    imul    eax, edx      ; * c
    sub     eax, ecx      ; - d
    pop     rbp           ; 恢复栈帧
    ret
```

**ARM64 AAPCS**：

```asm
// 参数传递：x0-x7（整数/指针），v0-v7（浮点数）
// 返回值：x0（整数），v0（浮点数）
// 被调用者保存：x19-x29
// 调用者保存：x0-x18

f:
    add     w0, w0, w1    ; a + b
    mul     w0, w0, w2    ; * c
    sub     w0, w0, w3    ; - d
    ret
```

---

## 四、指令调度

### 流水线 (Pipeline)

现代 CPU 将指令执行分为多个阶段：

```
IF (取指) → ID (译码) → EX (执行) → MEM (访存) → WB (写回)
```

**无调度**（有数据冒险）：

```asm
// 每条指令必须等待上一条完成
add r1, r2, r3    ; IF ID EX MEM WB
add r4, r1, r5    ;    IF ID 等待 1,2 等待...
                    ;       IF ID (r1 不可用) ... EX MEM WB
```

**调度后**（插入指令消除冒险）：

```asm
// 编译器重排指令，在依赖指令间插入无关指令
ldr r1, [sp+0]    ; 加载内存 → r1（耗时较长）
add r2, r3, r4    ; 无关计算（利用等待时间）
add r5, r1, r6    ; 此时 r1 已就绪
```

### 列表调度 (List Scheduling)

```
1. 构建数据依赖图（DAG）
2. 计算每个节点的优先级（路径长度）
3. 维护"就绪队列"（所有依赖已满足的节点）
4. 从就绪队列中选择最高优先级的节点
5. 调度该节点，更新就绪队列
6. 重复直到所有节点被调度
```

```asm
// 数据依赖图
add r1, r2, r3    ────────▶  sub r4, r1, r5
                                │
ldr r6, [sp+0]    ────────────▶  add r7, r6, r8

// 就绪顺序：
// 初始就绪: add r1, ldr r6
// 优先级: ldr（长延迟）先发出
// 调度: ldr r6 → add r1 → sub r4 → ... 或 add r1 → ldr r6 → sub r4
```

### 软件流水线 (Software Pipelining)

通过重叠不同迭代的执行来优化循环。

```asm
// 原始循环
loop:
    ld    r1, [a+i]       ; 加载
    mul   r2, r1, 2       ; 运算
    st    [b+i], r2       ; 存储
    add   i, i, 1
    cmp   i, n
    jl    loop

// 软件流水线后的循环
    ld    r1_0, [a+i]       ; 加载迭代 0
    add   i, i, 1
loop:
    ld    r1_1, [a+i]       ; 加载迭代 n+1
    mul   r2_0, r1_0, 2     ; 运算迭代 n
    st    [b+i-1], r2_0     ; 存储迭代 n
    add   i, i, 1
    cmp   i, n-1
    jl    loop
    // 收尾
    mul   r2_last, r1_1, 2
    st    [b+n-1], r2_last
```

---

## 五、栈帧管理

### 函数调用栈帧

```asm
; x86-64 栈帧布局
; 高地址
    ┌───────────────────┐
    │ 调用者栈帧         │
    │ ...               │
    │ 参数 N            │  ← rbp + 24
    │ 参数 7            │  ← rbp + 16
    │ 返回地址          │  ← rbp + 8
    ├───────────────────┤
    │ 保存的 rbp        │  ← rbp
    ├───────────────────┤
    │ 局部变量          │  ← rbp - 8, rbp - 16, ...
    │ 临时变量          │
    │ 溢出寄存器        │
    ├───────────────────┤
    │ 参数区（参数 1-6）│  ← rsp
    │ 用于调用其他函数  │
    ; 低地址   └───────────────────┘
```

### 栈帧代码生成

```asm
; 函数 prologue（序言）
f:
    push    rbp            ; 保存调用者的栈帧基址
    mov     rbp, rsp       ; 设置自己的栈帧
    sub     rsp, 32        ; 分配 32 字节局部变量空间

; 函数体
    mov     [rbp-8], edi   ; 保存参数 a
    mov     [rbp-12], esi  ; 保存参数 b
    mov     eax, [rbp-8]   ; 加载 a
    add     eax, [rbp-12]  ; a + b
    mov     [rbp-4], eax   ; 本地变量 c

; 函数 epilogue（尾声）
    mov     eax, [rbp-4]   ; 返回值
    mov     rsp, rbp       ; 恢复 rsp
    pop     rbp            ; 恢复 rbp
    ret                    ; 返回
```

### 不同语言的调用约定

```asm
; C/Go: 调用者清理参数
; Pascal/fastcall: 被调用者清理参数

; x86 cdecl（32位 C）：
push    arg3
push    arg2
push    arg1
call    func
add     sp, 12            ; 调用者清理

; x86 stdcall（Windows API）：
push    arg3
push    arg2
push    arg1
call    func              ; func 内部用 ret 12 清理
```

---

## 六、表达式与结构代码生成

### 表达式求值

```asm
; a = b + c * d
; 简单方法（很多临时变量）
    mov     t1, c
    mul     t1, d
    mov     t2, b
    add     t2, t1
    mov     a, t2

; 优化方法（更少的临时变量，假设可用寄存器）
    mov     eax, c
    imul    eax, d        ; eax = c*d
    add     eax, b        ; eax = b + c*d
    mov     a, eax        ; a = eax
```

### 控制结构

```asm
; if (x > 0) { y = 1; } else { y = -1; }
    cmp     x, 0
    jle     .L_else
    mov     y, 1
    jmp     .L_end
.L_else:
    mov     y, -1
.L_end:
    ; continue

; while (i < n) { sum += i; i++; }
.L_loop:
    cmp     i, n
    jge     .L_exit
    mov     eax, sum
    add     eax, i
    mov     sum, eax
    inc     i
    jmp     .L_loop
.L_exit:
    ; continue

; for 循环翻译
; for (i = 0; i < n; i++) { body; }
    mov     i, 0
    jmp     .L_cond
.L_loop:
    ; body
    inc     i
.L_cond:
    cmp     i, n
    jl      .L_loop
.L_exit:
```

### 数组访问

```asm
; int a[N];
; a[i] = a[i] * 2;
; 地址 = base + i * 4
    mov     eax, i
    shl     eax, 2           ; i * 4 (移位替代乘法)
    mov     ecx, [a + eax]   ; 读取 a[i]
    shl     ecx, 1           ; * 2
    mov     [a + eax], ecx   ; 写入 a[i]
```

### 函数调用

```asm
; result = foo(a, b, c);
    ; 准备参数
    mov     edi, a           ; 参数 1
    mov     esi, b           ; 参数 2
    mov     edx, c           ; 参数 3
    call    foo              ; 调用函数
    mov     result, eax      ; 获取返回值

; 函数本身
foo:
    push    rbp
    mov     rbp, rsp
    ; 函数体——使用参数 edi, esi, edx
    mov     eax, edi
    add     eax, esi
    imul    eax, edx         ; return (a+b)*c
    pop     rbp
    ret
```
