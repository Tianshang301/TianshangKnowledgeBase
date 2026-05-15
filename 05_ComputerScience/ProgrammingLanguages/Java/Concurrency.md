---
aliases: [Concurrency]
tags: ['ProgrammingLanguages', 'Java', 'Concurrency']
---

# Java 并发编程

## 线程创建

### 继承 Thread

```java
class MyThread extends Thread {
    @Override
    public void run() {
        System.out.println("Thread running: " + Thread.currentThread().getName());
    }
}

MyThread t = new MyThread();
t.start();  // 启动线程
```

### 实现 Runnable

```java
class MyRunnable implements Runnable {
    @Override
    public void run() {
        System.out.println("Runnable running");
    }
}

Thread t = new Thread(new MyRunnable());
t.start();

// Lambda 简化
Thread t2 = new Thread(() -> System.out.println("Lambda thread"));
t2.start();
```

### Callable + Future（带返回值）

```java
ExecutorService executor = Executors.newFixedThreadPool(2);
Future<Integer> future = executor.submit(new Callable<Integer>() {
    @Override
    public Integer call() throws Exception {
        Thread.sleep(1000);
        return 42;
    }
});

Integer result = future.get();       // 阻塞获取结果（1秒后返回 42）
boolean done = future.isDone();
future.cancel(true);                 // 取消任务
```

## 线程生命周期

```
NEW ──start()──> RUNNABLE ──> TERMINATED
                    │
              ┌─────┴──────┐
              │            │
           BLOCKED     WAITING/TIMED_WAITING
```

```java
Thread.State[] states = {
    Thread.State.NEW,             // 新建
    Thread.State.RUNNABLE,        // 可运行
    Thread.State.BLOCKED,         // 阻塞（等待锁）
    Thread.State.WAITING,         // 等待（wait/join/park）
    Thread.State.TIMED_WAITING,   // 定时等待
    Thread.State.TERMINATED       // 终止
};
```

## synchronized

### 同步方法

```java
public class Counter {
    private int count = 0;

    // 实例方法锁：锁 this 对象
    public synchronized void increment() {
        count++;
    }

    // 静态方法锁：锁 Class 对象
    public static synchronized void staticMethod() {
        // ...
    }
}
```

### 同步块

```java
public void add() {
    synchronized (this) {    // 锁对象
        count++;
    }
}

// 锁 class 对象
public void staticAdd() {
    synchronized (Counter.class) {
        // ...
    }
}

// 锁自定义对象
private final Object lock = new Object();
public void safeMethod() {
    synchronized (lock) {
        // 临界区
    }
}
```

## volatile

保证可见性，不保证原子性。

```java
public class VolatileExample {
    private volatile boolean running = true;

    public void stop() {
        running = false;  // 对其他线程立即可见
    }

    public void run() {
        while (running) {
            // 不会因为缓存导致死循环
        }
    }
}
```

## wait/notify/notifyAll

必须在 synchronized 块内使用。

```java
public class WaitNotifyExample {
    private final Object lock = new Object();
    private boolean ready = false;

    public void await() throws InterruptedException {
        synchronized (lock) {
            while (!ready) {          // 防止虚假唤醒
                lock.wait();          // 释放锁并等待
            }
        }
    }

    public void signal() {
        synchronized (lock) {
            ready = true;
            lock.notifyAll();         // 唤醒所有等待线程
        }
    }
}
```

## Lock 接口

### ReentrantLock

可重入、可中断、支持公平锁。

```java
Lock lock = new ReentrantLock();  // 默认为非公平锁

lock.lock();
try {
    // 临界区
} finally {
    lock.unlock();  // 必须在 finally 中释放
}

// tryLock 非阻塞获取
if (lock.tryLock(1, TimeUnit.SECONDS)) {
    try {
        // 获取锁成功
    } finally {
        lock.unlock();
    }
}
```

### ReadWriteLock

读写分离，读读不互斥，读写/写写互斥。

```java
ReadWriteLock rwLock = new ReentrantReadWriteLock();

// 读锁
Lock readLock = rwLock.readLock();
readLock.lock();
try {
    // 多个线程可同时读
} finally {
    readLock.unlock();
}

// 写锁
Lock writeLock = rwLock.writeLock();
writeLock.lock();
try {
    // 写时独占
} finally {
    writeLock.unlock();
}
```

## 原子类

基于 CAS（Compare-And-Swap）实现，无锁并发。

```java
AtomicInteger atomicInt = new AtomicInteger(0);
atomicInt.incrementAndGet();     // ++i
atomicInt.getAndIncrement();     // i++
atomicInt.addAndGet(5);          // += 5
atomicInt.compareAndSet(10, 20); // CAS

AtomicLong atomicLong = new AtomicLong();
AtomicBoolean atomicBool = new AtomicBoolean(false);

// 引用原子类
AtomicReference<String> ref = new AtomicReference<>("initial");
ref.compareAndSet("initial", "updated");

// 字段原子更新
public class Point {
    private volatile int x;
    private volatile int y;
}

AtomicIntegerFieldUpdater<Point> xUpdater =
    AtomicIntegerFieldUpdater.newUpdater(Point.class, "x");
```

## 并发集合

### ConcurrentHashMap

线程安全的 HashMap，JDK 8 采用 CAS + synchronized。

```java
ConcurrentHashMap<String, Integer> map = new ConcurrentHashMap<>();
map.put("A", 1);
map.putIfAbsent("A", 2);             // key 存在时不覆盖
map.computeIfAbsent("B", k -> 2);    // 不存在则计算
map.forEach((k, v) -> System.out.println(k + "=" + v));
```

### CopyOnWriteArrayList

写时复制，读操作无锁，适合读多写少场景。

```java
CopyOnWriteArrayList<String> list = new CopyOnWriteArrayList<>();
list.add("A");       // 内部创建新数组
list.add("B");
list.get(0);         // 无需加锁，直接读原数组
```

### BlockingQueue

支持阻塞的队列。

```java
// 有界阻塞队列
BlockingQueue<String> queue = new ArrayBlockingQueue<>(10);

// 生产者
queue.put("item");       // 队列满时阻塞
queue.offer("item", 1, TimeUnit.SECONDS);  // 超时等待

// 消费者
String item = queue.take();     // 队列空时阻塞
String item2 = queue.poll(1, TimeUnit.SECONDS);  // 超时等待

// 其他实现
BlockingQueue<Runnable> linkedQueue = new LinkedBlockingQueue<>();   // 无界
BlockingQueue<String> priorityQueue = new PriorityBlockingQueue<>(); // 优先级
BlockingQueue<String> delayQueue = new DelayQueue<>();               // 延迟
BlockingQueue<String> synchronousQueue = new SynchronousQueue<>();   // 直接传递
```

## ExecutorService

### 线程池

```java
// 固定大小线程池
ExecutorService executor = Executors.newFixedThreadPool(4);

// 缓存线程池（自动回收）
ExecutorService cachedPool = Executors.newCachedThreadPool();

// 单线程池
ExecutorService singlePool = Executors.newSingleThreadExecutor();

// 提交任务
executor.execute(() -> System.out.println("Runnable task"));
Future<String> future = executor.submit(() -> "Callable result");

// 关闭
executor.shutdown();                  // 不再接受新任务，等待已提交任务完成
// executor.shutdownNow();            // 尝试停止所有任务

try {
    executor.awaitTermination(5, TimeUnit.SECONDS);
} catch (InterruptedException e) {
    Thread.currentThread().interrupt();
}
```

### ScheduledExecutorService

```java
ScheduledExecutorService scheduler = Executors.newScheduledThreadPool(2);

// 延迟执行
scheduler.schedule(() -> System.out.println("Delayed"), 1, TimeUnit.SECONDS);

// 周期性执行（固定频率）
scheduler.scheduleAtFixedRate(() -> System.out.println("Fixed rate"), 0, 5, TimeUnit.SECONDS);

// 周期性执行（固定延迟）
scheduler.scheduleWithFixedDelay(() -> System.out.println("Fixed delay"), 0, 5, TimeUnit.SECONDS);
```

## CompletableFuture

异步编程利器，支持函数式组合。

```java
// 异步执行
CompletableFuture<String> future = CompletableFuture.supplyAsync(() -> {
    return "Hello";
});

// 链式处理
CompletableFuture<String> processed = future
    .thenApply(s -> s + " World")
    .thenApply(String::toUpperCase);

// 消费结果
future.thenAccept(System.out::println);

// 组合两个 Future
CompletableFuture<String> future1 = CompletableFuture.supplyAsync(() -> "Hello");
CompletableFuture<String> future2 = CompletableFuture.supplyAsync(() -> "World");
CompletableFuture<String> combined = future1.thenCombine(future2, (a, b) -> a + " " + b);

// 任意一个完成
CompletableFuture<Object> anyOf = CompletableFuture.anyOf(future1, future2);

// 全部完成
CompletableFuture<Void> allOf = CompletableFuture.allOf(future1, future2);

// 异常处理
CompletableFuture<String> withError = future
    .thenApply(s -> { throw new RuntimeException("Error"); })
    .exceptionally(ex -> "Fallback result");

// 自定义线程池
ExecutorService executor = Executors.newFixedThreadPool(4);
CompletableFuture.supplyAsync(() -> compute(), executor);
```

## 常见并发问题及解决方案

### 死锁

四个必要条件：互斥、持有并等待、不可剥夺、循环等待。

```java
// 死锁示例
Object lockA = new Object();
Object lockB = new Object();

// 线程1
new Thread(() -> {
    synchronized (lockA) {
        synchronized (lockB) { /* ... */ }
    }
}).start();

// 线程2（顺序与线程1相反导致死锁）
new Thread(() -> {
    synchronized (lockB) {
        synchronized (lockA) { /* ... */ }
    }
}).start();

// 解决方案：固定锁获取顺序、使用 tryLock 超时
```

### 活锁

线程不断重试但始终无法成功。解决方案：引入随机等待。

### 线程饥饿

低优先级线程始终无法获取执行机会。解决方案：使用公平锁。

```java
Lock fairLock = new ReentrantLock(true);  // 公平锁
```

### ABA 问题

CAS 中值被 A→B→A 误判为未修改。解决方案：AtomicStampedReference。

```java
AtomicStampedReference<String> ref = new AtomicStampedReference<>("A", 0);
int[] stampHolder = new int[1];
String value = ref.get(stampHolder);
int stamp = stampHolder[0];
ref.compareAndSet("A", "B", stamp, stamp + 1);
```

### 伪共享（False Sharing）

多线程修改独立变量但位于同一缓存行。解决方案：@Contended 或填充。

```java
@Contended
public class FalseSharingExample {
    public volatile long x;
    public volatile long y;
}
```
