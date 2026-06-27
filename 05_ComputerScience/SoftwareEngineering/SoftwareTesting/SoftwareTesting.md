---
aliases: [SoftwareTesting]
tags: ['SoftwareEngineering', 'SoftwareTesting', 'SoftwareTesting']
created: 2026-05-16
updated: 2026-05-16
---

# 软件测试

## 一、测试基础

### 验证 vs 确认

| 概念 | 英文 | 含义 |
|------|------|------|
| 验证（Verification） | Are we building the product right? | 确保实现符合规格 |
| 确认（Validation） | Are we building the right product? | 确保满足用户需求 |

### QA vs 测试

| QA | 测试 |
|----|------|
| 过程导向 | 产品导向 |
| 预防缺陷 | 发现缺陷 |
| 全流程活动 | 特定阶段活动 |
| 建立标准和方法 | 执行测试用例 |

### 测试级别

```
单元测试 (Unit) → 集成测试 (Integration) → 系统测试 (System) → 验收测试 (Acceptance)
```

| 级别 | 范围 | 执行者 | 频次 |
|------|------|--------|------|
| 单元测试 | 单个模块/函数 | 开发者 | 每次提交 |
| 集成测试 | 模块间交互 | 开发者 | 每日 |
| 系统测试 | 完整系统 | QA | 每次构建 |
| 验收测试 | 用户场景 | QA/客户 | 发布前 |

## 二、测试类型

| 类型 | 子类型 | 目的 | 技术 |
|------|--------|------|------|
| 功能测试 | 黑盒/白盒/灰盒 | 验证功能正确性 | 等价类、边界值 |
| 性能测试 | 负载/压力/耐久 | 评估系统性能 | 基准测试、分析 |
| 安全测试 | 渗透/漏洞扫描 | 发现安全缺陷 | OWASP 方法论 |
| 可用性测试 | 用户调研 | 评估用户体验 | 用户观察 |
| 可靠性测试 | 恢复/容错 | 验证稳定性 | 故障注入 |
| 兼容性测试 | 浏览器/设备 | 验证环境适配 | 矩阵测试 |

## 三、黑盒测试技术

### 等价类划分

将输入域划分为若干等价类，从每个等价类选取代表值进行测试。

```python
# 年龄输入验证：1-120 为有效
def test_age():
    valid = [1, 50, 120]           # 有效等价类
    invalid_low = [0, -1, -100]     # 无效（低于下限）
    invalid_high = [121, 200]       # 无效（高于上限）
```

### 边界值分析

在等价类的边界处选取测试值，发现边界缺陷。

$$BVA: min, min+1, max-1, max, min-1, max+1$$

示例（1-120）：

| 边界 | 值 |
|------|-----|
| 最小值 | 0（无效）, 1（有效） |
| 最大值 | 120（有效）, 121（无效） |
| 内部 | 2, 119 |

### 决策表测试

适用于多条件组合的场景，列出所有条件及其组合下的动作。

| 规则 | 条件1 (登录) | 条件2 (权限) | 条件3 (状态) | 结果 |
|------|------------|-------------|-------------|------|
| 1 | Y | Y | Y | 允许 |
| 2 | Y | Y | N | 拒绝 |
| 3 | Y | N | Y | 拒绝 |
| 4 | N | — | — | 拒绝 |

### 状态转换测试

适用于状态机驱动的系统，测试状态间的合法和非法转换。

### 成对测试（Pairwise Testing）

使用组合测试技术以最少的用例覆盖所有参数对的组合，显著减少测试用例数量。

## 四、白盒测试技术

### 覆盖率指标

$$DC = \frac{\text{number of conditions exercised}}{\text{total conditions}}$$

| 覆盖率类型 | 定义 | 强度 |
|-----------|------|------|
| 语句覆盖 | 每个语句至少执行一次 | 最低 |
| 分支覆盖 | 每个分支（true/false）至少执行一次 | 中 |
| 条件覆盖 | 每个条件的 true/false 至少一次 | 中高 |
| 路径覆盖 | 所有独立路径至少执行一次 | 高（可能无限） |
| MC/DC | 每个条件独立影响决策结果 | 航空安全标准 |

### MC/DC

MC/DC（Modified Condition/Decision Coverage）要求每个条件都能独立影响决策结果。

条件数 $n$ 所需的 MC/DC 测试用例数：$n + 1$

## 五、单元测试框架

### xUnit 架构

| 组件 | 作用 |
|------|------|
| TestCase | 单个测试类 |
| TestSuite | 测试用例集合 |
| TestRunner | 执行测试框架 |
| TestFixture | 测试前置/后置条件 |
| Assertions | 断言验证结果 |

### 各语言框架

| 语言 | 框架 | 断言示例 |
|------|------|---------|
| Java | JUnit 5 | `assertEquals(expected, actual)` |
| Python | pytest | `assert actual == expected` |
| C# | NUnit | `Assert.That(actual, Is.EqualTo(expected))` |
| JavaScript | Jest | `expect(actual).toBe(expected)` |
| Go | testing | `t.Errorf("got %v, want %v", got, want)` |

```python
# pytest 示例
import pytest

def test_addition():
    assert add(2, 3) == 5
    assert add(-1, 1) == 0

@pytest.mark.parametrize("a,b,expected", [
    (2, 3, 5), (-1, 1, 0), (0, 0, 0)
])
def test_add_param(a, b, expected):
    assert add(a, b) == expected

class TestMath:
    @pytest.fixture
    def setup(self):
        return {"data": [1, 2, 3]}

    def test_sum(self, setup):
        assert sum(setup["data"]) == 6
```

## 六、测试替身

| 类型 | 英文 | 说明 | 适用场景 |
|------|------|------|---------|
| 桩对象 | Stub | 返回预设值 | 替代外部依赖 |
| 模拟对象 | Mock | 验证交互行为 | 验证方法是否被调用 |
| 伪造对象 | Fake | 轻量级实现 | 替代数据库、网络 |
| 间谍对象 | Spy | 记录调用信息 | 验证调用次数和参数 |
| 虚拟对象 | Dummy | 占位参数 | 填充参数列表 |

```python
from unittest.mock import Mock, patch

# Mock 示例
mock_db = Mock()
mock_db.get_user.return_value = {"id": 1, "name": "Alice"}

# 验证交互
service = UserService(mock_db)
service.get_user_name(1)
mock_db.get_user.assert_called_once_with(1)

# patch 装饰器
@patch('module.ExternalAPI')
def test_api(mock_api):
    mock_api.fetch.return_value = {"status": "ok"}
    result = my_function()
    assert result == "ok"
```

## 七、TDD（测试驱动开发）

### 红-绿-重构循环

```
编写失败测试（红） → 编写最少代码通过（绿） → 重构代码（重构）
```

| 步骤 | 行为 | 目标 |
|------|------|------|
| 红 | 先写一个失败的测试 | 明确需求 |
| 绿 | 用最简代码让测试通过 | 快速实现 |
| 重构 | 优化代码质量 | 保持整洁 |

### 原则

- **先写测试，再写代码**
- **测试决定接口设计**：驱动更清晰、可测试的接口
- **小步迭代**：每次只增加一个小功能
- **测试是文档**：测试用例就是可执行的规格说明

### 挑战

| 挑战 | 缓解策略 |
|------|---------|
| 前期投入大 | 长期看节省调试时间 |
| 不适合探索性开发 | 原型阶段后引入 |
| 测试维护成本 | 保持测试简洁 |
| UI 测试脆弱 | 分层测试，UI 层少测 |

## 八、集成测试

### 策略对比

| 策略 | 方法 | 优点 | 缺点 |
|------|------|------|------|
| 大爆炸 | 一次性集成所有模块 | 简单 | 问题定位困难 |
| 自顶向下 | 从顶层向下集成 | 早期验证架构 | 底层模块 Mock 多 |
| 自底向上 | 从底层向上集成 | 底层验证充分 | 延迟验证顶层 |
| 三明治 | 上+下同时集成 | 并行度高 | 管理复杂 |

### 契约测试（Contract Testing）

服务间通过消费者驱动的契约（Consumer-Driven Contracts）验证接口兼容性。工具：Pact、Spring Cloud Contract。

## 九、端到端测试

| 工具 | 语言 | 适用场景 | 特点 |
|------|------|---------|------|
| Selenium WebDriver | 多语言 | Web 端到端 | 标准协议，慢 |
| Cypress | JavaScript | 现代 Web 应用 | 快，开发者友好 |
| Playwright | JS/Python/Java | 跨浏览器 | 现代，自动等待 |
| Appium | 多语言 | 移动端 | 跨平台 |

```javascript
// Playwright 示例
const { test, expect } = require('@playwright/test');

test('search functionality', async ({ page }) => {
    await page.goto('https://example.com');
    await page.fill('#search', 'test automation');
    await page.click('#search-btn');
    await expect(page.locator('.result')).toHaveCount(10);
});
```

## 十、CI/CD 集成

```yaml
# GitHub Actions 示例
name: Test
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
      - run: pip install -r requirements.txt
      - run: pytest --cov --junitxml=report.xml
      - uses: dorny/test-reporter@v1
```

**测试金字塔**：

```
        /\
       /E2E\
      /      \
     /Integration\
    /              \
   / Unit Test      \
  /__________________\
```

- 单元测试：70-80%，快速可靠
- 集成测试：15-20%，验证交互
- E2E 测试：5-10%，关键路径

## 十一、测试管理

| 工件 | 内容 |
|------|------|
| 测试计划 | 范围、策略、资源、进度 |
| 测试用例 | ID、描述、前置条件、步骤、预期结果 |
| 缺陷报告 | 标题、环境、复现步骤、严重级别 |
| 可追溯性矩阵 | 需求 ↔ 测试用例 ↔ 缺陷映射 |
| 测试报告 | 执行概要、通过率、覆盖率、风险 |

## 相关条目

- UnitTesting
- IntegrationTesting
- CI_CD
- TestAutomation

## 参考资源

- 《Software Testing》（Ron Patton）
- 《ISTQB 认证大纲》
- [OWASP Testing Guide](https://owasp.org/www-project-web-security-testing-guide/)
- [pytest 文档](https://docs.pytest.org/)
- 《xUnit Test Patterns》（Gerard Meszaros）
- [Google Testing Blog](https://testing.googleblog.com/)

