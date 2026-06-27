---
aliases: [JVM]
tags: ['ProgrammingLanguages', 'Java', 'JVM']
created: 2026-05-16
updated: 2026-05-16
---

# JVM 深入

## JVM 架构

```
┌─────────────────────────────────────────────────────┐
│                  Class Loader                        │
│  Bootstrap ──> Extension ──> Application            │
└──────────────────────┬──────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────┐
│                  Runtime Data Areas                  │
│  ┌──────────────┐  ┌──────────────┐                 │
│  │    Heap      │  │   Method     │                 │
│  │ (Young/Old)  │  │    Area      │                 │
│  └──────────────┘  └──────────────┘                 │
│  ┌──────────────┐  ┌──────────────┐                 │
│  │   Stack      │  │ PC Register  │                 │
│  └──────────────┘  └──────────────┘                 │
│  ┌──────────────┐                                   │
│  │Native Method │                                   │
│  │    Stack     │                                   │
│  └──────────────┘                                   │
└─────────────────────────────────────────────────────┘
```

### 运行时数据区

| 区域 | 线程共享 | 作用 | 异常 |
|------|---------|------|------|
| 堆（Heap） | 是 | 存放对象实例 | OutOfMemoryError |
| 方法区（Method Area） | 是 | 类信息、常量、静态变量 | OutOfMemoryError |
| 栈（Stack） | 否 | 方法调用、局部变量 | StackOverflowError, OutOfMemoryError |
| PC 寄存器 | 否 | 当前线程执行地址 | 无 |
| 本地方法栈 | 否 | native 方法调用 | StackOverflowError |

### 堆空间划分

```
┌───────────────── Heap ─────────────────┐
│  ┌──── Young Gen ────┐ ┌─── Old ───┐  │
│  │ Eden │ S0 │ S1    │ │          │  │
│  └───────────────────┘ └───────────┘  │
│                Metaspace               │
└────────────────────────────────────────┘
```

JDK 8 后 Metaspace（元空间）取代永久代，使用本地内存。

## 垃圾回收（GC）

### 判断对象是否存活

**引用计数法**：循环引用问题。

**可达性分析**（Java 使用）：从 GC Roots 出发，不可达的对象即为可回收。

GC Roots 包括：
- 栈帧中的局部变量引用的对象
- 静态变量引用的对象
- JNI 引用的对象
- 活跃线程

### 引用类型

| 引用类型 | 回收时机 | 使用场景 |
|---------|---------|---------|
| 强引用 | 永不回收 | new 对象 |
| 软引用 | 内存不足时回收 | 缓存 |
| 弱引用 | 下次 GC 即回收 | WeakHashMap, ThreadLocal |
| 虚引用 | 任何时候 | 对象回收跟踪 |

```java
// 软引用
SoftReference<Object> softRef = new SoftReference<>(new Object());

// 弱引用
WeakReference<Object> weakRef = new WeakReference<>(new Object());

// 虚引用
ReferenceQueue<Object> queue = new ReferenceQueue<>();
PhantomReference<Object> phantomRef = new PhantomReference<>(new Object(), queue);
```

### GC 算法

| 算法 | 描述 | 优点 | 缺点 |
|------|------|------|------|
| 标记-清除（Mark-Sweep） | 标记存活对象，清除未标记对象 | 实现简单 | 产生内存碎片 |
| 标记-整理（Mark-Compact） | 标记存活，整理到一端 | 无碎片 | 移动成本高 |
| 复制（Copying） | 将存活对象复制到另一半空间 | 无碎片、高效 | 空间浪费一半 |
| 分代收集（Generational） | 新生代复制、老年代标记整理 | 综合优势 | 需要分代协调 |

### GC 收集器

#### 新生代收集器

| 收集器 | 算法 | 线程 | 特点 |
|--------|------|------|------|
| Serial | 复制 | 单线程 | 简单高效，适合单核/客户端模式 |
| ParNew | 复制 | 多线程 | Serial 的多线程版本 |
| Parallel Scavenge | 复制 | 多线程 | 关注吞吐量，可控制吞吐量大小 |

```bash
# 使用 Serial + Serial Old
-XX:+UseSerialGC

# 使用 Parallel Scavenge + Parallel Old
-XX:+UseParallelGC
-XX:ParallelGCThreads=4
-XX:MaxGCPauseMillis=100
-XX:GCTimeRatio=19  # 吞吐量 95%
```

#### 老年代收集器

| 收集器 | 算法 | 线程 | 特点 |
|--------|------|------|------|
| Serial Old | 标记-整理 | 单线程 | CMS 后备方案 |
| Parallel Old | 标记-整理 | 多线程 | 配合 Parallel Scavenge |
| CMS | 标记-清除 | 多线程 | 低停顿，并发收集，产生碎片 |

```bash
# CMS 收集器
-XX:+UseConcMarkSweepGC
-XX:CMSInitiatingOccupancyFraction=70  # 触发 CMS 的老年代占比
-XX:+UseCMSCompactAtFullCollection     # 碎片整理
-XX:CMSFullGCsBeforeCompaction=5
```

**CMS 流程**：
1. 初始标记（STW）：标记 GC Roots 直接关联对象
2. 并发标记：从 GC Roots 追溯标记
3. 重新标记（STW）：修正并发标记期间变动的对象
4. 并发清除

**CMS 缺点**：CPU 敏感、浮动垃圾、内存碎片

#### G1 收集器（JDK 7u4+，JDK 9 默认）

将堆划分为 2048 个 Region，维护优先列表，优先回收收益最大的 Region。

```bash
-XX:+UseG1GC
-XX:G1HeapRegionSize=4M
-XX:MaxGCPauseMillis=200          # 目标停顿时间
-XX:ParallelGCThreads=8
-XX:ConcGCThreads=4
-XX:InitiatingHeapOccupancyPercent=45  # 触发并发标记的堆占比
```

**G1 流程**：
1. 年轻代 GC：复制 Eden 到 Survivor/Old
2. 并发标记：类似 CMS
3. 混合 GC：选择价值最高的 Region 回收

#### ZGC（JDK 11+，JDK 15 正式版）

超低延迟（<10ms），支持 TB 级堆。

```bash
-XX:+UseZGC
-XX:ZAllocationSpikeTolerance=2.0
-XX:ZCollectionInterval=120
```

## JMM（Java Memory Model）

### happens-before 规则

1. **程序次序规则**：同一个线程中，前面的操作 happens-before 后面的操作
2. **volatile 规则**：对 volatile 变量的写 happens-before 随后的读
3. **锁规则**：解锁 happens-before 后续的加锁
4. **线程启动规则**：Thread.start() happens-before 线程中的任何操作
5. **线程终止规则**：线程中的操作 happens-before 其他线程检测该线程终止
6. **线程中断规则**：interrupt() happens-before 检测中断事件
7. **对象终结规则**：构造完成 happens-before finalize()
8. **传递性**：A happens-before B, B happens-before C → A happens-before C

### 重排序

编译器重排序、处理器重排序、内存系统重排序。

内存屏障防止重排序：
- LoadLoad Barrier
- StoreStore Barrier
- LoadStore Barrier
- StoreLoad Barrier

## 类加载机制

### 类加载器

```
Bootstrap ClassLoader（C++ 实现，加载 rt.jar）
    └── Extension ClassLoader（加载 jre/lib/ext/*）
        └── Application/System ClassLoader（加载 classpath）
            └── 自定义 ClassLoader
```

### 双亲委派模型

```java
protected Class<?> loadClass(String name, boolean resolve)
        throws ClassNotFoundException {
    // 1. 检查是否已加载
    Class<?> c = findLoadedClass(name);
    if (c == null) {
        try {
            // 2. 委派给父加载器
            if (parent != null) {
                c = parent.loadClass(name, false);
            } else {
                c = findBootstrapClassOrNull(name);
            }
        } catch (ClassNotFoundException e) {
            // 父加载器无法加载
        }
        if (c == null) {
            // 3. 自己加载
            c = findClass(name);
        }
    }
    return c;
}
```

**破坏双亲委派**：重写 loadClass 方法（如 Tomcat、SPI）。

### 类加载过程

```
加载 ──> 验证 ──> 准备 ──> 解析 ──> 初始化
         └────────── 链接 ──────────┘
```

| 阶段 | 说明 |
|------|------|
| 加载 | 通过全限定名获取二进制字节流，生成 Class 对象 |
| 验证 | 文件格式、字节码语义、符号引用验证 |
| 准备 | 为静态变量分配内存并设默认值 |
| 解析 | 将符号引用替换为直接引用 |
| 初始化 | 执行 `<clinit>()` 方法，为静态变量赋值 |

## JVM 调优

### 常用 JVM 参数

```bash
# 堆设置
-Xms4g                     # 初始堆大小
-Xmx4g                     # 最大堆大小
-Xmn2g                     # 新生代大小
-XX:MetaspaceSize=256m     # 元空间初始大小
-XX:MaxMetaspaceSize=256m  # 元空间最大大小
-XX:SurvivorRatio=8        # Eden : Survivor = 8:1:1
-XX:+UseAdaptiveSizePolicy # 自适应调整

# GC 日志（JDK 8）
-XX:+PrintGCDetails
-XX:+PrintGCDateStamps
-Xloggc:/path/to/gc.log

# GC 日志（JDK 11+）
-Xlog:gc*:file=/path/to/gc.log:time,uptime,level,tags

# 内存溢出处理
-XX:+HeapDumpOnOutOfMemoryError
-XX:HeapDumpPath=/path/to/dump.hprof

# 其他
-XX:+DisableExplicitGC     # 禁止 System.gc()
-Djava.awt.headless=true
```

### 调优案例

#### 案例 1：频繁 Full GC

```bash
# 现象：频繁 Full GC，但老年代使用率并不高
# 原因：Metaspace 不断扩容触发 Full GC

# 解决：固定 Metaspace 大小
-XX:MetaspaceSize=256m -XX:MaxMetaspaceSize=256m
```

#### 案例 2：CMS 并发模式失败

```bash
# 现象：Concurrent Mode Failure 导致 Serial Old 执行
# 原因：老年代在 CMS 完成前被填满

# 解决：提前触发 CMS
-XX:CMSInitiatingOccupancyFraction=60
-XX:+UseCMSInitiatingOccupancyOnly
```

#### 案例 3：G1 停顿时间过长

```bash
# 调整 Region 大小
-XX:G1HeapRegionSize=8M

# 减少目标停顿时间
-XX:MaxGCPauseMillis=100

# 增加并发线程
-XX:ConcGCThreads=8
```

### 监控工具

| 工具 | 用途 |
|------|------|
| jps | 查看 Java 进程 |
| jstat | 查看 GC 统计信息 |
| jmap | 堆转储和内存信息 |
| jstack | 线程堆栈 |
| jinfo | JVM 参数 |
| jcmd | 综合诊断工具 |
| VisualVM | 可视化监控 |
| MAT | 堆转储分析 |
| Arthas | 在线诊断 |

```bash
# jstat：查看 GC 情况（每 1 秒输出一次，共 10 次）
jstat -gcutil <pid> 1000 10

# jmap：堆转储
jmap -dump:format=b,file=heap.hprof <pid>
jmap -heap <pid>

# jstack：查看线程
jstack <pid>
jstack <pid> | grep "BLOCKED"
```

