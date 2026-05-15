# 高速PCB设计要点

## 一、高速信号的定义

当信号的上升时间小于传输延迟的2倍时，导线应视为传输线而非普通连线。

$$
\text{临界长度} > \frac{t_r}{2 \times t_{pd}}
$$

其中 $t_r$ 为信号上升时间，$t_{pd}$ 为传输延迟。

常见接口速率分类：

| 信号类型 | 速率范围 | 典型接口 | 设计难度 |
|----------|----------|----------|----------|
| 低速 | < 10MHz | I2C, GPIO | 低 |
| 中速 | 10-100MHz | SPI, SDRAM | 中 |
| 高速 | 100MHz-1GHz | DDR, USB 2.0 | 高 |
| 超高速 | > 1GHz | DDR4/5, PCIe, HDMI | 极高 |
| 射频 | > 1GHz | WiFi, 5G | 极高 |

## 二、传输线理论

PCB传输线类型：

```
微带线 (Microstrip):
    W    (顶层走线)
   ╔══╗
   ║  ║  ε_r   (介质)
   ╚══╝
   ██████████ (参考平面)

带状线 (Stripline):
   ██████████ (参考平面)
   ╔══╗
   ║  ║  ε_r
   ╚══╝
   ██████████ (参考平面)
```

特性阻抗计算：

$$
Z_{0, microstrip} = \frac{87}{\sqrt{\epsilon_r + 1.41}} \ln\left(\frac{5.98h}{0.8w + t}\right)
$$

$$
Z_{0, stripline} = \frac{60}{\sqrt{\epsilon_r}} \ln\left(\frac{4h}{0.67\pi w(0.8 + t/h)}\right)
$$

其中 h 为介质厚度，w 为线宽，t 为铜厚。

典型四层板叠层结构：

```
层1: 信号层 (Top)
     - 介质: 0.2mm
层2: 地层 (GND)
     - 芯板: 1.2mm
层3: 电源层 (Power)
     - 介质: 0.2mm
层4: 信号层 (Bottom)
```

## 三、阻抗控制

目标阻抗常用值：

| 接口 | 单端阻抗 | 差分阻抗 |
|------|----------|----------|
| USB 2.0/3.0 | - | 90 |
| HDMI | 50 | 100 |
| PCIe | - | 85/100 |
| DDR4 | 50/40 | 80/100 |
| Ethernet | 50 | 100 |
| SATA | - | 100 |
| RF (50) | 50 | - |

阻抗计算公式（四层板）：

微带线单端50欧姆近似：

$$
w \approx \frac{5.98h}{\exp\left(\frac{Z_0\sqrt{\epsilon_r + 1.41}}{87}\right) - 1}
$$

差分阻抗关系：

$$ Z_{diff} \approx 2Z_0\left(1 - 0.48e^{-0.96s/h}\right) $$

其中 s 为差分对间距，h 为介质厚度。

## 四、信号完整性

信号完整性问题与解决方案：

| 问题 | 原因 | 解决方法 |
|------|------|----------|
| 反射 | 阻抗不连续 | 端接匹配电阻 |
| 串扰 | 平行走线过长 | 3W规则、屏蔽 |
| 振铃 | 过冲/欠冲 | 阻尼电阻 |
| 地弹 | 多个信号同时翻转 | 解耦电容、地平面 |
| 时序偏差 | 走线不等长 | 等长蛇形绕线 |
| EMI | 高频辐射 | 屏蔽、滤波、布局优化 |

端接方式对比：

| 端接类型 | 拓扑 | 优点 | 缺点 |
|----------|------|------|------|
| 串联端接 | R_s(串) -> 负载 | 低功耗 | 仅点对点 |
| 并联端接 | R_p(到Vcc/GND)| 信号质量好 | 功耗大 |
| AC端接 | R+C串联到GND | 无直流功耗 | 占用空间 |
| 戴维南端接 | R1到Vcc+R2到GND | 双向匹配 | 功耗大 |
| 差分端接 | Rt跨接差分对 | 匹配精度高 | 仅差分信号 |

串联端接阻值计算：

$$ R_s = Z_0 - R_{driver} $$

## 五、电源完整性

电源分配网络（PDN）设计目标是将阻抗控制在目标值以下：

$$
Z_{target} = \frac{V_{dd} \times Ripple}{I_{transient}}
$$

去耦电容布局：

```python
def calc_decap_impedance(c, esl, f):
    """计算去耦电容在频率f下的阻抗"""
    import math
    Z = 1/(2*math.pi*f*c) + 2*math.pi*f*esl
    return Z

# 示例: 0.1uF电容 + 1nH ESL
freq = 100e6
z = calc_decap_impedance(0.1e-6, 1e-9, freq)
print(f"100MHz时阻抗: {z:.2f}欧姆")
```

去耦电容选型：

| 频率范围 | 电容值 | 封装 | 放置位置 | 数量 |
|----------|--------|------|----------|------|
| < 1MHz | 10-100uF | 1206/0805 | 电源入口 | 1-2/电源轨 |
| 1-100MHz | 0.1-1uF | 0805/0603 | IC附近 | 1/IC |
| > 100MHz | 10-100nF | 0402/0201 | IC引脚旁 | 多颗 |

## 六、布局布线规则

高速信号布局原则：

```
1. 关键的信号线优先布线
2. 保持参考平面连续（不跨分割）
3. 高速信号远离板边（> 5mm）
4. 差分对等长（误差 < 5mil）
5. 时钟信号包地处理
6. 模拟信号与数字信号分离
7. 发热器件远离温度敏感器件
```

3W规则：走线间距为线宽的3倍以减少串扰。

蛇形线等长绕线：

```python
def serpentine_length(straight, segments, amplitude):
    """计算蛇形线总长"""
    import math
    # 每段蛇形长度
    per_seg = 2 * math.sqrt((amplitude/2)**2 + (straight/segments)**2)
    return per_seg * segments
```

## 七、DDR布线指南

DDR4/DDR5走线约束：

| 信号组 | 等长约束 | 阻抗 | 参考层 |
|--------|----------|------|--------|
| 地址/命令 | +/- 50mil | 50 | VDD |
| 控制线 | +/- 25mil | 50 | VDD |
| 时钟 | +/- 10mil | 50差分 | GND |
| DQ/DM | +/- 10mil | 50 | GND |
| DQS | +/- 5mil | 50 | GND |

DDR4拓扑结构比较：

```
Fly-by拓扑（推荐）:
   控制器 -> 颗粒1 -> 颗粒2 -> 颗粒3 -> (终端电阻)
      50R       V        V        V      50R到VTT

T型拓扑（低频）:
           颗粒1
   控制器 ----> 颗粒2
           颗粒3
```

## 八、PCB制造工艺要求

常见工艺参数：

| 参数 | 常规 | 高精度 | 备注 |
|------|------|--------|------|
| 最小线宽/间距 | 6/6mil | 3/3mil | 1mil=0.0254mm |
| 最小孔径 | 0.3mm | 0.2mm | 机械钻孔 |
| 激光钻孔 | - | 0.1mm | HDI板 |
| 铜厚 | 1oz (35um) | 0.5-2oz | 外层 |
| 板厚 | 1.6mm | 0.4-3.2mm | FR4 |
| 阻焊桥 | > 0.1mm | > 0.05mm | 细间距 |
| 表面处理 | HASL | ENIG/OSP | - |

## 九、仿真与验证

信号完整性仿真流程：

```python
# Python使用PyEDA或scikit-rf进行S参数分析
import numpy as np

def compute_s21(s_params, freq):
    """计算S21传输参数（简化）"""
    return np.abs(s_params)  # 简化模型

# 眼图质量评估
def eye_opening(signal, ui_period):
    """计算眼张开度"""
    samples_per_ui = len(signal) // 20
    eye_amplitude = np.max(signal) - np.min(signal)
    return eye_amplitude  # 简化计算
```

PCB设计检查清单：

```
1. 原理图检查：网络连接、电源树、引脚分配
2. 布局检查：分区、散热、机械限制
3. 布线检查：阻抗、等长、3W规则
4. 电源检查：PDN阻抗、去耦电容
5. 信号检查：SI仿真、时序分析
6. 制造检查：DFM规则、拼板、Mark点
7. 装配检查：BOM、元件封装、焊盘设计
```

## 相关条目

- [[PCBDesign]]
- [[05_ComputerScience/HardwareAndEmbeddedSystems/DigitalCircuits/INDEX|DigitalCircuits]]
- SignalIntegrity
- [[FPGA]]
- [[EmbeddedLinux]]

## 参考资源

1. 《高速数字设计》Howard Johnson 著
2. 《信号完整性分析》Eric Bogatin 著
3. IPC-2221 PCB设计通用标准
4. Altium Designer高速PCB设计指南
5. Cadence Allegro约束管理器文档
6. Keysight ADS高速仿真教程
7. SI-List信号完整性邮件列表
