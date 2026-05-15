---
aliases: [OOP]
tags: ['ProgrammingLanguages', 'Python', 'OOP']
---

# Python 面向对象编程

## 一、类与实例

### 基本定义

```python
class Student:
    """学生类"""
    
    # 类属性（所有实例共享）
    school = "北京大学"
    
    # 初始化方法
    def __init__(self, name: str, age: int, score: float = 0.0):
        self.name = name      # 实例属性
        self.age = age
        self.score = score
    
    # 实例方法
    def introduce(self) -> str:
        return f"我叫{self.name}, {self.age}岁, 来自{self.school}"

# 创建实例
s1 = Student("张三", 20, 95.5)
s2 = Student("李四", 21)

print(s1.introduce())  # 我叫张三, 20岁, 来自北京大学
print(s2.school)       # 北京大学（类属性）
Student.school = "清华大学"  # 修改类属性
print(s1.school)       # 清华大学
```

### self 与 __init__

```python
class Counter:
    def __init__(self, initial=0):
        self.count = initial
    
    def increment(self, step=1):
        self.count += step
        return self.count
    
    def __repr__(self):
        return f"Counter({self.count})"

c = Counter(10)
c.increment()      # 11
c.increment(5)     # 16
```

## 二、实例方法、类方法、静态方法

```python
class Date:
    def __init__(self, year, month, day):
        self.year = year
        self.month = month
        self.day = day
    
    # 实例方法 - 操作实例
    def format(self):
        return f"{self.year}-{self.month:02d}-{self.day:02d}"
    
    # 类方法 - 可以访问类, 常用于工厂方法
    @classmethod
    def from_string(cls, date_str):
        year, month, day = map(int, date_str.split("-"))
        return cls(year, month, day)
    
    # 类方法 - 获取当前日期
    @classmethod
    def today(cls):
        from datetime import date
        d = date.today()
        return cls(d.year, d.month, d.day)
    
    # 静态方法 - 不访问实例或类, 只是逻辑上属于这个类
    @staticmethod
    def is_valid(year, month, day):
        from datetime import date
        try:
            date(year, month, day)
            return True
        except ValueError:
            return False

d = Date(2024, 3, 15)
print(d.format())                # 2024-03-15

d2 = Date.from_string("2024-12-25")
print(d2.format())               # 2024-12-25

d3 = Date.today()
print(d3.format())

print(Date.is_valid(2024, 2, 30))  # False
```

## 三、继承

### 基本继承

```python
class Animal:
    def __init__(self, name):
        self.name = name
    
    def speak(self):
        raise NotImplementedError("子类必须实现")
    
    def move(self):
        return f"{self.name} 在移动"

class Dog(Animal):
    def speak(self):
        return f"{self.name}: 汪汪!"

class Cat(Animal):
    def speak(self):
        return f"{self.name}: 喵喵!"

dog = Dog("旺财")
cat = Cat("咪咪")

print(dog.speak())   # 旺财: 汪汪!
print(cat.speak())   # 咪咪: 喵喵!
print(dog.move())    # 旺财 在移动
```

### super() 与 MRO

```python
class A:
    def __init__(self):
        print("A.__init__")
        super().__init__()

class B(A):
    def __init__(self):
        print("B.__init__")
        super().__init__()

class C(A):
    def __init__(self):
        print("C.__init__")
        super().__init__()

class D(B, C):
    def __init__(self):
        print("D.__init__")
        super().__init__()

d = D()
# MRO: D -> B -> C -> A -> object
print(D.__mro__)

# 实际应用
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

class Employee(Person):
    def __init__(self, name, age, employee_id):
        super().__init__(name, age)  # 调用父类初始化
        self.employee_id = employee_id

class Manager(Employee):
    def __init__(self, name, age, employee_id, department):
        super().__init__(name, age, employee_id)
        self.department = department

mgr = Manager("张三", 35, "E001", "技术部")
print(mgr.name, mgr.department)  # 张三 技术部
```

## 四、封装

### 私有属性与 property

```python
class BankAccount:
    def __init__(self, owner, balance=0):
        self.owner = owner
        self._balance = balance       # 保护属性（约定）
        self.__password = "123456"    # 私有属性（名称修饰）
    
    # getter
    @property
    def balance(self):
        return self._balance
    
    # setter
    @balance.setter
    def balance(self, value):
        if value < 0:
            raise ValueError("余额不能为负")
        self._balance = value
    
    # deleter
    @balance.deleter
    def balance(self):
        print("不允许删除余额")
    
    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("存款金额必须为正")
        self._balance += amount
    
    def withdraw(self, amount):
        if amount > self._balance:
            raise ValueError("余额不足")
        self._balance -= amount

acc = BankAccount("李四", 1000)
print(acc.balance)     # 1000 (通过property访问)
acc.balance = 2000     # 通过setter
# acc.balance = -100   # ValueError!
acc.deposit(500)
print(acc.balance)     # 2500

# 私有属性
# print(acc.__password)  # AttributeError
print(acc._BankAccount__password)  # '123456'（名称修饰后的实际名称）
```

### 另一种 property 方式

```python
class Circle:
    def __init__(self, radius):
        self._radius = radius
    
    def _get_radius(self):
        return self._radius
    
    def _set_radius(self, value):
        if value <= 0:
            raise ValueError("半径必须为正数")
        self._radius = value
    
    radius = property(_get_radius, _set_radius)
    
    @property
    def area(self):
        return 3.14159 * self._radius ** 2
    
    @property
    def circumference(self):
        return 2 * 3.14159 * self._radius
```

## 五、多态

```python
class Shape:
    def area(self):
        pass

class Rectangle(Shape):
    def __init__(self, width, height):
        self.width = width
        self.height = height
    
    def area(self):
        return self.width * self.height

class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius
    
    def area(self):
        return 3.14 * self.radius ** 2

class Triangle(Shape):
    def __init__(self, base, height):
        self.base = base
        self.height = height
    
    def area(self):
        return 0.5 * self.base * self.height

# 多态 - 统一接口
shapes = [
    Rectangle(3, 4),
    Circle(5),
    Triangle(6, 8)
]

for shape in shapes:
    print(f"{shape.__class__.__name__} 面积: {shape.area()}")

# 鸭子类型
class Duck:
    def quack(self):
        return "嘎嘎"

class Person:
    def quack(self):
        return "学鸭子叫"

def make_it_quack(obj):
    print(obj.quack())

make_it_quack(Duck())    # 嘎嘎
make_it_quack(Person())  # 学鸭子叫
```

## 六、魔术方法

```python
class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    # 字符串表示
    def __str__(self):
        return f"Vector({self.x}, {self.y})"
    
    def __repr__(self):
        return f"Vector({self.x!r}, {self.y!r})"
    
    # 长度
    def __len__(self):
        return 2
    
    # 迭代
    def __iter__(self):
        return iter((self.x, self.y))
    
    # 索引
    def __getitem__(self, key):
        if key == 0 or key == "x":
            return self.x
        if key == 1 or key == "y":
            return self.y
        raise IndexError("Vector 只有2个元素")
    
    # 比较
    def __eq__(self, other):
        if not isinstance(other, Vector):
            return NotImplemented
        return self.x == other.x and self.y == other.y
    
    def __hash__(self):
        return hash((self.x, self.y))
    
    # 运算
    def __add__(self, other):
        if isinstance(other, Vector):
            return Vector(self.x + other.x, self.y + other.y)
        return NotImplemented
    
    def __sub__(self, other):
        if isinstance(other, Vector):
            return Vector(self.x - other.x, self.y - other.y)
        return NotImplemented
    
    def __mul__(self, scalar):
        return Vector(self.x * scalar, self.y * scalar)
    
    def __truediv__(self, scalar):
        return Vector(self.x / scalar, self.y / scalar)
    
    # 负号
    def __neg__(self):
        return Vector(-self.x, -self.y)
    
    # 绝对值
    def __abs__(self):
        return (self.x ** 2 + self.y ** 2) ** 0.5
    
    # bool
    def __bool__(self):
        return self.x != 0 or self.y != 0

v1 = Vector(3, 4)
v2 = Vector(1, 2)

print(v1)              # Vector(3, 4)
print(repr(v1))        # Vector(3, 4)
print(len(v1))         # 2
print(list(v1))        # [3, 4]
print(v1[0])           # 3
print(v1["y"])         # 4
print(v1 == v2)        # False
print(v1 + v2)         # Vector(4, 6)
print(v1 * 3)          # Vector(9, 12)
print(abs(v1))         # 5.0
print(bool(Vector(0,0)))  # False
```

## 七、抽象基类 (ABC)

```python
from abc import ABC, abstractmethod

class Payment(ABC):
    @abstractmethod
    def pay(self, amount):
        pass
    
    @abstractmethod
    def refund(self, amount):
        pass
    
    def receipt(self, amount):
        return f"收到付款: {amount}元"  # 共有的具体方法

class Alipay(Payment):
    def pay(self, amount):
        return f"支付宝支付: {amount}元"
    
    def refund(self, amount):
        return f"支付宝退款: {amount}元"

class WechatPay(Payment):
    def pay(self, amount):
        return f"微信支付: {amount}元"
    
    def refund(self, amount):
        return f"微信退款: {amount}元"

# p = Payment()  # TypeError! 不能实例化抽象类

alipay = Alipay()
print(alipay.pay(100))      # 支付宝支付: 100元
print(alipay.receipt(100))  # 收到付款: 100元
```

### 抽象属性

```python
class Base(ABC):
    @property
    @abstractmethod
    def id(self):
        pass

class Concrete(Base):
    @property
    def id(self):
        return 42
```

## 八、dataclasses (Python 3.7+)

```python
from dataclasses import dataclass, field, asdict, astuple
from typing import List

@dataclass
class Point:
    x: float
    y: float
    z: float = 0.0  # 默认值

@dataclass(order=True)
class Person:
    name: str
    age: int
    hobbies: List[str] = field(default_factory=list)
    
    def say_hello(self):
        return f"你好, 我是{self.name}"

p1 = Person("张三", 25, ["读书", "编程"])
p2 = Person("李四", 30)

print(p1)                      # Person(name='张三', age=25, hobbies=['读书', '编程'])
print(p1 == Person("张三", 25, ["读书", "编程"]))  # True
print(p1 > p2)                 # False (因为age比较)
print(asdict(p1))              # {'name': '张三', 'age': 25, 'hobbies': ['读书', '编程']}
```

### dataclass 高级用法

```python
@dataclass(frozen=True)  # 不可变
class Immutable:
    x: int
    y: int

# im = Immutable(1, 2)
# im.x = 10  # FrozenInstanceError!

@dataclass
class Config:
    host: str = "localhost"
    port: int = 8080
    debug: bool = field(default=False, repr=False)  # repr中不显示
    _internal: str = field(default="secret", init=False)  # 不在__init__中

config = Config()
print(config)  # Config(host='localhost', port=8080)
```

## 九、类型注解

```python
from typing import Optional, List, Dict, Tuple, Union

class User:
    def __init__(self, name: str, age: int, email: Optional[str] = None):
        self.name: str = name
        self.age: int = age
        self.email: Optional[str] = email
    
    def get_info(self) -> Dict[str, object]:
        return {
            "name": self.name,
            "age": self.age,
            "email": self.email
        }
    
    @staticmethod
    def from_list(data: List[str]) -> "User":
        return User(name=data[0], age=int(data[1]))

def process_users(users: List[User]) -> List[str]:
    return [u.name for u in users]

def get_config() -> Tuple[str, int, bool]:
    return ("localhost", 8080, True)

def handle_union(value: Union[int, str]) -> str:
    if isinstance(value, int):
        return str(value * 2)
    return value.upper()
```

> 面向对象编程是 Python 的核心范式。理解类、继承、封装、多态以及魔术方法, 对于编写可维护、可扩展的 Python 代码至关重要。
