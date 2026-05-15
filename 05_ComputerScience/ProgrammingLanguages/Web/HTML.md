---
aliases: [HTML]
tags: ['ProgrammingLanguages', 'Web', 'HTML']
---

# HTML5 完整参考

## 一、文档结构

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="页面描述">
    <meta name="keywords" content="关键词1,关键词2">
    <meta name="author" content="作者">
    <meta name="robots" content="index, follow">
    
    <meta property="og:title" content="社交分享标题">
    <meta property="og:description" content="社交分享描述">
    <meta property="og:image" content="分享图片URL">
    
    <link rel="icon" href="favicon.ico" type="image/x-icon">
    <link rel="stylesheet" href="style.css">
    
    <title>页面标题</title>
</head>
<body>
    <!-- 可见内容 -->
</body>
</html>
```

## 二、语义化元素

```html
<body>
    <header>
        <h1>网站标题</h1>
        <nav>
            <ul>
                <li><a href="/">首页</a></li>
                <li><a href="/about">关于</a></li>
                <li><a href="/contact">联系我们</a></li>
            </ul>
        </nav>
    </header>

    <main>
        <section>
            <h2>文章列表</h2>
            <article>
                <header>
                    <h3>文章标题</h3>
                    <time datetime="2024-03-15">2024年3月15日</time>
                </header>
                <p>文章内容...</p>
                <footer>
                    <span>作者: 张三</span>
                    <span>分类: 技术</span>
                </footer>
            </article>
        </section>

        <aside>
            <h2>侧边栏</h2>
            <section>
                <h3>热门文章</h3>
                <ul>
                    <li><a href="#">文章1</a></li>
                    <li><a href="#">文章2</a></li>
                </ul>
            </section>
        </aside>
    </main>

    <footer>
        <p>&copy; 2024 版权所有</p>
        <address>
            联系邮箱: <a href="mailto:admin@example.com">admin@example.com</a>
        </address>
    </footer>
</body>
```

### 语义化元素用途

| 元素 | 用途 |
|------|------|
| `<header>` | 页面或区块的头部, 包含标题/导航/Logo |
| `<nav>` | 导航链接区域 |
| `<main>` | 页面主要内容 (每个页面只有一个) |
| `<section>` | 相关内容的主题分组 |
| `<article>` | 独立的文章/帖子/评论等 |
| `<aside>` | 侧边栏/补充内容 |
| `<footer>` | 页面或区块的底部 |
| `<figure>` | 配图/图表/代码块 |
| `<figcaption>` | figure 的标题 |
| `<mark>` | 高亮文本 |
| `<time>` | 时间/日期 |
| `<details>` | 可展开/收起的内容 |
| `<summary>` | details 的摘要 |

## 三、文本元素

```html
<!-- 标题 -->
<h1>一级标题</h1>
<h2>二级标题</h2>
<h3>三级标题</h3>
<h4>四级标题</h4>
<h5>五级标题</h5>
<h6>六级标题</h6>

<!-- 段落与文本 -->
<p>这是一个段落。</p>

<!-- 行内文本 -->
<span>普通行内文本</span>
<strong>重要内容 (粗体)</strong>
<em>强调内容 (斜体)</em>
<b>粗体 (无语义)</b>
<i>斜体 (无语义)</i>
<u>下划线</u>
<s>删除线</s>
<small>小字/免责声明</small>
<mark>高亮文本</mark>
<del>已删除文本</del>
<ins>已插入文本</ins>
<sub>下标</sub>
<sup>上标</sup>
<code>code代码</code>
<pre>预格式
  保留 空格
和换行</pre>
<blockquote cite="https://example.com">
    长引用内容
</blockquote>
<q>短引用</q>
<abbr title="HyperText Markup Language">HTML</abbr>
```

## 四、链接与图片

```html
<!-- 链接 -->
<a href="https://example.com">普通链接</a>
<a href="page.html" target="_blank">新窗口打开</a>
<a href="#section-id">锚点链接</a>
<a href="mailto:user@example.com">发送邮件</a>
<a href="tel:+8613800000000">拨打电话</a>
<a href="file.pdf" download>下载文件</a>
<a href="page.html" rel="noopener noreferrer">安全外链</a>

<!-- 图片 -->
<img src="image.jpg" alt="图片描述" width="800" height="600" loading="lazy">
<img src="photo.webp" srcset="small.jpg 480w, medium.jpg 800w, large.jpg 1200w"
     sizes="(max-width: 600px) 480px, (max-width: 1200px) 800px, 1200px"
     alt="响应式图片">

<!-- 图片地图 -->
<img src="map.png" usemap="#map" alt="区域图">
<map name="map">
    <area shape="rect" coords="0,0,100,100" href="area1.html" alt="区域1">
    <area shape="circle" coords="200,200,50" href="area2.html" alt="区域2">
</map>
```

## 五、列表

```html
<!-- 无序列表 -->
<ul>
    <li>项目1</li>
    <li>项目2</li>
    <li>项目3</li>
</ul>

<!-- 有序列表 -->
<ol type="1" start="5">
    <li>第一步</li>
    <li>第二步</li>
    <li value="10">第三步 (指定编号)</li>
</ol>

<ol reversed>
    <li>倒序项1</li>
    <li>倒序项2</li>
</ol>

<!-- 嵌套列表 -->
<ul>
    <li>一级
        <ul>
            <li>二级
                <ul>
                    <li>三级</li>
                </ul>
            </li>
        </ul>
    </li>
</ul>

<!-- 定义列表 -->
<dl>
    <dt>HTML</dt>
    <dd>超文本标记语言</dd>
    <dt>CSS</dt>
    <dd>层叠样式表</dd>
</dl>
```

## 六、表格

```html
<table>
    <caption>员工信息表</caption>
    <thead>
        <tr>
            <th>ID</th>
            <th>姓名</th>
            <th>部门</th>
            <th>薪资</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>001</td>
            <td>张三</td>
            <td>技术部</td>
            <td>15000</td>
        </tr>
        <tr>
            <td>002</td>
            <td>李四</td>
            <td>市场部</td>
            <td>18000</td>
        </tr>
    </tbody>
    <tfoot>
        <tr>
            <td colspan="3">平均薪资</td>
            <td>16500</td>
        </tr>
    </tfoot>
</table>

<!-- 合并单元格 -->
<table>
    <tr>
        <th rowspan="2">姓名</th>
        <th colspan="2">成绩</th>
    </tr>
    <tr>
        <td>数学</td>
        <td>英语</td>
    </tr>
    <tr>
        <td>张三</td>
        <td>95</td>
        <td>88</td>
    </tr>
</table>
```

## 七、表单

### 输入类型

```html
<form action="/submit" method="POST" enctype="multipart/form-data">
    <!-- 文本输入 -->
    <label for="name">姓名:</label>
    <input type="text" id="name" name="name" 
           placeholder="请输入姓名" required maxlength="20">

    <!-- 密码 -->
    <label for="password">密码:</label>
    <input type="password" id="password" name="password" 
           minlength="6" required>

    <!-- 邮箱 -->
    <label for="email">邮箱:</label>
    <input type="email" id="email" name="email" required>

    <!-- 数字 -->
    <label for="age">年龄:</label>
    <input type="number" id="age" name="age" min="0" max="150" step="1">

    <!-- 电话 -->
    <label for="phone">电话:</label>
    <input type="tel" id="phone" name="phone" pattern="[0-9]{11}">

    <!-- URL -->
    <label for="website">网址:</label>
    <input type="url" id="website" name="website">

    <!-- 日期时间 -->
    <input type="date" name="date">
    <input type="time" name="time">
    <input type="datetime-local" name="datetime">
    <input type="month" name="month">
    <input type="week" name="week">

    <!-- 选择 -->
    <input type="color" name="color">
    <input type="range" name="range" min="0" max="100" value="50">

    <!-- 文件 -->
    <input type="file" name="file" accept="image/*,.pdf" multiple>

    <!-- 搜索 -->
    <input type="search" name="q" placeholder="搜索...">

    <!-- 隐藏 -->
    <input type="hidden" name="token" value="abc123">

    <!-- 选项 -->
    <input type="radio" name="gender" value="male" id="male">
    <label for="male">男</label>
    <input type="radio" name="gender" value="female" id="female">
    <label for="female">女</label>

    <input type="checkbox" name="hobbies" value="reading" id="reading">
    <label for="reading">阅读</label>
    <input type="checkbox" name="hobbies" value="coding" id="coding">
    <label for="coding">编程</label>

    <!-- 下拉框 -->
    <label for="city">城市:</label>
    <select id="city" name="city" required>
        <option value="">请选择</option>
        <option value="beijing">北京</option>
        <option value="shanghai" selected>上海</option>
        <option value="guangzhou">广州</option>
    </select>

    <!-- 多选下拉框 -->
    <select name="skills" multiple size="4">
        <option value="python">Python</option>
        <option value="javascript">JavaScript</option>
        <option value="java">Java</option>
        <option value="go">Go</option>
    </select>

    <!-- 文本框 -->
    <label for="bio">简介:</label>
    <textarea id="bio" name="bio" rows="4" cols="50" 
              placeholder="介绍一下自己..." maxlength="500"></textarea>

    <!-- 数据列表 -->
    <input list="browsers" name="browser">
    <datalist id="browsers">
        <option value="Chrome">
        <option value="Firefox">
        <option value="Edge">
        <option value="Safari">
    </datalist>

    <!-- 分组 -->
    <fieldset>
        <legend>个人信息</legend>
        <!-- 表单控件 -->
    </fieldset>

    <!-- 进度 -->
    <progress value="70" max="100">70%</progress>
    <meter value="0.7" min="0" max="1" low="0.3" high="0.8">70%</meter>

    <!-- 按钮 -->
    <button type="submit">提交</button>
    <button type="reset">重置</button>
    <button type="button" onclick="alert('点击')">普通按钮</button>
</form>
```

### HTML5 表单验证

```html
<form novalidate>  <!-- 禁用默认验证 -->
    <input type="text" required pattern="[A-Za-z]+" 
           title="只允许字母" 
           oninvalid="this.setCustomValidity('请输入字母')"
           oninput="this.setCustomValidity('')">
</form>
```

## 八、多媒体

```html
<!-- 音频 -->
<audio controls autoplay loop preload="auto">
    <source src="music.mp3" type="audio/mpeg">
    <source src="music.ogg" type="audio/ogg">
    您的浏览器不支持音频播放
</audio>

<!-- 视频 -->
<video controls width="800" height="450" poster="thumbnail.jpg">
    <source src="video.mp4" type="video/mp4">
    <source src="video.webm" type="video/webm">
    <track kind="subtitles" src="subtitles.vtt" srclang="zh" label="中文">
    您的浏览器不支持视频播放
</video>

<!-- 内联框架 -->
<iframe src="https://example.com" width="800" height="600"
        allowfullscreen loading="lazy"
        sandbox="allow-scripts allow-same-origin">
    <p>您的浏览器不支持 iframe</p>
</iframe>

<!-- 嵌入内容 -->
<embed src="file.pdf" type="application/pdf" width="800" height="600">
<object data="file.swf" type="application/x-shockwave-flash" width="800" height="600">
    <param name="quality" value="high">
</object>
```

## 九、Accessibility (无障碍)

```html
<!-- ARIA 属性 -->
<nav aria-label="主导航" role="navigation">
    <button aria-expanded="false" aria-controls="menu">菜单</button>
    <ul id="menu" role="menubar">
        <li role="none">
            <a href="#" role="menuitem" aria-current="page">首页</a>
        </li>
    </ul>
</nav>

<!-- 屏幕阅读器友好 -->
<button aria-label="关闭" onclick="close()">X</button>

<div role="alert" aria-live="assertive">
    操作成功!
</div>

<!-- 跳转链接 -->
<a href="#main-content" class="skip-link">跳到主要内容</a>
<main id="main-content">
    <!-- 核心内容 -->
</main>

<!-- 图片 Alt 文本 -->
<img src="chart.png" alt="2024年销售额柱状图: 第一季度100万, 第二季度150万">
<img src="decoration.png" alt="">  <!-- 装饰性图片使用空alt -->

<!-- 表单标签 -->
<label for="username">用户名:</label>
<input id="username" type="text" aria-describedby="username-help">
<span id="username-help" class="help-text">6-20个字符, 支持字母和数字</span>

<!-- 错误提示 -->
<input type="text" aria-invalid="true" aria-errormessage="error-msg">
<span id="error-msg" role="alert">请输入有效值</span>
```

## 十、Meta 标签与 SEO

```html
<!-- 基础 Meta -->
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="description" content="页面描述, 搜索引擎会显示在搜索结果中">
<meta name="keywords" content="关键词1, 关键词2, 关键词3">
<meta name="author" content="作者名">

<!-- SEO -->
<meta name="robots" content="index, follow">
<meta name="googlebot" content="index, follow">
<link rel="canonical" href="https://example.com/page">

<!-- Open Graph (社交分享) -->
<meta property="og:title" content="分享标题">
<meta property="og:description" content="分享描述">
<meta property="og:image" content="https://example.com/image.jpg">
<meta property="og:url" content="https://example.com">
<meta property="og:type" content="website">
<meta property="og:locale" content="zh_CN">

<!-- Twitter Card -->
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="标题">
<meta name="twitter:description" content="描述">
<meta name="twitter:image" content="https://example.com/image.jpg">

<!-- 移动端 -->
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="black">
<meta name="format-detection" content="telephone=no">
<link rel="apple-touch-icon" href="icon.png">

<!-- 预加载/预连接 -->
<link rel="preload" href="font.woff2" as="font" crossorigin>
<link rel="preconnect" href="https://api.example.com">
<link rel="dns-prefetch" href="https://example.com">
```

> HTML5 是 Web 开发的基石。重点掌握语义化结构、表单控件、无障碍访问。良好的 HTML 结构是 SEO 和可访问性的基础。
