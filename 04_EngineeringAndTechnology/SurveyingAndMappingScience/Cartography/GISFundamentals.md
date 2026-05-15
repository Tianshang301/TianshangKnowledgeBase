---
aliases: [GISFundamentals]
tags: ['SurveyingAndMappingScience', 'Cartography', 'GISFundamentals']
---

# 地理信息系统

## 定义
地理信息系统（GIS）是用于采集、存储、管理、分析和显示地理空间数据的计算机系统。

## 核心内容

### GIS组成

**硬件**：服务器、工作站、输入输出设备

**软件**：ArcGIS、QGIS、SuperMap、MapGIS

**数据**：矢量数据、栅格数据

**人员**：数据生产、系统管理、应用开发

### 空间数据模型

**矢量模型**：
- 点：$P(x,y)$
- 线：$L = \{(x_1,y_1),(x_2,y_2),\ldots\}$
- 面：$A = \{(x_1,y_1),(x_2,y_2),\ldots,(x_n,y_n)\}$

**栅格模型**：
- 像元矩阵
- 分辨率：像元大小

### 空间数据库

**数据组织**：
- 图层（Layer）
- 要素类（Feature Class）
- 要素数据集（Feature Dataset）

**拓扑关系**：
- 邻接性
- 连通性
- 包含关系

### 空间分析

**叠置分析**：
- 交集、并集、差集
- 加权叠置

**缓冲区分析**：
- 点缓冲、线缓冲、面缓冲

**网络分析**：
- 最短路径
- 最优路径
- 服务区分析

**空间插值**：
- 反距离加权（IDW）
- 克里金插值
- 样条函数

### GIS开发

**WebGIS**：
- 地图服务发布
- 前端地图库：Leaflet、OpenLayers、Mapbox GL

**二次开发**：
- ArcGIS Engine
- QGIS API
- Python脚本

## 经典教材
- 龚健雅《地理信息系统基础》
- 《地理信息系统原理与方法》
- Longley《Geographic Information Systems and Science》
- 《ArcGIS从基础到实践》

## 主要应用领域
- 城市规划
- 国土管理
- 环境监测
- 交通导航
- 应急管理
- 智慧城市
