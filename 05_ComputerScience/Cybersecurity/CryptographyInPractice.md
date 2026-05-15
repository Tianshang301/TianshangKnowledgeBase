---
aliases: [CryptographyInPractice]
tags: ['Cybersecurity', 'CryptographyInPractice']
---

# 密码学实践指南

## 概述

密码学是网络安全的数学基础。从 HTTPS 到区块链，密码学算法在背后保障着数据的机密性、完整性和认证性。本章聚焦于实际工程中如何正确使用密码学原语。

---

## 一、对称加密

### 1.1 AES（Advanced Encryption Standard）

AES 是目前最广泛使用的对称加密算法，支持 128/192/256 位密钥，分组大小为 128 位。

```
AES 加密轮数:
  AES-128: 10 轮
  AES-192: 12 轮
  AES-256: 14 轮
```

### 1.2 AES 工作模式对比

| 模式 | 是否需要 IV | 并行性 | 密文长度 | 安全性 | 典型用途 |
|------|-------------|--------|----------|--------|----------|
| ECB | 否 | 可并行 | 同明文 | **不安全**（相同明文块产生相同密文）| 已弃用 |
| CBC | 是（16 字节随机）| 不可并行（加密），可并行（解密）| 同明文 | 安全，但需注意 Padding Oracle | 文件加密 |
| CTR | 是（nonce+counter）| 可并行 | 同明文 | 安全 | 磁盘加密 |
| GCM | 是（12 字节推荐）| 可并行 | 多出 16 字节 Tag | **安全（认证加密）** | TLS, SSH |

```python
# AES-GCM 正确示例 (Python + cryptography)
from cryptography.fernet import Fernet

key = Fernet.generate_key()
cipher = Fernet(key)
token = cipher.encrypt(b"secret data")
plain = cipher.decrypt(token)
```

### 1.3 密钥派生函数 (KDF)

| 算法 | 设计目标 | 抗 GPU | 推荐参数 | 用途 |
|------|----------|--------|----------|------|
| PBKDF2 | 迭代哈希 | 低（易 GPU 加速）| 600000 次迭代 | 兼容场景 |
| bcrypt | Blowfish 加密 + 迭代 | 中 | cost=12 | 密码存储 |
| Argon2id | 内存硬 + 时间硬 | 高（内存占用）| m=64MB, t=3, p=4 | **推荐（2015 PHC 冠军）** |

```
Argon2id 参数说明:
  m (memory):   内存占用 (KiB), 推荐 64×1024 = 64MB
  t (time):     迭代次数, 推荐 3
  p (parallel): 并行度, 推荐 4
  输出长度: 32 字节

密码哈希选择:
  新项目 → Argon2id (首选)
  遗留系统 → bcrypt (可接受)
  避免 → 单次 SHA-256 / MD5 / PBKDF2 少迭代
```

---

## 二、非对称加密

### 2.1 RSA

RSA 的安全性基于大整数分解问题的困难性。

$$n = p \times q \quad\text{(p, q 为大素数)}$$
$$\phi(n) = (p-1)(q-1)$$
$$e \times d \equiv 1 \pmod{\phi(n)}$$
$$c = m^e \mod n \quad\text{(加密)}$$
$$m = c^d \mod n \quad\text{(解密)}$$

| 密钥长度 | 安全等级 | 性能 | 推荐状态 |
|----------|----------|------|----------|
| 1024 bit | < 80 bit | 快 | **不安全，已弃用** |
| 2048 bit | 112 bit | 中等 | **当前最低要求** |
| 3072 bit | 128 bit | 慢 | 推荐（2030 年+）|
| 4096 bit | 150 bit | 很慢 | 长期安全需求 |

### 2.2 椭圆曲线密码 (ECC)

ECC 在相同安全强度下密钥长度远小于 RSA。

$$y^2 = x^3 + ax + b \mod p$$

| 安全等级 | RSA 密钥长度 | ECC 密钥长度 | 曲线 |
|----------|-------------|-------------|------|
| 80 bit | 1024 bit | 160-223 bit | secp160k1（不安全）|
| 112 bit | 2048 bit | 224-255 bit | secp224k1, NIST P-224 |
| 128 bit | 3072 bit | 256-383 bit | **secp256k1, P-256, Curve25519** |
| 256 bit | 15360 bit | 512+ bit | P-521 |

### 2.3 密钥交换与签名

| 方案 | 类型 | 安全属性 | 典型曲线 |
|------|------|----------|----------|
| ECDH | 密钥交换 | 前向安全性（结合 ephemeral）| X25519 |
| ECDSA | 数字签名 | 可认证、不可否认 | P-256, secp256k1 |
| EdDSA (Ed25519) | 数字签名 | 防侧信道，恒定时间 | Curve25519 |
| RSA-OAEP | 加密（带填充）| IND-CCA2 安全 | — |
| RSA-PSS | 数字签名 | 概率性签名方案 | — |

```python
# Ed25519 签名 (推荐)
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

private_key = Ed25519PrivateKey.generate()
signature = private_key.sign(b"message")

public_key = private_key.public_key()
public_key.verify(signature, b"message")
```

---

## 三、TLS/SSL

### 3.1 TLS 握手

```
TLS 1.3 握手 (简化):
  Client → Server: ClientHello (支持的密码套件、Key Share)
  Server → Client: ServerHello + 证书 + 签名验证 + 完成
  Client → Server: 完成

  1-RTT 即可完成握手
  之前握手的历史: TLS 1.2 需要 2-RTT

核心组件:
  - 证书 (X.509): 身份认证
  - 密钥交换: ECDHE (前向安全)
  - 对称加密: AES-GCM / ChaCha20-Poly1305
  - 完整性: HMAC / AEAD
```

### 3.2 密码套件

```
TLS 1.2 示例: TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256
  └─密钥交换 ──认证─── 对称加密 ────────── MAC

TLS 1.3 简化套件 (只有 5 个):
  TLS_AES_128_GCM_SHA256
  TLS_AES_256_GCM_SHA384
  TLS_CHACHA20_POLY1305_SHA256
  TLS_AES_128_CCM_SHA256
  TLS_AES_128_CCM_8_SHA256
```

### 3.3 证书验证

| 检查项 | 说明 | 常见问题 |
|--------|------|----------|
| 证书链 | 是否由信任的 CA 签发 | 自签名证书、中间证书缺失 |
| 域名匹配 | CN/SAN 是否匹配访问域名 | 通配符不匹配 |
| 有效期 | 是否在有效期内 | 过期证书 |
| 吊销状态 | CRL / OCSP 检查 | 已吊销证书仍然信任 |
| 密钥强度 | RSA ≥ 2048, ECC ≥ 256 | 1024 位弱密钥 |

### 3.4 安全配置

```
HSTS:
  Strict-Transport-Security: max-age=31536000; includeSubDomains; preload

Certificate Pinning (已不推荐，推荐 CA 证书固定):
  问题: 证书更换导致应用不可用
  替代: 使用 Certificate Transparency (CT) + Expect-CT

推荐工具:
  SSL Labs: https://www.ssllabs.com/ssltest/
  testssl.sh: 命令行 TLS 安全检测
```

---

## 四、SSH

| 密钥类型 | 算法 | 安全等级 | 推荐 |
|----------|------|----------|------|
| RSA | RSA | 2048+ bit | 兼容性好 |
| ECDSA | ECDSA (NIST P-256/384/521) | 高 | 谨慎使用（后门疑虑）|
| Ed25519 | EdDSA (Curve25519) | 高 | **首选** |
| DSA | DSA | **不安全** | 禁用 |

```
SSH 安全配置:
  HostKeyAlgorithms: ssh-ed25519, rsa-sha2-512
  KexAlgorithms: curve25519-sha256, diffie-hellman-group16-sha512
  Ciphers: chacha20-poly1305@openssh.com, aes256-gcm@openssh.com
  MACs: hmac-sha2-512-etm@openssh.com

Host Key Verification:
  ssh-keygen -lf /etc/ssh/ssh_host_ed25519_key.pub
  → 验证指纹 (首次连接时对比)
```

---

## 五、PGP/GPG

GPG (GNU Privacy Guard) 是 OpenPGP 标准的开源实现，用于邮件加密和文件签名。

```
GPG 工作流:
  密钥生成:
    gpg --full-generate-key
    → 选择 RSA 4096 / Ed25519

  加密/解密:
    gpg --encrypt --recipient alice@example.com file.txt
    gpg --decrypt file.txt.gpg

  签名/验证:
    gpg --sign file.txt           → 生成二进制签名
    gpg --clearsign file.txt      → 生成明文签名
    gpg --verify file.txt.asc

  密钥服务器:
    gpg --keyserver keys.openpgp.org --send-key KEYID
    gpg --keyserver keys.openpgp.org --recv-key KEYID
```

Web of Trust: PGP 的去中心化信任模型，通过密钥签名聚会（Key Signing Party）构建信任网络。每个用户自主决定信任哪些人的签名，与 CA 的层次化模型不同。

---

## 六、哈希函数

| 算法 | 输出长度 | 碰撞抗性 | 长度扩展攻击 | 推荐用途 |
|------|----------|----------|-------------|----------|
| MD5 | 128 bit | ❌ 已破解 | ❌ 易受攻击 | 已弃用 |
| SHA-1 | 160 bit | ❌ SHAttered (2017) | ❌ | 已弃用 |
| SHA-256 | 256 bit | ✅ 安全 | ❌ 可扩展 | 数字签名、区块链 |
| SHA-512 | 512 bit | ✅ 安全 | ❌ 可扩展 | 高安全性需求 |
| SHA-3 | 任意 | ✅ 安全 | ✅ 抗扩展 | 新一代标准 |
| BLAKE2 | 任意 | ✅ 安全 | ✅ | 高性能场景 |
| HMAC | 可变 | ✅ 安全 | N/A | 消息认证码 |

```python
# HMAC 示例
import hmac
import hashlib

mac = hmac.new(key, message, hashlib.sha256).digest()
```

长度扩展攻击: MD5/SHA-1/SHA-2 均易受长度扩展攻击，即已知 $H(M)$ 可在不知道 $M$ 的情况下计算 $H(M \parallel \text{padding} \parallel \text{extra})$。SHA-3 通过海绵结构免疫此攻击。

---

## 七、密码分析入门

| 攻击类型 | 原理 | 适用场景 |
|----------|------|----------|
| 暴力破解 | 遍历所有密钥 | 密钥空间不足（DES 56-bit） |
| 彩虹表 | 预计算哈希链的时空权衡 | 未加盐的哈希密码 |
| 侧信道攻击 | 利用时间、功耗、电磁泄漏 | 智能卡、TEE |
| 线性/差分分析 | 统计分析方法 | 分组密码（对 AES 无效） |
| 量子攻击 | Grover 算法平方加速 | 需量子计算机（威胁对称加密）|

```
密码哈希加盐:
  未加盐: hash("password123") = 固定值 → 彩虹表直接命中
  加盐:   hash("password123" + random_salt) = 唯一值 → 不可预计算

  盐的要求: 密码学随机、每个密码不同、长度 ≥ 16 字节
```

---

## 八、后量子密码学

量子计算机对现有密码体系的威胁：
- Shor 算法可高效分解大整数 → RSA/ECC 不安全
- Grover 算法平方搜索 → AES 密钥长度需加倍

| 类型 | 算法 | 安全基础 | NIST 状态 |
|------|------|----------|-----------|
| 格密码 (Lattice) | **Kyber** (KEM), Dilithium (签名) | 带错误学习 (LWE) 问题 | **已选定** |
| 哈希签名 (Hash-based) | **SPHINCS+** | 哈希函数安全性 | **已选定** |
| 编码密码 (Code-based) | Classic McEliece | 二进制 Goppa 码解码 | 第 4 轮候选 |
| 多变量密码 (Multivariate) | Rainbow | 多变量二次方程组 | 已淘汰（被破解）|

```
NIST 已选定的后量子算法 (2024):
  ML-KEM (Kyber):     密钥封装机制
  ML-DSA (Dilithium): 数字签名
  SLH-DSA (SPHINCS+): 无状态哈希签名

密钥大小对比:
                  RSA-3072     Kyber-768     SPHINCS+-128s
  公钥:            550 B        1.18 KB       32 B
  私钥:            1.2 KB       2.4 KB         64 B
  密文/签名:       550 B        1.1 KB        7.8 KB
```

---

## 参考资源

- 《Applied Cryptography》— Bruce Schneier
- 《Serious Cryptography》— Jean-Philippe Aumasson
- NIST SP 800-175B: Guideline for Using Cryptographic Standards
- Cryptography Engineering — Ferguson, Schneier, Kohno
- IETF TLS 1.3 RFC 8446
- NIST Post-Quantum Cryptography Standardization
- Latacora Cryptographic Right Answers: https://latacora.micro.blog/2018/04/03/cryptographic-right-answers.html
