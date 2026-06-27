---
aliases: [ComputationalMaterials]
tags: ['MaterialsInformatics', 'ComputationalMaterials']
created: 2026-05-16
updated: 2026-05-13
---

# 计算材料?
## 概述

计算材料学是利用计算机模拟和理论计算方法研究材料性质、结构和行为的学科它在材料设计能预测和机理研究中发挥重要作用，是材料科学研究的重要手段?
## 第一性原理计算（DFT?
### 基本原理

**薛定谔方程：**
$$\hat{H}\Psi = E\Psi$$

**密度泛函理论?*
- Hohenberg-Kohn 定理
- Kohn-Sham 方程
- 电子密度作为基本变量

**Kohn-Sham 方程?*
$$\left[-\frac{\hbar^2}{2m}\nabla^2 + V_{eff}(r)\right]\psi_i(r) = \varepsilon_i\psi_i(r)$$

### 交换关联泛函

**屢域密度近似（LDA）：**
- 基于均匀电子?- 高估结合?- 低估晶格常数

**广义梯度近似（GGA）：**
- 考虑电子密度梯度
- PBE 泛函朢常用
- 改善 LDA 的系统误?
**杂化泛函?*
- 混合精确交换
- HSE06：带隙计?- 计算成本?
### 平面波基?
**展开形式?*
$$\psi(r) = \sum_G c_G e^{i(k+G)r}$$

**参数?*
- 截断能（Ecut）：基组大小
- k 点网格：布里渊区采样
- 收敛性测?
### 常用软件

**VASP?*
- 商业软件
- 广泛使用
- 功能强大

**Quantum ESPRESSO?*
- 弢源软?- 平面波基?- 活跃社区

**ABINIT?*
- 弢源软?- 多种功能
- 文档完善

**CASTEP?*
- 商业软件
- 材料模拟
- 界面友好

### 计算流程

1. 结构准备：晶体结构文件（POSCAR?2. 自洽计算（SCF）：电子结构
3. 非自洽计算：态密度能?4. 性质计算：弹性声子等
5. 结果分析：可视化、统?
## 分子动力学模?
### 经典分子动力?
**基本原理?*
- 牛顿运动定律
- 力场势函?- 数积?
**运动方程?*
$$m_i\frac{d^2r_i}{dt^2} = F_i = -\nabla_i U$$

**时间积分?*
- Verlet 算法
- Velocity Verlet
- 预测-校正算法

### 力场类型

**对势?*
- Lennard-Jones 势：$U(r) = 4\varepsilon\left[\left(\frac{\sigma}{r}\right)^{12} - \left(\frac{\sigma}{r}\right)^{6}\right]$
- Morse 势：$U(r) = D_e[1-e^{-a(r-r_e)}]^2$

**多体势：**
- EAM（嵌入原子法）：金属
- Tersoff 势：共价材料
- COMB 势：通用

### 从头算分子动力学（AIMD?
**原理?*
- DFT 计算?- 经典 MD 积分
- 自洽电子结构

**方法?*
- Car-Parrinello 方法
- Born-Oppenheimer MD

**应用?*
- 化学反应
- 离子液体
- 界面过程

### 常用软件

**LAMMPS?*
- 弢源软?- 大规模模?- 多种力场

**GROMACS?*
- 生物分子
- 高效计算
- 丰富分析

**NAMD?*
- 生物体系
- 并行计算
- 与 VMD 集成

**OpenMM?*
- Python 接口
- GPU 加?- 灵活定制

### 模拟流程

1. 系统构建：原子坐标盒?2. 能量朢小化：消除接?3. NVT 平衡：温度控?4. NPT 平衡：压力控?5. 生产模拟：数据采?6. 轨迹分析：质计算

## 有限元方法在材料力学中的应用

### 基本原理

**变分原理?*
- 朢小势能原?- 虚功原理
- 加权残法

**离散化：**
- 单元划分
- 形函?- 数积?
### 单元类型

**丢维单元：**
- 杆单?- 梁单?
**二维单元?*
- 三角形单?- 四边形单?
**三维单元?*
- 四面体单?- 六面体单?
### 材料力学应用

**弹分析：**
- 应力-应变关系
- 边界条件
- 位移和应力分?
**断裂力学?*
- 裂纹扩展
- 应力强度因子
- 疲劳寿命预测

**复合材料?*
- 多尺度建?- 界面行为
- 损伤演化

### 常用软件

- ABAQUS
- ANSYS
- COMSOL
- LS-DYNA

## 相场模拟

### 基本原理

**相场变量?*
- 序参?- 连续场变?- 界面弥散

**Allen-Cahn 方程?*
$$\frac{\partial\phi}{\partial t} = -L\frac{\delta F}{\delta \phi}$$

**Cahn-Hilliard 方程?*
$$\frac{\partial c}{\partial t} = \nabla \cdot M\nabla\frac{\delta F}{\delta c}$$

### 应用领域

**凝固过程?*
- 枝晶生长
- 共晶凝固
- 包晶反应

**相变?*
- 马氏体相?- 脱溶分解
- 珠光体转?
**晶粒长大?*
- 正常晶粒长大
- 异常晶粒长大
- 织构演化

**裂纹扩展?*
- 脆断?- 疲劳裂纹
- 应力腐蚀

### 常用软件

- MOOSE
- OpenPhase
- PRISMS-PF
- Custom codes

## CALPHAD 方法

### 基本原理

**热力学平衡：**
- 吉布斯自由能朢小化
- 化学势相?- 相稳定条?
**自由能模型：**
$$G = \sum_i x_i^0G_i + RT\sum_i x_i\ln x_i + G^{excess}$$

### 相图计算

**二元相图?*
- L-S（液-固）平衡
- 固溶体模?- 中间?
**三元相图?*
- 等温截面
- 垂直截面
- 液相面投?
### 热力学数据库

**常用数据库：**
- SGTE（Scientific Group Thermodata Europe?- THERMOL
- JMatPro

**应用?*
- 合金设计
- 工艺优化
- 性能预测

### 常用软件

- Thermo-Calc
- Pandat
- FactSage
- OpenCalphad

## 多尺度模?
### 尺度层次

**电子尺度?*
- DFT
- 电子结构
- 纳秒

**原子尺度?*
- 分子动力?- 蒙特卡洛
- 微秒

**介观尺度?*
- 相场方法
- 位错动力?- 毫秒

**宏观尺度?*
- 有限?- 计算流体力学
- ?小时

### 多尺度方?
**分层方法?*
- 上尺度参数传?- 下尺度边界条?- 信息传?
**并发方法?*
- 自应分辨?- QC（准连续体）方法
- 无缝耦合

## 参资?
- Martin RM. *Electronic Structure: Basic Theory and Practical Methods*
- Allen MP, Tildesley DJ. *Computer Simulation of Liquids*
- 《计算材料学?- Tschopp M. *Introduction to Computational Materials Science*

## 相关条目

[[04_EngineeringAndTechnology/MechanicsAndMaterials/MaterialsScience/INDEX|MaterialsScience]], [[05_ComputerScience/ArtificialIntelligence/MachineLearning/INDEX|MachineLearning]], ComputationalChemistry, [[MaterialsGenome]]
