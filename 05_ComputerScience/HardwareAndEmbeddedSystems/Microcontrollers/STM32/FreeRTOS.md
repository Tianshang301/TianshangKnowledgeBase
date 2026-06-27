---
aliases: [FreeRTOS]
tags: ['HardwareAndEmbeddedSystems', 'Microcontrollers', 'STM32', 'FreeRTOS']
created: 2026-05-16
updated: 2026-05-13
---

# FreeRTOS on STM32

## 概述

FreeRTOS 是 STM32 上最流行的实时操作系统内核，提供任务管理、同步、通信和内存管理功能。

## 任务创建与管理

### xTaskCreate

```c
TaskHandle_t task_handle;

void vTaskFunction(void *pvParameters) {
    while (1) {
        // 任务代码
        vTaskDelay(pdMS_TO_TICKS(1000));
    }
}

// 创建任务
xTaskCreate(
    vTaskFunction,          // 任务函数
    "TaskName",             // 任务名称 (调试用)
    128,                    // 堆栈大小 (字, 不是字节)
    NULL,                   // 参数
    1,                      // 优先级 (0=最低, configMAX_PRIORITIES-1=最高)
    &task_handle            // 任务句柄 (可选)
);
```

### 任务参数

| 参数 | 说明 |
|------|------|
| pvTaskCode | 任务函数指针 |
| pcName | 任务名称，最大 configMAX_TASK_NAME_LEN |
| usStackDepth | 堆栈深度 (单位: 字, 32位处理器为 4 字节) |
| pvParameters | 任务参数指针 |
| uxPriority | 任务优先级 (0 ~ configMAX_PRIORITIES-1) |
| pxCreatedTask | 返回任务句柄 |

### vTaskDelay

```c
// 延迟指定 tick 数
vTaskDelay(pdMS_TO_TICKS(100)); // 延迟 100ms

// 延迟到指定时间 (周期性任务)
TickType_t xLastWakeTime = xTaskGetTickCount();
while (1) {
    // 任务代码
    vTaskDelayUntil(&xLastWakeTime, pdMS_TO_TICKS(100));
}
```

## 任务状态

```
Running    → 正在执行 (由调度器分配)
Ready      → 可运行但尚未被调度
Blocked    → 等待事件或时间
Suspended  → 被显式挂起
```

```c
// 挂起任务
vTaskSuspend(task_handle);

// 恢复任务
vTaskResume(task_handle);

// 从中断中恢复任务
BaseType_t xHigherPriorityTaskWoken = pdFALSE;
xTaskResumeFromISR(task_handle, &xHigherPriorityTaskWoken);
portYIELD_FROM_ISR(xHigherPriorityTaskWoken);
```

## 队列 (Queue)

队列用于任务间通信 (发送/接收数据)。

### 创建和操作

```c
QueueHandle_t xQueue;

// 创建队列 (可容纳 10 个 int 值)
xQueue = xQueueCreate(10, sizeof(int));

// 发送 (任务中)
int data = 42;
xQueueSend(xQueue, &data, portMAX_DELAY);

// 接收 (任务中)
int received;
if (xQueueReceive(xQueue, &received, pdMS_TO_TICKS(100)) == pdPASS) {
    // received = 42
}

// 从中断发送
void ISR_Handler(void) {
    int data = read_sensor();
    BaseType_t xHigherPriorityTaskWoken = pdFALSE;
    xQueueSendFromISR(xQueue, &data, &xHigherPriorityTaskWoken);
    portYIELD_FROM_ISR(xHigherPriorityTaskWoken);
}

// 从中断接收
BaseType_t xHigherPriorityTaskWoken = pdFALSE;
xQueueReceiveFromISR(xQueue, &received, &xHigherPriorityTaskWoken);
```

### 队列发送 API 对比

| API | 使用场景 |
|-----|---------|
| xQueueSend | 任务中发送 (等效于 xQueueSendToBack) |
| xQueueSendToFront | 插入队首 |
| xQueueSendToBack | 插入队尾 |
| xQueueOverwrite | 覆盖 (队列长度为 1 时) |
| xQueueSendFromISR | ISR 中发送 |
| xQueueOverwriteFromISR | ISR 中覆盖 |

## 信号量 (Semaphore)

### 二进制信号量

```c
SemaphoreHandle_t xBinarySemaphore;

// 创建
xBinarySemaphore = xSemaphoreCreateBinary();

// 任务中获取
if (xSemaphoreTake(xBinarySemaphore, portMAX_DELAY) == pdPASS) {
    // 获得信号量
}

// ISR 中给予
BaseType_t xHigherPriorityTaskWoken = pdFALSE;
xSemaphoreGiveFromISR(xBinarySemaphore, &xHigherPriorityTaskWoken);
portYIELD_FROM_ISR(xHigherPriorityTaskWoken);
```

### 计数信号量

```c
// 创建计数信号量 (最大值 10，初始值 0)
SemaphoreHandle_t xCountingSemaphore = xSemaphoreCreateCounting(10, 0);

// 给予 (增加计数)
xSemaphoreGive(xCountingSemaphore);

// 获取 (减少计数)
xSemaphoreTake(xCountingSemaphore, portMAX_DELAY);
```

### 互斥量 (Mutex)

```c
SemaphoreHandle_t xMutex;

// 创建互斥量 (支持优先级继承)
xMutex = xSemaphoreCreateMutex();

// 获取
xSemaphoreTake(xMutex, portMAX_DELAY);
// 访问共享资源
shared_data++;
// 释放
xSemaphoreGive(xMutex);
```

### 二进制 vs 计数信号量 vs 互斥量

| 类型 | 用途 | 特性 |
|------|------|------|
| 二进制信号量 | 事件通知、同步 | 只有 0 和 1 两个状态 |
| 计数信号量 | 资源管理 (有限资源) | 可计数，表示可用资源数量 |
| 互斥量 | 互斥访问共享资源 | 支持优先级继承，必须由同一任务获取和释放 |

## 软件定时器

```c
TimerHandle_t xTimer;

void vTimerCallback(TimerHandle_t xTimer) {
    // 定时器到期执行
    HAL_GPIO_TogglePin(LED_PORT, LED_PIN);
}

// 创建自动重载定时器，周期 1000ms
xTimer = xTimerCreate(
    "Timer",                          // 名称
    pdMS_TO_TICKS(1000),              // 周期 tick
    pdTRUE,                           // 自动重载
    (void *)0,                        // ID
    vTimerCallback                    // 回调
);

// 启动定时器
xTimerStart(xTimer, 0);

// 改变周期
xTimerChangePeriod(xTimer, pdMS_TO_TICKS(500), 0);
```

## 任务通知 (Task Notifications)

每个任务有一个 32 位通知值，可替代信号量和队列（更高效）。

```c
TaskHandle_t xTaskToNotify;

// 发送通知
xTaskNotifyGive(xTaskToNotify);

// 发送通知 (带值)
uint32_t ulValue = 123;
xTaskNotify(xTaskToNotify, ulValue, eSetValueWithOverwrite);

// 等待通知 (阻塞)
ulTaskNotifyTake(pdTRUE, portMAX_DELAY);

// ISR 中发送
BaseType_t xHigherPriorityTaskWoken = pdFALSE;
xTaskNotifyFromISR(xTaskToNotify, ulValue, eSetValueWithOverwrite,
                   &xHigherPriorityTaskWoken);
```

## 内存管理

| Heap 方案 | 优点 | 缺点 |
|-----------|------|------|
| heap_1 | 最简单，无碎片 | 不能释放内存 |
| heap_2 | 可释放内存 | 可能产生碎片 |
| heap_3 | 使用标准 malloc/free，线程安全 | 依赖于链接器 |
| heap_4 | 合并相邻空闲块，减少碎片 | 比 heap_2 稍慢 |
| heap_5 | 支持多个不连续内存区域 | 配置复杂 |

```c
// FreeRTOSConfig.h 中选择
#define configTOTAL_HEAP_SIZE ((size_t)32768)  // 32KB 堆空间
```

## CMSIS-RTOS v2 封装

FreeRTOS 在 STM32CubeFW 中通过 CMSIS-RTOS v2 API 封装：

```c
#include "cmsis_os2.h"

osThreadId_t tid_thread;
osThreadAttr_t thread_attr = {
    .name = "myThread",
    .stack_size = 256 * 4,
    .priority = osPriorityNormal,
};

void thread_func(void *arg) {
    while (1) {
        osDelay(100);
    }
}

int main(void) {
    HAL_Init();
    SystemClock_Config();
    MX_GPIO_Init();
    MX_USART2_UART_Init();

    osKernelInitialize();
    tid_thread = osThreadNew(thread_func, NULL, &thread_attr);
    osKernelStart();

    while(1);
}
```

## 实践示例：多任务传感器读取与 UART 输出

```c
#include "FreeRTOS.h"
#include "task.h"
#include "queue.h"
#include "semphr.h"

QueueHandle_t sensor_queue;
SemaphoreHandle_t uart_mutex;

// 传感器读取任务
void vSensorTask(void *pvParameters) {
    uint32_t sensor_val;
    TickType_t xLastWakeTime = xTaskGetTickCount();

    while (1) {
        sensor_val = read_adc();                    // 读取传感器
        xQueueSend(sensor_queue, &sensor_val, 0);   // 发送到队列
        vTaskDelayUntil(&xLastWakeTime, pdMS_TO_TICKS(100));
    }
}

// UART 输出任务
void vUartTask(void *pvParameters) {
    uint32_t received_val;
    char msg[64];

    while (1) {
        if (xQueueReceive(sensor_queue, &received_val, portMAX_DELAY)) {
            xSemaphoreTake(uart_mutex, portMAX_DELAY);
            sprintf(msg, "Sensor: %lu\r\n", received_val);
            HAL_UART_Transmit(&huart2, (uint8_t*)msg, strlen(msg), HAL_MAX_DELAY);
            xSemaphoreGive(uart_mutex);
        }
    }
}

// LED 闪烁任务
void vLedTask(void *pvParameters) {
    TickType_t xLastWakeTime = xTaskGetTickCount();

    while (1) {
        HAL_GPIO_TogglePin(LED_PORT, LED_PIN);
        vTaskDelayUntil(&xLastWakeTime, pdMS_TO_TICKS(500));
    }
}

int main(void) {
    HAL_Init();
    SystemClock_Config();
    MX_GPIO_Init();
    MX_USART2_UART_Init();
    MX_ADC1_Init();

    sensor_queue = xQueueCreate(5, sizeof(uint32_t));
    uart_mutex = xSemaphoreCreateMutex();

    xTaskCreate(vSensorTask, "Sensor", 128, NULL, 2, NULL);
    xTaskCreate(vUartTask,   "UART",   256, NULL, 1, NULL);
    xTaskCreate(vLedTask,    "LED",    128, NULL, 1, NULL);

    vTaskStartScheduler();  // 启动调度器

    while (1);  // 不应到达这里
}
```

## FreeRTOSConfig.h 常用配置

```c
#define configUSE_PREEMPTION           1      // 抢占式调度
#define configUSE_TIME_SLICING         1      // 时间片轮转
#define configCPU_CLOCK_HZ             ((uint32_t)84000000)
#define configTICK_RATE_HZ             ((TickType_t)1000)  // 1ms tick
#define configMAX_PRIORITIES           5
#define configMINIMAL_STACK_SIZE       ((uint16_t)128)
#define configTOTAL_HEAP_SIZE          ((size_t)16384)
#define configUSE_MUTEXES              1
#define configUSE_COUNTING_SEMAPHORES  1
#define configUSE_TIMERS               1      // 软件定时器
#define configUSE_TASK_NOTIFICATIONS   1
#define INCLUDE_vTaskDelayUntil        1
#define INCLUDE_xSemaphoreGetMutexHolder 1
```

## 常见问题

1. **任务未运行**：检查堆栈大小是否不足，优先级是否过低
2. **HardFault**：通常是堆栈溢出，增大 `usStackDepth`
3. **ISR 中调用非 FromISR 函数**：必须使用 `FromISR` 版本的 API
4. **优先级反转**：使用互斥量（带优先级继承）而非二进制信号量
5. **内存不足**：检查 `configTOTAL_HEAP_SIZE`，使用 heap_4 减少碎片
