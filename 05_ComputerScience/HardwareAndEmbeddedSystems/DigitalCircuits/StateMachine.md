# 状态机设计

## Mealy 机 vs Moore 机

| 特性 | Mealy 机 | Moore 机 |
|------|---------|---------|
| 输出依赖 | 当前状态 + 输入 | 仅当前状态 |
| 输出变化 | 输入变化立即影响输出 | 仅在时钟沿变化 |
| 状态数 | 通常更少 | 通常更多 |
| 对毛刺敏感 | 是 (组合输出) | 否 (寄存输出) |
| 时序特性 | 异步 | 同步 |
| 典型应用 | 序列检测器 | 计数器、控制器 |

### 状态图对比

```
Mealy 机:                          Moore 机:
                                    
  输入/输出                         输出
                                    
  S0 ──0/0──→ S1                  S0/0 ──0──→ S1/1
   ↑           │                    ↑           │
   └──1/0──────┘                    └────1──────┘
```

## 状态编码

| 编码方式 | 描述 | 触发器数 | 特点 |
|---------|------|---------|------|
| 二进制 (Binary) | 状态按二进制顺序编码 | log₂N | 最省触发器 |
| 格雷码 (Gray) | 相邻状态仅一位不同 | log₂N | 减少毛刺 |
| 独热码 (One-Hot) | 每个状态一个触发器 | N | 译码简单，速度快 |

```verilog
// 状态编码示例 (4种状态)
parameter [1:0] S0 = 2'b00, S1 = 2'b01, S2 = 2'b10, S3 = 2'b11;  // 二进制
parameter [1:0] S0 = 2'b00, S1 = 2'b01, S2 = 2'b11, S3 = 2'b10;  // 格雷码
parameter [3:0] S0 = 4'b0001, S1 = 4'b0010, S2 = 4'b0100, S3 = 4'b1000;  // 独热码
```

### 编码对比

| 状态数 | 二进制触发器 | 独热码触发器 | 独热码优点 |
|--------|------------|------------|-----------|
| 4 | 2 | 4 | 译码简单 |
| 8 | 3 | 8 | 无组合译码延迟 |
| 16 | 4 | 16 | 适合高速 FPGA 实现 |
| 100 | 7 | 100 | 触发器多但速度快 |

## FSM 设计过程

### 标准步骤

1. **规格说明** (Specification): 明确输入、输出、功能
2. **状态图** (State Diagram): 画出所有状态和转移
3. **状态表** (State Table): 列出当前状态→下一状态和输出
4. **状态分配** (State Assignment): 选择编码方式
5. **次态逻辑** (Next-State Logic): 推导 D 触发器输入表达式
6. **输出逻辑** (Output Logic): 推导输出表达式
7. **实现** (Implementation): Verilog/VHDL 编码

### 状态表模板

| 当前状态 | 输入 | 下一状态 | 输出 |
|---------|------|---------|------|
| S0 | 0 | S1 | 0 |
| S0 | 1 | S0 | 0 |
| S1 | 0 | S2 | 0 |
| S1 | 1 | S0 | 1 |
| ... | ... | ... | ... |

## 示例 1：1101 序列检测器

### 规范

检测二进制输入序列中是否出现 "1101"，检测到时输出 1。

### 状态图 (Moore 机)

```
    0         1         0         1
S0 ──→ S0 ──→ S1 ──→ S2 ──→ S3 ──→ S4
  ←──    ←──    ←──    ←──    ←──
  1/1     0       1       0       0/1
```

- S0: 初始 (已匹配 "")
- S1: 已匹配 "1"
- S2: 已匹配 "11"
- S3: 已匹配 "110"
- S4: 已匹配 "1101" (输出 1)

### Verilog 实现

```verilog
module seq_detector_1101 (
    input clk, rst, din,
    output reg dout
);
    parameter [2:0] S0 = 3'b000, S1 = 3'b001, S2 = 3'b010,
                    S3 = 3'b011, S4 = 3'b100;

    reg [2:0] state, next_state;

    // 状态寄存器
    always @(posedge clk or posedge rst) begin
        if (rst)
            state <= S0;
        else
            state <= next_state;
    end

    // 次态逻辑
    always @(*) begin
        case (state)
            S0: next_state = din ? S1 : S0;
            S1: next_state = din ? S2 : S0;
            S2: next_state = din ? S2 : S3;
            S3: next_state = din ? S4 : S0;
            S4: next_state = din ? S1 : S0;
            default: next_state = S0;
        endcase
    end

    // 输出逻辑 (Moore)
    always @(posedge clk or posedge rst) begin
        if (rst)
            dout <= 0;
        else
            dout <= (state == S4);
    end
endmodule
```

### Mealy 机实现 (更省状态)

```verilog
module seq_detector_1101_mealy (
    input clk, rst, din,
    output reg dout
);
    parameter [1:0] S0 = 2'b00, S1 = 2'b01, S2 = 2'b10, S3 = 2'b11;

    reg [1:0] state, next_state;

    always @(posedge clk or posedge rst) begin
        if (rst) state <= S0;
        else state <= next_state;
    end

    always @(*) begin
        next_state = state;
        dout = 0;
        case (state)
            S0: if (din) next_state = S1;
            S1: if (din) next_state = S2; else next_state = S0;
            S2: if (din) next_state = S2; else next_state = S3;
            S3: if (din) begin next_state = S1; dout = 1; end
                 else next_state = S0;
        endcase
    end
endmodule
```

## 示例 2：交通灯控制器

### 规范

十字路口交通灯：
- 主干道 (Main) 绿灯 30s，黄灯 5s
- 次干道 (Side) 绿灯 20s，黄灯 5s
- 传感器检测次干道是否有车等待

### 状态图

```
                  传感器无车
  MG 30s ───────→ MY 5s ───────→ SG 20s ─────→ SY 5s
   ↑                                                    │
   └──────────────────── 传感器有车 ──────────────────────┘
```

### Verilog 实现

```verilog
module traffic_light_controller (
    input clk, rst, sensor,          // 传感器: 1=有车等待
    output reg [1:0] main_light,      // 00=绿, 01=黄, 10=红
    output reg [1:0] side_light       // 00=绿, 01=黄, 10=红
);
    parameter [1:0] MG=0, MY=1, SG=2, SY=3;
    reg [1:0] state, next_state;

    reg [4:0] counter;                // 计时器 (假设~1s 周期)
    reg timer_rst;

    // 状态转移
    always @(posedge clk or posedge rst) begin
        if (rst) state <= MG;
        else if (timer_rst) state <= next_state;
    end

    // 次态 + 定时逻辑
    always @(*) begin
        next_state = state;
        timer_rst = 0;
        case (state)
            MG: begin
                if (counter == 30) begin   // 30s 绿灯
                    next_state = MY;
                    timer_rst = 1;
                end
            end
            MY: begin
                if (counter == 5) begin    // 5s 黄灯
                    next_state = SG;
                    timer_rst = 1;
                end
            end
            SG: begin
                if (counter == 20 || (counter >= 10 && !sensor)) begin
                    next_state = SY;      // 无车等待则提前切换
                    timer_rst = 1;
                end
            end
            SY: begin
                if (counter == 5) begin    // 5s 黄灯
                    next_state = MG;
                    timer_rst = 1;
                end
            end
        endcase
    end

    // 输出
    always @(*) begin
        case (state)
            MG: begin main_light = 2'b00; side_light = 2'b10; end
            MY: begin main_light = 2'b01; side_light = 2'b10; end
            SG: begin main_light = 2'b10; side_light = 2'b00; end
            SY: begin main_light = 2'b10; side_light = 2'b01; end
        endcase
    end

    // 计时器
    always @(posedge clk or posedge rst) begin
        if (rst || timer_rst)
            counter <= 0;
        else
            counter <= counter + 1;
    end
endmodule
```

## 示例 3：自动售货机

### 规范

- 商品价格 15 元
- 可投币：5元、10元
- 投币总额 ≥ 15 时出货并找零
- 不退多投 (找零)

### 状态图

```
         5元              5元              5元
S0(0) ──→ S1(5) ──→ S2(10) ──→ S3(15) → 出货
  ↑        ↑         │         ↑
  │        └──10元───┘         │
  └───────────10元──────────────┘
          (找零5元)
```

## 状态最小化

### 划分法 (Partitioning Method)

1. 根据输出将所有状态分组
2. 根据下一状态分区分组
3. 重复直到无法进一步划分

### 示例

| 状态 | 输入=0 下一状态 | 输入=1 下一状态 | 输出 |
|------|---------------|---------------|------|
| A | B | C | 0 |
| B | A | D | 0 |
| C | B | A | 1 |
| D | B | A | 0 |

**划分步骤**:
1. P0 = {A,B,D} (输出0), {C} (输出1)
2. 检查 P0 中各状态下一状态是否在同一组:
   - A: 下一状态 B∈P0, C∈{C} → 不在同一组
   - B: 下一状态 A∈P0, D∈P0 → 在同一组
   - D: 下一状态 B∈P0, A∈P0 → 在同一组
3. P1 = {A}, {B,D}, {C}
4. B, D 的下一状态都在 {B,D} 中 → 可合并
5. 最终: {A}, {B,D}, {C}

## FSM 实现模板

```verilog
// 三段式 FSM 模板 (推荐)
module fsm_template (
    input clk, rst,
    input [W-1:0] din,
    output reg [Z-1:0] dout
);
    // 1. 状态定义
    parameter S0 = ..., S1 = ..., ...;
    reg [N-1:0] state, next_state;

    // 2. 状态寄存器 (时序)
    always @(posedge clk or posedge rst) begin
        if (rst) state <= S0;
        else state <= next_state;
    end

    // 3. 次态逻辑 (组合)
    always @(*) begin
        next_state = state;  // 默认保持
        case (state)
            S0: if (cond) next_state = S1;
            // ...
        endcase
    end

    // 4. 输出逻辑 (时序 - 同步输出)
    always @(posedge clk or posedge rst) begin
        if (rst) dout <= 0;
        else case (next_state)  // 提前一个周期输出
            // ...
        endcase
    end
endmodule
```

## 常见问题

1. **FSM 不启动**: 检查复位逻辑和初始状态
2. **状态跳转错误**: 次态逻辑遗漏 Default 分支 (导致锁存)
3. **毛刺输出**: Mealy 机的组合输出易受输入毛刺影响
4. **死锁**: 是否存在吸收态 (不可达状态被误使用)
5. **时序违规**: 保持等式中 FSM 状态码的独特性
