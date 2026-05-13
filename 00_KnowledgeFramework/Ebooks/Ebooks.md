# 电子书资源与管理指南

## 一、电子书格式

### 1.1 主流格式对比

| 格式 | 全称 | 开发者 | 版式 | DRM 支持 | 适用平台 |
|------|------|--------|:----:|:--------:|---------|
| EPUB | Electronic Publication | IDPF | 重排 | Adobe ADEPT | 通用（除 Kindle）|
| MOBI | Mobipocket | Amazon | 重排 | Kindle DRM | Kindle 旧设备 |
| AZW3 | Kindle Format 8 | Amazon | 重排 | Kindle DRM | Kindle 新设备 |
| PDF | Portable Document Format | Adobe | 固定 | 多种 | 通用 |
| DJVU | DjVu | AT&T | 固定 | 极少 | 扫描版图书 |

**特点详解**：
- **EPUB**：开放标准（ISO 24698），基于 XHTML + CSS，支持自适应排版，是目前最广泛支持的格式
- **AZW3/KF8**：Amazon 专有格式，支持 HTML5 + CSS3，Kindle 设备的最佳选择
- **PDF**：固定页面的排版保真度高，但小屏幕阅读体验差，适合 A4 学术论文
- **DJVU**：专门针对扫描文档优化的格式，压缩率约为 JPEG 的 5-10 倍
### 1.2 格式转换

$$ \text{Source} \xrightarrow{\text{Pandoc/Calibre}} \text{Target} $$

| 转换工具 | 支持的格式 | 特点 |
|---------|-----------|------|
| Pandoc | 30+ 格式 | 命令行、精确控制、学术首选 |
| Calibre | 20+ 格式 | GUI + 命令行、批量转换、元数据管理 |
| Kindle Previewer | MOBI/AZW3 | Amazon 官方、模拟 Kindle 设备 |
| Online Convert | 多格式 | 浏览器操作、无需安装 |

## 二、电子书创建流程

### 2.1 写作与转换
**推荐工作流**：
```
Markdown/LaTeX 源文件         → Pandoc
     EPUB/PDF
         → Calibre
     MOBI/AZW3
```

```markdown
% 使用 Pandoc 将 Markdown 转换为 EPUB
pandoc book.md -o book.epub --metadata title="书名" --metadata author="作者"
```

### 2.2 元数据管理
EPUB 元数据使用 OPF 文件定义，关键字段：

| 字段 | 描述 | Dublin Core 映射 |
|------|------|-----------------|
| title | 书名 | dc:title |
| creator | 作者 | dc:creator |
| publisher | 出版社 | dc:publisher |
| identifier | 唯一标识（ISBN/DOI）| dc:identifier |
| language | 语言代码（zh, en）| dc:language |
| date | 出版日期 | dc:date |
| subject | 分类主题 | dc:subject |
| rights | 版权声明 | dc:rights |

### 2.3 CSS 格式化
```css
/* EPUB 样式示例 */
body {
  font-family: "Noto Serif", "Source Han Serif", serif;
  line-height: 1.8;
  margin: 5%;
}
h1 { text-align: center; font-size: 1.6em; }
h2 { font-size: 1.3em; margin-top: 1.5em; }
p { text-indent: 2em; }
img { max-width: 100%; height: auto; }
```

## 三、阅读设备与软件

### 3.1 硬件设备

| 设备 | 屏幕技术 | 屏幕尺寸 | 优点 | 缺点 |
|------|---------|:--------:|------|------|
| Kindle | E-ink | 6"-10" | 护眼、续航长 | 格式封闭 |
| Kobo | E-ink | 6"-8" | EPUB 原生、开放 | 中文生态弱 |
| Remarkable | E-ink | 10.3" | 手写笔记 | 价格高 |
| iPad | LCD/OLED | 8"-13" | 彩色、App 丰富 | 伤眼、重 |
| 文石 Boox | E-ink | 6"-13.3" | Android 开放 | 价格高 |

### 3.2 阅读软件

| 软件 | 平台 | 特色功能 |
|------|------|---------|
| Kindle App | iOS/Android/PC | Whispersync 同步 |
| Google Play Books | iOS/Android/Web | 云存储、PDF 上传 |
| Apple Books | iOS/macOS | 美观、iCloud 同步 |
| Adobe Digital Editions | PC | EPUB/PDF + ADEPT DRM |
| 微信读书 | iOS/Android | 社交阅读、中文生态 |
| Marvin 3 | iOS | 自定义强、统计功能 |
| Moon+ Reader | Android | TTS、手势、格式支持广 |

## 四、数字版权管理（DRM）
### 4.1 DRM 方案对比

| DRM 方案 | 提供方 | 加密方法 | 设备限制 |
|---------|--------|---------|:--------:|
| Kindle DRM | Amazon | 专有加密 | 6 台设备 |
| Adobe ADEPT | Adobe | AES-256 | 6 台设备 |
| Apple FairPlay | Apple | 专有加密 | 生态内 |
| Marlin DRM | Marlin Trust | 开放标准 | 灵活 |
| LCP | Readium | AES-256 | 灵活 |

### 4.2 DRM 的利弊
| 维度 | 支持 DRM | 无 DRM |
|------|---------|--------|
| 版权保护 | 强 | 无 |
| 用户便利性 | 受限 | 自由使用 |
| 格式转换 | 不允许 | 允许 |
| 跨平台共享 | 受限 | 自由 |
| 长期保存 | 危险（服务器关闭）| 安全 |

## 五、开放获取电子书

### 5.1 主要资源

| 资源库 | 规模 | 内容类型 | 访问方式 |
|--------|:----:|---------|---------|
| Project Gutenberg | 70,000+ | 公版文学作品 | 免费下载 |
| Internet Archive | 10,000,000+ | 书籍/音频/视频 | 借阅+下载 |
| Open Library | 1,000,000+ | 现代书籍 | 借阅 |
| OAPEN | 20,000+ | 学术开放图书 | 免费阅读 |
| DOAB | 50,000+ | 同行评审学术图书 | 免费下载 |
| 国学大师 | 100,000+ | 中国古籍 | 在线阅读 |

### 5.2 Project Gutenberg 使用

Distributed Proofreaders 志愿者协作平台，图书经过 OCR → 校对 → 格式化 → 发布流程。支持 EPUB、Kindle、HTML、纯文本格式。
## 六、电子书发行

### 6.1 自出版平台对比
| 平台 | 分成模式 | 独家要求 | 格式要求 | DRM 选项 |
|------|---------|:--------:|---------|:--------:|
| Amazon KDP | 35%-70% | KDP Select | MOBI/EPUB | 可选 |
| Google Play Books | 52%-80% | 无 | EPUB/PDF | 可选 |
| Apple Books | 70% | 无 | EPUB | 可选 |
| Smashwords | 60%-80% | 无 | EPUB（通过 Meatgrinder）| 可选 |
| 豆瓣阅读 | 50%-70% | 无 | EPUB | 无 |

### 6.2 自出版 vs 传统出版

| 维度 | 自出版 | 传统出版 |
|------|--------|---------|
| 控制权 | 完全自主 | 出版社主导 |
| 周期 | 数天-数周 | 6 个月-2 年 |
| 编辑支持 | 自费/外包 | 专业编辑 |
| 发行渠道 | 有限 | 全面 |
| 版税率 | 35%-70% | 5%-15% |
| 前期投入 | 编校/封面设计 | 无 |
| 品牌背书 | 无 | 有 |

## 七、学术电子书

| 平台 | 学科覆盖 | 访问模式 | 特点 |
|------|---------|---------|------|
| SpringerLink | STEM | 机构订阅/购买 | Lecture Notes 系列 |
| Cambridge Core | 全学科 | 机构订阅 | 剑桥大学出版社 |
| Oxford Scholarship Online | 人文社科 | 机构订阅 | 专题合集 |
| JSTOR | 人文社科 | 机构订阅 | 过刊 + 电子书 |
| 中国知网（CNKI）| 全学科 | 按页付费 | 中文硕博论文 |
| 读秀 | 全学科 | 机构订阅 | 中文图书搜索 |

## 八、电子书库管理
### 8.1 Calibre 管理

Calibre 是开源的电子书管理瑞士军刀：
| 功能 | 描述 |
|------|------|
| 格式转换 | 支持 20+ 格式互转 |
| 元数据编辑 | 自动抓取豆瓣/Amazon/Google 信息 |
| 标签管理 | 自定义标签/分类 |
| 内容服务器 | 局域网无线访问 |
| 新闻下载 | 自动抓取 RSS 转换为电子书 |
| 批量操作 | 批量转换/编辑/重命名 |

### 8.2 元数据编辑建议
- 统一书名和作者格式（姓, 名）
- 添加标签，如 `#编程`, `#Python`, `#数据科学`
- 填写 ISBN 便于检索
- 添加封面图像（统一尺寸）
- 设置语言标签（zh, en, ja）
## 九、无障碍访问

| 无障碍特性 | 说明 | EPUB3 支持 |
|-----------|------|:----------:|
| 屏幕阅读器兼容 | NVDA, VoiceOver, TalkBack | ✓ |
| 文字重排 | 自定义字体/大小/间距 | ✓ |
| 高对比度模式 | 适应视力障碍 | ✓ |
| 替代文本（Alt Text）| 图像描述 | ✓ |
| 媒体替代 | 音频描述视频 | ✓ |
| 页面导航 | 标题/书签/页码 | ✓ |
| 语音合成（TTS）| 文本朗读 | ✓ |

WCAG 2.1 AA 是电子书无障碍的基本标准，EPUB3 对该标准提供良好支持。
## 参考资料
- 中国皮书网 (2024). *数字出版产业年度报告*.
- Project Gutenberg: https://www.gutenberg.org
- Calibre 官方: https://calibre-ebook.com
- Pandoc 文档: https://pandoc.org/MANUAL.html
- IDPF EPUB 规范: https://www.w3.org/publishing/epub3
- Open Access Publishing in European Networks: https://www.oapen.org

## 相关条目

DigitalLibrary, [[NoteTaking]], [[KnowledgeManagement]], EPUB
