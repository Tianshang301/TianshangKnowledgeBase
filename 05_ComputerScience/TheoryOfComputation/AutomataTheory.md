---
aliases: [AutomataTheory]
tags: ['TheoryOfComputation', 'AutomataTheory']
---

# 自动机理论

## 一、形式语言基础

形式语言理论是自动机理论的语言学基础。字母表 $\Sigma$ 是非空有限符号集合，$\Sigma^*$ 表示所有有限字符串的集合（含空串 $\epsilon$）。语言 $L$ 定义为 $\Sigma^*$ 的子集。

### 1.1 文法

文法 $G = (V, T, P, S)$ 由非终结符集合 $V$、终结符集合 $T$、产生式集合 $P$ 和起始符号 $S \in V$ 组成。文法通过推导（derivation）生成语言中的字符串：$S \Rightarrow^* w$ 当且仅当 $w \in L(G)$。

### 1.2 语言的运算

语言的三种基本运算——并、连接和Kleene星号——定义了正则语言的递归结构。此外，交、补、差、反转等运算扩展了语言操作能力。

## 二、自动机层次结构

自动机理论是理论计算机科学的基础分支，研究抽象计算模型及其识别语言的能力。自动机按照计算能力形成Chomsky层次结构：有限自动机（正则语言）< 下推自动机（上下文无关语言）< 线性有界自动机（上下文有关语言）< 图灵机（递归可枚举语言）。

每种自动机对应一个语言类和一个文法类型，整体构成对计算能力的完整刻画。

## 二、有限自动机

### 2.1 确定型有限自动机（DFA）

确定型有限自动机是一个五元组 $M = (Q, \Sigma, \delta, q_0, F)$，其中：
- $Q$ 为有限状态集合
- $\Sigma$ 为有限输入字母表
- $\delta: Q \times \Sigma \rightarrow Q$ 为转移函数
- $q_0 \in Q$ 为初始状态
- $F \subseteq Q$ 为接受状态集合

DFA接受的语言 $L(M) = \{w \in \Sigma^* \mid \hat{\delta}(q_0, w) \in F\}$，其中 $\hat{\delta}$ 为扩展转移函数。

### 2.2 非确定型有限自动机（NFA）

NFA允许从一个状态通过同一输入到达多个状态，或通过 $\epsilon$（空串）转移。NFA的五元组定义中转移函数为 $\delta: Q \times (\Sigma \cup \{\epsilon\}) \rightarrow \mathcal{P}(Q)$。

**子集构造法**：每个NFA可转换为等价的DFA。设NFA $N = (Q_N, \Sigma, \delta_N, q_0, F_N)$，则等价DFA $D = (Q_D, \Sigma, \delta_D, \{q_0\}, F_D)$，其中 $Q_D = \mathcal{P}(Q_N)$，$F_D = \{S \subseteq Q_N \mid S \cap F_N \neq \emptyset\}$。子集构造法在最坏情况下导致 $2^{|Q_N|}$ 个状态。

### 2.3 NFA与DFA的等价性

尽管NFA在描述上更简洁、更直观，但其计算能力与DFA严格等价。关键定理：对于任意NFA $N$，存在DFA $D$ 使得 $L(N) = L(D)$。转换通过子集构造法实现，在最坏情况下等价DFA的状态数可能达到 $2^{|Q_N|}$ 的指数级别。但在实践中，许多NFA的等价DFA状态数远小于理论最坏情况。

### 2.4 $\epsilon$-NFA

$\epsilon$-NFA允许 $\epsilon$ 转移，进一步简化了某些语言的自动机表示。每个 $\epsilon$-NFA可通过消除 $\epsilon$ 转移转换为普通NFA。$\epsilon$-闭包（$\epsilon$-closure）定义为从某个状态出发通过 $\epsilon$ 转移能到达的所有状态的集合。

### 2.5 DFA的封闭性构造

DFA支持多种构造性运算。给定两个DFA $M_1, M_2$，可构造：
- **积自动机**：$Q = Q_1 \times Q_2$，$\delta((q_1,q_2),a) = (\delta_1(q_1,a), \delta_2(q_2,a))$，用于实现交运算和并运算
- **补自动机**：交换接受状态与非接受状态
- **反转自动机**：反转所有转移方向并将初始状态与接受状态互换

### 2.6 DFA最小化

每个正则语言存在唯一的状态数最少的DFA（除同构外）。最小化算法基于等价关系：两个状态 $p, q$ 等价当且仅当对所有输入串 $w$，$\hat{\delta}(p, w) \in F \iff \hat{\delta}(q, w) \in F$。Myhill-Nerode定理提供了最小化DFA的代数理论基础。

## 三、正则语言

### 3.1 正则表达式

正则表达式（Regular Expression）递归定义：
1. $\emptyset$、$\epsilon$、$\forall a \in \Sigma$ 为正则表达式
2. 若 $R_1, R_2$ 为正则表达式，则 $R_1 + R_2$（并）、$R_1R_2$（连接）、$R_1^*$（Kleene星号）为正则表达式

正则表达式与有限自动机等价。Thompson构造法将正则表达式转换为NFA，子集构造法将NFA转换为DFA，DFA可转换为正则表达式（Kleene算法或状态消除法）。

### 3.2 正则语言的判定算法

对于给定的正则语言（以DFA形式），以下问题均可有效判定：
- **空性判定**：是否存在DFA接受的字符串？等价于检查是否存在从初始状态到接受状态的路径
- **成员性判定**：给定字符串 $w$，是否属于语言？在DFA上模拟运行即可，时间复杂度 $O(|w|)$
- **等价性判定**：两个DFA是否接受相同语言？可通过最小化DFA后比较同构性进行判定

### 3.3 正则语言的泵引理

$$\forall L \text{ 正则}, \exists p > 0 \text{ 使得 } \forall w \in L, |w| \ge p: w = xyz, |xy| \le p, |y| \ge 1, \forall i \ge 0, xy^iz \in L$$

即任何足够长的正则语言字符串中，存在一个可重复抽取的子串。

### 3.4 封闭性

正则语言在以下运算下封闭：并、交、补、差、连接、Kleene星号、反转、同态、逆同态、商运算。正则语言的封闭性在程序分析和验证中有重要应用，如类型检查系统中的正则表达式匹配。

### 3.5 Myhill-Nerode定理

Myhill-Nerode定理提供了正则语言的代数刻画：语言 $L$ 是正则的当且仅当在字符串集上定义的双射等价关系 $\equiv_L$（$x \equiv_L y$ 当且仅当 $\forall z, xz \in L \iff yz \in L$）具有有限个等价类。等价类的数量恰好等于最小DFA的状态数。该定理也从理论上证明了DFA最小化算法的正确性。

## 四、下推自动机

### 4.1 下推自动机（PDA）

下推自动机在有限自动机的基础上增加了一个栈（stack），提供无限容量的后进先出存储器。PDA的形式定义：

$$M = (Q, \Sigma, \Gamma, \delta, q_0, Z_0, F)$$

其中 $\Gamma$ 为栈字母表，$Z_0 \in \Gamma$ 为初始栈顶符号，转移函数 $\delta: Q \times (\Sigma \cup \{\epsilon\}) \times \Gamma \rightarrow \mathcal{P}(Q \times \Gamma^*)$。

PDA的计算由瞬时描述（ID）三元组 $(q, w, \gamma)$ 描述，其中 $q$ 为当前状态，$w$ 为剩余输入，$\gamma$ 为栈内容。转移关系 $(q, aw, X\gamma) \vdash (p, w, \beta\gamma)$ 表示在状态 $q$ 读入 $a$、栈顶为 $X$ 时转移到状态 $p$，并以 $\beta$ 替换栈顶。

### 4.2 确定型PDA与歧义性

如果上下文无关文法是无歧义的（每个字符串有唯一的派生树），该语言可由DPDA识别。但有些CFL本质上是歧义的（inherently ambiguous），即任何生成该语言的CFG都是歧义的。例如 $\{a^ib^jc^k \mid i = j \text{ 或 } j = k\}$ 是本质歧义语言。

确定型下推自动机（DPDA）在每个配置下至多有一个合法转移。非确定型下推自动机（NPDA）的计算能力严格强于DPDA。存在上下文无关语言（如回文语言 $\{ww^R\}$）需用NPDA识别。

### 4.3 DPDA与NPDA

PDA可通过两种方式接受语言：
- **终态接受**：$L(M) = \{w \mid (q_0, w, Z_0) \vdash^* (q, \epsilon, \gamma), q \in F\}$
- **空栈接受**：$L(M) = \{w \mid (q_0, w, Z_0) \vdash^* (q, \epsilon, \epsilon)\}$

两种接受方式等价，可相互转换。

### 4.5 PDA接受方式

上下文无关文法（CFG）与NPDA等价。给定CFG $G = (V, T, P, S)$，可构造NPDA $M$ 使得 $L(M) = L(G)$，构造方法利用NPDA模拟CFG的最左推导。反之，给定NPDA可构造等价的CFG，构造方法将ID对 $(p, X, q)$ 转化为语法变量，模拟栈内容的变化。

## 五、上下文无关文法

### 5.1 乔姆斯基范式（CNF）

任何不生成空串的CFG可转化为CNF：所有产生式形如 $A \rightarrow BC$ 或 $A \rightarrow a$，其中 $A,B,C \in V$，$a \in T$。转化步骤包括：消除 $\epsilon$-产生式、消除单元产生式、消除无用符号、将长产生式转化为二元产生式。

### 5.2 Greibach范式（GNF）

Greibach范式中所有产生式形如 $A \rightarrow a\alpha$，其中 $a \in T$，$\alpha \in V^*$。GNF中的每个推导步骤恰好生成一个终结符，使得推导长度与字符串长度成正比。GNF在构造自顶向下语法分析器时特别有用。

### 5.3 上下文无关语言的判定算法

- **CYK算法**：基于动态规划的成员性判定算法，时间复杂度 $O(n^3)$
- **Earley算法**：适用于任意CFG的成员性判定，时间复杂度 $O(n^3)$，但对某些文法可达到 $O(n^2)$ 或 $O(n)$
- **LL和LR语法分析**：LL($k$)文法可使用自顶向下分析，LR($k$)文法则使用自底向上分析，后者能处理更广泛的文法类

### 5.4 CYK算法

CYK（Cocke-Younger-Kasami）算法用于判断文法是否生成给定字符串，时间复杂度为 $O(n^3)$。算法基于动态规划，要求文法处于CNF。

### 5.5 上下文无关语言的封闭性

上下文无关语言在下列运算下封闭：并、连接、Kleene星号、反转、同态。但在交和补运算下不封闭。上下文无关语言与正则语言的交保持上下文无关性质，这一性质在程序语言分析和编译优化中具有实用价值。

### 5.6 上下文无关语言的泵引理

CFL泵引理：若 $L$ 为CFL，则存在 $p > 0$，使得 $\forall w \in L, |w| \ge p$，可将 $w$ 写为 $w = uvxyz$，满足：
- $|vxy| \le p$
- $|vy| \ge 1$
- $\forall i \ge 0, uv^ixy^iz \in L$

## 六、图灵机

### 6.1 基本图灵机

图灵机是计算能力的最高形式化模型。确定型图灵机形式定义：

$$M = (Q, \Sigma, \Gamma, \delta, q_0, B, F)$$

其中 $\Gamma$ 为带字母表（$\Sigma \subset \Gamma$），$B \in \Gamma \setminus \Sigma$ 为空格（blank），$\delta: Q \times \Gamma \rightarrow Q \times \Gamma \times \{L, R\}$ 为部分函数，$L/R$ 表示读写头向左/右移动一格。

### 6.2 图灵机作为语言接受器

图灵机接受的语言分为三类：
- **递归语言**（可判定）：存在图灵机对所有输入停机并正确接受/拒绝
- **递归可枚举语言**（半可判定）：存在图灵机接受该语言中的字符串，但对不在语言中的字符串可能不停机
- **非递归可枚举语言**：没有任何图灵机能够接受

### 6.3 图灵机变种

- **多带图灵机**：具有 $k$ 条带，每条带独立读写，计算能力与单带图灵机等价
- **非确定型图灵机**：转移函数为 $\delta: Q \times \Gamma \rightarrow \mathcal{P}(Q \times \Gamma \times \{L, R\})$
- **通用图灵机（UTM）**：能模拟任何图灵机的图灵机，为存储程序计算奠定了基础
- **带预言机的图灵机**：具有访问外部预言（oracle）的能力，用于研究相对化计算和多项式谱系

### 6.4 图灵机的变种等价性

所有"合理的"计算模型修改（多带、多维带、多头、非确定型）均与基本图灵机等价（Church-Turing论题）。这意味着图灵机捕获了"可有效计算"的直观概念。

## 七、Chomsky层次结构

**表1：Chomsky层次结构**

| 类型 | 文法 | 自动机 | 语言类 | 产生式限制 |
|------|------|--------|--------|------------|
| 0 | 无限制文法 | 图灵机 | 递归可枚举 | $\alpha \rightarrow \beta$，无限制 |
| 1 | 上下文有关文法 | 线性有界自动机 | 上下文有关 | $\alpha A \beta \rightarrow \alpha \gamma \beta$，$\gamma \neq \epsilon$ |
| 2 | 上下文无关文法 | 下推自动机 | 上下文无关 | $A \rightarrow \gamma$ |
| 3 | 正则文法 | 有限自动机 | 正则 | $A \rightarrow aB$ 或 $A \rightarrow a$ |

## 八、可判定性与半可判定性

语言 $L$ 是可判定的（递归的）当且仅当存在图灵机对所有输入停机并正确判定。语言 $L$ 是半可判定的（递归可枚举的）当且仅当存在图灵机接受 $L$ 中的字符串，但对不在 $L$ 中的字符串可能不停机。

著名的不可判定问题包括：停机问题（Halting Problem）、Post对应问题（Post Correspondence Problem）、希尔伯特第十问题（Hilbert's Tenth Problem）和矩阵死亡率问题（Matrix Mortality Problem）。

停机问题的不可判定性通过对角化证明：假设存在图灵机 $H$ 能判定任意图灵机 $M$ 在输入 $w$ 上是否停机，则可构造图灵机 $D$，以描述 $M$ 的编码 $\langle M \rangle$ 为输入，调用 $H$ 判定若 $M$ 在 $\langle M \rangle$ 上停机则进入死循环，反之则停机，从而导出矛盾。

**Rice定理**：任何关于图灵机所识别语言的非平凡性质都是不可判定的。这意味着程序功能性质的自动化分析在理论上存在根本限制。

**表2：重要不可判定问题示例**

| 问题 | 输入 | 不可判定性质 |
|------|------|-------------|
| 停机问题 | 图灵机$M$和输入$w$ | $M$是否在$w$上停机 |
| 空性判定 | 图灵机$M$ | $L(M) = \emptyset$ |
| 等价性判定 | 图灵机$M_1, M_2$ | $L(M_1) = L(M_2)$ |
| Post对应问题 | 字符串对集合 | 是否存在匹配序列 |
| 希尔伯特第十问题 | 多项式方程 | 是否存在整数解 |

## 相关条目

- [[ComputationalComplexity]]
- [[05_ComputerScience/CompilerPrinciples/INDEX|CompilerPrinciples]]
- FormalLanguages
- [[05_ComputerScience/TheoryOfComputation/INDEX|TheoryOfComputation]]

## 参考资源

1. Hopcroft J E, Motwani R, Ullman J D. Introduction to Automata Theory, Languages, and Computation. 3rd ed. Addison-Wesley, 2007.
2. Sipser M. Introduction to the Theory of Computation. 3rd ed. Cengage Learning, 2013.
3. Kozen D C. Automata and Computability. Springer, 1997.
4. 陈卫东. 自动机理论、语言和计算导论. 机械工业出版社, 2014.
5. 张立昂. 计算理论导引. 高等教育出版社, 2016.
