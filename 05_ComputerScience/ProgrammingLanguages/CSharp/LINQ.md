# LINQ 深入

## 标准查询运算符

### 过滤：Where / OfType

```csharp
int[] numbers = { 1, 2, 3, 4, 5, 6, 7, 8 };

// Where
var evens = numbers.Where(n => n % 2 == 0);
var odds = numbers.Where((n, idx) => n % 2 != 0 && idx > 2);

// OfType：按类型过滤
object[] mixed = { 1, "hello", 2.5, "world", 42 };
var strings = mixed.OfType<string>();  // "hello", "world"
var ints = mixed.OfType<int>();        // 1, 42
```

### 投影：Select / SelectMany

```csharp
// Select：一对一映射
var squares = numbers.Select(n => n * n);

// 索引投影
var indexed = numbers.Select((n, i) => $"索引{i}: {n}");

// SelectMany：一对多展开（扁平化）
var nested = new[] {
    new[] { 1, 2, 3 },
    new[] { 4, 5, 6 },
    new[] { 7, 8, 9 }
};

var flat = nested.SelectMany(arr => arr);
// 1, 2, 3, 4, 5, 6, 7, 8, 9

// 查询语法
var flat2 = from arr in nested
            from n in arr
            select n;

// SelectMany 带结果选择器
var cartesian = from a in new[] { 1, 2, 3 }
                from b in new[] { 'A', 'B' }
                select $"{a}{b}";
// 1A, 1B, 2A, 2B, 3A, 3B
```

### 排序：OrderBy / ThenBy

```csharp
var sorted = numbers.OrderBy(n => n);                 // 升序
var desc = numbers.OrderByDescending(n => n);         // 降序

// 多级排序
var people = new List<Person> { ... };
var ordered = people
    .OrderBy(p => p.LastName)
    .ThenBy(p => p.FirstName)
    .ThenByDescending(p => p.Age);

// 自定义比较器
var custom = numbers.OrderBy(n => n, new MyComparer());
```

### 分组：GroupBy

```csharp
var products = new List<Product> { ... };

// 按类别分组
var byCategory = products.GroupBy(p => p.Category);

foreach (var group in byCategory) {
    Console.WriteLine($"类别: {group.Key}, 数量: {group.Count()}");

    foreach (var product in group) {
        Console.WriteLine($"  - {product.Name}");
    }
}

// 分组后聚合
var summary = products
    .GroupBy(p => p.Category)
    .Select(g => new {
        Category = g.Key,
        Count = g.Count(),
        TotalPrice = g.Sum(p => p.Price),
        AvgPrice = g.Average(p => p.Price),
        MaxPrice = g.Max(p => p.Price),
        MinPrice = g.Min(p => p.Price)
    });

// 复合分组键
var byCategoryAndBrand = products
    .GroupBy(p => new { p.Category, p.Brand });
```

### 连接：Join / GroupJoin

```csharp
// 内连接
var innerJoin = from customer in customers
                join order in orders on customer.Id equals order.CustomerId
                select new { customer.Name, order.OrderDate, order.Total };

// 方法语法
var innerJoin2 = customers
    .Join(orders,
        c => c.Id,
        o => o.CustomerId,
        (c, o) => new { c.Name, o.OrderDate, o.Total });

// GroupJoin（左连接）
var groupJoin = from customer in customers
                join order in orders on customer.Id equals order.CustomerId into orderGroup
                select new {
                    customer.Name,
                    Orders = orderGroup.DefaultIfEmpty()
                };

// 左外连接
var leftJoin = from customer in customers
               join order in orders on customer.Id equals order.CustomerId into orderGroup
               from order in orderGroup.DefaultIfEmpty()
               select new {
                   customer.Name,
                   OrderDate = order?.OrderDate,
                   Total = order?.Total ?? 0
               };
```

### 聚合：Aggregate

```csharp
int[] numbers = { 1, 2, 3, 4, 5 };

int sum = numbers.Sum();
double avg = numbers.Average();
int count = numbers.Count();
int min = numbers.Min();
int max = numbers.Max();

// Aggregate：自定义累积
int product = numbers.Aggregate((a, b) => a * b);  // 120

string sentence = new[] { "I", "love", "LINQ" }
    .Aggregate((a, b) => $"{a} {b}");
// "I love LINQ"

// Aggregate 带种子值
int factorial = numbers.Aggregate(1, (acc, n) => acc * n);  // 120
```

### 限定符：Any / All / Contains

```csharp
bool anyEven = numbers.Any(n => n % 2 == 0);      // true
bool allEven = numbers.All(n => n % 2 == 0);      // false
bool hasThree = numbers.Contains(3);               // true

// Any() 无参数：检查是否包含元素
bool nonEmpty = numbers.Any();                     // true
```

### 元素操作：First / Single / Last / ElementAt

```csharp
int first = numbers.First();           // 第一个，空集合抛出异常
int firstOr = numbers.FirstOrDefault();  // 默认值 0

int single = numbers.Single(n => n == 3);  // 只有一个匹配
int singleOr = numbers.SingleOrDefault(n => n == 99);  // 0

int last = numbers.Last();             // 最后一个
int elementAt = numbers.ElementAt(2);  // 按索引

// 自定义默认值
int firstCustom = numbers
    .FirstOrDefault() != 0 ? numbers.First() : -1;

// 更简洁的方式（.NET 6+）
int firstFallback = numbers.FirstOrDefault(-1);
```

### 分区：Skip / Take

```csharp
// 分页
int pageSize = 3;
int pageNumber = 2;

var page = numbers
    .Skip((pageNumber - 1) * pageSize)
    .Take(pageSize);

// TakeWhile / SkipWhile
var taken = numbers.TakeWhile(n => n < 4);  // 1, 2, 3
var skipped = numbers.SkipWhile(n => n < 4); // 4, 5, 6, 7, 8

// Chunk（.NET 6+）
var chunks = numbers.Chunk(3);
// [[1,2,3], [4,5,6], [7,8]]
```

### 集合操作：Distinct / Union / Intersect / Except

```csharp
int[] a = { 1, 2, 3, 4, 5 };
int[] b = { 4, 5, 6, 7, 8 };

var distinct = a.Distinct();
var union = a.Union(b);          // 1-8（去重并集）
var intersect = a.Intersect(b);  // 4, 5
var except = a.Except(b);        // 1, 2, 3

// DistinctBy / UnionBy / IntersectBy / ExceptBy（.NET 6+）
var distinctByName = people.DistinctBy(p => p.Name);
```

### 生成操作：Range / Repeat / Empty

```csharp
var range = Enumerable.Range(0, 10);     // 0-9
var repeat = Enumerable.Repeat("A", 5);  // A, A, A, A, A
var empty = Enumerable.Empty<int>();     // 空集合

var squares = Enumerable.Range(1, 10).Select(n => n * n);
```

### 转换：ToArray / ToList / ToDictionary / ToLookup

```csharp
int[] arr = numbers.ToArray();
List<int> list = numbers.ToList();

// ToDictionary（key 必须唯一）
Dictionary<int, string> dict = people.ToDictionary(p => p.Id, p => p.Name);

// ToLookup（key 可重复）
var lookup = products.ToLookup(p => p.Category);
foreach (var product in lookup["Electronics"]) {
    Console.WriteLine(product.Name);
}

// ToHashSet
HashSet<int> set = numbers.ToHashSet();

// Cast / OfType
ArrayList oldList = new ArrayList { 1, 2, 3 };
IEnumerable<int> typed = oldList.Cast<int>();
```

## LINQ to SQL / Entities

```csharp
using var db = new AppDbContext();

// 查询直接翻译为 SQL
var results = from p in db.Products
              where p.Price > 100 && p.IsActive
              orderby p.Name
              select new { p.Name, p.Price };

// 分组聚合（SQL GROUP BY）
var categoryStats = db.Products
    .GroupBy(p => p.Category)
    .Select(g => new {
        Category = g.Key,
        Count = g.Count(),
        AvgPrice = g.Average(p => p.Price)
    });

// 分页
var page = db.Orders
    .Where(o => o.OrderDate > DateTime.UtcNow.AddDays(-30))
    .OrderByDescending(o => o.OrderDate)
    .Skip((pageNum - 1) * pageSize)
    .Take(pageSize)
    .ToList();
```

## 表达式树 vs 委托

```csharp
// 委托：编译为 IL，在内存中执行
Func<int, bool> isEven = n => n % 2 == 0;

// 表达式树：编译为数据结构，可被分析/转换
Expression<Func<int, bool>> expr = n => n % 2 == 0;

// 分析表达式树
var body = (BinaryExpression)expr.Body;
var left = (ParameterExpression)body.Left;
var right = (ConstantExpression)body.Right;
Console.WriteLine($"{left.Name} {body.NodeType} {right.Value}");
// "n Modulo 2"

// 编译为委托
var compiled = expr.Compile();
bool result = compiled(4);  // true
```

## 自定义 LINQ 扩展

```csharp
public static class LinqExtensions {
    // 自定义 Where 变体
    public static IEnumerable<T> WhereNot<T>(
        this IEnumerable<T> source,
        Func<T, bool> predicate) {
        return source.Where(x => !predicate(x));
    }

    // 自定义 Aggregate
    public static IEnumerable<T> TakeEvery<T>(
        this IEnumerable<T> source,
        int step) {
        return source.Where((_, idx) => idx % step == 0);
    }

    // 自定义 Let 操作
    public static IEnumerable<TResult> Let<TSource, TResult>(
        this IEnumerable<TSource> source,
        Func<IEnumerable<TSource>, IEnumerable<TResult>> selector) {
        return selector(source);
    }

    // 自定义操作符
    public static IEnumerable<T> Interleave<T>(
        this IEnumerable<T> first,
        IEnumerable<T> second) {
        using var e1 = first.GetEnumerator();
        using var e2 = second.GetEnumerator();
        bool has1, has2;

        while ((has1 = e1.MoveNext()) | (has2 = e2.MoveNext())) {
            if (has1) yield return e1.Current;
            if (has2) yield return e2.Current;
        }
    }
}

// 使用
var result = numbers
    .WhereNot(n => n == 0)
    .TakeEvery(2)
    .OrderByDescending(n => n);
```
