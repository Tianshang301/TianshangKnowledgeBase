# C++11/14/17/20/23 新特性

## C++11

### auto 与 decltype

```cpp
auto x = 42;                    // int
auto& y = x;                    // int&
const auto* p = &x;             // const int*

template<typename T1, typename T2>
auto add(T1 a, T2 b) -> decltype(a + b) {
    return a + b;
}
```

### 范围 for 循环

```cpp
vector<int> vec = {1, 2, 3, 4, 5};
for (const auto& v : vec) {
    cout << v << " ";
}
```

### 移动语义与右值引用

```cpp
string s1 = "hello";
string s2 = move(s1);           // 转移所有权

void process(string&& s) {      // 右值引用
    // 仅接受临时对象
}

template<typename T>
void wrapper(T&& arg) {
    func(forward<T>(arg));      // 完美转发
}
```

### 智能指针

```cpp
auto p1 = make_unique<int>(42);     // unique_ptr
auto p2 = make_shared<string>("hello");  // shared_ptr
weak_ptr<string> wp = p2;           // weak_ptr
```

### Lambda 表达式

```cpp
auto lambda = [capture](params) -> ret { body };

// 泛型 lambda（C++14）
auto generic = [](auto a, auto b) { return a + b; };

// 可变 lambda
auto counter = [cnt = 0]() mutable { return ++cnt; };
```

### 可变模板参数

```cpp
template<typename... Args>
auto sum(Args... args) {
    return (... + args);  // C++17 fold expression
}

template<typename T, typename... Args>
auto make_unique(Args&&... args) {
    return unique_ptr<T>(new T(forward<Args>(args)...));
}

// 递归展开
void print() {}
template<typename T, typename... Args>
void print(const T& first, const Args&... rest) {
    cout << first << " ";
    print(rest...);
}
```

### std::thread

```cpp
#include <thread>
#include <chrono>

void worker(int id) {
    this_thread::sleep_for(chrono::seconds(1));
    cout << "Worker " << id << " done\n";
}

vector<thread> threads;
for (int i = 0; i < 4; i++) {
    threads.emplace_back(worker, i);
}
for (auto& t : threads) {
    t.join();
}
```

### std::chrono

```cpp
using namespace chrono;

auto start = high_resolution_clock::now();
// 任务
auto end = high_resolution_clock::now();
auto duration = duration_cast<milliseconds>(end - start).count();

// 等待
this_thread::sleep_for(100ms);
this_thread::sleep_until(system_clock::now() + 5s);
```

### 其他 C++11 特性

```cpp
// nullptr
int* p = nullptr;

// override / final
class Derived : public Base {
    void foo() override;
};

// 委托构造函数
class Foo {
    Foo() : Foo(0, "") {}
    Foo(int x, string s) : x_(x), s_(s) {}
};

// 类内初始化
class Bar {
    int x = 0;
    string s = "default";
};

// static_assert
static_assert(sizeof(int) == 4, "int must be 4 bytes");

// enum class
enum class Color { Red, Green, Blue };
Color c = Color::Red;

// std::tuple
auto tup = make_tuple(42, "hello", 3.14);
auto [a, b, c] = tup;  // C++17
```

## C++14

### 泛型 Lambda

```cpp
auto lambda = [](auto a, auto b) { return a + b; };
cout << lambda(1, 2);         // 3
cout << lambda(1.5, 2.5);     // 4.0
cout << lambda(string("a"), string("b"));  // "ab"
```

### decltype(auto)

```cpp
template<typename F, typename... Args>
decltype(auto) invoke(F&& f, Args&&... args) {
    return forward<F>(f)(forward<Args>(args)...);
}

int x = 42;
decltype(auto) y = (x);  // int&（括号导致返回引用类型）
```

### constexpr 增强

```cpp
constexpr int factorial(int n) {
    if (n <= 1) return 1;     // C++14 允许 constexpr 函数中的分支
    return n * factorial(n - 1);
}

// C++14 允许 constexpr 中的循环和变量修改
constexpr int sum(int n) {
    int result = 0;
    for (int i = 1; i <= n; i++) {
        result += i;
    }
    return result;
}
```

### 其他 C++14 特性

```cpp
// 二进制字面量
int bin = 0b101010;

// 数字分隔符
int million = 1'000'000;

// make_unique
auto ptr = make_unique<int>(42);

// shared_ptr 数组
auto arr = make_shared<int[]>(100);

// 变量模板
template<typename T>
constexpr T pi = T(3.1415926535897932385);
cout << pi<float>;  // 3.14159
```

## C++17

### 结构化绑定

```cpp
// 数组
int arr[3] = {1, 2, 3};
auto [a, b, c] = arr;

// tuple
auto tup = make_tuple(42, "hello", 3.14);
auto [i, s, d] = tup;

// map
map<string, int> mp = {{"alice", 90}, {"bob", 85}};
for (const auto& [key, value] : mp) {
    cout << key << ": " << value << "\n";
}

// 自定义结构体
struct Point { int x, y; };
Point p{10, 20};
auto [x, y] = p;
```

### if constexpr

```cpp
template<typename T>
auto getValue(T t) {
    if constexpr (is_pointer_v<T>) {
        return *t;
    } else if constexpr (is_same_v<T, string>) {
        return stoi(t);
    } else {
        return t;
    }
}

// 编译期分支，不会生成未使用的代码
template<typename T>
string typeName() {
    if constexpr (is_same_v<T, int>) return "int";
    else if constexpr (is_same_v<T, double>) return "double";
    else return "unknown";
}
```

### Fold 表达式

```cpp
template<typename... Args>
auto sum(Args... args) {
    return (... + args);           // 一元左折
}

template<typename... Args>
auto rsum(Args... args) {
    return (args + ...);           // 一元右折
}

template<typename... Args>
void print(Args... args) {
    (cout << ... << args) << "\n";  // 二元左折
}

// 条件判断
template<typename... Args>
bool allTrue(Args... args) {
    return (... && args);
}

template<typename... Args>
bool anyTrue(Args... args) {
    return (... || args);
}

// 逗号表达式
template<typename... Args>
void doSomething(Args... args) {
    (process(args), ...);  // 逐个处理
}
```

### std::string_view

```cpp
// 字符串视图（不拥有内存，只读）
string_view sv = "Hello World";
sv.remove_prefix(6);         // "World"
sv.remove_suffix(2);         // "Wo"

// 高效子串
string url = "https://example.com/path";
string_view protocol = url.substr(0, url.find(':'));
```

### std::optional / std::variant / std::any

```cpp
// optional：可能为空的值
optional<int> divide(int a, int b) {
    if (b == 0) return nullopt;
    return a / b;
}

if (auto result = divide(10, 2)) {
    cout << *result;  // 5
}

// variant：类型安全的联合体
variant<int, double, string> v;
v = 42;
v = "hello";

if (holds_alternative<int>(v)) {
    cout << get<int>(v);
}

// visit
visit([](const auto& val) {
    cout << val;
}, v);

// any：类型擦除
any a = 42;
a = string("hello");

if (a.type() == typeid(string)) {
    cout << any_cast<string>(a);
}
```

### std::filesystem

```cpp
#include <filesystem>
namespace fs = filesystem;

// 路径操作
fs::path p = "/home/user/file.txt";
p.filename();          // "file.txt"
p.stem();              // "file"
p.extension();         // ".txt"
p.parent_path();       // "/home/user"

// 目录操作
fs::create_directory("new_dir");
fs::create_directories("a/b/c");

// 遍历目录
for (const auto& entry : fs::directory_iterator(".")) {
    cout << entry.path() << "\n";
}

// 递归遍历
for (const auto& entry : fs::recursive_directory_iterator(".")) {
    if (entry.is_regular_file() && entry.path().extension() == ".cpp") {
        cout << entry.path() << " - " << entry.file_size() << " bytes\n";
    }
}

// 文件操作
fs::copy("src.txt", "dst.txt", fs::copy_options::overwrite_existing);
fs::rename("old.txt", "new.txt");
fs::remove("unwanted.txt");
fs::remove_all("directory_to_delete");
```

## C++20

### Concepts

```cpp
#include <concepts>

// 基本 concept
template<typename T>
concept Integral = is_integral_v<T>;

template<typename T>
concept Hashable = requires(T v) {
    { hash<T>{}(v) } -> convertible_to<size_t>;
};

template<typename T>
concept Comparable = requires(T a, T b) {
    { a < b } -> convertible_to<bool>;
    { a == b } -> convertible_to<bool>;
};

// 使用 concepts
template<Integral T>
T gcd(T a, T b) {
    return b == 0 ? a : gcd(b, a % b);
}

// 简洁语法
void print(const Hashable auto& value) {
    cout << value;
}

// requires 子句
template<typename T>
    requires Comparable<T>
T max(const T& a, const T& b) {
    return a < b ? b : a;
}
```

### Ranges

```cpp
#include <ranges>

vector<int> vec = {1, 2, 3, 4, 5, 6, 7, 8};

// 管道操作
auto result = vec
    | views::filter([](int n) { return n % 2 == 0; })
    | views::transform([](int n) { return n * n; })
    | views::take(3);

for (int v : result) {
    cout << v << " ";  // 4 16 36
}

// 范围算法
ranges::sort(vec);
auto it = ranges::find(vec, 5);
```

### Coroutines（协程）

```cpp
#include <coroutine>
#include <generator>  // C++23

// 简化版生成器
template<typename T>
struct Generator {
    struct promise_type {
        T current_value;
        suspend_always yield_value(T value) {
            current_value = value;
            return {};
        }
        suspend_always initial_suspend() { return {}; }
        suspend_always final_suspend() noexcept { return {}; }
        Generator get_return_object() {
            return Generator{handle_type::from_promise(*this)};
        }
        void return_void() {}
        void unhandled_exception() { terminate(); }
    };
    using handle_type = coroutine_handle<promise_type>;

    handle_type coro;
    Generator(handle_type h) : coro(h) {}
    ~Generator() { if (coro) coro.destroy(); }

    bool next() {
        coro.resume();
        return !coro.done();
    }
    T value() { return coro.promise().current_value; }
};

Generator<int> range(int start, int end) {
    for (int i = start; i < end; i++) {
        co_yield i;
    }
}

// 使用
auto gen = range(0, 5);
while (gen.next()) {
    cout << gen.value() << " ";  // 0 1 2 3 4
}
```

### Modules（模块）

```cpp
// math.ixx (C++20 模块接口)
export module math;

export namespace math {
    int add(int a, int b) { return a + b; }
    int multiply(int a, int b) { return a * b; }
}

// main.cpp
import math;
int main() {
    cout << math::add(2, 3);  // 5
}
```

### std::span

```cpp
// 非拥有视图（类似 string_view，但用于连续序列）
void process(span<int> data) {
    for (int& v : data) {
        v *= 2;
    }
}

vector<int> vec = {1, 2, 3, 4, 5};
int arr[] = {6, 7, 8};

process(vec);          // {2, 4, 6, 8, 10}
process(arr);          // {12, 14, 16}
process({vec.data() + 1, 3});  // 只处理 {4, 6, 8}
```

### std::format（类似 Python f-string）

```cpp
#include <format>

cout << format("Hello, {}!", "World");  // "Hello, World!"
cout << format("int: {}, double: {:.2f}", 42, 3.14159);
cout << format("{:>10}", "right");     // "     right"
cout << format("{:0>5}", 42);          // "00042"
cout << format("{:x}", 255);           // "ff"（十六进制）
```

### std::jthread（可汇合线程）

```cpp
// jthread 在析构时自动 join
{
    jthread t1([](stop_token st) {
        while (!st.stop_requested()) {
            // 工作
        }
    });

    // 不需要显式 join
}  // 自动 join

// 请求停止
t1.request_stop();
```

## C++23

### std::expected

```cpp
#include <expected>

// 带错误码的返回值
expected<int, error_code> parse_int(string_view s) {
    int result;
    auto [ptr, ec] = from_chars(s.data(), s.data() + s.size(), result);
    if (ec == errc()) {
        return result;
    }
    return unexpected(error_code{1});
}

auto val = parse_int("42");
if (val) {
    cout << *val;  // 42
} else {
    cout << "Error: " << val.error().value();
}

// 链式调用
parse_int("42")
    .and_then([](int v) -> expected<int, error_code> {
        return v > 0 ? v : unexpected(error_code{2});
    })
    .or_else([](error_code e) -> expected<int, error_code> {
        return 0;  // 默认值
    });
```

### std::print

```cpp
#include <print>

print("Hello, {}!\n", "World");  // 自动换行
println("The answer is {}", 42);
println("{:.2f}°C", 23.456);     // "23.46°C"
```

### 其他 C++23 特性

```cpp
// 多维下标运算符
template<typename T, size_t N>
struct Matrix {
    T data[N][N];
    T& operator[](size_t row, size_t col) {  // C++23
        return data[row][col];
    }
};

// if consteval
constexpr int fn(int i) {
    if consteval {       // 在编译期执行
        return i * 2;
    } else {              // 在运行时执行
        return i + 1;
    }
}

// 显式 this（Deducing this）
struct Derived : public Base {
    void foo(this auto& self) {
        // self 自动推导为正确的派生类型
    }
};
```
