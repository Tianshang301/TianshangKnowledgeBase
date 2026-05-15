---
aliases: [Advanced]
tags: ['ProgrammingLanguages', 'Python', 'Advanced']
---

# Python 进阶特性

## 一、装饰器 (Decorators)

### 基础装饰器

```python
from functools import wraps
import time
import random
import functools

# 最简单的装饰器
def my_decorator(func):
    @wraps(func)  # 保留原函数元信息
    def wrapper(*args, **kwargs):
        print(f"调用函数: {func.__name__}")
        result = func(*args, **kwargs)
        print(f"函数返回: {result}")
        return result
    return wrapper

@my_decorator
def add(a, b):
    return a + b

add(3, 5)
# 调用函数: add
# 函数返回: 8
```

### 实用装饰器示例

```python
# 1. @timer - 计时装饰器
def timer(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        print(f"{func.__name__} 耗时: {elapsed:.4f}秒")
        return result
    return wrapper

@timer
def slow_function():
    time.sleep(0.5)
    return "done"

slow_function()

# 2. @retry - 重试装饰器
def retry(max_attempts=3, delay=0.1):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts:
                        raise
                    print(f"第{attempt}次失败: {e}, 重试中...")
                    time.sleep(delay)
            return None
        return wrapper
    return decorator

@retry(max_attempts=3)
def unstable_network():
    if random.random() < 0.7:
        raise ConnectionError("网络不稳定")
    return "成功!"

# 3. @cache - 缓存装饰器
def cache(func):
    memo = {}
    @wraps(func)
    def wrapper(*args, **kwargs):
        key = (args, tuple(sorted(kwargs.items())))
        if key not in memo:
            memo[key] = func(*args, **kwargs)
        return memo[key]
    return wrapper

@cache
def expensive_computation(n):
    print(f"计算: {n}")
    return sum(range(n))

print(expensive_computation(1000000))  # 计算
print(expensive_computation(1000000))  # 直接返回缓存

# 4. @debug - 调试装饰器
def debug(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        args_repr = [repr(a) for a in args]
        kwargs_repr = [f"{k}={v!r}" for k, v in kwargs.items()]
        signature = ", ".join(args_repr + kwargs_repr)
        print(f"调用: {func.__name__}({signature})")
        result = func(*args, **kwargs)
        print(f"返回: {func.__name__}(...) = {result!r}")
        return result
    return wrapper

@debug
def greet(name, greeting="你好"):
    return f"{greeting}, {name}!"

greet("张三")
greet("李四", greeting="Hello")
```

### 带参数的装饰器

```python
def repeat(times=2):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            results = []
            for _ in range(times):
                results.append(func(*args, **kwargs))
            return results
        return wrapper
    return decorator

@repeat(times=3)
def say_hello(name):
    return f"你好, {name}"

print(say_hello("张三"))
# ['你好, 张三', '你好, 张三', '你好, 张三']
```

### 类装饰器

```python
class CountCalls:
    def __init__(self, func):
        self.func = func
        self.count = 0
    
    def __call__(self, *args, **kwargs):
        self.count += 1
        print(f"第{self.count}次调用 {self.func.__name__}")
        return self.func(*args, **kwargs)

@CountCalls
def hello():
    print("Hello!")

hello()  # 第1次调用 hello
hello()  # 第2次调用 hello
```

### 多个装饰器组合

```python
@timer
@debug
def complex_func(x, y):
    time.sleep(0.1)
    return x ** y

# 执行顺序: timer(debug(complex_func))
# 由内向外装饰, 由外向内执行
complex_func(2, 10)
```

## 二、生成器 (Generators)

### yield 基础

```python
def countdown(n):
    print("开始倒计时")
    while n > 0:
        yield n
        n -= 1
    print("倒计时结束")

# 创建生成器对象
gen = countdown(3)
print(gen)  # <generator object countdown at 0x...>

# 手动迭代
print(next(gen))  # 3
print(next(gen))  # 2
print(next(gen))  # 1
# print(next(gen))  # StopIteration

# for 循环自动迭代
for x in countdown(3):
    print(x)

# 生成器表达式
squares = (x**2 for x in range(10))
print(next(squares))  # 0
print(list(squares))  # [1, 4, 9, 16, 25, 36, 49, 64, 81]
```

### 实用生成器

```python
# 无限序列
def fibonacci():
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b

fib = fibonacci()
first_10 = [next(fib) for _ in range(10)]
print(first_10)  # [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]

生成器延迟求值，内存复杂度 $O(1)$ 而非 $O(n)$。

# 文件行读取 (内存友好)
def read_lines(filename):
    with open(filename, "r", encoding="utf-8") as f:
        for line in f:
            yield line.strip()

# 分块读取大文件
def chunks(file, chunk_size=1024):
    while True:
        data = file.read(chunk_size)
        if not data:
            break
        yield data

# 管道处理
def grep(pattern, lines):
    for line in lines:
        if pattern in line:
            yield line

def upper(lines):
    for line in lines:
        yield line.upper()

lines = ["hello world", "python is great", "hello python"]
result = upper(grep("python", lines))
print(list(result))  # ['PYTHON IS GREAT', 'HELLO PYTHON']
```

### send / throw / close

```python
def interactive_counter():
    i = 0
    while True:
        received = yield i
        if received == "reset":
            i = 0
        elif received == "increment":
            i += 1
        else:
            i += 1

gen = interactive_counter()
print(next(gen))           # 0 (首次启动必须next或send(None))
print(gen.send("increment"))  # 1
print(gen.send("increment"))  # 2
print(gen.send("reset"))      # 0
# gen.throw(ValueError("自定义错误"))  # 向生成器抛异常
# gen.close()  # 关闭生成器
```

### yield from

```python
def reader():
    yield "A"
    yield "B"

def writer():
    yield "1"
    yield "2"

def combined():
    yield from reader()
    yield from writer()

print(list(combined()))  # ['A', 'B', '1', '2']

# 实际应用 - 递归遍历
def flatten(nested):
    for item in nested:
        if isinstance(item, (list, tuple)):
            yield from flatten(item)
        else:
            yield item

nested = [1, [2, [3, 4], 5], 6]
print(list(flatten(nested)))  # [1, 2, 3, 4, 5, 6]
```

## 三、上下文管理器 (Context Managers)

### with 语句

```python
# 自定义上下文管理器 (类方式)
class ManagedFile:
    def __init__(self, filename, mode="r", encoding="utf-8"):
        self.filename = filename
        self.mode = mode
        self.encoding = encoding
        self.file = None
    
    def __enter__(self):
        print(f"打开文件: {self.filename}")
        self.file = open(self.filename, self.mode, encoding=self.encoding)
        return self.file  # 绑定到 as 变量
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        print(f"关闭文件: {self.filename}")
        if self.file:
            self.file.close()
        # 返回False则传播异常, True则抑制异常
        return False

with ManagedFile("test.txt", "w") as f:
    f.write("Hello, 上下文管理器!")

# 上下文管理器应用于数据库连接
class DatabaseConnection:
    def __init__(self, connection_string):
        self.connection_string = connection_string
        self.connection = None
    
    def __enter__(self):
        print(f"连接数据库: {self.connection_string}")
        self.connection = {"connected": True}  # 模拟连接
        return self.connection
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        print("关闭数据库连接")
        self.connection = None
        if exc_type:
            print(f"发生异常: {exc_val}")
        return False
```

### contextlib 模块

```python
from contextlib import contextmanager, closing, suppress, redirect_stdout
import io

@contextmanager
def managed_file(filename, mode="r"):
    print("打开资源")
    file = open(filename, mode, encoding="utf-8")
    try:
        yield file
    finally:
        print("关闭资源")
        file.close()

with managed_file("test.txt", "w") as f:
    f.write("使用contextmanager")

# 计时上下文管理器
@contextmanager
def timed():
    start = time.perf_counter()
    try:
        yield
    finally:
        elapsed = time.perf_counter() - start
        print(f"耗时: {elapsed:.4f}秒")

with timed():
    time.sleep(0.3)

# closing - 自动调用close方法
from urllib.request import urlopen
# with closing(urlopen("http://example.com")) as page:
#     print(page.read())

# suppress - 忽略指定异常
with suppress(FileNotFoundError):
    with open("不存在的文件.txt") as f:
        print(f.read())
# 不会报错

# redirect_stdout - 重定向标准输出
buf = io.StringIO()
with redirect_stdout(buf):
    print("被捕获的内容")
output = buf.getvalue()
print(output)  # '被捕获的内容\n'
```

### 嵌套上下文管理器

```python
# 方式1: 嵌套with
with open("a.txt") as f1:
    with open("b.txt") as f2:
        pass

# 方式2: 单个with多个
with open("a.txt") as f1, open("b.txt") as f2:
    pass
```

## 四、元类 (Metaclasses)

```python
# 一切皆对象, 类也是对象
class MyClass:
    pass

print(type(MyClass))  # <class 'type'>
print(type(type))     # <class 'type'>

# 使用type动态创建类
MyDynamicClass = type("MyDynamicClass", (object,), {"x": 10, "hello": lambda self: "你好"})
obj = MyDynamicClass()
print(obj.x)         # 10
print(obj.hello())   # 你好

# 自定义元类
class UpperAttrMeta(type):
    """将所有属性名转为大写"""
    def __new__(cls, name, bases, attrs):
        upper_attrs = {}
        for attr_name, attr_value in attrs.items():
            if not attr_name.startswith("__"):
                upper_attrs[attr_name.upper()] = attr_value
            else:
                upper_attrs[attr_name] = attr_value
        return super().__new__(cls, name, bases, upper_attrs)

class MyClass(metaclass=UpperAttrMeta):
    name = "张三"
    age = 28

print(hasattr(MyClass, "name"))  # False
print(hasattr(MyClass, "NAME"))  # True
print(MyClass.NAME)  # 张三

# 实际应用: 单例元类
class SingletonMeta(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]

class Database(metaclass=SingletonMeta):
    def __init__(self):
        print("初始化数据库连接")

db1 = Database()  # 打印 "初始化数据库连接"
db2 = Database()  # 不打印
print(db1 is db2)  # True
```

## 五、描述器 (Descriptors)

```python
# 描述器协议: __get__, __set__, __delete__

class PositiveNumber:
    """描述器: 只允许正数"""
    def __set_name__(self, owner, name):
        self._name = name
    
    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        return obj.__dict__.get(self._name, 0)
    
    def __set__(self, obj, value):
        if not isinstance(value, (int, float)):
            raise TypeError(f"{self._name} 必须是数字")
        if value <= 0:
            raise ValueError(f"{self._name} 必须为正数")
        obj.__dict__[self._name] = value

class Product:
    price = PositiveNumber()
    quantity = PositiveNumber()
    
    def __init__(self, name, price, quantity):
        self.name = name
        self.price = price      # 自动验证
        self.quantity = quantity

# p = Product("手机", -100, 5)  # ValueError!
p = Product("手机", 2999, 100)
print(p.price)     # 2999
# p.price = -100   # ValueError!
```

### property 是描述器

```python
# @property 实际上就是一个描述器
class Celsius:
    def __init__(self, temperature=0):
        self._temperature = temperature
    
    @property
    def temperature(self):
        return self._temperature
    
    @temperature.setter
    def temperature(self, value):
        if value < -273.15:
            raise ValueError("温度不能低于绝对零度")
        self._temperature = value
```

## 六、`__slots__`

```python
# __slots__ 用于限制实例属性并节省内存

class WithoutSlots:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class WithSlots:
    __slots__ = ("x", "y")
    
    def __init__(self, x, y):
        self.x = x
        self.y = y

# 内存对比
import sys

ws = WithoutSlots(1, 2)
wos = WithSlots(1, 2)

print(f"无 __slots__: {sys.getsizeof(ws)} 字节")
print(f"有 __slots__: {sys.getsizeof(wos)} 字节")

`__slots__` 消除 `__dict__`，每个实例节省约 $\text{sizeof}(\text{\_\_dict\_\_}) \approx 56\text{ bytes} + O(n_{\text{attrs}})$。

# __slots__ 限制
# wos.z = 3  # AttributeError! 'WithSlots' object has no attribute 'z'

# 继承中的 __slots__
class Base:
    __slots__ = ("a",)

class Child(Base):
    __slots__ = ("b",)  # 子类也需要定义才能生效

c = Child()
c.a = 1  # OK
c.b = 2  # OK
# c.c = 3  # AttributeError
```

## 七、其他进阶技巧

```python
# 1. 运算符重载补充
class Matrix:
    def __init__(self, data):
        self.data = data
    
    def __matmul__(self, other):  # @ 运算符
        # 矩阵乘法
        result = [[0] * len(other.data[0]) for _ in range(len(self.data))]
        for i in range(len(self.data)):
            for j in range(len(other.data[0])):
                for k in range(len(other.data)):
                    result[i][j] += self.data[i][k] * other.data[k][j]
        return Matrix(result)

Python 中 `@` 运算符对应矩阵乘法 $(AB)_{ij} = \sum_{k=1}^m A_{ik}B_{kj}$，时间复杂度 $O(n^3)$。

A = Matrix([[1,2],[3,4]])
B = Matrix([[5,6],[7,8]])
C = A @ B

# 2. 函数注解
def func(a: int, b: str = "default") -> list:
    return [a, b]

print(func.__annotations__)  # {'a': int, 'b': str, 'return': list}

# 3. walrus 运算符 := (Python 3.8+)
if (n := len([1,2,3,4,5])) > 3:
    print(f"长度 {n} > 3")

# 读取文件块
# while chunk := file.read(1024):
#     process(chunk)

# 4. 枚举
from enum import Enum, auto

class Color(Enum):
    RED = 1
    GREEN = 2
    BLUE = 3

class Status(Enum):
    PENDING = auto()
    PROCESSING = auto()
    COMPLETED = auto()
    FAILED = auto()

print(Color.RED.value)       # 1
print(Color.RED.name)        # 'RED'
print(list(Color))           # [<Color.RED: 1>, ...]
```

> 进阶特性是区分 Python 新手和专家的关键。装饰器、生成器、上下文管理器是日常开发中使用最多的进阶特性, 建议重点掌握。元类和描述器虽然不常用, 但在框架开发中非常重要。
