---
aliases: [Traits]
tags: ['ProgrammingLanguages', 'Rust', 'Traits']
---

# Rust Trait 系统

## 定义与实现 Trait

```rust
// 定义 trait
trait Summary {
    fn summarize(&self) -> String;
}

// 为类型实现 trait
struct Article {
    title: String,
    author: String,
    content: String,
}

impl Summary for Article {
    fn summarize(&self) -> String {
        format!("{} by {}", self.title, self.author)
    }
}

struct Tweet {
    username: String,
    content: String,
}

impl Summary for Tweet {
    fn summarize(&self) -> String {
        format!("{}: {}", self.username, self.content)
    }
}

// 使用 trait
let article = Article { title: String::from("Rust"), author: String::from("Alice"), content: String::from("...") };
let tweet = Tweet { username: String::from("@bob"), content: String::from("Hello") };
println!("{}", article.summarize());
println!("{}", tweet.summarize());

// 不能为外部类型实现外部 trait（孤儿规则）
```

## 默认方法实现

```rust
trait Summary {
    fn summarize(&self) -> String {
        String::from("(Read more...)")  // 默认实现
    }
    fn author(&self) -> String;
}

struct Article {
    title: String,
    author: String,
}

impl Summary for Article {
    fn author(&self) -> String {
        self.author.clone()
    }
    // 可以选择覆盖默认实现
    fn summarize(&self) -> String {
        format!("{} by {}", self.title, self.author)
    }
}
```

## Trait 约束

```rust
// trait bound 语法
fn notify(item: &impl Summary) {
    println!("Breaking news! {}", item.summarize());
}

// 完整 trait bound 语法
fn notify<T: Summary>(item: &T) {
    println!("{}", item.summarize());
}

// 多个 trait 约束
fn notify(item: &(impl Summary + Display)) {}
fn notify<T: Summary + Display>(item: &T) {}

// where 子句（更清晰的语法）
fn some_function<T, U>(t: &T, u: &U) -> i32
where
    T: Display + Clone,
    U: Clone + Debug,
{
    // ...
}

// 返回实现了 trait 的类型
fn returns_summarizable() -> impl Summary {
    Tweet { username: String::from("horse_ebooks"), content: String::from("...") }
}

// 条件实现
impl<T: Display> ToString for T {
    // 为所有实现了 Display 的类型实现 ToString
}
```

## Trait 对象

```rust
// dyn Trait 动态分发
fn notify(item: &dyn Summary) {
    println!("{}", item.summarize());
}

// 存储在堆上
struct Screen {
    components: Vec<Box<dyn Summary>>,
}

// 对象安全规则
// 1. 方法返回类型不能是 Self
// 2. 方法不能有泛型类型参数
pub trait Clone {
    fn clone(&self) -> Self;  // 不是对象安全的
}

// 对象安全的 trait 可以用作 trait 对象
```

## 关联类型

```rust
trait Iterator {
    type Item;  // 关联类型
    fn next(&mut self) -> Option<Self::Item>;
}

struct Counter {
    count: u32,
}

impl Iterator for Counter {
    type Item = u32;

    fn next(&mut self) -> Option<Self::Item> {
        self.count += 1;
        if self.count < 6 {
            Some(self.count)
        } else {
            None
        }
    }
}
```

## 运算符重载

```rust
use std::ops::Add;

#[derive(Debug, PartialEq)]
struct Point {
    x: i32,
    y: i32,
}

impl Add for Point {
    type Output = Point;

    fn add(self, other: Point) -> Point {
        Point {
            x: self.x + other.x,
            y: self.y + other.y,
        }
    }
}

let p1 = Point { x: 1, y: 2 };
let p2 = Point { x: 3, y: 4 };
let p3 = p1 + p2;  // Point { x: 4, y: 6 }
```

## 常见标准库 Trait

```rust
use std::fmt;

// Display: 用户可读的输出
impl fmt::Display for Point {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "({}, {})", self.x, self.y)
    }
}

// Debug: 调试输出
#[derive(Debug)]
struct MyStruct { /* ... */ }

// Clone/Copy
#[derive(Clone, Copy)]
struct Simple { x: i32 }

// PartialEq/Eq
#[derive(PartialEq, Eq)]
struct Item { id: u32 }

// Hash
use std::hash::{Hash, Hasher};
#[derive(Hash)]
struct User { id: u32 }

// Default
#[derive(Default)]
struct Config {
    host: String,
    port: u16,
}

// Deref: 智能指针解引用
use std::ops::Deref;
struct MyBox<T>(T);
impl<T> Deref for MyBox<T> {
    type Target = T;
    fn deref(&self) -> &T { &self.0 }
}

// Drop: 析构
impl<T> Drop for MyBox<T> {
    fn drop(&mut self) {
        println!("Dropping MyBox");
    }
}

// From/Into: 类型转换
impl From<i32> for Point {
    fn from(value: i32) -> Self {
        Point { x: value, y: value }
    }
}
let p: Point = 42.into();  // 使用 Into

// Iterator/FromIterator
struct Range {
    start: u32,
    end: u32,
}

impl Iterator for Range {
    type Item = u32;
    fn next(&mut self) -> Option<Self::Item> {
        if self.start < self.end {
            let val = self.start;
            self.start += 1;
            Some(val)
        } else {
            None
        }
    }
}

let range = Range { start: 0, end: 5 };
let collected: Vec<u32> = range.collect();  // [0, 1, 2, 3, 4]
```
