---
aliases: [MakerEducation]
tags: ['CrossDisciplinaryK12', 'STEM', 'MakerEducation']
created: 2026-05-16
updated: 2026-05-16
---

# 创客教育

## 概述

创客教育是培养学生动手能力和创新精神的教育方式。本文档介绍创客空间建设、Arduino/树莓派基础项目、3D 打印应用以及创客文化。
## 创客空间建设

### 基本设备
- **工具设备**：3D 打印机、激光切割机、电烙铁、万用表
- **电子元件**：Arduino、传感器、LED、电阻、导。
- **材料**：木板、塑料板、纸板、布。
- **软件**：设计软件、编程软。
### 安全规范
1. 使用工具前进行安全培训2. 佩戴防护装备
3. 遵守操作规程
4. 保持工作区域整洁

### 组织管理
- 制定使用规则
- 建立预约系统
- 安排指导老师
- 组织展示活动

## Arduino 基础项目

### 项目1：LED 闪烁
```cpp
// 电路连接：LED 正极接引脚13，负极接 GND
void setup() {
  pinMode(13, OUTPUT);
}

void loop() {
  digitalWrite(13, HIGH);
  delay(1000);
  digitalWrite(13, LOW);
  delay(1000);
}
```

### 项目2：温度传感器
```cpp
// 电路连接：温度传感器接模拟引脚 A0
void setup() {
  Serial.begin(9600);
}

void loop() {
  int reading = analogRead(A0);
  float voltage = reading * 5.0 / 1024.0;
  float temperature = (voltage - 0.5) * 100;
  Serial.println(temperature);
  delay(1000);
}
```

### 项目3：超声波测距
```cpp
// 电路连接：Trig 接引脚9，Echo 接引脚10
void setup() {
  Serial.begin(9600);
  pinMode(9, OUTPUT);
  pinMode(10, INPUT);
}

void loop() {
  digitalWrite(9, LOW);
  delayMicroseconds(2);
  digitalWrite(9, HIGH);
  delayMicroseconds(10);
  digitalWrite(9, LOW);
  
  long duration = pulseIn(10, HIGH);
  long distance = duration * 0.034 / 2;
  
  Serial.print("距离: ");
  Serial.print(distance);
  Serial.println(" cm");
  delay(1000);
}
```

## 树莓派基础项目

### 项目1：GPIO 控制 LED
```python
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.OUT)

while True:
    GPIO.output(18, GPIO.HIGH)
    time.sleep(1)
    GPIO.output(18, GPIO.LOW)
    time.sleep(1)
```

### 项目2：读取传感器数据
```python
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.IN)

while True:
    if GPIO.input(17):
        print("检测到物体")
    time.sleep(0.1)
```

## 3D 打印应用

### 设计流程
1. **建模**：使用3D 建模软件设计模型
2. **切片**：将模型转换为打印路径3. **打印**：设置参数，开始打印4. **后处理*：去除支撑，表面处理

### 常用软件
- **建模软件**：Tinkercad、Fusion 360、Blender
- **切片软件**：Cura、PrusaSlicer

### 应用场景
- 原型制作
- 模型制作
- 零件定制
- 艺术创作

## 电子制作

### 基础项目
- LED 电路
- 按钮控制
- 蜂鸣。
- 电机控制

### 传感器项。
- 温度传感。
- 光敏传感。
- 超声波传感器
- 红外传感。
### 综合项目
- 智能小车
- 环境监测。
- 智能家居模型
- 机器。
## 创客文化

### 核心价。
- **开放*：分享设计和代码
- **分享**：交流经验和知识
- **动手实践**：注重实际制。
- **创新创业*：鼓励原创设。
### 创客精神
- 好奇心：对世界充满好。
- 创造力：勇于创。
- 执行力：将想法变为现。
- 合作精神：团队协。
### 发展趋势
- 人工智能
- 物联。
- 生物技。
- 可持续发。
## 参考资。
- Arduino 官网
- 树莓派官。
- 创客社区
- STEM 教育网站

## 相关条目

InterdisciplinaryLearning, [[01_K12/CrossDisciplinaryK12/STEM/INDEX|STEM]], [[00_KnowledgeFramework/Methodology/CriticalThinking|CriticalThinking]], ProjectBasedLearning


