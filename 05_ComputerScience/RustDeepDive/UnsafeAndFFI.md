---
aliases:
  - Rust unsafe
  - Rust FFI
  - unsafe Rust
  - 外部函数接口
tags:
  - Rust
  - unsafe
  - FFI
  - 裸指针
  - 计算机科学
created: 2026-06-27
updated: 2026-06-27
---

# unsafe与FFI

unsafe Rust 允许开发者绕过 Rust 的某些安全保证，用于底层系统编程和与外部代码交互。FFI（Foreign Function Interface）是 Rust 与其他语言互操作的标准机制。

## unsafe 基础

### unsafe 能做什么

unsafe 代码可以执行五种受限操作：

1. **解引用裸指针（Raw Pointer）**
2. **调用 unsafe 函数或方法**
3. **访问或修改可变静态变量（static mut）**
4. **实现 unsafe trait**
5. **访问 union 的字段**

```rust
fn main() {
    let mut num = 5;
    
    // 创建裸指针（安全）
    let r1 = &num as *const i32;
    let r2 = &mut num as *mut i32;
    
    // 解引用裸指针（需要 unsafe）
    unsafe {
        println!("r1 is: {}", *r1);
        *r2 = 10;
        println!("r2 is: {}", *r2);
    }
}
```

### 何时使用 unsafe

- **底层系统编程**：操作系统、驱动程序
- **性能关键代码**：绕过边界检查等
- **与 C 代码交互**：FFI 调用
- **实现 unsafe 数据结构**：链表、树等
- **硬件交互**：嵌入式系统

### unsafe 安全原则

- **最小化 unsafe 范围**：只在必要时使用 unsafe
- **封装 unsafe 代码**：提供安全的抽象接口
- **文档化安全条件**：说明调用者需要满足的条件
- **测试 unsafe 代码**：充分测试边界情况

## 裸指针

### 裸指针类型

```rust
// 不可变裸指针
let raw_const: *const i32 = &value as *const i32;

// 可变裸指针
let raw_mut: *mut i32 = &mut value as *mut i32;
```

### 裸指针操作

```rust
fn main() {
    let mut value = 42;
    let ptr = &mut value as *mut i32;
    
    unsafe {
        // 解引用
        println!("Value: {}", *ptr);
        
        // 修改值
        *ptr = 100;
        
        // 指针算术
        let arr = [1, 2, 3, 4, 5];
        let ptr = arr.as_ptr();
        for i in 0..5 {
            println!("arr[{}] = {}", i, *ptr.add(i));
        }
    }
}
```

### 指针有效性

```rust
// 有效指针条件：
// 1. 非空
// 2. 正确对齐
// 3. 指向有效内存
// 4. 满足借用规则（在解引用时）

fn is_valid_pointer(ptr: *const i32) -> bool {
    !ptr.is_null() && ptr.align_offset(std::mem::align_of::<i32>()) == 0
}
```

## unsafe 函数

### 定义 unsafe 函数

```rust
/// 将 slice 转换为另一个类型的 slice
///
/// # Safety
///
/// - `T` 和 `U` 必须具有相同的对齐方式
/// - `T` 的每个字节必须是 `U` 的有效值
unsafe fn cast_slice<T, U>(slice: &[T]) -> &[U] {
    let ptr = slice.as_ptr() as *const U;
    let len = slice.len() * std::mem::size_of::<T>() / std::mem::size_of::<U>();
    std::slice::from_raw_parts(ptr, len)
}
```

### 调用 unsafe 函数

```rust
fn main() {
    let bytes: &[u8] = &[0x01, 0x00, 0x00, 0x00];
    
    unsafe {
        // 安全调用条件：bytes 包含有效的 i32 值
        let ints = cast_slice::<u8, i32>(bytes);
        println!("Value: {}", ints[0]); // 1 (小端序)
    }
}
```

### 标准库 unsafe 函数示例

```rust
use std::mem;

fn main() {
    let mut value: i32 = 42;
    
    unsafe {
        // std::mem::transmute - 位模式转换
        let bytes: [u8; 4] = mem::transmute(value);
        
        // std::ptr::write - 写入指针位置
        let mut target = 0i32;
        ptr::write(&mut target, 100);
        
        // std::ptr::read - 从指针读取
        let read_value = ptr::read(&target);
        
        // std::alloc::alloc - 分配内存
        let layout = Layout::new::<i32>();
        let ptr = alloc::alloc(layout) as *mut i32;
        ptr::write(ptr, 42);
        println!("Allocated: {}", *ptr);
        alloc::dealloc(ptr as *mut u8, layout);
    }
}
```

## 静态变量

### 不可变静态变量

```rust
// 不可变静态变量（安全）
static MAX_POINTS: u32 = 100_000;

fn main() {
    println!("Max points: {}", MAX_POINTS);
}
```

### 可变静态变量

```rust
// 可变静态变量（不安全）
static mut COUNTER: u32 = 0;

fn add_to_counter(inc: u32) {
    unsafe {
        COUNTER += inc;
    }
}

fn main() {
    add_to_counter(3);
    unsafe {
        println!("COUNTER: {}", COUNTER);
    }
}
```

### 线程安全的静态变量

```rust
use std::sync::atomic::{AtomicU32, Ordering};

// 原子类型的静态变量（安全）
static ATOMIC_COUNTER: AtomicU32 = AtomicU32::new(0);

fn increment() {
    ATOMIC_COUNTER.fetch_add(1, Ordering::Relaxed);
}

fn main() {
    increment();
    println!("Counter: {}", ATOMIC_COUNTER.load(Ordering::Relaxed));
}
```

## unsafe trait

### 定义 unsafe trait

```rust
/// # Safety
/// 实现者必须确保 `is_valid` 对有效值返回 true
unsafe trait Validate {
    fn is_valid(&self) -> bool;
}

struct NonNullPtr(*mut i32);

unsafe impl Validate for NonNullPtr {
    fn is_valid(&self) -> bool {
        !self.0.is_null()
    }
}
```

### 标准库 unsafe trait

```rust
// Send - 可以安全地在线程间转移所有权
// Sync - 可以安全地在线程间共享引用

// 手动实现 Send/Sync（通常自动派生）
unsafe impl Send for MyType {}
unsafe impl Sync for MyType {}
```

## FFI 基础

### extern 关键字

```rust
// 声明外部 C 函数
extern "C" {
    fn abs(input: i32) -> i32;
    fn sqrt(input: f64) -> f64;
}

fn main() {
    unsafe {
        println!("Absolute value of -3: {}", abs(-3));
        println!("Square root of 9: {}", sqrt(9.0));
    }
}
```

### 导出函数给 C

```rust
// 导出函数供 C 代码调用
#[no_mangle]
pub extern "C" fn rust_function(x: i32) -> i32 {
    x * 2
}

// 使用 C ABI
#[no_mangle]
pub extern "C" fn add(a: i32, b: i32) -> i32 {
    a + b
}
```

### CMakeLists.txt 集成示例

```cmake
# CMakeLists.txt
add_library(mylib STATIC IMPORTED)
set_target_properties(mylib PROPERTIES
    IMPORTED_LOCATION "/path/to/libmylib.a"
)

target_link_libraries(myapp mylib)
```

## bindgen

### 自动生成绑定

bindgen 自动从 C/C++ 头文件生成 Rust FFI 绑定：

```rust
// build.rs
fn main() {
    println!("cargo:rerun-if-changed=wrapper.h");
    
    let bindings = bindgen::Builder::default()
        .header("wrapper.h")
        .parse_callbacks(Box::new(bindgen::CargoCallbacks))
        .generate()
        .expect("Unable to generate bindings");
    
    let out_path = std::path::PathBuf::from(std::env::var("OUT_DIR").unwrap());
    bindings
        .write_to_file(out_path.join("bindings.rs"))
        .expect("Couldn't write bindings!");
}
```

### 使用生成的绑定

```rust
// wrapper.h
#include <math.h>
#include <stdlib.h>

// src/lib.rs
#![allow(non_upper_case_globals)]
#![allow(non_camel_case_types)]
#![allow(non_snake_case)]

include!(concat!(env!("OUT_DIR"), "/bindings.rs"));

pub fn safe_sqrt(x: f64) -> f64 {
    unsafe { sqrt(x) }
}
```

## cbindgen

### 生成 C 头文件

cbindgen 从 Rust 代码生成 C/C++ 头文件：

```rust
// src/lib.rs
/// Opaque handle to Rust object
pub struct RustObject {
    // 私有字段
}

/// 创建新的 RustObject
#[no_mangle]
pub extern "C" fn rust_object_new() -> *mut RustObject {
    Box::into_raw(Box::new(RustObject {}))
}

/// 释放 RustObject
#[no_mangle]
pub extern "C" fn rust_object_free(obj: *mut RustObject) {
    if !obj.is_null() {
        unsafe {
            drop(Box::from_raw(obj));
        }
    }
}

/// 使用 RustObject
#[no_mangle]
pub extern "C" fn rust_object_process(obj: *const RustObject) -> i32 {
    // 处理逻辑
    42
}
```

### cbindgen.toml 配置

```toml
language = "C"
header = "/* Auto-generated bindings */"
include_guard = "MY_RUST_LIB_H"
autogen_warning = "/* Warning: auto-generated file */"
```

## 内存布局

### repr 属性

```rust
// C 布局
#[repr(C)]
struct CLayout {
    x: i32,
    y: i32,
}

// 透明布局（与内部类型相同）
#[repr(transparent)]
struct Wrapper(i32);

// 打包布局
#[repr(C, packed)]
struct Packed {
    a: u8,
    b: u32,
    c: u8,
}

// 对齐布局
#[repr(C, align(8))]
struct Aligned {
    x: i32,
}
```

### 布局兼容性

```rust
// 确保布局兼容
#[repr(C)]
union MyUnion {
    i: i32,
    f: f32,
}

#[repr(C)]
struct CCompatible {
    tag: u32,
    data: MyUnion,
}
```

## 安全封装模式

### 封装 unsafe 代码

```rust
/// 安全的 FFI 封装
mod ffi {
    extern "C" {
        fn c_function(input: i32) -> i32;
    }
    
    /// 安全的包装函数
    pub fn safe_function(input: i32) -> i32 {
        // 可以在这里添加安全检查
        unsafe { c_function(input) }
    }
}

// 使用安全接口
fn main() {
    let result = ffi::safe_function(42);
}
``RAII 模式

```rust
struct SafeWrapper {
    ptr: *mut u8,
    len: usize,
}

impl SafeWrapper {
    fn new(data: &[u8]) -> Self {
        let ptr = unsafe {
            let layout = Layout::array::<u8>(data.len()).unwrap();
            let ptr = alloc::alloc(layout);
            ptr::copy_nonoverlapping(data.as_ptr(), ptr, data.len());
            ptr
        };
        SafeWrapper { ptr, len: data.len() }
    }
    
    fn as_slice(&self) -> &[u8] {
        unsafe { std::slice::from_raw_parts(self.ptr, self.len) }
    }
}

impl Drop for SafeWrapper {
    fn drop(&mut self) {
        unsafe {
            let layout = Layout::array::<u8>(self.len).unwrap();
            alloc::dealloc(self.ptr, layout);
        }
    }
}
```

## 常见 FFI 模式

### 字符串处理

```rust
use std::ffi::{CStr, CString};
use std::os::raw::c_char;

/// 接收 C 字符串
#[no_mangle]
pub extern "C" fn process_string(input: *const c_char) -> i32 {
    let c_str = unsafe {
        assert!(!input.is_null());
        CStr::from_ptr(input)
    };
    
    let r_str = c_str.to_str().unwrap();
    r_str.len() as i32
}

/// 返回 C 字符串
#[no_mangle]
pub extern "C" fn get_string() -> *mut c_char {
    let s = CString::new("Hello from Rust").unwrap();
    s.into_raw()
}

/// 释放 C 字符串
#[no_mangle]
pub extern "C" fn free_string(s: *mut c_char) {
    if !s.is_null() {
        unsafe { drop(CString::from_raw(s)); }
    }
}
```

### 回调函数

```rust
type Callback = extern "C" fn(i32) -> i32;

#[no_mangle]
pub extern "C" fn register_callback(cb: Callback) {
    // 存储回调以便后续调用
    unsafe {
        CALLBACK = Some(cb);
    }
}

static mut CALLBACK: Option<Callback> = None;

#[no_mangle]
pub extern "C" fn invoke_callback(value: i32) -> i32 {
    unsafe {
        if let Some(cb) = CALLBACK {
            cb(value)
        } else {
            -1
        }
    }
}
```

## 调试 unsafe 代码

### Miri

Miri 是 Rust 的实验性解释器，用于检测未定义行为：

```bash
# 运行 Miri
cargo +nightly miri test
cargo +nightly miri run
```

### AddressSanitizer

```bash
# 启用 AddressSanitizer
RUSTFLAGS="-Z sanitizer=address" cargo +nightly run
```

### 调试工具

- **Valgrind**：内存错误检测
- **GDB/LLDB**：调试器
- **cargo-careful**：额外的运行时检查

## 最佳实践

### unsafe 代码规范

1. **最小化 unsafe 范围**：只在必要时使用
2. **文档化 Safety 条件**：说明调用者需要满足的条件
3. **提供安全抽象**：封装 unsafe 代码为安全接口
4. **充分测试**：覆盖所有边界情况
5. **代码审查**：unsafe 代码需要额外审查

### FFI 设计原则

1. **清晰的边界**：明确 FFI 边界
2. **错误处理**：定义清晰的错误码
3. **资源所有权**：明确谁负责释放资源
4. **线程安全**：考虑多线程安全性
5. **版本兼容**：保持 ABI 稳定性

## 相关链接

- [[OwnershipAndBorrowing]] - Rust 所有权与借用
- [[AsyncRust]] - 异步 Rust
