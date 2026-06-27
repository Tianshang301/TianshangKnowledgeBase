---
aliases:
  - MCP安全与最佳实践
  - MCP Security and Patterns
  - MCP安全模式
tags:
  - MCP
  - Security
  - Patterns
  - Best-Practices
  - Architecture
created: 2026-06-27
updated: 2026-06-27
---

# MCP 安全与最佳实践

## 概述

MCP 协议在设计时充分考虑了安全性，通过多层次的安全机制确保 AI 模型与外部工具交互的可控性。本文介绍 MCP 的信任模型、权限控制、安全防护措施以及架构设计模式。

## 信任模型

### 核心原则

MCP 的信任模型基于一个核心假设：**Host 是可信的中介者**。

```
User ──► Host ──► Client ──► Server
  │        │         │          │
  │     信任边界    信任边界     │
  │        │         │          │
  └────────┴─────────┴──────────┘
           用户授权范围
```

- **Host** 负责管理用户授权和安全策略
- **Client** 在 Host 的监督下与 Server 通信
- **Server** 被视为潜在不可信的第三方
- **User** 对所有关键操作拥有最终决定权

### 交互流程中的安全控制

1. **连接阶段**: Host 决定连接哪些 Server，用户可以审查 Server 列表
2. **发现阶段**: Client 获取 Server 的能力列表，Host 可以过滤或限制
3. **调用阶段**: 每次工具调用都可以要求用户确认
4. **执行阶段**: Host 可以监控工具执行过程
5. **结果阶段**: Host 可以对工具返回结果进行过滤或脱敏

## 用户同意机制

### 工具调用确认

Host 应在工具执行前征得用户同意，尤其是以下场景：

- 具有副作用的操作（写文件、发送消息、修改数据）
- 访问敏感资源（密码、密钥、个人信息）
- 网络请求（调用外部 API）
- 首次使用的工具

### 确认 UI 设计

Host 应向用户展示清晰的确认信息：

- 工具名称和描述
- 完整的调用参数
- 预期的操作结果
- 潜在的风险提示（如写操作、不可逆操作）

### 批量操作策略

对于连续的多次工具调用，Host 可以提供：

- 逐次确认（最安全）
- 批量确认（用户一次确认多个操作）
- 自动审批白名单（用户预先批准特定工具）

## 权限控制

### 工具级权限

Host 可以对每个工具设置独立的权限策略：

```json
{
  "permissions": {
    "filesystem": {
      "read_file": "auto",
      "write_file": "confirm",
      "delete_file": "deny"
    },
    "database": {
      "query": "auto",
      "execute": "confirm"
    }
  }
}
```

权限级别：

- `auto`: 自动允许，无需用户确认
- `confirm`: 每次调用需要用户确认
- `deny`: 禁止调用

### 资源访问控制

Host 可以限制 Server 可以访问的资源范围：

- **文件系统**: 通过 Roots 限定可访问的目录
- **网络**: 限制 Server 可以请求的域名
- **数据库**: 限制可访问的数据库和表
- **API**: 限制可用的 API 端点

### 粒度控制

权限控制可以细化到不同粒度：

- 全局策略：对所有 Server 生效
- Server 级策略：对特定 Server 生效
- 工具级策略：对特定工具生效
- 参数级策略：根据参数值决定权限

## 沙箱隔离

### 进程隔离（本地 Server）

本地 stdio 传输的 Server 以子进程方式运行，天然具有进程级隔离：

- Server 进程与 Host 进程独立
- Host 可以随时终止 Server 进程
- 进程级的资源限制（CPU、内存、文件句柄）
- 操作系统的权限机制提供额外保护

### 容器化部署（远程 Server）

远程 SSE 传输的 Server 推荐使用容器化部署：

```dockerfile
FROM node:20-slim
WORKDIR /app
COPY package*.json ./
RUN npm ci --production
COPY dist ./dist

# 非 root 用户运行
RUN addgroup --system appgroup && adduser --system --ingroup appgroup appuser
USER appuser

# 只暴露必要端口
EXPOSE 3000

CMD ["node", "dist/index.js"]
```

容器化的优势：

- 文件系统隔离，Server 只能访问挂载的卷
- 网络隔离，可以限制 Server 的网络访问
- 资源限制（CPU、内存、磁盘）
- 快速销毁和重建

### 操作系统级沙箱

对于高安全要求场景，可以使用操作系统级沙箱：

- **Linux**: seccomp、AppArmor、SELinux
- **Windows**: Windows Sandbox、AppContainer
- **macOS**: sandbox-exec

## OAuth 2.1 认证

### 远程 Server 认证

MCP 支持 OAuth 2.1 协议为远程 Server 提供认证：

```
Client ──► Authorization Server
   │            │
   │◄── token ──┘
   │
   └──► Resource Server (MCP Server)
        │
        │◄── Bearer token
        │
        └──► 授权访问
```

### 认证流程

1. Client 向 Authorization Server 请求授权
2. 用户在浏览器中完成授权
3. Authorization Server 返回 access token
4. Client 使用 token 访问 MCP Server
5. Server 验证 token 并决定是否允许访问

### Token 管理

- **存储**: token 应安全存储，避免明文暴露
- **刷新**: 支持 refresh token 机制，避免频繁授权
- **作用域**: 使用最小权限原则，只请求必要的 scope
- **过期**: 设置合理的 token 过期时间

### 配置示例

```json
{
  "mcpServers": {
    "remote-server": {
      "url": "https://mcp.example.com/sse",
      "oauth": {
        "clientId": "my-client-id",
        "authorizationEndpoint": "https://auth.example.com/authorize",
        "tokenEndpoint": "https://auth.example.com/token",
        "scopes": ["read", "write"]
      }
    }
  }
}
```

## 输入验证

### 防止注入攻击

Server 应严格验证所有输入参数，防止各种注入攻击：

**SQL 注入防护**:

```typescript
server.tool("query-db", { sql: z.string() }, async ({ sql }) => {
  // 使用参数化查询，而非字符串拼接
  const sanitized = sql.replace(/[^a-zA-Z0-9\s\,\.\(\)]/g, "");
  if (!sanitized.toUpperCase().startsWith("SELECT")) {
    return { content: [{ type: "text", text: "只允许 SELECT 查询" }], isError: true };
  }
  const result = await db.query(sanitized);
  return { content: [{ type: "text", text: JSON.stringify(result) }] };
});
```

**命令注入防护**:

```typescript
server.tool("run-command", { cmd: z.string() }, async ({ cmd }) => {
  // 禁止危险字符
  const dangerous = /[;&|`$(){}[\]!#]/;
  if (dangerous.test(cmd)) {
    return { content: [{ type: "text", text: "命令包含非法字符" }], isError: true };
  }
  // 使用白名单而非黑名单
  const allowedCommands = ["ls", "cat", "grep", "find"];
  const baseCmd = cmd.split(" ")[0];
  if (!allowedCommands.includes(baseCmd)) {
    return { content: [{ type: "text", text: `不允许的命令: ${baseCmd}` }], isError: true };
  }
});
```

**路径遍历防护**:

```typescript
server.tool("read-file", { path: z.string() }, async ({ path }) => {
  // 规范化路径并检查是否在允许的目录内
  const resolved = path.resolve(path);
  const allowedDir = "/project";
  if (!resolved.startsWith(allowedDir)) {
    return { content: [{ type: "text", text: "路径越界" }], isError: true };
  }
  // 检查路径遍历尝试
  if (path.includes("..")) {
    return { content: [{ type: "text", text: "不允许路径遍历" }], isError: true };
  }
});
```

### 参数消毒

对所有外部输入进行消毒处理：

- 字符串参数：限制长度、过滤特殊字符
- 数字参数：检查范围、防止溢出
- URL 参数：验证协议和域名
- 文件路径：规范化路径、检查白名单目录

## 速率限制

### 工具级速率限制

Server 可以对每个工具设置独立的速率限制：

```typescript
class RateLimiter {
  private limits = new Map<string, { count: number; resetTime: number }>();

  check(toolName: string, maxCalls: number, windowMs: number): boolean {
    const now = Date.now();
    const record = this.limits.get(toolName);

    if (!record || now > record.resetTime) {
      this.limits.set(toolName, { count: 1, resetTime: now + windowMs });
      return true;
    }

    if (record.count >= maxCalls) {
      return false;
    }

    record.count++;
    return true;
  }
}
```

### 成本管理

对于调用外部 API 的工具，需要考虑成本控制：

- 记录每个工具的 API 调用次数
- 设置每日/每月的调用上限
- 监控异常调用模式
- 在接近限额时发出警告

### Server 级限制

Host 可以对整个 Server 设置速率限制：

```json
{
  "rateLimits": {
    "requestsPerMinute": 60,
    "requestsPerHour": 1000,
    "maxConcurrent": 10
  }
}
```

## 设计模式

### 代理模式（Proxy Pattern）

聚合多个 MCP Server 的能力为统一接口：

```typescript
class AggregatingProxyServer {
  private servers: Map<string, Client> = new Map();

  constructor(private mcpServer: McpServer) {}

  async addServer(name: string, client: Client): Promise<void> {
    this.servers.set(name, client);
    const { tools } = await client.listTools();

    for (const tool of tools) {
      this.mcpServer.tool(
        `${name}_${tool.name}`,
        tool.description,
        tool.inputSchema,
        async (args) => {
          return client.callTool({ name: tool.name, arguments: args });
        }
      );
    }
  }
}
```

代理模式的优势：

- 为 Client 提供统一的工具入口
- 可以在代理层添加日志、缓存、限流等功能
- 屏蔽后端 Server 的差异
- 实现负载均衡和故障转移

### 中间件模式（Middleware Pattern）

在请求处理链中添加横切关注点：

```typescript
type Middleware = (
  toolName: string,
  args: Record<string, any>,
  next: () => Promise<any>
) => Promise<any>;

const loggingMiddleware: Middleware = async (toolName, args, next) => {
  console.log(`[${new Date().toISOString()}] Calling ${toolName}`, args);
  const start = Date.now();
  try {
    const result = await next();
    console.log(`[${new Date().toISOString()}] ${toolName} completed in ${Date.now() - start}ms`);
    return result;
  } catch (error) {
    console.error(`[${new Date().toISOString()}] ${toolName} failed:`, error.message);
    throw error;
  }
};

const authMiddleware: Middleware = async (toolName, args, next) => {
  if (!isAuthorized(toolName)) {
    throw new Error(`Unauthorized: ${toolName}`);
  }
  return next();
};

const cacheMiddleware: Middleware = async (toolName, args, next) => {
  const cacheKey = `${toolName}:${JSON.stringify(args)}`;
  const cached = cache.get(cacheKey);
  if (cached) return cached;
  const result = await next();
  cache.set(cacheKey, result, { ttl: 300000 });
  return result;
};
```

### 熔断器模式（Circuit Breaker）

防止故障级联，保护系统稳定性：

```typescript
enum CircuitState {
  CLOSED,    // 正常状态，允许请求
  OPEN,      // 熔断状态，拒绝请求
  HALF_OPEN, // 半开状态，允许少量请求探测
}

class CircuitBreaker {
  private state = CircuitState.CLOSED;
  private failureCount = 0;
  private lastFailureTime = 0;

  constructor(
    private failureThreshold = 5,
    private recoveryTimeout = 30000
  ) {}

  async call<T>(fn: () => Promise<T>): Promise<T> {
    if (this.state === CircuitState.OPEN) {
      if (Date.now() - this.lastFailureTime > this.recoveryTimeout) {
        this.state = CircuitState.HALF_OPEN;
      } else {
        throw new Error("Circuit is open");
      }
    }

    try {
      const result = await fn();
      this.onSuccess();
      return result;
    } catch (error) {
      this.onFailure();
      throw error;
    }
  }

  private onSuccess(): void {
    this.failureCount = 0;
    this.state = CircuitState.CLOSED;
  }

  private onFailure(): void {
    this.failureCount++;
    this.lastFailureTime = Date.now();
    if (this.failureCount >= this.failureThreshold) {
      this.state = CircuitState.OPEN;
    }
  }
}
```

### 重试模式（Retry Pattern）

对暂时性故障进行自动重试：

```typescript
async function withRetry<T>(
  fn: () => Promise<T>,
  options: {
    maxRetries?: number;
    baseDelay?: number;
    maxDelay?: number;
    retryableErrors?: string[];
  } = {}
): Promise<T> {
  const { maxRetries = 3, baseDelay = 1000, maxDelay = 10000 } = options;

  for (let attempt = 0; attempt <= maxRetries; attempt++) {
    try {
      return await fn();
    } catch (error) {
      if (attempt === maxRetries) throw error;

      const delay = Math.min(baseDelay * Math.pow(2, attempt), maxDelay);
      const jitter = delay * 0.1 * Math.random();
      await new Promise(r => setTimeout(r, delay + jitter));
    }
  }

  throw new Error("Max retries exceeded");
}
```

## 社区生态

### 官方参考 Server

MCP 官方提供了一系列参考 Server 实现：

- `@modelcontextprotocol/server-filesystem`: 文件系统访问
- `@modelcontextprotocol/server-github`: GitHub API 集成
- `@modelcontextprotocol/server-gitlab`: GitLab API 集成
- `@modelcontextprotocol/server-google-drive`: Google Drive 访问
- `@modelcontextprotocol/server-postgres`: PostgreSQL 数据库
- `@modelcontextprotocol/server-slack`: Slack 消息和频道
- `@modelcontextprotocol/server-memory`: 基于知识图谱的记忆系统
- `@modelcontextprotocol/server-puppeteer`: 浏览器自动化
- `@modelcontextprotocol/server-brave-search`: Brave 搜索
- `@modelcontextprotocol/server-fetch`: HTTP 请求和内容提取

### awesome-mcp-servers

社区维护的 MCP Server 列表，按类别分类：

- **开发工具**: Git、CI/CD、代码分析、文档生成
- **数据存储**: 各种数据库、对象存储、缓存系统
- **通信协作**: 邮件、即时通讯、项目管理
- **云服务**: AWS、GCP、Azure 各种服务
- **AI/ML**: 模型推理、数据处理、特征工程
- **实用工具**: 天气、翻译、计算、加密

### 生态贡献指南

开发并分享 MCP Server 的最佳实践：

- 遵循 MCP 协议规范
- 提供清晰的工具描述和参数文档
- 实现完善的输入验证和错误处理
- 支持配置化（环境变量、配置文件）
- 编写使用文档和示例
- 发布到 npm 或 PyPI

## 未来方向

### 多 Agent 系统中的 MCP

MCP 在多 Agent 架构中扮演重要角色：

- Agent 之间通过 MCP Server 共享工具和数据
- 每个 Agent 可以作为其他 Agent 的 MCP Server
- MCP Sampling 实现 Agent 间的 LLM 能力共享
- 统一的工具发现和调用机制简化 Agent 编排

### MCP Gateway 模式

Gateway 作为 MCP 生态的基础设施：

- 聚合多个后端 Server 为统一入口
- 提供认证、授权、限流等横切功能
- 实现工具的版本管理和灰度发布
- 监控和审计所有 MCP 交互
- 缓存工具结果，优化性能

### 企业级 MCP 平台

企业可以构建内部 MCP 平台：

- 将内部系统（ERP、CRM、OA）封装为 MCP Server
- 统一的权限管理和审计日志
- Server 注册中心和服务发现
- 工具市场和自助式工具发布
- 与企业现有 IAM 系统集成

### 协议演进

MCP 协议的未来发展方向：

- 更丰富的权限模型
- 流式工具调用（长时间运行的工具）
- 工具组合和工作流定义
- 跨 Server 的事务支持
- 性能优化（批量调用、并行执行）
