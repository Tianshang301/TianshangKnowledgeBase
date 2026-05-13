# Kubernetes 深入

## 概述

Kubernetes（K8s）是一个开源的容器编排平台，用于自动部署、扩展和管理容器化应用。它源自 Google 内部系统 Borg，于 2014 年开源，现已成为云原生计算基金会（CNCF）的旗舰项目。

---

## 一、Kubernetes 架构

### 1.1 控制平面 (Control Plane)

| 组件 | 功能 | 说明 |
|------|------|------|
| kube-apiserver | REST API 入口 | 所有组件通信的枢纽，etcd 的唯一访问者 |
| etcd | 分布式键值存储 | 存储集群状态，基于 Raft 共识 |
| kube-scheduler | Pod 调度 | 根据资源需求、约束、亲和性等策略选择节点 |
| kube-controller-manager | 控制器循环 | 包含 Deployment、ReplicaSet、Node 等多个控制器 |

### 1.2 工作节点 (Worker Node)

| 组件 | 功能 |
|------|------|
| kubelet | 节点代理，管理 Pod 生命周期 |
| kube-proxy | 网络代理，实现 Service 的负载均衡 |
| 容器运行时 | 运行容器（containerd、CRI-O、Docker） |

```
                    ┌─────────────────────────────────────┐
                    │          Control Plane               │
                    │  ┌──────────┐  ┌─────────────────┐  │
                    │  │kube-apiserver│    ┌──────────┐  │
                    │  └─────┬────┘  │    │  etcd    │  │
                    │  ┌─────┴────┐  │    └──────────┘  │
                    │  │  scheduler│ │                  │
                    │  └──────────┘  │                  │
                    │  ┌──────────┐  │                  │
                    │  │  c-m     │  │                  │
                    │  └──────────┘  │                  │
                    └────────┼──────┘                  │
                             │                          │
              ┌──────────────┼──────────────┐           │
              │              │              │           │
         ┌────┴────┐   ┌────┴────┐   ┌────┴────┐      │
         │ Node 1  │   │ Node 2  │   │ Node 3  │      │
         │ kubelet │   │ kubelet │   │ kubelet │      │
         │ kube-proxy│  │ kube-proxy│  │ kube-proxy│    │
         │ Pods    │   │ Pods    │   │ Pods    │      │
         └─────────┘   └─────────┘   └─────────┘      │
```

### 1.3 API 请求流程

```
kubectl apply → kube-apiserver (认证/授权/准入控制) → etcd (存储)
    ↓
kube-scheduler (监测未调度的 Pod) → 绑定节点
    ↓
kubelet (监测新调度 Pod) → 容器运行时 → Pod 运行
    ↓
kube-controller-manager (监测状态差异 → 调和)
```

---

## 二、核心对象

### 2.1 工作负载资源

| 资源 | 作用 | 适用场景 |
|------|------|----------|
| Pod | 最小调度单元，1 个或多个容器 | 所有工作负载的基本构建块 |
| Deployment | 声明式 Pod 管理（无状态） | Web 服务、API 后端 |
| StatefulSet | 有状态 Pod 管理 | 数据库、消息队列 |
| DaemonSet | 每个节点运行一个 Pod | 日志收集（Fluentd）、监控（Node Exporter） |
| Job | 一次性任务 | 批处理、数据迁移 |
| CronJob | 定时任务 | 定时备份、报告生成 |

### 2.2 服务发现与网络

| 资源 | 作用 | 说明 |
|------|------|------|
| Service | 稳定的网络端点 | ClusterIP（集群内）、NodePort（节点端口）、LoadBalancer（云负载均衡） |
| Ingress | HTTP/HTTPS 路由 | 基于域名和路径的流量分发 |
| NetworkPolicy | 网络访问控制 | 控制 Pod 间的流量规则 |

### 2.3 配置与存储

| 资源 | 作用 | 说明 |
|------|------|------|
| ConfigMap | 非敏感配置 | 环境变量、配置文件 |
| Secret | 敏感信息 | Base64 编码，支持 etcd 加密 |
| PVC (PersistentVolumeClaim) | 存储请求 | 动态/静态绑定 PV |
| StorageClass | 存储类定义 | 指定后端存储类型（SSD、HDD 等） |

### 2.4 权限与隔离

| 资源 | 作用 |
|------|------|
| Namespace | 逻辑隔离，多租户 |
| RBAC (Role/ClusterRole/RoleBinding/ClusterRoleBinding) | 基于角色的访问控制 |
| ServiceAccount | Pod 的身份标识 |

### 2.5 Deployment 示例

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx-deployment
spec:
  replicas: 3
  selector:
    matchLabels:
      app: nginx
  template:
    metadata:
      labels:
        app: nginx
    spec:
      containers:
      - name: nginx
        image: nginx:1.25
        ports:
        - containerPort: 80
        resources:
          requests:
            cpu: 100m
            memory: 128Mi
          limits:
            cpu: 500m
            memory: 256Mi
        livenessProbe:
          httpGet:
            path: /
            port: 80
        readinessProbe:
          httpGet:
            path: /
            port: 80
```

---

## 三、调度系统

### 3.1 调度策略

| 策略 | 类型 | 描述 |
|------|------|------|
| nodeSelector | 简单选择 | 匹配 Node label |
| NodeAffinity | 高级调度 | requiredDuringScheduling (硬约束) / preferredDuringScheduling (软约束) |
| PodAffinity / PodAntiAffinity | Pod 间亲和性 | 将 Pod 调度到同一/不同节点 |
| Taints and Tolerations | 污点与容忍 | 节点排斥某些 Pod |
| Pod Priority | 优先级调度 | 高优先级 Pod 抢占低优先级 Pod |

### 3.2 默认调度流程

```
Filtering (预选) → Scoring (优选) → Bind (绑定)
  过滤不满足条件的节点    对节点打分    将 Pod 绑定到最优节点

Scheduler 打分策略:
  - SelectorSpreadPriority: 减少同一 Service 的 Pod 分布在同一节点
  - LeastRequestedPriority: 优先调度到资源利用率低的节点
  - BalancedResourceAllocation: 优先选择资源使用均衡的节点
```

---

## 四、网络模型

### 4.1 CNI 与网络架构

Kubernetes 要求每个 Pod 拥有独立的 IP，Pod 间可以直接通信：

```
Pod 网络模型:
  - 每个 Pod 一个 IP（跨节点可直达）
  - 不需要 NAT 转换
  - Pod 内容器共享网络命名空间

主流 CNI 插件:
  - Calico: 基于 BGP 的路由方案，支持 NetworkPolicy
  - Flannel: 覆盖网络，简单易用
  - Cilium: 基于 eBPF，性能优异
  - Weave: 网状网络，自动发现
```

### 4.2 Service 类型对比

| 类型 | 访问范围 | 实现方式 | 典型场景 |
|------|----------|----------|----------|
| ClusterIP | 集群内部 | kube-proxy iptables/IPVS | 内部服务通信 |
| NodePort | 集群外部:NodePort | 每个节点开放端口 | 开发测试、固定端口 |
| LoadBalancer | 公网 | 云厂商 LB + NodePort | 生产环境对外暴露 |
| ExternalName | DNS CNAME | CoreDNS 返回 CNAME | 引入集群外服务 |

### 4.3 kube-proxy 模式

| 模式 | 原理 | 性能 | 特点 |
|------|------|------|------|
| userspace | 用户空间代理 | 低 | 旧版默认，已废弃 |
| iptables | 内核 Netfilter 规则链 | 中 | 规则数量多时更新慢 |
| IPVS | 内核 L4 负载均衡 | 高 | 支持更多调度算法（RR、LC、DH） |

### 4.4 Ingress 与 Gateway API

```
Ingress:
  ┌─────────┐      ┌──────────┐      ┌──────────┐
  │  Client  │ ──▶  │  Ingress  │ ──▶  │ Service  │
  │         │      │ Controller│      │ (ClusterIP)│
  └─────────┘      └──────────┘      └──────────┘

Gateway API (新一代):
  GatewayClass → Gateway → HTTPRoute → Service
  支持: 流量分割、Header 修改、重定向、TLS 终止
```

---

## 五、存储系统

### 5.1 CSI (Container Storage Interface)

CSI 是 Kubernetes 的存储插件标准：

```
Pod → PVC → PV (通过 CSI 驱动动态/静态创建) → 实际存储后端

存储后端示例:
  AWS:       EBS CSI Driver
  GCP:       PD CSI Driver
  NFS:       NFS CSI Driver
  Ceph:      RBD CSI Driver
```

### 5.2 PV/PVC 生命周期

| 阶段 | 说明 |
|------|------|
| Provisioning | 静态（管理员预创建）或动态（StorageClass 自动创建） |
| Binding | PVC 匹配 PV（匹配条件：存储大小、访问模式） |
| Using | Pod 通过 PVC 使用 PV |
| Reclaiming | PV 释放后的处理：Retain（保留）、Delete（删除）、Recycle（已废弃） |

### 5.3 访问模式

| 模式 | 描述 | 适用场景 |
|------|------|----------|
| RWO (ReadWriteOnce) | 单节点读写 | 大部分块存储（EBS、GPD） |
| ROX (ReadOnlyMany) | 多节点只读 | 共享配置、数据集 |
| RWX (ReadWriteMany) | 多节点读写 | 共享文件系统（NFS、EFS） |

---

## 六、自动伸缩

### 6.1 HPA (Horizontal Pod Autoscaler)

```
HPA 工作原理:
  Metrics Server 采集资源指标 → HPA 控制器计算 → 更新 Deployment 的 replicas

计算公式:
  desiredReplicas = ceil[currentReplicas × (currentMetricValue / desiredMetricValue)]

支持的指标:
  - 资源指标: CPU、内存（Metrics Server）
  - 自定义指标: Prometheus Adapter
  - 外部指标: 队列长度（KEDA）
```

### 6.2 VPA (Vertical Pod Autoscaler)

VPA 自动调整 Pod 的 CPU/内存 requests 和 limits：

| 模式 | 行为 |
|------|------|
| Auto | 自动更新资源限制，滚动更新 Pod |
| Initial | 仅创建时设置 |
| Off | 仅提供建议 |

### 6.3 Cluster Autoscaler

| 云平台 | 节点组 |
|--------|--------|
| AWS | Auto Scaling Group |
| GCP | Managed Instance Group |
| Azure | Virtual Machine Scale Set |

---

## 七、Helm 与 Operator

### 7.1 Helm

```
Helm 架构:
  Helm CLI → Tiller (v2) / Helm SDK (v3) → Kubernetes API

Chart 结构:
  mychart/
    Chart.yaml          # 元数据
    values.yaml         # 默认配置
    templates/          # Go Template 模板
    charts/             # 子依赖
    crds/               # CRD 定义
```

### 7.2 Operator 模式

Operator 是使用自定义控制器来管理应用生命周期的模式：

```
CRD (Custom Resource Definition) → 声明期望状态
Controller (控制循环) → 监测差异 → 调和到期望状态

知名 Operator:
  etcd-operator: 管理 etcd 集群
  prometheus-operator: 管理 Prometheus 监控栈
  strimzi: 管理 Kafka 集群
  cert-manager: 自动化 TLS 证书
```

---

## 八、安全机制

### 8.1 安全层级

```
安全层级（从外到内）:
  集群安全: RBAC, 网络策略, 准入控制
  Pod 安全: PodSecurity Admission, SecurityContext
  容器安全: 容器运行时隔离, 镜像扫描
  数据安全: Secret 加密, etcd 加密
```

### 8.2 PodSecurity Admission

| 级别 | 说明 | 限制 |
|------|------|------|
| Privileged | 无限制 | 运行特权容器 |
| Baseline | 最小限制 | 禁止 hostNetwork、hostPID、privileged 等 |
| Restricted | 严格限制 | 强制只读根文件系统、禁止 root 用户 |

### 8.3 Service Account 与 Secret

```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: my-app
---
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  namespace: default
  name: pod-reader
rules:
- apiGroups: [""]
  resources: ["pods"]
  verbs: ["get", "watch", "list"]
---
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: read-pods
subjects:
- kind: ServiceAccount
  name: my-app
roleRef:
  kind: Role
  name: pod-reader
  apiGroup: rbac.authorization.k8s.io
```

---

## 九、故障排查

### 9.1 常用排查命令

| 命令 | 用途 |
|------|------|
| `kubectl get events --sort-by='.lastTimestamp'` | 查看集群事件 |
| `kubectl describe pod <name>` | Pod 详细状态和事件 |
| `kubectl logs <pod> -c <container>` | 查看日志 |
| `kubectl exec -it <pod> -- sh` | 进入容器调试 |
| `kubectl debug -it <pod> --image=busybox` | 创建临时调试容器 |
| `kubectl top pod` | 查看 Pod 资源使用 |

### 9.2 常见问题

```
Pod Pending:
  - 资源不足（CPU/内存）
  - PVC 未绑定
  - Node 有污点没有对应容忍

Pod CrashLoopBackOff:
  - 应用启动失败 → kubectl logs
  - 资源限制太低 → OOMKilled
  - 启动探针失败 → livenessProbe 配置错误

Service 不通:
  - Endpoint 是否正常 → kubectl get endpoints
  - kube-proxy 是否运行
  - DNS 解析 → nslookup <service>.<namespace>
```

### 9.3 临时容器 (Ephemeral Containers)

Kubernetes v1.23+ 支持临时容器用于调试：

```bash
kubectl debug -it mypod --image=nicolaka/netshoot --target=mycontainer
```

临时容器共享目标 Pod 的进程、网络、存储命名空间，适合在 Pod 运行状态下排查网络和文件系统问题。

---

## 相关条目

- CloudComputing
- Containerization
- DevOps
- Microservices

## 参考资源

- 《Kubernetes in Action》— Marko Lukša
- 《Kubernetes: Up and Running》— Brendan Burns 等
- Kubernetes 官方文档: https://kubernetes.io/docs
- CNCF 云原生图谱: https://landscape.cncf.io
- Kelsey Hightower: Kubernetes the Hard Way
- etcd 文档: https://etcd.io/docs
- Helm 文档: https://helm.sh/docs
