# HTTP 协议与 API 设计

## 一、HTTP 方法

```http
GET     /users          # 获取资源列表 (幂等, 安全)
GET     /users/123      # 获取单个资源
POST    /users          # 创建新资源 (非幂等)
PUT     /users/123      # 完整替换资源 (幂等)
PATCH   /users/123      # 部分更新资源
DELETE  /users/123      # 删除资源
HEAD    /users          # 获取响应头 (无响应体)
OPTIONS /users          # 获取支持的HTTP方法
```

### 幂等性 (Idempotent)

```
GET, PUT, DELETE, HEAD, OPTIONS: 多次调用与一次调用效果相同 (幂等)
POST, PATCH: 多次调用可能产生不同结果 (非幂等)
```

## 二、状态码

### 2xx 成功

| 状态码 | 含义 | 使用场景 |
|--------|------|----------|
| 200 OK | 请求成功 | GET 请求返回数据 |
| 201 Created | 创建成功 | POST 创建资源后返回 |
| 202 Accepted | 请求已接受 | 异步任务 (后台处理) |
| 204 No Content | 无内容 | DELETE 成功, 或 GET 无数据 |
| 206 Partial Content | 部分内容 | 分页/断点续传 |

### 3xx 重定向

| 状态码 | 含义 | 使用场景 |
|--------|------|----------|
| 301 Moved Permanently | 永久重定向 | 域名变更 |
| 302 Found | 临时重定向 | 临时跳转 |
| 304 Not Modified | 未修改 | 缓存验证 |

### 4xx 客户端错误

| 状态码 | 含义 | 使用场景 |
|--------|------|----------|
| 400 Bad Request | 请求格式错误 | 参数校验失败 |
| 401 Unauthorized | 未认证 | 缺少/无效 token |
| 403 Forbidden | 无权限 | 已认证但权限不足 |
| 404 Not Found | 资源不存在 | URL 错误/资源已删除 |
| 405 Method Not Allowed | 方法不允许 | 使用错误的 HTTP 方法 |
| 409 Conflict | 资源冲突 | 创建重复资源 |
| 422 Unprocessable Entity | 语义错误 | 请求体验证失败 |
| 429 Too Many Requests | 请求过多 | 超过速率限制 |

### 5xx 服务器错误

| 状态码 | 含义 | 使用场景 |
|--------|------|----------|
| 500 Internal Server Error | 服务器内部错误 | 未预期的异常 |
| 502 Bad Gateway | 网关错误 | 上游服务不可用 |
| 503 Service Unavailable | 服务不可用 | 服务器过载/维护中 |
| 504 Gateway Timeout | 网关超时 | 上游服务响应超时 |

## 三、HTTP 头部

### 通用头部

```http
Cache-Control: no-cache, no-store, must-revalidate
Cache-Control: max-age=3600, public
Cache-Control: private, max-age=0
Connection: keep-alive
Date: Wed, 15 Mar 2024 10:00:00 GMT
```

### 请求头部

```http
# 认证
Authorization: Bearer eyJhbGciOiJIUzI1NiIs...
Authorization: Basic base64(username:password)
API-Key: abc123

# 内容协商
Accept: application/json
Accept: application/xml
Accept-Language: zh-CN,en-US;q=0.9
Accept-Encoding: gzip, deflate, br

# 条件请求
If-Modified-Since: Wed, 15 Mar 2024 10:00:00 GMT
If-None-Match: "etag-value"

# 缓存
Cache-Control: no-cache

# 跨域
Origin: https://example.com
Referer: https://example.com/page

# 其他
Content-Type: application/json
Content-Length: 123
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64)
```

### 响应头部

```http
# 缓存
Cache-Control: public, max-age=3600
ETag: "33a64df551425fcc55e4d42a148795d9f25f89d4"
Last-Modified: Wed, 15 Mar 2024 10:00:00 GMT
Expires: Wed, 15 Mar 2024 11:00:00 GMT

# CORS
Access-Control-Allow-Origin: https://example.com
Access-Control-Allow-Methods: GET, POST, PUT, DELETE, OPTIONS
Access-Control-Allow-Headers: Content-Type, Authorization
Access-Control-Allow-Credentials: true
Access-Control-Max-Age: 86400

# 安全
Strict-Transport-Security: max-age=31536000; includeSubDomains
X-Content-Type-Options: nosniff
X-Frame-Options: DENY
X-XSS-Protection: 1; mode=block
Content-Security-Policy: default-src 'self'
Referrer-Policy: strict-origin-when-cross-origin

# 速率限制
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 85
X-RateLimit-Reset: 1710511200
Retry-After: 3600

# 分页
Link: <https://api.example.com/users?page=2>; rel="next"
<https://api.example.com/users?page=5>; rel="last"
X-Total-Count: 500
X-Page: 1
X-Per-Page: 100
```

## 四、RESTful API 设计原则

### 资源命名

```http
# 好的命名
GET     /users                          # 用户列表
GET     /users/123                      # 单个用户
GET     /users/123/orders               # 用户的订单
GET     /users/123/orders/456           # 用户的某个订单
GET     /products                       # 产品列表
GET     /categories/electronics/products # 分类下的产品
GET     /search?q=keyword               # 搜索资源

# 错误命名 (避免)
GET     /getUsers                       # 动词在URL中
GET     /users/list                     # 不必要的路径
GET     /users/getUserById?id=123       # 查询参数表示资源
POST    /users/createUser               # 动词在URL中
GET     /users/123/delete               # 用DELETE方法代替
```

### API 版本管理

```http
# 方式1: URL 路径 (推荐)
GET /api/v1/users
GET /api/v2/users

# 方式2: 请求头
Accept: application/vnd.myapp.v1+json
Accept: application/vnd.myapp.v2+json

# 方式3: 查询参数
GET /api/users?version=1
```

### 过滤、排序、分页

```http
# 过滤
GET /users?role=admin
GET /users?age>=18&city=北京
GET /users?status=active&created_at>=2024-01-01

# 排序
GET /users?sort=name                      # 升序
GET /users?sort=-created_at               # 降序
GET /users?sort=age,-name                 # 多字段排序

# 分页
GET /users?page=1&per_page=20            # 页码分页
GET /users?offset=0&limit=20             # 偏移分页
GET /users?cursor=abc123&limit=20        # 游标分页

# 字段选择
GET /users?fields=id,name,email           # 只返回指定字段
GET /users?embed=orders,profile           # 包含关联资源

# 完整示例
GET /api/v1/users?role=admin&sort=-created_at&page=2&per_page=20&fields=id,name,email
```

### 字段选择与嵌入

```json
// 响应示例
{
    "data": [
        {
            "id": 1,
            "name": "张三",
            "email": "zhangsan@example.com",
            "_links": {
                "self": { "href": "/users/1" },
                "orders": { "href": "/users/1/orders" }
            }
        }
    ],
    "meta": {
        "page": 2,
        "per_page": 20,
        "total": 500,
        "total_pages": 25
    },
    "links": {
        "self": "/users?page=2&per_page=20",
        "first": "/users?page=1&per_page=20",
        "prev": "/users?page=1&per_page=20",
        "next": "/users?page=3&per_page=20",
        "last": "/users?page=25&per_page=20"
    }
}
```

### 错误响应格式

```json
{
    "error": {
        "code": "VALIDATION_ERROR",
        "message": "输入验证失败",
        "details": [
            {
                "field": "email",
                "message": "邮箱格式不正确",
                "code": "INVALID_FORMAT"
            },
            {
                "field": "age",
                "message": "年龄必须在0-150之间",
                "code": "OUT_OF_RANGE",
                "constraints": { "min": 0, "max": 150 }
            }
        ],
        "request_id": "req_abc123",
        "timestamp": "2024-03-15T10:30:00Z"
    }
}
```

## 五、API 安全

### CORS (跨域资源共享)

```javascript
// Express CORS 配置
const corsOptions = {
    origin: [
        'https://example.com',
        'https://admin.example.com'
    ],
    methods: ['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'OPTIONS'],
    allowedHeaders: ['Content-Type', 'Authorization'],
    exposedHeaders: ['X-RateLimit-Remaining'],
    credentials: true,
    maxAge: 86400  // 预检请求缓存时间 (秒)
};

app.use(cors(corsOptions));
```

### 速率限制 (Rate Limiting)

```javascript
// Express 速率限制
import rateLimit from 'express-rate-limit';

const limiter = rateLimit({
    windowMs: 15 * 60 * 1000,   // 15分钟窗口
    max: 100,                     // 每个IP最多100个请求
    standardHeaders: true,
    legacyHeaders: false,
    message: {
        error: {
            code: 'RATE_LIMIT_EXCEEDED',
            message: '请求过于频繁, 请稍后再试'
        }
    }
});

app.use('/api/', limiter);

// 针对特定路由的严格限制
const authLimiter = rateLimit({
    windowMs: 60 * 60 * 1000,    // 1小时
    max: 5,                       // 登录尝试最多5次
    skipSuccessfulRequests: true  // 成功请求不计数
});

app.use('/api/login', authLimiter);
```

### 认证与授权

```http
# 推荐: JWT Bearer Token
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...

# 替代: API Key (适合服务间调用)
X-API-Key: sk-abc123def456

# OAuth 2.0 授权码流程 (适合第三方应用)
GET /oauth/authorize?response_type=code&client_id=app1&redirect_uri=https://app.com/callback&scope=read&state=xyz

# HTTPS 强制
Strict-Transport-Security: max-age=31536000; includeSubDomains
```

## 六、GraphQL 基础

```graphql
# Schema 定义
type User {
    id: ID!
    name: String!
    email: String!
    age: Int
    posts: [Post!]!
    createdAt: DateTime!
}

type Post {
    id: ID!
    title: String!
    content: String!
    author: User!
    comments: [Comment!]!
}

type Query {
    user(id: ID!): User
    users(page: Int, limit: Int): [User!]!
    search(query: String!): [SearchResult!]!
}

type Mutation {
    createUser(input: CreateUserInput!): User!
    updateUser(id: ID!, input: UpdateUserInput!): User!
    deleteUser(id: ID!): Boolean!
}

input CreateUserInput {
    name: String!
    email: String!
    age: Int
}

union SearchResult = User | Post

# 查询示例
query GetUserWithPosts {
    user(id: "123") {
        name
        email
        posts {
            title
            comments {
                content
            }
        }
    }
}

# 变更示例
mutation CreateNewUser {
    createUser(input: {
        name: "张三"
        email: "zhangsan@example.com"
        age: 28
    }) {
        id
        name
        createdAt
    }
}
```

## 七、OpenAPI / Swagger 文档

```yaml
openapi: 3.0.3
info:
  title: 用户管理 API
  description: 用户管理系统 RESTful API
  version: 1.0.0
  contact:
    name: API 支持
    email: api@example.com

servers:
  - url: https://api.example.com/v1
    description: 生产环境
  - url: https://staging-api.example.com/v1
    description: 测试环境

components:
  securitySchemes:
    BearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT
    ApiKeyAuth:
      type: apiKey
      in: header
      name: X-API-Key

  schemas:
    User:
      type: object
      required: [name, email]
      properties:
        id:
          type: integer
          readOnly: true
        name:
          type: string
          minLength: 2
          maxLength: 50
        email:
          type: string
          format: email
        age:
          type: integer
          minimum: 0
          maximum: 150
        createdAt:
          type: string
          format: date-time
          readOnly: true

    Error:
      type: object
      properties:
        error:
          type: object
          properties:
            code:
              type: string
            message:
              type: string
            details:
              type: array
              items:
                type: object

paths:
  /users:
    get:
      summary: 获取用户列表
      security:
        - BearerAuth: []
      parameters:
        - name: page
          in: query
          schema:
            type: integer
            default: 1
        - name: per_page
          in: query
          schema:
            type: integer
            default: 20
            maximum: 100
        - name: role
          in: query
          schema:
            type: string
        - name: sort
          in: query
          schema:
            type: string
            example: -created_at
      responses:
        '200':
          description: 成功
          content:
            application/json:
              schema:
                type: object
                properties:
                  data:
                    type: array
                    items:
                      $ref: '#/components/schemas/User'
                  meta:
                    $ref: '#/components/schemas/PaginationMeta'
        '401':
          description: 未认证
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Error'

    post:
      summary: 创建用户
      security:
        - BearerAuth: []
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/CreateUserInput'
      responses:
        '201':
          description: 创建成功
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/User'
        '422':
          description: 验证失败
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Error'
```

## 八、cURL 使用

```bash
# GET 请求
curl https://api.example.com/users
curl -X GET "https://api.example.com/users?page=1&per_page=20"

# POST 请求
curl -X POST https://api.example.com/users \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer token123" \
  -d '{"name":"张三","email":"zhangsan@example.com","age":28}'

# PUT 更新
curl -X PUT https://api.example.com/users/123 \
  -H "Content-Type: application/json" \
  -d '{"name":"张三丰","email":"new@example.com"}'

# PATCH 部分更新
curl -X PATCH https://api.example.com/users/123 \
  -H "Content-Type: application/json" \
  -d '{"age": 29}'

# DELETE 删除
curl -X DELETE https://api.example.com/users/123 \
  -H "Authorization: Bearer token123"

# 文件上传
curl -X POST https://api.example.com/upload \
  -F "file=@image.jpg" \
  -F "description=产品图片"

# 自定义头部
curl -H "X-Request-ID: abc123" \
     -H "Accept-Language: zh-CN" \
     https://api.example.com/users

# 跟随重定向
curl -L http://example.com

# 输出详细信息
curl -v https://api.example.com/users

# 只获取响应头
curl -I https://api.example.com/users

# 超时设置
curl --connect-timeout 5 --max-time 30 https://api.example.com/users
```

## 九、API 设计最佳实践

```markdown
1. **使用 HTTPS** - 所有API必须使用HTTPS, 不能有明文HTTP
2. **版本管理** - URL路径版本 (/v1/, /v2/) 或请求头
3. **合理命名** - 使用名词复数, 小写, 连字符 (-)
4. **统一错误格式** - 所有错误使用相同结构
5. **分页** - 为列表接口提供分页, 默认20条
6. **过滤排序** - 支持字段过滤、排序、搜索
7. **HATEOAS** - 返回关联资源的链接
8. **幂等性** - PUT/DELETE 保证幂等
9. **速率限制** - 防止滥用, 返回限流头部
10. **缓存** - 合理使用 ETag / Cache-Control
11. **文档** - 提供 OpenAPI / Swagger 文档
12. **安全** - JWT 认证, CORS 配置, 输入验证
```

> HTTP 协议是 Web API 的基础。RESTful API 设计需要遵循统一约定, 关注安全性、可维护性和开发者体验。推荐使用 OpenAPI 规范进行文档管理。
