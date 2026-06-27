---
aliases: [KotlinBasics]
tags: ['05_ComputerScience', 'ProgrammingLanguages', 'Kotlin']
created: 2026-05-17
updated: 2026-05-13
---

# Kotlin 基础

Kotlin 是一种运行在 JVM 上的静态类型编程语言，由 JetBrains 开发，2017 年被 Google 宣布为 Android 官方开发语言。Kotlin 融合了面向对象和函数式编程范式，设计目标是简洁、安全、互操作。

## 语言特性对比

| 特性 | Kotlin | Java | 说明 |
|------|--------|------|------|
| 空安全 | 内建 | 需 Optional | Kotlin 在类型系统层面区分可空和不可空类型 |
| 扩展函数 | 支持 | 不支持 | 可为现有类添加新方法而无需继承 |
| 数据类 | data class | 需手写 POJO | 一行代码生成 equals/hashCode/toString/copy |
| 协程 | 内建 | 需 RxJava 等 | 轻量级并发方案，支持结构化并发 |
| 默认参数 | 支持 | 不支持 | 函数参数可设置默认值减少重载 |
| 智能类型转换 | 支持 | 需显式 cast | is 检查后自动类型转换 |
| 字符串模板 | 支持 | 需拼接 | $"变量" 语法 |
| 密封类 | sealed class | 无 | 受限的类层次结构，配合 when 使用 |

## 变量声明

### val 与 var

```kotlin
val name: String = "Kotlin"  // 不可变引用（类似 final）
var count: Int = 0           // 可变引用
count++                      // 合法
name = "Java"                // 编译错误：Val cannot be reassigned
```

### 类型推断

```kotlin
val message = "Hello"       // 推断为 String
val number = 42             // 推断为 Int
val pi = 3.14159            // 推断为 Double
val list = listOf(1, 2, 3)  // 推断为 List<Int>
```

### 可空类型与安全调用

```kotlin
var nullable: String? = null  // ? 表示该变量可为 null
val length = nullable?.length // 安全调用，结果为 null 而非 NPE
val len = nullable?.length ?: 0 // Elvis 运算符，提供默认值
val forced = nullable!!.length  // 非空断言，可能抛出 NPE
```

## 控制流

### when 表达式

```kotlin
fun describe(obj: Any): String = when (obj) {
    1          -> "One"
    in 2..10   -> "Between 2 and 10"
    is String  -> "String of length ${obj.length}"
    else       -> "Unknown"
}
```

### for 循环

```kotlin
for (i in 1..5) print(i)              // 12345
for (i in 1 until 5) print(i)         // 1234
for (i in 5 downTo 1 step 2) print(i) // 531
for ((index, value) in list.withIndex()) { }
```

## 函数

### 函数声明

```kotlin
fun sum(a: Int, b: Int): Int = a + b

// 默认参数
fun greet(name: String, prefix: String = "Hello") = "$prefix, $name!"

// 命名参数
greet(prefix = "Hi", name = "Kotlin")

// 可变参数（vararg）
fun varargExample(vararg args: String) { args.forEach { println(it) } }
```

### 高阶函数与 Lambda

```kotlin
val numbers = listOf(1, 2, 3, 4, 5)
val doubled = numbers.map { it * 2 }     // [2, 4, 6, 8, 10]
val evens = numbers.filter { it % 2 == 0 } // [2, 4]

// 函数作为参数
fun operate(a: Int, b: Int, op: (Int, Int) -> Int): Int = op(a, b)
operate(3, 4) { x, y -> x * y }  // 12
```

## 类与对象

### 类声明

```kotlin
class Person(val name: String, var age: Int) {
    init {
        require(age >= 0) { "Age must be non-negative" }
    }
    
    fun display() = "$name is $age years old"
}
```

### 数据类

```kotlin
data class User(val id: Long, val name: String, val email: String)
// 自动生成：toString(), equals(), hashCode(), copy(), componentN()
val user = User(1, "Alice", "alice@example.com")
val copy = user.copy(name = "Bob")
```

### 密封类

```kotlin
sealed class Result {
    data class Success(val data: String) : Result()
    data class Error(val message: String) : Result()
    object Loading : Result()
}

fun handle(result: Result) = when (result) {
    is Result.Success -> "Data: ${result.data}"
    is Result.Error   -> "Error: ${result.message}"
    Result.Loading    -> "Loading..."
    // 无需 else 分支，编译器确保全覆盖
}
```

### 单例对象

```kotlin
object DatabaseConfig {
    val url = "jdbc:postgresql://localhost/db"
    val user = "admin"
    fun connect() { /* ... */ }
}
```

## 扩展函数

```kotlin
fun String.isEmail(): Boolean = this.contains("@")

"user@example.com".isEmail()  // true

// 泛型扩展
fun <T> List<T>.secondOrNull(): T? = if (size >= 2) this[1] else null
```

## 集合操作

### 常用集合操作符

| 操作符 | 功能 | 示例 |
|--------|------|------|
| map | 转换每个元素 | list.map { it * 2 } |
| filter | 筛选元素 | list.filter { it > 0 } |
| reduce | 累积归约 | list.reduce { a, b -> a + b } |
| fold | 带初始值归约 | list.fold(0) { acc, i -> acc + i } |
| flatMap | 展平映射 | list.flatMap { it.split(",") } |
| groupBy | 分组 | list.groupBy { it.length } |
| sortedBy | 排序 | list.sortedBy { it } |

### 序列（Sequence）

```kotlin
val result = (1..1_000_000)
    .asSequence()
    .filter { it % 2 == 0 }
    .map { it * it }
    .take(10)
    .toList()
// 惰性求值，避免中间集合创建
```

## 协程基础

```kotlin
import kotlinx.coroutines.*

suspend fun fetchData(): String {
    delay(1000) // 非阻塞延迟
    return "Data loaded"
}

fun main() = runBlocking {
    val data = async { fetchData() }
    println("Waiting...")
    println(data.await())
}
```

### 协程构建器

| 构建器 | 作用 |
|--------|------|
| launch | 启动协程，返回 Job |
| async | 启动协程，返回 Deferred（可 await 获取结果） |
| runBlocking | 阻塞当前线程等待协程完成（用于桥接） |
| withContext | 切换协程上下文（如切换到 IO 调度器） |

## 与 Java 互操作

```kotlin
// Kotlin 调用 Java
val list = java.util.ArrayList<String>()
list.add("Kotlin")

// Java 调用 Kotlin
// Kotlin 文件会编译为 .class，可直接在 Java 中使用

// @JvmStatic 使 object 中的方法可以作为静态方法调用
// @JvmOverloads 为默认参数函数生成重载
// @JvmField 暴露 Kotlin 属性为 Java 字段
```

## 常见模式

### 委托

```kotlin
// 属性委托
var observableProperty by Delegates.observable("initial") {
    prop, old, new -> println("$old -> $new")
}

// 惰性初始化
val lazyValue: String by lazy {
    println("Computed once")
    "Hello"
}
```

### 作用域函数

| 函数 | 上下文对象 | 返回值 | 适用场景 |
|------|-----------|--------|---------|
| let | it | lambda 结果 | 非空检查、链式调用 |
| apply | this | 上下文对象本身 | 对象配置 |
| run | this | lambda 结果 | 对象配置并计算结果 |
| also | it | 上下文对象本身 | 副作用操作 |
| with | this | lambda 结果 | 对同一对象多次操作 |

```kotlin
val person = Person().apply {
    name = "Alice"
    age = 30
}

"Hello".let { println(it.length) }

val result = with(StringBuilder()) {
    append("Hello ")
    append("World")
    toString()
}
```

## 相关条目
- [[Coroutines]]
- [[Android]]
- [[Compose]]
- [[INDEX|当前目录索引]]
