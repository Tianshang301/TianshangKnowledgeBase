---
aliases: [RaspberryPi项目实践]
tags: ['HardwareAndEmbeddedSystems', 'RaspberryPi', 'RaspberryPi项目实践']
---

# RaspberryPi项目实践

## 一、Raspberry Pi平台概述

Raspberry Pi是树莓派基金会推出的单板计算机，广泛应用于嵌入式、教育和物联网项目。

各代产品对比：

| 型号 | SoC | RAM | CPU核心 | GPU | 网络 | USB | GPIO |
|------|-----|-----|---------|-----|------|-----|------|
| Pi 4B | BCM2711 | 1-8GB | 4xA72 1.5GHz | VideoCore VI | GbE+WiFi5 | 2xUSB3+2xUSB2 | 40pin |
| Pi 3B+ | BCM2837B0 | 1GB | 4xA53 1.4GHz | VideoCore IV | GbE+WiFi5 | 4xUSB2 | 40pin |
| Pi Zero 2W | RP3A0 | 512MB | 4xA53 1GHz | VideoCore IV | WiFi4 | 1xOTG | 40pin |
| Pi Pico | RP2040 | 264KB | 2xM0+ 133MHz | - | - | - | 26pin |
| Pi 5 | BCM2712 | 4-8GB | 4xA76 2.4GHz | VideoCore VII | GbE+WiFi5 | 2xUSB3+2xUSB2 | 40pin |

## 二、系统安装与配置

烧录系统到SD卡：

```bash
# 使用Raspberry Pi Imager（推荐）
sudo dd if=raspios-arm64.img of=/dev/sdX bs=4M status=progress

# 启用SSH
touch /boot/ssh

# 配置WiFi
cat > /boot/wpa_supplicant.conf << EOF
country=CN
ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1
network={
    ssid="YOUR_SSID"
    psk="YOUR_PASSWORD"
    key_mgmt=WPA-PSK
}
EOF
```

系统初始化：

```bash
# 更新系统
sudo apt update && sudo apt upgrade -y

# 安装常用工具
sudo apt install -y git vim htop screen tree build-essential

# 配置raspi-config
sudo raspi-config
```

## 三、GPIO编程基础

使用RPi.GPIO库控制GPIO：

```python
import RPi.GPIO as GPIO
import time

LED_PIN = 18
BUTTON_PIN = 17

GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN, GPIO.OUT)
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def button_callback(channel):
    print("Button pressed on channel", channel)
    GPIO.output(LED_PIN, not GPIO.input(LED_PIN))

GPIO.add_event_detect(
    BUTTON_PIN,
    GPIO.FALLING,
    callback=button_callback,
    bouncetime=200
)

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    GPIO.cleanup()
```

GPIO引脚功能分布：

| 功能 | 引脚号 | 功能 | 引脚号 |
|------|--------|------|--------|
| 3.3V | 1 | 5V | 2 |
| SDA (I2C) | 3 | 5V | 4 |
| SCL (I2C) | 5 | GND | 6 |
| GPIO 4 | 7 | TXD (UART) | 8 |
| GND | 9 | RXD (UART) | 10 |
| GPIO 17 | 11 | GPIO 18 | 12 |
| GPIO 27 | 13 | GND | 14 |
| GPIO 22 | 15 | GPIO 23 | 16 |

## 四、I2C传感器采集

通过I2C总线连接传感器：

```python
import smbus2
import time

BMP280_ADDR = 0x76
bus = smbus2.SMBus(1)

def read_bmp280():
    # 读取温度原始值
    temp_msb = bus.read_byte_data(BMP280_ADDR, 0xFA)
    temp_lsb = bus.read_byte_data(BMP280_ADDR, 0xFB)
    temp_xlsb = bus.read_byte_data(BMP280_ADDR, 0xFC)

    temp_raw = (temp_msb << 12) | (temp_lsb << 4) | (temp_xlsb >> 4)
    temperature = temp_raw / 100.0

    # 读取气压
    press_msb = bus.read_byte_data(BMP280_ADDR, 0xF7)
    press_lsb = bus.read_byte_data(BMP280_ADDR, 0xF8)
    press_xlsb = bus.read_byte_data(BMP280_ADDR, 0xF9)

    press_raw = (press_msb << 12) | (press_lsb << 4) | (press_xlsb >> 4)
    pressure = press_raw / 100.0

    return temperature, pressure

while True:
    temp, press = read_bmp280()
    print("Temperature:", round(temp, 2), "C, Pressure:", round(press, 2), "hPa")
    time.sleep(1)
```

## 五、摄像头与图像处理

使用Pi Camera Module进行人脸检测：

```python
from picamera2 import Picamera2
import cv2
import numpy as np

picam2 = Picamera2()
picam2.configure(
    picam2.create_preview_configuration(
        main={"size": (640, 480)}
    )
)
picam2.start()

def detect_faces(frame):
    face_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    )
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)

    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

    return frame

try:
    while True:
        frame = picam2.capture_array()
        frame = detect_faces(frame)
        cv2.imshow("Camera", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
finally:
    cv2.destroyAllWindows()
    picam2.stop()
```

## 六、网络编程与Web服务器

使用Flask搭建Web控制面板：

```python
from flask import Flask, render_template, request
import RPi.GPIO as GPIO

app = Flask(__name__)

LED_PIN = 18
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN, GPIO.OUT)

@app.route('/')
def index():
    status = GPIO.input(LED_PIN)
    return render_template('index.html', led_status=status)

@app.route('/led/on')
def led_on():
    GPIO.output(LED_PIN, GPIO.HIGH)
    return 'LED ON'

@app.route('/led/off')
def led_off():
    GPIO.output(LED_PIN, GPIO.LOW)
    return 'LED OFF'

@app.route('/api/sensor')
def sensor_data():
    temp, press = read_bmp280()
    return {
        'temperature': temp,
        'pressure': press,
        'unit': 'C'
    }

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
```

## 七、GPIO扩展与外设

常见扩展模块：

| 模块 | 接口 | 功能 | 驱动方式 |
|------|------|------|----------|
| MCP3008 | SPI | 8通道ADC | spidev |
| ADS1115 | I2C | 16位ADC | Adafruit_ADS1x15 |
| PCA9685 | I2C | 16通道PWM | Adafruit_PCA9685 |
| RFID-RC522 | SPI | RFID读取 | MFRC522-python |
| PCF8574 | I2C | IO扩展 | smbus |

使用MCP3008读取模拟信号：

```python
import spidev

spi = spidev.SpiDev()
spi.open(0, 0)
spi.max_speed_hz = 1350000

def read_adc(channel):
    adc = spi.xfer2([1, (8 + channel) << 4, 0])
    data = ((adc[1] & 3) << 8) + adc[2]
    return data

def convert_voltage(raw, vref=3.3):
    return raw * vref / 1023.0

channel_0 = read_adc(0)
voltage = convert_voltage(channel_0)
print("ADC Value:", channel_0, "Voltage:", round(voltage, 3))
```

## 八、低功耗与远程访问

远程访问方案：

```bash
# VNC远程桌面
sudo apt install -y realvnc-vnc-server realvnc-vnc-viewer
sudo systemctl enable vncserver-x11-serviced
sudo systemctl start vncserver-x11-serviced

# SSH远程隧道
ssh -R 52698:localhost:22 pi@remote-server.com

# 使用systemd管理自启动服务
cat > /etc/systemd/system/webcontrol.service << EOF
[Unit]
Description=Web Control Panel
After=network.target

[Service]
ExecStart=/usr/bin/python3 /home/pi/webapp.py
WorkingDirectory=/home/pi
Restart=always
User=pi

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl enable webcontrol.service
sudo systemctl start webcontrol.service
```

## 九、项目实战：家庭气象站

综合项目实现：

```python
import time
import sqlite3
from datetime import datetime

def init_db():
    conn = sqlite3.connect('weather.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS readings
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  timestamp TEXT,
                  temperature REAL,
                  pressure REAL,
                  humidity REAL)''')
    conn.commit()
    conn.close()

def log_data(temp, press, hum):
    conn = sqlite3.connect('weather.db')
    c = conn.cursor()
    c.execute('INSERT INTO readings (timestamp, temperature, pressure, humidity) VALUES (?, ?, ?, ?)',
              (datetime.now().isoformat(), temp, press, hum))
    conn.commit()
    conn.close()

def get_stats():
    conn = sqlite3.connect('weather.db')
    c = conn.cursor()
    c.execute('''SELECT AVG(temperature), MAX(temperature), MIN(temperature),
                        AVG(pressure), COUNT(*)
                 FROM readings
                 WHERE timestamp > datetime("now", "-1 day")''')
    stats = c.fetchone()
    conn.close()
    return stats

init_db()

while True:
    temp, press = read_bmp280()
    hum = 55.0  # 假设湿度传感器
    log_data(temp, press, hum)
    stats = get_stats()
    print("24h Avg Temp:", round(stats[0], 1), "C, max:", round(stats[1], 1), "C")
    time.sleep(300)  # 每5分钟记录一次
```

## 相关条目

- [[RaspberryPi]]
- [[EmbeddedLinux]]
- [[IoT]]
- [[05_ComputerScience/ProgrammingLanguages/Python/INDEX|Python]]
- [[GPIO]]

## 参考资源

1. Raspberry Pi官方文档：https://www.raspberrypi.com/documentation
2. RPi.GPIO库文档：https://sourceforge.net/p/raspberry-gpio-python
3. Picamera2用户指南：https://github.com/raspberrypi/picamera2
4. Adafruit树莓派教程：https://learn.adafruit.com/category/raspberry-pi
5. 《Raspberry Pi用户指南》Eben Upton 著
6. Raspberry Pi论坛：https://forums.raspberrypi.com
7. PiShrink - SD卡镜像压缩工具
