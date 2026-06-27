---
aliases:
  - 空间计算
  - Spatial Computing
  - 混合现实
tags:
  - 空间计算
  - VisionPro
  - 眼动追踪
  - 手势交互
  - 计算机科学
created: 2026-06-27
updated: 2026-06-27
---

# 空间计算

空间计算（Spatial Computing）是一种将计算融入三维物理空间的交互范式，用户通过自然的视线、手势和语音与数字内容交互，模糊了物理世界与数字世界的边界。

## Apple Vision Pro

### 硬件架构

Vision Pro 是 Apple 的空间计算设备，代表了当前最先进的技术集成：

- **M2 + R1 双芯片架构**：M2 负责计算，R1 专责传感器处理
- **12 个摄像头**：包括透视摄像头、眼动追踪摄像头、深度传感器
- **LiDAR 扫描仪**：实时深度感知和环境建模
- **Micro-OLED 显示屏**：单眼 4K 分辨率，2300 万像素
- **EyeSight**：外屏显示用户眼睛，支持社交感知

### visionOS 开发

visionOS 是空间计算的操作系统：

- **Window**：传统的 2D 窗口内容，可在空间中放置
- **Volume**：3D 体积内容，可从任意角度观察
- **Full Space**：完全沉浸式空间，替换现实环境
- **Shared Space**：多个应用共存的共享空间

```swift
// visionOS 窗口定义
@main
struct MyApp: App {
    var body: some Scene {
        WindowGroup {
            ContentView()
        }
        .windowStyle(.plain) // 无边框窗口
        
        Volume {
            Model3DView()
        }
        .volumeLayout(.fixed, size: CGSize(width: 1, height: 1, depth: 1))
    }
}
```

### RealityKit 增强

- **Entity Component System**：基于 ECS 的实体组件系统
- **MeshResource**：程序化生成和加载 3D 网格
- **Material System**：Physically Based Rendering 材质系统
- **Animation**：关键帧动画和骨骼动画支持
- **Spatial Audio**：空间音频集成

## 空间音频

### 基础概念

空间音频（Spatial Audio）是沉浸式体验的关键组成部分：

- **3D 音频定位**：在三维空间中精确定位声音来源
- **HRTF 渲染**：头部相关传输函数模拟声音传播
- **距离衰减**：声音随距离衰减的物理模拟
- **多普勒效应**：运动声源的频率变化模拟

### 音频场景

- **Ambisonics**：全景声格式，支持球形音频场
- **Object-based Audio**：基于对象的音频，独立定位每个声源
- **Scene-based Audio**：基于场景的音频混合
- **Binaural Rendering**：双耳渲染输出到耳机

### Apple 空间音频实现

```swift
// RealityKit 空间音频
let audioSource = AudioResource.load(named: "ambient.wav")
let audioEntity = Entity()
audioEntity.spatialAudio = SpatialAudioComponent(
    gain: -10,
    directivity: .beam(focus: 0.5),
    occlusion: .enabled
)
audioEntity.playAudio(audioSource)
```

### 音频设计原则

- **沉浸感优先**：音频应增强空间感而非分散注意力
- **物理真实性**：遵循声音传播的物理规律
- **交互反馈**：使用音频确认用户操作
- **环境氛围**：创建一致的音频环境氛围

## 手势交互

### 手部追踪

空间计算使用摄像头追踪手部姿态：

- **骨骼追踪**：追踪 26 个手部关节的 3D 位置
- **捏合检测**：拇指与食指的捏合手势
- **指向检测**：食指指向的方向
- **手掌检测**：手掌的朝向和位置

### 核心手势

Vision Pro 的核心交互手势：

- **捏合（Tap）**：拇指轻触食指，相当于点击
- **捏合拖动（Drag）**：捏合后移动手部，用于滚动和移动
- **注视+捏合**：先注视目标再捏合，精确选择
- **手指旋转**：双指旋转调整物体朝向

### 手势设计原则

- **自然直觉**：手势应符合人类自然动作习惯
- **容错性**：识别应有一定容错范围，避免误触
- **视觉反馈**：提供明确的视觉反馈确认手势识别
- **疲劳考虑**：避免需要长时间抬手的手势

### 手势 API

```swift
// SwiftUI 手势处理
struct ContentView: View {
    @State private var position: CGPoint = .zero
    
    var body: some View {
        Circle()
            .gesture(
                DragGesture()
                    .onChanged { value in
                        position = value.location
                    }
            )
            .hoverEffect(.highlight) // 注视高亮
    }
}
```

## 眼动追踪

### 技术原理

眼动追踪（Eye Tracking）是空间计算的革命性交互方式：

- **红外照明**：使用不可见红外光照射眼睛
- **瞳孔检测**：摄像头捕捉瞳孔位置和大小
- **注视点计算**：通过瞳孔位置计算 3D 空间中的注视点
- **校准系统**：个性化校准提高追踪精度

### 交互应用

- **注视选择**：注视目标后捏合选择
- **滚动控制**：注视边缘区域触发滚动
- **焦点深度**：根据注视距离调整渲染焦平面
- **用户意图预测**：通过注视模式预测用户意图

### 隐私保护

Apple 对眼动追踪数据的隐私保护：

- **本地处理**：眼动数据仅在设备本地处理
- **不共享数据**：不与应用开发者共享原始眼动数据
- **选择性交互**：应用只能知道用户是否注视其内容
- **隐私指示器**：使用眼动追踪时显示指示器

### 专注度检测

- **瞳孔直径**：瞳孔大小变化反映认知负荷
- **注视稳定性**：稳定的注视反映专注状态
- **眨眼频率**：眨眼模式与注意力相关
- **应用场景**：自适应内容呈现、疲劳检测

## 空间映射

### 环境理解

空间计算设备需要深度理解物理环境：

- **Mesh Reconstruction**：实时构建环境的 3D 网格
- **Plane Detection**：检测水平和垂直平面
- **Scene Understanding**：语义理解场景中的物体类型
- **Occlusion**：虚拟物体被真实物体正确遮挡

### 碰撞与物理

- **Physics Simulation**：虚拟物体与真实环境的物理交互
- **Collision Detection**：虚拟物体与真实网格的碰撞检测
- **Gravity Simulation**：虚拟物体受重力影响落在真实表面上
- **Portal Effect**：通过空间入口进入虚拟空间

## 开发框架对比

### Apple 生态

- **RealityKit**：Apple 的 3D 渲染和交互框架
- **ARKit**：底层 AR 能力提供者
- **RoomPlan**：房间扫描和建模
- **Compositor Services**：底层渲染控制

### 跨平台方案

- **Unity PolySpatial**：Unity 对 visionOS 的支持
- **WebXR**：Web 平台的 XR 标准
- **OpenXR**：开放的 XR 应用标准

## 未来展望

- **更自然的交互**：语音、手势、眼动的融合交互
- **环境智能**：设备对环境的深度理解和响应
- **协作体验**：多人共享的空间计算体验
- **健康应用**：眼动追踪在健康监测中的应用

## 相关链接

- [[VRDevelopment]] - VR 开发技术
- [[ARDevelopment]] - AR 开发技术
- [[XRInteractionDesign]] - XR 交互设计
- [[RenderingPipeline]] - 3D 渲染管线
