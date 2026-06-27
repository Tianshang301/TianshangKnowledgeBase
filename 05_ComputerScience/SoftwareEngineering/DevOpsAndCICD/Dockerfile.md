---
aliases: [Dockerfile]
tags: ['SoftwareEngineering', 'DevOpsAndCICD', 'Dockerfile']
created: 2026-05-16
updated: 2026-05-13
---

# Dockerfile 最佳实践

## 一、Dockerfile 指令详解

### FROM

指定基础镜像。

```dockerfile
FROM ubuntu:22.04
FROM node:18-alpine
FROM python:3.12-slim
FROM golang:1.22-alpine
FROM scratch               # 空镜像，用于静态编译
FROM alpine:3.19 AS builder  # 多阶段构建
```

### RUN

执行命令，每个 RUN 创建一个新镜像层。

```dockerfile
RUN apt-get update && apt-get install -y \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir -r requirements.txt
```

**重要**：将多个命令合并到单个 RUN 以减少层数。

### COPY vs ADD

```dockerfile
# COPY：简单的文件复制（推荐）
COPY package.json /app/
COPY . /app/
COPY --from=builder /app/dist /app/dist

# ADD：支持 URL 和自动解压（谨慎使用）
ADD https://example.com/file.tar.gz /tmp/
ADD app.tar.gz /app/     # 自动解压 tar.gz
```

**规则**：使用 COPY 而非 ADD，除非需要自动解压。

### CMD vs ENTRYPOINT

```dockerfile
# CMD：提供默认命令（可被覆盖）
CMD ["node", "server.js"]
CMD npm start

# ENTRYPOINT：设置主命令（不可被覆盖）
ENTRYPOINT ["python"]
CMD ["app.py"]           # 作为 ENTRYPOINT 的默认参数

# 组合使用
ENTRYPOINT ["gunicorn"]
CMD ["-w", "4", "-b", "0.0.0.0:8000", "app:app"]

# 覆盖示例
docker run my-image -w 8 -b 0.0.0.0:8001 app:app   # 覆盖 CMD
docker run --entrypoint bash my-image               # 覆盖 ENTRYPOINT
```

### WORKDIR

设置工作目录，自动创建不存在的目录。

```dockerfile
WORKDIR /app
RUN mkdir config
COPY . .
# 相当于 cd /app 后再执行后续指令
```

### ENV vs ARG

```dockerfile
# ARG：构建时变量（仅构建时存在）
ARG NODE_ENV=production
ARG APP_VERSION

# ENV：环境变量（构建和运行时都存在）
ENV NODE_ENV=${NODE_ENV}
ENV DATABASE_URL="mysql://user:pass@host/db"
ENV PORT=3000

# 构建时传递 ARG
docker build --build-arg NODE_ENV=development -t my-app .
```

### EXPOSE

声明容器监听的端口（文档性质，不实际发布端口）。

```dockerfile
EXPOSE 80
EXPOSE 3000
EXPOSE 443
# 实际发布端口需使用 -p 或 docker compose ports
```

### VOLUME

创建挂载点，用于持久化数据。

```dockerfile
VOLUME /var/lib/mysql
VOLUME /data
VOLUME ["/var/log", "/var/lib/data"]
```

### USER

指定运行用户，增强安全性。

```dockerfile
RUN addgroup -g 1001 -S appgroup && \
    adduser -u 1001 -S appuser -G appgroup
USER appuser
```

### LABEL

添加元数据。

```dockerfile
LABEL maintainer="dev@example.com"
LABEL version="1.0.0"
LABEL description="我的应用"
```

### HEALTHCHECK

定义容器健康检查。

```dockerfile
HEALTHCHECK --interval=30s --timeout=3s --retries=3 \
    CMD curl -f http://localhost:3000/health || exit 1
```

---

## 二、多阶段构建

多阶段构建大幅减小最终镜像大小。

### Go 应用

```dockerfile
# Stage 1: 构建
FROM golang:1.22-alpine AS builder
WORKDIR /build
COPY go.mod go.sum ./
RUN go mod download
COPY . .
RUN CGO_ENABLED=0 go build -o /app/server .

# Stage 2: 运行
FROM alpine:3.19
RUN apk add --no-cache ca-certificates tzdata
COPY --from=builder /app/server /server
EXPOSE 8080
CMD ["/server"]
```

### Node.js 应用

```dockerfile
# Stage 1: 构建
FROM node:18-alpine AS builder
WORKDIR /build
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

# Stage 2: 运行
FROM node:18-alpine
RUN addgroup -g 1001 -S appgroup && \
    adduser -u 1001 -S appuser -G appgroup
WORKDIR /app
COPY --from=builder /build/package*.json ./
COPY --from=builder /build/node_modules ./node_modules
COPY --from=builder /build/dist ./dist
USER appuser
EXPOSE 3000
CMD ["node", "dist/server.js"]
```

### Python 应用

```dockerfile
# Stage 1: 依赖
FROM python:3.12-slim AS builder
WORKDIR /build
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Stage 2: 运行
FROM python:3.12-slim
RUN addgroup -g 1001 -S appgroup && \
    adduser -u 1001 -S appuser -G appgroup
WORKDIR /app
COPY --from=builder /root/.local /home/appuser/.local
COPY app/ ./app/
USER appuser
ENV PATH=/home/appuser/.local/bin:$PATH
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Java 应用

```dockerfile
# Stage 1: 构建
FROM eclipse-temurin:21-jdk-alpine AS builder
WORKDIR /build
COPY mvnw pom.xml ./
COPY .mvn .mvn
RUN ./mvnw dependency:go-offline
COPY src ./src
RUN ./mvnw package -DskipTests

# Stage 2: 运行
FROM eclipse-temurin:21-jre-alpine
RUN addgroup -g 1001 -S appgroup && \
    adduser -u 1001 -S appuser -G appgroup
WORKDIR /app
COPY --from=builder /build/target/*.jar app.jar
USER appuser
EXPOSE 8080
ENTRYPOINT ["java", "-jar", "app.jar"]
```

---

## 三、构建上下文与 .dockerignore

### .dockerignore

```
# .dockerignore
.git
node_modules
.env
*.log
dist
.cache
.idea
.vscode
__pycache__
*.pyc
.venv
coverage
.DS_Store
docker-compose*.yml
```

### 构建上下文

```bash
# 构建上下文是发送给 Docker daemon 的文件集合
# 不要用根目录作为上下文
docker build -f docker/Dockerfile .          # 上下文 = 当前目录
docker build -f Dockerfile /path/to/context  # 上下文 = 指定目录

# 优化：使用 stdin 构建
docker build -t my-app - < Dockerfile
```

---

## 四、基础镜像选择

```dockerfile
# Alpine Linux（最小，约 5MB）
FROM alpine:3.19

# Debian Slim（适中，约 80MB）
FROM python:3.12-slim

# Distroless（仅运行时依赖）
FROM gcr.io/distroless/base-debian12

# Ubuntu（完整功能）
FROM ubuntu:22.04

# 特定语言镜像
FROM node:18-alpine      # Node.js
FROM python:3.12-slim    # Python
FROM golang:1.22-alpine  # Go
FROM eclipse-temurin:21-jre-alpine  # Java
FROM nginx:alpine        # Nginx
```

### 镜像大小比较

| 镜像 | 大小 | 适用场景 |
|------|------|----------|
| alpine:3.19 | 5MB | 静态编译 Go/Rust |
| python:3.12-slim | 120MB | Python 应用 |
| node:18-alpine | 120MB | Node.js 应用 |
| ubuntu:22.04 | 77MB | 需要完整工具链 |
| distroless/base | 20MB | 极简安全运行 |

---

## 五、最佳实践总结

```dockerfile
# 最终优化示例
FROM node:18-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci --ignore-scripts && npm cache clean --force
COPY . .
RUN npm run build

FROM node:18-alpine
RUN addgroup -g 1001 -S appuser && \
    adduser -u 1001 -S appuser -G appuser && \
    apk add --no-cache tini
WORKDIR /app
COPY --chown=appuser:appuser --from=builder /app/dist ./dist
COPY --chown=appuser:appuser package*.json ./
COPY --chown=appuser:appuser --from=builder /app/node_modules ./node_modules
USER appuser
EXPOSE 3000
HEALTHCHECK --interval=30s --timeout=3s --retries=3 \
    CMD wget -qO- http://localhost:3000/health || exit 1
ENTRYPOINT ["/sbin/tini", "--"]
CMD ["node", "dist/server.js"]
```

### 10 条最佳实践

| # | 规则 |
|---|------|
| 1 | 选择最小基础镜像（alpine/slim/distroless） |
| 2 | 多阶段构建分离构建和运行环境 |
| 3 | 合并 RUN 命令减少层数 |
| 4 | 使用 .dockerignore 减少上下文大小 |
| 5 | 设置非 root 用户运行 |
| 6 | 使用特定标签而非 latest |
| 7 | 利用构建缓存（复制 package.json 在前） |
| 8 | 添加 HEALTHCHECK |
| 9 | 使用 COPY 而非 ADD |
| 10 | 使用 --no-cache 和 --no-install-recommends |

## 相关条目

- [[Compose]]
- [[K8s]]
- [[QuickStart]]
- [[BestPractices]]
- [[CI-CD 与 DevOps 实践]]
