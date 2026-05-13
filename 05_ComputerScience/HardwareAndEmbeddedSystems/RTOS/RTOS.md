# 实时操作系统（RTOS）

## 一、RTOS 概述

实时操作系统（RTOS）是一种保证任务在确定时间内完成的操作系统，核心特性是**确定性和可预测性**。

### RTOS vs GPOS

| 特性 | RTOS | GPOS (Linux/Windows) |
|------|------|---------------------|
| 调度策略 | 优先级抢占 | 时间片轮转 + 动态优先级 |
| 响应延迟 | 微秒级可预测 | 毫秒级不可预测 |
| 内核大小 | 小（KB-MB） | 大（MB-GB） |
| 内存管理 | 静态分配为主 | 虚拟内存、交换 |
| 中断延迟 | 极短 | 受关中断影响 |
| 公平性 | 不保证 | 保证 |

### 硬实时 vs 软实时

| 类型 | 错过截止时间后果 | 典型应用 |
|------|-----------------|---------|
| 硬实时 | 系统故障、灾难 | 飞行控制、医疗设备、汽车安全 |
| 软实时 | 性能下降、体验变差 | 音频/视频流、多媒体 |

## 二、RTOS 内核架构

| 组件 | 功能 | 说明 |
|------|------|------|
| 调度器（Scheduler） | 决定下一个运行的任务 | 优先级抢占或时间片 |
| 定时器（Timer） | 提供时间基准 | 系统滴答（SysTick） |
| 中断管理 | 处理硬件中断 | ISR + 底半处理 |
| 内存管理 | 动态/静态内存分配 | 内存池、堆管理 |
| 同步原语 | 任务间协调 | 信号量、互斥量、事件组 |
| 通信机制 | 数据传递 | 队列、邮箱、管道 |

## 三、任务管理

### 任务状态

```
就绪（Ready） ↔ 运行（Running）
    ↑                    ↓
  阻塞（Blocked）    挂起（Suspended）
```

- **就绪**：可运行但未获得 CPU
- **运行**：正在占用 CPU
- **阻塞**：等待资源或事件
- **挂起**：被其他任务或自身挂起

### 任务控制块（TCB）

每个任务对应一个 TCB，包含：任务栈指针、优先级、状态、任务名、堆栈大小等。

```c
// FreeRTOS 任务创建
TaskHandle_t xTaskHandle;
xTaskCreate(
    vTaskFunction,      // 任务函数
    "TaskName",         // 任务名称
    configMINIMAL_STACK_SIZE, // 栈深度
    NULL,               // 参数
    1,                  // 优先级
    &xTaskHandle        // 任务句柄
);
```

## 四、调度算法

### 速率单调调度（RMS）

优先级与周期成反比（周期越短优先级越高）。可调度性条件：

$$U = \sum_{i=1}^{n} \frac{C_i}{T_i} \leq n(2^{1/n} - 1)$$

当 $n \to \infty$ 时，$U \approx \ln 2 \approx 0.693$。

RMS 可调度性利用率上限：

| 任务数 $n$ | 利用率上限 $n(2^{1/n} - 1)$ |
|-----------|---------------------------|
| 1 | 1.000 |
| 2 | 0.828 |
| 3 | 0.780 |
| 4 | 0.757 |
| 5 | 0.743 |
| $\infty$ | $\ln 2 \approx 0.693$ |

### EDF（最早截止时间优先）

动态优先级，截止时间越早优先级越高。可调度性条件：

$$U = \sum_{i=1}^{n} \frac{C_i}{T_i} \leq 1$$

### 调度算法对比

| 算法 | 类型 | 最优性 | 开销 | 适用场景 |
|------|------|--------|------|---------|
| RMS | 静态优先级 | 固定优先级最优 | 低 | 周期任务 |
| EDF | 动态优先级 | 全局最优 | 高 | 混合任务 |
| Deadline Monotonic | 静态优先级 | 固定优先级最优 | 低 | 非周期任务 |
| 时间片轮转 | 公平共享 | — | 低 | 同等优先级任务 |

### 响应时间分析（RTA）

固定优先级调度中，任务 $i$ 的最坏情况响应时间 $R_i$ 可通过以下迭代公式计算：

$$R_i = C_i + B_i + \sum_{j \in hp(i)} \left\lceil \frac{R_i}{T_j} \right\rceil C_j$$

其中：
- $C_i$：任务 $i$ 的最坏情况执行时间
- $B_i$：任务 $i$ 的阻塞时间（低优先级任务占用共享资源导致）
- $T_j$：高优先级任务 $j$ 的周期
- $hp(i)$：优先级高于任务 $i$ 的所有任务集合

响应时间迭代计算示例（三组任务）：

| 任务 | $C_i$ | $T_i$ | 优先级 | 初始 $R_i^{(0)}$ | 收敛 $R_i$ |
|------|-------|-------|--------|-----------------|-----------|
| $\tau_1$ | 1 | 5 | 高 | 1 | 1 |
| $\tau_2$ | 2 | 8 | 中 | 2 | 3 |
| $\tau_3$ | 1 | 20 | 低 | 1 | 4 |

### 实时性对比

| 特性 | RMS | EDF | 时间片轮转 |
|------|-----|-----|-----------|
| 调度决策 | 静态（固定优先级） | 动态（截止时间驱动） | 公平共享 |
| CPU 利用率上限 | $n(2^{1/n} - 1)$ | 100% | — |
| 可预测性 | 高 | 中 | 低 |
| 适合负载 | 周期任务 | 混合截止时间 | 批处理/交互 |

## 五、任务间通信

### 队列（Queue）

```c
// FreeRTOS 队列示例
QueueHandle_t xQueue;

xQueue = xQueueCreate(5, sizeof(int));  // 容量 5，每项 int

// 发送
int data = 42;
xQueueSend(xQueue, &data, portMAX_DELAY);

// 接收
int received;
xQueueReceive(xQueue, &received, portMAX_DELAY);
```

| 机制 | 类型 | 大小 | 同步能力 |
|------|------|------|---------|
| 队列 | FIFO | 任意 | 支持阻塞 |
| 邮箱 | 覆盖式 | 固定 | 支持阻塞 |
| 管道 | 字节流 | 可变 | 支持阻塞 |
| 共享内存 | 无拷贝 | 任意 | 需同步原语 |
| 事件标志 | 位标记 | 32/64 位 | 支持多事件等待 |

## 六、同步机制

### 互斥量（Mutex）

互斥量用于保护共享资源，具有**优先级继承**防止优先级反转。

**优先级反转问题**：
```
高优先级任务 → 等待低优先级任务占用的资源 → 中优先级任务抢占 → 高优先级无限等待
```

优先级反转导致高优先级任务的响应时间显著增加：

$$R_{high} = C_{high} + \sum C_{interference} + B_{inversion}$$

其中 $B_{inversion}$ 为因低优先级任务持有锁而造成的阻塞时间。

优先级反转场景中各任务的时间参数：

| 任务 | 优先级 | 执行时间 $C$ | 持有锁时间 | 阻塞时间 $B$ |
|------|--------|-------------|-----------|-------------|
| H | 高 | 3 ms | 无 | 被 L 阻塞 5 ms |
| M | 中 | 10 ms | 无 | 0 |
| L | 低 | 5 ms | 5 ms（临界区） | 0 |

| 解决方案 | 原理 | 复杂度 |  worst-case 阻塞上界 |
|---------|------|--------|-------------------|
| 优先级继承 | 低优先级任务临时继承高优先级 | 中等 | 受限于嵌套锁层数 |
| 优先级天花板 | 设置资源的最高优先级 | 低 | 可计算 |
| 关中断 | 临界区关中断 | 极低（影响响应） | 关中断期间所有任务被阻塞 |

### 信号量（Semaphore）

```c
// 二值信号量
SemaphoreHandle_t xSemaphore;
xSemaphore = xSemaphoreCreateBinary();
xSemaphoreGive(xSemaphore);        // 释放
xSemaphoreTake(xSemaphore, 1000);  // 获取（超时 1s）

// 计数信号量
xSemaphore = xSemaphoreCreateCounting(10, 0);  // 最大 10，初始 0
```

| 同步原语 | 用途 | 特点 |
|---------|------|------|
| 二值信号量 | 事件通知 | 只有 0/1 两种状态 |
| 计数信号量 | 资源管理 | 任意计数值 |
| 互斥量 | 资源互斥访问 | 支持优先级继承 |
| 事件组 | 多事件等待 | 按位组合等待 |
| 任务通知 | 轻量信号 | 直接向任务发送 |

## 七、中断处理

### ISR 设计原则

1. **ISR 越短越好**：仅做必要的处理
2. **使用底半处理**：ISR 通过队列/信号量将耗时工作委托给任务
3. **避免阻塞调用**：ISR 中不能使用阻塞 API
4. **保存和恢复上下文**：编译器自动处理

```c
// FreeRTOS ISR 示例
void vTimerISR(void) {
    BaseType_t xHigherPriorityTaskWoken = pdFALSE;
    xSemaphoreGiveFromISR(xSemaphore, &xHigherPriorityTaskWoken);
    portYIELD_FROM_ISR(xHigherPriorityTaskWoken);
}
```

**中断延迟**：从硬件中断发生到 ISR 开始执行的时间，包括：
- 硬件延迟（中断控制器响应）
- 内核关中断时间
- 上下文保存时间

## 八、内存管理

| 策略 | 碎片 | 速度 | 适用 |
|------|------|------|------|
| 静态分配 | 无 | 最快 | 确定系统 |
| 内存池（固定块） | 无内部碎片 | 快 | 大小固定的数据 |
| 堆分配（动态） | 有 | 慢 | 大小可变 |
| 栈分配 | 无 | 快 | 局部变量 |

FreeRTOS 提供 5 种 heap 实现：

| heap 方案 | 特性 | 释放 |
|-----------|------|------|
| heap_1 | 简单、无碎片 | 不支持释放 |
| heap_2 | 最佳匹配 | 支持（有碎片） |
| heap_3 | 包装 malloc/free | 依赖编译器 |
| heap_4 | 首匹配、合并相邻 | 支持 |
| heap_5 | heap_4 + 多区域 | 支持 |

## 九、主流 RTOS 对比

| 特性 | FreeRTOS | Zephyr | RT-Thread | VxWorks | μC/OS-III |
|------|----------|--------|-----------|---------|-----------|
| 开源 | 是（MIT） | 是（Apache 2.0） | 是（Apache 2.0） | 否 | 有限 |
| 最小 RAM | ~1 KB | ~8 KB | ~3 KB | ~50 KB | ~4 KB |
| 架构支持 | 30+ | 25+ | 20+ | 10+ | 40+ |
| 网络协议栈 | FreeRTOS+TCP | 内置 | lwIP | 内置 | μC/TCP-IP |
| 文件系统 | 可选 | FS | DFS | 内置 | μC/FS |
| 认证 | 无 | ISO 26262 | 无 | DO-178B | 医疗/航空 |
| 厂商 | Amazon | Linux Foundation | 睿赛德 | Wind River | Micrium |

## 十、FreeRTOS API 汇总

```c
// 任务管理
xTaskCreate(pvTaskCode, pcName, usStackDepth, pvParameters, uxPriority, pxCreatedTask);
vTaskDelay(xTicksToDelay);
vTaskDelayUntil(pxPreviousWakeTime, xTimeIncrement);

// 队列
xQueueCreate(uxQueueLength, uxItemSize);
xQueueSend(xQueue, pvItemToQueue, xTicksToWait);
xQueueReceive(xQueue, pvBuffer, xTicksToWait);

// 信号量
xSemaphoreCreateBinary();
xSemaphoreCreateCounting(uxMaxCount, uxInitialCount);
xSemaphoreGive(xSemaphore);
xSemaphoreTake(xSemaphore, xTicksToWait);

// 互斥量
xSemaphoreCreateMutex();

// 事件组
EventGroupHandle_t xEventGroupCreate();
xEventGroupSetBits(xEventGroup, uxBitsToSet);
xEventGroupWaitBits(xEventGroup, uxBitsToWaitFor, xClearOnExit, xWaitForAllBits, xTicksToWait);
```

### 节电模式（Tickless Idle）

当所有任务都在阻塞时，RTOS 进入低功耗模式，停止系统滴答中断，在下一个事件到来时唤醒。可大幅降低功耗，适用于电池供电设备。

## 相关条目

- [[FreeRTOS任务与同步]]
- [[EmbeddedLinux]]
- [[ProcessManagement]]
- [[Concurrency]]
- [[死锁与并发控制]]

## 参考资源

- [FreeRTOS 官方文档](https://www.freertos.org/Documentation/RTOS_book.html)
- 《Real-Time Concepts for Embedded Systems》（Qing Li）
- [Zephyr Project 文档](https://docs.zephyrproject.org/)
- [RT-Thread 文档中心](https://www.rt-thread.io/document.html)
- μC/OS-III: The Real-Time Kernel（Jean J. Labrosse）
