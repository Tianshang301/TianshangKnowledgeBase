---
aliases: [AircraftDesign]
tags: ['04_EngineeringAndTechnology', 'AerospaceAndMilitaryEngineering', 'AerospaceEngineering']
---

# 飞机设计 (Aircraft Design)

## 一、概述

飞机设计是将客户需求 (Customer Requirements) 转化为满足适航标准 (Airworthiness Standards) 的飞行器的系统化工程过程。
它综合了空气动力学 (Aerodynamics)、结构力学 (Structural Mechanics)、推进系统 (Propulsion)、飞行力学 (Flight Dynamics)、航电系统 (Avionics) 和制造工艺 (Manufacturing) 等多学科知识，是一项典型的 MDO (Multidisciplinary Design Optimization, 多学科设计优化) 工程。
设计流程通常分为概念设计 (Conceptual Design)、初步设计 (Preliminary Design)、详细设计 (Detailed Design) 和试制试飞 (Prototyping & Flight Test) 四个阶段。
一架现代客机 (如 B787 或 A350) 的研发周期约 7-10 年，投入资金超过 200 亿美元。
飞机设计的首要目标是安全性 (Safety)、经济性 (Economics) 和环保性 (Environmental Sustainability)。

## 二、设计流程

### 2.1 设计阶段

```mermaid
graph LR
    A[概念设计 Conceptual] --> B[初步设计 Preliminary]
    B --> C[详细设计 Detail]
    C --> D[试制与试飞 Prototyping]
    D --> E[适航取证 Certification]
    E --> F[量产 Production]
```

| 阶段 | 时间占比 | 成本占比 | 关键活动 | 输出物 |
|------|---------|---------|---------|--------|
| 概念设计 | 10% | 5% | 需求分析、布局选型 (Configuration)、参数估算 | 三视图、重量报告 |
| 初步设计 | 25% | 15% | CFD 分析、风洞实验 (Wind Tunnel)、结构布局 | CAD 模型、载荷谱 |
| 详细设计 | 45% | 55% | 零部件 CAD、强度校核、系统集成 | 生产图纸、BOM |
| 试制试飞 | 20% | 25% | 原型制造 (Prototype)、飞行测试、适航验证 | 型号合格证 (TC) |

### 2.2 初始参数估算

起飞重量构成：
$$W_{TO} = W_{crew} + W_{payload} + W_{fuel} + W_{empty}$$

空重估算经验公式：
$$\frac{W_{empty}}{W_{TO}} = A \cdot W_{TO}^C \cdot K_{vs}$$

$A$、$C$ 为统计回归系数，$K_{vs}$ 为技术因子 (Technology Factor, 复合材料占比、先进工艺等)。

**Breguet 航程方程 (Breguet Range Equation)** (喷气飞机)：
$$R = \frac{V \cdot L/D}{c} \ln\left(\frac{W_i}{W_f}\right)$$

$V$ 为巡航速度，$L/D$ 为升阻比 (Lift-to-Drag Ratio)，$c$ 为耗油率 (Specific Fuel Consumption)，$W_i$、$W_f$ 为航段初末重量。

**Breguet 航程方程** (螺旋桨飞机)：
$$R = \frac{\eta_p}{c} \cdot \frac{L}{D} \cdot \ln\left(\frac{W_i}{W_f}\right)$$

$\eta_p$ 为螺旋桨效率 (0.8-0.87)。

## 三、空气动力学设计 (Aerodynamic Design)

### 3.1 翼型设计 (Airfoil Design)

翼型几何参数：最大厚度比 $t/c$ (Thickness Ratio)、弯度 $f/c$ (Camber)、前缘半径 (Leading Edge Radius)。

**NACA 四位数字翼型** (如 NACA 2412)：
- 第1位：最大弯度百分比 (2% of chord)
- 第2位：距前缘位置/10 (40% of chord from LE)
- 末两位：最大厚度百分比 (12% of chord)

**薄翼理论 (Thin Airfoil Theory)**：$C_l = 2\pi \alpha$
实际翼型 $C_{l\alpha} \approx 5.73-6.28$ /rad (取决于厚度和弯度)。

### 3.2 机翼平面形状 (Wing Planform)

| 参数 | 定义 | 气动影响 | 结构影响 |
|------|------|---------|---------|
| 展弦比 $AR = b^2/S$ | 翼展平方/面积 | $AR \uparrow \Rightarrow$ 诱导阻力 $\downarrow$ | $AR \uparrow \Rightarrow$ 结构重量 $\uparrow$ |
| 后掠角 $\Lambda$ | 前/后缘与横向夹角 | $\Lambda \uparrow \Rightarrow M_{crit} \uparrow$ (临界马赫数) | 结构效率 $\downarrow$ |
| 根梢比 $\lambda = c_r/c_t$ | 根弦/尖弦 | 影响展向载荷分布 | 影响根部弯矩 |

**诱导阻力 (Induced Drag)**：
$$C_{Di} = \frac{C_L^2}{\pi AR \cdot e}$$

$e$ 为 Oswald 效率因子 (0.75-0.85, 椭圆载荷分布为 1.0)。

### 3.3 跨声速与超声速 (Transonic & Supersonic)

$M_{crit}$ (Critical Mach Number)：翼面首次出现局部超声速流 (Local Supersonic Flow) 的马赫数。
超临界翼型 (Supercritical Airfoil, Whitcomb 设计) 可使 $M_{crit}$ 提高 0.04-0.08，广泛应用于现代客机。

**面积律 (Area Rule, Whitcomb Area Rule)**：机身横截面积 (Cross-Sectional Area) 沿轴向光滑过渡，减小跨声速波阻 (Wave Drag)。波阻在 $M > M_{crit}$ 后急剧增加 (Drag Rise)。

### 3.4 高升力装置 (High-Lift Devices)

前缘缝翼 (Leading Edge Slat) + 后缘襟翼 (Trailing Edge Flap, Fowler/双缝/三缝襟翼)。
最大升力增量：
$$\Delta C_{L,max} = \eta_f \cdot \left(\frac{c_f}{c}\right) \cdot \Delta C_{l,max}$$

$\eta_f$ 为襟翼效率 (0.6-0.9)，$c_f/c$ 为襟翼弦长比。

## 四、结构设计 (Structural Design)

### 4.1 半硬壳式结构 (Semi-Monocoque)

蒙皮 (Skin) — 承受面内剪力和扭矩 (Shear & Torsion)
桁条 (Stringer) — 承受轴向力 (Axial Load)，增强蒙皮抗屈曲能力
隔框 (Frame) — 维持截面形状，传递集中力 (Concentrated Load)
翼梁 (Spar) — 承受弯矩 (腹板承受剪力 + 缘条承受弯矩)
翼肋 (Rib) — 维持翼型，传递气动载荷

### 4.2 载荷与 V-n 图 (Load Factor Diagram)

载荷因数 (Load Factor)：$n = \frac{L}{W}$
V-n 图边界 (Flight Envelope)：$n_{max}$ (最大正过载)、$n_{min}$ (最小负过载)、$V_D$ (设计俯冲速度)、$V_A$ (设计机动速度)。

**突风载荷 (Gust Load)**：$n = 1 \pm \frac{K_g \rho V a U}{2W/S}$，$U$ 为突风速度 (m/s)。

### 4.3 材料选择

| 材料 | 密度 (g/cm³) | 屈服强度 (MPa) | 比强度 | 应用 |
|------|-------------|---------------|--------|------|
| 2024-T3 Al | 2.78 | 345 | 中 | 机身蒙皮 (Skin) |
| 7075-T6 Al | 2.81 | 505 | 较高 | 机翼蒙皮 |
| Ti-6Al-4V | 4.43 | 830 | 高 | 起落架 (Landing Gear) |
| 300M 钢 | 7.85 | 1650 | 中 | 起落架 |
| CFRP (碳纤维增强聚合物) | 1.60 | 600 (纤维方向) | 很高 | 机翼/机身 (B787 占比 50%) |

**Tsai-Wu 失效准则 (Tsai-Wu Failure Criterion)**：$F_i \sigma_i + F_{ij} \sigma_i \sigma_j = 1$

### 4.4 疲劳与损伤容限 (Fatigue & Damage Tolerance)

**S-N 曲线 (Stress-Life Curve)**：应力幅 (Stress Amplitude) vs 疲劳寿命 (Cycles to Failure)。
**Paris 裂纹扩展定律 (Paris Law)**：$\frac{da}{dN} = C (\Delta K)^m$

$K_{IC}$ 为断裂韧性 (Fracture Toughness)。损伤容限设计 (Damage Tolerance Design) 通过裂纹扩展速率 $da/dN$ 确定检查间隔 (Inspection Interval)。

## 五、飞行力学与控制 (Flight Dynamics & Control)

### 5.1 纵向静稳定性 (Longitudinal Static Stability)

$$\frac{dC_m}{dC_L} = \bar{x}_{cg} - \bar{x}_{ac} < 0$$

静稳定裕度 (Static Margin) $SM = \bar{x}_{ac} - \bar{x}_{cg}$，典型 5%-15% MAC (Mean Aerodynamic Chord, 平均气动弦长)。

### 5.2 横航向稳定性 (Lateral-Directional Stability)

上反角 (Dihedral Angle) $\Gamma$：$C_{l\beta} < 0$ (正上反角提供横滚稳定性)。后掠角也贡献横滚稳定性。

### 5.3 飞控系统 (Flight Control System)

**电传操纵 (FBW, Fly-By-Wire)**：飞行员指令通过电缆 (Wire) 传输，飞行控制计算机 (FCC, Flight Control Computer) 解算舵面偏角。
控制增稳系统 (CAS, Control Augmentation System)、自动驾驶仪 (Autopilot)、自动油门 (Autothrottle)。

## 六、系统集成 (Systems Integration)

**飞控作动**：EHA (Electro-Hydrostatic Actuator, 电静液作动器)/EMA (Electro-Mechanical Actuator, 机电作动器)。
**航电 (Avionics)**：ARINC 429/664 数据总线，GPS/INS (惯性导航系统) 组合导航。
**液压系统**：3000/5000 psi (21/35 MPa)。
**电气系统**：270V DC / 115V 400Hz AC。
**环控系统 (ECS, Environmental Control System)**：引气 (Bleed Air) + 空气循环机 (ACM, Air Cycle Machine) + 座舱增压 (Cabin Pressurization)。

## 七、适航标准 (Airworthiness Standards)

| 标准 | 适用机型 | 机构 |
|------|------|------|
| FAR Part 25 | 运输类飞机 | FAA (美国联邦航空管理局) |
| CS-25 | 大型飞机 | EASA (欧洲航空安全局) |
| CCAR-25 | 运输类飞机 | CAAC (中国民用航空局) |
| MIL-HDBK-516 | 军用飞机 | USAF (美国空军) |

**取证试验 (Certification Tests)**：静力试验 (1.5 倍极限载荷, Ultimate Load)、鸟撞 (Bird Strike, 4/8 磅鸟)、雷击 (Lightning Strike)、HIRF (高强辐射场)。

## 八、先进概念

BWB (Blended Wing Body, 翼身融合体)、层流控制 (Laminar Flow Control)、分布式电推进 (DEP, Distributed Electric Propulsion)、主动气动弹性机翼 (Active Aeroelastic Wing)、无尾布局 (Tailless Configuration)、变后掠翼 (Variable Sweep Wing)。

## 九、MDO 优化 (Multidisciplinary Design Optimization)

$$\min f(\mathbf{x}), \quad \text{s.t. } g_j(\mathbf{x}) \leq 0, \quad h_k(\mathbf{x}) = 0$$

学科耦合：气动 (Aerodynamics) → 结构 (Structures) → 推进 (Propulsion) → 重量 (Weight) → 性能 (Performance)。
MDO 架构：CO (Collaborative Optimization, 协同优化)、BLISS (Bi-Level Integrated System Synthesis, 两级集成系统综合)、ATC (Analytical Target Cascading, 分析目标级联)。

## 十、飞行品质评估 (Handling Qualities)

### 10.1 飞行品质等级 (Flying Qualities Levels)

飞行品质 (Handling Qualities) 指飞行员完成规定任务 (Mission Task) 的难易程度。
Cooper-Harper 评分 (Cooper-Harper Rating, CHR) 是评价飞行品质的标准方法，等级 1-10。
**Level 1 (CHR 1-3.5)**：飞行品质令人满意，无需改进。
**Level 2 (CHR 3.5-6.5)**：飞行品质有不足，但可接受。
**Level 3 (CHR 6.5-9)**：飞行品质不足，需大幅改进。

### 10.2 MIL-STD-1797 规范

**短周期模态 (Short Period Mode)** 频率与阻尼要求：
$$ \zeta_{sp} = 0.35-1.30 \quad (\text{Level 1}), \quad \omega_{sp} \geq \text{下限} $$

**荷兰滚模态 (Dutch Roll Mode)** 要求：
$$ \zeta_d \geq 0.08 \quad (\text{Level 1}), \quad \omega_d \geq 0.4 \text{ rad/s} $$

**滚转时间常数 (Roll Mode Time Constant)**：
$$ \tau_r \leq 1.0 \text{ s} \quad (\text{Level 1, Class I-IV}) $$

### 10.3 舵面铰链力矩 (Hinge Moment)

舵面气动载荷产生铰链力矩 (Hinge Moment $H_e$)，需确定作动器 (Actuator) 容量：
$$ H_e = C_{he} \cdot q \cdot S_e \cdot \bar{c}_e $$

$C_{he}$ 为铰链力矩系数，$S_e$ 为舵面面积，$\bar{c}_e$ 为舵面平均气动弦。

## 十一、构型管理 (Configuration Management)

### 11.1 产品结构 (Product Breakdown Structure)

飞机级 Airplane Level
├── 机身 Fuselage Section (前/中/后)
├── 机翼 Wing (左/右, 内/外翼)
├── 尾翼 Empennage (平尾 HTP + 垂尾 VTP)
├── 动力装置 Powerplant (发动机 + 短舱 + 吊架)
├── 起落架 Landing Gear (前起 + 主起)
├── 飞行控制 Flight Control (主飞控 + 高升力)
├── 航电系统 Avionics (通信/导航/识别)
├── 电气系统 Electrical (发电/配电/应急)
├── 环控系统 ECS (空调/增压/防冰)
└── 内饰 Cabin Interior (座椅/厨房/卫生间)

### 11.2 构型基线 (Baseline) 管理

基线里程碑：
SRR (System Requirements Review) → PDR (Preliminary Design Review) → CDR (Critical Design Review) → TRR (Test Readiness Review)

ECP (Engineering Change Proposal, 工程变更建议) 流程：
1. 变更请求 (Change Request) → 2. 影响评估 (Impact Assessment, 成本/进度/性能) → 3. 构型控制委员会 (CCB, Configuration Control Board) 审批 → 4. 变更实施 → 5. 验证确认

### 11.3 数字化工具

**PLM (Product Lifecycle Management)**：达索 (Dassault) CATIA/ENOVIA, Siemens Teamcenter。
**MBSE (Model-Based Systems Engineering, 基于模型的系统工程)**：SysML 建模语言。
**数字孪生 (Digital Twin)**：在虚拟环境中集成气动/结构/热/控制系统仿真。

## 十二、先进制造工艺

### 12.1 复合材料制造

**自动铺丝 (AFP, Automated Fiber Placement)**：铺放速率 10-50 kg/h，精度 ±0.5 mm。
**自动铺带 (ATL, Automated Tape Layup)**：适用于平板/大曲率部件，铺带宽度 75-300 mm。
**热压罐固化 (Autoclave Curing)**：温度 180°C (热固性，Thermoset)，压力 6 bar，周期 8-12 h。
**OOA (Out of Autoclave, 非热压罐)**：降低制造成本，适用于大型结构。

### 12.2 增材制造 (Additive Manufacturing)

**EBM (Electron Beam Melting, 电子束熔炼)**：钛合金 (Ti-6Al-4V) 构件直接成型。
**SLM (Selective Laser Melting, 选择性激光熔融)**：复杂冷却通道、轻量化点阵结构 (Lattice Structure)。
**WAAM (Wire Arc Additive Manufacturing, 电弧增材)**：大型结构件快速成型，沉积速率可达 1-5 kg/h。

## 十三、试飞与适航验证

### 13.1 飞行试验项目

| 试验科目 | 内容 | 测试设备 |
|---------|------|---------|
| 性能试飞 | 起飞/着陆/爬升/巡航/下降性能 | GPS 差分定位、大气数据系统 |
| 操稳试飞 | 静/动稳定性、操纵品质 | 遥测地面站、机载数据记录仪 |
| 载荷试飞 | 飞行载荷、突风载荷谱 | 应变片桥盒、加速度计阵列 |
| 颤振试飞 | 气动弹性稳定性边界 | 激振器 (Vibroexcitation)、响应监测 |
| 噪声试飞 | 外部噪声适航符合性 | 地面麦克风阵列 (Flyover 测试) |
| 发动机试飞 | 喘振边界 (Surge Margin)、空中起动 | 发动机参数监测 (EHM) |
| 结冰试飞 | 自然结冰条件下性能和安全 | 结冰探头、防冰系统监控 |
| 功能可靠性 | 系统功能验证、中断起飞 (RTO) | 全机系统监控 |

**颤振试飞 (Flutter Flight Test)** 安全流程：
$$ V_{test} = V_D \times 1.15 \times K_{safety} $$

$V_D$ 为设计俯冲速度，$K_{safety}$ 根据马赫数确定 (0.85-1.0)。逐步逼近 (Staircase Approach) 颤振速度 $V_F$，在每个速度点激励并检验阻尼衰减。

### 13.2 适航取证过程

**型号合格证 (TC, Type Certificate)** 取证步骤：
1. 项目启动会 (Kickoff)
2. 审定基础 (Certification Basis) 确定 (FAR/CS 条款)
3. 符合性方法 (MOC, Means of Compliance): MOC 0-9
4. 取证试验试飞
5. TIA (Type Inspection Authorization) → TC 签发

**生产许可证 (PC, Production Certificate)** 和 单机适航证 (AC, Airworthiness Certificate)。

## 十四、未来技术趋势

**eVTOL (Electric Vertical Takeoff and Landing, 电动垂直起降飞行器)**：分布式电推进 (DEP)，多旋翼/倾转旋翼/升力+巡航构型。
**超声速客机 (Supersonic Transport, SST)**：低声爆设计 (Low Boom, X-59 QueSST)，声爆水平控制在 75 PLdB 以下。
**氢能飞机 (Hydrogen-Powered Aircraft)**：液态氢 LH₂ 储罐 (-253°C)，燃料电池 (Fuel Cell) + 电推进，或直接燃烧氢燃料。
**自适应变循环发动机 (Adaptive Versatile Engine Technology, ADVENT)**：三涵道 (Third Stream) 设计，兼顾高推力与低油耗。
**全电飞控 (Power-by-Wire)**：取消集中液压系统，采用分布式电静液作动器 (EHA) 和机电作动器 (EMA)。
**AI 辅助设计**：生成式设计 (Generative Design, 拓扑优化 Topology Optimization)、AI 代理加速 CFD 网格生成与气动优化。

## 相关条目

- [[04_EngineeringAndTechnology/AerospaceAndMilitaryEngineering/AerospaceEngineering/INDEX]]
- [[PropulsionSystems]]
- [[Astrodynamics]]
