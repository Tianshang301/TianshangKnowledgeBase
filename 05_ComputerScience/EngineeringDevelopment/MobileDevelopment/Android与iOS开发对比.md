---
aliases: [Android与iOS开发对比]
tags: ['EngineeringDevelopment', 'MobileDevelopment', 'Android与iOS开发对比']
---

# Android与iOS开发对比

## 一、开发环境与工具

两大平台的开发环境和工具链差异显著：

| 维度 | Android | iOS |
|------|---------|-----|
| IDE | Android Studio | Xcode |
| 编程语言 | Kotlin（首选）/ Java | Swift / Objective-C |
| 构建工具 | Gradle | Xcode Build System |
| 包管理器 | Maven Central / JitPack | CocoaPods / SPM |
| 模拟器 | Android Emulator (QEMU) | iOS Simulator |
| 调试工具 | ADB / Profiler | Instruments / LLDB |
| 最低系统要求 | 跨平台 | 仅macOS |

## 二、编程语言对比

Kotlin vs Swift 语法比较：

```kotlin
// Kotlin - 数据类
data class User(
    val id: Int,
    val name: String,
    val email: String
)

// Kotlin - 协程
suspend fun fetchUser(id: Int): User {
    return withContext(Dispatchers.IO) {
        api.getUser(id)
    }
}
```

```swift
// Swift - 结构体
struct User: Codable {
    let id: Int
    let name: String
    let email: String
}

// Swift - async/await
func fetchUser(id: Int) async throws -> User {
    let url = URL(string: "https://api.example.com/users/\(id)")!
    let (data, _) = try await URLSession.shared.data(from: url)
    return try JSONDecoder().decode(User.self, from: data)
}
```

| 特性 | Kotlin | Swift |
|------|--------|-------|
| 空安全 | 内置 | 可选类型 |
| 协程 | kotlinx.coroutines | Swift Concurrency |
| 函数式 | 良好 | 优秀 |
| 互操作性 | Java互操作 | ObjC互操作 |
| 编译速度 | 中等 | 快速 |

## 三、UI框架对比

Jetpack Compose vs SwiftUI：

```kotlin
// Jetpack Compose
@Composable
fun UserProfile(user: User) {
    Column(
        modifier = Modifier.padding(16.dp),
        horizontalAlignment = Alignment.CenterHorizontally
    ) {
        AsyncImage(
            model = user.avatarUrl,
            contentDescription = null,
            modifier = Modifier.size(80.dp).clip(CircleShape)
        )
        Text(
            text = user.name,
            style = MaterialTheme.typography.h6
        )
        Text(
            text = user.email,
            style = MaterialTheme.typography.body2,
            color = Color.Gray
        )
    }
}
```

```swift
// SwiftUI
struct UserProfile: View {
    let user: User

    var body: some View {
        VStack(alignment: .center, spacing: 16) {
            AsyncImage(url: user.avatarUrl) { phase in
                if let image = phase.image {
                    image
                        .resizable()
                        .frame(width: 80, height: 80)
                        .clipShape(Circle())
                }
            }
            Text(user.name)
                .font(.headline)
            Text(user.email)
                .font(.subheadline)
                .foregroundColor(.gray)
        }
        .padding()
    }
}
```

| 特性 | Jetpack Compose | SwiftUI |
|------|----------------|---------|
| 声明式 | 是 | 是 |
| 预览支持 | 实时预览 | Canvas预览 |
| 导航 | Navigation Compose | NavigationStack |
| 状态管理 | State/Hoist | @State/@Binding |
| 最低版本 | API 21+ | iOS 13+ |
| 成熟度 | 稳定 | 稳定 |

## 四、架构模式对比

Android推荐架构（MVVM + Repository）：

```kotlin
// ViewModel
class UserViewModel(
    private val repository: UserRepository
) : ViewModel() {
    private val _users = MutableStateFlow<List<User>>(emptyList())
    val users: StateFlow<List<User>> = _users.asStateFlow()

    fun loadUsers() {
        viewModelScope.launch {
            _users.value = repository.getUsers()
        }
    }
}

// Room Database
@Entity
data class UserEntity(
    @PrimaryKey val id: Int,
    val name: String,
    val email: String
)
```

iOS推荐架构（MVVM + Combine）：

```swift
// ViewModel
@MainActor
class UserViewModel: ObservableObject {
    @Published var users: [User] = []

    func loadUsers() {
        Task {
            users = try await repository.getUsers()
        }
    }
}

// CoreData
@objc(UserEntity)
class UserEntity: NSManagedObject {
    @NSManaged var id: Int32
    @NSManaged var name: String?
    @NSManaged var email: String?
}
```

## 五、应用生命周期

Android生命周期：

```
onCreate() -> onStart() -> onResume() -> [运行中] -> onPause() -> onStop() -> onDestroy()
                        |                                    |
                        +--- onRestart() <--------------------+
```

iOS生命周期：

```
application(_:didFinishLaunchingWithOptions:)
    -> applicationDidBecomeActive(_:)
    -> [运行中]
    -> applicationWillResignActive(_:)
    -> applicationDidEnterBackground(_:)
    -> applicationWillEnterForeground(_:)
    -> applicationDidBecomeActive(_:)
```

## 六、存储方案

| 需求 | Android | iOS |
|------|---------|-----|
| 键值存储 | SharedPreferences / DataStore | UserDefaults |
| 关系数据库 | Room (SQLite) | CoreData / SQLite |
| 文件系统 | Internal/External Storage | Documents Directory |
| 对象存储 | Realm (第三方) | Realm (第三方) |
| 云端存储 | Firebase / Cloud Firestore | CloudKit / Firebase |
| 安全存储 | EncryptedSharedPreferences | Keychain |

## 七、网络与并发

网络请求对比：

```kotlin
// Android - Retrofit + OkHttp
interface ApiService {
    @GET("users/{id}")
    suspend fun getUser(@Path("id") id: Int): User
}

val retrofit = Retrofit.Builder()
    .baseUrl("https://api.example.com/")
    .addConverterFactory(GsonConverterFactory.create())
    .build()
```

```swift
// iOS - URLSession + Codable
struct API {
    static let shared = API()
    let decoder = JSONDecoder()

    func getUser(id: Int) async throws -> User {
        let url = URL(string: "https://api.example.com/users/\(id)")!
        let (data, _) = try await URLSession.shared.data(from: url)
        return try decoder.decode(User.self, from: data)
    }
}
```

## 八、发布与分发

| 流程 | Google Play | App Store |
|------|-------------|-----------|
| 开发者注册 | 25美元（一次性） | 99美元/年 |
| 应用审核 | 自动（部分审查） | 人工审核（1-7天） |
| 测试渠道 | Internal/Closed/Open | TestFlight |
| 更新频率 | 灵活 | 审核后生效 |
| 分成比例 | 30%（15%首百万） | 30%（15%小企业） |
| 应用大小限制 | 4GB（含APK扩展） | 4GB |
| 上架成功率 | 高 | 中等 |

## 九、性能与优化

性能优化关注点对比：

```kotlin
// Android - 使用Profile GPU Rendering检测
// Android GPU Inspector分析帧率
// LeakCanary检测内存泄漏
@Composable
fun LazyList(items: List<Item>) {
    LazyColumn {
        items(items, key = { it.id }) { item ->
            ItemRow(item)
        }
    }
}
```

```swift
// iOS - Time Profiler检测性能瓶颈
// Allocations跟踪内存分配
// 使用UICollectionView的prefetching
List(items, id: \.id) { item in
    ItemRow(item: item)
}
.task {
    await loadMoreItems()
}
```

## 参考资源

1. Android官方文档：https://developer.android.com/docs
2. iOS开发者文档：https://developer.apple.com/documentation
3. Jetpack Compose指南：https://developer.android.com/jetpack/compose
4. SwiftUI教程：https://developer.apple.com/tutorials/swiftui
5. 《Android编程权威指南》书籍
6. 《iOS编程（第6版）》书籍
7. Google Codelabs：https://codelabs.developers.google.com
