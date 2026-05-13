# 图像处理

## 定义
图像处理是对图像进行分析、变换和处理的技术，包括图像增强、压缩、分割和特征提取等。是计算机视觉和模式识别的基础。

## 研究对象
- 数字图像的表示与模型
- 图像增强与复原
- 图像压缩编码
- 图像分割与特征提取

## 核心内容

### 数字图像表示

**灰度图像**：
- 像素值范围：0（黑）~ 255（白）
- 存储：$f(x,y)$，$x$ 为行，$y$ 为列

**彩色图像**：
- RGB模型：红、绿、蓝三通道
- HSV模型：色调、饱和度、亮度
- YCbCr模型：亮度、色度（用于视频压缩）

**图像分辨率**：
- 空间分辨率：像素数量（如1920×1080）
- 灰度分辨率：量化位数（8bit=256级）

### 图像增强

**直方图均衡化**：

$$s = T(r) = (L-1)\int_0^r p_r(w)dw$$

将灰度分布从非均匀变为均匀分布，增强对比度。

**空间域滤波**：
- 均值滤波：$g(x,y) = \frac{1}{mn}\sum_{(s,t)\in S}f(s,t)$
- 中值滤波：取邻域像素值的中值，去椒盐噪声
- 锐化滤波：拉普拉斯算子 $\nabla^2 f = \frac{\partial^2 f}{\partial x^2} + \frac{\partial^2 f}{\partial y^2}$

**频率域滤波**：
- 低通滤波：去除高频噪声
- 高通滤波：增强边缘
- 带通滤波：选择特定频率

### 图像压缩

**JPEG压缩原理**：
1. 颜色空间转换：RGB→YCbCr
2. 色度子采样：4:2:0
3. DCT变换：$8\times8$ 块
4. 量化：减少数据量
5. Z字形扫描
6. 熵编码：霍夫曼编码

**压缩性能指标**：
- 压缩比：$CR = \frac{原始大小}{压缩大小}$
- 峰值信噪比：$PSNR = 10\log_{10}\frac{255^2}{MSE}$

**其他压缩标准**：
- JPEG2000：小波变换
- H.264/AVC：视频压缩
- H.265/HEVC：高效视频压缩

### 边缘检测

**一阶导数算子**：
- Sobel算子：$G_x = \begin{pmatrix}-1&0&1\\-2&0&2\\-1&0&1\end{pmatrix}$
- Prewitt算子

**二阶导数算子**：
- Laplac算子：$\nabla^2 f = f(x+1,y)+f(x-1,y)+f(x,y+1)+f(x,y-1)-4f(x,y)$

**Canny边缘检测**：
1. 高斯滤波平滑
2. 计算梯度幅值和方向
3. 非极大值抑制
4. 双阈值检测和边缘连接

### 图像分割

**阈值分割**：
- 全局阈值：$g(x,y) = \begin{cases}1 & f(x,y)>T \\ 0 & \text{otherwise}\end{cases}$
- Otsu自适应阈值：最大类间方差法

**区域生长**：
- 选择种子点
- 根据相似准则合并邻域像素
- 直到满足停止条件

**分水岭算法**：
- 将图像视为地形
- 模拟从低处注水
- 分水岭线即为分割边界

### 形态学处理

**基本运算**：
- 腐蚀：$A\ominus B = \{z|(B)_z \subseteq A\}$
- 膨胀：$A\oplus B = \{z|(\hat{B})_z \cap A \neq \emptyset\}$
- 开运算：$A\circ B = (A\ominus B)\oplus B$
- 闭运算：$A\bullet B = (A\oplus B)\ominus B$

**应用**：
- 去除小噪声
- 分离连接的物体
- 填充孔洞
- 提取骨架

## 经典教材
- 阮秋琦《数字图像处理》
- Gonzalez《Digital Image Processing》
-冈萨雷斯《数字图像处理（MATLAB版）》
- Szeliski《Computer Vision: Algorithms and Applications》

## 主要应用领域
- 医学影像（CT、MRI、X光分析）
- 遥感图像处理
- 工业检测（缺陷检测）
- 安防监控（人脸识别）
- 自动驾驶（道路检测）
- 文档扫描（OCR）

## 相关条目

- [[DigitalSignalProcessing]]
- [[ComputerVision]]
- [[02_NaturalSciences/Physics/Optics/INDEX|Optics]]
- [[ArtificialIntelligence]]
- [[IC_Design]]
