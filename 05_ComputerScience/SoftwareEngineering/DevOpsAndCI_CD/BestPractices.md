---
aliases: [BestPractices]
tags: ['SoftwareEngineering', 'DevOpsAndCI_CD', 'BestPractices']
---

# Docker 生产实践

## 一、镜像优化

### Alpine / Slim / Distroless 对比

```dockerfile
# Alpine（推荐）— 5MB
FROM alpine:3.19
RUN apk add --no-cache python3

# Slim — 120MB
FROM python:3.12-slim

# Distroless — 20MB，仅运行时
FROM gcr.io/distroless/base-debian12

# Scratch — 0MB，静态编译
FROM scratch
COPY myapp /
CMD ["/myapp"]
```

| 类型 | 大小 | 安全性 | 调试 | 适用 |
|------|------|--------|------|------|
| Alpine | 小 | 好 | 方便（apk 安装） | 通用 |
| Slim | 中等 | 好 | 方便 | Python/Node |
| Distroless | 极小 | 最好 | 困难 | 生产 |
| Scratch | 极小 | 最好 | 困难 | Go/Rust 静态编译 |

### 减少镜像层数

```dockerfile
# ❌ 每行一个 RUN，层数多
RUN apt-get update
RUN apt-get install -y curl
RUN apt-get install -y git
RUN rm -rf /var/lib/apt/lists/*

# ✅ 合并 RUN
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        curl \
        git \
    && rm -rf /var/lib/apt/lists/*
```

### 多阶段构建

```dockerfile
# 最终镜像只有运行所需文件
FROM golang:1.22 AS build
WORKDIR /src
COPY . .
RUN CGO_ENABLED=0 go build -o /app

FROM alpine:3.19
COPY --from=build /app /app
CMD ["/app"]

# 大小对比：1.2GB（单阶段）→ 15MB（多阶段）
```

### 利用构建缓存

```dockerfile
# 先复制依赖描述文件
COPY package.json package-lock.json ./
RUN npm ci          # 依赖不变时使用缓存

# 后复制源代码
COPY . .
RUN npm run build
```

---

## 二、安全

### 非 Root 用户

```dockerfile
# ❌ 默认 root 运行
FROM node:18-alpine
WORKDIR /app
COPY . .
CMD ["node", "server.js"]

# ✅ 创建非 root 用户
FROM node:18-alpine
RUN addgroup -g 1001 -S appgroup && \
    adduser -u 1001 -S appuser -G appgroup
WORKDIR /app
COPY --chown=appuser:appgroup . .
USER appuser
CMD ["node", "server.js"]
```

### 镜像安全扫描

```bash
# Trivy 扫描
trivy image nginx:alpine
trivy image --severity CRITICAL,HIGH my-app:latest
trivy fs --severity HIGH .

# Docker Scout（Docker Desktop 内置）
docker scout quickview my-app:latest
docker scout cves my-app:latest

# 集成到 CI
# .gitlab-ci.yml 或 GitHub Actions
- name: 扫描镜像
  run: trivy image --exit-code 1 --severity CRITICAL my-app:latest
```

### Seccomp 和 AppArmor

```dockerfile
# 默认 seccomp 配置文件（限制系统调用）
docker run --security-opt seccomp=default.json nginx

# 禁用（不推荐）
docker run --security-opt seccomp=unconfined nginx

# 只读文件系统
docker run --read-only --tmpfs /tmp nginx
```

### 禁止特权

```bash
# ❌ 高危
docker run --privileged myapp
docker run --cap-add SYS_ADMIN myapp

# ✅ 最小权限
docker run --cap-drop ALL --cap-add NET_BIND_SERVICE myapp
```

---

## 三、日志与监控

### 日志管理

```bash
# 限制日志大小
docker run \
    --log-driver json-file \
    --log-opt max-size=10m \
    --log-opt max-file=3 \
    nginx

# Docker Compose 配置
services:
  app:
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"
```

### 日志驱动

```yaml
# Docker Compose 日志驱动
services:
  app:
    logging:
      driver: "fluentd"
      options:
        fluentd-address: "localhost:24224"
        tag: "app.log"
---
services:
  app:
    logging:
      driver: "awslogs"
      options:
        awslogs-group: "my-app"
        awslogs-region: "us-east-1"
```

### 监控

```yaml
# docker-compose.yml - 监控栈
services:
  prometheus:
    image: prom/prometheus
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
    ports:
      - "9090:9090"

  grafana:
    image: grafana/grafana
    ports:
      - "3000:3000"
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin

  cadvisor:
    image: gcr.io/cadvisor/cadvisor
    ports:
      - "8080:8080"
    volumes:
      - /:/rootfs:ro
      - /var/run:/var/run:ro
      - /sys:/sys:ro
      - /var/lib/docker/:/var/lib/docker:ro
```

---

## 四、资源限制

```bash
# 限制 CPU 和内存
docker run \
    --memory=512m \
    --memory-swap=1g \
    --cpus=0.5 \
    --cpu-shares=512 \
    nginx
```

```yaml
# Docker Compose
services:
  app:
    deploy:
      resources:
        limits:
          cpus: '0.50'
          memory: 512M
        reservations:
          cpus: '0.25'
          memory: 256M
```

---

## 五、健康检查

```dockerfile
HEALTHCHECK --interval=30s --timeout=3s --start-period=10s --retries=3 \
    CMD curl -f http://localhost:3000/health || exit 1
```

```yaml
services:
  app:
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:3000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
```

---

## 六、CI/CD 集成

### GitHub Actions

```yaml
name: Docker CI

on:
  push:
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: docker/setup-buildx-action@v3

      - name: Login to Docker Hub
        uses: docker/login-action@v3
        with:
          username: ${{ secrets.DOCKER_USERNAME }}
          password: ${{ secrets.DOCKER_PASSWORD }}

      - name: Build and push
        uses: docker/build-push-action@v5
        with:
          context: .
          push: true
          tags: |
            user/myapp:latest
            user/myapp:${{ github.sha }}
          cache-from: type=gha
          cache-to: type=gha,mode=max
```

### GitLab CI

```yaml
docker-build:
  stage: build
  image: docker:24
  services:
    - docker:24-dind
  script:
    - docker login -u $CI_REGISTRY_USER -p $CI_REGISTRY_PASSWORD $CI_REGISTRY
    - docker build -t $CI_REGISTRY_IMAGE:$CI_COMMIT_SHORT_SHA .
    - docker push $CI_REGISTRY_IMAGE:$CI_COMMIT_SHORT_SHA
```

---

## 七、镜像仓库

### Harbor

```bash
# 安装 Harbor
# https://goharbor.io/docs/2.10.0/install-config/

# 登录 Harbor
docker login harbor.example.com

# 推送
docker tag myapp:latest harbor.example.com/library/myapp:1.0.0
docker push harbor.example.com/library/myapp:1.0.0
```

### 清理策略

```bash
# 删除未使用的镜像和容器（生产环境定期运行）
docker system prune -af --volumes

# 保留最近 N 个镜像
# 在 Harbor 中配置保留策略
# 在 CI 中清理
```

---

## 八、安全清单

| # | 检查项 |
|---|--------|
| 1 | 基础镜像使用特定版本标签，非 latest |
| 2 | 使用非 root 用户运行容器 |
| 3 | 镜像离开 build 环境后做安全扫描 |
| 4 | 限制资源使用（CPU/内存） |
| 5 | 使用只读文件系统（--read-only） |
| 6 | 禁用不必要的能力（--cap-drop ALL） |
| 7 | 设置合理的日志限制 |
| 8 | 添加 HEALTHCHECK |
| 9 | 不使用 ADD 从远程 URL 下载 |
| 10 | 不在镜像中存储密钥（使用 Secret 或环境变量注入） |

## 相关条目

- [[Dockerfile]]
- [[Compose]]
- [[K8s]]
- [[CI-CD与DevOps实践]]
- [[QuickStart]]
