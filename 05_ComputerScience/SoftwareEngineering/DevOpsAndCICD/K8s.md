---
aliases: [K8s]
tags: ['SoftwareEngineering', 'DevOpsAndCICD', 'K8s']
created: 2026-05-16
updated: 2026-05-13
---

# Kubernetes 基础

## 一、核心概念

### Pod

Pod 是 K8s 最小的部署单位，包含一个或多个容器。

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: my-pod
  labels:
    app: myapp
    tier: frontend
spec:
  containers:
    - name: app
      image: nginx:alpine
      ports:
        - containerPort: 80
      resources:
        requests:
          cpu: "100m"
          memory: "128Mi"
        limits:
          cpu: "500m"
          memory: "256Mi"
      livenessProbe:
        httpGet:
          path: /health
          port: 80
        initialDelaySeconds: 5
        periodSeconds: 10
      readinessProbe:
        httpGet:
          path: /ready
          port: 80
        initialDelaySeconds: 3
```

### Deployment

Deployment 管理 Pod 的声明式更新和扩缩容。

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: web-deployment
  labels:
    app: web
spec:
  replicas: 3
  selector:
    matchLabels:
      app: web
  template:
    metadata:
      labels:
        app: web
    spec:
      containers:
        - name: nginx
          image: nginx:1.25-alpine
          ports:
            - containerPort: 80
      strategy:
        type: RollingUpdate
        rollingUpdate:
          maxSurge: 1
          maxUnavailable: 1
```

### Service

Service 提供稳定的网络访问点。

```yaml
apiVersion: v1
kind: Service
metadata:
  name: web-service
spec:
  selector:
    app: web
  ports:
    - port: 80
      targetPort: 80
  type: ClusterIP  # ClusterIP | NodePort | LoadBalancer
```

### Namespace

```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: production
---
apiVersion: v1
kind: Namespace
metadata:
  name: staging
```

---

## 二、架构

```
┌──────────────────────────────────────────────────┐
│              Master Node（控制平面）               │
│  ┌─────────┐ ┌──────────┐ ┌──────────────────┐  │
│  │ API     │ │ Scheduler│ │ Controller        │  │
│  │ Server  │ │          │ │ Manager           │  │
│  └────┬────┘ └──────────┘ └──────────────────┘  │
│       │                                          │
│  ┌────▼────┐                                     │
│  │  etcd   │ （分布式键值存储）                    │
│  └─────────┘                                     │
├──────────────────────────────────────────────────┤
│              Worker Node 1                       │
│  ┌─────────┐ ┌─────────┐ ┌─────────┐            │
│  │ Kubelet │ │ Kube-proxy│ │ Container│          │
│  │         │ │          │ │ Runtime │            │
│  └─────────┘ └─────────┘ └─────────┘            │
│  ┌──────┐ ┌──────┐ ┌──────┐                      │
│  │ Pod 1│ │ Pod 2│ │ Pod 3│                      │
│  └──────┘ └──────┘ └──────┘                      │
├──────────────────────────────────────────────────┤
│              Worker Node 2 (同 Node 1)            │
└──────────────────────────────────────────────────┘
```

### 组件说明

| 组件 | 说明 |
|------|------|
| kube-apiserver | 所有组件通信的中心，暴露 REST API |
| etcd | 分布式键值存储，保存集群状态 |
| kube-scheduler | 将 Pod 调度到合适的 Worker Node |
| kube-controller-manager | 运行各种控制器（Deployment, ReplicaSet 等） |
| kubelet | 每个节点上的代理，管理 Pod 和容器 |
| kube-proxy | 网络代理，实现 Service 负载均衡 |
| 容器运行时 | containerd / CRI-O / Docker |

---

## 三、Service 类型

### ClusterIP（默认）

集群内部可访问，外部不可访问。

```yaml
apiVersion: v1
kind: Service
metadata:
  name: internal-service
spec:
  type: ClusterIP
  selector:
    app: backend
  ports:
    - port: 8080
      targetPort: 8080
```

### NodePort

在每个节点的 IP 上暴露端口，外部可通过 `NodeIP:NodePort` 访问。

```yaml
apiVersion: v1
kind: Service
metadata:
  name: nodeport-service
spec:
  type: NodePort
  selector:
    app: web
  ports:
    - port: 80
      targetPort: 80
      nodePort: 30080  # 30000-32767
```

### LoadBalancer

云提供商（AWS/GCP/Azure）提供外部负载均衡器。

```yaml
apiVersion: v1
kind: Service
metadata:
  name: lb-service
spec:
  type: LoadBalancer
  selector:
    app: web
  ports:
    - port: 80
      targetPort: 80
```

---

## 四、ConfigMap & Secret

### ConfigMap

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: app-config
data:
  NODE_ENV: production
  LOG_LEVEL: info
  app.properties: |
    key1=value1
    key2=value2
---
apiVersion: apps/v1
kind: Deployment
spec:
  template:
    spec:
      containers:
        - envFrom:
            - configMapRef:
                name: app-config
          volumeMounts:
            - name: config
              mountPath: /etc/config
      volumes:
        - name: config
          configMap:
            name: app-config
```

### Secret

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: db-secret
type: Opaque
data:
  username: cm9vdA==      # echo -n "root" | base64
  password: cGFzc3dvcmQ=  # echo -n "password" | base64
---
apiVersion: apps/v1
kind: Deployment
spec:
  template:
    spec:
      containers:
        - env:
            - name: DB_USERNAME
              valueFrom:
                secretKeyRef:
                  name: db-secret
                  key: username
            - name: DB_PASSWORD
              valueFrom:
                secretKeyRef:
                  name: db-secret
                  key: password
```

---

## 五、Ingress

Ingress 提供 HTTP/HTTPS 路由到 Service。

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: my-ingress
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
spec:
  rules:
    - host: myapp.example.com
      http:
        paths:
          - path: /api
            pathType: Prefix
            backend:
              service:
                name: api-service
                port:
                  number: 8080
          - path: /
            pathType: Prefix
            backend:
              service:
                name: web-service
                port:
                  number: 80
  tls:
    - hosts:
        - myapp.example.com
      secretName: tls-secret
```

---

## 六、常用命令

```bash
# 资源管理
kubectl get pods
kubectl get pods -n production
kubectl get pods -o wide               # 显示更多信息
kubectl get all                        # 获取所有资源

# 创建和删除
kubectl apply -f deployment.yaml
kubectl delete -f deployment.yaml
kubectl delete pod my-pod

# 调试
kubectl describe pod my-pod
kubectl logs my-pod
kubectl logs -f deployment/web         # 流式日志
kubectl logs --tail=100 -l app=web     # 根据标签
kubectl exec -it my-pod -- bash
kubectl exec deployment/web -- ls -la

# 端口转发
kubectl port-forward pod/my-pod 8080:80
kubectl port-forward service/web-service 8080:80

# 扩缩容
kubectl scale deployment/web --replicas=5
kubectl autoscale deployment/web --min=2 --max=10 --cpu-percent=80

# 更新
kubectl set image deployment/web nginx=nginx:1.26-alpine
kubectl rollout status deployment/web
kubectl rollout history deployment/web
kubectl rollout undo deployment/web

# 上下文切换
kubectl config get-contexts
kubectl config use-context production
```

---

## 七、资源限制

```yaml
apiVersion: apps/v1
kind: Deployment
spec:
  template:
    spec:
      containers:
        - name: app
          resources:
            requests:
              cpu: "250m"        # 250 毫核
              memory: "256Mi"
            limits:
              cpu: "500m"
              memory: "512Mi"
---
# LimitRange（命名空间默认限制）
apiVersion: v1
kind: LimitRange
metadata:
  name: mem-limit-range
spec:
  limits:
    - default:
        memory: 512Mi
        cpu: "500m"
      defaultRequest:
        memory: 256Mi
        cpu: "250m"
      type: Container
```

## 八、Helm 基础

```bash
# 安装 Helm
curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash

# 仓库管理
helm repo add bitnami https://charts.bitnami.com/bitnami
helm repo update
helm search repo nginx

# 安装 chart
helm install my-release bitnami/nginx
helm install my-app ./my-chart

# 管理
helm list
helm upgrade my-release bitnami/nginx --set replicaCount=3
helm rollback my-release 1
helm uninstall my-release
```

```yaml
# Chart.yaml
apiVersion: v2
name: my-app
description: 我的应用
type: application
version: 0.1.0
appVersion: "1.0.0"
```

## 相关条目

- [[Dockerfile]]
- [[Compose]]
- [[CI-CD 与 DevOps 实践]]
- [[Pipeline]]
- [[BestPractices]]
