---
aliases:
  - Go并发模式
  - Go Concurrency Patterns
  - Fan-in
  - Fan-out
  - Pipeline
tags:
  - Go
  - 并发模式
  - Pipeline
  - Context
  - 计算机科学
created: 2026-06-27
updated: 2026-06-27
---

# Go并发模式

Go 的并发模型基于 CSP（Communicating Sequential Processes），通过 goroutine 和 channel 实现优雅的并发模式。本文介绍常见的并发模式和最佳实践。

## Pipeline 模式

### 基本 Pipeline

Pipeline 将数据处理分为多个阶段，每个阶段是独立的 goroutine：

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

// 阶段2：平方
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

// 阶段3：过滤
func filter(in <-chan int, fn func(int) bool) <-chan int {
    out := make(chan int)
    go func() {
        for n := range in {
            if fn(n) {
                out <- n
            }
        }
        close(out)
    }()
    return out
}

func main() {
    // 构建 pipeline
    nums := generate(1, 2, 3, 4, 5)
    squares := square(nums)
    evens := filter(squares, func(n int) bool {
        return n%2 == 0
    })
    
    // 消费结果
    for val := range evens {
        fmt.Println(val) // 4, 16, 36, 64, 100
    }
}
```

### 带错误处理的 Pipeline

```go
type Result struct {
    Value int
    Err   error
}

func process(in <-chan int) <-chan Result {
    out := make(chan Result)
    go func() {
        for n := range in {
            if n < 0 {
                out <- Result{Err: fmt.Errorf("negative number: %d", n)}
                continue
            }
            out <- Result{Value: n * n}
        }
        close(out)
    }()
    return out
}

func main() {
    nums := generate(1, -2, 3, -4, 5)
    results := process(nums)
    
    for result := range results {
        if result.Err != nil {
            fmt.Println("Error:", result.Err)
            continue
        }
        fmt.Println("Result:", result.Value)
    }
}
```

### 可取消的 Pipeline

```go
func generateWithCancel(ctx context.Context, nums ...int) <-chan int {
    out := make(chan int)
    go func() {
        defer close(out)
        for _, n := range nums {
            select {
            case out <- n:
            case <-ctx.Done():
                return
            }
        }
    }()
    return out
}

func squareWithCancel(ctx context.Context, in <-chan int) <-chan int {
    out := make(chan int)
    go func() {
        defer close(out)
        for n := range in {
            select {
            case out <- n * n:
            case <-ctx.Done():
                return
            }
        }
    }()
    return out
}

func main() {
    ctx, cancel := context.WithTimeout(context.Background(), 100*time.Millisecond)
    defer cancel()
    
    nums := generateWithCancel(ctx, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10)
    squares := squareWithCancel(ctx, nums)
    
    for val := range squares {
        fmt.Println(val)
    }
}
```

## Fan-out/Fan-in 模式

### Fan-out

Fan-out 将工作分发给多个 goroutine 并行处理：

```go
func fanOut(input <-chan int, workers int) []<-chan int {
    channels := make([]<-chan int, workers)
    for i := 0; i < workers; i++ {
        channels[i] = worker(input)
    }
    return channels
}

func worker(input <-chan int) <-chan int {
    out := make(chan int)
    go func() {
        defer close(out)
        for n := range input {
            // 模拟耗时处理
            time.Sleep(100 * time.Millisecond)
            out <- n * n
        }
    }()
    return out
}
```

### Fan-in

Fan-in 将多个 channel 合并为一个：

```go
func fanIn(channels ...<-chan int) <-chan int {
    var wg sync.WaitGroup
    merged := make(chan int)
    
    // 为每个输入 channel 启动一个 goroutine
    for _, ch := range channels {
        wg.Add(1)
        go func(c <-chan int) {
            defer wg.Done()
            for val := range c {
                merged <- val
            }
        }(ch)
    }
    
    // 等待所有输入完成后关闭 merged
    go func() {
        wg.Wait()
        close(merged)
    }()
    
    return merged
}

func main() {
    input := generate(1, 2, 3, 4, 5, 6, 7, 8, 9, 10)
    
    // Fan-out: 分发给 3 个 worker
    workers := fanOut(input, 3)
    
    // Fan-in: 合并结果
    results := fanIn(workers...)
    
    for val := range results {
        fmt.Println(val)
    }
}
```

### 带负载均衡的 Fan-out

```go
func balancedFanOut(input <-chan int, workers int) <-chan int {
    // 使用 channel 数组实现负载均衡
    channels := make([]chan int, workers)
    for i := range channels {
        channels[i] = make(chan int)
        go worker(channels[i])
    }
    
    // 轮询分发任务
    out := make(chan int)
    go func() {
        defer close(out)
        i := 0
        for val := range input {
            channels[i%workers] <- val
            i++
        }
        for _, ch := range channels {
            close(ch)
        }
    }()
    
    // 合并结果
    return merge(channels...)
}
```

## Context 模式

### 超时控制

```go
func longRunningTask(ctx context.Context) (string, error) {
    // 模拟长时间运行的任务
    select {
    case <-time.After(5 * time.Second):
        return "completed", nil
    case <-ctx.Done():
        return "", ctx.Err()
    }
}

func main() {
    ctx, cancel := context.WithTimeout(context.Background(), 2*time.Second)
    defer cancel()
    
    result, err := longRunningTask(ctx)
    if err != nil {
        fmt.Println("Error:", err) // Error: context deadline exceeded
        return
    }
    fmt.Println("Result:", result)
}
```

### 取消传播

```go
func parentTask(ctx context.Context) {
    ctx, cancel := context.WithCancel(ctx)
    defer cancel()
    
    // 启动子任务
    go childTask(ctx, "child1")
    go childTask(ctx, "child2")
    
    // 模拟父任务完成
    time.Sleep(2 * time.Second)
    cancel() // 取消所有子任务
    
    time.Sleep(100 * time.Millisecond)
}

func childTask(ctx context.Context, name string) {
    for {
        select {
        case <-ctx.Done():
            fmt.Printf("%s: cancelled\n", name)
            return
        case <-time.After(500 * time.Millisecond):
            fmt.Printf("%s: working\n", name)
        }
    }
}
```

### 值传递

```go
type contextKey string

const (
    requestIDKey contextKey = "requestID"
    userIDKey    contextKey = "userID"
)

func middleware(next http.Handler) http.Handler {
    return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        ctx := context.WithValue(r.Context(), requestIDKey, generateRequestID())
        next.ServeHTTP(w, r.WithContext(ctx))
    })
}

func handler(w http.ResponseWriter, r *http.Request) {
    requestID := r.Context().Value(requestIDKey).(string)
    fmt.Fprintf(w, "Request ID: %s", requestID)
}
```

## 同步模式

### 信号量模式

```go
type Semaphore struct {
    ch chan struct{}
}

func NewSemaphore(n int) *Semaphore {
    return &Semaphore{ch: make(chan struct{}, n)}
}

func (s *Semaphore) Acquire() {
    s.ch <- struct{}{}
}

func (s *Semaphore) Release() {
    <-s.ch
}

func main() {
    sem := NewSemaphore(3) // 最多 3 个并发
    var wg sync.WaitGroup
    
    for i := 0; i < 10; i++ {
        wg.Add(1)
        go func(id int) {
            defer wg.Done()
            sem.Acquire()
            defer sem.Release()
            
            fmt.Printf("Worker %d acquired semaphore\n", id)
            time.Sleep(time.Second)
            fmt.Printf("Worker %d released semaphore\n", id)
        }(i)
    }
    
    wg.Wait()
}
```

### Barrier 模式

```go
type Barrier struct {
    n      int
    count  int
    mu     sync.Mutex
    cond   *sync.Cond
}

func NewBarrier(n int) *Barrier {
    b := &Barrier{n: n}
    b.cond = sync.NewCond(&b.mu)
    return b
}

func (b *Barrier) Wait() {
    b.mu.Lock()
    b.count++
    if b.count == b.n {
        b.count = 0
        b.cond.Broadcast()
    } else {
        b.cond.Wait()
    }
    b.mu.Unlock()
}

func main() {
    barrier := NewBarrier(3)
    var wg sync.WaitGroup
    
    for i := 0; i < 3; i++ {
        wg.Add(1)
        go func(id int) {
            defer wg.Done()
            fmt.Printf("Worker %d: before barrier\n", id)
            time.Sleep(time.Duration(rand.Intn(1000)) * time.Millisecond)
            barrier.Wait()
            fmt.Printf("Worker %d: after barrier\n", id)
        }(i)
    }
    
    wg.Wait()
}
```

### Once 模式

```go
var (
    once     sync.Once
    instance *Singleton
)

type Singleton struct {
    data string
}

func GetInstance() *Singleton {
    once.Do(func() {
        instance = &Singleton{data: "initialized"}
    })
    return instance
}

func main() {
    // 多次调用只初始化一次
    s1 := GetInstance()
    s2 := GetInstance()
    fmt.Println(s1 == s2) // true
}
```

## 生产者-消费者模式

### 基本模式

```go
func producer(ch chan<- int, id int) {
    for i := 0; i < 5; i++ {
        ch <- id*10 + i
        time.Sleep(100 * time.Millisecond)
    }
}

func consumer(ch <-chan int, id int) {
    for val := range ch {
        fmt.Printf("Consumer %d: %d\n", id, val)
        time.Sleep(200 * time.Millisecond)
    }
}

func main() {
    ch := make(chan int, 10)
    var wg sync.WaitGroup
    
    // 启动 2 个生产者
    for i := 0; i < 2; i++ {
        wg.Add(1)
        go func(id int) {
            defer wg.Done()
            producer(ch, id)
        }(i)
    }
    
    // 启动 3 个消费者
    for i := 0; i < 3; i++ {
        wg.Add(1)
        go func(id int) {
            defer wg.Done()
            consumer(ch, id)
        }(i)
    }
    
    // 等待生产者完成
    go func() {
        wg.Wait()
        close(ch)
    }()
    
    time.Sleep(3 * time.Second)
}
```

### 带确认的生产者-消费者

```go
type Message struct {
    ID      int
    Data    string
    ReplyCh chan error
}

func producer(ch chan<- Message) {
    for i := 0; i < 5; i++ {
        reply := make(chan error)
        ch <- Message{ID: i, Data: fmt.Sprintf("msg-%d", i), ReplyCh: reply}
        
        // 等待确认
        if err := <-reply; err != nil {
            fmt.Printf("Producer: message %d failed: %v\n", i, err)
        } else {
            fmt.Printf("Producer: message %d acknowledged\n", i)
        }
    }
}

func consumer(ch <-chan Message) {
    for msg := range ch {
        fmt.Printf("Consumer: processing %d\n", msg.ID)
        // 处理消息
        msg.ReplyCh <- nil // 发送确认
    }
}
```

## 错误处理模式

### 错误组模式

```go
type ErrorGroup struct {
    errs []error
    mu   sync.Mutex
    wg   sync.WaitGroup
}

func (eg *ErrorGroup) Go(fn func() error) {
    eg.wg.Add(1)
    go func() {
        defer eg.wg.Done()
        if err := fn(); err != nil {
            eg.mu.Lock()
            eg.errs = append(eg.errs, err)
            eg.mu.Unlock()
        }
    }()
}

func (eg *ErrorGroup) Wait() []error {
    eg.wg.Wait()
    return eg.errs
}

func main() {
    eg := &ErrorGroup{}
    
    for i := 0; i < 5; i++ {
        i := i
        eg.Go(func() error {
            if i == 3 {
                return fmt.Errorf("task %d failed", i)
            }
            return nil
        })
    }
    
    errs := eg.Wait()
    if len(errs) > 0 {
        fmt.Println("Errors:", errs)
    }
}
```

### 限制并发的错误组

```go
type LimitedErrorGroup struct {
    sem chan struct{}
    err error
    mu  sync.Mutex
    wg  sync.WaitGroup
}

func NewLimitedErrorGroup(limit int) *LimitedErrorGroup {
    return &LimitedErrorGroup{sem: make(chan struct{}, limit)}
}

func (g *LimitedErrorGroup) Go(fn func() error) {
    g.wg.Add(1)
    go func() {
        defer g.wg.Done()
        
        g.sem <- struct{}{}        // 获取信号量
        defer func() { <-g.sem }() // 释放信号量
        
        if err := fn(); err != nil {
            g.mu.Lock()
            if g.err == nil {
                g.err = err
            }
            g.mu.Unlock()
        }
    }()
}

func (g *LimitedErrorGroup) Wait() error {
    g.wg.Wait()
    return g.err
}
```

## 并发安全数据结构

### 并发 Map

```go
type ConcurrentMap struct {
    mu    sync.RWMutex
    items map[string]interface{}
}

func NewConcurrentMap() *ConcurrentMap {
    return &ConcurrentMap{items: make(map[string]interface{})}
}

func (m *ConcurrentMap) Set(key string, value interface{}) {
    m.mu.Lock()
    defer m.mu.Unlock()
    m.items[key] = value
}

func (m *ConcurrentMap) Get(key string) (interface{}, bool) {
    m.mu.RLock()
    defer m.mu.RUnlock()
    val, ok := m.items[key]
    return val, ok
}

func (m *ConcurrentMap) Delete(key string) {
    m.mu.Lock()
    defer m.mu.Unlock()
    delete(m.items, key)
}
```

### 分片 Map

```go
type ShardedMap struct {
    shards [256]*Shard
}

type Shard struct {
    mu    sync.RWMutex
    items map[string]interface{}
}

func NewShardedMap() *ShardedMap {
    sm := &ShardedMap{}
    for i := range sm.shards {
        sm.shards[i] = &Shard{items: make(map[string]interface{})}
    }
    return sm
}

func (sm *ShardedMap) getShard(key string) *Shard {
    hash := fnv.New32a()
    hash.Write([]byte(key))
    return sm.shards[hash.Sum32()%256]
}

func (sm *ShardedMap) Set(key string, value interface{}) {
    shard := sm.getShard(key)
    shard.mu.Lock()
    defer shard.mu.Unlock()
    shard.items[key] = value
}
```

### 无锁队列

```go
type LockFreeQueue struct {
    head unsafe.Pointer
    tail unsafe.Pointer
}

type node struct {
    value interface{}
    next  unsafe.Pointer
}

func NewLockFreeQueue() *LockFreeQueue {
    n := &node{}
    return &LockFreeQueue{
        head: unsafe.Pointer(n),
        tail: unsafe.Pointer(n),
    }
}

func (q *LockFreeQueue) Push(value interface{}) {
    n := &node{value: value}
    for {
        tail := atomic.LoadPointer(&q.tail)
        next := atomic.LoadPointer(&(*node)(tail).next)
        if tail == atomic.LoadPointer(&q.tail) {
            if next == nil {
                if atomic.CompareAndSwapPointer(&(*node)(tail).next, next, unsafe.Pointer(n)) {
                    atomic.CompareAndSwapPointer(&q.tail, tail, unsafe.Pointer(n))
                    return
                }
            }
        }
    }
}
```

## 最佳实践

### 并发设计原则

1. **通过通信共享内存**：优先使用 channel 而非共享内存
2. **最小化临界区**：尽量减少锁的持有时间
3. **避免过度并发**：合理控制 goroutine 数量
4. **优雅退出**：使用 context 控制 goroutine 生命周期

### 性能优化

1. **使用 buffered channel**：减少阻塞
2. **避免 goroutine 泄漏**：确保 goroutine 能够退出
3. **合理使用 sync.Pool**：复用对象
4. **使用 atomic 操作**：简单场景使用原子操作替代锁

### 调试技巧

```bash
# 竞态检测
go run -race main.go

# pprof 分析
go tool pprof http://localhost:6060/debug/pprof/goroutine

# trace 分析
go tool trace trace.out
```

## 相关链接

- [[GoroutineAndChannel]] - Goroutine 与 Channel
- [[GoMicroservices]] - Go 微服务
