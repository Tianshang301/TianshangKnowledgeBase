# Arduino

## 一、Arduino 平台概述

Arduino 是一个开源电子原型平台，基于 ATmega 系列微控制器，提供简洁的编程接口和丰富的生态系统。Arduino IDE 使用 C/C++ 简化版语法，降低了嵌入式开发入门门槛。

## 二、常见开发板对比

| 型号 | 主控芯片 | 工作电压 | 数字 I/O | 模拟输入 | 闪存 | SRAM | 时钟频率 |
|------|---------|---------|---------|---------|------|------|---------|
| Uno R3 | ATmega328P | 5V | 14 | 6 | 32 KB | 2 KB | 16 MHz |
| Nano | ATmega328P | 5V | 14 | 8 | 32 KB | 2 KB | 16 MHz |
| Mega 2560 | ATmega2560 | 5V | 54 | 16 | 256 KB | 8 KB | 16 MHz |
| Due | ATSAM3X8E (ARM) | 3.3V | 54 | 12 | 512 KB | 96 KB | 84 MHz |
| ESP32 | Xtensa LX6 | 3.3V | 34 | 15 | 4 MB | 520 KB | 240 MHz |
| Raspberry Pi Pico | RP2040 | 3.3V | 26 | 3 | 2 MB | 264 KB | 133 MHz |

## 三、数字 I/O

数字引脚配置：

```cpp
pinMode(pin, OUTPUT);     // 设置为输出模式
pinMode(pin, INPUT);      // 设置为输入模式
pinMode(pin, INPUT_PULLUP); // 输入模式并启用内部上拉

digitalWrite(pin, HIGH);  // 输出高电平
digitalWrite(pin, LOW);   // 输出低电平

int val = digitalRead(pin); // 读取数字电平
```

内部上拉电阻典型值为 20-50 kΩ，可用于避免浮空输入。

## 四、模拟 I/O

### analogRead（）

Arduino 的 ADC 为 10 位分辨率，返回值 0-1023 对应 0-Vref：

```cpp
int sensorValue = analogRead(A0);      // 读取模拟值
float voltage = sensorValue * (5.0 / 1023.0); // 转换为电压
```

ADC 转换公式：

$$V_{in} = V_{ref} \times \frac{\text{value}}{1024}$$

各型号 ADC 规格对比：

| 型号 | 分辨率 | 通道数 | 参考电压 |
|------|--------|--------|---------|
| Uno/Nano | 10 位 | 6/8 | 5V（默认） |
| Mega 2560 | 10 位 | 16 | 5V（默认） |
| Due | 12 位 | 12 | 3.3V（固定） |
| ESP32 | 12 位 | 15 | 0-3.3V |

### analogWrite（）和 PWM

`analogWrite()` 输出 PWM 信号，分辨率 8 位（0-255）：

```cpp
analogWrite(pin, 128); // 50% 占空比 PWM
```

PWM 占空比计算公式：

$$\text{Duty Cycle} = \frac{\text{value}}{255} \times 100\%$$

PWM 频率默认约 490 Hz（Uno 引脚 5、6 为 980 Hz）。频率可通过修改定时器寄存器调整。

PWM 占空比通用表达式：

$$D = \frac{t_{on}}{T}$$

PWM 周期与频率的关系：

$$T = \frac{1}{f}$$

## 五、串行通信

| 通信协议 | 引脚 | 最大速率 | 距离 | 设备数 |
|---------|------|---------|------|--------|
| UART | TX/RX | 可达 2 Mbps | 短 | 1:1 |
| I2C | SDA/SCL | 400 kbps (Fast Mode) | 短 | 多主机 |
| SPI | MOSI/MISO/SCK/SS | 可达 10 Mbps | 短 | 主从 |

### UART

```cpp
Serial.begin(9600);           // 初始化串口，波特率 9600
Serial.print("Value: ");      // 打印文本
Serial.println(data);         // 打印并换行
Serial.available();           // 检查是否有数据
char c = Serial.read();       // 读取一个字节
```

### I2C（Wire 库）

```cpp
#include <Wire.h>
Wire.begin();                  // 主设备初始化
Wire.beginTransmission(0x68);  // 开始传输到从设备地址
Wire.write(data);              // 发送数据
Wire.endTransmission();        // 结束传输
Wire.requestFrom(address, count); // 请求数据
```

### SPI（SPI 库）

```cpp
#include <SPI.h>
SPI.begin();                   // 初始化 SPI
SPI.beginTransaction(SPISettings(1000000, MSBFIRST, SPI_MODE0));
digitalWrite(SS, LOW);         // 片选使能
SPI.transfer(0xFF);            // 发送并接收一个字节
digitalWrite(SS, HIGH);        // 片选禁用
SPI.endTransaction();
```

## 六、中断

```cpp
attachInterrupt(digitalPinToInterrupt(pin), ISR, mode);
```

| 触发模式 | 触发条件 |
|---------|---------|
| LOW | 低电平触发 |
| CHANGE | 电平变化触发 |
| RISING | 上升沿触发 |
| FALLING | 下降沿触发 |

**ISR 设计原则**：
- ISR 应尽量短小快速
- 避免使用 `delay()` 和 `Serial.print()`
- 使用 `volatile` 修饰共享变量
- 需要 `millis()` 读取时注意精度

### 按键消抖

```cpp
volatile bool pressed = false;
unsigned long lastDebounceTime = 0;

void isr() {
  if (millis() - lastDebounceTime > 50) {
    pressed = true;
    lastDebounceTime = millis();
  }
}
```

## 七、定时器

| 函数 | 分辨率 | 溢出时间 | 用途 |
|------|--------|---------|------|
| `millis()` | 1 ms | 约 50 天 | 通用计时 |
| `micros()` | 4 $\mu$s | 约 70 分钟 | 高精度计时 |
| `delay(ms)` | 1 ms | — | 阻塞延时 |

PWM 频率通过定时器寄存器控制。例如 Uno 的 Timer1（引脚 9、10）：

```cpp
TCCR1B = (TCCR1B & 0xF8) | 0x01; // 设置 prescaler = 1，约 32 kHz

定时器分频系数（Prescaler）与 PWM 频率的关系：

$$f_{PWM} = \frac{f_{clk}}{N \cdot (1 + \text{TOP})}$$

其中 $N$ 为分频系数，$\text{TOP}$ 为计数上限值。在 8 位快速 PWM 模式下 $\text{TOP} = 255$：

| 分频系数 $N$ | CS 位设置 | 16 MHz PWM 频率 |
|-------------|----------|----------------|
| 1 | CSx=001 | 62.50 kHz |
| 8 | CSx=010 | 7.81 kHz |
| 64 | CSx=011 | 976.56 Hz |
| 256 | CSx=100 | 244.14 Hz |
| 1024 | CSx=101 | 61.04 Hz |

## 八、传感器接口

| 传感器 | 类型 | 接口 | 库 |
|--------|------|------|----|
| DHT11/DHT22 | 温湿度 | 单总线 | DHT.h |
| HC-SR04 | 超声波测距 | 数字 I/O | 无（自行实现） |
| PIR (HC-SR501) | 人体红外 | 数字 I/O | 无 |
| BME280 | 温湿度气压 | I2C/SPI | Adafruit_BME280 |
| MPU6050 | 6 轴 IMU | I2C | MPU6050.h |
| DS18B20 | 温度 | 单总线 | OneWire.h |

### HC-SR04 示例

```cpp
digitalWrite(TRIG, LOW); delayMicroseconds(2);
digitalWrite(TRIG, HIGH); delayMicroseconds(10);
digitalWrite(TRIG, LOW);
long duration = pulseIn(ECHO, HIGH);
float distance = duration * 0.034 / 2; // cm
```

## 九、执行器控制

### 舵机

```cpp
#include <Servo.h>
Servo myservo;
myservo.attach(9);        // 信号线接引脚 9
myservo.write(90);        // 转动到 90°
```

### 直流电机（L298N）

| L298N 输入 | 电机状态 |
|-----------|---------|
| IN1=HIGH, IN2=LOW | 正转 |
| IN1=LOW, IN2=HIGH | 反转 |
| IN1=IN2=LOW | 停止 |
| ENA(PWM) | 调速 |

### 步进电机

使用 Stepper 库或 AccelStepper 库控制步进电机的步数和速度。

## 十、电源管理

| 供电方式 | 电压范围 | 说明 |
|---------|---------|------|
| USB | 5V | 开发调试 |
| DC 插头 | 7-12V | 板载稳压器 |
| Vin 引脚 | 7-12V | 同 DC 插头 |
| 3.3V 引脚 | 3.3V | 仅输出，最大 150mA |

低功耗模式：使用 `sleep.h` 库进入空闲/掉电模式，降低功耗至 $\mu$A 级别。

## 十一、项目示例

- **智能家居**：温湿度监测 + 继电器控制 + OLED 显示
- **机器人小车**：L298N 驱动 + HC-SR04 避障 + 红外遥控
- **气象站**：BME280 + 雨量传感器 + LoRa 无线传输
- **可穿戴设备**：MPU6050 姿态检测 + 蓝牙 BLE 传输

## 相关条目

- [[Arduino传感器与执行器]]
- [[RaspberryPi]]
- [[IoT]]
- [[MCU51]]
- [[Robotics]]

## 参考资源

- [Arduino 官方文档](https://www.arduino.cc/reference/)
- 《Arduino Cookbook》（Michael Margolis）
- [Arduino 项目中心](https://projecthub.arduino.cc/)
- ATmega328P 数据手册
