---
aliases: [LaTeXTemplates]
tags: ['Templates', 'LaTeXTemplates']
created: 2026-05-16
updated: 2026-05-16
---

# LaTeX 模板

收集和整理常用的 LaTeX 文档模板，覆盖论文、报告、演示文稿、作业等常见场景。每个模板附带代码示例和使用说明。

---

## 常用文档类

| 文档类 | 适用场景 | 特点 |
|--------|----------|------|
| article | 期刊论文、短文档 | 默认无章节编号 |
| report | 技术报告、长文档 | 支持 chapter |
| book | 书籍 | 对称页边距、附录支持 |
| beamer | 演示文稿（PPT 替代） | 基于框架的页面 |
| memoir | 书稿/学位论文 | 极其灵活的定制性 |
| standalone | 独立公式/图片 | 仅生成内容本身 |

### 中文支持

- **ctex 文档类**：ctexart、ctexrep、ctexbook — 原生中文支持
- **xeCJK 宏包**：XeLaTeX 编译下的中日韩文字排版
- **fontspec 宏包**：系统字体设置
- **zhnumber 宏包**：中文数字/日期

```latex
% 推荐的中文配置
\documentclass[UTF8]{ctexart}
% 或使用通用配置
\documentclass[12pt,a4paper]{article}
\usepackage[UTF8]{ctex}
```

---

## 学术论文模板

### IEEE 模板（会议/期刊）

```latex
\documentclass[conference]{IEEEtran}
% 或 \documentclass[journal]{IEEEtran}
\usepackage{cite}
\usepackage{amsmath,amssymb}
\usepackage{graphicx}

\title{A Novel Approach to ...}
\author{\IEEEauthorblockN{Author Name\\
\IEEEauthorblockA{Department, University\\
Email}}
}
\begin{document}
\maketitle
\begin{abstract}
...
\end{abstract}
\keywords{...}
\section{Introduction}
\section{Method}
\section{Experiments}
\section{Conclusion}
\bibliographystyle{IEEEtran}
\bibliography{refs}
\end{document}
```

### ACM 模板

```latex
\documentclass[sigconf]{acmart}
\settopmatter{printfolios=true}
\title{Title}
\author{Author}
\begin{document}
\maketitle
\end{document}
```

### 通用中文学术模板

```latex
\documentclass[12pt,a4paper]{article}
\usepackage[UTF8]{ctex}
\usepackage{amsmath,amssymb}
\usepackage{graphicx}
\usepackage{geometry}
\geometry{left=2.5cm,right=2.5cm,top=2.5cm,bottom=2.5cm}
\usepackage{hyperref}

\title{论文标题}
\author{作者}
\date{\today}

\begin{document}
\maketitle
\begin{abstract}
摘要内容。
\end{abstract}
\section{引言}
\section{相关工作}
\section{方法}
\section{实验}
\subsection{数据集}
\subsection{评价指标}
\subsection{结果分析}
\section{结论}
\bibliographystyle{gbt7714-numerical}
\bibliography{refs}
\end{document}
```

---

## Beamer 演示文稿模板

```latex
\documentclass{beamer}
\usetheme{Madrid}  % 主题：Madrid / Berlin / CambridgeUS / metropolis
\usecolortheme{default}

\title{演示文稿标题}
\author{作者}
\institute{机构}
\date{\today}

\begin{document}

\begin{frame}
\titlepage
\end{frame}

\begin{frame}{目录}
\tableofcontents
\end{frame}

\section{引言}
\begin{frame}{引言}
\begin{itemize}
    \item 要点一
    \item 要点二
\end{itemize}
\end{frame}

\section{核心内容}
\begin{frame}{核心内容}
\begin{block}{定义}
这是定义块
\end{block}
\begin{alertblock}{注意}
警告块
\end{alertblock}
\begin{example}
示例块
\end{example}
\end{frame}

\begin{frame}{代码展示}
\begin{lstlisting}[language=Python]
def hello():
    print("Hello, World!")
\end{lstlisting}
\end{frame}

\end{document}
```

---

## 作业/习题模板

```latex
\documentclass[12pt,a4paper]{article}
\usepackage[UTF8]{ctex}
\usepackage{amsmath,amssymb}
\usepackage{enumerate}

\title{作业标题}
\author{姓名 \quad 学号}
\date{\today}

\begin{document}
\maketitle

\section*{问题 1}
\begin{enumerate}[(a)]
    \item 解答步骤...
    \begin{align*}
        x^2 + y^2 &= z^2
    \end{align*}
    \item 继续解答...
\end{enumerate}

\section*{问题 2}
...
\end{document}
```

---

## 常用命令速查

### 数学模式
| 命令 | 效果 |
|------|------|
| `\frac{a}{b}` | 分数 |
| `\sum_{i=1}^n` | 求和 |
| `\int_a^b` | 积分 |
| `\lim_{x \to 0}` | 极限 |
| `\alpha, \beta, \gamma` | 希腊字母 |
| `\vec{v}` | 向量 |
| `\mathbf{X}` | 矩阵 |
| `\mathcal{L}` | 花体 |
| `\mathbb{R}` | 黑板粗体 |
| `\begin{bmatrix} ... \end{bmatrix}` | 矩阵括号 |
| `\begin{cases} ... \end{cases}` | 分段函数 |
| `\hat{x}, \tilde{x}, \bar{x}` | 上标记 |

### 表格与图片
```latex
% 图片
\includegraphics[width=0.8\textwidth]{figure.png}

% 表格
\begin{table}[htbp]
\centering
\caption{标题}
\begin{tabular}{|c|c|c|}
\hline
列1 & 列2 & 列3 \\
\hline
数据 & 数据 & 数据 \\
\hline
\end{tabular}
\label{tab:label}
\end{table}
```

### 引用与交叉引用
```latex
% 引用文献
\cite{ref_key}

% 交叉引用
\label{sec:intro}
\ref{sec:intro}  % 显示编号
\pageref{sec:intro} % 显示页码

% 脚注
\footnote{注释内容}
```

---

## 模板资源

- **Overleaf 模板库**：https://www.overleaf.com/latex/templates
- **LaTeX 模板中心**：https://www.latextemplates.com
- **清华大学 LaTeX 模板**：https://github.com/tuna/thuthesis
- **中国科学院大学学位论文模板**：https://github.com/mohuangrui/ucasthesis
- **中国国家标准 GB/T 7714-2015**：biblatex-gb7714-2015 宏包

---

## 相关条目

- [[NoteTaking]] — 笔记法（与 LaTeX 笔记模板配合）
- [[AcademicPapers]] — 学术论文写作
- [[Documentation]] — 文档规范
- [[Markdown]] — Markdown 语法（轻量级替代方案）
