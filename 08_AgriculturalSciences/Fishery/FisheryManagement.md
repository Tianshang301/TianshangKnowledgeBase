# 渔业管理

## 概述

渔业管理（Fisheries Management）是在可持续利用前提下，对渔业资源进行科学评估、合理配置和有效监管的过程。其核心目标是在保障生态系统的健康和生物多样性的同时，实现渔业资源的经济效益和社会效益最大化。

---

## 渔业管理目标

### 最大可持续产量（MSY）
最大可持续产量（Maximum Sustainable Yield, MSY）是传统渔业管理的核心目标，指在不损害资源长期生产力的前提下，能够持续从渔业种群中捕获的最大年产量。MSY 概念建立在种群增长模型基础上。

### 基于生态系统的渔业管理（EAF）
基于生态系统的渔业管理（Ecosystem-Based Fisheries Management, EBFM/EAF）超越了单一物种管理，综合考虑：
- 种间关系（捕食、竞争、互惠）
- 栖息地保护
- 兼捕（bycatch）和丢弃物
- 环境变化（气候、污染）
- 社会经济因素

### 预防性方法（Precautionary Approach）
当科学信息不确定时，采取保守的管理措施。FAO《负责任渔业行为守则》强调：缺乏充分的科学信息不应成为推迟或放弃采取保护措施的理由。

### 参考点（Reference Points）
- **目标参考点**（Target Reference Point, TRP）：渔业管理期望达到的状态
- **极限参考点**（Limit Reference Point, LRP）：不应逾越的边界，一旦越过即表明资源面临过度捕捞风险
- **触发参考点**（Trigger Reference Point）：触发管理行动的信号值

---

## 种群动力学模型

### 逻辑斯蒂增长模型（Logistic Growth Model）

种群在有限环境下的增长遵循逻辑斯蒂方程：

$$ \frac{dN}{dt} = rN\left(1 - \frac{N}{K}\right) $$

其中：
- $N$：种群数量
- $r$：内禀增长率
- $K$：环境容量

当种群大小为 $K/2$ 时，增长速率最大，此时获得最大可持续产量。

### 剩余产量模型（Surplus Production Model）

#### Schaefer 模型
Schaefer 模型是最经典的剩余产量模型，假设种群增长服从逻辑斯蒂曲线：

$$ B_{t+1} = B_t + rB_t\left(1 - \frac{B_t}{K}\right) - C_t $$

其中 $B_t$ 为第 $t$ 年的生物量，$C_t$ 为年渔获量。

关键参数：
- **最大可持续产量**：$MSY = rK/4$
- **最优生物量**：$B_{MSY} = K/2$
- **最优捕捞死亡率**：$F_{MSY} = r/2$

#### Fox 模型
Fox 模型是 Schaefer 模型的非对称扩展：

$$ \frac{dB}{dt} = rB\ln\left(\frac{K}{B}\right) - C $$

此时 MSY 发生在 $B_{MSY} = K/e \approx 0.368K$ 处。

### 年龄结构模型（Age-Structured Models）

#### 捕获曲线（Catch Curve）
基于渔获物年龄组成估算总死亡系数 $Z$：

$$ \ln(N_t) = \ln(N_0) - Zt $$

其中 $Z = F + M$（捕捞死亡系数 + 自然死亡系数）。

#### 体长频率分析（Length-Based Methods）
通过渔获物体长组成数据推算种群参数（生长参数、死亡系数、补充量等），适用于缺乏年龄数据的渔业。

#### 世代分析（Cohort Analysis）与 VPA
虚拟种群分析（Virtual Population Analysis, VPA）利用渔获量年龄组成数据，反向推算各年龄组的资源尾数：

$$ N_{a} = N_{a+1}e^{Z_a} + C_a e^{Z_a/2} $$

VPA 从最老年龄组（"终结点"）开始，假设终点的捕捞死亡率 $F_{terminal}$，逆向推算各年龄组资源量。

### 贝叶斯评估方法

将先验信息（历史调查、类似渔业数据）与观测数据（渔获量、调查指数）结合，通过贝叶斯更新得到参数的后验分布，量化管理建议的不确定性。

---

## 资源评估方法

### 基于渔获量数据的方法

| 方法 | 数据需求 | 适用条件 |
|------|----------|----------|
| CMSY | 渔获量时间序列 | 数据有限渔业 |
| 剩余产量模型 | 渔获量+CPUE | 有相对丰度指数 |
| ASPIC | 渔获量+CPUE | 非平衡动态 |
| 统计捕获曲线 | 渔获量年龄组成 | 有年龄数据 |

### 基于调查的评估

- **拖网调查**（Trawl Survey）：标准化调查设计，估算单位努力捕捞量
- **声学调查**（Acoustic Survey）：利用回声探测技术估算鱼类丰度
- **水下视频**（Underwater Video/Baited Remote Underwater Video, BRUV）：适用于岩礁和复杂生境
- **标志重捕**（Mark-Recapture）：通过标记释放和重捕比例估算种群大小

### 数据有限方法（Data-Limited Methods）

当缺乏年龄结构数据时，采用以下方法：
- **体长基准法**（Length-Based Spawning Potential Ratio, LBSPR）：利用体长频率分布估算产卵潜力比
- **DB-SRA**（Depletion-Based Stock Reduction Analysis）：基于消耗量的简化评估
- **Catch-MSY**：仅需渔获量数据的快速评估
- **DCAC**（Depletion-Corrected Average Catch）：校正消耗的平均渔获量法

---

## 捕捞技术与渔具选择

### 主要渔具类型对比

| 渔具类型 | 作业方式 | 选择性 | 生境影响 | 能耗 | 主要捕捞对象 |
|----------|----------|--------|----------|------|-------------|
| 拖网（Trawl） | 拖曳网具 | 低 | 高（底拖破坏生境） | 高 | 底层/中层鱼类、虾类 |
| 围网（Purse Seine） | 包围鱼群 | 中 | 低 | 中 | 中上层集群鱼类（金枪鱼、鲭） |
| 延绳钓（Longline） | 长干绳挂支线钓钩 | 高 | 低 | 中 | 金枪鱼、旗鱼、底栖鱼类 |
| 刺网（Gillnet） | 挂网拦截 | 中 | 低-中（缠绕丢失） | 低 | 多种鱼类 |
| 张网（Trap/Pot） | 笼具诱捕 | 高 | 低 | 低 | 龙虾、蟹、章鱼 |
| 板网（Danish Seine） | 绳索围曳 | 中 | 中 | 中 | 底层鱼类 |

### 兼捕减缓技术（Bycatch Mitigation）

- **海龟排除装置**（Turtle Excluder Device, TED）：在拖网中安装可让海龟逃逸的格栅门
- **鸟吓绳**（Tori Line/Bird Scaring Line）：防止海鸟吞食钓饵
- **渔获物释放钩**（Circle Hook）：减少海龟误吞死亡率
- **声波驱赶器**（Pinger）：驱离海豚和小型鲸类
- **时间与区域禁渔**（Time-Area Closures）：产卵期/育幼区季节性关闭

---

## 渔业治理体系

### 国际法框架

#### UNCLOS（联合国海洋法公约）
- 确立了**专属经济区**（Exclusive Economic Zone, EEZ）制度，沿海国对200海里内渔业资源拥有主权权利
- 公海渔业自由原则

#### UNFSA（联合国鱼类种群协定）
- 管理跨界鱼类种群和高度洄游鱼类种群
- 强调预防性原则和基于生态系统的管理

#### FAO《负责任渔业行为守则》
- 1995年由联合国粮农组织通过
- 为可持续渔业提供综合性国际框架

### 区域渔业管理组织（RFMOs）

| RFMO | 管辖区域 | 主要管理对象 |
|------|----------|-------------|
| ICCAT | 大西洋 | 金枪鱼、旗鱼类 |
| IATTC | 东太平洋 | 金枪鱼 |
| WCPFC | 中西太平洋 | 金枪鱼 |
| CCAMLR | 南极海域 | 南极磷虾、犬牙鱼 |
| NAFO | 西北大西洋 | 底层鱼类 |
| IOTC | 印度洋 | 金枪鱼 |

### 配额管理机制

#### TAC（总允许渔获量）
按年度设定特定物种的总可捕捞量，是多数渔业管理系统的核心。

#### ITQ（个人可转让配额）
将 TAC 分配为个体配额，并允许其在捕捞者之间自由转让。ITQ 的优点包括：
- 消除"渔业竞赛"（race to fish）
- 提高经济效益
- 延长渔汛期，提高渔获品质和安全性
- 减少过度投资

缺点：配额集中、新渔民准入困难、MCS（监测-控制-监视）要求高。

#### IQ（个人配额）与 IVQ（个体船舶配额）
类似 ITQ 但不可转让，或仅限同一企业内转让。

---

## 水产养殖认证体系

### ASC（水产养殖管理委员会）
- 覆盖虾类、三文鱼、罗非鱼、鲶鱼等十余个品种标准
- 要求：降低疾病传播风险、限制化学品使用、保护生态系统和社区权益

### BAP（最佳水产养殖实践）
- 由全球水产养殖联盟（GAA）开发，四星级认证体系（从养殖场到加工厂）
- 涵盖食品安全、动物健康、环境责任和社会责任

### GlobalG.A.P.
- 起源于欧洲的全球良好农业规范
- 水产养殖模块包括可追溯性、饲料安全、疾病管理和环境管理

### 有机水产认证
- 中国有机产品标准（GB/T 19630）：禁止使用化学合成投入品
- 欧盟有机水产养殖标准（EU 834/2007）：关注鱼群密度、饲料来源

---

## 海洋保护与管理

### 海洋保护区（MPA）
- **严格保护区**（No-Take Zone）：禁止任何捕捞活动
- **多功能保护区**（Multiple-Use MPA）：分区分级管理
- **社区管理区**（Locally Managed Marine Area, LMMA）：由本地社区主导的海洋保护

MPA 效果评估指标：
- 鱼类生物量恢复
- 物种丰富度增加
- 溢出效应（spillover）
- 生态弹性提升

### 海洋空间规划（Marine Spatial Planning, MSP）

基于生态系统的海洋空间管理工具，协调不同海洋利用的冲突：
- 渔业活动与保护区的空间配置
- 航运通道与渔业区域的分离
- 海上风电、油气开采与渔业的兼容性
- 海水养殖区的系统规划

### 综合海洋管理

通过多部门协调机制实现：
- 陆海统筹（Land-Sea Interface）
- 流域-河口-近海一体化管理
- 基于生态系统的渔业与沿海管理

---

## IUU 捕捞预防

IUU（Illegal, Unreported and Unregulated）捕捞是当前全球渔业面临的最严重威胁之一。

### 主要措施

1. **港口国措施协定**（PSMA）：拒绝 IUU 渔船进入港口和卸货
2. **渔获文件计划**（Catch Documentation Scheme, CDS）：追溯渔获物从捕获到市场的全过程
3. **船舶监测系统**（Vessel Monitoring System, VMS）：卫星追踪渔船位置
4. **自动识别系统**（AIS）：辅助渔船监控
5. **公海登临检查**：RFMO 授权执法人员登船检查
6. **黑色清单制度**（IUU Vessel List）：列入名单的船只禁止停靠成员港口
7. **电子监控技术**：船上 CCTV 摄像头和传感器

### RFMO 的 IUU 清单示例

| 组织 | 列入船舶数 | 主要违规类型 |
|------|-----------|-------------|
| CCAMLR | ~25 | 非法捕捞犬牙鱼 |
| ICCAT | ~15 | 非法捕捞大西洋金枪鱼 |
| IOTC | ~20 | 非法捕捞印度洋金枪鱼 |
| NAFO | ~10 | 非法捕捞底层鱼类 |

---

## 气候变化对渔业的影响

### 主要影响途径

1. **海水升温**
   - 物种地理分布变迁（向极地和深水移动）
   - 产卵期提前，生长速率变化
   - 热应激导致繁殖力下降

2. **海洋酸化**
   - 影响钙化生物（贝类、珊瑚、浮游有孔虫）
   - 降低幼鱼存活率
   - 改变食物网结构

3. **海平面上升与缺氧**
   - 沿海养殖设施淹没风险
   - 底层水体缺氧加剧
   - 栖息地丧失（红树林、海草床）

4. **极端天气频发**
   - 台风/飓风对养殖设施和渔港的破坏
   - 风暴导致捕捞作业时间减少
   - 降雨模式变化影响河口鱼类繁殖

### 适应性管理策略

- 发展抗逆性养殖品种
- 建立气候变化条件下的预警系统
- 渔业管理参考点的动态调整
- 可移动渔业配额制度使渔业能够响应资源分布变化
- 扩展和优化 MPA 网络以增强生态韧性

---

## 相关条目

- [[02_NaturalSciences/EarthSciences/Oceanography/INDEX|Oceanography]]
- [[MarineBiology]]
- [[Aquaculture]]
- [[08_AgriculturalSciences/FoodScience/INDEX|FoodScience]]

## 参考文献与拓展阅读

- FAO. (2020). *The State of World Fisheries and Aquaculture 2020*. Rome: FAO.
- Hilborn, R., & Walters, C. J. (1992). *Quantitative Fisheries Stock Assessment*. Chapman & Hall.
- Quinn, T. J., & Deriso, R. B. (1999). *Quantitative Fish Dynamics*. Oxford University Press.
- Cochrane, K. L., & Garcia, S. M. (Eds.). (2009). *A Fishery Manager's Guidebook*. FAO/Wiley-Blackwell.
- 联合国海洋法公约 (UNCLOS, 1982)
- FAO 负责任渔业行为守则 (1995)
