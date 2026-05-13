# Kotlin 基础语法

## 变量声明

```kotlin
// val: 只读变量（不可变引用），类似 final
val name: String = "Kotlin"
// name = "Java"  // 编译错误

// var: 可变变量
var age: Int = 25
age = 26

// 类型推断
val msg = "Hello"     // 推断为 String
val count = 42        // 推断为 Int
val pi = 3.14159      // 推断为 Double
```

## 空安全

```kotlin
var nullable: String? = null  // ? 表示可为空
var nonNull: String = "safe"  // 不可为空

// ?. 安全调用运算符
val len = nullable?.length     // 如果 null 则返回 null

// ?: Elvis 运算符
val len2 = nullable?.length ?: 0  // null 时返回默认值

// !! 非空断言（谨慎使用）
val len3 = nullable!!.length   // 为 null 则抛 NPE

// 安全转换 as?
val obj: Any = "Hello"
val str: String? = obj as? String
```

## 数据类型

```kotlin
// 基本类型
val b: Byte = 127
val s: Short = 32767
val i: Int = 2147483647
val l: Long = 9223372036854775807L
val f: Float = 3.14F
val d: Double = 3.14159265358979
val bool: Boolean = true
val c: Char = 'A'

// 字符串模板
val name = "World"
val greeting = "Hello, $name!"        // Hello, World!
val calc = "1 + 2 = ${1 + 2}"         // 1 + 2 = 3
val raw = """
    |多行字符串
    |支持模板 $name
""".trimMargin()
```

## 控制流

```kotlin
// if 是表达式
val max = if (a > b) a else b

// when 表达式（类似 switch）
val result = when (x) {
    1 -> "one"
    2, 3 -> "two or three"
    in 4..10 -> "in range"
    is String -> "is string"
    else -> "unknown"
}

// for 循环
for (i in 1..5) print(i)           // 12345
for (i in 6 downTo 0 step 2)       // 6,4,2,0
for (item in list) println(item)
for ((index, value) in array.withIndex()) {}

// while 循环
while (x > 0) { x-- }
do { x++ } while (x < 10)
```

## 函数

```kotlin
// 表达式体函数
fun sum(a: Int, b: Int) = a + b

// 默认参数
fun greet(name: String = "World", prefix: String = "Hello") = "$prefix, $name!"

// 命名参数
greet(prefix = "Hi", name = "Kotlin")

// 可变参数 vararg
fun printAll(vararg items: String) {
    for (item in items) println(item)
}
printAll("a", "b", "c")

// 扩展函数
fun String.isEmail(): Boolean = this.contains("@")
println("test@example.com".isEmail())  // true
```

## 类

```kotlin
// 主构造函数
class Person(val name: String, var age: Int)

// 次要构造函数
class Student {
    constructor(name: String) : this(name, 18)
    constructor(name: String, age: Int)
}

// 数据类：自动生成 equals/hashCode/toString/copy
data class User(val id: Long, val name: String)

// 密封类：受限的类层次结构
sealed class Result {
    data class Success(val data: String) : Result()
    data class Error(val msg: String) : Result()
}

// 单例对象
object DatabaseConfig {
    val url = "jdbc:mysql://localhost:3306/db"
    fun connect() { /* ... */ }
}

// 伴生对象
class MyClass {
    companion object Factory {
        fun create(): MyClass = MyClass()
    }
}
```

## 集合

```kotlin
val list = listOf(1, 2, 3)            // 不可变列表
val mutable = mutableListOf(1, 2, 3)  // 可变列表
val map = mapOf(1 to "a", 2 to "b")   // 不可变映射

// 函数式操作
val numbers = listOf(1, 2, 3, 4, 5)
val even = numbers.filter { it % 2 == 0 }    // [2, 4]
val squared = numbers.map { it * it }         // [1, 4, 9, 16, 25]
val sorted = numbers.sortedByDescending { it } // [5, 4, 3, 2, 1]
```

## Lambda 和高阶函数

```kotlin
// Lambda 表达式
val sum = { x: Int, y: Int -> x + y }

// 高阶函数：接收函数作为参数
fun operateOnNumbers(a: Int, b: Int, op: (Int, Int) -> Int): Int {
    return op(a, b)
}
operateOnNumbers(3, 4) { x, y -> x * y }  // 12

// 常用内置高阶函数
list.any { it > 3 }       // 是否有元素 > 3
list.all { it > 0 }       // 是否全部 > 0
list.none { it < 0 }      // 是否没有 < 0
list.find { it == 3 }     // 查找第一个匹配
list.count { it > 2 }     // 计数
list.groupBy { it % 2 }   // 分组

// 带接受者的函数类型
val sb = StringBuilder()
sb.apply {
    append("Hello ")
    append("World")
}
println(sb.toString())  // Hello World
```
