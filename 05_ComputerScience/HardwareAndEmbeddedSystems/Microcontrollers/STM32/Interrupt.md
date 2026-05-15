---
aliases: [Interrupt]
tags: ['HardwareAndEmbeddedSystems', 'Microcontrollers', 'STM32', 'Interrupt']
---

# STM32 中断系统

## NVIC (Nested Vectored Interrupt Controller)

NVIC 是 ARM Cortex-M 内核的中断控制器，支持：
- 最多 240 个中断源
- 可编程中断优先级 (8~256 级)
- 中断嵌套 (高优先级可抢占低优先级)
- 向量化中断 (每个中断有独立入口地址)

## 中断优先级

### 优先级分组

| 分组 | 抢占优先级位数 | 子优先级位数 | 优先级数量 |
|------|---------------|-------------|-----------|
| NVIC_PRIORITYGROUP_0 | 0 | 4 | 16 级子优先级 |
| NVIC_PRIORITYGROUP_1 | 1 | 3 | 2 级抢占 × 8 级子优先 |
| NVIC_PRIORITYGROUP_2 | 2 | 2 | 4 × 4 |
| NVIC_PRIORITYGROUP_3 | 3 | 1 | 8 × 2 |
| NVIC_PRIORITYGROUP_4 | 4 | 0 | 16 级抢占 |

数字越小，优先级越高。

```c
// 设置优先级分组 (整个系统只能调用一次)
HAL_NVIC_SetPriorityGrouping(NVIC_PRIORITYGROUP_2);

// 配置具体中断优先级
// 中断: USART1_IRQn, 抢占优先级=1, 子优先级=1
HAL_NVIC_SetPriority(USART1_IRQn, 1, 1);
HAL_NVIC_EnableIRQ(USART1_IRQn);

// 禁用中断
HAL_NVIC_DisableIRQ(USART1_IRQn);
```

## EXTI (外部中断)

EXTI 支持最多 16 个外部中断线，每个 GPIO 引脚可通过 AFIO/SYSCFG 映射到 EXTI 线。

| 中断线 | 可选 GPIO |
|--------|-----------|
| EXTI0 | PA0, PB0, PC0, PD0, ... |
| EXTI1 | PA1, PB1, PC1, PD1, ... |
| ... | ... |
| EXTI15 | PA15, PB15, PC15, PD15, ... |

### 配置外部中断

```c
void MX_GPIO_Init(void) {
    GPIO_InitTypeDef GPIO_InitStruct = {0};

    __HAL_RCC_GPIOA_CLK_ENABLE();
    __HAL_RCC_SYSCFG_CLK_ENABLE();

    // PA0 外部中断 (按键)
    GPIO_InitStruct.Pin = GPIO_PIN_0;
    GPIO_InitStruct.Mode = GPIO_MODE_IT_FALLING; // 下降沿触发
    GPIO_InitStruct.Pull = GPIO_PULLUP;
    HAL_GPIO_Init(GPIOA, &GPIO_InitStruct);

    // 配置 NVIC
    HAL_NVIC_SetPriority(EXTI0_IRQn, 2, 0);
    HAL_NVIC_EnableIRQ(EXTI0_IRQn);
}
```

## 中断服务程序 (ISR)

### 中断向量表

中断向量表位于 Flash 起始地址，每个中断入口对应一个函数名。

```c
// 文件: startup_stm32f4xx.s
// DCD EXTI0_IRQHandler   ; EXTI Line0
```

### 编写 ISR

```c
// 中断入口函数 (在 startup 文件中声明)
void EXTI0_IRQHandler(void) {
    // 检查中断标志
    if (__HAL_GPIO_EXTI_GET_IT(GPIO_PIN_0) != RESET) {
        // 清除中断标志
        __HAL_GPIO_EXTI_CLEAR_IT(GPIO_PIN_0);

        // 用户代码
        HAL_GPIO_TogglePin(GPIOC, GPIO_PIN_13);
    }
}
```

### HAL 中断回调

使用 HAL 库时，通常不直接写 ISR，而是使用回调函数：

```c
// HAL 已经实现了 EXTI0_IRQHandler，在其中调用此回调
void HAL_GPIO_EXTI_Callback(uint16_t GPIO_Pin) {
    if (GPIO_Pin == GPIO_PIN_0) {
        HAL_GPIO_TogglePin(GPIOC, GPIO_PIN_13);
    }
}
```

### 定时器中断回调

```c
void HAL_TIM_PeriodElapsedCallback(TIM_HandleTypeDef *htim) {
    if (htim->Instance == TIM3) {
        // 定时器溢出，每 1ms 执行
        sensor_read_flag = 1;
    }
}
```

### UART 接收中断回调

```c
uint8_t rx_byte;
HAL_UART_Receive_IT(&huart1, &rx_byte, 1);

void HAL_UART_RxCpltCallback(UART_HandleTypeDef *huart) {
    if (huart->Instance == USART1) {
        // 处理接收到的字节
        rx_buffer[rx_index++] = rx_byte;
        HAL_UART_Receive_IT(&huart1, &rx_byte, 1); // 重新启动接收
    }
}
```

## 中断嵌套

当高优先级中断在低优先级中断执行时发生，CPU 会暂停低优先级 ISR，执行高优先级 ISR。

```
主程序 (Thread mode)
  ↓ (低优先级中断请求)
EXTI0_IRQHandler (抢占优先级=3)
  ↓ (高优先级中断请求，可抢占)
TIM3_IRQHandler (抢占优先级=1)
  ↓ (TIM3 ISR 执行完毕返回)
EXTI0_IRQHandler 继续执行
  ↓ (EXTI0 ISR 执行完毕返回)
主程序继续
```

## 中断延迟

中断延迟 = CPU 响应中断到执行第一条 ISR 指令的时间。

Cortex-M3/M4 的中断延迟约为 12 个时钟周期。影响因素：
- 优先级分组
- 正在执行的中断
- Flash 等待周期
- CPU 频率

### 减少中断延迟的方法

```c
// 1. 在 RAM 中执行中断函数 (通过 __RAM_FUNC)
__RAM_FUNC void EXTI0_IRQHandler(void) {
    // ...
}

// 2. 精简 ISR 代码，只做必要操作
void EXTI0_IRQHandler(void) {
    __HAL_GPIO_EXTI_CLEAR_IT(GPIO_PIN_0);
    event_flag = 1; // 设标志，主循环处理
}
```

## 中断安全编程实践

### 1. 共享数据保护

```c
volatile uint32_t shared_counter;

// ISR 中修改
void TIM3_IRQHandler(void) {
    shared_counter++;
}

// 主程序中读取，需关中断
uint32_t read_counter_safe(void) {
    uint32_t temp;
    __disable_irq();
    temp = shared_counter;
    __enable_irq();
    return temp;
}
```

### 2. 在 ISR 中调用 HAL 函数

```c
void EXTI0_IRQHandler(void) {
    // 正确: 清除标志, 设标志
    __HAL_GPIO_EXTI_CLEAR_IT(GPIO_PIN_0);
    button_pressed = 1;

    // 错误: ISR 中调用 HAL_Delay (依赖 SysTick 中断)
    // HAL_Delay(10);
}
```

### 3. 临界区保护

```c
// 进入临界区 (关中断)
__disable_irq();
// 操作共享资源
buffer[index++] = data;
// 退出临界区
__enable_irq();
```

### 4. FreeRTOS 中 ISR 注意事项

```c
void EXTI0_IRQHandler(void) {
    BaseType_t xHigherPriorityTaskWoken = pdFALSE;
    __HAL_GPIO_EXTI_CLEAR_IT(GPIO_PIN_0);

    // 使用 FromISR 版本
    xQueueSendFromISR(queue_handle, &data, &xHigherPriorityTaskWoken);

    // 如果需要任务切换
    portYIELD_FROM_ISR(xHigherPriorityTaskWoken);
}
```

## 中断源汇总表 (STM32F4)

| 中断号 | 名称 | 描述 |
|--------|------|------|
| 0 | WWDG | 窗口看门狗 |
| 1 | PVD | 电压检测 |
| 2 | TAMP_STAMP | 篡改/时间戳 |
| 3 | RTC_WKUP | RTC 唤醒 |
| 6 | EXTI0 | 外部中断 0 |
| 7 | EXTI1 | 外部中断 1 |
| ... | ... | ... |
| 28 | TIM3 | TIM3 全局中断 |
| 37 | USART1 | USART1 全局中断 |
| 45 | TIM1_CC | TIM1 捕获比较 |
| 51 | DMA1_Stream0 | DMA1 数据流 0 |

## 相关条目

- [[GPIO]]
- [[Timer]]
- [[ADCDAC]]
- [[Communication]]
- [[FreeRTOS]]
