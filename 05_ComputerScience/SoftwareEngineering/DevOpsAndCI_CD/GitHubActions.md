---
aliases: [GitHubActions]
tags: ['SoftwareEngineering', 'DevOpsAndCI_CD', 'GitHubActions']
---

# GitHub Actions 指南

## 一、Workflow 语法

### 基本结构

```yaml
name: CI Pipeline                    # 工作流名称
run-name: ${{ github.actor }} 的部署  # 运行名称

on:                                  # 触发条件
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

env:                                 # 全局环境变量
  NODE_VERSION: 18
  APP_ENV: production

jobs:                                # 任务列表
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: echo "运行测试"
```

### 触发器 (on)

```yaml
# 分支推送
on:
  push:
    branches: [main, 'feature/*']
    tags: ['v*']
    paths:        # 仅特定文件变化时触发
      - 'src/**'
      - '!docs/**'

# PR
on:
  pull_request:
    types: [opened, synchronize, reopened]
    branches: [main]

# 定时触发（cron 格式）
on:
  schedule:
    - cron: '0 2 * * *'      # 每天 UTC 2:00
    - cron: '0 */6 * * *'    # 每 6 小时

# 手动触发
on:
  workflow_dispatch:
    inputs:
      environment:
        description: '部署环境'
        required: true
        default: 'staging'
        type: choice
        options:
          - staging
          - production
      version:
        description: '版本号'
        required: true

# 外部事件触发
on:
  repository_dispatch:
    types: [deploy-event]
```

---

## 二、Job 配置

### 运行环境

```yaml
jobs:
  test:
    runs-on: ubuntu-latest
    # 可选：ubuntu-latest, windows-latest, macos-latest
    # 也可使用自定义标签：self-hosted, linux, x64

  test-win:
    runs-on: windows-latest
    defaults:
      run:
        shell: pwsh          # PowerShell Core
```

### Matrix 构建

```yaml
jobs:
  test:
    strategy:
      matrix:
        os: [ubuntu-latest, windows-latest]
        node: [18, 20, 22]
        include:                     # 添加额外组合
          - os: ubuntu-latest
            node: 20
            coverage: true
        exclude:                     # 排除组合
          - os: windows-latest
            node: 22
      fail-fast: false               # 一个失败不取消其他

    runs-on: ${{ matrix.os }}
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: ${{ matrix.node }}
      - run: npm test
```

### 依赖关系

```yaml
jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - run: npm run lint

  test:
    needs: lint                      # 等待 lint 完成
    runs-on: ubuntu-latest
    steps:
      - run: npm test

  build:
    needs: [lint, test]              # 等待多个 job
    runs-on: ubuntu-latest
    steps:
      - run: npm run build

  deploy:
    if: github.ref == 'refs/heads/main'
    needs: build
    runs-on: ubuntu-latest
    steps:
      - run: deploy
```

---

## 三、常用 Action

### 官方 Action

```yaml
steps:
  # 检出代码
  - uses: actions/checkout@v4
    with:
      fetch-depth: 0            # 获取完整历史
      ref: ${{ github.head_ref }}

  # 设置 Node.js
  - uses: actions/setup-node@v4
    with:
      node-version: 20
      cache: 'npm'
      registry-url: 'https://registry.npmjs.org'

  # 设置 Python
  - uses: actions/setup-python@v5
    with:
      python-version: '3.12'
      cache: 'pip'

  # 设置 Java
  - uses: actions/setup-java@v4
    with:
      distribution: 'temurin'
      java-version: '21'
      cache: 'maven'

  # 缓存
  - uses: actions/cache@v4
    with:
      path: ~/.npm
      key: ${{ runner.os }}-node-${{ hashFiles('package-lock.json') }}
      restore-keys: |
        ${{ runner.os }}-node-

  # 上传/下载制品
  - uses: actions/upload-artifact@v4
    with:
      name: build-output
      path: dist/

  - uses: actions/download-artifact@v4
    with:
      name: build-output
      path: dist/
```

### 第三方 Action

```yaml
steps:
  # Docker 构建
  - uses: docker/setup-buildx-action@v3
  - uses: docker/login-action@v3
    with:
      username: ${{ secrets.DOCKER_USERNAME }}
      password: ${{ secrets.DOCKER_PASSWORD }}
  - uses: docker/build-push-action@v5
    with:
      push: true
      tags: user/app:latest

  # AWS
  - uses: aws-actions/configure-aws-credentials@v4
    with:
      aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
      aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
      aws-region: us-east-1

  # SSH 部署
  - uses: easingthemes/ssh-deploy@main
    with:
      SSH_PRIVATE_KEY: ${{ secrets.SSH_KEY }}
      ARGS: "-rlgoDzvc -i"
      SOURCE: "dist/"
      REMOTE_HOST: ${{ secrets.REMOTE_HOST }}
      REMOTE_USER: ${{ secrets.REMOTE_USER }}
      TARGET: /var/www/html

  # Slack 通知
  - uses: 8398a7/action-slack@v3
    with:
      status: ${{ job.status }}
      fields: repo,message,commit,author
    env:
      SLACK_WEBHOOK_URL: ${{ secrets.SLACK_WEBHOOK }}
```

---

## 四、环境变量与 Secrets

```yaml
jobs:
  deploy:
    runs-on: ubuntu-latest
    environment: production        # 关联 GitHub 环境
    env:
      NODE_ENV: production

    steps:
      - name: 使用 Secret
        run: |
          echo "${{ secrets.API_KEY }}" | docker login -u user --password-stdin
          echo "部署到 ${{ vars.DEPLOY_TARGET }}"

      - name: 使用 Context
        run: |
          echo "SHA: ${{ github.sha }}"
          echo "Ref: ${{ github.ref }}"
          echo "Actor: ${{ github.actor }}"
          echo "Event: ${{ github.event_name }}"
          echo "Workspace: ${{ github.workspace }}"
```

---

## 五、完整工作流示例

### Node.js 项目

```yaml
name: Node.js CI/CD

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

env:
  NODE_VERSION: 20

jobs:
  quality:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: ${{ env.NODE_VERSION }}
          cache: 'npm'
      - run: npm ci
      - run: npm run lint
      - run: npm run typecheck
      - run: npm audit --audit-level=high

  test:
    needs: quality
    runs-on: ubuntu-latest
    strategy:
      matrix:
        node: [18, 20, 22]
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: ${{ matrix.node }}
          cache: 'npm'
      - run: npm ci
      - run: npm test -- --coverage
      - uses: actions/upload-artifact@v4
        if: ${{ matrix.node == 20 }}
        with:
          name: coverage
          path: coverage/

  build:
    needs: test
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: ${{ env.NODE_VERSION }}
          cache: 'npm'
      - run: npm ci
      - run: npm run build
      - uses: actions/upload-artifact@v4
        with:
          name: build
          path: dist/

  deploy:
    needs: build
    runs-on: ubuntu-latest
    environment: production
    steps:
      - name: Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v4
        with:
          aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
          aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          aws-region: us-east-1
      - uses: actions/download-artifact@v4
        with:
          name: build
          path: dist/
      - name: Deploy to S3
        run: aws s3 sync dist/ s3://my-app-bucket --delete
```

### Python 项目

```yaml
name: Python CI

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ['3.10', '3.11', '3.12']

    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}
          cache: 'pip'
      - run: pip install -r requirements-dev.txt
      - run: ruff check .
      - run: mypy .
      - run: pytest --cov=src
```

### Java / Spring Boot

```yaml
name: Java CI/CD

on:
  push:
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-java@v4
        with:
          distribution: 'temurin'
          java-version: '21'
          cache: 'maven'
      - run: ./mvnw clean verify
      - uses: docker/setup-buildx-action@v3
      - run: ./mvnw spring-boot:build-image
      - uses: docker/login-action@v3
        with:
          registry: ghcr.io
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}
      - run: |
          docker tag my-app:latest ghcr.io/${{ github.repository }}:latest
          docker push ghcr.io/${{ github.repository }}:latest
```

---

## 六、复用工工作流

### Composite Action

```yaml
# .github/actions/setup-node/action.yml
name: 'Setup Node.js'
description: '设置 Node.js 环境并安装依赖'
inputs:
  node-version:
    description: 'Node.js 版本'
    required: false
    default: '18'
runs:
  using: 'composite'
  steps:
    - uses: actions/setup-node@v4
      with:
        node-version: ${{ inputs.node-version }}
        cache: 'npm'
    - run: npm ci
      shell: bash
```

### Reusable Workflow

```yaml
# .github/workflows/deploy.yml（可复用工作流）
name: Deploy

on:
  workflow_call:
    inputs:
      environment:
        required: true
        type: string
    secrets:
      CLOUD_TOKEN:
        required: true

jobs:
  deploy:
    runs-on: ubuntu-latest
    environment: ${{ inputs.environment }}
    steps:
      - run: echo "部署到 ${{ inputs.environment }}"
```

```yaml
# 调用可复用工作流
jobs:
  deploy-staging:
    uses: ./.github/workflows/deploy.yml
    with:
      environment: staging
    secrets:
      CLOUD_TOKEN: ${{ secrets.CLOUD_TOKEN }}
```

## 相关条目

- [[CI-CD与DevOps实践]]
- [[Pipeline]]
- [[Jenkins]]
- [[GitHub]]
- [[Dockerfile]]
