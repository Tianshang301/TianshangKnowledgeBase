---
aliases: [TCPIP 协议栈详解]
tags: ['ComputerNetworks', 'NetworkModels', 'TCPIP 协议栈详解']
---

# TCP/IP 协议栈详解

## 一、TCP/IP 协议分层模型

TCP/IP 协议栈是互联网通信的事实标准，采用分层架构将复杂的网络通信分解为四个层次。与 OSI 七层模型相比，TCP/IP 模型更加简化实用。

| 层级 | 功能 | 核心协议 | PDU 名称 |
|------|------|----------|---------|
| 应用层 | 用户应用通信 | HTTP, FTP, SMTP, DNS | 消息 |
| 传输层 | 端到端通信 | TCP, UDP | 段/数据报 |
| 网络层 | 路由与寻址 | IP, ICMP, ARP | 包 |
| 网络接口层 | 物理传输 | Ethernet, WiFi | 帧 |

## 二、网络接口层

网络接口层负责在物理链路上传输数据帧。以太网帧的格式包括前导码、目标 MAC 地址(6字节)、源 MAC 地址(6字节)、类型/长度(2字节)、数据和 FCS 校验(4字节)。

**MAC 地址**是网卡在全球的唯一标识符，长度为48位，通常表示为12位十六进制数。ARP 协议通过广播请求解析 IP 地址到 MAC 地址的映射：发送方广播"谁有 IP X.X.X.X"，目标主机回复自己的 MAC 地址。

## 三、网络层：IP 协议

### 3.1 IPv4协议

IPv4数据报头部长度为20-60字节，关键字段包括：版本(4位)、首部长度、总长度(16位，最大65535字节)、标识、标志、片偏移(用于分片)、生存时间 TTL、协议(标识上层协议)、首部校验和、源 IP 地址和目标 IP 地址。

IP 分片机制：当数据报长度超过链路 MTU 时，路由器将其分片。每个分片包含原始标识、偏移量和 MF 标志。

$$
\text{offset} = \frac{\text{数据在原包中的位置}}{8}
$$

### 3.2 IPv6协议

IPv6的128位地址空间解决了 IPv4地址枯竭问题。IPv6头部简化为固定40字节，取消了校验和、分片等字段以提高转发效率：

| 特性 | IPv4 | IPv6 |
|------|------|------|
| 地址长度 | 32位 | 128位 |
| 地址数量 | 约43亿 | 约3.4e38 |
| 自动配置 | DHCP | SLAAC(无状态) |
| 安全性 | 可选的 IPSec | 原生支持 |
| 分片 | 路由器可执行 | 仅发送端执行 |
| 校验和 | 有 | 无 |

### 3.3 路由协议

路由协议分为两大类：

- **内部网关协议(IGP)**：RIP(距离向量，跳数限制15)、OSPF(链路状态，Dijkstra 算法)、IS-IS
- **外部网关协议(EGP)**：BGP(路径向量协议，互联网主干路由)

OSPF 使用 Dijkstra 最短路径算法计算路由：

$$
\text{cost}(P) = \sum_{i=1}^{n} \text{cost}(link_i)
$$

## 四、传输层：TCP 协议

### 4.1 TCP 头部

TCP 头部最小20字节，关键字段包括：源端口(2字节)、目标端口、序列号(32位)、确认号、数据偏移、标志位(URG/ACK/PSH/RST/SYN/FIN)、窗口大小(16位)、校验和和紧急指针。

### 4.2 三次握手与四次挥手

**三次握手建立连接**：
1. 客户端发送 SYN，序列号 $seq = x$
2. 服务器回复 SYN-ACK，$seq = y, ack = x+1$
3. 客户端发送 ACK，$seq = x+1, ack = y+1$

**四次挥手关闭连接**：
1. 发送方发送 FIN
2. 接收方回复 ACK
3. 接收方发送 FIN
4. 发送方回复 ACK
   等待2MSL 后关闭

### 4.3 可靠传输机制

TCP 通过累积确认和重传保证可靠性。**超时重传**使用指数退避算法，超时时间(RTO)基于 RTT 估算：

$$
\text{SRTT} = (1-\alpha) \times \text{SRTT} + \alpha \times \text{RTT}
$$
$$
\text{RTO} = \text{SRTT} + 4 \times \text{RTTVAR}
$$

**快速重传**：收到3个重复 ACK 时立即重传，无需等待超时。

### 4.4 拥塞控制

TCP 拥塞控制包含四个算法：

1. **慢启动(SS)**：cwnd 指数增长，每收到一个 ACK 增加1 MSS
2. **拥塞避免(CA)**：cwnd 线性增长，每 RTT 增加1 MSS
3. **快速恢复**：收到重复 ACK 时调整 ssthresh
4. **快重传**：3个重复 ACK 立即重传

$$
\text{cwnd} \leftarrow \begin{cases}
\text{cwnd} + 1 & \text{ssthresh 阶段, 每 ACK} \\
\text{cwnd} + \frac{1}{\text{cwnd}} & \text{CA 阶段, 每 ACK}
\end{cases}
$$

**CUBIC TCP**是 Linux 默认拥塞控制算法，更适合高带宽网络。

## 五、传输层：UDP 协议

UDP 提供无连接、不可靠的传输服务，头部仅8字节(源端口、目标端口、长度、校验和)。UDP 的优势在于低延迟和简单性，适用于 DNS 查询、视频流、VoIP 和在线游戏等场景。

QUIC 协议(基于 UDP)在应用层实现类似 TCP 的可靠性和拥塞控制，同时减少连接建立延迟。

## 六、应用层协议

| 协议 | 端口 | 传输层 | 特点 |
|------|------|--------|------|
| HTTP/3 | 443 | QUIC | 多路复用、0-RTT |
| DNS | 53 | UDP/TCP | 层次域名解析 |
| DHCP | 67/68 | UDP | 动态地址分配 |
| SMTP | 25 | TCP | 邮件发送 |
| FTP | 20/21 | TCP | 文件传输，双通道 |

## 七、协议栈性能优化

- **TCP 快开(TFO)**：在 SYN 中携带数据，减少1-RTT
- **窗口缩放**：窗口字段扩展为30位，支持高吞吐
- **选择性确认(SACK)**：选择性重传丢失段
- **Nagle 算法**：合并小数据段减少小包数量
- **延迟确认**：合并多个 ACK 减少控制包开销

## 相关条目

- [[NetworkModels]]
- [[ApplicationLayer]]
- [[TransportLayer]]
- [[NetworkLayer]]
- [[LinkLayer]]

## 参考资源

1. Stevens, W. R. "TCP/IP Illustrated, Volume 1: The Protocols." 2nd ed., Addison-Wesley, 2011.
2. Postel, J. "RFC 791: Internet Protocol." 1981.
3. Postel, J. "RFC 793: Transmission Control Protocol." 1981.
4. Deering, S., Hinden, R. "RFC 2460: Internet Protocol, Version 6." 1998.
5. Jacobson, V. "Congestion Avoidance and Control." ACM SIGCOMM, 1988.
6. Ha, S., et al. "CUBIC: A New TCP-Friendly High-Speed TCP Variant." ACM SIGOPS, 2008.
7. Iyengar, J., Thomson, M. "RFC 9000: QUIC: A UDP-Based Multiplexed and Secure Transport." 2021.
