---
aliases: [LaTeX]
tags: ['DigitalNotes', 'LaTeX', 'LaTeX']
created: 2026-05-16
updated: 2026-05-16
---

# LaTeX 完全指南

## 概述

LaTeX 是一个基于 TeX 的文档排版系统，广泛用于学术论文、技术报告和书籍的编写。与传统所见即所得编辑器（如 Word）不同，LaTeX 采用"所想即所得"的编写方式，用户专注于内容，由系统自动处理排版。

---

## 一、LaTeX vs Word

| 特性 | LaTeX | Microsoft Word |
|------|-------|---------------|
| 排版质量 | 专业出版级别 | 一般 |
| 数学公式 | 极佳（原生支持） | 差（公式编辑器） |
| 文献管理 | BibTeX/biblatex 自动化 | 手动或 Zotero |
| 版本控制 | 纯文本，Git 友好 | 二进制文件难合并 |
| 学习曲线 | 陡峭 | 平缓 |
| 协作 | 可 diff / 可 review | 修订模式 |
| 图表管理 | 浮动体自动定位 | 手动放置 |
| 模板 | 丰富（期刊提供） | 有限 |

### 1.2 TeX 发行版

| 发行版      | 平台                  | 特点              |
| -------- | ------------------- | --------------- |
| TeX Live | Windows/Linux/macOS | 最完整，推荐          |
| MiKTeX   | Windows             | 轻量级，按需安装包       |
| MacTeX   | macOS               | Mac 上的 TeX Live |

---

## 二、文档结构

### 2.1 基本框架

```latex
\documentclass[12pt,a4paper]{article}

% 导言区 (Preamble)
\usepackage[UTF8]{ctex}       % 中文支持
\usepackage{amsmath,amssymb}  % 数学符号
\usepackage{geometry}         % 页面设置
\geometry{margin=2.5cm}
\usepackage{graphicx}         % 插图
\usepackage{hyperref}         % 超链接

\title{LaTeX 入门指南}
\author{作者姓名}
\date{\today}

\begin{document}
\maketitle
\tableofcontents
\newpage

% 正文
\section{引言}
这里是正文内容...

\end{document}
```

### 2.2 文档类

| 文档类 | 用途 | 适用场景 |
|--------|------|----------|
| article | 文章、短文 | 期刊论文、短报告 |
| report | 长报告、论文 | 学位论文、技术报告 |
| book | 书籍 | 教科书、专著 |
| beamer | 幻灯片 | 演讲、会议展示 |
| memoir | 自定义 | 书籍设计定制 |

---

## 三、文本格式

### 3.1 基本格式

```latex
\textbf{粗体文本}
\textit{斜体文本}
\underline{下划线文本}
\texttt{等宽字体}
\textsc{小型大写字母}
\textcolor{red}{红色文本}

字体大小:
\tiny \scriptsize \footnotesize \small \normalsize 
\large \Large \LARGE \huge \Huge
```

### 3.2 列表环境

```latex
无序列表:
\begin{itemize}
    \item 第一项
    \item 第二项
\end{itemize}

有序列表:
\begin{enumerate}
    \item 第一步
    \item 第二步
\end{enumerate}

描述列表:
\begin{description}
    \item[CPU] Central Processing Unit
    \item[GPU] Graphics Processing Unit
\end{description}
```

---

## 四、数学公式

### 4.1 行内与行间公式

```latex
行内公式: $E = mc^2$

行间公式: 
$$E = mc^2$$

编号公式:
\begin{equation}
    E = mc^2
    \label{eq:energy}
\end{equation}
引用: 如公式~\ref{eq:energy} 所示
```

### 4.2 常用数学符号

| 符号        | LaTeX     | 符号         | LaTeX      |
| --------- | --------- | ---------- | ---------- |
| $\alpha$  | `\alpha`  | $\beta$    | `\beta`    |
| $\gamma$  | `\gamma`  | $\theta$   | `\theta`   |
| $\lambda$ | `\lambda` | $\mu$      | `\mu`      |
| $\sigma$  | `\sigma`  | $\omega$   | `\omega`   |
| $\sum$    | `\sum`    | $\prod$    | `\prod`    |
| $\int$    | `\int`    | $\partial$ | `\partial` |
| $\infty$  | `\infty`  | $\nabla$   | `\nabla`   |

### 4.3 矩阵与方程组

```latex
矩阵:
\[
\begin{bmatrix}
    a_{11} & a_{12} & \cdots & a_{1n} \\
    a_{21} & a_{22} & \cdots & a_{2n} \\
    \vdots & \vdots & \ddots & \vdots \\
    a_{m1} & a_{m2} & \cdots & a_{mn}
\end{bmatrix}
\]

方程组 (align 环境):
\begin{align}
    x + y &= 10 \label{eq:1} \\
    2x - y &= 5 \label{eq:2}
\end{align}
```

### 4.4 数学函数与运算符

```latex
\lim_{x \to 0} \frac{\sin x}{x} = 1

\sum_{i=1}^{n} i = \frac{n(n+1)}{2}

\int_{0}^{\infty} e^{-x^2} dx = \frac{\sqrt{\pi}}{2}

\frac{\partial^2 f}{\partial x^2} + \frac{\partial^2 f}{\partial y^2} = 0
```

---

## 五、表格

```latex
\begin{table}[h]
    \centering
    \caption{性能对比}
    \label{tab:comparison}
    \begin{tabular}{|c|c|c|c|}
        \hline
        算法 & 准确率 & 召回率 & F1分数 \\
        \hline
        CNN & 95.2\% & 94.8\% & 95.0\% \\
        RNN & 92.1\% & 91.5\% & 91.8\% \\
        Transformer & 96.8\% & 96.3\% & 96.5\% \\
        \hline
    \end{tabular}
\end{table}

多行/多列表格:
\usepackage{multirow}
\begin{tabular}{|c|c|}
    \hline
    \multirow{2}{*}{合并行} & 单元格1 \\
    \cline{2-2}
                           & 单元格2 \\
    \hline
    \multicolumn{2}{|c|}{合并列} \\
    \hline
\end{tabular}
```

---

## 六、插图

```latex
\usepackage{graphicx}

\begin{figure}[h]
    \centering
    \includegraphics[width=0.8\textwidth]{images/architecture.png}
    \caption{系统架构图}
    \label{fig:architecture}
\end{figure}

引用: 如图~\ref{fig:architecture} 所示
```

---

## 七、参考文献

### 7.1 BibTeX

```latex
% 文件: references.bib
@article{goodfellow2014generative,
    title={Generative Adversarial Nets},
    author={Goodfellow, Ian and Pouget-Abadie, Jean and Mirza, Mehdi and others},
    journal={Advances in Neural Information Processing Systems},
    volume={27},
    year={2014}
}

@inproceedings{vaswani2017attention,
    title={Attention Is All You Need},
    author={Vaswani, Ashish and Shazeer, Noam and Parmar, Niki and others},
    booktitle={Advances in Neural Information Processing Systems},
    year={2017}
}

@book{knuth1997art,
    title={The Art of Computer Programming},
    author={Knuth, Donald E.},
    volume={1},
    year={1997},
    publisher={Addison-Wesley}
}
```

```latex
% 文档中引用
引用: \cite{goodfellow2014generative}
无括号引用: \citet{vaswani2017attention}

\bibliographystyle{plain}  % 可选: ieeetr, acm, alpha, unsrt
\bibliography{references}
```

### 7.2 引用样式

| 样式 | 格式 | 适用 |
|------|------|------|
| plain | [1], [2] | 通用 |
| ieeetr | [1], [2] | IEEE 期刊 |
| acm | [1], [2], 作者缩写 | ACM 会议 |
| alpha | [Knu97] | 字母标签 |
| apalike | (Knuth, 1997) | APA 格式 |

---

## 八、常用宏包

| 包名 | 功能 | 示例 |
|------|------|------|
| amsmath | 数学公式增强 | `\text`, `\boxed`, `\xrightarrow` |
| amssymb | 更多数学符号 | `\blacksquare`, `\therefore` |
| geometry | 页面设置 | `\geometry{left=3cm}` |
| hyperref | 超链接和书签 | `\href{url}{text}` |
| listings | 代码高亮 | `\begin{lstlisting}` |
| tikz | 矢量图绘制 | `\draw (0,0) -- (1,1)` |
| graphicx | 插图 | `\includegraphics` |
| caption | 图表标题定制 | `\captionsetup{font=small}` |
| fancyhdr | 页眉页脚 | `\fancyhead[L]{Section}` |
| algorithm | 算法伪代码 | `\begin{algorithm}` |

---

## 九、编译流程

```
LaTeX 编译工作流:

pdflatex (-> DVI 或直接 PDF)
  适用于: 英文文档
  特点: 编译快，不支持中文

xelatex (-> PDF)
  适用于: 中文文档
  特点: 原生支持 Unicode，直接使用系统字体

lualatex (-> PDF)
  适用于: 复杂排版
  特点: 支持 Lua 脚本，Unicode 支持

BibTeX 编译顺序:
  pdflatex → bibtex → pdflatex → pdflatex
  (需要多次编译以解析交叉引用)
```

---

## 十、Beamer 幻灯片

```latex
\documentclass{beamer}
\usetheme{Madrid}
\usecolortheme{default}

\title{LaTeX 幻灯片制作}
\author{作者}
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

\begin{frame}{公式展示}
    $$E = mc^2$$
    \begin{block}{备注}
        这是爱因斯坦的质能方程
    \end{block}
\end{frame}

\end{document}
```

---

## 十一、Overleaf

Overleaf 是最流行的在线 LaTeX 编辑器：

- 无需安装，浏览器即可使用
- 实时协作编辑
- 数百个模板（论文、CV、报告）
- 与 Git 集成
- 自动编译

---

## 十二、常见错误调试

| 错误 | 原因 | 解决方法 |
|------|------|----------|
| `Undefined control sequence` | 命令拼写错误或未导入宏包 | 检查拼写，`\usepackage` 相关包 |
| `Missing $ inserted` | 数学模式外使用数学命令 | 添加 `$` 或使用 `\(...\)` |
| `File not found` | 引用了不存在的文件 | 检查文件路径和文件名 |
| `Overfull \hbox` | 内容超出页面宽度 | 使用 `\sloppy` 或手动换行 |
| `Citation undefined` | 未找到引用 | 确保运行 BibTeX，检查引用 key |

---

## 相关条目

- [[05_ComputerScience/DigitalNotes/Markdown/Markdown|Markdown]]
- [[13_Others/AcademicWriting/AcademicWriting|AcademicWriting]]
- [[05_ComputerScience/ProfessionalEnglish/ProfessionalEnglish|ProfessionalEnglish]]
- Typesetting

## 参考资源

- LaTeX 官方文档: https://www.latex-project.org
- Overleaf 文档: https://www.overleaf.com/learn
- 《LaTeX 入门》— 刘海洋
- 《The LaTeX Companion》— Mittelbach 等
- BibTeX 样式指南: https://www.bibtex.com
- CTAN (宏包仓库): https://ctan.org


