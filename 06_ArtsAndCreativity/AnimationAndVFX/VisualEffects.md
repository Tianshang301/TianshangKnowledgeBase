---
aliases:
  - 视觉特效
  - Visual Effects
  - VFX
tags:
  - vfx
  - animation
  - arts
  - creativity
created: 2026-06-27
updated: 2026-06-27
---

# 视觉特效

视觉特效（Visual Effects，简称 VFX）是通过数字技术创造或增强画面中无法通过实拍获得的视觉元素。从好莱坞大片中的爆炸场景到天气预报中的虚拟背景，VFX 已渗透到视觉媒体的方方面面。

## 粒子系统（Particle System）

粒子系统是 VFX 中最基础也最强大的工具之一，用于模拟大量微小元素的集合行为，如火焰、烟雾、雨雪、灰尘、魔法效果等。

### 核心概念

- **发射器（Emitter）**：粒子产生的源头，控制粒子的发射位置、速率和方向
- **粒子属性**：包括生命周期（Lifetime）、速度（Velocity）、大小（Size）、颜色（Color）、旋转（Rotation）等
- **力场（Force Fields）**：风力、重力、涡旋等外部力影响粒子运动轨迹
- **碰撞检测（Collision）**：粒子与场景物体的交互，如雨滴落在地面溅起水花

### 粒子渲染方式

- **点精灵（Point Sprite）**：最简单的渲染方式，每个粒子是一个面向摄像机的面片
- **实例化渲染（Instanced Rendering）**：将粒子替换为复杂几何体，如树叶、碎片
- **体积渲染（Volume Rendering）**：用于烟雾、云层等半透明体积效果

### 高级粒子技术

GPU 加速粒子系统允许同时模拟数百万粒子。Houdini 的 VEX 和 Niagara（Unreal Engine）支持程序化粒子行为控制。集群粒子（Clustered Particles）和层级粒子系统可以创建复杂的连锁反应效果。

## 流体模拟（Fluid Simulation）

流体模拟用于创建逼真的液体和气体运动效果，是 VFX 中计算密集度最高的领域之一。

### 模拟方法

- **欧拉方法（Eulerian）**：在固定网格上计算流体属性变化，适合大规模水体
- **拉格朗日方法（Lagrangian）**：跟踪单个粒子的运动轨迹，如 SPH（Smoothed Particle Hydrodynamics）
- **FLIP/APIC 方法**：结合两者优势的混合方法，是目前主流水体模拟方案

### 流体模拟应用

| 应用场景 | 技术方案 | 代表工具 |
|---------|---------|---------|
| 海洋表面 | 波浪叠加 + FFT | Houdini Ocean |
| 水花飞溅 | SPH/FLIP 粒子 | Houdini FLIP |
| 烟雾火焰 | Navier-Stokes 方程 | Phoenix FD, Houdini Pyro |
| 布料模拟 | 弹簧-质点系统/有限元 | Marvelous Designer |

## 刚体动力学（Rigid Body Dynamics）

刚体动力学模拟硬质物体的物理运动，包括碰撞、反弹、碎裂等效果。

### 核心参数

- **质量（Mass）**：决定物体的惯性和碰撞响应
- **摩擦力（Friction）**：控制表面接触时的阻力
- **弹性系数（Restitution/Bounciness）**：决定碰撞后的反弹程度
- **碰撞形状（Collision Shape）**：Box、Sphere、Convex Hull、Mesh 等

### 碎裂效果

Voronoi 碎裂是最常用的预计算碎裂方法。通过在物体内部生成 Voronoi 图，将模型分割为多个碎片。高级碎裂系统支持**层次化碎裂**——先大块碎裂，碎片再细碎。Bullet Physics 和 Houdini 的 RBD Solver 是主流的刚体求解器。

## 绿幕抠像（Chroma Keying）

绿幕抠像是将拍摄主体从单一颜色背景中分离出来的技术，是影视合成的基础环节。

### 抠像技术分类

- **色度键（Chroma Key）**：基于颜色差异进行抠像，绿幕和蓝幕最常用
- **亮度键（Luminance Key）**：基于亮度差异抠像，适用于高对比度场景
- **差异键（Difference Key）**：通过对比有背景和无背景的画面进行抠像
- **深度学习抠像**：如 MODNet、BackgroundMattingV2，可实现无绿幕的实时抠像

### 抠像质量优化

1. **灯光均匀**：绿幕照明不均会导致抠像边缘不干净
2. **避免溢色（Spill）**：绿色反射到主体边缘需要单独处理
3. **边缘处理（Edge Treatment）**：使用 Core Matte 和 Edge Matte 分层处理
4. **运动模糊保留**：确保快速运动的区域不被过度侵蚀

## 合成（Compositing）

合成是将多个视觉元素组合为最终画面的过程，是 VFX 流水线的最后也是最关键的环节。

### 合成工作流程

1. **分层渲染（Render Passes/AOV）**：将 Diffuse、Specular、Shadow、Reflection 等分别输出
2. **颜色校正（Color Correction）**：统一不同来源素材的色调和曝光
3. **匹配运动（Match Moving）**：将 CG 元素与实拍画面的摄像机运动对齐
4. **景深与运动模糊（DOF & Motion Blur）**：后期添加或增强这些摄影效果
5. **最终调色（Grading）**：统一画面风格和情感基调

### 合成软件

- **Nuke**：影视合成行业标准，节点式工作流，支持深度合成（Deep Compositing）
- **Fusion**：DaVinci Resolve 内置，与调色无缝衔接
- **After Effects**：适合动态设计和中小规模合成项目
- **Natron**：开源节点式合成软件

## 实践建议

1. 从简单的粒子效果开始，逐步挑战复杂的物理模拟
2. 理解物理原理比记忆软件操作更重要——知道"为什么"才能应对新情况
3. 学习基本的摄影和灯光知识，这对实拍素材的 VFX 处理至关重要
4. 建立标准化的文件管理和版本控制流程，VFX 项目通常涉及大量资产
5. 关注实时 VFX 的发展——游戏引擎中的特效制作正在快速成长
