# STM32 GPIO 详解

## 概述

GPIO (General Purpose Input/Output) 是 STM32 最基本的外设接口，每个 GPIO 引脚可独立配置为输入、输出、复用功能或模拟模式。

## GPIO 模式

| 模式 | 描述 | 应用场景 |
|------|------|----------|
| 输入 (Input) | 读取外部信号电平 | 按键、传感器 |
| 输出 (Output) | 驱动外部器件电平 | LED、蜂鸣器 |
| 复用功能 (Alternate Function) | 引脚由片上外设控制 | USART、SPI、I2C |
| 模拟 (Analog) | 引脚连接 ADC/DAC 内部 | 模拟信号采集 |

## 输出类型

| 类型 | 特性 | 使用场景 |
|------|------|----------|
| 推挽 (Push-Pull) | 输出高低电平，驱动能力强 | 普通数字输出 |
| 开漏 (Open-Drain) | 输出低电平或高阻，需外部上拉 | I2C 总线、电平转换 |

## 输出速度

| 速度等级 | 适用场景 |
|----------|----------|
| Low (2 MHz) | 低功耗、低频信号 |
| Medium (10 MHz) | 通用 GPIO |
| High (50 MHz) | 高速通信如 SPI |
| Very High (100 MHz+) | 高速外设如 FMC |

## 上下拉电阻

| 配置 | 作用 |
|------|------|
| 上拉 (Pull-Up) | 引脚空闲时为高电平 |
| 下拉 (Pull-Down) | 引脚空闲时为低电平 |
| 浮空 (No Pull) | 引脚电平由外部决定 |

## HAL GPIO 函数

### 写引脚

```c
HAL_GPIO_WritePin(GPIOB, GPIO_PIN_0, GPIO_PIN_SET);   // 高电平
HAL_GPIO_WritePin(GPIOB, GPIO_PIN_0, GPIO_PIN_RESET); // 低电平
```

### 读引脚

```c
GPIO_PinState state = HAL_GPIO_ReadPin(GPIOA, GPIO_PIN_0);
if (state == GPIO_PIN_SET) {
    // 高电平
}
```

### 翻转引脚

```c
HAL_GPIO_TogglePin(GPIOC, GPIO_PIN_13);
```

### 初始化 GPIO

```c
GPIO_InitTypeDef GPIO_InitStruct = {0};

__HAL_RCC_GPIOA_CLK_ENABLE(); // 使能 GPIO 时钟

GPIO_InitStruct.Pin = GPIO_PIN_5 | GPIO_PIN_6;
GPIO_InitStruct.Mode = GPIO_MODE_OUTPUT_PP;
GPIO_InitStruct.Pull = GPIO_NOPULL;
GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_LOW;
HAL_GPIO_Init(GPIOA, &GPIO_InitStruct);
```

## 寄存器级配置

| 寄存器 | 位数 | 功能 |
|--------|------|------|
| GPIOx_MODER | 2 bit/pin | 模式选择: 00=输入, 01=输出, 10=复用, 11=模拟 |
| GPIOx_OTYPER | 1 bit/pin | 输出类型: 0=推挽, 1=开漏 |
| GPIOx_OSPEEDR | 2 bit/pin | 输出速度: 00=Low, 01=Medium, 10=High, 11=Very High |
| GPIOx_PUPDR | 2 bit/pin | 上下拉: 00=无, 01=上拉, 10=下拉, 11=保留 |
| GPIOx_IDR | 1 bit/pin | 输入数据寄存器 (只读) |
| GPIOx_ODR | 1 bit/pin | 输出数据寄存器 |
| GPIOx_BSRR | 16+16 bit | 位设置/复位寄存器 (写 1 有效) |

### 寄存器操作示例

```c
// 直接操作寄存器 - PB0 输出高电平
GPIOB->BSRR = GPIO_PIN_0;

// PB0 输出低电平
GPIOB->BSRR = (uint32_t)GPIO_PIN_0 << 16;

// 设置 PA5 为推挽输出
GPIOA->MODER &= ~(GPIO_MODER_MODER5);       // 清位
GPIOA->MODER |= GPIO_MODER_MODER5_0;         // 设为 01 (输出)
GPIOA->OTYPER &= ~(GPIO_OTYPER_OT_5);        // 推挽
GPIOA->OSPEEDR |= GPIO_OSPEEDR_OSPEEDR5;     // 高速
GPIOA->PUPDR &= ~(GPIO_PUPDR_PUPDR5);        // 无上下拉
```

## 在 CubeMX 中配置

1. Pinout & Configuration → GPIO 选择引脚
2. 设置: GPIO mode, Pull-up/Pull-down, Speed, User Label
3. 自动生成 `MX_GPIO_Init()` 代码

## 示例：LED 闪烁与按键检测

```c
// main.c
int main(void) {
    HAL_Init();
    SystemClock_Config();
    MX_GPIO_Init();

    while (1) {
        // 读取按键 (PA0, 按下为低电平)
        if (HAL_GPIO_ReadPin(GPIOA, GPIO_PIN_0) == GPIO_PIN_RESET) {
            HAL_GPIO_TogglePin(GPIOC, GPIO_PIN_13); // 翻转 LED
            HAL_Delay(200);
        }
    }
}
```

```c
// MX_GPIO_Init()
static void MX_GPIO_Init(void) {
    GPIO_InitTypeDef GPIO_InitStruct = {0};

    __HAL_RCC_GPIOA_CLK_ENABLE();
    __HAL_RCC_GPIOC_CLK_ENABLE();

    // LED PC13 - 推挽输出
    GPIO_InitStruct.Pin = GPIO_PIN_13;
    GPIO_InitStruct.Mode = GPIO_MODE_OUTPUT_PP;
    GPIO_InitStruct.Pull = GPIO_NOPULL;
    GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_LOW;
    HAL_GPIO_Init(GPIOC, &GPIO_InitStruct);

    // 按键 PA0 - 上拉输入 (按下接地)
    GPIO_InitStruct.Pin = GPIO_PIN_0;
    GPIO_InitStruct.Mode = GPIO_MODE_INPUT;
    GPIO_InitStruct.Pull = GPIO_PULLUP;
    HAL_GPIO_Init(GPIOA, &GPIO_InitStruct);
}
```

## 常见问题

1. **引脚无输出**：忘记使能 GPIO 时钟 (`__HAL_RCC_GPIOx_CLK_ENABLE()`)
2. **浮空电平不稳定**：配置上拉或下拉电阻
3. **开漏输出无高电平**：未接外部上拉电阻
4. **复用功能不工作**：AFR 寄存器配置错误，或外设时钟未使能

## 相关条目

- [[05_ComputerScience/HardwareAndEmbeddedSystems/Microcontrollers/STM32/INDEX|STM32]]
- [[Timer]]
- [[Interrupt]]
- [[ADC_DAC]]
- [[Communication]]
