---
aliases: [CHANGELOG]
tags: ['00_KnowledgeFramework', 'VersionHistory', 'CHANGELOG']
---

# 版本历史

记录 TianshangKnowledgeBase 的重要更新。本文件遵循语义化版本规范（Semantic Versioning）。

格式说明：
- **新增**：新条目、新目录、新文件
- **修改**：内容更新、结构优化
- **修复**：错误修正、链接修复
- **移除**：删除过时内容

---

## v3.7 (2026-05-17) — 全库内容填充 + 编码清理

### 新增
- **Stub 文件批量扩充**：
  - 48 个存根文件（原 47–125 行）扩展至 200–250 行，含 Mermaid 流程图、LaTeX 公式、多级章节
  - 涵盖 04_EngineeringAndTechnology、03_HumanitiesAndSocialSciences、06_ArtsAndCreativity 等 10+ 学科门类
- **编码清理收官**：
  - 修复最后 2 个 INDEX.md 文件中的 U+FFFD 乱码
  - 全库 2,301 个 .md 文件零 U+FFFD、零 GBK 伪影、零解码错误 ✅

### 修改
- README 统计同步更新：Markdown 文件数 2,264 → 2,301，行数 339,718 → 474,311，大小 11.3 MB → 16.5 MB

### 修复
- 全库 Mermaid 流程图：`\n` → `<br/>` 替换（57 个文件），确保 Obsidian 正常渲染
- 全库 Markdown 表格：补全表格前后空行（230 个文件）
- 修复 8 个零字节文件（写入过程中损坏）
- 全库 335 个乱码文件重写（100 个 U+FFFD 型 + 235 个 GBK/PUA 型）

## v3.5 (2026-05-16) — 全库优化大版本

### 新增
- **YAML Frontmatter 全覆盖**：2,271 个文件统一添加 `aliases` + `tags`（从路径自动推导）
- **UpperCamelCase 命名规范化**：89 个英文文件名重命名（含 `51_MCU` → `MCU51`, `Node.js` → `NodeJS`）
- **Vocabulary 拆分**：`Vocabulary_3500.md` → 1 字母序全表 + 4 主题分册（2,278 条目）
- **缺失文件创建**：~300 个顶层 Wiki-Link 目标文件（含 30 个关键主题 + 270 个 _Stubs 占位）
- **CI 增强**：新增 markdownlint 检查、失败门禁、超时控制、并发控制
- **Arts 内容恢复**：06_ArtsAndCreativity 下 42 个编码乱码文件通过 WebFetch 恢复中文正文
- **Sports/Management 内容填充**：35 个 stub 文件充实为完整笔记
- **Security 文件**：新增 Cryptography、NetworkSecurity、SecurityFrameworks 等网络安全专题

### 修改
- **全库链接修复**：
  - 修复 1,100+ vault-root 路径缺失前缀错误
  - 修复 35 条 `../` 相对路径导航错误
  - 修复 05_CS/ → 05_ComputerScience/ 错误引用
  - 所有 INDEX 导航链接统一为 vault-root 相对路径
- `.gitignore` 增强：新增 `Desktop.ini`、`*.swp`、`.env` 等模式
- `.gitattributes` 增强：新增 `linguist-detectable`、`export-ignore`、二进制类型声明
- INDEX.md 修复：空标签清理 + 4 个目录 INDEX 补全
- 06_Arts 各 INDEX 文件修复路径引用

### 修复
- 02_NaturalSciences/EarthSciences/PhysicalGeography 下 3 个文件乱码修复（土壤地理学、地貌学、水文地理学）
- 06_ArtsAndCreativity 全部 42 个文件编码损坏修复（GBK→UTF-8 转换乱码）
- 全库破损 Wiki-Link 清零（此前 ~2,500 处 → 0）
- GitHub Actions CI check.yml：修复从不 fail 的问题，添加超时/并发

### 移除
- 旧版 `fix_garbled.py`、`fix_remaining.ps1` 等临时脚本
- `_Stubs/` 目录中 270 个待完善占位文件（保留为内容骨架）

### 基础设施
- Git 仓库优化：`git gc --aggressive`（.git: 17.9 MB → 12.6 MB）
- `.opencode/fixes/` 下保留全部自动化修复脚本

## v3.6 (2026-05-16) — 目录结构优化 + Stub 迁移大版本

### 新增
- **_Stubs 迁移**：268 个存根文件全部归入主分类体系（14 大学科门类下 70+ 个目录），零内容丢失
  - `04_EngineeringAndTechnology`：120+ 个文件迁至 CivilEngineering、MechanicsAndMaterials、ControlAndSystemsEngineering 等 18 个子目录
  - `05_ComputerScience`：50+ 个文件迁至 DataStructuresAndAlgorithms、ProgrammingLanguages、SoftwareEngineering 等 15 个子目录
  - `03_HumanitiesAndSocialSciences`：60+ 个文件迁至 Law、History、Philosophy、Economics、Sociology 等 12 个子目录
  - `02_NaturalSciences`：30+ 个文件迁至 Physics、Chemistry、Biology、EarthSciences 等 6 个子目录
  - 其余迁至 01_K12、06_ArtsAndCreativity、08-13 等目录

### 移除
- **_Stubs 目录**：整体删除（268 个占位文件已全部迁移至主分类）
- **04_EngineeringAndTechnology 存根目录**：删除 4 个仅含 INDEX.md 的重复目录
  - `AerospaceEngineering/`（内容已位于 `AerospaceAndMilitaryEngineering/AerospaceEngineering/`）
  - `MarineEngineering/`（内容已位于 `HydraulicAndMarineEngineering/`）
  - `TextileEngineering/`（内容已位于 `TextileAndFoodEngineering/TextileScience/`）
  - `MiningAndMetallurgicalEngineering/`（内容分散于 `MiningAndMineralEngineering/` 和 `MetallurgicalEngineering/`）
- **04_EngineeringAndTechnology 文件/目录名冲突**：删除 2 个空壳文件
  - `ElectronicsAndCommunications/SignalProcessing.md`（同名目录有实体内容）
  - `EnvironmentalScienceAndEngineering/EnvironmentalEngineering.md`（同名目录有实体内容）
- **根目录辅助文件**：删除 `dedup_related.py`、`fix_garbled.py`、`fix_arts.py`、`fix_remaining.ps1`、`alias_mismatch_temp.txt`、`stale_files.txt`

### 修改
- README 统计同步更新：Markdown 文件数 2,271 → 2,264，内容目录数 530 → 532

## v3.5 (2026-05-16) — 全库优化大版本

### 新增
- 00_KnowledgeFramework 下全部 stub 文件扩充至完整内容（~100-150 行/文件）
- LearningPaths/LearningPaths.md：结构化路径/自主路径/项目路径/跨学科路径分类
- LearningPaths/CourseIndex.md：扩充课程条目至 40+ 门
- Methodology/Methodology.md：三类方法论体系详解
- NoteTaking/NoteTaking.md：Zettelkasten/Cornell/PARA/渐进式总结四大系统

### 修改
- 各模块 README 文件同步更新前方指引链接

## v3.3 (2026-05-10)

### 新增
- 00_KnowledgeFramework 下新增 ClassificationMappings 模块
- 新增 Ebooks/、Infographics/、DataSets/、LicenseAndCopyright/ 模块

### 修改
- 编号重排：09-14 → 08-13
- 多个弱覆盖方向批量扩充目录与内容
- 所有学科目录 README 统一格式模板

### 修复
- 修复交叉引用断裂问题、路径相对链接错误、目录层级错位

## v3.2 (2026-05-09)

### 修改
- Others 目录移至末尾（14_Others）
- 前序目录编号同步前移（01~13）
- README 目录树、覆盖范围表同步更新

### 移除
- 移除重复的旧版 Archive 目录中的冗余文件

## v3.1 (2026-05-09)

### 修改
- 全部顶级目录使用两位数字前缀（00-14）
- 统一所有目录 README 的格式模板

### 新增
- 为每个一级目录添加 README.md 概览文件
- 新增 INDEX.md 索引文件模板

## v3.0 (2026-05-XX)

### 新增
- 完成全部 15 个学科门类四级目录填充
- 新增交叉学科、军事学、管理学、体育学目录

### 修改
- 目录深度统一为四级：学科 → 方向 → 专题 → 知识点
- README 中增加知识覆盖范围总表

## v2.0

### 新增
- 依据 UNESCO 学科分类 + 中国学科门类体系重构目录
- 引入 Obsidian 双向链接体系
- 引入 Zettelkasten 卡片笔记法规范

### 修改
- 目录结构由两级扩展为四级

## v1.0

### 新增
- 初始版本发布
- 基础目录结构建立（10 个一级学科）
- 第一版知识条目填充

---

## 未来计划

### v4.0 (规划中)
- 自动化交叉引用完整性检查（CI 中已有基础实现）
- 增加更多学科的高频面试题与解题思路
- 完善 07_InterdisciplinarySciences 下跨学科主题研究
- 为 _Stubs/ 目录逐步填充内容

### v5.0 (远期规划)
- 增加 Anki 间隔重复卡片导出功能
- 整合 arXiv 论文摘要自动同步
- 建立社区贡献与审稿流程
