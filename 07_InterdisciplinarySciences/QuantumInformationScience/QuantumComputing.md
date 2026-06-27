---
aliases: [QuantumComputing]
tags: ['QuantumInformationScience', 'QuantumComputing']
created: 2026-05-16
updated: 2026-05-16
---

# 量子计算

## 概述

量子计算是利用量子力学原理（如叠加和纠缠）进行信息处理的新型计算范式。它有望在特定问题上实现指数级加速，对密码学、优化机器学习等领域产生革命性影响?
## 量子比特

### 基本概念

**经典比特?* 0?

**量子比特（Qubit）：**
$$|\psi\rangle = \alpha|0\rangle + \beta|1\rangle$$

其中$|\alpha|^2 + |\beta|^2 = 1$

### 叠加?
**原理?*
- 量子比特可同时处??的叠?- 测量时坍缩到其中丢个状?- 测量概率由系数决?
**示例?*
$$|+\rangle = \frac{1}{\sqrt{2}}(|0\rangle + |1\rangle)$$

### 纠缠?
**Bell 态：**
$$|\Phi^+\rangle = \frac{1}{\sqrt{2}}(|00\rangle + |11\rangle)$$

**特：**
- 非局域关?- 测量丢个粒子影响另丢?- 量子通信基础

### Bloch 球表?
**单量子比特状态：**
$$|\psi\rangle = \cos\frac{\theta}{2}|0\rangle + e^{i\phi}\sin\frac{\theta}{2}|1\rangle$$

**几何表示?*
- 北极：|0?- 南极：|1?- 赤道：叠加?
## 量子?
### 单量子比特门

**Pauli 门：**
$$X = \begin{pmatrix} 0 & 1 \\ 1 & 0 \end{pmatrix}, \quad Y = \begin{pmatrix} 0 & -i \\ i & 0 \end{pmatrix}, \quad Z = \begin{pmatrix} 1 & 0 \\ 0 & -1 \end{pmatrix}$$

**Hadamard 门（H）：**
$$H = \frac{1}{\sqrt{2}}\begin{pmatrix} 1 & 1 \\ 1 & -1 \end{pmatrix}$$

作用：创建叠加?$$H|0\rangle = |+\rangle, \quad H|1\rangle = |-\rangle$$

**相位门（S、T）：**
$$S = \begin{pmatrix} 1 & 0 \\ 0 & i \end{pmatrix}, \quad T = \begin{pmatrix} 1 & 0 \\ 0 & e^{i\pi/4} \end{pmatrix}$$

**旋转门（Rx、Ry、Rz）：**
$$R_x(\theta) = \begin{pmatrix} \cos\frac{\theta}{2} & -i\sin\frac{\theta}{2} \\ -i\sin\frac{\theta}{2} & \cos\frac{\theta}{2} \end{pmatrix}$$

### 多量子比特门

**CNOT 门（受控非门）：**
$$CNOT = \begin{pmatrix} 1 & 0 & 0 & 0 \\ 0 & 1 & 0 & 0 \\ 0 & 0 & 0 & 1 \\ 0 & 0 & 1 & 0 \end{pmatrix}$$

作用：控制比特为1时，目标比特翻转

**Toffoli 门（CCNOT）：**
- 双控制非?- 可计算基硢
- 通用经典计算

**SWAP 门：**
$$SWAP = \begin{pmatrix} 1 & 0 & 0 & 0 \\ 0 & 0 & 1 & 0 \\ 0 & 1 & 0 & 0 \\ 0 & 0 & 0 & 1 \end{pmatrix}$$

### 通用量子门集

**通用门集?*
- {H, T, CNOT}构成通用门集
- 可近似任意酉变换
- Solovay-Kitaev 定理

## 量子算法

### Shor 算法

**问题?* 大整数分?
**经典算法?* 指数时间
**Shor 算法?* 多项式时?
**核心思想?*
1. 将分解问题转化为求阶问题
2. 量子傅里叶变换求周期
3. 经典后处理得到因?
**步骤?*
1. 随机选择 a < N
2. 用量子电路求 f(x) = a^x mod N 的周期 r
3. 若 r 为偶数，计算 gcd(a^(r/2) ± 1, N)

**影响?*
- RSA 加密面临威胁
- 推动后量子密码发?
### Grover 算法

**问题?* 无序数据库搜?
**经典算法?* O(N)
**Grover 算法?* O(√N)

**核心思想?*
- 量子振幅放大
- 迭代放大目标态振?
**算法步骤?*
1. 初始化均匢叠加?2. 重复√N 次：
   - Oracle 标记目标?   - 扩散算子放大振幅
3. 测量得到目标

**应用?*
- 数据库搜?- 优化问题
- SAT 问题

### 其他重要算法

**量子相位估计?*
- 估计酉算子的本征?- 许多量子算法的基硢

**HHL 算法?*
- 线方程组求解
- 指数加（特定条件?
**VQE（变分量子本征求解器）：**
- 混合量子-经典算法
- 量子化学应用
- 适合近期 NISQ 设备

**QAOA（量子近似优化算法）?*
- 组合优化问题
- 变分方法
- NISQ 友好

## 量子纠错

### 量子错误类型

**比特翻转错误?* |0⟩→|1?**相位翻转错误?* |+⟩→|−⟩
**比特-相位翻转错误?* 两的组合

### 量子纠错?
**Shor 码：**
- 9量子比特?- 纠正任意单量子比特错?- 概念验证

**Steane 码：**
- 7量子比特?- CSS?- 容错计算基础

**表面码：**
- 二维结构
- 高容错阈?- 实验可行性高

### 容错量子计算

**容错阈定理：**
- 若错误率低于阈，可任意降?- 霢要冗余编?- 阈约0.1%-1%

## 物理实现

### 超导量子比特

**类型?*
- Transmon：最常用
- Fluxonium
- Xmon

**特点?*
- 操作速度快（~ns?- 可扩展好
- 霢要极低温（~10 mK?
**代表?*
- IBM 量子计算?- Google Sycamore

### 离子?
**原理?*
- 濢光囚禁离?- 内部能级编码
- 离子运动耦合

**特点?*
- 相干时间?- 门保真度?- 操作速度较慢

**代表?*
- IonQ
- Quantinuum

### 拓扑量子计算

**原理?*
- 非阿贝尔任意?- 拓扑保护
- 天然容错

**状：**
- 理论研究阶段
- 实验探索?- 微软研究

### 其他平台

- **中原子：** 里德堡?- **量子点：** 半导体自?- **NV 中心?* 金刚石缺?
## 量子计算编程框架

### Qiskit

**特点?*
- IBM 弢?- Python API
- 丰富的组?
**主要模块?*
- qiskit-terra：基硢电路
- qiskit-aer：模拟器
- qiskit-ignis：纠?- qiskit-aqua：应?
**示例代码?*
```python
from qiskit import QuantumCircuit, execute, Aer

# 创建量子电路
qc = QuantumCircuit(2, 2)
qc.h(0)
qc.cx(0, 1)
qc.measure([0, 1], [0, 1])

# 模拟
backend = Aer.get_backend('qasm_simulator')
result = execute(qc, backend, shots=1024).result()
print(result.get_counts())
```

### Cirq

**特点?*
- Google 弢?- NISQ 导向
- 灵活定制

**主要功能?*
- 电路构建
- 模拟?- 与量子硬件接?
**示例代码?*
```python
import cirq

# 创建量子比特
q0, q1 = cirq.LineQubit.range(2)

# 创建电路
circuit = cirq.Circuit([
    cirq.H(q0),
    cirq.CNOT(q0, q1),
    cirq.measure(q0, q1)
])

# 模拟
simulator = cirq.Simulator()
result = simulator.run(circuit, repetitions=1024)
print(result.histogram(key='q(0),q(1)'))
```

### 其他框架

- **PennyLane?* 量子机器学习
- **Q#?* 微软量子弢?- **Strawberry Fields?* 光量子计?
## 参资?
- Nielsen MA, Chuang IL. *Quantum Computation and Quantum Information*
- 《量子计算与量子信息?- Qiskit 教材：https://qiskit.org/learn/
- Preskill J. *Quantum Computing in the NISQ Era and Beyond*

## 相关条目

[[02_NaturalSciences/Physics/QuantumMechanics/INDEX|QuantumMechanics]], ComputerScience, Cryptography, [[QuantumComputing]]

