---
aliases: [Memory]
tags: ['ProgrammingLanguages', 'CCpp', 'Memory']
created: 2026-05-16
updated: 2026-05-13
---

# C++ 内存模型

## 内存布局

```
High Address
  ┌──────────────────┐
  │     Stack        │  ← 局部变量、函数调用帧（向下增长）
  ├──────────────────┤
  │        ↓         │
  │                  │
  │        ↑         │
  ├──────────────────┤
  │     Heap         │  ← 动态分配（向上增长）
  ├──────────────────┤
  │  BSS (Block      │  ← 未初始化全局/静态变量
  │  Started by      │     （zero-initialized）
  │  Symbol)         │
  ├──────────────────┤
  │  Data Segment    │  ← 已初始化全局/静态变量
  ├──────────────────┤
  │  Text (Code)     │  ← 程序代码（只读）
  Low Address
```

```cpp
// 全局变量（数据段）
int globalVar = 42;
int globalUninit;       // BSS 段

static int staticVar = 10;  // 静态存储期

void func() {
    static int funcStatic = 0;  // 静态存储期，BSS 段
    int localVar = 100;         // 栈
    int* heapVar = new int(200); // 堆
    delete heapVar;
}
```

## 存储期

| 存储期 | 生命周期 | 作用域 | 示例 |
|--------|---------|--------|------|
| static | 程序开始到结束 | 文件/函数内 | 全局变量、static 变量 |
| thread_local | 线程开始到结束 | 线程内 | thread_local 变量 |
| automatic | 代码块开始到结束 | 代码块内 | 局部变量 |
| dynamic | new 到 delete | 由指针管理 | new 分配的对象 |

```cpp
thread_local int tlsVar = 0;  // 每个线程有自己的副本

class Logger {
    static int instances;           // 所有对象共享
    thread_local static int cache;  // 每个线程独立缓存
};
```

## Placement New

在已分配的内存上构造对象。

```cpp
#include <new>

// 在缓冲区上构造
alignas(alignof(string)) char buffer[sizeof(string)];

string* p = new (buffer) string("Hello");  // placement new
cout << *p;  // Hello

// 必须显式调用析构函数
p->~string();
```

```cpp
// 内存池示例
class MemoryPool {
    char* pool_;
    size_t offset_;
public:
    MemoryPool(size_t size) : pool_(new char[size]), offset_(0) {}

    void* allocate(size_t size) {
        if (offset_ + size > pool_size) return nullptr;
        void* ptr = pool_ + offset_;
        offset_ += size;
        return ptr;
    }

    void reset() { offset_ = 0; }
    ~MemoryPool() { delete[] pool_; }
};

MemoryPool pool(4096);
int* p = new (pool.allocate(sizeof(int))) int(42);
string* s = new (pool.allocate(sizeof(string))) string("test");
```

## Allocator（分配器）

```cpp
template<typename T>
struct LoggingAllocator {
    using value_type = T;

    LoggingAllocator() = default;

    T* allocate(size_t n) {
        cout << "分配 " << n << " 个元素\n";
        return static_cast<T*>(::operator new(n * sizeof(T)));
    }

    void deallocate(T* p, size_t n) {
        cout << "释放 " << n << " 个元素\n";
        ::operator delete(p);
    }

    template<typename U>
    bool operator==(const LoggingAllocator<U>&) const {
        return true;
    }
};

// 使用自定义分配器
vector<int, LoggingAllocator<int>> vec;
vec.push_back(1);
vec.push_back(2);
// 输出：
// 分配 1 个元素
// 分配 2 个元素
// 释放 1 个元素
// 释放 2 个元素
```

## 内存对齐

```cpp
#include <cstdalign>

struct alignas(16) AlignedStruct {
    float x, y, z, w;  // 16 字节对齐，适合 SIMD
};

alignas(64) int cacheAligned[8];  // 缓存行对齐

// alignof
cout << alignof(int);              // 4
cout << alignof(AlignedStruct);    // 16
cout << alignof(max_align_t);      // 最大默认对齐（通常 8 或 16）

// 手动对齐分配
void* ptr = aligned_alloc(64, 1024);  // C11/C++17
free(ptr);

// C++17 对齐分配
auto p = make_unique<int[]>(100);  // 自动对齐
```

## 缓存友好编程

```cpp
// 缓存行大小通常为 64 字节
constexpr size_t CACHE_LINE_SIZE = 64;

// 伪共享（False Sharing）
struct alignas(CACHE_LINE_SIZE) Counter {
    volatile long value;
};

struct Counters {
    alignas(CACHE_LINE_SIZE) Counter c1;
    alignas(CACHE_LINE_SIZE) Counter c2;
    alignas(CACHE_LINE_SIZE) Counter c3;
};

// 空间局部性：按行遍历（缓存友好）
int matrix[N][N];

// 友好：连续访问
for (int i = 0; i < N; i++)
    for (int j = 0; j < N; j++)
        matrix[i][j] = 0;

// 不友好：跳跃访问
for (int j = 0; j < N; j++)
    for (int i = 0; i < N; i++)
        matrix[i][j] = 0;
```

## 复制省略（Copy Elision）

### RVO（Return Value Optimization）

```cpp
struct BigObject {
    int data[1000];
    BigObject() { cout << "构造\n"; }
    BigObject(const BigObject&) { cout << "拷贝构造\n"; }
    BigObject(BigObject&&) noexcept { cout << "移动构造\n"; }
};

BigObject createObject() {
    return BigObject{};  // RVO：直接在返回值位置构造
}

BigObject obj = createObject();  // 可能只输出一次"构造"
```

### NRVO（Named RVO）

```cpp
BigObject createNamed() {
    BigObject obj;        // 具名对象
    // 处理 obj
    return obj;           // NRVO：编译器可能省略拷贝
}
```

### 强制复制省略（C++17）

```cpp
// C++17 保证某些情况下的复制省略
struct NonMovable {
    NonMovable() = default;
    NonMovable(const NonMovable&) = delete;
    NonMovable(NonMovable&&) = delete;
};

NonMovable create() {
    return NonMovable{};  // C++17 保证 OK（复制省略）
}
```

## 移动语义

```cpp
class Buffer {
    int* data_;
    size_t size_;

public:
    // 移动构造函数
    Buffer(Buffer&& other) noexcept
        : data_(std::exchange(other.data_, nullptr))
        , size_(std::exchange(other.size_, 0))
    {}

    // 移动赋值
    Buffer& operator=(Buffer&& other) noexcept {
        if (this != &other) {
            delete[] data_;
            data_ = std::exchange(other.data_, nullptr);
            size_ = std::exchange(other.size_, 0);
        }
        return *this;
    }
};

// std::move
string s1 = "hello";
string s2 = std::move(s1);  // s1 被移动，内容转移到 s2
// s1 处于有效但未指定状态

// std::forward（完美转发）
template<typename T>
void wrapper(T&& arg) {
    // 保持值类别转发
    func(std::forward<T>(arg));
}
```
