---
aliases: [SwiftUI 与 iOS 开发]
tags: ['ProgrammingLanguages', 'Swift', 'SwiftUI 与 iOS 开发']
---

# SwiftUI 与 iOS 开发

## 一、Swift 语言基础

Swift 是 Apple 于2014年推出的编程语言，结合了现代语言特性与 Objective-C 的运行时能力。

```swift
// 基本语法
let name: String = "Swift"       // 常量
var version = 5.9                // 变量（类型推断）

// 函数与闭包
func greet(_ person: String, from place: String = "unknown") -> String {
    return "Hello, \(person) from \(place)!"
}

let numbers = [1, 2, 3, 4, 5]
let squared = numbers.map { $0 * $0 }  // 闭包

// 枚举与关联值
enum Result<T> {
    case success(T)
    case failure(Error)
}

// 协议与扩展
protocol Drawable {
    func draw() -> String
}

extension String: Drawable {
    func draw() -> String { return "Drawing: \(self)" }
}
```

Swift 版本演进：

| 版本 | 年份 | 关键特性 |
|------|------|----------|
| Swift 1.0 | 2014 | 初始发布 |
| Swift 2.0 | 2015 | Error handling, guard |
| Swift 3.0 | 2016 | API 命名规范统一 |
| Swift 4.0 | 2017 | Codable, String 改进 |
| Swift 5.0 | 2019 | ABI 稳定, Module 稳定性 |
| Swift 5.5 | 2021 | async/await, Actor |
| Swift 5.9 | 2023 | 宏系统, 所有权 |

## 二、SwiftUI 声明式 UI

SwiftUI 是 Apple 的声明式 UI 框架，2019年随 iOS 13发布。

核心概念：View 是 UI 的基本构建块，通过组合和修饰器构建界面。

```swift
import SwiftUI

struct ContentView: View {
    @State private var count = 0
    @State private var name = ""

    var body: some View {
        NavigationStack {
            VStack(spacing: 20) {
                // 文本
                Text("Hello, SwiftUI!")
                    .font(.largeTitle)
                    .foregroundColor(.blue)
                    .padding()

                // 输入框
                TextField("Enter your name", text: $name)
                    .textFieldStyle(.roundedBorder)
                    .padding(.horizontal)

                // 按钮
                Button(action: { count += 1 }) {
                    Label("Count: \(count)", systemImage: "hand.tap")
                }
                .buttonStyle(.borderedProminent)

                // 列表
                List {
                    Section("Fruits") {
                        Text("Apple")
                        Text("Banana")
                        Text("Orange")
                    }
                }
                .listStyle(.insetGrouped)
            }
            .navigationTitle("SwiftUI Demo")
            .toolbar {
                ToolbarItem(placement: .topBarTrailing) {
                    Button("Reset") { count = 0 }
                }
            }
        }
    }
}
```

## 三、布局与容器

SwiftUI 布局系统基于三个核心容器：

| 容器 | 方向 | 对齐 | 间距 | 适用场景 |
|------|------|------|------|----------|
| VStack | 垂直 | 水平对齐 | 垂直间距 | 列表式布局 |
| HStack | 水平 | 垂直对齐 | 水平间距 | 行式布局 |
| ZStack | Z 轴叠放 | 齐 | 无间距 | 叠加效果 |

```swift
struct LayoutDemo: View {
    var body: some View {
        VStack(alignment: .leading, spacing: 10) {
            Text("Profile").font(.title)

            HStack(alignment: .center, spacing: 16) {
                Image(systemName: "person.circle.fill")
                    .resizable()
                    .frame(width: 60, height: 60)
                    .foregroundColor(.gray)

                VStack(alignment: .leading) {
                    Text("John Doe")
                        .font(.headline)
                    Text("iOS Developer")
                        .font(.subheadline)
                        .foregroundColor(.secondary)
                }

                Spacer()
            }
            .padding()
            .background(Color(.systemGray6))
            .cornerRadius(12)

            // 使用 GeometryReader 自适应布局
            GeometryReader { geo in
                HStack(spacing: 0) {
                    Rectangle()
                        .fill(.red)
                        .frame(width: geo.size.width * 0.3)
                    Rectangle()
                        .fill(.blue)
                        .frame(width: geo.size.width * 0.7)
                }
            }
            .frame(height: 50)
        }
        .padding()
    }
}
```

## 四、数据流与状态管理

SwiftUI 的数据驱动模型：

```swift
// @State: 视图私有状态
struct CounterView: View {
    @State private var count = 0

    var body: some View {
        Stepper("Count: \(count)", value: $count)
    }
}

// @Binding: 父子视图共享状态
struct ChildView: View {
    @Binding var isPresented: Bool

    var body: some View {
        Button("Dismiss") { isPresented = false }
    }
}

// @ObservedObject / @StateObject: 引用类型数据
class UserViewModel: ObservableObject {
    @Published var userName = ""
    @Published var isLoggedIn = false
}

struct ProfileView: View {
    @StateObject private var viewModel = UserViewModel()

    var body: some View {
        Text("User: \(viewModel.userName)")
    }
}

// @EnvironmentObject: 全局依赖注入
struct AppView: View {
    @EnvironmentObject var settings: AppSettings

    var body: some View {
        Text("Theme: \(settings.theme)")
    }
}
```

Property Wrapper 对比：

| 包装器 | 所有权 | 生命周期 | 触发 UI 更新 | 用途 |
|--------|--------|----------|-----------|------|
| @State | 视图私有 | 视图生命周期 | 是 | 简单值类型 |
| @Binding | 共享引用 | 源视图生命周期 | 是 | 传递状态 |
| @StateObject | 视图创建 | 视图生命周期 | 是 | 复杂数据模型 |
| @ObservedObject | 外部传入 | 外部管理 | 是 | 外部数据 |
| @EnvironmentObject | 隐式依赖 | 祖先提供 | 是 | 全局状态 |

## 五、导航与路由

```swift
// NavigationStack (iOS 16+)
struct NavigationDemo: View {
    var body: some View {
        NavigationStack {
            List {
                NavigationLink("Basic View", destination: BasicView())
                NavigationLink("Detail View", value: DetailType.detail)
                NavigationLink("Settings", value: "settings")
            }
            .navigationDestination(for: DetailType.self) { type in
                DetailView(type: type)
            }
            .navigationDestination(for: String.self) { route in
                if route == "settings" {
                    SettingsView()
                }
            }
        }
    }
}

enum DetailType: Hashable {
    case detail
    case info
    case edit
}

// TabView
struct TabBarView: View {
    var body: some View {
        TabView {
            HomeView()
                .tabItem {
                    Label("Home", systemImage: "house")
                }

            SearchView()
                .tabItem {
                    Label("Search", systemImage: "magnifyingglass")
                }

            SettingsView()
                .tabItem {
                    Label("Settings", systemImage: "gear")
                }
        }
    }
}
```

## 六、网络请求与异步编程

```swift
import SwiftUI

struct User: Codable, Identifiable {
    let id: Int
    let name: String
    let email: String
}

@MainActor
class UserListViewModel: ObservableObject {
    @Published var users: [User] = []
    @Published var isLoading = false
    @Published var errorMessage: String?

    func fetchUsers() async {
        isLoading = true
        errorMessage = nil

        do {
            let url = URL(string: "https://jsonplaceholder.typicode.com/users")!
            let (data, _) = try await URLSession.shared.data(from: url)
            users = try JSONDecoder().decode([User].self, from: data)
        } catch {
            errorMessage = error.localizedDescription
        }

        isLoading = false
    }
}

struct UserListView: View {
    @StateObject private var viewModel = UserListViewModel()

    var body: some View {
        NavigationStack {
            Group {
                if viewModel.isLoading {
                    ProgressView("Loading...")
                } else if let error = viewModel.errorMessage {
                    VStack {
                        Text("Error: \(error)")
                            .foregroundColor(.red)
                        Button("Retry") {
                            Task { await viewModel.fetchUsers() }
                        }
                    }
                } else {
                    List(viewModel.users) { user in
                        VStack(alignment: .leading) {
                            Text(user.name).font(.headline)
                            Text(user.email).font(.caption)
                        }
                    }
                }
            }
            .navigationTitle("Users")
            .task {
                await viewModel.fetchUsers()
            }
            .refreshable {
                await viewModel.fetchUsers()
            }
        }
    }
}
```

## 七、Core Data 持久化

```swift
import CoreData

// 数据模型定义
@Model
class Task {
    @Attribute(.unique) var id: UUID
    var title: String
    var isCompleted: Bool
    var dueDate: Date
    @Relationship(inverse: \Category.tasks) var category: Category?

    init(title: String, dueDate: Date = Date()) {
        self.id = UUID()
        self.title = title
        self.isCompleted = false
        self.dueDate = dueDate
    }
}

@Model
class Category {
    @Attribute(.unique) var name: String
    var tasks: [Task] = []

    init(name: String) {
        self.name = name
    }
}

// SwiftUI 集成
struct TaskListView: View {
    @Environment(\.modelContext) private var modelContext
    @Query(sort: \Task.dueDate, order: .forward) private var tasks: [Task]

    var body: some View {
        List {
            ForEach(tasks) { task in
                HStack {
                    Button(action: {
                        task.isCompleted.toggle()
                    }) {
                        Image(systemName: task.isCompleted
                            ? "checkmark.circle.fill"
                            : "circle")
                    }

                    VStack(alignment: .leading) {
                        Text(task.title)
                            .strikethrough(task.isCompleted)
                        Text(task.dueDate, style: .date)
                            .font(.caption)
                            .foregroundColor(.secondary)
                    }
                }
            }
            .onDelete(perform: deleteTasks)
        }
    }

    private func deleteTasks(at offsets: IndexSet) {
        for index in offsets {
            modelContext.delete(tasks[index])
        }
    }
}
```

## 八、动画与过渡

```swift
struct AnimationDemo: View {
    @State private var isAnimated = false

    var body: some View {
        VStack {
            // 隐式动画
            Circle()
                .fill(isAnimated ? .blue : .red)
                .frame(width: 100, height: 100)
                .scaleEffect(isAnimated ? 1.5 : 1.0)
                .animation(.spring(response: 0.5, dampingFraction: 0.6),
                           value: isAnimated)

            // 显式动画
            RoundedRectangle(cornerRadius: 20)
                .fill(.green)
                .frame(width: isAnimated ? 300 : 100, height: 100)

            // 转场动画
            if isAnimated {
                Text("Fade In")
                    .transition(.move(edge: .bottom).combined(with: .opacity))
            }

            Button("Animate") {
                withAnimation(.easeInOut(duration: 0.8)) {
                    isAnimated.toggle()
                }
            }
            .buttonStyle(.borderedProminent)
        }
    }
}
```

## 九、测试与调试

```swift
import XCTest

// 单元测试
final class UserViewModelTests: XCTestCase {
    var viewModel: UserListViewModel!

    override func setUp() {
        super.setUp()
        viewModel = UserListViewModel()
    }

    override func tearDown() {
        viewModel = nil
        super.tearDown()
    }

    func testInitialState() {
        XCTAssertTrue(viewModel.users.isEmpty)
        XCTAssertFalse(viewModel.isLoading)
        XCTAssertNil(viewModel.errorMessage)
    }
}

// UI 测试
final class AppUITests: XCTestCase {
    let app = XCUIApplication()

    override func setUp() {
        continueAfterFailure = false
        app.launch()
    }

    func testNavigation() {
        XCTAssertTrue(app.navigationBars["SwiftUI Demo"].exists)
        app.buttons["Reset"].tap()
    }
}
```

## 相关条目

- [[Swift]]
- [[MobileDevelopment]]
- UI_UX
- AppDevelopment

## 参考资源

1. Apple SwiftUI 文档：https://developer.apple.com/documentation/swiftui
2. 《Swift 编程》第6版
3. Hacking with Swift 教程：https://www.hackingwithswift.com
4. Swift 官方文档：https://docs.swift.org
5. Swift UI 设计指南：Apple HIG
6. WWDC SwiftUI 相关视频
7. Point-Free 函数式 Swift 教程
