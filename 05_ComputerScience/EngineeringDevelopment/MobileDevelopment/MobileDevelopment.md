---
aliases: [MobileDevelopment]
tags: ['EngineeringDevelopment', 'MobileDevelopment', 'MobileDevelopment']
---

# 移动开发完全指南

## 概述

移动开发涉及为智能手机和平板电脑创建应用程序。两大主导平台是 Android 和 iOS，此外跨平台框架也在快速发展。移动开发需要考虑屏幕适配、性能优化、电池续航、网络连接等多方面因素。

---

## 一、移动平台对比

| 维度 | Android | iOS |
|------|---------|-----|
| 开发语言 | Kotlin(主流), Java | Swift(主流), Objective-C |
| 开发工具 | Android Studio | Xcode |
| UI 框架 | Jetpack Compose, XML | SwiftUI, UIKit |
| 应用商店 | Google Play | App Store |
| 市场份额 | ~70% | ~30% |
| 系统开放性 | 开放(可侧载 APK) | 封闭(仅 App Store) |
| 设备碎片化 | 严重(多种屏幕/系统版本) | 较少(有限设备) |
| 审核周期 | 数小时 | 1-7 天 |
| 开发成本 | 一次性注册 $25 | 年费 $99 |

---

## 二、Android 开发

### 2.1 核心组件

| 组件 | 作用 | 说明 |
|------|------|------|
| Activity | 用户界面入口 | 每个界面一个 Activity |
| Fragment | 界面模块 | 可复用的 UI 片段 |
| Service | 后台任务 | 不提供 UI |
| BroadcastReceiver | 广播消息监听 | 系统事件、自定义事件 |
| ContentProvider | 数据共享 | 跨应用数据访问 |
| Intent | 组件间通信 | 显式/隐式 Intent |

### 2.2 Activity 生命周期

```
         ┌─────────┐
         │ onCreate │ ← 创建 (初始化)
         └────┬─────┘
              │
         ┌────▼─────┐
         │ onStart  │ ← 可见 (但不可交互)
         └────┬─────┘
              │
         ┌────▼─────┐
         │ onResume │ ← 可交互
         └────┬─────┘
              │
    ┌─────────┴─────────┐
    │                   │
┌────▼─────┐      ┌────▼─────┐
│ onPause  │      │ 正常运行  │ (部分可见)
└────┬─────┘      └────┬─────┘
     │                  │
┌────▼─────┐      ┌────▼─────┐
│ onStop   │      │ 完全不可见 │
└────┬─────┘      └──────────┘
     │
┌────▼─────┐
│ onDestroy│ ← 销毁 (释放资源)
└──────────┘

Activity A → Activity B:
  A.onPause() → B.onCreate() → B.onStart() → B.onResume() → A.onStop()
```

### 2.3 Jetpack Compose vs XML

```kotlin
// Jetpack Compose (声明式)
@Composable
fun Greeting(name: String) {
    Column(modifier = Modifier.padding(16.dp)) {
        Text(text = "Hello, $name!", style = MaterialTheme.typography.h4)
        Button(onClick = { /* 点击事件 */ }) {
            Text("点击我")
        }
    }
}
```

```xml
<!-- XML 布局 (命令式) -->
<LinearLayout
    xmlns:android="http://schemas.android.com/apk/res/android"
    android:layout_width="match_parent"
    android:layout_height="wrap_content"
    android:padding="16dp">
    <TextView
        android:id="@+id/greeting"
        android:textSize="24sp"
        android:text="Hello, World!" />
    <Button
        android:id="@+id/button"
        android:text="点击我" />
</LinearLayout>
```

---

## 三、iOS 开发

### 3.1 UIKit 视图控制器生命周期

```
viewDidLoad      → 视图加载完成 (初始化设置)
viewWillAppear   → 视图即将显示
viewDidAppear    → 视图已显示 (动画、网络请求)
viewWillDisappear→ 视图即将消失
viewDidDisappear → 视图已消失
deinit           → 控制器销毁
```

### 3.2 SwiftUI 示例

```swift
import SwiftUI

struct ContentView: View {
    @State private var count = 0
    
    var body: some View {
        VStack(spacing: 20) {
            Text("计数: \(count)")
                .font(.largeTitle)
                .foregroundColor(.blue)
            
            Button(action: {
                count += 1
            }) {
                Text("点击增加")
                    .padding()
                    .background(Color.blue)
                    .foregroundColor(.white)
                    .cornerRadius(10)
            }
        }
    }
}
```

### 3.3 Auto Layout

```
Auto Layout 约束:
  button.leading  = view.leading + 16
  button.trailing = view.trailing - 16
  button.top      = label.bottom + 8
  button.height   = 44

优先级 (Priority):
  Required (1000): 必须满足
  DefaultHigh (750): 尽量满足
  DefaultLow (250): 低优先级

等宽/等高:
  多个视图等宽约束
  适配不同屏幕尺寸
```

### 3.4 Core Data

```swift
// Core Data 示例
@main
struct MyApp: App {
    let persistenceController = PersistenceController.shared
    
    var body: some Scene {
        WindowGroup {
            ContentView()
                .environment(\.managedObjectContext, persistenceController.container.viewContext)
        }
    }
}

// 数据操作
let newItem = Item(context: viewContext)
newItem.name = "示例"
newItem.timestamp = Date()

do {
    try viewContext.save()
} catch {
    print("保存失败: \(error)")
}
```

---

## 四、跨平台框架

| 框架 | 语言 | 渲染引擎 | 性能 | 热重载 | 学习成本 |
|------|------|----------|------|--------|----------|
| Flutter | Dart | Skia (自绘引擎) | 优秀 | 支持 | 中等 |
| React Native | JavaScript | 原生组件桥接 | 良好 | 支持 | 中等 |
| .NET MAUI | C# | 原生渲染 | 良好 | 支持 (Hot Reload) | 较高 |
| Kotlin Multiplatform | Kotlin | 原生 UI | 优秀 | 部分 | 中等 |
| Ionic | TypeScript | WebView | 一般 | 支持 | 较低 |

### 4.1 Flutter 核心概念

```dart
class MyWidget extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('Flutter 示例')),
      body: Center(
        child: Column(
          children: [
            Text('Hello Flutter', style: TextStyle(fontSize: 24)),
            ElevatedButton(
              onPressed: () => print('点击'),
              child: Text('按钮'),
            ),
          ],
        ),
      ),
    );
  }
}
```

---

## 五、移动 UI/UX

| 平台 | 设计语言 | 核心原则 |
|------|----------|----------|
| Android | Material Design 3 | 动效 (Motion)、自适应 (Adaptive)、个性化 (Personalization) |
| iOS | Human Interface Guidelines | 清晰 (Clarity)、谦逊 (Deference)、深度 (Depth) |

```
响应式设计:
  安全区域 (Safe Area): 避开刘海/圆角
  适配不同屏幕尺寸: 使用相对单位而非绝对像素
  dp/pt: 密度无关像素
  Sp: 可缩放像素 (字体)
  
触摸目标:
  最小触摸目标: 48x48 dp (Android) / 44x44 pt (iOS)
  触摸反馈: 涟漪效果 (Ripple) / 高亮 (Highlight)
```

---

## 六、网络通信

```kotlin
// Retrofit (Android)
interface ApiService {
    @GET("users/{id}")
    suspend fun getUser(@Path("id") id: Int): User
    
    @POST("users")
    suspend fun createUser(@Body user: User): User
}
```

```swift
// URLSession (iOS)
func fetchUser(id: Int) async throws -> User {
    let url = URL(string: "https://api.example.com/users/\(id)")!
    let (data, response) = try await URLSession.shared.data(from: url)
    return try JSONDecoder().decode(User.self, from: data)
}
```

**离线缓存策略**:

| 策略 | 描述 | 适用 |
|------|------|------|
| 网络优先 | 先请求网络 → 缓存结果 | 实时数据 |
| 缓存优先 | 先显示缓存 → 后台更新 | 内容展示 |
| 缓存优先(网络回退) | 有缓存用缓存，无则网络 | 新闻阅读 |
| 仅缓存 | 从不请求网络 | 静态内容 |

---

## 七、本地存储

| 技术 | 平台 | 存储类型 | 特点 |
|------|------|----------|------|
| Room | Android | SQLite ORM | 编译时 SQL 验证 |
| SQLite | 通用 | 关系型数据库 | 轻量、通用 |
| Core Data | iOS | 对象图管理 | 复杂数据模型 |
| SharedPreferences | Android | 键值对 | 简单配置 |
| UserDefaults | iOS | 键值对 | 简单配置 |
| File System | 通用 | 文件存储 | 大文件、缓存 |

---

## 八、推送通知

```
FCM (Firebase Cloud Messaging):
  App Server → FCM → 设备
  ↓ 流程:
  1. 注册 FCM
  2. 获取 Token
  3. 存储到应用服务器
  4. 服务器发送推送
  5. 系统/应用处理

APNs (Apple Push Notification):
  Provider Server → APNs → 设备
  ↓ 区别:
  - FCM 支持 Android + iOS
  - APNs 仅 iOS
  - 推送达率: APNs > FCM (iOS)
```

---

## 九、应用发布

| 阶段 | Android (Google Play) | iOS (App Store) |
|------|----------------------|-----------------|
| 签名 | 使用 keystore 签名 | 使用 Apple 证书签名 |
| 应用包 | AAB (推荐), APK | IPA |
| 上传 | Google Play Console | App Store Connect |
| 审核 | 自动化审核 | 人工 + 自动化 |
| 测试 | 内部/封闭/开放测试 | TestFlight (最多 10000 人) |
| 发布 | 逐步/完全/分阶段 | 手动/自动 |

---

## 十、性能优化

### 性能指标

| 指标 | 公式 | 说明 |
|------|------|------|
| FPS | $\text{FPS} = \dfrac{1}{\Delta t}$ | 帧率，$\Delta t$ 为帧间隔 |
| 帧时间 | $t_{\text{frame}} = t_{\text{CPU}} + t_{\text{GPU}}$ | CPU 与 GPU 耗时之和 |
| 启动时间 | $t_{\text{cold}} = t_{\text{init}} + t_{\text{layout}} + t_{\text{network}}$ | 冷启动总耗时 |
| 内存占用 | $M_{\text{app}} = M_{\text{code}} + M_{\text{heap}} + M_{\text{stack}} + M_{\text{gfx}}$ | 应用总内存 |
| 包体大小 | $S_{\text{apk}} = S_{\text{dex}} + S_{\text{res}} + S_{\text{lib}} + S_{\text{assets}}$ | APK 构成 |
| 耗电量 | $E = \int P(t)\,dt$ | 功耗对时间的积分 |

### 时间复杂度与内存分析

常见数据操作的时间复杂度与内存增长：

| 数据结构 | 访问 | 搜索 | 插入 | 删除 | 额外内存 |
|---------|------|------|------|------|---------|
| 数组 | $O(1)$ | $O(n)$ | $O(n)$ | $O(n)$ | $O(n)$ |
| 链表 | $O(n)$ | $O(n)$ | $O(1)$ | $O(1)$ | $O(n)$ |
| 哈希表 | $O(1)$ | $O(1)$ | $O(1)$ | $O(1)$ | $O(n)$ |
| 二叉搜索树 | $O(\log n)$ | $O(\log n)$ | $O(\log n)$ | $O(\log n)$ | $O(n)$ |

**内存泄漏检测：**
$$\text{Leaked} = M_{\text{alloc}} - M_{\text{free}} > 0 \quad \text{持续增长} \Rightarrow \text{内存泄漏}$$

**Bitmap 内存计算：**
$$M_{\text{bitmap}} = \text{width} \times \text{height} \times \text{bytesPerPixel}$$

| 像素格式 | bytesPerPixel | 示例（1080×1920） |
|---------|---------------|-------------------|
| ARGB_8888 | 4 | 约 7.9 MB |
| RGB_565 | 2 | 约 3.9 MB |
| Alpha_8 | 1 | 约 2.0 MB |

### 性能优化策略

| 优化方向 | 方法 | 效果量级 |
|---------|------|---------|
| 布局优化 | 减少嵌套、使用 ConstraintLayout | 10-30% |
| 绘制优化 | 减少 overdraw、使用 GPU 缓存 | 20-50% |
| 内存优化 | 对象池、图片压缩、LRU 缓存 | 减少 GC 暂停 |
| 网络优化 | 请求合并、数据压缩、DNS 预解析 | 30-60% 延迟降低 |
| 线程优化 | 异步任务、线程池复用 | 避免主线程阻塞 |
| 启动优化 | 懒加载、启动任务图并行化 | 缩短 30-50% 启动时间 |

## 相关条目

- [[WebDevelopment]]
- [[DesktopDevelopment]]
- AppDevelopment
- UI_UX

## 参考资源

- Android 开发者文档: https://developer.android.com/docs
- Apple 开发者文档: https://developer.apple.com/documentation
- Flutter 官方文档: https://flutter.dev/docs
- React Native 文档: https://reactnative.dev/docs
- Material Design: https://material.io/design
- Human Interface Guidelines: https://developer.apple.com/design/human-interface-guidelines
