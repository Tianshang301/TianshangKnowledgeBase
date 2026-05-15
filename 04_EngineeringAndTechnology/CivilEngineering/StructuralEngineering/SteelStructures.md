---
aliases: [SteelStructures]
tags: ['CivilEngineering', 'StructuralEngineering', 'SteelStructures']
---

# 钢结构

## 定义
钢结构是以钢材为主要材料制作的结构。具有强度高、自重轻、塑性韧性好、工业化程度高等特点。

## 研究对象
- 钢材性能与选用
- 连接设计（焊接、螺栓连接）
- 受弯构件设计
- 轴心受力构件设计
- 压弯构件设计
- 钢结构稳定性

## 核心内容

### 钢材性能

**常用钢材牌号**：
- Q235：碳素结构钢，屈服强度235MPa
- Q345：低合金高强度钢，屈服强度345MPa
- Q390、Q420：更高强度等级

**力学性能指标**：
- 屈服强度 $f_y$：设计强度依据
- 抗拉强度 $f_u$：极限强度
- 伸长率 $\delta$：塑性指标
- 冲击韧性：低温脆断抗力

**钢材选用原则**：
- 受拉构件：强度控制
- 受压构件：稳定性控制
- 疲劳构件：疲劳强度控制

### 连接设计

**焊接连接**：
- 对接焊缝：等强度设计
- 角焊缝：$f_{fw} = \frac{F}{h_e l_w} \leq f_{fw}^w$
- 焊缝强度设计值 $f_{fw}^w$：与钢材和焊条匹配
- 焊接缺陷：气孔、夹渣、未熔合

**螺栓连接**：
- 普通螺栓：C级（粗制），A/B级（精制）
- 高强度螺栓：摩擦型（抗滑移）和承压型
- 螺栓承载力计算

### 受弯构件（梁的设计）

**强度计算**：

$$\sigma = \frac{M}{W_n} \leq f$$

$W_n$ 为净截面模量，$f$ 为钢材抗弯强度设计值。

**整体稳定**：

$$\sigma = \frac{M}{\varphi_b W_x} \leq f$$

$\varphi_b$ 为整体稳定系数。

**局部稳定**：
- 受压翼缘：宽厚比限值
- 腹板：高厚比限值，可能需要加劲肋

### 轴心受力构件

**强度计算**：

$$\sigma = \frac{N}{A_n} \leq f$$

**整体稳定**：

$$\frac{N}{\varphi A} \leq f$$

$\varphi$ 为轴心受压构件稳定系数，取决于长细比 $\lambda = l_0/i$。

**局部稳定**：板件宽厚比限值

### 压弯构件

**弯矩作用平面内稳定**：

$$\frac{N}{\varphi_x A} + \frac{\beta_{mx}M_x}{\gamma_x W_{1x}(1-0.8N/N_{Ex}')} \leq f$$

**弯矩作用平面外稳定**：

$$\frac{N}{\varphi_y A} + \frac{\eta\beta_{tx}M_x}{\varphi_b W_{1x}} \leq f$$

### 钢结构稳定性

**整体失稳**：构件偏离原平衡位置发生过大变形

**局部失稳**：板件在压应力作用下发生屈曲

**设计措施**：
- 控制长细比
- 设置支撑系统
- 加劲肋设计
- 选用合适截面形式

## 经典教材
- 陈绍蕃《钢结构》
- 戴国欣《钢结构》
- Segui《Steel Design》
- McCormac《Structural Steel Design》

## 主要应用领域
- 高层建筑（钢结构框架）
- 大跨度空间结构（体育场馆、会展中心）
- 桥梁工程（钢箱梁、钢桁架）
- 工业厂房（门式刚架）
- 塔桅结构（输电塔、通信塔）
- 海洋平台

## 相关条目

- [[04_EngineeringAndTechnology/MechanicsAndMaterials/INDEX|MechanicsAndMaterials]]
- [[04_EngineeringAndTechnology/CivilEngineering/GeotechnicalEngineering/INDEX|GeotechnicalEngineering]]
- EarthquakeEngineering
