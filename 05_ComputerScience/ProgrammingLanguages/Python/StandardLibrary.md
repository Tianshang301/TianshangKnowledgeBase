---
aliases: [StandardLibrary]
tags: ['ProgrammingLanguages', 'Python', 'StandardLibrary']
---

# Python 标准库常用模块

## 一、os 模块 — 操作系统接口

```python
import os

# 路径操作
os.getcwd()          # 获取当前工作目录
os.chdir("..")       # 更改工作目录
os.listdir(".")      # 列出目录内容
os.mkdir("new_dir")  # 创建目录
os.makedirs("a/b/c", exist_ok=True)  # 创建多层目录

# 文件操作
os.rename("old.txt", "new.txt")
os.remove("file.txt")
os.rmdir("dir")      # 删除空目录
os.removedirs("a/b/c")  # 递归删除

# 路径拼接 (跨平台)
path = os.path.join("folder", "sub", "file.txt")
# 'folder\\sub\\file.txt' (Windows)
# 'folder/sub/file.txt' (Unix)

# 路径信息
os.path.abspath(".")           # 绝对路径
os.path.dirname("a/b/c.txt")   # 'a/b'
os.path.basename("a/b/c.txt")  # 'c.txt'
os.path.split("a/b/c.txt")     # ('a/b', 'c.txt')
os.path.splitext("file.txt")   # ('file', '.txt')
os.path.exists("file.txt")     # 是否存在
os.path.isfile("file.txt")     # 是否是文件
os.path.isdir("dir")           # 是否是目录
os.path.getsize("file.txt")    # 文件大小(字节)
os.path.getmtime("file.txt")   # 修改时间戳

# 环境变量
os.environ["PATH"]             # 获取环境变量
os.environ.get("HOME", "/tmp")
os.environ["MY_VAR"] = "value"  # 设置环境变量

# 执行系统命令
os.system("echo hello")        # 执行命令(不推荐)
os.popen("dir").read()         # 读取命令输出
```

## 二、sys 模块 — 系统参数

```python
import sys

# 命令行参数
# python script.py arg1 arg2
print(sys.argv)         # ['script.py', 'arg1', 'arg2']
script_name = sys.argv[0]
args = sys.argv[1:]

# Python 解释器信息
sys.version             # '3.12.0 (...)'
sys.version_info        # sys.version_info(major=3, minor=12, micro=0)
sys.executable          # Python 解释器路径
sys.platform            # 'win32' / 'linux' / 'darwin'

# 模块搜索路径
sys.path                # 模块搜索路径列表
sys.path.append("/my/modules")
sys.path.insert(0, "/my/modules")

# 标准输入输出
sys.stdin.read()        # 读取标准输入
sys.stdout.write("hello\n")
sys.stderr.write("error\n")

# 退出程序
sys.exit(0)             # 正常退出
sys.exit(1)             # 异常退出

# 递归深度
sys.getrecursionlimit()  # 默认 1000
sys.setrecursionlimit(2000)

# 内存管理
sys.getsizeof([1,2,3])  # 对象大小(字节)
```

## 三、re 模块 — 正则表达式

```python
import re

# re.search - 搜索第一个匹配
text = "我的邮箱是 user@example.com, 电话是 138-0000-0000"
match = re.search(r'\w+@\w+\.\w+', text)
if match:
    print(match.group())      # 'user@example.com'
    print(match.start())      # 匹配起始位置
    print(match.end())        # 匹配结束位置

# re.match - 从开头匹配
print(re.match(r'我的', text))   # 匹配成功
print(re.match(r'邮箱', text))   # None

# re.findall - 找出所有匹配
phones = re.findall(r'\d{3}-\d{4}-\d{4}', text)
emails = re.findall(r'([\w.]+)@([\w.]+)', text)
# [('user', 'example.com')]

# re.sub - 替换
result = re.sub(r'\d{3}-\d{4}-\d{4}', '***-****-****', text)

# re.compile - 编译正则(提高性能)
pattern = re.compile(r'(\d{3})-(\d{4})-(\d{4})')
m = pattern.search("电话: 138-0000-0000")
print(m.groups())       # ('138', '0000', '0000')
print(m.group(1))       # '138'

# 常用正则
r'\d+'               # 数字
r'\w+'               # 单词字符
r'\s+'               # 空白字符
r'^start'            # 以start开头
r'end$'              # 以end结尾
r'[A-Za-z]+'         # 字母
r'[\u4e00-\u9fa5]+'  # 中文字符
r'(?P<name>\w+)@'    # 命名分组

# 标志位
re.IGNORECASE   # 忽略大小写
re.MULTILINE    # 多行模式(^$匹配每行)
re.DOTALL       # . 匹配换行符
re.VERBOSE      # 允许注释和换行
```

## 四、json 模块 — JSON 处理

```python
import json

# Python -> JSON
data = {
    "name": "张三",
    "age": 28,
    "scores": [95, 88, 92],
    "active": True,
    "address": None
}

json_str = json.dumps(data, ensure_ascii=False, indent=2)
print(json_str)

# JSON -> Python
parsed = json.loads(json_str)
print(parsed["name"])   # '张三'

# 文件读写
with open("data.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

with open("data.json", "r", encoding="utf-8") as f:
    loaded = json.load(f)

# 自定义序列化
from datetime import datetime

class CustomEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        if isinstance(obj, set):
            return list(obj)
        return super().default(obj)

data = {
    "time": datetime.now(),
    "tags": {"python", "json"}
}
print(json.dumps(data, cls=CustomEncoder, ensure_ascii=False))
```

## 五、datetime 模块 — 日期时间

```python
from datetime import date, time, datetime, timedelta, timezone

# date
today = date.today()
print(today)                 # 2024-03-15
print(today.year, today.month, today.day)
date.fromisoformat("2024-12-25")

# time
t = time(14, 30, 15)
print(t.hour, t.minute, t.second)

# datetime
now = datetime.now()
utc_now = datetime.utcnow()
dt = datetime(2024, 3, 15, 14, 30, 0, 0)
print(dt.isoformat())  # '2024-03-15T14:30:00'

# timedelta - 时间差
td = timedelta(days=7, hours=3)
future = now + td
past = now - timedelta(days=30)
print(td.days)           # 7
print(td.total_seconds())  # 裸秒数

# strftime - 日期格式化为字符串
print(now.strftime("%Y-%m-%d %H:%M:%S"))      # 2024-03-15 14:30:00
print(now.strftime("%A, %B %d, %Y"))          # Friday, March 15, 2024
print(now.strftime("当前时间: %H点%M分%S秒"))   # 中文格式

# strptime - 字符串解析为日期
date_str = "2024-03-15 14:30:00"
dt = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")

# 时区处理
from zoneinfo import ZoneInfo
with_tz = now.replace(tzinfo=ZoneInfo("Asia/Shanghai"))
print(with_tz)

# 时间戳
timestamp = now.timestamp()
dt_from_ts = datetime.fromtimestamp(timestamp)
```

## 六、collections 模块 — 容器数据类型

```python
from collections import deque, Counter, defaultdict, namedtuple, OrderedDict

# deque - 双端队列 (高效两端操作)
dq = deque([1, 2, 3])
dq.append(4)          # 右侧添加 [1,2,3,4]
dq.appendleft(0)      # 左侧添加 [0,1,2,3,4]
dq.pop()              # 右侧移除
dq.popleft()          # 左侧移除
dq.rotate(1)          # 向右旋转 [4,0,1,2,3]
dq.rotate(-1)         # 向左旋转 [0,1,2,3,4]

# 应用: 固定大小队列
dq = deque(maxlen=5)
for i in range(10):
    dq.append(i)
print(dq)  # deque([5,6,7,8,9], maxlen=5)

# Counter - 计数器
words = "python is awesome and python is fun"
counter = Counter(words.split())
print(counter)              # Counter({'python': 2, 'is': 2, ...})
print(counter.most_common(2))  # [('python', 2), ('is', 2)]

# 合并计数器
c1 = Counter(a=3, b=1)
c2 = Counter(a=1, b=2)
print(c1 + c2)  # Counter({'a': 4, 'b': 3})
print(c1 - c2)  # Counter({'a': 2})

# defaultdict - 默认值字典
dd = defaultdict(int)
dd["a"] += 1        # 不存在时自动初始化为0
print(dd["a"])      # 1
print(dd["b"])      # 0 (自动创建)

dd_list = defaultdict(list)
dd_list["group1"].append("item1")  # 自动创建空列表

dd_set = defaultdict(set)
dd_set["tags"].add("python")

# namedtuple - 命名元组
Point = namedtuple("Point", ["x", "y", "z"])
p = Point(1, 2, 3)
print(p.x, p.y, p.z)   # 1 2 3
print(p[0])             # 1 (也支持索引)

# 带默认值的命名元组
Person = namedtuple("Person", ["name", "age", "city"])
Person.__new__.__defaults__ = ("北京",)  # city 默认值
p1 = Person("张三", 25)
print(p1)  # Person(name='张三', age=25, city='北京')

# OrderedDict - 有序字典 (Python 3.7+ 普通dict也有序)
od = OrderedDict()
od["a"] = 1
od["b"] = 2
od.move_to_end("a")  # 将'a'移到末尾
od.move_to_end("b", last=False)  # 将'b'移到开头
```

## 七、itertools 模块 — 迭代器工具

```python
from itertools import chain, product, permutations, combinations, groupby, cycle, count, repeat, accumulate

# chain - 连接多个迭代器
list(chain([1,2,3], [4,5]))  # [1,2,3,4,5]
list(chain.from_iterable([[1,2], [3,4]]))  # [1,2,3,4]

# product - 笛卡尔积
list(product([1,2], [3,4]))
# [(1,3), (1,4), (2,3), (2,4)]

list(product("AB", repeat=2))
# [('A','A'), ('A','B'), ('B','A'), ('B','B')]

# permutations - 排列
list(permutations([1,2,3], 2))
# [(1,2), (1,3), (2,1), (2,3), (3,1), (3,2)]

# combinations - 组合
list(combinations([1,2,3,4], 2))
# [(1,2), (1,3), (1,4), (2,3), (2,4), (3,4)]

# combinations_with_replacement - 可重复组合
from itertools import combinations_with_replacement
list(combinations_with_replacement([1,2,3], 2))
# [(1,1), (1,2), (1,3), (2,2), (2,3), (3,3)]

# groupby - 分组 (需要预先排序)
data = [("A", 1), ("A", 2), ("B", 3), ("B", 4)]
data.sort(key=lambda x: x[0])
for key, group in groupby(data, key=lambda x: x[0]):
    print(key, list(group))

# cycle, count, repeat
list(zip(range(5), cycle("AB")))  # [(0,'A'),(1,'B'),(2,'A'),(3,'B'),(4,'A')]
list(zip(count(10, 2), "ABC"))    # [(10,'A'),(12,'B'),(14,'C')]
list(repeat("x", 3))              # ['x','x','x']

# accumulate - 累积
list(accumulate([1,2,3,4]))                      # [1,3,6,10]
list(accumulate([1,2,3,4], lambda a,b: a*b))     # [1,2,6,24]
```

## 八、math 模块 — 数学函数

```python
import math

# 常量
math.pi        # 3.141592...
math.e         # 2.718281...
math.inf       # 无穷大
math.nan       # 非数值

# 基础计算
math.ceil(3.2)     # 4 向上取整
math.floor(3.8)    # 3 向下取整
math.trunc(3.7)    # 3 截断取整
math.round(3.5)    # Python内置, 银行家舍入

math.fabs(-3.5)    # 3.5 绝对值
math.factorial(5)  # 120 阶乘
math.gcd(12, 18)   # 6 最大公约数
math.lcm(12, 18)   # 36 最小公倍数 (Python 3.9+)

# 幂和对数
math.pow(2, 10)    # 1024.0
math.sqrt(16)      # 4.0
math.exp(2)        # e^2
math.log(100)      # ln(100)
math.log(100, 10)  # 以10为底的对数
math.log2(1024)    # 10.0
math.log10(100)    # 2.0

# 三角函数
math.sin(math.pi/2)   # 1.0
math.cos(0)           # 1.0
math.tan(math.pi/4)   # 0.999...
math.asin(1)          # π/2
math.radians(180)     # 角度转弧度
math.degrees(math.pi) # 弧度转角度

# 双曲函数
math.sinh, math.cosh, math.tanh

# 特殊函数
math.erf(0)        # 误差函数
math.gamma(5)      # 24.0 (阶乘的一般化)
math.isclose(0.1+0.2, 0.3)  # 浮点数比较
math.isfinite(x)   # 是否有限
math.isinf(x)      # 是否无穷
math.isnan(x)      # 是否非数值
```

## 九、random 模块 — 随机数

```python
import random

# 基础随机
random.random()              # [0.0, 1.0) 之间的浮点数
random.uniform(10, 20)       # [10, 20] 之间的浮点数
random.randint(1, 10)        # [1, 10] 之间的整数
random.randrange(0, 10, 2)   # 从 range(0,10,2) 中随机选一个

# 序列操作
random.choice(["A", "B", "C"])         # 随机选一个
random.choices(["A","B","C"], k=2)     # 有放回选k个
random.sample(["A","B","C","D"], 2)    # 无放回选k个
items = [1, 2, 3, 4, 5]
random.shuffle(items)                  # 原地打乱

# 设置种子 (可复现)
random.seed(42)
print(random.random())  # 每次运行都相同
random.seed(42)
print(random.random())  # 同上

# 分布 (在科学计算中更常用)
random.gauss(0, 1)      # 高斯分布 (均值0, 标准差1)
random.expovariate(1)   # 指数分布
random.betavariate(2, 5) # Beta分布
```

## 十、statistics 模块 — 统计函数

```python
import statistics

data = [1, 2, 3, 4, 5, 5, 6]

# 中心趋势
statistics.mean(data)      # 3.714... 均值
statistics.median(data)    # 4 中位数
statistics.mode(data)      # 5 众数
statistics.median_low(data)  # 4 (偶数个时取下中位数)
statistics.median_high(data) # 4 (偶数个时取上中位数)

# 离散度
statistics.stdev(data)     # 1.799... 样本标准差
statistics.pstdev(data)    # 1.667... 总体标准差
statistics.variance(data)  # 3.238... 样本方差
statistics.pvariance(data) # 2.777... 总体方差

# 注意: 数据量较小时 statistics 模块很方便
# 大数据集建议用 numpy/scipy
```

## 十一、functools 模块 — 函数工具

```python
from functools import lru_cache, partial, wraps, reduce

# lru_cache - 缓存计算结果
@lru_cache(maxsize=128)
def fibonacci(n):
    if n < 2:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

# partial - 偏函数
int_base2 = partial(int, base=2)
print(int_base2("1010"))  # 10

# reduce - 归约
product = reduce(lambda a, b: a * b, [1, 2, 3, 4])
print(product)  # 24

# wraps - 保留原函数元信息
from functools import wraps

def my_decorator(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        print("before")
        result = f(*args, **kwargs)
        print("after")
        return result
    return wrapper

@my_decorator
def hello():
    """Say hello"""
    print("hello")

print(hello.__name__)  # 'hello' (没有wraps会输出'wrapper')
```

> 熟练掌握标准库能大幅提高开发效率。建议重点掌握 os/sys、re、json、datetime、collections 和 itertools, 它们是日常开发中使用最频繁的模块。
