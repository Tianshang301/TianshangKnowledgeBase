# Arduino传感器与执行器

## 一、Arduino平台概述

Arduino是基于AVR微控制器的开源电子原型平台。常见开发板对比：

| 型号 | MCU | Flash | SRAM | 工作电压 | 数字IO | 模拟输入 |
|------|-----|-------|------|----------|--------|----------|
| Uno R3 | ATmega328P | 32KB | 2KB | 5V | 14 | 6 |
| Nano | ATmega328P | 32KB | 2KB | 5V | 14 | 8 |
| Mega 2560 | ATmega2560 | 256KB | 8KB | 5V | 54 | 16 |
| Leonardo | ATmega32U4 | 32KB | 2.5KB | 5V | 20 | 12 |
| Due | ATSAM3X8E | 512KB | 96KB | 3.3V | 54 | 12 |

## 二、数字传感器

数字传感器直接输出数字信号，无需ADC转换。

DHT11/DHT22温湿度传感器：

```cpp
#include <DHT.h>

#define DHTPIN 2
#define DHTTYPE DHT11

DHT dht(DHTPIN, DHTTYPE);

void setup() {
  Serial.begin(9600);
  dht.begin();
}

void loop() {
  float h = dht.readHumidity();
  float t = dht.readTemperature();
  
  if (isnan(h) || isnan(t)) {
    Serial.println("传感器读取失败");
    return;
  }
  
  Serial.print("湿度: ");
  Serial.print(h);
  Serial.print(" %\t");
  Serial.print("温度: ");
  Serial.print(t);
  Serial.println(" *C");
  delay(2000);
}
```

超声波测距模块HC-SR04：

```cpp
#define TRIG_PIN 9
#define ECHO_PIN 10

void setup() {
  Serial.begin(9600);
  pinMode(TRIG_PIN, OUTPUT);
  pinMode(ECHO_PIN, INPUT);
}

float measureDistance() {
  digitalWrite(TRIG_PIN, LOW);
  delayMicroseconds(2);
  digitalWrite(TRIG_PIN, HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIG_PIN, LOW);
  
  long duration = pulseIn(ECHO_PIN, HIGH);
  float distance = duration * 0.034 / 2;
  return distance;
}

void loop() {
  float dist = measureDistance();
  Serial.print("距离: ");
  Serial.print(dist);
  Serial.println(" cm");
  delay(500);
}
```

| 传感器 | 接口类型 | 测量范围 | 精度 | 价格 |
|--------|----------|----------|------|------|
| HC-SR04 | 数字脉冲 | 2cm-4m | 3mm | 极低 |
| DHT11 | 单总线 | 20-90%/0-50C | 2C/5% | 极低 |
| DHT22 | 单总线 | 0-100%/-40-80C | 0.5C/2% | 低 |
| DS18B20 | 单总线 | -55-125C | 0.5C | 低 |
| MPU6050 | I2C | 6轴IMU | 中 | 低 |
| BMP280 | I2C/SPI | 300-1100hPa | 1hPa | 低 |

## 三、模拟传感器

模拟传感器输出连续电压，经ADC转换为数字量。Arduino Uno的ADC为10位，分辨率为 $V_{ref}/1024$。

光敏电阻模块：

```cpp
#define LIGHT_SENSOR A0

void setup() {
  Serial.begin(9600);
}

void loop() {
  int raw = analogRead(LIGHT_SENSOR);
  float voltage = raw * (5.0 / 1023.0);
  float resistance = voltage / (5.0 - voltage) * 10000;
  
  Serial.print("原始值: ");
  Serial.print(raw);
  Serial.print(" 电压: ");
  Serial.print(voltage, 2);
  Serial.println(" V");
  delay(500);
}
```

模拟温度传感器LM35：

$$
T(^{\circ}C) = V_{out}(mV) \times 100
$$

---

```cpp
float readLM35(int pin) {
  int raw = analogRead(pin);
  float voltage = raw * (5.0 / 1023.0);
  float temperature = voltage * 100.0;
  return temperature;
}
```

## 四、I2C与SPI传感器

I2C传感器采用地址寻址，使用SDA和SCL引脚。

MPU6050六轴陀螺仪+加速度计：

```cpp
#include <Wire.h>
#include <MPU6050.h>

MPU6050 mpu;

void setup() {
  Serial.begin(9600);
  Wire.begin();
  mpu.initialize();
  
  if (!mpu.testConnection()) {
    Serial.println("MPU6050连接失败");
    while (1);
  }
}

void loop() {
  int16_t ax, ay, az, gx, gy, gz;
  mpu.getMotion6(&ax, &ay, &az, &gx, &gy, &gz);
  
  float ax_g = ax / 16384.0;
  float ay_g = ay / 16384.0;
  float az_g = az / 16384.0;
  
  float pitch = atan2(-ax_g, sqrt(ay_g * ay_g + az_g * az_g)) * 180 / PI;
  float roll = atan2(ay_g, az_g) * 180 / PI;
  
  Serial.print("Pitch: ");
  Serial.print(pitch, 1);
  Serial.print(" Roll: ");
  Serial.println(roll, 1);
  delay(100);
}
```

I2C与SPI对比：

| 特性 | I2C | SPI |
|------|-----|-----|
| 连线数量 | 2 (SDA+SCL) | 4 (MOSI+MISO+SCK+SS) |
| 通信模式 | 半双工 | 全双工 |
| 速度 | 100k-400kHz (最高3.4MHz) | 最高可达数十MHz |
| 寻址 | 7位/10位地址 | 片选信号 |
| 多设备 | 总线式，最多127个 | 每设备需一个片选引脚 |
| 功耗 | 较低 | 较高 |
| 距离 | 较短 | 稍长 |

## 五、执行器控制

直流电机驱动（L298N）：

```cpp
#define ENA 5
#define IN1 6
#define IN2 7

void setup() {
  pinMode(ENA, OUTPUT);
  pinMode(IN1, OUTPUT);
  pinMode(IN2, OUTPUT);
}

void motorForward(int speed) {
  digitalWrite(IN1, HIGH);
  digitalWrite(IN2, LOW);
  analogWrite(ENA, speed);
}

void motorBackward(int speed) {
  digitalWrite(IN1, LOW);
  digitalWrite(IN2, HIGH);
  analogWrite(ENA, speed);
}

void motorStop() {
  digitalWrite(IN1, LOW);
  digitalWrite(IN2, LOW);
  analogWrite(ENA, 0);
}
```

## 六、舵机控制

```cpp
#include <Servo.h>

Servo myservo;
int pos = 0;

void setup() {
  myservo.attach(9);
}

void loop() {
  for (pos = 0; pos <= 180; pos += 1) {
    myservo.write(pos);
    delay(15);
  }
  for (pos = 180; pos >= 0; pos -= 1) {
    myservo.write(pos);
    delay(15);
  }
}
```

舵机控制信号：

$$
\text{脉冲宽度} = \frac{\text{角度}}{180} \times (2000 - 1000) + 1000 \quad \mu s
$$

| 执行器类型 | 控制方式 | 工作电压 | 电流 | 应用 |
|-----------|---------|----------|------|------|
| 直流电机 | PWM | 5-12V | 100mA-数A | 车轮、风扇 |
| 步进电机 | 脉冲序列 | 5-24V | 数百mA | 精确定位 |
| 舵机 | PWM (50Hz) | 4.8-7.2V | 100-500mA | 机械臂、转向 |
| 继电器 | 高低电平 | 5V触发 | 数十mA | 高压开关 |
| LED | PWM | 1.8-3.3V | 10-20mA | 指示、照明 |
| 蜂鸣器 | 高低电平/PWM | 5V | 10-50mA | 报警、提示 |

## 七、传感器数据处理

滑动平均滤波（Moving Average Filter）：

```cpp
#define WINDOW_SIZE 10

class MovingAverage {
private:
  float buffer[WINDOW_SIZE];
  int index = 0;
  float sum = 0;
  int count = 0;

public:
  float addSample(float value) {
    if (count < WINDOW_SIZE) {
      count++;
    } else {
      sum -= buffer[index];
    }
    buffer[index] = value;
    sum += value;
    index = (index + 1) % WINDOW_SIZE;
    return sum / count;
  }
};

MovingAverage filter;

void setup() {
  Serial.begin(9600);
}

void loop() {
  int raw = analogRead(A0);
  float filtered = filter.addSample(raw);
  Serial.println(filtered);
  delay(10);
}
```

## 八、低功耗与电源管理

睡眠模式降低功耗：

```cpp
#include <avr/sleep.h>
#include <avr/power.h>

void enterSleep() {
  set_sleep_mode(SLEEP_MODE_PWR_DOWN);
  sleep_enable();
  power_all_disable();
  sleep_cpu();
  sleep_disable();
  power_all_enable();
}
```

不同模式功耗对比：

| 模式 | 电流消耗 | 唤醒方式 |
|------|----------|----------|
| 活跃模式 | 15-50mA | - |
| 空闲模式 | 6-10mA | 中断 |
| 省电模式 | 1-4mA | 定时器/中断 |
| 掉电模式 | 0.1-1uA | 外部中断 |

## 相关条目

- [[Arduino]]
- [[RaspberryPi]]
- [[IoT]]
- [[Robotics]]
- [[AnalogCircuits]]

## 参考资源

1. Arduino官方文档：https://www.arduino.cc/reference
2. Arduino传感器套件指南
3. Adafruit传感器教程：https://learn.adafruit.com
4. SparkFun传感器入门：https://learn.sparkfun.com
5. 《Arduino权威指南》Massimo Banzi 著
6. MPU6050数据手册
7. HC-SR04数据手册
