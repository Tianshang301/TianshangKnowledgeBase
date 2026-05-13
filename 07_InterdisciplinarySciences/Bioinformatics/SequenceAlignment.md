# 搴忓垪姣斿

## 姒傝堪

搴忓垪姣斿鏄敓鐗╀俊鎭鐨勫熀纭€鎶€鏈紝鐢ㄤ簬姣旇緝涓や釜鎴栧涓敓鐗╁簭鍒楋紙DNA銆丷NA鎴栬泲鐧借川锛夌殑鐩镐技鎬с€傞€氳繃姣斿鍙互鍙戠幇搴忓垪闂寸殑鍚屾簮鎬с€佷繚瀹堝尯鍩熷拰鍔熻兘浣嶇偣銆?
## 鍙屽簭鍒楁瘮瀵?
### 鍏ㄥ眬姣斿锛圢eedleman-Wunsch绠楁硶锛?
**鍘熺悊锛?*
- 瀵逛袱鏉″簭鍒楄繘琛屽叏绋嬫瘮瀵?- 閫傜敤浜庨暱搴﹀拰鐩镐技鎬ц緝楂樼殑搴忓垪

**绠楁硶姝ラ锛?*
1. 鍒濆鍖栧緱鍒嗙煩闃靛拰璺緞鐭╅樀
2. 閫掑綊濉厖鐭╅樀锛堝姩鎬佽鍒掞級
3. 鍥炴函鎵惧埌鏈€浼樻瘮瀵硅矾寰?
**寰楀垎鐭╅樀锛?*
$$F(i,j) = \max\begin{cases} F(i-1,j-1) + s(x_i, y_j) & \text{鍖归厤/閿欓厤} \\ F(i-1,j) + d & \text{鎻掑叆锛坓ap锛墋 \\ F(i,j-1) + d & \text{鍒犻櫎锛坓ap锛墋 \end{cases}$$

**鍙傛暟锛?*
- 鏇挎崲鐭╅樀锛歅AM銆丅LOSUM
- 绌轰綅缃氬垎锛坓ap penalty锛?
**Python瀹炵幇锛?*
```python
def needleman_wunsch(seq1, seq2, match=1, mismatch=-1, gap=-2):
    n, m = len(seq1), len(seq2)
    score = [[0]*(m+1) for _ in range(n+1)]
    
    # 鍒濆鍖?    for i in range(n+1):
        score[i][0] = i * gap
    for j in range(m+1):
        score[0][j] = j * gap
    
    # 濉厖鐭╅樀
    for i in range(1, n+1):
        for j in range(1, m+1):
            if seq1[i-1] == seq2[j-1]:
                diag = score[i-1][j-1] + match
            else:
                diag = score[i-1][j-1] + mismatch
            up = score[i-1][j] + gap
            left = score[i][j-1] + gap
            score[i][j] = max(diag, up, left)
    
    return score[n][m]
```

### 灞€閮ㄦ瘮瀵癸紙Smith-Waterman绠楁硶锛?
**鍘熺悊锛?*
- 瀵绘壘涓ゆ潯搴忓垪涓渶鐩镐技鐨勫眬閮ㄥ尯鍩?- 閫傜敤浜庨暱搴﹀樊寮傚ぇ鎴栧彧鏈夐儴鍒嗙浉浼肩殑搴忓垪

**涓庡叏灞€姣斿鐨勫尯鍒細**
- 鐭╅樀涓厑璁歌礋鍒嗗嚭鐜?- 鍥炴函浠庢渶楂樺垎寮€濮?- 鍦ㄩ亣鍒?鏃跺仠姝?
**寰楀垎鐭╅樀锛?*
$$F(i,j) = \max\begin{cases} 0 \\ F(i-1,j-1) + s(x_i, y_j) \\ F(i-1,j) + d \\ F(i,j-1) + d \end{cases}$$

**搴旂敤锛?*
- 瀵绘壘淇濆畧缁撴瀯鍩?- 妫€娴嬪眬閮ㄧ浉浼兼€?- 铔嬬櫧璐ㄥ姛鑳戒綅鐐硅瘑鍒?
## 澶氬簭鍒楁瘮瀵?
### ClustalW

**鍘熺悊锛?*
- 娓愯繘姣斿鏂规硶
- 鍏堟瀯寤哄紩瀵兼爲
- 鎸夌収杩涘寲鍏崇郴閫愭鍚堝苟姣斿

**姝ラ锛?*
1. 璁＄畻涓や袱璺濈鐭╅樀
2. 鏋勫缓寮曞鏍戯紙NJ娉曪級
3. 鎸夌収鏍戠殑椤哄簭娓愯繘姣斿
4. 浼樺寲姣斿缁撴灉

**鍙傛暟锛?*
- 鏇挎崲鐭╅樀閫夋嫨
- 绌轰綅寮€鏀惧拰寤朵几缃氬垎
- 寰幆杩唬娆℃暟

### MUSCLE

**鍘熺悊锛?*
- 澶氬簭鍒楁瘮瀵圭殑杩唬浼樺寲
- 缁撳悎澶氱姣斿绛栫暐

**鐗圭偣锛?*
- 閫熷害蹇簬ClustalW
- 鍑嗙‘鎬ц緝楂?- 鍙鐞嗗ぇ瑙勬ā鏁版嵁

**姝ラ锛?*
1. 鍒濆姣斿锛坘-mer璺濈锛?2. 鏋勫缓寮曞鏍?3. 娓愯繘姣斿
4. 杩唬浼樺寲锛堟渶澶?6杞級

### MAFFT

**鍘熺悊锛?*
- 鍩轰簬蹇€熷倕閲屽彾鍙樻崲
- 楂樻晥澶勭悊澶ц妯℃暟鎹?
**绠楁硶锛?*
- FFT-NS-1锛氬揩閫熸瘮瀵?- FFT-NS-2锛氫袱杞凯浠?- L-INS-i锛氳€冭檻灞€閮ㄧ粨鏋?- E-INS-i锛氳€冭檻澶氫釜绌轰綅

**浼樺娍锛?*
- 澶勭悊閫熷害蹇?- 鏀寔澶ц妯℃暟鎹?- 澶氱绠楁硶閫夋嫨

### 姣斿璐ㄩ噺璇勪及

**璇勪及鎸囨爣锛?*
- SP-SUM锛氭€婚厤瀵瑰緱鍒?- TC锛氫竴鑷存€у緱鍒?- 涓€鑷存€х櫨鍒嗘瘮

**鍙鍖栵細**
- Jalview
- BoxShade
- ESPript

## 姣斿璇勫垎绯荤粺

### 鏇挎崲鐭╅樀

**PAM鐭╅樀锛圥oint Accepted Mutation锛夛細**
- 鍩轰簬杩涘寲妯″瀷
- PAM250锛氶€傜敤浜?5%搴忓垪涓€鑷存€?- 鏁板€艰秺澶э紝杩涘寲璺濈瓒婅繙

**璁＄畻鏂规硶锛?*
1. 缁熻宸茬煡杩涘寲璺濈鐨勮泲鐧借川瀵?2. 璁＄畻姘ㄥ熀閰告浛鎹㈤鐜?3. 杞崲涓哄鏁板嚑鐜囧緱鍒?
**BLOSUM鐭╅樀锛圔LOcks SUbstitution Matrix锛夛細**
- 鍩轰簬淇濆畧鍖哄煙
- BLOSUM62锛氶€傜敤浜?0%搴忓垪涓€鑷存€?- 鏁板€艰秺澶э紝淇濆畧鎬ц秺楂?
**甯哥敤鐭╅樀锛?*
- BLOSUM45锛氳繙缂樺簭鍒?- BLOSUM62锛氶€氱敤锛堥粯璁わ級
- BLOSUM80锛氳繎缂樺簭鍒?
### 绌轰綅缃氬垎

**绾挎€х┖浣嶇綒鍒嗭細**
$$G(k) = -k \times d$$
鍏朵腑k涓虹┖浣嶉暱搴︼紝d涓虹綒鍒?
**浠垮皠绌轰綅缃氬垎锛?*
$$G(k) = -d - (k-1) \times e$$
鍏朵腑d涓虹┖浣嶅紑鏀剧綒鍒嗭紝e涓虹┖浣嶅欢浼哥綒鍒?
**鍙傛暟閫夋嫨锛?*
- 涓ユ牸姣斿锛氶珮缃氬垎
- 鏉惧紱姣斿锛氫綆缃氬垎
- 閫氬父d=10锛宔=1

## 闅愰┈灏斿彲澶ā鍨嬪湪姣斿涓殑搴旂敤

### HMM鍩烘湰鍘熺悊

**缁勬垚锛?*
- 闅愮姸鎬侊細姣斿浣嶇疆
- 瑙傛祴鐘舵€侊細姘ㄥ熀閰?纰卞熀
- 杞Щ姒傜巼锛氱姸鎬侀棿杞崲姒傜巼
- 鍙戝皠姒傜巼锛氬悇鐘舵€佷骇鐢熻娴嬬殑姒傜巼

**涓変釜鍩烘湰闂锛?*
1. 璇勪及闂锛氱粰瀹氭ā鍨嬪拰瑙傛祴搴忓垪锛岃绠楁鐜囷紙鍓嶅悜绠楁硶锛?2. 瑙ｇ爜闂锛氱粰瀹氭ā鍨嬪拰瑙傛祴搴忓垪锛屾壘鍒版渶鍙兘鐨勭姸鎬佸簭鍒楋紙Viterbi绠楁硶锛?3. 瀛︿範闂锛氱粰瀹氳娴嬪簭鍒楋紝浼拌妯″瀷鍙傛暟锛圔aum-Welch绠楁硶锛?
### Profile HMM

**缁撴瀯锛?*
- 鍖归厤鐘舵€侊紙M锛夛細淇濆畧浣嶇疆
- 鎻掑叆鐘舵€侊紙I锛夛細鍏佽鎻掑叆
- 缂哄け鐘舵€侊紙D锛夛細鍏佽缂哄け

**搴旂敤锛?*
- 搴忓垪瀹舵棌姣斿
- 闅愮浣嶇偣妫€娴?- 铔嬬櫧璐ㄥ鏃忓垎绫?
### HMMER

**鍔熻兘锛?*
- 搴忓垪鎼滅储锛坔mmscan锛?- 搴忓垪姣斿锛坔mmalign锛?- 鏁版嵁搴撴悳绱紙hmmsearch锛?
**浣跨敤锛?*
```bash
# 鏋勫缓HMM妯″瀷
hmmbuild alignment.afa seqs.afa

# 鎼滅储鏁版嵁搴?hmmsearch --domtblout results.txt model.hmm database.fa

# 姣斿搴忓垪
hmmalign model.hmm sequences.fa > aligned.afa
```

## 瀹為檯搴旂敤

### 鍩哄洜缁勬敞閲?
- 鍩哄洜璇嗗埆
- 澶栨樉瀛愰娴?- 璋冩帶鍏冧欢璇嗗埆

### 绯荤粺鍙戣偛鍒嗘瀽

- 搴忓垪姣斿浣滀负杈撳叆
- 鏋勫缓杩涘寲鏍?- 鎺ㄦ柇杩涘寲鍏崇郴

### 鍔熻兘棰勬祴

- 淇濆畧鍖哄煙璇嗗埆
- 鍔熻兘浣嶇偣棰勬祴
- 铔嬬櫧璐ㄧ浉浜掍綔鐢ㄩ娴?
### 鐤剧梾鐮旂┒

- 绐佸彉妫€娴?- 鐤剧梾鐩稿叧鍩哄洜璇嗗埆
- 鑽墿闈剁偣鍙戠幇

## 鍙傝€冭祫婧?
- Altschul SF, et al. *Gapped BLAST and PSI-BLAST*
- Thompson JD, et al. *CLUSTAL W: improving the sensitivity of progressive multiple sequence alignment*
- 銆婄敓鐗╀俊鎭銆嬭淳涓?- 銆婂簭鍒楁暟鎹殑缁熻鍒嗘瀽銆?

## 鐩稿叧鏉＄洰

ComputationalBiology, [[02_NaturalSciences/Biology/Genetics/INDEX|Genetics]], [[07_InterdisciplinarySciences/DataScience/INDEX|DataScience]], Genomics, [[02_NaturalSciences/Biology/MolecularBiology/INDEX|MolecularBiology]]
