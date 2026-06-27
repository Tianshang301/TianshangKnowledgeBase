---
aliases:
  - Verilog数字设计
  - Verilog Digital Design
  - 硬件描述语言
  - 数字电路设计
  - FPGA设计
tags:
  - verilog
  - digital-design
  - fpga
  - hardware
  - rtl
  - cpu-design
created: 2026-06-27
updated: 2026-06-27
---

# Verilog 数字设计

## 1. Verilog 基础

### 1.1 模块声明

```verilog
// Verilog 模块基本结构
module module_name (
    input  wire        clk,        // 时钟信号
    input  wire        rst_n,      // 异步复位 (低有效)
    input  wire [7:0]  data_in,    // 8位输入
    input  wire        valid_in,   // 输入有效信号
    output reg  [7:0]  data_out,   // 8位输出
    output wire        valid_out   // 输出有效信号
);
    // 模块内容
endmodule

// 端口类型:
// input:   输入端口 (只能读取)
// output:  输出端口 (只能写入)
// inout:   双向端口 (可读可写)

// 数据类型:
// wire:    线网类型 (组合逻辑, 连续赋值)
// reg:     寄存器类型 (时序逻辑, 过程赋值)
// integer: 32位整数 (仿真用)
// real:    浮点数 (仿真用)
```

### 1.2 Wire vs Reg

```verilog
// Wire: 用于组合逻辑, 连续赋值
wire [7:0] sum;
assign sum = a + b;  // 连续赋值, sum 是 wire

// Reg: 用于过程块中的赋值
reg [7:0] result;
always @(*) begin
    result = a + b;  // 过程赋值, result 是 reg
end

// 注意: reg 不一定综合为寄存器!
// 在 always @(*) 中的 reg → 组合逻辑 (LUT)
// 在 always @(posedge clk) 中的 reg → 寄存器 (FF)

// 示例: 2选1多路选择器
module mux2to1 (
    input  wire a,
    input  wire b,
    input  wire sel,
    output wire y
);
    assign y = sel ? b : a;  // 连续赋值
endmodule

// 等价的 always 实现
module mux2to1_always (
    input  wire a,
    input  wire b,
    input  wire sel,
    output reg  y           // 过程赋值目标必须是 reg
);
    always @(*) begin
        if (sel)
            y = b;
        else
            y = a;
    end
endmodule
```

## 2. 组合逻辑

### 2.1 基本组合逻辑

```verilog
// 与门
module and_gate (
    input  wire a, b,
    output wire y
);
    assign y = a & b;
endmodule

// 4选1多路选择器
module mux4to1 (
    input  wire [3:0] d,     // 4个数据输入
    input  wire [1:0] sel,   // 2位选择信号
    output reg        y
);
    always @(*) begin
        case (sel)
            2'b00: y = d[0];
            2'b01: y = d[1];
            2'b10: y = d[2];
            2'b11: y = d[3];
            default: y = 1'b0;
        endcase
    end
endmodule

// 2-4 译码器
module decoder_2to4 (
    input  wire [1:0] a,
    input  wire       en,
    output reg  [3:0] y
);
    always @(*) begin
        if (!en)
            y = 4'b0000;
        else begin
            case (a)
                2'b00: y = 4'b0001;
                2'b01: y = 4'b0010;
                2'b10: y = 4'b0100;
                2'b11: y = 4'b1000;
            endcase
        end
    end
endmodule

// 4-2 优先编码器
module encoder_4to2_priority (
    input  wire [3:0] a,
    output reg  [1:0] y,
    output reg        valid
);
    always @(*) begin
        valid = 1'b1;
        if (a[3])      y = 2'b11;
        else if (a[2]) y = 2'b10;
        else if (a[1]) y = 2'b01;
        else if (a[0]) y = 2'b00;
        else begin
            y = 2'b00;
            valid = 1'b0;
        end
    end
endmodule
```

### 2.2 运算符

```verilog
// 算术运算符
assign sum = a + b;       // 加法
assign diff = a - b;      // 减法
assign prod = a * b;      // 乘法
assign quot = a / b;      // 除法
assign rem = a % b;       // 取模

// 位运算符
assign and_out = a & b;   // 按位与
assign or_out = a | b;    // 按位或
assign xor_out = a ^ b;   // 按位异或
assign not_out = ~a;      // 按位取反

// 逻辑运算符
assign land = a && b;     // 逻辑与
assign lor = a || b;      // 逻辑或
assign lnot = !a;         // 逻辑非

// 移位运算符
assign left_shift = a << 2;   // 逻辑左移
assign right_shift = a >> 2;  // 逻辑右移
assign arith_right = $signed(a) >>> 2;  // 算术右移

// 关系运算符
assign eq = (a == b);     // 等于
assign neq = (a != b);    // 不等于
assign gt = (a > b);      // 大于
assign lt = (a < b);      // 小于

// 拼接运算符
assign concat = {a, b};           // 拼接
assign replicate = {4{a}};        // 重复 {aaaa}
assign partial = {a[7:4], b[3:0]}; // 部分拼接

// 条件运算符
assign y = sel ? a : b;  // 三元运算符
```

## 3. 时序逻辑

### 3.1 触发器与寄存器

```verilog
// D触发器 (上升沿触发)
module d_ff (
    input  wire clk,
    input  wire rst_n,
    input  wire d,
    output reg  q
);
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n)
            q <= 1'b0;          // 异步复位
        else
            q <= d;             // 数据锁存
    end
endmodule

// 带使能的D触发器
module d_ff_en (
    input  wire clk,
    input  wire rst_n,
    input  wire en,
    input  wire d,
    output reg  q
);
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n)
            q <= 1'b0;
        else if (en)
            q <= d;             // 仅在使能时更新
    end
endmodule

// 8位寄存器
module register_8bit (
    input  wire       clk,
    input  wire       rst_n,
    input  wire       load,
    input  wire [7:0] d,
    output reg  [7:0] q
);
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n)
            q <= 8'b0;
        else if (load)
            q <= d;
    end
endmodule

// 移位寄存器
module shift_register (
    input  wire       clk,
    input  wire       rst_n,
    input  wire       en,
    input  wire       serial_in,
    output wire       serial_out,
    output wire [7:0] parallel_out
);
    reg [7:0] shift_reg;

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n)
            shift_reg <= 8'b0;
        else if (en)
            shift_reg <= {shift_reg[6:0], serial_in};  // 左移
    end

    assign serial_out = shift_reg[7];
    assign parallel_out = shift_reg;
endmodule
```

### 3.2 计数器

```verilog
// 自由运行计数器
module counter_free (
    input  wire       clk,
    input  wire       rst_n,
    output reg  [7:0] count
);
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n)
            count <= 8'b0;
        else
            count <= count + 1'b1;
    end
endmodule

// 带使能和终端计数的计数器
module counter_tc (
    input  wire       clk,
    input  wire       rst_n,
    input  wire       en,
    input  wire [7:0] max_count,
    output reg  [7:0] count,
    output wire       tc          // Terminal Count
);
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n)
            count <= 8'b0;
        else if (en) begin
            if (count == max_count)
                count <= 8'b0;
            else
                count <= count + 1'b1;
        end
    end

    assign tc = (count == max_count) && en;
endmodule

// 可逆计数器 (上下计数)
module counter_updown (
    input  wire       clk,
    input  wire       rst_n,
    input  wire       en,
    input  wire       up_down,  // 1=上, 0=下
    output reg  [7:0] count
);
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n)
            count <= 8'b0;
        else if (en) begin
            if (up_down)
                count <= count + 1'b1;
            else
                count <= count - 1'b1;
        end
    end
endmodule
```

## 4. 有限状态机 (FSM)

### 4.1 Mealy 与 Moore 状态机

```verilog
// Mealy 状态机: 输出依赖于状态和输入
module fsm_mealy (
    input  wire clk,
    input  wire rst_n,
    input  wire in,
    output reg  out
);
    // 状态编码
    localparam S0 = 2'b00;
    localparam S1 = 2'b01;
    localparam S2 = 2'b10;

    reg [1:0] state, next_state;

    // 状态寄存器
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n)
            state <= S0;
        else
            state <= next_state;
    end

    // 次态逻辑 (组合)
    always @(*) begin
        case (state)
            S0: next_state = in ? S1 : S0;
            S1: next_state = in ? S2 : S0;
            S2: next_state = in ? S2 : S0;
            default: next_state = S0;
        endcase
    end

    // 输出逻辑 (Mealy: 依赖状态和输入)
    always @(*) begin
        case (state)
            S2: out = in ? 1'b1 : 1'b0;  // 在S2且in=1时输出
            default: out = 1'b0;
        endcase
    end
endmodule

// Moore 状态机: 输出仅依赖于状态
module fsm_moore (
    input  wire clk,
    input  wire rst_n,
    input  wire in,
    output reg  out
);
    localparam S0 = 3'b000;
    localparam S1 = 3'b001;
    localparam S2 = 3'b010;
    localparam S3 = 3'b100;  // One-hot encoding

    reg [2:0] state, next_state;

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n)
            state <= S0;
        else
            state <= next_state;
    end

    always @(*) begin
        case (state)
            S0: next_state = in ? S1 : S0;
            S1: next_state = in ? S2 : S0;
            S2: next_state = in ? S3 : S0;
            S3: next_state = in ? S3 : S0;
            default: next_state = S0;
        endcase
    end

    // Moore 输出: 仅依赖状态
    always @(*) begin
        out = (state == S3);  // 在S3时输出1
    end
endmodule
```

### 4.2 状态编码方式

```verilog
// 二进制编码: 节省触发器, 译码逻辑复杂
localparam S0 = 2'b00;
localparam S1 = 2'b01;
localparam S2 = 2'b10;
localparam S3 = 2'b11;

// One-Hot 编码: 每个状态一个触发器, 译码简单
localparam S0 = 4'b0001;
localparam S1 = 4'b0010;
localparam S2 = 4'b0100;
localparam S3 = 4'b1000;

// Gray 编码: 相邻状态仅1位不同, 减少毛刺
localparam S0 = 2'b00;
localparam S1 = 2'b01;
localparam S2 = 2'b11;
localparam S3 = 2'b10;

// 编码选择指南:
// ┌─────────────┬────────────┬────────────┬────────────┐
// │ 编码方式    │ 触发器数   │ 译码复杂度 │ 适用场景   │
// ├─────────────┼────────────┼────────────┼────────────┤
// │ Binary      │ log2(N)    │ 高         │ 资源受限   │
// │ One-Hot     │ N          │ 低         │ 速度优先   │
// │ Gray        │ log2(N)    │ 中         │ 低功耗     │
// └─────────────┴────────────┴────────────┴────────────┘
```

## 5. 存储器设计

### 5.1 寄存器文件

```verilog
// 32×32 寄存器文件 (类似 RISC-V)
module register_file (
    input  wire        clk,
    input  wire        rst_n,
    // 读端口1
    input  wire [4:0]  raddr1,
    output wire [31:0] rdata1,
    // 读端口2
    input  wire [4:0]  raddr2,
    output wire [31:0] rdata2,
    // 写端口
    input  wire [4:0]  waddr,
    input  wire [31:0] wdata,
    input  wire        we
);
    reg [31:0] regs [0:31];
    integer i;

    // 写操作
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            for (i = 0; i < 32; i = i + 1)
                regs[i] <= 32'b0;
        end
        else if (we && waddr != 5'b0)
            regs[waddr] <= wdata;
    end

    // 读操作 (组合逻辑)
    assign rdata1 = (raddr1 == 5'b0) ? 32'b0 : regs[raddr1];
    assign rdata2 = (raddr2 == 5'b0) ? 32'b0 : regs[raddr2];
endmodule
```

### 5.2 SRAM 模型

```verilog
// 同步单端口 SRAM
module sram_sp (
    input  wire        clk,
    input  wire        ce_n,      // 片选 (低有效)
    input  wire        we_n,      // 写使能 (低有效)
    input  wire [9:0]  addr,      // 10位地址 (1024字)
    input  wire [31:0] wdata,
    output reg  [31:0] rdata
);
    reg [31:0] mem [0:1023];

    always @(posedge clk) begin
        if (!ce_n) begin
            if (!we_n)
                mem[addr] <= wdata;  // 写
            else
                rdata <= mem[addr];  // 读
        end
    end
endmodule

// 同步双端口 SRAM (简单双端口)
module sram_sdpram (
    input  wire        clk,
    // 写端口
    input  wire        wr_en,
    input  wire [9:0]  wr_addr,
    input  wire [31:0] wr_data,
    // 读端口
    input  wire        rd_en,
    input  wire [9:0]  rd_addr,
    output reg  [31:0] rd_data
);
    reg [31:0] mem [0:1023];

    // 写端口
    always @(posedge clk) begin
        if (wr_en)
            mem[wr_addr] <= wr_data;
    end

    // 读端口
    always @(posedge clk) begin
        if (rd_en)
            rd_data <= mem[rd_addr];
    end
endmodule
```

## 6. CPU 流水线实现

### 6.1 五级流水线框架

```verilog
// RISC-V 五级流水线 CPU
module pipeline_cpu (
    input  wire        clk,
    input  wire        rst_n,
    // 指令存储器接口
    output wire [31:0] imem_addr,
    input  wire [31:0] imem_rdata,
    // 数据存储器接口
    output wire [31:0] dmem_addr,
    output wire [31:0] dmem_wdata,
    input  wire [31:0] dmem_rdata,
    output wire        dmem_we,
    output wire        dmem_re
);
    // ============================================================
    // IF (Instruction Fetch) 阶段
    // ============================================================
    reg  [31:0] pc;
    wire [31:0] pc_next;
    wire [31:0] if_instr;

    // PC 寄存器
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n)
            pc <= 32'h0000_0000;
        else if (!stall_if)
            pc <= pc_next;
    end

    assign pc_next = branch_taken ? branch_target : pc + 4;
    assign imem_addr = pc;
    assign if_instr = imem_rdata;

    // IF/ID 流水线寄存器
    reg [31:0] if_id_pc, if_id_instr;
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n || flush_if_id) begin
            if_id_pc    <= 32'b0;
            if_id_instr <= 32'b0;  // NOP
        end else if (!stall_if_id) begin
            if_id_pc    <= pc;
            if_id_instr <= if_instr;
        end
    end

    // ============================================================
    // ID (Instruction Decode) 阶段
    // ============================================================
    wire [6:0]  opcode = if_id_instr[6:0];
    wire [4:0]  rd     = if_id_instr[11:7];
    wire [2:0]  funct3 = if_id_instr[14:12];
    wire [4:0]  rs1    = if_id_instr[19:15];
    wire [4:0]  rs2    = if_id_instr[24:20];
    wire [6:0]  funct7 = if_id_instr[31:25];

    wire [31:0] rs1_data, rs2_data;
    wire [31:0] imm;

    // 寄存器文件
    register_file rf (
        .clk(clk), .rst_n(rst_n),
        .raddr1(rs1), .rdata1(rs1_data),
        .raddr2(rs2), .rdata2(rs2_data),
        .waddr(wb_rd), .wdata(wb_wdata), .we(wb_reg_we)
    );

    // 立即数生成
    imm_gen imm_gen_inst (
        .instr(if_id_instr),
        .imm(imm)
    );

    // 控制单元
    wire id_reg_we, id_alu_src, id_mem_we, id_mem_re;
    wire id_mem_to_reg, id_branch, id_jump;
    wire [3:0] id_alu_op;

    control_unit ctrl (
        .opcode(opcode),
        .funct3(funct3),
        .funct7(funct7),
        .reg_we(id_reg_we),
        .alu_src(id_alu_src),
        .alu_op(id_alu_op),
        .mem_we(id_mem_we),
        .mem_re(id_mem_re),
        .mem_to_reg(id_mem_to_reg),
        .branch(id_branch),
        .jump(id_jump)
    );

    // ID/EX 流水线寄存器
    reg [31:0] id_ex_pc, id_ex_rs1_data, id_ex_rs2_data, id_ex_imm;
    reg [4:0]  id_ex_rs1, id_ex_rs2, id_ex_rd;
    reg        id_ex_reg_we, id_ex_alu_src, id_ex_mem_we, id_ex_mem_re;
    reg        id_ex_mem_to_reg, id_ex_branch, id_ex_jump;
    reg [3:0]  id_ex_alu_op;

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n || flush_id_ex) begin
            // 清零 (NOP)
            id_ex_reg_we <= 1'b0;
            id_ex_mem_we <= 1'b0;
            // ... 其他信号清零
        end else if (!stall_id_ex) begin
            id_ex_pc         <= if_id_pc;
            id_ex_rs1_data   <= rs1_data;
            id_ex_rs2_data   <= rs2_data;
            id_ex_imm        <= imm;
            id_ex_rs1        <= rs1;
            id_ex_rs2        <= rs2;
            id_ex_rd         <= rd;
            id_ex_reg_we     <= id_reg_we;
            id_ex_alu_src    <= id_alu_src;
            id_ex_alu_op     <= id_alu_op;
            id_ex_mem_we     <= id_mem_we;
            id_ex_mem_re     <= id_mem_re;
            id_ex_mem_to_reg <= id_mem_to_reg;
            id_ex_branch     <= id_branch;
            id_ex_jump       <= id_jump;
        end
    end

    // ============================================================
    // EX (Execute) 阶段
    // ============================================================
    wire [31:0] alu_a = forward_a == 2'b10 ? ex_mem_alu_result :
                        forward_a == 2'b01 ? wb_wdata :
                        id_ex_rs1_data;
    wire [31:0] alu_b_mux = id_ex_alu_src ? id_ex_imm : id_ex_rs2_data;
    wire [31:0] alu_b = forward_b == 2'b10 ? ex_mem_alu_result :
                        forward_b == 2'b01 ? wb_wdata :
                        alu_b_mux;

    wire [31:0] alu_result;
    wire        alu_zero;

    alu alu_inst (
        .a(alu_a),
        .b(alu_b),
        .alu_op(id_ex_alu_op),
        .result(alu_result),
        .zero(alu_zero)
    );

    // 分支计算
    wire branch_taken = id_ex_branch && alu_zero;
    wire [31:0] branch_target = id_ex_pc + id_ex_imm;

    // EX/MEM 流水线寄存器 (简化)
    reg [31:0] ex_mem_alu_result, ex_mem_rs2_data;
    reg [4:0]  ex_mem_rd;
    reg        ex_mem_reg_we, ex_mem_mem_we, ex_mem_mem_re, ex_mem_mem_to_reg;

    // ============================================================
    // MEM (Memory Access) 阶段
    // ============================================================
    assign dmem_addr  = ex_mem_alu_result;
    assign dmem_wdata = ex_mem_rs2_data;
    assign dmem_we    = ex_mem_mem_we;
    assign dmem_re    = ex_mem_mem_re;

    // MEM/WB 流水线寄存器
    reg [31:0] mem_wb_alu_result, mem_wb_mem_data;
    reg [4:0]  mem_wb_rd;
    reg        mem_wb_reg_we, mem_wb_mem_to_reg;

    // ============================================================
    // WB (Write Back) 阶段
    // ============================================================
    wire [4:0]  wb_rd      = mem_wb_rd;
    wire        wb_reg_we  = mem_wb_reg_we;
    wire [31:0] wb_wdata   = mem_wb_mem_to_reg ? mem_wb_mem_data : mem_wb_alu_result;

    // ============================================================
    // Hazard Detection & Forwarding
    // ============================================================
    wire stall_if, stall_if_id, stall_id_ex;
    wire flush_if_id, flush_id_ex;
    wire [1:0] forward_a, forward_b;

    hazard_unit hazard (
        .id_ex_rs1(id_ex_rs1),
        .id_ex_rs2(id_ex_rs2),
        .ex_mem_rd(ex_mem_rd),
        .mem_wb_rd(mem_wb_rd),
        .ex_mem_reg_we(ex_mem_reg_we),
        .mem_wb_reg_we(mem_wb_reg_we),
        .branch_taken(branch_taken),
        .forward_a(forward_a),
        .forward_b(forward_b),
        .stall_if(stall_if),
        .stall_if_id(stall_if_id),
        .stall_id_ex(stall_id_ex),
        .flush_if_id(flush_if_id),
        .flush_id_ex(flush_id_ex)
    );
endmodule
```

### 6.2 冒险检测单元

```verilog
// 数据冒险检测与前递
module hazard_unit (
    input  wire [4:0] id_ex_rs1,
    input  wire [4:0] id_ex_rs2,
    input  wire [4:0] ex_mem_rd,
    input  wire [4:0] mem_wb_rd,
    input  wire       ex_mem_reg_we,
    input  wire       mem_wb_reg_we,
    input  wire       branch_taken,
    output reg  [1:0] forward_a,
    output reg  [1:0] forward_b,
    output wire       stall_if,
    output wire       stall_if_id,
    output wire       stall_id_ex,
    output wire       flush_if_id,
    output wire       flush_id_ex
);
    // 前递逻辑 (Forwarding)
    always @(*) begin
        // 前递到 ALU 输入 A
        if (ex_mem_reg_we && ex_mem_rd != 5'b0 &&
            ex_mem_rd == id_ex_rs1)
            forward_a = 2'b10;  // 从 EX/MEM 前递
        else if (mem_wb_reg_we && mem_wb_rd != 5'b0 &&
                 mem_wb_rd == id_ex_rs1)
            forward_a = 2'b01;  // 从 MEM/WB 前递
        else
            forward_a = 2'b00;  // 无前递

        // 前递到 ALU 输入 B
        if (ex_mem_reg_we && ex_mem_rd != 5'b0 &&
            ex_mem_rd == id_ex_rs2)
            forward_b = 2'b10;
        else if (mem_wb_reg_we && mem_wb_rd != 5'b0 &&
                 mem_wb_rd == id_ex_rs2)
            forward_b = 2'b01;
        else
            forward_b = 2'b00;
    end

    // Load-Use 冒险检测 (需要停顿1周期)
    wire load_use = id_ex_mem_re &&
                    (id_ex_rd == id_ex_rs1 || id_ex_rd == id_ex_rs2);

    assign stall_if   = load_use;
    assign stall_if_id = load_use;
    assign stall_id_ex = load_use;

    // 控制冒险 (分支时冲刷)
    assign flush_if_id = branch_taken;
    assign flush_id_ex = branch_taken;
endmodule
```

## 7. 仿真与测试

### 7.1 测试平台

```verilog
// 测试平台 (Testbench)
`timescale 1ns / 1ps

module tb_pipeline_cpu;
    reg         clk;
    reg         rst_n;
    wire [31:0] imem_addr;
    reg  [31:0] imem_rdata;
    wire [31:0] dmem_addr;
    wire [31:0] dmem_wdata;
    reg  [31:0] dmem_rdata;
    wire        dmem_we;
    wire        dmem_re;

    // 实例化被测模块
    pipeline_cpu uut (
        .clk(clk),
        .rst_n(rst_n),
        .imem_addr(imem_addr),
        .imem_rdata(imem_rdata),
        .dmem_addr(dmem_addr),
        .dmem_wdata(dmem_wdata),
        .dmem_rdata(dmem_rdata),
        .dmem_we(dmem_we),
        .dmem_re(dmem_re)
    );

    // 时钟生成 (10ns 周期)
    initial clk = 0;
    always #5 clk = ~clk;

    // 指令存储器
    reg [31:0] instr_mem [0:1023];
    always @(*) begin
        imem_rdata = instr_mem[imem_addr[11:2]];
    end

    // 数据存储器
    reg [31:0] data_mem [0:1023];
    always @(posedge clk) begin
        if (dmem_we)
            data_mem[dmem_addr[11:2]] <= dmem_wdata;
        if (dmem_re)
            dmem_rdata <= data_mem[dmem_addr[11:2]];
    end

    // 测试程序
    initial begin
        // 加载指令
        instr_mem[0] = 32'h00500093;  // addi x1, x0, 5
        instr_mem[1] = 32'h00A00113;  // addi x2, x0, 10
        instr_mem[2] = 32'h002081B3;  // add x3, x1, x2
        instr_mem[3] = 32'h0030A023;  // sw x3, 0(x1)
        instr_mem[4] = 32'h0000A203;  // lw x4, 0(x1)

        // 初始化
        rst_n = 0;
        #20;
        rst_n = 1;

        // 运行100个周期
        #1000;

        // 检查结果
        $display("=== Register Values ===");
        $display("x1 = %d", uut.rf.regs[1]);
        $display("x2 = %d", uut.rf.regs[2]);
        $display("x3 = %d", uut.rf.regs[3]);
        $display("x4 = %d", uut.rf.regs[4]);

        $finish;
    end

    // 波形输出
    initial begin
        $dumpfile("pipeline.vcd");
        $dumpvars(0, tb_pipeline_cpu);
    end

    // 监控信号
    initial begin
        $monitor("Time=%0t PC=%h Instr=%h",
                 $time, imem_addr, imem_rdata);
    end
endmodule
```

### 7.2 时序分析

```
时序约束 (Setup/Hold Time):

┌─────────────────────────────────────────────────────────┐
│  Setup Time (tsu): 数据必须在时钟沿前稳定的最小时间    │
│  Hold Time (th):   数据必须在时钟沿后保持的最小时间    │
│                                                         │
│         ┌──────────────────────────────────────────┐    │
│  Data:  ─┘        ┌────────┐        └─────────────    │
│                   │        │                           │
│                   │  tsu   │  th                       │
│                   │◄──────►│◄────►│                    │
│         ─────────┐│        ││┌─────────────────────    │
│  Clock:          └┘        └┘                          │
│                   ▲                                    │
│               Clock Edge                               │
│                                                         │
│  时序约束:                                              │
│  Tclk > tpd_comb + tsu + tskew                         │
│                                                         │
│  其中:                                                  │
│  Tclk: 时钟周期                                        │
│  tpd_comb: 组合逻辑传播延迟                            │
│  tsu: 触发器建立时间                                    │
│  tskew: 时钟偏斜                                        │
│                                                         │
│  时序违例:                                              │
│  如果 tpd_comb > Tclk - tsu - tskew                    │
│  → Setup 违例! 需要优化或降频                          │
└─────────────────────────────────────────────────────────┘

时钟域交叉 (CDC):
┌─────────────────────────────────────────────────────────┐
│  问题: 不同时钟域的信号直接连接可能导致亚稳态          │
│                                                         │
│  解决方案:                                              │
│  1. 双触发器同步器:                                     │
│     ┌────────┐  ┌────────┐                             │
│     │ D FF   │──│ D FF   │── 同步后信号               │
│     └────────┘  └────────┘                             │
│       ▲           ▲                                    │
│       clk_b       clk_b                                │
│       (目标时钟域)                                      │
│                                                         │
│  2. 握手协议:                                           │
│     req → 同步 → ack → 同步                            │
│                                                         │
│  3. 异步 FIFO:                                          │
│     格雷码指针 + 双触发器同步                          │
└─────────────────────────────────────────────────────────┘
```

## 8. FPGA vs ASIC

```
FPGA vs ASIC 设计对比:

┌─────────────────────────────────────────────────────────┐
│  特性          │ FPGA                    │ ASIC         │
├────────────────┼─────────────────────────┼──────────────┤
│  开发周期      │ 数周                    │ 数月-数年    │
│  NRE 成本      │ 低 (仅工具)             │ 高 ($1M+)    │
│  单片成本      │ 高                      │ 低 (量产后)  │
│  性能          │ 中等                    │ 高           │
│  功耗          │ 高                      │ 低           │
│  灵活性        │ 可重编程                │ 固定         │
│  适用场景      │ 原型/小批量/可重构      │ 大批量       │
│  最小工艺      │ 3nm (最新)              │ 3nm          │
│  逻辑单元      │ LUT + FF                │ 标准单元库   │
└────────────────┴─────────────────────────┴──────────────┘

FPGA 内部结构:
┌─────────────────────────────────────────────────────────┐
│                    FPGA 架构                             │
│                                                         │
│  ┌─────┐  ┌─────┐  ┌─────┐  ┌─────┐  ┌─────┐        │
│  │ CLB │──│ CLB │──│ CLB │──│ CLB │──│ CLB │        │
│  └──┬──┘  └──┬──┘  └──┬──┘  └──┬──┘  └──┬──┘        │
│     │        │        │        │        │              │
│  ┌──┴────────┴────────┴────────┴────────┴──┐          │
│  │           Switch Matrix                 │          │
│  └──┬────────┬────────┬────────┬────────┬──┘          │
│     │        │        │        │        │              │
│  ┌──┴──┐  ┌──┴──┐  ┌──┴──┐  ┌──┴──┐  ┌──┴──┐        │
│  │ BRAM│  │ DSP │  │ IOB │  │ IOB │  │ PLL │        │
│  └─────┘  └─────┘  └─────┘  └─────┘  └─────┘        │
│                                                         │
│  CLB (Configurable Logic Block):                        │
│  ┌─────────────────────────────────┐                   │
│  │  LUT (Look-Up Table)            │                   │
│  │  ┌───────────────────────────┐  │                   │
│  │  │ 6-input LUT (64 bits)    │  │                   │
│  │  └───────────────────────────┘  │                   │
│  │  ┌────────┐ ┌────────┐         │                   │
│  │  │ FF     │ │ FF     │         │                   │
│  │  └────────┘ └────────┘         │                   │
│  │  ┌────────┐ ┌────────┐         │                   │
│  │  │ MUX    │ │ Carry  │         │                   │
│  │  └────────┘ └────────┘         │                   │
│  └─────────────────────────────────┘                   │
└─────────────────────────────────────────────────────────┘

综合目标选择:
┌─────────────────────────────────────────────────────────┐
│  // Xilinx Vivado FPGA 综合                             │
│  set_property TARGET_ARCHITECTURE VirtexUltraScale+     │
│  synth_design -top my_module                            │
│                                                         │
│  // ASIC 综合 (Synopsys Design Compiler)                │
│  set target_library "tsmc7nm_ss_0p725v_125c.db"        │
│  compile -map_effort high                               │
│                                                         │
│  关键差异:                                              │
│  - FPGA: LUT 实现任意逻辑, 进位链有限                  │
│  - ASIC: 标准单元库, 可定制单元, 时序更精确            │
│  - FPGA: 时钟树由 PLL/MMCM 管理                        │
│  - ASIC: 需要手动设计时钟树 (CTS)                      │
└─────────────────────────────────────────────────────────┘
```
