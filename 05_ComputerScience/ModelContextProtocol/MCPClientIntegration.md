---
aliases:
  - MCP Client集成
  - MCP Client Integration
  - MCP客户端集成
tags:
  - MCP
  - Client
  - Integration
  - Claude
  - Cursor
  - Cline
created: 2026-06-27
updated: 2026-06-27
---

# MCP Client 集成

## 概述

MCP 的价值在于连接——将 AI 应用与外部工具和数据源连接起来。本文介绍如何在各种主流 AI 应用中配置和使用 MCP Server，以及如何构建自定义的 MCP Client。

## Claude Desktop

### 配置文件

Claude Desktop 通过 `claude_desktop_config.json` 配置 MCP Server：

**macOS 路径**: `~/Library/Application Support/Claude/claude_desktop_config.json`

**Windows 路径**: `%APPDATA%\Claude\claude_desktop_config.json`

### 配置格式

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-filesystem",
        "/Users/username/Documents",
        "/Users/username/Desktop"
      ]
    },
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "ghp_xxxxxxxxxxxx"
      }
    }
  }
}
```

### 配置项说明

- `command`: 启动 Server 的命令（stdio 模式）
- `args`: 命令参数数组
- `env`: 环境变量，用于传递 API Key 等敏感配置

### 使用流程

1. 编辑配置文件，添加所需的 MCP Server
2. 重启 Claude Desktop
3. 在对话中，Claude 会自动识别可用的工具
4. 当 Claude 决定使用工具时，会弹出确认对话框
5. 用户确认后，Claude 调用工具并获取结果
6. 工具调用结果会以可折叠卡片形式展示在对话中

### 常见配置示例

**文件系统 Server**:

```json
{
  "filesystem": {
    "command": "npx",
    "args": ["-y", "@modelcontextprotocol/server-filesystem", "C:\\Users\\username\\projects"]
  }
}
```

**SQLite Server**:

```json
{
  "sqlite": {
    "command": "uvx",
    "args": ["mcp-server-sqlite", "--db-path", "/path/to/database.db"]
  }
}
```

**Brave Search Server**:

```json
{
  "brave-search": {
    "command": "npx",
    "args": ["-y", "@modelcontextprotocol/server-brave-search"],
    "env": {
      "BRAVE_API_KEY": "your-api-key"
    }
  }
}
```

## Cursor IDE

### MCP 设置

Cursor 通过设置面板配置 MCP Server：

1. 打开 Cursor Settings → MCP
2. 点击 "Add new MCP server"
3. 选择传输类型（stdio 或 SSE）
4. 填写配置信息

### 配置文件

Cursor 的 MCP 配置存储在 `.cursor/mcp.json`（项目级）或全局配置中：

```json
{
  "mcpServers": {
    "my-server": {
      "command": "node",
      "args": ["path/to/server.js"],
      "env": {}
    }
  }
}
```

### 工具审批

Cursor 提供了灵活的工具审批机制：

- **自动审批**: 对于可信的工具，可以设置自动执行
- **手动审批**: 每次工具调用都需要用户确认
- **按工具配置**: 可以为不同的工具设置不同的审批策略

工具调用结果会直接嵌入到 AI 对话和代码编辑上下文中。

### Agent 模式集成

在 Cursor 的 Agent 模式下，MCP 工具被深度集成：

- Agent 可以自主决定何时调用工具
- 工具结果直接影响代码生成和编辑
- 支持多工具链式调用
- 工具输出可以作为代码上下文的一部分

## Cline (VS Code)

### MCP 配置

Cline 是 VS Code 中流行的 AI 编程助手，支持 MCP 集成：

1. 打开 VS Code 设置
2. 搜索 "Cline MCP"
3. 编辑 MCP Server 配置

配置文件位于 VS Code 的 settings.json 中：

```json
{
  "cline.mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "/path/to/dir"],
      "alwaysAllow": ["read_file", "list_directory"],
      "disabled": false
    }
  }
}
```

### 自动审批设置

Cline 提供了细粒度的自动审批控制：

- `alwaysAllow`: 自动批准的工具列表，无需每次确认
- `autoApprove`: 全局自动审批开关
- 可以按工具类型（只读/写入/网络）设置不同的审批策略

### 工具调用展示

Cline 会在聊天界面中展示工具调用的详细过程：

- 显示调用的工具名称和参数
- 展示工具执行的实时状态
- 折叠显示工具返回的结果
- 支持查看原始 JSON-RPC 消息

## VS Code Copilot

### Agent 模式

VS Code Copilot 的 Agent 模式支持 MCP 集成：

1. 打开 VS Code 设置
2. 搜索 `github.copilot.chat.agent.enabled`
3. 启用 Agent 模式
4. 配置 MCP Server

### 配置方式

VS Code Copilot 使用与 Cline 类似的配置格式：

```json
{
  "github.copilot.chat.agent.mcpServers": {
    "my-server": {
      "command": "node",
      "args": ["server.js"],
      "env": {}
    }
  }
}
```

### 工具使用

在 Agent 模式下，Copilot 可以：

- 自动选择合适的 MCP 工具
- 将工具结果整合到代码建议中
- 支持多步骤工具调用
- 在聊天中展示工具执行过程

## 构建自定义 Client

### TypeScript Client SDK

```typescript
import { Client } from "@modelcontextprotocol/sdk/client/index.js";
import { StdioClientTransport } from "@modelcontextprotocol/sdk/client/stdio.js";

// 创建 Client
const client = new Client({
  name: "my-client",
  version: "1.0.0",
});

// 配置传输
const transport = new StdioClientTransport({
  command: "node",
  args: ["server.js"],
});

// 连接
await client.connect(transport);

// 列出工具
const { tools } = await client.listTools();
console.log("可用工具:", tools.map(t => t.name));

// 调用工具
const result = await client.callTool({
  name: "get-weather",
  arguments: { city: "北京" },
});
console.log("结果:", result.content[0].text);

// 列出资源
const { resources } = await client.listResources();
console.log("可用资源:", resources.map(r => r.name));

// 读取资源
const resource = await client.readResource({
  uri: "file:///app/config.json",
});
console.log("资源内容:", resource.contents[0].text);

// 调用 Prompt
const prompt = await client.getPrompt({
  name: "code-review",
  arguments: { code: "console.log('hello')", language: "javascript" },
});
console.log("Prompt:", prompt.messages);
```

### Python Client SDK

```python
from mcp.client.session import ClientSession
from mcp.client.stdio import StdioServerParameters, stdio_client

# 配置 Server 参数
server_params = StdioServerParameters(
    command="python",
    args=["server.py"],
    env=None,
)

# 连接并使用
async with stdio_client(server_params) as (read, write):
    async with ClientSession(read, write) as session:
        # 初始化
        await session.initialize()

        # 列出工具
        tools = await session.list_tools()
        print(f"可用工具: {[t.name for t in tools.tools]}")

        # 调用工具
        result = await session.call_tool("get-weather", {"city": "北京"})
        print(f"结果: {result.content[0].text}")

        # 列出资源
        resources = await session.list_resources()
        print(f"可用资源: {[r.name for r in resources.resources]}")

        # 读取资源
        resource = await session.read_resource("file:///app/config.json")
        print(f"资源内容: {resource.contents[0].text}")
```

### 连接管理

```typescript
class MCPClientManager {
  private clients: Map<string, Client> = new Map();

  async connect(name: string, transport: Transport): Promise<Client> {
    const client = new Client({ name: "manager", version: "1.0.0" });
    await client.connect(transport);
    this.clients.set(name, client);
    return client;
  }

  async disconnect(name: string): Promise<void> {
    const client = this.clients.get(name);
    if (client) {
      await client.close();
      this.clients.delete(name);
    }
  }

  getClient(name: string): Client | undefined {
    return this.clients.get(name);
  }

  async disconnectAll(): Promise<void> {
    for (const [name] of this.clients) {
      await this.disconnect(name);
    }
  }
}
```

### 工具调用封装

```typescript
class ToolInvoker {
  constructor(private client: Client) {}

  async invoke(toolName: string, args: Record<string, any>): Promise<string> {
    const result = await this.client.callTool({
      name: toolName,
      arguments: args,
    });

    if (result.isError) {
      throw new Error(`Tool error: ${result.content[0].text}`);
    }

    return result.content
      .filter(c => c.type === "text")
      .map(c => c.text)
      .join("\n");
  }

  async listAvailable(): Promise<string[]> {
    const { tools } = await this.client.listTools();
    return tools.map(t => `${t.name}: ${t.description}`);
  }
}
```

## 多 Server 编排

### 连接多个 Server

实际应用中通常需要连接多个 MCP Server，每个提供不同的能力：

```typescript
const manager = new MCPClientManager();

// 连接文件系统 Server
await manager.connect("filesystem", new StdioClientTransport({
  command: "npx",
  args: ["-y", "@modelcontextprotocol/server-filesystem", "/project"],
}));

// 连接 GitHub Server
await manager.connect("github", new StdioClientTransport({
  command: "npx",
  args: ["-y", "@modelcontextprotocol/server-github"],
  env: { GITHUB_TOKEN: process.env.GITHUB_TOKEN },
}));

// 连接数据库 Server
await manager.connect("database", new StdioClientTransport({
  command: "uvx",
  args: ["mcp-server-sqlite", "--db-path", "/data/app.db"],
}));
```

### 工具路由

将工具调用路由到正确的 Server：

```typescript
class ToolRouter {
  private toolToClient: Map<string, string> = new Map();

  async discoverTools(manager: MCPClientManager): Promise<void> {
    for (const [name, client] of manager.clients) {
      const { tools } = await client.listTools();
      for (const tool of tools) {
        this.toolToClient.set(tool.name, name);
      }
    }
  }

  async route(toolName: string, args: Record<string, any>, manager: MCPClientManager): Promise<any> {
    const clientName = this.toolToClient.get(toolName);
    if (!clientName) throw new Error(`Unknown tool: ${toolName}`);
    const client = manager.getClient(clientName);
    return client.callTool({ name: toolName, arguments: args });
  }
}
```

### 聚合查询

同时查询多个 Server 的资源：

```typescript
async function searchAllServers(
  manager: MCPClientManager,
  query: string
): Promise<Map<string, any[]>> {
  const results = new Map<string, any[]>();

  await Promise.all(
    Array.from(manager.clients.entries()).map(async ([name, client]) => {
      try {
        const { resources } = await client.listResources();
        const matched = resources.filter(r =>
          r.name.toLowerCase().includes(query.toLowerCase())
        );
        results.set(name, matched);
      } catch (error) {
        results.set(name, []);
      }
    })
  );

  return results;
}
```

## 错误处理

### 连接失败

```typescript
async function connectWithRetry(
  client: Client,
  transport: Transport,
  maxRetries = 3
): Promise<void> {
  for (let i = 0; i < maxRetries; i++) {
    try {
      await client.connect(transport);
      return;
    } catch (error) {
      console.error(`Connection attempt ${i + 1} failed:`, error.message);
      if (i === maxRetries - 1) throw error;
      await new Promise(r => setTimeout(r, 1000 * (i + 1)));
    }
  }
}
```

### 超时处理

```typescript
async function callToolWithTimeout(
  client: Client,
  toolName: string,
  args: Record<string, any>,
  timeoutMs = 30000
): Promise<any> {
  return Promise.race([
    client.callTool({ name: toolName, arguments: args }),
    new Promise((_, reject) =>
      setTimeout(() => reject(new Error("Tool call timeout")), timeoutMs)
    ),
  ]);
}
```

### 速率限制

```typescript
class RateLimiter {
  private timestamps: number[] = [];

  constructor(private maxCalls: number, private windowMs: number) {}

  async acquire(): Promise<void> {
    const now = Date.now();
    this.timestamps = this.timestamps.filter(t => now - t < this.windowMs);

    if (this.timestamps.length >= this.maxCalls) {
      const waitTime = this.windowMs - (now - this.timestamps[0]);
      await new Promise(r => setTimeout(r, waitTime));
    }

    this.timestamps.push(Date.now());
  }
}
```

### 优雅降级

当某个 Server 不可用时，提供降级方案：

```typescript
async function callToolSafe(
  manager: MCPClientManager,
  toolName: string,
  args: Record<string, any>,
  fallbackMessage: string
): Promise<string> {
  try {
    const router = new ToolRouter();
    await router.discoverTools(manager);
    const result = await router.route(toolName, args, manager);
    return result.content[0].text;
  } catch (error) {
    console.error(`Tool ${toolName} failed:`, error.message);
    return fallbackMessage;
  }
}
```
