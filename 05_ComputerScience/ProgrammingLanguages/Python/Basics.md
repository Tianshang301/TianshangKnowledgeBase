---
aliases: [Basics]
tags: ['ProgrammingLanguages', 'Python', 'Basics']
created: 2026-05-16
updated: 2026-05-13
---

# Python 基础语法详解

## 一、数据类型

### 基本数据类型

```python
# int - 整数
a = 42
b = -7
c = 0b1010  # 二进制 10
d = 0xFF    # 十六进制 255
e = 1_000_000  # 1000000（可读性分隔符）

# float - 浮点数
f = 3.14
g = 1.5e-3   # 0.0015
h = float('inf')  # 无穷大
i = float('nan')  # 非数值

# str - 字符串
s1 = 'hello'
s2 = "world"
s3 = '''多行
字符串'''

# bool - 布尔值
t = True
f_val = False

# None - 空值
n = None
```

### 类型转换

```python
int("42")        # 42
float("3.14")    # 3.14
str(123)         # "123"
bool(1)          # True
bool(0)          # False
bool("")         # False
bool([])         # False
bool("non")      # True

# 进制转换
bin(255)         # '0b11111111'
oct(255)         # '0o377'
hex(255)         # '0xff'

# 类型检查
isinstance(42, int)     # True
type(3.14) is float     # True
```

## 二、字符串操作

### 切片

```python
s = "Python 编程"

s[0]       # 'P'
s[-1]      # '程'
s[0:3]     # 'Pyt'
s[::2]     # 'Pto 编'
s[::-1]    # '程编 nohtyP'
s[1:-1]    # 'ython 编'
```

### 常用方法

```python
s = "  hello, WORLD!  "

s.lower()          # '  hello, world!  '
s.upper()          # '  HELLO, WORLD!  '
s.strip()          # 'hello, WORLD!'
s.replace("l", "L")  # '  heLLo, WORLD!  '
s.split(",")       # ['  hello', ' WORLD!  ']
",".join(["a","b","c"])  # 'a,b,c'
s.startswith("  h")  # True
s.find("WOR")      # 9
s.count("l")       # 3
len(s)             # 17
```

### f-string (Python 3.6+)

```python
name = "张三"
age = 28
score = 92.5678

f"姓名: {name}, 年龄: {age}"
# '姓名: 张三, 年龄: 28'

f"成绩: {score:.1f}"       # '成绩: 92.6'
f"成绩: {score:.2f}"       # '成绩: 92.57'
f"十六进制: {255:#x}"      # '十六进制: 0xff'
f"百分比: {0.856:.1%}"    # '百分比: 85.6%'

# 表达式
f"总和: {sum([1,2,3])}"   # '总和: 6'

# 多行 f-string
msg = (
    f"姓名: {name}\n"
    f"年龄: {age}"
)
```

## 三、列表

### 创建与操作

```python
# 创建
lst = [1, 2, 3, 4, 5]
empty = []
nested = [[1,2], [3,4]]
mixed = [1, "hello", 3.14, True]

# 索引与切片
lst[0]       # 1
lst[-1]      # 5
lst[1:4]     # [2, 3, 4]
lst[::2]     # [1, 3, 5]

# 修改
lst[0] = 10
lst[1:3] = [20, 30]
```

### 常用方法

```python
lst = [3, 1, 4, 1, 5]

lst.append(9)      # [3, 1, 4, 1, 5, 9]
lst.extend([2, 6]) # [3, 1, 4, 1, 5, 9, 2, 6]
lst.insert(0, 0)   # [0, 3, 1, 4, 1, 5, 9, 2, 6]
lst.remove(1)      # 移除第一个1
lst.pop()          # 移除并返回最后一个元素
lst.pop(0)         # 移除并返回索引0元素
lst.sort()         # 原地排序
lst.reverse()      # 原地反转
lst.index(4)       # 返回4的索引
lst.count(1)       # 统计1出现的次数
len(lst)           # 列表长度
```

### 列表推导式

```python
# 基本
squares = [x**2 for x in range(10)]
# [0, 1, 4, 9, 16, 25, 36, 49, 64, 81]

# 带条件
evens = [x for x in range(20) if x % 2 == 0]

# 嵌套
pairs = [(x, y) for x in [1,2,3] for y in [4,5]]
# [(1,4), (1,5), (2,4), (2,5), (3,4), (3,5)]

# 条件表达式
labels = ["even" if x % 2 == 0 else "odd" for x in range(5)]
# ['even', 'odd', 'even', 'odd', 'even']

# 展平嵌套列表
matrix = [[1,2,3], [4,5,6], [7,8,9]]
flat = [x for row in matrix for x in row]
# [1, 2, 3, 4, 5, 6, 7, 8, 9]
```

## 四、元组

```python
# 创建
t = (1, 2, 3)
single = (1,)       # 注意逗号
no_paren = 1, 2, 3  # 也是元组

# 解包
a, b, c = (1, 2, 3)
a, *rest = [1, 2, 3, 4]  # a=1, rest=[2,3,4]

# 元组不可变
# t[0] = 10  # TypeError!

# 交换变量（元组解包）
a, b = b, a

# 作为字典键
d = {(1,2): "value"}  # 合法, 列表不行
```

## 五、集合

```python
# 创建
s = {1, 2, 3, 3, 2}  # {1, 2, 3}
empty_set = set()

# 操作
s.add(4)
s.remove(2)     # 不存在则 KeyError
s.discard(10)   # 不存在不报错
s.pop()         # 移除并返回任意元素

# 集合运算
a = {1, 2, 3, 4}
b = {3, 4, 5, 6}

a | b    # 并集 {1,2,3,4,5,6}
a & b    # 交集 {3,4}
a - b    # 差集 {1,2}
a ^ b    # 对称差 {1,2,5,6}

# 集合推导式
{x**2 for x in range(5)}  # {0, 1, 4, 9, 16}
```

## 六、字典

```python
# 创建
d = {"name": "张三", "age": 28}
d2 = dict(name="李四", age=25)
d3 = dict(zip(["a","b"], [1,2]))
d4 = {x: x**2 for x in range(5)}

# 访问
d["name"]          # '张三'
d.get("name")      # '张三'
d.get("gender", "未知")  # '未知'
d.keys()           # dict_keys(['name', 'age'])
d.values()         # dict_values(['张三', 28])
d.items()          # dict_items([('name','张三'), ('age',28)])

# 修改
d["gender"] = "男"
d.update({"age": 29, "city": "北京"})

# 删除
del d["gender"]
removed = d.pop("city")  # 返回 '北京'
d.clear()

# 安全访问
d.setdefault("count", 0)  # 不存在则设置默认值并返回
d.setdefault("count", 0)  # 已存在则返回现有值
```

## 七、控制流

### if/elif/else

```python
score = 85

if score >= 90:
    grade = "A"
elif score >= 80:
    grade = "B"
elif score >= 70:
    grade = "C"
elif score >= 60:
    grade = "D"
else:
    grade = "F"

# 条件表达式（三元运算符）
status = "通过" if score >= 60 else "挂科"

# 短路求值
name = input() or "匿名"
```

### for 循环

```python
# 遍历序列
for item in [1, 2, 3]:
    print(item)

# enumerate 获取索引
for i, v in enumerate(["a", "b", "c"]):
    print(i, v)

# zip 并行遍历
for name, age in zip(["张三","李四"], [28, 25]):
    print(f"{name}: {age}")

# range
for i in range(5):       # 0-4
    pass
for i in range(2, 8, 2): # 2,4,6
    pass

# reversed 反向遍历
for c in reversed("hello"):
    print(c)

# sorted 排序遍历
for v in sorted([3,1,4,1,5]):
    print(v)
```

### while 循环

```python
i = 0
while i < 5:
    print(i)
    i += 1

# break / continue / else
i = 0
while i < 10:
    i += 1
    if i == 3:
        continue  # 跳过3
    if i == 7:
        break     # 到7退出
else:
    print("未被打断")  # break 时不会执行
```

## 八、函数

### 定义与调用

```python
def greet(name):
    return f"你好, {name}!"

# 默认参数
def power(base, exp=2):
    return base ** exp

# 可变参数 *args
def sum_all(*args):
    return sum(args)

sum_all(1, 2, 3, 4)  # 10

# 关键字参数 **kwargs
def print_info(**kwargs):
    for k, v in kwargs.items():
        print(f"{k}: {v}")

print_info(name="张三", age=28)

# 混合使用
def func(a, b, *args, c=10, **kwargs):
    pass

# 仅限关键字参数
def func(a, b, *, verbose=False):
    pass

func(1, 2, verbose=True)  # verbose 必须用关键字
```

### 作用域

```python
x = "全局"

def outer():
    x = "外层"
    def inner():
        nonlocal x  # 修改外层非全局变量
        x = "内层"
        global g   # 声明使用全局变量
        g = "全局变量"
    inner()
    print(x)  # 内层

outer()
print(x)  # 全局
```

### lambda

```python
# 匿名函数
square = lambda x: x**2
square(5)  # 25

# 常用场景 - sort 的 key
students = [("张三", 85), ("李四", 92), ("王五", 78)]
students.sort(key=lambda s: s[1], reverse=True)

# map/filter/reduce
list(map(lambda x: x*2, [1,2,3]))      # [2,4,6]
list(filter(lambda x: x > 2, [1,2,3,4]))  # [3,4]
from functools import reduce
reduce(lambda a, b: a*b, [1,2,3,4])    # 24
```

## 九、输入输出

```python
# 输入
name = input("请输入姓名: ")  # 返回字符串
age = int(input("请输入年龄: "))

# 输出
print("hello", "world", sep=", ")  # hello, world
print("hello", end="!!!\n")        # hello!!!
print(*[1,2,3])                    # 1 2 3

# 格式化输出
name = "张三"
print("姓名: %s, 年龄: %d" % (name, age))
print("姓名: {}, 年龄: {}".format(name, age))
print(f"姓名: {name}, 年龄: {age}")
```

## 十、文件处理

```python
# 写入文件
with open("example.txt", "w", encoding="utf-8") as f:
    f.write("第一行\n")
    f.write("第二行\n")
    lines = ["行1\n", "行2\n", "行3\n"]
    f.writelines(lines)

# 读取文件
with open("example.txt", "r", encoding="utf-8") as f:
    content = f.read()           # 全部读取
    f.seek(0)
    line = f.readline()          # 读取一行
    f.seek(0)
    all_lines = f.readlines()    # 读取所有行

# 逐行读取（推荐）
with open("example.txt", "r", encoding="utf-8") as f:
    for line in f:
        print(line.strip())

# 追加
with open("example.txt", "a", encoding="utf-8") as f:
    f.write("追加的内容\n")

# 二进制模式
with open("image.jpg", "rb") as f:
    data = f.read()

with open("copy.jpg", "wb") as f:
    f.write(data)

# 上下文管理器 with
# 自动关闭文件, 即使发生异常
```

## 十一、异常处理

```python
try:
    result = 10 / 0
except ZeroDivisionError:
    print("除数不能为0")
except (ValueError, TypeError) as e:
    print(f"类型错误: {e}")
else:
    print("没有异常时执行")
finally:
    print("无论是否异常都执行")

# 自定义异常
class MyError(Exception):
    pass

raise MyError("自定义错误信息")

# 断言
assert x > 0, "x 必须大于0"
```

## 十二、模块与包

```python
# 导入模块
import math
from datetime import datetime, timedelta
from collections import defaultdict as dd

# __name__ 用法
if __name__ == "__main__":
    # 仅当直接运行此文件时执行
    main()
```

> 本文涵盖了 Python 最常用的基础语法。每个知识点都配有代码示例，建议读者在 Python 环境中亲自运行验证。
