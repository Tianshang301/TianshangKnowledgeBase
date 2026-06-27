---
aliases: [EngineeringEconomics]
tags: ['EngineeringFundamentals', 'EngineeringEconomics.md']
created: 2026-05-17
updated: 2026-05-17
---

---
aliases: [EngineeringEconomics]
tags: ['04_EngineeringAndTechnology', 'EngineeringFundamentals']
---

# 工程经济学 (Engineering Economics)

## 一、概述

工程经济学 (Engineering Economics) 是运用经济学原理和方法评估工程技术方案经济效益的学科。
核心任务是帮助工程师在有限资源条件下做出最优技术决策。
涉及资金时间价值 (Time Value of Money)、投资评价方法 (Investment Evaluation)、成本效益分析 (Cost-Benefit Analysis)、风险分析 (Risk Analysis) 和不确定性决策 (Decision Under Uncertainty) 等内容。
工程经济分析贯穿项目全生命周期 (Project Life Cycle)——从可行性研究 (Feasibility Study)、初步设计、详细设计到施工运营 (Operation) 和维护 (Maintenance)。
MARR (Minimum Attractive Rate of Return, 最低期望收益率) 是工程经济分析的核心基准参数。

## 二、资金的时间价值 (Time Value of Money)

### 2.1 复利与终值 (Compound Interest & Future Value)

$$F = P(1+i)^n$$

$F$ 为终值 (Future Value)，$P$ 为现值 (Present Value)，$i$ 为折现率 (Discount Rate)，$n$ 为期数。

**有效年利率 (EAR, Effective Annual Rate)**：
$$i_{eff} = \left(1 + \frac{r}{m}\right)^m - 1$$

$r$ 为名义年利率 (Nominal Annual Rate)，$m$ 为年计息次数 (Compounding Periods)。连续复利 (Continuous Compounding) 时 $i_{eff} = e^r - 1$。

### 2.2 现值与折现 (Present Value & Discounting)

$$P = \frac{F}{(1+i)^n} = F(1+i)^{-n}$$

折现率越高，远期现金流量的现值越低。折现率反映了资金的机会成本 (Opportunity Cost) 和风险溢价 (Risk Premium)。

### 2.3 年金公式 (Annuity Formulas)

| 名称 | 已知 | 求 | 公式 |
|------|------|-----|------|
| 年金终值 (F/A) | $A$ | $F$ | $F = A \cdot \frac{(1+i)^n - 1}{i}$ |
| 偿债基金 (A/F) | $F$ | $A$ | $A = F \cdot \frac{i}{(1+i)^n - 1}$ |
| 年金现值 (P/A) | $A$ | $P$ | $P = A \cdot \frac{(1+i)^n - 1}{i(1+i)^n}$ |
| 资金回收 (A/P) | $P$ | $A$ | $A = P \cdot \frac{i(1+i)^n}{(1+i)^n - 1}$ |

**永续年金 (Perpetuity)**：
$$P = \frac{A}{i}$$

**增长永续年金 (Growing Perpetuity)**：
$$P = \frac{A_1}{i - g} \quad (i > g)$$

$g$ 为年增长率，此公式在公司估值 (Gordon Growth Model) 中常用。

### 2.4 梯度系列 (Gradient Series)

**等差梯度 (Arithmetic Gradient)**：每期递增固定金额 $G$。

$$P = G \cdot \frac{(1+i)^n - in - 1}{i^2(1+i)^n}$$

**等比梯度 (Geometric Gradient)**：每期按比例 $g$ 递增。

$$P = A_1 \cdot \frac{1 - (1+g)^n (1+i)^{-n}}{i - g} \quad (i \neq g)$$

## 三、投资评价方法 (Investment Evaluation Methods)

### 3.1 净现值法 (NPV, Net Present Value)

$$NPV = \sum_{t=0}^n \frac{CF_t}{(1+MARR)^t}$$

$CF_t$ 为第 $t$ 年净现金流量 (Net Cash Flow)，$MARR$ 为最低期望收益率 (Minimum Attractive Rate of Return)。MARR 通常取为加权平均资本成本 (WACC, Weighted Average Cost of Capital) + 风险溢价。

**决策准则**：$NPV > 0$ 可行。多个独立方案选择 $NPV$ 最大者 (在预算约束下)。

### 3.2 内部收益率法 (IRR, Internal Rate of Return)

使 $NPV=0$ 的折现率：

$$0 = \sum_{t=0}^n \frac{CF_t}{(1+IRR)^t}$$

**决策准则**：$IRR > MARR$ 可行。互斥方案需用增量内部收益率 $\Delta IRR$ 比较 (Incremental Analysis)。
IRR 的局限性：非常规现金流 (Non-Conventional Cash Flow) 可能出现多解或无解 (多个 IRR 或不存在 IRR)。

### 3.3 投资回收期 (Payback Period)

**静态回收期 (Simple Payback Period)**：累计现金流量由负转正的时间，忽略资金时间价值。

**动态回收期 (Discounted Payback Period)**：考虑折现后的累计现金流转正时间。动态回收期通常长于静态回收期。

### 3.4 效益成本比 (B/C Ratio, Benefit-Cost Ratio)

$$B/C = \frac{\text{效益现值 (Present Value of Benefits)}}{\text{成本现值 (Present Value of Costs)}}$$

**决策准则**：$B/C \geq 1$ 可行。B/C 法适用于公共项目 (Public Project) 和基础设施项目的社会效益评估。

### 3.5 年值法 (AW, Annual Worth)

$$AW = NPV \cdot \frac{i(1+i)^n}{(1+i)^n - 1}$$ (即 A/P 系数)

适合寿命期不同 (Unequal Lives) 的方案比较。选择 $AW$ 最大者。

## 四、成本类型与估算

| 成本类型 | 定义 | 工程示例 |
|---------|------|---------|
| 固定成本 FC (Fixed Cost) | 不随产量变化 | 厂房折旧、管理人员工资 |
| 可变成本 VC (Variable Cost) | 随产量成正比 | 原材料、直接人工 |
| 直接成本 (Direct Cost) | 可直接归集到产品 | 材料费、人工费 |
| 间接成本 (Indirect Cost / Overhead) | 需分摊 | 水电费、维护费 |
| 沉没成本 (Sunk Cost) | 已发生不可回收 | 前期研发投入 |
| 机会成本 (Opportunity Cost) | 放弃次优方案的收益 | 资金用于 A 而非 B |
| 边际成本 MC (Marginal Cost) | 增加一单位产量的额外成本 | $\Delta TC / \Delta Q$ |

**学习曲线 (Learning Curve / Experience Curve)**：
$$C_n = C_1 \cdot n^{-b}$$

$C_1$ 为第一件成本，$n$ 为累计产量 (Cumulative Production)，$b = \log(LR)/\log 2$，$LR$ 为学习率 (Learning Rate)。学习率 80% 意味着累计产量翻倍时成本降至原 80%。

## 五、折旧与税收 (Depreciation & Tax)

**直线折旧 (Straight Line, SL)**：
$$D_k = \frac{P - S}{n}$$

$P$ 为原值，$S$ 为残值 (Salvage Value)，$n$ 为折旧年限。

**双倍余额递减法 (Double Declining Balance, DDB)**：
$$D_k = \frac{2}{n} \cdot B_{k-1}$$ ($B_{k-1}$ 为第 $k-1$ 年末账面值)

**年数总和法 (Sum-of-Years' Digits, SYD)**：
$$D_k = \frac{n - k + 1}{n(n+1)/2} \cdot (P - S)$$

**税后现金流 (ATCF, After-Tax Cash Flow)**：
$$ATCF = (收入 - 运营费用 - 折旧) \times (1 - T) + 折旧 - 投资$$

$T$ 为企业所得税率 (中国标准 25%，高新企业 15%)。折旧的"税盾"效应 (Tax Shield)：折旧费用减少应税收入，增加税后现金流。

## 六、盈亏平衡分析 (Break-Even Analysis)

$$Q^* = \frac{FC}{P - VC_{unit}}$$

$P$ 为单价，$VC_{unit}$ 为单位可变成本，$Q^*$ 为盈亏平衡点产量 (Break-Even Quantity)。

**安全边际 (Margin of Safety)**：
$$MS\% = \frac{Q_{actual} - Q^*}{Q_{actual}} \times 100\%$$

**经营杠杆 (DOL, Degree of Operating Leverage)**：
$$DOL = \frac{Q(P - VC)}{Q(P - VC) - FC}$$

高固定成本行业 (如航空、制造) DOL 高，收入波动对利润影响大。

## 七、敏感性分析 (Sensitivity Analysis)

**单因素敏感性分析 (One-at-a-Time Sensitivity)**：逐一改变参数，观察 $NPV$ 变化。

**敏感性系数 (Sensitivity Coefficient)**：
$$\beta_i = \frac{\Delta NPV / NPV}{\Delta x_i / x_i}$$

$\beta$ 越大，该参数对项目价值影响越大。

**蒙特卡洛模拟 (Monte Carlo Simulation)**：对关键参数 (收入、成本、折现率) 的概率分布随机抽样 10,000+ 次，统计得到 $NPV$ 的概率分布、期望值、标准差和 VaR (Value at Risk, 在险价值)。

## 八、不确定性决策 (Decision Under Uncertainty)

| 准则 | 决策方法 | 适用心理 |
|------|---------|---------|
| 期望值准则 (Expected Value) | $\max E[NPV]$ | 风险中性 (Risk Neutral) |
| Maximin (最大最小) | $\max \min V_{ij}$ | 保守/悲观 (Conservative) |
| Maximax (最大最大) | $\max \max V_{ij}$ | 激进/乐观 (Aggressive) |
| Minimax Regret (最小最大后悔) | $\min \max R_{ij}$ | 风险规避 (Risk Averse) |
| Laplace (拉普拉斯) | 等可能假设 | 无信息 (Ignorance) |

**决策树 (Decision Tree)** 用于多阶段决策 (Multi-Stage Decision)：
- 决策节点 (□, Decision Node)：方案选择
- 概率节点 (○, Chance Node)：自然状态及概率
- 终节点 (Terminal Node)：收益值

## 九、公共项目评价 (Public Project Evaluation)

**社会折现率 (Social Discount Rate)**：中国 8%，国际 3%-7%。低于私人项目折现率 (反映社会时间偏好)。

**无形效益量化 (Intangible Benefits)**：
- 生命价值 VSL (Value of Statistical Life)：中国约 500-800 万元
- 时间价值 VOT (Value of Time)：按人均 GDP 折算
- 环境效益：旅行成本法 (TCM, Travel Cost Method)、条件估值法 (CVM, Contingent Valuation Method)

**CBA 成本效益分析步骤 (Cost-Benefit Analysis)**：
1. 识别项目成本和效益 (包括外部性, Externalities)
2. 货币化所有影响 (Monetization)
3. 折现到同一时间基准
4. 计算 NPV/B/C 等指标
5. 敏感性分析检验稳健性

## 十、通货膨胀 (Inflation)

**Fisher 方程 (Fisher Equation)**：
$$i_{real} = \frac{1 + i_{nominal}}{1 + f} - 1 \approx i_{nominal} - f$$

$f$ 为通货膨胀率 (Inflation Rate)。常价分析 (Constant Dollar Analysis) 用实际利率 (Real Interest Rate)。时价分析 (Current Dollar Analysis) 用名义利率 (Nominal Interest Rate)。两种方法应得到一致的 NPV 结论。

## 十一、置换与更新分析 (Replacement Analysis)

**经济寿命 (Economic Life)**：使年值成本 (EAC, Equivalent Annual Cost) 最小的服役年限。

**边际成本法 (Marginal Cost Approach)**：当下一年的边际成本 > 当前年值成本 (EAC) 时，应置换设备。

**税后置换分析 (After-Tax Replacement Analysis)**：考虑旧设备变卖利得/损失 (Gain/Loss on Disposal) 对税负的影响。

## 相关条目

- [[INDEX|当前目录索引]]
- [[04_EngineeringAndTechnology/EngineeringFundamentals/EngineeringMathematics/INDEX]]

## 十二、项目融资 (Project Financing)

### 12.1 资本结构 (Capital Structure)

**债务融资 (Debt Financing)**：银行贷款、企业债券，有固定利息和到期日。
**权益融资 (Equity Financing)**：发行股票、引入战略投资者，无固定回报但稀释控制权。
**WACC (加权平均资本成本)**：
 WACC = \frac{E}{V} \cdot r_e + \frac{D}{V} \cdot r_d \cdot (1 - T)

$ 为权益市值，$ 为债务市值， = E + D$，$ 为权益成本，$ 为债务成本。

### 12.2 项目融资模式 (Project Finance)

**BOT (Build-Operate-Transfer, 建设-运营-移交)**：私营企业建设基础设施，运营一定年限后移交政府。
**PPP (Public-Private Partnership, 公私合营)**：政府与企业共担风险，收益按协议分配。
**特许经营 (Concession)**：政府授予特定区域内排他性运营权，适用于高速公路、水处理项目。

**关键合同**：EPC (Engineering Procurement Construction, 设计采购施工总承包)、O&M (Operation & Maintenance, 运营维护)。

### 12.3 风险分担 (Risk Allocation)

| 风险类型 | 分担原则 | 典型案例 |
|---------|---------|---------|
| 政治风险 (Political) | 政府承担 | 汇率管制、国有化 |
| 建设风险 (Construction) | 承包商承担 | 工期延误、成本超支 |
| 运营风险 (Operational) | 运营商承担 | 设备故障、效率低下 |
| 市场风险 (Market) | 双方共担 | 原材料涨价、需求不足 |
| 不可抗力 (Force Majeure) | 保险覆盖 | 地震、洪水、战争 |

## 十三、实物期权 (Real Options)

### 13.1 期权类型

传统 NPV 方法忽略管理的灵活性 (Management Flexibility)。
实物期权 (Real Options) 思想：投资项目类似金融看涨期权。

| 期权类型 | 工程场景 | 类比金融期权 |
|---------|---------|-------------|
| 延迟期权 (Option to Defer) | 等待技术成熟或市场确认 | 美式看涨 (American Call) |
| 扩张期权 (Option to Expand) | 先小规模试点，成功后扩建 | 看涨期权 |
| 收缩期权 (Option to Contract) | 市场需求下降时缩减产能 | 看跌期权 (Put) |
| 放弃期权 (Option to Abandon) | 项目不可行时退出，回收残值 | 美式看跌 |
| 转换期权 (Option to Switch) | 在不同原材料或产品间切换 | 交换期权 (Exchange Option) |

### 13.2 实物期权定价

**Black-Scholes 公式类比**：
 C = S_0 N(d_1) - K e^{-rt} N(d_2)
 d_1 = \frac{\ln(S_0/K) + (r + \sigma^2/2)t}{\sigma\sqrt{t}}, \quad d_2 = d_1 - \sigma\sqrt{t}

$ 为项目现值，$ 为投资成本，$ 为无风险利率，$\sigma$ 为项目波动率，$ 为到期时间。

**二叉树模型 (Binomial Tree)**：离散时间下多阶段决策 (Multi-Stage Decision)。

## 十四、工程经济软件工具

| 工具 | 开发商 | 用途 |
|------|--------|------|
| Excel (NPV/IRR/Payback) | Microsoft | 基础财务建模 (Financial Modeling) |
| @RISK | Palisade | 蒙特卡洛模拟 (Monte Carlo Simulation) |
| Crystal Ball | Oracle | 概率风险分析和预测 |
| MATLAB Financial Toolbox | MathWorks | 金融建模和衍生品定价 |
| COMFAR (Computer Model for Feasibility Analysis) | UNIDO | 投资项目可行性分析 |
| Analytica | Lumina | 决策分析和敏感性分析 |

**工程经济分析所需数据**：
- 投资估算 (资本支出 CAPEX + 运营支出 OPEX)
- 产品价格和市场需求预测
- 税率、折旧政策、通胀率
- 融资方案和利率
- 项目寿命周期 (一般 10-30 年)

## 十五、案例研究：高速公路 BOT 项目

**项目概况**：全长 150 km，4 车道高速公路，总投资 120 亿元。
**特许期**：30 年（含建设期 4 年）。
**融资结构**：自有资金 30% + 银行贷款 70%（利率 5%）。

**关键参数**：
- 年均日交通量 (AADT) 初始 35,000 pcu/天，年增长率 5%
- 收费标准 0.5 元/km/车
- 年运营维护成本 初始 1.5 亿，年增 3%
- MARR = 8%

**评价结果**：
- 税前 NPV (8%) = 18.6 亿元
- IRR = 10.2% > MARR 8%
- 动态回收期 = 14.3 年
- 敏感性分析：交通量下降 10% 时 IRR = 8.8%，风险可控

## 十六、通货膨胀与汇率风险管理

### 16.1 通货膨胀调整 (Inflation Adjustment)

工程建设周期长 (3-10 年)，通胀对总投资影响显著。
**价格调整公式 (Price Adjustment Formula)**：
 C_t = C_{base} \times \frac{CPI_t}{CPI_{base}}

**Escalation (涨价预备费)**：根据物价指数预测逐年调整投资估算。

### 16.2 汇率风险 (Exchange Rate Risk)

对外工程承包 (International Engineering Contract) 面临汇率波动风险。
**对冲策略 (Hedging Strategy)**：
- 远期合约 (Forward Contract)：锁定未来汇率
- 货币互换 (Currency Swap)：互换不同币种现金流
- 自然对冲 (Natural Hedge)：收入与支出币种匹配
- 汇率波动预留金 (Contingency Allowance for FX)

### 16.3 国别风险分析 (Country Risk Analysis)

| 风险维度 | 评估内容 | 信息来源 |
|---------|---------|---------|
| 政治风险 | 政权稳定性、政策连续性 | 经济学人 (EIU)、穆迪 (Moody's) |
| 经济风险 | 通胀率、GDP 增长、外债水平 | 世界银行、IMF |
| 法律风险 | 合同法完备性、仲裁执行 | 世界银行营商环境报告 |
| 社会风险 | 劳资关系、文化差异 | 咨询公司专项报告 |
