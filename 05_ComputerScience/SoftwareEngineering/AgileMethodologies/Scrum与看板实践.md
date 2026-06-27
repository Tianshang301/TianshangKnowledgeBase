---
aliases: [Scrum 与看板实践]
tags: ['SoftwareEngineering', 'AgileMethodologies', 'Scrum 与看板实践']
---

# Scrum 与看板实践

## 一、敏捷开发概述

敏捷开发是2001年敏捷宣言发布后兴起的软件开发方法论。

敏捷宣言四大价值观：

```
1. 个体和互动 > 流程和工具
2. 可工作的软件 > 详尽的文档
3. 客户合作 > 合同谈判
4. 响应变化 > 遵循计划
```

敏捷原则（12条）：

```
1. 最优先的是通过尽早和持续交付有价值的软件来满足客户
2. 欢迎不断变化的需求
3. 频繁交付可工作的软件（几周或几个月）
4. 业务人员与开发人员日常合作
5. 围绕有积极性的个体构建项目
6. 面对面交谈是最有效的沟通方式
7. 可工作的软件是进度的主要衡量标准
8. 提倡可持续的开发速度
9. 持续关注技术卓越和好的设计
10. 简化（最大化不做的工作量）
11. 最好的架构、需求和设计出自自组织团队
12. 团队定期反省如何变得更有效
```

## 二、Scrum 框架

Scrum 是最广泛使用的敏捷框架，强调迭代、增量交付和团队自组织。

Scrum 角色：

| 角色 | 职责 | 关键活动 |
|------|------|----------|
| Product Owner | 管理 Product Backlog, 最大化产品价值 | 优先级排序、需求澄清 |
| Scrum Master | 确保 Scrum 流程正确执行 | 消除障碍、教练引导 |
| Development Team | 自组织、跨职能完成交付 | 估算、开发、测试 |

Scrum 事件：

```
Sprint (2-4周):
  Sprint Planning (规划)
    确定 Sprint Goal
    选择 Backlog Items
  Daily Scrum (15分钟站会)
    昨天做了什么 + 今天做什么 + 有什么障碍
  Sprint Review (评审)
    演示完成的功能，收集反馈
  Sprint Retrospective (回顾)
    什么做得好 + 什么可改进 + 下一步行动
```

用户故事（User Story）格式：

```
作为<角色>, 我希望<功能>, 以便<价值>

Acceptance Criteria:
1. 条件1: ...
2. 条件2: ...
```

## 三、Scrum 工件

Product Backlog 管理：

```python
class ProductBacklog:
    def __init__(self):
        self.items = []
        self.next_id = 1

    def add_item(self, description, value, effort, priority):
        self.items.append({
            'id': self.next_id,
            'description': description,
            'business_value': value,
            'effort': effort,
            'priority': priority,
            'status': 'backlog'
        })
        self.next_id += 1
        self.items.sort(key=lambda x: x['priority'], reverse=True)

    def get_top_n(self, n):
        return self.items[:n]

    def estimate_velocity(self, completed_sprints):
        if not completed_sprints:
            return 0
        return sum(sprint['completed_points']
                   for sprint in completed_sprints) / len(completed_sprints)


backlog = ProductBacklog()
backlog.add_item('用户登录功能', 10, 5, 100)
backlog.add_item('搜索功能', 8, 8, 90)
backlog.add_item('分享功能', 6, 3, 70)
```

Definition of Done（完成的定义）示例：

```
1. 代码已编写并通过 Code Review
2. 单元测试覆盖率达到80%以上
3. 集成测试通过
4. UI/UX 符合设计要求
5. 功能已部署到 Staging 环境
6. 产品负责人已验收
7. 文档已更新
```

## 四、Scrum 估算技术

常用估算方法对比：

| 方法 | 单位 | 精度 | 适用场景 | 耗时 |
|------|------|------|----------|------|
| 故事点 | 相对值 | 中 | 高层规划 | 快 |
| 理想人天 | 时间 | 高 | 详细计划 | 中 |
| T 恤尺寸 | S/M/L/XL | 低 | 快速筛选 | 极快 |
| 亲和估算 | 分组排序 | 中 | 大量 Backlog | 快 |

Planning Poker 流程：

```
1. PO 讲解一个 User Story
2. 团队讨论需求细节
3. 每人选择一张估算牌（Fibonacci 数列: 1,2,3,5,8,13,21）
4. 同时亮牌
5. 差异大者解释原因
6. 重复直到达成一致
```

## 五、看板方法

看板（Kanban）源自丰田生产系统，强调可视化工作流和限制在制品。

看板核心实践：

```
1. 可视化工作流 (Visualize the workflow)
2. 限制在制品 (Limit WIP)
3. 管理流程 (Manage flow)
4. 明确流程规则 (Make process policies explicit)
5. 实施反馈环 (Implement feedback loops)
6. 协作改进 (Improve collaboratively)
```

典型看板板：

```
Backlog | Analysis | Development | Testing | Done
  [ ]       [ ]         [ ]         [ ]      [done]
  [ ]       [ ]         [ ]         [ ]
  [ ]                   [ ]
  [ ]                   [ ]
WIP Limit: 3           2            2
```

## 六、Scrum vs 看板对比

| 维度 | Scrum | 看板 |
|------|-------|------|
| 迭代周期 | 固定时间盒（2-4周）| 持续流动 |
| 角色定义 | PO, SM, Dev Team | 不强制定义 |
| 变更策略 | Sprint 内不允许变更 | 随时可加入新项 |
| 度量指标 | 速度（Velocity）| 前置时间、吞吐量 |
| 在制品限制 | 隐含（Sprint 容量）| 明确的 WIP 限制 |
| 定期会议 | 计划、站会、评审、回顾 | 非强制 |
| 适用场景 | 新功能开发 | 运维、支持型工作 |
| 团队结构 | 固定跨职能团队 | 灵活 |

## 七、Scrum Master 工具

燃尽图（Burndown Chart）追踪：

```python
def generate_burndown(total_points, sprint_days):
    """生成理想燃尽线"""
    ideal_burn_rate = total_points / sprint_days
    burndown = []
    for day in range(sprint_days + 1):
        remaining = total_points - (ideal_burn_rate * day)
        burndown.append(max(0, remaining))
    return burndown


def calculate_actual_burndown(completed_by_day, total_points):
    actual = [total_points]
    for daily_completed in completed_by_day:
        actual.append(max(0, actual[-1] - daily_completed))
    return actual


total_points = 40
sprint_days = 10
ideal = generate_burndown(total_points, sprint_days)
actual = calculate_actual_burndown([3, 5, 4, 6, 3, 4, 5, 4, 3, 3], total_points)

for day in range(sprint_days + 1):
    print(f"Day {day}: Ideal={ideal[day]:.1f}, Actual={actual[day]}")
```

累积流图（Cumulative Flow Diagram）：

| 时间 | 待办 | 进行中 | 完成 |
|------|------|--------|------|
| W1 | 20 | 5 | 0 |
| W2 | 15 | 8 | 7 |
| W3 | 10 | 6 | 14 |
| W4 | 8 | 4 | 22 |

循环时间 = 平均在 WIP 中的天数

前置时间 = 从进入 Backlog 到完成的总时间

## 八、规模化敏捷

规模化敏捷框架：

| 框架 | 适用规模 | 核心概念 | 复杂度 |
|------|----------|----------|--------|
| SAFe | 企业级（50+人）| ARTs, PI Planning | 高 |
| LeSS | 多团队（2-8团队）| 一个 Product Backlog | 中 |
| Scrum@Scale | 任意规模 | Scrum of Scrums | 中 |
| Nexus | 3-9个 Scrum 团队 | Nexus Integration Team | 中 |

SAFe 核心层级：

```
Portfolio Level: 战略投资组合
    |
Program Level: 敏捷发布火车 (ART)
    |
Team Level: Scrum 团队
```

## 九、常见问题与最佳实践

常见反模式：

```
1. Scrum But: 选择性遵守 Scrum 规则
2. 需求瀑布: Sprint 内实际仍用瀑布方式
3. 幽灵 Sprint: 外部干扰导致 Sprint 目标改变
4. 超长 Daily Scrum: 变成问题讨论会
5. PO 缺席: 需求优先级无人决策
6. 无价值度量: 仅关注产出不关注结果
```

改善建议：

| 问题 | 症状 | 解决方法 |
|------|------|----------|
| 估时不准 | 经常延期 | 使用 T shirt size + 历史数据校准 |
| 需求蔓延 | Sprint 目标变化 | 强化 Product Owner 决策权 |
| 团队倦怠 | 加班增多 | 限制 WIP, 可持续节奏 |
| 回顾无效 | 重复问题 | 改变回顾形式, 使用不同议题框架 |

## 相关条目

- [[AgileMethodologies]]
- [[05_ComputerScience/SoftwareEngineering/SoftwareDevelopmentLifecycle/SoftwareDevelopmentLifecycle|SoftwareDevelopmentLifecycle]]
- [[CI-CD 与 DevOps 实践]]
- [[自动化测试框架]]
- [[架构模式与企业应用]]

## 参考资源

1. 《Scrum 指南》Ken Schwaber & Jeff Sutherland 著
2. 《看板方法》David J. Anderson 著
3. 《敏捷软件开发》Robert C. Martin 著
4. SAFe 官网：https://scaledagileframework.com
5. Scrum.org 官方资源：https://www.scrum.org
6. 《用户故事与敏捷方法》Mike Cohn 著
7. Atlassian 敏捷指南：https://www.atlassian.com/agile

