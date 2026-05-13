# Kotlin 协程详解

## 协程基础

```kotlin
import kotlinx.coroutines.*

// runBlocking: 阻塞当前线程等待协程完成（桥接非协程世界）
fun main() = runBlocking {
    launch {                     // 启动一个协程，不阻塞
        delay(1000L)
        println("World!")
    }
    println("Hello,")            // 先打印 Hello,
    delay(2000L)                 // 等待协程完成
}

// async/await: 并发执行并返回结果
suspend fun fetchData1(): String { delay(1000L); return "Data1" }
suspend fun fetchData2(): String { delay(1000L); return "Data2" }

fun main() = runBlocking {
    val result1 = async { fetchData1() }
    val result2 = async { fetchData2() }
    println("${result1.await()} + ${result2.await()}")  // 约 1 秒完成
}
```

## 挂起函数

```kotlin
// suspend 关键字标记可挂起的函数
suspend fun doWork(): String {
    delay(1000L)                // 挂起但不阻塞线程
    return "Done"
}

// 只能在协程或其他挂起函数中调用
fun main() = runBlocking {
    val result = doWork()
    println(result)
}
```

## 协程上下文与调度器

```kotlin
fun main() = runBlocking {
    // Dispatchers.Default: CPU 密集型任务
    launch(Dispatchers.Default) {
        // 大数据处理、排序等
    }

    // Dispatchers.IO: IO 密集型任务
    launch(Dispatchers.IO) {
        // 文件读写、网络请求
    }

    // Dispatchers.Main: UI 线程（仅在 Android 等平台可用）
    launch(Dispatchers.Main) {
        // 更新 UI
    }

    // Dispatchers.Unconfined: 不限制特定线程
    launch(Dispatchers.Unconfined) {
        // 最初在调用者线程，但挂起后可能恢复在其他线程
    }

    // 自定义线程池
    val myDispatcher = Executors.newFixedThreadPool(4).asCoroutineDispatcher()
    launch(myDispatcher) { /* ... */ }
    myDispatcher.close()  // 必须关闭
}
```

## 结构化并发

```kotlin
// coroutineScope: 等待所有子协程完成，失败时取消所有子协程
suspend fun fetchDocs() = coroutineScope {
    val doc1 = async { fetchDocument(1) }
    val doc2 = async { fetchDocument(2) }
    doc1.await() + doc2.await()
}

// supervisorScope: 子协程失败不影响其他子协程
suspend fun fetchUsers() = supervisorScope {
    val child1 = launch {
        try {
            delay(Long.MAX_VALUE)
        } catch (e: CancellationException) {
            println("child1 cancelled")
        }
    }
    val child2 = launch {
        delay(100)
        throw RuntimeException("child2 failed")
    }
    // child1 继续运行
}
```

## Job 和 Deferred

```kotlin
fun main() = runBlocking {
    // Job: 协程的句柄
    val job: Job = launch {
        delay(1000L)
        println("Job done")
    }
    job.join()  // 等待完成

    // 取消协程
    val cancellable = launch {
        repeat(1000) { i ->
            if (!isActive) return@launch  // 检查取消状态
            delay(500L)
            println("Working $i")
        }
    }
    delay(2000L)
    cancellable.cancel()       // 取消协程
    cancellable.join()         // 等待完成

    // Deferred: 有返回值的 Job
    val deferred: Deferred<String> = async {
        delay(1000L)
        "Result"
    }
    println(deferred.await())
}
```

## 协程取消与超时

```kotlin
fun main() = runBlocking {
    // 超时
    try {
        withTimeout(1300L) {
            repeat(1000) { i ->
                println("Working $i")
                delay(500L)
            }
        }
    } catch (e: TimeoutCancellationException) {
        println("Timed out")
    }

    // 超时不抛异常
    val result = withTimeoutOrNull(1300L) {
        repeat(1000) { i ->
            println("Working $i")
            delay(500L)
        }
        "Done"
    }
    println("Result: $result")  // null

    // 不可取消的代码块
    launch {
        withContext(NonCancellable) {
            // 即使协程被取消，这段代码也会执行完毕
            delay(1000L)
            println("Cleanup done")
        }
    }
}
```

## Channel

```kotlin
fun main() = runBlocking {
    // 通道：协程间通信
    val channel = Channel<Int>()

    launch {
        for (x in 1..5) {
            delay(100)
            channel.send(x * x)
        }
        channel.close()  // 关闭通道
    }

    // 接收
    for (y in channel) {
        println(y)
    }

    // produce/consume 模式
    val squares = produce {
        for (x in 1..5) send(x * x)
    }
    squares.consumeEach { println(it) }
}
```

## Flow（冷流）

```kotlin
import kotlinx.coroutines.flow.*

// 构建 Flow
fun simpleFlow(): Flow<Int> = flow {
    for (i in 1..3) {
        delay(100)
        emit(i)  // 发射元素
    }
}

fun main() = runBlocking {
    // 收集 Flow
    simpleFlow().collect { value ->
        println("Received $value")
    }

    // 操作符
    flowOf(1, 2, 3, 4, 5)
        .filter { it % 2 == 0 }
        .map { it * it }
        .catch { e -> println("Error: $e") }
        .collect { println(it) }

    // 终端操作符
    val first = flowOf(1, 2, 3).first()           // 1
    val single = flowOf(1).single()               // 1
    val list = flowOf(1, 2, 3).toList()           // [1, 2, 3]
    val count = flowOf(1, 2, 3).count()           // 3
    val reduced = flowOf(1, 2, 3).reduce { a, b -> a + b }  // 6
}

// StateFlow: 有状态的热流，始终有值
class MyViewModel {
    private val _state = MutableStateFlow("Initial")
    val state: StateFlow<String> = _state.asStateFlow()

    fun updateState(value: String) {
        _state.value = value
    }
}

// SharedFlow: 无状态的熱流，可配置重放
val sharedFlow = MutableSharedFlow<Int>(replay = 3)
```

## 异常处理

```kotlin
fun main() = runBlocking {
    // 全局异常处理
    val handler = CoroutineExceptionHandler { _, exception ->
        println("Caught: $exception")
    }

    val job = GlobalScope.launch(handler) {
        throw RuntimeException("Oops!")
    }
    job.join()

    // try/catch 在协程中
    val deferred = GlobalScope.async {
        throw RuntimeException("Failed")
    }
    try {
        deferred.await()
    } catch (e: Exception) {
        println("Handled: $e")
    }

    // supervisorScope 防止异常传播
    supervisorScope {
        val child = launch {
            throw RuntimeException("Child failed")
        }
        // 其他子协程不受影响
    }
}
```

## 协程 vs 线程

| 特性 | 协程 | 线程 |
|------|------|------|
| 调度 | 用户态调度（协作式） | 内核态调度（抢占式） |
| 创建成本 | 极低（内存中创建） | 较高（需要系统调用） |
| 上下文切换 | 只需保存少量寄存器 | 完整上下文切换 |
| 数量限制 | 可创建数十万 | 通常数千 |
| 阻塞 | 挂起不阻塞线程 | 阻塞系统线程 |
| 通信 | Channel/Flow 安全 | 需要锁/原子操作 |
| 调试 | 栈信息较浅 | 完整调用栈 |
