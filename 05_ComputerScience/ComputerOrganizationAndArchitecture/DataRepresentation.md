---
aliases: [DataRepresentation]
tags: ['05_ComputerScience', 'ComputerOrganizationAndArchitecture']
---

# 数据表示 (Data Representation)

## 一、整数表示 (Integer Representation)

| 类型 | 位数 | 最小值 | 最大值 | 说明 |
|------|------|--------|--------|------|
| 无符号整型 | 8 | 0 | $2^8-1 = 255$ | 全部用于数值 |
| 无符号整型 | 16 | 0 | $2^{16}-1 = 65535$ | 范围翻倍 |
| 无符号整型 | 32 | 0 | $2^{32}-1 \approx 4.29\times10^9$ | 常用 |
| 无符号整型 | 64 | 0 | $2^{64}-1 \approx 1.84\times10^{19}$ | 大数场景 |
| 有符号整型 | 8 | $-2^7 = -128$ | $2^7-1 = 127$ | 补码表示 |
| 有符号整型 | 32 | $-2^{31}$ | $2^{31}-1$ | 默认 int |
| 有符号整型 | 64 | $-2^{63}$ | $2^{63}-1$ | long long |

### 补码原理 (Two's Complement)

$$[x]_\text{补}= \begin{cases} x & 0 \leq x \leq 2^{n-1}-1 \\ x + 2^n & -2^{n-1} \leq x < 0 \end{cases}$$

补码加法的模运算性质：$$[x+y]_\text{补}\equiv [x]_\text{补}+ [y]_\text{补}\pmod{2^n}$$

### 溢出检测 (Overflow Detection)

```text
符号标志 SF = MSB of result（结果的最高位）
零标志   ZF = result == 0
进位标志 CF = unsigned overflow
溢出标志 OF = signed overflow
```

溢出条件：两个同符号数相加得异符号结果：
$$\text{OF} = (A_{n-1} \oplus R_{n-1}) \land (B_{n-1} \oplus R_{n-1})$$

## 二、浮点数 (Floating-Point Numbers) — IEEE 754

标准格式：
$$V = (-1)^s \times M \times 2^{E}$$

其中 $M = 1.f$（规范化），$s$ 为符号位，$E = e - \text{bias}$（指数偏移）

| 精度 | 总位数 | 符号位 | 指数位 | 尾数位 | Bias | 范围 |
|------|--------|--------|--------|--------|------|------|
| 单精度 float | 32 | 1 | 8 | 23 | 127 | $\pm1.2\times10^{-38} \sim \pm3.4\times10^{38}$ |
| 双精度 double | 64 | 1 | 11 | 52 | 1023 | $\pm2.2\times10^{-308} \sim \pm1.8\times10^{308}$ |
| 半精度 half | 16 | 1 | 5 | 10 | 15 | $\pm6.1\times10^{-5} \sim \pm6.5\times10^{4}$ |

### 特殊值 (Special Values)

```text
指数 = 0, 尾数 = 0   →  0（+0 和 -0）
指数 = 0, 尾数 ≠ 0   →  非规范化数 (Subnormal)
指数 = 全1, 尾数 = 0   →  ∞（正负无穷）
指数 = 全1, 尾数 ≠ 0   →  NaN (Not a Number)
```

### 精度问题 (Precision Issues)

浮点数不能精确表示所有十进制小数。例如 $0.1_{10}$：$$0.1_{10} = 0.0001100110011..._2 \text{（无限循环）}$$

相对舍入误差（Unit in the Last Place, ULP）：
$$\text{ULP} = 2^{E - p + 1}$$
其中 $p$ 为精度位数（float: 24, double: 53）

### 浮点运算注意事项

- 避免直接比较相等（用 $\|a-b\| < \epsilon$）
- 大数加小数可能被"吞噬"（Catastrophic Cancellation）
- Kahan 求和算法可减少累积误差

## 三、字符编码 (Character Encoding)

| 编码 | 位数 | 编码空间 | 特点 | 兼容性 |
|------|------|---------|------|--------|
| ASCII | 7 | 128 | 仅英文和基本符号 | — |
| Latin-1 (ISO-8859-1) | 8 | 256 | 西欧语言 | 兼容 ASCII |
| Unicode | 21 | 1,112,064 | 全球所有字符标准 | — |
| UTF-8 | 8-32 | Unicode | 变长，英文 1 字节 | **兼容 ASCII** |
| UTF-16 | 16/32 | Unicode | Windows/NTFS 原生，BOM | 基本平面 2 字节 |
| UTF-32 | 32 | Unicode | 定长，浪费空间 | 处理简单 |

### UTF-8 编码规则

```
U+0000 - U+007F:   0xxxxxxx                     (1 字节)
U+0080 - U+07FF:   110xxxxx 10xxxxxx            (2 字节)
U+0800 - U+FFFF:   1110xxxx 10xxxxxx 10xxxxxx   (3 字节)
U+10000-U+10FFFF:  11110xxx 10xxxxxx 10xxxxxx 10xxxxxx (4 字节)
```

## 四、字节序 (Endianness)

| 字节序 | 说明 | 架构 | 网络协议 |
|--------|------|------|---------|
| 大端 (Big Endian/BE) | 高字节在低地址 | PowerPC, SPARC, MIPS | TCP/IP（网络字节序）|
| 小端 (Little Endian/LE) | 低字节在低地址 | **x86/x86-64**, ARM* | — |

32 位整数 `0x12345678` 在内存中的存储：
```text
地址:    0x00  0x01  0x02  0x03
大端:    0x12  0x34  0x56  0x78
小端:    0x78  0x56  0x34  0x12
```

*注：ARM 架构支持双端（Bi-Endian），默认小端

## 五、位域与对齐 (Bit Fields and Alignment)

### 结构体对齐 (Struct Padding)

```c
struct Example {
    char a;     // 1 byte  + 3 padding
    int  b;     // 4 bytes
    short c;    // 2 bytes + 2 padding
};  // total: 12 bytes (不是 7!)
```

对齐规则：结构体大小为最大成员对齐数的整数倍，每个成员地址对齐到其大小的倍数。

### 定点数 DSP 应用 (Fixed-Point in DSP)

嵌入式 DSP（如音频编解码、数字滤波器）常用定点数而非浮点数：

```c
// Q15 定点数示例 (16-bit, 1 sign + 15 fraction)
// 范围: [-1, 1 - 2^-15]
// 精度: 2^-15 ≈ 3.05e-5

int16_t q15_from_float(float x) {
    return (int16_t)(x * 32768.0f);
}

float q15_to_float(int16_t x) {
    return (float)x / 32768.0f;
}

// Q15 乘法: 乘积再右移 15 位
int16_t q15_mul(int16_t a, int16_t b) {
    int32_t prod = (int32_t)a * (int32_t)b;
    return (int16_t)(prod >> 15);
}
```

### 浮点数特殊值表 (IEEE 754 Single Precision)

| 符号 s | 指数 e | 尾数 f | 值 | 说明 |
|--------|--------|--------|-----|------|
| 0 | 0xFF | 0x000000 | $+\infty$ | 正无穷 |
| 1 | 0xFF | 0x000000 | $-\infty$ | 负无穷 |
| 0/1 | 0xFF | $\neq 0$ | NaN | 非数（Not a Number）|
| 0 | 0x00 | 0x000000 | $+0$ | 正零 |
| 1 | 0x00 | 0x000000 | $-0$ | 负零 |
| 0/1 | 0x00 | $\neq 0$ | $(-1)^s \times 2^{-126} \times 0.f$ | 非规范化数（Subnormal）|

### 浮点数运算精度问题

```python
# Python 中浮点数的"惊喜"
>>> 0.1 + 0.2
0.30000000000000004  # 不是 0.3!

>>> 1.0 + 2.0**-52
1.0  # 精度不足，被舍入

# Kahan 求和减少误差
def kahan_sum(values):
    s = 0.0
    c = 0.0  # 补偿项
    for v in values:
        y = v - c
        t = s + y
        c = (t - s) - y
        s = t
    return s

# 不使用 Kahan: 大数 + 小数可能丢失
values = [1e16, 1.0, -1e16]
print(sum(values))           # 0.0 (错误的！)
print(kahan_sum(values))     # 1.0 (正确的)
```

## 六、二进制安全与漏洞 (Binary Security)

### 整数溢出 (Integer Overflow)

```c
// 有符号整数溢出是未定义行为 (UB)
int x = INT_MAX;  // 2147483647
x = x + 1;         // UB: 可能变为 INT_MIN = -2147483648

// 无符号整数溢出定义良好：回绕
unsigned int y = UINT_MAX;  // 4294967295
y = y + 1;                  // 0 (定义良好)

// 缓冲区溢出漏洞：整数溢出导致
void vulnerable(char *src, size_t len) {
    char *buf = malloc(len + 1);  // 如果 len = SIZE_MAX, len+1 = 0
    memcpy(buf, src, len);        // 堆溢出！
}
```

### 数据序列化 (Serialization)

```c
// 大端-小端转换（网络字节序）
uint16_t htons(uint16_t host);     // host → network (big endian)
uint16_t ntohs(uint16_t net);      // network → host
uint32_t htonl(uint32_t host);
uint32_t ntohl(uint32_t net);
```

## 七、数据压缩基础 (Data Compression Basics)

### 无损压缩算法对比

| 算法 | 类型 | 压缩比（文本）| 速度 | 适用 |
|------|------|-------------|------|------|
| **Run-Length Encoding (RLE)** | 游程编码 | 依赖数据重复度 | 极快 | 简单图形/位图 |
| **LZ77/LZ78** | 字典编码 | 2-4× | 快 | ZIP, PNG, gzip |
| **Huffman Coding** | 熵编码 | 2-3× | 中 | JPEG, DEFLATE |
| **Arithmetic Coding** | 熵编码 | 2-4× | 慢 | JPEG 2000, H.264 |
| **LZW** | 字典编码 | 2-3× | 快 | GIF, TIFF, Unix compress |

### 整数压缩 (Integer Compression)

用于数据库和搜索引擎的倒排索引：
- **Variable Byte (VarInt)**：每字节用 1 bit 表示是否继续
- **Simple9/16**：在一个 32-bit 字中打包尽可能多的整数
- **PForDelta (Patched Frame-of-Reference)**：将整数转为差值后用可变长打包

$$\text{Compression Ratio} = \frac{\text{原始大小}}{\text{压缩后大小}}$$

## 八、内存对齐与性能 (Memory Alignment & Performance)

```c
// 未对齐访问
struct Bad {
    char a;   // 地址偏移 0
    int  b;   // 地址偏移 1（非 4 对齐！）
    short c;  // 地址偏移 5（非 2 对齐！）
};
// sizeof(Bad) = 12 (padding 到 4 的倍数)

// 对齐优化
struct Good {
    int  b;   // 偏移 0
    short c;  // 偏移 4
    char a;   // 偏移 6
};  // sizeof(Good) = 8 (无 padding)
// 按成员大小降序排列可最大化空间效率
```

未对齐访问在 x86 上可工作但有性能惩罚（2-3× 延迟），在 ARM 上可能触发异常。

## 相关条目
- [[BinaryAndHexadecimal]]
- [[NumberSystems]]
- [[InstructionSetArchitecture]]
- [[CacheMemory]]
- [[05_ComputerScience/ComputerOrganizationAndArchitecture/INDEX]]
