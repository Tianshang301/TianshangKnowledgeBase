# 网络安全完全指南

## 概述

网络安全（Cybersecurity）是保护计算机系统、网络和数据免受数字攻击、损害和未授权访问的实践。随着数字化转型的深入，网络安全已成为组织运营的核心环节。

---

## 一、安全基础：CIA 三元组

CIA 三元组是信息安全的基石模型：

| 属性 | 定义 | 威胁 | 防护措施 |
|------|------|------|----------|
| 机密性 (Confidentiality) | 信息不被未授权访问 | 数据泄露、窃听 | 加密、访问控制 |
| 完整性 (Integrity) | 信息不被未授权修改 | 篡改、重放攻击 | 哈希、数字签名 |
| 可用性 (Availability) | 信息在需要时可用 | DDoS、勒索软件 | 冗余、备份、DDoS 防护 |

扩展模型还包含：真实性（Authenticity）、可追溯性（Accountability）、不可否认性（Non-repudiation）。

---

## 二、密码学

### 2.1 对称加密

| 算法 | 密钥长度 | 分组大小 | 模式 | 安全性 |
|------|---------|----------|------|--------|
| AES | 128/192/256 bit | 128 bit | ECB, CBC, GCM, CTR | 安全（推荐） |
| DES | 56 bit | 64 bit | ECB, CBC | 不安全（可暴力破解） |
| 3DES | 112/168 bit | 64 bit | — | 已弃用，速度慢 |
| ChaCha20 | 256 bit | 流加密 | 与 Poly1305 组合 | 安全（移动端广泛使用） |

```
AES 加密流程 (128-bit):
  明文 → AddRoundKey → SubBytes → ShiftRows → MixColumns → ... → Ciphertext
  10/12/14 轮 (取决于密钥长度 128/192/256)
```

### 2.2 非对称加密

RSA 算法基于大整数分解的困难性：

$$c = m^e \mod n \quad\text{(加密)}$$
$$m = c^d \mod n \quad\text{(解密)}$$

其中 $n = pq$，$p$ 和 $q$ 为大素数，$e \cdot d \equiv 1 \pmod{\phi(n)}$。

| 算法 | 安全性基础 | 密钥长度 | 性能 | 用途 |
|------|-----------|----------|------|------|
| RSA | 大整数分解 | 2048-4096 bit | 慢 | 密钥交换、数字签名 |
| ECC (ECDSA, EdDSA) | 椭圆曲线离散对数 | 256 bit ≈ RSA 3072 | 快 | 数字签名、密钥交换 |
| Diffie-Hellman | 离散对数问题 | 2048+ bit | 中等 | 密钥交换 |

### 2.3 哈希函数

| 算法 | 输出长度 | 安全性 | 应用 |
|------|---------|--------|------|
| MD5 | 128 bit | 不安全（碰撞已展示） | 已弃用 |
| SHA-1 | 160 bit | 不安全（SHAttered 攻击） | 已弃用 |
| SHA-256 | 256 bit | 安全 | 区块链、证书、TLS |
| SHA-3 | 可变 | 安全 | 新一代标准 |
| HMAC | 可变 | 安全 | 消息认证 |

### 2.4 数字签名

```
签名流程:
  消息 → Hash → 私钥加密 → 签名

验证流程:
  消息 → Hash → 公钥解密签名 → 比较哈希值

非对称加密 + 哈希 → 既保证完整性又保证认证性
```

---

## 三、认证与访问控制

### 3.1 认证方法

| 因素 | 类型 | 示例 | 安全性 |
|------|------|------|--------|
| 知识因素 | 你知道什么 | 密码、PIN | 低（易钓鱼） |
| 持有因素 | 你有什么 | 手机（TOTP）、硬件密钥 | 中 |
| 固有因素 | 你是什么 | 指纹、面部、虹膜 | 高 |
| 行为因素 | 你做什么 | 签名、打字节奏 | 中 |

MFA（多因素认证）组合两种以上因素，显著提高安全性。

### 3.2 访问控制模型

| 模型 | 全称 | 原理 | 应用 |
|------|------|------|------|
| DAC | Discretionary AC | 资源所有者管理权限 | Windows/Unix 文件系统 |
| MAC | Mandatory AC | 系统强制标签控制 | 军事/government 系统 |
| RBAC | Role-Based AC | 角色 → 权限映射 | 企业应用（最广泛） |
| ABAC | Attribute-Based AC | 基于属性（用户、资源、环境）策略 | 云服务、微服务 |

```
RBAC 示例:
  ┌──────┐    ┌──────┐    ┌──────────┐
  │ 用户A │───▶│ 管理员 │───▶│ 创建用户  │
  ├──────┤    │ 角色  │    │ 删除用户  │
  │ 用户B │───▶│       │    │ 修改配置  │
  ├──────┤    └──────┘    └──────────┘
  │ 用户C │───▶│ 普通用户 │───▶│ 查看文章  │
  └──────┘    └──────┘    │ 发表评论  │
                          └──────────┘
```

---

## 四、网络安全

| 技术 | 功能 | 层级 |
|------|------|------|
| 防火墙 | 基于规则的流量过滤 | 网络层/传输层 |
| IDS (入侵检测系统) | 监控告警异常流量 | 网络层/应用层 |
| IPS (入侵防御系统) | 检测并自动阻断 | 网络层/应用层 |
| VPN (虚拟专用网络) | 加密隧道保护通信 | 网络层（IPSec）/传输层（TLS）|
| WAF (Web 应用防火墙) | 过滤 HTTP/HTTPS 恶意请求 | 应用层 |
| DDoS 缓解 | 过滤恶意流量，保持可用性 | 多层 |

```
VPN 隧道协议对比:
  协议       | 端口 | 加密 | 速度
  IPsec/IKEv2| 500/UDP | AES-256 | 快
  OpenVPN    | 1194/UDP| AES-256 | 中等
  WireGuard  | 51820/UDP| ChaCha20 | 最快
  SSTP       | 443/TCP | AES-256 | 受限于 TCP
```

---

## 五、Web 安全：OWASP Top 10

### 5.1 核心漏洞

| 类别 | 原理 | 攻击示例 | 防护 |
|------|------|----------|------|
| SQL 注入 | 未过滤的用户输入拼入 SQL | `' OR 1=1 --` | 参数化查询、ORM |
| XSS (跨站脚本) | 恶意脚本注入页面 | `<script>stealCookie()</script>` | 输出转义、CSP |
| CSRF | 跨站伪造请求 | 诱导用户点击恶意链接 | CSRF Token、SameSite Cookie |
| SSRF | 服务端请求伪造 | 访问内网 `http://169.254.169.254/` | 白名单、URL 限制 |

```
SQL 注入示例:
  原始查询: SELECT * FROM users WHERE username = '$input' AND password = '$pass'
  恶意输入: username = admin' -- 
  实际查询: SELECT * FROM users WHERE username = 'admin' -- ' AND password = 'xxx'
  → 绕过认证！

  防护: 使用参数化查询
  cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
```

### 5.2 其他关键漏洞

- **不安全的反序列化**: 攻击者构造恶意序列化数据导致 RCE
- **已知漏洞组件**: 使用含有 CVE 的第三方库
- **认证失效**: 弱密码、无 MFA、会话固定
- **敏感数据泄露**: 未加密存储、日志泄露

---

## 六、恶意软件分析

| 类型 | 特征 | 传播方式 | 典型行为 |
|------|------|----------|----------|
| 病毒 (Virus) | 感染其他文件 | 文件共享、USB | 破坏数据、消耗资源 |
| 蠕虫 (Worm) | 自我复制，不需要宿主 | 网络漏洞自动传播 | 消耗带宽、传播载荷 |
| 木马 (Trojan) | 伪装成正常软件 | 社交工程 | 后门、窃取数据 |
| 勒索软件 (Ransomware) | 加密文件索要赎金 | 钓鱼邮件、漏洞利用 | 加密 + 勒索信 |
| Rootkit | 隐藏自身存在 | 驱动/内核级 | 维持持久化访问 |

---

## 七、渗透测试方法论

渗透测试（Penetration Testing）模拟攻击者视角评估安全性。

```
标准流程:
  1. 信息收集 (Reconnaissance)
     - 被动: OSINT, DNS 查询, Shodan
     - 主动: 端口扫描 (nmap), 目录枚举
  2. 漏洞分析
     - 自动化扫描 (Nessus, OpenVAS)
     - 手动验证
  3. 漏洞利用 (Exploitation)
     - Metasploit, CVE PoC
  4. 权限提升
     - 提权漏洞、凭证窃取 (Mimikatz)
  5. 横向移动
     - 内网扫描、凭据复用
  6. 痕迹清除
     - 日志清理、持久化后门移除
  7. 报告输出
```

---

## 八、数字取证

```
取证原则 (Locard's Exchange Principle):
  "每次接触都会留下痕迹"
  
取证流程:
  1. 保全现场 (隔离、拍照)
  2. 获取证据 (磁盘镜像: dd, FTK Imager)
  3. 分析证据 (文件系统、日志、内存: Volatility)
  4. 时间线重建
  5. 形成报告 (法庭可接受)
```

---

## 九、安全标准与框架

| 标准 | 组织 | 范围 | 关键要求 |
|------|------|------|----------|
| ISO 27001 | ISO | ISMS 管理体系 | 风险评估、安全控制、持续改进 |
| NIST CSF | NIST | 整体网络安全 | 识别、保护、检测、响应、恢复 |
| PCI DSS | PCI SSC | 支付卡数据 | 加密、访问控制、日志审计 |
| SOC 2 | AICPA | 服务组织 | 安全性、可用性、机密性等 |

---

## 十、零信任架构

零信任（Zero Trust）的核心原则：**Never trust, always verify**。

```
传统模型 (边界安全):
  内部网络 = 可信
  外部网络 = 不可信
  缺点: 一旦突破边界，内部横行无阻

零信任模型:
  永不信任，始终验证
  假设已沦陷 (Assume Breach)
  最小权限 (Least Privilege)
  微隔离 (Micro-segmentation)

关键组件:
  - IAM (身份和访问管理)
  - MFA (多因素认证)
  - 持续验证 (访问时、访问后)
  - 加密 (传输中 + 静态)
  - 日志和监控 (SIEM/SOAR)
```

---

## 相关条目

- [[NetworkSecurity]]
- Cryptography
- [[AIEthics]]
- [[Blockchain]]

## 参考资源

- 《网络安全基础》— Stallings & Brown
- OWASP Top 10: https://owasp.org/www-project-top-ten
- NIST Cybersecurity Framework: https://www.nist.gov/cyberframework
- MITRE ATT&CK: https://attack.mitre.org
- 《The Web Application Hacker's Handbook》— Stuttard & Pinto
- ISO 27001 标准文档
