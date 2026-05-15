---
aliases: [NodeJS]
tags: ['ProgrammingLanguages', 'Web', 'NodeJS']
---

# NodeJS 指南

## 一、模块系统

### CommonJS

```javascript
// math.js (导出)
const PI = 3.14159;

function add(a, b) {
    return a + b;
}

class Calculator {
    multiply(a, b) {
        return a * b;
    }
}

module.exports = { PI, add, Calculator };
module.exports.subtract = (a, b) => a - b;

// main.js (导入)
const math = require('./math.js');
const { PI, add, Calculator } = require('./math.js');

console.log(add(3, 5));  // 8
console.log(PI);         // 3.14159
```

### ESM (ECMAScript Modules)

```javascript
// math.mjs / package.json 中设置 "type": "module"
export const PI = 3.14159;
export function add(a, b) { return a + b; }
export class Calculator {
    multiply(a, b) { return a * b; }
}
export default { PI, add, Calculator };

// main.mjs
import { PI, add } from './math.mjs';
import * as math from './math.mjs';
import calc from './math.mjs';

// 动态导入
const module = await import('./math.mjs');
```

## 二、npm / yarn / pnpm

```json
// package.json
{
    "name": "my-project",
    "version": "1.0.0",
    "description": "项目描述",
    "main": "src/index.js",
    "type": "module",
    "scripts": {
        "dev": "node --watch src/index.js",
        "start": "node src/index.js",
        "test": "jest",
        "build": "tsc",
        "lint": "eslint src/",
        "format": "prettier --write src/"
    },
    "dependencies": {
        "express": "^4.18.2",
        "lodash": "~4.17.21"
    },
    "devDependencies": {
        "jest": "^29.7.0",
        "typescript": "^5.3.0"
    }
}

// 常用命令
// npm init -y          创建 package.json
// npm install express  安装依赖
// npm install -g nodemon 全局安装
// npm install --save-dev jest 开发依赖
// npm uninstall express 卸载
// npm update            更新依赖
// npm run dev           运行脚本
// npx create-react-app my-app 使用 npx

// 版本号
// ^1.2.3  兼容 1.x.x
// ~1.2.3  兼容 1.2.x
// 1.2.3   精确版本
// *       最新版本
```

## 三、内置模块

### fs - 文件系统

```javascript
import fs from 'fs';
import fsPromises from 'fs/promises';

// 同步 (不推荐在服务器使用)
const data = fs.readFileSync('file.txt', 'utf-8');
fs.writeFileSync('output.txt', '内容');
fs.appendFileSync('log.txt', '新行\n');

// 回调 (旧式)
fs.readFile('file.txt', 'utf-8', (err, data) => {
    if (err) {
        console.error('读取失败:', err);
        return;
    }
    console.log(data);
});

// Promise (推荐)
async function fileOps() {
    try {
        // 读取
        const data = await fsPromises.readFile('file.txt', 'utf-8');
        
        // 写入
        await fsPromises.writeFile('output.txt', data.toUpperCase());
        
        // 追加
        await fsPromises.appendFile('log.txt', `${new Date().toISOString()}\n`);
        
        // 目录操作
        await fsPromises.mkdir('new-dir', { recursive: true });
        const files = await fsPromises.readdir('.');
        
        // 文件信息
        const stat = await fsPromises.stat('file.txt');
        console.log(stat.size, stat.isFile(), stat.isDirectory());
        
        // 流式读取 (大文件)
        const readStream = fs.createReadStream('large-file.txt', { highWaterMark: 64 * 1024 });
        const writeStream = fs.createWriteStream('copy.txt');
        
        readStream.pipe(writeStream);
        
        readStream.on('data', chunk => console.log(`读取 ${chunk.length} 字节`));
        readStream.on('end', () => console.log('读取完成'));
        
    } catch (err) {
        console.error('操作失败:', err);
    }
}
```

### path - 路径处理

```javascript
import path from 'path';
import { fileURLToPath } from 'url';

// 当前文件路径 (ESM)
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// 路径操作
path.join('/usr', 'local', 'bin');      // '/usr/local/bin' (跨平台)
path.resolve('src', '..', 'dist');      // 解析为绝对路径
path.normalize('a//b/../c');            // 'a/c' 规范化
path.relative('/data/a', '/data/b');    // '../b' 相对路径

// 路径信息
path.basename('/a/b/file.txt');         // 'file.txt'
path.dirname('/a/b/file.txt');          // '/a/b'
path.extname('/a/b/file.txt');          // '.txt'
path.parse('/a/b/file.txt');
// { root: '/', dir: '/a/b', base: 'file.txt', ext: '.txt', name: 'file' }

// 跨平台路径分隔符
path.sep;        // Windows: '\', Unix: '/'
path.delimiter;  // Windows: ';', Unix: ':'
```

### http - HTTP 服务器

```javascript
import http from 'http';

const server = http.createServer((req, res) => {
    // 请求信息
    console.log(`${req.method} ${req.url}`);
    console.log('Headers:', req.headers);
    
    // 设置响应头
    res.writeHead(200, {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
        'Cache-Control': 'no-cache'
    });
    
    // 响应数据
    res.end(JSON.stringify({
        message: 'Hello World',
        timestamp: new Date().toISOString(),
        url: req.url
    }));
});

server.listen(3000, () => {
    console.log('服务器运行在 http://localhost:3000');
});

// 获取请求体
function getRequestBody(req) {
    return new Promise((resolve, reject) => {
        let body = '';
        req.on('data', chunk => body += chunk);
        req.on('end', () => {
            try {
                resolve(JSON.parse(body));
            } catch {
                resolve(body);
            }
        });
        req.on('error', reject);
    });
}
```

### events - 事件发射器

```javascript
import EventEmitter from 'events';

class MyEmitter extends EventEmitter {
    constructor() {
        super();
        this.counter = 0;
    }
    
    start() {
        this.interval = setInterval(() => {
            this.counter++;
            this.emit('tick', this.counter);
            
            if (this.counter >= 5) {
                this.emit('done', this.counter);
                this.stop();
            }
        }, 1000);
    }
    
    stop() {
        clearInterval(this.interval);
        this.removeAllListeners();
    }
}

const emitter = new MyEmitter();

emitter.on('tick', (count) => {
    console.log(`Tick #${count}`);
});

emitter.once('done', (finalCount) => {
    console.log(`完成! 最终计数: ${finalCount}`);
});

// emitter.start();

// 事件监听器管理
emitter.getMaxListeners();       // 默认 10
emitter.setMaxListeners(20);     // 增加限制
emitter.eventNames();            // 所有事件名
emitter.listenerCount('tick');   // 监听器数量
emitter.emit('custom', 'data');  // 触发自定义事件
```

### stream - 流

```javascript
import { Readable, Writable, Transform, pipeline } from 'stream';

// 可读流
const readable = Readable.from(['Hello', ' ', 'World', '!']);

// 可写流
const writable = new Writable({
    write(chunk, encoding, callback) {
        console.log('写入:', chunk.toString());
        callback();
    }
});

// 转换流
const upperCase = new Transform({
    transform(chunk, encoding, callback) {
        this.push(chunk.toString().toUpperCase());
        callback();
    }
});

// 管道链
readable.pipe(upperCase).pipe(writable);
// 或使用 pipeline (推荐, 自动处理错误)
pipeline(readable, upperCase, writable, (err) => {
    if (err) console.error('管道错误:', err);
});

// 文件流解压缩
import zlib from 'zlib';
// fs.createReadStream('file.txt')
//     .pipe(zlib.createGzip())
//     .pipe(fs.createWriteStream('file.txt.gz'));
```

## 四、Express.js

```javascript
import express from 'express';
import cors from 'cors';
import helmet from 'helmet';
import morgan from 'morgan';

const app = express();
const PORT = process.env.PORT || 3000;

// 中间件
app.use(helmet());                    // 安全头
app.use(cors());                      // 跨域
app.use(morgan('combined'));          // 日志
app.use(express.json());              // JSON 解析
app.use(express.urlencoded({ extended: true }));
app.use(express.static('public'));    // 静态文件

// 路由
app.get('/', (req, res) => {
    res.json({ message: 'Hello World' });
});

app.get('/users', (req, res) => {
    const { page = 1, limit = 10, sort } = req.query;
    res.json({ page, limit, sort, users: [] });
});

app.get('/users/:id', (req, res) => {
    const { id } = req.params;
    res.json({ id, name: `User ${id}` });
});

app.post('/users', (req, res) => {
    const { name, email } = req.body;
    // 验证
    if (!name || !email) {
        return res.status(400).json({ error: '缺少必填字段' });
    }
    // 创建用户...
    res.status(201).json({ id: Date.now(), name, email });
});

app.put('/users/:id', (req, res) => {
    const { id } = req.params;
    // 更新用户...
    res.json({ id, ...req.body });
});

app.delete('/users/:id', (req, res) => {
    const { id } = req.params;
    // 删除用户...
    res.status(204).send();
});

// 错误处理中间件
app.use((err, req, res, next) => {
    console.error('未捕获错误:', err);
    res.status(err.status || 500).json({
        error: err.message || '服务器内部错误',
        ...(process.env.NODE_ENV === 'development' && { stack: err.stack })
    });
});

// 404 处理
app.use((req, res) => {
    res.status(404).json({ error: '路径未找到' });
});

app.listen(PORT, () => {
    console.log(`服务器运行在 http://localhost:${PORT}`);
});
```

### Router 分离

```javascript
// routes/users.js
const router = express.Router();

router.get('/', (req, res) => res.json({ users: [] }));
router.get('/:id', (req, res) => res.json({ id: req.params.id }));
router.post('/', (req, res) => res.status(201).json(req.body));

export default router;

// app.js
import userRouter from './routes/users.js';
app.use('/api/users', userRouter);
```

## 五、认证 (JWT)

```javascript
// npm install jsonwebtoken bcrypt
import jwt from 'jsonwebtoken';
import bcrypt from 'bcrypt';

const JWT_SECRET = process.env.JWT_SECRET || 'your-secret-key';
const JWT_EXPIRES_IN = '7d';

// 密码哈希
async function hashPassword(password) {
    const salt = await bcrypt.genSalt(12);
    return bcrypt.hash(password, salt);
}

async function verifyPassword(password, hash) {
    return bcrypt.compare(password, hash);
}

// 生成 JWT
function generateToken(payload) {
    return jwt.sign(payload, JWT_SECRET, { 
        expiresIn: JWT_EXPIRES_IN,
        issuer: 'my-app'
    });
}

// 验证 JWT 中间件
function authenticateToken(req, res, next) {
    const authHeader = req.headers['authorization'];
    const token = authHeader && authHeader.split(' ')[1];  // Bearer TOKEN
    
    if (!token) {
        return res.status(401).json({ error: '未提供认证令牌' });
    }
    
    try {
        const decoded = jwt.verify(token, JWT_SECRET);
        req.user = decoded;
        next();
    } catch (err) {
        if (err.name === 'TokenExpiredError') {
            return res.status(401).json({ error: '令牌已过期' });
        }
        return res.status(403).json({ error: '无效的令牌' });
    }
}

// 登录路由
app.post('/api/login', async (req, res) => {
    const { username, password } = req.body;
    
    // 验证用户名密码...
    const user = { id: 1, username: 'admin', role: 'admin' };
    
    const token = generateToken({ 
        userId: user.id, 
        role: user.role 
    });
    
    res.json({ token, user: { id: user.id, username: user.username } });
});

// 受保护路由
app.get('/api/profile', authenticateToken, (req, res) => {
    res.json({ user: req.user });
});

// 角色授权
function authorizeRole(...roles) {
    return (req, res, next) => {
        if (!roles.includes(req.user.role)) {
            return res.status(403).json({ error: '权限不足' });
        }
        next();
    };
}

app.delete('/api/users/:id', authenticateToken, authorizeRole('admin'), async (req, res) => {
    // 仅管理员可删除
});
```

## 六、环境变量

```javascript
// npm install dotenv

// .env 文件
/*
PORT=3000
NODE_ENV=development
DATABASE_URL=mongodb://localhost:27017/myapp
JWT_SECRET=your-super-secret-key
API_KEY=abc123
LOG_LEVEL=debug
*/

// dotenv 配置
import dotenv from 'dotenv';
dotenv.config();

// 或直接在 package.json scripts 中:
// "start": "node -r dotenv/config src/index.js"

// 使用环境变量
const config = {
    port: parseInt(process.env.PORT, 10) || 3000,
    nodeEnv: process.env.NODE_ENV || 'development',
    databaseUrl: process.env.DATABASE_URL,
    jwtSecret: process.env.JWT_SECRET,
    isProduction: process.env.NODE_ENV === 'production',
    logLevel: process.env.LOG_LEVEL || 'info'
};

// 验证必需的环境变量
const requiredVars = ['DATABASE_URL', 'JWT_SECRET'];
requiredVars.forEach(varName => {
    if (!process.env[varName]) {
        throw new Error(`缺少必需的环境变量: ${varName}`);
    }
});
```

## 七、错误处理模式

```javascript
// 自定义错误类
class AppError extends Error {
    constructor(message, statusCode = 500) {
        super(message);
        this.statusCode = statusCode;
        this.isOperational = true;
        Error.captureStackTrace(this, this.constructor);
    }
}

class NotFoundError extends AppError {
    constructor(resource = '资源') {
        super(`${resource}未找到`, 404);
    }
}

class ValidationError extends AppError {
    constructor(message) {
        super(message, 400);
    }
}

// 统一错误处理
function errorHandler(err, req, res, next) {
    err.statusCode = err.statusCode || 500;
    err.status = err.statusCode.toString().startsWith('4') ? 'fail' : 'error';
    
    // 开发环境: 返回详细错误
    if (process.env.NODE_ENV === 'development') {
        return res.status(err.statusCode).json({
            status: err.status,
            error: err,
            message: err.message,
            stack: err.stack
        });
    }
    
    // 生产环境: 只返回简单信息
    if (err.isOperational) {
        return res.status(err.statusCode).json({
            status: err.status,
            message: err.message
        });
    }
    
    // 未知错误: 不暴露细节
    console.error('意外错误:', err);
    return res.status(500).json({
        status: 'error',
        message: '服务器内部错误'
    });
}

// 异步错误包装
function asyncHandler(fn) {
    return (req, res, next) => {
        Promise.resolve(fn(req, res, next)).catch(next);
    };
}

// 使用
app.get('/api/users/:id', asyncHandler(async (req, res) => {
    const user = await findUser(req.params.id);
    if (!user) throw new NotFoundError('用户');
    res.json(user);
}));
```

> NodeJS 是构建高性能后端服务的基础。重点掌握: 模块系统、Express 框架、异步编程、JWT 认证、错误处理模式。对于新项目, 建议使用 ESM 模块和现代 async/await 风格。
