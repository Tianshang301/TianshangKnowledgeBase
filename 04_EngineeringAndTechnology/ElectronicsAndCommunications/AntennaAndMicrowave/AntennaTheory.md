# 天线理论

## 定义
天线理论是研究电磁波辐射与接收的基本理论、天线的设计方法和性能分析的学科。天线是无线通信系统中实现电磁波与导行波转换的关键器件。

## 研究对象
- 天线的基本参数
- 基本天线类型
- 天线阵列理论
- 天线测量方法

## 核心内容

### 天线参数

**方向性系数**：

$$D = \frac{4\pi U_{max}}{P_{rad}}$$

$U_{max}$ 为最大辐射强度，$P_{rad}$ 为总辐射功率。

**增益**：

$$G = \eta_r D$$

$\eta_r$ 为天线效率。通常用dB表示：$G_{dB} = 10\log_{10}G$。

**输入阻抗**：

$$Z_{in} = R_{in} + jX_{in}$$

匹配条件：$Z_{in} = Z_0$（通常50Ω）

**带宽**：
- 绝对带宽：$BW = f_H - f_L$
- 相对带宽：$FBW = \frac{f_H-f_L}{f_0} \times 100\%$

**极化**：线极化、圆极化、椭圆极化

**有效面积**：

$$A_e = \frac{\lambda^2}{4\pi}G$$

### 基本天线类型

**偶极子天线**：
- 半波偶极子：$l = \lambda/2$
- 输入阻抗：$Z_{in} = 73 + j42.5\Omega$
- 方向图：环形

**单极子天线**：
- 长度：$l = \lambda/4$
- 地面作为镜像
- 方向图：半空间

**八木天线**：
- 由一个有源振子、一个反射器和多个引向器组成
- 方向性强
- 增益：10~15dBi
- 应用：电视接收、业余无线电

**微带天线**：
- 贴片+介质基板+接地板
- 优点：低剖面、轻重量、易共形
- 缺点：带宽窄、效率较低
- 应用：GPS、手机、卫星通信

### 天线阵列

**阵因子（AF）**：

$$AF = \sum_{n=0}^{N-1} w_n e^{jnkd\cos\theta}$$

**均匀线阵**：

$$|AF| = \left|\frac{\sin(N\psi/2)}{\sin(\psi/2)}\right|$$

$\psi = kd\cos\theta + \beta$，$\beta$ 为相邻单元激励相位差。

**波束成形**：
- 通过控制各单元的幅度和相位
- 实现波束扫描和波束赋形
- 相控阵天线：电子波束扫描

**阵列综合**：
- 均匀幅度：副瓣高（-13.2dB）
- 切比雪夫分布：等副瓣
- 泰勒分布：副瓣递减

### MIMO天线

**MIMO系统**：

$$y = Hx + n$$

$H$ 为信道矩阵，$x$ 为发射信号，$n$ 为噪声。

**天线间距**：通常 $\geq \lambda/2$ 以保证空间相关性低

**天线设计要求**：
- 低相关性
- 高隔离度（>15dB）
- 紧凑尺寸
- 宽带特性

### 天线测量方法

**方向图测量**：
- 远场条件：$r > 2D^2/\lambda$
- 转台法：旋转天线测量方向图
- 紧缩场法：缩短测量距离

**增益测量**：
- 比较法：与标准天线比较
- 三天线法：消除增益不确定性

**阻抗测量**：
- 矢量网络分析仪（VNA）
- 回波损耗：$S_{11}(dB) = 20\log_{10}|\Gamma|$
- 驻波比：$VSWR = \frac{1+|\Gamma|}{1-|\Gamma|}$

## 经典教材
- 钟顺时《微带天线理论与工程》
- Balanis《Antenna Theory: Analysis and Design》
- Kraus《Antennas: For All Applications》
- Stutzman《Antenna Theory and Design》

## 主要应用领域
- 移动通信基站天线
- 卫星通信天线
- 雷达天线
- GPS/GNSS天线
- 物联网天线（RFID、LoRa）
- 汽车雷达天线

## 相关条目

- [[RF_Engineering]]
- [[MicrowaveEngineering]]
- [[WirelessCommunications]]
- [[02_NaturalSciences/Physics/Electromagnetism/INDEX|Electromagnetism]]
- [[CommunicationTheory]]
