---
aliases: [FPGA]
tags: ['HardwareAndEmbeddedSystems', 'FPGA', 'FPGA']
created: 2026-05-16
updated: 2026-05-16
---

# FPGA

## 一、FPGA 架构

FPGA（Field-Programmable Gate Array）由可编程逻辑块和可编程互连组成。

### 基本结构

| 组件 | 功能 | 说明 |
|------|------|------|
| 逻辑块（Logic Block） | 实现组合和时序逻辑 | 含 LUT、Flip-Flop、MUX、Carry Chain |
| 查找表（LUT） | 实现组合逻辑函数 | 4/6 输入 LUT，存储真值表 |
| 触发器（Flip-Flop） | 时序逻辑存储单元 | D 触发器，可配置为寄存器 |
| 互连资源（Routing） | 连接逻辑块 | 可编程开关矩阵、连线 |
| I/O 块（IOB） | 芯片与外部接口 | 支持多种电平标准 |
| DSP 切片 | 数字信号处理 | 硬件乘法器、累加器 |
| BRAM（块 RAM） | 嵌入式存储 | 通常 18/36 Kb 每块 |

### FPGA vs CPLD vs ASIC vs GPU

| 特性 | FPGA | CPLD | ASIC | GPU |
|------|------|------|------|-----|
| 可重配置 | 可多次 | 可多次 | 不可 | 不可 |
| 逻辑密度 | 高（百万门） | 低（万门） | 极高 | 固定架构 |
| 功耗 | 中 | 低 | 低 | 高 |
| 开发周期 | 短 | 很短 | 很长 | — |
| 单位成本 | 中 | 低 | 低（量大） | 中 |
| 适合场景 | 原型验证、中量 | 胶合逻辑 | 大规模量产 | 图形/并行计算 |

## 二、HDL 基础

### Verilog

```verilog
// 模块定义
module counter (
    input  wire       clk,
    input  wire       rst_n,
    output reg  [7:0] count
);
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n)
            count <= 8'd0;
        else
            count <= count + 1'b1;
    end
endmodule
```

| 关键字 | 用途 |
|--------|------|
| `module/endmodule` | 模块定义 |
| `input/output/inout` | 端口方向 |
| `wire` | 线网类型（组合逻辑连线） |
| `reg` | 寄存器类型（always 中赋值） |
| `assign` | 连续赋值 |
| `always @(sensitivity)` | 过程块 |
| `posedge/negedge` | 边沿触发 |

### VHDL

```vhdl
entity counter is
    port (
        clk   : in  std_logic;
        rst_n : in  std_logic;
        count : out std_logic_vector(7 downto 0)
    );
end entity;

architecture rtl of counter is
    signal cnt_reg : unsigned(7 downto 0) := (others => '0');
begin
    process(clk, rst_n)
    begin
        if rst_n = '0' then
            cnt_reg <= (others => '0');
        elsif rising_edge(clk) then
            cnt_reg <= cnt_reg + 1;
        end if;
    end process;
    count <= std_logic_vector(cnt_reg);
end architecture;
```

## 三、数字电路设计

### 组合逻辑

| 电路 | 描述 | 实现 |
|------|------|------|
| 加法器 | $S = A + B$ | 全加器级联 / 超前进位 |
| 多路选择器 | $Y = S ? A : B$ | 组合逻辑 / LUT |
| 译码器 | $n$ 输入 $2^n$ 输出 | 与门阵列 |
| 乘法器 | $P = A \times B$ | LUT / DSP 切片 |

### 时序逻辑

| 电路 | 描述 |
|------|------|
| 计数器 | 二进制/模 N/环形计数器 |
| 移位寄存器 | 串入串出/串入并出/并入串出 |
| 状态机（FSM） | Moore / Mealy 型 |
| 分频器 | 偶数/奇数/半整数分频 |

### 有限状态机（FSM）

```verilog
// Moore 型状态机
localparam IDLE = 2'b00, S1 = 2'b01, S2 = 2'b10;

always @(posedge clk or negedge rst_n)
    if (!rst_n) state <= IDLE;
    else        state <= next_state;

always @(*) begin
    case (state)
        IDLE: next_state = (start) ? S1 : IDLE;
        S1:   next_state = (done)  ? S2 : S1;
        S2:   next_state = IDLE;
        default: next_state = IDLE;
    endcase
end

always @(*) begin
    case (state)
        IDLE:  out = 0;
        S1:    out = 1;
        S2:    out = 0;
        default: out = 0;
    endcase
end
```

## 四、综合与实现流程

```
RTL 代码 → 综合（Synthesis）→ 技术映射 → 布局（Placement）→ 布线（Routing）→ 位流生成
```

| 阶段 | 输入 | 输出 | 工具 |
|------|------|------|------|
| RTL 综合 | Verilog/VHDL | 网表（Netlist） | Vivado, Quartus, Yosys |
| 技术映射 | 网表 | 目标工艺原语 | 同上 |
| 布局 | 映射后网表 | 物理位置 | Vivado, Quartus |
| 布线 | 布局结果 | 完整连线 | Vivado, Quartus |
| 位流生成 | 布局布线结果 | .bit 文件 | Vivado, Quartus |

## 五、仿真

```verilog
// 测试平台（Testbench）
module tb_counter;
    reg  clk, rst_n;
    wire [7:0] count;

    counter uut (.clk(clk), .rst_n(rst_n), .count(count));

    initial begin
        clk = 0;
        forever #5 clk = ~clk;  // 100 MHz 时钟
    end

    initial begin
        rst_n = 0;
        #20 rst_n = 1;
        #200 $finish;
    end

    initial begin
        $monitor("Time=%t count=%d", $time, count);
    end
endmodule
```

| 仿真器 | 类型 | 特点 |
|--------|------|------|
| ModelSim/Questa | 商业 | 功能强大、支持广泛 |
| Vivado Simulator | 商业 | Xilinx 集成 |
| VCS | 商业 | Synopsys 高性能 |
| Icarus Verilog | 开源 | 轻量免费 |
| GHDL | 开源 | VHDL 开源仿真 |

## 六、时序分析

时序约束确保信号在时钟沿之前稳定到达。

**建立时间（Setup Time）**：数据必须在时钟沿之前 $T_{setup}$ 到达。

**保持时间（Hold Time）**：数据必须在时钟沿之后保持 $T_{hold}$ 稳定。

**时钟域交叉（CDC）**：不同时钟域之间传递信号需同步器。

```verilog
// 两级同步器处理 CDC
reg sync1, sync2;
always @(posedge clk2)
    {sync2, sync1} <= {sync1, data_from_clk1};
```

**FIFO 同步**：使用异步 FIFO 跨时钟域传输多 bit 数据，通过格雷码编码指针。

## 七、IP 核集成

IP 核是预设计的逻辑模块，可快速集成到设计中：

| IP 类型 | 示例 |
|---------|------|
| 存储控制器 | DDR3/4/5 控制器 |
| 通信接口 | Ethernet, PCIe, USB |
| 信号处理 | FIR/IIR 滤波器, FFT |
| 处理器 | MicroBlaze, Nios II, RISC-V |

## 八、高层次综合（HLS）

HLS 使用 C/C++ 描述硬件行为，自动生成 RTL：

```c
// HLS FIR 滤波器
void fir(int input, int output[1], int coeff[32]) {
    #pragma HLS PIPELINE II=1
    static int shift_reg[32];
    int acc = 0;
    for (int i = 31; i > 0; i--)
        shift_reg[i] = shift_reg[i-1];
    shift_reg[0] = input;
    for (int i = 0; i < 32; i++)
        acc += shift_reg[i] * coeff[i];
    output[0] = acc;
}
```

## 九、主流厂商对比

| 特性 | Xilinx (AMD) | Intel (Altera) |
|------|-------------|----------------|
| 旗舰系列 | Virtex/Kintex/Artix | Stratix/Arria/Cyclone |
| 开发工具 | Vivado / Vitis | Quartus Prime |
| 软核 CPU | MicroBlaze | Nios II |
| AI 引擎 | ACAP (Versal) | FPGA + OneAPI |
| 开源支持 | 部分（Pynq） | 部分 |
| 常见应用 | 数据中心、通信 | 工业、嵌入 |

## 十、FPGA 典型应用

- **数字信号处理**：FIR/IIR 滤波器、FFT、调制解调
- **密码学**：AES、RSA 硬件加速
- **AI 推理加速**：CNN 卷积加速、神经网络推理
- **高速通信**：Ethernet MAC、PCIe、SerDes
- **软件定义无线电（SDR）**：基带信号处理
- **原型验证**：ASIC 原型在 FPGA 上验证

## 相关条目

- [[05_ComputerScience/ComputerOrganizationAndArchitecture/DigitalLogic/DigitalLogic|DigitalLogic]]
- ComputerOrganization
- [[05_ComputerScience/ProgrammingLanguages/Assembly/Assembly|Assembly]]
- [[05_ComputerScience/HardwareAndEmbeddedSystems/PCBDesign/PCBDesign|PCBDesign]]

## 参考资源

- 《Digital Design and Computer Architecture》（Harris & Harris）
- 《FPGA Prototyping by Verilog Examples》（Pong P. Chu）
- [Vivado Design Suite 用户指南](https://docs.xilinx.com/)
- [Quartus Prime 文档](https://www.intel.com/content/www/us/en/docs/programmable/)
- [OpenCores - 开源 IP 核](https://opencores.org/)


