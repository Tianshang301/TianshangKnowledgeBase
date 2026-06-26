---
aliases: [PerformanceAndDebugging, iOS性能优化, Instruments, 内存管理]
tags: ['05_ComputerScience', 'ProgrammingLanguages', 'Swift', 'iOS']
created: 2026-06-27
updated: 2026-06-27
---

# iOS 性能优化与调试 (Performance & Debugging)

## 一、概述

iOS 应用性能优化涵盖启动时间、内存管理、渲染性能、网络优化和电池消耗等方面。本文档介绍性能分析工具和优化最佳实践。

---

## 二、Instruments 工具

### 2.1 Time Profiler

用于分析 CPU 使用和方法调用时间：

```
1. 打开 Xcode → Product → Profile
2. 选择 Time Profiler 模板
3. 点击 Record 开始录制
4. 操作应用
5. 停止录制，分析结果
```

**关键指标**：
- **Weight**：方法执行时间占比
- **Self**：方法自身执行时间
- **Call Tree**：调用树视图

### 2.2 Leaks

检测内存泄漏：

```swift
// 容易泄漏的代码
class ViewController: UIViewController {
    var closure: (() -> Void)?
    
    override func viewDidLoad() {
        super.viewDidLoad()
        
        // 循环引用
        closure = {
            self.view.backgroundColor = .red  // 强引用 self
        }
    }
}

// 修复
class ViewController: UIViewController {
    var closure: (() -> Void)?
    
    override func viewDidLoad() {
        super.viewDidLoad()
        
        closure = { [weak self] in
            self?.view.backgroundColor = .red
        }
    }
}
```

### 2.3 Allocations

分析内存分配和增长：

**关键指标**：
- **Live Bytes**：当前活跃内存
- **# Living**：活跃对象数
- **Persistent Bytes**：持久内存

### 2.4 Network

分析网络请求：

```
1. 选择 Network 模板
2. 查看请求详情：
   - 请求/响应头
   - 请求/响应体
   - 时间线
   - 错误信息
```

---

## 三、内存管理

### 3.1 ARC 原理

```swift
// 强引用
class Person {
    let name: String
    var apartment: Apartment?
    
    init(name: String) { self.name = name }
    deinit { print("\(name) is being deinitialized") }
}

class Apartment {
    let unit: String
    weak var tenant: Person?  // 弱引用
    
    init(unit: String) { self.unit = unit }
    deinit { print("Apartment \(unit) is being deinitialized") }
}

var person: Person? = Person(name: "John")
var apartment: Apartment? = Apartment(unit: "4A")

person?.apartment = apartment
apartment?.tenant = person

person = nil  // Person 被释放
apartment = nil  // Apartment 被释放
```

### 3.2 内存泄漏检测

```swift
// 使用 deinit 检测
class ViewController: UIViewController {
    deinit {
        print("ViewController deallocated")
    }
}

// 使用 Instruments Leaks
// 使用 Memory Graph Debugger

// 弱引用 self 检测
class ViewModel {
    func fetchData() {
        APIService.shared.request { [weak self] result in
            guard let self = self else {
                print("ViewModel was deallocated")
                return
            }
            // 使用 self
        }
    }
}
```

### 3.3 内存优化

```swift
// 1. 图片内存优化
func loadImage(named: String) -> UIImage? {
    guard let path = Bundle.main.path(forResource: named, ofType: "png") else {
        return nil
    }
    
    // 使用 UIImage(contentsOfFile:) 而不是 UIImage(named:)
    // contentsOfFile 不会缓存
    return UIImage(contentsOfFile: path)
}

// 2. 大图片降采样
func downsample(imageAt imageURL: URL, to pointSize: CGSize, scale: CGFloat) -> UIImage? {
    let imageSourceOptions = [kCGImageSourceShouldCache: false] as CFDictionary
    guard let imageSource = CGImageSourceCreateWithURL(imageURL as CFURL, imageSourceOptions) else {
        return nil
    }
    
    let maxDimensionInPixels = max(pointSize.width, pointSize.height) * scale
    let downsampleOptions = [
        kCGImageSourceCreateThumbnailFromImageAlways: true,
        kCGImageSourceShouldCacheImmediately: true,
        kCGImageSourceCreateThumbnailWithTransform: true,
        kCGImageSourceThumbnailMaxPixelSize: maxDimensionInPixels
    ] as CFDictionary
    
    guard let downsampledImage = CGImageSourceCreateThumbnailAtIndex(imageSource, 0, downsampleOptions) else {
        return nil
    }
    
    return UIImage(cgImage: downsampledImage)
}

// 3. 缓存策略
class ImageCache {
    static let shared = ImageCache()
    
    private let cache = NSCache<NSString, UIImage>()
    
    init() {
        cache.countLimit = 100
        cache.totalCostLimit = 50 * 1024 * 1024 // 50MB
    }
    
    func image(forKey key: String) -> UIImage? {
        cache.object(forKey: key as NSString)
    }
    
    func setImage(_ image: UIImage, forKey key: String) {
        let cost = Int(image.size.width * image.size.height * image.scale * image.scale * 4)
        cache.setObject(image, forKey: key as NSString, cost: cost)
    }
}
```

---

## 四、启动优化

### 4.1 启动时间分析

```swift
// 在 main.swift 中记录启动时间
import Foundation

let startTime = CFAbsoluteTimeGetCurrent()

// 应用启动代码

// 在 applicationDidFinishLaunching 中记录
func application(_ application: UIApplication, didFinishLaunchingWithOptions launchOptions: [UIApplication.LaunchOptionsKey: Any]?) -> Bool {
    let launchTime = CFAbsoluteTimeGetCurrent() - startTime
    print("Launch time: \(launchTime) seconds")
    
    return true
}
```

### 4.2 启动优化策略

| 阶段 | 优化策略 |
|------|---------|
| **pre-main** | 减少动态库数量、减少+load方法 |
| **didFinishLaunching** | 延迟初始化、异步初始化 |
| **首屏渲染** | 减少布局复杂度、预加载数据 |

```swift
// 延迟初始化
class AppDelegate: UIResponder, UIApplicationDelegate {
    func application(_ application: UIApplication, didFinishLaunchingWithOptions launchOptions: [UIApplication.LaunchOptionsKey: Any]?) -> Bool {
        
        // 必须立即初始化
        setupCrashReporting()
        setupAnalytics()
        
        // 延迟初始化
        DispatchQueue.main.async {
            self.setupNotifications()
        }
        
        // 异步初始化
        DispatchQueue.global().async {
            self.setupMLModels()
        }
        
        return true
    }
}
```

---

## 五、渲染优化

### 5.1 离屏渲染

```swift
// 避免离屏渲染
// 错误：使用 cornerRadius + masksToBounds
view.layer.cornerRadius = 10
view.layer.masksToBounds = true  // 触发离屏渲染

// 正确：使用 CAShapeLayer
let path = UIBezierPath(roundedRect: view.bounds, cornerRadius: 10)
let mask = CAShapeLayer()
mask.path = path.cgPath
view.layer.mask = mask

// 或使用预渲染图片
func roundedImage(_ image: UIImage, cornerRadius: CGFloat) -> UIImage {
    let rect = CGRect(origin: .zero, size: image.size)
    UIGraphicsBeginImageContextWithOptions(image.size, false, image.scale)
    
    let path = UIBezierPath(roundedRect: rect, cornerRadius: cornerRadius)
    path.addClip()
    image.draw(in: rect)
    
    let result = UIGraphicsGetImageFromCurrentImageContext()!
    UIGraphicsEndImageContext()
    return result
}
```

### 5.2 图片优化

```swift
// 1. 使用 Asset Catalog
// 自动处理 1x/2x/3x

// 2. 图片解码优化
func decodedImage(_ image: UIImage) -> UIImage? {
    guard let cgImage = image.cgImage else { return nil }
    
    let size = CGSize(width: cgImage.width, height: cgImage.height)
    UIGraphicsBeginImageContextWithOptions(size, true, 1.0)
    
    let context = UIGraphicsGetCurrentContext()
    context?.draw(cgImage, in: CGRect(origin: .zero, size: size))
    
    let decodedImage = UIGraphicsGetImageFromCurrentImageContext()
    UIGraphicsEndImageContext()
    
    return decodedImage
}

// 3. 异步解码
func asyncDecode(_ image: UIImage, completion: @escaping (UIImage?) -> Void) {
    DispatchQueue.global().async {
        let decoded = self.decodedImage(image)
        DispatchQueue.main.async {
            completion(decoded)
        }
    }
}
```

### 5.3 列表优化

```swift
// 1. 使用 Diffable Data Source
// 2. 使用预取
extension ViewController: UITableViewDataSourcePrefetching {
    func tableView(_ tableView: UITableView, prefetchRowsAt indexPaths: [IndexPath]) {
        for indexPath in indexPaths {
            let item = items[indexPath.row]
            ImageLoader.shared.loadImage(for: item.imageURL)
        }
    }
}

// 3. 单元格复用
class CustomCell: UITableViewCell {
    override func prepareForReuse() {
        super.prepareForReuse()
        imageView?.image = nil
        // 取消正在进行的加载
    }
}
```

---

## 六、网络优化

### 6.1 请求优化

```swift
// 1. 请求合并
class RequestCoalescer {
    private var pendingRequests: [URL: [CheckedContinuation<Data, Error>]] = [:]
    private let lock = NSLock()
    
    func request(_ url: URL) async throws -> Data {
        // 检查是否有相同请求
        let (shouldExecute, continuation) = lock.withLock {
            if pendingRequests[url] != nil {
                pendingRequests[url]!.append(CheckedContinuation<Data, Error>())
                return (false, pendingRequests[url]!.last!)
            } else {
                pendingRequests[url] = [CheckedContinuation<Data, Error>()]
                return (true, pendingRequests[url]!.last!)
            }
        }
        
        if shouldExecute {
            do {
                let (data, _) = try await URLSession.shared.data(from: url)
                // 通知所有等待者
                let continuations = lock.withLock {
                    let continuations = pendingRequests[url]!
                    pendingRequests[url] = nil
                    return continuations
                }
                continuations.forEach { $0.resume(returning: data) }
                return data
            } catch {
                let continuations = lock.withLock {
                    let continuations = pendingRequests[url]!
                    pendingRequests[url] = nil
                    return continuations
                }
                continuations.forEach { $0.resume(throwing: error) }
                throw error
            }
        } else {
            return try await withCheckedThrowingContinuation { continuation in
                // 已在上面添加
            }
        }
    }
}

// 2. 请求重试
func retryRequest<T>(
    maxRetries: Int = 3,
    retryDelay: TimeInterval = 1,
    request: @escaping () async throws -> T
) async throws -> T {
    var lastError: Error?
    
    for attempt in 0..<maxRetries {
        do {
            return try await request()
        } catch {
            lastError = error
            
            if attempt < maxRetries - 1 {
                let delay = retryDelay * pow(2, Double(attempt))
                try await Task.sleep(nanoseconds: UInt64(delay * 1_000_000_000))
            }
        }
    }
    
    throw lastError!
}

// 3. 缓存策略
class CachedURLCache: URLCache {
    override func cachedRequest(for request: URLRequest) -> CachedURLResponse? {
        // 自定义缓存逻辑
        return super.cachedRequest(for: request)
    }
}
```

---

## 七、电池优化

### 7.1 定位优化

```swift
// 使用合适的精度
locationManager.desiredAccuracy = kCLLocationAccuracyHundredMeters  // 而不是 Best

// 使用 significant location changes
locationManager.startMonitoringSignificantLocationChanges()

// 按需启动/停止
locationManager.startUpdatingLocation()
// 获取位置后
locationManager.stopUpdatingLocation()
```

### 7.2 后台任务

```swift
// 申请后台任务时间
var backgroundTask: UIBackgroundTaskIdentifier = .invalid

backgroundTask = UIApplication.shared.beginBackgroundTask {
    // 超时处理
    UIApplication.shared.endBackgroundTask(backgroundTask)
    backgroundTask = .invalid
}

// 执行后台工作
DispatchQueue.global().async {
    // 完成工作
    UIApplication.shared.endBackgroundTask(backgroundTask)
    backgroundTask = .invalid
}
```

---

## 八、调试技巧

### 8.1 LLDB 调试

```bash
# 打印视图层次
po self.view.recursiveDescription()

# 打印约束
po self.view.constraintsAffectingLayout(for: .horizontal)

# 条件断点
breakpoint set --file ViewController.swift --line 100 --condition 'self.isLoading'

# 表达式
expression let $view = UIView()
expression self.view.addSubview($view)
```

### 8.2 调试工具

| 工具 | 用途 |
|------|------|
| **View Debugger** | 3D 视图层次 |
| **Memory Graph** | 内存引用关系 |
| **Network Link Conditioner** | 网络条件模拟 |
| **Simulator** | 模拟器调试 |
| **Console** | 系统日志 |

---

## 相关条目

- [[Swift]]
- [[UIKitDeepDive]]
- [[CoreFrameworks]]

## 参考资源

1. Apple. "Instruments Help." developer.apple.com
2. Apple. "Performance Documentation." developer.apple.com
3. Apple. "Memory Management Guide." developer.apple.com
4. raywenderlich.com. "iOS Performance Tuning." raywenderlich.com
