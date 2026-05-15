# 命令行 vs 图形界面

## 对比总览

| 维度 | CLI (命令行) | GUI (图形界面) |
|------|-------------|---------------|
| 学习曲线 | 陡峭（需记住命令） | 平缓（直观可见） |
| 操作效率 | 极高（批量、管道、脚本） | 中等（点击拖拽） |
| 自动化能力 | 强（脚本化、定时任务） | 弱（依赖宏/自动化工具） |
| 资源占用 | 极低 | 较高 |
| 远程操作 | 原生支持（SSH） | 需要远程桌面/VNC |
| 可重复性 | 精确可重复 | 手动操作易出错 |
| 可视化能力 | 弱 | 强（图表、图像编辑等） |
| 批量处理 | 一行命令处理上千文件 | 逐一操作繁琐 |
| 错误恢复 | 命令可重试、可脚本化回滚 | 通常需要手动恢复 |

## 何时用 CLI

| 场景 | 原因 | 示例 |
|------|------|------|
| **批量文件操作** | 一行命令处理数千文件 | `find . -name "*.tmp" -delete` |
| **自动化/脚本** | 定时任务、CI/CD 流水线 | cron + shell script |
| **远程服务器管理** | SSH 即可，无需图形界面 | `ssh user@host` |
| **开发工具** | 编译器、版本控制更高效 | `git`, `gcc`, `npm` |
| **资源受限环境** | 嵌入式系统、容器、旧硬件 | Docker 容器内操作 |
| **数据处理** | 管道组合处理文本/日志 | `grep \| awk \| sort \| uniq` |

### CLI 示例：批量重命名图片

```bash
# 将所有 .jpg 文件重命名为 IMG_0001.jpg, IMG_0002.jpg, ...
# Windows PowerShell
$i = 1; Get-ChildItem *.jpg | Rename-Item -NewName { "IMG_{0:D4}{1}" -f $i++, $_.Extension }

# Linux/macOS
i=1; for f in *.jpg; do mv "$f" "IMG_$(printf %04d $i).jpg"; i=$((i+1)); done
```

## 何时用 GUI

| 场景 | 原因 | 示例 |
|------|------|------|
| **图形设计/视频编辑** | 需要视觉反馈 | Photoshop, Premiere, Figma |
| **新手入门** | 降低认知负荷 | 文件管理器、浏览器设置 |
| **复杂配置界面** | 多选项可视化呈现 | 系统设置、IDE 配置 |
| **文档阅读/编辑** | WYSIWYG 更自然 | Word, OneNote, Obsidian |
| **监控仪表盘** | 实时图表更直观 | Grafana, 任务管理器图表 |

## CLI 基础命令速查

### 文件操作对照

| 操作 | Windows (CMD) | Windows (PowerShell) | Linux/macOS (Bash) |
|------|--------------|---------------------|-------------------|
| 列出文件 | `dir` | `ls` / `Get-ChildItem` | `ls` |
| 切换目录 | `cd path` | `cd path` | `cd path` |
| 当前目录 | `cd` | `pwd` / `Get-Location` | `pwd` |
| 创建目录 | `mkdir name` | `mkdir name` | `mkdir name` |
| 删除文件 | `del file` | `Remove-Item file` | `rm file` |
| 删除目录 | `rmdir /s folder` | `Remove-Item -Recurse folder` | `rm -rf folder` |
| 复制文件 | `copy src dst` | `Copy-Item src dst` | `cp src dst` |
| 移动/重命名 | `move src dst` | `Move-Item src dst` | `mv src dst` |
| 查看文件内容 | `type file` | `Get-Content file` / `cat file` | `cat file` |
| 清屏 | `cls` | `cls` / `Clear-Host` | `clear` |
| 查找字符串 | `findstr pattern` | `Select-String pattern` | `grep pattern` |
| 查看帮助 | `command /?` | `Get-Help command` | `man command` |

### 管道示例

```bash
# CMD: 查找所有 log 文件中包含 "ERROR" 的行并排序
findstr "ERROR" *.log | sort

# PowerShell: 查找占用内存前 5 的进程
Get-Process | Sort-Object WorkingSet -Descending | Select-Object -First 5

# Bash: 统计每个 IP 的访问次数
cat access.log | awk '{print $1}' | sort | uniq -c | sort -nr
```

## PowerShell vs Cmd vs Bash

| 特性 | Cmd (cmd.exe) | PowerShell | Bash |
|------|--------------|-----------|------|
| 平台 | Windows | Windows, Linux, macOS | Linux, macOS, WSL |
| 输出类型 | 文本 (string) | 对象 (Object) | 文本 (string) |
| 脚本语言 | 批处理 (.bat) | PowerShell (.ps1) | Shell Script (.sh) |
| 大小写敏感 | 否 | 否 | 是 |
| 路径分隔符 | `\` | `\` (可处理 `/`) | `/` |
| 管道传递 | 文本 | 对象（.NET 对象） | 文本 |
| 模块系统 | 无 | 丰富（PowerShell Gallery） | 丰富（apt, brew 等） |
| 现代程度 | 老旧（1980s） | 现代（2006+） | 现代（1970s+不断进化） |

### PowerShell 优势示例

```powershell
# Cmd 只能操作文本
ipconfig | findstr "IPv4"

# PowerShell 操作对象，可以直接访问属性
Get-NetIPAddress | Where-Object { $_.AddressFamily -eq "IPv4" } | Select-Object IPAddress

# 管理 Windows 服务
Get-Service | Where-Object { $_.Status -eq "Running" } | Restart-Service

# 操作 CSV
Import-Csv data.csv | Where-Object { $_.Age -gt 18 } | Export-Csv result.csv
```

### Bash 优势示例

```bash
# 强大的文本处理管道
ps aux | grep python | awk '{print $2, $11}' | sort -k2

# 一行命令下载并执行
curl -sSL https://example.com/install.sh | bash

# 文件监控
tail -f /var/log/syslog | grep --line-buffered "ERROR"

# 进程替换
diff <(ls dir1) <(ls dir2)
```

## 实用技巧

### 查看命令历史

```powershell
# PowerShell
Get-History

# Cmd
doskey /history

# Bash
history
```

### 重复执行上次命令

| 快捷键/命令 | 效果 |
|------------|------|
| 上箭头 | 浏览历史 |
| `!!` (Bash) | 执行上一条命令 |
| `!$` (Bash) | 上一个命令的最后一个参数 |
| `r` (PowerShell) | 搜索命令历史（输入后按 F8） |
| `F3` (Cmd) | 重复上一个命令 |

### 快速打开终端

| 系统 | 快捷键 |
|------|--------|
| Windows Terminal | Win+ 右键 → "在终端中打开" |
| 当前目录开 CMD | 地址栏输入 `cmd` 回车 |
| macOS | 访达 → 服务 → 新建位于文件夹位置的终端标签页 |
| VS Code | Ctrl+` (反引号) 打开集成终端 |
