---
aliases: [Basics]
tags: ['ProgrammingLanguages', 'CCpp', 'Basics']
created: 2026-05-16
updated: 2026-05-13
---

# C/C++ 基础语法

## C 基础

### 变量与类型

```c
#include <stdio.h>
#include <stdbool.h>

// 基本类型
int a = 42;               // 整型
short s = 100;            // 短整型
long l = 100000L;         // 长整型
long long ll = 1LL << 60; // 长长整型
unsigned int u = 100;     // 无符号整型

float f = 3.14f;          // 单精度浮点
double d = 3.1415926;     // 双精度浮点
char c = 'A';             // 字符

_Bool flag = 1;           // 布尔（C99）
bool flag2 = true;        // 需要 <stdbool.h>
```

### 控制流

```c
// if-else
int score = 85;
if (score >= 90) {
    printf("优秀\n");
} else if (score >= 60) {
    printf("及格\n");
} else {
    printf("不及格\n");
}

// switch
switch (score / 10) {
    case 10:
    case 9:  printf("A\n"); break;
    case 8:  printf("B\n"); break;
    case 7:  printf("C\n"); break;
    case 6:  printf("D\n"); break;
    default: printf("F\n");
}

// for
for (int i = 0; i < 10; i++) {
    printf("%d ", i);
}

// while / do-while
int i = 0;
while (i < 5) {
    printf("%d ", i++);
}

int j = 0;
do {
    printf("%d ", j++);
} while (j < 5);
```

### 函数

```c
// 函数声明
int add(int a, int b);

// 函数定义
int add(int a, int b) {
    return a + b;
}

// 静态函数（文件作用域）
static void helper() {
    printf("内部函数\n");
}

// inline 函数（C99）
inline int max(int a, int b) {
    return a > b ? a : b;
}
```

### 数组

```c
int arr[5] = {1, 2, 3, 4, 5};
int arr2[] = {1, 2, 3};     // 自动推断大小
int matrix[3][4] = {{1,2,3,4}, {5,6,7,8}};

// 遍历
for (int i = 0; i < 5; i++) {
    printf("%d ", arr[i]);
}
```

### 字符串（char[]）

```c
char str1[] = "Hello";              // 自动添加 '\0'
char str2[6] = {'H', 'e', 'l', 'l', 'o', '\0'};
const char* str3 = "World";         // 字符串字面量

// 常用函数（<string.h>）
#include <string.h>
strlen(str1);               // 长度
strcpy(dest, src);          // 复制
strcat(dest, src);          // 拼接
strcmp(str1, str2);         // 比较（相等返回0）
strchr(str1, 'l');          // 查找字符
strstr(str1, "ll");         // 查找子串
```

### struct / union / enum

```c
// 结构体
struct Point {
    int x;
    int y;
};

struct Point p1 = {10, 20};
p1.x = 30;

typedef struct {
    char name[50];
    int age;
} Person;

Person p2 = {"Alice", 25};

// 联合体（所有成员共享同一内存）
union Data {
    int i;
    float f;
    char str[4];
};

union Data data;
data.i = 42;

// 枚举
enum Color {
    RED = 0,
    GREEN = 1,
    BLUE = 2
};

enum Color c = RED;
```

## C++ 新增特性

### 引用（Reference）

```cpp
int x = 10;
int& ref = x;         // 引用（别名）
ref = 20;             // 修改 x 为 20

void swap(int& a, int& b) {
    int temp = a;
    a = b;
    b = temp;
}

// const 引用（可绑定临时对象）
const int& cr = 42;
```

### 函数重载

```cpp
int max(int a, int b) {
    return a > b ? a : b;
}

double max(double a, double b) {
    return a > b ? a : b;
}

string max(const string& a, const string& b) {
    return a > b ? a : b;
}
```

### 默认参数

```cpp
void print(const string& msg, int times = 1, char sep = '\n') {
    for (int i = 0; i < times; i++) {
        cout << msg << sep;
    }
}

print("Hello");              // times=1, sep='\n'
print("Hi", 3);              // times=3, sep='\n'
print("Hey", 2, ' ');        // times=2, sep=' '
```

### 命名空间

```cpp
namespace MyApp {
    namespace Utils {
        int calculate(int x) {
            return x * 2;
        }
    }

    inline namespace V1 {
        void foo() {}
    }
}

// 使用
using namespace MyApp::Utils;
using namespace MyApp;

int result = calculate(10);
MyApp::V1::foo();
```

### std::string

```cpp
#include <string>

string s1 = "Hello";
string s2("World");
string s3 = s1 + " " + s2;  // "Hello World"

// 常用方法
s1.length();                 // 5
s1.size();                   // 5
s1[0];                       // 'H'
s1.at(0);                    // 'H'（带边界检查）
s1.substr(1, 3);             // "ell"
s1.find("ll");               // 2
s1.find('o');                // 4
s1.rfind('l');               // 3
s1.replace(1, 2, "xx");      // "Hxxo"
s1.insert(5, "!");           // "Hello!"
s1.erase(5);                 // "Hello"
s1.c_str();                  // 转 const char*

// C++17 string_view
string_view sv = s1;
sv.remove_prefix(1);         // "ello"
sv.remove_suffix(1);         // "ell"
```

### 类型转换

```cpp
// static_cast（编译时检查）
double d = 3.14;
int i = static_cast<int>(d);                    // 3
Base* base = static_cast<Derived*>(derived);    // 上行转换

// dynamic_cast（运行时检查，需要 RTTI）
if (Derived* d = dynamic_cast<Derived*>(base)) {
    d->derivedMethod();
}

// const_cast（去除 const）
const int* cp = &i;
int* p = const_cast<int*>(cp);
*p = 42;

// reinterpret_cast（位模式重新解释）
int* ptr = &i;
uintptr_t addr = reinterpret_cast<uintptr_t>(ptr);
```

### auto 与 decltype

```cpp
auto x = 42;                 // int
auto y = 3.14;               // double
auto z = "hello";            // const char*
auto& ref = x;               // int&
const auto& cr = x;          // const int&

auto lambda = [](int a) { return a * 2; };

// decltype
int a = 10;
decltype(a) b = 20;          // int

template<typename T1, typename T2>
auto add(T1 a, T2 b) -> decltype(a + b) {
    return a + b;
}
```

### 范围 for 循环

```cpp
vector<int> vec = {1, 2, 3, 4, 5};

for (int v : vec) {
    cout << v << " ";
}

for (auto& v : vec) {
    v *= 2;  // 修改元素
}

for (const auto& v : vec) {
    cout << v << " ";
}

// C++17 结构化绑定 + 范围 for
map<string, int> mp = {{"a", 1}, {"b", 2}};
for (const auto& [key, value] : mp) {
    cout << key << ": " << value << endl;
}
```

### nullptr

```cpp
// C++11 引入，代替 NULL
int* ptr = nullptr;

void foo(int);
void foo(char*);

foo(nullptr);  // 调用 foo(char*)
// foo(NULL);  // 歧义，可能调用 foo(int)
```

### constexpr

```cpp
// 编译期求值
constexpr int factorial(int n) {
    return n <= 1 ? 1 : n * factorial(n - 1);
}

constexpr int result = factorial(5);  // 编译期计算

// C++17 constexpr if
template<typename T>
auto getValue(T t) {
    if constexpr (is_pointer_v<T>) {
        return *t;
    } else {
        return t;
    }
}
```
