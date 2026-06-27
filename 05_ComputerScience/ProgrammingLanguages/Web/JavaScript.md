---
aliases: [JavaScript]
tags: ['ProgrammingLanguages', 'Web', 'JavaScript']
created: 2026-05-16
updated: 2026-05-16
---

# JavaScript 完整指南

## 一、数据类型与类型转换

```javascript
// 基本类型
let num = 42;                  // Number
let str = "Hello";             // String
let bool = true;               // Boolean
let undef = undefined;         // Undefined
let nul = null;                // Null
let sym = Symbol("id");        // Symbol (ES6)
let big = 9007199254740991n;   // BigInt (ES2020)

// 引用类型
let obj = { name: "张三" };    // Object
let arr = [1, 2, 3];           // Array
let func = function() {};      // Function

// typeof 检查
typeof 42          // 'number'
typeof "hello"     // 'string'
typeof true        // 'boolean'
typeof undefined   // 'undefined'
typeof null        // 'object' (历史遗留 bug!)
typeof Symbol()    // 'symbol'
typeof function(){} // 'function'
typeof []          // 'object'

// 类型转换
String(123)        // '123'
Number("456")      // 456
Boolean(0)         // false
Boolean("")        // false
Boolean("non")     // true
parseInt("12.5")   // 12
parseFloat("3.14") // 3.14

// 隐式转换 (注意!)
"5" - 2      // 3
"5" + 2      // '52'
!"hello"     // false
!!"hello"    // true
```

## 二、对象

```javascript
// 创建对象
const person = {
    name: "张三",
    age: 28,
    "full-name": "张三丰",  // 带特殊字符的键
    greet() {              // 方法简写
        return `你好, 我是${this.name}`;
    }
};

// 访问属性
person.name           // '张三'
person["full-name"]   // '张三丰'
person.greet()        // '你好, 我是张三'

// 添加/修改/删除
person.city = "北京";
delete person.age;

// 属性检测
"name" in person           // true
person.hasOwnProperty("name")  // true

// 遍历
Object.keys(person)    // ['name', 'full-name', 'city', 'greet']
Object.values(person)  // ['张三', '张三丰', '北京', function]
Object.entries(person) // [['name','张三'], ...]

for (let key in person) {
    console.log(key, person[key]);
}

Object.assign(target, source);  // 合并对象
const clone = { ...person };    // 浅拷贝 (ES6)
```

## 三、数组

```javascript
const arr = [1, 2, 3, 4, 5];

// 添加/删除
arr.push(6)        // 末尾添加 -> [1,2,3,4,5,6]
arr.pop()          // 末尾移除 -> 返回6
arr.unshift(0)     // 开头添加 -> [0,1,2,3,4,5]
arr.shift()        // 开头移除 -> 返回0

// 拼接
arr.slice(1, 3)    // [2, 3] (不修改原数组)
arr.splice(1, 2, "a", "b")  // 删除+插入 -> 修改原数组

// 遍历
arr.forEach((item, index) => console.log(item, index));

// 转换
const doubled = arr.map(x => x * 2);       // [2,4,6,8,10]
const evens = arr.filter(x => x % 2 === 0); // [2,4]
const sum = arr.reduce((acc, cur) => acc + cur, 0);  // 15
const first = arr.find(x => x > 3);        // 4
const index = arr.findIndex(x => x > 3);   // 3
const allPositive = arr.every(x => x > 0); // true
const hasEven = arr.some(x => x % 2 === 0);// true

// 排序
arr.sort();                    // 字典序排序!
arr.sort((a, b) => a - b);     // 数字升序
arr.sort((a, b) => b - a);     // 数字降序

// 其他
arr.includes(3)    // true
arr.indexOf(3)     // 2
arr.join("-")      // '1-2-3-4-5'
arr.flat()         // 展平嵌套数组
arr.flatMap(x => [x, x*2])  // 映射后展平
```

## 四、函数

```javascript
// 函数声明 (hoisting)
function add(a, b) {
    return a + b;
}

// 函数表达式 (不 hoisting)
const subtract = function(a, b) {
    return a - b;
};

// 箭头函数 (ES6)
const multiply = (a, b) => a * b;
const square = x => x ** 2;
const empty = () => {};
const retObj = () => ({ key: "value" });  // 返回对象需要括号

// this 指向
const obj = {
    name: "obj",
    normal: function() {
        console.log(this.name);  // 'obj'
    },
    arrow: () => {
        console.log(this.name);  // undefined (继承外部 this)
    }
};

// 闭包
function createCounter() {
    let count = 0;
    return {
        increment: () => ++count,
        decrement: () => --count,
        getCount: () => count
    };
}
const counter = createCounter();
counter.increment();  // 1
counter.increment();  // 2
counter.decrement();  // 1

// IIFE (立即执行函数)
(function() {
    console.log("立即执行");
})();

(() => {
    console.log("箭头 IIFE");
})();

// 默认参数
function greet(name = "匿名", greeting = "你好") {
    return `${greeting}, ${name}`;
}

// 剩余参数
function sum(...numbers) {
    return numbers.reduce((acc, cur) => acc + cur, 0);
}
```

## 五、ES6+ 特性

```javascript
// 解构
const person = { name: "张三", age: 28, city: "北京" };
const { name, age, city = "默认值" } = person;
const { name: userName, ...rest } = person;

const arr = [1, 2, 3, 4];
const [first, second, ...others] = arr;
const [a, , c] = arr;  // 跳过一个元素: a=1, c=3

// 交换变量
[a, b] = [b, a];

// Spread 展开
const arr1 = [1, 2, 3];
const arr2 = [4, 5, 6];
const merged = [...arr1, ...arr2];  // [1,2,3,4,5,6]

const obj1 = { a: 1, b: 2 };
const obj2 = { b: 3, c: 4 };
const mergedObj = { ...obj1, ...obj2 };  // {a:1, b:3, c:4}

// 模板字面量
const name = "张三";
const html = `
    <div>
        <h1>你好, ${name}</h1>
        <p>${1 + 2}月</p>
    </div>
`;

// let/const
let x = 1;      // 块级作用域, 可修改
const y = 2;    // 块级作用域, 不可修改

// 模块
// math.js
export const PI = 3.14159;
export function add(a, b) { return a + b; }
export default class Calculator { /* ... */ }

// main.js
import calc, { PI, add as sum } from './math.js';
import * as math from './math.js';
```

## 六、DOM 操作

```javascript
// 选择元素
document.getElementById("app");
document.querySelector(".container");        // 第一个匹配
document.querySelectorAll(".item");          // 所有匹配 (NodeList)
document.getElementsByClassName("btn");      // HTMLCollection (动态)

// 创建元素
const div = document.createElement("div");
div.textContent = "Hello";
div.innerHTML = "<strong>加粗</strong>";
div.className = "box active";
div.id = "myDiv";
div.setAttribute("data-id", "123");
div.dataset.id = "123";  // 等价

// 插入
document.body.appendChild(div);
parent.insertBefore(div, referenceNode);
parent.append(div);        // 可插入多个节点和字符串
parent.prepend(div);
div.insertAdjacentHTML("beforebegin", "<p>前面</p>");
// afterbegin | afterend | beforebegin | beforeend

// 删除
div.remove();
parent.removeChild(child);

// 事件
element.addEventListener("click", (event) => {
    console.log(event.target);
    console.log(event.type);
    console.log(event.clientX, event.clientY);
}, { capture: false, once: false, passive: true });

// 事件委托
document.querySelector("#list").addEventListener("click", (e) => {
    if (e.target.matches("li")) {
        console.log("点击了列表项:", e.target.textContent);
    }
});

// 常用事件
// click, dblclick, mouseenter, mouseleave, mouseover, mouseout
// keydown, keyup, keypress
// submit, change, input, focus, blur
// scroll, resize, load, DOMContentLoaded
// touchstart, touchmove, touchend

// 样式操作
element.style.color = "red";
element.style.cssText = "color: red; font-size: 16px;";
element.classList.add("active");
element.classList.remove("hidden");
element.classList.toggle("visible");
element.classList.contains("active");

// 尺寸与位置
element.getBoundingClientRect();   // {top, left, bottom, right, width, height}
element.offsetWidth;               // 包括 padding 和 border
element.clientWidth;               // 包括 padding, 不包括 border
element.scrollHeight;              // 内容总高度
window.innerWidth;                 // 视口宽度
window.pageYOffset;                // 滚动位置
```

## 七、异步 JavaScript

```javascript
// 1. Callback (回调)
function fetchData(callback) {
    setTimeout(() => {
        callback({ id: 1, name: "数据" });
    }, 1000);
}
fetchData(data => console.log(data));

// 回调地狱
fs.readFile("a.txt", (err, data) => {
    fs.readFile("b.txt", (err, data2) => {
        fs.readFile("c.txt", (err, data3) => {
            // 嵌套地狱
        });
    });
});

// 2. Promise (ES6)
const promise = new Promise((resolve, reject) => {
    setTimeout(() => {
        const success = true;
        if (success) {
            resolve("操作成功");
        } else {
            reject(new Error("操作失败"));
        }
    }, 1000);
});

promise
    .then(result => console.log(result))
    .catch(error => console.error(error))
    .finally(() => console.log("完成"));

// Promise 链
fetchUser()
    .then(user => fetchPosts(user.id))
    .then(posts => fetchComments(posts[0].id))
    .then(comments => console.log(comments))
    .catch(err => console.error(err));

// Promise 静态方法
Promise.all([p1, p2, p3])           // 全部成功才成功
    .then(([r1, r2, r3]) => {});
Promise.allSettled([p1, p2, p3])    // 等待所有完成 (不论成功失败)
Promise.race([p1, p2, p3])          // 第一个完成
Promise.any([p1, p2, p3])          // 第一个成功

// 3. async/await (ES2017)
async function getData() {
    try {
        const user = await fetchUser();
        const posts = await fetchPosts(user.id);
        return posts;
    } catch (error) {
        console.error("获取数据失败:", error);
        throw error;
    }
}

// 并发请求
async function getAll() {
    const [users, posts, comments] = await Promise.all([
        fetchUsers(),
        fetchPosts(),
        fetchComments()
    ]);
    return { users, posts, comments };
}

// 4. Fetch API
async function fetchExample() {
    // GET
    const response = await fetch("https://api.example.com/users");
    if (!response.ok) {
        throw new Error(`HTTP Error: ${response.status}`);
    }
    const data = await response.json();

    // POST
    const postResponse = await fetch("https://api.example.com/users", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "Authorization": "Bearer token"
        },
        body: JSON.stringify({ name: "张三", age: 28 })
    });
    const result = await postResponse.json();

    // 文件上传
    const formData = new FormData();
    formData.append("file", fileInput.files[0]);
    const uploadResponse = await fetch("/upload", {
        method: "POST",
        body: formData
    });
}
```

## 八、错误处理

```javascript
// try/catch/finally
try {
    const result = riskyOperation();
    console.log(result);
} catch (error) {
    if (error instanceof TypeError) {
        console.error("类型错误:", error.message);
    } else if (error instanceof RangeError) {
        console.error("范围错误:", error.message);
    } else {
        console.error("其他错误:", error);
    }
} finally {
    console.log("总是执行");
}

// throw
function divide(a, b) {
    if (b === 0) {
        throw new Error("除数不能为0");
    }
    if (typeof a !== "number" || typeof b !== "number") {
        throw new TypeError("参数必须是数字");
    }
    return a / b;
}

// 自定义错误
class ValidationError extends Error {
    constructor(message, field) {
        super(message);
        this.name = "ValidationError";
        this.field = field;
    }
}
```

## 九、原型与类

```javascript
// 原型链
function Person(name, age) {
    this.name = name;
    this.age = age;
}
Person.prototype.greet = function() {
    return `你好, 我是${this.name}`;
};
Person.prototype.species = "人类";

const p = new Person("张三", 28);
console.log(p.greet());
console.log(p.__proto__ === Person.prototype);  // true

// 类 (ES6 语法糖)
class Animal {
    constructor(name) {
        this.name = name;
    }
    
    speak() {
        throw new Error("子类必须实现");
    }
    
    static create(name) {
        return new Animal(name);
    }
}

class Dog extends Animal {
    constructor(name, breed) {
        super(name);  // 调用父类构造
        this.breed = breed;
    }
    
    speak() {
        return `${this.name}: 汪汪!`;
    }
    
    static fromJSON(json) {
        const { name, breed } = JSON.parse(json);
        return new Dog(name, breed);
    }
}

const dog = new Dog("旺财", "金毛");
console.log(dog.speak());  // 旺财: 汪汪!
console.log(dog instanceof Dog);    // true
console.log(dog instanceof Animal); // true

// 私有字段 (ES2022)
class BankAccount {
    #balance = 0;  // 私有字段
    
    constructor(initial) {
        this.#balance = initial;
    }
    
    getBalance() {
        return this.#balance;
    }
    
    #validate(amount) {  // 私有方法
        if (amount <= 0) throw new Error("金额必须为正");
    }
    
    deposit(amount) {
        this.#validate(amount);
        this.#balance += amount;
    }
}
```

## 十、常用模式

```javascript
// 1. 模块模式 (Module Pattern)
const Calculator = (function() {
    let lastResult = 0;
    
    function validate(n) {
        return typeof n === "number";
    }
    
    return {
        add(a, b) {
            if (!validate(a) || !validate(b)) throw new Error("Invalid input");
            lastResult = a + b;
            return lastResult;
        },
        getLastResult() {
            return lastResult;
        }
    };
})();

// 2. 观察者模式
class EventEmitter {
    constructor() {
        this.events = {};
    }
    
    on(event, listener) {
        if (!this.events[event]) this.events[event] = [];
        this.events[event].push(listener);
        return () => this.off(event, listener);
    }
    
    off(event, listener) {
        if (!this.events[event]) return;
        this.events[event] = this.events[event].filter(l => l !== listener);
    }
    
    emit(event, ...args) {
        if (!this.events[event]) return;
        this.events[event].forEach(listener => listener(...args));
    }
}

// 3. 防抖 (Debounce)
function debounce(func, delay = 300) {
    let timeoutId;
    return function(...args) {
        clearTimeout(timeoutId);
        timeoutId = setTimeout(() => func.apply(this, args), delay);
    };
}

// 4. 节流 (Throttle)
function throttle(func, limit = 300) {
    let inThrottle = false;
    return function(...args) {
        if (!inThrottle) {
            func.apply(this, args);
            inThrottle = true;
            setTimeout(() => inThrottle = false, limit);
        }
    };
}
```

> JavaScript 是 Web 的核心语言。重点掌握: ES6+ 语法、异步编程 (Promise/async-await)、DOM 操作、原型与类。理解闭包和作用域是进阶的关键。

