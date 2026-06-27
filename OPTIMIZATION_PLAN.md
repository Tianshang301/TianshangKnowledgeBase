---
aliases: [OPTIMIZATION_PLAN]
tags: ['untagged']
---

# TianshangKnowledgeBase 优化计划

---

## 一、CI/CD 自动化加固

### 1.1 完整链接检查（三类链接全覆盖）

**现状：** 仅检查 simple-name `[[Link]]`（无路径分隔符），漏检：
-  vault-root 相对路径 `[[Dir/Subdir/File]]`
-  相对路径 `[[../Sibling/File]]`

**方案：**

```yaml
# 新增步骤：完整 wiki-link 检查
- name: Check all wiki-links (full coverage)
  run: |
    exit_code=0
    find . -name '*.md' -not -path './.git/*' | while read f; do
      dir=$(dirname "$f")
      grep -oP '\[\[\K[^\]|#]+' "$f" | while read link; do
        # 清理显示名和锚点
        target=$(echo "$link" | cut -d'|' -f1 | cut -d'#' -f1 | sed 's/^[[:space:]]*//;s/[[:space:]]*$//')
        [ -z "$target" ] && continue
        [ "$target" = "INDEX" -o "$target" = "LearningPath" -o "$target" = "README" -o "$target" = "404" ] && continue
        
        # Type 1: simple-name [[Link]]
        if ! echo "$target" | grep -q '/'; then
          if [ ! -f "$dir/$target.md" ]; then
            # Type 2: vault-root relative [[Dir/File]]
            if [ ! -f "$target.md" ]; then
              echo "BROKEN: $target (from $f)"
              exit_code=1
            fi
          fi
        else
          # Type 3: path-based [[Dir/Subdir/File]]
          if [ ! -f "$target.md" ]; then
            # Try relative from source dir
            resolved="$dir/$target.md"
            if [ ! -f "$resolved" ]; then
              echo "BROKEN: $target (from $f)"
              exit_code=1
            fi
          fi
        fi
      done
    done
    exit $exit_code
```

### 1.2 Frontmatter 校验

**现状：** 无任何 frontmatter 检查

**方案：** 新增 CI 步骤验证所有 `.md` 文件具有正确 frontmatter：

```yaml
- name: Validate frontmatter
  run: |
    exit_code=0
    find . -name '*.md' -not -path './.git/*' | while read f; do
      header=$(head -1 "$f")
      if [ "$header" != "---" ]; then
        echo "MISSING FM: $f"
        exit_code=1
        continue
      fi
      # 检查 aliases 存在
      if ! grep -q '^aliases:' "$f"; then
        echo "MISSING aliases: $f"
        exit_code=1
      fi
      # 检查 tags 存在
      if ! grep -q '^tags:' "$f"; then
        echo "MISSING tags: $f"
        exit_code=1
      fi
    done
    exit $exit_code
```

### 1.3 命名规范检查

**现状：** 不检查文件名是否符合 UpperCamelCase

**方案：** 新增 CI 步骤验证英文文件名：

```yaml
- name: Check file naming convention (UpperCamelCase)
  run: |
    exit_code=0
    find . -name '*.md' -not -path './.git/*' -not -path './.obsidian/*' | while read f; do
      base=$(basename "$f" .md)
      # 只检查纯英文文件（不含中文）
      if echo "$base" | grep -qP '^[A-Za-z0-9_]+$'; then
        if ! echo "$base" | grep -qP '^[A-Z][a-zA-Z0-9]*$'; then
          # 允许 INDEX, README, LearningPath 等约定名
          case "$base" in
            INDEX|README|LearningPath|404) ;;
            *) echo "NON-CONFORMING: $f"; exit_code=1 ;;
          esac
        fi
      fi
    done
    exit $exit_code
```

### 1.4 孤立文件检测

**现状：** 无入链检测，大量文件可能没有任何链接指向它们

**方案：**

```yaml
- name: Find orphan files (no incoming wiki-links)
  run: |
    exit_code=0
    find . -name '*.md' -not -path './.git/*' -not -name 'INDEX.md' -not -name 'README.md' -not -name '404.md' -not -name 'LearningPath.md' | while read f; do
      basename_noext=$(basename "$f" .md)
      # 搜索全库是否有 wiki-link 指向该文件
      if ! grep -qr "\[\[$basename_noext" --include='*.md' . 2>/dev/null; then
        # 也检查路径链接 [[Dir/File]]
        rel=$(echo "$f" | sed 's|^\./||;s|\.md$||')
        if ! grep -qr "\[\[$rel" --include='*.md' . 2>/dev/null; then
          echo "ORPHAN: $f (no incoming links)"
          exit_code=1
        fi
      fi
    done
    exit $exit_code
```

### 1.5 markdownlint 渐进收紧

**现状：** 仅启用 4/14 条规则

**阶段一（当前）：** 保持现有规则
**阶段二（2周后）：** 新增：
- `MD001` (heading increment) — 标题层级递增
- `MD007` (unordered list indentation) — 无序列表缩进
- `MD029` (ordered list item prefix) — 有序列表编号
**阶段三（1月后）：** 再新增：
- `MD026` (no trailing punctuation in heading)
- `MD030` (spaces after list markers)
- `MD034` (no bare URLs)

### 1.6 其他 CI 改进

- 增加 `actions/cache@v4` 缓存 markdownlint 工具（加速）
- 增加外链死链检查（`lychee` 或 `github.com/lycheeverse/lychee-action`），每月定时运行而非每次 push
- 增加编码检查（UTF-8 without BOM）

---

## 二、维护脚本优化

### 2.1 脚本可移植化

**现状：** 所有 Python 脚本硬编码 `BASE = r'F:\TianshangKnowledgeBase'`

**方案：** 统一使用环境变量 + 自动发现：

```python
import os
import pathlib

# 自动发现：从脚本所在目录向上找到项目根
SCRIPT_DIR = pathlib.Path(__file__).resolve().parent
# 项目根特征：存在 INDEX.md
for p in [SCRIPT_DIR, *SCRIPT_DIR.parents]:
    if (p / 'INDEX.md').exists():
        BASE = str(p)
        break
else:
    # 回退到环境变量
    BASE = os.environ.get('KNOWLEDGE_BASE_DIR', os.getcwd())
```

所有脚本统一引入此逻辑，消除硬编码。

### 2.2 备份机制

**现状：** 脚本原地修改文件，无自动备份

**方案：** 在每个修复脚本中添加 git stash 或自动快照：

```python
import subprocess
# 执行前自动 commit 当前状态
subprocess.run(['git', 'stash', '--include-untracked'], cwd=BASE)
# 或者建立临时备份目录
import shutil, tempfile
backup_dir = tempfile.mkdtemp(prefix='kb_backup_')
for f in modified_files:
    shutil.copy2(f, os.path.join(backup_dir, os.path.relpath(f, BASE)))
```

### 2.3 硬编码映射自动发现

**现状：** `fix_all_broken.py` 中 250+ 条 `TOPIC_DIR_MAP` 硬编码

**方案：** 改为从目录结构自动推导主题映射：

```python
def auto_discover_topic_map(base_path):
    """从实际目录结构自动建立主题→目录映射"""
    topic_map = {}
    for root, dirs, files in os.walk(base_path):
        if '.git' in root or '.obsidian' in root:
            continue
        rel = os.path.relpath(root, base_path).replace('\\', '/')
        for f in files:
            if f.endswith('.md') and f not in ('INDEX.md', 'README.md', 'LearningPath.md'):
                name = f[:-3]
                topic_map[name] = rel
                # 也注册文件夹名作为主题
                rel_parts = rel.split('/')
                for p in rel_parts:
                    topic_map[p] = rel
    return topic_map
```

保留手写映射作为 override，自动发现作为 fallback。

### 2.4 依赖管理

**现状：** 无 `requirements.txt` 或 `pyproject.toml`

**方案：** 创建 `.opencode/fixes/requirements.txt`：

```
# 核心依赖（当前脚本仅依赖标准库）
# 如需第三方库请在此添加
# pip install -r requirements.txt
```

同时创建 `.opencode/fixes/pyproject.toml` 用于 ruff 等工具配置。

### 2.5 `.gitignore` 细化

**现状：** `*.py` 匹配所有目录，导致 `.opencode/fixes/` 下的脚本不被追踪

**方案：**

```
# 根目录级别脚本忽略（如果有）
/*.py

# 但保留 .opencode/fixes/ 下的脚本
!.opencode/fixes/*.py
!.github/**/*.py

# Python cache
__pycache__/
*.pyc
.ruff_cache/
```

---

## 三、内容与结构质量

### 3.1 日期元数据批量补充

**现状：** 仅 ~87/2301 文件有 `created`/`updated` 字段（~4%）

**方案：**

```python
# 批量补充日期字段
# 对于无日期的文件：
# - created: 从 git log 获取首次提交日期
# - updated: 从 git log 获取最后修改日期
import subprocess, os

def get_git_date(filepath, fmt='%Y-%m-%d'):
    """从 git 历史获取文件创建和修改日期"""
    try:
        # 首次提交日期
        created = subprocess.run(
            ['git', 'log', '--follow', '--format=%ai', '--reverse', filepath],
            cwd=BASE, capture_output=True, text=True, timeout=10
        ).stdout.strip().split('\n')[0].split()[0]
        # 最后修改日期
        updated = subprocess.run(
            ['git', 'log', '--follow', '-1', '--format=%ai', filepath],
            cwd=BASE, capture_output=True, text=True, timeout=10
        ).stdout.strip().split()[0]
        return created, updated
    except:
        return None, None
```

**优先级：** 先补充有实际内容的文件（非 stub），INDEX/LearningPath 可选。

### 3.2 Stub 文件智能填充

**现状：** 大量 stub 文件仅含 frontmatter + 标题 + "此页面未完成"

**方案：**

1. **从链接上下文推断内容：** 搜集所有指向该 stub 的链接文本（`[[Stub|显示名]]`），作为内容线索
2. **模板增强：** 使用更详细的模板：

```markdown
---
aliases: [TopicName]
tags: ['Category', 'Topic']
status: stub
---

# TopicName

> 此页面为占位 stub，内容待补充。

## 相关条目
<!-- 从入链自动生成 -->
- [[SourceA|链接文本 A]]
- [[SourceB|链接文本 B]]
```

### 3.3 重复目录合并

**现状：**

| 路径 A | 路径 B | 操作 |
|--------|--------|------|
| `05_CS/CloudComputing/` | `05_CS/CloudComputingAndDistributedSystems/` | 合并到 B，A 重定向 |
| `05_CS/AI/NLP/` | `05_CS/AI/NaturalLanguageProcessing/` | 合并到 NLP |

**合并策略：**
1. 将 B 的内容合并到 A（文件去重，取内容更完整的）
2. 在 B 位置创建 `.md` 重定向文件（内容仅含 frontmatter + `> 此页面已移至 [[A/INDEX]]`）
3. 全局搜索旧链接并更新

### 3.4 命名规范清理

**现状：** 少量目录使用下划线而非 UpperCamelCase（如 `01_K12/Arts_and_Sports/`）

**方案：**
1. 扫描所有二级及以下目录，识别非 UpperCamelCase 名称
2. 生成重命名映射
3. 全局更新所有 wiki-link 引用
4. 执行 git mv

### 3.5 `status` 字段引入

**方案：** 在 frontmatter 中添加可选 `status` 字段，取值为：
- `stub` — 占位页面，内容极少
- `seedling` — 初稿，骨架已全
- `growing` — 内容持续补充中
- `evergreen` — 内容基本完善

配合 Dataview 可生成内容成熟度仪表盘：

```dataview
TABLE status, length(file.outlinks) AS 出链数, length(file.inlinks) AS 入链数
FROM ""
WHERE status
SORT choice(status = 'evergreen', 0, choice(status = 'growing', 1, choice(status = 'seedling', 2, 3)))
```

---

## 四、性能优化

### 4.1 大文件拆分

**现状：** 部分文件过大

**扫描命令：**

```bash
find . -name '*.md' -not -path './.git/*' -exec wc -l {} + | sort -rn | head -20
```

**拆分标准：**
- `> 500 行` — 警告，考虑拆分为子主题
- `> 1000 行` — 必须拆分

**拆分方法：** 按章节分隔，拆分为多个文件，原文件变为 MOC（Map of Content）。

### 4.2 目录深度优化

**现状：** 最深 5 级目录（`05_CS/DataStructuresAndAlgorithms/Algorithms/BFSDFS.md`）

**建议：** 保持 ≤ 3 级深度。对于深入内容，使用 wiki-link 而非目录嵌套：

```
05_ComputerScience/
  DataStructuresAndAlgorithms/
    INDEX.md          <-- 这里链接到 Algorithms/BFSDFS
    DataStructures/
    Algorithms/
      INDEX.md        <-- 列出所有算法
```

### 4.3 Obsidian 性能调优

**建议配置（`.obsidian/app.json`）：**

```json
{
  "livePreview": false,
  "spellcheck": false,
  "showFrontmatter": false,
  "strictLineBreaks": true,
  "useTab": false,
  "tabSize": 2
}
```

**建议插件优化：**
- 禁用不必要的核心插件（如日记、录音、幻灯片）
- 使用 Obsidian 1.5+ 的 Properties 替代部分 Dataview 查询

---

## 五、工程化与可维护性

### 5.1 Pre-commit Hook

**方案：** 配置 pre-commit 框架

`.pre-commit-config.yaml`：

```yaml
repos:
  - repo: https://github.com/pre-commit/mirrors-prettier
    rev: v3.0.0
    hooks:
      - id: prettier
        types: [markdown]
  - repo: https://github.com/igorshubovych/markdownlint-cli
    rev: v0.37.0
    hooks:
      - id: markdownlint
  - repo: local
    hooks:
      - id: check-ufffd
        name: Check U+FFFD
        entry: grep -rl $'\ufffd' --include='*.md' .
        language: system
        fail_fast: false
      - id: check-trailing-whitespace
        name: Check trailing whitespace
        entry: grep -rnP '\s+$' --include='*.md' .
        language: system
        fail_fast: false
```

安装：`pip install pre-commit && pre-commit install`

### 5.2 CHANGELOG

**方案：** 创建 `CHANGELOG.md`，采用 Keep a Changelog 格式：

```markdown
# Changelog

## [Unreleased]

### Added
- CI: Wiki-link 完整覆盖检查
- CI: Frontmatter 校验
- CI: 命名规范检查

### Changed
- 脚本可移植化（消除硬编码路径）
- .gitignore 细化

### Fixed
- 修复重复目录冲突
- 补充日期元数据

## [1.0.0] - 2026-05-18

### Added
- 初始版本：14 大学科门类，2301 个 Markdown 文件
```

### 5.3 PR 模板

**方案：** 创建 `.github/PULL_REQUEST_TEMPLATE.md`：

```markdown
## 变更类型
- [ ] 新内容
- [ ] 内容修订
- [ ] 结构重组
- [ ] CI/工具链
- [ ] Bug 修复

## 变更描述
<!-- 简要描述变更内容和动机 -->

## 检查清单
- [ ] Frontmatter (aliases + tags) 完整
- [ ] 所有 wiki-link 可解析
- [ ] 无尾部空白
- [ ] 无 U+FFFD
- [ ] 命名符合 UpperCamelCase
```

### 5.4 静态站发布

**推荐方案：** Quartz (https://quartz.jzhao.xyz/)

- 原生支持 Obsidian 语法（wiki-link、嵌入、frontmatter）
- 支持 Graph View
- 一键部署到 GitHub Pages

**备选方案：** mkdocs-material + mkdocs-roamlinks-plugin

```bash
# 安装
pip install mkdocs-material mkdocs-roamlinks-plugin

# mkdocs.yml
site_name: TianshangKnowledgeBase
theme:
  name: material
plugins:
  - roamlinks
  - search
```

---

## 六、执行路线图

### Phase 1 — 基础设施（1-2 天）
- [x] 备份知识库
- [x] 脚本可移植化（消除硬编码路径）
- [ ] .gitignore 细化
- [ ] 创建 requirements.txt + pyproject.toml

### Phase 2 — CI/CD（1 天）
- [ ] 完整链接检查（三类链接全覆盖）
- [ ] Frontmatter 校验
- [ ] 命名规范检查
- [ ] markdownlint 规则收紧

### Phase 3 — 内容质量（2-3 天）
- [ ] 日期元数据批量补充
- [ ] Stub 文件模板升级
- [ ] 重复目录合并
- [ ] 命名规范清理

### Phase 4 — 工程化（1 天）
- [ ] Pre-commit hook 配置
- [ ] CHANGELOG 创建
- [ ] PR 模板

### Phase 5 — 持续优化（长期）
- [ ] 孤立文件检测与处理
- [ ] 大文件拆分
- [ ] 静态站发布
- [ ] 外链死链定时检查
- [ ] status 字段引入

---

## 七、薄弱门类内容补充计划

基于 2026-05 全库扫描分析，14 个门类中 3 个最薄弱门类的针对性补充方案。

### 7.1 优先级总览

| 优先级 | 门类 | 当前文件数 | 目标文件数 | 需补充 |
|:------:|------|:----------:|:----------:|:------:|
| P0 | 10_军事科学 | 29 | 45+ | 16 篇 |
| P1 | 11_管理科学 | 49 | 65+ | 16 篇 |
| P2 | 09_医药健康 | 52 | 70+ | 18 篇 |

> 07_交叉学科（69 篇）和 08_农学（68 篇）内容较完整，仅需少量扩写，不列入本轮重点。

### 7.2 P0 — 10_军事科学（29 → 45+）

现有文件质量高（平均 12.5 KB），但 LearningPath 规划的大量专题缺失。

#### 第一批：新增核心缺项（5 篇）

| 文件 | 说明 |
|------|------|
| `MilitaryGeography.md` | 军事地理学，基础前提学科 |
| `MilitaryOperationsResearch.md` | 军事运筹学，定量分析基础 |
| `ArmsAndServices.md` | 军兵种知识（陆海空火战支） |
| `C4ISR.md` | 指挥信息系统，信息化战争核心 |
| `UnmannedSystems.md` | 无人系统与无人机作战，当前热点 |

#### 第二批：新增专题（5 篇）

| 文件 | 说明 |
|------|------|
| `InformationWarfare.md` | 信息化战争，扩展 MilitaryTechnology |
| `SpaceStrategy.md` | 太空战略，新兴战略领域 |
| `SpecialOperations.md` | 特种作战，LearningPath 规划 |
| `UrbanWarfare.md` | 城市战，LearningPath 规划 |
| `AmphibiousOperations.md` | 两栖作战，LearningPath 规划 |

#### 第三批：扩充子目录（6 篇）

- `NationalDefense/` 从 4 篇扩至 6-7 篇（国防工业、兵役制度、国防预算）
- `MilitaryLogistics/` 从 2 篇扩至 4-5 篇（军事供应链、医疗后送）

### 7.3 P1 — 11_管理科学（49 → 65+）

现有内容扎实（平均 9.5 KB），缺少学科基础课核心文件。

#### 第一批：新增核心缺项（5 篇）

| 文件 | 说明 |
|------|------|
| `ManagementPrinciples.md` | 管理学原理，七大职能（计划/组织/领导/控制） |
| `OrganizationalBehavior.md` | 组织行为学，核心基础 |
| `StrategicManagement.md` | 战略管理，工商管理顶石课程 |
| `Microeconomics.md` | 微观经济学，衔接 03_Economics |
| `Macroeconomics.md` | 宏观经济学，同上 |

#### 第二批：新增专题 + 扩写（5 篇）

| 文件 | 说明 |
|------|------|
| `BusinessEthics.md` | 商业伦理，LearningPath 规划 |
| `EconomicLaw.md` | 经济法，LearningPath 规划 |
| `ManagementInformationSystems.md` | 管理信息系统，管科缺项 |
| `NonprofitManagement.md` | 非营利组织管理，公共管理缺项 |
| `OperationsManagement.md` | 运营管理，LearningPath 规划 |

#### 第三批：扩充子目录 + 结构整理（6 篇）

- `PublicAdministration/` 从 4 篇扩至 6+ 篇（公共管理理论、城市治理）
- `LibraryAndArchive/` 从 4 篇扩至 6+ 篇（数字图书馆、元数据标准）
- 根层级 `Productivity.md` / `TimeBlocking.md` 等归入子目录

### 7.4 P2 — 09_医药健康（52 → 70+）

现有内容平均 10.7 KB，部分核心文件偏薄（Physiology 7.5KB、InternalMedicine 7.5KB、Surgery 7.4KB）。

#### 第一批：新增基础与临床核心（6 篇）

| 文件 | 说明 |
|------|------|
| `BiochemistryAndMolecularBiology.md` | 生物化学与分子生物学，基础医学核心缺项 |
| `HistologyAndEmbryology.md` | 组织学与胚胎学，基础医学缺项 |
| `Pathophysiology.md` | 病理生理学，基础→临床桥梁课 |
| `Neurology.md` | 神经病学，五大临床主干之一 |
| `Psychiatry.md` | 精神病学，重要临床学科 |
| `Anesthesiology.md` | 麻醉学，围术期关键学科 |

#### 第二批：扩写薄文件（5 篇）

| 文件 | 现状 | 目标 | 说明 |
|------|:---:|:----:|------|
| `Epidemiology.md` | 4.5 KB | 10 KB+ | 当前为提纲式，改叙述体 |
| `Physiology.md` | 7.5 KB | 12 KB+ | 追赶 Anatomy 深度 |
| `InternalMedicine.md` | 7.5 KB | 15 KB+ | 最重要的临床学科 |
| `Surgery.md` | 7.4 KB | 15 KB+ | 同上 |
| `Virology.md` | 5.3 KB | 10 KB+ | 后疫情时代基本要求 |

#### 第三批：新增临床缺项 + 扩写（7 篇）

| 文件 | 说明 |
|------|------|
| `MedicalStatistics.md` | 医学统计学，LearningPath 规划 |
| `Ophthalmology.md` | 眼科学，临床缺项 |
| `Otorhinolaryngology.md` | 耳鼻咽喉科学，临床缺项 |
| `Dermatology.md` | 皮肤性病学，临床缺项 |
| `MedicalPhysics.md` 扩写 | 4.7 KB → 8 KB+ |
| 扩写 `ChineseMateriaMedica.md` | 8.3 KB → 12 KB+ |
| 扩写 `TraditionalChineseMedicine.md` | 5.1 KB → 10 KB+ |

### 7.5 工作量汇总

| 阶段 | 军事 | 管理 | 医药 | 合计 |
|:----:|:----:|:----:|:----:|:----:|
| 第一批（新增核心缺项） | 5 | 5 | 6 | **16 篇** |
| 第二批（专题/扩写） | 5 | 5 | 5 | **15 篇** |
| 第三批（扩充/完善） | 6 | 6 | 7 | **19 篇** |
| **总计** | **16 篇** | **16 篇** | **18 篇** | **~50 篇** |

### 7.6 写作规范

- 体例沿用已有文件：YAML frontmatter（`aliases` + `tags` + `created`），UpperCamelCase 文件名
- 篇幅参照同目录文件：平均 10-15 KB / 150-250 行
- 结构：概述 → 分节 → 表格/图表 → 参考文献
- 跨门类引用：军事地理 ↔ 地球科学；经济学 ↔ 人文社科；生化 ↔ 生物学

### 7.7 纳入执行路线图

```
### Phase 6 — 内容补充（长期，分批执行）
- [ ] P0 军事科学第一批（5 篇核心缺项）
- [ ] P0 军事科学第二批（5 篇专题）
- [ ] P0 军事科学第三批（6 篇扩充）
- [ ] P1 管理科学第一批（5 篇核心缺项）
- [ ] P1 管理科学第二批（5 篇专题）
- [ ] P1 管理科学第三批（6 篇扩充+整理）
- [ ] P2 医药健康第一批（6 篇核心缺项）
- [ ] P2 医药健康第二批（5 篇扩写）
- [ ] P2 医药健康第三批（7 篇临床缺项+扩写）
```
