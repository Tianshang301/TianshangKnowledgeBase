---
aliases: [LearningPath]
tags: ['SoftwareEngineering', 'LearningPath']
created: 2026-05-16
updated: 2026-05-16
---

# 工具链学习路线图

## 必须掌握 (Must-Learn)

### 1. Git - 版本控制

**日常工作流：**
```bash
git clone <repo>
git checkout -b feature-branch
git add <file>
git commit -m "message"
git push origin feature-branch
git checkout main
git pull
git merge feature-branch
```

**进阶操作：**
- 合并冲突解决
- `git rebase` vs `git merge`
- `git stash` 暂存工作
- `git bisect` 二分查找 bug
- `git log` 高级查询

**资源：**
- Learn Git Branching（交互式教学）
- Pro Git 书（免费在线）

### 2. Shell (Bash / PowerShell)

**Bash 核心命令：**
```bash
# 文件操作
ls, cd, pwd, cp, mv, rm, mkdir, touch, find

# 查看文件
cat, less, head, tail, wc, sort, uniq

# 文本处理
grep, sed, awk, cut, tr

# 权限
chmod, chown

# 进程
ps, top, kill, nohup
```

**PowerShell 核心：**
```powershell
Get-ChildItem, Set-Location, Copy-Item, Move-Item
Remove-Item, New-Item, Get-Content
Select-String (类似 grep)
Where-Object, ForEach-Object
```

**脚本基础：**
- 变量、条件判断、循环
- 函数定义
- 管道和重定向

### 3. 正则表达式

**核心概念：**
- `.` 任意字符，`*` 零次或多次，`+` 一次或多次
- `?` 零次或一次，`[]` 字符集
- `()` 分组，`|` 或，`^` 开头，`$` 结尾
- `\d` 数字，`\w` 单词字符，`\s` 空白

**示例：**
```python
import re
# 匹配邮箱
pattern = r'[\w.-]+@[\w.-]+\.\w+'
# 匹配 URL
pattern = r'https?://[\w./-]+'
# 替换
re.sub(r'\s+', ' ', text)
```

### 4. 编辑器 (VS Code / Vim)

**VS Code 必学：**
- 快捷键：Ctrl+P 文件搜索，Ctrl+Shift+P 命令面板
- 多光标编辑：Alt+Click
- 集成终端
- 插件：Live Share、GitLens、Prettier

**Vim 入门：**
- 模式切换：i 插入，Esc 正常，v 可视
- 导航：h/j/k/l，w/b，0/$
- 编辑：dd 删除行，yy 复制，p 粘贴
- 保存退出：:wq，:q!

## 项目工具 (Project Tools)

### 1. Docker

**核心概念：**
- **镜像 (Image)**：应用的只读模板
- **容器 (Container)**：镜像的运行实例
- **Dockerfile**：构建镜像的脚本

**基本命令：**
```bash
docker build -t myapp .
docker run -d -p 8080:80 myapp
docker ps
docker logs <container>
docker exec -it <container> bash
docker-compose up -d
```

**Docker Compose：**
```yaml
version: '3'
services:
  web:
    build: .
    ports:
      - "5000:5000"
  db:
    image: postgres
    environment:
      POSTGRES_PASSWORD: example
```

### 2. CI/CD 基础

**GitHub Actions 示例：**
```yaml
name: CI
on: [push]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - run: npm install
      - run: npm test
```

## 高级工具

| 工具 | 用途 | 学习难度 |
|------|------|---------|
| Kubernetes | 容器编排 | ⭐⭐⭐⭐⭐ |
| Terraform | 基础设施即代码 | ⭐⭐⭐⭐ |
| Ansible | 配置管理 | ⭐⭐⭐ |
| Prometheus + Grafana | 监控 | ⭐⭐⭐⭐ |
| ELK Stack | 日志管理 | ⭐⭐⭐⭐ |

## 学习顺序建议

1. **第 1 周**：Git 基础（add/commit/push/pull）
2. **第 2 周**：Shell 基础（cd/ls/grep/管道）
3. **第 3 周**：VS Code 高效使用
4. **第 4 周**：正则表达式
5. **第 2 个月**：Docker + Docker Compose
6. **第 3 个月**：CI/CD 基础
7. **长期**：K8s / Terraform 等高级工具

## 学习资源

- **Git**：Pro Git 书籍
- **Shell**：The Linux Command Line（William Shotts）
- **Docker**：Docker 官方文档 + Play with Docker
- **正则**：RegexOne 交互式教学
- **Vim**：vimtutor（终端直接运行）

