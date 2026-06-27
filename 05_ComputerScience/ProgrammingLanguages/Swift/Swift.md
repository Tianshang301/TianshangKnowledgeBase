---
aliases: [Swift]
tags: ['ProgrammingLanguages', 'Swift', 'Swift']
created: 2026-05-16
updated: 2026-05-16
---

# Swift

## 一、Swift 概述

Swift 是 Apple 于 2014 年推出的现代编程语言，融合了 C 和 Objective-C 的优点，同时引入函数式编程和安全特性。Swift 是类型安全、内存安全、高性能的编译型语言。

| 特性 | 说明 |
|------|------|
| 开发公司 | Apple Inc. |
| 开源 | 是（Apache 2.0 许可证） |
| 主要用途 | iOS/macOS/watchOS/tvOS 开发, 服务端 (Vapor) |
| 编译方式 | LLVM 编译器 |
| 内存管理 | ARC（自动引用计数） |
| 类型系统 | 静态、强类型、类型推断 |
| 范式 | OOP + 协议导向 + 函数式 |

### 集合类型时间复杂度

| 操作 | Array | Set | Dictionary |
|------|-------|-----|-----------|
| 读下标 | $O(1)$ | — | — |
| contains/search | $O(n)$ | $O(1)$ | $O(1)$ |
| 插入 | $O(1)$ 均摊 | $O(1)$ 均摊 | $O(1)$ 均摊 |
| 删除 | $O(n)$ | $O(1)$ | $O(1)$ |
| append | $O(1)$ 均摊 | — | — |
| sort | $O(n \log n)$ | — | — |

### ARC 引用计数

Swift 使用 ARC (Automatic Reference Counting) 管理内存，每个对象维护引用计数值：

$$ \text{retain: } \text{RC} \gets \text{RC} + 1 $$
$$ \text{release: } \text{RC} \gets \text{RC} - 1 $$
$$ \text{dealloc} \iff \text{RC} = 0 $$

**循环引用**：使用 `weak`（弱引用，RC 不加 1）或 `unowned`（无主引用）打破强引用环。

## 二、基本语法

### 变量与常量

```swift
var name = "Alice"          // 可变变量
let pi = 3.14159            // 不可变常量
var x: Int = 42             // 显式类型标注

// 基本类型
let int: Int = 10
let double: Double = 3.14
let bool: Bool = true
let str: String = "Hello"
let char: Character = "A"

// 集合类型
let array: [Int] = [1, 2, 3]
let dict: [String: Int] = ["a": 1, "b": 2]
let set: Set<Int> = [1, 2, 3]
```

### 类型推断

```swift
let message = "Hello"       // 推断为 String
let count = 42              // 推断为 Int
```

## 三、可选类型（Optionals）

可选类型是 Swift 的核心安全特性，表示值可能存在也可能为 `nil`。

```swift
var optionalName: String? = "Alice"
optionalName = nil

// 强制解包（不安全）
print(optionalName!)

// if let 绑定
if let name = optionalName {
    print("Hello, \(name)")
}

// guard let 提前返回
guard let name = optionalName else {
    return
}

// nil 合并运算符
let displayName = optionalName ?? "Guest"

// 可选链
let length = optionalName?.count
```

## 四、控制流

```swift
// for-in 循环
for i in 0..<5 {             // 半开区间：0,1,2,3,4
    print(i)
}

for item in array {
    print(item)
}

for (key, value) in dict {
    print("\(key): \(value)")
}

// while / repeat-while
while condition {
    // 处理
}

repeat {
    // 至少执行一次
} while condition

// switch（功能强大，无需 break）
let value = 42
switch value {
case 0:
    print("zero")
case 1..<10:
    print("small")
case 10...100:
    print("medium")
case let x where x > 100:
    print("large: \(x)")
default:
    break
}
```

## 五、函数与闭包

### 函数

```swift
// 基本函数
func greet(name: String) -> String {
    return "Hello, \(name)"
}

// 参数标签
func add(_ a: Int, to b: Int) -> Int {
    return a + b
}
add(3, to: 5)             // 8

// 默认参数
func multiply(_ a: Int, by b: Int = 2) -> Int {
    return a * b
}

// 可变参数
func sum(_ numbers: Int...) -> Int {
    return numbers.reduce(0, +)
}

// inout 参数
func swap(_ a: inout Int, _ b: inout Int) {
    let temp = a; a = b; b = temp
}
```

### 闭包

```swift
// 闭包表达式
let square: (Int) -> Int = { x in
    return x * x
}

// 简化语法
let add = { $0 + $1 }

// 尾随闭包
let sorted = array.sorted { $0 < $1 }

// @escaping（逃逸闭包）
func fetch(completion: @escaping (Data) -> Void) {
    DispatchQueue.global().async {
        // 长时间任务
        completion(data)
    }
}

// @autoclosure（自动闭包）
func assert(_ condition: @autoclosure () -> Bool) {
    if !condition() { fatalError() }
}
```

## 六、结构体 vs 类

| 特性 | 结构体 (struct) | 类 (class) |
|------|----------------|-----------|
| 类型 | 值类型 | 引用类型 |
| 赋值语义 | 拷贝 | 共享引用 |
| 继承 | 不支持 | 支持 |
| 析构器 | 不支持 | 支持（deinit） |
| 可变性 | 方法需 `mutating` | 方法可直接修改 |
| 存储位置 | 栈（通常） | 堆 |
| 协议遵循 | 支持 | 支持 |

```swift
struct Point {
    var x: Double
    var y: Double

    mutating func moveBy(dx: Double, dy: Double) {
        x += dx
        y += dy
    }
}

class Person {
    let name: String
    var age: Int

    init(name: String, age: Int) {
        self.name = name
        self.age = age
    }

    deinit {
        print("\(name) deallocated")
    }
}
```

## 七、协议

协议定义接口规范，Swift 强调**协议导向编程**。

```swift
protocol Drivable {
    var speed: Double { get set }
    func drive()
}

protocol Flyable: Drivable {       // 协议继承
    func fly()
}

// 协议组合
func test(vehicle: Drivable & Flyable) { }

// 协议扩展（提供默认实现）
extension Drivable {
    func drive() {
        print("Driving at \(speed) km/h")
    }
}

// 关联类型
protocol Container {
    associatedtype Item
    mutating func append(_ item: Item)
    var count: Int { get }
}
```

## 八、错误处理

```swift
enum FileError: Error {
    case notFound
    case permissionDenied
    case corrupted
}

// 抛出错误
func readFile(path: String) throws -> String {
    guard path.isEmpty == false else {
        throw FileError.notFound
    }
    return "file content"
}

// do-catch
do {
    let content = try readFile(path: "data.txt")
    print(content)
} catch FileError.notFound {
    print("File not found")
} catch {
    print("Unknown error: \(error)")
}

// try?（将错误转为可选）
let content = try? readFile(path: "data.txt")

// try!（强制解包）
let content = try! readFile(path: "data.txt")

// Result 类型
func fetchData() -> Result<Data, Error> {
    if success {
        return .success(data)
    } else {
        return .failure(error)
    }
}
```

## 九、并发编程（async/await）

Swift 5.5+ 引入结构化并发。

```swift
// 异步函数
func fetchUser(id: Int) async throws -> User {
    let url = URL(string: "https://api.example.com/user/\(id)")!
    let (data, _) = try await URLSession.shared.data(from: url)
    return try JSONDecoder().decode(User.self, from: data)
}

// Task 和 await
Task {
    do {
        let user = try await fetchUser(id: 42)
        print(user.name)
    } catch {
        print(error)
    }
}

// Actor（保护可变状态）
actor BankAccount {
    private var balance: Double = 0

    func deposit(amount: Double) {
        balance += amount
    }

    func getBalance() -> Double {
        return balance
    }
}

// Sendable 协议（标记可跨并发域传递的类型）
struct User: Sendable {
    let id: Int
    let name: String
}
```

## 十、SwiftUI 基础

```swift
import SwiftUI

struct ContentView: View {
    @State private var count = 0
    @State private var name = ""
    @StateObject private var viewModel = ViewModel()

    var body: some View {
        NavigationView {
            VStack(spacing: 20) {
                Text("Count: \(count)")
                    .font(.largeTitle)
                    .foregroundColor(.blue)

                HStack {
                    Button("-") { count -= 1 }
                    Button("+") { count += 1 }
                }

                TextField("Enter name", text: $name)
                    .textFieldStyle(RoundedBorderTextFieldStyle())
                    .padding()

                Text("Hello, \(name.isEmpty ? "World" : name)")

                List(viewModel.items, id: \.self) { item in
                    Text(item)
                }
            }
            .padding()
            .navigationTitle("SwiftUI Demo")
        }
    }
}
```

| 修饰符 | 功能 |
|--------|------|
| `@State` | 视图本地状态 |
| `@Binding` | 传递状态引用 |
| `@ObservedObject` | 引用类型可观察对象 |
| `@StateObject` | 视图拥有的可观察对象 |
| `@Published` | 属性变化自动通知 |
| `@EnvironmentObject` | 全局共享状态 |

## 十一、Swift Package Manager (SPM)

```swift
// Package.swift
// swift-tools-version:5.7
import PackageDescription

let package = Package(
    name: "MyLibrary",
    platforms: [
        .macOS(.v12), .iOS(.v15)
    ],
    products: [
        .library(name: "MyLibrary", targets: ["MyLibrary"]),
    ],
    dependencies: [
        .package(url: "https://github.com/Alamofire/Alamofire.git",
                 from: "5.6.0"),
    ],
    targets: [
        .target(
            name: "MyLibrary",
            dependencies: ["Alamofire"]),
        .testTarget(
            name: "MyLibraryTests",
            dependencies: ["MyLibrary"]),
    ]
)
```

## 相关条目

- [[05_ComputerScience/EngineeringDevelopment/MobileDevelopment/MobileDevelopment|MobileDevelopment]]
- iOS
- [[05_ComputerScience/ProgrammingLanguages/INDEX|ProgrammingLanguages]]
- AppDevelopment

## 参考资源

- [Swift 官方文档](https://docs.swift.org/swift-book/)
- [Swift 论坛](https://forums.swift.org/)
- [SwiftUI 教程](https://developer.apple.com/tutorials/swiftui)
- 《Swift Programming: The Big Nerd Ranch Guide》
- [Swift Package Index](https://swiftpackageindex.com/)


