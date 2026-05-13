# HTTP 协议深度指南 (HTTP Protocol Deep Guide)

## 1. HTTP 版本演进

| 版本 | 年份 | 核心改进 |
|------|------|---------|
| **HTTP/0.9** | 1991 | 仅支持GET, 纯文本HTML |
| **HTTP/1.0** | 1996 | 支持HEAD/POST, 状态码, 头部, Content-Type |
| **HTTP/1.1** | 1997 | 持久连接, 管道化, 分块传输, 缓存控制, Host头 |
| **HTTP/2** | 2015 | 二进制分帧, 多路复用, 服务器推送, 头部压缩(HPACK) |
| **HTTP/3** | 2022 | 基于QUIC(UDP), 0-RTT, 无队头阻塞 |

## 2. HTTP/1.1 核心特性

### 2.1 持久连接 (Persistent Connection)

```http
# HTTP/1.0: 每次请求都新建TCP连接
GET /page1 HTTP/1.0
Connection: keep-alive  # 扩展头, 非标准

# HTTP/1.1: 默认持久连接
GET /page1 HTTP/1.1
Host: example.com
# 连接默认保持, 可发送多个请求
```

```bash
# 查看连接头部
curl -v http://example.com 2>&1 | grep -i "Connection"
```

### 2.2 管道化 (Pipelining)

```
无管道:    请求1→响应1→请求2→响应2→请求3→响应3
有管道:    请求1→请求2→请求3→响应1→响应2→响应3

# 注意: 仍存在队头阻塞(HOL blocking)
# 实践中很少启用(代理/NAT兼容性问题)
```

### 2.3 分块传输编码 (Chunked Transfer)

用于未知内容长度的动态响应。

```http
HTTP/1.1 200 OK
Content-Type: text/html
Transfer-Encoding: chunked

25                                      # 块大小(十六进制)
<html><body><h1>Hello World</h1>       # 块数据
7                                       # 下一块大小
</body>
0                                       # 结束块
                                        # 尾部(可选)
```

### 2.4 缓存控制头

```http
# 强制缓存
Cache-Control: max-age=3600              # 缓存1小时
Cache-Control: no-store                   # 不缓存
Cache-Control: public                     # 可被任何缓存缓存
Cache-Control: private                    # 仅浏览器可缓存

# 协商缓存
Last-Modified: Mon, 15 Jan 2024 10:00:00 GMT
ETag: "abc123"

# 请求时:
If-Modified-Since: Mon, 15 Jan 2024 10:00:00 GMT
If-None-Match: "abc123"
# 响应: 304 Not Modified (无响应体) 或 200 OK (新内容)
```

## 3. HTTP/2 核心特性

### 3.1 二进制分帧 (Binary Framing)

```
HTTP/1.x: 文本协议, 以换行符分隔
HTTP/2:   二进制协议, 以帧(frame)为单位

帧类型:
├── DATA         # 数据帧
├── HEADERS      # 头帧
├── PRIORITY     # 优先级帧
├── RST_STREAM   # 流重置帧
├── SETTINGS     # 设置帧
├── PUSH_PROMISE # 推送承诺帧
├── PING         # 心跳帧
├── GOAWAY       # 关闭帧
└── WINDOW_UPDATE # 流量控制帧
```

### 3.2 多路复用 (Multiplexing)

```
HTTP/1.1 (一个连接一个请求):
┌─────────────────────┐
│ GET /style.css      │
│ GET /script.js      │  (排队等待)
│ GET /image.png      │
│ GET /api/data       │
└─────────────────────┘

HTTP/2 (一个连接多个流):
┌─────────────────────┐
│ Stream 1: /style.css│
│ Stream 2: /script.js│ ← 可同时传输
│ Stream 3: /image.png│
│ Stream 4: /api/data │
└─────────────────────┘
```

### 3.3 服务器推送 (Server Push)

```
浏览器请求 index.html
    │
服务器: 知道index.html需要style.css和script.js
    │
    ├── 推送 style.css (浏览器无需请求)
    ├── 推送 script.js
    └── 响应 index.html

# 注意: Chrome 106+ 已移除对Server Push的支持
```

### 3.4 HPACK 头部压缩

```http
# 静态表 (预定义的常见头)
:method: GET       → 索引 2
:path: /index.html → 索引 5 (如果匹配)
:status: 200       → 索引 8
content-type: text/html; charset=utf-8 → 索引 31

# 动态表 (连接过程中新增的头)
# 使用Huffman编码进一步压缩

# 示例: 一个典型请求头从~800字节压缩到~100字节
```

### 3.5 流优先级 (Stream Prioritization)

```
依赖树:
        ┌─── root ───┐
        │            │
    index.html    style.css (权重=50)
        │
   ┌────┴────┐
   │         │
script.js  image.png
(权重=20)  (权重=5)
```

### 3.6 连接管理

```
# SETTINGS 帧 (连接开始时交换设置)
SETTINGS_MAX_CONCURRENT_STREAMS = 100
SETTINGS_INITIAL_WINDOW_SIZE = 65535
SETTINGS_MAX_FRAME_SIZE = 16384

# 流量控制: 基于WINDOW_UPDATE帧
# 流级别 + 连接级别
```

## 4. HTTP/3 & QUIC

### QUIC 协议栈

```
HTTP/3                   HTTP/2                HTTP/1.1
    │                       │                      │
  QUIC                   TLS 1.3                TLS 1.3
    │                    ┌──┴──┐               ┌──┴──┐
   UDP                    TCP                  TCP
```

### QUIC 核心特性

| 特性 | QUIC | TCP+TLS |
|------|------|---------|
| 连接建立 | 1-RTT (首次), 0-RTT (重复) | 3-RTT (TCP+TLS 1.3) |
| 连接迁移 | 支持(连接ID不变) | 不支持(IP变化需重连) |
| 队头阻塞 | 无(每流独立) | 有(TCP级) |
| 加密 | 内置(TLS 1.3) | 额外TLS层 |
| 丢包恢复 | 更快的丢包检测 | 依赖超时 |

### QUIC 连接建立 (0-RTT)

```
首次连接:
客户端 → 服务器:  Client Hello + 传输参数
服务器 → 客户端:  Server Hello + 证书 + 传输参数
客户端 → 服务器:  加密的HTTP请求! (1-RTT完成)

再次连接:
客户端 → 服务器:  加密的HTTP请求 + 之前缓存的参数 (0-RTT!)
服务器 → 客户端:  加密的HTTP响应
```

### 连接迁移

```python
# 传统TCP: 从WiFi切换到4G需要新建连接
# QUIC: 使用连接ID, 不受IP地址变化影响

QUIC连接:
  客户端(连接ID: A) ←→ 服务器(连接ID: B)
  WiFi: 客户端IP=192.168.1.2, 端口=12345
  4G:    客户端IP=10.0.0.5, 端口=54321
  → 连接ID不变, 无需重连!
```

## 5. HTTPS / TLS

### TLS 1.3 完整握手 (1-RTT)

```
客户端                                   服务器
   │                                        │
   │ ClientHello                           │
   │   TLS版本, 密码套件列表, KeyShare      │
   │───────────────────────────────────────►│
   │                                        │
   │ ServerHello                           │
   │   选择的密码套件, KeyShare, 证书        │
   │◄───────────────────────────────────────│
   │                                        │
   │ 证书验证                               │
   │   验证证书链                           │
   │   验证数字签名                         │
   │                                        │
   │ Finished (加密的握手完成消息)           │
   │───────────────────────────────────────►│
   │◄───────────────────────────────────────│
   │    Finished                            │
   │                                        │
   │ 开始加密应用数据传输                    │
```

### TLS 1.3 0-RTT

```
客户端 (之前连接过, 缓存了PSK):
   │
   │ ClientHello + PSK + 0-RTT数据
   │ (0-RTT数据: HTTP GET请求等)
   │───────────────────────────────────────►
   │
   │ ServerHello + Finished + 服务器响应
   │◄───────────────────────────────────────
```

### 密码套件 (Cipher Suites)

```
TLS 1.3 支持的密码套件 (只有5个):
TLS_AES_128_GCM_SHA256
TLS_AES_256_GCM_SHA384
TLS_CHACHA20_POLY1305_SHA256
TLS_AES_128_CCM_SHA256
TLS_AES_128_CCM_8_SHA256

TLS 1.2 (仍有大量):
TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256
TLS_ECDHE_ECDSA_WITH_AES_256_GCM_SHA384
...
```

### 证书链验证

```
浏览器信任的根CA
    ↓ 签发
中间CA证书           (如 Let's Encrypt R3)
    ↓ 签发
服务器证书           (如 *.example.com)

验证过程:
1. 服务器证书: 域名匹配
2. 中间CA签名: 用中间CA公钥验证服务器证书签名
3. 根CA签名: 用根CA公钥验证中间CA签名
4. 根CA: 在操作系统/browser的信任存储中
```

## 6. REST API 最佳实践

### URL设计

```
# 好的RESTful API:
GET    /api/v1/users              # 获取用户列表
GET    /api/v1/users/123          # 获取单个用户
POST   /api/v1/users              # 创建用户
PUT    /api/v1/users/123          # 更新整个用户
PATCH  /api/v1/users/123          # 部分更新
DELETE /api/v1/users/123          # 删除用户

# 资源关系:
GET    /api/v1/users/123/orders   # 用户的订单
GET    /api/v1/orders/456/items   # 订单的商品

# 过滤/排序/分页:
GET    /api/v1/users?role=admin&status=active
GET    /api/v1/users?sort=-created_at&page=2&per_page=20
GET    /api/v1/users?fields=id,name,email
```

### 状态码使用

```http
# 成功
200 OK                          # GET成功
201 Created                     # POST成功
204 No Content                  # DELETE成功

# 重定向
301 Moved Permanently           # 资源URL变更
302 Found                       # 临时重定向
304 Not Modified                # 缓存未过期

# 客户端错误
400 Bad Request                 # 请求格式错误
401 Unauthorized                # 未认证
403 Forbidden                   # 无权限
404 Not Found                   # 资源不存在
405 Method Not Allowed          # 不允许的方法
409 Conflict                    # 冲突(如重复创建)
422 Unprocessable Entity        # 验证失败
429 Too Many Requests           # 限流

# 服务器错误
500 Internal Server Error       # 服务器内部错误
502 Bad Gateway                 # 上游服务异常
503 Service Unavailable         # 服务暂不可用
504 Gateway Timeout             # 上游超时
```

### 请求/响应格式

```http
# 请求示例
POST /api/v1/users HTTP/1.1
Content-Type: application/json
Authorization: Bearer eyJhbGciOiJIUzI1NiIs...
Accept: application/json

{
    "name": "张三",
    "email": "zhangsan@example.com",
    "role": "admin"
}

# 响应示例
HTTP/1.1 201 Created
Content-Type: application/json
Location: /api/v1/users/123
X-Request-Id: req-abc-123-def

{
    "id": 123,
    "name": "张三",
    "email": "zhangsan@example.com",
    "role": "admin",
    "created_at": "2026-05-09T10:00:00Z",
    "_links": {
        "self": { "href": "/api/v1/users/123" },
        "orders": { "href": "/api/v1/users/123/orders" }
    }
}

# 错误响应
HTTP/1.1 422 Unprocessable Entity
{
    "error": {
        "code": "VALIDATION_ERROR",
        "message": "输入验证失败",
        "details": [
            { "field": "email", "message": "邮箱格式不正确" },
            { "field": "name", "message": "名称不能为空" }
        ]
    }
}
```

### 分页

```http
GET /api/v1/users?page=2&per_page=20

HTTP/1.1 200 OK
Link: <https://api.example.com/users?page=1>; rel="first",
      <https://api.example.com/users?page=1>; rel="prev",
      <https://api.example.com/users?page=3>; rel="next",
      <https://api.example.com/users?page=10>; rel="last"
X-Total-Count: 200
X-Total-Pages: 10
```

## 7. HTTP 调试工具

```bash
# curl (最常用)
curl -v https://api.example.com          # 详细输出(含请求/响应头)
curl -i https://api.example.com          # 包含响应头
curl -X POST -d '{"key":"value"}' -H 'Content-Type: application/json' URL
curl -o output.html https://example.com  # 保存到文件
curl -L https://example.com              # 跟随重定向
curl --cacert ca.pem https://example.com # 指定CA证书
curl --resolve example.com:443:127.0.0.1 https://example.com  # 指定IP

# HTTP/2 测试
curl --http2 -v https://nghttp2.org
curl -v https://www.google.com 2>&1 | grep "ALPN"  # 查看HTTP/2协商

# HTTPie (更友好的curl)
http GET https://api.example.com
http POST https://api.example.com/users name="张三" email="test@test.com"
http PUT https://api.example.com/users/123 name="李四"
http DELETE https://api.example.com/users/123

# wscat (WebSocket测试)
wscat -c wss://echo.websocket.org
\`\`\`

## 相关条目

- [[ApplicationLayer]]
- [[TransportLayer]]
- [[NetworkLayer]]
- [[DNS]]
- [[NetworkModels]]
