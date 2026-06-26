---
aliases: [Pipeline]
tags: ['SoftwareEngineering', 'DevOpsAndCI_CD', 'Pipeline']
---

# CI/CD 流水线设计

## 一、流水线阶段

### 典型流水线

```
┌──────┐ ┌──────┐ ┌───────┐ ┌──────┐ ┌───────┐ ┌──────┐ ┌──────┐
│ Lint │→│ Test │→│ Build │→│Scan  │→│Package│→│Stage │→│Deploy│
└──────┘ └──────┘ └───────┘ └──────┘ └───────┘ └──────┘ └──────┘
```

### 各阶段说明

| 阶段 | 工具示例 | 目的 |
|------|----------|------|
| Lint | ESLint, Ruff, Checkstyle | 代码风格和质量检查 |
| Test | Jest, Pytest, JUnit | 单元测试、集成测试 |
| Build | Webpack, Maven, Go build | 编译、打包 |
| Scan | Trivy, SonarQube, Snyk | 安全漏洞和代码质量扫描 |
| Package | Docker, Helm | 制作镜像、Chart |
| Stage | K8s staging, 预发布 | 预发布环境部署验证 |
| Deploy | K8s, Ansible, Terraform | 生产环境部署 |

---

## 二、环境管理

### 多环境配置

```yaml
# .env 文件结构
.env.development     # 开发环境
.env.staging         # 预发布环境
.env.production      # 生产环境
```

```python
# 应用层读取
import os

ENV = os.getenv('APP_ENV', 'development')
config = {
    'development': {
        'DB_HOST': 'localhost',
        'LOG_LEVEL': 'DEBUG',
    },
    'staging': {
        'DB_HOST': 'staging-db.example.com',
        'LOG_LEVEL': 'INFO',
    },
    'production': {
        'DB_HOST': 'prod-db.example.com',
        'LOG_LEVEL': 'WARNING',
    },
}[ENV]
```

### 部署流程

```yaml
# 环境提升（Promotion）
develop → staging → production
   │         │          │
   │ 自动    │ 手动审批  │ 手动审批+冷却
   ▼         ▼          ▼
  测试      UAT验收    生产

# 部署门禁（Gate）
environment:
  staging:
    required_approvals: 0     # 自动部署
    tests: integration, smoke
  production:
    required_approvals: 2     # 需要 2 人审批
    tests: full_regression
    cooldown: 10m             # 发布后冷却 10 分钟
```

---

## 三、部署策略

### 蓝绿部署 (Blue-Green)

```
┌────────┐         ┌────────┐
│  Blue  │◀── 活跃  │ 用户   │
│ v1.0.0 │         └────────┘
└────────┘
     │ 部署新版本
     ▼
┌────────┐         ┌────────┐
│  Blue  │         │ Green  │
│ v1.0.0 │         │ v2.0.0 │
└────────┘         └────────┘
                       │ 切换流量
                       ▼
┌────────┐         ┌────────┐
│  Blue  │         │ Green  │◀── 活跃
│ v1.0.0 │         │ v2.0.0 │
└────────┘         └────────┘
```

```yaml
# Kubernetes 蓝绿部署
apiVersion: v1
kind: Service
metadata:
  name: my-app
spec:
  selector:
    app: my-app
    version: green   # 切换 blue/green
```

### 金丝雀发布 (Canary Release)

逐步将流量导入新版本。

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  annotations:
    nginx.ingress.kubernetes.io/canary: "true"
    nginx.ingress.kubernetes.io/canary-weight: "10"  # 10% 流量
spec:
  rules:
    - http:
        paths:
          - backend:
              service:
                name: my-app-canary  # 新版本
```

```python
# 应用层的金丝雀逻辑
import random

CANARY_PERCENT = 10

def get_backend():
    if random.randint(1, 100) <= CANARY_PERCENT:
        return "new-backend"   # 新版本
    return "stable-backend"    # 旧版本
```

### 滚动更新 (Rolling Update)

```yaml
apiVersion: apps/v1
kind: Deployment
spec:
  replicas: 10
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 2          # 最多超量 2 个副本
      maxUnavailable: 1    # 最多 1 个副本不可用
  template:
    spec:
      containers:
        - name: app
          image: myapp:2.0.0
```

```
滚动过程：
旧: [1][2][3][4][5][6][7][8][9][10]
新: [N1]
旧: [1][2][3][4][5][6][7][8][9] 新: [N1]
旧: [1][2][3][4][5][6][7][8]    新: [N1][N2]
...
新: [N1][N2][N3][N4][N5][N6][N7][N8][N9][N10]
```

### A/B 测试

通过路由规则将不同用户导向不同版本。

```yaml
# 基于 HTTP Header 路由
apiVersion: v1
kind: Service
metadata:
  annotations:
    traefik.ingress.kubernetes.io/service-weights: |
      my-app-v1: 90
      my-app-v2: 10
```

---

## 四、审批门禁

```yaml
# GitHub Environments
environments:
  staging:
    deployment_branch: develop
    auto_deploy: true

  production:
    deployment_branch: main
    required_reviewers:
      - tech-lead
      - qa-lead
    wait_timer: 5  # 审批后等待 5 分钟冷却
```

```groovy
// Jenkins 审批门禁
stage('Deploy to Production') {
    input {
        message "确认部署 v${params.VERSION} 到生产环境？"
        ok "确认"
        parameters {
            string(name: 'VERSION', defaultValue: params.VERSION)
        }
    }
    steps {
        deploy('production')
    }
    post {
        success {
            slackSend(
                channel: '#deployments',
                message: "✅ ${env.JOB_NAME} v${params.VERSION} 已部署到生产"
            )
        }
    }
}
```

---

## 五、制品管理

### 版本策略 (SemVer)

```
MAJOR.MINOR.PATCH
  1  .  2  .  3

# Git tag + 自动递增
v1.2.3 → v1.2.4 (patch: bug 修复)
v1.2.3 → v1.3.0 (minor: 新功能)
v1.2.3 → v2.0.0 (major: 破坏性变更)

# Git commit 信息触发版本号（语义化提交）
feat:      → minor 递增
fix:       → patch 递增
BREAKING:  → major 递增
```

### 制品标签

```bash
# Docker 镜像标签策略
myapp:latest              # 最新
myapp:v1.2.3             # 版本号
myapp:sha-a1b2c3d        # Git commit SHA
myapp:20240601-123456    # 构建时间

# 推送到仓库
docker tag myapp registry.example.com/myapp:v1.2.3
docker push registry.example.com/myapp:v1.2.3
```

### 仓储管理

```yaml
# Nexus / Artifactory 制品仓库
repository:
  snapshots:  # 开发版本
    - myapp:1.2.4-SNAPSHOT
    - myapp:1.2.4-20240601.123456-1

  releases:   # 发布版本
    - myapp:1.2.3
    - myapp:1.2.2
```

---

## 六、CI/CD 最佳实践

### 失败快速 (Fail Fast)

```groovy
pipeline {
    stages {
        stage('Lint') {
            steps {
                sh 'npm run lint'
                // lint 失败后不继续执行测试
            }
        }
        stage('Test') {
            steps {
                sh 'npm test'
            }
        }
    }
}
```

### 幂等性 (Idempotent)

每次构建产生相同结果，不依赖外部状态。

```yaml
# ✅ 好的实践
- 使用 hash 作为镜像标签（不变）
- 锁定依赖版本（lockfile）
- 从零构建，不依赖缓存

# ❌ 坏的实践
- 使用 latest 标签
- 依赖全局安装的工具
- 手工修改服务器配置
```

### 不可变产物 (Immutable Artifact)

```
# 每个构建产生唯一的不可变产物
build-1 → myapp:v1.0.0-build.1
build-2 → myapp:v1.0.0-build.2

# 产物通过提升方式部署（不修改）
build-1 提升到 staging → 验证通过
build-1 提升到 production → 使用同一产物

# 不要这样：
staging 上调试 → 修改配置 → 部署到 production ❌
```

### 流水线设计原则

| 原则 | 说明 |
|------|------|
| Fail Fast | 尽早失败，减少浪费 |
| 幂等 | 多次运行结果一致 |
| 不可变 | 每个构建产出一致的制品 |
| 可追溯 | 版本、时间、提交、构建人可查 |
| 自动化 | 除了审批，全部自动化 |
| 安全 | 密钥不写入代码，使用 Secret 管理 |

## 相关条目

- [[CI-CD与DevOps实践]]
- [[Jenkins]]
- [[GitHubActions]]
- [[Dockerfile]]
- [[K8s]]
