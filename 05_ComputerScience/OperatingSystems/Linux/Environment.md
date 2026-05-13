# Shell 环境配置

## Shell 启动文件

```bash
# Bash 启动文件加载顺序

# 登录 shell（如 ssh 登录）
# 1. /etc/profile
# 2. ~/.bash_profile, ~/.bash_login, ~/.profile（按顺序找到第一个）

# 非登录交互 shell（如打开终端）
# 1. /etc/bash.bashrc
# 2. ~/.bashrc

# 非交互 shell（如运行脚本）
# 1. $BASH_ENV 指定的文件

# 推荐配置方式
# ~/.bash_profile:
if [ -f ~/.bashrc ]; then
    . ~/.bashrc
fi

# ~/.bashrc:
# 别名、函数、提示符等放在这里

# ~/.profile:
# 环境变量放在这里

# Zsh 启动文件
# ~/.zshrc       # 交互 shell
# ~/.zshenv      # 所有 shell
# ~/.zprofile    # 登录 shell

# Fish 启动文件
# ~/.config/fish/config.fish
```

## PATH 管理

```bash
# ~/.bashrc 或 ~/.profile

# 追加到 PATH
export PATH="$PATH:$HOME/bin"
export PATH="$PATH:$HOME/.local/bin"

# 添加到 PATH 开头（优先查找）
export PATH="$HOME/go/bin:$PATH"

# 检查重复项
path_remove() {
    PATH=$(echo "$PATH" | tr ':' '\n' | grep -v "^$1$" | tr '\n' ':' | sed 's/:$//')
}

path_prepend() {
    path_remove "$1"
    PATH="$1:$PATH"
}

path_append() {
    path_remove "$1"
    PATH="$PATH:$1"
}

# 使用
path_prepend "$HOME/bin"
path_append "/usr/local/bin"

# 安全添加（目录存在才加）
add_to_path() {
    if [ -d "$1" ] && ":$PATH:" != *":$1:"*; then
        export PATH="$1:$PATH"
    fi
}

add_to_path "$HOME/.cargo/bin"
add_to_path "$HOME/.local/bin"
add_to_path "/snap/bin"
```

## 别名

```bash
# 基础别名
alias ll='ls -la'
alias la='ls -A'
alias l='ls -CF'
alias ..='cd ..'
alias ...='cd ../..'
alias grep='grep --color=auto'
alias fgrep='fgrep --color=auto'
alias egrep='egrep --color=auto'

# Git 别名
alias gs='git status'
alias ga='git add'
alias gc='git commit'
alias gco='git checkout'
alias gb='git branch'
alias gl='git log --oneline --graph --decorate --all'
alias gp='git push'
alias gpl='git pull'

# 安全别名
alias rm='rm -i'
alias cp='cp -i'
alias mv='mv -i'
alias ln='ln -i'

# 文件操作
alias mkdir='mkdir -p'
alias df='df -h'
alias du='du -h'
alias free='free -h'

# 网络
alias ip='ip -c'
alias myip='curl -s ifconfig.me'
alias ports='netstat -tulanp'

# 取消别名
unalias ll

# 查看所有别名
alias -p
```

## Shell 选项

```bash
# shopt 命令（Bash 特有选项）
shopt -s cdspell          # 自动修正 cd 拼写错误
shopt -s checkwinsize     # 窗口大小变化时更新 LINES/COLUMNS
shopt -s globstar         # 启用 ** 递归匹配
shopt -s histappend       # 历史记录追加而非覆盖
shopt -s cmdhist          # 多行命令保存为一条记录
shopt -s expand_aliases   # 展开别名
shopt -s autocd           # 输入目录名自动 cd
shopt -s dirspell         # 目录名拼写修正
shopt -s no_empty_cmd_completion  # 空行不补全

# 关闭选项
shopt -u mailwarn

# set 命令选项
set -o vi                 # 使用 vi 模式编辑命令行
set -o emacs              # 使用 emacs 模式（默认）
set -o noclobber          # 防止重定向覆盖文件
set -o notify             # 后台任务完成后立即通知
set -o ignoreeof          # Ctrl+D 不退出

# ~/.inputrc（Readline 配置）
# 禁用 Ctrl+S 冻结终端
stty -ixon

# 设置 Tab 补全大小写不敏感
# ~/.inputrc:
set completion-ignore-case on
# 或者 ~/.bashrc:
bind 'set completion-ignore-case on'
```

## 提示符自定义

```bash
# PS1 提示符
# 常用转义序列：
# \u    用户名
# \h    主机名（短格式）
# \H    主机名（完整）
# \w    当前目录（绝对路径）
# \W    当前目录（仅名称）
# \d    日期 (星期 月 日)
# \t    时间 (HH:MM:SS)
# \T    时间 (HH:MM:SS, 12小时)
# \@    时间 (AM/PM)
# \n    换行
# \!    历史编号
# \#    命令编号
# \$    普通用户 $, root #
# \\    反斜杠
# \[\]  包裹非打印字符（颜色码）

# 基础提示符
PS1='\u@\h:\w\$ '

# 彩色提示符
RED='\[\033[0;31m\]'
GREEN='\[\033[0;32m\]'
YELLOW='\[\033[0;33m\]'
BLUE='\[\033[0;34m\]'
MAGENTA='\[\033[0;35m\]'
CYAN='\[\033[0;36m\]'
WHITE='\[\033[0;37m\]'
BOLD='\[\033[1m\]'
RESET='\[\033[0m\]'

# Git 分支显示
parse_git_branch() {
    git branch 2>/dev/null | sed -n '/\* /s/* //p'
}

git_prompt() {
    local branch
    branch=$(parse_git_branch)
    if [ -n "$branch" ]; then
        echo " ($branch)"
    fi
}

# 完整的 PS1
PS1="${GREEN}\u${RESET}@${BLUE}\h${RESET}:${YELLOW}\w${RESET}${MAGENTA}\$(git_prompt)${RESET}\n${WHITE}\$${RESET} "

# 显示前一命令退出码
PS1='${?#0} \u@\h:\w\$ '

# 多行提示符
PS1='\n\[\e[32m\]\u@\h\[\e[0m\] \[\e[33m\]\w\[\e[0m\]\n\$ '

# 保存提示符
# source: https://github.com/magicmonty/bash-git-prompt

# 颜色码速查
# 前景色: 30黑 31红 32绿 33黄 34蓝 35紫 36青 37白
# 背景色: 40黑 41红 42绿 43黄 44蓝 45紫 46青 47白
# 效果: 0重置 1粗体 4下划线 5闪烁 7反色
```

## Bash 补全

```bash
# 加载默认补全
source /usr/share/bash-completion/bash_completion  # Linux
source /usr/local/etc/bash_completion              # macOS

# 自定义补全
complete -W "start stop restart status" myservice

# 动态补全函数
_myservice_completion() {
    local cur prev opts
    COMPREPLY=()
    cur="${COMP_WORDS[COMP_CWORD]}"
    prev="${COMP_WORDS[COMP_CWORD-1]}"
    opts="start stop restart status"

    if ${cur} == * ; then
        COMPREPLY=( $(compgen -W "${opts}" -- ${cur}) )
        return 0
    fi
}
complete -F _myservice_completion myservice

# 安装常用补全
# Git 补全
source /usr/share/bash-completion/completions/git
# 或
curl -L https://raw.github.com/git/git/master/contrib/completion/git-completion.bash -o ~/.git-completion.bash
source ~/.git-completion.bash

# Docker 补全
source /usr/share/bash-completion/completions/docker

# kubectl 补全
source <(kubectl completion bash)
```

## Dotfiles 管理

```bash
# 方法1: 裸 Git 仓库（推荐）
# 初始化
git init --bare $HOME/.dotfiles

# 创建别名
alias config='/usr/bin/git --git-dir=$HOME/.dotfiles --work-tree=$HOME'

# 添加到 .bashrc
echo "alias config='/usr/bin/git --git-dir=\$HOME/.dotfiles --work-tree=\$HOME'" >> $HOME/.bashrc
echo ".dotfiles" >> $HOME/.gitignore

# 使用
config status
config add .bashrc
config commit -m "Add bashrc"
config remote add origin <repo-url>
config push

# 在新机器上恢复
git clone --bare <repo-url> $HOME/.dotfiles
alias config='/usr/bin/git --git-dir=$HOME/.dotfiles --work-tree=$HOME'
config checkout
# 如果冲突：
config checkout -f

# 方法2: chezmoi
# 安装
sh -c "$(curl -fsLS get.chezmoi.io)"

# 初始化
chezmoi init

# 管理文件
chezmoi add ~/.bashrc
chezmoi edit ~/.bashrc

# 应用
chezmoi apply

# 差异查看
chezmoi diff

# 从远程恢复
chezmoi init <github-repo>
chezmoi apply

# 方法3: 符号链接
# 手动管理
mkdir ~/dotfiles
mv ~/.bashrc ~/dotfiles/
ln -s ~/dotfiles/.bashrc ~/.bashrc
```

## 常用环境变量

```bash
# ~/.bashrc 或 ~/.profile

# 编辑器
export EDITOR=vim
export VISUAL=vim

# 语言
export LANG=zh_CN.UTF-8
export LC_ALL=zh_CN.UTF-8

# 历史记录
export HISTSIZE=10000
export HISTFILESIZE=20000
export HISTTIMEFORMAT="%Y-%m-%d %H:%M:%S "
export HISTCONTROL=ignoredups:erasedups
export HISTIGNORE="&:ls:[bf]g:exit:history"

# 默认权限
umask 022

# 分页器
export PAGER=less
export LESS='-R -F -X -i'

# Man 手册颜色
export LESS_TERMCAP_mb=$'\e[1;31m'
export LESS_TERMCAP_md=$'\e[1;34m'
export LESS_TERMCAP_me=$'\e[0m'
export LESS_TERMCAP_se=$'\e[0m'
export LESS_TERMCAP_so=$'\e[01;44;33m'
export LESS_TERMCAP_ue=$'\e[0m'
export LESS_TERMCAP_us=$'\e[1;32m'
```

## 环境模块系统

```bash
# Environment Modules（环境模块系统）
# 用于动态修改用户环境

# 加载模块
module load gcc/9.3.0
module load python/3.9

# 查看可用模块
module avail

# 列出已加载模块
module list

# 卸载模块
module unload python/3.9

# 切换模块
module switch gcc gcc/10.2.0

# 查看模块信息
module show python/3.9

# 创建模块文件
# /usr/share/modules/modulefiles/python/3.9.lua
whatis("Python 3.9")

prepend_path("PATH", "/usr/local/python3.9/bin")
prepend_path("LD_LIBRARY_PATH", "/usr/local/python3.9/lib")
setenv("PYTHON_HOME", "/usr/local/python3.9")

# 或 Tcl 格式
#%Module1.0
proc ModulesHelp {} {
    puts stderr "Python 3.9"
}
prepend-path PATH /usr/local/python3.9/bin
prepend-path LD_LIBRARY_PATH /usr/local/python3.9/lib
setenv PYTHON_HOME /usr/local/python3.9
```

## 相关条目

- [[Bash]]
- [[Scripting]]
- [[Config]]
- [[Basics]]
- [[LinuxKernel]]
