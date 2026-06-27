---
aliases:
  - AI Agent框架
  - 智能体框架
  - LLM Agent
tags:
  - AI Agent
  - LangChain
  - LlamaIndex
  - 多智能体
  - 工具调用
created: 2026-06-27
updated: 2026-06-27
---

# AI Agent框架

AI Agent（智能体）是以大语言模型为核心，具备自主规划、工具调用、记忆存储和反思能力的智能系统。Agent能够将复杂任务分解为子任务，选择合适的工具执行，并根据结果调整策略，是LLM从"对话"走向"行动"的关键技术。

## Agent架构模式

### ReAct（Reasoning + Acting）

ReAct是最经典的Agent架构，交替进行推理和行动：

- **流程**：Thought → Action → Observation → Thought → ...
- **优势**：推理过程透明、可解释性强
- **局限**：串行执行、效率较低

```
Question: 北京今天天气怎么样？
Thought: 我需要查询北京今天的天气信息
Action: search_weather(city="北京", date="today")
Observation: 北京今天晴，气温25-32℃
Thought: 我已经获得了天气信息
Answer: 北京今天晴天，气温25到32摄氏度。
```

### Plan-and-Execute

先制定计划，再逐步执行：

- **Planner**：分析任务，制定执行计划
- **Executor**：按计划执行具体步骤
- **Re-planner**：根据执行结果调整计划

- **优势**：适合复杂任务、全局视野
- **局限**：初始计划可能不准确

### Reflection（反思）

在执行后进行自我反思和改进：

- **流程**：生成 → 评估 → 反思 → 改进
- **变体**：
  - Reflexion：带自我反思的强化学习
  - Self-Refine：迭代自我优化
  - Tree of Thoughts：树状搜索和评估

### LATS（Language Agent Tree Search）

结合蒙特卡洛树搜索的Agent架构：

- **特点**：树状搜索、回溯探索、价值评估
- **适用**：需要多步推理的复杂任务

## LangChain/LangGraph

### LangChain

LangChain是最流行的LLM应用开发框架：

**核心组件**：
- **Models**：支持多种LLM和Embedding模型
- **Prompts**：提示词模板管理
- **Chains**：组件的线性组合
- **Agents**：带工具调用的智能体
- **Memory**：对话历史管理
- **Retrievers**：文档检索集成

```python
from langchain.agents import AgentExecutor, create_react_agent
from langchain_openai import ChatOpenAI
from langchain.tools import Tool

llm = ChatOpenAI(model="gpt-4")
tools = [
    Tool(name="Search", func=search_func, description="搜索信息"),
    Tool(name="Calculator", func=calc_func, description="数学计算"),
]
agent = create_react_agent(llm, tools, prompt)
executor = AgentExecutor(agent=agent, tools=tools)
result = executor.invoke({"input": "北京的人口是多少？"})
```

### LangGraph

LangGraph是LangChain的图编排扩展：

- **核心概念**：
  - State：共享状态
  - Node：执行单元
  - Edge：节点间的转移逻辑
  - Conditional Edge：条件转移

- **优势**：
  - 支持循环和分支
  - 状态管理和持久化
  - 可视化执行流程
  - 人机协作支持

```python
from langgraph.graph import StateGraph, END

workflow = StateGraph(AgentState)
workflow.add_node("agent", agent_node)
workflow.add_node("tools", tool_node)
workflow.add_edge("agent", "tools")
workflow.add_conditional_edges("tools", should_continue)
workflow.set_entry_point("agent")
app = workflow.compile()
```

## LlamaIndex

LlamaIndex专注于数据连接和检索增强：

### 核心能力

- **数据连接器**：支持150+数据源
- **索引结构**：Vector、Tree、Keyword、Knowledge Graph
- **查询引擎**：自然语言查询接口
- **Agent框架**：ReActAgent、FunctionAgent

### 与LangChain对比

| 特性 | LangChain | LlamaIndex |
|------|-----------|------------|
| 核心定位 | 通用LLM应用框架 | 数据索引和检索 |
| 数据处理 | 基础支持 | 强大支持 |
| Agent能力 | 成熟完善 | 快速发展 |
| 学习曲线 | 较陡 | 较平缓 |

```python
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader

documents = SimpleDirectoryReader("./data").load_data()
index = VectorStoreIndex.from_documents(documents)
query_engine = index.as_query_engine()
response = query_engine.query("这个文档的主要内容是什么？")
```

## AutoGen/CrewAI

### AutoGen

微软开源的多Agent对话框架：

- **核心概念**：
  - AssistantAgent：AI助手
  - UserProxyAgent：用户代理
  - GroupChat：多Agent群聊

- **特点**：
  - 灵活的对话模式
  - 代码执行能力
  - 人机协作支持

```python
from autogen import AssistantAgent, UserProxyAgent

assistant = AssistantAgent("assistant", llm_config=llm_config)
user_proxy = UserProxyAgent("user_proxy", code_execution_config={"work_dir": "coding"})
user_proxy.initiate_chat(assistant, message="帮我写一个快速排序算法")
```

### CrewAI

专注于角色扮演的多Agent框架：

- **核心概念**：
  - Agent：具有角色、目标、背景的智能体
  - Task：具体任务定义
  - Crew：Agent团队
  - Process：执行流程（Sequential、Hierarchical）

- **特点**：
  - 角色扮演增强
  - 任务委派机制
  - 简洁的API设计

```python
from crewai import Agent, Task, Crew

researcher = Agent(role="研究员", goal="收集信息", backstory="资深分析师")
writer = Agent(role="作家", goal="撰写报告", backstory="专业写手")

research_task = Task(description="研究AI趋势", agent=researcher)
write_task = Task(description="撰写研究报告", agent=writer)

crew = Crew(agents=[researcher, writer], tasks=[research_task, write_task])
result = crew.kickoff()
```

## 工具调用（Function Calling / Tool Use）

### Function Calling

LLM调用外部函数的标准机制：

- **流程**：
  1. 定义函数schema（名称、参数、描述）
  2. 用户输入触发函数调用决策
  3. LLM输出函数调用参数
  4. 执行函数并返回结果
  5. LLM基于结果生成最终回答

```python
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "获取指定城市的天气",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {"type": "string", "description": "城市名"}
                },
                "required": ["city"]
            }
        }
    }
]
response = client.chat.completions.create(
    model="gpt-4",
    messages=[{"role": "user", "content": "北京天气怎么样？"}],
    tools=tools
)
```

### 工具设计原则

- **单一职责**：每个工具只做一件事
- **清晰描述**：工具描述要准确、无歧义
- **参数校验**：输入验证和错误处理
- **幂等性**：相同输入产生相同结果

### 常用工具类型

- **信息检索**：搜索引擎、知识库查询
- **数据处理**：计算、格式转换、数据分析
- **外部交互**：API调用、数据库操作、文件读写
- **代码执行**：Python、SQL、Shell执行

## 多Agent协作模式

### 协作架构

- **中心化**：一个Orchestrator协调多个Worker
- **去中心化**：Agent之间平等协作
- **层级化**：多层级的管理和执行关系

### 通信模式

- **直接通信**：Agent之间直接传递消息
- **共享黑板**：通过共享状态交换信息
- **消息队列**：异步消息传递

### 协作策略

- **分工协作**：不同Agent负责不同子任务
- **辩论模式**：多个Agent辩论得出结论
- **投票决策**：多个Agent投票选择方案
- **专家咨询**：向特定领域的Agent咨询

## Agent记忆系统

### 短期记忆（Working Memory）

- **内容**：当前对话上下文、任务状态
- **实现**：对话历史、状态变量
- **管理**：滑动窗口、摘要压缩

### 长期记忆（Long-term Memory）

- **内容**：历史对话、用户偏好、知识积累
- **实现**：向量数据库、关系数据库
- **检索**：基于相关性、时间衰减

### 情景记忆（Episodic Memory）

- **内容**：过往任务经验和解决方案
- **用途**：类似任务快速解决
- **实现**：经验存储和检索

### 程序记忆（Procedural Memory）

- **内容**：工具使用方法、操作流程
- **用途**：技能执行和优化
- **实现**：工具文档、执行历史

```python
# 记忆系统示例
class AgentMemory:
    def __init__(self):
        self.short_term = ConversationBufferMemory()
        self.long_term = VectorStoreMemory(vector_store)
        self.episodic = EpisodicMemory()
    
    def store(self, content, memory_type):
        if memory_type == "short":
            self.short_term.add(content)
        elif memory_type == "long":
            self.long_term.add(content)
    
    def retrieve(self, query, k=5):
        short_results = self.short_term.search(query)
        long_results = self.long_term.search(query, k=k)
        return combine_results(short_results, long_results)
```

## Agent评估与可观测性

### 评估维度

- **任务完成率**：Agent是否成功完成任务
- **执行效率**：完成任务的步骤数、时间、成本
- **输出质量**：结果的准确性、完整性、相关性
- **工具使用**：工具选择是否合理、调用是否正确

### 评估方法

- **基准测试**：标准任务集评估
- **A/B测试**：对比不同Agent策略
- **人工评估**：输出质量人工打分
- **自动评估**：使用LLM自动评估

### 可观测性

- **执行追踪**：记录Agent的每一步决策和行动
- **状态监控**：实时监控Agent状态和资源使用
- **日志记录**：详细的执行日志用于调试
- **可视化**：执行流程的可视化展示

### 监控工具

- **LangSmith**：LangChain官方的追踪平台
- **Phoenix**：开源的LLM可观测性工具
- **Weights & Biases**：实验追踪和可视化

## 最佳实践

1. **明确目标**：清晰定义Agent的任务范围和能力边界
2. **工具精简**：只提供必要的工具，避免工具过多导致选择困难
3. **错误处理**：优雅处理工具调用失败、超时等异常
4. **人机协作**：关键决策点引入人类审核
5. **持续优化**：基于反馈不断优化Agent策略
6. **安全控制**：限制Agent的权限范围，防止意外操作

## 总结

AI Agent框架正在快速发展，从简单的ReAct架构向更复杂的多Agent协作系统演进。选择合适的框架和架构模式，需要根据具体任务需求、性能要求和开发成本综合考虑。随着技术成熟，Agent将在更多领域替代或增强人类工作，成为AI应用的核心形态。
