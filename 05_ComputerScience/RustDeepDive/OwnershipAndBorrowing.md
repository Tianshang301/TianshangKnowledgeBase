---
aliases:
  - Rust所有权
  - Rust借用
  - Ownership and Borrowing
  - Rust内存安全
tags:
  - Rust
  - 所有权
  - 借用
  - 生命周期
  - 计算机科学
created: 2026-06-27
updated: 2026-06-27
---

# Rust所有权与借用

所有权（Ownership）和借用（Borrowing）是 Rust 语言的核心机制，它们在编译期保证内存安全，无需垃圾回收器（GC），同时避免了悬垂指针和数据竞争等问题。

## 所有权规则

### 基本规则

Rust 所有权系统的三条基本规则：

1. **每个值都有一个所有者（Owner）**
2. **同一时间只能有一个所有者**
3. **当所有者离开作用域时，值被丢弃（Drop）**

```rust
fn main() {
    let s1 = String::from("hello"); // s1 是字符串的所有者
    let s2 = s1;                    // 所有权转移到 s2
    // println!("{}", s1);          // 编译错误！s1 已失效
    println!("{}", s2);             // 正常，s2 是所有者
}   // s2 离开作用域，字符串被释放
```

### 移动语义

Rust 中赋值和传参默认是移动（Move）：

- **赋值移动**：`let s2 = s1;` 将所有权从 s1 移动到 s2
- **函数传参**：将值传递给函数会移动所有权
- **函数返回**：函数可以返回值的所有权
- **集合移动**：将值放入集合会移动所有权

```rust
fn takes_ownership(s: String) {
    println!("{}", s);
}   // s 被丢弃

fn gives_ownership() -> String {
    let s = String::from("hello");
    s   // 返回所有权
}

fn main() {
    let s1 = String::from("hello");
    takes_ownership(s1);        // s1 的所有权移动到函数内
    // println!("{}", s1);      // 编译错误！
    
    let s2 = gives_ownership(); // s2 获得所有权
}   // s2 被丢弃
```

### Copy trait

简单类型实现了 Copy trait，赋值时会复制而非移动：

- **整数类型**：i32, u64, usize 等
- **浮点类型**：f32, f64
- **布尔类型**：bool
- **字符类型**：char
- **元组**：所有元素都是 Copy 的元组

```rust
fn main() {
    let x = 5;
    let y = x;  // 复制，不是移动
    println!("x = {}, y = {}", x, y); // 都有效
}
```

## 借用机制

### 不可变借用

不可变借用（Immutable Borrow）允许读取但不修改值：

- **语法**：`&T`，使用 `&` 获取引用
- **多个借用**：同一时间可以有多个不可变借用
- **只读访问**：不能通过不可变引用修改值
- **非移动**：借用不会转移所有权

```rust
fn calculate_length(s: &String) -> usize {
    s.len()   // 可以读取
    // s.push_str(" world"); // 编译错误！不能修改
}

fn main() {
    let s1 = String::from("hello");
    let len = calculate_length(&s1); // 借用 s1
    println!("{} has length {}", s1, len); // s1 仍然有效
}
```

### 可变借用

可变借用（Mutable Borrow）允许修改值：

- **语法**：`&mut T`，使用 `&mut` 获取可变引用
- **独占访问**：同一时间只能有一个可变借用
- **互斥性**：可变借用与不可变借用不能同时存在
- **修改值**：可以通过可变引用修改值

```rust
fn add_world(s: &mut String) {
    s.push_str(" world");
}

fn main() {
    let mut s = String::from("hello");
    add_world(&mut s);  // 可变借用
    println!("{}", s);  // 输出 "hello world"
}
```

### 借用规则总结

```
借用规则：
1. 任意数量的不可变引用 &T
   或
2. 恰好一个可变引用 &mut T
   不能同时存在！

目的：防止数据竞争
- 两个或更多指针同时访问同一数据
- 至少一个指针用于写入
- 没有同步机制
```

### 悬垂引用防护

Rust 编译器保证不会出现悬垂引用（Dangling Reference）：

```rust
fn dangle() -> &String {  // 编译错误！
    let s = String::from("hello");
    &s  // s 在函数结束时被释放，返回的引用将指向无效内存
}

fn no_dangle() -> String {
    let s = String::from("hello");
    s   // 移动所有权，调用者负责释放
}
```

## 生命周期标注

### 生命周期概念

生命周期（Lifetime）描述引用的有效范围：

- **作用域**：引用在哪个范围内有效
- **编译器推断**：大多数情况编译器自动推断
- **显式标注**：复杂情况需要显式标注
- **生命周期参数**：使用 `'a` 语法标注

### 函数签名中的生命周期

```rust
// 编译器无法推断返回引用的生命周期
fn longest<'a>(x: &'a str, y: &'a str) -> &'a str {
    if x.len() > y.len() { x } else { y }
}

fn main() {
    let string1 = String::from("long string");
    let result;
    {
        let string2 = String::from("xyz");
        result = longest(string1.as_str(), string2.as_str());
        println!("Longest is {}", result);
    }
    // println!("Longest is {}", result); // 编译错误！string2 已被释放
}
```

### 生命周期省略规则

编译器的生命周期省略规则（Lifetime Elision Rules）：

1. **每个引用参数都有自己的生命周期**
2. **只有一个输入生命周期，该生命周期赋给所有输出引用**
3. **方法中 &self 的生命周期赋给所有输出引用**

```rust
// 省略前
fn first_word(s: &str) -> &str { ... }

// 省略后（编译器自动推断）
fn first_word<'a>(s: &'a str) -> &'a str { ... }
```

### 结构体中的生命周期

```rust
// 包含引用的结构体必须标注生命周期
struct ImportantExcerpt<'a> {
    part: &'a str,
}

impl<'a> ImportantExcerpt<'a> {
    fn level(&self) -> i32 {
        3
    }
    
    // 第三条省略规则适用
    fn announce_and_return_part(&self, announcement: &str) -> &str {
        println!("Attention: {}", announcement);
        self.part
    }
}
```

### 'static 生命周期

'static 是特殊的生命周期，表示整个程序运行期间有效：

- **字符串字面量**：所有字符串字面量都是 'static
- **全局变量**：全局变量的引用是 'static
- **泄漏数据**：使用 Box::leak 创建 'static 引用
- **谨慎使用**：不要滥用 'static

```rust
let s: &'static str = "I have a static lifetime.";
```

## 智能指针

### Box<T>

Box 是堆上分配的智能指针：

- **堆分配**：将数据存储在堆上
- **单一所有权**：拥有堆上数据的所有权
- **自动释放**：离开作用域时自动释放堆内存
- **递归类型**：用于创建递归数据结构

```rust
enum List {
    Cons(i32, Box<List>),
    Nil,
}

use List::{Cons, Nil};

fn main() {
    let list = Cons(1, Box::new(Cons(2, Box::new(Nil))));
}
```

### Rc<T>

Rc（Reference Counting）是引用计数智能指针：

- **共享所有权**：多个变量可以拥有同一数据
- **引用计数**：跟踪有多少所有者
- **不可变访问**：Rc 只提供不可变访问
- **循环引用**：需要注意避免循环引用

```rust
use std::rc::Rc;

fn main() {
    let a = Rc::new(List::Cons(5, Rc::new(List::Nil)));
    let b = Rc::clone(&a);  // 增加引用计数
    let c = Rc::clone(&a);  // 增加引用计数
    
    println!("Reference count = {}", Rc::strong_count(&a)); // 3
}
```

### RefCell<T>

RefCell 提供内部可变性：

- **运行时借用检查**：在运行时而非编译时检查借用规则
- **内部可变性**：即使在不可变引用下也能修改数据
- **借用方法**：borrow() 和 borrow_mut()
- **panic!**：违反借用规则时会 panic

```rust
use std::cell::RefCell;

fn main() {
    let data = RefCell::new(5);
    
    *data.borrow_mut() += 1;  // 运行时借用检查
    
    println!("{}", data.borrow()); // 6
}
```

## 所有权模式

### RAII 模式

资源获取即初始化（RAII）：

- **构造时获取**：在构造函数中获取资源
- **析构时释放**：在 Drop trait 中释放资源
- **作用域绑定**：资源生命周期绑定到变量作用域
- **异常安全**：即使发生 panic 也能正确释放

```rust
struct DatabaseConnection {
    // 连接资源
}

impl Drop for DatabaseConnection {
    fn drop(&mut self) {
        println!("Closing database connection");
        // 释放连接资源
    }
}

fn main() {
    let conn = DatabaseConnection { /* ... */ };
    // 使用连接...
}   // conn 离开作用域，自动调用 drop
```

### Builder 模式

使用所有权实现 Builder 模式：

```rust
struct QueryBuilder {
    table: String,
    conditions: Vec<String>,
    limit: Option<usize>,
}

impl QueryBuilder {
    fn new(table: &str) -> Self {
        QueryBuilder {
            table: table.to_string(),
            conditions: Vec::new(),
            limit: None,
        }
    }
    
    fn where_clause(mut self, condition: &str) -> Self {
        self.conditions.push(condition.to_string());
        self   // 返回 self，所有权转移
    }
    
    fn limit(mut self, limit: usize) -> Self {
        self.limit = Some(limit);
        self
    }
    
    fn build(self) -> String {
        // 消费 self，生成查询字符串
        format!("SELECT * FROM {}", self.table)
    }
}

fn main() {
    let query = QueryBuilder::new("users")
        .where_clause("age > 18")
        .limit(10)
        .build();
}
```

## 常见所有权问题

### 生命周期不匹配

```rust
// 问题：返回引用的生命周期
fn invalid_return() -> &str {  // 编译错误
    let s = String::from("hello");
    &s  // s 将被释放
}

// 解决方案：返回拥有的值
fn valid_return() -> String {
    String::from("hello")
}
```

### 多重可变借用

```rust
fn main() {
    let mut v = vec![1, 2, 3];
    
    // 问题：同时存在不可变和可变借用
    let first = &v[0];     // 不可变借用
    v.push(4);             // 可变借用
    println!("{}", first); // 使用不可变借用
}
```

### 部分移动

```rust
struct Data {
    name: String,
    value: i32,
}

fn main() {
    let data = Data {
        name: String::from("test"),
        value: 42,
    };
    
    let name = data.name;  // 部分移动
    // println!("{}", data.name);  // 编译错误！name 已移动
    println!("{}", data.value);    // 正常，value 未移动
}
```

## 最佳实践

### 设计原则

- **最小化可变性**：优先使用不可变引用
- **明确所有权**：清晰的所有权转移意图
- **避免生命周期复杂化**：简化生命周期标注
- **使用智能指针**：需要共享所有权时使用 Rc/Arc

### 性能考量

- **零成本抽象**：所有权系统是编译时检查，运行时零开销
- **移动优于复制**：移动比复制更高效
- **栈分配优先**：尽可能使用栈分配
- **避免不必要的堆分配**：减少 Box/Rc 的使用

## 相关链接

- [[AsyncRust]] - 异步 Rust
- [[UnsafeAndFFI]] - unsafe 与 FFI
