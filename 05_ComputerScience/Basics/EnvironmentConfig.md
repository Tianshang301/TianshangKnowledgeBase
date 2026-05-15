---
aliases: [EnvironmentConfig]
tags: ['Basics', 'EnvironmentConfig']
---

# 环境配置完全指南

## PATH 环境变量

### 什么是 PATH

PATH 是一个操作系统环境变量，告诉系统在哪里查找可执行文件。当你在命令行输入一个命令（如 `python`、`java`），系统会按顺序搜索 PATH 中列出的每个目录。

### 查看 PATH

```powershell
# Windows (PowerShell)
Get-ChildItem Env:Path
# 或
echo $env:Path

# Windows (CMD)
echo %PATH%

# Linux/macOS
echo $PATH
```

### 修改 PATH

#### 图形界面（Windows）

1. `Win+R` → `sysdm.cpl` → 高级 → 环境变量
2. 在"系统变量"或"用户变量"中找到 `Path` → 编辑
3. 点击"新建" → 粘贴目录路径 → 确定

#### 命令行（Windows PowerShell）

```powershell
# 临时添加（仅当前会话有效）
$env:Path += ";C:\MyTools"

# 永久添加（用户级别）
[Environment]::SetEnvironmentVariable("Path", $env:Path + ";C:\MyTools", "User")

# 永久添加（系统级别，需要管理员权限）
[Environment]::SetEnvironmentVariable("Path", $env:Path + ";C:\MyTools", "Machine")
```

#### 命令行（Linux/macOS）

```bash
# 临时添加
export PATH=$PATH:/opt/myapp/bin

# 永久添加（写入 ~/.bashrc 或 ~/.zshrc）
echo 'export PATH=$PATH:/opt/myapp/bin' >> ~/.bashrc
source ~/.bashrc
```

## JAVA_HOME 配置

### 为什么需要 JAVA_HOME

许多 Java 应用（Maven、Gradle、Tomcat、Jenkins）依赖 `JAVA_HOME` 环境变量来定位 JDK。

### 配置步骤

1. 安装 JDK（如 `C:\Program Files\Java\jdk-17`）
2. 新建系统变量：
   - 变量名：`JAVA_HOME`
   - 变量值：`C:\Program Files\Java\jdk-17`
3. 在 `Path` 中添加：`%JAVA_HOME%\bin`

### 验证

```bash
echo %JAVA_HOME%   # Windows
java -version
javac -version
```

## Python 环境变量配置

### 标准配置

```powershell
# Python 安装目录
C:\Users\Username\AppData\Local\Programs\Python\Python311

# Scripts 目录（包含 pip）
C:\Users\Username\AppData\Local\Programs\Python\Python311\Scripts
```

> **提示**：安装 Python 时勾选 **"Add Python to PATH"** 可自动配置。

### 多版本 Python 管理

使用 `py` 启动器（Windows）或 `update-alternatives`（Linux）：

```bash
# Windows: 使用 py 启动器
py -3.10 script.py   # 使用 Python 3.10
py -3.11 script.py   # 使用 Python 3.11

# Linux: update-alternatives
sudo update-alternatives --config python3
```

## 系统变量 vs 用户变量

| 特性 | 用户变量 | 系统变量 |
|------|---------|---------|
| 作用范围 | 当前用户 | 所有用户 |
| 优先级 | 高于系统变量 | 低于用户变量 |
| 修改权限 | 无需管理员 | 需要管理员权限 |
| 典型存储 | `%USERPROFILE%` 相关路径 | `C:\Windows\System32` 等系统路径 |

**优先级规则**：当同名变量冲突时，系统先读取系统变量，再读取用户变量，用户变量会覆盖系统变量。而 PATH 是合并的：`系统PATH + 用户PATH`。

## 命令行临时设置环境变量

### Windows

```powershell
# PowerShell 设置临时变量
$env:MY_VAR = "hello"
$env:JAVA_HOME = "C:\Program Files\Java\jdk-17"

# CMD 设置临时变量
set MY_VAR=hello
set JAVA_HOME=C:\Program Files\Java\jdk-17
```

### Linux/macOS

```bash
# 设置临时变量（仅当前 shell 和子进程有效）
export MY_VAR="hello"

# 单行命令设置变量
MY_VAR="hello" python script.py

# 取消设置
unset MY_VAR
```

## .env 文件管理

### 什么是 .env 文件

`.env` 文件用于存储环境变量（特别是敏感信息如 API 密钥），**不应该提交到 Git 仓库**。

### 格式规范

```env
# .env 文件示例
DATABASE_URL=postgresql://user:pass@localhost:5432/mydb
API_KEY=sk-abc123def456
DEBUG=true
PORT=3000
NODE_ENV=production
```

### Python 中使用 .env

```bash
pip install python-dotenv
```

```python
from dotenv import load_dotenv
import os

load_dotenv()  # 加载 .env 文件

database_url = os.getenv("DATABASE_URL")
api_key = os.getenv("API_KEY")
debug = os.getenv("DEBUG", "false")  # 默认值
```

### .gitignore 配置

```gitignore
# .gitignore
.env
.env.local
.env.*.local
```

### 最佳实践

| 实践 | 说明 |
|------|------|
| 提供 `.env.example` | 提交模板到仓库，包含所有变量名但不含真实值 |
| 不使用空格 | 值中不要加引号（除非值本身包含空格） |
| 不用引号包裹 | 除非值包含空格，如 `SECRET="my secret"` |
| 不使用换行 | 每行一个键值对 |
| 生产环境禁掉 DEBUG | `.env.production` 中的 `DEBUG=false` |
