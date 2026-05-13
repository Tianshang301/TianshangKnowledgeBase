# STM32 ADC/DAC 详解

## ADC (模数转换器)

### 主要特性

| 特性 | STM32F4 | STM32F1 | STM32L4 |
|------|---------|---------|---------|
| 分辨率 | 12位 (可配置 6/8/10/12) | 12位 | 12位 |
| 通道数 | 16+ (外部) + 2 (内部) | 16+ | 16+ |
| 转换时间 | 最快 0.5μs | 最快 1μs | 最快 5μs |
| 转换模式 | 单次/连续/扫描/注入 | 单次/连续/扫描/注入 | 单次/连续/扫描/注入 |
| 内部通道 | 温度传感器、Vrefint | 温度传感器、Vrefint | 温度传感器、Vrefint、VBAT |

### 转换模式

| 模式 | 描述 | 使用场景 |
|------|------|----------|
| 单次转换 (Single) | 转换一次后停止 | 单通道单次采样 |
| 连续转换 (Continuous) | 持续转换并更新数据 | 连续监测 |
| 扫描模式 (Scan) | 按序转换多个通道 | 多通道采集 |
| 注入模式 (Injected) | 抢占式转换 (优先级高于常规) | 紧急采样 |

### 常规组 vs 注入组

- **常规组 (Regular Group)**：最多 16 个通道，按顺序转换，产生 DMA 请求
- **注入组 (Injected Group)**：最多 4 个通道，可打断常规组转换，类似中断

### HAL ADC 函数

#### 单次转换 (轮询)

```c
ADC_HandleTypeDef hadc1;

void MX_ADC1_Init(void) {
    ADC_ChannelConfTypeDef sConfig = {0};

    __HAL_RCC_ADC1_CLK_ENABLE();

    hadc1.Instance = ADC1;
    hadc1.Init.ClockPrescaler = ADC_CLOCK_SYNC_PCLK_DIV4;
    hadc1.Init.Resolution = ADC_RESOLUTION_12B;
    hadc1.Init.ScanConvMode = DISABLE;
    hadc1.Init.ContinuousConvMode = DISABLE;
    hadc1.Init.DiscontinuousConvMode = DISABLE;
    hadc1.Init.ExternalTrigConv = ADC_SOFTWARE_START;
    hadc1.Init.DataAlign = ADC_DATAALIGN_RIGHT;
    hadc1.Init.NbrOfConversion = 1;
    hadc1.Init.DMAContinuousRequests = DISABLE;
    hadc1.Init.EOCSelection = ADC_EOC_SINGLE_CONV;
    HAL_ADC_Init(&hadc1);

    sConfig.Channel = ADC_CHANNEL_0;    // PA0
    sConfig.Rank = 1;
    sConfig.SamplingTime = ADC_SAMPLETIME_3CYCLES;
    HAL_ADC_ConfigChannel(&hadc1, &sConfig);
}

// 读取模拟值 (阻塞)
uint32_t read_adc(void) {
    HAL_ADC_Start(&hadc1);
    HAL_ADC_PollForConversion(&hadc1, HAL_MAX_DELAY);
    return HAL_ADC_GetValue(&hadc1);
}
```

#### 中断方式

```c
HAL_ADC_Start_IT(&hadc1);

void HAL_ADC_ConvCpltCallback(ADC_HandleTypeDef* hadc) {
    if (hadc->Instance == ADC1) {
        uint32_t adc_val = HAL_ADC_GetValue(hadc);
        // 处理转换结果
    }
}
```

#### DMA 方式 (多通道连续采集)

```c
#define ADC_BUFFER_SIZE 128
uint32_t adc_buffer[ADC_BUFFER_SIZE];

void MX_ADC1_DMA_Init(void) {
    // ... ADC 初始化 (开启扫描模式和连续转换)

    HAL_ADC_Start_DMA(&hadc1, adc_buffer, ADC_BUFFER_SIZE);
}

void HAL_ADC_ConvHalfCpltCallback(ADC_HandleTypeDef* hadc) {
    // 前半缓冲区填满
    process_adc_data(adc_buffer, ADC_BUFFER_SIZE / 2);
}

void HAL_ADC_ConvCpltCallback(ADC_HandleTypeDef* hadc) {
    // 后半缓冲区填满
    process_adc_data(&adc_buffer[ADC_BUFFER_SIZE / 2], ADC_BUFFER_SIZE / 2);
}
```

### ADC 电压计算

```c
// 3.3V 参考电压, 12位分辨率
float adc_to_voltage(uint32_t adc_value) {
    return (adc_value * 3.3f) / 4095.0f;
}

// 使用内部参考电压校准 (更精确)
float adc_to_voltage_calibrated(uint32_t adc_value) {
    // Vrefint 典型值 1.21V，实际值在生产时校准
    return (adc_value * 3.3f) / 4095.0f;
}
```

### 双 ADC 模式

STM32 支持两个 ADC 同步采样，用于需要同时采集两个通道的应用（如三相电流检测）。

| 模式 | 描述 |
|------|------|
| ADC1 + ADC2 同时 | 同步采样 |
| 交替采样 | 交错采样提高等效采样率 |
| 交替触发 | 交替触发转换 |

## DAC (数模转换器)

### 主要特性

| 特性 | 参数 |
|------|------|
| 分辨率 | 8位 或 12位 |
| 通道数 | 2 (DAC1_OUT = PA4, DAC2_OUT = PA5) |
| 转换时间 | 最快 1μs |
| 输出缓冲 | 可配置 (缓冲输出驱动能力强) |
| 波形生成 | 三角波、噪声 (无需 CPU 干预) |

### HAL DAC 函数

```c
DAC_HandleTypeDef hdac;

void MX_DAC_Init(void) {
    DAC_ChannelConfTypeDef sConfig = {0};

    __HAL_RCC_DAC_CLK_ENABLE();

    hdac.Instance = DAC;
    HAL_DAC_Init(&hdac);

    sConfig.DAC_Trigger = DAC_TRIGGER_NONE;     // 软件触发
    sConfig.DAC_OutputBuffer = DAC_OUTPUTBUFFER_ENABLE;
    HAL_DAC_ConfigChannel(&hdac, &sConfig, DAC_CHANNEL_1);
}
```

#### 设置 DAC 输出

```c
// 12位右对齐
HAL_DAC_SetValue(&hdac, DAC_CHANNEL_1, DAC_ALIGN_12B_R, 2048); // 1.65V

// 8位右对齐
HAL_DAC_SetValue(&hdac, DAC_CHANNEL_1, DAC_ALIGN_8B_R, 128);   // 1.65V

// 启动 DAC
HAL_DAC_Start(&hdac, DAC_CHANNEL_1);
```

#### DMA 方式 (波形生成)

```c
#define WAVE_SIZE 256
uint16_t sine_wave[WAVE_SIZE];

// 生成正弦波表
void gen_sine_wave(void) {
    for (int i = 0; i < WAVE_SIZE; i++) {
        sine_wave[i] = (uint16_t)(2048 + 2047 * sin(2 * M_PI * i / WAVE_SIZE));
    }
}

// 使用定时器触发 DMA 传输
HAL_DAC_Start_DMA(&hdac, DAC_CHANNEL_1, sine_wave, WAVE_SIZE, DAC_ALIGN_12B_R);
```

## 实际应用示例

### 1. 电位器读取与串口输出

```c
#include <stdio.h>

int main(void) {
    HAL_Init();
    SystemClock_Config();
    MX_USART2_UART_Init();  // 串口初始化
    MX_ADC1_Init();          // ADC 初始化 (PA0)

    char msg[64];

    while (1) {
        uint32_t adc_val = read_adc();
        float voltage = adc_to_voltage(adc_val);
        sprintf(msg, "ADC: %lu, Voltage: %.2fV\r\n", adc_val, voltage);
        HAL_UART_Transmit(&huart2, (uint8_t*)msg, strlen(msg), HAL_MAX_DELAY);
        HAL_Delay(500);
    }
}
```

### 2. 模拟信号输出 (正弦波发生器)

```c
// PA4 (DAC1_OUT) 输出正弦波, TIM6 触发 DAC

void generate_sine_wave_dma(void) {
    // 正弦波表 (128个采样点)
    uint16_t sine_table[128];
    for (int i = 0; i < 128; i++) {
        sine_table[i] = (uint16_t)(2048 + 2047 * sin(2 * M_PI * i / 128));
    }

    // 启动 DAC DMA (TIM6 触发更新)
    HAL_DAC_Start_DMA(&hdac, DAC_CHANNEL_1, sine_table, 128, DAC_ALIGN_12B_R);
    // 启动定时器触发
    HAL_TIM_Base_Start(&htim6);
    // 输出频率 = TIM6频率 / 128
}
```

### 3. ADC + DAC 音频回路

```c
// ADC 采集音频输入 → 处理后 DAC 输出
// 使用 DMA 双缓冲实现流水线处理
HAL_ADC_Start_DMA(&hadc1, adc_buffer, BUFFER_SIZE);
HAL_DAC_Start_DMA(&hdac, DAC_CHANNEL_1, dac_buffer, BUFFER_SIZE, DAC_ALIGN_12B_R);
```

## 常见问题

1. **ADC 值跳动**：增加采样时间、硬件滤波（RC 低通）、软件均值滤波
2. **DAC 输出不准确**：检查参考电压、输出缓冲是否启用
3. **DMA 传输不完整**：检查 DMA 配置、循环模式设置
4. **多通道顺序不对**：检查扫描顺序和通道等级配置

## 相关条目

- [[GPIO]]
- [[Timer]]
- [[Interrupt]]
- [[Communication]]
- [[AnalogCircuits]]
