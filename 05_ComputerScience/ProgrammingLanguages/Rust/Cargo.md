# Rust 包管理与 Cargo

## Cargo 常用命令

```bash
# 创建新项目
cargo new my_project        # 创建二进制项目
cargo new my_lib --lib      # 创建库项目
cargo init                  # 在当前目录初始化

# 构建和运行
cargo build                 # 调试构建
cargo build --release       # 发布构建（带优化）
cargo run                   # 构建并运行
cargo check                 # 快速检查代码是否能编译（不生成可执行文件）

# 测试
cargo test                  # 运行测试
cargo test -- --nocapture   # 显示测试输出

# 代码质量
cargo clippy                # 代码 lint 检查
cargo fmt                   # 代码格式化
cargo fix                   # 自动修复编译警告

# 文档
cargo doc                   # 生成文档
cargo doc --open            # 生成并在浏览器打开

# 依赖管理
cargo add serde             # 添加依赖
cargo add serde --features derive
cargo remove serde          # 移除依赖
cargo update                # 更新依赖
cargo outdated              # 检查过时依赖

# 发布
cargo package               # 打包检查
cargo publish               # 发布到 crates.io

# 其他
cargo clean                 # 清理构建产物
cargo tree                  # 显示依赖树
cargo audit                 # 检查安全漏洞
```

## Cargo.toml 结构

```toml
[package]
name = "my_project"
version = "0.1.0"
edition = "2021"                    # Rust 版本: 2015, 2018, 2021
description = "项目描述"
license = "MIT"
authors = ["Your Name <email@example.com>"]
repository = "https://github.com/user/repo"
documentation = "https://docs.rs/my_project"
readme = "README.md"
keywords = ["cli", "tool"]
categories = ["command-line-utilities"]

# 依赖
[dependencies]
serde = { version = "1.0", features = ["derive"] }
tokio = { version = "1.0", features = ["full"] }
regex = "1.5"
reqwest = { version = "0.11", default-features = false, features = ["json"] }

[dev-dependencies]                  # 仅用于测试的依赖
tempfile = "3.0"
criterion = "0.3"

[build-dependencies]                # 构建脚本依赖
cc = "1.0"

[features]                          # 特性标记
default = ["std"]
std = []
full = ["std", "extra"]
extra = []

[lib]
name = "my_lib"
path = "src/lib.rs"
crate-type = ["lib", "cdylib"]      # 库类型

bin                             # 二进制目标
name = "my_bin"
path = "src/bin/main.rs"

example
name = "example1"
path = "examples/example1.rs"

test
name = "integration_test"
path = "tests/integration_test.rs"
```

## 特性标记

```toml
[features]
default = ["full"]
full = ["network", "database"]
network = []
database = ["diesel"]

[dependencies]
diesel = { version = "2.0", optional = true }

# 代码中使用
#[cfg(feature = "network")]
fn network_function() { /* ... */ }

#[cfg(not(feature = "database"))]
fn no_database() { /* ... */ }

// 使用方式
// Cargo.toml 依赖方:
// my_crate = { version = "0.1", default-features = false, features = ["network"] }
```

## 工作空间（Workspace）

```toml
# 根目录 Cargo.toml
[workspace]
members = [
    "crates/core",
    "crates/cli",
    "crates/web",
]
resolver = "2"

# 子 crate 的 Cargo.toml
# [package]
# name = "core"
# version = "0.1.0"
# edition = "2021"

# 工作空间级命令
# cargo build --workspace    # 构建所有 crate
# cargo test --workspace     # 测试所有 crate
# cargo run -p cli          # 运行特定 crate
```

## 构建脚本 (build.rs)

```rust
// build.rs
fn main() {
    // 编译时执行
    println!("cargo:rerun-if-changed=build.rs");
    println!("cargo:rerun-if-changed=src/config.proto");

    // 生成代码
    // prost_build::compile_protos(&["src/config.proto"], &["src/"]).unwrap();

    // 设置环境变量
    println!("cargo:rustc-env=BUILD_DATE={}", chrono::Local::now().format("%Y-%m-%d"));

    // 链接系统库
    // println!("cargo:rustc-link-lib=ssl");
}
```

## 测试

```rust
// 单元测试（与代码在同一文件）
pub fn add(a: i32, b: i32) -> i32 {
    a + b
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_add() {
        assert_eq!(add(2, 3), 5);
    }

    #[test]
    fn test_add_negative() {
        assert_eq!(add(-1, 1), 0);
    }

    #[test]
    #[should_panic(expected = "overflow")]
    fn test_overflow() {
        // 预期会 panic
    }

    #[test]
    fn test_with_result() -> Result<(), String> {
        if add(2, 2) == 4 {
            Ok(())
        } else {
            Err(String::from("2 + 2 != 4"))
        }
    }

    #[test]
    #[ignore]
    fn expensive_test() {
        // 需要较长运行的测试
    }
}

// 集成测试（tests/ 目录）
// tests/integration_test.rs
use my_crate;

#[test]
fn test_integration() {
    assert!(my_crate::do_something());
}

// 文档测试（文档中的代码示例会被测试）
/// ```
/// let result = my_crate::add(2, 3);
/// assert_eq!(result, 5);
/// ```
pub fn add(a: i32, b: i32) -> i32 {
    a + b
}

// 基准测试
#[cfg(test)]
mod benchmarks {
    use super::*;
    use test::Bencher;

    #[bench]
    fn bench_add(b: &mut Bencher) {
        b.iter(|| add(1000, 2000));
    }
}
```

## 发布到 crates.io

```bash
# 登录
cargo login <api-token>

# 打包验证
cargo package

# 发布
cargo publish

# 版本更新
# 修改 Cargo.toml 中的 version
cargo publish

# 废弃版本
cargo yank --version 0.1.0
cargo yank --version 0.1.0 --undo
```

## Cargo.lock

- 记录所有依赖的确切版本
- 二进制项目应提交 Cargo.lock 到版本控制
- 库项目不应提交 Cargo.lock（让下游决定依赖版本）
- `cargo update` 根据语义版本规则更新依赖
