# DNS 深入指南 (DNS In-Depth Guide)

## 1. 域名层次结构 (Domain Hierarchy)

```
根域 (Root, ".")
├── 通用顶级域 (gTLD)
│   ├── .com    (商业, Verisign)
│   ├── .org    (非营利, PIR)
│   ├── .net    (网络服务, Verisign)
│   ├── .edu    (教育, Educause)
│   ├── .gov    (美国政府)
│   └── .info, .biz, .name, ...
│
├── 国家和地区顶级域 (ccTLD)
│   ├── .cn     (中国, CNNIC)
│   ├── .jp     (日本)
│   ├── .uk     (英国)
│   ├── .de     (德国)
│   ├── .io     (英属印度洋领地)
│   └── 250+ 其他
│
└── 新通用顶级域 (new gTLD)
    ├── .app, .dev, .blog
    ├── .shop, .online, .tech
    └── 1200+
```

```
完整域名: www.example.com.
          │       │       │  │
        主机    二级域  顶级域 根
                 (SLD)  (TLD)
```

## 2. DNS 服务器类型

| 服务器类型 | 职责 | 数量 |
|-----------|------|------|
| **根服务器 (Root)** | 指向TLD服务器 | 13套(>1000实例) |
| **TLD服务器** | 管理顶级域 | ~1500+ |
| **权威服务器 (Authoritative)** | 提供具体域名记录 | 无数 |
| **递归解析器 (Resolver)** | 替客户端递归查询 | ISP/公共DNS |

### 全球13台根服务器

```
A.ROOT-SERVERS.NET    (Verisign, 美国)
B.ROOT-SERVERS.NET    (ISC, 美国)
C.ROOT-SERVERS.NET    (Cogent, 美国)
D.ROOT-SERVERS.NET    (马里兰大学, 美国)
E.ROOT-SERVERS.NET    (NASA, 美国)
F.ROOT-SERVERS.NET    (ISC, 全球任播)
G.ROOT-SERVERS.NET    (美国国防部)
H.ROOT-SERVERS.NET    (美国陆军研究实验室)
I.ROOT-SERVERS.NET    (Netnod, 瑞典)
J.ROOT-SERVERS.NET    (Verisign, 全球任播)
K.ROOT-SERVERS.NET    (RIPE NCC, 全球任播)
L.ROOT-SERVERS.NET    (ICANN, 全球任播)
M.ROOT-SERVERS.NET    (WIDE Project, 日本)
```

### 公共DNS服务器

```bash
# 常用公共DNS
# 设置方法: /etc/resolv.conf 或 路由器配置

Google:       8.8.8.8 / 8.8.4.4
Cloudflare:   1.1.1.1 / 1.0.0.1
Quad9:        9.9.9.9 / 149.112.112.112
OpenDNS:      208.67.222.222 / 208.67.220.220
阿里DNS:      223.5.5.5 / 223.6.6.6
114DNS:       114.114.114.114 / 114.114.115.115
百度DNS:      180.76.76.76
```

## 3. DNS 解析过程

### 递归 vs 迭代查询

```
递归查询 (Recursive Query):
客户端 → 递归解析器
  "帮我查www.example.com, 不管多少步"

迭代查询 (Iterative Query):
递归解析器 → 根服务器
  "www.example.com? 我不知道, 去问.com TLD"

完整解析过程:
```

```
客户端 (浏览器)
    │  查询: www.example.com
    ▼
┌─────────────────────┐
│ 递归解析器           │
│ (如 8.8.8.8)        │
└─────┬───────────────┘
    │
    ├── 1. 询问根服务器: "www.example.com的IP?"
    │   ← "去问.com TLD服务器, 地址是a.gtld-servers.net"
    │
    ├── 2. 询问.com TLD: "www.example.com的IP?"
    │   ← "去问example.com的权威服务器, 地址是ns1.example.com"
    │
    ├── 3. 询问example.com权威: "www.example.com的IP?"
    │   ← "93.184.216.34"
    │
    └── 返回结果给客户端
```

```bash
# 查看完整解析路径
dig +trace www.example.com

# 使用特定解析器
dig @8.8.8.8 www.example.com
```

## 4. DNS 缓存

```
缓存层次:
┌─────────────┐
│ 浏览器缓存   │  → chrome://net-internals/#dns
├─────────────┤
│ OS缓存      │  → ipconfig /displaydns (Windows)
├─────────────┤       systemd-resolve --statistics (Linux)
│ 递归解析器   │  → 常用: 公共DNS(Google/Cloudflare)也有缓存
├─────────────┤
│ ISP缓存     │  → 上游DNS服务器
└─────────────┘

TTL (Time To Live):
- SOA记录中的最小值
- 典型值: A记录=300-3600s, NS=86400s
```

```bash
# 清除DNS缓存
# Linux
sudo systemd-resolve --flush-caches  # systemd-resolved
sudo /etc/init.d/nscd restart        # nscd
sudo service dnsmasq restart         # dnsmasq

# Windows
ipconfig /flushdns

# macOS
sudo dscacheutil -flushcache
sudo killall -HUP mDNSResponder
```

## 5. DNS 资源记录 (Resource Records)

### SOA (Start of Authority)

定义区域的权威信息。

```dns
example.com. 3600 IN SOA ns1.example.com. admin.example.com. (
    2026050901  ; Serial (YYYYMMDDNN)
    7200        ; Refresh (2小时)
    3600        ; Retry (1小时)
    1209600     ; Expire (2周)
    3600        ; Minimum TTL (1小时)
)
```

### A / AAAA 记录

```dns
# A记录 (IPv4)
example.com.     300 IN A    93.184.216.34
www.example.com. 300 IN A    93.184.216.34
api.example.com. 300 IN A    93.184.216.35

# AAAA记录 (IPv6)
example.com.     300 IN AAAA 2606:2800:220:1:248:1893:25c8:1946
```

### CNAME (别名)

```dns
# www是example.com的别名
www.example.com. 3600 IN CNAME example.com.

# 域名必须指向另一个域名, 不能和别的记录共存
# 根域名不能是CNAME
```

### MX (邮件交换)

```dns
# 优先级: 数值越小越优先
example.com. 3600 IN MX 10 mail.example.com.
example.com. 3600 IN MX 20 mail2.example.com.
```

### NS (名称服务器)

```dns
# 授权给哪些DNS服务器管理这个域
example.com. 86400 IN NS ns1.example.com.
example.com. 86400 IN NS ns2.example.com.
```

### TXT (文本记录)

```dns
# SPF (发件人策略框架)
example.com. 3600 IN TXT "v=spf1 ip4:192.0.2.0/24 include:_spf.google.com ~all"

# DKIM (域名密钥识别邮件)
default._domainkey.example.com. 3600 IN TXT "v=DKIM1; k=rsa; p=MIGfMA0GCSqGSIb4..."

# DMARC (域基消息认证报告)
_dmarc.example.com. 3600 IN TXT "v=DMARC1; p=reject; rua=mailto:dmarc@example.com"
```

### SRV (服务定位)

```dns
# _服务._协议.域名 优先级 权重 端口 目标
_sip._tcp.example.com. 3600 IN SRV 10 60 5060 sipserver.example.com.
_sip._tcp.example.com. 3600 IN SRV 20 40 5060 sipserver2.example.com.
```

## 6. DNSSEC (DNS Security Extensions)

对DNS响应进行数字签名，防止缓存投毒/中间人攻击。

```
DNSSEC 记录类型:
├── DNSKEY     → 公钥
├── RRSIG      → 资源记录签名
├── DS         → 委派签名器(父域对子域签名的哈希)
└── NSEC/NSEC3 → 不存在证明(防止域遍历)

验证链:
根 → .com → example.com → www.example.com
↓      ↓         ↓              ↓
根KSK   .com KSK  example KSK   A记录+RRSIG
```

```bash
# 验证DNSSEC
dig +dnssec www.example.com
dig +cdflag www.example.com      # 不验证(CD=Checking Disabled)
dig +adflag www.example.com      # 要求验证(AD=Authenticated Data)

# 查看DNSSEC信任链
delv +multiline www.example.com
```

## 7. DNS over HTTPS/TLS (DoH/DoT)

| 协议 | 端口 | 描述 | 优点 |
|------|------|------|------|
| **DoT** (DNS over TLS) | 853 | 标准DNS over TLS连接 | 简单 |
| **DoH** (DNS over HTTPS) | 443 | DNS over HTTP/2或1.1 | 防审查(混在HTTPS中) |

```bash
# DoH 示例 (使用 curl)
curl -H "accept: application/dns-json" "https://cloudflare-dns.com/dns-query?name=example.com&type=A"

# 配置系统DoH (Linux systemd-resolved)
sudo resolvectl dns eth0 1.1.1.1
sudo resolvectl dnsovertls eth0 yes
```

## 8. CDN 与 DNS (GeoDNS)

CDN利用DNS进行流量调度:

```
用户在中国 → 解析到中国CDN节点 (203.0.113.10)
用户在美国 → 解析到美国CDN节点 (198.51.100.20)

权威DNS服务器根据请求来源IP(EDNS Client Subnet):
┌───────────────────────────────┐
│  DNS服务器                    │
│  1. 收到www.example.com查询   │
│  2. 检查请求者IP (ECS)        │
│  3. 返回最近节点IP            │
│  4. 用户连接到最近节点         │
└───────────────────────────────┘
```

```bash
# 从不同位置查询(模拟)
dig @8.8.8.8 www.example.com
dig @1.1.1.1 www.example.com
dig @223.5.5.5 www.example.com
```

## 9. DNS 排错工具

```bash
# dig 详细用法
dig www.baidu.com                     # A记录查询
dig -t AAAA www.google.com            # AAAA记录
dig -t MX gmail.com                   # MX记录
dig -t NS example.com                 # NS记录
dig -t CNAME www.example.com           # CNAME记录
dig +short www.baidu.com              # 简洁输出
dig +trace www.example.com            # 跟踪解析路径
dig @8.8.8.8 www.example.com          # 指定DNS服务器
dig -x 8.8.8.8                       # 反向查询(PTR)
dig +dnssec www.example.com           # DNSSEC查询
dig +multiline example.com SOA        # 多行格式SOA

# nslookup
nslookup www.baidu.com
nslookup -type=MX example.com
nslookup example.com 8.8.8.8

# host
host www.baidu.com
host -t MX example.com
host -a example.com                  # 所有记录

# whois
whois example.com
whois 8.8.8.8

# 批量查询
for domain in example.com google.com baidu.com; do
    echo "=== $domain ==="
    dig +short $domain
done
\`\`\`

## 相关条目

- [[ApplicationLayer]]
- [[HTTP]]
- [[NetworkLayer]]
- [[TransportLayer]]
- [[NetworkModels]]
