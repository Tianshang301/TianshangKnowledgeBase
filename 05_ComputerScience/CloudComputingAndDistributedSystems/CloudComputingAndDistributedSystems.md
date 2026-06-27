---
aliases: [CloudComputingAndDistributedSystems]
tags: ['CloudComputingAndDistributedSystems', 'CloudComputingAndDistributedSystems']
created: 2026-05-16
updated: 2026-05-13
---

# 云计算与分布式系统完全指南

## 概述

云计算通过网络按需提供计算资源（服务器、存储、数据库、网络、软件等），而分布式系统研究如何将多台计算机组织成一个统一的计算平台。二者相辅相成，是现代互联网基础设施的基石。

---

## 一、云服务模型

### 1.1 服务模型对比

| 模型 | 管理范围 | 用户控制 | 典型场景 | 代表产品 |
|------|---------|----------|----------|----------|
| IaaS | 虚拟机、存储、网络 | 高 | 迁移现有应用 | AWS EC2, GCP Compute Engine |
| PaaS | 运行时、中间件 | 中 | 应用开发部署 | Heroku, Google App Engine |
| SaaS | 完整应用 | 低 | 直接使用 | Gmail, Office 365, Salesforce |
| FaaS | 函数级别 | 非常高 | 事件驱动任务 | AWS Lambda, Cloud Functions |

```
IaaS:                    PaaS:                    SaaS:
┌─────────────┐         ┌─────────────┐         ┌─────────────┐
│  应用        │         │  应用        │         │  应用        │
│  运行时      │         │  运行时      │         │  运行时      │
│  中间件      │         │  中间件      │         │  中间件      │
│  操作系统    │         │  操作系统    │         │  操作系统    │
│  虚拟化      │◄─用户   │  虚拟化      │◄─用户   │  虚拟化      │
│  服务器      │         │  服务器      │         │  服务器      │
│  存储        │         │  存储        │         │  存储        │
│  网络        │         │  网络        │         │  网络        │
└─────────────┘         └─────────────┘         └─────────────┘
   用户管理区             用户管理区             用户管理区
   虚线以下: 云厂商管理    实线以下: 云厂商管理    全部由厂商管理
```

### 1.2 部署模型

| 部署模型 | 定义 | 适用场景 |
|----------|------|----------|
| 公有云 | 第三方提供商通过互联网提供资源 | 初创公司、弹性工作负载 |
| 私有云 | 为单一组织专用构建 | 金融、政府等合规要求高的行业 |
| 混合云 | 公有云 + 私有云协同使用 | 数据敏感+弹性需求并存 |
| 多云 | 使用多个公有云服务 | 避免厂商锁定、灾备 |

---

## 二、虚拟化技术

### 2.1 Hypervisor

Hypervisor（虚拟机监视器）是虚拟化的核心，分为两类：

| 类型 | 架构 | 性能 | 示例 |
|------|------|------|------|
| Type 1 (裸机型) | 直接运行在硬件上 | 高 | VMware ESXi, Xen, KVM, Hyper-V |
| Type 2 (宿主型) | 运行在操作系统之上 | 较低 | VirtualBox, VMware Workstation |

### 2.2 容器 vs 虚拟机

```
虚拟机:                          容器:
┌─────────────────┐             ┌──────────────────────┐
│ App A │ App B   │             │ App A │ App B │ App C│
│ Libs  │ Libs    │             │ Libs  │ Libs  │ Libs │
│ Guest OS│Guest OS│             ├──────┴───────┴──────┤
├───────┴─────────┤             │     容器运行时       │
│   Hypervisor    │             │      (Docker)        │
├─────────────────┤             ├──────────────────────┤
│   宿主机 OS      │             │      宿主机 OS       │
├─────────────────┤             ├──────────────────────┤
│     硬件        │             │       硬件           │
└─────────────────┘             └──────────────────────┘
```

| 特性 | 虚拟机 | 容器 |
|------|--------|------|
| 启动时间 | 分钟级 | 毫秒级 |
| 镜像大小 | GB 级 | MB 级 |
| 隔离级别 | 强（完全隔离） | 进程级隔离（共享内核） |
| 每台机器实例数 | 数十个 | 数百到数千个 |

---

## 三、Docker

### 3.1 核心概念

```
Docker 架构:
┌──────────┐    ┌──────────┐    ┌──────────┐
│  Client  │───▶│  Daemon  │───▶│ Registry │
│  (CLI)   │    │ (dockerd)│    │ (Hub)    │
└──────────┘    └────┬─────┘    └──────────┘
                     │
              ┌──────┴──────┐
              │   Images    │
              │  ┌──────┐   │
              │  │Container│  │
              │  └──────┘   │
              └─────────────┘
```

### 3.2 Dockerfile 示例

```dockerfile
FROM node:18-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=builder /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

### 3.3 Docker Compose

```yaml
version: "3.9"
services:
  app:
    build: .
    ports:
      - "3000:3000"
    environment:
      - DB_HOST=db
      - DB_USER=user
    depends_on:
      - db
  db:
    image: postgres:15
    volumes:
      - pgdata:/var/lib/postgresql/data
    environment:
      POSTGRES_DB: myapp
      POSTGRES_PASSWORD: secret

volumes:
  pgdata:
```

---

## 四、Kubernetes

### 4.1 核心资源

| 资源 | 作用 | 说明 |
|------|------|------|
| Pod | 最小调度单位（一个或多个容器） | 共享网络和存储 |
| Service | 稳定的网络入口 | 负载均衡 + 服务发现 |
| Deployment | 声明式 Pod 管理 | 滚动更新、回滚、扩缩容 |
| Ingress | HTTP/HTTPS 路由 | 域名 + 路径 → Service |
| ConfigMap | 非敏感配置 | 环境变量、配置文件 |
| Secret | 敏感信息 | Base64 编码、etcd 加密 |
| HPA | 自动水平扩缩容 | 基于 CPU/内存/自定义指标 |

### 4.2 Kubernetes 架构

```
┌─────────────────────────────────────────────────┐
│                  Control Plane                   │
│  ┌──────┐  ┌────────┐  ┌──────┐  ┌──────────┐  │
│  │API   │  │Scheduler│  │CM    │  │etcd      │  │
│  │Server│  │         │  │      │  │(键值存储) │  │
│  └──┬───┘  └────────┘  └──────┘  └──────────┘  │
└─────┼───────────────────────────────────────────┘
      │
┌─────┼───────────────────────────────────────────┐
│  ┌──┴──────┐  Node 1                           │
│  │  kubelet│─▶ Pod  │  Pod  │  Pod             │
│  └─────────┘                                    │
│  ┌─────────┐  Node 2                           │
│  │  kubelet│─▶ Pod  │  Pod                      │
│  └─────────┘                                    │
└─────────────────────────────────────────────────┘
```

### 4.3 Ingress 配置

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: myapp-ingress
spec:
  rules:
  - host: api.myapp.com
    http:
      paths:
      - path: /v1
        pathType: Prefix
        backend:
          service:
            name: api-service
            port:
              number: 8080
  - host: www.myapp.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: web-service
            port:
              number: 80
```

---

## 五、分布式系统基础

### 5.1 CAP 定理

CAP 定理指出分布式系统在一致性（Consistency）、可用性（Availability）和分区容错性（Partition Tolerance）三者中最多只能同时满足两个。

```
         一致性 (C)
          /   \
         /     \
        /       \
       /         \
  可用性 (A) ──── 分区容错性 (P)

  CP: 保证一致性和分区容错 → 牺牲可用性（如: Zookeeper, HBase）
  AP: 保证可用性和分区容错 → 牺牲一致性（如: Cassandra, DNS）
  CA: 保证一致性和可用性 → 实际上在分布式系统中无法实现
```

### 5.2 时钟同步

| 机制 | 原理 | 精度 | 使用场景 |
|------|------|------|----------|
| NTP | 层级时间服务器同步 | 毫秒级 | 大多数分布式系统 |
| Lamport 时钟 | 逻辑时钟（因果关系） | 无物理时间 | 事件排序 |
| 向量时钟 | 多节点逻辑时钟 | 可检测冲突 | 版本控制（Dynamo, Riak） |

Lamport 时钟规则:
1. 每个事件发生时，$C_i = C_i + 1$
2. 发送消息时附带 $C_i$
3. 接收时 $C_j = \max(C_j, C_{msg}) + 1$

### 5.3 共识算法

| 算法 | 容错 | 性能 | 特点 | 生产使用 |
|------|------|------|------|----------|
| Paxos | $n/2$ | 中等 | 理论基石，理解困难 | Google Chubby |
| Raft | $n/2$ | 中等（与 Paxos 相近） | 易理解，强领导者 | etcd, Consul, TiKV |
| Zab | $n/2$ | 中等 | 类似 Paxos，用于 ZK | Apache ZooKeeper |
| PBFT | $n/3$ | 较低 | 拜占庭容错 | Hyperledger Fabric |

```
Raft 领导者选举:
  节点状态: Follower → Candidate → Leader
  Term: 选举周期
  超时时间: 150-300ms (随机)
  获得多数票 → 成为 Leader
  Leader 发送心跳维持权威
```

---

## 六、分布式存储

| 系统 | 类型 | 特点 | 适用场景 |
|------|------|------|----------|
| HDFS | 分布式文件系统 | 大文件、高吞吐、流式访问 | Hadoop 生态、数据湖 |
| Ceph | 分布式存储 | 统一存储（块/文件/对象） | OpenStack、云存储 |
| MinIO | 对象存储 | S3 兼容、高性能、轻量级 | 私有云、AI 数据存储 |
| Cassandra | NoSQL 数据库 | AP 系统、宽表、去中心化 | 时序数据、IoT |

---

## 七、无服务器计算 (Serverless)

### 7.1 AWS Lambda

```python
import json
import boto3

def handler(event, context):
    """AWS Lambda 函数处理 S3 事件"""
    # 从 event 中获取 S3 对象信息
    bucket = event["Records"][0]["s3"]["bucket"]["name"]
    key = event["Records"][0]["s3"]["object"]["key"]
    
    # 处理文件
    s3 = boto3.client("s3")
    response = s3.get_object(Bucket=bucket, Key=key)
    content = response["Body"].read().decode("utf-8")
    
    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": f"Processed {key} from {bucket}",
            "lines": len(content.splitlines())
        })
    }
```

### 7.2 冷启动

函数冷启动（Cold Start）是 Serverless 的主要挑战。首次调用或闲置后调用需要加载运行时。

```
冷启动延迟因素:
  - 代码包大小 (zip 越大 → 越慢)
  - 运行时 (Java/C# > Python/Node.js)
  - VPC 配置 (需要创建 ENI)
  - 依赖项数量

优化策略:
  - 预热 (定期调用保持热实例)
  - 使用 Provisioned Concurrency
  - 减少依赖包大小
  - 使用 SnapStart (Java)
```

---

## 八、主流云厂商对比

| 服务 | AWS | Azure | GCP | Alibaba Cloud |
|------|-----|-------|-----|---------------|
| 计算 | EC2 | VM | Compute Engine | ECS |
| 容器 | EKS | AKS | GKE | ACK |
| 函数 | Lambda | Functions | Cloud Functions | FC |
| 数据库 | RDS | SQL Database | Cloud SQL | RDS |
| 对象存储 | S3 | Blob | Cloud Storage | OSS |
| 全球区域 | 30+ | 60+ | 40+ | 30+ |
| 市场份额 | ~32% | ~23% | ~11% | ~4% |

---

## 九、云原生设计模式

| 模式 | 描述 | 解决什么问题 |
|------|------|-------------|
| 断路器 (Circuit Breaker) | 失败快速回退，避免级联故障 | 服务雪崩 |
| 重试 + 退避 (Retry with Backoff) | 可失败操作自动重试，指数退避 | 临时网络问题 |
| 舱壁 (Bulkhead) | 隔离资源池，防止故障蔓延 | 资源隔离 |
| 事件溯源 (Event Sourcing) | 以事件序列存储状态变更 | 审计日志、历史重建 |
| CQRS | 读写分离架构 | 读写负载不均衡 |
| 边车 (Sidecar) | 主容器旁运行辅助容器 | 日志收集、服务网格 |
| 优雅降级 (Graceful Degradation) | 部分功能失败时提供降级体验 | 高可用 |

---

## 相关条目

- [[ComputerNetworks]]
- [[BigDataTechnologies]]
- [[Cybersecurity]]
- Virtualization

## 参考资源

- 《Designing Data-Intensive Applications》— Martin Kleppmann
- 《Kubernetes in Action》— Marko Lukša
- 《分布式系统：概念与设计》— Coulouris 等
- AWS Well-Architected Framework
- Docker 官方文档: https://docs.docker.com
- Kubernetes 官方文档: https://kubernetes.io/docs
