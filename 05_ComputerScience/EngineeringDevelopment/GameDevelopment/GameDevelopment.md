---
aliases: [GameDevelopment]
tags: ['EngineeringDevelopment', 'GameDevelopment']
created: 2026-05-17
updated: 2026-05-17
---

# 游戏开发 (Game Development)

## 概述

游戏开发是结合程序设计、美术设计、音效设计和游戏设计的综合性工程。现代游戏开发涉及复杂的数学物理模拟、高性能图形渲染、网络同步和人工智能等多个领域。

---

## 一、游戏引擎架构

### 1.1 核心架构

```
现代游戏引擎模块:
┌─────────────────────────────┐
│            工具层             │
│ (编辑器、资源管线、调试工具)   │
├─────────────────────────────┤
│            功能层             │
│ ┌──────┐ ┌──────┐ ┌──────┐ │
│ │渲染   │ │物理   │ │音效   │ │
│ │引擎   │ │引擎   │ │引擎   │ │
│ └──────┘ └──────┘ └──────┘ │
│ ┌──────┐ ┌──────┐ ┌──────┐ │
│ │AI     │ │网络   │ │动画   │ │
│ │系统   │ │系统   │ │系统   │ │
│ └──────┘ └──────┘ └──────┘ │
├─────────────────────────────┤
│           核心层              │
│ (游戏循环、资源管理、事件系统)  │
├─────────────────────────────┤
│           平台层              │
│ (DirectX, Vulkan, OpenGL, 平台 SDK)│
└─────────────────────────────┘
```

### 1.2 游戏循环

```
while (running) {
    ProcessInput();    // 处理输入
    Update(deltaTime); // 更新逻辑 (固定/可变时间步)
    Render();          // 渲染帧
}

固定时间步 (Fixed Timestep):
  const float FIXED_DT = 1.0f / 60.0f;
  float accumulator = 0.0f;
  
  while (running) {
      float frameTime = GetFrameTime();
      accumulator += frameTime;
      while (accumulator >= FIXED_DT) {
          FixedUpdate(FIXED_DT);
          accumulator -= FIXED_DT;
      }
      float alpha = accumulator / FIXED_DT;
      Render(alpha);  // 插值渲染
  }
}
```

### 1.3 帧率与时间步

| 指标 | 公式 | 说明 |
|------|------|------|
| 帧率 | $FPS = \dfrac{1}{\Delta t}$ | 每秒渲染帧数，$\Delta t$ 为帧间隔（秒）|
| 帧间隔 | $\Delta t = \dfrac{1}{FPS}$ | 相邻两帧的时间差 |
| 帧时间预算 | $t_{\text{budget}} \leq \dfrac{1000}{FPS_{\text{target}}}\;\text{ms}$ | 目标帧率下每帧最大耗时 |
| 渲染利用率 | $U = \dfrac{t_{\text{render}}}{t_{\text{budget}}} \times 100\%$ | GPU 时间占用百分比 |

**常见帧率目标：**

| 场景 | 目标 FPS | 帧预算 |
|------|----------|--------|
| 电影 | 24 FPS | 41.67 ms |
| 标准显示 | 30 FPS | 33.33 ms |
| 流畅游戏 | 60 FPS | 16.67 ms |
| 高刷新率 | 120 / 144 FPS | 8.33 / 6.94 ms |
| VR | 90 / 120 FPS | 11.11 / 8.33 ms |

### 1.4 Entity-Component-System (ECS)

ECS 是游戏开发中流行的架构模式，取代传统的深层次继承结构。

```
┌──────────┐    ┌──────────┐    ┌──────────┐
│ Entity   ├───►│ Position │    │ Movement │
│ (ID)     │    │ Component│    │ System   │
└──────────┘    │ x, y, z  │    │          │
                 └──────────┘    │MoveByVel │
┌──────────┐    ┌──────────┐    └──────────┘
│ Entity   ├───►│ Render   │    ┌──────────┐
│ (ID)     │    │ Component│    │ Render   │
└──────────┘    │ mesh,mat │    │ System   │
                 └──────────┘    └──────────┘
```

---

## 二、游戏引擎对比

| 引擎 | 语言 | 收费模式 | 适用平台 | 代表游戏 |
|------|------|----------|----------|----------|
| Unity | C# | 免费/Pro $2K/年 | 全平台 | 原神, 崩坏3, DOTA Underlords |
| Unreal Engine | C++, Blueprints | 免版税 (5% 收入超 $1M) | 全平台 | 黑神话悟空, 堡垒之夜 |
| Godot | GDScript, C#, C++ | 完全免费开源 | 多平台 | Cruelty Squad, Cassette Beasts |
| Cocos Creator | TypeScript | 免费 | 移动/Web | 开心消消乐 |
| Custom Engine | C/C++ | 开发成本高 | 自定义 | 使命召唤, FIFA |

---

## 三、2D 游戏开发

### 3.1 核心概念

```
精灵 (Sprite):
  纹理 → Sprite Renderer → 屏幕位置
  
瓦片地图 (Tilemap):
  网格化地图，每个格子对应一个瓦片纹理
  适用于: 平台游戏、RPG 地图

碰撞检测 (2D):
  轴对齐包围盒 (AABB): 
    if (a.x < b.x + b.w && a.x + a.w > b.x &&
        a.y < b.y + b.h && a.y + a.h > b.y)
        → 碰撞发生
  
  圆形碰撞:
    if (distance(a.pos, b.pos) < a.radius + b.radius)
        → 碰撞发生
```

### 3.2 2D 物理: Box2D

```
Box2D 工作流程:
  1. 创建物理世界 (World)
  2. 创建刚体 (Body: dynamic/static/kinematic)
  3. 创建 Fixture (形状 + 物理材质)
  4. 更新: world.Step(timeStep, velocityIterations, positionIterations)
  5. 读取物理状态应用到渲染变换
```

---

## 四、3D 游戏开发

### 4.1 渲染管线

```
Forward Rendering:
  每个光源 → 逐物体逐像素计算光照
  优点: 透明物体渲染好，MSAA 支持
  缺点: 大量光源时性能下降
  适用: 移动端、中低端硬件

Deferred Rendering:
  几何 Pass → 写入 G-Buffer (位置、法线、颜色、材质)
  光照 Pass → 逐像素读取 G-Buffer 计算
  优点: 支持大量光源
  缺点: 透明物体难处理，不支持 MSAA
  适用: PC/主机 AAA 游戏
```

### 4.2 PBR (基于物理的渲染)

```
PBR 核心参数:
  Albedo (基础颜色): 漫反射颜色
  Metalness (金属度): 0 = 非金属, 1 = 金属
  Roughness (粗糙度): 0 = 完全光滑, 1 = 完全粗糙
  Normal (法线贴图): 模拟表面细节
  AO (环境光遮蔽): 模拟接触阴影

渲染方程 (Cook-Torrance BRDF):
  f_r = k_d * f_lambert + k_s * f_cook_torrance
```

### 4.3 渲染管线顶点变换

三维顶点到屏幕的变换过程：

$$v_{\text{clip}} = M_{\text{proj}} \cdot M_{\text{view}} \cdot M_{\text{model}} \cdot v_{\text{obj}}$$

| 变换阶段 | 坐标系 | 作用 |
|---------|--------|------|
| **模型变换** $M_{\text{model}}$ | 模型空间 → 世界空间 | 平移、旋转、缩放物体 |
| **视图变换** $M_{\text{view}}$ | 世界空间 → 观察空间 | 以相机为原点重新定位场景 |
| **投影变换** $M_{\text{proj}}$ | 观察空间 → 裁剪空间 | 透视/正交投影，视锥体裁剪 |
| **视口变换**（固定管线）| 裁剪空间 → 屏幕空间 | 映射到像素坐标 |

透视投影矩阵：

$$M_{\text{persp}} = \begin{pmatrix}
\frac{1}{\tan(\text{FOV}/2) \cdot \text{aspect}} & 0 & 0 & 0 \\
0 & \frac{1}{\tan(\text{FOV}/2)} & 0 & 0 \\
0 & 0 & \frac{z_{\text{far}}}{z_{\text{far}} - z_{\text{near}}} & -\frac{z_{\text{far}}z_{\text{near}}}{z_{\text{far}} - z_{\text{near}}} \\
0 & 0 & 1 & 0
\end{pmatrix}$$

---

## 五、物理仿真

### 5.1 刚体与碰撞检测

| 碰撞检测算法 | 复杂度 | 精度 | 适用场景 |
|-------------|--------|------|----------|
| AABB (轴对齐包围盒) | O(1) | 低 | 快速粗检测 |
| OBB (有向包围盒) | O(1) | 中 | 旋转物体 |
| 球体碰撞 | O(1) | 低 | 粒子、球形物体 |
| GJK | O(log n) | 高 | 凸多边形精确碰撞 |
| SAT (分离轴定理) | O(n) | 高 | 凸多边形碰撞 |

### 5.2 LOD (细节层次) 管理

LOD 根据物体与相机的距离选择不同精度的网格，以平衡渲染质量与性能。

**LOD 切换指标：**

| 指标 | 公式 / 说明 |
|------|------------|
| 屏幕空间误差 | $E_{\text{screen}} = \dfrac{E_{\text{world}} \cdot \text{height}}{2d \cdot \tan(\text{FOV}/2)}$，超过阈值则升级 LOD |
| 距离阈值 | $d_{\text{switch}} = \dfrac{E_{\text{world}} \cdot \text{height}}{2 \cdot E_{\text{max}} \cdot \tan(\text{FOV}/2)}$ |
| 三角形预算 | $N_{\text{tri}} = \sum_{i=1}^{n} \text{LOD}_i \text{ 三角面数}$，控制总面数在预算内 |
| 切换迟滞 | 加入 $\pm h\%$ 迟滞区间防止频繁切换 |

**典型 LOD 级别：**

| 级别 | 三角面占比 | 距离范围 | 适用对象 |
|------|-----------|---------|---------|
| LOD 0（最高）| 100% | $d < d_1$ | 近处物体 |
| LOD 1 | 50% | $d_1 \leq d < d_2$ | 中等距离 |
| LOD 2 | 25% | $d_2 \leq d < d_3$ | 远处物体 |
| LOD 3（最低）| 5-10% | $d \geq d_3$ | 极远 / 剔除 |

### 5.3 物理引擎对比

| 引擎 | 语言 | 支持 | 特点 |
|------|------|------|------|
| PhysX | C++ | Unity, Unreal | NVIDIA 开发，GPU 加速 |
| Bullet | C++ | Godot, Blender | 开源，影视常用 |
| Box2D | C++ | 2D 游戏 | 轻量，2D 物理标准 |
| Havok | C++ | AAA 游戏 | 高性能，商业 |

---

## 六、音频

```
空间音频:
  3D 音源位置 → 听者位置/朝向 → 多声道输出
  关键参数: 距离衰减、多普勒效应、混响区域

音频中间件:
  FMOD:    流行中间件，支持 Unity/Unreal，动态混音
  Wwise:   专业级，AAA 广泛使用，音频处理管线
  
常见音频格式:
  MP3: 有损压缩，文件小
  OGG: 有损，开源，游戏常用
  WAV: 无损，原始数据，音效常用
```

---

## 七、网络同步

| 模型 | 描述 | 优点 | 缺点 |
|------|------|------|------|
| Client-Server | 服务器权威 | 防作弊，一致性 | 服务器成本高 |
| P2P | 节点直连 | 无服务器成本 | 延迟问题，NAT 穿透 |
| 监听服务器 | 主机自建服务器 | 低成本 | 主机优势 |
| 专用服务器 | 独立服务器 | 最好一致性 | 运营成本高 |

```
客户端预测 + 服务器回滚:
  客户端: 立即作用于输入 → 平滑体验
  服务器: 权威状态验证
  不一致时 → 回滚 + 修正

延迟补偿 (Lag Compensation):
  记录玩家历史位置
  服务器选择玩家"过去"的位置进行命中检测
  减少高 ping 玩家的不公平感
```

---

## 八、游戏 AI

| 技术 | 原理 | 应用 |
|------|------|------|
| 有限状态机 (FSM) | 状态 + 转移条件 | NPC 行为: 巡逻→追踪→攻击→巡逻 |
| 行为树 (Behavior Tree) | 组合节点 (Sequence, Selector, Decorator) | 复杂 AI: 敌人战术决策 |
| A* 寻路 | 启发式搜索 $f(n) = g(n) + h(n)$ | 游戏世界路径规划 |
| 导航网格 (Navmesh) | 凸多边形表示的可行走区域 | 开放世界 AI 移动 |
| 群体行为 (Flocking) | Separation + Alignment + Cohesion | 鱼群、鸟群、人群 |

---

## 九、游戏设计原理

```
核心循环 (Core Loop):
  玩家行动 → 系统反馈 → 玩家成长 → 新的挑战 → ...

难度曲线:
  目标: 心流通道 (Flow Channel)
  太简单 → 无聊
  太难   → 焦虑
  恰到好处 → 心流 (Flow)

玩家动机 (Bartle 分类):
  - 成就者 (Achiever): 完成目标、收集
  - 探索者 (Explorer): 发现世界秘密
  - 社交者 (Socializer): 与其他人互动
  - 杀手 (Killer): 竞争、击败他人
```

---

## 相关条目

- [[05_ComputerScience/ComputerGraphicsAndVision/ComputerGraphics|ComputerGraphics]]
- [[05_ComputerScience/ArtificialIntelligence/ComputerVision/ComputerVision|ComputerVision]]
- PhysicsEngine
- VR_AR


