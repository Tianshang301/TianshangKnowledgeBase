---
aliases:
  - 虚幻引擎5
  - UE5
  - Unreal Engine 5
tags:
  - UE5
  - 游戏引擎
  - Nanite
  - Lumen
  - 计算机科学
created: 2026-06-27
updated: 2026-06-27
---

# 虚幻引擎5

Unreal Engine 5（UE5）是 Epic Games 开发的最新一代游戏引擎，引入了 Nanite、Lumen 等革命性技术，大幅提升了视觉质量和开发效率。

## Nanite 虚拟化几何体

### 技术原理

Nanite 是 UE5 的虚拟化微多边形几何系统：

- **虚拟化几何体**：将几何体虚拟化，按需加载细节
- **自动 LOD**：运行时自动生成和切换 LOD 层级
- **微多边形渲染**：支持电影级资产的实时渲染
- **GPU 驱动渲染**：完全由 GPU 驱动的渲染管线

### 工作流程

```
导入高精度模型（数百万多边形）
    ↓
Nanite 自动处理
    ├── 构建细节层级 (Cluster Hierarchy)
    ├── 量化顶点位置
    └── 压缩几何数据
    ↓
运行时渲染
    ├── 视锥体剔除
    ├── 遮挡剔除
    ├── 细节选择
    └── GPU 光栅化
```

### 使用限制

- **不支持骨骼网格**：目前仅支持静态网格
- **不支持半透明**：需要传统渲染路径
- **材质限制**：不支持 World Position Offset
- **性能考量**：极小三角形可能产生过度绘制

### 最佳实践

- **直接导入高模**：无需手动创建 LOD
- **合理使用材质**：避免过于复杂的材质图
- **内存管理**：注意 Nanite 的内存占用
- **性能分析**：使用 Nanite 可视化工具分析

## Lumen 全局光照

### 技术原理

Lumen 是 UE5 的全动态全局光照和反射系统：

- **无限反弹光照**：支持无限次光线反弹
- **实时更新**：完全动态，无需烘焙
- **多种追踪方式**：Screen Tracing、SDF Tracing、Hardware Ray Tracing
- **自适应降噪**：智能降噪减少噪点

### 追踪方式

- **Screen Space Tracing**：在屏幕空间快速追踪
- **Surface Cache**：缓存表面信息加速追踪
- **SDF Tracing**：有符号距离场追踪
- **Hardware Ray Tracing**：硬件加速光线追踪（可选）

### 配置选项

```
Lumen 设置：
├── 全局光照质量
│   ├── Final Gather Quality
│   ├── Max Trace Distance
│   └── Scene View Distance
├── 反射质量
│   ├── Reflection Method
│   └── Max Reflection Bounces
└── 性能设置
    ├── Software Ray Tracing Mode
    └── Hardware Ray Tracing (可选)
```

### 性能优化

- **调整追踪距离**：减少不必要的远距离追踪
- **降低反射质量**：根据平台调整反射精度
- **Hardware Ray Tracing**：支持 RT 的硬件可启用加速
- **Lumen Scene 更新频率**：根据需求调整更新频率

## MetaHuman

### 技术概述

MetaHuman 是创建高保真数字人类的完整框架：

- **MetaHuman Creator**：云端数字人创建工具
- **高精度面部**：基于扫描的真实面部数据
- **骨骼绑定**：标准化的面部骨骼系统
- **动画支持**：面部捕捉和程序化动画

### 创建流程

1. **选择基础模板**：从预设模板开始
2. **调整面部特征**：滑块调整五官细节
3. **选择发型和服装**：配置外观细节
4. **导出资产**：导出到 Unreal Engine

### 面部动画

- **面部捕捉**：支持 iPhone ARKit 面部捕捉
- **Audio to Speech**：语音驱动口型动画
- **Control Rig**：程序化面部动画控制
- **Blend Shape**：面部表情混合变形

### 性能优化

- **LOD 系统**：MetaHuman 内置多级 LOD
- **细节剔除**：根据距离剔除面部细节
- **GPU 优化**：面部渲染的 GPU 优化
- **移动端适配**：简化版本用于移动平台

## World Partition

### 系统概述

World Partition 是 UE5 的世界分区系统，替代了 World Composition：

- **自动分区**：自动将大世界分割为网格单元
- **按需加载**：根据玩家位置动态加载/卸载
- **流式加载**：无缝的流式世界加载
- **数据层**：支持不同数据层的独立管理

### 工作流程

```
大世界场景
    ↓
World Partition 自动分割
    ├── 按网格单元分割
    ├── 建立 Actor 层级
    └── 生成流式数据
    ↓
运行时
    ├── 检测玩家位置
    ├── 加载附近单元
    └── 卸载远处单元
```

### Data Layers

- **Runtime Data Layers**：运行时动态加载的数据层
- **Editor Data Layers**：编辑器中组织数据的层
- **HLOD**：分层 LOD 系统集成
- **Streaming Source**：定义流式加载源

### 最佳实践

- **合理设置网格大小**：根据场景密度调整
- **使用 HLOD**：为远处区域创建 HLOD
- **管理加载距离**：设置合适的加载/卸载距离
- **Data Layer 策略**：合理规划数据层

## 蓝图系统

### 蓝图概述

Blueprint 是 UE5 的可视化脚本系统：

- **节点编辑器**：可视化连接节点创建逻辑
- **完全集成**：与 C++ 完全互操作
- **快速原型**：快速实现游戏逻辑原型
- **设计师友好**：非程序员也能使用

### 蓝图类型

- **Blueprint Class**：可实例化的蓝图类
- **Level Blueprint**：关卡特定的蓝图逻辑
- **Animation Blueprint**：动画状态机和逻辑
- **Widget Blueprint**：UI 界面蓝图
- **Material Blueprint**：材质编辑器（节点材质）

### 蓝图最佳实践

- **避免过度使用**：复杂逻辑使用 C++
- **组织节点**：使用 Comment 和 Reroute 节点
- **命名规范**：清晰的变量和函数命名
- **性能注意**：避免每帧执行的复杂蓝图逻辑

### C++ 与蓝图交互

```cpp
// C++ 中暴露给蓝图
UCLASS(Blueprintable)
class AMyActor : public AActor
{
    GENERATED_BODY()
    
public:
    // 蓝图可调用函数
    UFUNCTION(BlueprintCallable, Category="MyActor")
    void DoSomething();
    
    // 蓝图可读写属性
    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category="MyActor")
    float Health;
    
    // 蓝图可实现事件
    UFUNCTION(BlueprintImplementableEvent, Category="MyActor")
    void OnDamageReceived(float Damage);
};
```

## 渲染特性

### Nanite + Lumen 协同

- **几何与光照解耦**：Nanite 处理几何，Lumen 处理光照
- **无缝集成**：两者协同工作提供最佳视觉效果
- **性能平衡**：可根据平台调整两者质量

### Virtual Shadow Maps

- **高分辨率阴影**：匹配 Nanite 几何细节的阴影
- **虚拟化**：类似 Nanite 的虚拟化阴影贴图
- **性能优化**：只渲染可见区域的阴影

### Temporal Super Resolution (TSR)

- **高质量上采样**：从低分辨率生成高质量图像
- **时间复用**：利用前帧信息提升质量
- **性能提升**：渲染较低分辨率后上采样

## 开发工作流

### 项目设置

- **模板选择**：根据项目类型选择合适模板
- **插件管理**：启用需要的引擎插件
- **平台设置**：配置目标平台和质量级别
- **版本控制**：集成 Perforce/Git 版本控制

### 资产管理

- **Content Browser**：组织和管理项目资产
- **Asset Registry**：资产注册和引用管理
- **Primary Asset**：主要资产和资产管理器
- **Size Map**：分析资产大小和依赖

### 调试工具

- **Unreal Insights**：性能分析工具
- **Stat 命令**：实时统计数据显示
- **Visual Logger**：可视化日志工具
- **Gameplay Debugger**：游戏逻辑调试

## 平台支持

### 目标平台

- **PC**：Windows、Mac、Linux
- **主机**：PlayStation、Xbox、Nintendo Switch
- **移动**：iOS、Android
- **XR**：VR、AR、MR 设备
- **Web**：WebGL（实验性）

### 性能目标

| 平台 | 目标帧率 | Nanite | Lumen |
|------|---------|--------|-------|
| 高端 PC | 60+ fps | 支持 | 支持 |
| 主机 | 30/60 fps | 支持 | 部分支持 |
| 移动端 | 30 fps | 不支持 | 不支持 |
| VR | 90 fps | 部分支持 | 部分支持 |

## 相关链接

- [[UnityDeep]] - Unity 引擎深度
- [[GraphicsRendering]] - 图形学渲染
- [[RenderingPipeline]] - 3D 渲染管线
- [[GamePhysics]] - 游戏物理
