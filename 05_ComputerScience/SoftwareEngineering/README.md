---
aliases: [README]
tags: ['SoftwareEngineering', 'README']
created: 2026-05-16
updated: 2026-05-16
---

# IDE 配置与效率技巧

## VS Code

### 常用快捷键

| 快捷键 | 功能 |
|--------|------|
| `Ctrl+P` | 快速打开文件 |
| `Ctrl+Shift+P` | 命令面板 |
| `Ctrl+\`` | 打开终端 |
| `Ctrl+B` | 切换侧栏 |
| `Ctrl+D` | 选中下一个相同词 |
| `Alt+↑/↓` | 移动行 |
| `Shift+Alt+↑/↓` | 复制行 |
| `Ctrl+/` | 行注释 |
| `Shift+Alt+A` | 块注释 |
| `Ctrl+Shift+K` | 删除行 |
| `F2` | 重命名符号 |
| `F12` | 跳转到定义 |
| `Ctrl+-` | 返回上一次位置 |
| `Ctrl+Shift+F` | 全局搜索 |
| `Ctrl+Shift+H` | 全局替换 |
| `Ctrl+` + `` ` `` | 多光标编辑 |

### settings.json 配置要点

```jsonc
{
  // 编辑器
  "editor.fontSize": 14,
  "editor.fontFamily": "'Cascadia Code', 'JetBrains Mono', monospace",
  "editor.fontLigatures": true,
  "editor.tabSize": 2,
  "editor.renderWhitespace": "boundary",
  "editor.formatOnSave": true,
  "editor.codeActionsOnSave": {
    "source.fixAll.eslint": "explicit",
    "source.organizeImports": "explicit"
  },
  "editor.minimap.enabled": false,
  "editor.bracketPairColorization.enabled": true,
  "editor.guides.indentation": true,
  "editor.cursorBlinking": "smooth",

  // 文件
  "files.autoSave": "onFocusChange",
  "files.exclude": {
    "**/node_modules": true,
    "**/__pycache__": true,
    "**/.git": true
  },

  // 终端
  "terminal.integrated.defaultProfile.windows": "PowerShell",
  "terminal.integrated.fontSize": 13,
  "terminal.integrated.cursorBlinking": true,

  // 工作台
  "workbench.colorTheme": "One Dark Pro",
  "workbench.iconTheme": "material-icon-theme",
  "workbench.startupEditor": "readme",

  // Git
  "git.enableSmartCommit": true,
  "git.confirmSync": false,
  "git.autofetch": true,

  // 语言特定配置
  "[python]": {
    "editor.tabSize": 4,
    "editor.formatOnSave": true
  },
  "[javascript]": {
    "editor.tabSize": 2
  }
}
```

### 必备插件推荐

| 插件 | 用途 |
|------|------|
| **Prettier** | 代码格式化 |
| **ESLint** | JavaScript/TypeScript 语法检查 |
| **Python** | Python 语言支持 |
| **Live Share** | 实时协作编辑 |
| **GitLens** | Git 历史查看增强 |
| **Error Lens** | 行内错误显示 |
| **Path Intellisense** | 路径智能提示 |
| **Material Icon Theme** | 文件图标主题 |

### LaTeX Workshop

```jsonc
// settings.json 中 LaTeX 配置
{
  "latex-workshop.latex.tools": [
    {
      "name": "xelatex",
      "command": "xelatex",
      "args": [
        "-synctex=1",
        "-interaction=nonstopmode",
        "-file-line-error",
        "%DOC%"
      ]
    }
  ],
  "latex-workshop.latex.recipes": [
    {
      "name": "xelatex",
      "tools": ["xelatex"]
    },
    {
      "name": "xelatex -> bibtex -> xelatex*2",
      "tools": ["xelatex", "bibtex", "xelatex", "xelatex"]
    }
  ],
  "latex-workshop.view.pdf.viewer": "tab",
  "latex-workshop.latex.autoBuild.run": "onFileChange"
}
```

### Remote SSH 开发

```bash
# 安装 Remote SSH 扩展后配置
# ~/.ssh/config
Host dev-server
    HostName 192.168.1.100
    User developer
    Port 22
    IdentityFile ~/.ssh/id_ed25519

# VS Code 中操作
# Ctrl+Shift+P → Remote-SSH: Connect to Host → 选择 dev-server
```

## JetBrains 系列

### 各产品差异

| IDE | 语言 | 适用场景 |
|-----|------|----------|
| **IntelliJ IDEA** | Java, Kotlin, 多种语言 | Java/Android 开发 |
| **PyCharm** | Python | Python 数据分析/Web |
| **CLion** | C/C++ | 嵌入式、系统开发 |
| **GoLand** | Go | Go 微服务开发 |
| **WebStorm** | JavaScript/TypeScript | 前端/Node.js 开发 |
| **RubyMine** | Ruby | Rails 开发 |
| **DataGrip** | SQL | 数据库管理 |

### JetBrains 快捷键

| 快捷键 | 功能 |
|--------|------|
| `Shift+Shift` | 全局搜索（双击 Shift） |
| `Ctrl+Shift+A` | 查找动作 |
| `Alt+Enter` | 快速修复 |
| `Ctrl+Alt+L` | 格式化代码 |
| `Ctrl+Shift+F` | 全局搜索 |
| `Ctrl+E` | 最近文件 |
| `Ctrl+W` | 递进选择 |
| `Ctrl+Shift+↑/↓` | 移动代码块 |
| `Ctrl+D` | 复制行 |
| `Ctrl+Y` | 删除行 |
| `Alt+Insert` | 生成代码（getter/setter/构造器） |
| `Ctrl+Alt+O` | 优化导入 |
| `Shift+F6` | 重命名 |
| `Ctrl+B` | 跳转到定义 |

### JetBrains 配置迁移

```bash
# 导出配置
File → Manage IDE Settings → Export Settings

# 同步设置 (IntelliJ IDEA)
File → Settings → Tools → Settings Repository

# 使用 .idea 目录共享项目配置
# 推荐放入 .gitignore 的内容
.idea/workspace.xml
.idea/tasks.xml
.idea/shelf/
```

## VSCode vs JetBrains 对比

| 维度 | VS Code | JetBrains |
|------|---------|-----------|
| **启动速度** | 快 | 较慢 |
| **内存占用** | 低~中 | 高 |
| **开箱即用** | 需配置插件 | 功能完整 |
| **语言支持深度** | 需插件 | 原生深度支持 |
| **重构能力** | 基础 | 强大 |
| **调试器** | 良好 | 优秀 |
| **价格** | 免费 | 付费（社区版免费） |
| **扩展生态** | 极其丰富 | 丰富 |
| **Git 集成** | 良好 | 优秀 |

**选择建议**：
- 全栈/前端开发 → VS Code
- Java/Kotlin 开发 → IntelliJ IDEA
- Python 数据分析 → VS Code 或 PyCharm
- 大型项目重构 → JetBrains
- 资源有限的设备 → VS Code

## 远程开发

### SSH 远程开发

```bash
# 服务器上安装开发环境
# VS Code Remote-SSH 或 JetBrains Gateway

# JetBrains Gateway
# 下载 Gateway → SSH 连接服务器 → 选择 IDE → 开始远程开发

# 端口转发（开发环境调试）
ssh -L 3000:localhost:3000 dev-server
```

### Dev Containers

```jsonc
// .devcontainer/devcontainer.json
{
  "name": "Python 3.11 Dev",
  "image": "mcr.microsoft.com/devcontainers/python:3.11",
  "features": {
    "ghcr.io/devcontainers/features/node:1": {}
  },
  "customizations": {
    "vscode": {
      "extensions": [
        "ms-python.python",
        "ms-python.vscode-pylance",
        "GitHub.copilot"
      ],
      "settings": {
        "python.defaultInterpreterPath": "/usr/local/bin/python"
      }
    }
  },
  "postCreateCommand": "pip install -r requirements.txt",
  "forwardPorts": [8000],
  "remoteUser": "vscode"
}
```

### GitHub Codespaces

``` yaml
# .devcontainer/devcontainer.json (用于 Codespaces)
{
  "name": "Node.js Development",
  "image": "mcr.microsoft.com/devcontainers/javascript-node:18",
  "hostRequirements": {
    "cpus": 4,
    "memory": "8gb",
    "storage": "32gb"
  },
  "postCreateCommand": "npm install",
  "portsAttributes": {
    "3000": {
      "label": "Application",
      "onAutoForward": "openBrowser"
    }
  }
}

```

## 相关条目

- [[05_ComputerScience/SoftwareEngineering/AgileMethodologies/AgileMethodologies|AgileMethodologies]]
- [[05_ComputerScience/SoftwareEngineering/DesignPatterns/DesignPatterns|DesignPatterns]]
- [[05_ComputerScience/SoftwareEngineering/SoftwareTesting/SoftwareTesting|SoftwareTesting]]
- [[11_ManagementSciences/ManagementScienceAndEngineering/ProjectManagement|ProjectManagement]]


