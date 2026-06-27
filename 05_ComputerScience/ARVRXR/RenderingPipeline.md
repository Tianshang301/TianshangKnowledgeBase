---
aliases:
  - 3D渲染管线
  - 渲染管线
  - Rendering Pipeline
  - 图形管线
tags:
  - 渲染管线
  - 图形学
  - Shader
  - 光栅化
  - 计算机科学
created: 2026-06-27
updated: 2026-06-27
---

# 3D渲染管线

渲染管线（Rendering Pipeline）是将 3D 场景描述转换为 2D 图像的完整处理流程，定义了从顶点数据到最终像素的各个处理阶段。

## 管线概述

### 传统渲染管线

传统图形管线分为三个主要阶段：

```
应用程序阶段 (Application)
    ↓
几何阶段 (Geometry)
    ↓
光栅化阶段 (Rasterization)
```

### 现代可编程管线

现代 GPU 管线引入了可编程着色器：

- **顶点着色器（Vertex Shader）**：逐顶点处理
- **曲面细分着色器（Tessellation Shader）**：细分几何体
- **几何着色器（Geometry Shader）**：逐图元处理
- **片段着色器（Fragment/Pixel Shader）**：逐像素处理
- **计算着色器（Compute Shader）**：通用计算

## 顶点阶段

### 顶点着色器

顶点着色器是管线的第一个可编程阶段：

- **模型变换**：将顶点从模型空间变换到世界空间
- **视图变换**：从世界空间变换到相机空间
- **投影变换**：从相机空间变换到裁剪空间
- **顶点属性处理**：法线、纹理坐标、颜色等

```glsl
// 顶点着色器示例
#version 330 core
layout (location = 0) in vec3 aPos;
layout (location = 1) in vec3 aNormal;
layout (location = 2) in vec2 aTexCoord;

uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;

out vec3 FragPos;
out vec3 Normal;
out vec2 TexCoord;

void main() {
    FragPos = vec3(model * vec4(aPos, 1.0));
    Normal = mat3(transpose(inverse(model))) * aNormal;
    TexCoord = aTexCoord;
    gl_Position = projection * view * vec4(FragPos, 1.0);
}
```

### 曲面细分

曲面细分（Tessellation）在运行时增加几何细节：

- **Hull Shader**：定义细分参数和控制点
- **Tessellator**：硬件固定功能，生成细分坐标
- **Domain Shader**：根据细分坐标计算最终顶点位置
- **应用场景**：地形 LOD、角色细节、置换贴图

### 几何着色器

几何着色器处理完整的图元（点、线、三角形）：

- **图元生成**：可以生成新的图元
- **图元丢弃**：可以剔除不需要的图元
- **应用场景**：粒子系统、轮廓线、阴影体

## 裁剪与屏幕映射

### 裁剪阶段

裁剪（Clipping）移除视锥体外的几何体：

- **视锥体裁剪**：移除相机视锥体外的图元
- **用户裁剪平面**：自定义裁剪平面
- **齐次裁剪**：在裁剪空间中进行裁剪判断
- **图元分割**：跨越裁剪边界的图元被分割

### 背面剔除

背面剔除（Back-face Culling）优化渲染性能：

- **面朝向判断**：通过叉积判断三角形朝向
- **剔除模式**：剔除正面、背面或两者
- **双面渲染**：某些材质需要双面渲染

### 屏幕映射

将裁剪后的坐标映射到屏幕坐标：

- **视口变换**：映射到指定的屏幕区域
- **深度范围**：映射到深度缓冲范围 [0, 1]
- **坐标系转换**：处理不同 API 的坐标系差异

## 光栅化阶段

### 三角形设置

三角形设置（Triangle Setup）准备光栅化数据：

- **边方程计算**：计算三角形三条边的方程
- **增量计算**：准备逐像素的增量值
- **属性插值准备**：准备顶点属性的插值参数

### 三角形遍历

三角形遍历（Triangle Traversal）确定哪些像素被覆盖：

- **扫描线算法**：逐行扫描确定覆盖像素
- **边界判断**：判断像素中心是否在三角形内
- **子像素精度**：亚像素级别的覆盖判断
- **多重采样**：MSAA 在子采样点进行覆盖判断

### 片段着色器

片段着色器计算每个像素的最终颜色：

```glsl
// 片段着色器示例 - Blinn-Phong 光照
#version 330 core
in vec3 FragPos;
in vec3 Normal;
in vec2 TexCoord;

uniform vec3 lightPos;
uniform vec3 viewPos;
uniform vec3 lightColor;
uniform sampler2D diffuseTexture;

out vec4 FragColor;

void main() {
    vec3 diffuse = texture(diffuseTexture, TexCoord).rgb;
    
    // Ambient
    vec3 ambient = 0.1 * lightColor;
    
    // Diffuse
    vec3 norm = normalize(Normal);
    vec3 lightDir = normalize(lightPos - FragPos);
    float diff = max(dot(norm, lightDir), 0.0);
    vec3 diffuseLight = diff * lightColor;
    
    // Specular
    vec3 viewDir = normalize(viewPos - FragPos);
    vec3 halfDir = normalize(lightDir + viewDir);
    float spec = pow(max(dot(norm, halfDir), 0.0), 32.0);
    vec3 specular = spec * lightColor;
    
    FragColor = vec4((ambient + diffuseLight + specular) * diffuse, 1.0);
}
```

### 逐片段操作

- **模板测试（Stencil Test）**：基于模板缓冲的像素过滤
- **深度测试（Depth Test）**：Z-buffer 深度比较
- **混合（Blending）**：透明度混合和颜色混合
- **抖动（Dithering）**：减少色带的颜色量化

## 延迟渲染

### 延迟渲染管线

延迟渲染（Deferred Rendering）将光照计算延迟到屏幕空间：

- **几何通道（G-Buffer Pass）**：渲染几何信息到多个 Render Target
- **光照通道（Lighting Pass）**：在屏幕空间计算光照
- **G-Buffer 内容**：位置、法线、漫反射、高光等

### G-Buffer 布局

```
G-Buffer 0: RGB = Albedo, A = Specular
G-Buffer 1: RGB = World Normal, A = Roughness
G-Buffer 2: RGB = World Position, A = Metallic
G-Buffer 3: RGB = Emission, A = AO
```

### 延迟渲染优缺点

**优点**：
- 光源数量不影响几何复杂度
- 光照计算与场景复杂度解耦
- 便于实现屏幕空间效果

**缺点**：
- 显存占用大（多个 Render Target）
- 不支持透明物体（需要单独处理）
- MSAA 支持复杂

### 延迟渲染变体

- **Tiled Deferred Rendering**：分块延迟渲染
- **Clustered Deferred Rendering**：聚类延迟渲染
- **Forward+**：前向渲染 + 分块光照剔除

## 前向渲染与比较

### 前向渲染

前向渲染（Forward Rendering）是传统渲染方式：

- **逐物体渲染**：每个物体依次渲染
- **逐光源计算**：每个物体计算所有影响光源
- **光源数量限制**：多光源性能下降严重
- **透明物体支持**：天然支持透明物体

### 渲染路径选择

| 特性 | 前向渲染 | 延迟渲染 |
|------|---------|---------|
| 光源数量 | 受限 | 无限制 |
| 透明物体 | 支持 | 需额外处理 |
| MSAA | 支持 | 复杂 |
| 显存占用 | 低 | 高 |
| 带宽需求 | 低 | 高 |

## 高级渲染技术

### 阴影渲染

- **Shadow Mapping**：从光源视角渲染深度图
- **Cascaded Shadow Maps**：分层级联阴影
- **Shadow Volumes**：基于几何的阴影体
- **Percentage Closer Filtering**：软阴影过滤

### 后处理效果

- **Bloom**：高亮区域泛光效果
- **SSAO**：屏幕空间环境光遮蔽
- **SSR**：屏幕空间反射
- **DOF**：景深效果
- **Motion Blur**：运动模糊
- **Tone Mapping**：色调映射
- **Anti-aliasing**：FXAA、TAA 等抗锯齿

## 性能优化

### GPU 优化策略

- **Draw Call 合并**：减少 CPU 到 GPU 的调用次数
- **实例化渲染**：批量渲染相同网格
- **LOD 系统**：根据距离调整细节层次
- **遮挡剔除**：不渲染被遮挡的物体
- **纹理压缩**：减少显存和带宽占用

### 着色器优化

- **避免动态分支**：减少 GPU 分支预测开销
- **减少纹理采样**：合并纹理或降低采样频率
- **精度优化**：使用 half/mediump 精度
- **数学优化**：使用近似函数替代复杂计算

## 相关链接

- [[05_ComputerScience/GameEngineDevelopment/GraphicsRendering|GraphicsRendering]] - 图形学渲染
- [[05_ComputerScience/GameEngineDevelopment/UnityDeep|UnityDeep]] - Unity 深度
- [[05_ComputerScience/GameEngineDevelopment/UnrealEngine5|UnrealEngine5]] - 虚幻引擎 5
- [[XRInteractionDesign]] - XR 交互设计

