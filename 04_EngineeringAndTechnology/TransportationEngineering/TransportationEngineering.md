# 交通运输工程

## 学科定义
交通运输工程研究交通系统规划、设计、建设与运营管理的工程学科。

## 核心公式

### 交通流基本模型
$$ q = k \cdot v $$

其中 $q$ 为交通流量，$k$ 为密度，$v$ 为速度。

### Greenshields 模型
$$ v = v_f \left(1 - \frac{k}{k_j}\right) $$

**流量-密度关系**：
$$ q = v_f k \left(1 - \frac{k}{k_j}\right) $$

**最大流量对应密度与速度**：
$$ k_m = \frac{k_j}{2},\quad v_m = \frac{v_f}{2},\quad q_{\max} = \frac{v_f k_j}{4} $$

其中 $v_f$ 为自由流速度，$k_j$ 为阻塞密度。

### 跟驰模型
$$ a_n(t) = \alpha \frac{v_n(t) - v_{n-1}(t)}{\Delta x_n(t - T)} $$

### 道路通行能力
$$ C = \frac{3600}{h_t} $$

### 停车视距
$$ S = \frac{v}{3.6}t + \frac{v^2}{254(\varphi + i)} $$

### 交通分配用户均衡
$$ \sum_a \int_0^{x_a} t_a(\omega)d\omega \to \min $$

## 服务水平分级

| 等级 | 密度 (veh/km/lane) | 速度 (km/h) | 流量 (veh/h/lane) | 行驶状态 |
|------|-------------------|-------------|-------------------|---------|
| A | ≤ 7 | ≥ 100 | ≤ 700 | 自由流 |
| B | ≤ 18 | ≥ 90 | ≤ 1100 | 稳定流 |
| C | ≤ 25 | ≥ 80 | ≤ 1550 | 接近稳定流 |
| D | ≤ 40 | ≥ 60 | ≤ 1850 | 接近不稳定流 |
| E | ≤ 60 | ≥ 48 | ≤ 2000 | 拥堵流 |
| F | > 60 | < 48 | 不稳定 | 强制流/拥堵 |

## 交通方式比较

| 交通方式 | 速度(km/h) | 运量(万人/h) | 能耗 | 成本(亿元/km) | 适用范围 |
|----------|------------|--------------|------|---------------|----------|
| 高速公路 | 80~120 | 0.5~1.5 | 中 | 0.5~1 | 中长途客运 |
| 高速铁路 | 250~350 | 1~5 | 低 | 1~3 | 中长途客运 |
| 城市轨道 | 30~80 | 2~8 | 低 | 3~8 | 城市通勤 |
| 航空运输 | 800~900 | 0.1~0.5 | 高 | — | 长途 |
| 水运 | 10~30 | 0.5~10 | 最低 | — | 货运 |

## 研究对象
- 交通规划
- 道路与铁道工程
- 桥梁与隧道工程
- 交通运输管理
- 交通信息工程

## 核心课程
- 交通工程学
- 道路勘测设计
- 桥梁工程
- 铁道工程
- 交通规划
- 交通管理与控制

## 学习路径
1. 基础阶段：力学、工程制图、材料学
2. 专业基础：交通工程、道路工程、桥梁工程
3. 专业核心：路线设计、交通规划、轨道工程
4. 专业拓展：智能交通、BIM技术

## 经典教材
- 王炜《交通工程学》
- 李杰《道路勘测设计》
- 邵旭东《桥梁工程》
- 沈志云《铁道工程》

## 主要应用领域
- 道路交通规划
- 高速铁路建设
- 城市轨道交通
- 桥梁与隧道工程
- 智能交通系统

## 相关条目

- [[04_EngineeringAndTechnology/CivilEngineering/INDEX|CivilEngineering]]
- [[04_EngineeringAndTechnology/CivilEngineering/UrbanPlanning/INDEX|UrbanPlanning]]
- [[04_EngineeringAndTechnology/TransportationEngineering/Logistics/INDEX|Logistics]]
- [[04_EngineeringAndTechnology/MechanicalAndElectricalEngineering/MechanicalEngineering/INDEX|MechanicalEngineering]]
- [[HighwayEngineering]]
- [[TrafficEngineering]]
