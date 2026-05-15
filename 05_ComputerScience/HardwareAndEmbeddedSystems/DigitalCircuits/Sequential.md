---
aliases: [Sequential]
tags: ['HardwareAndEmbeddedSystems', 'DigitalCircuits', 'Sequential']
---

# 时序逻辑电路

## 锁存器 (Latches)

### SR 锁存器 (NAND 实现)

| S | R | Q | Q' | 状态 |
|---|---|----|----|------|
| 1 | 1 | Q0 | Q0' | 保持 |
| 1 | 0 | 0 | 1 | 复位 |
| 0 | 1 | 1 | 0 | 置位 |
| 0 | 0 | 1 | 1 | 禁止 (不定) |

### SR 锁存器 (NOR 实现)

| S | R | Q | Q' | 状态 |
|---|---|----|----|------|
| 0 | 0 | Q0 | Q0' | 保持 |
| 0 | 1 | 0 | 1 | 复位 |
| 1 | 0 | 1 | 0 | 置位 |
| 1 | 1 | 0 | 0 | 禁止 (不定) |

### D 锁存器 (Gated Latch)

| E | D | Q | 功能 |
|---|---|----|------|
| 0 | X | Q0 | 保持 |
| 1 | 0 | 0 | 透明 (传输 0) |
| 1 | 1 | 1 | 透明 (传输 1) |

当使能信号 E=1 时，D 锁存器是透明的 (输出随输入变化)。

## 触发器 (Flip-Flops)

### 边沿触发 vs 电平敏感

- **电平敏感** (Latch): 在使能信号有效期间都透明
- **边沿触发** (Flip-Flop): 仅在时钟边沿 (上升沿或下降沿) 采样输入

### D 触发器

**特性表**:

| CLK | D | Q_next | 功能 |
|-----|---|--------|------|
| ↑ | 0 | 0 | 复位 |
| ↑ | 1 | 1 | 置位 |
| 其他 | X | Q0 | 保持 |

**激励表**:

| Q | Q_next | D |
|---|---|---|
| 0 | 0 | 0 |
| 0 | 1 | 1 |
| 1 | 0 | 0 |
| 1 | 1 | 1 |

**时序图**:
```
CLK  ┌┐  ┌┐  ┌┐  ┌┐  ┌┐  ┌┐
     ┘ └──┘ └──┘ └──┘ └──┘ └
D    ────┐   ┌───────────┐
         └───┘           └──────
Q    ──────┐   ┌─────────────
           └───┘
```

### JK 触发器

**特性表**:

| CLK | J | K | Q_next | 功能 |
|-----|---|---|--------|------|
| ↑ | 0 | 0 | Q0 | 保持 |
| ↑ | 0 | 1 | 0 | 复位 |
| ↑ | 1 | 0 | 1 | 置位 |
| ↑ | 1 | 1 | Q0' | 翻转 |

**激励表**:

| Q | Q_next | J | K |
|---|---|---|---|
| 0 | 0 | 0 | X |
| 0 | 1 | 1 | X |
| 1 | 0 | X | 1 |
| 1 | 1 | X | 0 |

### T 触发器

**特性表**:

| CLK | T | Q_next |
|-----|---|--------|
| ↑ | 0 | Q0 |
| ↑ | 1 | Q0' |

T 触发器常用于计数器 (T=1 时每时钟翻转一次)。

### 触发器类型对比

| 类型 | 输入 | 特性 |
|------|------|------|
| D | D | Q_next = D，最常用，适合寄存器 |
| JK | J, K | 功能最全，无禁止态 |
| T | T | T=1 翻转，适合计数器 |
| SR | S, R | 有禁止态 (S=R=1) |

## 寄存器 (Registers)

### 移位寄存器 (Shift Register)

```
串行输入 → [FF0] → [FF1] → [FF2] → [FF3] → 串行输出
             Q0      Q1      Q2      Q3
```

```verilog
module shift_reg #(parameter N=8) (
    input clk, rst, sin,
    output reg [N-1:0] q
);
    always @(posedge clk) begin
        if (rst)
            q <= 0;
        else
            q <= {q[N-2:0], sin};
    end
endmodule
```

### 移位寄存器类型

| 类型 | 输入 | 输出 | 描述 |
|------|------|------|------|
| SISO | 串行 | 串行 | 串入串出，用于延时 |
| SIPO | 串行 | 并行 | 串入并出，用于串行转并行 |
| PISO | 并行 | 串行 | 并入串出，用于并行转串行 |
| PIPO | 并行 | 并行 | 并入并出，普通寄存器 |

### 双向移位寄存器

```verilog
module bidirectional_shift (
    input clk, rst, dir, sin,
    input [3:0] parallel_in,
    input load,
    output reg [3:0] q
);
    always @(posedge clk) begin
        if (rst)
            q <= 4'b0000;
        else if (load)
            q <= parallel_in;
        else if (dir)  // 左移
            q <= {q[2:0], sin};
        else            // 右移
            q <= {sin, q[3:1]};
    end
endmodule
```

## 计数器 (Counters)

### 异步计数器 (波纹计数器)

```
CLK → [FF0] → [FF1] → [FF2] → [FF3]
        Q0      Q1      Q2      Q3
```

每个触发器的输出作为下一级的时钟，延迟累积。

```
延迟 ≈ N × t_prop (N 为位数)
```

### 同步计数器

所有触发器共用同一时钟，延迟固定 (与位数无关)。

```verilog
// 4位同步二进制计数器
module counter_sync (
    input clk, rst, en,
    output reg [3:0] q
);
    always @(posedge clk) begin
        if (rst)
            q <= 4'b0000;
        else if (en)
            q <= q + 1;
    end
endmodule
```

### 加减计数器 (Up/Down Counter)

```verilog
module updown_counter (
    input clk, rst, up,
    output reg [3:0] q
);
    always @(posedge clk) begin
        if (rst)
            q <= 4'b0000;
        else if (up)
            q <= q + 1;    // 加计数
        else
            q <= q - 1;    // 减计数
    end
endmodule
```

### BCD 计数器 (模10)

```verilog
module bcd_counter (
    input clk, rst,
    output reg [3:0] q,
    output carry
);
    assign carry = (q == 4'b1001);

    always @(posedge clk) begin
        if (rst)
            q <= 4'b0000;
        else if (carry)
            q <= 4'b0000;
        else
            q <= q + 1;
    end
endmodule
```

### 约翰逊计数器 (Johnson Counter)

环形移位寄存器，最后一级的反相输出反馈到第一级。

```
初始: 0000
序列: 0000 → 1000 → 1100 → 1110 → 1111 → 0111 → 0011 → 0001 → 0000...
```

特点: N 级产生 2N 种状态，译码简单 (每状态只有一个输出变化)。

### 环形计数器 (Ring Counter)

```
初始: 1000
序列: 1000 → 0100 → 0010 → 0001 → 1000...
```

特点: N 级产生 N 种状态，每次只有一个输出有效。

### 模 N 计数器 (Modulo-N Counter)

```verilog
// 模 60 计数器 (BCD 秒计数器)
module mod60_counter (
    input clk, rst,
    output reg [3:0] tens,    // 十位 (0-5)
    output reg [3:0] ones,    // 个位 (0-9)
    output carry
);
    assign carry = (tens == 5 && ones == 9);

    always @(posedge clk) begin
        if (rst) begin
            tens <= 0;
            ones <= 0;
        end else if (carry) begin
            tens <= 0;
            ones <= 0;
        end else if (ones == 9) begin
            ones <= 0;
            tens <= tens + 1;
        end else begin
            ones <= ones + 1;
        end
    end
endmodule
```

## 频率分频器 (Frequency Divider)

| 分频比 | 触发器数 | 实现方式 |
|--------|---------|----------|
| 2分频 | 1 | 1个T触发器 (Q0翻转) |
| 4分频 | 2 | 2级TFF级联 |
| N分频 | log₂N | 计数器 + 译码复位 |
| 非2^n分频 | 取决于设计 | 模N计数器 |

```verilog
// 通用分频器
module divider #(parameter N = 100) (
    input clk, rst,
    output reg out
);
    reg [$clog2(N)-1:0] count;

    always @(posedge clk) begin
        if (rst || count == N/2 - 1) begin
            count <= 0;
            out <= ~out;
        end else begin
            count <= count + 1;
        end
    end
endmodule
```

## 时序参数

| 参数 | 符号 | 定义 |
|------|------|------|
| 建立时间 | t_su | 数据在时钟沿之前必须保持稳定的最短时间 |
| 保持时间 | t_h | 数据在时钟沿之后必须保持稳定的最长时间 |
| 传输延迟 | t_prop | 时钟沿到输出变化的时间 |
| 最小时钟周期 | T_min | 允许的最小时钟周期 = t_prop + t_su + 布线延迟 |
| 最高频率 | F_max | 1 / T_min |

## 同步与异步设计

### 同步复位

```verilog
always @(posedge clk)
    if (rst) q <= 0;   // 仅在时钟沿复位
```

### 异步复位

```verilog
always @(posedge clk or posedge rst)
    if (rst) q <= 0;   // 立即复位 (不受时钟控制)
```

### 亚稳态 (Metastability)

当建立/保持时间不满足时，触发器的输出可能进入不确定状态。

**解决方法**: 
- 使用两级同步器 (2-FF synchronizer)
- 降低时钟频率
- 使用边沿检测器
