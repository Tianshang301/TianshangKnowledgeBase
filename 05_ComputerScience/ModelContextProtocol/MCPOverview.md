---
aliases:
  - MCP协议概述
  - Model Context Protocol Overview
  - MCP总览
tags:
  - MCP
  - AI
  - Protocol
  - LLM
  - Tool-Integration
created: 2026-06-27
updated: 2026-06-27
---

# MCP协议概述

## 什么是MCP

Model Context Protocol (MCP) 是由 Anthropic 于 2024 年发起的一项开放协议，旨在为 AI 模型连接外部工具和数据提供标准化方式。MCP 定义了一套统一的通信规范，使得 LLM 应用能够以一致的方式访问文件系统、数据库、API 等外部资源，而无需为每个数据源或工具编写定制化集成代码。

MCP 的核心理念类似于 USB-C 接口之于硬件设备——它为 AI 应用与外部世界之间建立了一个通用的连接标准。无论底层的 LLM 提供商是谁，只要遵循 MCP 协议，任何 AI 应用都可以无缝接入已有的工具生态。

## 设计动机

### M×N 问题

在 MCP 出现之前，AI 工具集成面临严重的碎片化问题：

- 每个 AI 应用（M 个）需要为每个外部工具/数据源（N 个）编写独立的集成代码
- 总集成数量 = M × N，导致大量的重复工作
- 当新增一个 AI 应用时，需要连接所有 N 个工具；当新增一个工具时，需要适配所有 M 个应用
- 每个集成的接口规范、认证方式、错误处理各不相同，维护成本极高

### MCP 的解决方案：M+N 模式

MCP 通过标准化协议将 M×N 问题简化为 M+N 问题：

- M 个 AI 应用各自实现 MCP Client（M 个集成）
- N 个工具/数据源各自实现 MCP Server（N 个集成）
- 任何 Client 可以与任何 Server 通信，无需额外适配
- 新增应用或工具只需实现一次 MCP 接口即可

这种模式极大地降低了集成成本，促进了工具生态的复用和共享。

## 架构设计

MCP 采用经典的三层架构模型：

```
┌─────────────────────────────────────────┐
│              Host (宿主应用)              │
│  Claude Desktop / Cursor / 自定义应用    │
│                                         │
│  ┌───────────────┐  ┌───────────────┐  │
│  │  MCP Client 1  │  │  MCP Client 2  │  │
│  └───────┬───────┘  └───────┬───────┘  │
└──────────┼──────────────────┼──────────┘
           │                  │
           ▼                  ▼
    ┌──────────────┐  ┌──────────────┐
    │  MCP Server 1 │  │  MCP Server 2 │
    │  (文件系统)    │  │  (GitHub API) │
    └──────────────┘  └──────────────┘
```

### Host（宿主应用）

Host 是运行 AI 模型的应用程序，例如 Claude Desktop、Cursor IDE 或自建应用。Host 负责：

- 管理一个或多个 MCP Client 实例
- 控制用户授权和权限策略
- 协调多个 Client 之间的资源访问
- 渲染 UI 并展示工具执行结果

### Client（客户端）

Client 是 MCP 协议的客户端实现，内嵌在 Host 中。每个 Client 与一个 Server 建立一对一的有状态连接。Client 负责：

- 与 Server 进行能力协商（capability negotiation）
- 发送请求并接收响应
- 处理 Server 发起的通知
- 管理连接生命周期

### Server（服务端）

Server 是工具和数据的提供者，可以是本地进程或远程服务。Server 负责：

- 注册并暴露 Tools、Resources、Prompts 等原语
- 处理 Client 的请求
- 发送通知和进度更新
- 管理自身的状态和资源

## 传输层

MCP 支持两种主要的传输机制：

### stdio（标准输入/输出）

- 适用于本地进程间通信
- Host 以子进程方式启动 Server
- 通过 stdin/stdout 传递 JSON-RPC 2.0 消息
- 每条消息占一行（换行符分隔）
- stderr 用于日志输出，不传输协议消息
- 低延迟、零网络开销，适合本地工具

### HTTP + SSE（Server-Sent Events）

- 适用于远程服务通信
- Client 通过 HTTP POST 发送请求到 Server
- Server 通过 SSE 推送响应和通知
- 支持无状态和有状态两种模式
- 需要考虑认证、CORS、负载均衡等网络问题
- 适合部署在云端的 MCP Server

### 消息格式

所有传输层统一使用 JSON-RPC 2.0 消息格式：

- **Request**: `{"jsonrpc": "2.0", "id": 1, "method": "tools/call", "params": {...}}`
- **Response**: `{"jsonrpc": "2.0", "id": 1, "result": {...}}` 或 `{"jsonrpc": "2.0", "id": 1, "error": {...}}`
- **Notification**: `{"jsonrpc": "2.0", "method": "notifications/progress", "params": {...}}`（无 id 字段）

## 能力协商

MCP 连接建立时，Client 和 Server 通过 `initialize` 握手交换能力信息：

1. Client 发送 `initialize` 请求，声明支持的协议版本和能力
2. Server 响应自己的协议版本、能力集合和服务器信息
3. Client 发送 `initialized` 通知确认握手完成

Server 在握手时可声明以下能力：

- `tools`: 支持工具调用（Tool Calling）
- `resources`: 支持资源访问（Resource Access）
- `prompts`: 支持提示模板（Prompt Templates）
- `sampling`: 支持向 Host 请求 LLM 推理
- `logging`: 支持日志输出

能力协商确保双方了解对方支持的功能，避免不兼容的操作。

## 生命周期

MCP 连接遵循严格的生命周期管理：

```
initialize ──► normal operation ──► shutdown
     │              │                    │
     │         ┌────┴────┐              │
     │         │ request  │              │
     │         │ response │              │
     │         │ notify   │              │
     │         └─────────┘              │
     ▼                                   ▼
  握手阶段                           关闭阶段
```

- **Initialize**: 能力协商，建立连接
- **Normal Operation**: 正常的请求-响应通信，支持并发请求
- **Shutdown**: 优雅关闭，释放资源，Client 发送 `close()` 或连接断开

## MCP 与其他方案对比

| 特性 | MCP | OpenAI Function Calling | LangChain Tools | Semantic Kernel |
|------|-----|------------------------|-----------------|-----------------|
| 开放标准 | ✅ 协议级开放 | ❌ 平台私有 | ❌ 框架绑定 | ❌ 框架绑定 |
| 跨模型兼容 | ✅ 任意 LLM | ❌ 仅 OpenAI | ⚠️ 部分支持 | ⚠️ 部分支持 |
| 工具复用 | ✅ Server 可复用 | ❌ 需重复定义 | ❌ 需重复集成 | ❌ 需重复集成 |
| 双向通信 | ✅ 支持 | ❌ 单向 | ❌ 单向 | ❌ 单向 |
| 动态发现 | ✅ 运行时发现 | ❌ 编译时定义 | ⚠️ 有限 | ⚠️ 有限 |
| 生态规模 | 🚀 快速增长 | 📈 成熟 | 📈 成熟 | 📈 成熟 |

### MCP 的核心优势

- **互操作性**: 一个 Server 可被任意数量的 Client 使用
- **模型无关**: 不绑定特定 LLM 提供商
- **协议级标准化**: 通信规范而非库级 API
- **丰富原语**: Tools、Resources、Prompts、Sampling 四大原语
- **双向通信**: Server 可主动发起请求（Sampling）

## 生态系统

### MCP Server 注册中心

MCP 拥有快速增长的 Server 生态：

- **官方仓库**: `github.com/modelcontextprotocol/servers`
- **社区列表**: `awesome-mcp-servers` 汇总了大量社区贡献的 Server
- **分类索引**: 按功能分类（文件系统、数据库、版本控制、通信、搜索等）

### 热门 MCP Server

| Server | 功能描述 |
|--------|----------|
| `filesystem` | 文件读写、目录浏览、文件搜索 |
| `github` | GitHub API 集成，仓库/Issue/PR 管理 |
| `slack` | Slack 消息发送、频道管理 |
| `postgres` / `sqlite` | 数据库查询和管理 |
| `brave-search` | 网络搜索 |
| `puppeteer` | 浏览器自动化和网页抓取 |
| `memory` | 基于知识图谱的持久化记忆 |
| `fetch` | HTTP 请求和网页内容提取 |

### 生态发展趋势

- MCP Server 数量持续增长，覆盖越来越多的工具和数据源
- 企业开始将内部系统暴露为 MCP Server
- 云服务商提供托管式 MCP Server 方案
- MCP Gateway 模式出现，聚合多个 Server 的能力
- 多 Agent 系统中 MCP 成为 Agent 间通信的标准协议之一

## 协议版本历史

| 版本 | 发布时间 | 主要变更 |
|------|----------|----------|
| 2024-11-05 | 2024年11月 | 首个公开版本，定义 Tools、Resources、Prompts 基础原语 |
| 2025-03-26 | 2025年3月 | 引入 OAuth 2.1 认证、Completions 自动补全、音频内容类型 |
| 2025-06-18 | 2025年6月 | 引入 MCP Registry、结构化工具输出、Elicitation 用户交互 |

协议采用日期版本号（`YYYY-MM-DD`）语义化版本方案，确保向后兼容性。

## 快速开始

### 安装 MCP Server（以文件系统为例）

在 Claude Desktop 配置文件中添加：

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "/path/to/dir"]
    }
  }
}
```

重启 Claude Desktop 后，Claude 即可自动访问指定目录中的文件。

### 开发自定义 Server

使用 TypeScript SDK 创建一个最简 Server：

```typescript
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";

const server = new McpServer({ name: "hello-server", version: "1.0.0" });

server.tool("greet", "问候用户", { name: z.string() }, async ({ name }) => ({
  content: [{ type: "text", text: `你好，${name}！` }],
}));

const transport = new StdioServerTransport();
await server.connect(transport);
```

运行方式：`node dist/index.js`，通过 stdio 与 Host 通信。

## JSON-RPC 2.0 消息详解

### 请求消息

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/call",
  "params": {
    "name": "get-weather",
    "arguments": { "city": "北京" }
  }
}
```

### 成功响应

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "content": [{ "type": "text", "text": "北京：晴，25°C" }]
  }
}
```

### 错误响应

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "error": {
    "code": -32602,
    "message": "Invalid params",
    "data": { "details": "缺少必填参数 'city'" }
  }
}
```

### 通知消息

```json
{
  "jsonrpc": "2.0",
  "method": "notifications/progress",
  "params": { "progress": 50, "total": 100, "message": "处理中..." }
}
```

通知没有 `id` 字段，不期望响应。

## 常见错误码

| 错误码 | 名称 | 说明 |
|--------|------|------|
| -32700 | Parse error | JSON 解析失败 |
| -32600 | Invalid Request | 请求格式无效 |
| -32601 | Method not found | 方法不存在 |
| -32602 | Invalid params | 参数无效 |
| -32603 | Internal error | Server 内部错误 |
| -32000 到 -32099 | Server error | Server 自定义错误范围 |
