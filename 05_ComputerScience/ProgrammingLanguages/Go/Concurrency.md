# Go 并发编程

## Goroutine

```go
package main

import (
    "fmt"
    "time"
)

func say(s string) {
    for i := 0; i < 5; i++ {
        time.Sleep(100 * time.Millisecond)
        fmt.Println(s)
    }
}

func main() {
    go say("world")  // 启动 goroutine
    say("hello")     // 在主 goroutine 中运行
}

// goroutine 是轻量级线程
// M:N 调度模型：M 个 goroutine 多路复用到 N 个 OS 线程
// 栈空间初始仅 2KB，可动态增长（最大 1GB）
// 创建数十万 goroutine 是可行的
```

## Channel

```go
// 无缓冲 channel（同步通信）
func main() {
    ch := make(chan string)  // 无缓冲

    go func() {
        msg := <-ch   // 接收（阻塞直到有数据）
        fmt.Println("收到:", msg)
    }()

    ch <- "ping"  // 发送（阻塞直到被接收）
    time.Sleep(time.Second)
}

// 有缓冲 channel（异步通信）
func main() {
    ch := make(chan int, 3)  // 缓冲大小 3
    ch <- 1
    ch <- 2
    ch <- 3
    // ch <- 4  // 阻塞：缓冲区已满

    fmt.Println(<-ch)  // 1
    fmt.Println(<-ch)  // 2
    fmt.Println(<-ch)  // 3
}

// 方向 channel
func producer(ch chan<- int) {  // 只能发送
    for i := 0; i < 5; i++ {
        ch <- i
    }
    close(ch)
}

func consumer(ch <-chan int) {  // 只能接收
    for val := range ch {
        fmt.Println("消费:", val)
    }
}

// range 遍历 channel
func main() {
    ch := make(chan int)
    go func() {
        for i := 0; i < 5; i++ {
            ch <- i
        }
        close(ch)  // 必须关闭，否则 range 死锁
    }()
    for val := range ch {
        fmt.Println(val)
    }
}

// select 多路复用
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

    select {
    case msg1 := <-ch1:
        fmt.Println("从 ch1 收到:", msg1)
    case msg2 := <-ch2:
        fmt.Println("从 ch2 收到:", msg2)
    case <-time.After(3 * time.Second):
        fmt.Println("超时")
    default:
        fmt.Println("非阻塞，无数据")
    }
}

// select 超时模式
func main() {
    ch := make(chan int)
    select {
    case v := <-ch:
        fmt.Println(v)
    case <-time.After(1 * time.Second):
        fmt.Println("超时")
    }
}
```

## sync 同步原语

```go
// WaitGroup
func main() {
    var wg sync.WaitGroup

    for i := 1; i <= 5; i++ {
        wg.Add(1)  // 计数器 +1
        go func(id int) {
            defer wg.Done()  // 计数器 -1
            fmt.Printf("Worker %d 开始\n", id)
            time.Sleep(time.Second)
            fmt.Printf("Worker %d 结束\n", id)
        }(i)
    }

    wg.Wait()  // 等待所有 worker 完成
    fmt.Println("所有 worker 完成")
}

// Mutex
type Counter struct {
    mu    sync.Mutex
    value int
}

func (c *Counter) Increment() {
    c.mu.Lock()
    defer c.mu.Unlock()
    c.value++
}

func (c *Counter) Value() int {
    c.mu.Lock()
    defer c.mu.Unlock()
    return c.value
}

// RWMutex（读写锁）
type Cache struct {
    mu    sync.RWMutex
    data  map[string]string
}

func (c *Cache) Get(key string) string {
    c.mu.RLock()   // 读锁：可并发读
    defer c.mu.RUnlock()
    return c.data[key]
}

func (c *Cache) Set(key, value string) {
    c.mu.Lock()    // 写锁：独占
    defer c.mu.Unlock()
    c.data[key] = value
}

// Once（只执行一次）
var once sync.Once
var instance *Singleton

func GetInstance() *Singleton {
    once.Do(func() {
        instance = &Singleton{}
    })
    return instance
}

// Cond（条件变量）
func main() {
    var mu sync.Mutex
    cond := sync.NewCond(&mu)
    ready := false

    go func() {
        time.Sleep(time.Second)
        mu.Lock()
        ready = true
        cond.Signal()  // 唤醒一个等待者
        mu.Unlock()
    }()

    mu.Lock()
    for !ready {
        cond.Wait()  // 等待条件满足
    }
    mu.Unlock()
    fmt.Println("就绪")
}

// Pool（对象池）
var pool = sync.Pool{
    New: func() interface{} {
        return make([]byte, 1024)
    },
}

func process() {
    buf := pool.Get().([]byte)
    defer pool.Put(buf)
    // 使用 buf
}

// Map（并发安全的 map）
var m sync.Map

func main() {
    m.Store("key", "value")
    val, ok := m.Load("key")
    m.Delete("key")
    m.Range(func(key, value interface{}) bool {
        fmt.Println(key, value)
        return true  // 继续遍历
    })
}
```

## Worker Pool 模式

```go
func worker(id int, jobs <-chan int, results chan<- int) {
    for job := range jobs {
        fmt.Printf("Worker %d 处理任务 %d\n", id, job)
        time.Sleep(time.Second)
        results <- job * 2
    }
}

func main() {
    const numJobs = 10
    jobs := make(chan int, numJobs)
    results := make(chan int, numJobs)

    // 启动 3 个 worker
    for w := 1; w <= 3; w++ {
        go worker(w, jobs, results)
    }

    // 发送任务
    for j := 1; j <= numJobs; j++ {
        jobs <- j
    }
    close(jobs)

    // 收集结果
    for a := 1; a <= numJobs; a++ {
        <-results
    }
}
```

## Pipeline 模式

```go
func gen(nums ...int) <-chan int {
    out := make(chan int)
    go func() {
        for _, n := range nums {
            out <- n
        }
        close(out)
    }()
    return out
}

func sq(in <-chan int) <-chan int {
    out := make(chan int)
    go func() {
        for n := range in {
            out <- n * n
        }
        close(out)
    }()
    return out
}

func main() {
    // 构建 pipeline
    c := gen(2, 3, 4)
    out := sq(c)

    // 消费
    fmt.Println(<-out)  // 4
    fmt.Println(<-out)  // 9
    fmt.Println(<-out)  // 16
}
```

## Context 包

```go
// 取消传播
func main() {
    ctx, cancel := context.WithCancel(context.Background())
    defer cancel()

    go func() {
        time.Sleep(2 * time.Second)
        cancel()  // 取消 context
    }()

    select {
    case <-ctx.Done():
        fmt.Println("取消:", ctx.Err())
    }
}

// 超时
func main() {
    ctx, cancel := context.WithTimeout(context.Background(), 1*time.Second)
    defer cancel()

    select {
    case <-time.After(2 * time.Second):
        fmt.Println("太晚了")
    case <-ctx.Done():
        fmt.Println("超时:", ctx.Err())
    }
}

// 传递值
func main() {
    ctx := context.WithValue(context.Background(), "userID", 42)
    processRequest(ctx)
}

func processRequest(ctx context.Context) {
    if userID := ctx.Value("userID"); userID != nil {
        fmt.Println("用户 ID:", userID)
    }
}

// context 在 HTTP 中的应用
func fetch(ctx context.Context, url string) (*http.Response, error) {
    req, err := http.NewRequestWithContext(ctx, "GET", url, nil)
    if err != nil {
        return nil, err
    }
    return http.DefaultClient.Do(req)
}
```

## 竞态检测

```go
// go run -race main.go
// 编译时加入 -race 标志：go build -race

func main() {
    var counter int
    var wg sync.WaitGroup

    for i := 0; i < 1000; i++ {
        wg.Add(1)
        go func() {
            defer wg.Done()
            counter++  // 数据竞态！
        }()
    }
    wg.Wait()
    fmt.Println(counter)
}
```

## Goroutine vs 线程对比

| 特性 | Goroutine | OS 线程 |
|------|-----------|---------|
| 创建成本 | ~4KB 栈 | ~1MB 栈 |
| 调度 | Go 运行时（M:N） | OS 内核调度 |
| 上下文切换 | ~100ns | ~1μs |
| 栈管理 | 动态增长 | 固定大小 |
| 通信方式 | Channel（CSP） | 共享内存+锁 |
| 标识符 | 无内置 ID | 有线程 ID |
| 调度点 | channel/syscall/函数调用 | 时间片/抢占 |
