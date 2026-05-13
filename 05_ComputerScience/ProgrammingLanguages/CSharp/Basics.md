# C# 基础语法

## 数据类型

### 值类型 vs 引用类型

| 特性 | 值类型 | 引用类型 |
|------|--------|---------|
| 存储 | 栈（或内联在堆中） | 堆 |
| 默认值 | 0 或等价 | null |
| 赋值 | 复制值 | 复制引用 |
| 示例 | int, struct, enum | class, string, array |

```csharp
// 值类型
int a = 42;
double b = 3.14;
char c = 'A';
bool flag = true;

// 引用类型
string s = "Hello";
int[] arr = new int[10];
object obj = new object();
```

### 值类型分类

```csharp
// 简单类型
sbyte, byte, short, ushort, int, uint, long, ulong
float, double, decimal
char, bool

// 结构体
struct Point {
    public int X;
    public int Y;
}

// 枚举
enum Color { Red, Green, Blue }
```

### 可空类型

```csharp
int? nullableInt = null;
double? d = 3.14;

// 空合并运算符
int result = nullableInt ?? -1;

// 空条件运算符
int? length = s?.Length;

// 模式匹配
if (nullableInt is int val) {
    Console.WriteLine(val);
}
```

### var 关键字

```csharp
var x = 42;              // int
var items = new List<int>();  // List<int>
var query = from n in numbers where n > 5 select n;  // IEnumerable<int>

// 不能用于字段、参数和返回类型
// var y;  // 错误：必须初始化
```

## 字符串插值

```csharp
string name = "Alice";
int age = 30;

string message = $"姓名: {name}, 年龄: {age}";
string padded = $"数值: {42,10}";        // 右对齐 10 位
string formatted = $"PI: {Math.PI:F2}";  // "PI: 3.14"

// 原始字符串字面量（C# 11）
string json = """
    {
        "name": "Alice",
        "age": 30
    }
    """;
```

## 空条件运算符

```csharp
// ?. 和 ?[]
string? str = null;
int? len = str?.Length;     // null（不抛出异常）

List<int>? list = null;
int? first = list?[0];      // null

// ?? 运算符（提供默认值）
int result = nullableInt ?? 0;

// ??= 运算符（如果为 null 则赋值）
nullableInt ??= 10;

// 空条件+空合并组合
string? maybeNull = GetString();
string value = maybeNull?.Trim() ?? "default";
```

## 属性

```csharp
public class Person {
    // 自动属性
    public string Name { get; set; }
    public int Age { get; init; }  // init-only（只能在构造时设置）

    // 只读自动属性
    public string Id { get; }

    // 带表达式体的属性
    public string Greeting => $"Hello, {Name}";

    // 完整属性定义
    private string _email;
    public string Email {
        get => _email;
        set {
            if (string.IsNullOrWhiteSpace(value))
                throw new ArgumentException("Email不能为空");
            _email = value;
        }
    }

    // 计算属性
    public bool IsAdult => Age >= 18;

    // 私有 set
    public DateTime CreatedAt { get; private set; }
}
```

## 索引器

```csharp
public class StringCollection {
    private List<string> _items = new();

    public string this[int index] {
        get => _items[index];
        set => _items[index] = value;
    }

    public string? this[string name] {
        get => _items.Find(s => s == name);
    }

    public void Add(string item) => _items.Add(item);
}

// 使用
var coll = new StringCollection();
coll.Add("Alice");
coll.Add("Bob");
string first = coll[0];        // "Alice"
string? bob = coll["Bob"];     // "Bob"
```

## Records（C# 9+）

```csharp
// 位置记录（immutable，值相等）
public record Person(string Name, int Age);

// 可变记录
public record Car {
    public string Brand { get; set; }
    public string Model { get; set; }
}

var p1 = new Person("Alice", 30);
var p2 = new Person("Alice", 30);
Console.WriteLine(p1 == p2);  // true（值相等）

// with 表达式创建副本
var p3 = p1 with { Age = 31 };

// 解构
var (name, age) = p1;
```

## 模式匹配

### switch 表达式

```csharp
int number = 3;
string result = number switch {
    1 => "一",
    2 => "二",
    3 => "三",
    _ => "其他"
};

// 元组模式
string Describe((int x, int y) point) => point switch {
    (0, 0) => "原点",
    (0, _) => "Y轴",
    (_, 0) => "X轴",
    _ => "普通点"
};

// 关系模式
string Classify(int age) => age switch {
    < 0 => "无效",
    < 18 => "未成年",
    >= 18 and < 60 => "成年",
    _ => "老年"
};

// 属性模式
string GetDiscount(Customer customer) => customer switch {
    { IsPremium: true, Age: >= 60 } => "30%",
    { IsPremium: true } => "20%",
    { Age: >= 60 } => "15%",
    _ => "0%"
};

// 列表模式（C# 11）
int[] numbers = { 1, 2, 3 };
string desc = numbers switch {
    [0] => "单元素0",
    [1, ..] => "以1开头",
    [.., 3] => "以3结尾",
    _ => "其他"
};
```

## 异常处理

```csharp
try {
    int result = Divide(10, 0);
} catch (DivideByZeroException ex) {
    Console.WriteLine($"除零错误: {ex.Message}");
} catch (Exception ex) when (ex is ArgumentException or InvalidOperationException) {
    Console.WriteLine($"参数或操作错误: {ex.Message}");
} finally {
    Console.WriteLine("清理资源");
}

// 异常过滤器
try {
    ProcessFile(path);
} catch (IOException ex) when (ex is FileNotFoundException || ex is DirectoryNotFoundException) {
    Console.WriteLine("文件或目录不存在");
}

// throw 表达式
string? value = GetValue();
string result = value ?? throw new ArgumentNullException(nameof(value));
```

## LINQ 基础

### 查询语法 vs 方法语法

```csharp
int[] numbers = { 5, 2, 8, 1, 9, 3, 7, 4, 6 };

// 查询语法
var query = from n in numbers
            where n > 5
            orderby n descending
            select n;

// 方法语法
var method = numbers
    .Where(n => n > 5)
    .OrderByDescending(n => n);

// 投影
var squared = from n in numbers
              select new { Number = n, Square = n * n };

// 分组
var groups = from n in numbers
             group n by n % 2 into g
             select new { Key = g.Key, Items = g };

// 连接
var joined = from person in people
             join order in orders on person.Id equals order.PersonId
             select new { person.Name, order.Product };
```

### IEnumerable vs IQueryable

| 特性 | IEnumerable | IQueryable |
|------|-------------|------------|
| 执行 | 内存中 | 可延迟到数据库 |
| 适用 | LINQ to Objects | LINQ to SQL/EF |
| 委托 | Func<T, bool> | Expression<Func<T, bool>> |

```csharp
// IEnumerable：在内存中过滤
IEnumerable<Product> memoryFilter = products
    .Where(p => p.Price > 100);  // 所有数据加载到内存后再过滤

// IQueryable：在数据库端过滤
IQueryable<Product> dbFilter = dbContext.Products
    .Where(p => p.Price > 100);  // 生成 SQL WHERE 子句
```

### 延迟执行

```csharp
var query = numbers.Where(n => {
    Console.WriteLine($"检查: {n}");
    return n > 5;
});

Console.WriteLine("查询已定义但未执行");
// 直到迭代才开始执行
foreach (var n in query) {
    Console.WriteLine($"结果: {n}");
}

// 立即执行
List<int> list = query.ToList();
int count = query.Count();
int first = query.First();
```
