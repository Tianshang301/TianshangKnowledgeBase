---
aliases: [Async]
tags: ['ProgrammingLanguages', 'CSharp', 'Async']
---

# C# 异步编程

## Task-Based Asynchronous Pattern (TAP)

### 基本用法

```csharp
// 同步方法
string DownloadContent(string url) {
    using var client = new HttpClient();
    return client.GetStringAsync(url).GetAwaiter().GetResult();
}

// 异步方法
async Task<string> DownloadContentAsync(string url) {
    using var client = new HttpClient();
    return await client.GetStringAsync(url);
}

// 调用
string result = await DownloadContentAsync("https://example.com");
```

### async/await 规则

- 方法签名包含 `async` 关键字
- 返回类型为 `Task`、`Task<T>`、`ValueTask<T>` 或 `void`（仅事件处理）
- 方法名建议以 `Async` 结尾
- `await` 等待一个 awaitable 对象

```csharp
// 正确模式
public async Task<string> ProcessAsync() {
    var data = await FetchDataAsync();
    var result = await ComputeAsync(data);
    return result;
}

// async void 仅用于事件处理器
public async void OnButtonClick(object sender, EventArgs e) {
    await ProcessAsync();
}
```

## Task 与 ValueTask

```csharp
// Task：引用类型，适合异步结果
Task<int> task = GetResultAsync();

// ValueTask：值类型，减少堆分配，适合同步完成的情况
public ValueTask<int> GetCachedResultAsync() {
    if (_cache.TryGetValue(key, out int value)) {
        return new ValueTask<int>(value);  // 同步完成，无分配
    }
    return new ValueTask<int>(LoadFromDbAsync());  // 真正的异步
}
```

## Task.WhenAll / WhenAny

```csharp
// 并行执行多个任务
Task task1 = DownloadAsync("url1");
Task task2 = DownloadAsync("url2");
Task task3 = DownloadAsync("url3");

// 等待所有完成
await Task.WhenAll(task1, task2, task3);

// 等待任意一个完成
Task first = await Task.WhenAny(task1, task2, task3);

// 收集结果
Task<string>[] downloads = urls.Select(url => DownloadAsync(url)).ToArray();
string[] results = await Task.WhenAll(downloads);

// 超时控制
var timeoutTask = Task.Delay(TimeSpan.FromSeconds(5));
var workTask = ProcessAsync();

if (await Task.WhenAny(workTask, timeoutTask) == timeoutTask) {
    throw new TimeoutException("操作超时");
}
```

## CancellationToken

```csharp
public async Task ProcessAsync(CancellationToken cancellationToken = default) {
    for (int i = 0; i < 100; i++) {
        cancellationToken.ThrowIfCancellationRequested();
        // 或
        if (cancellationToken.IsCancellationRequested) {
            await CleanupAsync();
            break;
        }

        await Task.Delay(100, cancellationToken);
    }
}

// 创建 CancellationTokenSource
using var cts = new CancellationTokenSource();
cts.CancelAfter(TimeSpan.FromSeconds(5));  // 5秒后取消

try {
    await ProcessAsync(cts.Token);
} catch (OperationCanceledException) {
    Console.WriteLine("操作已取消");
}

// 链接 Token
using var linkedCts = CancellationTokenSource.CreateLinkedTokenSource(cts1.Token, cts2.Token);
await ProcessAsync(linkedCts.Token);
```

## ConfigureAwait

```csharp
// ConfigureAwait(false)：不回到原 SynchronizationContext
// 适用于库代码，避免死锁
public async Task<string> ReadFileAsync(string path) {
    using var reader = File.OpenText(path);
    string content = await reader.ReadToEndAsync().ConfigureAwait(false);
    // 此处不在原上下文中
    return content;
}

// UI 代码（WPF/WinForms）需要回到原上下文
public async Task UpdateUIAsync() {
    string data = await FetchDataAsync();  // 自动回到 UI 线程
    this.TextBox.Text = data;
}
```

## 异步流（IAsyncEnumerable）

```csharp
// 异步流生成器
public async IAsyncEnumerable<int> GenerateSequenceAsync(
    int start, int count,
    [EnumeratorCancellation] CancellationToken cancellationToken = default) {
    for (int i = start; i < start + count; i++) {
        await Task.Delay(100, cancellationToken);
        yield return i;
    }
}

// 消费异步流
await foreach (var number in GenerateSequenceAsync(0, 10)) {
    Console.WriteLine(number);
}

// 带取消
await foreach (var item in GenerateSequenceAsync(0, 100)
    .WithCancellation(cancellationToken)) {
    Process(item);
}

// LINQ 操作（需要 System.Linq.Async）
var result = await GenerateSequenceAsync(0, 100)
    .Where(x => x % 2 == 0)
    .Select(x => x * x)
    .ToListAsync();
```

## 后台任务

```csharp
// Fire-and-forget 模式（谨慎使用）
public void FireAndForget(Task task) {
    _ = task.ContinueWith(t => {
        Log.Error(t.Exception, "后台任务失败");
    }, TaskContinuationOptions.OnlyOnFaulted);
}

// BackgroundService（ASP.NET Core）
public class MyBackgroundService : BackgroundService {
    protected override async Task ExecuteAsync(CancellationToken stoppingToken) {
        while (!stoppingToken.IsCancellationRequested) {
            await DoWorkAsync();
            await Task.Delay(TimeSpan.FromMinutes(5), stoppingToken);
        }
    }
}

// 队列处理
public class BackgroundTaskQueue {
    private readonly Channel<Func<CancellationToken, ValueTask>> _queue =
        Channel.CreateBounded<Func<CancellationToken, ValueTask>>(100);

    public async Task QueueAsync(Func<CancellationToken, ValueTask> task) {
        await _queue.Writer.WriteAsync(task);
    }

    public async Task ProcessAsync(CancellationToken cancellationToken) {
        await foreach (var task in _queue.Reader.ReadAllAsync(cancellationToken)) {
            await task(cancellationToken);
        }
    }
}
```

## 常见陷阱

### 死锁：.Result / .Wait

```csharp
// ❌ 危险：同步阻塞异步代码
public string GetData() {
    return FetchDataAsync().Result;  // 可能死锁！
}

// ❌
public void Process() {
    FetchDataAsync().Wait();  // 死锁！
}

// ✅ 正确：使用 async/await 一直到顶层
public async Task<string> GetDataAsync() {
    return await FetchDataAsync();
}

// ✅ 或使用 ConfigureAwait(false)（库代码）
public string GetData() {
    return FetchDataAsync().GetAwaiter().GetResult();
}
```

### Sync-over-Async

```csharp
// ❌ 不推荐
Task.Run(async () => await SomeAsyncMethod()).Result;

// ✅ 推荐：使用异步路径
await SomeAsyncMethod();
```

### 任务未等待

```csharp
// ❌ 忘记 await
var task = ProcessAsync();
// task 未被等待，异常可能丢失

// ✅ 存储并等待
await ProcessAsync();

// ✅ 或显式处理
_ = ProcessAsync().ContinueWith(t => {
    Log.Error(t.Exception, "错误");
}, TaskContinuationOptions.OnlyOnFaulted);
```

### 异步序列错误处理

```csharp
// await foreach 中的异常处理
try {
    await foreach (var item in GetAsyncEnumerable()) {
        Process(item);
    }
} catch (Exception ex) {
    Console.WriteLine($"枚举时出错: {ex.Message}");
}
```

## 完整示例

```csharp
public class DataProcessor {
    private readonly HttpClient _httpClient;
    private readonly ILogger<DataProcessor> _logger;

    public DataProcessor(HttpClient httpClient, ILogger<DataProcessor> logger) {
        _httpClient = httpClient;
        _logger = logger;
    }

    public async Task<IReadOnlyList<Result>> ProcessUrlsAsync(
        IEnumerable<string> urls,
        CancellationToken cancellationToken = default) {
        var tasks = urls.Select(url => ProcessSingleUrlAsync(url, cancellationToken));
        var results = await Task.WhenAll(tasks);
        return results.Where(r => r != null).ToList()!;
    }

    private async Task<Result?> ProcessSingleUrlAsync(
        string url,
        CancellationToken cancellationToken) {
        try {
            _logger.LogInformation("开始处理: {Url}", url);

            var response = await _httpClient
                .GetAsync(url, HttpCompletionOption.ResponseHeadersRead, cancellationToken)
                .ConfigureAwait(false);

            response.EnsureSuccessStatusCode();

            var content = await response.Content
                .ReadAsStringAsync(cancellationToken)
                .ConfigureAwait(false);

            return new Result(url, content.Length);
        } catch (OperationCanceledException) {
            _logger.LogWarning("已取消: {Url}", url);
            return null;
        } catch (HttpRequestException ex) {
            _logger.LogError(ex, "请求失败: {Url}", url);
            return null;
        }
    }
}

public record Result(string Url, int ContentLength);
```
