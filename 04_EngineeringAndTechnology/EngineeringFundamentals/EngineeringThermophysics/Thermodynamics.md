# 工程热力学

## 定义
工程热力学是研究热能与机械能转换规律的学科。是能源动力工程的理论基础。

## 核心内容

### 基本概念

**热力系统**：研究对象的指定范围

**状态参数**：
- 温度 $T$、压力 $p$、比容 $v$
- 内能 $u$、焓 $h$、熵 $s$

**准静态过程**：系统始终无限接近平衡态

### 热力学第一定律

**闭口系统**：$Q = \Delta U + W$

**开口系统**：$Q = \Delta H + W_s + \Delta E_k + \Delta E_p$

**稳定流动**：$q = \Delta h + w_s$

### 理想气体

**状态方程**：$pv = RT$

**比热容**：
- 定容比热：$c_v = \frac{\partial u}{\partial T}|_v$
- 定压比热：$c_p = \frac{\partial h}{\partial T}|_p$

**理想气体过程**：

| 过程 | 过程方程 | 热量 $q$ | 功 $w$ | 内能变化 $\Delta u$ | 熵变 $\Delta s$ |
|------|---------|----------|--------|---------------------|-----------------|
| 等容 | $v = \text{const}$ | $c_v\Delta T$ | $0$ | $c_v\Delta T$ | $c_v\ln(T_2/T_1)$ |
| 等压 | $p = \text{const}$ | $c_p\Delta T$ | $p\Delta v$ | $c_v\Delta T$ | $c_p\ln(T_2/T_1)$ |
| 等温 | $pv = \text{const}$ | $RT\ln(v_2/v_1)$ | $RT\ln(v_2/v_1)$ | $0$ | $R\ln(v_2/v_1)$ |
| 绝热 | $pv^k = \text{const}$ | $0$ | $-\Delta u$ | $c_v\Delta T$ | $0$（可逆） |
| 多变 | $pv^n = \text{const}$ | $\frac{n-k}{n-1}c_v\Delta T$ | $\frac{R}{n-1}(T_1-T_2)$ | $c_v\Delta T$ | — |

其中绝热指数 $k = c_p/c_v$，多变指数 $n$ 可在 $-\infty$ 到 $+\infty$ 之间取值。

### 热力学第二定律

**克劳修斯表述**：热量不可能自发地从低温物体传向高温物体

**开尔文表述**：不可能从单一热源吸热使之完全变为功而不产生其他效果

**熵增原理**：$dS_{iso} \geq 0$

**卡诺循环效率**：

$$\eta_{Carnot} = 1-\frac{T_L}{T_H}$$

### 水蒸气

**水蒸气性质**：
- 饱和线：饱和液线、饱和气线
- 过热区、湿蒸汽区、过冷区

**水蒸气表**：饱和水蒸汽表、过热水蒸气表

### 湿空气

**湿度**：
- 绝对湿度：$\rho_v$
- 相对湿度：$\phi = \frac{p_v}{p_s}$
- 含湿量：$d = 0.622\frac{p_v}{p_B-p_v}$

**湿空气过程**：
- 加热/冷却
- 加湿/减湿
- 冷却去湿

### 热力循环

**朗肯循环**：蒸汽动力循环，由四个过程组成：
1. 等压加热（锅炉）
2. 绝热膨胀（汽轮机）
3. 等压放热（凝汽器）
4. 绝热压缩（给水泵）

效率：$\eta_{\text{Ran}} = \frac{w_{\text{net}}}{q_H} = 1 - \frac{h_4 - h_1}{h_3 - h_2}$

**制冷与热泵循环对比**：

| 循环类型 | 目的 | 性能系数 | 温度关系 |
|---------|------|---------|---------|
| 蒸气压缩制冷 | 从低温热源吸热 | $COP_R = \frac{q_L}{w_{\text{net}}} = \frac{h_1 - h_4}{h_2 - h_1}$ | $T_L < T_0 < T_H$ |
| 吸收式制冷 | 热能驱动制冷 | $COP = \frac{q_L}{q_G}$ | 需高温热源驱动 |
| 热泵（供热） | 向高温热源放热 | $COP_{HP} = \frac{q_H}{w_{\text{net}}} = \frac{h_2 - h_4}{h_2 - h_1}$ | $COP_{HP} = COP_R + 1$ |

**卡诺循环性能界限**：
- 卡诺热机：$\eta_{\text{Carnot}} = 1 - \frac{T_L}{T_H}$
- 卡诺制冷：$COP_{R,\text{Carnot}} = \frac{T_L}{T_H - T_L}$
- 卡诺热泵：$COP_{HP,\text{Carnot}} = \frac{T_H}{T_H - T_L}$

## 经典教材
- 曾丹苓《工程热力学》
- 沈维道《工程热力学》
- Cengel《Thermodynamics: An Engineering Approach》
- Moran《Fundamentals of Engineering Thermodynamics》

## 主要应用领域
- 火力发电
- 制冷空调
- 内燃机
- 航空发动机
- 化工过程
- 新能源系统
