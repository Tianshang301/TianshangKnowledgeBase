---
aliases:
  - MCP Server开发实战
  - MCP Server Development
  - MCP服务端开发
tags:
  - MCP
  - Server
  - TypeScript
  - Python
  - SDK
  - Development
created: 2026-06-27
updated: 2026-06-27
---

# MCP Server 开发实战

## 概述

MCP Server 是 MCP 生态的核心组成部分，负责将工具和数据暴露给 AI 模型。本文介绍使用 TypeScript 和 Python SDK 开发 MCP Server 的完整流程，包括工具实现、资源管理、传输配置、测试和发布。

## TypeScript SDK

### 安装与初始化

使用 `@modelcontextprotocol/sdk` 包开发 TypeScript Server：

```bash
npm init -y
npm install @modelcontextprotocol/sdk zod
npm install -D typescript @types/node
```

### Server 基本结构

```typescript
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";

const server = new McpServer({
  name: "my-mcp-server",
  version: "1.0.0",
});

// 注册工具、资源、提示...

const transport = new StdioServerTransport();
await server.connect(transport);
```

### 注册工具（Tools）

使用 `server.tool()` 方法注册工具：

```typescript
server.tool(
  "get-weather",
  "获取指定城市的天气信息",
  {
    city: z.string().describe("城市名称"),
    unit: z.enum(["celsius", "fahrenheit"]).default("celsius"),
  },
  async ({ city, unit }) => {
    const weather = await fetchWeather(city, unit);
    return {
      content: [
        {
          type: "text",
          text: `${city} 天气: ${weather.temp}°${unit === "celsius" ? "C" : "F"}, ${weather.condition}`,
        },
      ],
    };
  }
);
```

工具定义包括名称、描述、参数 Schema 和处理函数。Zod schema 用于运行时输入验证。

### 注册资源（Resources）

使用 `server.resource()` 方法注册资源：

```typescript
// 静态资源
server.resource(
  "config",
  "file:///app/config.json",
  { mimeType: "application/json" },
  async (uri) => ({
    contents: [
      {
        uri: uri.href,
        text: JSON.stringify({ theme: "dark", lang: "zh" }),
      },
    ],
  })
);

// 动态资源模板
server.resource(
  "file-content",
  new ResourceTemplate("file:///{path}", { list: undefined }),
  async (uri, { path }) => ({
    contents: [
      {
        uri: uri.href,
        text: await readFile(path as string, "utf-8"),
      },
    ],
  })
);
```

### 注册提示（Prompts）

使用 `server.prompt()` 方法注册提示模板：

```typescript
server.prompt(
  "code-review",
  "代码审查助手",
  {
    code: z.string().describe("待审查的代码"),
    language: z.string().describe("编程语言"),
  },
  ({ code, language }) => ({
    messages: [
      {
        role: "user",
        content: {
          type: "text",
          text: `请审查以下 ${language} 代码：\n\n\`\`\`${language}\n${code}\n\`\`\`\n\n请指出潜在问题并提供改进建议。`,
        },
      },
    ],
  })
);
```

## Python SDK

### 安装与初始化

使用 `mcp` 包开发 Python Server：

```bash
pip install mcp
```

### FastMCP 高级 API

FastMCP 提供了装饰器风格的简洁 API：

```python
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("my-mcp-server")

@mcp.tool()
def get_weather(city: str, unit: str = "celsius") -> str:
    """获取指定城市的天气信息"""
    weather = fetch_weather(city, unit)
    return f"{city} 天气: {weather['temp']}°{'C' if unit == 'celsius' else 'F'}"

@mcp.resource("config://app")
def get_config() -> str:
    """获取应用配置"""
    return json.dumps({"theme": "dark", "lang": "zh"})

@mcp.prompt()
def code_review(code: str, language: str) -> str:
    """代码审查助手"""
    return f"请审查以下 {language} 代码：\n\n```{language}\n{code}\n```"
```

### 底层 Server API

对于更精细的控制，可以使用底层 API：

```python
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

server = Server("my-mcp-server")

@server.list_tools()
async def list_tools():
    return [
        Tool(
            name="get-weather",
            description="获取天气信息",
            inputSchema={
                "type": "object",
                "properties": {
                    "city": {"type": "string", "description": "城市名称"}
                },
                "required": ["city"]
            }
        )
    ]

@server.call_tool()
async def call_tool(name: str, arguments: dict):
    if name == "get-weather":
        result = fetch_weather(arguments["city"])
        return [TextContent(type="text", text=str(result))]

async def main():
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, server.create_initialization_options())
```

## 工具实现最佳实践

### 输入验证

**TypeScript (Zod)**:

```typescript
const schema = z.object({
  query: z.string().min(1).max(1000),
  limit: z.number().int().min(1).max(100).default(10),
  format: z.enum(["json", "csv", "text"]).default("json"),
});
```

**Python (Pydantic)**:

```python
from pydantic import BaseModel, Field

class QueryParams(BaseModel):
    query: str = Field(..., min_length=1, max_length=1000)
    limit: int = Field(default=10, ge=1, le=100)
    format: str = Field(default="json", pattern="^(json|csv|text)$")
```

### 错误处理

```typescript
server.tool("risky-operation", {}, async () => {
  try {
    const result = await doRiskyThing();
    return { content: [{ type: "text", text: result }] };
  } catch (error) {
    return {
      content: [{ type: "text", text: `操作失败: ${error.message}` }],
      isError: true,
    };
  }
});
```

工具执行错误应返回 `isError: true`，而非抛出异常。这使 LLM 能够理解错误并尝试修正。

### 进度报告

```typescript
server.tool("long-task", {}, async (_, { sendNotification }) => {
  for (let i = 0; i < 100; i++) {
    await processItem(i);
    await sendNotification({
      method: "notifications/progress",
      params: { progress: i + 1, total: 100, message: `处理第 ${i + 1} 项` },
    });
  }
  return { content: [{ type: "text", text: "处理完成" }] };
});
```

## 传输层配置

### stdio 传输

适用于本地进程，最常用的传输方式：

```typescript
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
const transport = new StdioServerTransport();
await server.connect(transport);
```

```python
from mcp.server.stdio import stdio_server
async with stdio_server() as (read_stream, write_stream):
    await server.run(read_stream, write_stream)
```

### SSE 传输

适用于远程部署，基于 HTTP + Server-Sent Events：

```typescript
import { SSEServerTransport } from "@modelcontextprotocol/sdk/server/sse.js";
import express from "express";

const app = express();
let transport: SSEServerTransport;

app.get("/sse", async (req, res) => {
  transport = new SSEServerTransport("/messages", res);
  await server.connect(transport);
});

app.post("/messages", async (req, res) => {
  await transport.handlePostMessage(req, res);
});

app.listen(3000);
```

```python
from mcp.server.sse import SseServerTransport
from starlette.applications import Starlette
from starlette.routing import Route, Mount

sse = SseServerTransport("/messages")

async def handle_sse(request):
    async with sse.connect_sse(request.scope, request.receive, request._send) as streams:
        await server.run(streams[0], streams[1], server.create_initialization_options())

app = Starlette(
    routes=[
        Route("/sse", endpoint=handle_sse),
        Mount("/messages", app=sse.handle_post_message),
    ]
)
```

### 自定义传输

实现 `Transport` 接口即可创建自定义传输：

```typescript
interface Transport {
  start(): Promise<void>;
  close(): Promise<void>;
  send(message: JSONRPCMessage): Promise<void>;
  onclose?: () => void;
  onerror?: (error: Error) => void;
  onmessage?: (message: JSONRPCMessage) => void;
}
```

## 测试策略

### MCP Inspector

MCP Inspector 是官方提供的调试工具，用于交互式测试 MCP Server：

```bash
npx @modelcontextprotocol/inspector node dist/index.js
```

Inspector 提供 Web UI，可以：

- 浏览 Server 暴露的 Tools、Resources、Prompts
- 手动调用 Tools 并查看返回结果
- 读取 Resources 内容
- 测试 Prompts 模板
- 查看原始 JSON-RPC 消息

### 单元测试

```typescript
import { Client } from "@modelcontextprotocol/sdk/client/index.js";
import { InMemoryTransport } from "@modelcontextprotocol/sdk/inMemory.js";

describe("MCP Server", () => {
  let client: Client;
  let server: McpServer;

  beforeEach(async () => {
    server = createServer(); // 你的 Server 创建函数
    client = new Client({ name: "test-client", version: "1.0.0" });
    const [clientTransport, serverTransport] = InMemoryTransport.createPair();
    await Promise.all([
      client.connect(clientTransport),
      server.connect(serverTransport),
    ]);
  });

  test("should list tools", async () => {
    const { tools } = await client.listTools();
    expect(tools).toHaveLength(1);
    expect(tools[0].name).toBe("get-weather");
  });

  test("should call tool", async () => {
    const result = await client.callTool({ name: "get-weather", arguments: { city: "北京" } });
    expect(result.content[0].text).toContain("北京");
  });
});
```

## 实战示例

### 数据库查询 Server

```typescript
server.tool(
  "query-database",
  "执行 SQL 查询（只读）",
  {
    sql: z.string().describe("SQL 查询语句"),
    database: z.string().default("main"),
  },
  async ({ sql, database }) => {
    // 安全检查：只允许 SELECT 语句
    if (!sql.trim().toUpperCase().startsWith("SELECT")) {
      return {
        content: [{ type: "text", text: "错误：只允许 SELECT 查询" }],
        isError: true,
      };
    }
    const result = await db.query(sql, database);
    return { content: [{ type: "text", text: JSON.stringify(result, null, 2) }] };
  }
);
```

### 文件搜索 Server

```typescript
server.tool(
  "search-files",
  "在项目中搜索文件内容",
  {
    pattern: z.string().describe("搜索关键词或正则表达式"),
    path: z.string().default(".").describe("搜索目录"),
    fileTypes: z.array(z.string()).optional().describe("文件类型过滤"),
  },
  async ({ pattern, path, fileTypes }) => {
    const results = await grep(pattern, path, fileTypes);
    return {
      content: [{ type: "text", text: formatSearchResults(results) }],
    };
  }
);
```

### API 集成 Server

```typescript
server.tool(
  "api-request",
  "发送 HTTP API 请求",
  {
    method: z.enum(["GET", "POST", "PUT", "DELETE"]),
    url: z.string().url(),
    headers: z.record(z.string()).optional(),
    body: z.any().optional(),
  },
  async ({ method, url, headers, body }) => {
    const response = await fetch(url, {
      method,
      headers: { "Content-Type": "application/json", ...headers },
      body: body ? JSON.stringify(body) : undefined,
    });
    const data = await response.json();
    return { content: [{ type: "text", text: JSON.stringify(data, null, 2) }] };
  }
);
```

## 发布与部署

### npm 包发布

```json
{
  "name": "mcp-server-example",
  "version": "1.0.0",
  "bin": { "mcp-server-example": "./dist/index.js" },
  "files": ["dist"],
  "scripts": { "build": "tsc", "prepublishOnly": "npm run build" }
}
```

在 `package.json` 中添加 `bin` 字段使 Server 可以通过 `npx` 直接运行。

### PyPI 包发布

```toml
[project]
name = "mcp-server-example"
version = "0.1.0"
[project.scripts]
mcp-server-example = "my_server:main"
```

使用 `hatchling` 或 `setuptools` 构建并发布到 PyPI。

### Docker 容器化

```dockerfile
FROM node:20-slim
WORKDIR /app
COPY package*.json ./
RUN npm ci --production
COPY dist ./dist
CMD ["node", "dist/index.js"]
```

容器化部署适合远程 SSE 传输模式，便于水平扩展和负载均衡。

### 配置管理

Server 通常需要配置信息（API Key、数据库连接等），推荐方式：

- 环境变量（最常用）
- 命令行参数
- 配置文件
- Host 应用通过 `initialize` 请求传递
