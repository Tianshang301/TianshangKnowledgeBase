---
aliases: [NetworkSecurity]
tags: ['ComputerNetworks', 'NetworkSecurity', 'NetworkSecurity']
created: 2026-05-16
updated: 2026-05-16
---

# 网络安全 (Network Security)

## 1. 威胁态势 (Threat Landscape)

### 恶意软件类型

| 类型 | 描述 | 传播方式 | 示例 |
|------|------|---------|------|
| 病毒 (Virus) | 寄生于正常文件 | 文件共享、邮件附件 | CIH, Melissa |
| 蠕虫 (Worm) | 自我复制传播 | 网络漏洞利用 | Morris, Conficker |
| 木马 (Trojan) | 伪装为合法软件 | 社会工程学 | Zeus, Emotet |
| 勒索软件 (Ransomware) | 加密文件索要赎金 | 钓鱼邮件、漏洞利用 | WannaCry, LockBit |
| 间谍软件 (Spyware) | 窃取信息 | 捆绑安装 | Pegasus |
| Rootkit | 隐藏自身及恶意活动 | 内核级感染 | Sony BMG Rootkit |
| 僵尸网络 (Botnet) | 受控的感染设备群 | 多种方式 | Mirai, Emotet |

### 常见网络攻击

| 攻击类型 | 原理 | 防御措施 |
|---------|------|---------|
| **DDoS** | 多源流量淹没目标 | CDN 清洗、速率限制、Anycast |
| **Phishing** | 伪造可信页面骗取凭证 | 邮件过滤、安全意识培训、MFA |
| **MitM** | 拦截通信篡改数据 | HTTPS、证书固定、VPN |
| **ARP 欺骗** | 伪造 ARP 响应劫持流量 | DAI、DHCP Snooping |
| **DNS 劫持** | 篡改 DNS 响应 | DNSSEC、DoH/DoT |
| **SYN Flood** | 半连接耗尽资源 | SYN Cookie、连接限制 |
| **SQL 注入** | Web 应用输入注入 | 参数化查询、WAF |
| **XSS** | 注入恶意脚本到网页 | CSP、输入转义 |
| **CSRF** | 跨站请求伪造 | Anti-CSRF Token、SameSite Cookie |
| **会话劫持** | 窃取 Session ID | HTTPS、Secure/HttpOnly Cookie |

```
DDoS 攻击层级：
  应用层 (L7)      ─── HTTP Flood, Slowloris
  传输层 (L4)      ─── SYN Flood, UDP Flood
  网络层 (L3)      ─── ICMP Flood, IP Spoofing
  链路层 (L2)      ─── MAC Flooding
```

## 2. 防火墙 (Firewall)

### 防火墙类型对比

| 类型 | 工作层 | 检查内容 | 性能 | 安全性 |
|------|-------|---------|------|--------|
| 包过滤 | L3/L4 | IP、端口、协议 | 高 | 低 |
| 状态检测 | L3/L4 | 连接状态 | 中高 | 中 |
| 应用层代理 | L7 | 应用协议内容 | 低 | 高 |
| 下一代防火墙(NGFW) | L3-L7 | 用户、应用、威胁情报 | 中 | 高 |

### 防火墙规则示例

```
# 包过滤防火墙规则
Access-list 100 permit tcp any any eq 80         # 允许 HTTP
Access-list 100 permit tcp any any eq 443        # 允许 HTTPS
Access-list 100 permit tcp 10.0.0.0 0.255.255.255 any eq 22  # 允许内网 SSH
Access-list 100 deny ip any any                  # 拒绝其他

# 状态检测防火墙（自动允许已建立连接的回程流量）
```

### WAF（Web 应用防火墙）

```
WAF 防护能力：
  ┌────────────────────────────────────────────┐
  │  SQL 注入检测    │  XSS 检测               │
  │  CSRF 防护       │  路径遍历检测            │
  │  CC 攻击防护     │  协议合规检查            │
  │  自定义规则引擎  │  机器学习检测            │
  └────────────────────────────────────────────┘

部署方式：
  云 WAF：Cloudflare, AWS WAF, Azure WAF
  硬件 WAF：F5, Imperva
  软件 WAF：ModSecurity, Nginx WAF
```

## 3. IDS/IPS（入侵检测/防御系统）

### 分类

| 类型 | 检测方式 | 响应 | 误报率 | 示例 |
|------|---------|------|--------|------|
| NIDS | 网络流量分析 | 告警 | 中 | Snort, Suricata |
| HIDS | 主机日志/系统调用 | 告警 | 低 | OSSEC, Wazuh |
| NIPS | 网络流量分析 | 阻断 | 高 | Palo Alto |
| HIPS | 主机行为监控 | 阻止 | 中 | CrowdStrike |

### 检测技术

```
签名检测 (Signature-based):
  ┌──────────────────────────────────────────┐
  │ 匹配已知攻击特征                           │
  │ 优点：准确率高、误报少                     │
  │ 缺点：无法检测未知攻击（0-day）            │
  │ 示例：Snort 规则库                        │
  └──────────────────────────────────────────┘

异常检测 (Anomaly-based):
  ┌──────────────────────────────────────────┐
  │ 基于基线行为模型判断                       │
  │ 优点：可检测未知攻击                       │
  │ 缺点：误报率高                             │
  │ 示例：机器学习行为分析                     │
  └──────────────────────────────────────────┘
```

## 4. VPN（虚拟专用网络）

### VPN 类型

```
Site-to-Site VPN (站点到站点):
  总部 ─── Internet ─── 分支
        [IPSec 隧道]       路由器/防火墙建立

Remote Access VPN (远程访问):
  员工 ─── Internet ─── 公司网络
        [TLS/SSL]         VPN 网关
```

### IPSec vs SSL VPN

| 特性 | IPSec VPN | SSL/TLS VPN |
|------|-----------|-------------|
| 工作层 | L3（网络层） | L4-L7（传输层以上） |
| 客户端 | 需安装客户端 | 浏览器即可 |
| 加密粒度 | 整个网络流量 | 仅应用流量 |
| 灵活性 | 低 | 高 |
| 典型场景 | 站点到站点 | 远程接入 |
| 协议 | IKE + ESP/AH | TLS 1.2/1.3 |

### IPSec 协议

```
IPSec 组件：
  IKE (Internet Key Exchange)  ─── 密钥协商 (UDP 500)
  ESP (Encapsulating Security Payload) ─── 加密+认证
  AH (Authentication Header)     ─── 仅认证

传输模式 vs 隧道模式：
  传输模式: [IP 头][ESP 头][TCP/UDP][ESP 尾]
  隧道模式: [外 IP 头][ESP 头][内 IP 头][TCP/UDP][ESP 尾]
```

## 5. 密码学在网络中的应用

### 对称加密

| 算法 | 密钥长度 | 块大小 | 特点 |
|------|---------|--------|------|
| AES | 128/192/256 | 128bit | 现代标准，广泛使用 |
| 3DES | 168 | 64bit | 过时，逐渐淘汰 |
| ChaCha20 | 256 | 流密码 | 移动设备高效 |

### 非对称加密

| 算法 | 密钥长度 | 特点 | 用途 |
|------|---------|------|------|
| RSA | 2048/4096 | 基于大数分解 | 数字签名、密钥交换 |
| ECC | 256/384 | 基于椭圆曲线 | 更短的密钥相同安全度 |
| Ed25519 | 256 | EdDSA 签名 | 高性能签名 |

### TLS 密码套件

```
示例：TLS_AES_128_GCM_SHA256
         │    │      │
      密钥交换 加密算法  HMAC 算法

RSA 密钥交换: 使用 RSA 加密传输 Pre-Master Secret
ECDHE 密钥交换: 使用 ECDH 临时密钥，前向安全性
```

### PKI（公钥基础设施）

```
PKI 组成：
  CA (Certificate Authority)   ─── 签发证书
  RA (Registration Authority)  ─── 审核身份
  CRL (Certificate Revocation List) ─── 吊销列表
  OCSP (Online Certificate Status Protocol) ─── 在线状态查询

证书链：
  根 CA (自签名，离线存储)
    └── 中间 CA
          └── 服务器证书 (example.com)
```

## 6. 无线安全

| 标准 | 加密 | 认证 | 状态 |
|------|------|------|------|
| WEP | RC4 (弱) | 共享密钥 | 已废弃 |
| WPA | TKIP/RC4 | 802.1X 或 PSK | 过时 |
| WPA2 | AES-CCMP | 802.1X 或 PSK | 当前标准 |
| WPA3 | AES-GCMP | SAE (同步认证) | 最新标准 |

## 7. 网络隔离 (Segmentation)

### VLAN

```
VLAN 划分：
  VLAN 10 ─── 服务器群  (192.168.10.0/24)
  VLAN 20 ─── 办公网络  (192.168.20.0/24)
  VLAN 30 ─── 访客网络  (192.168.30.0/24)
  VLAN 99 ─── 管理网络  (192.168.99.0/24)

VLAN 间路由：通过三层交换机或路由器实现
  802.1Q 标签：在以太网帧中插入 4 字节 VLAN 标签
```

### DMZ（非军事区）

```
                  Internet
                     │
              ┌──────┴──────┐
              │   防火墙     │
              └──────┬──────┘
                     │
        ┌────────────┼────────────┐
        │            │            │
    ┌───┴───┐   ┌───┴───┐   ┌───┴───┐
    │ Web   │   │  DNS  │   │  Email│   ← DMZ
    └───────┘   └───────┘   └───────┘
        │            │            │
        └────────────┼────────────┘
                     │
              ┌──────┴──────┐
              │  内网防火墙   │
              └──────┬──────┘
                     │
              ┌──────┴──────┐
              │   内部网络    │
              │  (数据库, AD)│
              └─────────────┘
```

## 8. 零信任架构 (Zero Trust)

### 核心原则

```
零信任三大原则：
  1. 始终验证 (Never Trust, Always Verify)
     不信任任何网络位置，持续验证身份

  2. 最小权限 (Least Privilege)
     仅授予完成任务所需的最小访问权限

  3. 假设被突破 (Assume Breach)
     默认网络已受损，分段保护、持续监控

传统模型 vs 零信任：
  传统: 内网可信 → 外网不可信 → 边界防护
  零信任: 无信任网络 → 身份验证 → 微隔离
```

### SASE（安全访问服务边缘）

```
SASE 融合网络与安全功能：
  ┌─────────────────────────────┐
  │   SD-WAN                    │
  │   SWG (安全 Web 网关)          │
  │   CASB (云访问安全代理)       │
  │   ZTNA (零信任网络访问)       │
  │   FWaaS (防火墙即服务)        │
  └─────────────────────────────┘
```

## 9. 安全协议

| 协议 | 端口 | 作用 | 替代 |
|------|------|------|------|
| HTTPS | 443 | HTTP + TLS 加密 | HTTP |
| SSH | 22 | 远程登录加密 | Telnet (23, 明文) |
| SFTP/FTPS | 22/990 | 安全文件传输 | FTP (明文) |
| SMTP over TLS | 587 | 加密邮件发送 | SMTP (25) |
| IMAPS/POP3S | 993/995 | 加密邮件接收 | IMAP/POP3 (明文) |
| DoH (DNS over HTTPS) | 443 | 加密 DNS 查询 | DNS (明文) |
| DoT (DNS over TLS) | 853 | 加密 DNS 查询 | DNS (明文) |
| DNSSEC | — | DNS 数据完整性 | DNS（无验证） |
| IPsec | 500/4500 | IP 层加密 | 无保护 IP |

---

## 相关条目

- [[05_ComputerScience/Cybersecurity/Cybersecurity|Cybersecurity]]
- Cryptography
- [[05_ComputerScience/ComputerNetworks/NetworkProtocols/NetworkProtocols|NetworkProtocols]]

## 参考资源

- 《网络安全基础》(Stallings)
- OWASP Top 10 (https://owasp.org/)
- NIST 网络安全框架
- RFC 8446 (TLS 1.3)
- 《零信任网络》(Kindervag)


