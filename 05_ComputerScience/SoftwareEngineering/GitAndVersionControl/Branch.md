---
aliases: [Branch]
tags: ['SoftwareEngineering', 'GitAndVersionControl', 'Branch']
---

# Git 分支策略

## 一、分支概念

### 分支的本质

Git 分支本质上是一个指向提交对象的可变指针。

```bash
# HEAD 是当前所在分支的引用
# 分支只是一个 40 字节的 SHA-1 文件
cat .git/HEAD           # ref: refs/heads/main
cat .git/refs/heads/main  # 某个提交的 SHA-1 值
```

### 分支创建

```bash
# HEAD 指向 main，创建 dev 分支后 HEAD 仍指向 main
git branch dev
# .git/refs/heads/dev → 指向与 main 相同的提交
```

### HEAD 指针

```
        ┌───── HEAD
        │
        ▼
    ┌──────┐     ┌──────┐     ┌──────┐
    │ C1   │────▶│ C2   │────▶│ C3   │
    └──────┘     └──────┘     └──────┘
                                ▲
                                │
                          ┌─────┴─────┐
                          │ main      │
                          │ dev       │
                          └───────────┘
```

## 二、Merge vs Rebase

### Merge（合并）

```bash
# 将 feature 分支合并到 main
git checkout main
git merge feature
```

```
合并前：
    A───B───C  (main)
         \
          D───E  (feature)

合并后：
    A───B───C───F (merge commit)
         \     /
          D───E
```

**优点**：
- 保留完整的历史记录
- 不重写提交历史
- 适合公共分支

**缺点**：
- 历史图可能变得杂乱
- 合并提交增加历史复杂度

### Rebase（变基）

```bash
# 将 feature 变基到 main
git checkout feature
git rebase main     # 或 git rebase main feature
```

```
变基前：
    A───B───C  (main)
         \
          D───E  (feature)

变基后（Git 会重写 D, E 为 D', E'）：
    A───B───C  (main)
             \
              D'───E'  (feature)

快速合并到 main：
    git checkout main
    git merge feature   # 快进合并，无额外提交

最终：
    A───B───C───D'───E'  (main, feature)
```

**优点**：
- 线性历史，整洁清晰
- 无多余合并提交
- 便于 bisect 定位问题

**缺点**：
- 重写提交历史
- 公共分支上使用会导致混乱
- 需处理多次冲突

### 选择指南

| 场景 | 使用 |
|------|------|
| 公共分支（main, develop） | Merge |
| 个人/私有分支 | Rebase |
| 拉取远程分支 | `git pull --rebase` |
| 提交到 PR | Rebase 后再合并 |
| 保留精确历史 | Merge |
| 整洁历史 | Rebase |

```bash
# 安全变基：只对你尚未推送的提交变基
# 绝不 rebase 已推送到远程的提交

# 黄金法则：
# 1. 公共分支用 merge
# 2. 个人分支用 rebase
# 3. 从不 rebase 已推送的提交
```

---

## 三、Pull --rebase

```bash
# 传统 pull（会创建合并提交）
git pull = git fetch + git merge

# 推荐方式（线性历史）
git pull --rebase = git fetch + git rebase

# 设置为默认
git config --global pull.rebase true
```

### 场景：有本地提交时拉取

```bash
# 本地有提交，远程也有了新提交
# main: A───B───C (远程)
# main: A───B───D (本地)

# git pull（默认 merge）：
# A───B───C───M (merge commit)
#      \     /
#       D───┘

# git pull --rebase：
# A───B───C───D' (线性历史，D 被重签到 C 之后)
```

---

## 四、冲突解决

### 冲突标记

```c
<<<<<<< HEAD          // 当前分支版本
int max_count = 100;
=======               // 分隔符
int max_count = 200;  // 合并进来的版本
>>>>>>> feature       // 来源分支
```

### 冲突解决步骤

```bash
# 1. 发生冲突
git merge feature
# 输出：CONFLICT in file.txt

# 2. 查看冲突文件
git status

# 3. 手动编辑解决冲突
vim file.txt
# 保留需要的内容，删除冲突标记

# 4. 标记已解决
git add file.txt

# 5. 完成合并
git commit

# 或使用工具
git mergetool    # 配置的外部合并工具
```

### 合并策略

```bash
# 常用策略
git merge -s recursive feature        # 默认（递归策略）
git merge -s resolve feature          # 简单三路合并（更快但更保守）
git merge -s octopus feature1 feature2  # 合并多个分支（默认）
git merge -s ours feature             # 保留当前分支，忽略其他

# 子策略
git merge -X ours feature             # 冲突时使用当前分支版本
git merge -X theirs feature           # 冲突时使用合并分支版本
git merge -X patience feature         # 更精细的差异算法
```

---

## 五、高级分支管理

### 远程跟踪分支

```bash
# 远程跟踪分支 origin/main 反映远程仓库的状态
# 本地分支 main 跟踪远程的 origin/main

# 查看跟踪关系
git branch -vv
git remote show origin

# 设置跟踪
git branch -u origin/develop
git branch --set-upstream-to=origin/develop develop

# 首次推送设置跟踪
git push -u origin develop

# 同步远程分支引用
git fetch --prune     # 删除本地已不存在的远程分支引用
```

### 分离 HEAD 状态

```bash
# 查看历史提交会导致 HEAD 分离
git checkout HEAD~3

# 在分离 HEAD 状态下做修改
# 如果创建了新提交，没有分支指向它
# 需要创建一个分支来保存工作
git branch new-branch
git checkout new-branch

# 或者在分离状态下
git switch -c new-branch    # 创建分支并切换（安全）
```

### 分支清理

```bash
# 删除已合并的分支
git branch --merged | grep -v "\*" | xargs -n 1 git branch -d

# 查看未合并的分支
git branch --no-merged

# 清理远程已删除分支的本地引用
git remote prune origin

# 批量删除本地分支（除 main 外）
git branch | grep -v "main" | xargs git branch -D
```

---

## 六、分支命名规范

```bash
# 推荐命名方式
feature/xxx         # 新功能
bugfix/xxx          # 修改错误
hotfix/xxx          # 紧急修复
release/xxx         # 发布准备
chore/xxx           # 工具/配置变更
docs/xxx            # 文档
refactor/xxx        # 重构

# 示例
git checkout -b feature/user-login
git checkout -b bugfix/fix-null-pointer
git checkout -b hotfix/critical-security-fix
git checkout -b release/v2.0.0
```

---

## 七、最佳实践

### 分支工作流建议

```bash
# 1. 保持分支短命
#    创建分支 → 完成工作 → 合并 → 删除

# 2. 经常同步主分支
git checkout feature
git fetch origin
git rebase origin/main    # 或 merge

# 3. 提交粒度适中
#    每个提交一个逻辑变更

# 4. 提交信息清晰
#    提交前 git diff --staged 检查变更
#    git commit -m "feat: 添加用户注册功能"

# 5. 合并前压缩提交
git rebase -i HEAD~5
# 将多个 WIP 提交压缩为一个
```

### 常见场景

```bash
# 场景1：误提交到 main 分支
git branch feature           # 创建分支保存提交
git reset --hard origin/main # 重置 main
git checkout feature         # 在 feature 继续工作

# 场景2：合并错分支
git merge --abort

# 场景3：找回误删的分支
git reflog
git branch recover-branch HASH

# 场景4：将一个分支的部分文件合并到另一个
git checkout file.txt feature/branch
# 或
git checkout --patch feature/branch file.txt

# 场景5：暂存部分修改
git add -p    # 交互式暂存
```

## 相关条目

- [[Workflow]]
- [[Commands]]
- [[Advanced]]
- [[GitHub]]
- [[05_ComputerScience/SoftwareEngineering/GitAndVersionControl/INDEX|GitAndVersionControl]]
