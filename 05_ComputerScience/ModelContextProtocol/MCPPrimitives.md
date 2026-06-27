---
aliases:
  - MCP原语详解
  - Model Context Protocol Primitives
  - MCP核心原语
tags:
  - MCP
  - AI
  - Protocol
  - Tools
  - Resources
  - Prompts
created: 2026-06-27
updated: 2026-06-27
---

# MCP原语详解

## 概述

MCP 协议定义了一组核心原语（Primitives），它们构成了 Client 与 Server 之间交互的基础。每种原语有不同的控制模型和使用场景：

- **Tools**: 由模型（LLM）控制，执行操作
- **Resources**: 由应用程序控制，读取数据
- **Prompts**: 由用户控制，模板化交互
- **Sampling**: 由 Server 发起，请求 LLM 推理
- **Roots**: 定义 Server 的操作边界
- **Completions**: 参数自动补全

## Tools（工具）

### 基本概念

Tools 是 Server 暴露给 LLM 的可执行函数。与 OpenAI Function Calling 类似，但 MCP 的 Tools 是在协议层面标准化的，具有跨模型互操作性。

**控制模型**: Tools 由 LLM 自主决定何时调用。模型根据用户请求和工具描述，推理出需要调用的工具及其参数。Host 应用可以在调用前插入用户确认步骤。

### 定义格式

每个 Tool 包含以下字段：

- `name`: 工具的唯一标识符，如 `database_query`
- `description`: 工具功能的自然语言描述，LLM 依据此描述决定是否调用
- `inputSchema`: JSON Schema 格式的输入参数定义
- `annotations`（可选）: 工具的元信息标注，如是否为只读操作、是否具有破坏性

### 调用流程

```
LLM 推理 → Client 发送 tools/call 请求 → Server 执行 → 返回结果
                                          │
                                    可能包含进度通知
```

1. LLM 根据对话上下文决定调用某个 Tool
2. Client 向 Server 发送 `tools/call` 请求，携带工具名和参数
3. Server 验证输入、执行操作、返回结果
4. 结果可以包含文本、图片、资源引用等多种内容类型

### 输入验证

Server 应严格验证 Tool 的输入参数：

- **TypeScript SDK**: 使用 Zod schema 进行运行时验证
- **Python SDK**: 使用 Pydantic model 进行验证
- 验证失败应返回明确的错误信息，帮助 LLM 理解如何修正调用

### 执行语义

- Tools 执行是同步的（在请求-响应周期内），但可以发送进度通知
- Server 可以声明 Tool 是否为幂等操作
- 长时间运行的 Tool 应通过 `notifications/progress` 报告进度
- Tool 可以返回多种内容类型：text、image、audio、resource 引用

### 错误处理

Tool 执行错误分为两类：

- **协议错误**: JSON-RPC 层面的错误（如方法不存在、参数格式错误）
- **工具错误**: Tool 执行逻辑中的错误（如查询失败、API 超时）

工具错误应在 `result` 中标记 `isError: true`，而非使用 JSON-RPC error。

## Resources（资源）

### 基本概念

Resources 是 Server 暴露给应用程序的数据源。与 Tools 不同，Resources 主要用于数据读取而非操作执行。

**控制模型**: Resources 由应用程序（Host/Client）控制，LLM 通常不直接决定资源访问。应用程序可以根据用户操作或上下文自动加载相关资源。

### URI 体系

每个 Resource 通过唯一的 URI 标识：

- `file:///path/to/file`: 文件系统资源
- `https://api.example.com/data`: HTTP 资源
- `postgres://db/table`: 数据库资源
- `custom://scheme/path`: 自定义 scheme

URI scheme 不限于标准协议，Server 可以定义任意的自定义 scheme 来标识资源。

### 资源类型

**静态资源**: Server 在 `resources/list` 中显式列出的资源。

```json
{
  "uri": "file:///project/README.md",
  "name": "Project README",
  "description": "项目说明文档",
  "mimeType": "text/markdown"
}
```

**动态资源模板**: 使用 URI Template（RFC 6570）定义的参数化资源。

```json
{
  "uriTemplate": "file:///project/{path}",
  "name": "Project Files",
  "description": "项目中的任意文件",
  "mimeType": "application/octet-stream"
}
```

Client 通过填充模板参数生成具体资源 URI。

### 读取操作

Client 通过 `resources/read` 请求读取资源内容：

- 返回资源的内容，可能包含多个部分（text 和 blob）
- 每个内容部分带有 `mimeType` 信息
- 大型资源可以分页读取

### 订阅机制

Client 可以订阅资源变更通知：

1. Client 发送 `resources/subscribe` 请求
2. 当资源内容变化时，Server 发送 `notifications/resources/updated` 通知
3. Client 重新读取资源获取最新内容
4. Client 可以发送 `resources/unsubscribe` 取消订阅

这使得实时数据同步成为可能。

## Prompts（提示模板）

### 基本概念

Prompts 是 Server 预定义的可重用提示模板。它们将复杂的提示工程封装为可参数化的模板，用户可以通过选择和填写参数快速构建高质量提示。

**控制模型**: Prompts 由用户控制。用户主动选择使用哪个 Prompt，填写参数后发送给 LLM。通常在 Host UI 中以斜杠命令（Slash Command）形式呈现。

### 定义格式

每个 Prompt 包含：

- `name`: 唯一标识符，如 `code-review`
- `description`: 功能描述
- `arguments`: 参数列表，每个参数有名称、描述和是否必填

### 参数替换

Prompt 使用参数化设计：

```json
{
  "name": "code-review",
  "description": "代码审查",
  "arguments": [
    {"name": "language", "description": "编程语言", "required": true},
    {"name": "code", "description": "待审查代码", "required": true}
  ]
}
```

当用户调用时，Client 发送 `prompts/get` 请求，Server 返回填充后的消息序列。

### 返回格式

Prompt 返回的是一个消息数组（`messages`），每条消息包含：

- `role`: `user` 或 `assistant`
- `content`: 消息内容，可以是 text、image 或 resource 引用

这使得 Prompt 可以构建复杂的多轮对话上下文，甚至嵌入图片或文件内容。

### 斜杠命令集成

Host 应用通常将 Prompts 映射为斜杠命令：

- `/code-review` → 调用 `code-review` Prompt
- `/translate` → 调用 `translate` Prompt
- `/explain` → 调用 `explain` Prompt

用户在输入框中输入 `/` 即可看到可用的命令列表。

## Sampling（采样）

### 基本概念

Sampling 是 MCP 的独特特性，允许 Server 反向请求 Host 执行 LLM 推理。这打破了传统的单向调用模式，使 Server 能够借助 LLM 的能力处理复杂逻辑。

**控制模型**: Sampling 由 Server 发起，但需要 Host 和用户的明确批准。这是一种"人在回路"（Human-in-the-Loop）的设计，确保用户对 LLM 调用有完全的控制权。

### 使用场景

- Server 需要 LLM 帮助分析数据
- Server 需要 LLM 生成自然语言摘要
- Server 需要 LLM 做决策或分类
- 实现 Agent 嵌套（Server 内部使用 LLM）

### 请求格式

Server 发送 `sampling/createMessage` 请求：

```json
{
  "messages": [
    {"role": "user", "content": {"type": "text", "text": "分析这段日志..."}}
  ],
  "modelPreferences": {
    "hints": [{"name": "claude-sonnet-4-20250514"}],
    "costPriority": 0.5,
    "speedPriority": 0.8,
    "intelligencePriority": 0.9
  },
  "systemPrompt": "你是一个日志分析专家",
  "maxTokens": 1024
}
```

### 审批流程

1. Server 发送 Sampling 请求
2. Host 展示请求内容给用户
3. 用户可以批准、修改或拒绝请求
4. 如果批准，Host 调用 LLM 并返回结果
5. Host 可以对请求内容进行脱敏或截断

### 消息格式

Sampling 请求中的消息格式与标准 LLM API 一致：

- `role`: `user` 或 `assistant`
- `content`: 可以是 `text` 类型或 `image` 类型
- 支持多模态输入（文本 + 图片）

## Roots（根路径）

### 基本概念

Roots 定义了 Server 可以访问的文件系统边界或 URI 范围。它们为 Server 提供了上下文信息，告知 Server 应该关注哪些目录或资源。

### 用途

- 限制文件系统 Server 的访问范围
- 为 Server 提供项目上下文（如工作区根目录）
- 安全隔离，防止 Server 访问超出范围的文件

### 定义格式

```json
{
  "roots": [
    {"uri": "file:///home/user/project", "name": "My Project"},
    {"uri": "https://api.example.com", "name": "API Server"}
  ]
}
```

Roots 在 `initialize` 阶段通过 Client 的能力声明传递给 Server。

## Completions（自动补全）

### 基本概念

Completions 为 Prompts 和 Resources 的参数提供自动补全功能。当用户输入参数时，Client 可以向 Server 请求补全建议，提升用户体验。

### 工作流程

1. 用户在 Prompt 参数输入框中输入部分内容
2. Client 发送 `completion/complete` 请求
3. Server 返回匹配的补全建议列表
4. Client 展示建议供用户选择

### 补全范围

- `ref/prompt`: 对 Prompt 参数的补全
- `ref/resource`: 对 Resource URI 的补全

```json
{
  "ref": {"type": "ref/prompt", "name": "code-review"},
  "argument": {"name": "language", "value": "py"}
}
```

Server 返回 `["python", "pydantic", "pyspark"]` 等匹配建议。

## Notifications（通知）

### 概述

MCP 支持 Server 向 Client 发送异步通知，用于报告进度、资源变更等信息。通知是单向的，不期望响应。

### 通知类型

**进度通知** (`notifications/progress`):

- 报告长时间操作的执行进度
- 包含 `progress`（当前进度）、`total`（总量）、`message`（描述信息）
- 通过 `progressToken` 关联到原始请求

**资源变更通知** (`notifications/resources/updated`):

- 通知 Client 资源内容已变化
- 包含变化资源的 URI
- Client 可选择重新读取资源

**工具列表变更** (`notifications/tools/list_changed`):

- 通知 Client Server 的工具列表发生变化
- Client 应重新调用 `tools/list` 获取最新列表

**提示列表变更** (`notifications/prompts/list_changed`):

- 通知 Client Server 的 Prompt 列表发生变化

**日志通知** (`notifications/message`):

- Server 向 Client 输出日志信息
- 包含日志级别（debug/info/warning/error）
- Host 可选择展示或记录这些日志

## Pagination（分页）

### 概述

对于可能返回大量结果的列表操作，MCP 支持基于游标的分页机制。

### 支持分页的操作

- `tools/list`
- `resources/list`
- `prompts/list`
- `resources/templates/list`

### 分页流程

1. Client 发送首次请求（不带 `cursor`）
2. 如果结果未完，Server 在响应中返回 `nextCursor`
3. Client 使用 `nextCursor` 作为后续请求的 `cursor` 参数
4. 重复直到不再返回 `nextCursor`

```json
// 首次请求
{"method": "tools/list"}

// 响应
{
  "tools": [...],
  "nextCursor": "eyJwYWdlIjogMn0="
}

// 后续请求
{"method": "tools/list", "params": {"cursor": "eyJwYWdlIjogMn0="}}
```

分页机制确保了大规模 Server（拥有大量工具或资源）的性能表现。
