---
aliases: [WebDevelopment]
tags: ['EngineeringDevelopment', 'WebDevelopment', 'WebDevelopment']
created: 2026-05-16
updated: 2026-05-16
---

# Web 开发完全指南

## 概述

Web 开发涵盖构建网站和 Web 应用的全部技术栈，从前端用户界面到后端服务器、数据库和部署运维。随着 Web 技术的发展，现代 Web 应用已具备媲美原生应用的体验和功能。

---

## 一、Web 架构基础

### 1.1 客户端-服务器模型

```
客户端 (浏览器)                   服务器
┌─────────────┐                ┌─────────────┐
│  浏览器     │  ──HTTP 请求──▶  │  Web Server  │
│  (HTML/CSS  │                │  (Nginx/Apache)|
│   /JS)      │  ◀──HTTP 响应──  │      │        │
└─────────────┘                └──────┼────────┘
                                     │
                              ┌──────▼────────┐
                              │  应用服务器    │
                              │  (业务逻辑)    │
                              └──────┼────────┘
                                     │
                              ┌──────▼────────┐
                              │    数据库      │
                              │  (持久化)      │
                              └───────────────┘
```

### 1.2 HTTP 协议

```
HTTP/1.1 vs HTTP/2 vs HTTP/3:
  特性          | HTTP/1.1    | HTTP/2        | HTTP/3
  连接模型      | 串行 (每个请求一个 TCP) | 多路复用 (单一 TCP)| 多路复用 (QUIC/UDP)
  头部压缩      | 无          | HPACK        | QPACK
  服务器推送    | 无          | 支持          | 支持
  队头阻塞      | 有          | TCP 级别      | 无
  加密          | 可选        | 通常强制 HTTPS | 强制

请求方法:
  GET    — 获取资源 (幂等)
  POST   — 创建资源
  PUT    — 完全替换资源 (幂等)
  PATCH  — 部分更新资源
  DELETE — 删除资源 (幂等)
```

### 1.3 延迟与吞吐量模型

**网络延迟组成**：

$$ L = L_{\text{propagation}} + L_{\text{transmission}} + L_{\text{queuing}} + L_{\text{processing}} $$

- 传播延迟 $L_{\text{propagation}} = d / v$（距离 / 光速）
- 传输延迟 $L_{\text{transmission}} = s / B$（数据大小 / 带宽）
- **吞吐量** $\text{Throughput} = 1 / L$（每秒请求数）

**缓存命中率**：

$$ \text{有效延迟} = h \cdot L_{\text{cache}} + (1 - h) \cdot L_{\text{origin}} $$

其中 $h$ 为缓存命中率，$L_{\text{cache}}$ 为缓存访问延迟，$L_{\text{origin}}$ 为源站延迟。

### 1.4 RESTful API 设计

```
设计原则:
  - 资源导向: /users, /articles, /comments
  - HTTP 方法表示操作
  - 无状态 (Stateless): 每个请求包含所有必要信息
  - 统一接口

示例:
  GET    /api/users          → 获取用户列表
  GET    /api/users/1        → 获取用户 1
  POST   /api/users          → 创建用户
  PUT    /api/users/1        → 更新用户 1 (全部)
  PATCH  /api/users/1        → 部分更新用户 1
  DELETE /api/users/1        → 删除用户 1
  GET    /api/users/1/articles → 用户 1 的文章列表
```

---

## 二、前端开发

### 2.1 HTML5

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Web 应用</title>
    <link rel="stylesheet" href="styles.css">
</head>
<body>
    <header>
        <nav>
            <ul>
                <li><a href="/">首页</a></li>
                <li><a href="/about">关于</a></li>
            </ul>
        </nav>
    </header>
    <main>
        <article>
            <section>
                <h1>文章标题</h1>
                <p>正文内容</p>
            </section>
        </article>
        <aside>侧边栏</aside>
    </main>
    <footer>&copy; 2024</footer>
</body>
</html>
```

### 2.2 CSS3

```css
/* Flexbox */
.container {
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 16px;
    flex-wrap: wrap;
}

/* Grid */
.grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 24px;
}

/* 响应式设计 */
@media (max-width: 768px) {
    .container {
        flex-direction: column;
    }
    .grid {
        grid-template-columns: 1fr;
    }
}

/* CSS 变量 */
:root {
    --primary: #0070f3;
    --secondary: #0070f3;
    --spacing: 8px;
}
```

### 2.3 JavaScript (ES6+)

```javascript
// 箭头函数、模板字符串、解构赋值
const createUser = ({ name, email, age }) => {
    return {
        id: crypto.randomUUID(),
        name,
        email: email.toLowerCase(),
        isAdult: age >= 18
    };
};

// async/await
async function fetchUsers() {
    try {
        const response = await fetch('/api/users');
        if (!response.ok) throw new Error('Network error');
        return await response.json();
    } catch (error) {
        console.error('Failed to fetch users:', error);
        return [];
    }
}

// DOM 操作
document.querySelector('#submit-btn').addEventListener('click', async (e) => {
    e.preventDefault();
    // 处理表单
});
```

### 2.4 前端框架对比

| 特性 | React | Vue | Angular |
|------|-------|-----|---------|
| 开发者 | Meta | 尤雨溪 | Google |
| 语言 | JSX + JavaScript/TypeScript | Template + JS/TS | TypeScript |
| 数据绑定 | 单向 (one-way) | 双向 (two-way) | 双向 |
| 状态管理 | Redux, Zustand, Context | Pinia, Vuex | NgRx, Signals |
| 学习曲线 | 中等 | 低 | 高 |
| 适用规模 | 中到大 | 小到中 | 大到企业级 |
| 包体积 | 较小 | 最小 | 较大 |
| 路由 | React Router | Vue Router | Angular Router |

---

## 三、后端开发

| 语言/框架 | 特点 | 速度 | 适用场景 | 公司 |
|-----------|------|------|----------|------|
| Node.js + Express | 事件驱动、NPM 生态 | 高 (I/O) | API 服务、实时应用 | Netflix, PayPal |
| Python + Django | 全栈、"电池齐全" | 中 | 快速开发、CMS | Instagram, Pinterest |
| Python + FastAPI | 异步、自动文档 | 高 | 高性能 API | Uber |
| Java + Spring Boot | 企业级、强类型 | 高 | 大型系统、微服务 | 阿里, 银行 |
| Go + Gin | 高性能、协程 | 极高 | 微服务、中间件 | Docker, Kubernetes |
| C# + ASP.NET Core | 跨平台、强类型 | 高 | 企业应用、游戏服务器 | Microsoft |

### 3.1 Express 示例

```javascript
const express = require('express');
const app = express();

app.use(express.json());

// 中间件
app.use((req, res, next) => {
    console.log(`${req.method} ${req.url}`);
    next();
});

// 路由
app.get('/api/users', async (req, res) => {
    try {
        const users = await db.query('SELECT * FROM users');
        res.json(users);
    } catch (err) {
        res.status(500).json({ error: err.message });
    }
});

app.listen(3000, () => console.log('Server running on port 3000'));
```

---

## 四、数据库集成 (ORM)

| ORM | 语言 | 数据库 | 特点 |
|-----|------|--------|------|
| Prisma | TypeScript | PostgreSQL, MySQL, SQLite | 类型安全、自动迁移 |
| Sequelize | JavaScript | 多种 SQL | 成熟稳定 |
| TypeORM | TypeScript | 多种 SQL | Active Record + Data Mapper |
| Hibernate | Java | 多种 SQL | JPA 标准 |
| SQLAlchemy | Python | 多种 SQL | ORM + Core 双层 |
| Entity Framework | C# | 多种 SQL | LINQ 集成 |

```javascript
// Prisma 示例
const user = await prisma.user.create({
    data: {
        name: 'Alice',
        email: 'alice@example.com',
        posts: {
            create: { title: 'Hello World' }
        }
    },
    include: { posts: true }
});
```

---

## 五、认证

| 方案 | 原理 | 适用场景 |
|------|------|----------|
| Session-based | 服务器存储 session，返回 cookie | 传统 Web 应用 |
| JWT (JSON Web Token) | 自包含 token，无状态 | REST API, SPA |
| OAuth 2.0 | 授权委托 (第三方登录) | 社交登录 (Google, GitHub) |
| SSO (单点登录) | 一次登录，多处可用 | 企业应用生态 |

```
JWT 结构:
  header.payload.signature
  
  header:    {"alg": "HS256", "typ": "JWT"}
  payload:   {"sub": "123", "name": "Alice", "iat": 1516239022}
  signature: HMACSHA256(base64(header) + "." + base64(payload), secret)
```

---

## 六、Web 安全

| 机制 | 作用 | 实现 |
|------|------|------|
| HTTPS (TLS) | 传输加密 | Let's Encrypt 免费证书 |
| CORS | 跨域访问控制 | `Access-Control-Allow-Origin` |
| CSP | 内容安全策略 | `Content-Security-Policy` 头 |
| XSS 防护 | 脚本注入防护 | 输出转义、CSP |
| CSRF 防护 | 跨站请求伪造防护 | CSRF Token, SameSite Cookie |
| SQL 注入防护 | 数据库注入防护 | 参数化查询、ORM |

---

## 七、部署

| 平台 | 类型 | 适合 | 特点 |
|------|------|------|------|
| Vercel | 前端托管 | Next.js, SPA | 自动部署、Edge Functions |
| Netlify | 前端托管 | 静态站点、Jamstack | 表单、Lambda 函数 |
| Railway | 全栈托管 | 全栈应用 | 数据库集成、自动部署 |
| AWS | 云平台 | 企业级 | 全面但复杂 |
| Docker | 容器化 | 任何应用 | 环境一致性、可移植 |

```yaml
# Nginx 配置
server {
    listen 80;
    server_name example.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl;
    server_name example.com;

    location / {
        proxy_pass http://localhost:3000;
        proxy_set_header Host $host;
    }

    location /static/ {
        alias /var/www/static/;
        expires 365d;
    }
}
```

---

## 八、测试

| 层级 | 范围 | 工具 | 速度 |
|------|------|------|------|
| 单元测试 | 单个函数/组件 | Vitest, Jest, JUnit | 极快 |
| 集成测试 | 模块间交互 | Supertest, Testing Library | 快 |
| E2E 测试 | 完整用户流程 | Playwright, Cypress | 慢 |
| 快照测试 | UI 输出对比 | Storybook, Jest Snapshot | 快 |
| 性能测试 | 负载/压力 | k6, Lighthouse | 慢 |

---

## 相关条目

- Frontend
- Backend
- [[05_ComputerScience/EngineeringDevelopment/MobileDevelopment/MobileDevelopment|MobileDevelopment]]
- Database
- DevOps

## 参考资源

- MDN Web 文档: https://developer.mozilla.org
- React 官方文档: https://react.dev
- Vue 官方文档: https://vuejs.org
- Node.js 文档: https://nodejs.org/docs
- 《Web 全栈工程师的自我修养》— 余果
- 《HTTP 权威指南》— Gourley 等
- web.dev: https://web.dev


