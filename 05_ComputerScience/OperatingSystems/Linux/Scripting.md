---
aliases: [Scripting]
tags: ['OperatingSystems', 'Linux', 'Scripting']
created: 2026-05-16
updated: 2026-05-16
---

# Shell 脚本最佳实践

## 脚本模板

```bash
#!/usr/bin/env bash
#
# 脚本名称: script.sh
# 描述: 脚本功能说明
# 作者: Author
# 用法: ./script.sh [选项] [参数]

set -euo pipefail
IFS=$'\n\t'

# 版本信息
VERSION="1.0.0"

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 日志函数
log_info()    { echo -e "${GREEN}[INFO]${NC}  $*"; }
log_warn()    { echo -e "${YELLOW}[WARN]${NC}  $*" >&2; }
log_error()   { echo -e "${RED}[ERROR]${NC} $*" >&2; }
log_debug()   { [ "${DEBUG:-false}" = "true" ] && echo -e "${BLUE}[DEBUG]${NC} $*" >&2; }

# 清理函数
cleanup() {
    local exit_code=$?
    log_debug "执行清理 (退出码: $exit_code)"
    # 清理临时文件等
    [ -d "$TEMP_DIR" ] && rm -rf "$TEMP_DIR"
    exit "$exit_code"
}

# 错误处理
error_handler() {
    local line_no=$1
    local command=$2
    log_error "第 $line_no 行命令 '$command' 失败"
    exit 1
}

# 设置陷阱
trap cleanup EXIT
trap 'error_handler $LINENO "$BASH_COMMAND"' ERR

# 用法说明
usage() {
    cat <<EOF
用法: $0 [选项] [参数]

选项:
    -o, --output <文件>   输出文件
    -v, --verbose         详细输出
    -d, --debug           调试模式
    -h, --help            显示此帮助
EOF
    exit 0
}

# 解析命令行参数
parse_args() {
    # 使用 getopt 支持长选项
    TEMP=$(getopt -o 'o:vdh' --long 'output:,verbose,debug,help' -n "$0" -- "$@")
    if [ $? -ne 0 ]; then
        usage
    fi
    eval set -- "$TEMP"

    while true; do
        case "$1" in
            '-o'|'--output')
                OUTPUT_FILE="$2"
                shift 2
                ;;
            '-v'|'--verbose')
                VERBOSE=true
                shift
                ;;
            '-d'|'--debug')
                DEBUG=true
                set -x
                shift
                ;;
            '-h'|'--help')
                usage
                ;;
            '--')
                shift
                break
                ;;
            *)
                usage
                ;;
        esac
    done

    ARGS=("$@")
}

# 主函数
main() {
    parse_args "$@"

    # 创建临时目录
    TEMP_DIR=$(mktemp -d "/tmp/${0##*/}.XXXXXX")
    log_debug "临时目录: $TEMP_DIR"

    # 检查依赖
    for cmd in curl jq sed awk; do
        if ! command -v "$cmd" &>/dev/null; then
            log_error "缺少依赖: $cmd"
            exit 1
        fi
    done

    # 主逻辑
    log_info "脚本开始执行"

    # ...

    log_info "脚本执行完成"
}

# 执行主函数
main "$@"
```

## 命令行参数解析

```bash
# 方法1: getopts（内置，支持短选项）
while getopts "f:o:vh" opt; do
    case "$opt" in
        f) INPUT_FILE="$OPTARG" ;;
        o) OUTPUT_FILE="$OPTARG" ;;
        v) VERBOSE=true ;;
        h) usage ;;
        \?) echo "无效选项: -$OPTARG" >&2; usage ;;
    esac
done
shift $((OPTIND - 1))

# 方法2: getopt（支持长选项）
ARGS=$(getopt -o 'f:o:vh' -l 'file:,output:,verbose,help' -n "$0" -- "$@")
eval set -- "$ARGS"

# 方法3: 简单手动解析（无依赖）
for arg in "$@"; do
    case "$arg" in
        --help|-h) usage ;;
        --verbose|-v) VERBOSE=true ;;
        --file=*) INPUT_FILE="${arg#*=}" ;;
    esac
done
```

## 错误处理

```bash
# 严格模式
set -euo pipefail

# 自定义错误函数
die() {
    echo "[FATAL] $*" >&2
    exit 1
}

# 使用
[ -f "$config_file" ] || die "配置文件 $config_file 不存在"

# 命令执行检查
if ! command_that_might_fail; then
    log_error "命令失败"
    exit 1
fi

# 管道错误处理
set -o pipefail
# 如果 sort 或 uniq 失败，整体算失败
cat data.txt | sort | uniq > result.txt || die "处理数据失败"

# 错误陷阱
trap 'echo "第 $LINENO 行出错"; exit 1' ERR

# 异常退出陷阱
trap 'echo "脚本被中断"; exit 1' INT TERM
```

## 日志函数

```bash
#!/bin/bash

# 日志级别
LOG_LEVEL=${LOG_LEVEL:-INFO}
LOG_FILE=${LOG_FILE:-}

log() {
    local level="$1"
    shift
    local message="$*"
    local timestamp
    timestamp=$(date '+%Y-%m-%d %H:%M:%S')

    # 级别过滤
    case "$LOG_LEVEL" in
        DEBUG) ;;
        INFO)  [ "$level" = "DEBUG" ] && return ;;
        WARN)  INFO)$  && return ;;
        ERROR) [ "$level" != "ERROR" ] && return ;;
    esac

    local output="[$timestamp] [$level] $message"

    if [ -n "$LOG_FILE" ]; then
        echo "$output" >> "$LOG_FILE"
    else
        if [ "$level" = "ERROR" ] || [ "$level" = "WARN" ]; then
            echo "$output" >&2
        else
            echo "$output"
        fi
    fi
}

log_debug() { log "DEBUG" "$@"; }
log_info()  { log "INFO"  "$@"; }
log_warn()  { log "WARN"  "$@"; }
log_error() { log "ERROR" "$@"; }
```

## 清理（trap）

```bash
#!/bin/bash

# 临时文件清理
TEMP_FILES=()

cleanup() {
    local exit_code=$?

    echo "清理中..."

    # 删除临时文件
    for f in "${TEMP_FILES[@]}"; do
        [ -f "$f" ] && rm -f "$f"
    done

    # 删除临时目录
    [ -d "$TEMP_DIR" ] && rm -rf "$TEMP_DIR"

    # 恢复原始设置
    [ -f "${ORIGINAL_FILE}.bak" ] && mv "${ORIGINAL_FILE}.bak" "$ORIGINAL_FILE"

    echo "清理完成"
    exit "$exit_code"
}

# 设置多个信号
trap cleanup EXIT      # 正常退出
trap 'cleanup; exit 1' INT TERM HUP  # 中断信号
trap 'echo "不受 SIGQUIT 影响"' QUIT

# 注册临时文件
TEMP_FILE=$(mktemp)
TEMP_FILES+=("$TEMP_FILE")

TEMP_DIR=$(mktemp -d)
```

## 幂等脚本

```bash
#!/bin/bash

# 幂等性检查函数
is_already_setup() {
    # 检查是否已配置
    if [ -f "/etc/myapp/configured" ]; then
        return 0
    fi
    return 1
}

mark_configured() {
    mkdir -p /etc/myapp
    date > "/etc/myapp/configured"
}

# 检查并跳过
if is_already_setup; then
    log_info "系统已配置，跳过"
    exit 0
fi

# 执行配置
log_info "开始配置..."
# ... 配置逻辑 ...

mark_configured
log_info "配置完成"
```

## 跨平台脚本

```bash
#!/usr/bin/env bash

# 检测操作系统
detect_os() {
    case "$(uname -s)" in
        Linux*)     echo "linux" ;;
        Darwin*)    echo "macos" ;;
        CYGWIN*|MINGW*|MSYS*) echo "windows" ;;
        *)          echo "unknown" ;;
    esac
}

OS=$(detect_os)

# 根据 OS 调整行为
case "$OS" in
    linux)
        SED='sed'
        PATH_SEP='/'
        ;;
    macos)
        SED='gsed'  # 需要安装 gnu-sed
        PATH_SEP='/'
        ;;
    windows)
        SED='sed'  # Git Bash 环境
        PATH_SEP='\\'
        ;;
esac

# 路径处理
normalize_path() {
    local path="$1"
    case "$OS" in
        windows)
            # 转换 /c/Users 到 C:\Users
            echo "$path" | sed 's|^/\([a-zA-Z]\)/|\1:\\|g'
            ;;
        *)
            echo "$path"
            ;;
    esac
}
```

## 脚本安全

```bash
# 避免使用 eval
# 不安全: eval "echo $input"
# 安全: echo "$input"

# 始终使用双引号包裹变量
rm -rf "/tmp/$filename"   # 安全
# rm -rf /tmp/$filename   # 不安全（若 filename 含空格）

# 使用 printf 而非 echo
printf '%s\n' "$variable"

# 避免临时文件中的敏感信息
# 使用管道而非临时文件
secret=$(command_that_outputs_secret | head -1)
# 而不是:
# command_that_outputs_secret > /tmp/secret.txt

# 限制文件权限
umask 077

# 检查文件所有权
[ "$(stat -c '%U' /etc/config)" = "root" ] || die "文件所有权错误"

# 不要信任外部输入
validate_input() {
    local input="$1"
    # 只允许字母数字和下划线
    [[ "$input" =~ ^[a-zA-Z0-9_]+$ ]] || die "无效输入: $input"
}
```

## 性能优化

```bash
# 避免不必要的子 shell
# 慢: result=$(cat file | grep pattern)
# 快: result=$(grep pattern file)

# 使用内置命令而非外部命令
# 慢: result=$(expr 1 + 2)
# 快: result=$(( 1 + 2 ))

# 避免在循环中使用管道
# 慢:
# while read line; do
#     echo "$line" | grep pattern
# done < file

# 快:
# while IFS= read -r line; do
#     "$line" =~ pattern && printf '%s\n' "$line"
# done < file

# 使用 IFS 和 read 处理文件
while IFS=, read -r col1 col2 col3; do
    printf '列1: %s, 列2: %s\n' "$col1" "$col2"
done < data.csv

# 批量操作而非逐个操作
# 慢:
# for f in *.txt; do
#     mv "$f" "${f%.txt}.bak"
# done

# 快:
# rename 's/\.txt$/.bak/' *.txt

# 使用 find ... -exec 或 xargs
find . -name "*.tmp" -exec rm {} \;
find . -name "*.log" | xargs gzip
```

## 测试脚本

```bash
#!/bin/bash

# 简单的单元测试框架
test_count=0
pass_count=0

assert_eq() {
    local expected="$1"
    local actual="$2"
    local msg="${3:-}"
    ((test_count++))
    if [ "$expected" = "$actual" ]; then
        ((pass_count++))
        echo "PASS: $msg"
    else
        echo "FAIL: $msg (预期: '$expected', 实际: '$actual')"
    fi
}

test_add() {
    local result
    result=$(add 2 3)
    assert_eq "5" "$result" "add(2, 3)"
}

test_subtract() {
    local result
    result=$(subtract 5 3)
    assert_eq "2" "$result" "subtract(5, 3)"
}

# 运行测试
test_add
test_subtract

# 报告
echo "总计: $test_count, 通过: $pass_count, 失败: $((test_count - pass_count))"
[ "$pass_count" -eq "$test_count" ] || exit 1
```

## 相关条目

- [[Bash]]
- [[Environment]]
- [[Advanced]]
- [[Neovim]]
- [[05_ComputerScience/OperatingSystems/LinuxKernel|LinuxKernel]]


