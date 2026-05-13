# 各语言正则实现对比

## Python

```python
import re

# 基本用法
pattern = r'\d{3}-\d{4}'
text = "电话: 123-4567, 办公: 987-6543"

# 查找
match = re.search(pattern, text)
if match:
    print(match.group())       # "123-4567"
    print(match.start())       # 起始位置
    print(match.end())         # 结束位置

# 查找所有
matches = re.findall(pattern, text)
print(matches)                 # ['123-4567', '987-6543']

# 查找所有并返回迭代器
for match in re.finditer(pattern, text):
    print(match.group())

# 替换
result = re.sub(pattern, 'XXX-XXXX', text)
print(result)                  # "电话: XXX-XXXX, 办公: XXX-XXXX"

# 分割
parts = re.split(r'[,;]\s*', "a, b; c, d")
print(parts)                   # ['a', 'b', 'c', 'd']

# 编译（性能优化）
compiled = re.compile(r'\d{3}-\d{4}')
matches = compiled.findall(text)

# 标志位
re.IGNORECASE    # 忽略大小写
re.MULTILINE     # 多行模式（^ $ 匹配每行）
re.DOTALL        # . 匹配换行符
re.VERBOSE       # 详细模式（允许注释和空白）
re.ASCII         # ASCII 模式（\w \d \s 限于 ASCII）

# 详细模式示例
pattern = re.compile(r"""
    \d{3}      # 区号
    -          # 分隔符
    \d{4}      # 号码
""", re.VERBOSE)

# 分组
pattern = r'(\d{3})-(\d{4})'
match = re.search(pattern, "123-4567")
print(match.group(0))          # "123-4567"（完整匹配）
print(match.group(1))          # "123"
print(match.group(2))          # "4567"
print(match.groups())          # ('123', '4567')

# 命名分组
pattern = r'(?P<area>\d{3})-(?P<num>\d{4})'
match = re.search(pattern, "123-4567")
print(match.group('area'))     # "123"
print(match.group('num'))      # "4567"

# 前瞻和后顾
text = "price: $100, $200, $300"

# 正向前瞻：匹配 $ 后的数字
print(re.findall(r'\$(?=\d+)', text))       # ['$', '$', '$']

# 正向后顾：匹配 $ 后的数字
print(re.findall(r'(?<=\$)\d+', text))       # ['100', '200', '300']

# 替换中使用函数
def uppercase(match):
    return match.group(0).upper()

text = "hello world"
result = re.sub(r'\b\w', uppercase, text)
print(result)                  # "Hello World"

# regex 模块（第三方，功能更全）
import regex
# 支持递归、模糊匹配等
pattern = regex.compile(r'\((?:[^()]++|(?R))*\)')
match = regex.search(pattern, "before (nested (parens)) after")
print(match.group())           # "(nested (parens))"
```

## JavaScript

```javascript
// RegExp 对象
const re1 = /\d{3}-\d{4}/;
const re2 = new RegExp('\\d{3}-\\d{4}');

// 标志位
// g: 全局匹配
// i: 忽略大小写
// m: 多行模式
// s: dotAll（ES2018）
// u: Unicode
// y: 粘性匹配

const text = "电话: 123-4567, 办公: 987-6543";

// test()
console.log(re1.test(text));    // true

// exec()
let match;
while ((match = re1.exec(text)) !== null) {
    console.log(match[0]);       // "123-4567", "987-6543"
    console.log(match.index);    // 匹配位置
}

// String 方法
text.match(/\d{3}-\d{4}/);      // 返回第一个匹配
text.match(/\d{3}-\d{4}/g);     // 返回所有匹配
text.search(/\d{3}-\d{4}/);     // 返回索引
text.replace(/\d{3}-\d{4}/g, 'XXX-XXXX');  // 替换
text.split(/[,;]\s*/);          // 分割

// 命名分组（ES2018+）
const date = "2024-01-15";
const dateRe = /(?<year>\d{4})-(?<month>\d{2})-(?<day>\d{2})/;
const m = date.match(dateRe);
console.log(m.groups.year);     // "2024"
console.log(m.groups.month);    // "01"

// Lookbehind（ES2018+）
const price = "$100";
console.log(price.match(/(?<=\$)\d+/));  // ["100"]

// Unicode 属性转义（ES2018+）
const chinese = "你好World";
console.log(chinese.match(/\p{Script=Han}+/gu));  // ["你好"]

// 粘性匹配（y 标志）
const sticky = /abc/y;
sticky.lastIndex = 0;
console.log(sticky.test("abcabc"));   // true（匹配位置 0）
console.log(sticky.lastIndex);        // 3
console.log(sticky.test("abcabc"));   // true（匹配位置 3）
```

## Java

```java
import java.util.regex.*;

public class RegexExample {
    public static void main(String[] args) {
        String text = "电话: 123-4567, 办公: 987-6543";
        String pattern = "\\d{3}-\\d{4}";

        // Pattern.compile
        Pattern p = Pattern.compile(pattern);
        Matcher m = p.matcher(text);

        // find()
        while (m.find()) {
            System.out.println(m.group());       // 123-4567, 987-6543
            System.out.println(m.start() + "-" + m.end());
        }

        // matches() - 必须完全匹配
        boolean isMatch = Pattern.matches("\\d{3}-\\d{4}", "123-4567");

        // 替换
        String result = text.replaceAll(pattern, "XXX-XXXX");
        String result2 = text.replaceFirst(pattern, "XXX-XXXX");

        // 分割
        String[] parts = "a,b;c".split("[,;]");

        // 分组
        Pattern groupPattern = Pattern.compile("(\\d{3})-(\\d{4})");
        Matcher gm = groupPattern.matcher("123-4567");
        if (gm.find()) {
            System.out.println(gm.group(1));     // 123
            System.out.println(gm.group(2));     // 4567
        }

        // 标志位
        Pattern caseInsensitive = Pattern.compile("hello", Pattern.CASE_INSENSITIVE);
        Pattern multiline = Pattern.compile("^hello", Pattern.MULTILINE);
        Pattern dotall = Pattern.compile("hello.world", Pattern.DOTALL);
        Pattern comments = Pattern.compile(
            "\\d{3}  # area code\n" +
            "-       # separator\n" +
            "\\d{4}  # number",
            Pattern.COMMENTS
        );

        // 命名分组（Java 7+）
        Pattern named = Pattern.compile("(?<area>\\d{3})-(?<num>\\d{4})");
        Matcher nm = named.matcher("123-4567");
        if (nm.find()) {
            System.out.println(nm.group("area"));  // 123
            System.out.println(nm.group("num"));   // 4567
        }

        // 编译标志组合
        int flags = Pattern.CASE_INSENSITIVE | Pattern.MULTILINE | Pattern.DOTALL;
        Pattern combined = Pattern.compile("pattern", flags);
    }
}
```

## C#

```csharp
using System;
using System.Text.RegularExpressions;

class Program {
    static void Main() {
        string text = "电话: 123-4567, 办公: 987-6543";
        string pattern = @"\d{3}-\d{4}";

        // 静态方法
        Match match = Regex.Match(text, pattern);
        if (match.Success) {
            Console.WriteLine(match.Value);      // 123-4567
        }

        // 查找所有
        MatchCollection matches = Regex.Matches(text, pattern);
        foreach (Match m in matches) {
            Console.WriteLine(m.Value);
        }

        // 替换
        string result = Regex.Replace(text, pattern, "XXX-XXXX");

        // 分割
        string[] parts = Regex.Split("a,b;c", @"[,;]");

        // 编译正则（性能优化）
        Regex compiled = new Regex(pattern, RegexOptions.Compiled);
        compiled.Match(text);

        // 选项
        RegexOptions.IgnoreCase     // 忽略大小写
        RegexOptions.Multiline      // 多行模式
        RegexOptions.Singleline     // 单行模式（. 匹配换行）
        RegexOptions.ExplicitCapture // 仅显式分组
        RegexOptions.Compiled       // 编译为 IL
        RegexOptions.IgnorePatternWhitespace  // 忽略空白

        // 命名分组
        string datePattern = @"(?<year>\d{4})-(?<month>\d{2})-(?<day>\d{2})";
        Match dm = Regex.Match("2024-01-15", datePattern);
        if (dm.Success) {
            Console.WriteLine(dm.Groups["year"]);   // 2024
            Console.WriteLine(dm.Groups["month"]);  // 01
        }

        // 正向后顾
        string pricePattern = @"(?<=\$)\d+";
        MatchCollection prices = Regex.Matches("$100 $200 $300", pricePattern);
        foreach (Match p in prices) {
            Console.WriteLine(p.Value);  // 100, 200, 300
        }

        // 超时控制（防止灾难性回溯）
        try {
            Regex badPattern = new Regex(@"(a|aa|aaa)+b", RegexOptions.None, TimeSpan.FromSeconds(1));
            badPattern.Match("aaaaaaaaac");
        } catch (RegexMatchTimeoutException) {
            Console.WriteLine("正则超时");
        }

        // 平衡组（匹配嵌套结构）
        string nestedPattern = @"<div[^>]*>(?<open>)|</div>(?<-open>)|[^<>]*)*(?(open)(?!))";
        // 用于匹配嵌套的 <div> 标签
    }
}
```

## Go (regexp)

```go
package main

import (
    "fmt"
    "regexp"
)

func main() {
    text := "电话: 123-4567, 办公: 987-6543"

    // Compile
    re, err := regexp.Compile(`\d{3}-\d{4}`)
    if err != nil {
        panic(err)
    }

    // MustCompile（panic on error）
    re = regexp.MustCompile(`\d{3}-\d{4}`)

    // MatchString
    fmt.Println(re.MatchString(text))          // true

    // FindString
    fmt.Println(re.FindString(text))           // "123-4567"

    // FindAllString
    fmt.Println(re.FindAllString(text, -1))    // ["123-4567", "987-6543"]
    fmt.Println(re.FindAllString(text, 1))     // ["123-4567"]（只找 1 个）

    // FindStringSubmatch（分组）
    groupRe := regexp.MustCompile(`(\d{3})-(\d{4})`)
    match := groupRe.FindStringSubmatch("123-4567")
    fmt.Println(match[1])                      // "123"
    fmt.Println(match[2])                      // "4567"

    // 命名分组（通过索引访问）
    namedRe := regexp.MustCompile(`(?P<area>\d{3})-(?P<num>\d{4})`)
    match = namedRe.FindStringSubmatch("123-4567")
    fmt.Println(match[1])                      // "123"
    fmt.Println(match[2])                      // "4567"
    // 注意：Go 不支持通过名字访问分组

    // ReplaceAllString
    result := re.ReplaceAllString(text, "XXX-XXXX")
    fmt.Println(result)                        // "电话: XXX-XXXX, 办公: XXX-XXXX"

    // ReplaceAllStringFunc
    result = re.ReplaceAllStringFunc(text, func(s string) string {
        return "(已隐藏)"
    })
    fmt.Println(result)                        // "电话: (已隐藏), 办公: (已隐藏)"

    // Split
    parts := regexp.MustCompile(`[,;]\s*`).Split("a, b; c", -1)
    fmt.Println(parts)                         // ["a", "b", "c"]

    // RE2 限制（Go 使用 RE2 引擎）
    // ❌ 不支持：前瞻、后顾、反向引用、原子组、占有量词
    // ✅ 支持：基本匹配、分组、字符类、量词
}
```

## grep/sed/awk

```bash
# grep - 基本正则（BRE）
grep 'pattern' file
grep '^[A-Z]' file          # 大写字母开头行
grep '[0-9]\{3\}' file      # BRE 中 { } 需要转义
grep 'a\+' file             # BRE 中 + 需要转义

# grep - 扩展正则（ERE）
grep -E 'pattern' file
grep -E '^[A-Z]' file
grep -E '[0-9]{3}' file     # ERE 中 { } 不需要转义
grep -E 'a+' file           # ERE 中 + 不需要转义

# grep - Perl 兼容（PCRE）
grep -P '\d{3}-\d{4}' file  # PCRE 支持 \d 等

# grep 常用选项
grep -i 'pattern' file      # 忽略大小写
grep -r 'pattern' dir/      # 递归搜索
grep -l 'pattern' *         # 只输出文件名
grep -c 'pattern' file      # 计数
grep -v 'pattern' file      # 反向匹配
grep -n 'pattern' file      # 显示行号
grep -o 'pattern' file      # 只输出匹配部分
grep -A2 'pattern' file     # 输出匹配行和后 2 行
grep -B2 'pattern' file     # 输出匹配行和前 2 行
grep -C2 'pattern' file     # 输出匹配行和前后各 2 行

# sed
sed 's/pattern/replacement/' file         # 替换每行第一个
sed 's/pattern/replacement/g' file        # 替换全部
sed 's/pattern/replacement/2' file        # 替换第二个
sed -i 's/old/new/g' file                 # 直接修改文件
sed -E 's/([0-9]{3})-([0-9]{4})/\1****/' file  # ERE 分组

# sed 地址范围
sed '3s/pattern/replacement/' file        # 只在第 3 行
sed '1,5s/pattern/replacement/' file      # 1-5 行
sed '/^#/s/pattern/replacement/' file     # 注释行
sed '/start/,/end/s/pattern/replacement/' file  # 范围

# awk
awk '/pattern/ {print}' file              # 打印匹配行
awk '{gsub(/pattern/, "replacement"); print}' file  # 替换
awk 'match($0, /[0-9]+/) {print substr($0, RSTART, RLENGTH)}' file  # 提取匹配

# GNU 扩展
grep -oP '\K\d+' file                     # \K 重置匹配起点（类似 lookbehind）
grep -oP '(?<=abc)\d+' file              # 前瞻（GNU grep 支持）
# grep -oP '(?<!abc)def' file            # 后顾（部分版本不支持）
```

## Rust (regex crate)

```rust
use regex::Regex;

fn main() {
    let text = "电话: 123-4567, 办公: 987-6543";

    // 编译
    let re = Regex::new(r"\d{3}-\d{4}").unwrap();

    // 匹配
    println!("{}", re.is_match(text));          // true

    // 查找第一个
    if let Some(m) = re.find(text) {
        println!("{}", m.as_str());             // "123-4567"
        println!("{}..{}", m.start(), m.end()); // 位置
    }

    // 查找所有
    for m in re.find_iter(text) {
        println!("{}", m.as_str());
    }

    // 捕获组
    let group_re = Regex::new(r"(\d{3})-(\d{4})").unwrap();
    if let Some(caps) = group_re.captures(text) {
        println!("{}", &caps[1]);               // "123"
        println!("{}", &caps[2]);               // "4567"
    }

    // 命名捕获
    let named = Regex::new(r"(?P<area>\d{3})-(?P<num>\d{4})").unwrap();
    if let Some(caps) = named.captures(text) {
        println!("{}", &caps["area"]);          // "123"
        println!("{}", &caps["num"]);           // "4567"
    }

    // 替换
    let result = re.replace_all(text, "XXX-XXXX");
    println!("{}", result);

    // 替换使用函数
    let result = re.replace_all(text, |caps: &regex::Captures| {
        format!("***-{}", &caps[2])
    });
    println!("{}", result);

    // 分割
    let parts: Vec<&str> = Regex::new(r"[,;]\s*").unwrap().split("a, b; c").collect();
    println!("{:?}", parts);                    // ["a", "b", "c"]

    // regex crate 限制
    // ❌ 不支持：前瞻、后顾、反向引用、原子组
    // ✅ 支持：基本匹配、分组、字符类、量词
}
```

## VSCode 查找替换

```regex
# VSCode 正则查找替换特性

# 基本语法
# 在查找框启用 .* 正则模式

# 捕获组引用
# 查找: (\w+)\.(\w+)
# 替换: $1_$2          # 转换为下划线命名

# 命名捕获组（VSCode 1.49+）
# 查找: (?<first>\w+)\.(?<second>\w+)
# 替换: ${first}_${second}

# 大小写转换
# \U...\E 转为大写（VSCode 1.74+）
# 查找: (\w+)
# 替换: \U$1\E          # 转为大写

# \L...\E 转为小写
# 查找: (\w+)
# 替换: \L$1\E          # 转为小写

# 实际案例
# 1. 交换键值对
# 查找: "(\w+)":\s*"([^"]+)"
# 替换: "$2": "$1"

# 2. 移除空行
# 查找: ^\s*\n
# 替换: (留空)

# 3. 添加行号
# 查找: ^
# 替换: $1. （需要循环操作）

# 4. 将驼峰转为下划线
# 查找: ([a-z])([A-Z])
# 替换: $1_$2
# 然后替换为小写

# 5. 提取所有 URL
# 查找: https?://[^\s"']+
# 替换: (留空或标记)

# 6. 格式化日期
# 查找: (\d{4})-(\d{2})-(\d{2})
# 替换: $3/$2/$1

# 7. 移除行末空格
# 查找: \s+$
# 替换: (留空)

# 8. 注释/取消注释
# 添加注释:
# 查找: ^(.+)$
# 替换: // $1

# 移除注释:
# 查找: ^\s*//\s?(.*)$
# 替换: $1
```

## 相关条目

- [[Basics]]
- [[Advanced]]
- [[Examples]]
- [[Bash]]
- [[Scripting]]
