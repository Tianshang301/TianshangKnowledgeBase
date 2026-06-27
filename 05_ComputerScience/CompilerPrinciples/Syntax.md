---
aliases: [Syntax]
tags: ['CompilerPrinciples', 'Syntax']
created: 2026-05-16
updated: 2026-05-16
---

# 语法分析

## 一、概述

语法分析（Parsing）将词法分析产生的 Token 序列按照文法规则组织成语法树（Parse Tree / Syntax Tree），验证源程序的语法正确性。

### 位置

```
Token 序列 → 语法分析器 → 语法树 → 语义分析器
```

---

## 二、上下文无关文法 (CFG)

### 定义

CFG 是一个四元组 `G = (V, T, P, S)`：

| 符号 | 含义 | 说明 |
|------|------|------|
| V | 非终结符集合 | 语法变量（如 `Expr`、`Stmt`） |
| T | 终结符集合 | Token（如 `+`、`id`、`num`） |
| P | 产生式集合 | 形如 `A → α` 的规则 |
| S | 起始符号 | S ∈ V，文法的开始 |

### 产生式示例

```text
Program  → StmtList
StmtList → Stmt StmtList | ε
Stmt     → AssignStmt | IfStmt | WhileStmt
AssignStmt → id = Expr ;
IfStmt   → if ( Expr ) Stmt | if ( Expr ) Stmt else Stmt
WhileStmt → while ( Expr ) Stmt
Expr     → Expr + Term | Expr - Term | Term
Term     → Term * Factor | Term / Factor | Factor
Factor   → ( Expr ) | id | num
```

### 推导

**最左推导**：每次替换最左边的非终结符

```text
Expr → Expr + Term
     → Term + Term
     → Factor + Term
     → id + Term
     → id + Term * Factor
     → id + Factor * Factor
     → id + id * Factor
     → id + id * id
```

**最右推导**：每次替换最右边的非终结符

```text
Expr → Expr + Term
     → Expr + Term * Factor
     → Expr + Term * id
     → Expr + Factor * id
     → Expr + id * id
     → Term + id * id
     → Factor + id * id
     → id + id * id
```

### 语法树

```
       Expr
      /    \
   Expr     Term
    |      / | \
   Term   Term * Factor
    |      |      |
  Factor  Factor  id
    |       |
   id      id
```

---

## 三、二义性

### 经典二义性：Dangling-Else

```text
Stmt → if Expr then Stmt
     | if Expr then Stmt else Stmt
     | OtherStmt
```

对于输入 `if a then if b then c else d`，有两种解释：

```text
匹配1:  if a then (if b then c else d)    -- 最近的 if 匹配 else
匹配2:  if a then (if b then c) else d    -- else 匹配外层 if
```

**消除二义性**：规定 else 匹配最近的未匹配 if，或改写文法：

```text
Stmt     → MatchedStmt | OpenStmt
MatchedStmt → if Expr then MatchedStmt else MatchedStmt
           | OtherStmt
OpenStmt → if Expr then Stmt
         | if Expr then MatchedStmt else OpenStmt
```

### 运算符优先级二义性

```text
// 二义性：1 + 2 * 3 可以是 (1+2)*3 或 1+(2*3)
// 通过分层消除
Expr  → Expr + Term | Expr - Term | Term
Term  → Term * Factor | Term / Factor | Factor
Factor → ( Expr ) | id | num
```

---

## 四、LL 分析

LL(k) 分析从左到右扫描、最左推导、向前看 k 个 token。

### FIRST 集合

计算每个非终结符可能开头的终结符集合。

```text
算法：
1. 如果 X 是终结符，FIRST(X) = {X}
2. 如果 X → ε，加入 ε 到 FIRST(X)
3. 如果 X → Y1 Y2 ... Yk:
   a. 将 FIRST(Y1) 中非 ε 的元素加入 FIRST(X)
   b. 如果 ε ∈ FIRST(Y1)，加入 FIRST(Y2) 的非 ε 元素
   c. 重复直到所有 Yi 都能推出 ε
```

示例：

```text
Expr  → Term Expr'
Expr' → + Term Expr' | ε
Term  → Factor Term'
Term' → * Factor Term' | ε
Factor → ( Expr ) | id

FIRST(Expr)   = { (, id }
FIRST(Expr')  = { +, ε }
FIRST(Term)   = { (, id }
FIRST(Term')  = { *, ε }
FIRST(Factor) = { (, id }
```

### FOLLOW 集合

计算可能跟在非终结符之后的终结符集合。

```text
算法：
1. 将 $ 加入 FOLLOW(S)
2. 对于 A → αBβ:
   a. 将 FIRST(β) 的非 ε 元素加入 FOLLOW(B)
   b. 如果 ε ∈ FIRST(β)，将 FOLLOW(A) 加入 FOLLOW(B)
3. 对于 A → αB，将 FOLLOW(A) 加入 FOLLOW(B)
```

示例：

```text
FOLLOW(Expr)   = { $, ) }
FOLLOW(Expr')  = { $, ) }
FOLLOW(Term)   = { +, $, ) }
FOLLOW(Term')  = { +, $, ) }
FOLLOW(Factor) = { *, +, $, ) }
```

### 预测分析表

| 非终结符 | id | + | * | ( | ) | $ |
|----------|----|----|----|----|----|----|
| Expr | Term Expr' | | | Term Expr' | | |
| Expr' | | + Term Expr' | | | ε | ε |
| Term | Factor Term' | | | Factor Term' | | |
| Term' | | ε | * Factor Term' | | ε | ε |
| Factor | id | | | ( Expr ) | | |

### 递归下降分析

```c
// 递归下降语法分析器（手写）
typedef struct {
    Token tokens[MAX_TOKENS];
    int pos;
} Parser;

Parser parser;

Token peek() { return parser.tokens[parser.pos]; }
Token consume() { return parser.tokens[parser.pos++]; }

// Expr → Term Expr'
ASTNode *parse_expr() {
    ASTNode *left = parse_term();
    while (peek().type == TOKEN_PLUS || peek().type == TOKEN_MINUS) {
        Token op = consume();
        ASTNode *right = parse_term();
        ASTNode *node = create_node(NODE_BINOP);
        node->data.op = op.type;
        node->left = left;
        node->right = right;
        left = node;
    }
    return left;
}

// Term → Factor Term'
ASTNode *parse_term() {
    ASTNode *left = parse_factor();
    while (peek().type == TOKEN_MUL || peek().type == TOKEN_DIV) {
        Token op = consume();
        ASTNode *right = parse_factor();
        ASTNode *node = create_node(NODE_BINOP);
        node->data.op = op.type;
        node->left = left;
        node->right = right;
        left = node;
    }
    return left;
}

// Factor → ( Expr ) | id | num
ASTNode *parse_factor() {
    if (peek().type == TOKEN_LPAREN) {
        consume();  // '('
        ASTNode *node = parse_expr();
        expect(TOKEN_RPAREN);
        return node;
    } else if (peek().type == TOKEN_ID || peek().type == TOKEN_NUM) {
        Token t = consume();
        ASTNode *node = create_node(NODE_LEAF);
        node->data = t;
        return node;
    } else {
        error("语法错误: 期望 id 或 (");
        return NULL;
    }
}
```

---

## 五、LR 分析

LR 分析从左到右扫描、最右推导的逆过程。

### LR(0) 项目

项目 = 产生式 + 点标记（表示已分析的位置）

```text
表达式: Expr → Expr + Term
项目:
  Expr → · Expr + Term    (尚未识别)
  Expr → Expr · + Term    (已识别 Expr，等待 +)
  Expr → Expr + · Term    (已识别 Expr +，等待 Term)
  Expr → Expr + Term ·    (已完全识别，可规约)
```

### LR(0) 自动机

```
I0: Expr' → · Expr
    Expr  → · Term
    Expr  → · Expr + Term
    Term  → · id
    Term  → · ( Expr )

I1 (goto I0, Expr):
    Expr' → Expr ·
    Expr  → Expr · + Term

I2 (goto I0, Term):
    Expr  → Term ·

I3 (goto I0, id):
    Term  → id ·

I4 (goto I1, +):
    Expr  → Expr + · Term
    Term  → · id
    Term  → · ( Expr )

I5 (goto I4, Term):
    Expr  → Expr + Term ·

I6 (goto I4, id):
    Term  → id ·

I7 (goto I4, ():
    Term  → ( · Expr )
    ...
```

### SLR(1) 分析表

| 状态 | id | + | ( | ) | $ | Expr | Term |
|------|----|----|----|----|----|----|------|
| 0 | s3 | | s7 | | | 1 | 2 |
| 1 | | s4 | | | acc | | |
| 2 | r2 | r2 | | | r2 | | |
| 3 | r3 | r3 | | | r3 | | |
| 4 | s3 | | s7 | | | | 5 |
| 5 | r1 | r1 | | | r1 | | |

`s3` = 移进到状态3, `r1` = 用产生式1规约, `acc` = 接受

### LR 分析器比较

| 类型 | 能力 | 表大小 | 构建难度 | 实用 |
|------|------|--------|----------|------|
| LR(0) | 最小 | 小 | 简单 | 不实用（太多冲突） |
| SLR(1) | 中等 | 小 | 简单 | 可用于简单文法 |
| LR(1) | 最大 | 非常大 | 复杂 | 理论完整，表太大 |
| LALR(1) | 接近 LR(1) | 小（合并状态） | 复杂 | 最实用 |

---

## 六、BNF 与 EBNF

### BNF

```bnf
<expr> ::= <term> { ("+" | "-") <term> }
<term> ::= <factor> { ("*" | "/") <factor> }
<factor> ::= "(" <expr> ")" | <id> | <num>
<id> ::= <letter> { <letter> | <digit> }
<num> ::= <digit> { <digit> }
```

### EBNF

```ebnf
expr   = term, { ("+" | "-"), term } ;
term   = factor, { ("*" | "/"), factor } ;
factor = "(", expr, ")"
       | id
       | num ;
id     = letter, { letter | digit } ;
num    = digit, { digit } ;
```

EBNF 增强符号：

| 符号 | 含义 |
|------|------|
| `[]` | 可选（0或1次） |
| `{}` | 重复（0或多次） |
| `()` | 分组 |
| `\|` | 选择 |
| `,` | 连接 |

---

## 七、YACC/Bison 与 ANTLR

### YACC 文件结构

```yacc
%{
/* C 代码头 */
#include <stdio.h>
extern int yylex();
void yyerror(const char *s) { fprintf(stderr, "错误: %s\n", s); }
%}

%token NUMBER ID IF ELSE WHILE
%left '+' '-'
%left '*' '/'

%%
program: stmt_list
       ;

stmt_list: stmt
         | stmt_list stmt
         ;

stmt: expr ';'
    | IF '(' expr ')' stmt
    | IF '(' expr ')' stmt ELSE stmt
    | WHILE '(' expr ')' stmt
    ;

expr: expr '+' term   { $$ = $1 + $3; }
    | expr '-' term   { $$ = $1 - $3; }
    | term
    ;

term: term '*' factor { $$ = $1 * $3; }
    | term '/' factor { $$ = $1 / $3; }
    | factor
    ;

factor: NUMBER        { $$ = $1; }
      | ID
      | '(' expr ')'  { $$ = $2; }
      ;
%%

int main() { yyparse(); return 0; }
```

### ANTLR 示例

```antlr
grammar SimpleCalc;

@header {
package com.example;
}

program: expr EOF ;

expr: expr ('*'|'/') expr   # MulDiv
    | expr ('+'|'-') expr   # AddSub
    | INT                   # Int
    | '(' expr ')'          # Paren
    ;

INT: [0-9]+ ;
WS: [ \t\r\n]+ -> skip ;
```

```java
// ANTLR 生成的 Listener
public class CalcListener extends SimpleCalcBaseListener {
    @Override
    public void exitAddSub(SimpleCalcParser.AddSubContext ctx) {
        int left = values.get(ctx.expr(0));
        int right = values.get(ctx.expr(1));
        values.put(ctx, ctx.op.getText().equals("+") ? left + right : left - right);
    }
}
```

