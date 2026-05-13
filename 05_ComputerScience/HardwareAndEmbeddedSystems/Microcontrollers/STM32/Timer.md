# STM32 定时器详解

## 定时器类型

| 类型 | 定时器 | 位数 | 主要特性 |
|------|--------|------|----------|
| 基本定时器 | TIM6, TIM7 | 16位 | 基本定时、DAC触发 |
| 通用定时器 | TIM2~TIM5, TIM9~TIM14 | 16/32位 | 输入捕获、输出比较、PWM、编码器 |
| 高级定时器 | TIM1, TIM8 | 16位 | 通用功能 + 死区插入、互补输出、刹车 |

## 定时器功能

### 时基 (Time Base)

定时器时钟经过预分频器 (PSC) 分频后驱动计数器 (CNT) 递增/递减，与自动重载值 (ARR) 比较产生事件。

```
定时频率 = TIMx_CLK / (PSC + 1) / (ARR + 1)
```

```c
// TIM3 配置为 1ms 中断
TIM_HandleTypeDef htim3;

void MX_TIM3_Init(void) {
    htim3.Instance = TIM3;
    htim3.Init.Prescaler = 84 - 1;         // 84MHz / 84 = 1MHz (1us)
    htim3.Init.CounterMode = TIM_COUNTERMODE_UP;
    htim3.Init.Period = 1000 - 1;           // 1MHz / 1000 = 1kHz (1ms)
    htim3.Init.ClockDivision = TIM_CLOCKDIVISION_DIV1;
    htim3.Init.AutoReloadPreload = TIM_AUTORELOAD_PRELOAD_ENABLE;
    HAL_TIM_Base_Init(&htim3);
}
```

### 输入捕获 (Input Capture)

测量外部脉冲的频率、周期、占空比。

```c
// 输入捕获中断启动
HAL_TIM_IC_Start_IT(&htim2, TIM_CHANNEL_1);

// 捕获回调
uint32_t capturedValue;
void HAL_TIM_IC_CaptureCallback(TIM_HandleTypeDef *htim) {
    if (htim->Instance == TIM2) {
        capturedValue = HAL_TIM_ReadCapturedValue(htim, TIM_CHANNEL_1);
        // 频率 = TIM_CLK / (PSC+1) / capturedValue
    }
}
```

### 输出比较 (Output Compare)

在指定计数值时改变输出电平，用于产生精确延时或脉冲。

### PWM 生成

PWM 模式通过比较 CNT 与 CCRx 产生可变占空比的方波。

```
PWM 频率 = TIM_CLK / (PSC + 1) / (ARR + 1)
PWM 占空比 = CCRx / (ARR + 1) * 100%
```

```c
// TIM4 配置 PWM，PA6 输出
TIM_HandleTypeDef htim4;

void MX_TIM4_PWM_Init(void) {
    TIM_OC_InitTypeDef sConfigOC = {0};

    htim4.Instance = TIM4;
    htim4.Init.Prescaler = 84 - 1;         // 1MHz
    htim4.Init.Period = 1000 - 1;           // PWM 频率 1kHz
    htim4.Init.CounterMode = TIM_COUNTERMODE_UP;
    HAL_TIM_PWM_Init(&htim4);

    sConfigOC.OCMode = TIM_OCMODE_PWM1;
    sConfigOC.Pulse = 500;                  // 占空比 50%
    sConfigOC.OCPolarity = TIM_OCPOLARITY_HIGH;
    sConfigOC.OCFastMode = TIM_OCFAST_DISABLE;
    HAL_TIM_PWM_ConfigChannel(&htim4, &sConfigOC, TIM_CHANNEL_1);
}

// 启动 PWM
HAL_TIM_PWM_Start(&htim4, TIM_CHANNEL_1);

// 动态改变占空比
__HAL_TIM_SET_COMPARE(&htim4, TIM_CHANNEL_1, 750); // 75%
```

#### LED 呼吸灯示例

```c
void breathing_led(void) {
    // 定时器已配置: TIM4 CH1 (PA6), PWM 1kHz
    HAL_TIM_PWM_Start(&htim4, TIM_CHANNEL_1);

    while (1) {
        // 亮度渐增
        for (int i = 0; i <= 1000; i++) {
            __HAL_TIM_SET_COMPARE(&htim4, TIM_CHANNEL_1, i);
            HAL_Delay(1);
        }
        // 亮度渐减
        for (int i = 1000; i >= 0; i--) {
            __HAL_TIM_SET_COMPARE(&htim4, TIM_CHANNEL_1, i);
            HAL_Delay(1);
        }
    }
}
```

### 单脉冲模式 (One-Pulse Mode)

在外部触发后产生一个可编程宽度的脉冲。

### 编码器接口

直接连接增量式编码器的 A、B 相，自动计数脉冲和方向。

```c
// TIM3 编码器模式配置
TIM_Encoder_InitTypeDef sEncoder = {0};

sEncoder.EncoderMode = TIM_ENCODERMODE_TI12;      // TI1+TI2 双边沿
sEncoder.IC1Polarity = TIM_ICPOLARITY_RISING;
sEncoder.IC1Selection = TIM_ICSELECTION_DIRECTTI;
sEncoder.IC1Prescaler = TIM_ICPSC_DIV1;
sEncoder.IC1Filter = 0;
// IC2 同理
HAL_TIM_Encoder_Init(&htim3, &sEncoder);

HAL_TIM_Encoder_Start(&htim3, TIM_CHANNEL_ALL);

// 读取编码器值
int32_t enc_value = (int16_t)__HAL_TIM_GET_COUNTER(&htim3);
```

## 中断与 DMA 操作

| 方式 | 优点 | 缺点 |
|------|------|------|
| 轮询 | 简单 | 占用 CPU |
| 中断 | 实时性好 | 频繁中断开销大 |
| DMA | CPU 几乎不参与 | 配置复杂 |

```c
// 中断方式定时
HAL_TIM_Base_Start_IT(&htim3);

void HAL_TIM_PeriodElapsedCallback(TIM_HandleTypeDef *htim) {
    if (htim->Instance == TIM3) {
        // 每 1ms 执行一次
        HAL_GPIO_TogglePin(GPIOC, GPIO_PIN_13);
    }
}
```

```c
// DMA 方式更新多个 PWM 通道
HAL_TIM_PWM_Start_DMA(&htim1, TIM_CHANNEL_1, (uint32_t*)pwm_buffer, CHANNEL_COUNT);
```

## 频率测量示例 (输入捕获)

```c
// 使用 TIM2 CH1 测量输入频率
volatile uint32_t ic_val1, ic_val2;
volatile uint8_t capture_done = 0;

void HAL_TIM_IC_CaptureCallback(TIM_HandleTypeDef *htim) {
    if (htim->Instance == TIM2) {
        if (htim->Channel == HAL_TIM_ACTIVE_CHANNEL_1) {
            ic_val1 = HAL_TIM_ReadCapturedValue(htim, TIM_CHANNEL_1);
            capture_done = 1;
        }
    }
}

// 测量频率
uint32_t measure_frequency(void) {
    uint32_t freq;
    HAL_TIM_IC_Start_IT(&htim2, TIM_CHANNEL_1);
    while (!capture_done);
    capture_done = 0;
    // 频率 = 1MHz / ic_val1
    freq = 1000000 / ic_val1;
    return freq;
}
```

## 定时器同步与级联

多个定时器可以同步或级联工作，实现更复杂的时序控制：

- 一个定时器触发另一个定时器
- 主从模式 (Master/Slave)
- 定时器同步输出多个 PWM

## 常见问题

1. **PWM 不输出**：检查 GPIO 复用功能配置
2. **定时不准**：确认时钟源频率和预分频器计算
3. **输入捕获无中断**：检查 NVIC 使能和中断优先级
4. **编码器计数反向**：交换 A/B 相或改变极性设置

## 相关条目

- [[GPIO]]
- [[Interrupt]]
- [[ADC_DAC]]
- PWM
- [[05_ComputerScience/HardwareAndEmbeddedSystems/Microcontrollers/STM32/INDEX|STM32]]
