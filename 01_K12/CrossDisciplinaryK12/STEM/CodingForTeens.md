---
aliases: [CodingForTeens]
tags: ['CrossDisciplinaryK12', 'STEM', 'CodingForTeens']
---

# 青少年编程
## 概述

编程是计算思维的核心技能。本文档介绍Scratch图形化编程、Python入门、计算思维以及编程竞赛简介。
## Scratch图形化编程
### 基本概念
- **角色（Sprite）**：程序中的角色。
- **舞台（Stage）**：角色活动的区域
- **脚本（Script）**：控制角色的程序
- **事件（Event）**：触发脚本执行的条件

### 核心模块
| 模块 | 功能 | 示例 |
|------|------|------|
| 运动 | 控制角色移动 | 移动10步、面向方向 |
| 外观 | 改变角色外观 | 说"你好"、切换造型 |
| 声音 | 播放声音 | 播放声音、改变音量 |
| 事件 | 触发脚本 | 当绿旗被点击、当按下空格 |
| 控制 | 控制程序流程 | 重复执行、如果那么 |
| 侦测 | 检测条件 | 碰到边缘、鼠标按下 |
| 运算 | 数学运算 | 加减乘除、随机数 |
| 变量 | 存储数据 | 建立变量、设置变量 |
| 自制积木 | 创建自定义模块 | 制作新积木 |

### 编程实例
```
让角色在舞台上移动：
1. 当绿旗被点击
2. 重复执行
3.   移动10步
4.   如果碰到边缘，就反弹
```

## Python入门

### 基本概念
- **变量**：存储数据的容器
- **数据类型**：整数、浮点数、字符串、列表。
- **运算符**：算术、比较、逻辑运算符。
- **控制结构**：条件语句、循环语句。
### 变量与数据类型
```python
# 变量赋值
name = "小明"
age = 12
height = 1.5

# 数据类型
print(type(name))   # <class 'str'>
print(type(age))    # <class 'int'>
print(type(height)) # <class 'float'>
```

### 条件语句
```python
# if语句
score = 85
if score >= 90:
    print("优秀")
elif score >= 80:
    print("良好")
elif score >= 60:
    print("及格")
else:
    print("不及格")
```

### 循环语句
```python
# for循环
for i in range(10):
    print(i)

# while循环
count = 0
while count < 5:
    print(count)
    count += 1
```

### 函数
```python
# 定义函数
def greet(name):
    print(f"你好，{name}")

# 调用函数
greet("小明")
```

### 编程实例
```python
# 猜数字游戏
import random

target = random.randint(1, 100)
guess = 0

while guess != target:
    guess = int(input("猜一个1-100的数字："))
    if guess < target:
        print("太小了")
    elif guess > target:
        print("太大了")

print("恭喜你猜对了！")
```

## 计算思维

### 核心要素

#### 1. 分解（Decomposition）
- 将复杂问题分解成更小、更易管理的部分
- 示例：将写作文分解为：选题→列提纲→写开头→写正文→写结尾。
#### 2. 模式识别（Pattern Recognition）
- 在问题中识别规律和模式。
- 示例：在数字序列中找规律：2,4,6,8...（每次加2）
#### 3. 抽象（Abstraction）
- 忽略不重要的细节，关注核心信息。
- 示例：用地图表示实际地形，只保留重要信息

#### 4. 算法（Algorithm）
- 设计解决问题的步骤。
- 示例：排序算法、搜索算法。
## 编程竞赛简介
### 主要竞赛

#### NOIP（全国青少年信息学奥林匹克联赛）
- **级别**：省级。
- **内容**：C++编程
- **适合对象**：初中、高中生

#### CSP（计算机软件能力认证）
- **级别**：全国。
- **内容**：编程能力测试。
- **适合对象**：所有学生。
#### NOI（全国青少年信息学奥林匹克竞赛）
- **级别**：国家级
- **内容**：算法设计与编程
- **适合对象**：优秀选手

### 竞赛准备
1. 学习基础算法
2. 多做练习
3. 参加在线评测
4. 组建学习小组

## 参考资料
- Scratch官方网站
- Python官方教程
- 编程学习网站（LeetCode、Codeforces）
- 编程竞赛题库。

## 相关条目

InterdisciplinaryLearning, [[01_K12/CrossDisciplinaryK12/STEM/INDEX|STEM]], [[CriticalThinking]], ProjectBasedLearning
