---
aliases:
  - 游戏物理
  - 物理引擎
  - Game Physics
  - Physics Engine
tags:
  - 物理
  - 碰撞检测
  - PhysX
  - 刚体
  - 计算机科学
created: 2026-06-27
updated: 2026-06-27
---

# 游戏物理

游戏物理是模拟现实世界物理规律的技术领域，通过数值计算实现物体的运动、碰撞、布料、流体等物理效果，为游戏提供真实感和交互性。

## 刚体动力学

### 基础概念

刚体（Rigid Body）是形状不会改变的物理对象：

- **质量（Mass）**：物体的惯性量度
- **质心（Center of Mass）**：质量分布的中心点
- **惯性张量（Inertia Tensor）**：旋转惯性的量度
- **速度（Velocity）**：线速度和角速度

### 运动方程

```
线性运动：
F = ma (牛顿第二定律)
v = v0 + at
x = x0 + v0t + 0.5at²

旋转运动：
τ = Iα (转动定律)
ω = ω0 + αt
θ = θ0 + ω0t + 0.5αt²

其中：
F = 力, m = 质量, a = 加速度
τ = 扭矩, I = 惯性张量, α = 角加速度
```

### 力的应用

- **重力**：G = mg，常用于全局力
- **推力**：在特定点施加力
- **扭矩**：产生旋转的力矩
- **弹簧力**：F = -kx，胡克定律
- **阻尼力**：F = -cv，速度相关阻力

### 数值积分

- **显式欧拉**：简单但不稳定，能量会增加
- **隐式欧拉**：稳定但耗能，能量会减少
- **半隐式欧拉**：Symplectic Euler，较好的平衡
- **Verlet 积分**：直接积分加速度，无速度存储
- **RK4（四阶龙格-库塔）**：高精度但计算量大

```csharp
// 半隐式欧拉积分示例
void SemiImplicitEuler(RigidBody body, float dt)
{
    body.Velocity += body.Force / body.Mass * dt;
    body.Position += body.Velocity * dt;
    
    body.AngularVelocity += body.Torque * body.InverseInertia * dt;
    body.Rotation += body.AngularVelocity * dt;
}
```

## 碰撞检测

### 碰撞检测阶段

碰撞检测通常分为两个阶段：

- **粗阶段（Broad Phase）**：快速排除不可能碰撞的对象对
- **细阶段（Narrow Phase）**：精确检测碰撞和计算碰撞信息

### Broad Phase 算法

- **空间分区**：均匀网格、四叉树/八叉树、BSP 树
- **排序扫描**：Sort and Sweep 算法
- **包围体层次（BVH）**：层次化包围盒树
- **动态 AABB 树**：动态轴对齐包围盒树

```
AABB 树示例：
        [Root AABB]
       /            \
  [AABB Left]    [AABB Right]
   /      \       /      \
[Obj1] [Obj2] [Obj3] [Obj4]
```

### Narrow Phase 算法

- **GJK 算法**：判断两个凸体是否相交
- **EPA 算法**：计算穿透深度和碰撞法线
- **SAT（分离轴定理）**：测试分离轴判断碰撞
- **球体碰撞**：简单的距离判断
- **AABB 碰撞**：轴对齐包围盒重叠测试

### 碰撞响应

碰撞响应处理碰撞后的物理行为：

- **冲量计算**：基于碰撞法线计算冲量
- **摩擦力**：切线方向的摩擦冲量
- **恢复系数**：碰撞弹性系数
- **碰撞点**：碰撞接触点计算

```csharp
// 碰撞响应冲量计算
Vector3 CalculateImpulse(ContactPoint contact)
{
    Vector3 relativeVelocity = bodyB.Velocity - bodyA.Velocity;
    float velocityAlongNormal = Vector3.Dot(relativeVelocity, contact.Normal);
    
    if (velocityAlongNormal > 0) return Vector3.zero;
    
    float e = Mathf.Min(bodyA.Restitution, bodyB.Restitution);
    float j = -(1 + e) * velocityAlongNormal;
    j /= bodyA.InverseMass + bodyB.InverseMass;
    
    return j * contact.Normal;
}
```

## 碰撞形状

### 基础形状

- **球体（Sphere）**：最简单的碰撞形状
- **胶囊体（Capsule）**：圆柱+半球，适合角色
- **盒体（Box）**：轴对齐或定向包围盒
- **凸包（Convex Hull）**：任意凸多面体

### 复合形状

- **Compound Shape**：多个基础形状组合
- **三角网格（Triangle Mesh）**：静态环境碰撞
- **高度场（Height Field）**：地形碰撞优化

### 形状选择原则

- **简单优先**：尽量使用最简单的碰撞形状
- **凸体要求**：物理引擎通常只支持凸体碰撞
- **凹体处理**：使用多个凸体组合表示凹体
- **性能考量**：球体 > 胶囊体 > 盒体 > 凸包 > 网格

## 布料模拟

### 质点-弹簧模型

布料模拟的经典方法：

- **质点**：布料的采样点
- **弹簧**：连接质点的弹性约束
- **结构弹簧**：水平和垂直方向
- **剪切弹簧**：对角线方向
- **弯曲弹簧**：抵抗弯曲的弹簧

```
质点-弹簧网络：
○───○───○───○
│╲ │╱ │╲ │╱ │
○───○───○───○
│╱ │╲ │╱ │╲ │
○───○───○───○

─ = 结构弹簧
╲╱ = 剪切弹簧
```

### 约束方法

- **位置基础动力学（PBD）**：直接修正位置满足约束
- **XPBD**：扩展的 PBD，更好的收敛性
- **迭代求解**：多次迭代逼近约束解

### 碰撞处理

- **自碰撞**：布料与自身的碰撞
- **环境碰撞**：布料与其他物体的碰撞
- **穿刺处理**：防止布料穿透物体
- **摩擦力**：布料表面的摩擦

## 流体模拟

### 粒子方法

- **SPH（光滑粒子流体动力学）**：基于粒子的流体模拟
- **位置基础流体（PBFluids）**：基于 PBD 的流体
- **FLIP/PIC**：混合粒子和网格的方法

### 网格方法

- **Euler 方法**：固定网格求解纳维-斯托克斯方程
- **MAC 网格**：交错网格存储速度分量
- **流体体积（VOF）**：追踪流体界面

### 实时流体

- **浅水方程**：简化 2D 流体模拟
- **流体贴图**：使用纹理模拟流体效果
- **屏幕空间流体**：在屏幕空间渲染流体

## 物理引擎

### PhysX（NVIDIA）

PhysX 是最广泛使用的商业物理引擎：

- **CPU/GPU 加速**：支持 GPU 硬件加速
- **刚体模拟**：完整的刚体动力学
- **布料模拟**：高质量布料系统
- **粒子系统**：粒子物理模拟
- **场景查询**：射线检测、重叠检测

### Havok

Havok 是另一款主流商业物理引擎：

- **高性能**：优化的刚体模拟
- **破坏系统**：可破坏的环境
- **布娃娃**：角色布娃娃系统
- **动画物理**：物理与动画融合

### 开源引擎

- **Bullet**：开源物理引擎，广泛用于电影和游戏
- **Box2D**：2D 物理引擎
- **Jolt Physics**：由 Horizon Zero Dawn 团队开发

### 引擎集成

```
物理引擎工作流：
Game Logic
    ↓
Physics World.Step()
    ├── Broad Phase
    ├── Narrow Phase
    ├── Constraint Solver
    └── Integration
    ↓
Collision Callbacks
    ↓
Game Logic Update
```

## 物理优化

### 性能优化

- **简化碰撞体**：使用最简单的碰撞形状
- **休眠机制**：静止物体进入休眠状态
- **空间分区**：优化 Broad Phase 性能
- **子步进**：固定物理更新频率

### 稳定性优化

- **约束迭代次数**：增加迭代提高稳定性
- **碰撞容差**：设置合适的碰撞容差
- **最大速度限制**：防止物体穿透
- **CCD（连续碰撞检测）**：快速物体使用 CCD

### 调试工具

- **可视化调试**：绘制碰撞形状和约束
- **物理统计**：性能统计信息
- **场景查询测试**：测试射线检测等查询

## 应用场景

### 角色物理

- **角色控制器**：胶囊体 + 覆盖检测
- **布娃娃系统**：角色死亡时的物理模拟
- **动画物理混合**：动画和物理的融合
- **IK（反向动力学）**：物理感知的 IK

### 载具物理

- **轮式载具**：轮胎模型和悬挂系统
- **飞行器**：空气动力学简化模型
- **船舶**：浮力和水阻力模拟

### 破坏系统

- **预定义破坏**：预先分割的破碎模型
- **程序化破坏**：运行时计算破碎
- **Voronoi 分割**：基于 Voronoi 图的破碎
- **碎片管理**：碎片的生命周期管理

## 相关链接

- [[UnrealEngine5]] - 虚幻引擎物理系统
- [[UnityDeep]] - Unity 物理系统
- [[RenderingPipeline]] - 渲染管线
- [[GameAI]] - 游戏 AI
