# Docker Compose 详解

## 一、Compose 文件结构

```yaml
version: '3.8'

services:      # 服务定义
  web:         # 服务名称
    image:     # 镜像
    build:     # 构建配置
    ports:     # 端口映射
    volumes:   # 卷挂载
    environment:  # 环境变量
    depends_on:  # 依赖关系
    restart:     # 重启策略
    healthcheck: # 健康检查

networks:      # 网络定义
  frontend:
  backend:

volumes:       # 卷定义
  db-data:
```

## 二、服务配置详解

### image / build

```yaml
services:
  # 使用已有镜像
  web:
    image: nginx:alpine

  # 从 Dockerfile 构建
  app:
    build: .
    build:
      context: .
      dockerfile: Dockerfile.prod
      args:
        NODE_ENV: production
      labels:
        - "version=1.0"
      cache_from:
        - my-app:cache

  # 从远程仓库
  db:
    image: registry.example.com/myapp/db:latest
```

### ports

```yaml
services:
  web:
    ports:
      - "80:80"              # host:container
      - "8080:80"            # 不同端口
      - "3000"               # 随机分配 host 端口
      - "127.0.0.1:8080:80" # 绑定到特定 IP
      - "443:443/tcp"        # 指定协议
```

### volumes

```yaml
services:
  db:
    volumes:
      # 命名卷（持久化，推荐）
      - db-data:/var/lib/mysql

      # 绑定挂载（开发用）
      - ./data:/var/lib/mysql
      - ./config/my.cnf:/etc/mysql/my.cnf:ro

      # 匿名卷
      - /var/lib/mysql

  app:
    volumes:
      - ./src:/app/src          # 开发热重载
      - /app/node_modules       # 排除 node_modules

volumes:
  db-data:                      # 命名卷声明
```

### environment / env_file

```yaml
services:
  api:
    environment:
      - NODE_ENV=production
      - DB_HOST=db
      - DB_PORT=3306
      - SECRET_KEY=${SECRET_KEY}  # 从 .env 文件读取

    # 优先使用 env_file
    env_file:
      - .env
      - .env.production
```

### depends_on

```yaml
services:
  web:
    depends_on:
      - db
      - redis

  # 带条件等待
  app:
    depends_on:
      db:
        condition: service_healthy
      redis:
        condition: service_started
```

### restart

```yaml
services:
  # 重启策略
  app:
    restart: "no"                # 不自动重启（默认）
    restart: always              # 总是重启
    restart: unless-stopped      # 除非手动停止，否则总是重启
    restart: on-failure          # 仅退出码非0时重启
    restart: on-failure:5        # 最多重启5次
```

### healthcheck

```yaml
services:
  app:
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:3000/health"]
      interval: 30s              # 检查间隔
      timeout: 10s               # 超时时间
      retries: 3                 # 重试次数
      start_period: 40s          # 启动宽限时间
```

### networks

```yaml
services:
  web:
    networks:
      - frontend

  api:
    networks:
      - frontend
      - backend

  db:
    networks:
      - backend

networks:
  frontend:
    driver: bridge
  backend:
    driver: bridge
    internal: true               # 禁止外部访问
```

---

## 三、环境变量与 .env

### .env 文件

```bash
# .env
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=secret123
SECRET_KEY=abc123def456
REDIS_HOST=redis
REDIS_PORT=6379
```

### 在 Compose 中使用

```yaml
services:
  app:
    environment:
      DB_HOST: ${DB_HOST:-localhost}
      DB_PORT: ${DB_PORT:-3306}
      DB_PASSWORD: ${DB_PASSWORD}
    env_file:
      - .env
    ports:
      - "${APP_PORT:-3000}:3000"
```

---

## 四、完整实例：Web + DB + Redis + Nginx

```yaml
version: '3.8'

services:
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx/conf.d:/etc/nginx/conf.d:ro
      - ./nginx/ssl:/etc/nginx/ssl:ro
      - static-files:/static
    depends_on:
      - app
    networks:
      - frontend
    healthcheck:
      test: ["CMD", "nginx", "-t"]
      interval: 30s

  app:
    build:
      context: .
      dockerfile: Dockerfile
    expose:
      - "8000"
    environment:
      - NODE_ENV=production
      - DB_HOST=db
      - REDIS_HOST=redis
      - SECRET_KEY=${SECRET_KEY}
    depends_on:
      db:
        condition: service_healthy
      redis:
        condition: service_started
    volumes:
      - static-files:/app/static
    networks:
      - frontend
      - backend
    restart: unless-stopped

  db:
    image: postgres:16-alpine
    environment:
      POSTGRES_DB: myapp
      POSTGRES_USER: myapp
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    volumes:
      - db-data:/var/lib/postgresql/data
      - ./db/init:/docker-entrypoint-initdb.d
    networks:
      - backend
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U myapp"]
      interval: 10s
      timeout: 5s
      retries: 5
    restart: unless-stopped

  redis:
    image: redis:7-alpine
    command: redis-server --appendonly yes
    volumes:
      - redis-data:/data
    networks:
      - backend
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s

volumes:
  db-data:
  redis-data:
  static-files:

networks:
  frontend:
  backend:
    internal: true
```

---

## 五、Profiles（配置文件）

```yaml
services:
  app:
    image: myapp
    profiles: ["core"]        # 默认启动

  db:
    image: postgres
    profiles: ["core"]

  redis:
    image: redis
    profiles: ["core"]

  adminer:
    image: adminer
    profiles: ["dev", "tools"]
    ports:
      - "8080:8080"

  mailhog:
    image: mailhog/mailhog
    profiles: ["dev"]
    ports:
      - "8025:8025"

  prometheus:
    image: prom/prometheus
    profiles: ["monitoring"]

  grafana:
    image: grafana/grafana
    profiles: ["monitoring"]
```

```bash
# 仅启动核心服务
docker compose up

# 启动开发和核心服务
docker compose --profile dev up

# 启动监控和核心服务
docker compose --profile monitoring up

# 多 profile
docker compose --profile dev --profile tools up
```

---

## 六、生产环境考虑

### Docker Compose vs Docker Swarm

```yaml
# docker-compose.yml（开发）
services:
  app:
    build: .
    ports:
      - "3000:3000"
    volumes:
      - ./src:/app/src

# docker-stack.yml（生产/Swarm）
services:
  app:
    image: registry.example.com/myapp:latest
    ports:
      - "3000:3000"
    deploy:
      replicas: 3
      update_config:
        parallelism: 1
        delay: 10s
      restart_policy:
        condition: any
```

### 常用命令

```bash
# 启动
docker compose up -d
docker compose up -d --build     # 重建镜像并启动

# 查看
docker compose ps
docker compose top
docker compose logs -f app

# 执行命令
docker compose exec app bash
docker compose run --rm app npm test

# 扩缩容
docker compose up -d --scale app=3

# 停止清理
docker compose down
docker compose down -v           # 删除卷
docker compose down --rmi all    # 删除镜像

# 更新配置后重启
docker compose up -d --force-recreate
```

## 相关条目

- [[Dockerfile]]
- [[K8s]]
- [[QuickStart]]
- [[BestPractices]]
- [[CI-CD与DevOps实践]]
