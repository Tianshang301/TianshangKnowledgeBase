---
aliases: [RaspberryPi]
tags: ['HardwareAndEmbeddedSystems', 'RaspberryPi', 'RaspberryPi']
created: 2026-05-16
updated: 2026-05-16
---

# Raspberry Pi

## 一、Raspberry Pi 概述

Raspberry Pi 是由 Raspberry Pi Foundation 开发的单板计算机，广泛应用于教育、嵌入式开发和 DIY 项目。

### 型号对比

| 型号 | SoC | RAM | 无线 | GPIO | 价格 | 功耗 |
|------|-----|-----|------|------|------|------|
| Pi 5 | BCM2712 (Cortex-A76) | 4/8 GB | Wi-Fi 5 + BT 5.0 | 40-pin | ~$60-80 | 15-27W |
| Pi 4 B | BCM2711 (Cortex-A72) | 1/2/4/8 GB | Wi-Fi 5 + BT 5.0 | 40-pin | ~$35-75 | 7.6-15W |
| Pi 3 B+ | BCM2837B0 (Cortex-A53) | 1 GB | Wi-Fi 5 + BT 4.2 | 40-pin | ~$35 | 5-12W |
| Zero 2W | RP3A0 (Cortex-A53) | 512 MB | Wi-Fi 4 + BT 4.2 | 40-pin | ~$15 | ~1.5W |
| Pi Pico | RP2040 (Dual Cortex-M0+) | 264 KB SRAM | 无 | 26-pin | ~$4 | ~0.3W |
| Pi Pico W | RP2040 | 264 KB SRAM | Wi-Fi 4 | 26-pin | ~$6 | ~0.4W |

功耗计算公式：

$$P = V \times I$$

其中 $V$ 为供电电压，$I$ 为工作电流。

## 二、系统安装

### Raspberry Pi OS

```bash
# 使用 Raspberry Pi Imager 烧录
# 支持 SSH 和 Wi-Fi 预设

# 烧录后启动，默认用户: pi / raspberry
# 启用 SSH（无头模式在 boot 分区创建 ssh 文件）
```

### 无头设置（Headless）

1. 烧录系统到 SD 卡
2. 在 boot 分区创建空的 `ssh` 文件
3. 创建 `wpa_supplicant.conf` 配置 Wi-Fi
```
country=CN
ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
network={
    ssid="YourWiFi"
    psk="YourPassword"
}
```
4. 插入 SD 卡上电，SSH 连接 `raspberrypi.local`

## 三、GPIO 编程

### GPIO 引脚

Raspberry Pi 40-pin GPIO 引出头包含：

| 功能 | 引脚数 | 说明 |
|------|--------|------|
| 数字 I/O | 26 | 可编程通用 IO |
| 电源 | 2 (5V), 2 (3.3V), 8 (GND) | 供电 |
| I2C | 2 (SDA/SCL) | ID_EEPROM 和额外 I2C |
| SPI | 2 组 (MOSI/MISO/SCK/CE) | 高速外围 |
| UART | TX/RX | 串口控制台 |
| PWM | 2 路硬件 PWM | 电机、LED 调光 |

GPIO 输出高电平为 3.3V，最大输出电流约 16 mA（每引脚），总电流不超过 50 mA。

GPIO 电气特性对比：

| 参数 | Pi 5 / Pi 4 | Pi Pico |
|------|------------|---------|
| I/O 电压 | 3.3V | 3.3V |
| 最大每引脚电流 | 16 mA | 50 mA |
| 内部上拉电阻 | 50-65 kΩ | 50-80 kΩ |
| 输出驱动强度 | 可调（2-16 mA） | 固定 |

**时钟速度与性能：**

$$\text{Clock Speed (Hz)} = \text{Base Clock} \times \text{Multiplier}$$

各型号时钟与性能对比：

| 型号 | 默认频率 | 最高超频 | 性能 (DMIPS) |
|------|---------|---------|-------------|
| Pi 5 | 2.4 GHz | 3.0 GHz | ~13500 |
| Pi 4 B | 1.8 GHz | 2.15 GHz | ~4000 |
| Pi 3 B+ | 1.4 GHz | 1.55 GHz | ~2600 |
| Zero 2W | 1.0 GHz | 1.2 GHz | ~2000 |
| Pico | 133 MHz | 266 MHz | 335 |

### RPi.GPIO 库

```python
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)           # 使用 BCM 编号
GPIO.setup(18, GPIO.OUT)         # 设置输出
GPIO.output(18, GPIO.HIGH)       # 输出高电平

GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)
state = GPIO.input(17)           # 读取输入

# PWM
pwm = GPIO.PWM(18, 1000)         # 1 kHz
pwm.start(50)                    # 50% 占空比

GPIO.cleanup()
```

### gpiozero 库

```python
from gpiozero import LED, Button, PWMLED

led = LED(18)
led.on()

btn = Button(17, pull_up=True)
btn.when_pressed = lambda: led.off()

pwm_led = PWMLED(18)
pwm_led.value = 0.5              # 50% 亮度
```

## 四、传感器与执行器接口

| 器件 | 接口 | 库 | 说明 |
|------|------|----|------|
| DHT22 | 单总线 | Adafruit_DHT | 温湿度 |
| BME280 | I2C/SPI | Adafruit_BME280 | 温湿度气压 |
| HC-SR04 | 数字 I/O | gpiozero | 超声波测距 |
| 摄像头 | CSI | picamera2 | 视频/图像 |
| 舵机 | PWM | gpiozero.Servo | 角度控制 |
| 步进电机 | 数字 I/O | gpiozero | 精确位置 |
| 继电器 | 数字 I/O | — | 高压开关 |
| LED 矩阵 | I2C/SPI | luma.led_matrix | 显示 |

```python
# picamera2 示例
from picamera2 import Picamera2
picam2 = Picamera2()
config = picam2.create_still_configuration()
picam2.configure(config)
picam2.start()
picam2.capture_file("photo.jpg")
```

## 五、I2C/SPI/UART 配置

```bash
# 启用接口
sudo raspi-config
# → Interface Options → I2C/SPI/Serial

# I2C 检测
sudo apt install i2c-tools
i2cdetect -y 1

# 查看 SPI 设备
ls /dev/spidev*
```

```python
# I2C 示例（BME280）
import smbus2
bus = smbus2.SMBus(1)
address = 0x76
data = bus.read_i2c_block_data(address, 0xF7, 8)

# SPI 示例
import spidev
spi = spidev.SpiDev()
spi.open(0, 0)
spi.max_speed_hz = 1000000
resp = spi.xfer2([0x00, 0x00])
```

## 六、服务器应用

| 用途 | 软件 | 端口 |
|------|------|------|
| Web 服务器 | Nginx, Apache | 80/443 |
| Node.js 应用 | Node.js + Express | 3000 |
| 文件服务器 | Samba | 445 |
| DNS 过滤 | Pi-hole | 53 |
| 家庭自动化 | Home Assistant | 8123 |
| 容器 | Docker | 各种 |
| 数据库 | MariaDB, PostgreSQL | 3306/5432 |

```bash
# 安装 Pi-hole
curl -sSL https://install.pi-hole.net | bash

# Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
```

## 七、多媒体

| 应用 | 功能 | 命令/库 |
|------|------|---------|
| Kodi | 媒体中心 | `sudo apt install kodi` |
| VLC | 视频播放 | `vlc video.mp4` |
| OMXPlayer | 硬件加速播放 | `omxplayer video.mp4` |
| picamera2 | 摄像头控制 | Python 库 |
| FFmpeg | 视频处理 | `ffmpeg -i input ...` |
| RPi Cam Web Interface | 网络摄像头 | Web 界面 |

硬件加速编解码由 GPU（VideoCore）提供，支持 H.264 编解码。

## 八、集群计算

Raspberry Pi 可以组成低成本集群用于学习和实验：

```bash
# 安装 MPI
sudo apt install mpich

# MPI 程序
mpicc -o hello hello_mpi.c
mpirun -hostfile hosts -np 4 ./hello
```

**Kubernetes 集群**：使用 k3s（轻量级 Kubernetes）在 Pi 集群上部署容器化应用。

## 九、Pico 微控制器

### MicroPython

```python
from machine import Pin, PWM, ADC
import utime

led = Pin(25, Pin.OUT)
led.toggle()

adc = ADC(0)
val = adc.read_u16()

pwm = PWM(Pin(0))
pwm.freq(1000)
pwm.duty_u16(32768)  # 50%
```

### C++ SDK

```c
#include "pico/stdlib.h"
int main() {
    stdio_init_all();
    gpio_init(PICO_DEFAULT_LED_PIN);
    gpio_set_dir(PICO_DEFAULT_LED_PIN, GPIO_OUT);
    while (true) {
        gpio_put(PICO_DEFAULT_LED_PIN, 1);
        sleep_ms(500);
        gpio_put(PICO_DEFAULT_LED_PIN, 0);
        sleep_ms(500);
    }
}
```

**PIO（Programmable I/O）**：RP2040 的独特功能，通过状态机实现自定义 IO 协议。

## 十、电源和配件

- **电源要求**：Pi 5 推荐 5V/5A USB-C PD，Pi 4 推荐 5V/3A USB-C
- **散热**：Pi 5 需主动散热（含散热器 + 风扇）

当 SoC 温度超过 85°C 时触发热节流（Thermal Throttling），内核频率自动降低以保护芯片。温度升高 $\Delta T$ 与功耗的关系：

$$\Delta T = P \times R_{\theta}$$

其中 $R_{\theta}$ 为 SoC 到环境的热阻。

各型号热阻与节流温度对比：

| 型号 | 节流温度 | 强致节流温度 | 典型 $R_{\theta JA}$ |
|------|---------|------------|-------------------|
| Pi 5 | 85°C | 100°C | ~6 °C/W |
| Pi 4 B | 85°C | 100°C | ~8 °C/W |
| Pi 3 B+ | 85°C | 100°C | ~10 °C/W |
| Zero 2W | 85°C | 100°C | ~15 °C/W |

- **存储**：推荐 A2 级别的 microSD 卡，或用 NVMe SSD（Pi 5 支持 PCIe）
- **外壳**：官方外壳含散热，Argon 系列含 SSD 支架

## 相关条目

- [[RaspberryPi 项目实践]]
- [[05_ComputerScience/HardwareAndEmbeddedSystems/EmbeddedLinux/EmbeddedLinux|EmbeddedLinux]]
- [[05_ComputerScience/HardwareAndEmbeddedSystems/IoT/IoT|IoT]]
- [[05_ComputerScience/HardwareAndEmbeddedSystems/Arduino/Arduino|Arduino]]
- [[05_ComputerScience/OperatingSystems/Linux/INDEX|Linux]]

## 参考资源

- [Raspberry Pi 官方文档](https://www.raspberrypi.com/documentation/)
- [RPi.GPIO 库文档](https://sourceforge.net/p/raspberry-gpio-python/wiki/)
- [picamera2 文档](https://github.com/raspberrypi/picamera2)
- [Pico C++ SDK 文档](https://datasheets.raspberrypi.com/pico/raspberry-pi-pico-c-sdk.pdf)
- 《Raspberry Pi Cookbook》（Simon Monk）


