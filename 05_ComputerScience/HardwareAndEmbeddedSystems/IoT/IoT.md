---
aliases: [IoT]
tags: ['HardwareAndEmbeddedSystems', 'IoT', 'IoT']
created: 2026-05-16
updated: 2026-05-13
---

# 物联网（IoT）

## 一、IoT 架构

| 层级 | 功能 | 技术/组件 |
|------|------|-----------|
| 感知层 | 数据采集 | 传感器、执行器、RFID |
| 网络层 | 数据传输 | Wi-Fi, BLE, LoRaWAN, 5G |
| 平台层 | 数据管理和处理 | AWS IoT, Azure IoT, ThingsBoard |
| 应用层 | 业务逻辑和呈现 | Web/移动应用、仪表盘、自动化 |

## 二、通信协议

| 协议 | 传输层 | 架构 | QoS | 适用场景 |
|------|--------|------|-----|---------|
| MQTT | TCP | 发布/订阅 | 3 级 QoS | 低带宽、不可靠网络 |
| CoAP | UDP | 请求/响应 | 弱 | 资源极度受限设备 |
| HTTP/HTTPS | TCP | 请求/响应 | — | Web 集成 |
| AMQP | TCP | 点对点/发布订阅 | 可靠 | 企业级消息系统 |

### MQTT 详解

MQTT 基于发布/订阅模式，通过 Broker 中转消息：

- **QoS 0**：最多一次（At most once），不确认
- **QoS 1**：至少一次（At least once），确认重传
- **QoS 2**：恰好一次（Exactly once），四步握手

```python
# Paho MQTT 客户端示例
import paho.mqtt.client as mqtt

def on_connect(client, userdata, flags, rc):
    client.subscribe("sensor/temperature")

def on_message(client, userdata, msg):
    print(f"{msg.topic}: {msg.payload}")

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect("broker.emqx.io", 1883, 60)
client.loop_forever()
```

## 三、硬件平台对比

| 平台 | 处理器 | 无线连接 | 价格 | 功耗 | 适用场景 |
|------|--------|---------|------|------|---------|
| ESP32 | Xtensa LX6 | Wi-Fi + BLE | ~$3 | 中 | 通用 IoT |
| Raspberry Pi 4/5 | ARM Cortex-A | 无（可外接） | ~$35-80 | 高 | 边缘网关 |
| Arduino Uno | ATmega328P | 无 | ~$5 | 低 | 传感器采集 |
| STM32 | ARM Cortex-M | 可选 | ~$2-10 | 低 | 工业控制 |
| nRF52840 | ARM Cortex-M4F | BLE + Thread | ~$5 | 极低 | 可穿戴 |

## 四、传感器与执行器

| 传感器类型 | 常见型号 | 接口 | 测量范围 |
|-----------|---------|------|---------|
| 温度/湿度 | DHT22, BME280, SHT30 | 单总线/I2C | -40~80°C, 0~100%RH |
| 气压 | BMP280, LPS22HB | I2C/SPI | 300~1100 hPa |
| 运动 | MPU6050, LSM6DS3 | I2C | 6/9 轴 |
| 气体 | MQ-2, MQ-135 | 模拟 | 可燃气体/空气质量 |
| 距离 | HC-SR04, VL53L0X | 数字/I2C | 2cm~4m |
| GPS | NEO-6M, u-blox | UART | 全球定位 |

| 执行器类型 | 控制方式 | 典型应用 |
|-----------|---------|---------|
| 继电器 | 数字 I/O 通断 | 家电开关 |
| 直流电机 | PWM + H 桥 | 风扇、车轮 |
| 舵机 | PWM 脉冲 | 阀门、云台 |
| 步进电机 | 脉冲序列 | 精确定位 |

## 五、边缘计算 vs 云计算

| 特性 | 边缘计算 | 云计算 |
|------|---------|--------|
| 延迟 | 毫秒级 | 数十毫秒以上 |
| 带宽 | 节约 | 需要大量带宽 |
| 离线能力 | 支持 | 不支持 |
| 计算能力 | 有限 | 几乎无限 |
| 数据隐私 | 本地处理 | 上传到云端 |
| 管理复杂度 | 分布式管理 | 集中管理 |

边缘计算适用于实时控制（如工业机器人），云计算适用于大规模数据分析和模型训练。

## 六、IoT 连接技术

| 技术 | 频段 | 速率 | 距离 | 功耗 | 适用场景 |
|------|------|------|------|------|---------|
| Wi-Fi 6 | 2.4/5 GHz | 高达 9.6 Gbps | ~50m | 中 | 家庭/办公室 |
| BLE 5.0 | 2.4 GHz | 2 Mbps | ~100m | 极低 | 可穿戴、信标 |
| Zigbee 3.0 | 2.4 GHz | 250 kbps | ~100m | 低 | 智能家居 |
| LoRaWAN | Sub-GHz | 0.3-50 kbps | ~5-15 km | 极低 | 广域传感器 |
| NB-IoT | LTE 频段 | 200 kbps | ~10-15 km | 低 | 表计、停车 |
| 5G | 毫米波/Sub-6 | Gbps 级 | ~100-500m | 中 | 自动驾驶、URLLC |

## 七、IoT 平台

| 平台 | 类型 | 特点 | 计费 |
|------|------|------|------|
| AWS IoT Core | 公有云 | Device Shadow, Rules Engine, Greengrass | 按消息量 |
| Azure IoT Hub | 公有云 | Device Twins, IoT Edge | 按消息量 |
| ThingsBoard | 开源 | 设备管理、仪表盘、规则链 | 免费/企业版 |
| Home Assistant | 开源 | 智能家居集成、本地控制 | 免费 |
| Blynk | SaaS | 低代码、移动端仪表盘 | 按设备数 |

## 八、数据流水线

```
传感器 → 边缘采集 → MQTT Broker → 数据摄取 → 时序数据库 → 分析/可视化
```

**时序数据库**：InfluxDB、TimescaleDB 专门存储和处理时间序列数据，支持高写入吞吐量和降采样查询。

## 九、IoT 安全

| 安全威胁 | 防护措施 |
|---------|---------|
| 设备仿冒 | 设备证书、TLS 双向认证 |
| 数据窃听 | TLS/DTLS 加密传输 |
| 固件篡改 | 安全启动、固件签名 |
| 拒绝服务（DDoS） | 限流、异常检测 |
| 侧信道攻击 | 物理防护、屏蔽 |

```bash
# Mosquitto MQTT Broker 启用 TLS
listener 8883
cafile /etc/mosquitto/certs/ca.crt
certfile /etc/mosquitto/certs/server.crt
keyfile /etc/mosquitto/certs/server.key
require_certificate true
```

## 十、案例

| 领域 | 应用场景 | 关键技术 |
|------|---------|---------|
| 智能家居 | 灯光/空调/安防控制 | ESP32, MQTT, Home Assistant |
| 工业 IoT | 设备监控、预测性维护 | PLC, OPC UA, Edge Computing |
| 智慧农业 | 温湿度监测、自动灌溉 | LoRaWAN, Soil Sensor, Actuator |
| 智慧城市 | 停车、照明、垃圾管理 | NB-IoT, 5G, Cloud Platform |

## 相关条目

- [[WirelessNetworks]]
- EmbeddedSystems
- [[Cybersecurity]]
- CloudComputing

## 参考资源

- [MQTT 官方规范](https://mqtt.org/)
- [AWS IoT 文档](https://docs.aws.amazon.com/iot/)
- 《Building the Internet of Things》（Maciej Kranz）
- [ThingsBoard 文档](https://thingsboard.io/docs/)
- [ESP-IDF 编程指南](https://docs.espressif.com/projects/esp-idf/)
