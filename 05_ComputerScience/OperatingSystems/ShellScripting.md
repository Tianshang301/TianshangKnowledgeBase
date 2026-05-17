---
aliases: [ShellScripting]
tags: ['05_ComputerScience', 'OperatingSystems']
---

# Shell 脚本编程 (Shell Scripting)

## 一、概述 (Overview)

Shell 脚本是 Linux/Unix 系统中的命令行脚本语言，用于自动化系统管理任务、批量处理和工具链集成。Bash (Bourne Again SHell) 是最常用的 Shell，兼容 POSIX 标准。

### Shell 类型

| Shell | 路径 | 特点 | 默认系统 |
|-------|------|------|---------|
| Bash | `/bin/bash` | 功能丰富，Linux 默认 | 大多数 Linux |
| Zsh | `/bin/zsh` | 高级补全，主题支持 | macOS (Catalina+) |
| Fish | `/usr/bin/fish` | 语法高亮，用户友好 | — |
| sh (POSIX) | `/bin/sh` | 最简，最大兼容性 | 嵌入式系统 |
| PowerShell | `pwsh` | 面向对象，.NET 集成 | Windows |

## 二、基础语法 (Basic Syntax)

### Shebang 与执行

```bash
#!/bin/bash
# -*- coding: utf-8 -*-

set -euo pipefail   # 严格模式：出错即停、未定义变量报错、管道检测
IFS=$'\n\t'        # 分隔符设置

echo "Hello, World!"
```

执行方式：
```bash
chmod +x script.sh && ./script.sh    # 直接执行
bash script.sh                        # 作为参数
source script.sh                      # 当前 Shell 执行（保留变量）
```

### 变量 (Variables)

```bash
# 变量赋值（= 两边无空格）
NAME="Alice"
readonly PI=3.14159                  # 只读变量
local COUNT=0                        # 函数内局部变量

# 变量引用
echo "$NAME"                         # 双引号：变量展开
echo '$NAME'                         # 单引号：禁止展开
echo "${NAME}_suffix"                # 边界明确化
echo ${NAME:-default}                # 默认值
echo ${NAME:0:3}                     # 子串：Ali

# 特殊变量
echo "PID: $$, 退出码: $?, 参数个数: $#"
echo "所有参数: $@, 脚本名: $0, 首参: $1"
```

### 数组 (Arrays)

```bash
# 索引数组
fruits=("apple" "banana" "cherry")
echo ${fruits[0]}                    # apple
echo ${fruits[@]}                    # 所有元素
echo ${#fruits[@]}                   # 数组长度

# 关联数组 (Bash 4+)
declare -A user
user[name]="Alice"
user[age]=30
echo "${user[name]}"
```

## 三、流程控制 (Control Flow)

### 条件判断

```bash
# if-elif-else
if [[ $# -eq 0 ]]; then
    echo "Usage: $0 <filename>"
    exit 1
elif [[ -f "$1" ]]; then
    echo "File exists: $1"
else
    echo "File not found"
fi

# 文件测试运算符
[[ -f "$file" ]]    # 是否为常规文件
[[ -d "$dir" ]]     # 是否为目录
[[ -x "$bin" ]]     # 是否可执行
[[ -z "$str" ]]     # 字符串是否为空
[[ -n "$str" ]]     # 字符串非空

# 数值比较
[[ $a -eq $b ]]     # 等于（= 表示字符串相等）
[[ $a -ne $b ]]     # 不等于
[[ $a -lt $b ]]     # 小于（-le ≤, -gt >, -ge ≥）
```

### 循环 (Loops)

```bash
# for 循环
for i in {1..5}; do
    echo "Count: $i"
done

for file in /var/log/*.log; do
    [[ -f "$file" ]] && echo "Log: $file"
done

# while 循环
while IFS= read -r line; do
    echo "Line: $line"
done < /etc/passwd

# until 循环
until ping -c1 example.com &>/dev/null; do
    sleep 1
done
```

## 四、函数 (Functions)

```bash
# 函数定义
log() {
    local level="$1"
    local msg="$2"
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] [$level] $msg"
}

# 返回值：0 表示成功，非 0 表示错误码
check_port() {
    local port=$1
    ss -tuln | grep -q ":$port "
    return $?   # 返回 grep 结果
}

log "INFO" "Service starting"
if check_port 8080; then
    log "WARN" "Port 8080 already in use"
fi
```

## 五、文本处理 (Text Processing)

Bash + `awk`/`sed`/`grep` 三剑客：

```bash
# grep —— 搜索
grep -r "ERROR" /var/log/         # 递归搜索
grep -E "^[0-9]{3}-" file         # 扩展正则
grep -c "pattern" file            # 统计匹配行数

# sed —— 流编辑器
sed -n '10,20p' file              # 打印 10-20 行
sed -i 's/foo/bar/g' file         # 原地替换
sed '/^#/d' file                  # 删除注释行

# awk —— 列处理
awk '{print $1, $NF}' file        # 打印首列和末列
awk '$3 > 100 {print $1}'         # 条件过滤
awk -F: '{print $1, $3}' /etc/passwd  # 自定义分隔符
```

### 常用脚本模式

```bash
#!/bin/bash
# 使用 getopts 解析命令行选项

usage() {
    echo "Usage: $0 [-v] [-o output] <input>"
    exit 1
}

while getopts "vo:h" opt; do
    case $opt in
        v) VERBOSE=true ;;
        o) OUTPUT="$OPTARG" ;;
        h) usage ;;
        *) usage ;;
    esac
done
shift $((OPTIND - 1))
```

## 六、错误处理 (Error Handling)

```bash
set -e          # 任何命令失败立即退出
set -u          # 使用未定义变量报错
set -o pipefail # 管道中任一步失败即失败
trap 'echo "Error on line $LINENO"; exit 1' ERR
trap 'cleanup_function' EXIT      # 脚本退出时清理
```

## 七、最佳实践 (Best Practices)

| 规则 | 说明 | 示例 |
|------|------|------|
| 始终引用变量 | 防止单词分割和路径扩展 | `"$var"` 而非 `$var` |
| 使用 `[[ ]]` | 比 `[ ]` 更安全、更强大 | `[[ $str == *.txt ]]` |
| 避免解析 `ls` | 文件名包含空格时会出错 | 使用 `for file in *` |
| 使用函数模块化 | 提高可读性和复用性 | 超过 10 行考虑函数 |
| 添加错误处理 | 失败时给出明确信息 | `trap ERR` + 日志 |
| ShellCheck 检查 | 静态分析脚本问题 | `shellcheck script.sh` |

### ShellCheck 规则示例

```bash
# 不推荐
for i in $(ls *.txt); do     # SC2045: 不要解析 ls
    cat $i                    # SC2086: 未引用变量
done

# 推荐
for file in *.txt; do
    cat "$file"
done
```

## 八、实用示例 (Practical Examples)

```bash
#!/bin/bash
# 备份脚本：打包并保留最近 7 天备份

set -euo pipefail

BACKUP_DIR="/backup"
SOURCE="/var/www"
RETENTION=7

backup_name="www_$(date +%Y%m%d_%H%M%S).tar.gz"
tar -czf "${BACKUP_DIR}/${backup_name}" -C "$SOURCE" .

# 清理旧备份
find "$BACKUP_DIR" -name "www_*.tar.gz" -mtime +$RETENTION -delete

echo "Backup completed: ${BACKUP_DIR}/${backup_name}"
```

## 九、调试与测试 Shell 脚本

```bash
# Bash 调试模式
bash -x script.sh           # 显示每条命令的执行跟踪
bash -n script.sh           # 语法检查（不执行）
bash -v script.sh           # 显示输入行

# 在脚本中启用特定调试
set -x   # 开启跟踪
# ... 需要调试的代码 ...
set +x   # 关闭跟踪

# 使用 trap 调试
trap 'echo "Line $LINENO: \$var=$var"' DEBUG

# ShellCheck 静态分析 (CI 集成)
shellcheck script.sh

# 单元测试框架
# bats (Bash Automated Testing System)
@test "test addition" {
  result="$(add 1 2)"
  [ "$result" = "3" ]
}
```

## 十、跨平台兼容性

| 差异点 | Linux (Bash) | macOS (Zsh) | Windows (Git Bash) |
|-------|-------------|-------------|-------------------|
| `sed -i` | `sed -i 's/a/b/g' file` | `sed -i '' 's/a/b/g' file` | 需安装 sed |
| 路径分隔 | `/home/user` | `/Users/user` | `/c/Users/user` |
| `grep -P` | 支持 | 需安装 GNU grep | 有限支持 |
| `date +%s` | 支持 | 支持 | 需 MSYS |
| `/dev/stdin` | 支持 | 支持 | 有限支持 |

## 十一、常见 Shell 脚本框架

| 框架 | 描述 | 安装 |
|------|------|------|
| **bash-boilerplate** | 安全脚本模板 | 复制模板 |
| **shunit2** | xUnit 风格 Shell 测试 | `brew install shunit2` |
| **Bats** | TAP 兼容测试框架 | `npm install -g bats` |
| **ShellSpec** | BDD 风格测试 | `brew install shellspec` |

## 相关条目
- [[LinuxAdministration]]
- [[VersionControl]]
- [[05_ComputerScience/OperatingSystems/INDEX]]
