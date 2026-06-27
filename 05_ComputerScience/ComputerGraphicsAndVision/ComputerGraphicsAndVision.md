---
aliases: [ComputerGraphicsAndVision]
tags: ['ComputerGraphicsAndVision', 'ComputerGraphicsAndVision']
created: 2026-05-16
updated: 2026-05-16
---

# 计算机图形学与视觉完全指南

## 概述

计算机图形学（Computer Graphics）研究如何使用计算机生成、处理和显示图像。计算机视觉（Computer Vision）则研究如何让计算机理解和分析图像。二者共享大量数学基础，但方向相反：图形学从几何到图像，视觉从图像到语义。

---

## 一、图形渲染管线

渲染管线（Graphics Pipeline）是将 3D 场景转换为 2D 图像的一系列步骤。

### 1.1 管线阶段

```
顶点数据 → 顶点着色器 → 曲面细分 → 几何着色器 → 光栅化 → 片元着色器 → 输出合并 → 帧缓冲

  顶点着色器:    MVP 变换、逐顶点属性处理
  光栅化:       将图元（三角形）离散化为片元（像素候选）
  片元着色器:    逐像素计算颜色、光照、纹理采样
  输出合并:     深度测试、模板测试、混合、抗锯齿
```

### 1.2 顶点处理

```
输入: 模型空间顶点 (x, y, z, 1)
             │
             ▼
    Model Matrix (模型矩阵) — 将模型放到世界空间
             │
             ▼
    View Matrix (视图矩阵) — 将世界空间转换到相机空间
             │
             ▼
   Projection Matrix (投影矩阵) — 将相机空间转换到裁剪空间
             │
             ▼
   Perspective Division (透视除法) — 将齐次坐标归一化到 NDC
             │
             ▼
   Viewport Transform (视口变换) — NDC 映射到屏幕坐标
```

### 1.3 坐标系统与齐次坐标

齐次坐标用 $(x, y, z, w)$ 表示空间点，其中 $w=1$ 表示点，$w=0$ 表示方向向量。

```
平移矩阵:
[1 0 0 tx]   [x]   [x + tx]
[0 1 0 ty] · [y] = [y + ty]
[0 0 1 tz]   [z]   [z + tz]
[0 0 0 1 ]   [1]   [  1   ]

透视投影矩阵:
[f/aspect  0      0           0      ]
[   0      f      0           0      ]
[   0      0   (zF+zN)/(zN-zF) 2zFzN/(zN-zF)]
[   0      0     -1           0      ]
```

---

## 二、光照模型

### 2.1 Phong 光照模型

Phong 模型将光照分解为三个分量：

$$I = I_a k_a + I_d k_d (L \cdot N) + I_s k_s (R \cdot V)^n$$

其中：
- $I_a k_a$: 环境光（Ambient）— 模拟间接光照
- $I_d k_d (L \cdot N)$: 漫反射（Diffuse）— 朗伯反射
- $I_s k_s (R \cdot V)^n$: 镜面高光（Specular）— $n$ 控制高光锐利度

```
L: 光源方向（指向光源）
N: 表面法线
R: 反射向量 = 2(L·N)N - L
V: 视线方向
n: 光泽度 (Shininess)
```

### 2.2 着色模式对比

| 模式 | 频率 | 效果 | 性能 |
|------|------|------|------|
| Flat Shading | 逐三角形 | 块状着色，可见三角形边界 | 最快 |
| Gouraud Shading | 逐顶点（插值到像素） | 平滑过渡，但高光可能失真 | 中等 |
| Phong Shading | 逐像素插值法线 | 最平滑，高光准确 | 最慢 |

---

## 三、OpenGL / Vulkan 基础

```
OpenGL 渲染循环:
while (!window.shouldClose()) {
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);
    
    // 绑定着色器
    glUseProgram(shaderProgram);
    
    // 设置 uniform
    glUniformMatrix4fv(modelLoc, 1, GL_FALSE, &model[0][0]);
    
    // 绑定 VAO 并绘制
    glBindVertexArray(VAO);
    glDrawElements(GL_TRIANGLES, indexCount, GL_UNSIGNED_INT, 0);
    
    glfwSwapBuffers(window);
    glfwPollEvents();
}
```

```
Vulkan vs OpenGL:
  OpenGL: 单一线程、全局状态机、驱动负责内存管理、DSL（高级）
  Vulkan:  多线程命令缓冲、显式状态、显式内存管理、底层控制
```

---

## 四、光线追踪

### 4.1 Whitted 风格光线追踪

Whitted 风格光线追踪递归地追踪反射和折射光线。

```
从相机出发，每个像素发射一条光线:
  1. 与场景求交 → 找到最近的交点
  2. 连接光源 → 阴影测试
  3. 递归追踪反射光线 (反射方向)
  4. 递归追踪折射光线 (斯涅尔定律)
  5. 累加所有贡献 → 像素颜色

反射方向:
  R = 2(N · L)N - L

折射方向 (Snell's Law):
  η₁ sin(θ₁) = η₂ sin(θ₂)
```

### 4.2 路径追踪

路径追踪是蒙特卡洛方法在渲染中的应用，通过随机采样路径来求解渲染方程：

$$L_o(p, \omega_o) = L_e(p, \omega_o) + \int_{\Omega} f_r(p, \omega_i, \omega_o) L_i(p, \omega_i) (\omega_i \cdot n) d\omega_i$$

### 4.3 光栅化 vs 光线追踪

| 特性 | 光栅化 | 光线追踪 |
|------|--------|----------|
| 原理 | 几何 → 图像（正向） | 图像 ← 几何（逆向） |
| 速度 | 极快（实时） | 较慢（离线/硬件加速后实时） |
| 反射/折射 | 需要技巧（环境贴图等） | 自然支持 |
| 全局光照 | 模拟（AO、IBL） | 物理精确 |
| 硬件 | GPU 原生支持 | RT Core (NVIDIA RTX) 加速 |
| 应用 | 游戏、实时渲染 | 影视特效、建筑可视化 |

---

## 五、纹理映射

纹理映射将 2D 图像包裹到 3D 表面上。

```
纹理坐标 (UV):
  (0,1) ──────── (1,1)
    │             │
    │   纹理图像   │
    │             │
  (0,0) ──────── (1,0)

纹理过滤:
  最近邻 (Nearest): 像素风格，无插值（适合像素艺术）
  双线性 (Bilinear): 4 个 texel 插值（平滑）
  各向异性 (Anisotropic): 斜视角时更高质量

Mipmap 链:
  原始纹理 → 1/2 分辨率 → 1/4 → 1/8 → ...
  自动选择合适级别避免锯齿
```

---

## 六、抗锯齿

抗锯齿（Anti-Aliasing, AA）技术用于减少锯齿状边缘。

| 技术 | 原理 | 性能开销 | 质量 |
|------|------|----------|------|
| SSAA | 高分辨率渲染后下采样 | 极大 | 最好 |
| MSAA | 多重采样（仅边缘超采样） | 中等 | 良好 |
| FXAA | 后处理边缘检测模糊 | 极小 | 一般 |
| TAA | 利用帧间信息时间采样 | 小 | 优秀（有鬼影） |

---

## 七、几何建模

| 表示方法 | 优点 | 缺点 | 应用 |
|----------|------|------|------|
| 多边形网格 | 简单、广泛支持 | 曲面需要大量面 | 游戏、实时渲染 |
| NURBS | 精确光滑、控制点少 | 求交复杂 | CAD 工业设计 |
| 细分曲面 | 任意拓扑、光滑 | 计算较慢 | 动画电影（Pixar） |
| 隐式曲面 | 布尔运算简单 | 渲染困难 | CSG 建模 |

---

## 八、动画

| 类型 | 原理 | 应用场景 |
|------|------|----------|
| 关键帧动画 | 插值关键姿态 | 物体变换、简单角色 |
| 骨骼动画 | 蒙皮 + 骨骼层级变换 | 角色动画（游戏、电影） |
| 变形目标 (Blend Shape) | 多形态线性插值 | 面部表情 |
| 物理仿真 | 力学模拟驱动 | 布料、头发、流体 |

```
骨骼动画矩阵计算:
  最终顶点位置 = M_model · Σ(w_i · M_bind_i^{-1} · M_bone_i) · v_local
  
  M_bind_i:   骨骼 i 的绑定姿势矩阵
  M_bone_i:   骨骼 i 的当前姿势矩阵
  M_bind_i^{-1} · M_bone_i: 骨骼 i 从绑定到当前的变换
  w_i:        顶点对骨骼 i 的权重
```

---

## 九、GPU 架构与 CUDA

```
GPU 核心架构:
           ┌──────────────────────┐
           │    GPU (设备)        │
           ├──────────────────────┤
           │  SM 0    │  SM 1     │
           │  ┌────┐   ┌────┐    │
           │  │Core│   │Core│    │
           │  │... │   │... │    │
           │  └────┘   └────┘    │
           │  Shared Memory       │
           ├──────────────────────┤
           │  Global Memory (VRAM)│
           └──────────────────────┘

CUDA 编程模型:
  CPU (Host) → 调用 Kernel → GPU (Device) 执行
  Thread < Warp (32) < Block < Grid
  Memory: Global > Shared > Register (速度递增，容量递减)
```

```cuda
__global__ void addVectors(float* a, float* b, float* c, int n) {
    int i = blockIdx.x * blockDim.x + threadIdx.x;
    if (i < n) {
        c[i] = a[i] + b[i];
    }
}

// 调用: addVectors<<<numBlocks, blockSize>>>(d_a, d_b, d_c, N);
```

---

## 相关条目

- [[05_ComputerScience/ArtificialIntelligence/ComputerVision/ComputerVision|ComputerVision]]
- Mathematics/Geometry
- [[04_EngineeringAndTechnology/ElectronicsAndCommunications/SignalProcessing/ImageProcessing|ImageProcessing]]
- [[05_ComputerScience/EngineeringDevelopment/GameDevelopment/GameDevelopment|GameDevelopment]]

## 参考资源

- 《Fundamentals of Computer Graphics》— Shirley 等
- 《Ray Tracing in One Weekend》— Peter Shirley
- 《Real-Time Rendering》— Akenine-Möller 等
- OpenGL 官方文档: https://www.opengl.org/documentation
- Vulkan 教程: https://vulkan-tutorial.com
- NVIDIA CUDA 文档: https://docs.nvidia.com/cuda


