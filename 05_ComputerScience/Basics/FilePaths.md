---
aliases: [FilePaths]
tags: ['Basics', 'FilePaths']
created: 2026-05-16
updated: 2026-05-13
---

# 文件路径详解

## 绝对路径 vs 相对路径

| 特性 | 绝对路径 | 相对路径 |
|------|---------|---------|
| 定义 | 从根目录开始的完整路径 | 相对于当前工作目录的路径 |
| Windows 示例 | `C:\Users\Alice\Documents\report.pdf` | `Documents\report.pdf` |
| Unix 示例 | `/home/alice/Documents/report.pdf` | `Documents/report.pdf` |
| 标识 | 以盘符或 `/` 开头 | 不以根分隔符开头 |
| 稳定性 | 不会随工作目录变化 | 随工作目录变化 |
| 适用场景 | 配置文件、快捷方式、日志记录 | 项目内部文件引用 |

## Windows 路径格式

```
C:\Users\Alice\Documents\Projects\main.py
```

- 盘符：`C:`、`D:` 等
- 反斜杠 `\` 作为分隔符
- 最大路径长度：默认 260 字符（可通过组策略启用长路径）
- 根目录：`C:\`
- 当前用户目录：`C:\Users\用户名\`

### 特殊 Windows 路径

| 路径 | 含义 |
|------|------|
| `C:\Users\用户名` | 用户主目录 (`%USERPROFILE%`) |
| `C:\Program Files` | 64位程序安装目录 |
| `C:\Program Files (x86)` | 32位程序安装目录 |
| `C:\Windows\System32` | 系统关键文件 |
| `C:\Users\用户名\AppData` | 应用程序数据（Roaming/Local/LocalLow） |
| `\\Server\Share` | UNC 网络路径 |

## Unix/Linux 路径格式

```
/home/alice/Documents/Projects/main.py
```

- 以根 `/` 开头
- 正斜杠 `/` 作为分隔符
- 区分大小写（`File.txt` 和 `file.txt` 不同）
- 无盘符概念

### 标准目录结构

| 目录 | 用途 |
|------|------|
| `/` | 根目录 |
| `/home` | 用户主目录 |
| `/etc` | 系统配置文件 |
| `/var` | 可变数据（日志、数据库） |
| `/tmp` | 临时文件 |
| `/usr` | 用户程序和数据 |
| `/bin`, `/sbin` | 可执行文件 |

## 特殊目录

| 符号 | 含义 | 示例 |
|------|------|------|
| `.` | 当前目录 | `./script.py` = `script.py` |
| `..` | 父目录 | `../config.json` 表示上级目录中的文件 |
| `~` | 用户主目录 | `~/Documents` = `/home/alice/Documents` |
| `~用户名` | 指定用户主目录 | `~bob/project` |

### 示例：相对路径导航

```bash
# 当前目录：C:\Users\Alice\Projects
# 目标：C:\Users\Alice\Documents\notes.txt

# 相对路径
..\Documents\notes.txt

# 绝对路径
C:\Users\Alice\Documents\notes.txt
```

## 路径分隔符差异

| 系统 | 分隔符 | 转义 |
|------|--------|------|
| Windows | `\` (反斜杠) | 在字符串中写作 `\\` |
| Unix/Linux/macOS | `/` (正斜杠) | 无需转义 |

> **历史原因**：Windows 继承自 MS-DOS，使用 `\` 作为分隔符。Unix 使用 `/`。

### 跨平台兼容技巧

```python
# Python: 使用 pathlib（推荐）
from pathlib import Path

# 自动使用当前平台的分隔符
path = Path("documents") / "projects" / "main.py"
# Windows: documents\projects\main.py
# Linux:   documents/projects/main.py

# 强制使用正斜杠（JSON、URL 等场景）
url_path = "documents/projects/main.py"  # 始终用 /
```

## 代码中正确处理路径

### Python pathlib（推荐）

```python
from pathlib import Path

# 获取当前文件所在目录
BASE_DIR = Path(__file__).resolve().parent

# 拼接路径
data_path = BASE_DIR / "data" / "input.csv"

# 路径属性
print(data_path.name)       # input.csv
print(data_path.stem)       # input
print(data_path.suffix)     # .csv
print(data_path.parent)     # 父目录

# 检查路径
data_path.exists()
data_path.is_file()
data_path.is_dir()

# 遍历目录
for f in Path(".").glob("*.py"):
    print(f)

# 递归遍历
for f in Path("src").rglob("*.py"):
    print(f)

# 创建目录
Path("output/images").mkdir(parents=True, exist_ok=True)
```

### Python os.path（传统方式）

```python
import os

# 获取绝对路径
abs_path = os.path.abspath("relative/path")

# 拼接路径
full_path = os.path.join("base", "dir", "file.txt")

# 分离路径
dir_name = os.path.dirname("/path/to/file.txt")   # /path/to
base_name = os.path.basename("/path/to/file.txt")  # file.txt

# 拆分扩展名
name, ext = os.path.splitext("image.png")  # ('image', '.png')
```

## UNC 路径

**UNC** (Universal Naming Convention) 用于访问网络共享资源。

### 格式

```
\\ServerName\ShareName\Path\File
```

| 部分 | 含义 | 示例 |
|------|------|------|
| `\\ServerName` | 服务器名称或 IP | `\\fileserver` 或 `\\192.168.1.100` |
| `\ShareName` | 共享文件夹名 | `\documents` |
| `\Path\File` | 共享内的路径 | `\projects\report.docx` |

### 示例

```
\\nas-server\shared\projects\design-v3\mockup.fig
\\192.168.1.50\public\tools\installer.exe
```

### 在代码中使用 UNC

```python
from pathlib import Path

unc_path = Path(r"\\nas-server\shared\data\results.csv")
if unc_path.exists():
    with open(unc_path, "r") as f:
        content = f.read()
```

> **注意**：Python 中使用 UNC 路径时，建议使用原始字符串 `r"\\server\share"` 避免反斜杠转义问题。
