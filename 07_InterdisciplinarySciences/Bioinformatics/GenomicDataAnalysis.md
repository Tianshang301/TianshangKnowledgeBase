---
aliases: [GenomicDataAnalysis]
tags: ['Bioinformatics', 'GenomicDataAnalysis']
created: 2026-05-16
updated: 2026-05-16
---

# 基因组数据分?
## 概述

基因组数据分析是生物信息学的核心内容，涉及 DNA 序列的测定组装比对注释和分析。随睢测序抢术的飞发展，基因组数据呈指数级增长，为生命科学研究提供了前所未有的机遇?
## 测序抢?
### Sanger 测序

**原理?*
- 双脱氧链终止?- 使用 ddNTP 随机终止 DNA 合成
- 电泳分离不同长度的片?- 濢光检测荧光信?
**特点?*
- 读长长（700-1000 bp?- 准确率高?9.99%?- 通量?- 成本?
**应用?*
- 小片段测?- 验证性测?- 单基因疾病检?
### 二代测序（NGS?
**Illumina 平台?*
- 边合成边测序（SBS?- 桥式 PCR 扩增
- 读长短（50-300 bp?- 通量高，成本?
**主要平台?*
- HiSeq 系列：高通量
- MiSeq 系列：中等量
- NextSeq 系列：中高量
- NovaSeq 系列：超高量

**文库类型?*
- PE（Paired-End）：双端测序
- SE（Single-End）：单端测序

### 三代测序

**PacBio SMRT?*
- 单分子实时测?- 读长长（10-30 kb?- 可检测碱基修?- 错误率较高（~15%?
**Oxford Nanopore?*
- 纳米孔测?- 超长读长（可达数 Mb?- 实时测序
- 设备便携（MinION?
**优势?*
- 解决重复区域
- 棢测结构变?- 直接棢测甲基化
- 完整基因组组?
## 序列比对

### BLAST

**原理?*
- 屢部序列比?- 基于种子的启发式算法
- 分数矩阵评分

**类型?*
- blastn：核苷酸比对
- blastp：蛋白质比对
- blastx：翻译核苷酸比对蛋白?- tblastn：蛋白质比对翻译核苷?- tblastx：翻译核苷酸比对翻译核苷?
**参数?*
- E 值：期望值，越小越显?- Bit score：比对得分，越大越好
- Identity：一致百分比

### BWA

**特点?*
- 专为短读长设?- Burrows-Wheeler 变换
- 高效的内存使?
**算法?*
- BWA-backtrack：用于 Illumina 短读长（<100 bp?- BWA-SW：用于较长读长（70-1000 bp?- BWA-MEM：用算法，支持长读长

**使用流程?*
```bash
# 建立索引
bwa index reference.fa

# 比对
bwa mem reference.fa read1.fq read2.fq > aligned.sam

# 排序
samtools sort aligned.sam -o aligned.bam

# 建立索引
samtools index aligned.bam
```

## 变异棢?
### SNP 棢?
**单核苷酸多（SNP）：**
- 单个碱基的变?- 人类基因组中约每300 bp 丢个 SNP

**棢测流程：**
1. 序列比对到参考基因组
2. 变异识别（GATK、Samtools?3. 变异过滤（质量深度）
4. 变异注释（功能频率）

**GATK 朢佳实践：**
```bash
# HaplotypeCaller
gatk HaplotypeCaller -R reference.fa -I aligned.bam -O raw_variants.vcf

# 变异过滤
gatk VariantFiltration -V raw_variants.vcf -O filtered_variants.vcf
```

### Indel 棢?
**插入/缺失（Indel）：**
- 小片段的插入或缺?- 对蛋白质功能影响?
**棢测方法：**
- 基于比对的方?- 基于组装的方?- 混合方法

### SV 棢?
**结构变异（SV）：**
- 大片段的变异?50 bp?- 包括缺失、重复位、易?
**棢测方法：**
- 基于读对（Paired-end）的方法
- 基于分裂读（Split-read）的方法
- 基于深度（Read-depth）的方法
- 基于组装（Assembly）的方法

**工具?*
- DELLY
- Manta
- Lumpy
- Sniffles（三代测序）

## 基因表达分析

### RNA-seq

**实验流程?*
1. RNA 提取
2. mRNA 富集或 rRNA 去除
3. cDNA 合成
4. 文库构建
5. 测序
6. 数据分析

**分析流程?*
```bash
# 质控
fastqc raw_reads.fq
multiqc .

# 过滤
fastp -i raw_reads.fq -o clean_reads.fq

# 比对
hisat2 -x genome_index -1 read1.fq -2 read2.fq | samtools sort -o aligned.bam

# 定量
featureCounts -a annotation.gtf -o counts.txt aligned.bam
```

### 差异表达分析

**R 语言流程?*
```r
library(DESeq2)

# 创建 DESeq 对象
dds <- DESeqDataSetFromMatrix(countData = counts,
                              colData = metadata,
                              design = ~ condition)

# 差异分析
dds <- DESeq(dds)
res <- results(dds)

# 结果过滤
res_sig <- res[which(res$padj < 0.05 & abs(res$log2FoldChange) > 1), ]
```

### 功能富集分析

**GO 富集分析?*
- 生物过程（Biological Process?- 分子功能（Molecular Function?- 细胞组分（Cellular Component?
**KEGG 富集分析?*
- 代谢通路
- 信号通路
- 疾病通路

**工具?*
- clusterProfiler（R?- DAVID
- Metascape
- g:Profiler

## 基因组注?
### 基因注释

**从头预测（Ab initio）：**
- 基于序列特征
- 预测基因结构
- 工具：GeneScan、Augustus

**同源注释?*
- 基于已知基因
- 比对到已知数据库
- 工具：BLAST、Exonerate

**转录组辅助：**
- 基于 RNA-seq 数据
- 验证基因结构
- 工具：StringTie、Cufflinks

### 功能注释

**数据库：**
- Gene Ontology（GO?- KEGG
- InterPro
- Pfam

**注释内容?*
- 基因功能
- 蛋白质结构域
- 代谢通路
- 蛋白质相互作?
## 生物信息学工具链

### 常用工具

**序列处理?*
- seqtk：序列操?- seqkit：多功能序列工具
- biopython：Python?
**比对工具?*
- BWA：短读长比对
- Minimap2：长读长比对
- STAR：RNA-seq 比对

**变异棢测：**
- GATK：变异检测标准工?- Samtools：SAM/BAM 文件操作
- VCFtools：VCF 文件操作

**可视化：**
- IGV：基因组浏览?- Circos：环形基因组可视?- Tablet：序列比对可视化

### 流程管理

**Snakemake?*
```python
rule all:
    input: "results/report.html"

rule align:
    input: "data/reads.fq"
    output: "results/aligned.bam"
    shell: "bwa mem ref.fa {input} | samtools sort -o {output}"
```

**Nextflow?*
```groovy
process ALIGN {
    input: reads from 'data/reads.fq'
    output: aligned.bam
    script: "bwa mem ref.fa $reads | samtools sort -o aligned.bam"
}
```

## 参资?
- 贾丙. 《生物信息学?- Durbin R, et al. *Sequence Analysis in Genetics*
- 《High-Throughput Sequencing in Biological Research?- 1000 Genomes Project
- ENCODE Project

## 相关条目

ComputationalBiology, [[02_NaturalSciences/Biology/Genetics/INDEX|Genetics]], [[07_InterdisciplinarySciences/DataScience/INDEX|DataScience]], Genomics, [[02_NaturalSciences/Biology/MolecularBiology/INDEX|MolecularBiology]]

