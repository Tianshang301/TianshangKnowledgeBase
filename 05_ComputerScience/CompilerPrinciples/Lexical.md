---
aliases: [Lexical]
tags: ['CompilerPrinciples', 'Lexical']
created: 2026-05-16
updated: 2026-05-13
---

# 词法分析

## 一、概述

词法分析是编译器的第一阶段，将源代码字符序列转换为 token 序列。它读取源代码，识别出关键字、标识符、运算符、字面量等词法单元。

### 编译过程

```
源代码 → 词法分析 → Token 序列 → 语法分析 → 语义分析 → 中间代码 → 优化 → 目标代码
         (Lexer)           (Parser)
```

### Token 结构

```
Token = <Token 类型, Token 值, 位置信息>
```

```text
"int a = 10 + 20;"  →  Token 序列：
<int, "int", (1,1)>
<id, "a", (1,5)>
<op, "=", (1,7)>
<num, "10", (1,9)>
<op, "+", (1,12)>
<num, "20", (1,14)>
<delim, ";", (1,16)>
```

---

## 二、正则表达式

正则表达式用于描述词法规则。

### 基本符号

| 表达式 | 含义 | 说明 |
|--------|------|------|
| `a` | 字符 a | 单个字符 |
| `ε` | 空串 | 零长度字符串 |
| `a\|b` | 选择 | a 或 b |
| `ab` | 连接 | a 后跟 b |
| `a*` | 闭包 | 零个或多个 a |
| `a+` | 正闭包 | 一个或多个 a |
| `a?` | 可选 | 零个或一个 a |
| `[abc]` | 字符类 | a、b 或 c |
| `[a-z]` | 范围 | a 到 z 的任意字符 |
| `[^abc]` | 补集 | 非 a、b、c 的任意字符 |

### Token 模式定义

```text
关键字:    if|else|while|for|return|int|float|void
标识符:    [a-zA-Z_][a-zA-Z0-9_]*
整数:      [0-9]+
浮点数:    [0-9]+\.[0-9]*|\.?[0-9]+
科学计数:  [0-9]+(\.[0-9]*)?[eE][+-]?[0-9]+
字符串:    "([^"\\]|\\.)*"
注释:      //[^\n]*|/\*([^*]|\*+[^*/])*\*+/
空白:      [ \t\n\r]+
运算符:    +|-|*|/|==|!=|<|>|<=|>=|&&|\|\||!
分隔符:    ;|,|\(|\)|\{|\}|\[|\]
```

### 复杂 Token 示例

```text
// C 语言标识符
[a-zA-Z_][a-zA-Z0-9_]*

// 十六进制整数
0[xX][0-9a-fA-F]+

// 电子邮件（简化）
[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}

// IP 地址
([0-9]{1,3}\.){3}[0-9]{1,3}

// 单行注释
//.*

// 多行注释（嵌套版本）
/\*([^*]|\*[^/])*\*/
```

---

## 三、有限自动机

### NFA（非确定有限自动机）

NFA 是一个五元组 `M = (Q, Σ, δ, q0, F)`：

- **Q**：有限状态集合
- **Σ**：字母表
- **δ**：转移函数 `Q × (Σ ∪ {ε}) → P(Q)`
- **q0**：初始状态
- **F**：接受状态集合

NFA 的特点：
- 同一状态对同一输入可能有多个转移
- 支持 ε-转移（不消耗输入字符即可转移）

**示例：识别 `a*` 的 NFA**

```
状态: q0(初始,接受)
转移: q0 --a--> q0
```

**示例：识别 `a|b` 的 NFA**

```
      ε
q0 ──────▶ q1 ──a──▶ q3 (接受)
  \
   ε
    ────▶ q2 ──b──▶ q4 (接受)
```

### DFA（确定有限自动机）

DFA 是 NFA 的特例：
- 每个状态对每个输入符号最多有一个转移
- 没有 ε-转移
- 更易于实现（O(n) 时间复杂度）

**示例：识别 `a(b|c)*` 的 DFA**

```
q0 ──a──▶ q1 ──b──▶ q1
                  ──c──▶ q1
```

### 子集构造法（NFA → DFA）

将 NFA 的状态集合映射为 DFA 的状态：

```
算法：NFAtoDFA(NFA N) → DFA D

1. D 的初始状态 = ε-闭包(N 的初始状态)
2. 对每个未标记的 DFA 状态 T:
   a. 标记 T
   b. 对每个输入符号 a:
      U = ε-闭包(所有从 T 中状态经 a 到达的状态)
      if U 不在 D 的状态集合中:
          将 U 加入 D 的状态集合（未标记）
      D[T][a] = U
3. D 的接受状态 = 包含 NFA 接受状态的 DFA 状态
```

**示例**：将 `a|b` 的 NFA 转化为 DFA

```
NFA:
q0 --ε--> q1 --a--> q3(accept)
q0 --ε--> q2 --b--> q4(accept)

ε-闭包(q0) = {q0, q1, q2} → DFA 状态 A
  从 A 读 a: 可到 q3, ε-闭包(q3) = {q3} → DFA 状态 B(accept)
  从 A 读 b: 可到 q4, ε-闭包(q4) = {q4} → DFA 状态 C(accept)
```

### DFA 最小化

合并不可区分的状态：

```
算法：minimizeDFA(DFA D) → DFA D'

1. 将状态分为接受状态组和非接受状态组
2. 对每个组，按转移目标分组细分
3. 重复直到没有变化
4. 合并同一组内的状态
```

---

## 四、Lex/Flex 工具

### Lex 文件结构

```
%{
/* C 代码：头文件、全局变量 */
#include <stdio.h>
int line_num = 1;
%}

/* 正则表达式定义 */
letter     [a-zA-Z]
digit      [0-9]
identifier {letter}({letter}|{digit})*
number     {digit}+(\.{digit}+)?([eE][+-]?{digit}+)?

%%
/* 规则部分：模式 + 动作 */

{number}     { printf("NUM: %s\n", yytext); return NUM; }
{identifier} { printf("ID: %s\n", yytext); return ID; }
"if"         { return IF; }
"else"       { return ELSE; }
"while"      { return WHILE; }
"return"     { return RETURN; }
"+"          { return PLUS; }
"-"          { return MINUS; }
"*"          { return TIMES; }
"/"          { return DIVIDE; }
"=="         { return EQ; }
"!="         { return NE; }
"<"          { return LT; }
">"          { return GT; }
";"          { return SEMI; }
"("          { return LPAREN; }
")"          { return RPAREN; }
"{"          { return LBRACE; }
"}"          { return RBRACE; }
[ \t]        { /* 忽略空白 */ }
\n           { line_num++; }
"//".*       { /* 忽略单行注释 */ }
"/*"         { /* 处理多行注释 */
               char c;
               do {
                   while ((c = input()) != '*'');
                   c = input();
               } while (c != '/');
             }
.            { printf("非法字符: %s\n", yytext); }

%%
/* 辅助函数 */
int yywrap() { return 1; }

int main() {
    yylex();
    return 0;
}
```

### Flex 编译使用

```bash
flex lexer.l          # 生成 lex.yy.c
gcc lex.yy.c -lfl     # 编译为可执行文件
./a.out < input.txt   # 运行词法分析器
```

---

## 五、符号表管理

符号表在词法分析和后续阶段中记录标识符信息。

### 符号表结构

```
符号表条目:
┌─────────────────────────────────────┐
│ name       | "calculate"            │
│ type       | function               │
│ scope      | global                 │
│ return_type| int                    │
│ params     | [(int, "x"), (int, "y")]│
│ address    | 0x1000                 │
└─────────────────────────────────────┘
```

### 链式符号表实现

```c
#define MAX_SCOPE 100

// 符号表条目
typedef struct Symbol {
    char name[64];
    int type;        // 0: variable, 1: function, 2: array
    int data_type;   // 0: int, 1: float, 2: char
    int scope_level;
    struct Symbol *next;  // 链式冲突解决
} Symbol;

// 符号表（每个作用域一个）
typedef struct ScopeTable {
    Symbol *buckets[211];
    struct ScopeTable *parent;  // 外层作用域
} ScopeTable;

ScopeTable *current_scope;

// 插入符号
void insert_symbol(const char *name, int type, int data_type) {
    int hash = hash_function(name) % 211;
    Symbol *sym = malloc(sizeof(Symbol));
    strcpy(sym->name, name);
    sym->type = type;
    sym->data_type = data_type;
    sym->scope_level = current_scope->level;
    sym->next = current_scope->buckets[hash];
    current_scope->buckets[hash] = sym;
}

// 查找符号（逐层向上）
Symbol *lookup_symbol(const char *name) {
    for (ScopeTable *s = current_scope; s != NULL; s = s->parent) {
        int hash = hash_function(name) % 211;
        for (Symbol *sym = s->buckets[hash]; sym != NULL; sym = sym->next) {
            if (strcmp(sym->name, name) == 0)
                return sym;
        }
    }
    return NULL;
}
```

---

## 六、词法分析器生成器对比

| 工具 | 语言 | 特点 |
|------|------|------|
| Lex/Flex | C/C++ | 最经典，广泛使用 |
| JLex | Java | Java 词法分析器生成器 |
| ANTLR | Java/多语言 | 同时支持词法和语法 |
| Ragel | C/C++/Go/Ruby | 编译为状态机，效率高 |
| RE2C | C/C++ | 将正则编译为 DFA，速度极快 |

### 手写词法分析器

```c
// 简单的手写字词分析器
typedef enum {
    TOKEN_EOF, TOKEN_ID, TOKEN_NUM, TOKEN_IF, TOKEN_ELSE,
    TOKEN_PLUS, TOKEN_MINUS, TOKEN_MUL, TOKEN_DIV,
    TOKEN_ASSIGN, TOKEN_SEMI, TOKEN_LPAREN, TOKEN_RPAREN,
    TOKEN_LBRACE, TOKEN_RBRACE, TOKEN_ERROR
} TokenType;

typedef struct {
    TokenType type;
    char lexeme[256];
    int line;
    int column;
} Token;

Token current_token;
const char *source;
int pos = 0;

Token get_next_token() {
    skip_whitespace();
    Token token = { .line = line, .column = col };

    if (source[pos] == '\0') {
        token.type = TOKEN_EOF;
        return token;
    }

    // 识别标识符和关键字
    if (is_alpha(source[pos])) {
        int i = 0;
        while (is_alnum(source[pos]))
            token.lexeme[i++] = source[pos++];
        token.lexeme[i] = '\0';

        if (strcmp(token.lexeme, "if") == 0)    token.type = TOKEN_IF;
        else if (strcmp(token.lexeme, "else") == 0) token.type = TOKEN_ELSE;
        else token.type = TOKEN_ID;
        return token;
    }

    // 识别数字
    if (is_digit(source[pos])) {
        int i = 0;
        while (is_digit(source[pos]))
            token.lexeme[i++] = source[pos++];
        token.lexeme[i] = '\0';
        token.type = TOKEN_NUM;
        return token;
    }

    // 识别运算符和分隔符
    switch (source[pos++]) {
        case '+': token.type = TOKEN_PLUS; break;
        case '-': token.type = TOKEN_MINUS; break;
        case '*': token.type = TOKEN_MUL; break;
        case '/': token.type = TOKEN_DIV; break;
        case '=': token.type = TOKEN_ASSIGN; break;
        case ';': token.type = TOKEN_SEMI; break;
        case '(': token.type = TOKEN_LPAREN; break;
        case ')': token.type = TOKEN_RPAREN; break;
        case '{': token.type = TOKEN_LBRACE; break;
        case '}': token.type = TOKEN_RBRACE; break;
        default:  token.type = TOKEN_ERROR;
    }
    return token;
}
```
