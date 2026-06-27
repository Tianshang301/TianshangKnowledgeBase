---
aliases:
  - React Native深度
  - RN架构
  - React Native New Architecture
tags:
  - Mobile/CrossPlatform
  - ReactNative
  - JavaScript
created: 2026-06-28
updated: 2026-06-28
---

# React Native深度

React Native允许使用JavaScript/TypeScript构建原生移动应用，自2015年发布以来经历了多次架构演进。本文深入分析其新架构、原生模块系统、性能优化及与Flutter的对比。

## 架构演进

### 旧架构（Bridge架构）

React Native最初采用的三层架构：

- **JS层**：React组件、业务逻辑
- **Bridge层**：异步JSON序列化通信
- **Native层**：原生UI渲染、平台API

核心问题：
- Bridge是异步的，序列化/反序列化开销大
- 三线程模型（JS Thread、Shadow Thread、UI Thread）导致延迟
- 大列表滚动、手势处理等场景性能瓶颈明显

### New Architecture

2022年开始逐步推出的新架构，彻底重构了核心通信机制。

#### JSI（JavaScript Interface）

直接在C++层面暴露JavaScript引擎的API，替代Bridge。

- **同步调用**：JS可直接同步调用C++/Native方法
- **共享内存**：JS和Native共享HostObject，无需序列化
- **引擎无关**：理论上可适配不同JS引擎（Hermes、V8、JSC）
- **HostObject**：C++对象直接暴露给JS，属性访问触发C++ getter

#### Fabric

新的渲染系统，替代旧的UI Manager。

- **同步渲染**：JS可同步创建和更新Shadow Tree
- **Yoga同步执行**：布局计算可在JS线程同步完成
- **并发渲染**：支持React 18的Concurrent Features
- **组件映射**：Shadow Tree直接映射到Host Tree（原生View）
- **优先级调度**：支持高优先级更新（如手势响应）

#### TurboModules

替代旧的NativeModules系统。

- **懒加载**：模块在首次调用时才初始化，减少启动时间
- **类型安全**：通过Codegen生成类型安全的JS-Native接口
- **同步方法**：支持同步调用原生方法
- **共享模块**：多个ReactRoot可共享同一模块实例

#### Codegen

静态类型系统，确保JS-Native接口的类型安全。

- 从TypeScript/Flow类型定义生成C++/Java/ObjC接口代码
- 支持复杂类型：对象、数组、联合类型、Promise、回调
- 构建时生成，避免运行时类型检查开销

## 原生模块与桥接

### iOS原生模块（ObjC/Swift）

```objc
// ObjC实现
RCT_EXPORT_METHOD(getData:(NSString *)key
                  resolver:(RCTPromiseResolveBlock)resolve
                  rejecter:(RCTPromiseRejectBlock)reject) {
    // 原生实现
    resolve(result);
}
```

- 使用宏 `RCT_EXPORT_METHOD` 导出方法
- 支持Promise、回调、事件发送
- Swift需通过桥接头文件或NSObject暴露

### Android原生模块（Java/Kotlin）

```kotlin
@ReactMethod
fun getData(key: String, promise: Promise) {
    // 原生实现
    promise.resolve(result)
}
```

- 继承 `ReactContextBaseJavaModule`
- 使用 `@ReactMethod` 注解导出方法
- 通过 `@ReactModule` 注解声明模块名

### TurboModule原生模块

新架构下的模块定义更加类型安全：

```typescript
// JS接口定义（Spec）
export interface Spec extends TurboModule {
  getData(key: string): Promise<string>;
  multiply(a: number, b: number): number;
}
```

Codegen自动生成对应的C++接口，Native端实现该接口。

### 自定义View组件

- 旧架构：ViewManager + Props
- 新架构：ComponentDescriptor + ShadowNode + Props
- 支持自定义事件和命令

## 性能优化

### Hermes引擎

Meta专为React Native优化的JavaScript引擎。

- **AOT编译**：将JS编译为字节码，减少启动时的解析和JIT开销
- **启动速度**：相比JSC提升约2倍
- **内存占用**：更低的内存footprint
- **调试支持**：支持Chrome DevTools Protocol
- **ES6+支持**：完整支持现代JavaScript特性
- **Hermes 2.0**：进一步优化GC和正则表达式性能

### 列表优化

- **FlatList**：虚拟化列表，只渲染可见区域
  - `initialNumToRender`：首屏渲染数量
  - `maxToRenderPerBatch`：每批增量渲染数量
  - `windowSize`：可视区域外的渲染窗口大小
  - `removeClippedSubviews`：移除可视区域外的视图
- **SectionList**：分组列表，继承FlatList优化
- **FlashList**（Shopify）：基于recycling原理，性能更优

### 渲染优化

- **React.memo**：避免不必要的组件重渲染
- **useMemo/useCallback**：缓存计算结果和回调函数
- **避免内联样式**：使用StyleSheet.create预创建样式
- **InteractionManager**：将重计算推迟到动画/交互完成后
- **React.lazy + Suspense**：代码分割和懒加载

### 内存优化

- **图片优化**：使用合适的尺寸、格式，启用缓存
- **避免内存泄漏**：清理定时器、取消订阅、解除事件监听
- **Profile工具**：Flipper、React DevTools、Xcode/Android Studio内存分析

### 启动优化

- **预加载**：提前初始化常用模块
- **代码分割**：按需加载业务模块
- **Bundle拆分**：将JS Bundle拆分为主Bundle和按需加载Bundle
- **原生Splash Screen**：掩盖初始化时间

## 与Flutter对比

### 架构差异

| 维度 | React Native | Flutter |
|------|-------------|---------|
| 语言 | JavaScript/TypeScript | Dart |
| 渲染 | 原生组件 | 自绘引擎（Skia/Impeller） |
| UI映射 | 映射到平台原生View | 自己绘制所有像素 |
| 状态管理 | React范式（hooks/context） | Widget树 + setState/Provider/Riverpod |
| 热重载 | Fast Refresh | Hot Reload（更快更完整） |

### 性能对比

- **启动速度**：Flutter略快（AOT编译Dart），RN借助Hermes已大幅缩小差距
- **UI流畅度**：Flutter通常更稳定（无bridge开销），RN新架构已显著改善
- **包体积**：Flutter较大（自带引擎），RN较小
- **内存占用**：Flutter通常更高（引擎+Dart Runtime）

### 生态对比

- **RN优势**：npm生态庞大、Web开发者上手容易、可复用Web代码、社区成熟
- **Flutter优势**：UI一致性好、动画能力强、Google维护的Material Design组件、文档质量高
- **平台支持**：两者均支持iOS/Android/Web/Desktop

### 选择建议

- **选React Native**：团队有JS/React背景、需要与Web共享代码、大量使用原生平台特性
- **选Flutter**：UI一致性要求高、自定义UI复杂、追求最佳性能、新项目无历史包袱
- **两者都在快速演进**：实际选择应基于团队能力和项目需求
