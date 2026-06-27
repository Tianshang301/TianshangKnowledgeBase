---
aliases:
  - 异步Rust
  - Async Rust
  - Rust异步编程
  - tokio
tags:
  - Rust
  - async
  - await
  - tokio
  - 计算机科学
created: 2026-06-27
updated: 2026-06-27
---

# 异步Rust

异步 Rust 是 Rust 处理并发 I/O 的核心机制，通过 async/await 语法和 Future trait 实现高效的非阻塞并发，无需操作系统线程的开销。

## async/await 基础

### 基本语法

async/await 是 Rust 异步编程的语法糖：

- **async fn**：声明异步函数，返回 Future
- **.await**：等待 Future 完成，不阻塞当前线程
- **惰性执行**：Future 在被 .await 或 poll 时才开始执行
- **零成本**：async/await 在编译时转换为状态机

```rust
async fn fetch_data(url: &str) -> Result<String, Error> {
    let response = reqwest::get(url).await?;
    let body = response.text().await?;
    Ok(body)
}

#[tokio::main]
async fn main() {
    match fetch_data("https://api.example.com/data").await {
        Ok(data) => println!("Got data: {}", data),
        Err(e) => eprintln!("Error: {}", e),
    }
}
```

### Future trait

Future 是异步计算的核心 trait：

```rust
pub trait Future {
    type Output;
    
    fn poll(self: Pin<&mut Self>, cx: &mut Context<'_>) -> Poll<Self::Output>;
}

pub enum Poll<T> {
    Ready(T),    // Future 完成，返回结果
    Pending,     // Future 未完成，稍后再次 poll
}
```

### 执行器（Executor）

执行器负责驱动 Future 执行：

- **tokio**：最流行的异步运行时
- **async-std**：标准库风格的异步运行时
- **smol**：轻量级异步运行时
- **自定义执行器**：可以根据需求自定义

```rust
// tokio 运行时
#[tokio::main]
async fn main() {
    // 异步代码
}

// 或手动创建运行时
fn main() {
    let rt = tokio::runtime::Runtime::new().unwrap();
    rt.block_on(async {
        // 异步代码
    });
}
```

## tokio 运行时

### 运行时配置

tokio 提供灵活的运行时配置：

```rust
use tokio::runtime::Builder;

fn main() {
    let rt = Builder::new_multi_thread()
        .worker_threads(4)        // 工作线程数
        .enable_all()             // 启用所有功能
        .build()
        .unwrap();
    
    rt.block_on(async {
        // 异步代码
    });
}
```

### tokio 核心组件

- **Runtime**：异步运行时
- **Task**：异步任务
- **Channel**：任务间通信
- **Sync**：同步原语
- **IO**：异步 I/O

### 任务创建

```rust
use tokio::task;

#[tokio::main]
async fn main() {
    // 生成任务
    let handle = task::spawn(async {
        // 异步工作
        42
    });
    
    // 等待任务完成
    let result = handle.await.unwrap();
    println!("Result: {}", result);
}

// 带返回值的任务
async fn process_data(data: Vec<u8>) -> Vec<u8> {
    // 处理数据
    data
}
```

### 并发执行

```rust
use tokio::task;

#[tokio::main]
async fn main() {
    // 并发执行多个任务
    let (r1, r2, r3) = tokio::join!(
        fetch_data("url1"),
        fetch_data("url2"),
        fetch_data("url3"),
    );
    
    // 或使用 select!
    tokio::select! {
        result = fetch_data("url1") => {
            println!("First completed: {:?}", result);
        }
        _ = tokio::time::sleep(Duration::from_secs(5)) => {
            println!("Timeout!");
        }
    }
}
```

## Pin 与 Unpin

### Pin 概念

Pin 用于固定值在内存中的位置：

- **自引用结构**：异步函数生成的状态机可能包含自引用
- **安全性**：Pin 保证被固定的值不会被移动
- **Pin<P>**：固定指针 P 指向的值
- **Unpin**：实现了 Unpin 的类型可以安全移动

```rust
use std::pin::Pin;

// 自引用结构
struct SelfReferential {
    data: String,
    // 指向 data 的引用
    pointer: *const String,
}

// 需要 Pin 来保证安全
impl SelfReferential {
    fn new(data: String) -> Pin<Box<Self>> {
        let mut boxed = Box::new(SelfReferential {
            data,
            pointer: std::ptr::null(),
        });
        let pointer = &boxed.data as *const String;
        
        // 安全地创建自引用
        unsafe {
            let mut_ref = Pin::as_mut(&mut Pin::new(&mut *boxed));
            Pin::get_unchecked_mut(mut_ref).pointer = pointer;
        }
        
        Pin::new(boxed)
    }
}
```

### Unpin trait

```rust
// 大多数类型自动实现 Unpin
pub auto trait Unpin {}

// !Unpin 的类型需要 Pin 来保证安全
// 例如：async fn 生成的 Future
```

### Pin 使用场景

```rust
use std::pin::Pin;
use std::future::Future;

// 接受 pinned future
async fn process_future(f: Pin<Box<dyn Future<Output = i32>>>) -> i32 {
    f.await
}

// 返回 pinned future
fn create_future() -> Pin<Box<dyn Future<Output = i32>>> {
    Box::pin(async { 42 })
}
```

## 异步流（Async Stream）

### Stream trait

Stream 是异步版本的 Iterator：

```rust
use futures::stream::Stream;

pub trait Stream {
    type Item;
    
    fn poll_next(
        self: Pin<&mut Self>,
        cx: &mut Context<'_>,
    ) -> Poll<Option<Self::Item>>;
}
```

### 使用 tokio-stream

```rust
use tokio_stream::StreamExt;
use tokio::time::{interval, Duration};

#[tokio::main]
async fn main() {
    let mut stream = tokio_stream::wrappers::IntervalStream::new(
        interval(Duration::from_secs(1))
    );
    
    while let Some(item) = stream.next().await {
        println!("Tick: {:?}", item);
    }
}
```

### 自定义 Stream

```rust
use tokio_stream::Stream;
use std::pin::Pin;
use std::task::{Context, Poll};

struct Counter {
    count: u32,
    max: u32,
}

impl Stream for Counter {
    type Item = u32;
    
    fn poll_next(mut self: Pin<&mut Self>, cx: &mut Context<'_>) -> Poll<Option<u32>> {
        if self.count < self.max {
            self.count += 1;
            Poll::Ready(Some(self.count))
        } else {
            Poll::Ready(None)
        }
    }
}
```

## 异步同步原语

### Mutex

异步互斥锁：

```rust
use tokio::sync::Mutex;
use std::sync::Arc;

#[tokio::main]
async fn main() {
    let data = Arc::new(Mutex::new(Vec::new()));
    
    let mut handles = vec![];
    for i in 0..10 {
        let data = Arc::clone(&data);
        handles.push(tokio::spawn(async move {
            let mut locked = data.lock().await;
            locked.push(i);
        }));
    }
    
    for handle in handles {
        handle.await.unwrap();
    }
    
    println!("Data: {:?}", data.lock().await);
}
```

### Channel

异步通道：

```rust
use tokio::sync::{mpsc, oneshot, broadcast};

#[tokio::main]
async fn main() {
    // mpsc 通道：多生产者，单消费者
    let (tx, mut rx) = mpsc::channel(32);
    
    tokio::spawn(async move {
        tx.send("hello").await.unwrap();
    });
    
    let msg = rx.recv().await.unwrap();
    println!("Received: {}", msg);
    
    // oneshot 通道：单次发送
    let (tx, rx) = oneshot::channel();
    tokio::spawn(async move {
        tx.send(42).unwrap();
    });
    let value = rx.await.unwrap();
    
    // broadcast 通道：广播
    let (tx, _) = broadcast::channel(16);
    let mut rx1 = tx.subscribe();
    let mut rx2 = tx.subscribe();
    
    tokio::spawn(async move {
        tx.send("broadcast").unwrap();
    });
    
    println!("rx1: {}", rx1.recv().await.unwrap());
    println!("rx2: {}", rx2.recv().await.unwrap());
}
```

### RwLock

异步读写锁：

```rust
use tokio::sync::RwLock;
use std::sync::Arc;

#[tokio::main]
async fn main() {
    let lock = Arc::new(RwLock::new(0));
    
    // 多个读者可以并发
    let r1 = lock.read().await;
    let r2 = lock.read().await;
    println!("Readers: {} {}", r1, r2);
    drop(r1);
    drop(r2);
    
    // 写者独占访问
    let mut w = lock.write().await;
    *w += 1;
}
```

## 异步错误处理

### 错误传播

```rust
use tokio::fs::File;
use tokio::io::AsyncReadExt;

async fn read_file(path: &str) -> Result<String, Box<dyn std::error::Error>> {
    let mut file = File::open(path).await?;
    let mut contents = String::new();
    file.read_to_string(&mut contents).await?;
    Ok(contents)
}

#[tokio::main]
async fn main() {
    match read_file("data.txt").await {
        Ok(contents) => println!("File: {}", contents),
        Err(e) => eprintln!("Error: {}", e),
    }
}
```

### 超时处理

```rust
use tokio::time::{timeout, Duration};

#[tokio::main]
async fn main() {
    match timeout(Duration::from_secs(5), fetch_data()).await {
        Ok(result) => println!("Got result: {:?}", result),
        Err(_) => println!("Timeout!"),
    }
}
```

## 性能优化

### 避免阻塞

```rust
use tokio::task;

// 错误：在异步上下文中使用阻塞操作
async fn bad_example() {
    std::thread::sleep(Duration::from_secs(1)); // 阻塞！
}

// 正确：使用异步版本或 spawn_blocking
async fn good_example() {
    // 使用异步版本
    tokio::time::sleep(Duration::from_secs(1)).await;
    
    // 或将阻塞操作移到专用线程
    let result = task::spawn_blocking(|| {
        // 阻塞操作
        expensive_computation()
    }).await.unwrap();
}
```

### 任务调度

```rust
use tokio::task::yield_now;

async fn cooperative_task() {
    for i in 0..1000 {
        // 长时间运行的任务应该定期让出执行权
        if i % 100 == 0 {
            tokio::task::yield_now().await;
        }
        // 处理数据
    }
}
```

### 连接池

```rust
use bb8::Pool;
use bb8_postgres::PostgresConnectionManager;
use tokio_postgres::NoTls;

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    let manager = PostgresConnectionManager::new(
        "host=localhost user=test dbname=test".parse()?,
        NoTls,
    );
    
    let pool = Pool::builder().build(manager).await?;
    
    let conn = pool.get().await?;
    // 使用连接...
    
    Ok(())
}
```

## 调试与测试

### 异步测试

```rust
#[tokio::test]
async fn test_fetch_data() {
    let result = fetch_data("https://example.com").await;
    assert!(result.is_ok());
}

#[tokio::test(flavor = "multi_thread", worker_threads = 2)]
async fn test_concurrent() {
    // 测试并发场景
}
```

### 调试工具

- **tokio-console**：实时诊断 tokio 应用
- **tracing**：异步感知的日志和追踪
- **flamegraph**：性能分析

```rust
use tracing::{info, instrument};

#[instrument]
async fn process_request(id: u64) {
    info!("Processing request");
    // 处理逻辑
}
```

## 常见陷阱

### 借用问题

```rust
// 问题：async move 和借用
async fn problem() {
    let data = vec![1, 2, 3];
    tokio::spawn(async move {
        println!("{:?}", data);
    });
    // println!("{:?}", data); // 编译错误！data 已移动
}

// 解决方案：使用 Arc 或 clone
async fn solution() {
    let data = Arc::new(vec![1, 2, 3]);
    let data_clone = Arc::clone(&data);
    tokio::spawn(async move {
        println!("{:?}", data_clone);
    });
    println!("{:?}", data);
}
```

### Send 约束

```rust
// tokio::spawn 要求 Future 是 Send 的
// !Send 的类型不能直接在 spawn 中使用

// 解决方案：使用 LocalSet 或 spawn_local
use tokio::task::LocalSet;

#[tokio::main]
async fn main() {
    let local = LocalSet::new();
    local.run_until(async {
        tokio::task::spawn_local(async {
            // 可以使用 !Send 类型
        }).await;
    }).await;
}
```

## 相关链接

- [[OwnershipAndBorrowing]] - Rust 所有权与借用
- [[UnsafeAndFFI]] - unsafe 与 FFI
