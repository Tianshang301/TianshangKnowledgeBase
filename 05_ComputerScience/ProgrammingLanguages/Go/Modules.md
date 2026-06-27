---
aliases: [Modules]
tags: ['ProgrammingLanguages', 'Go', 'Modules']
created: 2026-05-16
updated: 2026-05-16
---

# Go Modules 包管理

## 初始化模块

```bash
# 创建新模块
go mod init github.com/user/myproject

# 添加依赖后自动更新 go.mod
go get github.com/gin-gonic/gin

# 整理依赖（删除未使用，添加缺失）
go mod tidy

# 下载依赖到本地缓存
go mod download

# 查看依赖
go list -m all

# 查看依赖版本
go list -u -m all
```

## go.mod 文件结构

```
module github.com/user/myproject

go 1.21

require (
    github.com/gin-gonic/gin v1.9.1
    github.com/go-sql-driver/mysql v1.7.1
    golang.org/x/text v0.14.0
)

require (
    github.com/bytedance/sonic v1.9.1 // indirect
    github.com/chenzhuoyu/base64x v0.0.0-20221115062448-fe3a3abb8f00 // indirect
)

exclude (
    github.com/old/module v1.2.3
)

replace (
    github.com/original/module => github.com/fork/module v1.0.0
    github.com/unstable/module => ./local/path/module
)

retract (
    v1.0.0 // 版本已废弃
    v1.1.0 // 有严重安全漏洞
)
```

## 常用 go mod 命令

```bash
# 初始化
go mod init <module-path>

# 添加依赖
go get github.com/pkg/errors@v0.9.1
go get github.com/pkg/errors@latest
go get github.com/pkg/errors@master  # 最新 commit

# 升级/降级依赖
go get -u                    # 升级所有直接依赖
go get -u ./...              # 升级当前模块所有依赖
go get -u=patch              # 仅升级补丁版本
go get github.com/gin@v1.8.0

# 移除不再需要的依赖
go mod tidy

# 创建 vendor 目录
go mod vendor

# 验证依赖
go mod verify

# 查看为什么需要某个依赖
go mod why -m <module>

# 查看依赖图
go mod graph

# 清理模块缓存
go clean -modcache

# 复制依赖到本地
go mod download <module>@<version>
```

## go.sum 文件

```bash
# go.sum 记录每个模块版本的哈希值
# 包含 go.mod 中所有直接和间接依赖的加密哈希

# go.sum 文件格式：
# <module> <version> <hash>
# <module> <version>/go.mod <hash>

# 作用：
# 1. 确保依赖完整性（防篡改）
# 2. 提供可复现的构建
# 3. 在多个开发者间保持一致

# go.sum 应提交到版本控制
```

## 语义导入版本控制

```bash
# Go 模块遵循语义化版本：
# vMAJOR.MINOR.PATCH
#   - MAJOR: 不兼容的 API 变更
#   - MINOR: 向后兼容的功能新增
#   - PATCH: 向后兼容的 bug 修复

# 主版本升级（v2+）：
# 方式1：修改 module 路径（推荐）
# go.mod:
module github.com/user/myproject/v2

# 方式2：使用独立分支/目录
# github.com/user/myproject/v2/

# 导入时：
import "github.com/user/myproject/v2/pkg/util"

# 预发布版本：
v1.2.3-alpha.1
v1.2.3-beta.1
v1.2.3-rc.1

# 伪版本（基于 commit）：
v0.0.0-20230901000000-abcdef123456
```

## replace 指令

```go
// 替换依赖为本地路径（常用于开发调试）
replace github.com/my/lib => ../my-lib

// 替换为其他 fork
replace github.com/original/pkg => github.com/myfork/pkg v1.2.3

// 替换为不同版本
replace github.com/gin-gonic/gin => github.com/gin-gonic/gin v1.8.0

// 全局替换所有引用
replace golang.org/x/net => golang.org/x/net v0.17.0
```

## Workspace (Go 1.18+)

```bash
# 创建工作空间
go work init ./module1 ./module2

# go.work 文件
go 1.21

use (
    ./path/to/module1
    ./path/to/module2
)

replace example.com/lib => ./local/lib

# 同时开发多个模块
# 无需在每个模块间使用 replace 指令
# go work use ./new-module  # 添加模块到 workspace
# go work edit -dropuse ./old-module  # 移除

# go.work 不应提交到版本控制（通常是 .gitignore）
```

## GOPATH vs Modules

```bash
# GOPATH 模式（Go 1.11 之前）
# GOPATH/
#   src/    # 源代码
#   pkg/   # 编译包
#   bin/   # 可执行文件

# Module 模式（Go 1.11+，默认 1.16+）
# 项目可以在任何位置
# 不依赖 GOPATH
# 每个模块有独立的 go.mod

# 环境变量设置
go env -w GO111MODULE=on    # 强制使用 modules
go env -w GO111MODULE=auto  # 在 GOPATH 外自动启用
go env -w GO111MODULE=off   # 禁用 modules

# GOPROXY 设置
go env -w GOPROXY=https://goproxy.cn,direct  # 中国地区推荐
go env -w GOPROXY=https://proxy.golang.org,direct  # 官方
go env -w GOPRIVATE=github.com/private/*  # 私有仓库不走代理
```

## 私有仓库

```bash
# 配置私有仓库（不走代理）
go env -w GOPRIVATE=github.com/mycompany/*,gitlab.internal.com/*

# 配置 GONOSUMDB（不检查哈希的模块）
go env -w GONOSUMDB=github.com/mycompany/*

# 配置 GONOSUMCHECK（不检查 checksum 数据库）
go env -w GONOSUMCHECK=private.example.com/*

# Git 配置（私有仓库认证）
# ~/.gitconfig
[url "ssh://git@github.com/mycompany/"]
    insteadOf = https://github.com/mycompany/

# 或者使用 .netrc 文件
# ~/_netrc（Windows）
machine github.com login <token> password x-oauth-basic
```

## 依赖管理最佳实践

```bash
# 1. 固定主版本
go get github.com/gin-gonic/gin@v1.9.1

# 2. 定期更新依赖
go get -u ./...
go mod tidy

# 3. 使用依赖审计工具
go install golang.org/x/vuln/cmd/govulncheck@latest
govulncheck ./...

# 4. 提交 go.sum 到版本控制
# go.sum 确保构建可复现

# 5. 避免使用 latest 标签
# 在 CI/CD 中使用确切版本

# 6. 最小版本选择（MVS）
# Go 选择满足所有依赖的最小兼容版本
# 不会像 npm/maven 那样激进的版本升级

# 7. 保持整洁的 go.mod
# 清除未使用的依赖
go mod tidy

# 8. 使用工具检查
go install github.com/dominikh/go-tools/cmd/staticcheck@latest
staticcheck ./...
```

