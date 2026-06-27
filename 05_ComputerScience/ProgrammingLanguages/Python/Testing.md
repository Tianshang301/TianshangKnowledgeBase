---
aliases: [Testing]
tags: ['ProgrammingLanguages', 'Python', 'Testing']
created: 2026-05-16
updated: 2026-05-13
---

# Python 测试指南

## 一、unittest 标准库

### TestCase 基础

```python
import unittest
from typing import List, Optional

class Calculator:
    def add(self, a, b):
        return a + b
    
    def divide(self, a, b):
        if b == 0:
            raise ValueError("除数不能为0")
        return a / b
    
    def is_prime(self, n: int) -> bool:
        if n < 2:
            return False
        for i in range(2, int(n ** 0.5) + 1):
            if n % i == 0:
                return False
        return True

class TestCalculator(unittest.TestCase):
    def setUp(self):
        """每个测试方法前执行"""
        self.calc = Calculator()
    
    def tearDown(self):
        """每个测试方法后执行"""
        pass
    
    def test_add(self):
        self.assertEqual(self.calc.add(3, 5), 8)
        self.assertEqual(self.calc.add(-1, 1), 0)
        self.assertEqual(self.calc.add(0, 0), 0)
    
    def test_divide(self):
        self.assertEqual(self.calc.divide(10, 2), 5)
        self.assertAlmostEqual(self.calc.divide(1, 3), 0.3333, places=4)
    
    def test_divide_by_zero(self):
        with self.assertRaises(ValueError):
            self.calc.divide(10, 0)
    
    def test_is_prime(self):
        self.assertTrue(self.calc.is_prime(7))
        self.assertTrue(self.calc.is_prime(2))
        self.assertFalse(self.calc.is_prime(1))
        self.assertFalse(self.calc.is_prime(4))
        self.assertFalse(self.calc.is_prime(0))

# 运行测试
if __name__ == "__main__":
    unittest.main()
```

### 常用断言

```python
class TestAssertions(unittest.TestCase):
    def test_assertions(self):
        self.assertEqual(a, b)        # a == b
        self.assertNotEqual(a, b)     # a != b
        self.assertTrue(x)            # bool(x) is True
        self.assertFalse(x)           # bool(x) is False
        self.assertIs(a, b)           # a is b
        self.assertIsNot(a, b)        # a is not b
        self.assertIsNone(x)          # x is None
        self.assertIsNotNone(x)       # x is not None
        self.assertIn(a, b)           # a in b
        self.assertNotIn(a, b)        # a not in b
        self.assertIsInstance(a, b)   # isinstance(a, b)
        self.assertNotIsInstance(a, b)
        self.assertAlmostEqual(a, b, places=3)   # 浮点数近似相等
        self.assertRaises(ValueError, func, arg)  # 预期异常
        self.assertWarns(UserWarning, func)       # 预期警告
        self.assertLogs(logger, level)            # 预期日志
```

### setUpClass / tearDownClass

```python
class TestDatabase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """所有测试前执行一次"""
        print("连接数据库")
    
    @classmethod
    def tearDownClass(cls):
        """所有测试后执行一次"""
        print("关闭数据库连接")
    
    def test_query(self):
        pass
```

### TestSuite

```python
def suite():
    suite = unittest.TestSuite()
    suite.addTest(TestCalculator("test_add"))
    suite.addTest(TestCalculator("test_divide"))
    
    # 加载整个测试类
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestCalculator))
    
    # 发现测试
    loader = unittest.TestLoader()
    suite.addTests(loader.discover("tests", pattern="test_*.py"))
    
    return suite

if __name__ == "__main__":
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite())
```

## 二、pytest

### 基础用法

```python
# test_calculator.py (文件名必须以 test_ 开头)
def test_add():
    assert Calculator().add(3, 5) == 8

def test_divide():
    assert Calculator().divide(10, 2) == 5

def test_divide_by_zero():
    import pytest
    with pytest.raises(ValueError):
        Calculator().divide(10, 0)

# 命令行: pytest test_calculator.py -v
# 发现规则: test_*.py 文件中的 test_* 函数
```

### Fixtures

```python
import pytest

@pytest.fixture
def calculator():
    """提供 Calculator 实例"""
    return Calculator()

@pytest.fixture
def sample_data():
    return {"a": 10, "b": 20}

def test_add_with_fixture(calculator, sample_data):
    result = calculator.add(sample_data["a"], sample_data["b"])
    assert result == 30

# Fixture 作用域
@pytest.fixture(scope="module")  # module, class, function, session
def database():
    print("设置数据库")
    db = {"connected": True}
    yield db  # yield 之前是 setUp, 之后是 tearDown
    print("关闭数据库")
    db["connected"] = False

# Fixture 自动使用
@pytest.fixture(autouse=True)
def setup_teardown():
    print("每个测试前执行")
    yield
    print("每个测试后执行")
```

### conftest.py

```python
# conftest.py (放在测试目录下, pytest 自动加载)
import pytest

@pytest.fixture
def api_client():
    """提供 API 测试客户端"""
    class Client:
        def get(self, url):
            return {"status": 200, "data": "ok"}
        def post(self, url, data):
            return {"status": 201, "id": 1}
    return Client()

@pytest.fixture
def auth_token():
    return "test-token-12345"

# 可以在 conftest.py 中定义钩子
def pytest_configure(config):
    config.addinivalue_line("markers", "slow: 慢速测试")
```

### Parametrize

```python
@pytest.mark.parametrize("a,b,expected", [
    (3, 5, 8),
    (-1, 1, 0),
    (0, 0, 0),
    (100, 200, 300),
])
def test_add_parametrize(a, b, expected):
    assert Calculator().add(a, b) == expected

# 多个参数组合
@pytest.mark.parametrize("a", [1, 2])
@pytest.mark.parametrize("b", [3, 4])
def test_cartesian(a, b):
    pass  # 运行: (1,3), (1,4), (2,3), (2,4)
```

### Markers

```python
import pytest

@pytest.mark.slow
def test_heavy_computation():
    import time
    time.sleep(5)
    assert True

@pytest.mark.skip(reason="功能未实现")
def test_not_ready():
    pass

@pytest.mark.skipif(False, reason="条件不满足")
def test_conditional_skip():
    pass

@pytest.mark.xfail
def test_expected_failure():
    assert False  # 预期失败

@pytest.mark.xfail(strict=True)
def test_expected_failure_strict():
    assert True  # 预期失败但实际上通过 -> 失败

# 自定义标记
@pytest.mark.api
@pytest.mark.smoke
def test_api():
    pass

# 命令行: pytest -m "slow"         # 只运行标记 slow 的
# 命令行: pytest -m "not slow"     # 排除 slow
# 命令行: pytest -m "api or smoke" # 逻辑组合
```

### monkeypatch

```python
import pytest
import os

def get_env_config():
    return os.getenv("DATABASE_URL", "default")

def test_config(monkeypatch):
    # 设置环境变量
    monkeypatch.setenv("DATABASE_URL", "test://localhost")
    assert get_env_config() == "test://localhost"
    
    # 删除环境变量
    monkeypatch.delenv("DATABASE_URL", raising=False)
    assert get_env_config() == "default"

# 模拟对象
class ExternalAPI:
    def fetch_data(self):
        raise ConnectionError("网络错误")

def test_external_api(monkeypatch):
    def mock_fetch():
        return {"mock": "data"}
    
    api = ExternalAPI()
    monkeypatch.setattr(api, "fetch_data", mock_fetch)
    assert api.fetch_data() == {"mock": "data"}
```

## 三、Mock 与 MagicMock

```python
from unittest.mock import Mock, MagicMock, patch, PropertyMock, call
import pytest

# Mock 基础
mock = Mock()
mock.return_value = 42
assert mock() == 42

mock.side_effect = [1, 2, 3]
assert mock() == 1
assert mock() == 2
assert mock() == 3

mock.side_effect = ValueError("错误")
with pytest.raises(ValueError):
    mock()

# MagicMock - 支持魔术方法
magic = MagicMock()
magic.__len__.return_value = 5
assert len(magic) == 5

magic.__str__.return_value = "magic"
assert str(magic) == "magic"

# patch 上下文管理器
class Database:
    def query(self, sql):
        raise NotImplementedError

def get_users():
    db = Database()
    return db.query("SELECT * FROM users")

def test_get_users():
    with patch("test_module.Database") as MockDB:
        mock_db = MockDB.return_value
        mock_db.query.return_value = [{"id": 1, "name": "张三"}]
        
        result = get_users()
        assert result == [{"id": 1, "name": "张三"}]
        mock_db.query.assert_called_once_with("SELECT * FROM users")

# patch 装饰器
@patch("test_module.Database")
def test_get_users_decorator(MockDB):
    mock_db = MockDB.return_value
    mock_db.query.return_value = []
    assert get_users() == []

# patch.object
@patch.object(Database, "query", return_value=[{"id": 1}])
def test_patch_object(mock_query):
    db = Database()
    result = db.query("SELECT ...")
    assert result == [{"id": 1}]

# PropertyMock
class Person:
    @property
    def age(self):
        return 30

def test_property_mock():
    person = Person()
    with patch.object(Person, "age", new_callable=PropertyMock) as mock_age:
        mock_age.return_value = 25
        assert person.age == 25

# 断言方法
mock = Mock()
mock(1, 2, key="value")

mock.assert_called()                           # 至少被调用一次
mock.assert_called_once()                      # 恰好被调用一次
mock.assert_called_with(1, 2, key="value")     # 最近一次调用参数匹配
mock.assert_called_once_with(1, 2, key="value") # 唯一一次调用匹配
mock.assert_any_call(1, 2, key="value")        # 任意一次调用匹配
assert mock.call_count == 1

# 跟踪调用
mock("a")
mock("b", c="d")
print(mock.call_args_list)
# [call('a'), call('b', c='d')]

# 重置
mock.reset_mock()
```

## 四、测试覆盖率

```python
# 安装: pip install pytest-cov

# 命令行:
# pytest --cov=myproject tests/
# pytest --cov=myproject --cov-report=html tests/
# pytest --cov=myproject --cov-report=term-missing tests/

# .coveragerc 配置文件
"""
[run]
source = myproject
omit = */tests/*,*/migrations/*

[report]
exclude_lines =
    pragma: no cover
    def __repr__
    raise NotImplementedError
    if __name__ == "__main__":
"""

# 在 pytest 中配置
# pytest.ini
"""
[pytest]
addopts = --cov=myproject --cov-report=term-missing --cov-report=html
testpaths = tests
"""
```

## 五、TDD 示例

```python
# TDD (测试驱动开发) 流程: 红 -> 绿 -> 重构

# 1. 先写测试
def test_fizzbuzz():
    assert fizzbuzz(1) == "1"
    assert fizzbuzz(3) == "Fizz"
    assert fizzbuzz(5) == "Buzz"
    assert fizzbuzz(15) == "FizzBuzz"
    assert fizzbuzz(7) == "7"

# 2. 实现
def fizzbuzz(n: int) -> str:
    if n % 15 == 0:
        return "FizzBuzz"
    if n % 3 == 0:
        return "Fizz"
    if n % 5 == 0:
        return "Buzz"
    return str(n)

# 3. 重构 (优化)
def fizzbuzz_refactored(n: int) -> str:
    result = ""
    if n % 3 == 0:
        result += "Fizz"
    if n % 5 == 0:
        result += "Buzz"
    return result or str(n)
```

## 六、Property-Based Testing (hypothesis)

```python
# 安装: pip install hypothesis

from hypothesis import given, strategies as st, assume
from hypothesis import HealthCheck, settings

# 基本使用
@given(st.integers())
def test_abs_non_negative(x):
    assert abs(x) >= 0

@given(st.lists(st.integers()))
def test_reverse_twice(lst):
    assert lst[::-1][::-1] == lst

# 复杂策略
@given(
    name=st.text(min_size=1, max_size=10),
    age=st.integers(min_value=0, max_value=120),
    email=st.emails()
)
def test_user_creation(name, age, email):
    user = {"name": name, "age": age, "email": email}
    assert "@" in user["email"]

# 自定义策略
positive_ints = st.integers(min_value=1)
even_ints = st.integers().filter(lambda x: x % 2 == 0)

@given(positive_ints)
def test_positive_division(n):
    assert 100 / n > 0

# assume 条件过滤
@given(st.integers(), st.integers())
def test_division(a, b):
    assume(b != 0)  # 排除除数为0
    assert isinstance(a / b, float)

# settings
@given(st.lists(st.integers()))
@settings(max_examples=100, suppress_health_check=[HealthCheck.too_slow])
def test_sorting(lst):
    sorted_lst = sorted(lst)
    assert all(sorted_lst[i] <= sorted_lst[i+1] for i in range(len(sorted_lst)-1))
```

## 七、最佳实践

```python
"""
1. 测试命名规范
   - 文件: test_<module>.py
   - 类: Test<Feature>
   - 方法: test_<should_do_what>

2. 测试结构 (AAA)
   - Arrange: 准备测试数据
   - Act: 执行被测代码
   - Assert: 验证结果

3. 测试隔离
   - 每个测试独立运行
   - 不依赖其他测试的执行结果
   - 使用 setUp/tearDown 清理状态

4. Mock 原则
   - 只 mock 外部依赖 (网络、数据库、文件系统)
   - 不 mock 被测试类内部方法
   - mock 边界要清晰

5. 测试覆盖重点
   - 正常路径 (Happy Path)
   - 边界条件 (空值、0、负数、最大值)
   - 错误路径 (异常、超时)
"""
```

> 测试是保障代码质量的关键。unittest 适合简单项目, pytest 提供更强大的功能和更简洁的语法。建议 pytest + pytest-cov + unittest.mock 组合使用。对于关键业务逻辑, 可辅以 hypothesis 进行属性基测试。
