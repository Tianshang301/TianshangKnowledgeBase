# BibTeX 入门与使用

## 一、什么是 BibTeX

BibTeX 是 LaTeX 的参考文献管理工具，由 Oren Patashnik 于 1985 年开发。它通过单独的 .bib 文件存储文献数据，配合 .bst 样式文件自动生成格式化的参考文献列表。BibLaTeX 是其后继方案，提供更多功能和灵活性。

## 二、bib 文件结构

一个 .bib 文件包含多条文献条目，每条条目遵循以下格式：

```
@条目类型{引用标签,
   字段1 = {值},
   字段2 = {值},
   ...
}
```

- 引用标签：正文中通过 `\cite{标签}` 引用
- 字段值用花括号 `{}` 或双引号 `""` 包裹
- 各字段之间以逗号分隔（最后一个字段后不加逗号）

## 三、常见条目类型对比
| 条目类型 | 用途 | 必填字段 | 常用可选字段 |
|----------|------|----------|-------------|
| @article | 期刊论文 | author, title, journal, year, volume | number, pages, doi, issn, month |
| @book | 书籍 | author/editor, title, publisher, year | edition, volume, series, isbn |
| @inproceedings | 会议论文 | author, title, booktitle, year | pages, editor, volume, series, doi |
| @phdthesis | 博士论文 | author, title, school, year | month, address, doi |
| @mastersthesis | 硕士论文 | author, title, school, year | month, address, type |
| @incollection | 书中的章节 | author, title, booktitle, publisher, year | editor, pages, chapter |
| @techreport | 技术报告 | author, title, institution, year | number, address, month, type |
| @misc | 杂项 | 无必填 | author, title, howpublished, year, note |
| @proceedings | 会议论文集 | title, year | editor, publisher, organization |
| @inbook | 书中的一部分 | author/editor, title, chapter/pages, publisher, year | edition, series |

## 四、字段说明
核心字段详解：
- author：作者名，多作者用 `and` 分隔。格式：`First Last` 或 `Last, First`
  - 示例：`author = {John Smith and Jane Doe}`
- editor：编者（格式同 author）
- title：标题。对书名、期刊名使用大小写敏感时，用花括号保护
  - 示例：`title = {The {LaTeX} Companion}`
- journal：期刊名称
- year：出版年份
- volume：卷号
- number：期号（期刊）或报告号
- pages：页码，格式为 `12--34`（使用双连字符）
- publisher：出版商
- address：出版地
- doi：数字对象标识符
- url：在线链接
- note：补充说明

## 五、示例 bib 条目

```
@article{li2023deep,
  author    = {Li, Ming and Zhang, Wei and Wang, Yu},
  title     = {Deep Learning for Natural Language Processing: A Comprehensive Survey},
  journal   = {Journal of Artificial Intelligence Research},
  year      = {2023},
  volume    = {76},
  number    = {2},
  pages     = {345--389},
  doi       = {10.1613/jair.1.14567}
}

@book{knuth1984tex,
  author    = {Knuth, Donald E.},
  title     = {The {TeX}book},
  publisher = {Addison-Wesley},
  year      = {1984},
  address   = {Reading, Massachusetts},
  isbn      = {0-201-13448-9}
}

@inproceedings{vaswani2017attention,
  author    = {Vaswani, Ashish and Shazeer, Noam and Parmar, Niki and others},
  title     = {Attention Is All You Need},
  booktitle = {Advances in Neural Information Processing Systems},
  year      = {2017},
  volume    = {30},
  pages     = {5998--6008}
}

@phdthesis{zhang2022representation,
  author  = {Zhang, Yiming},
  title   = {Representation Learning on Graph-Structured Data},
  school  = {Peking University},
  year    = {2022},
  month   = jun
}

@misc{openai2023gpt,
  author       = {{OpenAI}},
  title        = {{GPT}-4 Technical Report},
  howpublished = {arXiv:2303.08774},
  year         = {2023},
  note         = {Preprint}
}
```

## 六、在 LaTeX 中使用 BibTeX

基本流程：
1. 在 LaTeX 源文件中：
   ```
   \documentclass{article}
   \bibliographystyle{plain}  % 指定 .bst 样式
   \begin{document}
   ...正文内容，使用 \cite{li2023deep} 引用...
   \bibliography{myrefs}  % 指定 .bib 文件（不含扩展名）
   \end{document}
   ```

2. 编译流程（四步）：
   ```
   pdflatex paper.tex       % 生成 .aux 文件
   bibtex paper             % 根据 .aux 中的引用生成 .bbl
   pdflatex paper.tex       % 插入参考文献
   pdflatex paper.tex       % 更新交叉引用
   ```

3. 常用引用命令：
   - `\cite{key}` — 标准引用
   - `\citep{key}` — 括号引用（需 natbib 包）
   - `\citet{key}` — 文本引用（需 natbib 包）
   - `\cite[page 12]{key}` — 带页码引用
   - `\nocite{*}` — 列出 .bib 中所有文献
   - `\citen{key}` — 上标引用

## 七、BibTeX 样式文件（bst）
常用内置样式：
| 样式 | 引用格式 | 参考文献格式 |
|------|----------|-------------|
| plain | [1] 数字编号 | 按首次引用顺序排列 |
| unsrt | [1] 数字编号 | 按引用出现顺序排列（同 plain 但顺序不同） |
| alpha | [Knu84] 作者+年份缩写 | 按标签字母顺序排列 |
| abbrv | [1] 数字编号 | 名字、月份等缩写 |
| apalike | (Knuth, 1984) | 著者-出版年制 |
| ieeetr | [1] 数字编号 | IEEE 格式 |
| siam | [1] 数字编号 | SIAM 期刊格式 |

自定义样式可使用 `makebst` 工具（随 LaTeX 发行版提供）交互式生成。

## 八、常见问题与技巧
| 问题 | 解决方法 |
|------|----------|
| 引用问号出现 | 重新编译：pdflatex -> bibtex -> pdflatex x2 |
| 特殊字符处理 | 使用 `{\"o}` 或 `\"o` 表示 umlaut 等变音符号 |
| 中文文献 | 使用 `ctex` 包，BibTeX 配合 `gbt7714` 样式 |
| URL 过长换行 | 使用 `url` 包，或 `\usepackage{breakurl}` |
| 同一作者多篇文献 | 在 year 后加 a, b, c 区分（如 2023a, 2023b） |
| 标题保持大小写 | 对专有名词用花括号包裹：`{Deep Learning}` |

## 参考资料
- BibTeX 官方文档：tug.org/bibtex
- LaTeX 维基百科：en.wikibooks.org/wiki/LaTeX/Bibliography_Management
- Oetiker 等人《The Not So Short Introduction to LaTeX》
- GB/T 7714-2015 信息与文献参考文献著录规则
- JabRef 参考文献管理软件：jabref.org
- biblatex 包文档：ctan.org/pkg/biblatex
- natbib 包文档：ctan.org/pkg/natbib

## 相关条目

[[AcademicPapers]], CitationManagement, [[ResearchMethods]], [[LaTeX]]
