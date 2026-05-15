---
aliases: [NetworkProtocols]
tags: ['ComputerNetworks', 'NetworkProtocols', 'NetworkProtocols']
---

# 网络协议 (Network Protocols)

## 1. ARP（地址解析协议）

ARP 将 IP 地址解析为 MAC 地址，工作在数据链路层与网络层之间。

### ARP 请求与响应

```
ARP 请求（广播）：
┌─────────────────────────────────────────┐
│ 源 MAC:   00:1A:2B:00:00:01             │
│ 源 IP:    192.168.1.10                  │
│ 目标 MAC: FF:FF:FF:FF:FF:FF (广播)      │
│ 目标 IP:  192.168.1.1                   │
│ 操作:     请求 (1)                      │
└─────────────────────────────────────────┘
                   ↓
ARP 响应（单播）：
┌─────────────────────────────────────────┐
│ 源 MAC:   00:1A:2B:FF:FF:FF             │
│ 源 IP:    192.168.1.1                   │
│ 目标 MAC: 00:1A:2B:00:00:01             │
│ 目标 IP:  192.168.1.10                  │
│ 操作:     响应 (2)                      │
└─────────────────────────────────────────┘
```

### ARP 缓存

```
ARP 缓存表（Linux: `arp -a` / Windows: `arp -a`）：
  192.168.1.1   00:1A:2B:FF:FF:FF  动态  2分钟
  192.168.1.5   3C:22:FB:12:34:56  动态  2分钟
  192.168.1.254 08:00:27:A1:B2:C3  静态  永久

ARP 攻击原理：发送伪造 ARP 响应，劫持流量。
防御：DAI (Dynamic ARP Inspection)、DHCP Snooping。
```

## 2. ICMP（Internet 控制报文协议）

ICMP 用于网络层的差错报告和诊断，封装在 IP 数据报中。

### ICMP 报文类型

| 类型 | 代码 | 含义 | 用途 |
|------|------|------|------|
| 0 | 0 | Echo Reply | ping 响应 |
| 3 | 0 | 目标网络不可达 | 路由错误 |
| 3 | 1 | 目标主机不可达 | 主机不存在 |
| 3 | 3 | 目标端口不可达 | 端口未监听 |
| 8 | 0 | Echo Request | ping 请求 |
| 11 | 0 | TTL 超时 | traceroute 使用 |

### Ping 与 Traceroute

```
# ping 工作原理
发送 ICMP Echo Request → 目标回复 Echo Reply
用于测试连通性和 RTT

ping www.baidu.com
  来自 39.156.66.18 的回复: 字节=32 时间=12ms TTL=52
  来自 39.156.66.18 的回复: 字节=32 时间=11ms TTL=52

# traceroute 工作原理
发送 TTL=1,2,3... 的 UDP 包或 ICMP 请求
每个路由器将 TTL 减1，减到0时返回 ICMP 超时报文

traceroute www.baidu.com
  1  192.168.1.1 (2ms)
  2  10.0.0.1 (5ms)
  3  202.106.0.1 (15ms)
  ...
```

## 3. DHCP（动态主机配置协议）

DHCP 自动分配 IP 地址、子网掩码、网关、DNS 等配置。

### DORA 过程

```
DHCP 客户端                    DHCP 服务器
    │                              │
    │ 1. DHCP DISCOVER             │
    │    源: 0.0.0.0:68            │
    │    目标: 255.255.255.255:67  │
    │    "谁可以提供IP地址？"       │
    │─────────────────────────────►│
    │                              │
    │ 2. DHCP OFFER                │
    │    "提供IP: 192.168.1.100    │
    │     子网掩码: 255.255.255.0  │
    │     网关: 192.168.1.1       │
    │     DNS: 8.8.8.8"           │
    │◄─────────────────────────────│
    │                              │
    │ 3. DHCP REQUEST              │
    │    "我接受 192.168.1.100"    │
    │─────────────────────────────►│
    │                              │
    │ 4. DHCP ACK                  │
    │    "确认，租期 86400s"       │
    │◄─────────────────────────────│
```

### DHCP 选项

| 选项代码 | 名称 | 说明 |
|---------|------|------|
| 1 | Subnet Mask | 子网掩码 |
| 3 | Router | 默认网关 |
| 6 | DNS Server | DNS 服务器 |
| 15 | Domain Name | 域名后缀 |
| 42 | NTP Server | 时间服务器 |
| 51 | IP Address Lease Time | 租期 |
| 53 | DHCP Message Type | 消息类型 |

## 4. DNS（域名系统）

DNS 将域名解析为 IP 地址，采用层次化的分布式数据库。

### DNS 层次结构

```
根域 (Root)              . (13台根服务器)
  ├── 通用顶级域 (gTLD)  .com .org .net .edu .gov
  ├── 国家顶级域 (ccTLD) .cn .jp .uk .de .us
  └── 反向域 (ARPA)      .in-addr.arpa (反向解析)

完整域名: www.example.com.
               ├──┘    ├──┘ ├─┘
             主机    二级域 TLD
```

### DNS 解析过程

```
递归查询（客户端 → 本地DNS服务器）：
  客户端 → 递归解析器 → 根 → TLD → 权威服务器 → 返回IP

迭代查询（本地DNS服务器 → 各级服务器）：
  客户端 ──► 递归解析器
                │
                ├──► 根DNS服务器
                │   └──► 返回 .com TLD 地址
                │
                ├──► .com TLD 服务器
                │   └──► 返回 example.com 权威地址
                │
                ├──► example.com 权威服务器
                │   └──► 返回 A 记录 93.184.216.34
                │
                ◄── 返回结果给客户端
```

### DNS 记录类型

| 记录 | 用途 | 示例 |
|------|------|------|
| A | IPv4 地址 | example.com A 93.184.216.34 |
| AAAA | IPv6 地址 | example.com AAAA 2606:2800:220::1 |
| CNAME | 别名 | www CNAME example.com |
| MX | 邮件交换 | MX 10 mail.example.com |
| NS | 名称服务器 | NS ns1.example.com |
| TXT | 文本记录 | "v=spf1 include:_spf.google.com" |
| SOA | 区域权威信息 | 主服务器、管理员邮箱、序列号 |
| SRV | 服务定位 | _sip._tcp.example.com SRV ... |

## 5. HTTP/HTTPS

### HTTP 方法

| 方法 | 用途 | 幂等 | 安全 | 请求体 |
|------|------|------|------|--------|
| GET | 获取资源 | ✓ | ✓ | ✗ |
| POST | 创建资源 | ✗ | ✗ | ✓ |
| PUT | 全量更新 | ✓ | ✗ | ✓ |
| PATCH | 部分更新 | ✗ | ✗ | ✓ |
| DELETE | 删除资源 | ✓ | ✗ | 可有 |
| HEAD | 获取响应头 | ✓ | ✓ | ✗ |
| OPTIONS | 查询支持方法 | ✓ | ✓ | ✗ |

### HTTP 状态码

```
1xx 信息:
  100 Continue, 101 Switching Protocols (WebSocket)

2xx 成功:
  200 OK, 201 Created, 204 No Content

3xx 重定向:
  301 Moved Permanently, 302 Found, 304 Not Modified

4xx 客户端错误:
  400 Bad Request, 401 Unauthorized, 403 Forbidden
  404 Not Found, 405 Method Not Allowed, 429 Too Many Requests

5xx 服务器错误:
  500 Internal Server Error, 502 Bad Gateway
  503 Service Unavailable, 504 Gateway Timeout
```

### HTTP/2 特性

| 特性 | 说明 |
|------|------|
| 二进制分帧 | 取代 HTTP/1.1 的文本格式 |
| 多路复用 | 一个 TCP 连接并发多个流 |
| HPACK 头部压缩 | 静态/动态字典减少开销 |
| 服务器推送 | 主动推送关联资源 |
| 流优先级 | 设置资源加载优先级 |

### HTTP/3 (QUIC)

```
HTTP/3
  │
QUIC (基于 UDP)
  │
TLS 1.3 (内置)
  │
UDP

QUIC 优势：
  - 0-RTT 连接建立（重复连接时）
  - 连接迁移（切换网络不中断）
  - 消除 TCP 队头阻塞
  - 内置加密（TLS 1.3 强制）
```

## 6. 电子邮件协议

| 协议 | 端口 | 功能 | 特点 |
|------|------|------|------|
| SMTP | 25/587/465 | 发送邮件 | 推送协议 |
| POP3 | 110/995 | 接收邮件 | 下载后本地管理 |
| IMAP | 143/993 | 同步邮件 | 服务器端管理 |

## 7. FTP/TFTP

| 协议 | 端口 | 传输方式 | 认证 | 特点 |
|------|------|---------|------|------|
| FTP | 21(控制)+20(数据) | TCP | 用户名/密码或匿名 | 支持主动/被动模式 |
| TFTP | 69 | UDP | 无认证 | 简单，用于网络设备引导 |

### FTP 模式

```
主动模式 (Active):
  客户端(随机端口N) ──控制(21)──► 服务器
  客户端(端口N+1)  ◄──数据(20)── 服务器
  (服务器主动连客户端)

被动模式 (Passive):
  客户端(随机端口N) ──控制(21)──► 服务器
  客户端(端口N+1)  ──数据(>=1024)──► 服务器
  (客户端主动连服务器，PASV命令)
```

## 8. SNMP（简单网络管理协议）

SNMP 用于网络设备监控和管理。

| 版本 | 安全特性 | 特点 |
|------|---------|------|
| SNMPv1 | 团体名(明文) | 基本功能 |
| SNMPv2c | 团体名(明文) | 增加批量操作 |
| SNMPv3 | 加密+认证 | 完整安全 |

```
管理体系结构：
  NMS (网络管理系统) ←→ 被管设备 (路由器/交换机)
      使用 SNMP 协议
                            ┌─────────────────┐
                            │     MIB          │
  NMS ──GetRequest──►  ────│ (管理信息库)      │
  NMS ◄──GetResponse──      │ .1.3.6.1.2.1.1  │
  NMS ──SetRequest──►  ────│ .1.3.6.1.2.1.2  │
  Agent ◄──Trap─────── NMS  │ ...              │
                            └─────────────────┘
```

## 9. TLS/SSL

### TLS 握手过程（TLS 1.3）

```
客户端                         服务器
  │                              │
  │ ClientHello                  │
  │ (TLS版本, 密码套件, 随机数)   │
  │─────────────────────────────►│
  │                              │
  │ ServerHello                  │
  │ (选定版本/密码套件, 随机数)    │
  │◄─────────────────────────────│
  │ EncryptedExtensions          │
  │ Certificate + Verify         │
  │◄─────────────────────────────│
  │                              │
  │ Finished                     │
  │─────────────────────────────►│
  │                              │
  │ [加密通信开始]               │
  │◄════════════════════════════►│
```

## 10. 协议对比总表

| 协议 | 层 | 传输层 | 端口 | 用途 |
|------|-----|--------|------|------|
| ARP | 链路/网络 | — | — | IP→MAC 解析 |
| ICMP | 网络层 | — | — | 差错报告/诊断 |
| DHCP | 应用层 | UDP | 67/68 | 动态 IP 分配 |
| DNS | 应用层 | UDP/TCP | 53 | 域名解析 |
| HTTP | 应用层 | TCP | 80 | Web 访问 |
| HTTPS | 应用层 | TCP | 443 | 加密 Web |
| FTP | 应用层 | TCP | 20/21 | 文件传输 |
| TFTP | 应用层 | UDP | 69 | 简单文件传输 |
| SMTP | 应用层 | TCP | 25/587 | 发送邮件 |
| POP3 | 应用层 | TCP | 110/995 | 接收邮件 |
| IMAP | 应用层 | TCP | 143/993 | 邮件同步 |
| SNMP | 应用层 | UDP | 161/162 | 网络管理 |
| SSH | 应用层 | TCP | 22 | 远程登录 |
| WebSocket | 应用层 | TCP | 80/443 | 全双工通信 |
| QUIC | 传输层 | UDP | 443 | 低延迟传输 |

---

## 相关条目

- [[NetworkSecurity]]
- [[WirelessNetworks]]
- [[Cybersecurity]]

## 参考资源

- 《TCP/IP 详解 卷1：协议》(Stevens)
- IETF RFC 文档
- 《计算机网络：自顶向下方法》(Kurose & Ross)
- MDN Web 文档 (HTTP)
