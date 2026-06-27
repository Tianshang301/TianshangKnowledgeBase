---
aliases: [ComputationalComplexity]
tags: ['TheoryOfComputation', 'ComputationalComplexity']
created: 2026-05-16
updated: 2026-05-16
---

# 计算复杂性理论

## 一、计算问题与模型

### 1.1 判定问题与语言

计算复杂性理论通常将计算问题形式化为判定问题（Decision Problem）：给定输入 $x$，判断其是否满足性质 $P$。判定问题可等价地转换为语言识别问题：$L = \{x \mid P(x) \text{ 为真}\}$。

函数问题（Function Problem）要求计算输出（如"求最大团"），可通过调用判定问题解决。优化问题寻找最优解，是函数问题的特例。

### 1.2 计算模型

通用计算模型为图灵机。非确定型图灵机在每一步可有多个合法选择，其接受定义为存在一个接受的计算分支。多项式时间归约和类定义均基于图灵机模型的合理变种。

## 二、时间复杂性

### 2.1 基本定义

计算复杂性理论研究求解计算问题所需资源（时间、空间）的界限。设 $M$ 为在所有输入上停机的确定型图灵机，$M$ 的时间复杂度 $t(n)$ 定义为对所有长度为 $n$ 的输入，$M$ 的最大运行步数。

复杂性类的定义通常使用大 O 记号，忽略常数因子和低阶项。时间可构造函数（Time-Constructible Function）确保图灵机能在 $O(T(n))$ 步内计算 $T(n)$，是分层定理的基础。

### 2.2 主要时间复杂性类

**表1：时间复杂性类**

| 类 | 定义 | 典型问题 |
|----|------|----------|
| P | $\bigcup_{k \ge 0} \text{TIME}(n^k)$ | 最短路径、线性规划、上下文无关文法分析 |
| NP | $\bigcup_{k \ge 0} \text{NTIME}(n^k)$ | SAT、团问题、旅行商问题 |
| EXP | $\bigcup_{k \ge 0} \text{TIME}(2^{n^k})$ | 广义围棋、Presburger 算术 |
| NEXP | $\bigcup_{k \ge 0} \text{NTIME}(2^{n^k})$ | 片段句法一致性 |

**类间关系**：$P \subseteq NP \subseteq EXP \subseteq NEXP$。时间分层定理保证 $P \subsetneq EXP$ 和 $NP \subsetneq NEXP$ 为严格包含关系。P 是否等于 NP 是计算机科学中最重要的未解决问题。

时间分层定理和空间分层定理是复杂性理论中的基本工具，它们通过对角化方法证明更多资源能解决更广泛的问题类。这些定理保证了复杂性类的层次结构不会坍塌在低层。

## 三、NP 完全性

### 3.1 Cook-Levin 定理

Cook-Levin 定理是 NP 完全性理论的奠基性结果：布尔可满足性问题（SAT）是 NP 完全的。证明思路是对任意 NP 图灵机 $M$ 和输入 $w$，构造一个布尔公式 $\phi_{M,w}$，使得 $\phi_{M,w}$ 可满足当且仅当 $M$ 接受 $w$。

### 3.2 归约类型

归约（Reduction）是建立问题间复杂关系的基本工具。

- **Karp 归约**（多项式时间多一归约）：函数 $f: \Sigma^* \rightarrow \Sigma^*$ 满足 $w \in L \iff f(w) \in L'$，$f$ 可在多项式时间内计算
- **Cook 归约**（多项式时间图灵归约）：利用预言机求解问题的归约方式

Karp 归约是 NP 完全性定义的常用归约，Cook 归约更通用但用于更广泛的复杂性分析。两种归约在 NP 完全性上下文中等价：若一个问题关于 Karp 归约是 NP 完全的，则关于 Cook 归约也是 NP 完全的。

### 3.3 NP 难问题

NP 难（NP-hard）问题定义为所有 NP 问题可通过多项式时间归约到的问题。NP 完全问题是 NP 难与 NP 的交集。非 NP 的 NP 难问题包括：停机问题（不可判定）、最优电路设计（$\Sigma_2^P$-hard）和最小电路规模问题（MCSP）。

### 3.4 经典 NP 完全问题

以下21个问题（Karp 的21个 NP 完全问题）已被证明为 NP 完全：

**表3：代表性 NP 完全问题**

| 问题 | 输入 | 判断 |
|------|------|------|
| 3SAT | 3合取范式布尔公式 | 是否存在可满足赋值 |
| 团（Clique） | 图$G$，整数$k$ | 是否存在$k$个顶点的团 |
| 顶点覆盖（Vertex Cover） | 图$G$，整数$k$ | 是否存在$k$个顶点的顶点覆盖 |
| 哈密顿路径（Hamiltonian Path） | 图$G$ | 是否存在经过所有顶点的路径 |
| 子集和（Subset Sum） | 整数集合$S$，目标$t$ | 是否存在子集和为$t$ |
| 背包（Knapsack） | 物品集合（重量、价值），容量$C$ | 总价值能否至少为$V$且不超重 |

### 3.5 结构型 NP 完全问题

除 SAT 类问题外，图论中的 NP 完全问题构成了重要的子类。顶点覆盖、团和独立集之间存在直接的归约关系：给定图 $G = (V,E)$，顶点覆盖 $C$ 的补集 $V \setminus C$ 即为独立集，而独立集与团之间通过补图对应。这一关系链展示了不同结构问题之间的深层联系。

### 3.6 归约链

NP 完全性的证明通常通过归约链：SAT $\leq_p$ 3SAT $\leq_p$ 团 $\leq_p$ 顶点覆盖 $\leq_p$ 哈密顿路径 $\leq_p$ 旅行商问题。这些归约保持了问题的计算难度，提供了问题间难度关系的系统理解。

## 三、空间复杂性

### 3.1 基本定义

空间复杂度 $s(n)$ 定义为图灵机在处理长度为 $n$ 的输入时使用的最大工作带格子数。输入带不计入空间消耗。

### 3.2 空间复杂性类

- **L**（对数空间）：$\text{SPACE}(\log n)$
- **NL**（非确定型对数空间）：$\text{NSPACE}(\log n)$，典型问题为有向图可达性（STCON）
- **PSPACE**：$\bigcup_{k \ge 0} \text{SPACE}(n^k)$，典型问题为量词布尔公式（QBF）
- **NPSPACE**：$\bigcup_{k \ge 0} \text{NSPACE}(n^k)$

### 3.3 Savitch 定理

Savitch 定理建立了确定型与非确定型空间复杂性的关系：

$$\text{NSPACE}(f(n)) \subseteq \text{SPACE}(f(n)^2)$$

其中 $f(n) \ge \log n$ 为空间可构造函数。该定理表明 $\text{NPSPACE} = \text{PSPACE}$，即非确定多项式空间并不比确定型更强。

### 3.4 空间与时间的关系

空间与时间的包含关系：$L \subseteq NL \subseteq P \subseteq NP \subseteq PSPACE \subseteq EXP$。其中 $L \neq PSPACE$ 由空间分层定理保证。

## 四、多项式谱系

多项式谱系（Polynomial Hierarchy, PH）扩展了 P 和 NP 的概念，将交替量词引入复杂性分类。定义如下：

- $\Sigma_0^P = \Pi_0^P = P$
- $\Sigma_{k+1}^P = NP^{\Sigma_k^P}$（带$\Sigma_k^P$预言机的 NP）
- $\Pi_{k+1}^P = coNP^{\Sigma_k^P}$

量词角度刻画：$\Sigma_k^P$ 中的问题可表示为 $\exists x_1 \forall x_2 \exists x_3 \cdots Q_k x_k : \phi(x_1,\ldots,x_k)$，其中 $Q_k$ 为 $\exists$（$k$为奇数）或 $\forall$（$k$为偶数）。$\Pi_k^P$ 则从 $\forall$ 量词开始。

多项式谱系中的每一层包含上一层：$\Sigma_k^P \cup \Pi_k^P \subseteq \Sigma_{k+1}^P \cap \Pi_{k+1}^P$。若 PH 在某层坍塌，即 $\Sigma_k^P = \Sigma_{k+1}^P$，则 PH 坍塌至第$k$层。一般认为 PH 不会坍塌。

**表4：多项式谱系中的典型问题**

| 层次 | 问题 | 描述 |
|------|------|------|
| $\Sigma_1^P$ = NP | SAT | 布尔公式是否存在满足赋值 |
| $\Pi_1^P$ = coNP | TAUTOLOGY | 布尔公式是否永真 |
| $\Sigma_2^P$ | 极小不可满足 | 公式不可满足但删除任一子句后可满足 |
| $\Pi_2^P$ | 极小等价 | 两个公式是否在所有更短公式中等价 |
| $\Sigma_3^P$ | 3级 QBF | $\exists x \forall y \exists z : \phi(x,y,z)$ |

## 五、交互式证明与 PCP

### 5.1 交互式证明系统（IP）

交互式证明系统由证明者（Prover）和验证者（Verifier）组成，验证者使用随机化策略在多项式轮交互中验证命题的真假。Arthur-Merlin 协议是交互式证明的标准形式化。

重要结果：
- $IP = PSPACE$：交互式证明的能力等价于多项式空间
- $MIP = NEXP$：多证明者交互式证明等价于非确定型指数时间
- $AM = NP$：常数轮交互式证明等价于 NP（在某些硬度假设下）

### 5.2 PCP 定理

PCP 定理（概率可检验证明定理）是1990年代计算复杂性理论最深刻的成果之一：

$$NP = PCP[O(\log n), O(1)]$$

这意味着 NP 中的每个问题都有一组证明，验证者仅需读取常数个比特并以高概率验证正确性。PCP 定理的直接推论是许多优化问题的不可近似性，如最大团问题和最小着色问题。

### 5.3 IP 中的零知识证明

零知识证明允许证明者向验证者证明命题的真实性而不泄露任何额外的知识。零知识证明在密码学中具有广泛应用，包括身份认证、电子投票和区块链隐私保护。

## 六、随机化复杂性

随机化算法使用随机位做出决策，允许一定的错误概率。

**表5：随机化复杂性类**

| 类 | 错误类型 | 错误概率 | 典型算法 |
|----|----------|----------|----------|
| RP | 单侧（不接受假阳性） | $< 1/2$ | 素数检测（Miller-Rabin） |
| co-RP | 单侧（不接受假阴性） | $< 1/2$ | 矩阵乘法验证 |
| BPP | 双侧 | $< 1/3$ | 多项式等价性检验 |
| ZPP | 无差错（期望多项式时间） | 0 | 素数检测（AKS 前） |

随机化类间关系：$RP \subseteq BPP$，$ZPP = RP \cap co-RP$。广泛认为 $P = BPP$（基于伪随机生成器存在性的假设）。

### 6.1 去随机化

去随机化（Derandomization）研究了在何种条件下随机化算法可以被确定性算法有效模拟。伪随机生成器（PRG）是去随机化的核心工具：如果存在足够强的 PRG，则 $P = BPP$。目前已知在电路复杂度假设下，$BPP$ 包含在 $P$ 的子指数时间变体中。

硬性假设（如存在指数级电路下界）可推导出去随机化结论，这一方向连接了电路复杂性和随机化复杂性。

## 七、可近似性

当优化问题为 NP 难时，研究其近似解的质量具有重要意义。

- **APX**：存在常数因子近似算法的优化问题
- **PTAS**（多项式时间近似方案）：对任意 $\epsilon > 0$，存在 $(1+\epsilon)$ 近似算法
- **FPTAS**（完全多项式时间近似方案）：运行时间为 $\text{poly}(n, 1/\epsilon)$ 的 PTAS

**表6：近似复杂性层次**

| 类 | 含义 | 典型问题 |
|----|------|----------|
| FPTAS | 完全多项式时间近似方案 | 背包问题 |
| PTAS | 多项式时间近似方案 | 欧几里得旅行商问题 |
| APX | 常数因子可近似 | 顶点覆盖（2-近似），最大割 |
| log-APX | 对数因子可近似 | 集合覆盖（$O(\log n)$-近似） |
| poly-APX | 多项式因子可近似 | 最大团（$O(n/\log^2 n)$-近似） |
| NPO-complete | 不可近似（除非 P=NP） | 旅行商问题（一般情形） |

PCP 定理给出的不可近似性结果：最大团问题不可近似到 $n^{1-\epsilon}$，最小着色问题不可近似到 $n^{1-\epsilon}$，MAX-3SAT 存在常数不可近性阈值。

## 八、电路复杂性

布尔电路由与门、或门、非门构成，电路族 $\{C_n\}$ 计算语言。

- **P/poly**：存在多项式规模电路族的语言类，包含所有 P，且包含某些不可判定问题
- **NC**：由对数深度、多项式规模电路族可计算的语言类
- **AC**：与 NC 类似但允许门具有无界扇入

$NC \subseteq P \subseteq NP$。$P$是否包含在$NC$中（即计算能否被高度并行化）是重要未解决问题。

电路复杂性的下界结果是计算复杂性理论中最困难的领域之一。已知结果包括：奇偶函数（PARITY）不属于 $AC^0$（Håstad 定理），但尚无 $P \not\subset NC^1$ 或 $NP \not\subset P/poly$ 的非条件性证明。

Karp-Lipton 定理：若 $NP \subseteq P/poly$，则 $PH$ 坍塌至 $\Sigma_2^P$。该结果为 $NP$ 不存在多项式规模电路提供了间接证据。

## 九、量子复杂性

量子计算模型——量子图灵机/量子电路——对应复杂性类 **BQP**（有界错误量子多项式时间）。

量子算法的重要成就：Shor 算法在 BQP 中求解整数分解（打破 RSA），Grover 算法在 $O(\sqrt{N})$ 时间内搜索无序数据库。

关系：$P \subseteq BPP \subseteq BQP \subseteq PSPACE$。BQP 与 NP 的关系尚不清楚，但一般认为 NP 不完全包含在 BQP 中。

## 十、去随机化与硬度放大

去随机化研究连接了伪随机性和电路复杂度下界。硬度放大（Hardness Amplification）将弱下界转化为强下界：如果存在轻微困难（最坏情况困难）的函数，可构造极困难（平均情况困难）的函数。

平均情况复杂性在密码学中至关重要：单向函数的安全性依赖于某些问题在平均情况下的困难性。平均情况 NP 完全性的概念（distNP）为密码学安全提供了复杂性理论基础。

## 十一、开放问题

计算复杂性理论中最重要的未解决问题：

- **P vs NP**：是否存在 NP 完全问题的多项式时间算法？
- **P vs BPP**：随机化是否真正增强了计算能力？
- **NP vs co-NP**：NP 在补运算下是否封闭？
- **NC vs P**：计算能否被完全并行化？
- **单向函数存在性**：是否存在可有效计算但不可逆转的函数？

这些问题中的每一个都有深刻的理论意义和广泛的实际影响。

## 相关条目

- [[AutomataTheory]]
- [[05_ComputerScience/TheoryOfComputation/INDEX|TheoryOfComputation]]
- [[05_ComputerScience/DataStructuresAndAlgorithms/Algorithms/INDEX|Algorithms]]
- NPCompleteness

## 参考资源

1. Arora S, Barak B. Computational Complexity: A Modern Approach. Cambridge University Press, 2009.
2. Sipser M. Introduction to the Theory of Computation. 3rd ed. Cengage Learning, 2013.
3. Papadimitriou C H. Computational Complexity. Addison-Wesley, 1994.
4. Goldreich O. Computational Complexity: A Conceptual Perspective. Cambridge University Press, 2008.
5. 堵丁柱. 计算复杂性理论. 高等教育出版社, 2017.

