---
aliases: [Commands]
tags: ['SoftwareEngineering', 'GitAndVersionControl', 'Commands']
created: 2026-05-16
updated: 2026-05-16
---

# Git 命令速查

## 一、配置

```bash
# 用户信息
git config --global user.name "Your Name"
git config --global user.email "your@email.com"

# 别名
git config --global alias.st status
git config --global alias.br branch
git config --global alias.co checkout
git config --global alias.ci commit
git config --global alias.df diff
git config --global alias.lg "log --oneline --graph --all"
git config --global alias.last "log -1 HEAD"

# 凭证（凭据助手）
git config --global credential.helper store
git config --global credential.helper 'cache --timeout=3600'

# 默认编辑器
git config --global core.editor "vim"

# 行尾处理
git config --global core.autocrlf true    # Windows
git config --global core.autocrlf input   # Mac/Linux

# 查看配置
git config --list
git config --global --list
git config user.name
```

## 二、仓库管理

```bash
# 初始化
git init
git init my-project

# 克隆
git clone https://github.com/user/repo.git
git clone git@github.com:user/repo.git
git clone --depth 1 https://github.com/user/repo.git   # 浅克隆（只取最新版本）
git clone --branch develop https://github.com/user/repo.git

# 远程仓库
git remote -v
git remote add origin https://github.com/user/repo.git
git remote remove origin
git remote rename old-name new-name
git remote set-url origin https://new-url.com/repo.git
```

## 三、基本工作流

```bash
# 状态
git status
git status -s    # 简短格式

# 添加
git add file.txt
git add -A        # 添加所有变化
git add .         # 添加当前目录所有文件
git add *.js      # 添加所有 JS 文件
git add -p        # 交互式分段添加

# 提交
git commit -m "fix: 修复登录超时问题"
git commit -a -m "提交所有已跟踪文件的修改"   # 跳过 git add
git commit --amend                  # 修改上次提交
git commit --amend -m "新的提交信息"
git commit --amend --no-edit        # 不修改提交信息，只修改内容

# 日志
git log
git log --oneline
git log --oneline --graph --all
git log -p                     # 显示差异
git log --stat                 # 统计文件修改
git log --author="name"        # 按作者筛选
git log --since="2024-01-01"   # 按时间筛选
git log --grep="bug"           # 按提交信息搜索
git log --follow file.txt      # 显示文件历史（包括重命名）
git log --oneline -n 5         # 仅最近5条
git log --format="%h - %an, %ar : %s"

# 差异
git diff                        # 工作区 vs 暂存区
git diff --staged               # 暂存区 vs 最近提交
git diff HEAD                   # 工作区 vs 最近提交
git diff branch1..branch2       # 两个分支差异
git diff commit1 commit2        # 两个提交差异
git diff --name-only            # 只显示文件名

# 查看
git show HEAD
git show HEAD:file.txt
git show --stat HEAD
```

## 四、分支与合并

```bash
# 分支管理
git branch                     # 列出本地分支
git branch -r                  # 列出远程分支
git branch -a                  # 列出所有分支
git branch new-feature         # 创建分支
git branch -m old-name new-name    # 重命名
git branch -d old-branch       # 删除分支（已合并）
git branch -D old-branch       # 强制删除

# 切换分支
git checkout develop
git checkout -b new-branch     # 创建并切换
git switch develop             # Git 2.23+ 新语法
git switch -C new-branch

# 合并
git merge feature              # 将 feature 合并到当前分支
git merge --no-ff feature      # 强制创建合并提交
git merge --abort              # 取消合并
git merge --continue           # 解决冲突后继续合并

# 变基
git rebase main                # 将当前分支变基到 main
git rebase -i HEAD~3           # 交互式变基（最近3个提交）
git rebase --continue          # 解决冲突后继续
git rebase --skip              # 跳过当前提交
git rebase --abort             # 取消变基

# Cherry-Pick
git cherry-pick commit-hash
git cherry-pick hash1 hash2 hash3
git cherry-pick -n hash        # 只应用变更，不产生提交

# 标签
git tag v1.0.0
git tag -a v1.0.0 -m "版本 1.0.0 发布"
git tag -a v1.0.0 commit-hash
git tag -l "v1.*"
git tag -d v1.0.0
git push origin v1.0.0
git push origin --tags
```

## 五、协作

```bash
# 拉取与推送
git fetch origin
git fetch origin develop
git pull                        # git fetch + git merge
git pull --rebase               # git fetch + git rebase
git push origin main
git push origin develop:main    # 推送到不同分支名
git push -u origin develop      # 跟踪远程分支
git push --force origin main    # 强制推送（谨慎使用）
git push --force-with-lease     # 更安全的强制推送

# 远程分支
git branch -u origin/develop    # 设置上游分支
git branch -vv                  # 查看跟踪关系
git checkout -b local origin/remote  # 从远程分支创建本地分支
git push origin --delete develop     # 删除远程分支
git remote prune origin              # 清理已删除的远程分支引用
```

## 六、撤销

```bash
# 撤销工作区修改
git checkout -- file.txt       # 丢弃工作区的修改
git restore file.txt           # Git 2.23+ 新语法
git checkout .                 # 丢弃所有工作区修改

# 撤销暂存
git reset HEAD file.txt        # 取消暂存
git restore --staged file.txt  # Git 2.23+ 新语法

# 重置
git reset --soft HEAD~1        # 撤销上次提交，保留工作区和暂存区
git reset --mixed HEAD~1       # 撤销上次提交，保留工作区（默认）
git reset --hard HEAD~1        # 完全撤销到上一次提交（⚠ 危险）
git reset --hard commit-hash   # 回退到指定提交

# 恢复
git revert HEAD                # 撤销上次提交（产生新提交）
git revert commit-hash
git revert -n commit-hash      # 不自动提交
```

## 七、贮藏

```bash
git stash                          # 贮藏当前修改
git stash push -m "message"        # 带消息的贮藏
git stash list                     # 查看贮藏列表
git stash pop                      # 应用最近贮藏并删除
git stash apply                    # 应用最近贮藏但不删除
git stash apply stash@{2}          # 应用指定贮藏
git stash drop stash@{0}           # 删除指定贮藏
git stash clear                    # 清空所有贮藏
git stash branch new-branch        # 从贮藏创建分支
git stash show -p                  # 查看贮藏的详细差异
```

## 八、高级命令

```bash
# 二分查找
git bisect start
git bisect bad HEAD
git bisect good v1.0.0
git bisect good/bad
git bisect reset

# 指责（逐行追溯）
git blame file.txt
git blame -L 10,30 file.txt

# 搜索
git grep "function_name"
git grep "search_term" v1.0.0

# 短日志
git shortlog -sn      # 按提交次数排序的贡献者列表
git shortlog -sn --since="2024-01-01"

# 清理
git clean -n           # 预览要删除的未跟踪文件
git clean -f           # 删除未跟踪文件
git clean -fd          # 删除未跟踪文件和目录

# 打包
git gc                 # 垃圾回收
git gc --aggressive    # 激进压缩
git count-objects -v   # 查看仓库存储详情

# 检查
git fsck               # 检查仓库完整性
git fsck --lost-found  # 查找丢失的提交
git reflog             # 引用日志
git reflog expire --expire=now --all

# 子模块
git submodule add https://github.com/user/lib.git libs/lib
git submodule init
git submodule update
git submodule update --init --recursive
```

## 相关条目

- [[Branch]]
- [[Workflow]]
- [[Advanced]]
- [[GitHub]]
- [[05_ComputerScience/SoftwareEngineering/GitAndVersionControl/INDEX|GitAndVersionControl]]

