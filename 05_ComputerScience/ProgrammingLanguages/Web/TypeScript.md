---
aliases: [TypeScript]
tags: ['ProgrammingLanguages', 'Web', 'TypeScript']
---

# TypeScript 快速指南

## 一、类型系统

```typescript
// 基本类型
const name: string = "张三";
const age: number = 28;
const isActive: boolean = true;
const data: null = null;
const notDefined: undefined = undefined;
const big: bigint = 9007199254740991n;
const sym: symbol = Symbol("key");

// 数组
const arr1: number[] = [1, 2, 3];
const arr2: Array<string> = ["a", "b", "c"];

// 元组 (Tuple)
const tuple: [string, number, boolean] = ["张三", 28, true];
tuple[0].charAt(0);  // 类型安全
// tuple[3] = "extra";  // 错误! 索引越界

// 枚举 (Enum)
enum Direction {
    Up = "UP",
    Down = "DOWN",
    Left = "LEFT",
    Right = "RIGHT"
}
console.log(Direction.Up);  // "UP"

enum StatusCode {
    Success = 200,
    NotFound = 404,
    Error = 500
}

// any - 避开类型检查 (尽量避免)
let anything: any = 42;
anything = "string";
anything = true;

// unknown - 类型安全的 any
let unknown: unknown = 42;
unknown = "hello";
// unknown.toUpperCase();  // 错误! 需要类型收窄
if (typeof unknown === "string") {
    unknown.toUpperCase();  // 正确
}

// never - 永远不会发生的类型
function throwError(message: string): never {
    throw new Error(message);
}

function infiniteLoop(): never {
    while (true) {}
}

// void - 没有返回值
function log(message: string): void {
    console.log(message);
}
```

## 二、接口 (Interface)

```typescript
interface User {
    readonly id: number;       // 只读
    name: string;
    age?: number;              // 可选
    email: string;
    readonly createdAt: Date;  // 只读
}

const user: User = {
    id: 1,
    name: "张三",
    email: "zhangsan@example.com",
    createdAt: new Date()
};
// user.id = 2;  // 错误! 只读属性

// 方法定义
interface Animal {
    name: string;
    speak(): string;
    move?(distance: number): void;  // 可选方法
}

// 索引签名
interface StringDictionary {
    [key: string]: string;
}
const dict: StringDictionary = {
    hello: "你好",
    world: "世界"
};

// 继承
interface Person {
    name: string;
    age: number;
}

interface Employee extends Person {
    employeeId: string;
    department: string;
}

const emp: Employee = {
    name: "李四",
    age: 30,
    employeeId: "E001",
    department: "技术部"
};

// 函数类型接口
interface CompareFunction {
    (a: number, b: number): number;
}
const sortAsc: CompareFunction = (a, b) => a - b;
```

## 三、类型别名 (Type Alias)

```typescript
// 基本别名
type ID = string | number;
type Point = {
    x: number;
    y: number;
};
type Callback = (result: string) => void;

// 联合类型 (Union)
type Status = "pending" | "processing" | "completed" | "failed";
type Result = SuccessResult | ErrorResult;

interface SuccessResult {
    ok: true;
    data: string;
}
interface ErrorResult {
    ok: false;
    error: string;
}

function handleResult(result: Result) {
    if (result.ok) {
        console.log(result.data);
    } else {
        console.error(result.error);
    }
}

// 交叉类型 (Intersection)
type Named = { name: string };
type Aged = { age: number };
type Person = Named & Aged;  // { name: string; age: number; }

// 字面量类型
const pi: 3.14159 = 3.14159;
type DiceValue = 1 | 2 | 3 | 4 | 5 | 6;
```

## 四、泛型 (Generics)

```typescript
// 泛型函数
function identity<T>(arg: T): T {
    return arg;
}
const num = identity<number>(42);
const str = identity("hello");  // 类型推断

// 泛型约束
interface HasLength {
    length: number;
}
function logLength<T extends HasLength>(arg: T): T {
    console.log(arg.length);
    return arg;
}
logLength("hello");     // 5
logLength([1, 2, 3]);   // 3
// logLength(123);       // 错误!

// 泛型接口
interface Repository<T> {
    getById(id: string): T | undefined;
    getAll(): T[];
    create(item: T): T;
    update(id: string, item: Partial<T>): T;
    delete(id: string): boolean;
}

class UserRepository implements Repository<User> {
    private users: User[] = [];
    
    getById(id: string): User | undefined {
        return this.users.find(u => u.id.toString() === id);
    }
    getAll(): User[] { return this.users; }
    create(item: User): User {
        this.users.push(item);
        return item;
    }
    update(id: string, item: Partial<User>): User {
        const user = this.getById(id);
        if (!user) throw new Error("User not found");
        Object.assign(user, item);
        return user;
    }
    delete(id: string): boolean {
        const index = this.users.findIndex(u => u.id.toString() === id);
        if (index === -1) return false;
        this.users.splice(index, 1);
        return true;
    }
}

// 泛型类
class Stack<T> {
    private items: T[] = [];
    
    push(item: T): void {
        this.items.push(item);
    }
    pop(): T | undefined {
        return this.items.pop();
    }
    peek(): T | undefined {
        return this.items[this.items.length - 1];
    }
    get size(): number {
        return this.items.length;
    }
}
```

## 五、工具类型 (Utility Types)

```typescript
interface Todo {
    title: string;
    description: string;
    completed: boolean;
    createdAt: Date;
}

// Partial - 所有属性可选
function updateTodo(todo: Todo, fieldsToUpdate: Partial<Todo>): Todo {
    return { ...todo, ...fieldsToUpdate };
}

// Required - 所有属性必选
type RequiredTodo = Required<Partial<Todo>>;

// Readonly - 所有属性只读
type ReadonlyTodo = Readonly<Todo>;

// Pick - 选取属性
type TodoPreview = Pick<Todo, "title" | "completed">;

// Omit - 排除属性
type TodoWithoutTime = Omit<Todo, "createdAt">;

// Record - 构造对象类型
type PageInfo = {
    title: string;
    url: string;
};
type Pages = Record<"home" | "about" | "contact", PageInfo>;

// Exclude - 排除联合类型中的某些类型
type T0 = Exclude<"a" | "b" | "c", "a">;  // "b" | "c"

// Extract - 提取联合类型中的某些类型
type T1 = Extract<"a" | "b" | "c", "a" | "f">;  // "a"

// NonNullable - 排除 null 和 undefined
type T2 = NonNullable<string | number | null | undefined>;  // string | number

// ReturnType - 获取函数返回类型
type Fn = () => { a: number; b: string };
type FnReturnType = ReturnType<Fn>;  // { a: number; b: string }

// Parameters - 获取函数参数类型
type FnParams = Parameters<(a: number, b: string) => void>;  // [number, string]

// Awaited - 获取 Promise 解析类型
type AsyncResult = Awaited<Promise<string>>;  // string
```

## 六、装饰器

```typescript
// 类装饰器
function Logger<T extends { new(...args: any[]): {} }>(constructor: T) {
    return class extends constructor {
        constructor(...args: any[]) {
            console.log(`创建实例: ${constructor.name}`);
            super(...args);
        }
    };
}

@Logger
class Person {
    constructor(public name: string) {}
}

// 方法装饰器
function Log(target: any, propertyKey: string, descriptor: PropertyDescriptor) {
    const originalMethod = descriptor.value;
    descriptor.value = function(...args: any[]) {
        console.log(`调用方法: ${propertyKey}`, args);
        return originalMethod.apply(this, args);
    };
    return descriptor;
}

class Calculator {
    @Log
    add(a: number, b: number): number {
        return a + b;
    }
}

// 属性装饰器
function DefaultValue(value: string) {
    return (target: any, propertyKey: string) => {
        target[propertyKey] = value;
    };
}

class User {
    @DefaultValue("匿名")
    name: string;
}

// 装饰器工厂
function Enumerable(enumerable: boolean) {
    return (target: any, propertyKey: string, descriptor: PropertyDescriptor) => {
        descriptor.enumerable = enumerable;
    };
}

class MyClass {
    @Enumerable(false)
    secretMethod() {}
}
```

## 七、tsconfig.json

```json
{
    "compilerOptions": {
        "target": "ES2020",
        "module": "ESNext",
        "lib": ["ES2020", "DOM", "DOM.Iterable"],
        "outDir": "./dist",
        "rootDir": "./src",
        "strict": true,
        "esModuleInterop": true,
        "skipLibCheck": true,
        "forceConsistentCasingInFileNames": true,
        "resolveJsonModule": true,
        "declaration": true,
        "declarationMap": true,
        "sourceMap": true,
        "moduleResolution": "bundler",
        "allowImportingTsExtensions": true,
        "noEmit": true,
        "jsx": "react-jsx",
        
        "noUnusedLocals": true,
        "noUnusedParameters": true,
        "noImplicitReturns": true,
        "noFallthroughCasesInSwitch": true
    },
    "include": ["src"],
    "exclude": ["node_modules", "dist", "**/*.test.ts"]
}
```

## 八、React with TypeScript

```typescript
import React, { useState, useEffect, useCallback, useMemo, FC } from 'react';

// Props 类型
interface ButtonProps {
    label: string;
    variant?: 'primary' | 'secondary' | 'danger';
    size?: 'small' | 'medium' | 'large';
    disabled?: boolean;
    onClick: (event: React.MouseEvent<HTMLButtonElement>) => void;
    children?: React.ReactNode;
}

// 函数组件
const Button: FC<ButtonProps> = ({
    label,
    variant = 'primary',
    size = 'medium',
    disabled = false,
    onClick,
    children
}) => {
    return (
        <button
            className={`btn btn-${variant} btn-${size}`}
            disabled={disabled}
            onClick={onClick}
        >
            {label}{children}
        </button>
    );
};

// 带状态和事件的组件
interface UserListProps {
    initialUsers?: User[];
}

const UserList: FC<UserListProps> = ({ initialUsers = [] }) => {
    const [users, setUsers] = useState<User[]>(initialUsers);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        const loadUsers = async () => {
            setLoading(true);
            try {
                const response = await fetch('/api/users');
                const data: User[] = await response.json();
                setUsers(data);
            } catch (err) {
                setError(err instanceof Error ? err.message : '加载失败');
            } finally {
                setLoading(false);
            }
        };
        loadUsers();
    }, []);

    const addUser = useCallback((user: User) => {
        setUsers(prev => [...prev, user]);
    }, []);

    const totalAge = useMemo(() => {
        return users.reduce((sum, u) => sum + u.age, 0);
    }, [users]);

    if (loading) return <div>加载中...</div>;
    if (error) return <div>错误: {error}</div>;

    return (
        <div>
            <h2>用户列表 (共{users.length}人, 总年龄{totalAge})</h2>
            <ul>
                {users.map(user => (
                    <li key={user.id}>{user.name} - {user.age}岁</li>
                ))}
            </ul>
        </div>
    );
};

// useRef
const InputWithFocus: FC = () => {
    const inputRef = useRef<HTMLInputElement>(null);
    
    useEffect(() => {
        inputRef.current?.focus();
    }, []);
    
    return <input ref={inputRef} type="text" />;
};

// useContext
interface ThemeContext {
    primary: string;
    background: string;
    text: string;
}
const ThemeContext = React.createContext<ThemeContext>({
    primary: '#3498db',
    background: '#fff',
    text: '#333'
});

// useReducer
type Action = 
    | { type: 'increment' }
    | { type: 'decrement' }
    | { type: 'reset'; payload: number };

const counterReducer = (state: number, action: Action): number => {
    switch (action.type) {
        case 'increment': return state + 1;
        case 'decrement': return state - 1;
        case 'reset': return action.payload;
        default: return state;
    }
};

const Counter: FC = () => {
    const [count, dispatch] = useReducer(counterReducer, 0);
    return (
        <div>
            <p>{count}</p>
            <button onClick={() => dispatch({ type: 'increment' })}>+</button>
            <button onClick={() => dispatch({ type: 'decrement' })}>-</button>
            <button onClick={() => dispatch({ type: 'reset', payload: 0 })}>重置</button>
        </div>
    );
};
```

> TypeScript 为 JavaScript 添加了类型安全, 显著提升大型项目的可维护性。重点掌握: 接口与类型别名、泛型、工具类型, 以及 React 与 TypeScript 的结合使用。
