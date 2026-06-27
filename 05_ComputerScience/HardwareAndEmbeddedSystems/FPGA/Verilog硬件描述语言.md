---
aliases: [Verilog 硬件描述语言]
tags: ['HardwareAndEmbeddedSystems', 'FPGA', 'Verilog']
---

# Verilog 硬件描述语言

## 一、Verilog 语言基础

Verilog HDL 用于数字电路的设计与建模，自1995年成为 IEEE 标准（IEEE 1364）。

设计流程：

```
需求分析 -> 架构设计 -> RTL 编码 -> 功能仿真 -> 综合 -> 布局布线 -> 时序分析 -> 比特流生成 -> 下载配置
```

模块基本结构：

```verilog
module counter (
    input  wire       clk,
    input  wire       reset_n,
    input  wire       enable,
    output reg  [7:0] count,
    output reg        overflow
);

always @(posedge clk or negedge reset_n) begin
    if (!reset_n) begin
        count    <= 8'b0;
        overflow <= 1'b0;
    end else if (enable) begin
        if (count == 8'hFF) begin
            count    <= 8'b0;
            overflow <= 1'b1;
        end else begin
            count    <= count + 1'b1;
            overflow <= 1'b0;
        end
    end
end

endmodule
```

## 二、数据类型与运算符

Verilog 主要数据类型：

| 类型 | 含义 | 位宽定义 | 默认值 |
|------|------|----------|--------|
| wire | 连线 | 默认1位 | Z |
| reg | 寄存器 | 默认1位 | X |
| integer | 32位有符号整数 | 固定32位 | X |
| parameter | 常量参数 | 用户定义 | - |
| localparam | 局部常量 | 用户定义 | - |

运算符优先级：

$$
\begin{aligned}
&1: \{\} \quad \text{(拼接)} \\
&2: * / \% \quad \text{(算术)} \\
&3: + - \quad \text{(算术)} \\
&4: << >> \quad \text{(移位)} \\
&5: < <= > >= \quad \text{(关系)} \\
&6: == != === !== \quad \text{(相等)} \\
&7: \& \quad \text{(按位与)} \\
&8: \wedge \quad \text{(按位异或)} \\
&9: | \quad \text{(按位或)} \\
&10: \&\& \quad \text{(逻辑与)} \\
&11: || \quad \text{(逻辑或)}
\end{aligned}
$$

## 三、组合逻辑电路

使用 `assign` 连续赋值实现组合逻辑：

```verilog
// 全加器
module full_adder (
    input  wire a, b, cin,
    output wire sum, cout
);
    assign {cout, sum} = a + b + cin;
endmodule

// 4-16译码器
module decoder_4to16 (
    input  wire [3:0] in,
    input  wire       enable,
    output reg  [15:0] out
);

always @(*) begin
    out = 16'b0;
    if (enable)
        out = 1'b1 << in;
end

endmodule

// 多路选择器
module mux_4to1 #(
    parameter WIDTH = 8
) (
    input  wire [1:0]         sel,
    input  wire [WIDTH-1:0]  d0, d1, d2, d3,
    output reg  [WIDTH-1:0]  y
);

always @(*) begin
    case (sel)
        2'b00:   y = d0;
        2'b01:   y = d1;
        2'b10:   y = d2;
        2'b11:   y = d3;
        default: y = {WIDTH{1'bx}};
    endcase
end

endmodule
```

## 四、时序逻辑电路

时序逻辑依赖时钟边沿触发：

```verilog
// 同步复位 D 触发器
module d_flip_flop (
    input  wire       clk,
    input  wire       reset_n,
    input  wire       d,
    output reg        q
);

always @(posedge clk) begin
    if (!reset_n)
        q <= 1'b0;
    else
        q <= d;
end

endmodule

// 移位寄存器
module shift_reg #(
    parameter WIDTH = 8
) (
    input  wire            clk,
    input  wire            enable,
    input  wire            serial_in,
    output wire            serial_out,
    output reg  [WIDTH-1:0] parallel
);

always @(posedge clk) begin
    if (enable)
        parallel <= {parallel[WIDTH-2:0], serial_in};
end

assign serial_out = parallel[WIDTH-1];

endmodule
```

阻塞赋值 `=` 与非阻塞赋值 `<=` 的区别：

| 特性 | 阻塞赋值 = | 非阻塞赋值 <= |
|------|------------|---------------|
| 执行顺序 | 立即执行 | 并行执行 |
| 用途 | 组合逻辑 | 时序逻辑 |
| 仿真结果 | 顺序执行效果 | 同时更新效果 |
| 综合结果 | 组合逻辑 | 寄存器/触发器 |

## 五、有限状态机

三段式状态机是推荐编码风格：

```verilog
module traffic_light (
    input  wire        clk,
    input  wire        reset_n,
    input  wire        car_sensor,
    output reg  [1:0]  highway_light,
    output reg  [1:0]  farm_light
);

localparam [1:0]
    GREEN  = 2'b00,
    YELLOW = 2'b01,
    RED    = 2'b10;

reg [1:0] state, next_state;
reg [4:0] timer;

// 状态寄存器
always @(posedge clk or negedge reset_n) begin
    if (!reset_n)
        state <= GREEN;
    else
        state <= next_state;
end

// 次态逻辑
always @(*) begin
    next_state = state;
    case (state)
        GREEN: begin
            if (car_sensor && timer == 30)
                next_state = YELLOW;
        end
        YELLOW: begin
            if (timer == 5)
                next_state = RED;
        end
        RED: begin
            if (timer == 20)
                next_state = GREEN;
        end
    endcase
end

// 输出逻辑 + 定时器
always @(posedge clk or negedge reset_n) begin
    if (!reset_n) begin
        timer <= 0;
        {highway_light, farm_light} <= {GREEN, RED};
    end else begin
        timer <= timer + 1;
        case (state)
            GREEN:  {highway_light, farm_light} <= {GREEN, RED};
            YELLOW: {highway_light, farm_light} <= {YELLOW, RED};
            RED:    {highway_light, farm_light} <= {RED, GREEN};
        endcase
    end
end

endmodule
```

## 六、仿真与测试

Testbench 编写：

```verilog
`timescale 1ns / 1ps

module tb_counter;

reg        clk;
reg        reset_n;
reg        enable;
wire [7:0] count;
wire       overflow;

counter uut (
    .clk(clk),
    .reset_n(reset_n),
    .enable(enable),
    .count(count),
    .overflow(overflow)
);

initial begin
    clk = 0;
    forever #5 clk = ~clk;  // 100MHz 时钟
end

initial begin
    // 初始化
    reset_n = 0;
    enable  = 0;
    #20;

    // 复位释放
    reset_n = 1;
    #10;

    // 使能计数
    enable = 1;
    #500;

    // 停止计数
    enable = 0;
    #100;

    $finish;
end

initial begin
    $monitor("Time=%0t count=%d overflow=%b",
             $time, count, overflow);
    $dumpfile("waveform.vcd");
    $dumpvars(0, tb_counter);
end

endmodule
```

## 七、综合与实现

综合约束示例：

```tcl
# SDC 时序约束
create_clock -period 10.000 [get_ports clk]
set_input_delay  -clock clk -max 2.0 [get_ports d*]
set_output_delay -clock clk -max 3.5 [get_ports q*]

# 伪路径
set_false_path -from [get_clocks slow_clk] -to [get_clocks fast_clk]

# 多周期路径
set_multicycle_path -setup 2 -from [get_pins regA/C] -to [get_pins regB/D]
```

综合后资源利用率报告示例：

```
Slice Logic Utilization:
  Number of Slice Registers:     1,245  out of 106,400   1%
  Number of Slice LUTs:            892  out of  53,200   1%
  Number of occupied Slices:       312  out of  26,600   1%
  Number of DSP48E1s:               8  out of     220   3%
  Number of BlockRAM/FIFO:          4  out of     140   2%
  Number of BUFG/BUFGCTRLs:         2  out of      32   6%
```

## 八、高级设计技巧

流水线（Pipeline）设计：

```verilog
module pipelined_multiplier (
    input  wire        clk,
    input  wire [15:0] a, b,
    output reg  [31:0] result
);

reg [15:0] a_reg, b_reg;
reg [31:0] partial;

always @(posedge clk) begin
    a_reg <= a;
    b_reg <= b;
end

always @(posedge clk) begin
    partial <= a_reg * b_reg;  // 第1级
end

always @(posedge clk) begin
    result <= partial;          // 第2级
end

endmodule
```

流水线与组合逻辑对比：

| 特性 | 组合逻辑 | 流水线 |
|------|----------|--------|
| 吞吐量 | 1数据/周期 | 1数据/周期 |
| 延迟 | 1周期 | N 周期 |
| 最大频率 | 较低 | 较高 |
| 面积 | 小 | 大（寄存器开销） |

## 九、常见问题与调试

时序违反常见原因：

```
1. 组合逻辑路径过长
2. 扇出过大
3. 时钟抖动
4. 跨时钟域未同步
5. 复位信号未做同步处理
```

跨时钟域同步处理：

```verilog
module sync_bit (
    input  wire clk_dst,
    input  wire async_in,
    output reg  sync_out
);

reg sync_ff;

always @(posedge clk_dst) begin
    sync_ff  <= async_in;
    sync_out <= sync_ff;
end

endmodule
```

## 相关条目

- [[FPGA]]
- [[05_ComputerScience/ComputerOrganizationAndArchitecture/DigitalLogic/DigitalLogic|DigitalLogic]]
- [[时序逻辑与状态机]]
- [[05_ComputerScience/HardwareAndEmbeddedSystems/DigitalCircuits/Combinational|Combinational]]
- [[05_ComputerScience/HardwareAndEmbeddedSystems/DigitalCircuits/Sequential|Sequential]]

## 参考资料

1. IEEE Std 1364-2001 Verilog 标准文档
2. 《Verilog HDL 高级数字设计》 Michael D. Ciletti 著
3. Xilinx Vivado 设计套件用户指南
4. Altera/Intel Quartus Prime 手册
5. OpenCores 开源 IP 核库：https://opencores.org
6. EDA Playground 在线仿真平台
7. Verilog Tutorial：https://www.chipverify.com

