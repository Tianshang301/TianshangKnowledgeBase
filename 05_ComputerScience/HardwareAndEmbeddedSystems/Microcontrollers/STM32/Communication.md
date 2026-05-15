---
aliases: [Communication]
tags: ['HardwareAndEmbeddedSystems', 'Microcontrollers', 'STM32', 'Communication']
---

# STM32 通信协议详解

## 通信协议对比

| 协议 | 类型 | 引脚数 | 速度 | 最大距离 | 拓扑 | 典型应用 |
|------|------|--------|------|----------|------|----------|
| UART | 异步串行 | 2 (TX/RX) | 最高 10 Mbps | ~15m@9600 | 点对点 | 调试、GPS、蓝牙 |
| I2C | 同步串行 | 2 (SCL/SDA) | 100/400/1000 kHz | ~1m | 多主多从 | 传感器、EEPROM |
| SPI | 同步串行 | 4 (SCK/MOSI/MISO/CS) | 最高 45 MHz | ~1m | 一主多从 | 显示屏、SD卡、ADC |
| CAN | 差分串行 | 2 (CAN_H/CAN_L) | 最高 1 Mbps | ~40m@1M ~1km@50k | 多主 | 汽车、工业控制 |

## USART/UART

### 基本特性

- 全双工异步串行通信
- 可配置数据位 (7/8/9)、停止位 (0.5/1/1.5/2)、校验位 (无/奇/偶)
- 支持同步模式 (USART)
- 支持硬件流控 (RTS/CTS)
- 支持 LIN、IrDA、SmartCard

### 波特率计算

```
USART 波特率 = USART_CLK / (16 * USARTDIV)
USARTDIV 是浮点数，由 BRR 寄存器设置
```

```c
// 配置 UART (115200-8-N-1)
UART_HandleTypeDef huart2;

void MX_USART2_UART_Init(void) {
    huart2.Instance = USART2;
    huart2.Init.BaudRate = 115200;
    huart2.Init.WordLength = UART_WORDLENGTH_8B;
    huart2.Init.StopBits = UART_STOPBITS_1;
    huart2.Init.Parity = UART_PARITY_NONE;
    huart2.Init.Mode = UART_MODE_TX_RX;
    huart2.Init.HwFlowCtl = UART_HWCONTROL_NONE;
    huart2.Init.OverSampling = UART_OVERSAMPLING_16;
    HAL_UART_Init(&huart2);
}
```

### HAL 数据收发

```c
// 阻塞发送
uint8_t data[] = "Hello STM32\r\n";
HAL_UART_Transmit(&huart2, data, sizeof(data), HAL_MAX_DELAY);

// 阻塞接收
uint8_t rx_byte;
HAL_UART_Receive(&huart2, &rx_byte, 1, 1000); // 超时 1s

// 中断接收
HAL_UART_Receive_IT(&huart2, &rx_byte, 1);

// DMA 发送
HAL_UART_Transmit_DMA(&huart2, tx_buffer, size);

// DMA 接收
HAL_UART_Receive_DMA(&huart2, rx_buffer, size);
```

### printf 重定向

```c
// 重定向 printf 到 USART2
int __io_putchar(int ch) {
    HAL_UART_Transmit(&huart2, (uint8_t*)&ch, 1, HAL_MAX_DELAY);
    return ch;
}

// 使用
printf("ADC Value: %lu\r\n", adc_value);
```

### 中断接收完整帧

```c
uint8_t rx_buffer[256];
uint16_t rx_index = 0;

void HAL_UART_RxCpltCallback(UART_HandleTypeDef *huart) {
    if (huart->Instance == USART2) {
        rx_buffer[rx_index++] = rx_byte;

        // 检测帧结束 (假设 \n 或 \r\n)
        if (rx_byte == '\n' || rx_index >= 256) {
            rx_buffer[rx_index] = '\0';
            process_command((char*)rx_buffer);
            rx_index = 0;
        }

        // 继续接收
        HAL_UART_Receive_IT(&huart2, &rx_byte, 1);
    }
}
```

## I2C

### 基本特性

- 两线制: SCL (时钟) + SDA (数据)
- 多主多从架构，地址冲突检测
- 7位或10位寻址
- 标准模式 (100kHz)、快速模式 (400kHz)、高速模式 (3.4MHz)

### I2C 时序

```
┌──────┐    ┌──────┐    ┌──────┐
      SCL   │      │    │      │    │
      ──┘      └──────┘      └──────
      SDA   ────    ──────────────────
            START  BIT7-1+W/R  ACK   STOP
```

### HAL I2C 函数

```c
I2C_HandleTypeDef hi2c1;

void MX_I2C1_Init(void) {
    hi2c1.Instance = I2C1;
    hi2c1.Init.ClockSpeed = 100000;        // 100kHz
    hi2c1.Init.DutyCycle = I2C_DUTYCYCLE_2;
    hi2c1.Init.OwnAddress1 = 0;
    hi2c1.Init.AddressingMode = I2C_ADDRESSINGMODE_7BIT;
    hi2c1.Init.DualAddressMode = I2C_DUALADDRESS_DISABLE;
    hi2c1.Init.OwnAddress2 = 0;
    hi2c1.Init.GeneralCallMode = I2C_GENERALCALL_DISABLE;
    hi2c1.Init.NoStretchMode = I2C_NOSTRETCH_DISABLE;
    HAL_I2C_Init(&hi2c1);
}
```

### EEPROM (AT24C02) 读写

```c
#define EEPROM_ADDR 0xA0   // AT24C02 设备地址

// 写入一个字节到指定地址
HAL_StatusTypeDef eeprom_write_byte(uint16_t mem_addr, uint8_t data) {
    return HAL_I2C_Mem_Write(&hi2c1, EEPROM_ADDR, mem_addr,
                             I2C_MEMADD_SIZE_8BIT, &data, 1, HAL_MAX_DELAY);
}

// 从指定地址读取一个字节
HAL_StatusTypeDef eeprom_read_byte(uint16_t mem_addr, uint8_t *data) {
    return HAL_I2C_Mem_Read(&hi2c1, EEPROM_ADDR, mem_addr,
                            I2C_MEMADD_SIZE_8BIT, data, 1, HAL_MAX_DELAY);
}

// 写入多个字节 (页写入)
HAL_StatusTypeDef eeprom_write_page(uint16_t mem_addr, uint8_t *data, uint16_t len) {
    return HAL_I2C_Mem_Write(&hi2c1, EEPROM_ADDR, mem_addr,
                             I2C_MEMADD_SIZE_8BIT, data, len, HAL_MAX_DELAY);
}
```

### I2C 传感器读取 (MPU6050)

```c
#define MPU6050_ADDR 0xD0

// 读取加速度数据
void mpu6050_read_accel(int16_t *ax, int16_t *ay, int16_t *az) {
    uint8_t buf[6];
    HAL_I2C_Mem_Read(&hi2c1, MPU6050_ADDR, 0x3B,
                     I2C_MEMADD_SIZE_8BIT, buf, 6, HAL_MAX_DELAY);
    *ax = (buf[0] << 8) | buf[1];
    *ay = (buf[2] << 8) | buf[3];
    *az = (buf[4] << 8) | buf[5];
}
```

## SPI

### 基本特性

- 四线制: SCK (时钟) + MOSI (主出从入) + MISO (主入从出) + CS (片选)
- 全双工同步通信
- 四种模式 (CPOL/CPHA 组合)

### SPI 模式

| 模式 | CPOL | CPHA | 时钟极性/相位 | 
|------|------|------|---------------|
| 0 | 0 | 0 | 空闲低，第一个边沿采样 |
| 1 | 0 | 1 | 空闲低，第二个边沿采样 |
| 2 | 1 | 0 | 空闲高，第一个边沿采样 |
| 3 | 1 | 1 | 空闲高，第二个边沿采样 |

### HAL SPI 函数

```c
SPI_HandleTypeDef hspi1;

void MX_SPI1_Init(void) {
    hspi1.Instance = SPI1;
    hspi1.Init.Mode = SPI_MODE_MASTER;
    hspi1.Init.Direction = SPI_DIRECTION_2LINES;
    hspi1.Init.DataSize = SPI_DATASIZE_8BIT;
    hspi1.Init.CLKPolarity = SPI_POLARITY_LOW;
    hspi1.Init.CLKPhase = SPI_PHASE_1EDGE;
    hspi1.Init.NSS = SPI_NSS_SOFT;
    hspi1.Init.BaudRatePrescaler = SPI_BAUDRATEPRESCALER_8;
    hspi1.Init.FirstBit = SPI_FIRSTBIT_MSB;
    hspi1.Init.TIMode = SPI_TIMODE_DISABLE;
    hspi1.Init.CRCCalculation = SPI_CRCCALCULATION_DISABLE;
    hspi1.Init.CRCPolynomial = 10;
    HAL_SPI_Init(&hspi1);
}
```

### 收发数据

```c
uint8_t tx_data[] = {0x01, 0x02, 0x03};
uint8_t rx_data[3];

// 全双工
HAL_SPI_TransmitReceive(&hspi1, tx_data, rx_data, 3, HAL_MAX_DELAY);

// 只发送
HAL_SPI_Transmit(&hspi1, tx_data, 3, HAL_MAX_DELAY);

// 只接收 (发送 dummy 字节)
HAL_SPI_Receive(&hspi1, rx_data, 3, HAL_MAX_DELAY);

// DMA 方式
HAL_SPI_TransmitReceive_DMA(&hspi1, tx_data, rx_data, 3);
```

### LCD 显示屏 (ST7789) 示例

```c
#define LCD_CS_LOW()    HAL_GPIO_WritePin(LCD_CS_PORT, LCD_CS_PIN, GPIO_PIN_RESET)
#define LCD_CS_HIGH()   HAL_GPIO_WritePin(LCD_CS_PORT, LCD_CS_PIN, GPIO_PIN_SET)
#define LCD_DC_HIGH()   HAL_GPIO_WritePin(LCD_DC_PORT, LCD_DC_PIN, GPIO_PIN_SET)
#define LCD_DC_LOW()    HAL_GPIO_WritePin(LCD_DC_PORT, LCD_DC_PIN, GPIO_PIN_RESET)
#define LCD_RST_LOW()   HAL_GPIO_WritePin(LCD_RST_PORT, LCD_RST_PIN, GPIO_PIN_RESET)
#define LCD_RST_HIGH()  HAL_GPIO_WritePin(LCD_RST_PORT, LCD_RST_PIN, GPIO_PIN_SET)

void lcd_write_cmd(uint8_t cmd) {
    LCD_DC_LOW();
    LCD_CS_LOW();
    HAL_SPI_Transmit(&hspi1, &cmd, 1, HAL_MAX_DELAY);
    LCD_CS_HIGH();
}

void lcd_write_data(uint8_t data) {
    LCD_DC_HIGH();
    LCD_CS_LOW();
    HAL_SPI_Transmit(&hspi1, &data, 1, HAL_MAX_DELAY);
    LCD_CS_HIGH();
}

void lcd_init(void) {
    LCD_RST_HIGH();
    HAL_Delay(10);
    LCD_RST_LOW();
    HAL_Delay(10);
    LCD_RST_HIGH();
    HAL_Delay(10);

    lcd_write_cmd(0x36); // MADCTL
    lcd_write_data(0x00);
    lcd_write_cmd(0x3A); // COLMOD
    lcd_write_data(0x05); // 16-bit color
    lcd_write_cmd(0x11); // SLPOUT
    HAL_Delay(120);
    lcd_write_cmd(0x29); // DISPON
}
```

### SD 卡 (SPI 模式)

使用 FatFs 文件系统库，底层通过 SPI 读写 SD 卡。

```c
// FatFs 底层 SPI 读写接口
DSTATUS disk_initialize(BYTE pdrv) {
    // SPI 初始化 + SD 卡初始化命令 (CMD0, CMD8, ACMD41...)
}

DRESULT disk_read(BYTE pdrv, BYTE *buff, LBA_t sector, UINT count) {
    // 发送 CMD17 (单块读) 或 CMD18 (多块读)
}

DRESULT disk_write(BYTE pdrv, const BYTE *buff, LBA_t sector, UINT count) {
    // 发送 CMD24 (单块写) 或 CMD25 (多块写)
}
```

## CAN (控制器局域网)

### 基本特性

- 差分信号: CAN_H 和 CAN_L
- 多主总线，基于消息优先级仲裁
- 错误检测和处理机制
- 最大 1 Mbps (40m)，低速可达 10km+

### STM32 bxCAN

STM32 的 bxCAN 支持：
- 标准帧 (11位标识符) 和扩展帧 (29位标识符)
- 多个发送/接收邮箱
- 可配置过滤器 (标识符掩码/列表模式)

### 基本配置

```c
CAN_HandleTypeDef hcan;

void MX_CAN_Init(void) {
    CAN_FilterTypeDef sFilterConfig = {0};

    hcan.Instance = CAN1;
    hcan.Init.Prescaler = 6;                     // 42MHz / 6 = 7MHz
    hcan.Init.Mode = CAN_MODE_NORMAL;             // 正常模式
    hcan.Init.SyncJumpWidth = CAN_SJW_1TQ;
    hcan.Init.TimeSeg1 = CAN_BS1_10TQ;             // 7MHz / (1+10+4) = 500kbps
    hcan.Init.TimeSeg2 = CAN_BS2_4TQ;
    hcan.Init.TimeTriggeredMode = DISABLE;
    hcan.Init.AutoBusOff = ENABLE;
    hcan.Init.AutoWakeUp = DISABLE;
    hcan.Init.AutoRetransmission = ENABLE;
    hcan.Init.ReceiveFifoLocked = DISABLE;
    hcan.Init.TransmitFifoPriority = DISABLE;
    HAL_CAN_Init(&hcan);

    // 过滤器配置: 接收所有 ID (掩码全为 0)
    sFilterConfig.FilterBank = 0;
    sFilterConfig.FilterMode = CAN_FILTERMODE_IDMASK;
    sFilterConfig.FilterScale = CAN_FILTERSCALE_32BIT;
    sFilterConfig.FilterIdHigh = 0;
    sFilterConfig.FilterIdLow = 0;
    sFilterConfig.FilterMaskIdHigh = 0;
    sFilterConfig.FilterMaskIdLow = 0;
    sFilterConfig.FilterFIFOAssignment = CAN_RX_FIFO0;
    sFilterConfig.FilterActivation = ENABLE;
    HAL_CAN_ConfigFilter(&hcan, &sFilterConfig);
}
```

### 发送与接收

```c
// CAN 发送
CAN_TxHeaderTypeDef tx_header;
uint8_t tx_data[8] = {0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08};
uint32_t tx_mailbox;

tx_header.StdId = 0x123;
tx_header.ExtId = 0;
tx_header.IDE = CAN_ID_STD;
tx_header.RTR = CAN_RTR_DATA;
tx_header.DLC = 8;
tx_header.TransmitGlobalTime = DISABLE;

HAL_CAN_AddTxMessage(&hcan, &tx_header, tx_data, &tx_mailbox);

// CAN 接收 (中断)
void HAL_CAN_RxFifo0MsgPendingCallback(CAN_HandleTypeDef *hcan) {
    CAN_RxHeaderTypeDef rx_header;
    uint8_t rx_data[8];

    HAL_CAN_GetRxMessage(hcan, CAN_RX_FIFO0, &rx_header, rx_data);

    printf("CAN ID: 0x%03lX, DLC: %d\r\n", rx_header.StdId, rx_header.DLC);
    for (int i = 0; i < rx_header.DLC; i++) {
        printf("0x%02X ", rx_data[i]);
    }
    printf("\r\n");
}
```

## 总结

- **UART**: 简单、点对点、调试首选
- **I2C**: 引脚少、多从机、适合传感器总线
- **SPI**: 高速、全双工、适合大数据量传输
- **CAN**: 高可靠性、远距离、工业/汽车标准

根据项目需求选择合适的通信协议，考虑速度、距离、可靠性、引脚资源和功耗等因素。
