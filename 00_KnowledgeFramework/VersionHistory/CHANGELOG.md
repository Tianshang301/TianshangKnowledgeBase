# 版本历史

记录 TianshangKnowledgeBase 的重要更新。本文件遵循语义化版本规范（Semantic Versioning）。

格式说明：
- **新增**：新条目、新目录、新文件
- **修改**：内容更新、结构优化
- **修复**：错误修正、链接修复
- **移除**：删除过时内容

---

## v3.4 (2026-05-12)

### 新增
- 00_KnowledgeFramework 下全部 stub 文件扩充至完整内容（~100-150 行/文件）
- LearningPaths/LearningPaths.md：增加结构化路径/自主路径/项目路径/跨学科路径分类，增加 5 步设计法
- LearningPaths/CourseIndex.md：扩充计算机、数学、物理、经济学、生物学课程条目至 40+ 门
- LearningPaths/OpenCourseware_INDEX.md：增加国际平台详情表、国内平台、垂直领域资源、学习建议
- Methodology/Methodology.md：增加三类方法论体系详解（学习/研究/问题解决），费曼技巧 5 步法，SQ3R 步骤，策略选择矩阵
- NoteTaking/NoteTaking.md：增加 Zettelkasten/Cornell/PARA/渐进式总结四大系统，数字笔记组织策略，三级回顾体系
- Templates/LaTeX_Templates.md：增加 IEEE/ACM/通用中文/Beamer/作业五套完整模板，常用命令速查表

### 修改
- 各模块 README 文件同步更新前方指引链接
- Methodology.md 增加方法论选择决策矩阵
- NoteTaking.md 增加工具推荐对比表
- LaTeX_Templates.md 增加数学命令/表格/引用示例代码

## v3.3 (2026-05-10)

### 新增
- 00_KnowledgeFramework 下新增 ClassificationMappings 模块（UNESCO/中国学科交叉映射）
- 新增 Ebooks/ 电子书管理模块，包含索引与工具指南
- 新增 Infographics/ 信息图模块，包含信息图设计原理
- 新增 DataSets/ 数据集索引模块
- 新增 LicenseAndCopyright/ 许可证与版权模块

### 修改
- 编号重排：09-14 → 08-13（08_ArchiveAndReferences 已合并入 00）
- 多个弱覆盖方向批量扩充目录与内容
- 00_KnowledgeFramework 目录结构精简优化
- 所有学科目录 README 统一格式模板
- 优化 07_InterdisciplinarySciences 下的跨学科笔记整理规范

### 修复
- 修复 03_Engineering 下交叉引用断裂问题
- 修复部分学科目录中 README 的路径相对链接错误
- 修复 12_Arts 目录下的分类层级错位

## v3.2 (2026-05-09)

### 修改
- Others 目录移至末尾（14_Others）
- 前序目录编号同步前移（01~13）
- README 目录树、覆盖范围表同步更新
- 调整 12_Arts 子目录为 10+ 个二级目录

### 移除
- 移除重复的旧版 Archive 目录中的冗余文件
- 删除过时的 TODO 标记文件

## v3.1 (2026-05-09)

### 修改
- 全部顶级目录使用两位数字前缀（00-14）
- 排序优化：00 知识框架 → 14 体育学
- README 目录树、覆盖范围表同步更新
- 统一所有目录 README 的格式模板

### 新增
- 为每个一级目录添加 README.md 概览文件
- 新增 INDEX.md 索引文件模板

## v3.0 (2026-05-XX)

### 新增
- 完成全部 15 个学科门类四级目录填充
- 新增交叉学科目录（07_InterdisciplinarySciences）
- 新增军事学目录（11_MilitaryScience）
- 新增管理学目录（10_Management）
- 新增体育学目录（14_SportsScience）

### 修改
- Others 移至末位并重新编号
- 目录深度统一为四级：一级（学科）→ 二级（方向）→ 三级（专题）→ 四级（知识点）
- README 中增加知识覆盖范围总表

## v2.0

### 新增
- 依据 UNESCO 学科分类 + 中国学科门类体系重构目录
- 新增交叉学科、军事学、管理学、体育学目录
- 引入 Obsidian 双向链接体系
- 引入 Zettelkasten 卡片笔记法规范

### 修改
- 目录结构由两级扩展为四级
- 文件命名规范统一为中文 + 英文驼峰混合

## v1.0

### 新增
- 初始版本发布
- 基础目录结构建立（10 个一级学科）
- 核心 README 文件
- 第一版知识条目填充

---

## 未来计划

### v4.0 (规划中)
- 引入知识图谱可视化（基于 Obsidian Graph View + Gephi）
- 建立自动化交叉引用检查脚本
- 增加更多学科的高频面试题与解题思路
- 完善 07_InterdisciplinarySciences 下跨学科主题研究

### v5.0 (远期规划)
- 增加 Anki 间隔重复卡片导出功能
- 整合 arXiv 论文摘要自动同步
- 建立社区贡献与审稿流程
