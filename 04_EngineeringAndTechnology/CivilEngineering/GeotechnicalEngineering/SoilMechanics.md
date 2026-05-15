---
aliases: [SoilMechanics]
tags: ['CivilEngineering', 'GeotechnicalEngineering', 'SoilMechanics']
---

# 土力学

## 定义
土力学是研究土的应力、变形、强度和稳定性以及土与结构物相互作用的学科。是地基基础工程的理论基础。

## 研究对象
- 土的物理性质
- 土中应力计算
- 土的渗透性
- 土的抗剪强度
- 土压力理论

## 核心内容

### 土的三相组成

**三相**：固相（土颗粒）、液相（水）、气相（空气）

**物理性质指标分类与定义**：

| 指标类型 | 指标符号 | 定义公式 | 物理意义 |
|---------|---------|---------|---------|
| 基本指标 | 含水量 $w$ | $w = \frac{m_w}{m_s} \times 100\%$ | 水质量与土颗粒质量之比 |
| 基本指标 | 密度 $\rho$ | $\rho = \frac{m}{V}$ | 单位体积土的质量 |
| 基本指标 | 土粒比重 $G_s$ | $G_s = \frac{m_s}{V_s \rho_w}$ | 土粒密度与水密度之比 |
| 导出指标 | 干密度 $\rho_d$ | $\rho_d = \frac{m_s}{V}$ | 单位体积干土的质量 |
| 导出指标 | 饱和密度 $\rho_{sat}$ | $\rho_{sat} = \frac{m_s + V_v \rho_w}{V}$ | 孔隙充满水时的密度 |
| 导出指标 | 有效密度 $\rho'$ | $\rho' = \rho_{sat} - \rho_w$ | 水下土的浮密度 |
| 导出指标 | 孔隙比 $e$ | $e = \frac{V_v}{V_s}$ | 孔隙体积与土粒体积之比 |
| 导出指标 | 孔隙率 $n$ | $n = \frac{V_v}{V} \times 100\%$ | 孔隙体积与总体积之比 |
| 导出指标 | 饱和度 $S_r$ | $S_r = \frac{V_w}{V_v} \times 100\%$ | 水体积与孔隙体积之比 |

**典型土的物理性质指标**：

| 土类 | 孔隙比 $e$ | 含水量 $w(\%)$ | 渗透系数 $k$ (cm/s) | 压缩性 |
|------|-----------|---------------|-------------------|--------|
| 碎石土 | $0.4 \sim 0.7$ | 小 | $10^{-1} \sim 10^{-2}$ | 低 |
| 砂土 | $0.3 \sim 0.9$ | $0 \sim 40$ | $10^{-2} \sim 10^{-5}$ | 低-中 |
| 粉土 | $0.6 \sim 1.1$ | $15 \sim 50$ | $10^{-5} \sim 10^{-7}$ | 中 |
| 粉质粘土 | $0.7 \sim 1.2$ | $20 \sim 60$ | $10^{-6} \sim 10^{-8}$ | 中-高 |
| 粘土 | $0.8 \sim 1.5$ | $30 \sim 80$ | $10^{-7} \sim 10^{-9}$ | 高 |

**指标换算**：

$$\rho_d = \frac{\rho}{1+w}, \quad \rho_{sat} = \frac{G_s+e}{1+e}\rho_w$$

### 土的渗透性

**达西定律**：

$$v = ki$$

$v$ 为渗透速度，$k$ 为渗透系数，$i$ 为水力梯度。

**渗透系数**：
- 砂土：$k = 10^{-2} \sim 10^{-3}$ cm/s
- 粘土：$k = 10^{-7} \sim 10^{-9}$ cm/s

**渗透力**：$j = i\gamma_w$（单位体积渗透力）

### 土中应力计算

**自重应力**：

$$\sigma_z = \sum \gamma_i h_i$$

**附加应力**（Boussinesq解）：

$$\sigma_z = \frac{3P}{2\pi z^2}\frac{1}{[1+(r/z)^2]^{5/2}}$$

**矩形均布荷载角点法**：$\sigma_z = K_c p$

$K_c$ 为角点应力系数。

### 土的抗剪强度

**库仑定律**：

$$\tau_f = c + \sigma\tan\varphi$$

$c$ 为粘聚力，$\varphi$ 为内摩擦角。

**莫尔圆**：

$$\left(\frac{\sigma_1-\sigma_3}{2}\right)^2 + \tau^2 = \left(\frac{\sigma_1+\sigma_3}{2}\right)^2$$

**抗剪强度试验方法对比**：

| 试验方法 | 排水条件 | 应力状态 | 强度指标 | 适用土类 | 优点 | 缺点 |
|---------|---------|---------|---------|---------|------|------|
| **直剪试验** | 快剪/固结快剪/慢剪 | 平面应变 | $c_d, \varphi_d$ | 各类土 | 设备简单，操作方便 | 排水条件不易控制，应力分布不均匀 |
| **三轴UU试验** | 不排水 | 轴对称 | $c_u, \varphi_u$ | 饱和粘土 | 严格控制排水条件 | 无法模拟实际工程排水条件 |
| **三轴CU试验** | 固结不排水 | 轴对称 | $c_{cu}, \varphi_{cu}$ | 饱和粘土 | 可测孔隙水压力 | 操作复杂，试验时间长 |
| **三轴CD试验** | 固结排水 | 轴对称 | $c', \varphi'$ | 各类土 | 得到有效应力强度指标 | 试验时间最长 |
| **十字板剪切** | 原位不排水 | — | $c_u$ | 饱和软粘土 | 原位测试，无取样扰动 | 仅适用于软粘土 |

**有效应力原理**：土的抗剪强度由有效应力决定：

$$\tau_f = c' + (\sigma - u)\tan\varphi' = c' + \sigma'\tan\varphi'$$

其中 $u$ 为孔隙水压力，$\sigma'$ 为有效应力。

### 地基承载力

**Terzaghi极限承载力公式**（条形基础）：
$$p_u = cN_c + \gamma D N_q + \frac{1}{2}\gamma B N_\gamma$$

其中承载力系数：
$$N_q = e^{\pi\tan\varphi}\tan^2\left(45^\circ+\frac{\varphi}{2}\right),\quad N_c = (N_q-1)\cot\varphi,\quad N_\gamma = 2(N_q+1)\tan\varphi$$

**地基容许承载力**：$p_a = p_u / F_s$，安全系数 $F_s = 2.5 \sim 3.0$

### 地基沉降计算

**分层总和法沉降量**：
$$S = \sum_{i=1}^n \frac{e_{1i} - e_{2i}}{1+e_{1i}} h_i = \sum_{i=1}^n \frac{a_i}{1+e_{1i}} \Delta p_i h_i$$

其中 $a_i$ 为压缩系数，$e_{1i}, e_{2i}$ 为压缩前后孔隙比。

**压缩指标**：
- 压缩系数：$a = \frac{e_1 - e_2}{p_2 - p_1}$（MPa⁻¹）
- 压缩模量：$E_s = \frac{1+e_1}{a}$（MPa）
- 压缩指数：$C_c = \frac{e_1 - e_2}{\log(p_2/p_1)}$

**土体压缩性分类**：

| 压缩性 | 压缩系数 $a_{1-2}$ (MPa⁻¹) | 压缩模量 $E_s$ (MPa) | 典型土类 |
|-------|--------------------------|--------------------|---------|
| 低压缩性 | $a < 0.1$ | $E_s > 15$ | 密实砂土、砾石 |
| 中压缩性 | $0.1 \leq a < 0.5$ | $4 < E_s \leq 15$ | 粉质粘土 |
| 高压缩性 | $a \geq 0.5$ | $E_s \leq 4$ | 软粘土、淤泥 |

### 土压力理论

**静止土压力**：

$$E_0 = \frac{1}{2}K_0\gamma H^2$$

$K_0 = 1-\sin\varphi$（经验公式）

**主动土压力（Rankine理论）**：

$$E_a = \frac{1}{2}\gamma H^2\tan^2\left(45°-\frac{\varphi}{2}\right) - 2cH\tan\left(45°-\frac{\varphi}{2}\right)$$

**被动土压力**：

$$E_p = \frac{1}{2}\gamma H^2\tan^2\left(45°+\frac{\varphi}{2}\right) + 2cH\tan\left(45°+\frac{\varphi}{2}\right)$$

**三种土压力理论对比**：

| 土压力类型 | 理论 | 发生条件 | 墙后填土状态 | 合力公式 | 特点 |
|-----------|------|---------|-------------|---------|------|
| **静止土压力** | 弹性理论 | 挡土墙静止不动 | 弹性平衡 | $E_0 = \frac{1}{2}K_0\gamma H^2$ | 与土的侧压力系数有关 |
| **主动土压力** | Rankine/Coulomb | 墙离开填土位移 | 主动极限平衡 | $E_a = \frac{1}{2}\gamma H^2 K_a$ | 位移量较小（约0.1%~0.5%H） |
| **被动土压力** | Rankine/Coulomb | 墙推向填土位移 | 被动极限平衡 | $E_p = \frac{1}{2}\gamma H^2 K_p$ | 位移量较大（约1%~5%H） |

**Rankine与Coulomb土压力理论对比**：

| 特性 | Rankine理论 | Coulomb理论 |
|------|------------|-------------|
| 假设条件 | 墙背竖直、光滑、填土水平 | 墙背倾斜、粗糙、填土倾斜 |
| 滑动面 | 平面（与水平成 $45^\circ+\varphi/2$） | 平面 |
| 适用范围 | 特定几何条件 | 一般挡土墙情况 |
| 粘聚力 $c$ | 可考虑 | 经典公式仅适用于无粘性土 |
| 土压力分布 | 三角形（无粘性土） | 三角形 |

**土压力系数**：

| 系数 | 主动 | 被动 | 静止 |
|------|------|------|------|
| 表达式 | $K_a = \tan^2\left(45^\circ-\frac{\varphi}{2}\right)$ | $K_p = \tan^2\left(45^\circ+\frac{\varphi}{2}\right)$ | $K_0 = 1 - \sin\varphi'$ |
| 大小关系 | $K_a < 1$ | $K_p > 1$ | $K_0 \approx 0.3 \sim 0.7$ |

**土压力关系**：$E_p > E_0 > E_a$，大小关系为：$K_p/K_a = \tan^4\left(45^\circ+\frac{\varphi}{2}\right)$

### 边坡稳定性

**瑞典圆弧法**（$\varphi=0$ 分析）：
$$F_s = \frac{\sum (c_i l_i + W_i \cos\alpha_i \tan\varphi_i)}{\sum W_i \sin\alpha_i}$$

**Bishop简化法**：
$$F_s = \frac{\sum \left[c_i b_i + (W_i - u_i b_i)\tan\varphi_i\right]/m_{\alpha i}}{\sum W_i \sin\alpha_i}$$
其中 $m_{\alpha i} = \cos\alpha_i + \sin\alpha_i\tan\varphi_i/F_s$

**边坡安全系数**：

| 边坡类型 | 临时边坡 | 永久边坡 |
|---------|---------|---------|
| 正常工况 | $F_s \geq 1.20$ | $F_s \geq 1.30$ |
| 地震工况 | $F_s \geq 1.10$ | $F_s \geq 1.15$ |

## 经典教材
- 龚晓南《土力学》
- 陈仲颐《土力学》
- Das《Principles of Geotechnical Engineering》
- Craig《Soil Mechanics》

## 主要应用领域
- 地基设计
- 基坑支护
- 边坡稳定
- 挡土墙设计
- 地下工程
- 地震工程（液化分析）

## 相关条目

- [[SoilMechanics]]
- [[FoundationEngineering]]
- RockMechanics
- [[02_NaturalSciences/EarthSciences/Geology/INDEX|Geology]]
