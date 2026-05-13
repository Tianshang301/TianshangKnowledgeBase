# 指针与内存管理

## 指针基础

### 声明与解引用

```c
int x = 42;
int* ptr = &x;       // 声明指针并取地址
*ptr = 100;          // 解引用，修改 x 为 100

printf("%p\n", ptr); // 打印地址
printf("%d\n", *ptr);// 100
```

### 指针运算

```c
int arr[5] = {10, 20, 30, 40, 50};
int* p = arr;         // 指向数组首元素

p[0];                 // 10（下标访问）
*p;                   // 10
*(p + 1);             // 20
*(p + 2);             // 30

// 遍历
for (int* p = arr; p < arr + 5; p++) {
    printf("%d ", *p);
}
```

### 指针与数组

```c
int arr[5] = {1, 2, 3, 4, 5};
int* ptr = arr;

// arr 和 ptr 的区别
sizeof(arr);  // 20（5 * 4）
sizeof(ptr);  // 8（指针本身大小）

// 数组指针 vs 指针数组
int (*arrPtr)[5] = &arr;  // 指向数组的指针
int* ptrArr[5];            // 指针数组

// 二维数组与指针
int matrix[3][4] = {{1,2,3,4},{5,6,7,8}};
int (*row)[4] = matrix;   // 指向包含4个int的数组
(*row)[0];                // 1
*(*(matrix + 1) + 2);     // 7
```

### 函数指针

```c
// 函数指针声明
int (*funcPtr)(int, int);

// 赋值
funcPtr = &add;
funcPtr = add;            // 隐式转换

// 调用
int result = funcPtr(3, 4);

// 作为参数
void sort(int* arr, int n, int (*cmp)(int, int)) {
    for (int i = 0; i < n; i++) {
        for (int j = i + 1; j < n; j++) {
            if (cmp(arr[i], arr[j]) > 0) {
                int t = arr[i]; arr[i] = arr[j]; arr[j] = t;
            }
        }
    }
}

int asc(int a, int b) { return a - b; }
int desc(int a, int b) { return b - a; }

// 函数指针数组
int (*ops[])(int, int) = {add, sub, mul, div};
```

### void 指针

```c
void* ptr;
int x = 42;
char c = 'A';

ptr = &x;
int* ip = (int*)ptr;    // 必须显式转换

ptr = &c;
char* cp = (char*)ptr;

// 泛型函数
void swap(void* a, void* b, size_t size) {
    char* ca = (char*)a;
    char* cb = (char*)b;
    for (size_t i = 0; i < size; i++) {
        char t = ca[i];
        ca[i] = cb[i];
        cb[i] = t;
    }
}
```

### const 指针

```c
// const 指针 vs 指向 const 的指针
const int* p1;      // 指向 const int（不能通过 p1 修改值）
int const* p2;      // 同上
int* const p3;      // const 指针（不能修改 p3 指向的地址）
const int* const p4;// const 指针 + 指向 const int

int x = 10, y = 20;
const int* p = &x;
// *p = 20;         // 错误
p = &y;              // 正确

int* const q = &x;
*q = 20;             // 正确
// q = &y;          // 错误
```

## 动态内存管理

### C 风格（malloc/free）

```c
#include <stdlib.h>

// 分配
int* arr = (int*)malloc(5 * sizeof(int));
if (arr == NULL) {
    fprintf(stderr, "内存分配失败\n");
    exit(1);
}

// 初始化
memset(arr, 0, 5 * sizeof(int));
int* arr2 = (int*)calloc(5, sizeof(int));  // 自动初始化为 0

// 重新分配
arr = (int*)realloc(arr, 10 * sizeof(int));

// 释放
free(arr);
arr = NULL;  // 避免悬空指针
```

### C++ 风格（new/delete）

```cpp
// 单个对象
int* p = new int(42);
delete p;

// 数组
int* arr = new int[10];
delete[] arr;

// 对象
MyClass* obj = new MyClass(params);
delete obj;

// nothrow 版本
int* safe = new(std::nothrow) int[1000];
if (safe == nullptr) {
    // 处理失败
}
```

## 智能指针（C++11）

### unique_ptr

独占所有权，不可复制，可移动。

```cpp
#include <memory>

// 创建
auto ptr = make_unique<int>(42);
unique_ptr<int> ptr2(new int(42));

// 转移所有权
auto ptr3 = std::move(ptr);  // ptr 变为 null

// 自定义删除器
auto fileDeleter = [](FILE* f) { fclose(f); };
unique_ptr<FILE, decltype(fileDeleter)> filePtr(fopen("test.txt", "r"), fileDeleter);

// 工厂函数
template<typename T, typename... Args>
unique_ptr<T> make_unique(Args&&... args) {
    return unique_ptr<T>(new T(std::forward<Args>(args)...));
}
```

### shared_ptr

共享所有权，引用计数。

```cpp
auto p1 = make_shared<int>(42);
auto p2 = p1;       // 引用计数 +1

cout << p1.use_count();  // 2

p1.reset();         // 引用计数 -1
// p2 仍有效

// 自定义删除器
auto deleter = [](int* p) {
    cout << "删除 " << *p << endl;
    delete p;
};
shared_ptr<int> p3(new int(100), deleter);

// 数组（C++17）
shared_ptr<int[]> arr(new int[10]);
```

### weak_ptr

弱引用，不增加引用计数，解决循环引用。

```cpp
class Node {
public:
    shared_ptr<Node> next;
    weak_ptr<Node> prev;  // 用 weak_ptr 避免循环引用
    ~Node() { cout << "Node destroyed\n"; }
};

auto n1 = make_shared<Node>();
auto n2 = make_shared<Node>();
n1->next = n2;
n2->prev = n1;      // 不会导致引用计数增加

// 使用 weak_ptr
if (auto p = n2->prev.lock()) {  // lock() 返回 shared_ptr
    cout << "节点仍存在\n";
}
```

### enable_shared_from_this

```cpp
class Task : public enable_shared_from_this<Task> {
public:
    void start() {
        // 正确获取 shared_ptr
        auto self = shared_from_this();
        executor.submit([self]() {
            self->process();
        });
    }
    void process() { /* ... */ }
};
```

## RAII 原则

资源获取即初始化（Resource Acquisition Is Initialization）。

```cpp
class File {
    FILE* file_;
public:
    File(const char* filename, const char* mode)
        : file_(fopen(filename, mode)) {
        if (!file_) throw runtime_error("打开文件失败");
    }

    ~File() {
        if (file_) fclose(file_);
    }

    // 禁止复制
    File(const File&) = delete;
    File& operator=(const File&) = delete;

    // 可移动
    File(File&& other) noexcept : file_(other.file_) {
        other.file_ = nullptr;
    }
};

// 使用
void processFile() {
    File f("data.txt", "r");  // 构造函数获取资源
    // 处理文件
}  // 析构函数自动释放
```

## 常见指针错误

### 悬空指针（Dangling Pointer）

```cpp
int* getDangling() {
    int x = 42;
    return &x;   // 返回局部变量的地址
}

// 正确
int* getValid() {
    int* p = new int(42);
    return p;    // 动态分配的对象
}
```

### 空指针解引用

```cpp
int* ptr = nullptr;
// *ptr = 42;   // 崩溃！

// 正确做法
if (ptr != nullptr) {
    *ptr = 42;
}
```

### 内存泄漏

```cpp
void leak() {
    int* arr = new int[1000];
    // 忘记 delete[] arr
}

// 解决方案：使用智能指针
void noLeak() {
    auto arr = make_unique<int[]>(1000);
}
```

### 双重释放

```cpp
int* p = new int(42);
delete p;
// delete p;   // 未定义行为！

// 释放后置空指针
delete p;
p = nullptr;
// delete p;   // 删除空指针安全
```

### 缓冲区溢出

```cpp
char buffer[10];
// strcpy(buffer, "This is too long");  // 溢出！

// 正确
strncpy(buffer, "Hi", sizeof(buffer) - 1);
buffer[sizeof(buffer) - 1] = '\0';
```

### 使用已释放内存

```cpp
int* p = new int(42);
delete p;
// *p = 100;   // 使用已释放内存，未定义行为
```

## 指针 vs 引用

| 特性 | 指针 | 引用 |
|------|------|------|
| 空值 | 可以为 nullptr | 必须初始化且不能为空 |
| 重新绑定 | 可以指向不同对象 | 一旦绑定不可改变 |
| 语法 | 需要 * 解引用 | 自动解引用 |
| 算术运算 | 支持指针运算 | 不支持 |
| 内存 | 需要额外存储 | 别名，通常不占用额外内存 |
| 适用场景 | 可选参数、动态分配、数组遍历 | 函数参数传递、运算符重载 |
