---
aliases: [Semantic]
tags: ['CompilerPrinciples', 'Semantic']
created: 2026-05-16
updated: 2026-05-16
---

# 语义分析

## 一、概述

语义分析是编译器的第三阶段，检查语法树是否符合语言的语义规则，进行类型检查、作用域分析、控制流检查等，并为代码生成提供信息。

### 语义分析的任务

1. **类型检查**：验证运算操作数的类型兼容性
2. **作用域解析**：将变量名绑定到其声明
3. **类型推断**：推导表达式类型
4. **类型转换**：插入隐式类型转换
5. **控制流检查**：return 语句、break/continue 合法性
6. **唯一性检查**：标识符不重复声明
7. **一致性检查**：函数参数数量是否匹配

---

## 二、属性文法

属性文法在上下文无关文法的基础上为每个文法符号关联属性，并用语义规则描述属性如何计算。

### 综合属性

综合属性（Synthesized Attribute）从子节点向父节点传递：

```
Productions:    Expr → Expr + Term
Semantic Rule:  Expr.val = Expr1.val + Term.val

语法树：
     Expr.val = 15
    /    \
 Expr.val=7  Term.val=8
   │            │
   id(a).val=7  num(8).val=8

属性从叶子节点向根节点计算。
```

### 继承属性

继承属性（Inherited Attribute）从父节点或兄弟节点向子节点传递：

```
Productions:    Decl → Type id
Semantic Rule:  id.type = Type.type

语法树：
     Decl
    /    \
 Type.type=int  id.type=int

属性从上到下或从左到右传递。
```

---

## 三、S-属性与 L-属性定义

### S-属性定义

只使用综合属性，适合自底向上分析（LR）。

```text
Productions          Semantic Rules
─────────────────────────────────────────
Expr → Expr + Term   Expr.val = Expr1.val + Term.val
Expr → Term          Expr.val = Term.val
Term → Term * Factor Term.val = Term1.val * Factor.val
Term → Factor        Term.val = Factor.val
Factor → ( Expr )    Factor.val = Expr.val
Factor → num         Factor.val = num.lexval
```

### L-属性定义

继承属性只依赖于左侧或上方节点的属性，可自顶向下或深度优先计算。

```text
Productions                      Semantic Rules
────────────────────────────────────────────────────
Decl → Type VarList              VarList.in_type = Type.type
VarList → id VarList1            id.type = VarList.in_type
                                 VarList1.in_type = VarList.in_type
VarList → id                     id.type = VarList.in_type
```

---

## 四、类型检查

### 类型系统分类

| 分类 | 说明 | 语言示例 |
|------|------|----------|
| 静态类型 | 编译时检查 | Java, C++, Go, Rust |
| 动态类型 | 运行时检查 | Python, JavaScript, Ruby |
| 强类型 | 不允许隐式类型混用 | Python, Java, Rust |
| 弱类型 | 允许隐式类型转换 | C, JavaScript |
| 显式类型 | 必须声明类型 | Java, C, Go |
| 类型推断 | 自动推断类型 | Rust, Kotlin, TypeScript |

### 类型等价

**结构等价**（Structural Equivalence）：两个类型有相同的结构

```java
// Java 使用名称等价
class Point { int x; int y; }
class Color { int r; int g; int b; }
// Point 和 Color 不等价，即使它们有相同字段

// C 使用结构等价
struct point { int x; int y; };
struct point p1, p2;   // 相同类型
```

**名称等价**（Name Equivalence）：只有类型名相同才等价

### 类型检查规则

```text
──────────────────────────────────
规则 1: 常量/字面量的类型
intConst.type = int
floatConst.type = float
stringConst.type = string

──────────────────────────────────
规则 2: 标识符类型（查符号表）
lookup(id.name) → 类型

──────────────────────────────────
规则 3: 算术运算
Expr1.type in {int, float}  AND  Expr2.type in {int, float}
────────────────────────────────────────────
Expr1 op Expr2.type = promote(Expr1.type, Expr2.type)

──────────────────────────────────
规则 4: 关系运算
Expr1.type == Expr2.type
────────────────────────────────
Expr1 relop Expr2.type = bool

──────────────────────────────────
规则 5: 赋值
Expr.type == LHS.type
────────────────
LHS = Expr → 合法

──────────────────────────────────
规则 6: 条件表达式
Expr.type == bool
────────────────
if (Expr) Stmt → 合法
```

### 类型转换

```c
// 隐式类型转换（类型提升）
int i = 10;
float f = 3.14;
double d = i + f;    // int → float → double（隐式提升）

// 显式类型转换（强制转换）
int i = (int)3.14;   // double → int，截断

// C 的整型提升规则
// char → short → int → unsigned int → long → unsigned long
```

### 类型检查实现

```c
typedef enum {
    TYPE_INT, TYPE_FLOAT, TYPE_BOOL, TYPE_CHAR,
    TYPE_ARRAY, TYPE_FUNCTION, TYPE_ERROR
} TypeKind;

typedef struct Type {
    TypeKind kind;
    union {
        struct { struct Type *element_type; int size; } array;
        struct { struct Type *return_type; struct Type **params; int param_count; } function;
    };
} Type;

// 检查赋值类型
bool check_assignment(Type *target, Type *source) {
    if (target->kind == TYPE_ERROR || source->kind == TYPE_ERROR)
        return true;  // 错误恢复

    if (target->kind == source->kind)
        return true;

    if (target->kind == TYPE_FLOAT && source->kind == TYPE_INT)
        return true;  // 允许 int → float

    if (target->kind == TYPE_INT && source->kind == TYPE_FLOAT) {
        printf("警告：float → int 可能丢失精度\n");
        return true;
    }

    return false;  // 类型不匹配
}

// 检查函数调用
bool check_function_call(Type *func_type, Type **arg_types, int argc) {
    if (func_type->kind != TYPE_FUNCTION) {
        printf("错误：调用非函数类型\n");
        return false;
    }
    if (func_type->function.param_count != argc) {
        printf("错误：参数数量不匹配，期望 %d 个，实际 %d 个\n",
               func_type->function.param_count, argc);
        return false;
    }
    for (int i = 0; i < argc; i++) {
        if (!check_assignment(func_type->function.params[i], arg_types[i]))
            return false;
    }
    return true;
}
```

---

## 五、符号表与作用域

### 嵌套作用域

```c
int x = 10;          // 全局作用域

void f() {
    int x = 20;      // 函数作用域，遮蔽全局 x
    if (1) {
        int x = 30;  // 块作用域，遮蔽上面的 x
        printf("%d", x);  // 30
    }
    printf("%d", x);  // 20
}
```

### 作用域栈实现

```c
typedef struct Scope {
    SymbolTable *table;
    struct Scope *parent;
    int level;
} Scope;

Scope *current_scope;
int scope_level = 0;

// 进入新作用域
void enter_scope() {
    Scope *new_scope = malloc(sizeof(Scope));
    new_scope->table = create_symbol_table();
    new_scope->parent = current_scope;
    new_scope->level = ++scope_level;
    current_scope = new_scope;
}

// 离开作用域
void leave_scope() {
    Scope *old = current_scope;
    current_scope = current_scope->parent;
    free_symbol_table(old->table);
    free(old);
    scope_level--;
}

// 声明符号（当前作用域）
void declare(const char *name, Type *type) {
    if (lookup_in_current_scope(name)) {
        printf("错误：变量 '%s' 在当前作用域已声明\n", name);
        return;
    }
    Symbol *sym = create_symbol(name, type);
    sym->scope_level = scope_level;
    insert_symbol(current_scope->table, name, sym);
}

// 查找符号（逐层向上）
Symbol *lookup(const char *name) {
    for (Scope *s = current_scope; s != NULL; s = s->parent) {
        Symbol *sym = find_symbol(s->table, name);
        if (sym) return sym;
    }
    printf("错误：未声明的标识符 '%s'\n", name);
    return NULL;
}
```

---

## 六、语义动作

在语法分析过程中执行语义动作。

### YACC 中的语义动作

```yacc
%union {
    int intval;
    float floatval;
    char *strval;
    struct ASTNode *node;
}

%token <intval> INT_CONST
%token <floatval> FLOAT_CONST
%token IF ELSE WHILE RETURN

%type <node> expr stmt program

%%

program: stmt_list { generate_code($1); }
       ;

stmt: IF '(' expr ')' stmt {
        $$ = create_if_node($3, $5, NULL);
        check_type($3, TYPE_BOOL);  // 语义检查
    }
    | IF '(' expr ')' stmt ELSE stmt {
        $$ = create_if_node($3, $5, $7);
        check_type($3, TYPE_BOOL);
    }
    | WHILE '(' expr ')' stmt {
        $$ = create_while_node($3, $5);
        check_type($3, TYPE_BOOL);
    }
    | RETURN expr ';' {
        $$ = create_return_node($2);
        check_return_type($2, current_function_return_type);
    }
    ;

expr: expr '+' term {
        check_arith_type($1, $3);
        $$ = create_binop_node('+', $1, $3);
        $$->type = promote_type($1->type, $3->type);
    }
    | expr EQ term {
        check_compatible_type($1, $3);
        $$ = create_binop_node('=', $1, $3);
        $$->type = TYPE_BOOL;
    }
    | term
    ;

term: term '*' factor {
        check_arith_type($1, $3);
        $$ = create_binop_node('*', $1, $3);
        $$->type = promote_type($1->type, $3->type);
    }
    | factor
    ;

factor: INT_CONST  { $$ = create_const_node($1); $$->type = TYPE_INT; }
      | FLOAT_CONST { $$ = create_const_node($1); $$->type = TYPE_FLOAT; }
      | IDENTIFIER { $$ = create_id_node($1); $$->type = lookup_type($1); }
      | '(' expr ')' { $$ = $2; }
      ;
```

### 典型语义错误

```c
// 1. 类型不匹配
int a = "hello";         // 错误：不能将字符串赋给 int

// 2. 运算符不能用于该类型
struct S { int x; } s1, s2;
s1 + s2;                 // 错误：结构体不支持加法

// 3. 函数参数不匹配
void f(int x);
f("hello");              // 错误：参数类型不匹配

// 4. 未声明的变量
x = 10;                  // 错误：x 未声明

// 5. 重复声明
int x;
float x;                 // 错误：x 重复声明

// 6. break/continue 在循环外
if (1) {
    break;               // 错误：break 不在循环或 switch 中
}

// 7. return 类型不匹配
int f() { return "hello"; }  // 错误：返回类型不匹配

// 8. void 表达式
int a = void_func();     // 错误：void 函数不能有返回值
```

