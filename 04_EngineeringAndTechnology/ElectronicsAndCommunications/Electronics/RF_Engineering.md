# 射频工程

## 定义
射频工程是研究射频（RF）和微波频段（通常300kHz~300GHz）信号的产生、传输、放大、变换和测量的工程技术学科。

## 研究对象
- 传输线理论与阻抗匹配
- 射频电路设计（放大器、振荡器、混频器）
- 射频滤波器设计
- 射频系统性能指标

## 核心内容

### 传输线理论

**传输线方程**：

$$\frac{\partial V}{\partial z} = -(R+j\omega L)I$$
$$\frac{\partial I}{\partial z} = -(G+j\omega C)V$$

**特性阻抗**：

$$Z_0 = \sqrt{\frac{R+j\omega L}{G+j\omega C}}$$

无损传输线：$Z_0 = \sqrt{L/C}$

**反射系数**：

$$\Gamma = \frac{Z_L - Z_0}{Z_L + Z_0}$$

- $Z_L = Z_0$：匹配，无反射
- $Z_L = \infty$：开路，$\Gamma = 1$
- $Z_L = 0$：短路，$\Gamma = -1$

**驻波比（VSWR）**：

$$VSWR = \frac{1+|\Gamma|}{1-|\Gamma|}$$

**输入阻抗**：

$$Z_{in} = Z_0\frac{Z_L+jZ_0\tan(\beta l)}{Z_0+jZ_L\tan(\beta l)}$$

### Smith圆图

**阻抗归一化**：$z = Z/Z_0$

**Smith圆图组成**：
- 等电阻圆：圆心在实轴上
- 等电抗圆：圆心在虚轴上
- 等反射系数圆：圆心在原点

**应用**：
- 阻抗匹配网络设计
- 稳定性分析
- 增益圆和噪声圆
- 窄带和宽带匹配

### 射频放大器设计

**稳定性判据**：
- Rollett稳定性因子：

$$K = \frac{1-|S_{11}|^2-|S_{22}|^2+|\Delta|^2}{2|S_{12}||S_{21}|}$$

- 无条件稳定：$K>1$ 且 $|\Delta|<1$

**增益**：
- 转换增益：$G_T = \frac{P_{L}}{P_{avs}}$
- 最大可用增益（MAG）：$MAG = \frac{|S_{21}|}{|S_{12}|}(K-\sqrt{K^2-1})$
- 最大稳定增益（MSG）：$MSG = \frac{|S_{21}|}{|S_{12}|}$

**噪声系数**：

$$F = F_{min} + \frac{4R_n}{Z_0}\cdot\frac{|\Gamma_s-\Gamma_{opt}|^2}{(1-|\Gamma_s|^2)|1+\Gamma_{opt}|^2}$$

### 振荡器

**LC振荡器**：
- 哈特莱振荡器：电感分压反馈
- 科尔匹兹振荡器：电容分压反馈
- 振荡条件：环路增益 $|A\beta| \geq 1$，相位 $\angle A\beta = 0°$

**晶体振荡器**：
- 石英晶体谐振器：频率稳定度高
- 品质因数Q：可达$10^4 \sim 10^6$
- 频率稳定度：$10^{-6} \sim 10^{-8}$

**VCO（压控振荡器）**：
- 输出频率随控制电压变化
- 线性度、调谐范围、相位噪声

### 混频器

**功能**：实现频率变换 $f_{IF} = |f_{RF} \pm f_{LO}|$

**混频器类型**：
- 无源混频器（二极管混频器）：无增益，线性度好
- 有源混频器（晶体管混频器）：有增益，噪声较高

**性能指标**：
- 变频损耗/增益
- 噪声系数
- 线性度（IIP3、P1dB）
- 端口隔离度

### 滤波器设计

**滤波器类型**：
- 低通滤波器（LPF）
- 高通滤波器（HPF）
- 带通滤波器（BPF）
- 带阻滤波器（BSF）

**滤波器逼近函数**：
- 巴特沃斯（最大平坦）
- 切比雪夫（等纹波）
- 椭圆函数（最陡峭）

**微带滤波器**：
- 低通原型→微带实现
- 阶梯阻抗滤波器
- 耦合线滤波器

### 射频系统指标

**噪声系数**：

$$F = \frac{SNR_{in}}{SNR_{out}}$$

级联系统噪声系数：

$$F_{total} = F_1 + \frac{F_2-1}{G_1} + \frac{F_3-1}{G_1G_2} + \cdots$$

**增益**：$G(dB) = 10\log_{10}(P_{out}/P_{in})$

**线性度**：
- 1dB压缩点（P1dB）：增益压缩1dB时的输入功率
- 三阶交调截点（IIP3）：三阶交调产物与基波功率相等时的输入功率
- 动态范围：$DR = \frac{2}{3}(IIP3(dBm)-NF(dB)-P_{in,min}(dBm))$

## 经典教材
- 雷振亚《射频电路设计》
- Pozar《Microwave Engineering》
- Gonzalez《Microwave Transistor Amplifiers》
- Ludwig《RF Circuit Design: Theory and Applications》

## 主要应用领域
- 移动通信（手机射频前端）
- 雷达系统
- 卫星通信
- 物联网（RFID、Zigbee）
- 汽车雷达（77GHz）
- 医疗电子（微波热疗）

## 相关条目

- [[AntennaTheory]]
- [[MicrowaveEngineering]]
- [[WirelessCommunications]]
- [[CommunicationTheory]]
- [[AnalogElectronics]]
