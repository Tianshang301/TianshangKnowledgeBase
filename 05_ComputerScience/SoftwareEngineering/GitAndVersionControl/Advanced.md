# Git 高级技巧

## 一、交互式 Rebase

交互式 rebase 是 Git 最强大的功能之一，允许编辑、压缩、删除、重排提交。

```bash
# 交互式 rebase 最近 3 个提交
git rebase -i HEAD~3
```

### 进入编辑器

```
pick a1b2c3d feat: 添加用户登录
pick e4f5g6h fix: 修复登录验证
pick i7j8k9l feat: 添加用户注销

# 可用命令：
# p, pick   = 保留此提交
# r, reword = 保留提交但修改提交信息
# e, edit   = 保留提交但暂停修改
# s, squash = 合并到上一个提交
# f, fixup  = 类似 squash，但丢弃提交信息
# d, drop   = 删除此提交
# x, exec   = 使用 shell 运行命令
# b, break  = 在此处暂停（使用 git rebase --continue 继续）
# t, reword = 合并但不包括提交信息

# 行重新排序 = 更改提交顺序
```

### 压缩多个提交

```bash
# 将最后 4 个提交压缩为 1 个
git rebase -i HEAD~4

# 修改为：
pick a1b2c3d feat: 完整的登录功能  # 保留最上面的
squash e4f5g6h WIP
squash i7j8k9l 修复一个 bug
squash m9n0o1p 清理代码

# 结果：一个干净的提交
feat: 完整的登录功能
```

### 修改历史提交

```bash
# 1. edit 模式
git rebase -i HEAD~5
# 将需要修改的提交标记为 edit

# 2. 修改内容
git commit --all --amend --no-edit

# 3. 继续
git rebase --continue

# 注意：如果已经推送了这些提交，需要强制推送
git push --force-with-lease
```

---

## 二、Bisect 二分查找

用于在提交历史中高效定位引入 bug 的提交。

```bash
# 1. 开始二分查找
git bisect start

# 2. 标记当前（有 bug）
git bisect bad

# 3. 标记已知正常的版本
git bisect good v1.0.0

# 4. Git 会切换到一个中间的提交
# 测试这个提交
git bisect good    # 如果这个提交正常
git bisect bad     # 如果这个提交有 bug

# 5. 重复步骤 4，直到定位到第一个引入 bug 的提交
# Bisecting: 0 revisions left
# a1b2c3d is the first bad commit

# 6. 结束
git bisect reset
```

### 自动 Bisect

```bash
# 编写测试脚本，返回 0 表示正常，非 0 表示有 bug
git bisect start HEAD v1.0.0
git bisect run npm test     # 自动二分
git bisect reset
```

```bash
# 使用自定义脚本
git bisect start HEAD v1.0.0
git bisect run python test_script.py
git bisect reset
```

---

## 三、Worktree 多工作区

Git worktree 允许一个仓库同时检出多个分支到不同目录。

```bash
# 创建新的工作树
git worktree add ../project-hotfix hotfix/bug-123
# 现在可以在 ../project-hotfix 中工作，不影响当前目录

# 创建带新分支的工作树
git worktree add -b feature/new-feature ../project-feature main

# 列出工作树
git worktree list

# 锁定工作树（防止被清理）
git worktree lock ../project-hotfix

# 移除工作树
git worktree remove ../project-hotfix

# 清理过期的工作树
git worktree prune
```

### 使用场景

```bash
# 场景1：并行处理多个任务
# 项目 A 目录 = main（发布版本）
# 项目 B 目录 = feature/xxx（新功能）
git worktree add ../myapp-main main

# 场景2：快速修复紧急 bug
# 切换到 hotfix 工作区修复
git worktree add ../myapp-hotfix -b hotfix/critical main
cd ../myapp-hotfix
# 修复、提交、推送
git commit -m "hotfix: critical fix"
git push -u origin hotfix/critical
```

---

## 四、子模块 (Submodule) vs 子树 (Subtree)

### 子模块

```bash
# 添加子模块
git submodule add https://github.com/user/lib.git libs/lib

# 克隆包含子模块的仓库
git clone --recurse-submodules https://github.com/user/project.git

# 更新子模块
git submodule update --init --recursive

# 更新到最新
git submodule update --remote

# 查看状态
git submodule status
```

**优缺点**：

| 优点 | 缺点 |
|------|------|
| 独立版本控制 | 操作复杂（需额外命令） |
| 不污染主仓库 | 新手容易忘记 init/update |
| | 分支切换需注意子模块 |

### 子树

```bash
# 添加子树
git remote add lib https://github.com/user/lib.git
git subtree add --prefix=libs/lib lib main --squash

# 更新子树
git subtree pull --prefix=libs/lib lib main --squash

# 推送对子树的修改
git subtree push --prefix=libs/lib lib feature
```

**优缺点**：

| 优点 | 缺点 |
|------|------|
| 单一仓库，操作简单 | 历史提交较多 |
| 无需额外命令 | 合并冲突可能复杂 |
| 适合小工具类依赖 | |

---

## 五、Git Hooks

Hooks 是 Git 事件触发的脚本，位于 `.git/hooks/` 目录。

### 客户端 Hooks

```bash
# pre-commit：提交前运行
# .git/hooks/pre-commit
#!/bin/bash
echo "运行 pre-commit 检查..."

# 检查是否包含调试代码
if grep -r "console.log\|debugger" --include="*.js" .; then
    echo "错误：包含调试代码！"
    exit 1
fi

# 运行代码格式化
npx prettier --check .

# 运行 lint
npm run lint
```

```bash
# commit-msg：验证提交信息格式
# .git/hooks/commit-msg
#!/bin/bash
MSG_FILE=$1
MSG=$(cat $MSG_FILE)

# 检查 Conventional Commits 格式
if ! echo "$MSG" | grep -qE "^(feat|fix|docs|style|refactor|perf|test|chore|ci|build)(\(.+\))?: .+"; then
    echo "错误：提交信息不符合 Conventional Commits 格式"
    echo "格式：<type>(<scope>): <description>"
    echo "示例：feat(login): 添加用户登录功能"
    exit 1
fi
```

### 服务端 Hooks

```bash
# pre-receive：推送到服务器前运行
# 检查分支保护
while read oldrev newrev refname; do
    # 不允许直接推送到 main
    if [ "$refname" = "refs/heads/main" ]; then
        echo "错误：不允许直接推送到 main 分支"
        exit 1
    fi
done
```

### 共享 Hooks（使用 husky）

```bash
# 使用 husky 让 hooks 进入版本控制
npx husky init

# .husky/pre-commit
npm run lint-staged

# .husky/commit-msg
npx --no-install commitlint --edit $1
```

---

## 六、Filter-branch 与 Filter-repo

用于大规模重写历史。

### Git Filter-branch

```bash
# 从整个历史中删除文件
git filter-branch --force --index-filter \
    "git rm --cached --ignore-unmatch passwords.txt" \
    --prune-empty --tag-name-filter cat -- --all

# 全局替换邮箱
git filter-branch --commit-filter '
    if [ "$GIT_AUTHOR_EMAIL" = "wrong@email.com" ];
    then
        GIT_AUTHOR_NAME="New Name"
        GIT_AUTHOR_EMAIL="correct@email.com"
        git commit-tree "$@"
    else
        git commit-tree "$@"
    fi' HEAD

# 清理
git for-each-ref --format="%(refname)" refs/original/ | xargs -n 1 git update-ref -d
git reflog expire --expire=now --all
git gc --aggressive --prune=now
```

### Git Filter-repo（推荐）

```bash
# 安装
pip install git-filter-repo

# 删除文件
git filter-repo --path passwords.txt --invert-paths

# 替换邮箱
git filter-repo --email-callback '
    return b"new@email.com" if email == b"old@email.com" else email
'

# 保留特定目录
git filter-repo --path src/ --path README.md
```

---

## 七、Rerere

Rerere（Reuse Recorded Resolution）自动记录并复用冲突解决。

```bash
# 启用 rerere
git config --global rerere.enabled true

# 工作流程
# 1. 第一次合并遇到冲突，解决并提交
# 2. rerere 自动记录解决方案
# 3. 下次遇到相同的冲突，rerere 自动应用
git merge feature
# Auto-merged file.txt
# CONFLICT
# 解决冲突...
git rerere            # 查看已记录的解决
git add file.txt
git commit

# 查看 rerere 状态
git rerere status
git rerere diff
```

---

## 八、Partial Clone 与 Sparse Checkout

### Partial Clone（部分克隆）

```bash
# 只下载最新版本的文件内容（不下载历史）
git clone --filter=blob:none https://github.com/user/repo.git

# 只下载历史文件的树状结构
git clone --filter=tree:0 https://github.com/user/repo.git

# 按需获取
git fetch --filter=blob:none origin
```

### Sparse Checkout（稀疏检出）

```bash
# 只检出部分目录
git clone --filter=blob:none --sparse https://github.com/user/repo.git
cd repo
git sparse-checkout set src/ docs/
git sparse-checkout add tests/

# 或者：
git clone --no-checkout https://github.com/user/repo.git
cd repo
git sparse-checkout init --cone
git sparse-checkout set src/app
git checkout main
```

---

## 九、Git 内部原理

### 对象存储

```
.git/
├── objects/        # Git 对象存储
│   ├── aa/         # SHA-1 前缀目录
│   │   └── bb...   # 对象文件（zlib 压缩）
│   └── pack/       # 打包文件
├── refs/           # 引用
│   ├── heads/      # 本地分支
│   ├── tags/       # 标签
│   └── remotes/    # 远程引用
├── HEAD            # 当前引用
├── config          # 仓库配置
└── index           # 暂存区
```

### 四种对象类型

```bash
# Blob（文件内容）
echo "hello" | git hash-object --stdin -w
# → 返回 SHA-1 哈希

# Tree（目录结构）

# Commit（提交对象）
git cat-file -p HEAD

# Tag（标签对象）
git cat-file -p v1.0.0
```

### 查看对象

```bash
# 查看对象类型
git cat-file -t a1b2c3d

# 查看对象内容
git cat-file -p a1b2c3d

# 查看树对象
git ls-tree HEAD

# 查看 pack 文件
git verify-pack .git/objects/pack/*.idx
```

## 相关条目

- [[Commands]]
- [[Branch]]
- [[Workflow]]
- [[GitHub]]
- [[05_ComputerScience/SoftwareEngineering/GitAndVersionControl/INDEX|GitAndVersionControl]]
