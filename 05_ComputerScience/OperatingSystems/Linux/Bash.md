# Bash 脚本编程

## Shebang 和基本结构

```bash
#!/bin/bash
# -*- coding: utf-8 -*-
# 脚本说明：这是一个 Bash 脚本示例

set -euo pipefail  # 严格模式

# 主函数
main() {
    echo "Hello, World!"
}

main "$@"
```

## 变量

```bash
# 声明和赋值（等号两侧不能有空格）
name="Alice"
age=30

# 使用变量
echo $name
echo "${name}"      # 推荐加花括号
echo "${name}你好"  # 花括号区分变量名边界

# 默认值
echo "${var:-default}"    # 变量未设置时使用默认值
echo "${var:=default}"    # 变量未设置时赋值并返回
echo "${var:?错误信息}"   # 变量未设置时报错
echo "${var:+替换值}"     # 变量已设置时使用替换值

# 局部变量
myfunc() {
    local local_var="仅在函数内可见"
    readonly CONST="常量"
    echo "$local_var"
}

# 数组
arr=("apple" "banana" "cherry")
echo "${arr[0]}"      # 第一个元素
echo "${arr[@]}"      # 所有元素
echo "${#arr[@]}"     # 数组长度
echo "${!arr[@]}"     # 所有索引

# 关联数组（Bash 4+）
declare -A user
user[name]="Alice"
user[age]=30
echo "${user[name]}"

# 只读变量
readonly PI=3.14159
```

## 特殊变量

```bash
echo "$0"      # 脚本名
echo "$?"      # 上一条命令退出码（0 成功，非 0 失败）
echo "$#"      # 参数个数
echo "$@"      # 所有参数（每个参数独立引号）
echo "$*"      # 所有参数（作为一个字符串）
echo "$$"      # 当前进程 PID
echo "$!"      # 最后一个后台进程 PID
echo "$-"      # 当前 shell 选项
echo "$_"      # 上一个命令的最后一个参数
```

## 字符串操作

```bash
str="Hello World"

echo "${#str}"                 # 长度：11
echo "${str:0:5}"              # 子串：Hello
echo "${str:6}"                # 从位置 6 到末尾：World
echo "${str#He}"               # 删除前缀：llo World
echo "${str%World}"            # 删除后缀：Hello
echo "${str/Hello/Hi}"         # 替换第一个：Hi World
echo "${str//o/X}"             # 替换所有：HellX WXrld
echo "${str^}"                 # 首字母大写：Hello World
echo "${str^^}"                # 全部大写：HELLO WORLD
echo "${str,}"                 # 首字母小写：hello World
echo "${str,,}"                # 全部小写：hello world
```

## 算术运算

```bash
# $(( ))
result=$(( 1 + 2 * 3 ))     # 7
echo $(( 10 / 3 ))           # 3（整数除法）
echo $(( 2 ** 10 ))          # 1024（幂运算）
echo $(( (5 + 5) / 2 ))     # 5

# let 命令
let a=5+5
let a+=2

# bc（浮点数）
echo "scale=2; 10 / 3" | bc  # 3.33
```

## 控制流

```bash
# if/then/elif/else/fi
if [ "$age" -ge 18 ]; then
    echo "成年"
elif [ "$age" -ge 60 ]; then
    echo "老年"
else
    echo "未成年"
fi

# test 命令 [ ]
[ -f "file.txt" ] && echo "文件存在"    # 文件检查
[ -d "dir" ] && echo "目录存在"         # 目录检查
[ -z "$var" ] && echo "变量为空"        # 字符串空
[ -n "$var" ] && echo "变量非空"        # 字符串非空
[ "$a" = "$b" ]                         # 字符串相等
[ "$a" != "$b" ]                        # 字符串不等
[ "$a" -eq "$b" ]                       # 数字相等
[ "$a" -ne "$b" ]                       # 数字不等
[ "$a" -lt "$b" ]                       # 小于
[ "$a" -le "$b" ]                       # 小于等于
[ "$a" -gt "$b" ]                       # 大于
[ "$a" -ge "$b" ]                       # 大于等于

# [[ ]] 增强测试（Bash 扩展）
"$str" == *.txt                   # 模式匹配
[[ "$str" =~ ^[0-9]+$ ]]               # 正则匹配
-f "$file" && -r "$file"          # 逻辑与

# for/in 循环
for i in {1..5}; do
    echo "$i"
done

for file in *.txt; do
    echo "$file"
done

for (( i=0; i<10; i++ )); do
    echo "$i"
done

# while 循环
count=0
while [ "$count" -lt 5 ]; do
    echo "$count"
    ((count++))
done

# until 循环
until [ "$count" -ge 5 ]; do
    echo "$count"
    ((count++))
done

# case/esac
case "$1" in
    start)
        echo "启动服务"
        ;;
    stop|kill)      # 多个模式
        echo "停止服务"
        ;;
    restart)
        echo "重启服务"
        ;;
    *)              # 默认
        echo "用法: $0 {start|stop|restart}"
        exit 1
        ;;
esac
```

## 函数

```bash
# 定义函数
function hello() {
    local name="$1"         # 局部变量
    echo "Hello, $name!"
    return 0                 # 返回码
}

# 简化写法
greet() {
    echo "Hello, $1!"
}

# 调用
hello "World"
result=$(greet "Alice")     # 捕获输出
echo "$result"

# 返回值
add() {
    return $(( $1 + $2 ))
}
add 3 4
echo $?  # 7（返回值限制 0-255）
```

## 重定向

```bash
# 重定向输出
command > file          # 覆盖写入 stdout
command >> file         # 追加写入 stdout
command 2> file         # 重定向 stderr
command &> file         # 重定向 stdout 和 stderr
command 2>&1            # stderr 合并到 stdout

# 重定向输入
command < file          # 从文件读取 stdin
command <<< "$var"      # 从变量读取 stdin

# Here Document
cat <<EOF
多行文本
支持变量 $var
EOF

# Here String
grep "pattern" <<< "$string"

# exec 重定向
exec 3< input.txt       # 打开文件描述符 3 用于读取
exec 4> output.txt      # 打开文件描述符 4 用于写入
read -u 3 line          # 从 fd 3 读取
echo "data" >&4         # 写入 fd 4
exec 3<&-               # 关闭 fd 3

# /dev/null
command > /dev/null 2>&1  # 丢弃所有输出
```

## 调试

```bash
#!/bin/bash
set -x   # 跟踪模式（打印每条命令）
set +x   # 关闭跟踪
set -e   # 出错即退出
set -u   # 使用未定义变量报错
set -o pipefail  # 管道中任一命令失败即退出

# 错误陷阱
trap 'echo "错误发生在第 $LINENO 行"; exit 1' ERR

# 单步调试
bash -n script.sh       # 语法检查（不执行）
bash -v script.sh       # 打印输入行
bash -x script.sh       # 跟踪执行

# 使用 shellcheck（静态分析）
# shellcheck script.sh

# 调试打印
debug() {
    if [ "${DEBUG}" = "true" ]; then
        echo "[DEBUG] $*" >&2
    fi
}
debug "变量值: $var"
```

## 完整脚本示例

```bash
#!/bin/bash
set -euo pipefail

# 日志函数
log_info()  { echo "[INFO]  $*"; }
log_warn()  { echo "[WARN]  $*" >&2; }
log_error() { echo "[ERROR] $*" >&2; }

# 清理函数
cleanup() {
    log_info "执行清理..."
    rm -rf "$TEMP_DIR"
}

# 用法说明
usage() {
    cat <<EOF
用法: $0 [选项] <输入文件>

选项:
    -o <文件>   输出文件
    -v          详细模式
    -h          显示帮助
EOF
    exit 1
}

# 解析命令行参数
while getopts "o:vh" opt; do
    case "$opt" in
        o) OUTPUT_FILE="$OPTARG" ;;
        v) VERBOSE=true ;;
        h) usage ;;
        *) usage ;;
    esac
done
shift $((OPTIND - 1))

# 检查参数
if [ $# -lt 1 ]; then
    log_error "缺少输入文件"
    usage
fi

INPUT_FILE="$1"

# 设置陷阱
trap cleanup EXIT

# 创建临时目录
TEMP_DIR=$(mktemp -d)
log_info "临时目录: $TEMP_DIR"

# 主逻辑
if [ -f "$INPUT_FILE" ]; then
    log_info "处理文件: $INPUT_FILE"
    cp "$INPUT_FILE" "$TEMP_DIR/"
    # 处理...
    log_info "完成"
else
    log_error "文件不存在: $INPUT_FILE"
    exit 1
fi
\`\`\`

## 相关条目

- Shell
- Linux命令
- [[ProcessManagement]]
