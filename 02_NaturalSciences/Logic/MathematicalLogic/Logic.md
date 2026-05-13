# 数理逻辑详解

## 一、命题逻辑 (Propositional Logic)

### 逻辑连接词

| 符号 | 名称 | 含义 | 真值条件 |
|------|------|------|---------|
| $\neg$ | 非 (NOT) | $\neg P$ | $P$ 为假时真 |
| $\wedge$ | 且 (AND) | $P \wedge Q$ | 两者皆真时真 |
| $\vee$ | 或 (OR) | $P \vee Q$ | 至少一个真时真 |
| $\to$ | 蕴含 (IF-THEN) | $P \to Q$ | $P$ 真 $Q$ 假时假 |
| $\leftrightarrow$ | 双蕴含 (IFF) | $P \leftrightarrow Q$ | 同真同假 |

### 真值表

以 $P \to Q$ 为例：

| $P$ | $Q$ | $\neg P$ | $P \wedge Q$ | $P \vee Q$ | $P \to Q$ | $P \leftrightarrow Q$ |
|-----|-----|----------|-------------|------------|-----------|----------------------|
| T | T | F | T | T | T | T |
| T | F | F | F | T | F | F |
| F | T | T | F | T | T | F |
| F | F | T | F | F | T | T |

### 永真式、矛盾式与可满足式

- **永真式 (Tautology)**：所有赋值下均为真
- **矛盾式 (Contradiction)**：所有赋值下均为假
- **可满足式 (Satisfiable)**：至少一个赋值下为真

### 逻辑等价

$P \equiv Q$ 如果 $P \leftrightarrow Q$ 为永真式。

**重要等价：**

- 双重否定：$\neg\neg P \equiv P$
- 德摩根律：$\neg(P \wedge Q) \equiv \neg P \vee \neg Q$，$\neg(P \vee Q) \equiv \neg P \wedge \neg Q$
- 交换律：$P \wedge Q \equiv Q \wedge P$，$P \vee Q \equiv Q \vee P$
- 结合律：$P \wedge (Q \wedge R) \equiv (P \wedge Q) \wedge R$
- 分配律：$P \wedge (Q \vee R) \equiv (P \wedge Q) \vee (P \wedge R)$
- 蕴含律：$P \to Q \equiv \neg P \vee Q$
- 假言易位：$P \to Q \equiv \neg Q \to \neg P$
- 双蕴含：$P \leftrightarrow Q \equiv (P \to Q) \wedge (Q \to P)$

### 范式

**CNF (合取范式)：** 子句的合取，如 $(P \vee Q) \wedge (\neg P \vee R)$

**DNF (析取范式)：** 子句的析取，如 $(P \wedge Q) \vee (\neg P \wedge R)$

### 功能完备集

一组连接词称为功能完备的，如果所有布尔函数均可仅用这些连接词表示。例如 $\{\neg, \wedge\}$、$\{\neg, \vee\}$、$\{\neg, \to\}$、$\{\text{NAND}\}$。

## 二、谓词逻辑 (Predicate Logic)

### 量词

- **全称量词 $\forall$**：$\forall x P(x)$ 表示"对所有 $x$，$P(x)$ 成立"
- **存在量词 $\exists$**：$\exists x P(x)$ 表示"存在 $x$ 使得 $P(x)$ 成立"

### 约束变量与自由变量

- $x$ 在 $\forall x P(x)$ 中受约束
- 未受量词约束的变量为自由变量

### 嵌套量词

$$\forall x \exists y L(x,y) \neq \exists y \forall x L(x,y)$$

- $\forall x \exists y$：每个 $x$ 存在（可能不同的）$y$
- $\exists y \forall x$：存在一个 $y$ 适用于所有 $x$

### 量词的否定

$$\neg \forall x P(x) \equiv \exists x \neg P(x)$$
$$\neg \exists x P(x) \equiv \forall x \neg P(x)$$

## 三、推理规则 (Inference Rules)

| 规则 | 名称 | 形式 |
|------|------|------|
| Modus Ponens | 肯定前件 | $P \to Q, P \therefore Q$ |
| Modus Tollens | 否定后件 | $P \to Q, \neg Q \therefore \neg P$ |
| 假言三段论 | 传递性 | $P \to Q, Q \to R \therefore P \to R$ |
| 析取三段论 | 消去析取 | $P \vee Q, \neg P \therefore Q$ |
| 简化律 | 消去合取 | $P \wedge Q \therefore P$ |
| 附加律 | 引入析取 | $P \therefore P \vee Q$ |
| 归结原理 | Resolution | $P \vee Q, \neg P \vee R \therefore Q \vee R$ |

## 四、证明技巧

### 直接证明

从前提直接推导出结论。

### 逆否证明

证明 $P \to Q$ 等价于证明其逆否命题 $\neg Q \to \neg P$。

### 反证法

假设结论为假，推导出矛盾，从而原结论为真。

### 数学归纳法

**基础步骤：** 证明 $P(1)$ 为真
**归纳步骤：** 假设 $P(k)$ 为真，证明 $P(k+1)$ 为真

$$\text{若 } P(1) \wedge \forall k(P(k) \to P(k+1)) \text{，则 } \forall n P(n)$$

**强归纳法：** 假设 $P(1), P(2), \dots, P(k)$ 均为真，证明 $P(k+1)$ 为真。

**示例：** 证明 $1 + 2 + \cdots + n = \frac{n(n+1)}{2}$

基础：$n=1$ 时 $1 = 1(2)/2 = 1$ ✓

归纳：假设 $1 + \cdots + k = k(k+1)/2$，则：
$$1 + \cdots + k + (k+1) = \frac{k(k+1)}{2} + (k+1) = \frac{(k+1)(k+2)}{2}$$ ✓
