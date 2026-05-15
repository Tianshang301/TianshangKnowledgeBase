---
aliases: [Econometrics]
tags: ['Economics', 'Econometrics', 'Econometrics']
---

# 计量经济学

## 一、经典线性回归模型

### 1.1 模型设定与OLS

经典线性回归模型（CLRM）：$Y_i = \beta_0 + \beta_1 X_{1i} + \beta_2 X_{2i} + \cdots + \beta_k X_{ki} + u_i$

矩阵形式：$\mathbf{Y} = \mathbf{X}\boldsymbol{\beta} + \mathbf{u}$

**OLS估计量**：$\hat{\boldsymbol{\beta}} = (\mathbf{X}'\mathbf{X})^{-1}\mathbf{X}'\mathbf{Y}$

OLS的直观含义：最小化残差平方和$\sum \hat{u}_i^2$。

### 1.2 高斯-马尔可夫假定与定理

| 假定 | 内容 | 违反后果 |
|------|------|----------|
| **MLR.1** 线性于参数 | 模型参数线性 | 设定偏误 |
| **MLR.2** 随机抽样 | 样本i.i.d. | 估计不一致 |
| **MLR.3** 零条件均值 | $E(u|X)=0$ | 有偏/不一致（内生性） |
| **MLR.4** 无完全共线性 | $X$矩阵满秩 | 无法估计 |
| **MLR.5** 同方差性（可选） | $Var(u|X)=\sigma^2$ | 标准误有偏（异方差） |
| **MLR.6** 正态性（可选） | $u|X \sim N(0,\sigma^2)$ | t/F检验小样本下不精确 |

**高斯-马尔可夫定理**：在MLR.1-MLR.5下，OLS是最优线性无偏估计量（BLUE）。

### 1.3 OLS的代数性质

- 残差均值为零：$\sum \hat{u}_i = 0$
- 残差与自变量正交：$\sum X_{ij}\hat{u}_i = 0$
- 拟合值与残差正交：$\sum \hat{Y}_i\hat{u}_i = 0$
- 回归线通过样本均值点：$(\bar{X}_1,\bar{X}_2,...,\bar{Y})$

## 二、模型诊断与选择

### 2.1 拟合优度

**R²**：$R^2 = 1 - \frac{SSR}{SST} = \frac{SSE}{SST}$。解释被解释变量变异中被模型解释的比例。问题：增加解释变量必然提高R²。

**调整R²**：$\bar{R}^2 = 1 - \frac{SSR/(n-k-1)}{SST/(n-1)}$。惩罚增加变量个数，用于嵌套模型比较。

### 2.2 信息准则

| 准则 | 公式 | 惩罚 | 倾向 |
|------|------|------|------|
| AIC | $n\ln(SSR/n) + 2k$ | 每加一变量+2 | 选更复杂模型 |
| BIC | $n\ln(SSR/n) + k\ln n$ | 每加一变量$+\ln n$ | 选更简洁模型 |
| 交叉验证 | 样本外预测误差 | 数据驱动 | 避免过拟合 |

### 2.3 假设检验

**单个系数t检验**：$t = \frac{\hat{\beta}_j}{se(\hat{\beta}_j)} \sim t_{n-k-1}$。**联合F检验**：$F = \frac{(SSR_r - SSR_{ur})/q}{SSR_{ur}/(n-k-1)} \sim F_{q, n-k-1}$。

## 三、异方差与自相关

### 3.1 异方差

**后果**：OLS仍无偏一致，但标准误有偏，t/F检验无效。

**检测方法**：
- **布罗施-帕甘检验**（BP）：残差平方对解释变量回归，$LM = nR^2 \sim \chi^2_k$
- **怀特检验**（White）：残差平方对解释变量、平方项和交叉项回归，更一般

**补救**：异方差稳健标准误（White/Huber标准误）——最常用，无需指定方差形式。WLS——需已知方差函数形式。

### 3.2 自相关

**后果**：OLS无偏但非有效，标准误有偏。

**检测**：Durbin-Watson检验——$DW \approx 2(1-\hat{\rho})$，接近2无自相关。BG检验（Breusch-Godfrey）适用于高阶自相关。

**补救**：Newey-West标准误（HAC标准误，异方差自相关一致）、广义最小二乘法（GLS，需已知自相关结构）、一阶差分（$\rho=1$时）。

## 四、内生性与工具变量

### 4.1 内生性来源

| 来源 | 说明 | 例子 |
|------|------|------|
| **遗漏变量** | 遗漏与解释变量相关的变量 | 能力影响教育和工作表现 |
| **测量误差** | 解释变量测量有误差 | 自报收入 vs 实际收入 |
| **反向因果** | Y影响X | 警察数量和犯罪率互为因果 |
| **选择偏差** | 样本非随机 | 只观察就业者的工资方程 |

### 4.2 工具变量法

**工具变量条件**：相关性$Cov(Z,X) \neq 0$ + 外生性$Cov(Z,u)=0$。

**两阶段最小二乘（2SLS）**：
- 第一阶段：$X = \pi Z + v$，得$\hat{X}$
- 第二阶段：$Y = \beta \hat{X} + \varepsilon$

**工具变量检验**：

| 检验 | 原假设 | 统计量 | 判断 |
|------|--------|--------|------|
| 弱工具变量检验 | 工具与内生变量弱相关 | 第一阶段F>10 | 弱工具使估计有偏 |
| 过度识别检验 | 所有工具外生 | Sargan/Hansen J | p>0.05接受 |
| 外生性检验 | 变量外生 | Hausman/DWH检验 | 显著则需IV |

### 4.3 常见IV应用

Angrist & Krueger（1991）：出生季度作为教育年限的工具变量——利用义务教育法产生的入学年龄差异。Acemoglu et al.（2001）：殖民者死亡率作为制度的工具变量。

## 五、面板数据

### 5.1 面板数据优势

控制不可观测的个体异质性、提供更多信息和变异、便于研究动态关系、可控制某些内生性问题。

### 5.2 面板模型

| 模型 | 对$\alpha_i$的假设 | 估计方法 | 一致性条件 |
|------|-------------------|----------|-----------|
| **混合OLS** | 无个体效应 | OLS | 需$Cov(\alpha_i,X)=0$ |
| **固定效应（FE）** | 与$X$相关 | 组内变换/LSDV | $E(u_{it}|X_i,\alpha_i)=0$ |
| **随机效应（RE）** | 与$X$不相关 | GLS | $Cov(\alpha_i,X)=0$ |
| **一阶差分（FD）** | 与$X$相关 | $\Delta Y=\beta\Delta X+\Delta u$ | 严格外生或弱外生 |

**豪斯曼检验**：$H_0$：RE一致且有效，$H_1$：RE不一致。拒绝$H_0$则用FE。

**聚类标准误**：面板数据标准误应在个体层面聚类，允许组内序列相关和异方差。

## 六、时间序列

### 6.1 平稳性与单位根

序列$Y_t$弱平稳的条件：$E[Y_t]=\mu$、$Var(Y_t)=\sigma^2$、$Cov(Y_t,Y_{t-k})=\gamma_k$——均与时间$t$无关。

**单位根检验**：
- ADF检验：$H_0$：有单位根（非平稳）
- KPSS检验：$H_0$：平稳（与ADF相反）

### 6.2 ARIMA模型

| 模型 | 数学形式 | 适用 |
|------|----------|------|
| AR(p) | $Y_t = c + \phi_1 Y_{t-1} + \cdots + \phi_p Y_{t-p} + u_t$ | 自回归过程 |
| MA(q) | $Y_t = c + u_t + \theta_1 u_{t-1} + \cdots + \theta_q u_{t-q}$ | 移动平均过程 |
| ARMA(p,q) | 两者结合 | 平稳时间序列 |
| ARIMA(p,d,q) | 对$Y_t$差分d次后为ARMA | 非平稳序列 |
| SARIMA | 加入季节成分 | 季节数据 |

**Box-Jenkins方法**：识别（判断p,d,q）→估计→诊断→预测。

### 6.3 协整与ECM

**协整**：两个$I(1)$变量的线性组合为$I(0)$，存在长期均衡关系。**误差修正模型（ECM）**：$\Delta y_t = \alpha + \beta \Delta x_t + \gamma(y_{t-1} - \theta x_{t-1}) + u_t$——将短期波动和长期均衡结合。

## 七、离散选择与因果推断

### 7.1 Probit与Logit

$P(Y=1|X) = F(\beta_0 + \beta_1 X_1 + \cdots + \beta_k X_k)$

| 模型 | 函数形式 | 尾部 |
|------|----------|------|
| Logit | $\Lambda(z) = e^z/(1+e^z)$ | 稍厚尾 |
| Probit | $\Phi(z)$ 标准正态CDF | 稍薄尾 |

系数方向一致，数值相差约1.6倍（Logit≈1.6×Probit）。**边际效应**：连续变量$\partial P/\partial X_j = f(X\beta)\beta_j$。

### 7.2 因果推断方法

| 方法 | 关键假设 | 应用场景 |
|------|----------|----------|
| DID | 平行趋势 | 政策前后比较 |
| RDD | 断点处连续性 | 阈值附近的政策效果 |
| 倾向得分匹配 | 可忽略性（unconfoundedness） | 处理选择偏差 |
| 合成控制法 | 对照组加权拟合处理组 | 单个处理单元评估 |
| 事件研究法 | 无预期效应 | 事件对股价影响 |

## 相关条目

[[Statistics]] · Mathematics/ProbabilityStatistics · [[07_InterdisciplinarySciences/DataScience/INDEX|DataScience]] · [[AppliedEconomics]]

## 参考资源

1. 伍德里奇《计量经济学导论：现代观点》，中国人民大学出版社
2. 斯托克、沃森《计量经济学》，格致出版社
3. 格林《计量经济分析》，中国人民大学出版社
4. 安格里斯特、皮施克《基本无害的计量经济学》，格致出版社
5. Wooldridge, J.M. *Econometric Analysis of Cross Section and Panel Data*, MIT Press
6. Hamilton, J.D. *Time Series Analysis*, Princeton University Press
7. 陈强《高级计量经济学及Stata应用》，高等教育出版社
8. Angrist & Pischke *Mostly Harmless Econometrics*, Princeton University Press
