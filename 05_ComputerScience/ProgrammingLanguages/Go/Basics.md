# Go 基础语法

## 包和导入

```go
package main

import (
    "fmt"
    "math/rand"
    "time"
)

// 导入别名
import f "fmt"

// 匿名导入（仅执行 init 函数）
import _ "image/png"
```

## 变量

```go
// var 声明
var name string = "Go"
var version = 1.21         // 类型推断
var x, y int = 1, 2        // 多变量声明

// 短变量声明（只能在函数内）
count := 42
msg := "Hello"

// 零值（默认值）
var i int       // 0
var f float64   // 0
var b bool      // false
var s string    // ""（空字符串）

// 分组声明
var (
    appName  = "MyApp"
    appPort  = 8080
    debug    = false
)
```

## 常量

```go
const Pi = 3.14159
const StatusOK = 200

// iota 枚举
const (
    Monday = iota      // 0
    Tuesday            // 1
    Wednesday          // 2
    Thursday
    Friday
    Saturday
    Sunday
)

const (
    _  = iota             // 忽略 0
    KB = 1 << (10 * iota) // 1024
    MB                    // 1048576
    GB                    // 1073741824
)
```

## 基本类型

```go
// 布尔
var ok bool = true

// 数字
var a int = -42
var b uint = 42
var c int8, int16, int32, int64
var d uint8, uint16, uint32, uint64
var e float32, float64
var f complex64, complex128

// byte = uint8
var b byte = 'A'

// rune = int32（Unicode 码点）
var r rune = '中'

// 字符串
var s1 string = "Hello"
var s2 = `多行
原始字符串`
```

## 控制流

```go
// if/else 支持语句
if x := compute(); x > 0 {
    fmt.Println("正数")
} else if x < 0 {
    fmt.Println("负数")
} else {
    fmt.Println("零")
}

// for（Go 只有 for 循环）
// 标准 for
for i := 0; i < 10; i++ {
    fmt.Println(i)
}

// 类似 while
sum := 1
for sum < 1000 {
    sum += sum
}

// 无限循环
for {
    // 直到 break
}

// range 遍历
nums := []int{1, 2, 3}
for index, value := range nums {
    fmt.Printf("索引 %d: %d\n", index, value)
}

for key, value := range map[string]string{"a": "A"} {
    fmt.Println(key, value)
}

for _, ch := range "Go语言" {
    fmt.Printf("%c ", ch)  // G o 语 言
}

// switch
switch os := runtime.GOOS; os {
case "darwin":
    fmt.Println("macOS")
case "linux":
    fmt.Println("Linux")
default:
    fmt.Printf("%s\n", os)
}

// switch 无表达式（替代 if-else 链）
score := 85
switch {
case score >= 90:
    fmt.Println("优秀")
case score >= 80:
    fmt.Println("良好")
case score >= 60:
    fmt.Println("及格")
default:
    fmt.Println("不及格")
}
```

## 函数

```go
// 多返回值
func divide(a, b int) (int, error) {
    if b == 0 {
        return 0, errors.New("除数不能为零")
    }
    return a / b, nil
}

// 命名返回值
func split(sum int) (x, y int) {
    x = sum * 4 / 9
    y = sum - x
    return  // 裸返回
}

// defer 延迟执行
func readFile() {
    f, err := os.Open("file.txt")
    if err != nil {
        return
    }
    defer f.Close()     // 函数返回时执行
    defer fmt.Println("最后执行")  // 后进先出
}

// 变参函数
func sum(nums ...int) int {
    total := 0
    for _, n := range nums {
        total += n
    }
    return total
}
sum(1, 2, 3)
nums := []int{1, 2, 3}
sum(nums...)  // 展开切片

// 函数值（闭包）
func adder() func(int) int {
    sum := 0
    return func(x int) int {
        sum += x
        return sum
    }
}
pos, neg := adder(), adder()
pos(1)   // 1
neg(-2)  // -2
```

## 指针

```go
var x int = 42
var p *int = &x   // p 指向 x 的地址
fmt.Println(*p)   // 42（解引用）
*p = 21           // 通过指针修改 x
fmt.Println(x)    // 21

// Go 不支持指针算术
// p++  // 编译错误
```

## 结构体和方法

```go
type Person struct {
    Name string
    Age  int
}

// 创建
p1 := Person{"Alice", 30}
p2 := Person{Name: "Bob", Age: 25}
p3 := Person{Name: "Charlie"}  // Age = 0
var p4 Person  // 零值

// 方法（值接收者）
func (p Person) String() string {
    return fmt.Sprintf("%s (%d)", p.Name, p.Age)
}

// 方法（指针接收者）
func (p *Person) Birthday() {
    p.Age++
}

// 结构体嵌入（类似继承）
type Employee struct {
    Person             // 嵌入
    Company string
}
e := Employee{Person{Name: "Dave"}, "Acme"}
fmt.Println(e.Name)    // 访问嵌入字段
```

## 接口

```go
// 隐式实现
type Stringer interface {
    String() string
}

// 任何实现了 String() string 的类型都满足 Stringer 接口
type Book struct {
    Title string
}

func (b Book) String() string {
    return b.Title
}

// 接口值
var s Stringer = Book{"The Go Programming Language"}
fmt.Println(s.String())

// 空接口（任意类型）
var anything interface{}
anything = 42
anything = "hello"
anything = Person{}

// 类型断言
val, ok := anything.(string)
if ok {
    fmt.Println("字符串:", val)
}

// 类型 switch
switch v := anything.(type) {
case int:
    fmt.Printf("整数 %d\n", v)
case string:
    fmt.Printf("字符串 %s\n", v)
default:
    fmt.Printf("未知类型 %T\n", v)
}
```

## 错误处理

```go
// error 接口
type error interface {
    Error() string
}

// 自定义错误
type ValidationError struct {
    Field string
    Value interface{}
}

func (e *ValidationError) Error() string {
    return fmt.Sprintf("字段 %s 的值 %v 无效", e.Field, e.Value)
}

// 使用
func validateAge(age int) error {
    if age < 0 || age > 150 {
        return &ValidationError{"age", age}
    }
    return nil
}

// panic/recover
func safeDivide(a, b int) (result int) {
    defer func() {
        if r := recover(); r != nil {
            fmt.Println("恢复:", r)
            result = 0
        }
    }()
    return a / b  // 如果 b=0 会 panic
}
```
