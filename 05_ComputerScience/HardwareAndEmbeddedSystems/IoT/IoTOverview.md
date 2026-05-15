---
aliases: [IoT]
tags: ['05_ComputerScience', 'HardwareAndEmbeddedSystems', 'IoT']
---


# 物联网 IoT Overview

物联网（Internet of Things, IoT）通过传感器、执行器与网络连接，将物理世界对象数字化并实现智能管控。其架构通常分为三层：感知层（传感器/ RFID / 摄像头/ 边缘设备采集数据）、网络层（Wi-Fi / 5G / 蓝牙/ ZigBee / LoRaWAN等协议传输数据）、应用层（云端/ 边缘计算平台处理数据并提供服务）。通信协议多样：MQTT为轻量级消息队列适用于低带宽场景，CoAP基于UDP适合资源受限设备，ZigBee与Z-Wave专注于智能家居组网，LoRaWAN与NB-IoT支撑广域低功耗需求。平台标准包括AWS IoT Core/ Azure IoT Hub/ 阿里云IoT等云平台，以及MQTT/ OPC-UA/ Matter等互联互通标准。应用领域涵盖智能家居（智能音箱/ 照明/ 安防）、工业4.0（预测性维护/ 数字孪生/ 工厂自动化）、智慧城市（智能交通/ 环境监测/ 智能电网）、医疗IoT（远程监护/ 可穿戴设备）。安全与隐私（设备认证/ 数据加密/ 固件更新）是IoT大规模部署的关键挑战。

## 相关条目

- [[MQTT|MQTT协议]]
- [[LoRaWAN|LoRaWAN协议]]
- [[SmartHome|智能家居]]
- [[IndustrialIoT|工业物联网]]
- [[IoTSecurity|物联网安全]]