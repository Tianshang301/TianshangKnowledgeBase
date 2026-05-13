# 应用层详解 (Application Layer)

## 1. DNS (Domain Name System)

域名系统将人类可读的域名转换为IP地址。

### 域名层次结构

```
根 (.)
├── .com         → 商业组织 (Verisign运营)
├── .org         → 非营利组织 (PIR运营)
├── .cn          → 中国 (CNNIC运营)
├── .net         → 网络服务
├── .edu         → 教育机构
└── 顶级域(TLD) 
    └── 二级域 (google.com, baidu.com)
        └── 子域 (www, mail, api)
```

### DNS 解析过程

```
用户浏览器                       本地DNS解析器                根DNS服务器
    │                               │                          │
    │ 1. 查询 www.example.com       │                          │
    │──────────────────────────────►│                          │
    │                               │ 2. 询问 .com的权威服务器 │
    │                               │─────────────────────────►│
    │                               │◄─────────────────────────│
    │                               │    返回 .com TLD服务器   │
    │                               │                          │
    │                               │ 3. 询问 example.com      │
    │                               │─────────────────────────►│ .com TLD
    │                               │◄─────────────────────────│
    │                               │    返回 example.com NS   │
    │                               │                          │
    │                               │ 4. 询问 www.example.com  │
    │                               │─────────────────────────►│ example.com
    │                               │◄─────────────────────────│ 权威服务器
    │                               │    返回 93.184.216.34    │
    │◄──────────────────────────────│                          │
    │ 5. 返回 93.184.216.34        │                          │
```

### DNS 记录类型

| 记录类型 | 用途 | 示例 |
|---------|------|------|
| **A** | IPv4地址 | example.com A 93.184.216.34 |
| **AAAA** | IPv6地址 | example.com AAAA 2606:2800:220:1:248:1893:25c8:1946 |
| **CNAME** | 别名 | www.example.com CNAME example.com |
| **MX** | 邮件服务器 | example.com MX 10 mail.example.com |
| **NS** | 名称服务器 | example.com NS ns1.example.com |
| **TXT** | 文本信息 | example.com TXT "v=spf1 include:_spf.google.com" |
| **SOA** | 区域权威信息 | (起始授权记录) |
| **SRV** | 服务位置 | _sip._tcp.example.com SRV 10 5 5060 sip.example.com |

### 查询工具

```bash
# dig (最详细)
dig www.baidu.com
dig -t AAAA www.google.com
dig -t MX gmail.com
dig +trace www.example.com    # 跟踪完整解析路径

# nslookup (较简单)
nslookup www.baidu.com
nslookup -type=MX gmail.com

# whois (查询域名注册信息)
whois example.com

# host (简洁)
host www.baidu.com
host -t MX gmail.com

# 使用特定DNS服务器
dig @8.8.8.8 www.baidu.com
nslookup www.baidu.com 8.8.8.8
```

## 2. HTTP/HTTPS

### HTTP 方法

| 方法 | 描述 | 幂等 | 安全 | 是否有请求体 |
|------|------|------|------|-------------|
| GET | 获取资源 | ✓ | ✓ | ✗ |
| HEAD | 获取响应头 | ✓ | ✓ | ✗ |
| POST | 提交/创建资源 | ✗ | ✗ | ✓ |
| PUT | 更新/替换资源 | ✓ | ✗ | ✓ |
| PATCH | 部分更新资源 | ✗ | ✗ | ✓ |
| DELETE | 删除资源 | ✓ | ✗ | 可能有 |
| OPTIONS | 查询支持的方法 | ✓ | ✓ | ✗ |
| TRACE | 回显请求(调试) | ✓ | ✓ | ✗ |

### HTTP 状态码

| 分类 | 范围 | 含义 | 常见状态码 |
|------|------|------|-----------|
| 信息 | 1xx | 请求已接收，继续处理 | 100 Continue, 101 Switching Protocols |
| 成功 | 2xx | 请求成功 | 200 OK, 201 Created, 204 No Content |
| 重定向 | 3xx | 需进一步操作 | 301 Moved Permanently, 302 Found, 304 Not Modified |
| 客户端错误 | 4xx | 客户端错误 | 400 Bad Request, 401 Unauthorized, 403 Forbidden, 404 Not Found, 429 Too Many Requests |
| 服务器错误 | 5xx | 服务器错误 | 500 Internal Server Error, 502 Bad Gateway, 503 Service Unavailable, 504 Gateway Timeout |

### HTTP 请求头

```http
GET /index.html HTTP/1.1
Host: www.example.com                           # 必需(HTTP/1.1)
User-Agent: Mozilla/5.0 (Windows NT 10.0)       # 客户端标识
Accept: text/html,application/json              # 可接受的响应类型
Accept-Language: zh-CN,en-US;q=0.9              # 语言偏好
Accept-Encoding: gzip, deflate, br              # 支持的压缩方式
Connection: keep-alive                          # 连接管理
Cookie: session_id=abc123                       # Cookie
Authorization: Bearer eyJhbGciOiJIUzI1NiIs...   # 认证
Cache-Control: no-cache                         # 缓存控制
If-Modified-Since: Mon, 15 Jan 2024 10:00:00 GMT # 条件请求
Referer: https://www.google.com/                # 来源页面
```

### HTTP 响应头

```http
HTTP/1.1 200 OK
Date: Sat, 09 May 2026 10:00:00 GMT
Server: nginx/1.24.0
Content-Type: text/html; charset=UTF-8
Content-Length: 1234
Content-Encoding: gzip
Last-Modified: Fri, 08 May 2026 12:00:00 GMT
ETag: "abc123def456"                            # 实体标签
Cache-Control: max-age=3600, public             # 缓存控制
Set-Cookie: session_id=xyz789; HttpOnly; Secure # 设置Cookie
Strict-Transport-Security: max-age=31536000     # HSTS
X-Frame-Options: DENY                           # 防点击劫持
X-Content-Type-Options: nosniff                 # 防MIME嗅探
```

### 缓存控制

```
# 强缓存 (不发送请求)
Cache-Control: max-age=3600          # 缓存3600秒
Expires: Sat, 09 May 2026 11:00:00   # HTTP/1.0兼容

# 协商缓存 (发送条件请求)
# 方式1: Last-Modified / If-Modified-Since
# 方式2: ETag / If-None-Match

请求:
GET /data.json
If-None-Match: "abc123"

响应(304 Not Modified):
HTTP/1.1 304 Not Modified
ETag: "abc123"
(无响应体)
```

### HTTP/2 特性

| 特性 | 描述 | 优势 |
|------|------|------|
| **二进制分帧** | 帧(frame)替代文本 | 解析更高效 |
| **多路复用** | 一个TCP连接并行多个流 | 解决队头阻塞 |
| **服务器推送** | 服务器主动推送资源 | 减少RTT |
| **头部压缩(HPACK)** | 使用静态/动态字典压缩头 | 减少开销 |
| **流优先级** | 设置资源加载优先级 | 优化页面加载 |
| **连接重置** | RST_STREAM只重置单个流 | 不中断其他流 |

### HTTP/3 & QUIC

```
HTTP/3
    │
QUIC (基于UDP)
    │
TLS 1.3 (内置加密)
    │
UDP
```

**QUIC 优势:**
- 0-RTT 连接建立 (之前连过的可直接发数据)
- 连接迁移 (切换网络不中断)
- 无TCP队头阻塞 (一个流丢包不影响其他流)
- 内置TLS 1.3

## 3. FTP (File Transfer Protocol)

### 主动模式 vs 被动模式

```
主动模式 (Active):
客户端(端口N) ──控制连接(21)──► 服务器
客户端(端口N+1)◄──数据连接(20)── 服务器
  (服务器主动连接客户端)

被动模式 (Passive):
客户端(端口N) ──控制连接(21)──► 服务器
客户端(端口N+1)──数据连接(>=1024)──► 服务器
  (客户端主动连接服务器, PASV命令)
```

```bash
# FTP命令示例
ftp ftp.example.com
> anonymous          # 匿名登录
> password@example.com
> ls                 # 列出文件
> binary             # 切换到二进制模式
> get file.zip       # 下载文件
> put local.txt      # 上传文件
> passive            # 切换被动模式
> quit

# 命令行直接下载
curl ftp://ftp.example.com/file.zip --user user:pass
wget ftp://ftp.example.com/file.zip
```

## 4. 电子邮件协议

### SMTP (Simple Mail Transfer Protocol)

```smtp
# SMTP 会话示例 (发送邮件)
S: 220 smtp.example.com ESMTP Postfix
C: HELO client.example.com
S: 250 Hello client.example.com
C: MAIL FROM:<alice@example.com>
S: 250 OK
C: RCPT TO:<bob@example.org>
S: 250 OK
C: DATA
S: 354 End data with <CRLF>.<CRLF>
C: From: alice@example.com
C: To: bob@example.org
C: Subject: Hello
C:
C: This is the email body.
C: .
S: 250 OK: message accepted
C: QUIT
S: 221 Bye
```

### POP3 (Post Office Protocol v3)

```pop3
# POP3 会话示例 (接收邮件)
C: USER alice
S: +OK
C: PASS secret
S: +OK mailbox has 3 messages
C: LIST
S: 1 1200
S: 2 3400
S: 3 890
S: .
C: RETR 1           # 读取第一封邮件
S: (邮件内容...)
S: .
C: DELE 1           # 删除邮件
S: +OK
C: QUIT
```

### IMAP (Internet Message Access Protocol)

```imap
# IMAP 会话示例
C: LOGIN alice secret
S: OK Logged in
C: LIST "" "*"
S: * LIST (\HasNoChildren) "/" INBOX
S: * LIST (\HasNoChildren) "/" Sent
C: SELECT INBOX
S: * 3 EXISTS
S: * OK
C: FETCH 1 BODY[]     # 获取第一封邮件
S: (邮件内容...)
C: STORE 1 +FLAGS (\Seen)   # 标记为已读
S: * 1 FETCH (FLAGS (\Seen))
C: LOGOUT
```

| 协议 | 默认端口 | 特点 |
|------|---------|------|
| SMTP | 25(明文), 587(提交), 465(SMTPS) | 发送邮件 |
| POP3 | 110(明文), 995(POP3S) | 下载后本地管理 |
| IMAP | 143(明文), 993(IMAPS) | 服务器端管理 |

## 5. DHCP (Dynamic Host Configuration Protocol)

### DORA 过程

```
DHCP Client                    DHCP Server
    │                              │
    │ 1. DHCP DISCOVER (广播)      │
    │ 源:0.0.0.0:68 → 255.255.255.255:67  │
    │─────────────────────────────►│
    │                              │
    │ 2. DHCP OFFER (可选单播或广播)│
    │ 提供IP: 192.168.1.100       │
    │◄─────────────────────────────│
    │                              │
    │ 3. DHCP REQUEST (广播)       │
    │ "我接受 192.168.1.100"       │
    │─────────────────────────────►│
    │                              │
    │ 4. DHCP ACK                  │
    │ "确认, 租期3600秒"           │
    │◄─────────────────────────────│
```

```bash
# Linux DHCP客户端
dhclient eth0                # 获取IP
dhclient -r eth0             # 释放IP
dhclient -v eth0             # 显示详细信息

# Windows
ipconfig /renew              # 续租IP
ipconfig /release            # 释放IP
ipconfig /all                # 查看DHCP信息
```

## 6. SSH (Secure Shell)

### SSH 连接过程

```
客户端                        服务器
  │                              │
  │ 1. TCP握手(端口22)           │
  │─────────────────────────────►│
  │◄─────────────────────────────│
  │                              │
  │ 2. 版本协商                  │
  │ SSH-2.0-OpenSSH_9.3         │
  │                              │
  │ 3. 密钥交换 (Diffie-Hellman) │
  │ 生成共享密钥                 │
  │                              │
  │ 4. 服务器认证                │
  │    服务器发送主机密钥        │
  │◄─────────────────────────────│
  │ 信任? (/etc/ssh/ssh_known_hosts)│
  │                              │
  │ 5. 用户认证                  │
  │    密码 / 公钥 / GSSAPI      │
  │─────────────────────────────►│
  │◄─────────────────────────────│
  │                              │
  │ 6. 建立加密通道              │
  │    开始交互                  │
```

### SSH 常用命令

```bash
# 基本连接
ssh user@example.com
ssh -p 2222 user@example.com    # 指定端口

# 公钥认证
ssh-keygen -t ed25519 -C "my@email.com"        # 生成密钥对
ssh-copy-id user@example.com                   # 复制公钥到服务器

# SSH配置文件 (~/.ssh/config)
# Host myserver
#     HostName example.com
#     User admin
#     Port 2222
#     IdentityFile ~/.ssh/id_ed25519
ssh myserver   # 使用配置别名

# 端口转发
# 本地转发: 将本地8080转发到远程的internal:80
ssh -L 8080:internal:80 user@gateway

# 远程转发: 将远程8080转发到本地的localhost:80
ssh -R 8080:localhost:80 user@gateway

# 动态转发 (SOCKS代理)
ssh -D 1080 user@gateway

# 隧道
ssh -J jumpuser@jump_host target_user@target_host
```

### SCP / SFTP

```bash
# SCP (基于SSH的文件复制)
scp file.txt user@example.com:/remote/path/
scp -r dir/ user@example.com:/remote/path/
scp user@example.com:/remote/file.txt ./local/

# SFTP (基于SSH的文件传输, 类似FTP)
sftp user@example.com
> ls
> get remote_file.txt
> put local_file.txt
> bye
\`\`\`

## 相关条目

- [[TransportLayer]]
- [[DNS]]
- [[HTTP]]
- [[NetworkModels]]
- [[NetworkLayer]]
