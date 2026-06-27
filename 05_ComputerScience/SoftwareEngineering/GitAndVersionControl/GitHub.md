---
aliases: [GitHub, GitHub 使用]
tags: ['SoftwareEngineering', 'GitAndVersionControl', 'GitHub']
created: 2026-05-17
updated: 2026-05-13
---

# GitHub 使用 (GitHub Usage)

## 一、仓库设置

### 创建仓库

```bash
# 命令行创建
gh repo create my-project --public --clone

# 从本地推送
git remote add origin https://github.com/user/repo.git
git branch -M main
git push -u origin main
```

### 仓库设置选项

| 设置 | 说明 |
|------|------|
| Public / Private | 公开/私有仓库 |
| README | 自动生成介绍文件 |
| .gitignore | 选择语言模板 |
| License | 开源许可证 |
| Branch protection | 分支保护规则 |
| Topics | 仓库主题标签 |

### 分支保护规则

```yaml
# Settings -> Branches -> Add rule
Branch name pattern: main
Require pull request reviews before merging: 2
Dismiss stale pull request approvals when new commits are pushed
Require status checks to pass before merging
  - continuous-integration/ci
  - lint
  - test
```

## 二、Issues 与 Project Boards

### Issue 模板

```yaml
# .github/ISSUE_TEMPLATE/bug_report.md
---
name: Bug 报告
about: 创建报告帮助改进
title: "[Bug] "
labels: bug
assignees: ''
---

**描述问题**
清晰简洁地描述问题。

**重现步骤**
1. 访问 '...'
2. 点击 '....'
3. 看到错误

**期望行为**
清晰描述期望的结果。

**环境信息**
 - 操作系统: [e.g. Windows 10]
 - 浏览器: [e.g. Chrome 120]
 - 版本: [e.g. v1.2.0]
```

### Labels 管理

| 标签 | 含义 |
|------|------|
| bug | 需要修复的问题 |
| enhancement | 新功能 |
| documentation | 文档相关 |
| good first issue | 适合新手 |
| help wanted | 需要帮助 |
| question | 需要解答 |
| duplicate | 重复 Issue |
| priority-high | 高优先级 |

### Project Boards (Projects v2)

| To Do | In Progress | Review | Done |
|-------|-------------|--------|------|
| #123 登录 | #125 注册 | #127 搜索 | #120 首页 |
| #124 权限 | #126 日志 | | #121 404页 |

## 三、Pull Request 工作流

### 创建 PR

```bash
# 1. 创建分支
git checkout -b feature/awesome main
# 2. 开发并提交
git add .
git commit -m "feat: 添加超棒功能"
# 3. 推送
git push -u origin feature/awesome
# 4. 创建 PR
gh pr create --title "feat: 添加超棒功能" --body "实现了..." --base main
```

### PR 模板

```markdown
# .github/PULL_REQUEST_TEMPLATE.md

## 变更类型
- [ ] 新功能 (feat)
- [ ] Bug 修复 (fix)
- [ ] 重构 (refactor)
- [ ] 性能优化 (perf)
- [ ] 文档更新 (docs)
- [ ] 测试 (test)
- [ ] CI/CD (ci)

## 描述
请在此描述变更内容和动机。

## 关联 Issue
Fixes #123

## 测试
- [ ] 单元测试通过
- [ ] 集成测试通过
- [ ] 手动测试完成
```

### PR 合并选项

| 合并方式 | 效果 | 适用场景 |
|----------|------|----------|
| Create a merge commit | 保留所有提交，产生合并提交 | 团队合作分支 |
| Squash and merge | 压缩为单个提交，历史干净 | 完成的功能 |
| Rebase and merge | 变基到目标分支，无合并提交 | 个人分支 |

## 四、代码审查

### 审查评论级别

```text
级别 1: 建议 (Suggestion)
  "个人建议，不是强制要求"

级别 2: 问题 (Question)
  "这里有点困惑，能解释一下吗？"

级别 3: 阻塞 (Blocking)
  "这个逻辑有 bug，需要修改"
```

### Suggest Changes

GitHub 支持直接在评论中插入代码建议：

```suggestion
-const result = await fetch(url).then(res => res.json());
+const response = await fetch(url);
+const result = await response.json();
```

## 五、GitHub Actions

### 基本工作流

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
    strategy:
      matrix:
        node-version: [18, 20]

    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: ${{ matrix.node-version }}
      - run: npm ci
      - run: npm test
      - run: npm run build
```

### 常用 Actions

| Action | 用途 |
|--------|------|
| actions/checkout | 检出代码 |
| actions/setup-node | 设置 Node.js |
| actions/cache | 缓存依赖 |
| actions/upload-artifact | 上传构建产物 |
| actions/download-artifact | 下载构建产物 |
| actions/deploy-pages | 部署到 GitHub Pages |

## 六、GitHub Pages

```bash
# 从 main 分支发布
# Settings -> Pages -> Source: Deploy from a branch
# Branch: main, / (root) 或 /docs
```

```yaml
# .github/workflows/pages.yml
name: Deploy to GitHub Pages

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      pages: write
      id-token: write

    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 18
      - run: npm ci
      - run: npm run build
      - uses: actions/configure-pages@v3
      - uses: actions/upload-pages-artifact@v2
        with:
          path: './dist'
      - id: deployment
        uses: actions/deploy-pages@v2
```

## 七、安全

### Dependabot

```yaml
# .github/dependabot.yml
version: 2
updates:
  - package-ecosystem: "npm"
    directory: "/"
    schedule:
      interval: "weekly"
    open-pull-requests-limit: 10

  - package-ecosystem: "github-actions"
    directory: "/"
    schedule:
      interval: "weekly"
```

### Secret Scanning

```bash
# 安装 git-secrets 防止提交密钥
git secrets --install
git secrets --register-aws

# 扫描历史中的密钥
git secrets --scan-history
```

## 八、GitHub CLI 常用命令

```bash
# 认证
gh auth login
gh auth status

# 仓库
gh repo create my-project --public
gh repo clone user/repo
gh repo view user/repo

# Issue
gh issue list
gh issue create --title "Bug" --body "描述"
gh issue view 123
gh issue close 123

# PR
gh pr list
gh pr create --title "feat: xxx" --body "描述"
gh pr checkout 123
gh pr review 123 --approve
gh pr merge 123 --squash

# CI
gh run list
gh run view
gh run watch

# 发布
gh release create v1.0.0 --title "v1.0.0" --notes "发布说明"
```

## 相关条目

- [[GitHubActions]]
- [[Workflow]]
- [[Branch]]
- [[Commands]]
- [[Advanced]]
