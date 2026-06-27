---
aliases: [Concurrency]
tags: ['ProgrammingLanguages', 'Rust', 'Concurrency']
created: 2026-05-16
updated: 2026-05-16
---

# Rust 并发编程

## 线程创建

```rust
use std::thread;
use std::time::Duration;

// 基本线程
fn main() {
    let handle = thread::spawn(|| {
        for i in 1..10 {
            println!("子线程: {}", i);
            thread::sleep(Duration::from_millis(1));
        }
    });

    for i in 1..5 {
        println!("主线程: {}", i);
        thread::sleep(Duration::from_millis(1));
    }

    handle.join().unwrap();  // 等待子线程结束
}

// move 闭包
fn main() {
    let v = vec![1, 2, 3];
    let handle = thread::spawn(move || {
        println!("这里是: {:?}", v);  // 捕获 v 的所有权
    });
    // println!("{:?}", v);  // 编译错误，v 已移动
    handle.join().unwrap();
}
```

## 消息传递（mpsc 通道）

```rust
use std::sync::mpsc;
use std::thread;

fn main() {
    // 创建通道
    let (tx, rx) = mpsc::channel();
    // tx: 发送端（Transmitter）, rx: 接收端（Receiver）

    thread::spawn(move || {
        let val = String::from("hi");
        tx.send(val).unwrap();
        // println!("{}", val);  // 编译错误：val 已被发送
    });

    let received = rx.recv().unwrap();  // 阻塞接收
    println!("收到: {}", received);

    // 多个发送者
    let (tx, rx) = mpsc::channel();
    let tx1 = tx.clone();

    thread::spawn(move || {
        tx.send("来自线程1").unwrap();
    });
    thread::spawn(move || {
        tx1.send("来自线程2").unwrap();
    });

    for msg in rx {  // 迭代接收
        println!("{}", msg);
    }

    // 发送多个值
    let (tx, rx) = mpsc::channel();
    thread::spawn(move || {
        let vals = vec!["a", "b", "c"];
        for val in vals {
            tx.send(val).unwrap();
            thread::sleep(Duration::from_secs(1));
        }
    });
    for received in rx {
        println!("收到: {}", received);
    }
}
```

## 共享状态（Mutex/Arc）

```rust
use std::sync::{Arc, Mutex};
use std::thread;

// 单线程 Mutex
fn main() {
    let m = Mutex::new(5);
    {
        let mut num = m.lock().unwrap();
        *num = 6;
    }  // 自动释放锁
    println!("m = {:?}", m);  // m = Mutex { data: 6 }
}

// 多线程共享 Mutex (Arc)
fn main() {
    let counter = Arc::new(Mutex::new(0));
    let mut handles = vec![];

    for _ in 0..10 {
        let counter = Arc::clone(&counter);
        let handle = thread::spawn(move || {
            let mut num = counter.lock().unwrap();
            *num += 1;
        });
        handles.push(handle);
    }

    for handle in handles {
        handle.join().unwrap();
    }

    println!("结果: {}", *counter.lock().unwrap());  // 10
}

// RwLock: 读写锁
use std::sync::RwLock;

fn main() {
    let lock = RwLock::new(5);
    // 多个读锁可同时存在
    {
        let r1 = lock.read().unwrap();
        let r2 = lock.read().unwrap();
        println!("{}, {}", r1, r2);
    }
    // 写锁独占
    {
        let mut w = lock.write().unwrap();
        *w += 1;
    }
}

// 原子类型
use std::sync::atomic::{AtomicBool, Ordering};

fn main() {
    let flag = AtomicBool::new(false);
    flag.store(true, Ordering::SeqCst);
    let val = flag.load(Ordering::SeqCst);
    println!("{}", val);  // true
}
```

## Send 和 Sync Trait

```rust
// Send: 所有权可以跨线程转移
// 几乎所有类型都是 Send，除了 Rc<T> 等

// Sync: 引用可以跨线程共享
// 几乎所有类型都是 Sync，除了 Rc<T>、RefCell<T> 等

// 手动实现 Send/Sync 是不安全的（unsafe）
struct MyType {
    // 所有字段都是 Send + Sync
}

// Mutex<T> 实现了 Sync，允许跨线程共享
// Arc<T> 实现了 Send + Sync（当 T: Send + Sync 时）
```

## 异步编程

```rust
// async/await
use tokio::time::{sleep, Duration};

async fn say_world() {
    sleep(Duration::from_secs(1)).await;
    println!("world");
}

#[tokio::main]
async fn main() {
    let op = say_world();
    println!("hello");
    op.await;  // 等待异步操作完成
}

// 并发执行
async fn task1() -> String {
    sleep(Duration::from_secs(1)).await;
    "Task1".to_string()
}

async fn task2() -> String {
    sleep(Duration::from_secs(2)).await;
    "Task2".to_string()
}

#[tokio::main]
async fn main() {
    let (r1, r2) = tokio::join!(task1(), task2());
    println!("{}, {}", r1, r2);  // 总共约 2 秒
}

// tokio::spawn
#[tokio::main]
async fn main() {
    let handle = tokio::spawn(async {
        // 在后台运行
        "done"
    });
    let result = handle.await.unwrap();
    println!("{}", result);
}

// select! 宏
use tokio::select;

#[tokio::main]
async fn main() {
    let mut task1 = tokio::spawn(async { /* ... */ });
    let mut task2 = tokio::spawn(async { /* ... */ });

    select! {
        _ = &mut task1 => println!("task1 完成"),
        _ = &mut task2 => println!("task2 完成"),
    }
}

// tokio::sync 通道
use tokio::sync::mpsc;

#[tokio::main]
async fn main() {
    let (tx, mut rx) = mpsc::channel(32);
    tokio::spawn(async move {
        tx.send("hello").await.unwrap();
    });
    while let Some(msg) = rx.recv().await {
        println!("{}", msg);
    }
}

// 多线程运行时
#[tokio::main(flavor = "multi_thread", worker_threads = 4)]
async fn main() {
    // 多线程异步运行时
}
```

## 协程 vs OS 线程对比

| 特性 | 异步协程 | OS 线程 |
|------|---------|---------|
| 创建开销 | 极小（几十字节） | 较大（MB 级别） |
| 上下文切换 | 函数调用级别 | 内核态切换 |
| 数量上限 | 百万级 | 数千级 |
| 调度方式 | 协作式 | 抢占式 |
| CPU 密集任务 | 不适合（需 spawn_blocking） | 适合 |
| 阻塞操作 | 会阻塞整个线程 | 只阻塞当前线程 |
| 调试难度 | 较复杂 | 较直接 |

