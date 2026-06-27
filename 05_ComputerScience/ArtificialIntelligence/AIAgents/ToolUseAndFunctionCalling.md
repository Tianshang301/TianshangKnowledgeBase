---
aliases:
  - 工具使用与函数调用
  - Function Calling
  - Tool Use
tags:
  - AI/Agent
  - AI/ToolUse
  - AI/FunctionCalling
created: 2026-06-28
updated: 2026-06-28
---

# 工具使用与函数调用

工具使用（Tool Use）是将LLM从纯文本生成器转变为能与外部世界交互的智能Agent的关键能力。通过Function Calling，LLM可以调用API、操作数据库、执行代码、控制设备等，极大扩展了其应用范围。

## Function Calling机制

### OpenAI实现

OpenAI在2023年6月率先推出Function Calling功能，后续演进为Tools API。

**基本流程**：

1. 定义函数：在API请求中通过JSON Schema描述可用函数
2. 模型决策：LLM分析用户意图，决定是否调用函数及参数
3. 返回结构化调用：模型输出JSON格式的函数名和参数
4. 客户端执行：应用层执行实际函数调用
5. 结果回传：将执行结果作为新消息发回模型
6. 模型总结：模型基于结果生成最终回复

**关键参数**：

- `tools`：定义工具列表，每个工具包含`type`、`function`（含name、description、parameters）
- `tool_choice`：控制工具调用行为（`auto`/`none`/`required`/指定函数）
- `parallel_tool_calls`：是否允许并行调用多个工具

### Anthropic实现

Claude的Tool Use实现与OpenAI类似但有差异。

- 使用`tools`参数定义工具，格式略有不同
- 支持`tool_use`和`tool_result`内容块
- 内置Computer Use能力：直接操作鼠标键盘、截屏
- 支持并行工具调用
- `tool_choice`支持`auto`、`any`、`tool`三种模式

### 其他平台

- **Google Gemini**：支持Function Calling和Code Execution
- **开源模型**：通过微调或提示工程实现（如Gorilla、ToolLLaMA）
- **OpenAI兼容接口**：许多开源推理框架（vLLM、Ollama）实现了兼容的Function Calling协议

## 工具描述与JSON Schema

工具描述的质量直接影响LLM调用工具的准确性。

### 描述最佳实践

- **函数名**：使用动词+名词格式，清晰表达功能（如`get_weather`、`search_documents`）
- **描述**：简洁说明功能、适用场景和限制条件
- **参数**：明确类型、必填性、取值范围、默认值
- **示例**：在描述中提供典型用例

### JSON Schema规范

```json
{
  "type": "function",
  "function": {
    "name": "get_stock_price",
    "description": "查询指定股票的实时价格。仅支持A股和港股。",
    "parameters": {
      "type": "object",
      "properties": {
        "symbol": {
          "type": "string",
          "description": "股票代码，如 '600519' 或 '00700'"
        },
        "market": {
          "type": "string",
          "enum": ["A股", "港股"],
          "description": "市场类型"
        }
      },
      "required": ["symbol"]
    }
  }
}
```

### 常见陷阱

- 描述过于模糊导致模型错误调用
- 参数类型定义不严格导致格式错误
- 缺少边界条件说明导致异常输入
- 工具数量过多导致选择困难（建议不超过20个）

## 工具选择与编排

### 单步选择

- 模型根据用户意图从工具列表中选择最匹配的工具
- 可通过`tool_choice`强制调用特定工具
- 使用系统提示引导工具选择策略

### 多步编排

复杂任务需要多个工具按序或并行调用。

- **顺序执行**：前一步结果作为后一步输入（如先搜索再总结）
- **并行执行**：独立任务同时执行（如同时查询天气和新闻）
- **条件分支**：根据中间结果决定下一步操作
- **循环执行**：反复调用直到满足终止条件

### 编排框架

- **LangChain**：提供AgentExecutor、LCEL等编排机制
- **Semantic Kernel**：微软的AI编排框架，支持插件化工具
- **Haystack**：面向RAG的Pipeline编排
- **自定义循环**：简单的while循环 + 状态管理

## MCP协议（Model Context Protocol）

Anthropic于2024年推出的开放标准协议，旨在统一LLM与外部工具/数据源的连接方式。

### 核心概念

- **MCP Server**：暴露工具和资源的服务端
- **MCP Client**：集成在LLM应用中的客户端
- **Transport**：通信层，支持stdio和HTTP SSE两种方式
- **Resources**：服务器提供的可读数据源
- **Tools**：服务器提供的可调用函数
- **Prompts**：服务器提供的预定义提示模板

### 与Function Calling的区别

| 维度 | Function Calling | MCP |
|------|-----------------|-----|
| 集成方式 | 每个API单独集成 | 标准化协议 |
| 工具发现 | 手动定义 | 动态发现 |
| 生态 | 封闭 | 开放互操作 |
| 状态管理 | 无状态 | 支持有状态会话 |

### 实际应用

- 文件系统访问（读写本地文件）
- 数据库查询（SQL/NoSQL）
- API集成（GitHub、Slack、Jira等）
- 浏览器自动化
- 开发工具（IDE集成、代码执行）

## 安全与权限控制

工具使用引入了LLM与外部系统的交互，安全风险显著增加。

### 主要风险

- **提示注入攻击**：恶意输入诱导模型调用危险工具
- **过度授权**：工具权限过大，模型可能执行非预期操作
- **数据泄露**：工具返回的敏感信息被包含在模型输出中
- **间接注入**：外部数据源中嵌入的恶意指令

### 防护措施

- **最小权限原则**：工具只暴露必要的功能和数据
- **用户确认机制**：敏感操作前要求用户显式确认
- **输入验证**：对LLM生成的参数进行严格校验
- **沙箱执行**：代码执行在隔离环境中进行
- **审计日志**：记录所有工具调用行为
- **速率限制**：防止模型大量调用工具
- **输出过滤**：对工具返回结果进行脱敏处理

### 实践建议

1. 对工具按风险等级分类管理
2. 高风险工具（如文件删除、资金操作）必须人工确认
3. 定期审查工具调用日志
4. 为每个工具设置超时和重试策略
5. 在工具描述中明确说明安全约束
