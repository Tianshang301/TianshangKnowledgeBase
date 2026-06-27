---
aliases:
  - 图形学渲染
  - 图形API
  - Graphics Rendering
  - 光线追踪
tags:
  - Vulkan
  - DirectX
  - 光线追踪
  - 全局光照
  - 计算机科学
created: 2026-06-27
updated: 2026-06-27
---

# 图形学渲染

图形学渲染是将 3D 场景转换为 2D 图像的技术，涉及图形 API、渲染算法、光照模型等多个层面，是游戏和可视化应用的核心技术。

## Vulkan

### 设计哲学

Vulkan 是 Khronos Group 的新一代图形 API：

- **低开销**：最小化驱动层开销
- **显式控制**：开发者完全控制 GPU 资源
- **多线程友好**：原生支持多线程命令录制
- **跨平台**：支持 Windows、Linux、Android、iOS（通过 MoltenVK）

### 核心概念

```cpp
// Vulkan 核心对象
VkInstance          // 实例，连接应用和 Vulkan 运行时
VkPhysicalDevice    // 物理设备，GPU 硬件
VkDevice            // 逻辑设备，与 GPU 交互的接口
VkQueue             // 队列，提交命令到 GPU
VkCommandBuffer     // 命令缓冲区，录制 GPU 命令
VkSwapchain         // 交换链，管理呈现缓冲区
VkPipeline          // 管线，定义渲染状态
VkRenderPass        // 渲染通道，定义附件和子通道
VkFramebuffer       // 帧缓冲区，绑定附件
VkDescriptorSet     // 描述符集，绑定资源到着色器
```

### 命令录制

```cpp
// 命令缓冲区录制
VkCommandBufferBeginInfo beginInfo{};
beginInfo.sType = VK_STRUCTURE_TYPE_COMMAND_BUFFER_BEGIN_INFO;

vkBeginCommandBuffer(commandBuffer, &beginInfo);

VkRenderPassBeginInfo renderPassInfo{};
renderPassInfo.sType = VK_STRUCTURE_TYPE_RENDER_PASS_BEGIN_INFO;
renderPassInfo.renderPass = renderPass;
renderPassInfo.framebuffer = framebuffer;
renderPassInfo.renderArea = {{0, 0}, extent};

vkCmdBeginRenderPass(commandBuffer, &renderPassInfo, VK_SUBPASS_CONTENTS_INLINE);
vkCmdBindPipeline(commandBuffer, VK_PIPELINE_BIND_POINT_GRAPHICS, pipeline);
vkCmdDraw(commandBuffer, 3, 1, 0, 0);
vkCmdEndRenderPass(commandBuffer);

vkEndCommandBuffer(commandBuffer);
```

### 同步机制

- **Fence**：CPU-GPU 同步
- **Semaphore**：GPU-GPU 同步
- **Barrier**：资源状态转换
- **Pipeline Barrier**：管线阶段同步

### 内存管理

- **内存类型**：设备本地、主机可见、主机缓存等
- **内存分配**：手动管理 GPU 内存
- **缓冲区创建**：顶点、索引、Uniform 缓冲区
- **图像创建**：纹理、附件、存储图像

## DirectX 12

### 核心特性

DirectX 12 是 Microsoft 的低级图形 API：

- **显式资源管理**：开发者管理资源状态和生命周期
- **命令列表**：多线程命令录制
- **根签名**：定义着色器资源布局
- **描述符堆**：管理描述符的堆结构

### 关键概念

```cpp
// DX12 核心对象
ID3D12Device            // 设备接口
ID3D12CommandQueue      // 命令队列
ID3D12CommandAllocator  // 命令分配器
ID3D12GraphicsCommandList // 图形命令列表
ID3D12PipelineState     // 管线状态对象
ID3D12RootSignature     // 根签名
ID3D12DescriptorHeap    // 描述符堆
ID3D12Resource          // 资源（缓冲区、纹理）
```

### 资源屏障

```cpp
// 资源状态转换
D3D12_RESOURCE_BARRIER barrier{};
barrier.Type = D3D12_RESOURCE_BARRIER_TYPE_TRANSITION;
barrier.Transition.pResource = renderTarget;
barrier.Transition.StateBefore = D3D12_RESOURCE_STATE_PRESENT;
barrier.Transition.StateAfter = D3D12_RESOURCE_STATE_RENDER_TARGET;

commandList->ResourceBarrier(1, &barrier);
```

### DX12 与 Vulkan 对比

| 特性 | DirectX 12 | Vulkan |
|------|-----------|--------|
| 平台 | Windows/Xbox | 跨平台 |
| 着色器 | HLSL | GLSL/SPIR-V |
| 调试工具 | PIX | RenderDoc |
| 学习曲线 | 较陡 | 较陡 |
| 市场份额 | PC 游戏主流 | 移动/跨平台 |

## 光线追踪

### 基本原理

光线追踪（Ray Tracing）模拟光线的物理传播：

- **光线投射**：从相机发射光线穿过像素
- **求交测试**：光线与场景几何体求交
- **着色计算**：在交点计算颜色
- **递归追踪**：反射和折射光线的递归追踪

### 光线追踪算法

```
光线追踪流程：
Camera → Ray Generation
    ↓
Scene Intersection
    ├── 直接光照
    ├── 反射光线 → 递归追踪
    ├── 折射光线 → 递归追踪
    └── 阴影光线 → 光源可见性测试
    ↓
颜色累积 → 像素颜色
```

### 硬件加速

现代 GPU 的光线追踪硬件：

- **RT Core**：NVIDIA 的光线追踪硬件单元
- **BVH 遍历**：硬件加速的 BVH 遍历
- **求交测试**：硬件加速的光线-三角形求交
- **API 支持**：DXR、Vulkan RT、Metal RT

### 混合渲染

实际应用中通常使用混合渲染：

- **光栅化主通道**：主要几何体使用光栅化
- **光线追踪效果**：选择性使用光线追踪
  - 反射（Ray Traced Reflections）
  - 阴影（Ray Traced Shadows）
  - 全局光照（Ray Traced GI）
  - 环境光遮蔽（Ray Traced AO）

## 全局光照

### 全局光照概述

全局光照（Global Illumination）模拟光线在场景中的多次反弹：

- **直接光照**：光源直接照射到表面的光照
- **间接光照**：光线经多次反弹后的光照
- **颜色渗色**：物体颜色对周围环境的影响
- **柔和阴影**：面光源产生的柔和阴影

### 实时 GI 技术

- **Light Probes**：空间中的光照采样点
- **Reflection Probes**：环境反射探针
- **Lightmaps**：预烘焙的光照贴图
- **SSGI**：屏幕空间全局光照
- **VXGI**：体素全局光照
- **DDGI**：动态漫反射全局光照

### Lumen（UE5）

Lumen 是 UE5 的全动态 GI 系统：

- **多种追踪方式**：Screen Tracing、SDF Tracing、Hardware RT
- **Surface Cache**：缓存表面信息加速追踪
- **无限反弹**：支持无限次光照反弹
- **自适应质量**：根据性能自动调整质量

### GI 算法比较

| 技术 | 动态 | 质量 | 性能开销 |
|------|------|------|---------|
| Lightmap | 否 | 高 | 运行时低 |
| Light Probes | 是 | 中 | 低 |
| SSGI | 是 | 中低 | 中 |
| VXGI | 是 | 中高 | 高 |
| Ray Traced GI | 是 | 高 | 很高 |

## 体积渲染

### 体积效果

- **体积雾（Volumetric Fog）**：空间中的雾效果
- **体积云（Volumetric Clouds）**：程序化云朵渲染
- **体积光（Volumetric Lighting）**：光线散射效果（God Rays）
- **烟雾/火焰**：基于物理的烟雾和火焰效果

### 渲染技术

- **Ray Marching**：沿光线步进采样体积
- **光照累积**：在体积中累积光照散射
- **相位函数**：描述光在介质中的散射方向
- **Beer-Lambert 定律**：光在介质中的衰减

## 后处理效果

### 常见后处理

- **Bloom**：高亮区域泛光效果
- **Tone Mapping**：HDR 到 LDR 的色调映射
- **抗锯齿**：FXAA、TAA、MSAA
- **景深（DOF）**：模拟相机景深效果
- **运动模糊**：模拟相机运动模糊
- **色差（Chromatic Aberration）**：模拟镜头色差
- **暗角（Vignette）**：画面边缘变暗

### 屏幕空间技术

- **SSAO**：屏幕空间环境光遮蔽
- **SSR**：屏幕空间反射
- **SSGI**：屏幕空间全局光照
- **屏幕空间阴影**：改进近距离阴影质量

## 渲染优化

### GPU 优化

- **减少 Draw Call**：合批、实例化
- **减少 Overdraw**：前到后排序、Early-Z
- **减少带宽**：压缩纹理、减少 Render Target
- **着色器优化**：减少分支、降低精度

### 渲染策略

- **LOD 系统**：多级细节层次
- **遮挡剔除**：不渲染被遮挡物体
- **视锥体剔除**：剔除视锥体外物体
- **小物体剔除**：剔除屏幕上的微小物体

### 分辨率策略

- **动态分辨率**：根据负载调整渲染分辨率
- **棋盘渲染**：棋盘格式的像素着色
- **时间超采样**：利用前帧信息提升分辨率
- **注视点渲染**：中心高分辨率、边缘低分辨率

## 现代渲染趋势

- **光线追踪普及**：硬件 RT 的广泛应用
- **AI 超采样**：DLSS、FSR、XeSS
- **虚拟化几何**：Nanite 等技术
- **全动态 GI**：Lumen 等实时 GI 方案
- **GPU 驱动渲染**：更多逻辑移至 GPU

## 相关链接

- [[RenderingPipeline]] - 3D 渲染管线
- [[UnrealEngine5]] - 虚幻引擎 5
- [[UnityDeep]] - Unity 深度
- [[GamePhysics]] - 游戏物理
