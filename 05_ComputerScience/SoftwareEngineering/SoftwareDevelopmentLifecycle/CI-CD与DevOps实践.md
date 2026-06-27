---
aliases: [CI-CD 与 DevOps 实践]
tags: ['SoftwareEngineering', 'SoftwareDevelopmentLifecycle', 'CI-CD 与 DevOps 实践']
---

# CI-CD 与 DevOps 实践

## 一、DevOps 概述

DevOps 是 Development 和 Operations 的组合，旨在打破开发与运维之间的壁垒。

DevOps 核心原则：

```
CALMS 框架:
C - Culture (文化): 协作与信任
A - Automation (自动化): 自动化重复任务
L - Lean (精益): 消除浪费
M - Measurement (度量): 数据驱动决策
S - Sharing (共享): 知识与责任共享
```

DevOps 与传统的对比：

| 维度 | 传统模式 | DevOps 模式 |
|------|----------|-----------|
| 团队关系 | 开发与运维分离 | 统一团队 |
| 部署频率 | 月/季度 | 天/周 |
| 变更风险 | 高 | 低（小批量）|
| 故障恢复 | 小时级 | 分钟级 |
| 测试方式 | 手动测试为主 | 自动化测试 |
| 反馈周期 | 长 | 短 |

## 二、持续集成

持续集成（CI）要求开发者频繁地将代码合并到主干，每次合并都触发自动化构建和测试。

核心实践：

```
1. 频繁提交代码（每天至少一次）
2. 每次提交触发自动构建
3. 快速反馈（构建时间<10分钟）
4. 修复失败的构建是最高优先级
5. 保持构建脚本的维护
6. 所有开发者能看到构建状态
```

CI 服务器配置示例：

```yaml
# .github/workflows/ci.yml
name: CI Pipeline

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  build-and-test:
    runs-on: ubuntu-latest

    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_PASSWORD: test
        options: >-
          --health-cmd pg_isready
          --health-interval 10s

    steps:
      - uses: actions/checkout@v3

      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '20'
          cache: 'npm'

      - name: Install Dependencies
        run: npm ci

      - name: Lint
        run: npm run lint

      - name: Type Check
        run: npm run typecheck

      - name: Unit Tests
        run: npm run test:unit
        env:
          DATABASE_URL: postgresql://postgres:test@localhost:5432/test

      - name: Build
        run: npm run build

      - name: Upload Artifacts
        uses: actions/upload-artifact@v3
        with:
          name: build-output
          path: dist/
```

## 三、持续部署与交付

持续部署（CD）是 CI 的延伸，将通过测试的代码自动部署到生产环境。

部署策略对比：

| 策略 | 风险 | 部署时间 | 回滚速度 | 成本 | 适用场景 |
|------|------|----------|----------|------|----------|
| 蓝绿部署 | 低 | 中 | 极快 | 高 | 核心服务 |
| 滚动更新 | 中 | 长 | 慢 | 低 | 无状态服务 |
| 金丝雀部署 | 极低 | 长 | 快 | 中 | 新功能验证 |
| A/B 测试 | 低 | 长 | 快 | 中 | 特性对比 |
| 功能开关 | 极低 | 即时 | 即时 | 低 | 功能灰度发布 |

```yaml
# deploy.yml - 部署流水线
deploy-production:
  stage: deploy
  environment: production
  script:
    - # 构建 Docker 镜像
    - docker build -t app:$CI_COMMIT_SHORT_SHA .
    - docker push registry.example.com/app:$CI_COMMIT_SHORT_SHA

    - # 蓝绿切换
    - kubectl set image deployment/app-green app=app:$CI_COMMIT_SHORT_SHA
    - kubectl rollout status deployment/app-green

    - # 切换流量到 green
    - kubectl patch service app -p '{"spec":{"selector":{"version":"green"}}}'

    - # 验证
    - curl -f https://app.example.com/health
  only:
    - main
```

## 四、Docker 容器化

Docker 是 DevOps 中最核心的容器技术。

```dockerfile
# 多阶段构建
# Stage 1: Build
FROM node:20-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

# Stage 2: Production
FROM node:20-alpine
RUN addgroup -g 1001 -S appgroup && \
    adduser -S appuser -u 1001 -G appgroup

WORKDIR /app
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/package*.json ./
RUN npm ci --production && npm cache clean --force

USER appuser
EXPOSE 3000
HEALTHCHECK --interval=30s --timeout=3s \
    CMD wget --no-verbose --tries=1 --spider http://localhost:3000/health || exit 1

CMD ["node", "dist/main.js"]
```

```yaml
# docker-compose.yml
version: '3.8'

services:
  app:
    build: .
    ports:
      - "3000:3000"
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/app
    depends_on:
      db:
        condition: service_healthy
    restart: unless-stopped

  db:
    image: postgres:15-alpine
    volumes:
      - pgdata:/var/lib/postgresql/data
    environment:
      - POSTGRES_PASSWORD=pass
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 5s

  redis:
    image: redis:7-alpine
    volumes:
      - redisdata:/data

volumes:
  pgdata:
  redisdata:
```

## 五、Kubernetes 编排

Kubernetes 用于容器化应用的自动部署、扩展和管理。

```yaml
# deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: app
  labels:
    app: web
spec:
  replicas: 3
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxUnavailable: 1
      maxSurge: 1
  selector:
    matchLabels:
      app: web
  template:
    metadata:
      labels:
        app: web
    spec:
      containers:
      - name: app
        image: registry.example.com/app:latest
        ports:
        - containerPort: 3000
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: db-secret
              key: url
        resources:
          requests:
            memory: "128Mi"
            cpu: "100m"
          limits:
            memory: "256Mi"
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /health
            port: 3000
          initialDelaySeconds: 10
        readinessProbe:
          httpGet:
            path: /ready
            port: 3000
---
apiVersion: v1
kind: Service
metadata:
  name: app-service
spec:
  selector:
    app: web
  ports:
  - port: 80
    targetPort: 3000
  type: LoadBalancer

# HPA 自动扩展
---
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: app-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: app
  minReplicas: 3
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
```

## 六、基础设施即代码

IaC（Infrastructure as Code）通过代码管理基础设施。

| 工具 | 类型 | 声明式/命令式 | 状态管理 | 适用场景 |
|------|------|-------------|----------|----------|
| Terraform | 多云 | 声明式 | 有 | 云基础设施 |
| Pulumi | 多云 | 声明式 | 有 | 通用编程语言 |
| Ansible | 配置管理 | 命令式 | 无 | 服务器配置 |
| Chef | 配置管理 | 声明式 | 有 | 大规模配置 |
| Puppet | 配置管理 | 声明式 | 有 | 配置管理 |
| CloudFormation | AWS 专用 | 声明式 | 有 | AWS |

```hcl
# Terraform AWS 基础设施定义
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = "us-west-2"
}

resource "aws_vpc" "main" {
  cidr_block = "10.0.0.0/16"
  tags = {
    Name = "production"
  }
}

resource "aws_ecs_cluster" "app" {
  name = "app-cluster"
}

resource "aws_ecs_service" "app" {
  name            = "app-service"
  cluster         = aws_ecs_cluster.app.id
  task_definition = aws_ecs_task_definition.app.arn
  desired_count   = 3
  launch_type     = "FARGATE"
}
```

## 七、监控与可观测性

可观测性三大支柱：

```
1. 日志 (Logs): 结构化、可搜索
2. 指标 (Metrics): 时序数据、聚合
3. 链路追踪 (Traces): 请求全链路
```

```python
# OpenTelemetry 集成示例
from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import \
    OTLPSpanExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.instrumentation.flask import FlaskInstrumentor

# 初始化追踪
provider = TracerProvider()
processor = BatchSpanProcessor(OTLPSpanExporter(
    endpoint="http://otel-collector:4317"
))
provider.add_span_processor(processor)
trace.set_tracer_provider(provider)

# 自动 Instrument Flask 应用
app = Flask(__name__)
FlaskInstrumentor().instrument_app(app)

# 手动创建 Span
@app.route('/api/process')
def process():
    with trace.get_tracer(__name__).start_as_current_span("process_data") as span:
        span.set_attribute("user.id", get_current_user())
        result = do_processing()
        span.set_status(trace.Status(trace.StatusCode.OK))
        return result
```

## 八、安全 DevOps

DevSecOps 将安全嵌入整个 CI/CD 流程：

```
安全左移 (Shift Left):
开发 -> 编码检查 -> 构建 -> 依赖扫描 -> 测试 -> 镜像扫描 -> 部署 -> 运行时监控

工具链:
  代码分析:    SonarQube, ESLint Security
  依赖扫描:    Snyk, Dependabot, Trivy
  容器扫描:    Trivy, Clair, Anchore
  SAST:       Semgrep, CodeQL
  DAST:       OWASP ZAP, Burp Suite
  密钥检测:    GitLeaks, TruffleHog
```

```yaml
# 安全扫描流水线
security-scan:
  stage: security
  script:
    # 依赖扫描
    - npm audit --audit-level=high

    # 容器镜像扫描
    - trivy image --severity HIGH,CRITICAL \
        registry.example.com/app:$CI_COMMIT_SHORT_SHA

    # SAST 静态分析
    - semgrep --config=auto .

    # 密钥泄露检测
    - gitleaks detect --verbose

  rules:
    - if: $CI_PIPELINE_SOURCE == "merge_request_event"
```

## 相关条目

- [[05_ComputerScience/SoftwareEngineering/DevOpsAndCICD/Pipeline|Pipeline]]
- [[05_ComputerScience/SoftwareEngineering/DevOpsAndCICD/Jenkins|Jenkins]]
- [[05_ComputerScience/SoftwareEngineering/DevOpsAndCICD/GitHubActions|GitHubActions]]
- [[05_ComputerScience/SoftwareEngineering/DevOpsAndCICD/K8s|K8s]]
- [[05_ComputerScience/SoftwareEngineering/DevOpsAndCICD/Dockerfile|Dockerfile]]

## 参考资源

1. 《持续交付》Jez Humble & David Farley 著
2. 《DevOps 实践指南》Gene Kim 著
3. Kubernetes 官方文档：https://kubernetes.io/docs
4. Docker 官方文档：https://docs.docker.com
5. Terraform 入门指南：https://learn.hashicorp.com/terraform
6. 《Site Reliability Engineering》Google 著
7. CNCF 云原生全景图：https://landscape.cncf.io

