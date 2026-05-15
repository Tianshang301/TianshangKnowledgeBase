---
aliases: [NetworkModels]
tags: ['ComputerNetworks', 'NetworkModels', 'NetworkModels']
---

# 网络模型 (Network Models)

## 1. OSI 七层模型

OSI（Open Systems Interconnection）模型由 ISO 制定，将网络通信划分为七个层次，每层负责特定的功能。

```
7. 应用层 (Application)     ─── 为用户应用提供网络服务
6. 表示层 (Presentation)    ─── 数据格式转换、加密、压缩
5. 会话层 (Session)         ─── 会话管理与同步
4. 传输层 (Transport)       ─── 端到端可靠传输
3. 网络层 (Network)         ─── 路由与寻址
2. 数据链路层 (Data Link)   ─── 帧传输与差错控制
1. 物理层 (Physical)        ─── 比特流传输
```

### 各层详细功能

| 层 | 功能 | 设备 | 协议示例 |
|---|------|------|---------|
| 应用层 | 为用户应用提供网络接口、文件传输、邮件、Web 等 | 应用软件 | HTTP, FTP, SMTP, DNS |
| 表示层 | 数据格式转换（ASCII→EBCDIC）、加密（SSL/TLS）、压缩 | 网关 | JPEG, MPEG, SSL |
| 会话层 | 会话建立/维护/终止、同步点插入、对话控制（半双工/全双工） | 网关 | NetBIOS, RPC, PPTP |
| 传输层 | 端到端连接、分段重组、流量控制、差错恢复 | 防火墙 | TCP, UDP |
| 网络层 | 逻辑寻址（IP）、路由选择、分组转发、分片重组 | 路由器 | IP, ICMP, OSPF, BGP |
| 数据链路层 | 帧封装、MAC 寻址、差错检测（CRC）、介质访问控制 | 交换机/网桥 | Ethernet, PPP, ARP |
| 物理层 | 比特流传输、电气特性、接口定义、编码方式 | 中继器/集线器 | 10BASE-T, RS-232 |

## 2. TCP/IP 四层模型

TCP/IP 模型是实际 Internet 使用的协议栈，精简为四层。

```
应用层 (Application)          ─── 对应 OSI 上三层
    │
传输层 (Transport)            ─── TCP/UDP
    │
网络层 (Internet)             ─── IP
    │
网络接口层 (Network Access)    ─── 对应 OSI 下两层
```

### 各层核心协议

```
应用层:  HTTP | HTTPS | FTP | SMTP | DNS | DHCP | SSH
传输层:  TCP（可靠） | UDP（不可靠）
网络层:  IPv4 | IPv6 | ICMP | ARP
网络接口层: Ethernet | Wi-Fi | PPP | DSL
```

## 3. OSI 与 TCP/IP 对比

| 对比维度 | OSI 七层模型 | TCP/IP 四层模型 |
|---------|-------------|-----------------|
| 制定时间 | 1984年（理论先行） | 1970s（实践先行） |
| 层次数量 | 7 层 | 4 层（或 5 层混合模型） |
| 分层粒度 | 细（表示层、会话层独立） | 粗（合并到应用层） |
| 传输层可靠性 | 支持多种服务模型 | 明确 TCP/UDP 两种 |
| 网络层 | 无连接+面向连接（X.25） | 仅无连接（IP） |
| 协议紧耦合 | 协议与模型分离 | 协议与模型紧耦合 |
| 实际应用 | 教学参考/理论分析 | Internet 实际协议栈 |
| 标准化组织 | ISO | IETF |

### 五层混合模型（教学常用）

```
5. 应用层 (Application)        ─── 消息 (Message)
4. 传输层 (Transport)          ─── 段 (Segment) / 数据报 (Datagram)
3. 网络层 (Network)            ─── 包 (Packet)
2. 数据链路层 (Data Link)      ─── 帧 (Frame)
1. 物理层 (Physical)           ─── 比特 (Bit)
```

## 4. 封装与解封装 (Encapsulation & Decapsulation)

数据在发送端从上到下逐层添加头部，接收端从下到上逐层移除头部。

```
发送方封装过程：

[应用数据]                            ← 应用层消息 (Message)
    ↓
[应用层头部][应用数据]                 ← 表示层/会话层处理
    ↓
[传输层头部][上层数据]                ← 段 (Segment) / 数据报 (Datagram)
    ↓  (源端口+目的端口+序列号+...)
[网络层头部][传输层数据]              ← 包 (Packet)
    ↓  (源IP+目的IP+TTL+...)
[链路层头部][网络层数据][链路层尾部]    ← 帧 (Frame)
    ↓  (源MAC+目的MAC+类型+FCS)
[前导码][帧][IFG]                    ← 比特流 (Bits)

接收方解封装：逆向过程，逐层剥离头部
```

### PDU 命名规则

| 层级 | PDU 名称 | 封装内容 | 关键头部信息 |
|------|---------|---------|-------------|
| 应用层 | 消息 (Message) / 数据 (Data) | 应用数据 | — |
| 传输层 | 段 (Segment, TCP) / 数据报 (Datagram, UDP) | 应用数据 | 端口号、序列号 |
| 网络层 | 包 (Packet) / 数据报 (Datagram, IP) | 传输层数据 | IP 地址 |
| 数据链路层 | 帧 (Frame) | 网络层数据 | MAC 地址、FCS |
| 物理层 | 比特 (Bit) / 符号 (Symbol) | 编码后的信号 | — |

## 5. 服务模型

### 面向连接 vs 无连接

| 特性 | 面向连接 (Connection-Oriented) | 无连接 (Connectionless) |
|------|------------------------------|------------------------|
| 建立连接 | 需要（三次握手） | 不需要 |
| 状态维护 | 维护连接状态 | 无状态 |
| 可靠性 | 可靠（确认+重传） | 不可靠（尽力而为） |
| 顺序保证 | 保证有序 | 不保证 |
| 流量控制 | 支持 | 不支持 |
| 代表协议 | TCP, ATM | UDP, IP |
| 适用场景 | Web、文件、邮件 | 视频流、DNS、IoT |

### 服务原语

```
面向连接的服务原语：
  LISTEN    — 监听（服务器等待连接）
  CONNECT   — 连接请求（客户端发起）
  ACCEPT    — 接受连接（服务器响应）
  RECEIVE   — 接收数据
  SEND      — 发送数据
  DISCONNECT — 断开连接
```

### QoS 服务模型

| 模型 | 描述 | 典型应用 |
|------|------|---------|
| Best-Effort | 尽力而为，无保证 | 传统 Internet |
| Integrated Services (IntServ) | RSVP 预留资源，细粒度 | 实时视频会议 |
| Differentiated Services (DiffServ) | 分类服务，优先级队列 | VoIP、流媒体 |

## 6. 标准化组织

| 组织 | 全称 | 职责 | 重要标准 |
|------|------|------|---------|
| **ISO** | International Organization for Standardization | 国际标准制定 | OSI 模型 (ISO 7498) |
| **IEEE** | Institute of Electrical and Electronics Engineers | 电气电子标准 | IEEE 802.3 (以太网), 802.11 (Wi-Fi) |
| **IETF** | Internet Engineering Task Force | Internet 协议标准 | RFC 文档, TCP/IP 协议族 |
| **ITU-T** | International Telecommunication Union - Telecommunication | 电信标准 | H.264, G.729 |
| **ANSI** | American National Standards Institute | 美国国家标准 | FDDI |
| **W3C** | World Wide Web Consortium | Web 标准 | HTTP, HTML, CSS |
| **ICANN** | Internet Corporation for Assigned Names and Numbers | 域名/IP 分配 | 根域名管理 |

### 重要 RFC

| RFC | 标题 | 意义 |
|-----|------|------|
| RFC 791 | Internet Protocol | IPv4 规范 |
| RFC 793 | Transmission Control Protocol | TCP 规范 |
| RFC 826 | Ethernet Address Resolution Protocol | ARP 协议 |
| RFC 1034/1035 | Domain Names | DNS 规范 |
| RFC 2068 | HTTP/1.1 | HTTP/1.1 规范 |
| RFC 2616 | HTTP/1.1 (更新版) | HTTP/1.1 修订 |
| RFC 7540 | HTTP/2 | HTTP/2 规范 |
| RFC 9000 | QUIC | QUIC 传输协议 |
| RFC 8200 | IPv6 | IPv6 规范 |
| RFC 8446 | TLS 1.3 | TLS 1.3 规范 |

## 7. 数据链路层服务

### 成帧方法

```
字节计数法:   [长度][数据...]
字节填充法:   [FLAG][数据][FLAG]  (转义特殊字符)
比特填充法:   [01111110][数据][01111110] (5个1后插0)
违规编码法:   使用物理层非法编码表示帧边界
```

### 差错控制

```
检错码:
  ┌─────────────────────────────────────────────┐
  │  奇偶校验 (Parity)     — 1位校验位           │
  │  校验和 (Checksum)     — IP/TCP/UDP 头部     │
  │  CRC (循环冗余校验)    — 以太网 FCS          │
  └─────────────────────────────────────────────┘

纠错码:
  海明码 (Hamming Code)   — 可检测并纠正单比特错误
  里德-所罗门码 (RS)      — 用于光盘、二维码
  LDPC                   — 5G、Wi-Fi 6 采用
```

### 介质访问控制

| 协议 | 方式 | 特点 |
|------|------|------|
| CSMA/CD | 有线竞争 | 以太网（已淘汰） |
| CSMA/CA | 无线竞争 | Wi-Fi |
| Token Ring | 令牌传递 | 无冲突，已淘汰 |
| TDMA | 时分复用 | 蜂窝网络 |
| FDMA | 频分复用 | 模拟通信 |
| CDMA | 码分复用 | 3G |

---

## 相关条目

- [[NetworkProtocols]]
- OSIModel
- TCPIP
- NetworkArchitecture

## 参考资源

- 《计算机网络：自顶向下方法》(Kurose & Ross)
- 《TCP/IP 详解 卷1：协议》(Stevens)
- ISO/IEC 7498-1 (OSI 模型)
- RFC 1122/1123 (Internet 主机需求)
- IETF 官方文档 (https://www.ietf.org/)
