---
aliases:
  - Goroutine
  - Channel
  - Go并发
  - GMP模型
tags:
  - Go
  - goroutine
  - channel
  - 并发
  - 计算机科学
created: 2026-06-27
updated: 2026-06-27
---

# Goroutine与Channel

Goroutine 和 Channel 是 Go 语言并发编程的核心原语，通过 CSP（Communicating Sequential Processes）模型实现简洁高效的并发。

## Goroutine 基础

### 什么是 Goroutine

Goroutine 是 Go 运行时管理的轻量级线程：

- **极小栈空间**：初始仅 2KB，可动态增长
- **用户态调度**：由 Go 运行时调度，非操作系统
- **低成本创建**：创建和切换开销极小
- **M:N 模型**：M 个 Goroutine 映射到 N 个 OS 线程

```go
func main() {
    // 启动 goroutine
    go func() {
        fmt.Println("Hello from goroutine")
    }()
    
    // 主 goroutine 继续执行
    fmt.Println("Hello from main")
    
    // 等待（实际应用中应使用 sync.WaitGroup）
    time.Sleep(time.Second)
}
```

### 创建 Goroutine

```go
// 方式1：匿名函数
go func() {
    // 工作
}()

// 方式2：命名函数
go worker(id)

// 方式3：方法调用
go obj.Method()

func worker(id int) {
    fmt.Printf("Worker %d starting\n", id)
    time.Sleep(time.Second)
    fmt.Printf("Worker %d done\n", id)
}
```

### Goroutine 泄漏

```go
// 泄漏的 goroutine
func leakyFunction() {
    ch := make(chan int)
    go func() {
        // 如果没有从 ch 读取，这个 goroutine 永远阻塞
        ch <- 42
    }()
    // 忘记读取 ch，goroutine 泄漏
}

// 修复方案：使用 context 或 done channel
func fixedFunction(ctx context.Context) {
    ch := make(chan int)
    go func() {
        select {
        case ch <- 42:
        case <-ctx.Done():
            return // 安全退出
        }
    }()
}
```

## GMP 调度模型

### 模型概述

Go 的 GMP 调度模型：

- **G（Goroutine）**：用户态的执行单元
- **M（Machine）**：操作系统线程
- **P（Processor）**：逻辑处理器，持有运行队列

```
GMP 调度模型：
┌─────────────────────────────────────────┐
│                Go Runtime                │
├─────────────────────────────────────────┤
│  ┌─────┐  ┌─────┐  ┌─────┐  ┌─────┐   │
│  │  P  │  │  P  │  │  P  │  │  P  │   │
│  │Queue│  │Queue│  │Queue│  │Queue│   │
│  └──┬──┘  └──┬──┘  └──┬──┘  └──┬──┘   │
│     │        │        │        │       │
│  ┌──┴──┐  ┌──┴──┐  ┌──┴──┐  ┌──┴──┐   │
│  │  M  │  │  M  │  │  M  │  │  M  │   │
│  └─────┘  └─────┘  └─────┘  └─────┘   │
├─────────────────────────────────────────┤
│            Operating System             │
│   ┌─────┐  ┌─────┐  ┌─────┐           │
│   │Thread│  │Thread│  │Thread│          │
│   └─────┘  └─────┘  └─────┘           │
└─────────────────────────────────────────┘
```

### 调度策略

- **本地队列**：每个 P 维护本地 Goroutine 队列
- **工作窃取**：空闲 P 从其他 P 偷取 Goroutine
- **系统调用处理**：M 阻塞时，P 绑定到其他 M
- **抢占调度**：Go 1.14 引入基于信号的抢占

### GOMAXPROCS

```go
import "runtime"

func main() {
    // 设置逻辑处理器数量
    runtime.GOMAXPROCS(runtime.NumCPU())
    
    // 获取当前设置
    fmt.Println("GOMAXPROCS:", runtime.GOMAXPROCS(0))
}
```

## Channel 基础

### Channel 类型

Channel 是 Goroutine 间的通信管道：

```go
// 无缓冲 channel
ch := make(chan int)

// 有缓冲 channel
ch := make(chan int, 10)

// 只写 channel
var ch chan<- int

// 只读 channel
var ch <-chan int
```

### 发送与接收

```go
func main() {
    ch := make(chan string)
    
    // 发送数据
    go func() {
        ch <- "Hello from goroutine"
    }()
    
    // 接收数据
    msg := <-ch
    fmt.Println(msg)
}
```

### 无缓冲 vs 有缓冲

```go
// 无缓冲：同步通信
// 发送和接收都会阻塞，直到另一方准备好
ch := make(chan int)
go func() { ch <- 42 }() // 阻塞直到有人接收
val := <-ch               // 阻塞直到有人发送

// 有缓冲：异步通信
// 发送只在缓冲区满时阻塞，接收只在缓冲区空时阻塞
ch := make(chan int, 2)
ch <- 1  // 不阻塞
ch <- 2  // 不阻塞
// ch <- 3 // 阻塞！缓冲区已满
```

### Channel 方向

```go
// 双向 channel
ch := make(chan int)

// 只写 channel（发送端）
func producer(ch chan<- int) {
    ch <- 42
}

// 只读 channel（接收端）
func consumer(ch <-chan int) {
    val := <-ch
    fmt.Println(val)
}

func main() {
    ch := make(chan int)
    go producer(ch)
    consumer(ch)
}
```

## Select 语句

### 基本 select

```go
func main() {
    ch1 := make(chan string)
    ch2 := make(chan string)
    
    go func() {
        time.Sleep(1 * time.Second)
        ch1 <- "one"
    }()
    
    go func() {
        time.Sleep(2 * time.Second)
        ch2 <- "two"
    }()
    
    // 等待第一个就绪的 channel
    select {
    case msg := <-ch1:
        fmt.Println("Received", msg)
    case msg := <-ch2:
        fmt.Println("Received", msg)
    }
}
```

### 超时控制

```go
func main() {
    ch := make(chan string)
    
    go func() {
        time.Sleep(3 * time.Second)
        ch <- "result"
    }()
    
    select {
    case msg := <-ch:
        fmt.Println("Received:", msg)
    case <-time.After(2 * time.Second):
        fmt.Println("Timeout!")
    }
}
```

### 非阻塞操作

```go
func main() {
    ch := make(chan int, 1)
    
    select {
    case ch <- 42:
        fmt.Println("Sent 42")
    default:
        fmt.Println("Channel not ready")
    }
    
    select {
    case val := <-ch:
        fmt.Println("Received:", val)
    default:
        fmt.Println("No data available")
    }
}
```

### 退出 channel

```go
func worker(done chan bool) {
    fmt.Println("Working...")
    time.Sleep(time.Second)
    fmt.Println("Done")
    done <- true
}

func main() {
    done := make(chan bool, 1)
    go worker(done)
    
    <-done // 等待 worker 完成
}
```

## Channel 模式

### Fan-out/Fan-in

```go
// Fan-out：一个输入分发给多个 worker
func fanOut(input <-chan int, workers int) []<-chan int {
    channels := make([]<-chan int, workers)
    for i := 0; i < workers; i++ {
        channels[i] = worker(input)
    }
    return channels
}

// Fan-in：多个输入合并为一个输出
func fanIn(channels ...<-chan int) <-chan int {
    var wg sync.WaitGroup
    merged := make(chan int)
    
    for _, ch := range channels {
        wg.Add(1)
        go func(c <-chan int) {
            defer wg.Done()
            for val := range c {
                merged <- val
            }
        }(ch)
    }
    
    go func() {
        wg.Wait()
        close(merged)
    }()
    
    return merged
}
```

### Pipeline

```go
// 阶段1：生成数据
func generate(nums ...int) <-chan int {
    out := make(chan int)
    go func() {
        for _, n := range nums {
            out <- n
        }
        close(out)
    }()
    return out
}

// 阶段2：处理数据
func square(in <-chan int) <-chan int {
    out := make(chan int)
    go func() {
        for n := range in {
            out <- n * n
        }
        close(out)
    }()
    return out
}

// 阶段3：过滤数据
func filter(in <-chan int, predicate func(int) bool) <-chan int {
    out := make(chan int)
    go func() {
        for n := range in {
            if predicate(n) {
                out <- n
            }
        }
        close(out)
    }()
    return out
}

func main() {
    // 构建 pipeline
    nums := generate(1, 2, 3, 4, 5, 6, 7, 8, 9, 10)
    squares := square(nums)
    evens := filter(squares, func(n int) bool { return n%2 == 0 })
    
    for val := range evens {
        fmt.Println(val)
    }
}
```

### Worker Pool

```go
func workerPool(jobs <-chan int, results chan<- int, id int) {
    for job := range jobs {
        fmt.Printf("Worker %d processing job %d\n", id, job)
        time.Sleep(time.Second)
        results <- job * 2
    }
}

func main() {
    jobs := make(chan int, 100)
    results := make(chan int, 100)
    
    // 启动 worker pool
    for w := 1; w <= 3; w++ {
        go workerPool(jobs, results, w)
    }
    
    // 发送任务
    for j := 1; j <= 9; j++ {
        jobs <- j
    }
    close(jobs)
    
    // 收集结果
    for a := 1; a <= 9; a++ {
        fmt.Println("Result:", <-results)
    }
}
```

## Channel 关闭

### 关闭规则

```go
// 规则1：只有发送方应该关闭 channel
// 规则2：关闭已关闭的 channel 会 panic
// 规则3：向已关闭的 channel 发送会 panic
// 规则4：从已关闭的 channel 接收会返回零值

func main() {
    ch := make(chan int, 5)
    
    // 发送数据
    go func() {
        for i := 0; i < 5; i++ {
            ch <- i
        }
        close(ch) // 发送完毕后关闭
    }()
    
    // 接收数据，直到 channel 关闭
    for val := range ch {
        fmt.Println(val)
    }
}
```

### 检测 channel 关闭

```go
func main() {
    ch := make(chan int)
    close(ch)
    
    // 方式1：使用 ok 模式
    val, ok := <-ch
    if !ok {
        fmt.Println("Channel closed")
    }
    
    // 方式2：使用 range
    for val := range ch {
        fmt.Println(val) // 不会执行
    }
}
```

## 并发原语

### sync.WaitGroup

```go
func main() {
    var wg sync.WaitGroup
    
    for i := 1; i <= 5; i++ {
        wg.Add(1)
        go func(id int) {
            defer wg.Done()
            fmt.Printf("Worker %d starting\n", id)
            time.Sleep(time.Second)
            fmt.Printf("Worker %d done\n", id)
        }(i)
    }
    
    wg.Wait() // 等待所有 worker 完成
    fmt.Println("All workers done")
}
```

### sync.Mutex

```go
type SafeCounter struct {
    mu sync.Mutex
    v  map[string]int
}

func (c *SafeCounter) Inc(key string) {
    c.mu.Lock()
    defer c.mu.Unlock()
    c.v[key]++
}

func (c *SafeCounter) Value(key string) int {
    c.mu.Lock()
    defer c.mu.Unlock()
    return c.v[key]
}
```

### sync.Once

```go
var once sync.Once
var config *Config

func GetConfig() *Config {
    once.Do(func() {
        config = loadConfig()
    })
    return config
}
```

### sync.Pool

```go
var pool = sync.Pool{
    New: func() interface{} {
        return make([]byte, 1024)
    },
}

func main() {
    // 获取对象
    buf := pool.Get().([]byte)
    
    // 使用对象
    copy(buf, "Hello")
    
    // 归还对象
    pool.Put(buf)
}
```

## Context

### Context 基础

```go
func worker(ctx context.Context, id int) {
    for {
        select {
        case <-ctx.Done():
            fmt.Printf("Worker %d: context cancelled\n", id)
            return
        default:
            fmt.Printf("Worker %d: working\n", id)
            time.Sleep(time.Second)
        }
    }
}

func main() {
    ctx, cancel := context.WithTimeout(context.Background(), 3*time.Second)
    defer cancel()
    
    go worker(ctx, 1)
    go worker(ctx, 2)
    
    <-ctx.Done()
    fmt.Println("Main: context done")
}
```

### Context 类型

```go
// Background context
ctx := context.Background()

// WithCancel
ctx, cancel := context.WithCancel(parentCtx)

// WithTimeout
ctx, cancel := context.WithTimeout(parentCtx, 5*time.Second)

// WithDeadline
ctx, cancel := context.WithDeadline(parentCtx, time.Now().Add(5*time.Second))

// WithValue
ctx = context.WithValue(ctx, key, value)
```

### Context 最佳实践

```go
// context 应作为第一个参数
func DoSomething(ctx context.Context, arg string) error {
    // 使用 context
    select {
    case <-ctx.Done():
        return ctx.Err()
    default:
        // 继续执行
    }
    
    // 调用其他函数时传递 context
    return doMore(ctx, arg)
}
```

## 并发错误处理

### 错误传播

```go
type Result struct {
    Value interface{}
    Err   error
}

func worker(ctx context.Context, id int) Result {
    select {
    case <-ctx.Done():
        return Result{Err: ctx.Err()}
    default:
        if id == 3 {
            return Result{Err: fmt.Errorf("worker %d failed", id)}
        }
        return Result{Value: id * 2}
    }
}

func main() {
    ctx := context.Background()
    results := make(chan Result, 5)
    
    for i := 1; i <= 5; i++ {
        go func(id int) {
            results <- worker(ctx, id)
        }(i)
    }
    
    for i := 0; i < 5; i++ {
        result := <-results
        if result.Err != nil {
            fmt.Println("Error:", result.Err)
        } else {
            fmt.Println("Result:", result.Value)
        }
    }
}
```

## 性能优化

### 避免 goroutine 泄漏

```go
// 使用 context 控制生命周期
func controlledGoroutine(ctx context.Context) {
    for {
        select {
        case <-ctx.Done():
            return
        case <-time.After(time.Second):
            // 工作
        }
    }
}
```

### Channel 缓冲区大小

```go
// 根据预期吞吐量设置缓冲区
ch := make(chan int, runtime.NumCPU())

// 或使用动态缓冲区
func dynamicBuffer() chan int {
    ch := make(chan int, 0)
    // 根据负载动态调整
    return ch
}
```

### 减少锁竞争

```go
// 使用分片锁
type ShardedMap struct {
    shards [256]struct {
        mu sync.RWMutex
        m  map[string]interface{}
    }
}

func (s *ShardedMap) getShard(key string) int {
    h := fnv.New32a()
    h.Write([]byte(key))
    return int(h.Sum32() % 256)
}
```

## 调试并发代码

### Race Detector

```bash
# 启用竞态检测
go run -race main.go
go test -race ./...
```

### 常见并发问题

- **竞态条件**：多个 goroutine 访问共享数据
- **死锁**：所有 goroutine 都在等待
- **活锁**：goroutine 在重复相同操作
- **goroutine 泄漏**：goroutine 无法退出

## 相关链接

- [[GoConcurrencyPatterns]] - Go 并发模式
- [[GoMicroservices]] - Go 微服务
