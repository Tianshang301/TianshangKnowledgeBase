---
aliases: [QuickStart]
tags: ['SoftwareEngineering', 'DevOpsAndCICD', 'QuickStart']
created: 2026-05-16
updated: 2026-05-13
---

# Docker 快速入门

## 一、容器 vs 虚拟机

| 特性 | 容器 (Container) | 虚拟机 (VM) |
|------|-----------------|-------------|
| 启动速度 | 毫秒级 | 分钟级 |
| 大小 | MB 级 | GB 级 |
| 内核 | 共享宿主机内核 | 独立内核 |
| 隔离性 | 进程级隔离 | 完全隔离 |
| 资源占用 | 低（仅进程开销） | 高（完整 OS 开销） |
| 迁移性 | 极高 | 较高 |
| 适用场景 | 微服务、应用打包 | 不同 OS 需求、完全隔离 |

---

## 二、安装

### Windows

```powershell
# 下载 Docker Desktop for Windows
# https://docs.docker.com/desktop/install/windows-install/
# 需要 WSL2
wsl --install
# 安装 Docker Desktop 后启动
```

### Linux

```bash
# Ubuntu/Debian
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER  # 免 sudo 运行 docker

# CentOS/RHEL
sudo yum install -y yum-utils
sudo yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo
sudo yum install docker-ce docker-ce-cli containerd.io
sudo systemctl start docker
```

### macOS

```bash
# 下载 Docker Desktop for Mac
brew install --cask docker
```

---

## 三、核心命令

### 镜像管理

```bash
# 搜索镜像
docker search nginx
docker search --limit 5 python

# 拉取镜像
docker pull nginx:latest
docker pull python:3.12-slim
docker pull mysql:8.0

# 查看镜像
docker images
docker image ls
docker image ls --format "table {{.Repository}}\t{{.Tag}}\t{{.Size}}"

# 删除镜像
docker rmi nginx:latest
docker image prune        # 删除悬挂镜像
docker image prune -a     # 删除所有未使用的镜像

# 构建镜像
docker build -t my-app:1.0 .
docker build -f Dockerfile.prod -t my-app:prod .
```

### 容器管理

```bash
# 创建并启动容器
docker run nginx
docker run -d nginx                    # 后台运行
docker run --name my-nginx nginx       # 指定名称
docker run -p 8080:80 nginx            # 端口映射
docker run -v /host/path:/container/path nginx  # 挂载卷
docker run --rm nginx                  # 停止后自动删除
docker run -e ENV_VAR=value nginx      # 环境变量

# 完整示例
docker run -d \
    --name myapp \
    -p 3000:3000 \
    -v $(pwd):/app \
    -e NODE_ENV=production \
    --restart unless-stopped \
    node:18-alpine

# 查看容器
docker ps                    # 运行中的容器
docker ps -a                 # 所有容器
docker ps -q                 # 只显示 ID
docker ps --format "table {{.ID}}\t{{.Names}}\t{{.Status}}"

# 停止/启动/重启
docker stop container_id
docker start container_id
docker restart container_id

# 进入容器
docker exec -it container_id bash
docker exec -it container_id sh
docker exec container_id ls -la

# 查看日志
docker logs container_id
docker logs -f container_id        # 跟随日志
docker logs --tail 100 container_id # 最近 100 行

# 删除容器
docker rm container_id
docker rm -f container_id          # 强制删除运行中的
docker container prune             # 删除所有停止的容器
```

### 网络管理

```bash
# 网络类型
docker network ls
docker network inspect bridge

# 创建网络
docker network create my-network
docker network create --driver bridge my-bridge

# 连接容器到网络
docker network connect my-network container_id
docker run --network my-network nginx
```

### 数据卷

```bash
# 创建卷
docker volume create my-volume

# 挂载卷
docker run -v my-volume:/data nginx
docker run --mount source=my-volume,target=/data nginx

# 绑定挂载
docker run -v /host/path:/container/path nginx

# 查看卷
docker volume ls
docker volume inspect my-volume
```

---

## 四、Docker Compose 基础

### docker-compose.yml

```yaml
version: '3.8'

services:
  web:
    image: nginx:alpine
    ports:
      - "80:80"
    volumes:
      - ./html:/usr/share/nginx/html
    networks:
      - frontend

  app:
    build: .
    ports:
      - "3000:3000"
    environment:
      - DB_HOST=db
      - DB_PORT=3306
    depends_on:
      - db
    networks:
      - frontend
      - backend

  db:
    image: mysql:8.0
    environment:
      MYSQL_ROOT_PASSWORD: rootpass
      MYSQL_DATABASE: myapp
    volumes:
      - db-data:/var/lib/mysql
    networks:
      - backend

networks:
  frontend:
  backend:

volumes:
  db-data:
```

### Compose 命令

```bash
# 启动所有服务
docker compose up
docker compose up -d

# 查看状态
docker compose ps
docker compose logs -f

# 执行命令
docker compose exec app bash

# 停止服务
docker compose down
docker compose down -v          # 同时删除卷

# 重建
docker compose up -d --build

# 查看配置
docker compose config
```

---

## 五、实战步骤

### 步骤 1：获取代码

```bash
mkdir my-webapp && cd my-webapp
```

### 步骤 2：创建 Dockerfile

```dockerfile
FROM node:18-alpine
WORKDIR /app
COPY package*.json ./
RUN npm ci --production
COPY . .
EXPOSE 3000
CMD ["node", "server.js"]
```

### 步骤 3：创建 .dockerignore

```
node_modules
.git
.env
*.log
dist
```

### 步骤 4：构建并运行

```bash
docker build -t my-webapp .
docker run -d --name myapp -p 3000:3000 my-webapp
curl http://localhost:3000
```

### 步骤 5：使用 Compose

```bash
docker compose up -d
docker compose logs -f
```

---

## 六、常用场景示例

### 运行 MySQL

```bash
docker run -d \
    --name mysql \
    -p 3306:3306 \
    -e MYSQL_ROOT_PASSWORD=root123 \
    -e MYSQL_DATABASE=testdb \
    -v mysql-data:/var/lib/mysql \
    mysql:8.0
```

### 运行 Redis

```bash
docker run -d \
    --name redis \
    -p 6379:6379 \
    redis:7-alpine
```

### 运行 PostgreSQL

```bash
docker run -d \
    --name postgres \
    -p 5432:5432 \
    -e POSTGRES_PASSWORD=postgres \
    -e POSTGRES_DB=testdb \
    -v pg-data:/var/lib/postgresql/data \
    postgres:16-alpine
```

### 运行 Nginx 反向代理

```bash
docker run -d \
    --name nginx-proxy \
    -p 80:80 \
    -v ./nginx.conf:/etc/nginx/nginx.conf:ro \
    nginx:alpine
```

## 相关条目

- [[Dockerfile]]
- [[Compose]]
- [[K8s]]
- [[BestPractices]]
- [[CI-CD 与 DevOps 实践]]
