# 测绘科学与技术

## 学科定义
测绘科学与技术研究地球空间信息获取、处理、分析和表达的理论与方法。

## 核心公式

### 距离测量
视距测量公式：
$$D = K \cdot l \cdot \cos^2\theta$$

其中 $K$ 为视距乘常数（通常 $K=100$），$l$ 为视距间隔，$\theta$ 为竖直角。

### 水准测量高差
$$h = a - b$$

### 导线测量坐标增量
$$\Delta x = D \cdot \cos\alpha, \quad \Delta y = D \cdot \sin\alpha$$

### GPS定位基本方程
$$\rho_i = \sqrt{(x_i - x)^2 + (y_i - y)^2 + (z_i - z)^2} + c \cdot \delta t$$

### 三角测量（前方交会）
$$\tan\alpha = \frac{(x_B - x_A)\cot\beta + (y_B - y_A)}{(y_B - y_A)\cot\beta - (x_B - x_A)}$$

$$x_P = \frac{x_A\cot\beta + x_B\cot\alpha - y_A + y_B}{\cot\alpha + \cot\beta},\quad y_P = \frac{y_A\cot\beta + y_B\cot\alpha + x_A - x_B}{\cot\alpha + \cot\beta}$$

### 误差传播定律
$$\sigma_z^2 = \sum_{i=1}^n \left(\frac{\partial f}{\partial x_i}\right)^2 \sigma_{x_i}^2$$

对于线性函数 $z = a_1x_1 + a_2x_2 + \cdots + a_nx_n$：
$$\sigma_z^2 = a_1^2\sigma_{x_1}^2 + a_2^2\sigma_{x_2}^2 + \cdots + a_n^2\sigma_{x_n}^2$$

### 最小二乘平差
$$\hat{X} = (A^T P A)^{-1} A^T P L$$

## 测量方法比较

| 方法 | 精度 | 适用范围 | 效率 | 成本 |
|------|------|----------|------|------|
| 全站仪测量 | mm级 | 工程测量、控制网 | 中 | 中 |
| GPS定位 | cm~m级 | 大地测量、导航 | 高 | 中高 |
| 水准测量 | mm级 | 高程控制 | 低 | 低 |
| 摄影测量 | cm~m级 | 大面积测图 | 高 | 高 |
| 激光扫描 | mm~cm级 | 三维建模 | 高 | 高 |

## 研究对象
- 大地测量
- 摄影测量与遥感
- 地图学与GIS
- 工程测量

## 核心课程
- 测量学基础
- 大地测量学
- 摄影测量学
- 遥感原理
- 地理信息系统
- 误差理论与数据处理

## 学习路径
1. 基础阶段：测量学、数学、计算机基础
2. 专业基础：大地测量、摄影测量、遥感原理
3. 专业核心：GIS、数字测图、GPS定位
4. 专业拓展：InSAR、激光雷达、无人驾驶测量

## 经典教材
- 宁津生《测绘学概论》
- 李德仁《遥感导论》
- 孔祥元《大地测量学基础》
- 张祖勋《数字摄影测量学》

## 主要应用领域
- 国家基础测绘
- 工程建设测量
- 城市规划与管理
- 环境监测
- 智慧城市
- 自动驾驶导航

## 相关条目

- [[Cartography]]
- [[04_EngineeringAndTechnology/CivilEngineering/INDEX|CivilEngineering]]
- [[01_K12/JuniorHigh/Geography/INDEX|Geography]]
- GIS
