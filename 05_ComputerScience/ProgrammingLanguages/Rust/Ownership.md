# Rust 所有权系统

## 所有权规则

```rust
// 规则 1: Rust 中每个值都有一个所有者
// 规则 2: 每个值同时只能有一个所有者
// 规则 3: 当所有者离开作用域，值将被丢弃

{                           // s 尚未声明
    let s = String::from("hello");  // s 有效
    // 使用 s
}                           // 作用域结束，s 被 drop，内存释放
```

## 移动语义

```rust
// 移动：所有权转移
let s1 = String::from("hello");
let s2 = s1;  // s1 的所有权移动到 s2
// println!("{}", s1);  // 编译错误！s1 已失效

// 基本类型实现 Copy trait，不发生移动
let x = 5;
let y = x;    // x 仍然有效（i32 实现了 Copy）
println!("x = {}, y = {}", x, y);

// 函数参数和返回值的所有权转移
fn takes_ownership(s: String) {
    println!("{}", s);
}  // s 被 drop

fn gives_ownership() -> String {
    String::from("hello")
}

let s = gives_ownership();   // s 获得所有权
takes_ownership(s);          // 所有权转移到函数
// println!("{}", s);        // 编译错误！
```

## Clone 与 Copy

```rust
// Clone: 深拷贝（堆上数据）
let s1 = String::from("hello");
let s2 = s1.clone();
println!("s1 = {}, s2 = {}", s1, s2);  // 两者都有效

// Copy: 栈上复制（实现 Copy trait 的类型）
#[derive(Debug, Copy, Clone)]
struct Point {
    x: i32,
    y: i32,
}

// 实现 Copy 的类型：整数、浮点数、布尔、字符、元组（仅含 Copy 类型时）
```

## 借用

```rust
// 不可变借用 &T
fn calculate_length(s: &String) -> usize {
    s.len()
}  // s 不拥有所有权，离开作用域时不 drop

let s = String::from("hello");
let len = calculate_length(&s);  // 借用
println!("{} length: {}", s, len);  // s 仍然有效

// 可变借用 &mut T
fn change(s: &mut String) {
    s.push_str(", world");
}

let mut s = String::from("hello");
change(&mut s);
println!("{}", s);  // hello, world

// 借用规则
// 1. 任意时刻只能有一个可变引用，或任意多个不可变引用
// 2. 引用必须始终有效

let mut s = String::from("hello");
let r1 = &s;      // OK
let r2 = &s;      // OK
// let r3 = &mut s; // 编译错误！已有不可变引用
println!("{} {}", r1, r2);  // r1, r2 最后一次使用

let r3 = &mut s;  // 现在可以了
r3.push_str("!");

// 悬垂引用（编译器会阻止）
// fn dangle() -> &String {
//     let s = String::from("hello");
//     &s  // 编译错误：返回局部变量的引用
// }
```

## 切片

```rust
// 字符串切片 &str
let s = String::from("hello world");
let hello = &s[0..5];   // "hello"
let world = &s[6..11];  // "world"
let whole = &s[..];     // "hello world"

// 数组切片 &[T]
let arr = [1, 2, 3, 4, 5];
let slice = &arr[1..3];  // [2, 3]

// 函数参数中的切片
fn first_word(s: &str) -> &str {
    let bytes = s.as_bytes();
    for (i, &item) in bytes.iter().enumerate() {
        if item == b' ' {
            return &s[..i];
        }
    }
    &s[..]
}

let word = first_word("hello world");  // "hello"
```

## 生命周期注解

```rust
// 泛型生命周期参数
// &'a T 表示引用至少与 'a 一样长

fn longest<'a>(x: &'a str, y: &'a str) -> &'a str {
    if x.len() > y.len() { x } else { y }
}

let s1 = String::from("long");
let result;
{
    let s2 = String::from("short");
    result = longest(s1.as_str(), s2.as_str());
    // 编译错误！result 可能引用 s2，但 s2 即将释放
}

// 生命周期结构体
struct Excerpt<'a> {
    part: &'a str,
}

let novel = String::from("Call me Ishmael...");
let first_sentence = novel.split('.').next().expect("no .");
let excerpt = Excerpt { part: first_sentence };

// 生命周期省略规则
// 1. 每个输入引用都有自己的生命周期
// 2. 如果只有一个输入生命周期，它被赋予所有输出引用
// 3. 如果是 &self 或 &mut self，self 的生命周期被赋予所有输出引用

fn first_word(s: &str) -> &str {  // 省略后等价于 <'a>(&'a str) -> &'a str
    &s[..]
}

// 'static 生命周期
// 存活于整个程序期间
let s: &'static str = "Hello";  // 字符串字面量是 'static
```
