# 计算机图形学

## 概述

计算机图形学（Computer Graphics）研究如何使用计算机生成、处理和显示图像。从实时的游戏渲染到影视级别的离线渲染，图形学是现代数字娱乐、工业设计和科学可视化的核心技术基础。

---

## 一、图形渲染管线

### 1.1 完整的渲染管线

现代的渲染管线包含可编程和固定功能的多个阶段：

```
顶点输入 (Vertex Data)
    ↓
顶点着色器 (Vertex Shader) — 可编程, MVP 变换, 逐顶点属性
    ↓
曲面细分 (Tessellation) — 控制着色器 + 评估着色器 (可选)
    ↓
几何着色器 (Geometry Shader) — 增删改图元 (可选)
    ↓
光栅化 (Rasterization) — 图元离散化为片元 (固定功能)
    ↓
片元着色器 (Fragment Shader) — 可编程, 逐像素颜色/光照
    ↓
输出合并 (Output Merger) — 深度测试, 模板测试, 混合, 抗锯齿
    ↓
帧缓冲 (Framebuffer)
```

### 1.2 顶点处理与坐标变换

```
模型空间 (Local/Space)  ── Model Matrix ──▶ 世界空间 (World Space)
世界空间                  ── View Matrix ──▶ 相机空间 (View/Eye Space)
相机空间                  ── Projection ──▶ 裁剪空间 (Clip Space)
裁剪空间                  ── 透视除法 ──▶  NDC ([-1, 1]³)
NDC                      ── 视口变换 ──▶  屏幕空间 (Screen Space)
```

### 1.3 投影矩阵

**透视投影矩阵：**

$$
P = \begin{pmatrix}
\frac{1}{r \tan(fov/2)} & 0 & 0 & 0 \\
0 & \frac{1}{\tan(fov/2)} & 0 & 0 \\
0 & 0 & \frac{f+n}{n-f} & \frac{2fn}{n-f} \\
0 & 0 & -1 & 0
\end{pmatrix}
$$

其中 $fov$ 为视场角，$r$ 为宽高比，$n$ 为近平面，$f$ 为远平面。

**正交投影矩阵：**

$$
P = \begin{pmatrix}
\frac{2}{r-l} & 0 & 0 & -\frac{r+l}{r-l} \\
0 & \frac{2}{t-b} & 0 & -\frac{t+b}{t-b} \\
0 & 0 & \frac{2}{n-f} & -\frac{f+n}{n-f} \\
0 & 0 & 0 & 1
\end{pmatrix}
$$

**投影对比：**

| 特性 | 透视投影 | 正交投影 |
|------|----------|----------|
| 视体 | 平截头体 (Frustum) | 长方体 |
| 近大远小 | 是 | 否 |
| 应用 | 游戏、影视（人眼透视） | CAD、蓝图、2D 游戏 |
| w 分量 | 变换后 ≠ 1 | 变换后 = 1 |
| 透视除法后 | 产生深度非线性 | 深度线性 |

---

## 二、着色与光照

### 2.1 Phong 反射模型

Phong 模型将光照分解为三个分量：

$$I = k_a I_a + k_d I_d (L \cdot N) + k_s I_s (R \cdot V)^\alpha$$

| 分量 | 物理含义 | 公式 | 不依赖于 |
|------|----------|------|----------|
| 环境光 (Ambient) | 模拟间接光照散射 | $k_a I_a$ | 光源方向、视角 |
| 漫反射 (Diffuse) | 粗糙表面的散射 | $k_d I_d (L \cdot N)$ | 视角方向 |
| 镜面高光 (Specular) | 光滑表面的直接反射 | $k_s I_s (R \cdot V)^\alpha$ | 材质粗糙度 $\alpha$ |

### 2.2 Blinn-Phong 模型

Blinn-Phong 用半程向量 $H$ 代替反射向量 $R$，效率更高：

$$I_{spec} = k_s I_s (N \cdot H)^\alpha$$

其中半程向量 $H = \frac{L + V}{\|L + V\|}$。

### 2.3 PBR (Physically Based Rendering)

PBR 基于真实物理的光照模型，核心是 Cook-Torrance BRDF：

$$f_r(p, \omega_i, \omega_o) = k_d \frac{c}{\pi} + k_s \frac{DFG}{4(\omega_o \cdot n)(\omega_i \cdot n)}$$

| 项 | 含义 | 公式 |
|------|------|------|
| D (法线分布函数) | 微表面法线分布 | GGX/Trowbridge-Reitz |
| F (菲涅尔方程) | 视角相关反射率 | Schlick 近似 |
| G (几何函数) | 微表面互相遮蔽 | Smith GGX |

### 2.4 着色模式对比

| 模式 | 计算频率 | 效果 | 性能 |
|------|----------|------|------|
| Flat Shading | 逐三角形 | 块状着色，可见面边界 | 最快 |
| Gouraud Shading | 逐顶点 → 插值到片元 | 平滑但高光易失真 | 较快 |
| Phong Shading | 逐片元插值法线 | 高光精确平滑 | 较慢 |
| PBR Shading | 逐片元 + 纹理采样 | 最真实 | 最慢 |

---

## 三、光线追踪

### 3.1 Whitted 风格光线追踪

```
每像素主光线 (Primary Ray):
  1. 从相机经过像素发射光线
  2. 求最近交点
  3. 从交点向光源发射阴影光线 → 阴影
  4. 递归发射反射光线 (Phong 反射定律)
  5. 递归发射折射光线 (Snell 定律)
  6. 合并所有光贡献

反射方向:
  R = 2(N · L)N - L

折射 (Snell 定律):
  η₁ sin θ₁ = η₂ sin θ₂
```

### 3.2 路径追踪

路径追踪使用蒙特卡洛方法求解渲染方程：

$$L_o(p, \omega_o) = L_e(p, \omega_o) + \int_{\Omega} f_r(p, \omega_i, \omega_o) L_i(p, \omega_i) (\omega_i \cdot n) d\omega_i$$

**核心优化技术：**

| 技术 | 描述 | 效果 |
|------|------|------|
| Monte Carlo Integration | 随机采样近似积分 | 有噪点，随采样数增加收敛 |
| Importance Sampling | 按照 BRDF 分布采样 | 降低方差 |
| Russian Roulette | 概率终止路径 | 无偏，减少计算量 |
| Next Event Estimation (NEE) | 直接对光源采样 | 减少 Indirect 噪声 |
| Multiple Importance Sampling (MIS) | 混合多种采样策略 | 平衡直接/间接贡献 |

### 3.3 光栅化 vs 光线追踪

| 特性 | 光栅化 | 光线追踪 |
|------|--------|----------|
| 原理 | 几何变换 → 离散化 | 模拟光线物理传播 |
| 实时性 | 60+ FPS（原生） | 需 RT Core + DLSS |
| 反射 | 环境贴图 (SSR) | 物理精确 |
| 折射 | 近似 (Fake) | 物理精确 |
| 全局光照 | Lightmap, AO, IBL | 物理精确 |
| 阴影 | Shadow Map（有偏） | 精确硬/软阴影 |
| 硬件支持 | 所有 GPU | RTX (NVIDIA), RDNA2 (AMD) |
| 开发复杂度 | 较低 | 较高 |

---

## 四、GPU 架构与图形 API

### 4.1 GPU 架构概览

```
GPU 核心架构:
  ┌──────────────────────────────────┐
  │            GPU 芯片               │
  ├──────────────────────────────────┤
  │  GPC 0    │  GPC 1    │  GPC 2   │
  │  ┌────┐   │  ┌────┐   │  ┌────┐  │
  │  │SM  │   │  │SM  │   │  │SM  │  │  Streaming
  │  │SM  │   │  │SM  │   │  │SM  │  │  Multiprocessor
  │  └────┘   │  └────┘   │  └────┘  │
  ├───────────┴───────────┴──────────┤
  │      L2 Cache + Memory Ctrl      │
  └──────────────────────────────────┘
```

每 SM 包含：CUDA Cores、Tensor Cores (AI)、RT Cores (光线追踪)、Shared Memory、Register File、Warp Scheduler。

### 4.2 OpenGL vs Vulkan vs WebGPU

| 特性 | OpenGL 4.x | Vulkan 1.x | WebGPU |
|------|-----------|------------|--------|
| 年代 | 1992 | 2016 | 2023 |
| 状态管理 | 全局状态机 | 显式状态对象 | 显式状态对象 |
| 线程 | 单线程 | 支持多线程命令缓冲 | 支持多线程 |
| 着色器语言 | GLSL | GLSL/HLSL/SPIR-V | WGSL |
| 驱动开销 | 高 | 低 | 低 |
| 调试 | ARB_debug_output | Validation Layers | 内置 |
| 跨平台 | Windows/Linux/macOS | Windows/Linux/Android | 所有现代浏览器 |
| 内存管理 | 隐式 | 显式 | 半自动 |
| 学习曲线 | 中等 | 陡峭 | 中等 |
| 适合场景 | 学习、原型、遗留系统 | 高性能实时渲染 | Web、跨平台新开发 |

---

## 五、几何建模

| 表示方法 | 优点 | 缺点 | 典型应用 |
|----------|------|------|----------|
| 多边形网格 (Mesh) | 简单、广泛支持 | 曲面需大量三角形 | 游戏、实时渲染 |
| NURBS | 精确光滑、控制点少 | 求交复杂、实时困难 | CAD、工业设计 |
| 细分曲面 (Subdivision Surface) | 任意拓扑、光滑连续 | 需要细分步骤 | 动画电影 (Pixar) |
| 隐式曲面 (SDF) | 布尔运算简单 | 渲染/动画困难 | CSG、体积建模 |
| 点云 (Point Cloud) | 直接从扫描获取 | 无拓扑信息 | 3D 扫描、LiDAR |
| 体素 (Voxel) | 规则网格、布尔运算简单 | 占用大量内存 | 医学影像、游戏 (Minecraft) |

---

## 六、动画

| 类型 | 原理 | 优点 | 缺点 |
|------|------|------|------|
| 关键帧动画 | 插值关键帧姿态 | 可控性强 | 人工工作量大 |
| 骨骼动画 (Skinning) | 骨架 + 蒙皮权重 | 表现丰富 | 需要绑定过程 |
| 变形目标 (Blend Shape) | 多目标形状线性混合 | 表情自然 | 存储量大 |
| 物理模拟 | 物理方程驱动 | 真实自发行为 | 不可预测、控制难 |

**线性混合蒙皮 (Linear Blend Skinning)：**

$$v' = \sum_{i=1}^{n} w_i \cdot (M_i \cdot M_{bind_i}^{-1}) \cdot v$$

其中 $w_i$ 为顶点对骨骼 $i$ 的权重，$M_i$ 为骨骼 $i$ 的当前世界矩阵，$M_{bind_i}$ 为绑定姿势矩阵。

---

## 七、高级渲染技术

| 技术 | 描述 | 应用 |
|------|------|------|
| 延迟渲染 (Deferred Shading) | 先几何 G-Buffer 后光照 | 多光源场景 |
| 屏幕空间反射 (SSR) | 从屏幕像素反向追踪 | 实时反射 |
| 环境光遮蔽 (AO) | 模拟角落阴影 | 增强立体感 |
| 体积光照 (Volumetric) | 介质中的光散射 | 雾效、光束 |
| 全局光照 (GI) | 间接光多次反弹 | 光照真实感 |
| 时域超分辨率 (TAAU) | 时序累加重建高分辨率 | DLSS、FSR、XeSS |

---

## 相关条目

- [[ComputerVision]]
- [[GameDevelopment]]
- Mathematics/Geometry
- [[ImageProcessing]]

## 参考资源

- 《Fundamentals of Computer Graphics》— Peter Shirley 等
- 《Real-Time Rendering》— Akenine-Möller 等
- 《Physically Based Rendering: From Theory to Implementation》— Pharr, Jakob, Humphreys
- 《Ray Tracing in One Weekend》— Peter Shirley
- OpenGL 官方文档: https://www.opengl.org/documentation
- Vulkan 教程: https://vulkan-tutorial.com
- WebGPU 规范: https://www.w3.org/TR/webgpu
- LearnOpenGL: https://learnopengl.com
- Scratchapixel: https://www.scratchapixel.com
