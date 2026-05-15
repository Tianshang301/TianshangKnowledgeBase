---
aliases: [ProteinStructure]
tags: ['Bioinformatics', 'ProteinStructure']
---

# 蛋白质结?
## 概述

蛋白质结构研究是结构生物学的核心内容，对于理解蛋白质功能、药物设计和蛋白质工程具有重要意义蛋白质的三维结构决定了其生物学功能?
## 蛋白质结构层?
### 丢级结构（Primary Structure?
**定义?* 氨基酸的线序?
**特点?*
- 由基因编码决?- 决定蛋白质的高级结构
- 包含翻译后修饰信?
**表示方法?*
- 单字母代码：MKTIIALSYIFCLVFADYK...
- 三字母代码：Met-Lys-Thr-Ile-Ile-Ala-...

**数据库：**
- UniProt：蛋白质序列数据?- NCBI Protein：蛋白质序列

### 二级结构（Secondary Structure?
**定义?* 屢部主链的规则折叠模式

**主要类型?*

**α-螺旋（?helix）：**
- 螺旋上升：每个氨基酸上升1.5 Å
- 每圈3.6个氨基酸
- 氢键：第i个与第i+4个氨基酸之间
- 右手螺旋

**β-折叠（?sheet）：**
- 平行或反平行排列
- 氢键：链间形?- 折叠角度：约35°

**无规卷曲（Random Coil）：**
- 无规则结?- 连接其他二级结构元素
- 具有柔?
**预测工具?*
- PSIPRED：基于神经网?- JPred：基于HMM
- NetSurfP：表面可及预?
### 三级结构（Tertiary Structure?
**定义?* 整条多肽链的三维构象

**稳定因素?*
- 二硫键（S-S键）
- 疏水相互作用
- 氢键
- 离子键（盐桥?- 范德华力

**结构域（Domain）：**
- 独立折叠的功能单?- 可独立存?- 执行特定功能

**蛋白质折叠类型：**
- α/β型：α螺旋和β折叠交?- α+β型：α螺旋和β折叠分弢
- α型：主要由α螺旋组?- β型：主要由β折叠组?
### 四级结构（Quaternary Structure?
**定义?* 多个亚基的空间排?
**特征?*
- 亚基间的非共价相互作?- 协同效应（如衢红蛋白）
- 变构调节

**典型例子?*
- 衢红蛋白：α₂β₂四聚?- DNA聚合酶：多个亚基复合?- 抗体：四链结?
## 结构预测方法

### 同源建模（Homology Modeling?
**原理?*
- 基于已知结构的模板蛋?- 目标序列与模板序列同源?30%

**步骤?*
1. 模板搜索（BLAST?2. 序列比对
3. 骨架建模
4. 环区建模
5. 侧链建模
6. 能量朢小化
7. 模型评估

**常用软件?*
- MODELLER
- SWISS-MODEL
- Phyre2

### 穿线法（Threading?
**原理?*
- 将目标序列穿入已知的折叠模板
- 适用于远缘同源蛋?
**方法?*
- 基于势能函数
- 基于统计?- 机器学习方法

**工具?*
- I-TASSER
- LOMETS
- Phyre2

### AlphaFold

**AlphaFold2架构?*
- Evoformer：提取进化和结构信息
- Structure Module：生?D坐标
- 端到端学?
**创新点：**
- 注意力机制：捕获长程相互作用
- 迭代优化：步改进预测
- 置信度评估：pLDDT分数

**性能?*
- CASP14竞赛中表现优?- 接近实验精度（RMSD<1Å?
**使用?*
```bash
# 安装AlphaFold2
git clone https://github.com/deepmind/alphafold
cd alphafold

# 运行预测
python alphafold/data/tools/run_alphafold.py \
  --fasta_paths=sequence.fasta \
  --output_dir=output/
```

## 蛋白质折叠问?
### Levinthal悖论

**问题?* 如果蛋白质随机折叠，找到正确构象霢要的时间远超宇宙年龄

**解释?*
- 折叠不是随机搜索
- 存在能量漏斗
- 折叠路径是确定的

### 能量漏斗模型

**特征?*
- 未折叠：高能量，高熵
- 折叠中间态：能量逐渐降低
- 天然态：朢低能量构?
**折叠路径?*
1. 快疏水塌?2. 二级结构形成
3. 三级结构调整
4. 天然态优?
### 折叠疾病

**淢粉样变疾病：**
- 阿尔茨海默病：Aβ和tau蛋白
- 帕金森病：?突触核蛋?- 朊病毒病：朊蛋白
- 亨廷顿病：polyQ扩展

**机制?*
- 蛋白质错误折?- 聚集形成淢粉样纤维
- 细胞毒?
## 蛋白质数据库

### PDB（Protein Data Bank?
**内容?*
- 实验测定?D结构
- X射线晶体学NMR、Cryo-EM

**访问?*
- 网站：https://www.rcsb.org/
- FTP下载：ftp://ftp.wwpdb.org/

**PDB文件格式?*
```
ATOM      1  N   ALA A   1      27.340  24.430   2.614  1.00 10.30           N
ATOM      2  CA  ALA A   1      26.267  25.417   2.822  1.00  9.77           C
```

**主要字段?*
- ATOM：原子记?- HETATM：非标准原子
- CONECT：连接记?
### 其他数据?
**序列数据库：**
- UniProt：蛋白质序列和功?- NCBI Protein：综合序列数据库

**结构数据库：**
- SCOP：蛋白质结构分类
- CATH：结构分?- Pfam：蛋白质家族

**预测结构数据库：**
- AlphaFold DB：AI预测结构
- SWISS-MODEL Repository：同源建模结?
## 分子动力学模拟基硢

### 基本原理

**牛顿运动定律?*
$$F = ma = m\frac{d^2r}{dt^2}$$

**力场?*
$$E_{total} = E_{bond} + E_{angle} + E_{dihedral} + E_{vdW} + E_{electrostatic}$$

**常用力场?*
- AMBER
- CHARMM
- GROMOS
- OPLS

### 模拟流程

1. 系统准备（添加溶剂离子）
2. 能量朢小化
3. 平衡模拟
4. 生产模拟
5. 轨迹分析

### 常用软件

**GROMACS?*
```bash
# 能量朢小化
gmx grompp -f em.mdp -c system.gro -p topol.top -o em.tpr
gmx mdrun -v -deffnm em

# 平衡模拟
gmx grompp -f nvt.mdp -c em.gro -p topol.top -o nvt.tpr
gmx mdrun -deffnm nvt

# 生产模拟
gmx grompp -f md.mdp -c nvt.gro -p topol.top -o md.tpr
gmx mdrun -deffnm md
```

**其他软件?*
- AMBER
- NAMD
- OpenMM
- LAMMPS

### 轨迹分析

**常用分析?*
- RMSD：均方根偏差
- RMSF：均方根涨落
- 回转半径：蛋白质紧凑程度
- 氢键分析
- 二级结构演化

**可视化：**
- VMD
- PyMOL
- UCSF Chimera

## 参资?
- Alberts B, et al. *Molecular Biology of the Cell*
- 《蛋白质结构与功能?- AlphaFold DB：https://alphafold.ebi.ac.uk/
- PDB：https://www.rcsb.org/
- GROMACS官方文档

## 相关条目

ComputationalBiology, [[02_NaturalSciences/Biology/Genetics/INDEX|Genetics]], [[07_InterdisciplinarySciences/DataScience/INDEX|DataScience]], Genomics, [[02_NaturalSciences/Biology/MolecularBiology/INDEX|MolecularBiology]]
