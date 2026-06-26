---
aliases: [NetworkingAndPersistence, iOS网络, iOS持久化, URLSession, SwiftData]
tags: ['05_ComputerScience', 'ProgrammingLanguages', 'Swift', 'iOS']
created: 2026-06-27
updated: 2026-06-27
---

# iOS 网络与持久化 (Networking & Persistence)

## 一、概述

本文档涵盖 iOS 网络编程和数据持久化的核心技术，包括 URLSession、REST API 客户端、SwiftData、Core Data、CloudKit 和 Keychain。

---

## 二、URLSession

### 2.1 基础请求

```swift
// async/await 方式
func fetchData(from url: URL) async throws -> Data {
    let (data, response) = try await URLSession.shared.data(from: url)
    
    guard let httpResponse = response as? HTTPURLResponse,
          (200...299).contains(httpResponse.statusCode) else {
        throw NetworkError.invalidResponse
    }
    
    return data
}

// 使用
Task {
    do {
        let data = try await fetchData(from: URL(string: "https://api.example.com/users")!)
        let users = try JSONDecoder().decode([User].self, from: data)
    } catch {
        print("Error: \(error)")
    }
}
```

### 2.2 URLSessionConfiguration

```swift
// 默认配置
let defaultConfig = URLSessionConfiguration.default
defaultConfig.timeoutIntervalForRequest = 30
defaultConfig.timeoutIntervalForResource = 60
defaultConfig.httpAdditionalHeaders = [
    "Authorization": "Bearer \(token)",
    "Content-Type": "application/json"
]

// 后台配置
let backgroundConfig = URLSessionConfiguration.background(withIdentifier: "com.app.background")
backgroundConfig.isDiscretionary = true
backgroundConfig.sessionSendsLaunchEvents = true

// 临时配置
let ephemeralConfig = URLSessionConfiguration.ephemeral
ephemeralConfig.urlCache = nil
ephemeralConfig.requestCachePolicy = .reloadIgnoringLocalCacheData

// 创建 Session
let session = URLSession(configuration: defaultConfig)
```

### 2.3 请求构建

```swift
struct APIRequest {
    let baseURL: URL
    var path: String
    var method: HTTPMethod
    var headers: [String: String]
    var queryItems: [URLQueryItem]
    var body: Data?
    
    var url: URL {
        var components = URLComponents(url: baseURL.appendingPathComponent(path), resolvingAgainstBaseURL: true)!
        components.queryItems = queryItems.isEmpty ? nil : queryItems
        return components.url!
    }
    
    var urlRequest: URLRequest {
        var request = URLRequest(url: url)
        request.httpMethod = method.rawValue
        request.httpBody = body
        headers.forEach { request.setValue($1, forHTTPHeaderField: $0) }
        return request
    }
}

enum HTTPMethod: String {
    case get = "GET"
    case post = "POST"
    case put = "PUT"
    case patch = "PATCH"
    case delete = "DELETE"
}
```

---

## 三、REST API 客户端

### 3.1 通用 API 客户端

```swift
actor APIClient {
    static let shared = APIClient()
    
    private let session: URLSession
    private let decoder: JSONDecoder
    private let encoder: JSONEncoder
    
    init(session: URLSession = .shared) {
        self.session = session
        
        self.decoder = JSONDecoder()
        decoder.dateDecodingStrategy = .iso8601
        decoder.keyDecodingStrategy = .convertFromSnakeCase
        
        self.encoder = JSONEncoder()
        encoder.dateEncodingStrategy = .iso8601
        encoder.keyEncodingStrategy = .convertToSnakeCase
    }
    
    func request<T: Decodable>(_ endpoint: Endpoint) async throws -> T {
        let (data, response) = try await session.data(for: endpoint.urlRequest)
        
        guard let httpResponse = response as? HTTPURLResponse else {
            throw NetworkError.invalidResponse
        }
        
        switch httpResponse.statusCode {
        case 200...299:
            return try decoder.decode(T.self, from: data)
        case 401:
            throw NetworkError.unauthorized
        case 404:
            throw NetworkError.notFound
        case 500...599:
            throw NetworkError.serverError(httpResponse.statusCode)
        default:
            throw NetworkError.httpError(httpResponse.statusCode)
        }
    }
}

struct Endpoint {
    let path: String
    let method: HTTPMethod
    let queryItems: [URLQueryItem]
    let body: Encodable?
    let headers: [String: String]
    
    var urlRequest: URLRequest {
        var components = URLComponents(string: "https://api.example.com")!
        components.path = path
        components.queryItems = queryItems.isEmpty ? nil : queryItems
        
        var request = URLRequest(url: components.url!)
        request.httpMethod = method.rawValue
        headers.forEach { request.setValue($1, forHTTPHeaderField: $0) }
        
        if let body = body {
            request.httpBody = try? JSONEncoder().encode(body)
        }
        
        return request
    }
}
```

### 3.2 拦截器模式

```swift
protocol RequestInterceptor {
    func adapt(_ urlRequest: URLRequest) async throws -> URLRequest
    func retry(_ request: URLRequest, for session: URLSession, dueTo error: Error) async throws -> (URLRequest, TimeInterval)
}

class AuthInterceptor: RequestInterceptor {
    private let tokenProvider: () async throws -> String
    
    init(tokenProvider: @escaping () async throws -> String) {
        self.tokenProvider = tokenProvider
    }
    
    func adapt(_ urlRequest: URLRequest) async throws -> URLRequest {
        var request = urlRequest
        let token = try await tokenProvider()
        request.setValue("Bearer \(token)", forHTTPHeaderField: "Authorization")
        return request
    }
    
    func retry(_ request: URLRequest, for session: URLSession, dueTo error: Error) async throws -> (URLRequest, TimeInterval) {
        if case NetworkError.unauthorized = error {
            // 刷新 token
            let newToken = try await tokenProvider()
            var newRequest = request
            newRequest.setValue("Bearer \(newToken)", forHTTPHeaderField: "Authorization")
            return (newRequest, 0)
        }
        throw error
    }
}
```

---

## 四、图片加载与缓存

### 4.1 图片缓存

```swift
actor ImageCache {
    static let shared = ImageCache()
    
    private let memoryCache = NSCache<NSString, UIImage>()
    private var loadingTasks: [URL: Task<UIImage, Error>] = [:]
    
    init() {
        memoryCache.countLimit = 100
        memoryCache.totalCostLimit = 50 * 1024 * 1024 // 50MB
    }
    
    func image(for url: URL) async throws -> UIImage {
        let key = url.absoluteString as NSString
        
        // 检查内存缓存
        if let cached = memoryCache.object(forKey: key) {
            return cached
        }
        
        // 检查是否有进行中的加载
        if let existingTask = loadingTasks[url] {
            return try await existingTask.value
        }
        
        // 创建新加载任务
        let task = Task<UIImage, Error> {
            let (data, _) = try await URLSession.shared.data(from: url)
            guard let image = UIImage(data: data) else {
                throw ImageError.invalidData
            }
            memoryCache.setObject(image, forKey: key)
            return image
        }
        
        loadingTasks[url] = task
        
        do {
            let image = try await task.value
            loadingTasks[url] = nil
            return image
        } catch {
            loadingTasks[url] = nil
            throw error
        }
    }
}
```

---

## 五、SwiftData 深度

### 5.1 复杂查询

```swift
import SwiftData

@Model
class Article {
    var title: String
    var content: String
    var publishedAt: Date
    var isPublished: Bool
    var tags: [String]
    
    @Relationship
    var author: Author?
    
    init(title: String, content: String) {
        self.title = title
        self.content = content
        self.publishedAt = Date()
        self.isPublished = false
        self.tags = []
    }
}

// 复杂查询
struct ArticleListView: View {
    @Query(
        filter: #Predicate<Article> { article in
            article.isPublished && article.publishedAt > Date().addingTimeInterval(-86400 * 7)
        },
        sort: \Article.publishedAt,
        order: .reverse
    )
    private var recentArticles: [Article]
    
    @Query(
        filter: #Predicate<Article> { article in
            article.tags.contains("swift")
        }
    )
    private var swiftArticles: [Article]
}
```

### 5.2 数据迁移

```swift
// 版本化模型
let schema = Schema([
    User.self,
    Article.self
], version: Schema.Version(2, 0, 0))

// 迁移计划
let migrationPlan = SchemaMigrationPlan(
    schemas: [schemaV1, schemaV2],
    stages: [
        .lightweight(
            fromVersion: Schema.Version(1, 0, 0),
            toVersion: Schema.Version(2, 0, 0)
        )
    ]
)

// 创建容器
let container = try ModelContainer(
    for: schema,
    migrationPlan: migrationPlan
)
```

---

## 六、CloudKit

### 6.1 CloudKit 基础

```swift
import CloudKit

class CloudKitManager {
    let container = CKContainer.default()
    let database: CKDatabase
    
    init() {
        database = container.privateCloudDatabase
    }
    
    // 保存记录
    func saveUser(name: String, email: String) async throws -> CKRecord {
        let record = CKRecord(recordType: "User")
        record["name"] = name
        record["email"] = email
        
        return try await database.save(record)
    }
    
    // 查询记录
    func fetchUsers() async throws -> [CKRecord] {
        let predicate = NSPredicate(value: true)
        let query = CKQuery(recordType: "User", predicate: predicate)
        
        let (results, _) = try await database.records(matching: query)
        return results.compactMap { try? $0.1.get() }
    }
    
    // 订阅更新
    func subscribeToChanges() async throws {
        let predicate = NSPredicate(value: true)
        let subscription = CKQuerySubscription(
            recordType: "User",
            predicate: predicate,
            options: [.firesOnRecordCreation, .firesOnRecordUpdate]
        )
        
        let notificationInfo = CKSubscription.NotificationInfo()
        notificationInfo.alertBody = "用户数据已更新"
        subscription.notificationInfo = notificationInfo
        
        try await database.save(subscription)
    }
}
```

---

## 七、Keychain

### 7.1 Keychain 封装

```swift
import Security

class KeychainManager {
    static let shared = KeychainManager()
    
    func save(_ data: Data, for key: String) throws {
        let query: [String: Any] = [
            kSecClass as String: kSecClassGenericPassword,
            kSecAttrAccount as String: key,
            kSecValueData as String: data
        ]
        
        // 删除现有项目
        SecItemDelete(query as CFDictionary)
        
        // 添加新项目
        let status = SecItemAdd(query as CFDictionary, nil)
        
        guard status == errSecSuccess else {
            throw KeychainError.saveFailed(status)
        }
    }
    
    func load(for key: String) throws -> Data? {
        let query: [String: Any] = [
            kSecClass as String: kSecClassGenericPassword,
            kSecAttrAccount as String: key,
            kSecReturnData as String: true
        ]
        
        var result: AnyObject?
        let status = SecItemCopyMatching(query as CFDictionary, &result)
        
        guard status == errSecSuccess else {
            if status == errSecItemNotFound {
                return nil
            }
            throw KeychainError.loadFailed(status)
        }
        
        return result as? Data
    }
    
    func delete(for key: String) throws {
        let query: [String: Any] = [
            kSecClass as String: kSecClassGenericPassword,
            kSecAttrAccount as String: key
        ]
        
        let status = SecItemDelete(query as CFDictionary)
        
        guard status == errSecSuccess || status == errSecItemNotFound else {
            throw KeychainError.deleteFailed(status)
        }
    }
}

// 便捷方法
extension KeychainManager {
    func saveString(_ string: String, for key: String) throws {
        guard let data = string.data(using: .utf8) else {
            throw KeychainError.encodingFailed
        }
        try save(data, for: key)
    }
    
    func loadString(for key: String) throws -> String? {
        guard let data = try load(for: key) else { return nil }
        return String(data: data, encoding: .utf8)
    }
    
    func saveCodable<T: Codable>(_ value: T, for key: String) throws {
        let data = try JSONEncoder().encode(value)
        try save(data, for: key)
    }
    
    func loadCodable<T: Codable>(_ type: T.Type, for key: String) throws -> T? {
        guard let data = try load(for: key) else { return nil }
        return try JSONDecoder().decode(type, from: data)
    }
}

// 存储 Token
extension KeychainManager {
    func saveToken(_ token: String) throws {
        try saveString(token, for: "auth_token")
    }
    
    func loadToken() throws -> String? {
        try loadString(for: "auth_token")
    }
    
    func deleteToken() throws {
        try delete(for: "auth_token")
    }
}
```

---

## 八、UserDefaults

### 8.1 UserDefaults 封装

```swift
@propertyWrapper
struct UserDefault<T> {
    let key: String
    let defaultValue: T
    
    var wrappedValue: T {
        get { UserDefaults.standard.object(forKey: key) as? T ?? defaultValue }
        set { UserDefaults.standard.set(newValue, forKey: key) }
    }
}

// 使用
struct Settings {
    @UserDefault(key: "isDarkMode", defaultValue: false)
    static var isDarkMode: Bool
    
    @UserDefault(key: "fontSize", defaultValue: 16)
    static var fontSize: Int
    
    @UserDefault(key: "username", defaultValue: "")
    static var username: String
}
```

---

## 九、文件管理

### 9.1 文件操作

```swift
class FileManagerHelper {
    static let shared = FileManagerHelper()
    
    let documentsDirectory: URL = {
        FileManager.default.urls(for: .documentDirectory, in: .userDomainMask)[0]
    }()
    
    let cachesDirectory: URL = {
        FileManager.default.urls(for: .cachesDirectory, in: .userDomainMask)[0]
    }()
    
    // 保存数据
    func saveData(_ data: Data, to filename: String, in directory: URL? = nil) throws {
        let dir = directory ?? documentsDirectory
        let fileURL = dir.appendingPathComponent(filename)
        try data.write(to: fileURL)
    }
    
    // 加载数据
    func loadData(from filename: String, in directory: URL? = nil) throws -> Data {
        let dir = directory ?? documentsDirectory
        let fileURL = dir.appendingPathComponent(filename)
        return try Data(contentsOf: fileURL)
    }
    
    // 删除文件
    func deleteFile(_ filename: String, in directory: URL? = nil) throws {
        let dir = directory ?? documentsDirectory
        let fileURL = dir.appendingPathComponent(filename)
        try FileManager.default.removeItem(at: fileURL)
    }
    
    // 列出文件
    func listFiles(in directory: URL? = nil) throws -> [URL] {
        let dir = directory ?? documentsDirectory
        return try FileManager.default.contentsOfDirectory(
            at: dir,
            includingPropertiesForKeys: [.creationDateKey]
        )
    }
}
```

---

## 相关条目

- [[Swift]]
- [[SwiftConcurrency]]
- [[CoreFrameworks]]

## 参考资源

1. Apple. "URLSession Documentation." developer.apple.com
2. Apple. "SwiftData Documentation." developer.apple.com
3. Apple. "CloudKit Documentation." developer.apple.com
4. Apple. "Keychain Services Documentation." developer.apple.com
