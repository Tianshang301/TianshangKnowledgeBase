---
aliases:
  - 自主检索Agent
  - Agent RAG
  - 自反思RAG
tags:
  - RAG
  - Agent
  - Self-RAG
  - CRAG
  - LangGraph
  - LLM应用
created: 2026-06-27
updated: 2026-06-27
---

# AgenticRAG：自主检索Agent

AgenticRAG将Agent的自主决策能力引入RAG系统，使检索过程不再是固定的pipeline，而是由Agent根据查询动态决定是否检索、如何检索、检索结果是否可用。这种范式通过self-reflection和adaptive策略显著提升了RAG的可靠性和准确性。

## Self-RAG

Self-RAG（Asai et al., 2023）通过训练模型生成特殊的reflection token，实现自我反思式的检索和生成。

### 核心思想

传统RAG对所有查询都执行检索，Self-RAG让模型自己决定：
- **是否需要检索**（Retrieve token）
- **检索内容是否相关**（IsRel token）
- **生成内容是否有检索支持**（IsSup token）
- **生成内容是否有用**（IsUse token）

### Reflection Token体系

| Token | 含义 | 取值 |
|-------|------|------|
| Retrieve | 是否需要检索 | Yes/No |
| IsRel | 检索结果是否与查询相关 | Relevant/Irrelevant |
| IsSup | 生成内容是否被检索支持 | Fully/Partially/No |
| IsUse | 生成内容对用户是否有用 | 5/4/3/2/1 |

### 生成流程

```
用户查询 → 模型判断Retrieve？
    ├─ Retrieve=No → 直接生成答案
    └─ Retrieve=Yes → 执行检索
        → 评估IsRel（对每个检索结果）
            ├─ IsRel=Irrelevant → 忽略该结果
            └─ IsRel=Relevant → 用于生成
                → 生成候选答案
                    → 评估IsSup（答案是否有检索支持）
                    → 评估IsUse（答案是否有用）
                        → 选择最优答案
```

### 实现示例

```python
class SelfRAG:
    def __init__(self, llm, retriever):
        self.llm = llm
        self.retriever = retriever
    
    def generate(self, query):
        # 判断是否需要检索
        retrieve_decision = self.llm.generate(
            f"问题：{query}\n需要检索外部信息吗？回答Yes或No。"
        )
        
        if "Yes" in retrieve_decision:
            # 执行检索
            docs = self.retriever.retrieve(query)
            
            # 评估相关性
            relevant_docs = []
            for doc in docs:
                relevance = self.llm.generate(
                    f"问题：{query}\n文档：{doc}\n该文档与问题相关吗？回答Relevant或Irrelevant。"
                )
                if "Relevant" in relevance:
                    relevant_docs.append(doc)
            
            if relevant_docs:
                # 基于相关文档生成答案
                context = "\n".join(relevant_docs)
                answer = self.llm.generate(f"基于以下信息回答问题。\n{context}\n问题：{query}")
                
                # 评估支持度
                support = self.llm.generate(
                    f"问题：{query}\n答案：{answer}\n信息：{context}\n答案被信息充分支持吗？"
                )
                return answer, support
        
        # 无需检索或无相关文档，直接生成
        return self.llm.generate(query), None
```

### 训练方法

- **数据标注**：为训练数据标注reflection token
- **多任务训练**：同时训练生成和reflection任务
- **奖励模型**：使用reward model优化IsUse判断

## CRAG（Corrective RAG）

CRAG（Corrective RAG）通过检索质量评估和纠正机制，动态调整检索策略。

### 核心组件

```
用户查询 → 检索器 → 检索结果
              ↓
        检索质量评估器（轻量级模型）
              ↓
    ┌─────────┼─────────┐
    Correct   Ambiguous  Incorrect
    ↓         ↓         ↓
  精炼知识   保留原结果   Web搜索补充
    ↓         ↓         ↓
        知识融合 → 答案生成
```

### 检索质量评估

```python
class CRAGRetrievalEvaluator:
    def __init__(self, model):
        self.model = model  # 轻量级分类模型
    
    def evaluate(self, query, retrieved_doc):
        """评估检索结果质量：Correct/Ambiguous/Incorrect"""
        score = self.model.predict(query, retrieved_doc)
        if score > 0.8:
            return "Correct"
        elif score > 0.4:
            return "Ambiguous"
        else:
            return "Incorrect"
```

### 知识精炼

当检索结果被评为Correct时，进一步精炼去除噪声：

```python
def refine_knowledge(documents):
    """将文档分解为知识条目，过滤无关信息"""
    knowledge_items = []
    for doc in documents:
        items = decompose_to_items(doc)  # LLM分解
        for item in items:
            if is_relevant(item):  # 相关性过滤
                knowledge_items.append(item)
    return knowledge_items
```

### Web搜索回退

当本地检索结果为Incorrect时，转向Web搜索：

```python
def corrective_retrieval(query, local_docs, evaluator):
    status = evaluator.evaluate(query, local_docs[0])
    
    if status == "Correct":
        return refine_knowledge(local_docs)
    elif status == "Ambiguous":
        return local_docs  # 保留原结果
    else:
        # Web搜索补充
        web_results = web_search(query)
        return web_results
```

## Adaptive RAG

Adaptive RAG根据查询复杂度动态选择检索策略，避免对简单查询过度检索。

### 查询复杂度分类

```python
class QueryComplexityClassifier:
    """将查询分为三类复杂度"""
    
    CATEGORIES = {
        "direct": "简单事实性问题，无需检索",
        "single_retrieval": "需要一次检索的中等复杂度问题",
        "multi_step": "需要多步推理的复杂问题"
    }
    
    def classify(self, query):
        prompt = f"""判断以下查询的复杂度类别：
        - direct：简单事实，如"法国首都是哪里"
        - single_retrieval：需要查询外部信息，如"某论文的主要贡献"
        - multi_step：需要多步推理，如"比较A和B的优缺点"
        
        查询：{query}
        类别："""
        return llm.generate(prompt)
```

### 路由策略

```python
def adaptive_rag(query, classifier, direct_llm, single_retriever, multi_step_agent):
    complexity = classifier.classify(query)
    
    if complexity == "direct":
        return direct_llm.generate(query)
    elif complexity == "single_retrieval":
        docs = single_retriever.retrieve(query)
        return generate_with_context(query, docs)
    else:
        return multi_step_agent.execute(query)
```

## Multi-step Reasoning（多步推理）

### 迭代检索

```
查询 → 初始检索 → 初始答案
        ↓
    是否需要更多信息？
        ↓ Yes
    生成新查询 → 再次检索 → 更新答案
        ↓
    重复直到满足条件
```

### IRCoT（Interleaving Retrieval with Chain-of-Thought）

IRCoT将Chain-of-Thought推理与检索交替进行：

```python
def ircot(query, retriever, llm, max_steps=5):
    thought = query
    all_context = []
    
    for step in range(max_steps):
        # 检索与当前推理相关的文档
        docs = retriever.retrieve(thought)
        all_context.extend(docs)
        
        # 生成下一步推理
        thought = llm.generate(f"""
        问题：{query}
        已有信息：{format_context(all_context)}
        当前推理：{thought}
        
        基于新信息，继续推理。如果信息足够，给出最终答案。
        """)
        
        if is_final_answer(thought):
            break
    
    return thought
```

### Chain-of-Thought与检索结合

```python
def cot_with_retrieval(query, retriever, llm):
    # 步骤1：生成推理计划
    plan = llm.generate(f"为回答以下问题，列出需要的推理步骤：{query}")
    
    # 步骤2：逐步执行，每步检索
    context = []
    for step in parse_steps(plan):
        step_docs = retriever.retrieve(step)
        context.extend(step_docs)
    
    # 步骤3：基于所有信息生成答案
    return llm.generate(f"基于以下信息回答问题。\n{format_context(context)}\n问题：{query}")
```

## Active Learning（主动学习）

### 不确定性查询生成

当模型对答案不确定时，主动生成澄清查询：

```python
def uncertainty_driven_retrieval(query, llm, retriever):
    # 生成初步答案
    initial_answer, uncertainty = llm.generate_with_uncertainty(query)
    
    if uncertainty > threshold:
        # 生成针对性查询
        clarification_query = llm.generate(
            f"问题：{query}\n初步答案：{initial_answer}\n"
            f"为降低不确定性，需要检索什么信息？"
        )
        additional_docs = retriever.retrieve(clarification_query)
        return generate_with_context(query, additional_docs)
    
    return initial_answer
```

### Human-in-the-Loop

```python
def human_in_the_loop_rag(query, retriever, llm, confidence_threshold=0.8):
    docs = retriever.retrieve(query)
    answer, confidence = llm.generate_with_confidence(query, docs)
    
    if confidence < confidence_threshold:
        # 低置信度，请求人工确认
        return {
            "answer": answer,
            "confidence": confidence,
            "needs_review": True,
            "suggested_docs": docs
        }
    
    return {"answer": answer, "confidence": confidence, "needs_review": False}
```

## 实现框架

### LangGraph工作流

```python
from langgraph.graph import StateGraph, END

class RAGState(TypedDict):
    query: str
    complexity: str
    documents: list
    answer: str

def classify_query(state: RAGState):
    complexity = classify(state["query"])
    return {"complexity": complexity}

def retrieve(state: RAGState):
    docs = retriever.retrieve(state["query"])
    return {"documents": docs}

def generate(state: RAGState):
    answer = llm.generate(state["query"], state["documents"])
    return {"answer": answer}

# 构建工作流
workflow = StateGraph(RAGState)
workflow.add_node("classify", classify_query)
workflow.add_node("retrieve", retrieve)
workflow.add_node("generate", generate)

workflow.add_conditional_edges(
    "classify",
    lambda state: state["complexity"],
    {
        "direct": "generate",
        "single_retrieval": "retrieve",
        "multi_step": "retrieve"
    }
)
workflow.add_edge("retrieve", "generate")
workflow.add_edge("generate", END)

graph = workflow.compile()
```

### LlamaIndex Query Pipeline

```python
from llama_index.core.query_pipeline import QueryPipeline

# 定义pipeline组件
retriever_component = RetrieverComponent(retriever)
reranker_component = RerankerComponent(reranker)
generator_component = GeneratorComponent(llm)

# 组装pipeline
pipeline = QueryPipeline(chain=[
    retriever_component,
    reranker_component,
    generator_component
])
```

## 评估指标

### 检索质量指标

- **Context Precision（上下文精确度）**：检索结果中相关内容的比例
- **Context Recall（上下文召回）**：相关内容被检索到的比例

### 生成质量指标

- **Faithfulness（忠实度）**：答案是否基于检索内容，无幻觉
- **Answer Relevancy（答案相关性）**：答案是否回答了用户问题

### Agent特有指标

- **Decision Accuracy（决策准确度）**：是否正确判断是否需要检索
- **Retrieval Efficiency（检索效率）**：是否以最少检索次数获得足够信息
- **Recovery Rate（纠正率）**：检索失败后成功纠正的比例

```python
from ragas import evaluate
from ragas.metrics import faithfulness, answer_relevancy, context_precision, context_recall

result = evaluate(
    dataset=eval_dataset,
    metrics=[faithfulness, answer_relevancy, context_precision, context_recall],
)
```

## 最佳实践

1. **渐进式引入**：先实现基础RAG，再逐步引入Agent能力
2. **成本控制**：Self-RAG和CRAG会增加LLM调用次数，需要评估成本
3. **fallback机制**：Agent决策失败时回退到简单策略
4. **评估驱动**：建立完整的评估基准，量化Agent带来的改进
5. **监控与日志**：记录Agent的每步决策，便于调试和优化