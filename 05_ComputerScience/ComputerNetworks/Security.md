---
aliases: [Security]
tags: ['ComputerNetworks', 'Security']
---

# 网络安全详解 (Network Security)

## 1. 对称加密 (Symmetric Encryption)

加密和解密使用相同的密钥。

### 常见算法

| 算法 | 密钥长度 | 块大小 | 状态 | 说明 |
|------|---------|--------|------|------|
| **DES** | 56位 | 64位 | 不安全 | 1997年被破解 |
| **3DES** | 112/168位 | 64位 | 已弃用 | DES三次, 速度慢 |
| **AES** | 128/192/256位 | 128位 | 安全 | 当前标准 |
| **SM4** | 128位 | 128位 | 安全 | 中国国家标准 |
| **ChaCha20** | 256位 | 流密码 | 安全 | 移动端性能好 |

### AES 加密模式

| 模式 | 描述 | 特点 | 适用 |
|------|------|------|------|
| **ECB** | 电子密码本 | 简单, 不安全(相同明文→相同密文) | 不推荐 |
| **CBC** | 密码分组链接 | 需要IV, 串行加密 | 文件加密 |
| **CFB** | 密文反馈 | 流模式, 可加密任意长度 | 实时通信 |
| **OFB** | 输出反馈 | 流模式, 可预处理 | 卫星通信 |
| **CTR** | 计数器 | 流模式, 可并行 | 磁盘加密 |
| **GCM** | Galois/Counter | 认证加密(AEAD) | TLS 1.2/1.3 |

```python
# Python AES-GCM 示例
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import os

# AES-256-GCM 加密
key = AESGCM.generate_key(bit_length=256)  # 32字节
aesgcm = AESGCM(key)
nonce = os.urandom(12)  # 推荐96位nonce
ciphertext = aesgcm.encrypt(nonce, b"Hello, World!", None)
plaintext = aesgcm.decrypt(nonce, ciphertext, None)
print(plaintext.decode())  # Hello, World!
```

## 2. 非对称加密 (Asymmetric Encryption)

使用公钥加密、私钥解密（或反之）。

### RSA

```python
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes

# 生成密钥对 (2048位)
private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048
)
public_key = private_key.public_key()

# 加密 (使用公钥)
message = b"Secret Message"
ciphertext = public_key.encrypt(
    message,
    padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
    )
)

# 解密 (使用私钥)
plaintext = private_key.decrypt(
    ciphertext,
    padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
    )
)
```

### RSA 性能与限制

| 密钥长度 | 安全级别 | 加密速度 | 最大加密数据 |
|---------|---------|---------|------------|
| 1024位 | 80bit | 快 | 不安全(已破解) |
| 2048位 | 112bit | 中 | 117字节 |
| 4096位 | 128bit | 慢 | 245字节 |

### ECC (Elliptic Curve Cryptography)

```
ECC 优势: 更短的密钥达到相同安全级别

安全级别  RSA密钥长度  ECC密钥长度
80bit     1024位       160位
112bit    2048位       224位
128bit    3072位       256位 (如P-256)
256bit    15360位      512位 (如P-521)
```

### Diffie-Hellman 密钥交换

```
Alice                          Bob
   │                             │
   │ 选择素数p=23, 生成元g=5     │
   │────────────────────────────►│
   │                             │
   │ 选随机数a=6                 │  选随机数b=15
   │ A = g^a mod p              │  B = g^b mod p
   │   = 5^6 mod 23 = 8         │    = 5^15 mod 23 = 19
   │                             │
   │────── A=8 ────────────────►│
   │◄────── B=19 ───────────────│
   │                             │
   │ s = B^a mod p              │  s = A^b mod p
   │   = 19^6 mod 23 = 2        │    = 8^15 mod 23 = 2
   │                             │
   │   共享密钥 s=2 !!!          │
```

### 数字签名

```python
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec

# 使用ECDSA签名
private_key = ec.generate_private_key(ec.SECP256R1())
public_key = private_key.public_key()

message = b"Important document"

# 签名
signature = private_key.sign(
    message,
    ec.ECDSA(hashes.SHA256())
)

# 验签
try:
    public_key.verify(signature, message, ec.ECDSA(hashes.SHA256()))
    print("签名验证成功")
except:
    print("签名验证失败")
```

## 3. 哈希函数 (Hash Functions)

### 常见哈希算法

| 算法 | 输出长度 | 安全 | 用途 |
|------|---------|------|------|
| **MD5** | 128位 | 不安全(碰撞可构造) | 已废弃 |
| **SHA-1** | 160位 | 不安全(SHAttered攻击) | 已废弃 |
| **SHA-256** | 256位 | 安全 | TLS, 签名 |
| **SHA-384** | 384位 | 安全 | 美国政府标准 |
| **SHA-512** | 512位 | 安全 | 高性能(64位CPU) |
| **SHA-3** | 可变 | 安全 | 新一代标准 |
| **BLAKE2** | 可变 | 安全 | 比SHA-3快 |
| **bcrypt** | 可变 | 安全 | 密码存储(慢哈希) |
| **Argon2** | 可变 | 安全 | 密码存储(当前推荐) |

### 密码存储 (Password Hashing)

```python
import bcrypt

# 注册: 存储哈希
password = b"my_secure_password"
salt = bcrypt.gensalt(rounds=12)  # 12轮, 约250ms
hashed = bcrypt.hashpw(password, salt)
# 存储 hashed 到数据库

# 登录: 验证密码
input_password = b"my_secure_password"
if bcrypt.checkpw(input_password, hashed):
    print("密码正确")
else:
    print("密码错误")
```

## 4. PKI 与证书 (Public Key Infrastructure)

### X.509 证书结构

```
证书:
├── 版本 (v1/v2/v3)
├── 序列号
├── 签名算法 (SHA256-RSA)
├── 颁发者 (Issuer, 如 "CN=Let's Encrypt R3")
├── 有效期
│   ├── 起始时间
│   └── 结束时间
├── 主体 (Subject, 如 "CN=*.example.com")
├── 公钥
│   ├── 算法 (RSA/ECDSA)
│   └── 公钥值
├── 扩展
│   ├── Subject Alternative Names (SAN)
│   ├── Key Usage (digitalSignature, keyEncipherment)
│   ├── Extended Key Usage (serverAuth, clientAuth)
│   └── CA标志
└── 签名 (由颁发者私钥签名)
```

### 查看证书

```bash
# 查看服务器证书
openssl s_client -connect example.com:443 -showcerts

# 查看证书详情
openssl x509 -in cert.pem -text -noout

# 查看证书链
openssl s_client -connect example.com:443 -showcerts 2>/dev/null

# 下载证书
openssl s_client -connect example.com:443 </dev/null 2>/dev/null \
  | sed -n '/-----BEGIN/,/-----END/p' > cert.pem
```

### 证书类型

| 类型 | 验证级别 | 审核 | 地址栏显示 | 价格 |
|------|---------|------|-----------|------|
| DV (Domain Validated) | 域名控制权验证 | 自动 | 无 | 免费(Let's Encrypt) |
| OV (Organization Validated) | 企业信息验证 | 人工 | 无 | $50-200/年 |
| EV (Extended Validation) | 严格验证 | 深度审核 | 绿色公司名 | $200-500/年 |

### 自签名证书

```bash
# 创建自签名证书
openssl req -x509 -newkey rsa:2048 -nodes \
  -keyout key.pem -out cert.pem \
  -days 365 \
  -subj "/CN=localhost" \
  -addext "subjectAltName=DNS:localhost,DNS:*.example.com,IP:127.0.0.1"

# 创建CA并签发证书
# 1. 创建CA私钥和自签名证书
openssl req -x509 -newkey rsa:4096 -nodes \
  -keyout ca-key.pem -out ca-cert.pem \
  -days 3650 -subj "/CN=My CA"

# 2. 创建服务器私钥和证书签名请求(CSR)
openssl req -newkey rsa:2048 -nodes \
  -keyout server-key.pem -out server.csr \
  -subj "/CN=myserver.local"

# 3. 用CA签发服务器证书
openssl x509 -req -in server.csr \
  -CA ca-cert.pem -CAkey ca-key.pem -CAcreateserial \
  -out server-cert.pem -days 365 \
  -extfile <(echo "subjectAltName=DNS:myserver.local")
```

## 5. TLS/SSL 握手

### TLS 1.2 完整握手 (2-RTT)

```
客户端                                   服务器
   │                                        │
   │ ClientHello                            │
   │   最高支持TLS 1.2                      │
   │   密码套件列表(如TLS_RSA_WITH_AES_128_GCM_SHA256)│
   │   随机数random_C                       │
   │───────────────────────────────────────►│
   │                                        │
   │ ServerHello                            │
   │   选择TLS 1.2                          │
   │   选择密码套件                          │
   │   随机数random_S                       │
   │   服务器证书                           │
   │   ServerHelloDone                      │
   │◄───────────────────────────────────────│
   │                                        │
   │ 客户端验证证书                          │
   │ 生成预主密钥(premaster secret)           │
   │ 用服务器公钥加密                        │
   │                                        │
   │ ClientKeyExchange                      │
   │   加密的premaster secret                │
   │───────────────────────────────────────►│
   │                                        │
   │ (双方计算主密钥: master_secret)          │
   │                                        │
   │ ChangeCipherSpec                       │
   │ Finished (加密)                        │
   │───────────────────────────────────────►│
   │                                        │
   │ ChangeCipherSpec                       │
   │ Finished (加密)                        │
   │◄───────────────────────────────────────│
   │                                        │
   │ 开始加密应用数据传输                     │
```

### TLS 1.3 改进

| 特性 | TLS 1.2 | TLS 1.3 |
|------|---------|---------|
| 握手往返 | 2-RTT | 1-RTT (0-RTT复用) |
| 支持的密码套件 | 37 | 5 |
| 静态RSA密钥交换 | 支持 | 不支持(PFS强制) |
| 0-RTT | 不支持 | 支持 |
| 会话恢复 | Session ID/Ticket | PSK |
| 移除不安全特性 | - | 移除RC4, 3DES, CBC, EXPORT等 |

## 6. 常见攻击

### 6.1 中间人攻击 (MITM)

```
正常通信:                        MITM攻击:
客户端 ←→ 服务器                 客户端 ←→ 攻击者 ←→ 服务器
  (直接加密)                      (客户端以为和服务器通信)
                                  (攻击者解密/修改/重加密)

常见MITM:
- ARP欺骗 (局域网)
- DNS欺骗 (缓存投毒)
- Rogue AP (假WiFi)
- SSL剥离 (强制降级到HTTP)
```

### 6.2 DDoS (分布式拒绝服务)

| 攻击类型 | 描述 | 防御 |
|---------|------|------|
| SYN Flood | 大量SYN包不完成握手 | SYN Cookie |
| UDP Flood | 大流量UDP包 | 速率限制 |
| HTTP Flood | 大量HTTP请求 | WAF, 验证码 |
| DNS Amplification | 伪造源IP的DNS查询 | 关闭递归 |
| Slowloris | 慢速HTTP请求耗尽连接 | 限制超时 |

### 6.3 其他攻击

| 攻击 | 描述 | 防御 |
|------|------|------|
| DNS欺骗/投毒 | 污染DNS缓存 | DNSSEC |
| Session Hijacking | 窃取会话Cookie | HttpOnly, Secure flag |
| CSRF | 跨站请求伪造 | CSRF Token, SameSite Cookie |
| XSS | 跨站脚本攻击 | 输入验证, CSP |
| SQL注入 | 恶意SQL输入 | 参数化查询 |
| Path Traversal | 路径穿越 | 路径过滤 |

### SYN Flood 示例

```
攻击者: 发送大量SYN包(源IP伪造)
服务器: 每个SYN创建半开连接(SYN_RCVD), 发送SYN+ACK, 等待ACK
        半开连接占满队列后, 合法连接被拒绝

防御 - SYN Cookie:
1. 收到SYN时不分配连接, 而是用源/目标IP+端口+seq计算Cookie
2. 作为初始seq号发回(SYN+ACK)
3. 收到ACK时验证Cookie值
4. 若合法才分配连接
```

```bash
# Linux SYN Cookie (默认启用)
sysctl net.ipv4.tcp_syncookies
sysctl -w net.ipv4.tcp_syncookies=1
```

## 7. 防火墙 (Firewall)

### 防火墙类型

| 类型 | 工作层 | 特点 | 性能 |
|------|--------|------|------|
| **包过滤** | L3/L4 | 检查IP/端口, 速度快 | 高 |
| **状态检测** | L3-L4 | 跟踪连接状态, 自动允许回包 | 中 |
| **应用层** | L7 | 深度包检测(DPI), 检查内容 | 低 |
| **WAF** | L7 | 专门保护HTTP应用 | 中 |

### iptables / nftables 示例

```bash
# iptables 规则示例
# 放行SSH
iptables -A INPUT -p tcp --dport 22 -j ACCEPT

# 放行HTTP/HTTPS
iptables -A INPUT -p tcp -m multiport --dports 80,443 -j ACCEPT

# 放行已建立连接
iptables -A INPUT -m state --state ESTABLISHED,RELATED -j ACCEPT

# 拒绝所有其他入站
iptables -P INPUT DROP

# NAT转发
iptables -t nat -A PREROUTING -p tcp --dport 80 -j DNAT --to-destination 10.0.1.10:8080
iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE

# 保存规则
iptables-save > /etc/iptables/rules.v4
```

## 8. IDS/IPS & WAF

| 系统 | 描述 | 示例 |
|------|------|------|
| **IDS** (入侵检测) | 监控告警(被动) | Snort, Suricata |
| **IPS** (入侵防御) | 监控并阻止(主动) | Snort inline, Suricata IPS |
| **WAF** (Web应用防火墙) | 保护HTTP应用 | ModSecurity, Cloudflare WAF |

```bash
# ModSecurity规则示例
SecRule REQUEST_URI "@contains /admin" \
    "id:1001,phase:1,deny,status:403,msg:'Admin access blocked'"

SecRule ARGS "@detectSQLi" \
    "id:2001,phase:2,block,msg:'SQL Injection detected'"

SecRule REQUEST_BODY "@rx (javascript:|<script|onerror=)" \
    "id:3001,phase:2,block,msg:'XSS attempt detected'"
```

## 9. VPN (Virtual Private Network)

### 常见VPN协议

| 协议 | 端口 | 加密 | 速度 | 安全性 |
|------|------|------|------|--------|
| **IPsec (IKEv2)** | UDP 500/4500 | AES-256 | 快 | 高 |
| **OpenVPN** | UDP 1194/TCP 443 | AES-256 | 中 | 高 |
| **WireGuard** | UDP 51820 | ChaCha20 | 最快 | 高 |
| **L2TP/IPsec** | UDP 1701/500/4500 | AES-256 | 慢 | 中 |
| **PPTP** | TCP 1723 | MPPE | 快 | 不安全(已弃用) |

### IPsec 工作模式

```
传输模式 (Transport Mode):
┌────────────────┐
│ IP头 │ ESP头│ 数据 │ ESP尾│ ESP认证│
└────────────────┘

隧道模式 (Tunnel Mode):
┌────────────────────────────────┐
│ 外IP头 │ ESP头│ 内IP头 │ 数据 │ ESP尾│ ESP认证│
└────────────────────────────────┘
```

### WireGuard 配置

```ini
# /etc/wireguard/wg0.conf

# 服务器端
[Interface]
Address = 10.0.0.1/24
PrivateKey = <服务器私钥>
ListenPort = 51820

[Peer]
PublicKey = <客户端公钥>
AllowedIPs = 10.0.0.2/32

# 客户端
[Interface]
Address = 10.0.0.2/24
PrivateKey = <客户端私钥>
DNS = 1.1.1.1

[Peer]
PublicKey = <服务器公钥>
Endpoint = vpn.example.com:51820
AllowedIPs = 0.0.0.0/0, ::/0  # 全流量VPN
PersistentKeepalive = 25
```

```bash
# WireGuard 管理
wg genkey | tee privatekey | wg pubkey > publickey   # 生成密钥对
wg-quick up wg0                                       # 启动
wg-quick down wg0                                     # 停止
wg show                                                # 查看状态
systemctl enable wg-quick@wg0                          # 开机启动
\`\`\`

## 相关条目

- [[NetworkSecurity]]
- [[网络攻防技术]]
- [[TransportLayer]]
- [[HTTP]]
