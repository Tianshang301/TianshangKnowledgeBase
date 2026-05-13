# 鍩哄洜缁勬暟鎹垎鏋?
## 姒傝堪

鍩哄洜缁勬暟鎹垎鏋愭槸鐢熺墿淇℃伅瀛︾殑鏍稿績鍐呭锛屾秹鍙奃NA搴忓垪鐨勬祴瀹氥€佺粍瑁呫€佹瘮瀵广€佹敞閲婂拰鍒嗘瀽銆傞殢鐫€娴嬪簭鎶€鏈殑椋為€熷彂灞曪紝鍩哄洜缁勬暟鎹憟鎸囨暟绾у闀匡紝涓虹敓鍛界瀛︾爺绌舵彁渚涗簡鍓嶆墍鏈湁鐨勬満閬囥€?
## 娴嬪簭鎶€鏈?
### Sanger娴嬪簭

**鍘熺悊锛?*
- 鍙岃劚姘ч摼缁堟娉?- 浣跨敤ddNTP闅忔満缁堟DNA鍚堟垚
- 鐢垫吵鍒嗙涓嶅悓闀垮害鐨勭墖娈?- 婵€鍏夋娴嬭崸鍏変俊鍙?
**鐗圭偣锛?*
- 璇婚暱闀匡紙700-1000 bp锛?- 鍑嗙‘鐜囬珮锛?9.99%锛?- 閫氶噺浣?- 鎴愭湰楂?
**搴旂敤锛?*
- 灏忕墖娈垫祴搴?- 楠岃瘉鎬ф祴搴?- 鍗曞熀鍥犵柧鐥呮娴?
### 浜屼唬娴嬪簭锛圢GS锛?
**Illumina骞冲彴锛?*
- 杈瑰悎鎴愯竟娴嬪簭锛圫BS锛?- 妗ュ紡PCR鎵╁
- 璇婚暱鐭紙50-300 bp锛?- 閫氶噺楂橈紝鎴愭湰浣?
**涓昏骞冲彴锛?*
- HiSeq绯诲垪锛氶珮閫氶噺
- MiSeq绯诲垪锛氫腑绛夐€氶噺
- NextSeq绯诲垪锛氫腑楂橀€氶噺
- NovaSeq绯诲垪锛氳秴楂橀€氶噺

**鏂囧簱绫诲瀷锛?*
- PE锛圥aired-End锛夛細鍙岀娴嬪簭
- SE锛圫ingle-End锛夛細鍗曠娴嬪簭

### 涓変唬娴嬪簭

**PacBio SMRT锛?*
- 鍗曞垎瀛愬疄鏃舵祴搴?- 璇婚暱闀匡紙10-30 kb锛?- 鍙娴嬬⒈鍩轰慨楗?- 閿欒鐜囪緝楂橈紙~15%锛?
**Oxford Nanopore锛?*
- 绾崇背瀛旀祴搴?- 瓒呴暱璇婚暱锛堝彲杈炬暟Mb锛?- 瀹炴椂娴嬪簭
- 璁惧渚挎惡锛圡inION锛?
**浼樺娍锛?*
- 瑙ｅ喅閲嶅鍖哄煙
- 妫€娴嬬粨鏋勫彉寮?- 鐩存帴妫€娴嬬敳鍩哄寲
- 瀹屾暣鍩哄洜缁勭粍瑁?
## 搴忓垪姣斿

### BLAST

**鍘熺悊锛?*
- 灞€閮ㄥ簭鍒楁瘮瀵?- 鍩轰簬绉嶅瓙鐨勫惎鍙戝紡绠楁硶
- 鍒嗘暟鐭╅樀璇勫垎

**绫诲瀷锛?*
- blastn锛氭牳鑻烽吀姣斿
- blastp锛氳泲鐧借川姣斿
- blastx锛氱炕璇戞牳鑻烽吀姣斿铔嬬櫧璐?- tblastn锛氳泲鐧借川姣斿缈昏瘧鏍歌嫹閰?- tblastx锛氱炕璇戞牳鑻烽吀姣斿缈昏瘧鏍歌嫹閰?
**鍙傛暟锛?*
- E鍊硷細鏈熸湜鍊硷紝瓒婂皬瓒婃樉钁?- Bit score锛氭瘮瀵瑰緱鍒嗭紝瓒婂ぇ瓒婂ソ
- Identity锛氫竴鑷存€х櫨鍒嗘瘮

### BWA

**鐗圭偣锛?*
- 涓撲负鐭闀胯璁?- Burrows-Wheeler鍙樻崲
- 楂樻晥鐨勫唴瀛樹娇鐢?
**绠楁硶锛?*
- BWA-backtrack锛氶€傜敤浜嶪llumina鐭闀匡紙<100 bp锛?- BWA-SW锛氶€傜敤浜庤緝闀胯闀匡紙70-1000 bp锛?- BWA-MEM锛氶€氱敤绠楁硶锛屾敮鎸侀暱璇婚暱

**浣跨敤娴佺▼锛?*
```bash
# 寤虹珛绱㈠紩
bwa index reference.fa

# 姣斿
bwa mem reference.fa read1.fq read2.fq > aligned.sam

# 鎺掑簭
samtools sort aligned.sam -o aligned.bam

# 寤虹珛绱㈠紩
samtools index aligned.bam
```

## 鍙樺紓妫€娴?
### SNP妫€娴?
**鍗曟牳鑻烽吀澶氭€佹€э紙SNP锛夛細**
- 鍗曚釜纰卞熀鐨勫彉寮?- 浜虹被鍩哄洜缁勪腑绾︽瘡300 bp涓€涓猄NP

**妫€娴嬫祦绋嬶細**
1. 搴忓垪姣斿鍒板弬鑰冨熀鍥犵粍
2. 鍙樺紓璇嗗埆锛圙ATK銆丼amtools锛?3. 鍙樺紓杩囨护锛堣川閲忋€佹繁搴︼級
4. 鍙樺紓娉ㄩ噴锛堝姛鑳姐€侀鐜囷級

**GATK鏈€浣冲疄璺碉細**
```bash
# HaplotypeCaller
gatk HaplotypeCaller -R reference.fa -I aligned.bam -O raw_variants.vcf

# 鍙樺紓杩囨护
gatk VariantFiltration -V raw_variants.vcf -O filtered_variants.vcf
```

### Indel妫€娴?
**鎻掑叆/缂哄け锛圛ndel锛夛細**
- 灏忕墖娈电殑鎻掑叆鎴栫己澶?- 瀵硅泲鐧借川鍔熻兘褰卞搷澶?
**妫€娴嬫柟娉曪細**
- 鍩轰簬姣斿鐨勬柟娉?- 鍩轰簬缁勮鐨勬柟娉?- 娣峰悎鏂规硶

### SV妫€娴?
**缁撴瀯鍙樺紓锛圫V锛夛細**
- 澶х墖娈电殑鍙樺紓锛?50 bp锛?- 鍖呮嫭缂哄け銆侀噸澶嶃€佸€掍綅銆佹槗浣?
**妫€娴嬫柟娉曪細**
- 鍩轰簬璇诲锛圥aired-end锛夌殑鏂规硶
- 鍩轰簬鍒嗚璇伙紙Split-read锛夌殑鏂规硶
- 鍩轰簬娣卞害锛圧ead-depth锛夌殑鏂规硶
- 鍩轰簬缁勮锛圓ssembly锛夌殑鏂规硶

**宸ュ叿锛?*
- DELLY
- Manta
- Lumpy
- Sniffles锛堜笁浠ｆ祴搴忥級

## 鍩哄洜琛ㄨ揪鍒嗘瀽

### RNA-seq

**瀹為獙娴佺▼锛?*
1. RNA鎻愬彇
2. mRNA瀵岄泦鎴杛RNA鍘婚櫎
3. cDNA鍚堟垚
4. 鏂囧簱鏋勫缓
5. 娴嬪簭
6. 鏁版嵁鍒嗘瀽

**鍒嗘瀽娴佺▼锛?*
```bash
# 璐ㄦ帶
fastqc raw_reads.fq
multiqc .

# 杩囨护
fastp -i raw_reads.fq -o clean_reads.fq

# 姣斿
hisat2 -x genome_index -1 read1.fq -2 read2.fq | samtools sort -o aligned.bam

# 瀹氶噺
featureCounts -a annotation.gtf -o counts.txt aligned.bam
```

### 宸紓琛ㄨ揪鍒嗘瀽

**R璇█娴佺▼锛?*
```r
library(DESeq2)

# 鍒涘缓DESeq瀵硅薄
dds <- DESeqDataSetFromMatrix(countData = counts,
                              colData = metadata,
                              design = ~ condition)

# 宸紓鍒嗘瀽
dds <- DESeq(dds)
res <- results(dds)

# 缁撴灉杩囨护
res_sig <- res[which(res$padj < 0.05 & abs(res$log2FoldChange) > 1), ]
```

### 鍔熻兘瀵岄泦鍒嗘瀽

**GO瀵岄泦鍒嗘瀽锛?*
- 鐢熺墿杩囩▼锛圔iological Process锛?- 鍒嗗瓙鍔熻兘锛圡olecular Function锛?- 缁嗚優缁勫垎锛圕ellular Component锛?
**KEGG瀵岄泦鍒嗘瀽锛?*
- 浠ｈ阿閫氳矾
- 淇″彿閫氳矾
- 鐤剧梾閫氳矾

**宸ュ叿锛?*
- clusterProfiler锛圧锛?- DAVID
- Metascape
- g:Profiler

## 鍩哄洜缁勬敞閲?
### 鍩哄洜娉ㄩ噴

**浠庡ご棰勬祴锛圓b initio锛夛細**
- 鍩轰簬搴忓垪鐗瑰緛
- 棰勬祴鍩哄洜缁撴瀯
- 宸ュ叿锛欸eneScan銆丄ugustus

**鍚屾簮娉ㄩ噴锛?*
- 鍩轰簬宸茬煡鍩哄洜
- 姣斿鍒板凡鐭ユ暟鎹簱
- 宸ュ叿锛欱LAST銆丒xonerate

**杞綍缁勮緟鍔╋細**
- 鍩轰簬RNA-seq鏁版嵁
- 楠岃瘉鍩哄洜缁撴瀯
- 宸ュ叿锛歋tringTie銆丆ufflinks

### 鍔熻兘娉ㄩ噴

**鏁版嵁搴擄細**
- Gene Ontology锛圙O锛?- KEGG
- InterPro
- Pfam

**娉ㄩ噴鍐呭锛?*
- 鍩哄洜鍔熻兘
- 铔嬬櫧璐ㄧ粨鏋勫煙
- 浠ｈ阿閫氳矾
- 铔嬬櫧璐ㄧ浉浜掍綔鐢?
## 鐢熺墿淇℃伅瀛﹀伐鍏烽摼

### 甯哥敤宸ュ叿

**搴忓垪澶勭悊锛?*
- seqtk锛氬簭鍒楁搷浣?- seqkit锛氬鍔熻兘搴忓垪宸ュ叿
- biopython锛歅ython搴?
**姣斿宸ュ叿锛?*
- BWA锛氱煭璇婚暱姣斿
- Minimap2锛氶暱璇婚暱姣斿
- STAR锛歊NA-seq姣斿

**鍙樺紓妫€娴嬶細**
- GATK锛氬彉寮傛娴嬫爣鍑嗗伐鍏?- Samtools锛歋AM/BAM鏂囦欢鎿嶄綔
- VCFtools锛歏CF鏂囦欢鎿嶄綔

**鍙鍖栵細**
- IGV锛氬熀鍥犵粍娴忚鍣?- Circos锛氱幆褰㈠熀鍥犵粍鍙鍖?- Tablet锛氬簭鍒楁瘮瀵瑰彲瑙嗗寲

### 娴佺▼绠＄悊

**Snakemake锛?*
```python
rule all:
    input: "results/report.html"

rule align:
    input: "data/reads.fq"
    output: "results/aligned.bam"
    shell: "bwa mem ref.fa {input} | samtools sort -o {output}"
```

**Nextflow锛?*
```groovy
process ALIGN {
    input: reads from 'data/reads.fq'
    output: aligned.bam
    script: "bwa mem ref.fa $reads | samtools sort -o aligned.bam"
}
```

## 鍙傝€冭祫婧?
- 璐句笝. 銆婄敓鐗╀俊鎭銆?- Durbin R, et al. *Sequence Analysis in Genetics*
- 銆奌igh-Throughput Sequencing in Biological Research銆?- 1000 Genomes Project
- ENCODE Project

## 鐩稿叧鏉＄洰

ComputationalBiology, [[02_NaturalSciences/Biology/Genetics/INDEX|Genetics]], [[07_InterdisciplinarySciences/DataScience/INDEX|DataScience]], Genomics, [[02_NaturalSciences/Biology/MolecularBiology/INDEX|MolecularBiology]]
