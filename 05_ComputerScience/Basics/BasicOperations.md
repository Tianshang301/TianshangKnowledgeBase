# 计算机基础操作指南

## 文件管理

### 基本操作命令对照表

| 操作 | Windows (图形界面) | Windows (命令行) | Linux/macOS |
|------|-------------------|-----------------|-------------|
| 创建文件 | 右键 → 新建 | `type nul > file.txt` | `touch file.txt` |
| 创建文件夹 | 右键 → 新建文件夹 | `mkdir folder` | `mkdir folder` |
| 复制 | Ctrl+C, Ctrl+V | `copy src dest` | `cp src dest` |
| 移动 | Ctrl+X, Ctrl+V | `move src dest` | `mv src dest` |
| 删除 | Delete / Shift+Delete | `del file` / `rmdir folder` | `rm file` / `rm -rf folder` |
| 重命名 | F2（选中后按F2） | `ren old new` | `mv old new` |
| 查看文件列表 | 打开资源管理器 | `dir` | `ls` |

### 批量重命名示例

```powershell
# PowerShell：批量添加前缀
Get-ChildItem *.jpg | Rename-Item -NewName { "photo_" + $_.Name }
```

## 快捷键大全

### Windows 通用快捷键

| 快捷键 | 功能 |
|--------|------|
| Ctrl+C | 复制 |
| Ctrl+X | 剪切 |
| Ctrl+V | 粘贴 |
| Ctrl+Z | 撤销 |
| Ctrl+Y | 重做 |
| Ctrl+A | 全选 |
| Ctrl+S | 保存 |
| Ctrl+F | 查找 |
| Ctrl+H | 替换 |
| Ctrl+P | 打印 |

### Win 系列快捷键

| 快捷键 | 功能 |
|--------|------|
| Win+D | 显示桌面（切回） |
| Win+E | 打开文件资源管理器 |
| Win+I | 打开设置 |
| Win+L | 锁定电脑 |
| Win+R | 运行对话框 |
| Win+S | 搜索 |
| Win+Tab | 任务视图 |
| Win+V | 剪贴板历史 |
| Win+. | 表情符号面板 |
| Win+Shift+S | 截图（Snip & Sketch） |
| Win+数字键 | 打开任务栏第N个程序 |

## 截图与录屏

### 截图工具对比

| 方法 | 快捷键 | 说明 |
|------|--------|------|
| 全屏截图 | PrintScreen / Win+PrtSc | 保存到剪贴板/图片文件夹 |
| 活动窗口截图 | Alt+PrtSc | 仅当前窗口 |
| 区域截图 | Win+Shift+S | 矩形/任意形状/窗口/全屏 |
| Snipping Tool | Win+S → 搜索"截图" | 带延迟截图的工具 |
| 第三方 | — | Snipaste、ShareX（推荐） |

### 录屏

- **Xbox Game Bar**: `Win+G`，无需额外软件，支持录屏和音频
- **OBS Studio**: 免费开源，专业级录制/推流
- **ScreenRec**: 轻量级，支持即时分享

## 任务管理器

打开方式：`Ctrl+Shift+Esc` 或 `Ctrl+Alt+Del` → 选择任务管理器

### 常用功能

| 选项卡 | 用途 |
|--------|------|
| 进程 | 查看CPU/内存/磁盘占用，结束卡顿程序 |
| 性能 | 监控CPU/内存/磁盘/网络实时使用率 |
| 启动 | 管理开机自启程序（禁用不必要的可提速） |
| 用户 | 查看当前登录用户及其资源占用 |
| 详细信息 | 查看所有进程的PID、优先级等高级信息 |

**实用技巧**：
- 如果程序卡死，在"进程"页右键 → **结束任务**
- 在"启动"页禁用不需要的开机自启程序可显著提升开机速度

## 系统设置常用入口

| 操作 | 路径/快捷键 |
|------|------------|
| 系统设置 | Win+I |
| 控制面板 | Win+R → `control` |
| 设备管理器 | Win+R → `devmgmt.msc` |
| 磁盘管理 | Win+R → `diskmgmt.msc` |
| 网络连接 | Win+R → `ncpa.cpl` |
| 程序和功能 | Win+R → `appwiz.cpl` |
| 系统信息 | Win+R → `msinfo32` |
| 注册表编辑器 | Win+R → `regedit` |
| 组策略编辑器 | Win+R → `gpedit.msc`（专业版/企业版） |
| 服务管理 | Win+R → `services.msc` |

## 相关条目

- [[05_ComputerScience/ProgrammingLanguages/INDEX|ProgrammingLanguages]]
- [[05_ComputerScience/DataStructuresAndAlgorithms/DataStructures/INDEX|DataStructures]]
- [[01_K12/JuniorHigh/Mathematics/INDEX|Mathematics]]
- [[EngineeringFundamentals]]
