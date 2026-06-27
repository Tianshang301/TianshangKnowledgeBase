---
aliases:
  - 动态设计
  - Motion Design
  - Motion Graphics
tags:
  - motion-design
  - after-effects
  - arts
  - creativity
created: 2026-06-27
updated: 2026-06-27
---

# 动态设计

动态设计（Motion Design / Motion Graphics）是平面设计与动画的交叉领域，专注于通过运动传达信息和情感。从品牌标识动画到数据可视化，从 UI 交互反馈到电影片头，动态设计无处不在。

## Adobe After Effects

After Effects 是动态设计领域最广泛使用的软件，以其强大的合成功能和丰富的插件生态著称。

### 核心概念

- **合成（Composition）**：工作空间的基本单位，包含所有图层和动画信息
- **图层类型**：素材层、形状层、文字层、调整层、纯色层、摄像机层、灯光层
- **时间轴与关键帧**：通过设置关键帧并在 Graph Editor 中调整运动曲线
- **表达式（Expression）**：基于 JavaScript 的脚本语言，实现程序化动画控制

### 常用表达式

```javascript
// 弹性效果
amp = 0.05;
freq = 3;
decay = 5;
n = 0;
time_max = 4;
if (numKeys > 0){
  n = nearestKey(time).index;
  if (key(n).time > time) n--;
}
if (n > 0){
  t = time - key(n).time;
  if (t < time_max){
    v = velocityAtTime(key(n).time - 0.001);
    value + v*amp*Math.sin(freq*t*2*Math.PI)/Math.exp(decay*t);
  } else {
    value;
  }
} else {
  value;
}
```

### 必备插件

- **Trapcode Suite**：粒子（Particular）、光线（Shine）、3D Stroke 等
- **Duik Bassel**：角色骨骼绑定和动画工具
- **Flow**：运动曲线编辑的可视化工具
- **Motion v3**：快速动画辅助工具
- **Bodymovin/Lottie**：导出 Web 和移动端可用的矢量动画

## MG动画（Motion Graphics Animation）

MG动画是以图形元素为主要视觉载体的动态设计形式，强调信息传达的清晰性和视觉节奏感。

### 设计原则

1. **网格系统**：使用一致的网格确保视觉元素的对齐和秩序
2. **色彩体系**：建立有限的调色板，通常3-5个主色加辅助色
3. **字体层级**：通过大小、粗细、颜色建立清晰的信息层次
4. **运动一致性**：相似元素使用相似的运动方式，建立视觉语言

### 常见风格

- **扁平化风格（Flat Design）**：简洁的色块和几何形状
- **等距风格（Isometric）**：45度角的伪三维视角
- **线条风格（Line Art）**：以描边线条为主要视觉元素
- **混合媒体（Mixed Media）**：结合实拍素材与图形动画
- **3D 风格**：使用 Cinema 4D 或 Blender 创建三维图形动画

### 工作流程

1. **脚本撰写**：明确要传达的核心信息和叙事结构
2. **风格帧（Style Frame）**：设计2-3个关键画面确定视觉风格
3. **故事板（Storyboard）**：绘制分镜草图规划画面序列
4. **动态故事板（Animatic）**：加入时间节奏的粗略动画
5. **正式制作**：完成所有动画和合成
6. **声音设计**：添加音效和配乐增强表现力

## 数据可视化动画

数据可视化动画将复杂数据转化为直观的动态图形，使信息更易理解和记忆。

### 技术实现

- **D3.js**：Web 端最强大的数据可视化库，支持 SVG、Canvas 和 WebGL
- **After Effects + 数据驱动**：通过脚本将 CSV/JSON 数据导入 AE 驱动动画
- **Processing/p5.js**：创意编程工具，适合生成艺术风格的数据可视化
- **Tableau Public**：商业智能工具，支持动态图表导出

### 设计要点

- 动画过渡应帮助用户追踪数据变化，而非纯粹装饰
- 使用有意义的颜色映射——如温度数据使用冷暖色渐变
- 控制动画时长，太快看不清，太慢让人失去耐心
- 提供交互控制，让用户按需探索数据

## UI动效（UI Animation）

UI 动效是用户界面中的动画设计，兼顾美学表达和功能引导。

### 动效类型

| 类型 | 功能 | 示例 |
|------|------|------|
| 转场动画 | 页面/视图切换 | 滑动、淡入淡出、共享元素 |
| 反馈动画 | 确认用户操作 | 按钮点击波纹、加载进度 |
| 引导动画 | 教授新功能 | 新手引导、手势提示 |
| 品牌动画 | 建立品牌识别 | 启动动画、Logo 动画 |
| 状态动画 | 表示系统状态 | 骨架屏、加载占位 |

### 设计原则

- **60fps 标准**：确保动画流畅，避免卡顿
- **有意义的运动**：每个动画都应有明确的功能目的
- **自然的缓动曲线**：使用 Ease In-Out 而非线性运动
- **响应性**：动画不应延迟用户操作的响应
- **可访问性**：为有前庭障碍的用户提供减少动画的选项

### 原型工具

- **Principle**：macOS 上的交互动效原型工具
- **ProtoPie**：支持传感器和条件逻辑的高保真原型
- **Figma Smart Animate**：Figma 内置的原型动画功能
- **Lottie + After Effects**：将 AE 动画导出为代码可用的 JSON 格式

## 实践建议

1. 从临摹优秀作品开始，分析其运动曲线和时间节奏
2. 建立自己的动态素材库——常用动画预设、表达式、图形模板
3. 学习基本的平面设计原则，动态设计的根基是好的静态设计
4. 关注 Dribbble、Behance 上的 Motion Design 趋势
5. 掌握至少一种编程方式的动画（如 CSS Animation、Lottie），拓展实现能力
