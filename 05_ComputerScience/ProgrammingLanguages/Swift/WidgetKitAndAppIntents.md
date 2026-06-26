---
aliases: [WidgetKit, AppIntents, iOS小组件, LiveActivities]
tags: ['05_ComputerScience', 'ProgrammingLanguages', 'Swift', 'iOS']
created: 2026-06-27
updated: 2026-06-27
---

# WidgetKit 与 App Intents

## 一、概述

WidgetKit 是 Apple 的小组件框架，App Intents 是 Siri/Shortcuts 的现代化 API。两者结合可以创建强大的交互式小组件和快捷指令。

---

## 二、WidgetKit

### 2.1 Widget 基础结构

```swift
import WidgetKit
import SwiftUI

// Timeline Provider
struct WeatherProvider: TimelineProvider {
    func placeholder(in context: Context) -> WeatherEntry {
        WeatherEntry(date: Date(), temperature: 20, city: "北京")
    }
    
    func getSnapshot(in context: Context, completion: @escaping (WeatherEntry) -> Void) {
        let entry = WeatherEntry(date: Date(), temperature: 20, city: "北京")
        completion(entry)
    }
    
    func getTimeline(in context: Context, completion: @escaping (Timeline<WeatherEntry>) -> Void) {
        // 获取最新数据
        let currentDate = Date()
        let entry = WeatherEntry(date: currentDate, temperature: 22, city: "北京")
        
        // 每30分钟刷新一次
        let nextUpdate = Calendar.current.date(byAdding: .minute, value: 30, to: currentDate)!
        let timeline = Timeline(entries: [entry], policy: .after(nextUpdate))
        
        completion(timeline)
    }
}

// Timeline Entry
struct WeatherEntry: TimelineEntry {
    let date: Date
    let temperature: Int
    let city: String
}

// Widget View
struct WeatherWidgetEntryView: View {
    var entry: WeatherProvider.Entry
    
    var body: some View {
        VStack {
            Text(entry.city)
                .font(.headline)
            Text("\(entry.temperature)°C")
                .font(.largeTitle)
            Text(entry.date, style: .time)
                .font(.caption)
        }
        .containerBackground(.fill.tertiary, for: .widget)
    }
}

// Widget 配置
struct WeatherWidget: Widget {
    let kind: String = "WeatherWidget"
    
    var body: some WidgetConfiguration {
        StaticConfiguration(kind: kind, provider: WeatherProvider()) { entry in
            WeatherWidgetEntryView(entry: entry)
        }
        .configurationDisplayName("天气")
        .description("显示当前天气")
        .supportedFamilies([.systemSmall, .systemMedium, .systemLarge])
    }
}
```

### 2.2 可交互 Widget (iOS 17+)

```swift
// 使用 AppIntent 实现可交互 Widget
struct ToggleIntent: AppIntent {
    static var title: LocalizedStringResource = "切换状态"
    static var description = IntentDescription("切换任务完成状态")
    
    @Parameter(title: "任务ID")
    var taskId: String
    
    init() {}
    
    init(taskId: String) {
        self.taskId = taskId
    }
    
    func perform() async throws -> some IntentResult {
        // 更新任务状态
        try await TaskStore.shared.toggleTask(id: taskId)
        return .result()
    }
}

struct TaskWidgetEntryView: View {
    var entry: TaskProvider.Entry
    
    var body: some View {
        VStack {
            ForEach(entry.tasks) { task in
                HStack {
                    Text(task.title)
                    Spacer()
                    Button(intent: ToggleIntent(taskId: task.id.uuidString)) {
                        Image(systemName: task.isCompleted ? "checkmark.circle.fill" : "circle")
                    }
                    .buttonStyle(.plain)
                }
            }
        }
    }
}
```

### 2.3 Lock Screen Widget (iOS 16+)

```swift
// Lock Screen 小组件
struct LockScreenWidget: Widget {
    var body: some WidgetConfiguration {
        StaticConfiguration(kind: "LockScreen", provider: ActivityProvider()) { entry in
            LockScreenWidgetView(entry: entry)
        }
        .configurationDisplayName("步数")
        .description("显示今日步数")
        .supportedFamilies([
            .accessoryCircular,
            .accessoryRectangular,
            .accessoryInline
        ])
    }
}

struct LockScreenWidgetView: View {
    var entry: ActivityEntry
    
    @Environment(\.widgetFamily) var family
    
    var body: some View {
        switch family {
        case .accessoryCircular:
            Gauge(value: entry.progress) {
                Image(systemName: "figure.walk")
            }
            .gaugeStyle(.accessoryCircular)
            
        case .accessoryRectangular:
            VStack(alignment: .leading) {
                Label("\(entry.steps) 步", systemImage: "figure.walk")
                ProgressView(value: entry.progress)
            }
            
        case .accessoryInline:
            Label("\(entry.steps)/\(entry.goal) 步", systemImage: "figure.walk")
            
        default:
            EmptyView()
        }
    }
}
```

### 2.4 Live Activities (iOS 16.1+)

```swift
import ActivityKit

// Activity Attributes
struct DeliveryAttributes: ActivityAttributes {
    public struct ContentState: Codable, Hashable {
        var status: String
        var estimatedTime: String
        var driverName: String
    }
    
    var orderNumber: String
    var restaurantName: String
}

// 启动 Live Activity
func startDeliveryActivity(orderNumber: String, restaurantName: String) {
    let attributes = DeliveryAttributes(
        orderNumber: orderNumber,
        restaurantName: restaurantName
    )
    let state = DeliveryAttributes.ContentState(
        status: "骑手已接单",
        estimatedTime: "30分钟",
        driverName: "张三"
    )
    
    do {
        let activity = try Activity<DeliveryAttributes>.request(
            attributes: attributes,
            content: .init(state: state, staleDate: nil),
            pushType: .token
        )
        print("Activity started: \(activity.id)")
    } catch {
        print("Failed to start activity: \(error)")
    }
}

// 更新 Live Activity
func updateDeliveryActivity(status: String, estimatedTime: String) async {
    for activity in Activity<DeliveryAttributes>.activities {
        let state = DeliveryAttributes.ContentState(
            status: status,
            estimatedTime: estimatedTime,
            driverName: activity.content.state.driverName
        )
        await activity.update(.init(state: state, staleDate: nil))
    }
}

// Live Activity Widget
struct DeliveryLiveActivity: Widget {
    var body: some WidgetConfiguration {
        ActivityConfiguration(for: DeliveryAttributes.self) { context in
            // Lock Screen Banner
            VStack {
                HStack {
                    Text(context.attributes.restaurantName)
                        .font(.headline)
                    Spacer()
                    Text(context.attributes.orderNumber)
                        .font(.caption)
                }
                
                HStack {
                    Text(context.state.status)
                        .font(.title2)
                    Spacer()
                    Text(context.state.estimatedTime)
                }
            }
            .padding()
            
        } dynamicIsland: { context in
            // Dynamic Island
            DynamicIsland {
                DynamicIslandExpandedRegion(.leading) {
                    Image(systemName: "bicycle")
                        .font(.title2)
                }
                DynamicIslandExpandedRegion(.trailing) {
                    Text(context.state.estimatedTime)
                        .font(.caption)
                }
                DynamicIslandExpandedRegion(.bottom) {
                    Text(context.state.status)
                }
            } compactLeading: {
                Image(systemName: "bicycle")
            } compactTrailing: {
                Text(context.state.estimatedTime)
                    .font(.caption2)
            } minimal: {
                Image(systemName: "bicycle")
            }
        }
    }
}
```

---

## 三、App Intents

### 3.1 基础 Intent

```swift
import AppIntents

struct CreateNoteIntent: AppIntent {
    static var title: LocalizedStringResource = "创建笔记"
    static var description = IntentDescription("创建一个新笔记")
    
    @Parameter(title: "标题")
    var title: String
    
    @Parameter(title: "内容")
    var content: String
    
    func perform() async throws -> some IntentResult & ReturnsValue<String> {
        let note = try await NoteStore.shared.create(
            title: title,
            content: content
        )
        return .result(value: note.id.uuidString)
    }
}
```

### 3.2 Entity Query

```swift
struct NoteEntity: AppEntity {
    static var typeDisplayRepresentation = TypeDisplayRepresentation(name: "笔记")
    static var defaultQuery = NoteQuery()
    
    var id: UUID
    var title: String
    var content: String
    
    var displayRepresentation: DisplayRepresentation {
        DisplayRepresentation(title: "\(title)")
    }
}

struct NoteQuery: EntityQuery {
    func entities(for identifiers: [UUID]) async throws -> [NoteEntity] {
        try await NoteStore.shared.notes.filter { identifiers.contains($0.id) }
    }
    
    func suggestedEntities() async throws -> [NoteEntity] {
        try await NoteStore.shared.recentNotes
    }
    
    func entities(matching string: String) async throws -> [NoteEntity] {
        try await NoteStore.shared.search(query: string)
    }
}

// 使用 Entity 的 Intent
struct OpenNoteIntent: AppIntent {
    static var title: LocalizedStringResource = "打开笔记"
    
    @Parameter(title: "笔记")
    var note: NoteEntity
    
    func perform() async throws -> some IntentResult {
        // 打开笔记
        await NoteStore.shared.open(note)
        return .result()
    }
}
```

### 3.3 Shortcuts Integration

```swift
struct ShortcutsProvider: AppShortcutsProvider {
    static var appShortcuts: [AppShortcut] {
        AppShortcut(
            intent: CreateNoteIntent(),
            phrases: [
                "在 \(.applicationName) 创建笔记",
                "用 \(.applicationName) 新建笔记"
            ],
            shortTitle: "创建笔记",
            systemImageName: "plus.circle"
        )
        
        AppShortcut(
            intent: OpenNoteIntent(),
            phrases: [
                "在 \(.applicationName) 打开笔记",
                "用 \(.applicationName) 查看笔记"
            ],
            shortTitle: "打开笔记",
            systemImageName: "doc.text"
        )
    }
}
```

### 3.4 Siri Dialog

```swift
struct SiriNoteIntent: AppIntent {
    static var title: LocalizedStringResource = "Siri 笔记操作"
    static var openAppWhenRun: Bool = false
    
    @Parameter(title: "操作")
    var operation: NoteOperation
    
    @Parameter(title: "标题")
    var title: String
    
    func perform() async throws -> some IntentResult & ProvidesDialog {
        switch operation {
        case .create:
            let note = try await NoteStore.shared.create(title: title, content: "")
            return .result(dialog: "已创建笔记：\(title)")
        case .search:
            let results = try await NoteStore.shared.search(query: title)
            return .result(dialog: "找到 \(results.count) 条笔记")
        case .delete:
            try await NoteStore.shared.delete(title: title)
            return .result(dialog: "已删除笔记：\(title)")
        }
    }
}

enum NoteOperation: String, AppEnum {
    case create
    case search
    case delete
    
    static var typeDisplayRepresentation = TypeDisplayRepresentation(name: "操作")
    static var caseDisplayRepresentations: [NoteOperation: DisplayRepresentation] = [
        .create: "创建",
        .search: "搜索",
        .delete: "删除"
    ]
}
```

---

## 四、Spotlight 集成

### 4.1 Indexed Entity

```swift
import CoreSpotlight

extension NoteEntity {
    var searchableItem: CSSearchableItem {
        let attributeSet = CSSearchableItemAttributeSet(contentType: .text)
        attributeSet.title = title
        attributeSet.contentDescription = content
        attributeSet.keywords = [title, content]
        
        return CSSearchableItem(
            uniqueIdentifier: id.uuidString,
            domainIdentifier: "notes",
            attributeSet: attributeSet
        )
    }
}

// 索引笔记
func indexNote(_ note: NoteEntity) {
    let item = note.searchableItem
    CSSearchableIndex.default().indexSearchableItems([item]) { error in
        if let error = error {
            print("Indexing error: \(error)")
        }
    }
}
```

---

## 相关条目

- [[Swift]]
- [[SwiftUI与iOS开发]]
- [[CoreFrameworks]]

## 参考资源

1. Apple. "WidgetKit Documentation." developer.apple.com
2. Apple. "App Intents Documentation." developer.apple.com
3. Apple. "ActivityKit Documentation." developer.apple.com
4. WWDC 2023. "What's new in WidgetKit"
5. WWDC 2023. "Implement App Intents"
