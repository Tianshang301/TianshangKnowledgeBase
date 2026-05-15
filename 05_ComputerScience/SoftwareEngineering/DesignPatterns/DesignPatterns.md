---
aliases: [DesignPatterns]
tags: ['SoftwareEngineering', 'DesignPatterns', 'DesignPatterns']
---

# 设计模式

## 一、设计模式概述

设计模式（Design Patterns）是软件设计中常见问题的可复用解决方案。1994 年 GoF（Gang of Four）在《Design Patterns》中提出了 23 种经典模式，分为三大类。

| 类别 | 关注点 | 模式数量 |
|------|--------|---------|
| 创建型模式 | 对象的创建机制 | 5 |
| 结构型模式 | 对象/类的组合 | 7 |
| 行为型模式 | 对象间的交互和职责分配 | 11 |

## 二、创建型模式

### 单例模式（Singleton）

确保一个类只有一个实例，提供全局访问点。

```java
public class Singleton {
    private static volatile Singleton instance;

    private Singleton() {}

    public static Singleton getInstance() {
        if (instance == null) {
            synchronized (Singleton.class) {
                if (instance == null) {
                    instance = new Singleton();
                }
            }
        }
        return instance;
    }
}
```

| 优点 | 缺点 |
|------|------|
| 控制实例数量 | 违反单一职责 |
| 全局访问点 | 不利于测试 |
| 延迟初始化 | 多线程需注意 |

### 工厂方法模式（Factory Method）

定义一个创建对象的接口，让子类决定实例化哪个类。

```python
from abc import ABC, abstractmethod

class Creator(ABC):
    @abstractmethod
    def factory_method(self):
        pass

    def operation(self):
        product = self.factory_method()
        return f"Created {product}"

class ConcreteCreatorA(Creator):
    def factory_method(self):
        return ProductA()

class ConcreteCreatorB(Creator):
    def factory_method(self):
        return ProductB()
```

### 抽象工厂模式（Abstract Factory）

提供一个创建一系列相关或相互依赖对象的接口，无需指定具体类。

| 模式 | 产品等级 | 产品族 | 扩展性 |
|------|---------|--------|--------|
| 工厂方法 | 一个产品等级 | — | 增加产品等级容易 |
| 抽象工厂 | 多个产品等级 | 多个产品族 | 增加产品族容易 |

### 建造者模式（Builder）

将一个复杂对象的构建与表示分离，同样的构建过程可以创建不同的表示。

```java
Computer computer = new Computer.Builder()
    .setCPU("Intel i7")
    .setRAM("32GB")
    .setStorage("1TB SSD")
    .setGPU("RTX 4080")
    .build();
```

### 原型模式（Prototype）

通过拷贝已有对象创建新对象，而非通过 new 创建。

## 三、结构型模式

### 适配器模式（Adapter）

将一个类的接口转换成客户端期望的另一个接口。

```python
class Target:
    def request(self): return "Target"

class Adaptee:
    def specific_request(self): return "Adaptee"

class Adapter(Target):
    def __init__(self, adaptee):
        self.adaptee = adaptee

    def request(self):
        return self.adaptee.specific_request()
```

### 装饰器模式（Decorator）

动态地给对象添加额外的职责，比继承更灵活。

```python
def bold(func):
    def wrapper(*args, **kwargs):
        return f"<b>{func(*args, **kwargs)}</b>"
    return wrapper

def italic(func):
    def wrapper(*args, **kwargs):
        return f"<i>{func(*args, **kwargs)}</i>"
    return wrapper

@bold
@italic
def greet(name):
    return f"Hello, {name}"
```

### 代理模式（Proxy）

为另一个对象提供一个替身或占位符以控制对其的访问。

| 代理类型 | 用途 |
|---------|------|
| 虚拟代理 | 延迟加载大对象 |
| 保护代理 | 控制访问权限 |
| 远程代理 | 远程方法调用 |
| 智能引用 | 计数、缓存、日志 |

### 其他结构型模式

| 模式 | 作用 | 类比 |
|------|------|------|
| 桥接模式 | 将抽象和实现解耦 | 遥控器 ↔ 设备 |
| 组合模式 | 树形结构统一处理 | 文件系统 |
| 外观模式 | 为子系统提供统一接口 | 前台接待 |
| 享元模式 | 共享细粒度对象 | 文字渲染 |

## 四、行为型模式

### 策略模式（Strategy）

定义一系列算法，将每个算法封装起来，使它们可以相互替换。

```python
from abc import ABC, abstractmethod

class Strategy(ABC):
    @abstractmethod
    def execute(self, data): pass

class QuickSort(Strategy):
    def execute(self, data):
        return sorted(data)

class MergeSort(Strategy):
    def execute(self, data):
        # 归并排序实现
        return sorted(data)

class Context:
    def __init__(self, strategy: Strategy):
        self.strategy = strategy

    def sort(self, data):
        return self.strategy.execute(data)
```

### 观察者模式（Observer）

定义一对多依赖关系，当一个对象状态变化时，所有依赖对象自动更新。

```python
class Subject:
    def __init__(self):
        self._observers = []

    def attach(self, observer):
        self._observers.append(observer)

    def notify(self, data):
        for obs in self._observers:
            obs.update(data)

class Observer:
    def update(self, data):
        print(f"Received: {data}")
```

### 模板方法模式（Template Method）

在父类中定义算法的骨架，将某些步骤延迟到子类实现。

```java
abstract class DataProcessor {
    public final void process() {
        readData();
        processData();
        saveData();
    }

    abstract void readData();
    abstract void processData();

    void saveData() {
        System.out.println("Saving to database");
    }
}
```

### 其他行为型模式

| 模式 | 作用 | 典型场景 |
|------|------|---------|
| 责任链模式 | 请求沿链传递 | 日志级别、中间件 |
| 命令模式 | 将请求封装为对象 | 操作撤销/重做 |
| 迭代器模式 | 顺序访问集合元素 | 集合遍历 |
| 中介者模式 | 减少对象间直接耦合 | 聊天室 |
| 备忘录模式 | 保存和恢复对象状态 | 撤销操作 |
| 状态模式 | 对象状态改变行为 | 订单状态机 |
| 访问者模式 | 在不修改类的前提下增加操作 | AST 处理 |
| 解释器模式 | 定义语言语法解释器 | 表达式计算 |

## 五、模式选择原则

| 原则 | 说明 |
|------|------|
| SOLID 原则 | 单一职责、开闭、里氏替换、接口隔离、依赖反转 |
| 组合优于继承 | 使用组合增加灵活性 |
| 面向接口编程 | 依赖抽象而非具体实现 |
| 高内聚低耦合 | 模块内部紧密，模块间松散 |
| DRY（Don't Repeat Yourself） | 消除重复代码 |

## 六、反模式

常见反模式（Anti-Patterns）：

| 反模式 | 问题 | 解决方案 |
|--------|------|---------|
| 上帝类（God Class） | 一个类承担过多职责 | 拆分为多个类 |
| 面条代码（Spaghetti Code） | 流程混乱，难以维护 | 重构，引入设计模式 |
| 万能适配器（Kitchen Sink） | 接口过于庞大 | 接口隔离原则 |
| 重复代码（Copy-Paste） | 相同的代码多处出现 | 提取公共方法 |
| 过早优化 | 在需求未明确前优化 | 先实现，后优化 |

## 七、现代应用

### 函数式替代

一些经典模式可用函数式编程简化：

```python
# 策略模式 → 高阶函数
def sorter(strategy):
    return lambda data: strategy(data)

quick_sort = sorter(sorted)
merge_sort = sorter(merge_sort_impl)

# 命令模式 → 函数作为参数
def execute(fn, *args):
    return fn(*args)
```

### 框架中常见模式

| 框架 | 使用模式 |
|------|---------|
| Spring | 依赖注入（策略）、代理（AOP） |
| React | 观察者（状态管理）、组合（组件） |
| Django | 模板方法（CBV）、中间件（责任链） |
| Express | 中间件（责任链） |
| Vuex/Redux | 观察者、命令 |

## 相关条目

- ArchitecturePatterns
- [[OOP]]
- SOLID
- Refactoring

## 参考资源

- 《Design Patterns: Elements of Reusable Object-Oriented Software》（GoF）
- 《Head First Design Patterns》（O'Reilly）
- 《Clean Architecture》（Robert C. Martin）
- [Refactoring.Guru - 设计模式](https://refactoring.guru/design-patterns)
- [SourceMaking - Design Patterns](https://sourcemaking.com/design_patterns)
