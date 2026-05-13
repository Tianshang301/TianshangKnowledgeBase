# Git 工作流

## 一、Git Flow

### 分支模型

```
main ──────●─────────●─────────●─── (生产环境)
             \       / \       /
develop ──────●───●───●───●───●─── (开发主线)
               \     /     \
feature/xxx     ●───●       ●───●
                         \       \
release/v1.0              ●───●───●
                                   \
hotfix/critical            ●───────●
```

### 分支说明

| 分支 | 用途 | 来源 | 合并到 |
|------|------|------|--------|
| main | 生产发布 | — | — |
| develop | 日常开发 | main | main（发布时） |
| feature/* | 新功能 | develop | develop |
| release/* | 发布准备 | develop | main + develop |
| hotfix/* | 紧急修复 | main | main + develop |

### 工作流

```bash
# 1. 从 develop 创建 feature 分支
git checkout -b feature/user-login develop

# 2. 在 feature 分支开发
git add .
git commit -m "feat: 添加登录表单"
git commit -m "feat: 实现登录验证"

# 3. 完成功能，合并回 develop
git checkout develop
git merge --no-ff feature/user-login
git branch -d feature/user-login

# 4. 准备发布
git checkout -b release/v1.2.0 develop
# 修改版本号，修复小 bug

# 5. 发布
git checkout main
git merge --no-ff release/v1.2.0
git tag -a v1.2.0 -m "版本 1.2.0"

# 6. 合并回 develop
git checkout develop
git merge --no-ff release/v1.2.0
git branch -d release/v1.2.0

# 7. 紧急修复
git checkout -b hotfix/critical-fix main
# 修复并提交
git commit -m "hotfix: 修复安全漏洞"
git checkout main
git merge --no-ff hotfix/critical-fix
git tag -a v1.2.1 -m "安全修复 v1.2.1"
git checkout develop
git merge --no-ff hotfix/critical-fix
git branch -d hotfix/critical-fix
```

### Git Flow 优缺点

| 优点 | 缺点 |
|------|------|
| 结构清晰，适合版本发布 | 分支多，管理复杂 |
| 生产环境稳定 | 不适合持续部署 |
| 支持多版本并行 | 学习成本高 |

---

## 二、GitHub Flow

### 分支模型

```
main ──────●───●───●───●───●─── (始终可部署)
             \     /     \
feature/xxx   ●───●       ●───●
```

### 工作流

```bash
# 1. 从 main 创建 feature 分支
git checkout -b feature/new-page main

# 2. 提交修改
git commit -m "添加页面标题"
git commit -m "添加表单组件"

# 3. 推送并创建 Pull Request
git push -u origin feature/new-page
# 在 GitHub 上创建 PR

# 4. 代码审查
# 团队成员审查 PR，提出修改意见

# 5. 合并到 main
# 通过 GitHub 界面合并（通常 squash merge）
```

### PR 模板

```markdown
## 变更类型
- [ ] 新功能
- [ ] Bug 修复
- [ ] 重构
- [ ] 文档

## 描述
简要描述变更内容。

## 测试
- [ ] 单元测试通过
- [ ] 集成测试通过
- [ ] 手动测试

## 关联 Issue
Closes #123
```

### GitHub Flow 优缺点

| 优点 | 缺点 |
|------|------|
| 简单，易于理解 | 没有明确的分发阶段 |
| 适合持续部署 | 不适合多版本支持 |
| PR 审查流程自然 | 需要完善的 CI/CD |
| 适合小团队 | |

---

## 三、GitLab Flow

### 分支模型

GitLab Flow 融合了 Git Flow 和 GitHub Flow，增加了环境分支。

```
main ──────●───●───●───●─── (开发主线)
              \     \
staging         ●─────●─── (预发布环境)
                      \
production             ●─── (生产环境)
```

### 环境分支

```bash
# 环境分支
main        # 开发分支，包含所有功能
preprod     # 预发布环境
production  # 生产环境

# 部署流程
git checkout production
git merge preprod
git push origin production
```

### 功能分支 + Issue

```bash
# 创建功能分支（关联 Issue）
git checkout -b 123-user-login main

# 完成开发，提交
git commit -m "添加用户登录功能"

# 推送到远程，创建 MR（Merge Request）
git push -u origin 123-user-login

# 合并到 main（通过 MR）
```

### GitLab Flow 优缺点

| 优点 | 缺点 |
|------|------|
| 环境分支支持多环境部署 | 环境分支可能需要维护 |
| Issue 与分支关联 | 流程比 GitHub Flow 复杂 |
| 适合企业部署流程 | |

---

## 四、Trunk-Based Development（主干开发）

### 分支模型

```
main ──────●───●───●───●───●─── (主干)
             \ /       \ /
feature/xxx   ●         ●
```

核心原则：
- 每天至少合并到主干一次
- 分支存在时间不超过 2 天
- 使用 Feature Toggle（特性开关）

### 特性开关

```java
// 使用特性开关替代长期分支
public class FeatureFlags {
    private static boolean newLoginEnabled =
        System.getenv("NEW_LOGIN_ENABLED") != null;

    public static boolean isNewLoginEnabled() {
        return newLoginEnabled;
    }
}

// 使用
if (FeatureFlags.isNewLoginEnabled()) {
    // 新登录流程
} else {
    // 旧登录流程
}
```

### 主干开发优缺点

| 优点 | 缺点 |
|------|------|
| 极少数合并冲突 | 需要特性开关基础设施 |
| CI/CD 天然适合 | 不适合大型不便拆分的功能 |
| 持续集成友好 | 需要高代码质量纪律 |

---

## 五、工作流选择指南

| 团队规模 | 发布频率 | 推荐工作流 |
|----------|----------|-----------|
| 1-5 人 | 每天多次 | GitHub Flow / 主干开发 |
| 5-20 人 | 每周 | GitLab Flow |
| 20+ 人 | 每月 | Git Flow |
| 大型企业 | 按版本 | Git Flow |
| SaaS 产品 | 持续部署 | GitHub Flow / 主干开发 |
| 移动应用 | 按版本 | Git Flow |

### 混合工作流建议

```bash
# 结合不同工作流的优点
# main → develop → feature 层次（类似 Git Flow）
# 使用 PR 审查（类似 GitHub Flow）
# 环境分支部署（类似 Git Lab Flow）
main → develop → feature/xxx
                   ↓ PR
              develop (自动部署到 staging)
                   ↓
              main (自动部署到 production)
```

---

## 六、代码审查最佳实践

### 审查清单

```
□ 功能正确性
□ 代码风格符合规范
□ 是否覆盖了错误处理
□ 是否存在安全隐患
□ 是否有适当的单元测试
□ 是否有不必要的复杂度
□ 是否遵循 DRY 原则
□ 日志记录是否合理
□ 性能考虑（SQL、缓存）
□ 文档是否更新
```

### 审查流程

```bash
# 1. 审查前
git fetch origin
git log origin/main..origin/feature --oneline

# 2. 查看完整差异
git diff origin/main...origin/feature

# 3. 逐提交审查
git log -p origin/main..origin/feature

# 4. 时间线
# 创建 PR → CI 通过 → 至少 1 人审查 → 修改意见 → 更新 → 批准 → 合并
```

### PR 大小建议

| PR 大小 | 文件数 | 说明 |
|---------|--------|------|
| 小 | 1-3 文件 | 快速审查，推荐 |
| 中 | 4-10 文件 | 正常审查 |
| 大 | 11+ 文件 | 建议拆分 |

---

## 七、版本策略

### SemVer（语义化版本）

```text
主版本号.次版本号.修订号
   │        │       │
   │        │       └── 修订号：向后兼容的 bug 修复
   │        └────────── 次版本号：向后兼容的新功能
   └─────────────────── 主版本号：不兼容的 API 变更

示例：v2.1.3
- 1.0.0 → 1.0.1（修复 bug）
- 1.0.0 → 1.1.0（添加新功能）
- 1.1.0 → 2.0.0（破坏性变更）
```

### 版本分支管理

```bash
# 发布 v1.0.0
git checkout main
git tag -a v1.0.0 -m "正式版 v1.0.0"

# 如果在 v1.0.x 上发现严重 bug 需要修复
git checkout -b v1.0.x v1.0.0
# 在分支上修复
git commit -m "hotfix: 修复 v1.0 上的 bug"
git tag -a v1.0.1 -m "补丁 v1.0.1"

# 同时合并回 develop
git checkout develop
git merge v1.0.x
```

## 相关条目

- [[Branch]]
- [[Commands]]
- [[Advanced]]
- [[GitHub]]
- [[05_ComputerScience/SoftwareEngineering/GitAndVersionControl/INDEX|GitAndVersionControl]]
