---
aliases: [MedicalDevices]
tags: ['Biotechnologies', 'BiomedicalEngineering', 'MedicalDevices']
created: 2026-05-16
updated: 2026-05-16
---

# 医疗器械

## 定义
医疗器械是用于人体疾病诊断、治疗、监护的仪器、设备、材料的统称。

## 核心内容

### 医疗器械分类

**按风险等级**：
- Ⅰ类：低风险（手术器械、听诊器）
- Ⅱ类：中风险（B 超、心电图机）
- Ⅲ类：高风险（心脏起搏器、人工关节）

**按用途**：
- 诊断设备：医学影像、体外诊断
- 治疗设备：手术设备、放疗设备
- 监护设备：心电监护、血氧监测
- 植入器械：人工关节、心脏支架

### 医学影像设备

**X 射线设备**：
- DR（数字 X 线摄影）
- CT（计算机断层扫描）
- DSA（数字减影血管造影）

**X 射线衰减规律**（Beer-Lambert）：
$$I = I_0 e^{-\mu x}$$

**CT 值（Hounsfield 单位）**：
$$HU = 1000 \times \frac{\mu - \mu_{water}}{\mu_{water}}$$

**超声设备**：
- B 超：二维超声成像
- 彩色多普勒：血流成像
- 三维超声：立体成像

**多普勒频移**：
$$\Delta f = \frac{2f_0 v \cos\theta}{c}$$

其中 $f_0$ 为发射频率，$v$ 为血流速度，$\theta$ 为声束与血流方向夹角。

| 成像 modality | 物理原理 | 空间分辨率 | 有无电离辐射 | 典型应用 |
|:---|:---|---:|:---:|:---|
| X 光 | 光电效应/康普顿散射 | ~0.1 mm | 有 | 骨骼、胸部 |
| CT | 多角度 X 射线重建 | ~0.5 mm | 有 | 肿瘤、血管 |
| MRI | 核磁共振 | ~1 mm | 无 | 软组织、脑 |
| 超声 | 声波反射 | ~1 mm | 无 | 产科、心脏 |
| PET | 正电子湮灭 | ~4 mm | 有 | 代谢成像 |

**磁共振成像（MRI）**：
- T1加权像、T2加权像
- 功能 MRI（fMRI）
- 弥散加权成像（DWI）

**核医学设备**：
- PET（正电子发射断层扫描）
- SPECT（单光子发射计算机断层）

### 治疗设备

**手术设备**：
- 高频电刀
- 超声刀
- 激光手术器

**放疗设备**：
- 直线加速器
- γ刀
- 质子治疗

**康复设备**：
- 人工关节
- 心脏起搏器
- 人工晶体

### 医疗器械法规

**注册分类**：Ⅰ类备案、Ⅱ类注册、Ⅲ类注册

**质量体系**：ISO 13485

**临床评价**：临床试验、同品种对比

## 经典教材
- 《医疗器械原理与设计》
- Webster《Medical Instrumentation》
- Bronzino《The Biomedical Engineering Handbook》
- 《医疗器械监督管理条例》

## 主要应用领域
- 医学影像诊断
- 临床检验
- 手术治疗
- 康复治疗
- 家庭健康监测
- 远程医疗

## 相关条目
- [[Biomaterials]]
- [[09_MedicineAndHealth/Pharmacy/DrugDesign|DrugDesign]]
- [[04_EngineeringAndTechnology/MechanicalAndElectricalEngineering/InstrumentScience/SensorTechnology|SensorTechnology]]
- [[04_EngineeringAndTechnology/MechanicalAndElectricalEngineering/InstrumentScience/MeasurementTheory|MeasurementTheory]]
- [[04_EngineeringAndTechnology/MechanicalAndElectricalEngineering/OpticalEngineering/LaserTechnology|LaserTechnology]]


