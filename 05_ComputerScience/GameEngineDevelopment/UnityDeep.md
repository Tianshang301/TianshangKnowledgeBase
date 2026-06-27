---
aliases:
  - Unity深度
  - Unity高级开发
  - Unity ECS
  - Unity DOTS
tags:
  - Unity
  - ECS
  - DOTS
  - ShaderGraph
  - 计算机科学
created: 2026-06-27
updated: 2026-06-27
---

# Unity深度

Unity 是全球使用最广泛的游戏引擎之一，本篇深入探讨 Unity 的高级特性，包括 ECS/DOTS 架构、Shader Graph、渲染管线和资源管理等核心系统。

## ECS/DOTS 架构

### 核心概念

DOTS（Data-Oriented Technology Stack）是 Unity 的高性能技术栈：

- **Entity（实体）**：仅作为 ID 使用的轻量级标识符
- **Component（组件）**：纯数据容器，不包含逻辑
- **System（系统）**：处理组件数据的逻辑单元
- **World**：包含所有实体和系统的容器

### 与传统 OOP 对比

```
传统 OOP (MonoBehaviour):
GameObject
  ├── Transform (位置)
  ├── Renderer (渲染)
  └── Health (生命值)
  每个组件包含数据和逻辑

ECS 架构:
Entity ID: 42
  ├── LocalTransform (纯数据)
  ├── RenderMesh (纯数据)
  └── Health (纯数据)
  
System: HealthSystem (纯逻辑，处理所有 Health 组件)
System: RenderSystem (纯逻辑，处理所有渲染)
```

### 性能优势

- **缓存友好**：相同类型组件连续存储
- **并行处理**：System 可多线程并行执行
- **零开销抽象**：无虚函数调用开销
- **内存效率**：组件仅存储必要数据

### Burst Compiler

Burst 是 Unity 的高性能编译器：

- **LLVM 后端**：使用 LLVM 进行优化
- **SIMD 向量化**：自动利用 SIMD 指令
- **无 GC 分配**：避免垃圾回收
- **安全检查**：编译时检查内存安全

```csharp
[BurstCompile]
public partial struct MovementSystem : ISystem
{
    [BurstCompile]
    public void OnUpdate(ref SystemState state)
    {
        foreach (var (transform, velocity) in 
            SystemAPI.Query<RefRW<LocalTransform>, RefRO<Velocity>>())
        {
            transform.ValueRW.Position += 
                velocity.ValueRO.Value * SystemAPI.Time.DeltaTime;
        }
    }
}
```

### Jobs System

Unity 的多线程作业系统：

- **IJob**：基础作业接口
- **IJobParallelFor**：并行作业
- **IJobEntity**：基于实体的作业
- **JobHandle**：作业依赖管理

## Shader Graph

### 可视化着色器编辑

Shader Graph 是 Unity 的可视化着色器编辑器：

- **节点编辑**：拖拽节点创建着色器
- **实时预览**：即时查看着色器效果
- **PBR Master**：基于物理的渲染主节点
- **子图（Sub Graph）**：可复用的节点组

### 核心节点

- **Texture 2D**：纹理采样节点
- **Normal**：法线处理节点
- **Fresnel Effect**：菲涅尔效果
- **Triplanar**：三平面映射
- **Noise**：程序化噪声生成

### 自定义节点

```csharp
// 自定义 HLSL 节点
public class CustomNode : CodeFunctionNode
{
    public override string functionName => "CustomFunction";
    
    protected override string source => @"
        void CustomFunction_float(float3 input, out float3 output)
        {
            output = input * 0.5 + 0.5;
        }
    ";
}
```

### 着色器变体

- **Keyword 变体**：通过关键字切换效果
- **Shader Feature**：编辑时选择的变体
- **Multi Compile**：运行时可用的所有变体
- **变体管理**：减少变体数量优化编译

## 渲染管线

### URP（Universal Render Pipeline）

通用渲染管线，面向移动平台和中低端设备：

- **单通道前向渲染**：高效的前向渲染
- **可编程批处理器**：优化 Draw Call
- **Shader Stripping**：移除未使用的着色器代码
- **后处理集成**：内置后处理效果栈

```
URP 渲染流程：
├── 剔除（Culling）
│   ├── 视锥体剔除
│   └── 遮挡剔除
├── 渲染
│   ├── 不透明物体
│   ├── 天空盒
│   └── 透明物体
└── 后处理
    ├── 抗锯齿
    ├── Bloom
    └── 色调映射
```

### HDRP（High Definition Render Pipeline）

高清渲染管线，面向高端平台：

- **延迟渲染**：基于 Tile/Cluster 的延迟渲染
- **物理光照**：基于物理的光照模型
- **体积效果**：体积雾、体积云
- **光线追踪**：硬件加速光线追踪支持

### 管线对比

| 特性 | URP | HDRP |
|------|-----|------|
| 目标平台 | 移动/中端 | PC/主机 |
| 渲染路径 | 前向 | 延迟 |
| 光照模型 | 简化 PBR | 完整 PBR |
| 光线追踪 | 不支持 | 支持 |
| 性能开销 | 低 | 高 |

### 自定义渲染

- **Render Pass**：自定义渲染通道
- **Render Feature**：扩展渲染管线功能
- **Scriptable Render Context**：可编程渲染上下文
- **Command Buffer**：命令缓冲区

## Addressables

### 资源管理系统

Addressables 是 Unity 的资源管理和加载系统：

- **地址加载**：通过地址字符串加载资源
- **异步加载**：所有加载操作都是异步的
- **引用计数**：自动管理资源生命周期
- **远程加载**：支持从远程服务器加载

### 核心概念

```csharp
// 通过地址加载资源
async void LoadAsset()
{
    AsyncOperationHandle<GameObject> handle = 
        Addressables.LoadAssetAsync<GameObject>("prefabs/enemy");
    await handle.Task;
    Instantiate(handle.Result);
    
    // 释放资源
    Addressables.Release(handle);
}

// 通过标签加载多个资源
async void LoadByLabel()
{
    AsyncOperationHandle<IList<GameObject>> handle = 
        Addressables.LoadAssetsAsync<GameObject>("enemies", null);
    await handle.Task;
}
```

### Asset Groups

- **Group 设置**：将资源分组管理
- **打包策略**：决定资源如何打包
- **加载方式**：本地、远程或随构建
- **压缩选项**：LZ4、LZMA 等压缩方式

### Content Catalog

- **目录管理**：管理资源地址到实际路径的映射
- **版本控制**：目录的版本管理
- **远程更新**：支持目录的远程更新
- **多平台支持**：不同平台使用不同目录

## 性能优化

### CPU 优化

- **减少 GC 分配**：避免每帧分配内存
- **对象池**：复用频繁创建的对象
- **批处理合并**：减少 Draw Call
- **LOD 系统**：根据距离调整细节

### GPU 优化

- **减少 Overdraw**：优化渲染顺序
- **简化着色器**：降低着色器复杂度
- **纹理优化**：合理设置纹理尺寸和压缩
- **遮挡剔除**：不渲染被遮挡的物体

### 内存优化

- **纹理流式加载**：按需加载纹理 Mipmap
- **资源压缩**：使用合适的压缩格式
- **引用清理**：及时释放不用的资源
- **内存分析**：使用 Memory Profiler 分析

### Profiling 工具

- **Unity Profiler**：CPU/GPU/内存分析
- **Frame Debugger**：逐 Draw Call 调试
- **Memory Profiler**：内存快照分析
- **Profile Analyzer**：多帧数据分析

## 编辑器扩展

### 自定义编辑器

- **Custom Inspector**：自定义组件检查器
- **EditorWindow**：自定义编辑器窗口
- **PropertyDrawer**：自定义属性绘制
- **Gizmos**：场景内可视化

### 工具开发

- **ScriptableWizard**：向导式工具
- **Menu Item**：菜单命令扩展
- **Scene View**：场景视图交互
- **Asset Processor**：资源导入处理

### 自动化

- **Build Pipeline**：自动化构建流程
- **CI/CD 集成**：与持续集成系统集成
- **测试框架**：单元测试和集成测试
- **命令行构建**：无界面命令行构建

## 跨平台开发

### 平台抽象

- **Platform Dependent Compilation**：平台条件编译
- **Platform Abstraction Layer**：平台抽象层
- **Native Plugins**：原生插件集成
- **Platform Specific Assets**：平台特定资源

### 移动平台

- **Touch Input**：触摸输入处理
- **Mobile Performance**：移动端性能优化
- **App Bundle**：Android App Bundle 支持
- **Platform Services**：平台服务集成（IAP、广告等）

## 相关链接

- [[UnrealEngine5]] - 虚幻引擎 5
- [[RenderingPipeline]] - 3D 渲染管线
- [[GraphicsRendering]] - 图形学渲染
- [[GamePhysics]] - 游戏物理
