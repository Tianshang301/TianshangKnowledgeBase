---
aliases: [LinkLayer]
tags: ['ComputerNetworks', 'LinkLayer']
---

# 链路层详解 (Link Layer)

## 1. Ethernet (以太网)

### 以太网帧结构 (IEEE 802.3)

```
 前导码(7B)  |  SFD(1B)  |  目标MAC(6B)  |  源MAC(6B)  |  类型/长度(2B)  |  数据(46-1500B)  |  FCS(4B)
```

| 字段 | 大小 | 说明 |
|------|------|------|
| **前导码 (Preamble)** | 7字节 | 10101010... 同步时钟 |
| **SFD** | 1字节 | 起始定界符 10101011 |
| **目标MAC** | 6字节 | 接收方MAC地址 |
| **源MAC** | 6字节 | 发送方MAC地址 |
| **类型/长度** | 2字节 | >1536=类型(EtherType), ≤1500=长度 |
| **数据** | 46-1500字节 | 上层数据(最小46B保证碰撞检测) |
| **FCS** | 4字节 | CRC32校验 |

### MAC 地址

```
48位, 通常表示为 12:34:56:78:9A:BC

┌────────┬─────────────────────────┐
│  OUI   │         NIC             │
│ (24位) │        (24位)           │
│ 厂商ID  │       设备ID            │
└────────┴─────────────────────────┘

单播:  第一字节最低位=0  →  12:34:56:78:9A:BC
多播:  第一字节最低位=1  →  01:00:5E:00:00:01
广播:  FF:FF:FF:FF:FF:FF
```

### CSMA/CD (Carrier Sense Multiple Access with Collision Detection)

```
1. 监听信道 (Carrier Sense)
2. 信道空闲 → 发送数据
3. 信道忙 → 等待(随机退避)
4. 发送时检测碰撞 (Collision Detection)
5. 碰撞 → 发送Jamming信号(32bit) → 指数退避(二进制指数退避算法)
6. 重试(最多16次)

二进制指数退避:
等待时隙 = random(0, 2^k - 1) × 512bit时间
k = min(重试次数, 10)
```

## 2. 交换机 vs 集线器

| 特性 | 集线器 (Hub) | 交换机 (Switch) |
|------|-------------|----------------|
| 工作层 | 物理层(L1) | 链路层(L2) |
| 转发方式 | 广播所有端口 | 根据MAC地址表转发 |
| 带宽 | 共享(所有端口平分) | 独享(每端口独立带宽) |
| 碰撞域 | 一个(所有端口) | 每端口一个 |
| 广播域 | 一个 | 一个(可VLAN分割) |
| 工作模式 | 半双工 | 全双工 |
| 智能程度 | 无 | 学习、过滤、转发 |

## 3. 学习型交换机 (Learning Bridge)

### 自学习过程

```
初始MAC地址表: 空

1. A → B (A:00:11, B:00:22)
   交换机收到帧，源MAC=00:11 → 学习: 端口1=00:11
   目标MAC=00:22 → MAC表无记录 → 向所有其他端口洪泛(flooding)

2. B → A (响应)
   交换机收到帧，源MAC=00:22 → 学习: 端口2=00:22
   目标MAC=00:11 → MAC表有记录 → 仅转发到端口1

3. 后续通信: 直接转发, 不再洪泛

MAC地址表:
┌──────────┬────────────┐
│   MAC    │    端口     │
├──────────┼────────────┤
│ 00:00:11 │     1      │
│ 00:00:22 │     2      │
│ 00:00:33 │     3      │
└──────────┴────────────┘
```

**老化时间:** 默认300秒, 过期自动删除

## 4. VLAN (Virtual LAN)

将物理网络分割为多个逻辑网络。

### 802.1Q VLAN 帧

```
标准以太网帧:
┌──────┬──────┬──────┬──────┬──────┬──────┐
│ DMAC │ SMAC │ Type │ Data │ FCS  │
└──────┴──────┴──────┴──────┴──────┘

802.1Q带VLAN标签:
┌──────┬──────┬──────┬────┬────┬──────┬──────┐
│ DMAC │ SMAC │ TPID │ TCI│Type│ Data │ FCS  │
└──────┴──────┴──────┴────┴────┴──────┴──────┘
                   │      │
              0x8100  VLAN ID(12bit)
                       Priority(3bit)
                       CFI/DEI(1bit)
```

**VLAN 优点:**
- 隔离广播域
- 提高安全性
- 简化网络管理
- 降低设备成本

### Trunk (中继)

```
交换机A(Trunk) ═══════════════════ 交换机B(Trunk)
    │                                    │
 VLAN10: 192.168.10.0/24           VLAN10: 192.168.10.0/24
 VLAN20: 192.168.20.0/24           VLAN20: 192.168.20.0/24

Trunk端口: 同时传输VLAN10和VLAN20的数据帧(带VLAN标签)
```

```bash
# Cisco交换机配置示例
Switch(config)# vlan 10
Switch(config-vlan)# name Engineering
Switch(config)# vlan 20
Switch(config-vlan)# name Sales

# 端口加入VLAN
Switch(config)# interface fastEthernet 0/1
Switch(config-if)# switchport mode access
Switch(config-if)# switchport access vlan 10

# Trunk配置
Switch(config)# interface gigabitEthernet 0/1
Switch(config-if)# switchport mode trunk
Switch(config-if)# switchport trunk allowed vlan 10,20
```

## 5. PPP (Point-to-Point Protocol)

用于点对点连接的链路层协议。

### PPP 帧格式

```
┌──────┬──────┬──────┬──────┬──────────┬──────┬──────┐
│ Flag │ Addr │ Ctrl │Protocol│  Payload │ FCS  │ Flag │
│ 0x7E │ 0xFF │ 0x03 │ 1-2B  │  ≤1500B  │2-4B  │ 0x7E │
└──────┴──────┴──────┴──────┴──────────┴──────┴──────┘
```

**PPP 协议栈:**
- **LCP** (Link Control Protocol): 建立、配置、测试链路
- **NCP** (Network Control Protocol): 配置网络层协议(如IPCP分配IP)
- **认证:** PAP (明文密码), CHAP (挑战握手)

### PPPoE (PPP over Ethernet)

用于宽带拨号:

```
PPPoE发现阶段 → PPP LCP → PPP认证(CHAP) → PPP NCP(IPCP) → 数据传输

# Linux PPPoE
pppoe-setup           # 配置
pppoe-start           # 连接
pppoe-stop            # 断开
```

## 6. 错误检测 (Error Detection)

### 6.1 奇偶校验 (Parity)

**单奇偶校验:**
```
数据:  1011010
偶校验: 10110100 (1的个数=偶数)
奇校验: 10110101 (1的个数=奇数)

缺点: 只能检测奇数位错误
```

**二维奇偶校验:**
```
数据:   1011010  1
        1100101  0
        0011011  1
        0101101  0
        1101010  1 (列校验)
```

### 6.2 校验和 (Checksum)

**Internet校验和 (IP/TCP/UDP):**

```python
def checksum(data):
    """16位反码求和"""
    total = 0
    for i in range(0, len(data), 2):
        word = (data[i] << 8) + (data[i+1] if i+1 < len(data) else 0)
        total += word
        total = (total & 0xFFFF) + (total >> 16)
    return (~total) & 0xFFFF
```

### 6.3 CRC (Cyclic Redundancy Check)

**CRC-32 (以太网使用):**

```
生成多项式: G(x) = x³² + x²⁶ + x²³ + x²² + x¹⁶ + x¹² + x¹¹
                  + x¹⁰ + x⁸ + x⁷ + x⁵ + x⁴ + x² + x + 1

CRC-32 常数: 0xEDB88320

# CRC特性:
# 可以检测所有单bit错误
# 可以检测所有双bit错误 (多项式次数≥2)
# 可以检测所有奇数个错误 (多项式包含因子x+1)
# 可以检测所有长度≤32的突发错误
```

```python
# CRC32 计算 (Python)
def crc32(data):
    crc = 0xFFFFFFFF
    for byte in data:
        crc ^= byte
        for _ in range(8):
            if crc & 1:
                crc = (crc >> 1) ^ 0xEDB88320
            else:
                crc >>= 1
    return crc ^ 0xFFFFFFFF
```

## 7. MAC 协议 (Medium Access Control)

### 7.1 信道划分 (Channel Partitioning)

| 协议 | 原理 | 优点 | 缺点 | 适用 |
|------|------|------|------|------|
| **TDMA** | 时分多址, 各节点分配时隙 | 无碰撞 | 空闲时隙浪费 | 蜂窝网络 |
| **FDMA** | 频分多址, 各节点分配频率 | 无碰撞 | 频谱利用率低 | 广播电视 |
| **CDMA** | 码分多址, 用唯一编码 | 同时传输 | 实现复杂 | 3G |

### 7.2 随机接入 (Random Access)

| 协议 | 描述 | 吞吐量 |
|------|------|--------|
| **ALOHA** | 想发就发, 碰撞随机重发 | 18% |
| **Slotted ALOHA** | 时隙同步发送 | 37% |
| **CSMA** | 先听后发, 减少碰撞 | ~60% |
| **CSMA/CD** | 边发边听, 碰撞停止 | ~90%+ (以太网) |

**CSMA/CD 最小帧长:**

```
最小帧长 = 2 × 网络最大传播延迟 × 数据传输率

100Mbps以太网 (2500m):
最小帧 = 2 × 25.6μs × 100Mbps = 5120bit = 640字节
实际: 64字节 (512bit, 因时槽=512bit)
```

### 7.3 受控接入 (Taking Turns)

| 协议 | 描述 | 特点 |
|------|------|------|
| **轮询 (Polling)** | 主节点依次询问各节点 | 有轮询开销 |
| **令牌传递 (Token Passing)** | 持有令牌的节点可发送 | 令牌丢失需处理 |

## 8. 交换机配置基础

```bash
# 基本配置
Switch> enable
Switch# configure terminal
Switch(config)# hostname S1

# VLAN
S1(config)# vlan 100
S1(config-vlan)# name Management
S1(config-vlan)# exit
S1(config)# interface vlan 100
S1(config-if)# ip address 192.168.100.1 255.255.255.0
S1(config-if)# no shutdown

# Access端口
S1(config)# interface gigabitEthernet 1/0/1
S1(config-if)# switchport mode access
S1(config-if)# switchport access vlan 100

# Trunk
S1(config)# interface gigabitEthernet 1/0/24
S1(config-if)# switchport mode trunk
S1(config-if)# switchport trunk allowed vlan 100,200,300
S1(config-if)# switchport trunk native vlan 999   # Native VLAN(不带标签)

# STP (生成树协议)
S1(config)# spanning-tree mode mst                # 多生成树
S1(config)# spanning-tree vlan 100 priority 4096  # 设置优先级

# 端口安全
S1(config)# interface gigabitEthernet 1/0/1
S1(config-if)# switchport port-security
S1(config-if)# switchport port-security maximum 2
S1(config-if)# switchport port-security mac-address sticky
S1(config-if)# switchport port-security violation shutdown

# 查看
S1# show vlan brief
S1# show interfaces trunk
S1# show mac-address-table
S1# show spanning-tree
\`\`\`

## 相关条目

- [[NetworkLayer]]
- [[TransportLayer]]
- [[NetworkModels]]
- [[NetworkSecurity]]
