---
aliases: [Docker, Containerization, 容器化, Dockerfile]
tags: ['05_ComputerScience', 'SoftwareEngineering', 'Docker', 'DevOps']
created: 2026-06-27
updated: 2026-06-27
---

# Docker 与容器化 (Docker & Containerization)

## 一、概述

Docker 是一个开源的容器化平台，用于自动化应用程序的部署、扩展和管理。容器将应用及其依赖打包在一起，确保在任何环境中都能一致运行。

### 1.1 容器 vs 虚拟机

| 特性 | 容器 | 虚拟机 |
|------|------|--------|
| 启动速度 | 秒级 | 分钟级 |
| 资源占用 | 轻量级 | 重量级 |
| 隔离级别 | 进程级 | 系统级 |
| 镜像大小 | MB级 | GB级 |
| 性能 | 接近原生 | 有损耗 |

### 1.2 Docker 核心概念

| 概念 | 描述 |
|------|------|
| **镜像 (Image)** | 只读模板，包含运行应用所需的一切 |
| **容器 (Container)** | 镜像的运行实例 |
| **Dockerfile** | 构建镜像的脚本 |
| **Registry** | 镜像仓库（Docker Hub） |
| **Volume** | 持久化存储 |
| **Network** | 容器网络 |

---

## 二、Dockerfile

### 2.1 基础 Dockerfile

```dockerfile
# 基础镜像
FROM python:3.11-slim

# 设置工作目录
WORKDIR /app

# 复制依赖文件
COPY requirements.txt .

# 安装依赖
RUN pip install --no-cache-dir -r requirements.txt

# 复制应用代码
COPY . .

# 暴露端口
EXPOSE 8000

# 启动命令
CMD ["python", "main.py"]
```

### 2.2 多阶段构建

```dockerfile
# 构建阶段
FROM node:18 AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

# 生产阶段
FROM node:18-slim
WORKDIR /app
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/node_modules ./node_modules
COPY package.json .
EXPOSE 3000
CMD ["node", "dist/main.js"]
```

### 2.3 Python 应用 Dockerfile

```dockerfile
FROM python:3.11-slim

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# 创建非root用户
RUN useradd -m -u 1000 appuser

WORKDIR /app

# 安装Python依赖
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制应用
COPY --chown=appuser:appuser . .

# 切换用户
USER appuser

# 健康检查
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8000/health')"

EXPOSE 8000

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8000", "app:app"]
```

### 2.4 Go 应用 Dockerfile

```dockerfile
# 构建阶段
FROM golang:1.21-alpine AS builder
WORKDIR /app
COPY go.mod go.sum ./
RUN go mod download
COPY . .
RUN CGO_ENABLED=0 GOOS=linux go build -o main .

# 生产阶段
FROM alpine:3.18
RUN apk --no-cache add ca-certificates tzdata
WORKDIR /app
COPY --from=builder /app/main .
EXPOSE 8080
CMD ["./main"]
```

### 2.5 Java 应用 Dockerfile

```dockerfile
# 构建阶段
FROM maven:3.9-eclipse-temurin-17 AS builder
WORKDIR /app
COPY pom.xml .
RUN mvn dependency:go-offline
COPY src ./src
RUN mvn package -DskipTests

# 生产阶段
FROM eclipse-temurin:17-jre-alpine
WORKDIR /app
COPY --from=builder /app/target/*.jar app.jar
EXPOSE 8080
ENTRYPOINT ["java", "-jar", "app.jar"]
```

---

## 三、Docker Compose

### 3.1 基础 Compose 文件

```yaml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/mydb
      - REDIS_URL=redis://redis:6379
    depends_on:
      - db
      - redis
    volumes:
      - ./app:/app
    networks:
      - app-network

  db:
    image: postgres:15
    environment:
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=pass
      - POSTGRES_DB=mydb
    volumes:
      - postgres_data:/var/lib/postgresql/data
    networks:
      - app-network

  redis:
    image: redis:7-alpine
    networks:
      - app-network

volumes:
  postgres_data:

networks:
  app-network:
    driver: bridge
```

### 3.2 生产环境 Compose

```yaml
version: '3.8'

services:
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./certs:/etc/nginx/certs
    depends_on:
      - web
    restart: unless-stopped

  web:
    build:
      context: .
      dockerfile: Dockerfile
    deploy:
      replicas: 3
      resources:
        limits:
          cpus: '0.50'
          memory: 512M
    environment:
      - NODE_ENV=production
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:3000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
    restart: unless-stopped

  db:
    image: postgres:15
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./backup:/backup
    environment:
      - POSTGRES_PASSWORD_FILE=/run/secrets/db_password
    secrets:
      - db_password
    restart: unless-stopped

  redis:
    image: redis:7-alpine
    command: redis-server --requirepass ${REDIS_PASSWORD}
    volumes:
      - redis_data:/data
    restart: unless-stopped

secrets:
  db_password:
    file: ./secrets/db_password.txt

volumes:
  postgres_data:
  redis_data:
```

### 3.3 开发环境 Compose

```yaml
version: '3.8'

services:
  app:
    build:
      context: .
      target: development
    ports:
      - "3000:3000"
      - "9229:9229"  # Node.js debugger
    volumes:
      - .:/app
      - /app/node_modules
    environment:
      - NODE_ENV=development
    command: npm run dev

  test-db:
    image: postgres:15
    environment:
      - POSTGRES_DB=testdb
      - POSTGRES_PASSWORD=test
    tmpfs:
      - /var/lib/postgresql/data  # 内存存储，测试更快
```

---

## 四、Docker 网络

### 4.1 网络类型

```bash
# 创建自定义网络
docker network create --driver bridge my-network

# 查看网络
docker network ls

# 连接容器到网络
docker network connect my-network my-container

# 断开网络
docker network disconnect my-network my-container
```

### 4.2 网络配置

```yaml
# docker-compose.yml
services:
  web:
    networks:
      frontend:
        aliases:
          - web.local
      backend:
        aliases:
          - api.local

  db:
    networks:
      backend:
        aliases:
          - db.local

networks:
  frontend:
    driver: bridge
  backend:
    driver: bridge
    internal: true  # 不允许外部访问
```

---

## 五、Docker Volume

### 5.1 Volume 类型

```bash
# 命名卷
docker volume create my-volume
docker run -v my-volume:/app/data my-image

# 绑定挂载
docker run -v /host/path:/container/path my-image

# tmpfs 挂载（内存）
docker run --tmpfs /app/temp my-image
```

### 5.2 Volume 配置

```yaml
# docker-compose.yml
services:
  db:
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./init.sql:/docker-entrypoint-initdb.d/init.sql

  app:
    volumes:
      - type: bind
        source: ./app
        target: /app
      - type: tmpfs
        target: /app/temp

volumes:
  postgres_data:
    driver: local
```

---

## 六、Docker 安全

### 6.1 安全最佳实践

```dockerfile
# 使用非root用户
RUN useradd -m -u 1000 appuser
USER appuser

# 只读文件系统
docker run --read-only my-image

# 限制资源
docker run --memory=512m --cpus=0.5 my-image

# 扫描漏洞
docker scan my-image
```

### 6.2 Docker Content Trust

```bash
# 启用内容信任
export DOCKER_CONTENT_TRUST=1

# 签名镜像
docker push my-image:latest

# 验证签名
docker trust inspect --pretty my-image
```

---

## 七、Docker 镜像优化

### 7.1 减小镜像大小

```dockerfile
# 使用Alpine基础镜像
FROM python:3.11-alpine

# 合并RUN指令
RUN apk add --no-cache gcc musl-dev && \
    pip install --no-cache-dir -r requirements.txt && \
    apk del gcc musl-dev

# 使用.dockerignore
# .git
# node_modules
# __pycache__
# *.pyc
# .env
```

### 7.2 构建缓存优化

```dockerfile
# 先复制依赖文件
COPY requirements.txt .
RUN pip install -r requirements.txt

# 再复制代码
COPY . .
```

---

## 八、Docker Registry

### 8.1 私有 Registry

```yaml
# docker-compose.yml
version: '3.8'

services:
  registry:
    image: registry:2
    ports:
      - "5000:5000"
    volumes:
      - registry_data:/var/lib/registry
    environment:
      - REGISTRY_AUTH=htpasswd
      - REGISTRY_AUTH_HTPASSWD_REALM=Registry
      - REGISTRY_AUTH_HTPASSWD_PATH=/auth/htpasswd

volumes:
  registry_data:
```

### 8.2 推送镜像

```bash
# 标记镜像
docker tag my-image localhost:5000/my-image:latest

# 推送镜像
docker push localhost:5000/my-image:latest

# 拉取镜像
docker pull localhost:5000/my-image:latest
```

---

## 相关条目

- [[KubernetesDeep]]
- [[CI-CD]]
- [[DevOps]]

## 参考资源

1. Docker. "Official Documentation." docs.docker.com
2. Docker. "Best Practices." docs.docker.com/develop
3. Docker. "Compose File Reference." docs.docker.com/compose
