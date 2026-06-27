---
aliases: [OOP]
tags: ['ProgrammingLanguages', 'CCpp', 'OOP']
created: 2026-05-16
updated: 2026-05-13
---

# C++ 面向对象

## 类与对象

```cpp
class Rectangle {
private:
    double width_;
    double height_;

public:
    // 构造函数
    Rectangle(double w, double h) : width_(w), height_(h) {}

    // 成员函数
    double area() const { return width_ * height_; }
    double perimeter() const { return 2 * (width_ + height_); }

    // getter/setter
    double width() const { return width_; }
    void setWidth(double w) { width_ = w; }
};
```

## 访问控制

| 修饰符 | 同类 | 派生类 | 外部 |
|--------|------|--------|------|
| public | ✓ | ✓ | ✓ |
| protected | ✓ | ✓ | - |
| private | ✓ | - | - |

```cpp
class Base {
public:
    int pub;
protected:
    int prot;
private:
    int priv;
};
```

## 构造与析构

### 默认构造函数

```cpp
class Point {
public:
    Point() = default;              // C++11 默认构造
    Point(int x, int y) : x_(x), y_(y) {}

    // 禁止拷贝
    Point(const Point&) = delete;

private:
    int x_ = 0, y_ = 0;            // 类内初始化
};
```

### 初始化列表

```cpp
class Employee {
    string name_;
    int id_;
    double salary_;
    vector<int> scores_;

public:
    Employee(const string& name, int id)
        : name_(name)        // 直接初始化
        , id_(id)
        , salary_(0.0)
        , scores_{100, 90}   // uniform initialization
    {
        // 构造体
    }
};
```

### 委托构造（C++11）

```cpp
class Logger {
    string prefix_;
    ostream& out_;

public:
    Logger() : Logger("INFO", cout) {}
    Logger(const string& prefix) : Logger(prefix, cout) {}
    Logger(const string& prefix, ostream& out)
        : prefix_(prefix), out_(out) {}
};
```

### 析构函数

```cpp
class Resource {
    int* data_;
public:
    Resource(size_t size) : data_(new int[size]) {}

    ~Resource() {
        delete[] data_;
        data_ = nullptr;
    }
};
```

## Rule of Five（五法则）

如果一个类需要自定义析构函数、拷贝构造函数、拷贝赋值运算符、移动构造函数或移动赋值运算符中的任何一个，通常需要全部五个。

```cpp
class Buffer {
    int* data_;
    size_t size_;

public:
    // 构造函数
    Buffer(size_t size) : data_(new int[size]), size_(size) {
        fill(data_, data_ + size, 0);
    }

    // 析构函数
    ~Buffer() {
        delete[] data_;
    }

    // 拷贝构造函数
    Buffer(const Buffer& other)
        : data_(new int[other.size_])
        , size_(other.size_) {
        copy(other.data_, other.data_ + size_, data_);
    }

    // 拷贝赋值运算符
    Buffer& operator=(const Buffer& other) {
        if (this != &other) {
            // Copy-and-swap idiom
            Buffer tmp(other);
            swap(tmp);
        }
        return *this;
    }

    // 移动构造函数
    Buffer(Buffer&& other) noexcept
        : data_(other.data_)
        , size_(other.size_) {
        other.data_ = nullptr;
        other.size_ = 0;
    }

    // 移动赋值运算符
    Buffer& operator=(Buffer&& other) noexcept {
        if (this != &other) {
            delete[] data_;
            data_ = other.data_;
            size_ = other.size_;
            other.data_ = nullptr;
            other.size_ = 0;
        }
        return *this;
    }

    void swap(Buffer& other) noexcept {
        std::swap(data_, other.data_);
        std::swap(size_, other.size_);
    }
};
```

## 继承

### 继承方式

```cpp
class Base {
public:
    int a;
protected:
    int b;
private:
    int c;
};

// 公有继承
class DerivedPublic : public Base {
    // a: public, b: protected, c: 不可访问
};

// 保护继承
class DerivedProtected : protected Base {
    // a: protected, b: protected, c: 不可访问
};

// 私有继承
class DerivedPrivate : private Base {
    // a: private, b: private, c: 不可访问
};
```

### 虚继承（解决菱形继承）

```cpp
// 菱形继承
class Animal {
public:
    void breathe() {}
};

class Mammal : public virtual Animal {};
class Bird : public virtual Animal {};
class Bat : public Mammal, public Bird {
    // 只有一个 Animal 实例
};

// 如果不用虚继承：
// Bat bat;
// bat.breathe();  // 歧义！不知道调用哪个路径
```

### 菱形继承

```
    Animal
   /      \
Mammal    Bird
   \      /
    Bat
```

虚继承使得 `Bat` 中只有一份 `Animal` 的子对象，避免了二义性。

## 多态

### 虚函数

```cpp
class Shape {
public:
    virtual double area() const = 0;  // 纯虚函数
    virtual void draw() const {
        cout << "Drawing shape" << endl;
    }
    virtual ~Shape() = default;       // 虚析构函数
};

class Circle : public Shape {
    double radius_;
public:
    Circle(double r) : radius_(r) {}
    double area() const override {
        return 3.14159 * radius_ * radius_;
    }
    void draw() const override {
        cout << "Drawing circle" << endl;
    }
};

class Rectangle : public Shape {
    double w_, h_;
public:
    Rectangle(double w, double h) : w_(w), h_(h) {}
    double area() const override {
        return w_ * h_;
    }
};
```

### 虚函数表（vtable）与虚指针（vptr）

```cpp
// 每个包含虚函数的类有一个 vtable
// 每个对象有一个 vptr 指向 vtable

Shape* shapes[] = {new Circle(5), new Rectangle(3, 4)};
for (auto s : shapes) {
    s->draw();   // 动态绑定，通过 vptr -> vtable -> 函数
    delete s;
}
```

### 抽象类

包含至少一个纯虚函数（`= 0`）的类为抽象类，不能实例化。

```cpp
class Drawable {
public:
    virtual void draw() const = 0;
    virtual ~Drawable() = default;
};
```

### final 与 override（C++11）

```cpp
class Base {
    virtual void foo() {}
    virtual void bar() {}
};

class Derived final : public Base {   // final 类，不可被继承
    void foo() override {}            // 保证覆盖基类虚函数
    // void bar(int) override;        // 编译错误：没有匹配的基类函数
};

// final 虚函数
class Base2 {
    virtual void last() final {}
};
// class Derived2 : public Base2 {
//     void last() override {}  // 错误：last 是 final 的
// };
```

## friend

```cpp
class Matrix {
    vector<vector<double>> data_;
public:
    friend Matrix operator+(const Matrix& a, const Matrix& b);
    friend class MatrixFactory;      // 友元类
};

Matrix operator+(const Matrix& a, const Matrix& b) {
    Matrix result(a.data_.size(), a.data_[0].size());
    for (size_t i = 0; i < a.data_.size(); i++)
        for (size_t j = 0; j < a.data_[i].size(); j++)
            result.data_[i][j] = a.data_[i][j] + b.data_[i][j];
    return result;
}
```

## 静态成员

```cpp
class Counter {
    static int count_;       // 静态成员变量声明

public:
    Counter() { count_++; }
    ~Counter() { count_--; }

    static int count() {     // 静态成员函数
        return count_;
    }
};

// 静态成员变量定义（必须在类外）
int Counter::count_ = 0;

// 使用
Counter c1, c2;
cout << Counter::count();  // 2
```

## 嵌套类

```cpp
class Tree {
public:
    class Node {
    public:
        int value;
        Node* left;
        Node* right;

        Node(int v) : value(v), left(nullptr), right(nullptr) {}
    };

    Node* root;

    Tree() : root(nullptr) {}

    Node* insert(int value) {
        // 嵌套类可以访问外部类的私有成员吗？
        // 不能自动访问，但可以通过指针/引用
    }
};
```
