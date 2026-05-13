# 量子纠错

## 概述

量子纠错（Quantum Error Correction, QEC）是保护量子信息免受噪声和相干影响的关键技术由于量子不可克隆且测量会破坏量子信息，经典纠错方法无法直接移植。量子纠错过将辑量子比特编码到多个物理量子比特的纠缠态中，实现对错误的检出的纠正?
## 量子噪声与错误类?
### 比特翻转错误（Bit Flip Error?$X|0\rangle = |1\rangle$, $X|1\rangle = |0\rangle$，相当于经典比特?0? 翻转?
### 相位翻转错误（Phase Flip Error?$Z|0\rangle = |0\rangle$, $Z|1\rangle = -|1\rangle$，改变相对相位?Z$ 门在 $|+\rangle, |-\rangle$ 基下相当于比特翻转?
### 逢极化信道（Depolarizing Channel?每个量子比特以概?$p$ 被替换为朢大混合?$I/2$，等价于以概?$p/3$ 分别发生 $X$?Y$?Z$ 错误?
### 振幅阻尼（Amplitude Damping?描述能量耗散过程（如自发辐射），?$|1\rangle$ ?$|0\rangle$ 的不可跃迁由 Kraus 算子描述?
## 三量子比特码

### 比特翻转?编码?|0\rangle \rightarrow |0_L\rangle = |000\rangle$, $|1\rangle \rightarrow |1_L\rangle = |111\rangle$

### 纠错流程
1. **编码**：将逻辑态映射到三物理比特纠缠?2. **错误发生**：可能有丢个比特发?$X$ 翻转
3. **综合征测量（Syndrome Measurement?*：过辅助比特进行奇偶校验，不破坏量子?4. **恢复**：根据综合征施加对应的纠正操?
## 九量子比特Shor?
### 编码方案
Shor码结合了比特翻转码和相位翻转码的保护能力，可纠正任意单量子比特错误（$X$?Y$ ?$Z$）?
编码 $|0\rangle$ ?$|1\rangle$?$$|0_L\rangle = \frac{(|000\rangle + |111\rangle)(|000\rangle + |111\rangle)(|000\rangle + |111\rangle)}{2\sqrt{2}}$$
$$|1_L\rangle = \frac{(|000\rangle - |111\rangle)(|000\rangle - |111\rangle)(|000\rangle - |111\rangle)}{2\sqrt{2}}$$

### 错误纠正能力
- 第一层：三比特码保护每个块内的比特翻转错?- 第二层：通过 $|+\rangle, |-\rangle$ 基编码保护块间的相位翻转错误

## Steane?量子比特CSS?
### 基于经典纠错?Steane码基于经典[7,4,3] Hamming码，属于Calderbank-Shor-Steane（CSS）码家族?
### 特点
- 编码1个辑量子比特?个物理量子比?- 可纠正任意单量子比特错误
- 对称结构?X$ ?$Z$ 错误的纠正对称进?- 可过横向门（transversal gates）实现部分容错辑?
## 稳定子形式化（Stabilizer Formalism?
### Pauli?单量子比特Pauli群由 $\{I, X, Y, Z\}$ 及其相位因子 $\{\pm 1, \pm i\}$ 构成?n$ 量子比特Pauli群是张量积的集合?
### 稳定子码（Stabilizer Code?稳定?$S$ 是Pauli群的丢个阿贝尔子群，不?$-I$。合法码字是扢有稳定子算子?$+1$ 本征态：
$$S| \psi \rangle = | \psi \rangle, \quad \forall S \in S$$

### 综合征解?对每个稳定子生成?$g_i$ 进行测量，得到综合征 $s_i \in \{0, 1\}$。综合征向量 $s$ 唯一决定错误类型和位置，从实现纠错?
## 表面码（Surface Codes?
### 拓扑量子纠错
表面码在二维网格上定义，兼具高容错阈值和实验可实现的屢部?
### 平面码（Planar Code）与环面码（Toric Code?- **环面?*：定义在环面上（周期边界条件），编码数取决于拓扑
- **平面?*：定义在弢平面上（边界条件），编码1个辑量子比特
- **容错阈?*：表面码在独立错误模型下的阈值约?$\sim 1\%$

### 纠错机制
- 通过测量 plaquette ?star 算子实现综合征提?- 朢小权重完美匹配（MWPM）解码器寻找朢可能的错误配?
## 无相干子空间（Decoherence-Free Subspace, DFS?
利用系统的集体对称，在系统与环境耦合对称的特定子空间中编码量子信息当噪声具有集体对称性时，DFS 可以完全免于逢相干?
## 容错量子计算（Fault-Tolerant Quantum Computing?
### 阈定理（Threshold Theorem?如果每个物理门的错误率低于某个阈值（量子纠错码的容错阈），则可以通过分层编码实现任意精度的量子计算?
### 容错门实?- **横向?*（Transversal Gates）：对码字的每个物理比特分别执行，不会在丢个码块内传播错误
- **魔蒸?*（Magic State Distillation）：获得非克利福德门（如 $T$ 门）扢霢的辅助?- **门编?*：将量子算法编译到容错门集合?

## 相关条目

[[02_NaturalSciences/Physics/QuantumMechanics/INDEX|QuantumMechanics]], ComputerScience, Cryptography, [[QuantumComputing]]
