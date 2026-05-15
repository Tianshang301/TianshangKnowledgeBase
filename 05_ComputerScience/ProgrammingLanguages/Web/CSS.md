---
aliases: [CSS]
tags: ['ProgrammingLanguages', 'Web', 'CSS']
---

# CSS3 完整参考

## 一、选择器

```css
/* 基本选择器 */
*                    {}  /* 通配符: 所有元素 */
div                  {}  /* 元素选择器 */
.container           {}  /* 类选择器 */
#header              {}  /* ID选择器 */

/* 组合选择器 */
div p                {}  /* 后代选择器 (div内的所有p) */
div > p              {}  /* 子选择器 (div的直接子p) */
h1 + p               {}  /* 相邻兄弟 (h1后面的第一个p) */
h1 ~ p               {}  /* 通用兄弟 (h1后面的所有p) */
div, p               {}  /* 分组选择器 */

/* 属性选择器 */
[disabled]           {}  /* 有disabled属性的元素 */
[type="text"]        {}  /* type="text" */
[class~="btn"]       {}  /* class包含"btn" (空格分隔) */
[href^="https"]      {}  /* href以https开头 */
[src$=".jpg"]        {}  /* src以.jpg结尾 */
[data-*="value"]     {}  /* data-* 属性包含value */

/* 伪类 */
:root                {}  /* 根元素(html) */
:first-child         {}  /* 第一个子元素 */
:last-child          {}  /* 最后一个子元素 */
:nth-child(2n)       {}  /* 偶数位置 */
:nth-child(2n+1)     {}  /* 奇数位置 */
:nth-last-child(3)   {}  /* 倒数第3个 */
:first-of-type       {}  /* 同类型第一个 */
:last-of-type        {}  /* 同类型最后一个 */
:not(.class)         {}  /* 不匹配选择器的元素 */
:empty               {}  /* 空元素 */
:focus               {}  /* 获得焦点 */
:hover               {}  /* 鼠标悬停 */
:active              {}  /* 激活状态 */
:visited             {}  /* 已访问链接 */
:target              {}  /* 当前锚点目标 */
:enabled             {}  /* 可用元素 */
:disabled            {}  /* 禁用元素 */
:checked             {}  /* 选中复选框/单选 */
:required            {}  /* 必填字段 */
:valid               {}  /* 有效值 */
:invalid             {}  /* 无效值 */
:in-range            {}  /* 在范围内 */
:out-of-range        {}  /* 超出范围 */
:placeholder-shown   {}  /* 显示占位符时 */

/* 伪元素 */
::before             {}  /* 元素前插入内容 */
::after              {}  /* 元素后插入内容 */
::first-letter       {}  /* 首字母 */
::first-line         {}  /* 首行 */
::selection          {}  /* 选中文本 */
::placeholder        {}  /* 占位符 */
::backdrop           {}  /* 全屏背景 */
```

## 二、盒模型

```css
.box {
    /* 内容区域 (content-box) */
    width: 300px;
    height: 200px;
    
    /* 内边距 (padding) */
    padding: 20px;              /* 四边相同 */
    padding: 10px 20px;         /* 上下 左右 */
    padding: 10px 20px 15px;    /* 上 左右 下 */
    padding: 10px 20px 15px 5px; /* 上 右 下 左 */
    padding-top: 10px;
    padding-right: 20px;
    padding-bottom: 15px;
    padding-left: 5px;
    
    /* 边框 (border) */
    border: 2px solid #333;
    border-width: 2px;
    border-style: solid;  /* solid | dashed | dotted | double | groove | ridge | inset | outset | none */
    border-color: #333;
    border-radius: 10px;           /* 圆角 */
    border-radius: 10px 5px 15px 5px;
    border-radius: 50%;            /* 圆形 */
    
    /* 外边距 (margin) */
    margin: 20px;
    margin: 0 auto;                /* 水平居中 */
    margin-top: -10px;             /* 负边距 */
    
    /* 盒模型计算 */
    box-sizing: content-box;  /* 默认: width=content宽度 */
    box-sizing: border-box;   /* width=content+padding+border */
}
```

## 三、Flexbox 布局

```css
/* 容器属性 */
.container {
    display: flex;
    flex-direction: row;            /* row | column | row-reverse | column-reverse */
    flex-wrap: wrap;                /* nowrap | wrap | wrap-reverse */
    flex-flow: row wrap;            /* 上面两个的简写 */
    
    justify-content: flex-start;    /* flex-start | flex-end | center | space-between | space-around | space-evenly */
    align-items: stretch;           /* flex-start | flex-end | center | baseline | stretch */
    align-content: flex-start;      /* 多行对齐: flex-start | flex-end | center | space-between | space-around | stretch */
    
    gap: 20px;                      /* 间距 (推荐替代 margin) */
    row-gap: 10px;
    column-gap: 20px;
}

/* 项目属性 */
.item {
    flex-grow: 1;                   /* 放大比例, 默认0 */
    flex-shrink: 1;                 /* 缩小比例, 默认1 */
    flex-basis: auto;               /* 初始大小, 默认auto */
    flex: 1 1 300px;                /* grow shrink basis 简写 */
    
    align-self: center;             /* 单独对齐: auto | flex-start | flex-end | center | baseline | stretch */
    order: 0;                       /* 排列顺序, 数值越小越前 */
}

/* 常见布局示例 */
/* 1. 水平居中 */
.center-h {
    display: flex;
    justify-content: center;
}

/* 2. 垂直居中 */
.center-v {
    display: flex;
    align-items: center;
}

/* 3. 完全居中 */
.center {
    display: flex;
    justify-content: center;
    align-items: center;
}

/* 4. 等分布局 */
.equal-cols {
    display: flex;
}
.equal-cols > * {
    flex: 1;
}

/* 5. 圣杯布局 */
.holy-grail {
    display: flex;
    flex-direction: column;
    min-height: 100vh;
}
.holy-grail header,
.holy-grail footer {
    flex-shrink: 0;
}
.holy-grail .content {
    display: flex;
    flex: 1;
}
.holy-grail .content main {
    flex: 1;
}
.holy-grail .content nav,
.holy-grail .content aside {
    width: 200px;
}
```

## 四、Grid 布局

```css
/* 容器 */
.grid {
    display: grid;
    
    /* 列定义 */
    grid-template-columns: 200px 1fr 200px;    /* 固定 + 自适应 + 固定 */
    grid-template-columns: 1fr 2fr 1fr;        /* 比例 */
    grid-template-columns: repeat(3, 1fr);     /* 3等分 */
    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); /* 自适应 */
    
    /* 行定义 */
    grid-template-rows: 100px 1fr 80px;
    grid-template-rows: repeat(3, auto);
    
    /* 简写 */
    grid-template: 
        "header header header" 80px
        "nav    main   aside" 1fr
        "footer footer footer" 60px
        / 200px 1fr 200px;
    
    /* 间距 */
    gap: 20px;
    row-gap: 10px;
    column-gap: 20px;
    
    /* 对齐 */
    justify-items: stretch;  /* 水平对齐单个项目 */
    align-items: stretch;    /* 垂直对齐单个项目 */
    place-items: center center;  /* 简写 */
    
    justify-content: start;  /* 整个网格水平对齐 */
    align-content: start;    /* 整个网格垂直对齐 */
    place-content: center;   /* 简写 */
    
    /* 自动行大小 */
    grid-auto-rows: minmax(100px, auto);
    grid-auto-columns: minmax(100px, auto);
    grid-auto-flow: row;     /* row | column | dense */
}

/* 项目 */
.item {
    grid-column: 1 / 3;                  /* 跨越列 1-2 */
    grid-column: 1 / -1;                 /* 跨越所有列 */
    grid-column: span 2;                 /* 跨2列 */
    grid-row: 1 / 3;
    grid-area: header;                   /* 指定区域 */
    
    justify-self: center;                /* 单独水平对齐 */
    align-self: center;                  /* 单独垂直对齐 */
    place-self: center;                  /* 简写 */
}

/* 响应式 Grid 示例 */
.responsive-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 20px;
}
```

## 五、响应式设计

```css
/* 媒体查询 */
@media screen and (max-width: 1200px) {
    /* 大屏设备 */
}

@media screen and (max-width: 992px) {
    /* 中屏设备 */
}

@media screen and (max-width: 768px) {
    /* 平板 */
}

@media screen and (max-width: 576px) {
    /* 手机 */
}

/* 常用断点 */
@media (min-width: 576px) {}  /* >= 576px */
@media (min-width: 768px) {}  /* >= 768px */
@media (min-width: 992px) {}  /* >= 992px */
@media (min-width: 1200px) {} /* >= 1200px */

/* 其他媒体特性 */
@media (prefers-color-scheme: dark) {}     /* 深色模式 */
@media (prefers-reduced-motion: reduce) {} /* 减少动画 */
@media (pointer: coarse) {}                /* 触屏设备 */
@media (hover: none) {}                    /* 无悬停 */
@media print {}                            /* 打印样式 */

/* 响应式单位 */
.responsive {
    /* 相对单位 */
    width: 50%;           /* 父元素宽度的50% */
    font-size: 1.2rem;    /* 根元素字体大小的1.2倍 */
    padding: 2em;         /* 当前字体大小的2倍 */
    width: 80vw;          /* 视口宽度的80% */
    height: 60vh;         /* 视口高度的60% */
    font-size: 2vmin;     /* vw和vh中较小的那一个 */
    font-size: 2vmax;     /* vw和vh中较大的那一个 */
    
    /* 响应式字体 */
    font-size: clamp(1rem, 2.5vw, 2rem);    /* 范围限制 */
    font-size: calc(1rem + 0.5vw);          /* 动态计算 */
    
    /* 响应式图片 */
    max-width: 100%;
    height: auto;
}
```

## 六、动画与过渡

```css
/* 过渡 */
.transition-element {
    transition: all 0.3s ease;
    /* property duration timing-function delay */
    transition: opacity 0.3s ease, transform 0.5s cubic-bezier(0.4, 0, 0.2, 1) 0.1s;
    transition-duration: 0.3s;
    transition-property: opacity, transform;
    transition-timing-function: ease;  /* ease | linear | ease-in | ease-out | ease-in-out | cubic-bezier() */
    transition-delay: 0s;
}

.transition-element:hover {
    opacity: 0.8;
    transform: translateY(-5px);
}

/* 关键帧动画 */
@keyframes fadeIn {
    from { opacity: 0; transform: translateY(20px); }
    to   { opacity: 1; transform: translateY(0); }
}

@keyframes spin {
    0%   { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
}

@keyframes bounce {
    0%, 100% { transform: translateY(0); }
    50%      { transform: translateY(-30px); }
}

.animated {
    animation: fadeIn 0.5s ease-out forwards;
    animation-name: fadeIn;
    animation-duration: 0.5s;
    animation-timing-function: ease-out;
    animation-delay: 0.2s;
    animation-iteration-count: infinite;   /* 播放次数 */
    animation-direction: alternate;         /* normal | reverse | alternate | alternate-reverse */
    animation-fill-mode: forwards;          /* none | forwards | backwards | both */
    animation-play-state: running;          /* running | paused */
}

.animated:hover {
    animation-play-state: paused;
}
```

## 七、定位

```css
.positioning {
    /* 静态定位 (默认) */
    position: static;
    
    /* 相对定位 - 相对于自身原位置 */
    position: relative;
    top: 10px;
    left: 20px;
    z-index: 1;
    
    /* 绝对定位 - 相对于最近的已定位祖先 */
    position: absolute;
    top: 0;
    right: 0;
    z-index: 100;
    
    /* 固定定位 - 相对于视口 */
    position: fixed;
    bottom: 20px;
    right: 20px;
    
    /* 粘性定位 - 滚动到阈值后固定 */
    position: sticky;
    top: 0;  /* 到达顶部时固定 */
}

/* 层叠上下文 */
.z-index-example {
    position: relative;
    z-index: 10;
}

/* 居中技巧 */
.center-absolute {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
}

.center-flex {
    display: flex;
    justify-content: center;
    align-items: center;
}

.center-grid {
    display: grid;
    place-items: center;
}
```

## 八、变量与函数

```css
/* CSS 自定义属性 (变量) */
:root {
    --primary-color: #3498db;
    --secondary-color: #2ecc71;
    --text-color: #333;
    --bg-color: #fff;
    --font-size-base: 16px;
    --spacing-unit: 8px;
    --border-radius: 4px;
    --shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    --transition-speed: 0.3s;
}

.button {
    background-color: var(--primary-color);
    color: white;
    padding: calc(var(--spacing-unit) * 2) calc(var(--spacing-unit) * 3);
    border-radius: var(--border-radius);
    box-shadow: var(--shadow);
    transition: all var(--transition-speed);
}

.dark-theme {
    --bg-color: #1a1a2e;
    --text-color: #eee;
    --primary-color: #6c63ff;
}

/* CSS 函数 */
.function-example {
    /* 计算 */
    width: calc(100% - 40px);
    font-size: calc(1rem + 0.5vw);
    
    /* 最小/最大 */
    width: min(100%, 800px);
    font-size: max(1rem, 2vw);
    font-size: clamp(0.8rem, 2vw, 1.5rem);
    
    /* 颜色 */
    color: rgb(52, 152, 219);
    color: rgba(52, 152, 219, 0.5);
    color: hsl(204, 70%, 53%);
    color: hsla(204, 70%, 53%, 0.5);
    
    /* 渐变 */
    background: linear-gradient(45deg, #3498db, #2ecc71);
    background: radial-gradient(circle, #3498db, #2ecc71);
    background: conic-gradient(#3498db, #2ecc71, #e74c3c);
    
    /* 滤镜 */
    filter: blur(2px);
    filter: brightness(1.2);
    filter: contrast(150%);
    filter: grayscale(100%);
    filter: drop-shadow(0 2px 4px rgba(0,0,0,0.3));
    
    /* 变换 */
    transform: rotate(45deg);
    transform: scale(1.2);
    transform: translate(10px, 20px);
    transform: skew(10deg, 5deg);
    transform: rotate(45deg) scale(1.1);
    transform-origin: top left;
    
    /* 剪裁 */
    clip-path: circle(50%);
    clip-path: polygon(0 0, 100% 0, 100% 100%, 0 100%);
    
    /* 遮罩 */
    mask-image: linear-gradient(black, transparent);
}
```

## 九、实用样式

```css
/* 重置/标准化 */
*,
*::before,
*::after {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
}

/* 文本溢出省略 */
.ellipsis {
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
}

/* 多行省略 */
.multiline-ellipsis {
    display: -webkit-box;
    -webkit-line-clamp: 3;
    -webkit-box-orient: vertical;
    overflow: hidden;
}

/* 滚动条美化 */
::-webkit-scrollbar {
    width: 8px;
}
::-webkit-scrollbar-track {
    background: #f1f1f1;
}
::-webkit-scrollbar-thumb {
    background: #888;
    border-radius: 4px;
}

/* 打印样式 */
@media print {
    nav, .sidebar, .ads { display: none; }
    body { font-size: 12pt; }
    a[href]::after { content: " (" attr(href) ")"; }
}
```

> CSS3 是 Web 样式的核心, 重点掌握 Flexbox 和 Grid 布局、响应式设计、动画与过渡。建议采用 "移动优先" 的策略进行响应式开发。
