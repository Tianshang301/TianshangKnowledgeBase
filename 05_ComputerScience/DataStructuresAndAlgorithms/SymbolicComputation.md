---
aliases: [SymbolicComputation]
tags: ['05_ComputerScience', 'DataStructuresAndAlgorithms']
---

# 符号计算

符号计算（Symbolic Computation），又称计算机代数（Computer Algebra），是指用计算机对数学表达式进行精确符号操作的计算范式。与数值计算（Numerical Computation）的浮点近似不同，符号计算保持数学表达式的精确形式，例如将 √2 保留为符号而非输出 1.4142。典型计算机代数系统（CAS）包括 Mathematica、Maple、Maxima 和 SymPy（Python 符号计算库）。

核心操作包括 **多项式运算**（展开/因式分解/最大公因式/Gröbner 基）、**符号微分与积分**（自动求导导则/Risch 算法）、**方程求解**（多项式方程精确根/超越方程的解析解处理）以及表达式简化与模式匹配。符号计算在公式推导、定理证明、自动代码生成和物理建模中具有不可替代的作用，但其计算复杂度通常高于数值方法，在规模较大时可能面临表达式膨胀（Expression Swell）问题。数值计算侧重效率和近似精度，符号计算侧重精确性和推理完备性，二者在实践中常互补使用。

## 相关条目

- [[ComputerAlgebra]] 
- [[NumericalComputation]] 
- [[SymPy]] 
- [[Polynomial]] 
- [[AutomaticDifferentiation]]