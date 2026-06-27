---
aliases: [React]
tags: ['ProgrammingLanguages', 'Web', 'React']
created: 2026-05-16
updated: 2026-05-13
---

# React 快速指南

## 一、JSX

```jsx
import React from 'react';

// JSX 规则
const element = <h1>Hello, World!</h1>;

// 嵌入表达式
const name = "张三";
const greeting = <h1>你好, {name}!</h1>;

// 条件渲染
const isLoggedIn = true;
const status = (
    <div>
        {isLoggedIn ? <span>已登录</span> : <span>未登录</span>}
        {isLoggedIn && <span> - 欢迎回来</span>}
    </div>
);

// 列表渲染
const items = [1, 2, 3, 4, 5];
const list = (
    <ul>
        {items.map((item, index) => (
            <li key={index}>{item}</li>
        ))}
    </ul>
);

// 样式
const style = { color: 'blue', fontSize: '20px' };
const styled = <div style={style}>带样式的文本</div>;

// className
const classDiv = <div className="container">容器</div>;
```

## 二、组件

### 函数组件 (推荐)

```jsx
// 函数组件
function Welcome(props) {
    return <h1>你好, {props.name}</h1>;
}

// 箭头函数组件
const Welcome = ({ name }) => {
    return <h1>你好, {name}</h1>;
};

// 使用
function App() {
    return (
        <div>
            <Welcome name="张三" />
            <Welcome name="李四" />
        </div>
    );
}
```

### 类组件

```jsx
class Welcome extends React.Component {
    render() {
        return <h1>你好, {this.props.name}</h1>;
    }
}
```

## 三、Props

```jsx
// Props 传递
interface UserCardProps {
    name: string;
    age: number;
    isActive?: boolean;  // 可选
    onUpdate?: (id: number) => void;
    children?: React.ReactNode;
}

function UserCard({ name, age, isActive = true, onUpdate, children }: UserCardProps) {
    return (
        <div className={`card ${isActive ? 'active' : ''}`}>
            <h2>{name}</h2>
            <p>年龄: {age}</p>
            {children}
            {onUpdate && <button onClick={() => onUpdate(1)}>更新</button>}
        </div>
    );
}

// Children
function Card({ children }) {
    return <div className="card">{children}</div>;
}

<Card>
    <h2>卡片标题</h2>
    <p>卡片内容</p>
</Card>

// Default props
function Greeting({ name = "访客" }) {
    return <h1>你好, {name}</h1>;
}
```

## 四、State (useState)

```jsx
import React, { useState } from 'react';

function Counter() {
    const [count, setCount] = useState(0);
    const [text, setText] = useState('');

    return (
        <div>
            <p>计数: {count}</p>
            <button onClick={() => setCount(count + 1)}>+1</button>
            <button onClick={() => setCount(prev => prev - 1)}>-1</button>
            <button onClick={() => setCount(0)}>重置</button>
            
            <input value={text} onChange={e => setText(e.target.value)} />
        </div>
    );
}

// 对象状态
function UserForm() {
    const [user, setUser] = useState({ name: '', age: 0, email: '' });
    
    const updateField = (field, value) => {
        setUser(prev => ({ ...prev, [field]: value }));
    };
    
    return (
        <div>
            <input value={user.name} onChange={e => updateField('name', e.target.value)} />
            <input type="number" value={user.age} onChange={e => updateField('age', +e.target.value)} />
            <input value={user.email} onChange={e => updateField('email', e.target.value)} />
        </div>
    );
}

// 数组状态
function TodoList() {
    const [todos, setTodos] = useState([]);
    
    const addTodo = (text) => {
        setTodos(prev => [...prev, { id: Date.now(), text, done: false }]);
    };
    
    const toggleTodo = (id) => {
        setTodos(prev => prev.map(t => 
            t.id === id ? { ...t, done: !t.done } : t
        ));
    };
    
    const removeTodo = (id) => {
        setTodos(prev => prev.filter(t => t.id !== id));
    };
}
```

## 五、Effect (useEffect)

```jsx
import React, { useState, useEffect } from 'react';

function DataFetcher({ userId }) {
    const [data, setData] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        let cancelled = false;
        
        async function fetchData() {
            setLoading(true);
            setError(null);
            try {
                const response = await fetch(`/api/users/${userId}`);
                if (!response.ok) throw new Error('请求失败');
                const result = await response.json();
                if (!cancelled) setData(result);
            } catch (err) {
                if (!cancelled) setError(err.message);
            } finally {
                if (!cancelled) setLoading(false);
            }
        }
        
        fetchData();
        
        return () => {
            cancelled = true;  // 清理: 防止内存泄漏
        };
    }, [userId]);  // 依赖: userId 变化时重新执行

    if (loading) return <div>加载中...</div>;
    if (error) return <div>错误: {error}</div>;
    if (!data) return null;
    
    return <div>{data.name}</div>;
}

// useEffect 的3种模式
useEffect(() => {
    // 1. 不传依赖: 每次渲染后执行
});

useEffect(() => {
    // 2. 空数组: 仅组件挂载时执行一次
}, []);

useEffect(() => {
    // 3. 带依赖: 依赖变化时执行
}, [dep1, dep2]);
```

## 六、Hooks

### useContext

```jsx
const ThemeContext = React.createContext('light');
const UserContext = React.createContext(null);

function App() {
    return (
        <ThemeContext.Provider value="dark">
            <UserContext.Provider value={{ name: '张三', role: 'admin' }}>
                <Toolbar />
            </UserContext.Provider>
        </ThemeContext.Provider>
    );
}

function Toolbar() {
    const theme = useContext(ThemeContext);
    const user = useContext(UserContext);
    
    return (
        <div className={`theme-${theme}`}>
            <p>{user.name} - {user.role}</p>
        </div>
    );
}
```

### useRef

```jsx
function AutoFocusInput() {
    const inputRef = useRef(null);
    
    useEffect(() => {
        inputRef.current?.focus();
    }, []);
    
    return <input ref={inputRef} type="text" />;
}

// 存储可变值 (不触发重渲染)
function Timer() {
    const [count, setCount] = useState(0);
    const intervalRef = useRef(null);
    
    useEffect(() => {
        intervalRef.current = setInterval(() => {
            setCount(c => c + 1);
        }, 1000);
        return () => clearInterval(intervalRef.current);
    }, []);
    
    const stop = () => clearInterval(intervalRef.current);
    
    return (
        <div>
            <p>{count}</p>
            <button onClick={stop}>停止</button>
        </div>
    );
}
```

### useMemo & useCallback

```jsx
function ExpensiveComponent({ list, filter }) {
    // useMemo: 缓存计算结果
    const filteredList = useMemo(() => {
        console.log('过滤列表...');
        return list.filter(item => item.includes(filter));
    }, [list, filter]);
    
    // useCallback: 缓存函数引用
    const handleClick = useCallback((id) => {
        console.log(`点击了: ${id}`);
    }, []);  // 没有依赖, 函数引用永远不变
    
    return (
        <ul>
            {filteredList.map(item => (
                <li key={item} onClick={() => handleClick(item)}>{item}</li>
            ))}
        </ul>
    );
}
```

### useReducer

```jsx
const initialState = { count: 0, step: 1 };

function reducer(state, action) {
    switch (action.type) {
        case 'increment':
            return { ...state, count: state.count + state.step };
        case 'decrement':
            return { ...state, count: state.count - state.step };
        case 'setStep':
            return { ...state, step: action.payload };
        case 'reset':
            return initialState;
        default:
            throw new Error('未知 action 类型');
    }
}

function Counter() {
    const [state, dispatch] = useReducer(reducer, initialState);
    
    return (
        <div>
            <p>计数: {state.count}</p>
            <input type="number" value={state.step} 
                   onChange={e => dispatch({ type: 'setStep', payload: +e.target.value })} />
            <button onClick={() => dispatch({ type: 'increment' })}>+</button>
            <button onClick={() => dispatch({ type: 'decrement' })}>-</button>
            <button onClick={() => dispatch({ type: 'reset' })}>重置</button>
        </div>
    );
}
```

### 自定义 Hook

```jsx
// useFetch
function useFetch(url) {
    const [data, setData] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    
    useEffect(() => {
        let cancelled = false;
        setLoading(true);
        
        fetch(url)
            .then(res => {
                if (!res.ok) throw new Error(`HTTP ${res.status}`);
                return res.json();
            })
            .then(data => { if (!cancelled) setData(data); })
            .catch(err => { if (!cancelled) setError(err.message); })
            .finally(() => { if (!cancelled) setLoading(false); });
        
        return () => { cancelled = true; };
    }, [url]);
    
    return { data, loading, error };
}

// useLocalStorage
function useLocalStorage(key, initialValue) {
    const [value, setValue] = useState(() => {
        try {
            const item = localStorage.getItem(key);
            return item ? JSON.parse(item) : initialValue;
        } catch {
            return initialValue;
        }
    });
    
    useEffect(() => {
        localStorage.setItem(key, JSON.stringify(value));
    }, [key, value]);
    
    return [value, setValue];
}

// useDebounce
function useDebounce(value, delay = 300) {
    const [debouncedValue, setDebouncedValue] = useState(value);
    
    useEffect(() => {
        const timer = setTimeout(() => setDebouncedValue(value), delay);
        return () => clearTimeout(timer);
    }, [value, delay]);
    
    return debouncedValue;
}
```

## 七、事件处理

```jsx
function EventExample() {
    const handleClick = (event) => {
        event.preventDefault();
        console.log('点击', event.clientX, event.clientY);
    };
    
    const handleChange = (event) => {
        console.log('输入:', event.target.value);
    };
    
    const handleSubmit = (event) => {
        event.preventDefault();
        const formData = new FormData(event.target);
        console.log(Object.fromEntries(formData));
    };
    
    const handleKeyDown = (event) => {
        if (event.key === 'Enter') {
            console.log('按下了回车');
        }
    };
    
    return (
        <form onSubmit={handleSubmit}>
            <button onClick={handleClick}>点击</button>
            <input onChange={handleChange} onKeyDown={handleKeyDown} />
            <button type="submit">提交</button>
        </form>
    );
}
```

## 八、React Router

```jsx
// npm install react-router-dom

import { BrowserRouter, Routes, Route, Link, NavLink, 
         useParams, useNavigate, useLocation, Outlet } from 'react-router-dom';

function App() {
    return (
        <BrowserRouter>
            <nav>
                <Link to="/">首页</Link>
                <Link to="/about">关于</Link>
                <NavLink to="/users" className={({isActive}) => isActive ? 'active' : ''}>
                    用户管理
                </NavLink>
            </nav>
            <Routes>
                <Route path="/" element={<Home />} />
                <Route path="/about" element={<About />} />
                <Route path="/users" element={<UsersLayout />}>
                    <Route index element={<UserList />} />
                    <Route path=":id" element={<UserDetail />} />
                    <Route path="new" element={<NewUser />} />
                </Route>
                <Route path="*" element={<NotFound />} />
            </Routes>
        </BrowserRouter>
    );
}

// 路由参数
function UserDetail() {
    const { id } = useParams();
    const navigate = useNavigate();
    const location = useLocation();
    
    return (
        <div>
            <p>用户 ID: {id}</p>
            <p>当前路径: {location.pathname}</p>
            <button onClick={() => navigate('/users')}>返回列表</button>
            <button onClick={() => navigate(-1)}>后退</button>
        </div>
    );
}
```

## 九、状态管理

### Context API

```jsx
// store.js
const AppContext = createContext();

function AppProvider({ children }) {
    const [state, dispatch] = useReducer(appReducer, initialState);
    
    return (
        <AppContext.Provider value={{ state, dispatch }}>
            {children}
        </AppContext.Provider>
    );
}

// 使用
function useAppContext() {
    const context = useContext(AppContext);
    if (!context) throw new Error('必须在 AppProvider 内使用');
    return context;
}
```

### Zustand (推荐)

```jsx
// npm install zustand
import { create } from 'zustand';

const useStore = create((set, get) => ({
    count: 0,
    todos: [],
    
    increment: () => set(state => ({ count: state.count + 1 })),
    decrement: () => set(state => ({ count: state.count - 1 })),
    
    addTodo: (text) => set(state => ({
        todos: [...state.todos, { id: Date.now(), text, done: false }]
    })),
    
    toggleTodo: (id) => set(state => ({
        todos: state.todos.map(t => 
            t.id === id ? { ...t, done: !t.done } : t
        )
    })),
    
    getCompletedCount: () => get().todos.filter(t => t.done).length
}));

function Counter() {
    const count = useStore(state => state.count);
    const increment = useStore(state => state.increment);
    return <button onClick={increment}>{count}</button>;
}
```

## 十、性能优化

```jsx
// 1. React.memo - 避免不必要的重渲染
const MemoizedComponent = React.memo(function MyComponent({ name }) {
    return <div>{name}</div>;
}, (prevProps, nextProps) => {
    return prevProps.name === nextProps.name;  // 自定义比较
});

// 2. 虚拟列表 (react-window)
// npm install react-window
import { FixedSizeList } from 'react-window';

function VirtualList({ items }) {
    const Row = ({ index, style }) => (
        <div style={style}>{items[index].name}</div>
    );
    
    return (
        <FixedSizeList
            height={400}
            width={300}
            itemCount={items.length}
            itemSize={50}
        >
            {Row}
        </FixedSizeList>
    );
}

// 3. 懒加载
const LazyComponent = React.lazy(() => import('./HeavyComponent'));

function App() {
    return (
        <Suspense fallback={<div>加载中...</div>}>
            <LazyComponent />
        </Suspense>
    );
}

// 4. useTransition (React 18)
function SearchPage() {
    const [query, setQuery] = useState('');
    const [isPending, startTransition] = useTransition();
    
    const handleChange = (e) => {
        startTransition(() => {
            setQuery(e.target.value);
        });
    };
    
    return (
        <div>
            <input onChange={handleChange} />
            {isPending && <span>更新中...</span>}
            <SearchResults query={query} />
        </div>
    );
}
```

> React 是现代 Web 开发的主流框架。重点掌握: 函数组件、Hooks (useState/useEffect/useContext/useRef)、自定义 Hooks、性能优化。推荐使用 Zustand 进行简单状态管理, React Router 处理路由。
