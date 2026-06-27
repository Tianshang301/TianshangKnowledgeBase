---
aliases: [CICD, CI-CD, 持续集成, 持续部署, GitHub Actions]
tags: ['05_ComputerScience', 'SoftwareEngineering', 'DevOps', 'CI-CD']
created: 2026-06-27
updated: 2026-06-27
---

# CI/CD 流水线 (CI/CD Pipeline)

## 一、概述

CI/CD 是持续集成（Continuous Integration）和持续部署（Continuous Deployment）的缩写，是现代软件开发的核心实践。

### 1.1 核心概念

| 概念 | 描述 |
|------|------|
| **持续集成** | 频繁将代码集成到主干，每次集成都自动构建和测试 |
| **持续交付** | 代码随时可以部署到生产环境 |
| **持续部署** | 代码变更自动部署到生产环境 |

### 1.2 流程图

```mermaid
graph LR
    A[代码提交] --> B[构建]
    B --> C[单元测试]
    C --> D[集成测试]
    D --> E[代码质量检查]
    E --> F[构建镜像]
    F --> G[部署到测试环境]
    G --> H[自动化测试]
    H --> I[部署到生产环境]
```

---

## 二、GitHub Actions

### 2.1 基础工作流

```yaml
# .github/workflows/ci.yml
name: CI

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
          pip install -r requirements-dev.txt
      
      - name: Run tests
        run: |
          pytest tests/ --cov=app --cov-report=xml
      
      - name: Upload coverage
        uses: codecov/codecov-action@v3
        with:
          file: ./coverage.xml
```

### 2.2 Node.js 工作流

```yaml
name: Node.js CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest
    
    strategy:
      matrix:
        node-version: [18.x, 20.x]
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Use Node.js ${{ matrix.node-version }}
        uses: actions/setup-node@v4
        with:
          node-version: ${{ matrix.node-version }}
          cache: 'npm'
      
      - name: Install dependencies
        run: npm ci
      
      - name: Lint
        run: npm run lint
      
      - name: Test
        run: npm test
      
      - name: Build
        run: npm run build
```

### 2.3 Docker 构建和推送

```yaml
name: Docker Build

on:
  push:
    tags:
      - 'v*'

jobs:
  build:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3
      
      - name: Login to DockerHub
        uses: docker/login-action@v3
        with:
          username: ${{ secrets.DOCKERHUB_USERNAME }}
          password: ${{ secrets.DOCKERHUB_TOKEN }}
      
      - name: Extract metadata
        id: meta
        uses: docker/metadata-action@v5
        with:
          images: myapp
          tags: |
            type=semver,pattern={{version}}
            type=semver,pattern={{major}}.{{minor}}
      
      - name: Build and push
        uses: docker/build-push-action@v5
        with:
          context: .
          push: true
          tags: ${{ steps.meta.outputs.tags }}
          labels: ${{ steps.meta.outputs.labels }}
          cache-from: type=gha
          cache-to: type=gha,mode=max
```

### 2.4 部署到 Kubernetes

```yaml
name: Deploy to K8s

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    environment: production
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Set up kubectl
        uses: azure/setup-kubectl@v3
      
      - name: Configure kubeconfig
        run: |
          mkdir -p $HOME/.kube
          echo "${{ secrets.KUBE_CONFIG }}" | base64 -d > $HOME/.kube/config
      
      - name: Deploy
        run: |
          kubectl set image deployment/myapp myapp=myapp:${{ github.sha }}
          kubectl rollout status deployment/myapp
      
      - name: Verify deployment
        run: |
          kubectl get pods -l app=myapp
```

### 2.5 矩阵构建

```yaml
name: Matrix Build

on:
  push:
    branches: [main]

jobs:
  test:
    runs-on: ${{ matrix.os }}
    
    strategy:
      matrix:
        os: [ubuntu-latest, windows-latest, macos-latest]
        python-version: ['3.9', '3.10', '3.11']
        exclude:
          - os: windows-latest
            python-version: '3.9'
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}
      
      - name: Test
        run: pytest
```

---

## 三、GitLab CI

### 3.1 基础配置

```yaml
# .gitlab-ci.yml
stages:
  - build
  - test
  - deploy

variables:
  DOCKER_DRIVER: overlay2

build:
  stage: build
  image: docker:latest
  services:
    - docker:dind
  script:
    - docker build -t $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA .
    - docker push $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA

test:
  stage: test
  image: python:3.11
  script:
    - pip install -r requirements.txt
    - pytest tests/
  coverage: '/TOTAL.*\s+(\d+)%/'

deploy:
  stage: deploy
  image: bitnami/kubectl:latest
  script:
    - kubectl set image deployment/myapp myapp=$CI_REGISTRY_IMAGE:$CI_COMMIT_SHA
  only:
    - main
  when: manual
```

### 3.2 环境配置

```yaml
deploy_staging:
  stage: deploy
  environment:
    name: staging
    url: https://staging.example.com
  script:
    - ./deploy.sh staging
  only:
    - develop

deploy_production:
  stage: deploy
  environment:
    name: production
    url: https://example.com
  script:
    - ./deploy.sh production
  only:
    - main
  when: manual
```

---

## 四、Jenkins Pipeline

### 4.1 声明式 Pipeline

```groovy
// Jenkinsfile
pipeline {
    agent any
    
    environment {
        DOCKER_REGISTRY = 'registry.example.com'
        APP_NAME = 'myapp'
    }
    
    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        
        stage('Build') {
            steps {
                sh 'docker build -t ${APP_NAME}:${BUILD_NUMBER} .'
            }
        }
        
        stage('Test') {
            steps {
                sh 'docker run --rm ${APP_NAME}:${BUILD_NUMBER} pytest'
            }
        }
        
        stage('Push') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'docker-creds', usernameVariable: 'USER', passwordVariable: 'PASS')]) {
                    sh 'docker login ${DOCKER_REGISTRY} -u ${USER} -p ${PASS}'
                    sh 'docker tag ${APP_NAME}:${BUILD_NUMBER} ${DOCKER_REGISTRY}/${APP_NAME}:${BUILD_NUMBER}'
                    sh 'docker push ${DOCKER_REGISTRY}/${APP_NAME}:${BUILD_NUMBER}'
                }
            }
        }
        
        stage('Deploy') {
            steps {
                sh 'kubectl set image deployment/${APP_NAME} ${APP_NAME}=${DOCKER_REGISTRY}/${APP_NAME}:${BUILD_NUMBER}'
            }
        }
    }
    
    post {
        success {
            slackSend channel: '#deployments', message: "Deployed ${APP_NAME}:${BUILD_NUMBER}"
        }
        failure {
            slackSend channel: '#deployments', message: "Deployment failed: ${APP_NAME}:${BUILD_NUMBER}"
        }
    }
}
```

---

## 五、代码质量检查

### 5.1 代码覆盖率

```yaml
# GitHub Actions
- name: Run tests with coverage
  run: |
    pytest --cov=app --cov-report=xml --cov-report=html

- name: Upload coverage to Codecov
  uses: codecov/codecov-action@v3
  with:
    file: ./coverage.xml
    fail_ci_if_error: true
```

### 5.2 代码风格检查

```yaml
# GitHub Actions
- name: Lint with Ruff
  run: |
    ruff check .
    ruff format --check .

- name: Type check with MyPy
  run: mypy app/
```

### 5.3 安全扫描

```yaml
# GitHub Actions
- name: Run Trivy vulnerability scanner
  uses: aquasecurity/trivy-action@master
  with:
    image-ref: 'myapp:${{ github.sha }}'
    format: 'sarif'
    output: 'trivy-results.sarif'

- name: Upload Trivy scan results to GitHub Security tab
  uses: github/codeql-action/upload-sarif@v2
  with:
    sarif_file: 'trivy-results.sarif'
```

---

## 六、部署策略

### 6.1 蓝绿部署

```yaml
# Kubernetes 蓝绿部署
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp-blue
spec:
  replicas: 3
  selector:
    matchLabels:
      app: myapp
      version: blue
  template:
    metadata:
      labels:
        app: myapp
        version: blue
    spec:
      containers:
        - name: myapp
          image: myapp:1.0.0

---
apiVersion: v1
kind: Service
metadata:
  name: myapp
spec:
  selector:
    app: myapp
    version: blue  # 切换到 green 实现蓝绿部署
  ports:
    - port: 80
      targetPort: 8080
```

### 6.2 金丝雀部署

```yaml
# 金丝雀部署
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp-canary
spec:
  replicas: 1  # 少量实例
  selector:
    matchLabels:
      app: myapp
      version: canary
  template:
    metadata:
      labels:
        app: myapp
        version: canary
    spec:
      containers:
        - name: myapp
          image: myapp:2.0.0

---
# 通过 Ingress 控制流量比例
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: myapp
  annotations:
    nginx.ingress.kubernetes.io/canary: "true"
    nginx.ingress.kubernetes.io/canary-weight: "10"
spec:
  rules:
    - host: example.com
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: myapp-canary
                port:
                  number: 80
```

---

## 七、最佳实践

### 7.1 分支策略

```mermaid
gitgraph
    commit id: "init"
    branch develop
    commit id: "feature-1"
    branch feature-1
    commit id: "work-1"
    checkout develop
    merge feature-1
    commit id: "feature-2"
    branch feature-2
    commit id: "work-2"
    checkout develop
    merge feature-2
    checkout main
    merge develop
    commit id: "release-1.0"
```

### 7.2 环境管理

| 环境 | 用途 | 部署触发 |
|------|------|---------|
| **Development** | 开发测试 | 每次提交 |
| **Staging** | 预发布测试 | 合并到 develop |
| **Production** | 生产环境 | 合并到 main |

### 7.3 密钥管理

```yaml
# GitHub Secrets
# Settings > Secrets and variables > Actions

# 使用密钥
- name: Deploy
  env:
    API_KEY: ${{ secrets.API_KEY }}
    DATABASE_URL: ${{ secrets.DATABASE_URL }}
  run: ./deploy.sh
```

---

## 相关条目

- [[DockerAndContainerization]]
- [[KubernetesDeep]]
- [[05_ComputerScience/SoftwareEngineering/DevOpsAndCICD/DevOps|DevOps]]

## 参考资源

1. GitHub. "GitHub Actions Documentation." docs.github.com/actions
2. GitLab. "GitLab CI/CD Documentation." docs.gitlab.com
3. Jenkins. "Pipeline Documentation." jenkins.io/doc/book

