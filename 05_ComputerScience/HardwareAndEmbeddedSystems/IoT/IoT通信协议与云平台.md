# IoT通信协议与云平台

## 一、IoT通信协议概述

物联网设备的通信协议选择取决于带宽、功耗、延迟和传输距离需求。

协议分层：

```
应用层:    MQTT / CoAP / HTTP / AMQP
传输层:    TCP / UDP
网络层:    IPv4 / IPv6 / 6LoWPAN
链路层:    WiFi / BLE / LoRa / NB-IoT / Zigbee
物理层:    2.4GHz / Sub-GHz / Cellular
```

## 二、近距离无线通信协议

| 协议 | 频段 | 速率 | 距离 | 功耗 | 拓扑 |
|------|------|------|------|------|------|
| WiFi 6 | 2.4/5GHz | 600-9600Mbps | 50-100m | 高 | 星型 |
| BLE 5.0 | 2.4GHz | 1-2Mbps | 10-100m | 极低 | 星型/广播 |
| Zigbee 3.0 | 2.4GHz | 250kbps | 10-100m | 低 | 网状 |
| Z-Wave | 800-900MHz | 100kbps | 30m | 低 | 网状 |
| Thread | 2.4GHz | 250kbps | 30m | 低 | 网状 |

BLE连接与通信示例：

```cpp
// ESP32 BLE 客户端扫描
#include <BLEDevice.h>
#include <BLEUtils.h>
#include <BLEScan.h>

class MyAdvertisedDeviceCallbacks: public BLEAdvertisedDeviceCallbacks {
    void onResult(BLEAdvertisedDevice advertisedDevice) {
        Serial.printf("设备: %s, RSSI: %d\n",
            advertisedDevice.getAddress().toString().c_str(),
            advertisedDevice.getRSSI());

        if (advertisedDevice.haveServiceUUID() &&
            advertisedDevice.getServiceUUID().equals(BLEUUID(SERVICE_UUID))) {
            advertisedDevice.getScan()->stop();
        }
    }
};

void setup() {
    Serial.begin(115200);
    BLEDevice::init("ESP32_BLE_Scanner");

    BLEScan* pBLEScan = BLEDevice::getScan();
    pBLEScan->setAdvertisedDeviceCallbacks(new MyAdvertisedDeviceCallbacks());
    pBLEScan->setActiveScan(true);
    pBLEScan->setInterval(100);
    pBLEScan->setWindow(99);
    pBLEScan->start(30, false);
}
```

## 三、远距离低功耗网络

LPWAN技术对比：

| 特性 | LoRaWAN | NB-IoT | Sigfox |
|------|---------|--------|--------|
| 频段 | Sub-GHz | LTE频段 | Sub-GHz |
| 最大速率 | 50kbps | 250kbps | 100bps |
| 最大距离 | 2-15km | 1-10km | 3-50km |
| 电池寿命 | 5-10年 | 5-10年 | 5-10年 |
| 带宽 | 125/250/500kHz | 180kHz | 100Hz |
| 定位 | TDOA | 基站定位 | RSSI |
| 部署方式 | 私有/公共 | 运营商 | 运营商 |
| 标准 | LoRaWAN | 3GPP R13 | 私有 |

LoRaWAN数据速率计算公式：

$$
DR = SF \times \frac{BW}{2^{SF}} \times CR
$$

其中SF为扩频因子（7-12），BW为带宽，CR为编码率（4/5至4/8）。

```cpp
// LoRaWAN节点发送示例（Arduino + LoRa模块）
#include <MKRWAN.h>

LoRaModem modem;

void setup() {
    Serial.begin(115200);
    if (!modem.begin(EU868)) {
        Serial.println("LoRa模块初始化失败");
        while (1) {}
    }

    int connected = modem.joinOTAA(
        " APPEUI ",
        " APPKEY "
    );

    if (!connected) {
        Serial.println("OTAA入网失败");
        while (1) {}
    }

    modem.setPort(3);
    modem.beginPacket();
    modem.print("Hello LoRaWAN!");
    int err = modem.endPacket(true);
    if (err > 0) {
        Serial.println("发送成功");
    }
}

void loop() {
    modem.poll();
    if (modem.available()) {
        String msg;
        modem.read(msg);
        Serial.println("收到: " + msg);
    }
}
```

## 四、MQTT协议

MQTT是轻量级的发布/订阅消息协议，物联网的事实标准。

```
发布者 (Publisher)  -->  Broker (代理服务器)  -->  订阅者 (Subscriber)
```

MQTT报文结构：

```
固定头部: 控制包类型 + 标志位
可变头部: 协议名、协议级别、连接标志、心跳间隔
负载:    消息内容
```

```cpp
// ESP32 MQTT客户端示例
#include <WiFi.h>
#include <PubSubClient.h>

const char* ssid = "WiFi_SSID";
const char* password = "WiFi_PASSWORD";
const char* mqtt_server = "broker.emqx.io";
const int mqtt_port = 1883;

WiFiClient espClient;
PubSubClient client(espClient);

void callback(char* topic, byte* payload, unsigned int length) {
    Serial.print("主题: ");
    Serial.println(topic);

    String message;
    for (int i = 0; i < length; i++) {
        message += (char)payload[i];
    }
    Serial.println("消息: " + message);

    if (String(topic) == "device/led") {
        if (message == "ON") {
            digitalWrite(LED_BUILTIN, HIGH);
        } else {
            digitalWrite(LED_BUILTIN, LOW);
        }
    }
}

void reconnect() {
    while (!client.connected()) {
        if (client.connect("ESP32Client")) {
            client.subscribe("device/#");
        } else {
            delay(5000);
        }
    }
}

void setup() {
    Serial.begin(115200);
    pinMode(LED_BUILTIN, OUTPUT);

    WiFi.begin(ssid, password);
    while (WiFi.status() != WL_CONNECTED) {
        delay(500);
    }

    client.setServer(mqtt_server, mqtt_port);
    client.setCallback(callback);
}

void loop() {
    if (!client.connected()) {
        reconnect();
    }
    client.loop();

    // 发布传感器数据
    static unsigned long lastPub = 0;
    if (millis() - lastPub > 5000) {
        int sensorValue = analogRead(34);
        client.publish("sensor/temperature",
                       String(sensorValue).c_str());
        lastPub = millis();
    }
}
```

## 五、CoAP协议

CoAP是基于UDP的RESTful协议，专为受限设备设计。

```
CoAP  = HTTP 语义 + UDP 传输 + 重传机制
      + 资源发现 + 观察模式 + 块传输
```

CoAP与HTTP对比：

| 特性 | CoAP | HTTP |
|------|------|------|
| 传输层 | UDP | TCP |
| 请求/响应 | 确认/非确认 | 确认 |
| 方法 | GET/POST/PUT/DELETE | GET/POST/PUT/DELETE |
| URI | coap://host:port/path | http://host:port/path |
| 头部 | 4字节固定头 | 文本头部 |
| QoS | 确认/非确认 | 仅确认 |
| 观察模式 | 内置观察者模式 | WebSocket扩展 |

## 六、IoT云平台对比

| 特性 | AWS IoT Core | Azure IoT Hub | 阿里云IoT | 华为云IoT |
|------|-------------|---------------|-----------|-----------|
| 协议支持 | MQTT/HTTP/WebSocket | MQTT/AMQP/HTTP | MQTT/CoAP/HTTP | MQTT/CoAP/HTTP |
| 设备认证 | X.509/SigV4 | SAS/X.509 | DeviceSecret | X.509/密钥 |
| 规则引擎 | SQL规则 | IoT Edge | 数据流转 | 函数计算 |
| 边缘计算 | Greengrass | IoT Edge | Link IoT Edge | IEF |
| 影子设备 | Device Shadow | Device Twin | 设备影子 | 设备影子 |
| 免费配额 | 250K消息/月 | 8000消息/天 | 100万消息/月 | 100设备 |

设备连接AWS IoT Core示例：

```python
# Python AWS IoT设备SDK
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import json, time

def customCallback(client, userdata, message):
    print(f"收到消息: {message.payload}, 主题: {message.topic}")

myMQTTClient = AWSIoTMQTTClient("myDeviceID")
myMQTTClient.configureEndpoint("xxxxxxxxx-ats.iot.us-east-1.amazonaws.com", 8883)
myMQTTClient.configureCredentials("rootCA.pem", "private.key", "cert.pem")

myMQTTClient.connect()

myMQTTClient.subscribe("device/control", 1, customCallback)

# 发布数据
payload = {
    "temperature": 25.6,
    "humidity": 60.2,
    "timestamp": int(time.time())
}
myMQTTClient.publish("device/sensor", json.dumps(payload), 1)
```

## 七、IoT安全性

常见安全威胁与对策：

| 威胁 | 描述 | 防御措施 |
|------|------|----------|
| 设备劫持 | 物理访问设备 | 安全芯片、防篡改 |
| 中间人攻击 | 拦截通信 | TLS/DTLS加密 |
| 固件逆向 | 分析固件 | 加密固件、安全启动 |
| DDoS攻击 | 大量设备发起流量 | 速率限制、异常检测 |
| 重放攻击 | 重复发送有效数据 | 时间戳、随机数 |

安全认证流程：

```
设备 -> 注册中心 -> 签发证书
设备 -> 平台: 证书/TLS握手
平台 -> 设备: 验证通过
设备 -> 平台: 加密传输数据
```

## 八、数据流与消息队列

IoT数据管道架构：

```
传感器 -> 边缘网关 -> 消息队列 -> 流处理 -> 存储 -> 可视化
                              |
                        规则引擎 -> 告警/动作
```

消息队列选型：

| 产品 | 模型 | 持久化 | 延迟 | 适用场景 |
|------|------|--------|------|----------|
| Kafka | 发布/订阅 | 磁盘 | 低 | 大数据流处理 |
| RabbitMQ | AMQP | 可选 | 低 | 任务分发 |
| MQTT Broker | 发布/订阅 | 可选 | 极低 | 设备消息 |
| Pulsar | 发布/订阅 | 分层存储 | 低 | 混合负载 |

## 相关条目

- [[IoT]]
- [[EmbeddedLinux]]
- [[RaspberryPi]]
- [[Arduino]]
- [[NetworkProtocols]]

## 参考资源

1. MQTT 3.1.1规范：OASIS标准
2. LoRaWAN规范：LoRa Alliance
3. CoAP RFC 7252：IETF标准
4. AWS IoT Core文档：https://docs.aws.amazon.com/iot
5. Azure IoT文档：https://docs.microsoft.com/azure/iot
6. 《物联网：架构、协议与安全》书籍
7. MQTT X客户端工具：https://mqttx.app
