---
aliases: [README]
tags: ['00_KnowledgeFramework', 'README']
---

# TianshangKnowledgeBase（天殇知识库）

欢迎来到 **TianshangKnowledgeBase** – 个人综合知识库。  
本知识库依据 **联合国教科文组织（UNESCO）基础学科分类** 与 **中华人民共和国教育部学科门类体系** 构建，覆盖从小学到大学本科及以上所有主要学科领域。

> 让知识有序生长，日有所进。

---

## 📊 数据总览

| 指标 | 数值 |
|------|------|
| Markdown 文件数 | **2,271** |
| 总文本量 | **339,718 行 / 11.3 MB** |
| 内容目录数 | **530 个** |
| INDEX 导航覆盖 | **100%**（每目录均有 INDEX.md） |
| YAML Frontmatter 覆盖 | **100%**（统一 aliases + tags） |
| 命名规范 | **UpperCamelCase**（二级及以下目录 + 英文文件名） |
| 破损 Wiki-Link | **0** |
| CI 自动化 | GitHub Actions（link check + markdownlint + 编码检查） |
| 学科覆盖 | **14 大学科门类** |
| 版本控制 | Git + GitHub |

---

## 📁 目录结构

```text
TianshangKnowledgeBase/
│
├── 00_KnowledgeFramework/           # 知识体系框架（元知识）
├── 01_K12/                          # K12 基础教育
├── 02_NaturalSciences/              # 自然科学
├── 03_HumanitiesAndSocialSciences/  # 人文与社会科学
├── 04_EngineeringAndTechnology/     # 工学与技术科学
├── 05_ComputerScience/              # 计算机科学
├── 06_ArtsAndCreativity/            # 艺术与创造性领域
├── 07_InterdisciplinarySciences/    # 交叉学科
├── 08_AgriculturalSciences/         # 农学
├── 09_MedicineAndHealth/            # 医学与健康
├── 10_MilitarySciences/             # 军事科学
├── 11_ManagementSciences/           # 管理科学
├── 12_SportsScience/                # 体育科学
└── 13_Others/                       # 其他
```

> 各目录内均有 `INDEX.md` 提供文件导航，部分含 `LearningPath.md` 学习路径指南。

---

## ✅ 优化特性

### 命名规范
- 二级及以下目录：**UpperCamelCase**（如 `DataStructuresAndAlgorithms`, `MachineLearning`）
- Markdown 文件：英文名 **UpperCamelCase**，中文名保留汉字
- `INDEX.md` / `LearningPath.md` / `README.md` 作为约定文件名

### 元数据
- 全部文件含 YAML frontmatter：`aliases` + `tags`
- `tags` 从目录路径自动推导，支持 Obsidian Graph View 按标签着色

### CI/CD
- 每次推送自动验证：破损链接、U+FFFD 编码、行尾空白、INDEX 完整性
- markdownlint 强制格式一致性

---

## 🚀 使用建议

1. **克隆**
   ```bash
   git clone https://github.com/Tianshang301/TianshangKnowledgeBase.git
   ```

2. **推荐工具**
   - 本地编辑：Obsidian（免费）
   - AI 辅助：Obsidian Copilot（DeepSeek API）或 Ollama + Qwen2.5
   - 全文检索：Obsidian 内置搜索或 ripgrep

3. **与 AI 结合**
   - 支持 MCP 协议（Model Context Protocol），AI Agent 可直接读取知识库
   - 适用于 Claude Code、Cursor 等工具的上下文注入

---

## 📜 许可证

**CC BY-NC-SA 4.0**（署名 – 非商业性使用 – 相同方式共享）

---

**让知识有序生长，日有所进。**  
—— TianshangKnowledgeBase
