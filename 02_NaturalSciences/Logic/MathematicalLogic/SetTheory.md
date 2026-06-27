---
aliases: [SetTheory]
tags: ['Logic', 'MathematicalLogic', 'SetTheory']
created: 2026-05-16
updated: 2026-05-13
---

# 集合论详解

## 一、集合基础

### 集合表示

- **列举法**：$A = \{1, 2, 3, 4\}$
- **描述法**：$B = \{x \in \mathbb{R} \mid x^2 < 2\}$
- **空集**：$\emptyset = \{\}$

### 集合运算

- **并集**：$A \cup B = \{x \mid x \in A \vee x \in B\}$
- **交集**：$A \cap B = \{x \mid x \in A \wedge x \in B\}$
- **补集**：$A^c = \{x \in U \mid x \notin A\}$（相对于全集 $U$）
- **差集**：$A \setminus B = \{x \mid x \in A \wedge x \notin B\}$
- **对称差**：$A \triangle B = (A \setminus B) \cup (B \setminus A)$
- **笛卡尔积**：$A \times B = \{(a,b) \mid a \in A, b \in B\}$
  $$|A \times B| = |A| \cdot |B|, \quad |A^n| = |A|^n$$

### 集合恒等式

- 交换律：$A \cup B = B \cup A$，$A \cap B = B \cap A$
- 结合律：$A \cup (B \cup C) = (A \cup B) \cup C$
- 分配律：$A \cup (B \cap C) = (A \cup B) \cap (A \cup C)$
- 德摩根律：$(A \cup B)^c = A^c \cap B^c$，$(A \cap B)^c = A^c \cup B^c$
- 吸收律：$A \cup (A \cap B) = A$，$A \cap (A \cup B) = A$

**广义德摩根律**：
$$\left(\bigcup_{i \in I} A_i\right)^c = \bigcap_{i \in I} A_i^c, \quad \left(\bigcap_{i \in I} A_i\right)^c = \bigcup_{i \in I} A_i^c$$

## 二、文氏图 (Venn Diagrams)

文氏图直观表示集合关系和运算。例如 $A \cup B$ 为两个圆覆盖的区域，$A \cap B$ 为重叠区域。

## 三、幂集与基数

### 幂集 (Power Set)

$$P(A) = \{X \mid X \subseteq A\}$$

若 $|A| = n$，则 $|P(A)| = 2^n$。

**幂集元素计数**：
$$\left|\{X \in P(A) \mid |X| = k\}\right| = \binom{n}{k}$$
$$\sum_{k=0}^n \binom{n}{k} = 2^n$$

**示例：** $A = \{1, 2\}$，则 $P(A) = \{\emptyset, \{1\}, \{2\}, \{1,2\}\}$

### 基数 (Cardinality)

- 有限集：$|A|$ 为元素个数
- 可数集：与 $\mathbb{N}$ 等势，如 $\mathbb{Z}$、$\mathbb{Q}$
- 不可数集：如 $\mathbb{R}$、$(0,1)$

**康托尔定理：** $|A| < |P(A)|$

### 可数集与不可数集

- $\mathbb{N}$ 可数，$\mathbb{Z}$ 可数，$\mathbb{Q}$ 可数
- $\mathbb{R}$ 不可数（康托尔对角线论证）
- $(0,1) \sim \mathbb{R}$（存在双射）

## 四、关系 (Relations)

### 二元关系

$R \subseteq A \times B$，若 $A = B$，称 $R$ 为 $A$ 上的关系。

### 关系性质

- **自反**：$\forall a \in A, aRa$
- **对称**：$\forall a,b \in A, aRb \implies bRa$
- **传递**：$\forall a,b,c \in A, aRb \wedge bRc \implies aRc$
- **反对称**：$\forall a,b \in A, aRb \wedge bRa \implies a = b$

### 等价关系

满足自反、对称、传递的关系称为等价关系。等价关系将集合划分为等价类（划分）。

$$\text{等价类}：[a] = \{x \in A \mid xRa\}$$

**划分与 Bell 数**：$n$ 元集合上的等价关系数等于划分方式数 $B_n$：
$$B_n = \sum_{k=1}^n S(n,k), \quad S(n,k) = kS(n-1,k) + S(n-1,k-1)$$
其中 $S(n,k)$ 为第二类 Stirling 数。

### 偏序关系

满足自反、反对称、传递的关系称为偏序，记作 $\leq$。

- **哈斯图 (Hasse Diagram)**：偏序集的简化图表示
- **最大/最小元**：关于偏序比较的最大/最小元素
- **上界/下界**：集合的上界和下界

## 五、函数 (Functions)

### 定义

$f: A \to B$ 为从 $A$ 到 $B$ 的函数，$\forall a \in A$ 有唯一的 $b \in B$ 使 $f(a) = b$。

### 函数类型

- **单射 (Injective)**：$f(a_1) = f(a_2) \implies a_1 = a_2$
- **满射 (Surjective)**：$\forall b \in B, \exists a \in A, f(a) = b$
- **双射 (Bijective)**：同时为单射和满射

### 函数复合

$$(f \circ g)(x) = f(g(x))$$

### 逆函数

双射 $f$ 的逆函数 $f^{-1}$ 满足：

$$f^{-1}(y) = x \iff f(x) = y$$

### 像与原像

- **像**：$f(A) = \{f(a) \mid a \in A\}$
- **原像**：$f^{-1}(B) = \{x \in X \mid f(x) \in B\}$

## 六、无限集

### 集合的势

- $|A| = |B|$：存在双射 $f: A \to B$
- $|A| \leq |B|$：存在单射 $f: A \to B$
- **康托尔-伯恩斯坦定理**：若 $|A| \leq |B|$ 且 $|B| \leq |A|$，则 $|A| = |B|$

### 基数算术

$$|A| + |B| = |A \times \{0\} \cup B \times \{1\}|, \quad |A| \cdot |B| = |A \times B|$$
$$|\mathbb{N}| = \aleph_0, \quad |\mathbb{R}| = \mathfrak{c} = 2^{\aleph_0}, \quad |\mathbb{R}^n| = \mathfrak{c}$$
$$\aleph_0 + \aleph_0 = \aleph_0, \quad \aleph_0 \cdot \aleph_0 = \aleph_0, \quad 2^{\aleph_0} > \aleph_0$$

### 连续统假设

不存在基数严格介于 $\aleph_0$（可数）和 $2^{\aleph_0}$（连续统）之间的集合。
