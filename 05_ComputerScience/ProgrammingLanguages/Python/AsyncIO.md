# Python 异步编程

## 一、async/await 基础

```python
import asyncio
import time

# 定义协程
async def say_hello(name):
    print(f"你好, {name}!")
    await asyncio.sleep(1)  # 模拟异步IO
    print(f"再见, {name}!")

# 运行协程
async def main():
    await say_hello("张三")

# Python 3.7+ 方式
asyncio.run(main())

# 旧版方式 (Python 3.6)
# loop = asyncio.get_event_loop()
# loop.run_until_complete(main())
# loop.close()
```

### 理解 async/await

```python
# async def 定义协程函数
async def foo():
    return 42

# 调用协程函数返回协程对象 (不会立即执行)
coro = foo()
print(type(coro))  # <class 'coroutine'>

# 需要 await 或 run 才能执行
result = await foo()  # 只能在协程中使用

# 协程的3种运行方式:
# 1. asyncio.run(coro) - 顶层入口
# 2. await coro - 在另一个协程中
# 3. asyncio.create_task(coro) - 创建任务 (见下文)
```

## 二、任务 (Tasks)

```python
async def fetch_data(name, delay):
    print(f"开始获取 {name}...")
    await asyncio.sleep(delay)
    print(f"完成获取 {name}")
    return f"{name} 的数据"

async def main():
    # 创建任务 (并发执行)
    task1 = asyncio.create_task(fetch_data("数据A", 2))
    task2 = asyncio.create_task(fetch_data("数据B", 3))
    task3 = asyncio.create_task(fetch_data("数据C", 1))
    
    # 等待所有任务完成
    results = await asyncio.gather(task1, task2, task3)
    print(results)
    # 总耗时约3秒 (不是2+3+1=6秒)

asyncio.run(main())
```

### 任务管理

```python
async def main():
    task = asyncio.create_task(fetch_data("数据", 5))
    
    # 检查任务状态
    print(task.done())     # False
    print(task.cancelled()) # False
    
    # 超时控制
    try:
        result = await asyncio.wait_for(task, timeout=3)
    except asyncio.TimeoutError:
        print("任务超时!")
        task.cancel()  # 取消任务
    
    # 等待任务完成 (带超时)
    done, pending = await asyncio.wait(
        [asyncio.create_task(fetch_data("A", 2)),
         asyncio.create_task(fetch_data("B", 3))],
        timeout=5,
        return_when=asyncio.FIRST_COMPLETED
    )
    
    # 取消所有待处理任务
    for p in pending:
        p.cancel()
```

## 三、asyncio.gather 详解

```python
async def task(name, delay):
    await asyncio.sleep(delay)
    if delay == 2:
        raise ValueError(f"{name} 失败!")
    return f"{name} 完成"

async def main():
    # 基本用法 - 收集所有结果
    results = await asyncio.gather(
        task("A", 1),
        task("B", 3),
        task("C", 2),
        return_exceptions=False  # 默认: 第一个异常会传播
    )
    
    # return_exceptions=True: 异常作为结果返回
    results = await asyncio.gather(
        task("A", 1),
        task("B", 2),
        task("C", 3),
        return_exceptions=True
    )
    # [<正常结果>, ValueError(...), <正常结果>]
    
    # 处理结果中的异常
    for r in results:
        if isinstance(r, Exception):
            print(f"任务失败: {r}")
        else:
            print(f"成功: {r}")
```

## 四、异步上下文管理器

```python
# async with
class AsyncResource:
    async def __aenter__(self):
        print("获取资源...")
        await asyncio.sleep(0.5)
        print("资源就绪")
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        print("释放资源...")
        await asyncio.sleep(0.3)
        print("资源已释放")
        return False  # 不抑制异常
    
    async def work(self):
        await asyncio.sleep(0.5)
        return "工作完成"

async def main():
    async with AsyncResource() as res:
        result = await res.work()
        print(result)

# contextlib 方式
from contextlib import asynccontextmanager

@asynccontextmanager
async def managed_resource():
    print("获取资源")
    resource = {"connected": True}
    try:
        yield resource
    finally:
        print("释放资源")
        await asyncio.sleep(0.2)

async def main2():
    async with managed_resource() as res:
        print(res)
```

## 五、异步迭代器

```python
# async for
class AsyncRange:
    def __init__(self, start, end, delay=0.5):
        self.start = start
        self.end = end
        self.delay = delay
    
    def __aiter__(self):
        return self
    
    async def __anext__(self):
        if self.start >= self.end:
            raise StopAsyncIteration
        await asyncio.sleep(self.delay)
        value = self.start
        self.start += 1
        return value

async def main():
    async for num in AsyncRange(1, 5):
        print(num)

# 异步生成器
async def async_range(start, end, delay=0.3):
    for i in range(start, end):
        await asyncio.sleep(delay)
        yield i

async def main2():
    async for num in async_range(1, 5):
        print(num)
```

## 六、异步队列

```python
async def producer(queue, n):
    for i in range(n):
        await asyncio.sleep(0.5)
        item = f"项 {i}"
        await queue.put(item)
        print(f"生产: {item}")
    
    # 发送结束信号
    await queue.put(None)

async def consumer(queue, name):
    while True:
        item = await queue.get()
        if item is None:
            queue.task_done()
            break
        
        await asyncio.sleep(1)
        print(f"{name} 消费: {item}")
        queue.task_done()

async def main():
    queue = asyncio.Queue(maxsize=3)
    
    # 创建生产者和多个消费者
    producers = [asyncio.create_task(producer(queue, 5))]
    consumers = [asyncio.create_task(consumer(queue, f"Worker-{i}")) for i in range(2)]
    
    await asyncio.gather(*producers, *consumers)

# asyncio.run(main())
```

## 七、异步 HTTP (aiohttp)

```python
import aiohttp

async def fetch_url(session, url):
    async with session.get(url) as response:
        return await response.text()

async def fetch_all(urls):
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_url(session, url) for url in urls]
        return await asyncio.gather(*tasks)

# 使用示例
async def main():
    urls = [
        "http://example.com",
        "http://httpbin.org/get",
        "http://jsonplaceholder.typicode.com/posts/1"
    ]
    
    try:
        results = await fetch_all(urls)
        for url, content in zip(urls, results):
            print(f"{url}: {len(content)} 字节")
    except Exception as e:
        print(f"请求失败: {e}")

# 并发下载
async def download_file(session, url, filename):
    async with session.get(url) as response:
        with open(filename, "wb") as f:
            while True:
                chunk = await response.content.read(1024)
                if not chunk:
                    break
                f.write(chunk)
    return filename
```

## 八、信号量 (限制并发数)

```python
async def worker(semaphore, id):
    async with semaphore:
        print(f"Worker {id} 开始")
        await asyncio.sleep(2)
        print(f"Worker {id} 结束")

async def main():
    # 最多同时允许3个协程
    semaphore = asyncio.Semaphore(3)
    
    tasks = [asyncio.create_task(worker(semaphore, i)) for i in range(10)]
    await asyncio.gather(*tasks)
```

## 九、asyncio vs threading vs multiprocessing

```python
import asyncio
import threading
import multiprocessing
import time

# 1. asyncio - 单线程协作式 (适合IO密集型)
async def async_task(id):
    await asyncio.sleep(1)
    return id

async def async_main():
    tasks = [async_task(i) for i in range(100)]
    return await asyncio.gather(*tasks)
# 耗时: ~1秒 (并发100个)

# 2. threading - 多线程 (适合IO密集型)
def thread_task(results, id):
    time.sleep(1)
    results.append(id)

def thread_main():
    threads = []
    results = []
    for i in range(100):
        t = threading.Thread(target=thread_task, args=(results, i))
        threads.append(t)
        t.start()
    for t in threads:
        t.join()
    return results
# 耗时: ~1秒但有GIL限制

# 3. multiprocessing - 多进程 (适合CPU密集型)
def cpu_task(n):
    return sum(i * i for i in range(n))

def mp_main():
    with multiprocessing.Pool(4) as pool:
        results = pool.map(cpu_task, [10**6] * 8)
    return results
# 利用多核CPU

# 对比总结:
"""
asyncio:       单线程, 开销最小, 适合大量IO并发 (网络请求、文件读写)
threading:     多线程, 有GIL, 适合IO密集型, 但有线程安全问题
multiprocessing: 多进程, 无GIL, 适合CPU密集型, 但开销大

选择建议:
- 网络爬虫/Web服务: asyncio
- CPU密集计算: multiprocessing
- 混合场景: asyncio + multiprocessing (如 asyncio.run_in_executor)
"""
```

## 十、实用模式与技巧

```python
# 1. 超时包装器
async def timeout_wrapper(coro, timeout=5):
    try:
        return await asyncio.wait_for(coro, timeout=timeout)
    except asyncio.TimeoutError:
        print("操作超时")
        return None

# 2. 重试装饰器
def async_retry(max_retries=3, delay=1):
    def decorator(func):
        async def wrapper(*args, **kwargs):
            for attempt in range(max_retries):
                try:
                    return await func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_retries - 1:
                        raise
                    print(f"重试 {attempt + 1}/{max_retries}")
                    await asyncio.sleep(delay)
        return wrapper
    return decorator

@async_retry(max_retries=3)
async def unstable_api():
    # 模拟不稳定的API
    pass

# 3. asyncio.run_in_executor - 同步代码桥接
async def blocking_wrapper():
    loop = asyncio.get_event_loop()
    # 在线程池中运行阻塞函数
    result = await loop.run_in_executor(
        None,  # 使用默认线程池
        time.sleep,  # 阻塞函数
        2           # 参数
    )
    return result

# 4. 事件循环细节
async def event_loop_info():
    loop = asyncio.get_running_loop()
    print(f"事件循环: {loop}")
    print(f"是否运行: {loop.is_running()}")
    print(f"是否关闭: {loop.is_closed()}")

# 5. 自定义事件循环策略
class CustomEventLoopPolicy(asyncio.DefaultEventLoopPolicy):
    def new_event_loop(self):
        loop = super().new_event_loop()
        loop.set_debug(True)  # 开启调试
        return loop

# asyncio.set_event_loop_policy(CustomEventLoopPolicy())
```

> asyncio 是 Python 实现高并发的利器。核心思想: 在单线程中通过协程协作式调度, 遇到IO操作时主动让出控制权。熟练掌握 asyncio 能让你用少量资源处理大量并发连接。
