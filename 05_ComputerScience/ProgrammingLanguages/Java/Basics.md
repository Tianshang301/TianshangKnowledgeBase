---
aliases: [Basics]
tags: ['ProgrammingLanguages', 'Java', 'Basics']
created: 2026-05-16
updated: 2026-05-16
---

# Java 基础语法

## 数据类型

Java 数据类型分为基本类型（Primitive Types）和引用类型（Reference Types）。

### 基本类型

| 类型 | 大小 | 默认值 | 范围 |
|------|------|--------|------|
| byte | 8位 | 0 | -128 ~ 127 |
| short | 16位 | 0 | -32768 ~ 32767 |
| int | 32位 | 0 | -2^31 ~ 2^31-1 |
| long | 64位 | 0L | -2^63 ~ 2^63-1 |
| float | 32位 | 0.0f | ±3.4E-38 ~ ±3.4E+38 |
| double | 64位 | 0.0d | ±1.7E-308 ~ ±1.7E+308 |
| char | 16位 | '\u0000' | 0 ~ 65535 |
| boolean | JVM 实现相关 | false | true/false |

```java
int a = 42;
long b = 100L;
float f = 3.14f;
double d = 3.14159;
char c = 'A';
boolean flag = true;
```

### 引用类型

类、接口、数组、枚举都属于引用类型，默认值为 `null`。

```java
String s = "Hello";
int[] arr = new int[10];
```

### 自动装箱与拆箱

```java
Integer x = 100;       // 自动装箱: int -> Integer
int y = x;            // 自动拆箱: Integer -> int
```

`-128 ~ 127` 之间的整数缓存池对 `Integer` 生效。

## 变量

### 变量类型

```java
public class VariableDemo {
    static int classVar = 1;       // 类变量（静态变量）
    int instanceVar = 2;           // 实例变量
    final int CONSTANT = 100;      // 常量（不可变）

    public void method() {
        int localVar = 3;          // 局部变量（必须初始化）
        System.out.println(localVar);
    }
}
```

## 运算符

| 类别 | 运算符 |
|------|--------|
| 算术 | +, -, *, /, %, ++, -- |
| 关系 | ==, !=, >, <, >=, <= |
| 逻辑 | &&, ll, ! |
| 位运算 | &, l, ^, ~, <<, >>, >>> |
| 赋值 | =, +=, -=, *=, /=, %= |
| 三元 | ? : |

```java
int x = 10, y = 20;
int max = (x > y) ? x : y;       // 三元运算符
boolean isAdult = age >= 18 ? true : false;
```

## 控制流

### if-else

```java
int score = 85;
if (score >= 90) {
    System.out.println("优秀");
} else if (score >= 60) {
    System.out.println("及格");
} else {
    System.out.println("不及格");
}
```

### switch

```java
String day = "MONDAY";
switch (day) {
    case "MONDAY":
    case "FRIDAY":
        System.out.println("工作日");
        break;
    case "SATURDAY":
    case "SUNDAY":
        System.out.println("周末");
        break;
    default:
        System.out.println("未知");
}
```

Java 14+ 支持 switch 表达式：

```java
String result = switch (day) {
    case "MONDAY", "FRIDAY" -> "工作日";
    case "SATURDAY", "SUNDAY" -> "周末";
    default -> "未知";
};
```

### for

```java
for (int i = 0; i < 10; i++) {
    System.out.println(i);
}

// 增强 for 循环
int[] numbers = {1, 2, 3, 4, 5};
for (int n : numbers) {
    System.out.println(n);
}
```

### while / do-while

```java
int i = 0;
while (i < 5) {
    System.out.println(i++);
}

int j = 0;
do {
    System.out.println(j++);
} while (j < 5);  // 至少执行一次
```

## 数组

```java
// 声明和初始化
int[] arr1 = new int[5];
int[] arr2 = {1, 2, 3, 4, 5};
int[][] matrix = {{1, 2}, {3, 4}};

// 遍历
for (int i = 0; i < arr2.length; i++) {
    System.out.println(arr2[i]);
}

// 数组工具类
int[] copy = Arrays.copyOf(arr2, 10);
Arrays.sort(arr2);
int index = Arrays.binarySearch(arr2, 3);
```

## 字符串

### String（不可变）

```java
String s1 = "Hello";
String s2 = new String("World");
String s3 = s1 + " " + s2;  // "Hello World"

// 常用方法
s1.length();               // 5
s1.charAt(0);              // 'H'
s1.substring(1, 3);        // "el"
s1.equals("Hello");        // true
s1.contains("ell");        // true
s1.indexOf("l");           // 2
s1.replace("l", "p");      // "Heppo"
s1.toUpperCase();          // "HELLO"
```

### StringBuilder（可变、非线程安全）

```java
StringBuilder sb = new StringBuilder();
sb.append("Hello");
sb.append(" ");
sb.append("World");
sb.insert(5, ",");
sb.delete(5, 6);
String result = sb.toString();  // "HelloWorld"
```

### StringBuffer（可变、线程安全）

```java
StringBuffer sbf = new StringBuffer();
sbf.append("Hello");
String result = sbf.toString();
```

## 方法

### 方法重载

```java
public class MathUtils {
    public int add(int a, int b) {
        return a + b;
    }

    public double add(double a, double b) {
        return a + b;
    }

    public int add(int a, int b, int c) {
        return a + b + c;
    }
}
```

### 可变参数（Varargs）

```java
public int sum(int... numbers) {
    int total = 0;
    for (int n : numbers) {
        total += n;
    }
    return total;
}

// 调用
sum(1, 2, 3);
sum(1, 2, 3, 4, 5);
```

### 值传递（Pass-by-Value）

Java 严格按值传递。基本类型传值的副本，引用类型传引用的副本。

```java
public static void main(String[] args) {
    int x = 10;
    changePrimitive(x);
    System.out.println(x);  // 10（不变）

    StringBuilder sb = new StringBuilder("Hello");
    changeReference(sb);
    System.out.println(sb);  // "Hello World"（对象内容改变）
}

static void changePrimitive(int a) {
    a = 20;
}

static void changeReference(StringBuilder s) {
    s.append(" World");
}
```

## 异常处理

### try-catch-finally

```java
try {
    int result = 10 / 0;
} catch (ArithmeticException e) {
    System.err.println("除数不能为零: " + e.getMessage());
} finally {
    System.out.println("总是执行");
}
```

### try-with-resources（Java 7+）

自动关闭实现了 `AutoCloseable` 的资源：

```java
try (BufferedReader br = new BufferedReader(new FileReader("file.txt"))) {
    String line;
    while ((line = br.readLine()) != null) {
        System.out.println(line);
    }
} catch (IOException e) {
    e.printStackTrace();
}
```

### 受检异常 vs 非受检异常

| 特性 | Checked Exception | Unchecked Exception |
|------|-------------------|---------------------|
| 继承 | Exception（不含 RuntimeException） | RuntimeException |
| 编译检查 | 必须处理或声明 | 可选择性处理 |
| 示例 | IOException, SQLException | NullPointerException, IllegalArgumentException |
| 使用场景 | 外部因素（文件不存在、网络故障） | 程序 bug（空指针、越界） |

```java
// 受检异常必须 throws 或 try-catch
public void readFile() throws IOException {
    Files.readAllLines(Paths.get("test.txt"));
}

// 非受检异常不需要声明
public void process(String s) {
    if (s == null) {
        throw new IllegalArgumentException("参数不能为空");
    }
}
```

## 包和导入

```java
package com.example.myapp;    // 包声明

import java.util.List;         // 导入单个类
import java.util.*;            // 导入所有类
import static java.lang.Math.*; // 静态导入
```

### 包访问权限

| 修饰符 | 同类 | 同包 | 子类 | 所有类 |
|--------|------|------|------|--------|
| private | ✓ | - | - | - |
| default | ✓ | ✓ | - | - |
| protected | ✓ | ✓ | ✓ | - |
| public | ✓ | ✓ | ✓ | ✓ |

