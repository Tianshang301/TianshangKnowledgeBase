# 鐢熺墿缁熻瀛?
## 姒傝堪

鐢熺墿缁熻瀛︽槸灏嗙粺璁″鍘熺悊鍜屾柟娉曞簲鐢ㄤ簬鐢熺墿瀛﹀拰鍖诲鐮旂┒鐨勪氦鍙夊绉戙€傚畠涓哄疄楠岃璁°€佹暟鎹垎鏋愬拰绉戝鎺ㄦ柇鎻愪緵瀹氶噺宸ュ叿锛屾槸鐜颁唬鐢熷懡绉戝鐮旂┒涓嶅彲鎴栫己鐨勬柟娉曡鍩虹銆?
## 鐢熺墿缁熻瀛﹀熀纭€

### 鍋囪妫€楠?
鍋囪妫€楠屾槸鐢熺墿缁熻瀛︾殑鏍稿績鏂规硶涔嬩竴锛岀敤浜庡垽鏂瀵熷埌鐨勫樊寮傛槸鍚﹀叿鏈夌粺璁″鎰忎箟銆?
**鍩烘湰姝ラ锛?*
1. 寤虹珛鍘熷亣璁撅紙H鈧€锛夊拰澶囨嫨鍋囪锛圚鈧侊級
2. 閫夋嫨鏄捐憲鎬ф按骞筹紙伪锛夛紝閫氬父涓?.05
3. 璁＄畻妫€楠岀粺璁￠噺
4. 纭畾P鍊兼垨涓寸晫鍊?5. 鍋氬嚭缁熻鍐崇瓥

**甯哥敤妫€楠屾柟娉曪細**
- **t妫€楠?*锛氭瘮杈冧袱缁勫潎鍊煎樊寮傦紙鐙珛鏍锋湰t妫€楠屻€侀厤瀵箃妫€楠岋級
- **鏂瑰樊鍒嗘瀽锛圓NOVA锛?*锛氭瘮杈冨缁勫潎鍊煎樊寮?- **鍗℃柟妫€楠?*锛氭楠屽垎绫诲彉閲忛棿鐨勫叧鑱旀€?- **闈炲弬鏁版楠?*锛歐ilcoxon妫€楠屻€並ruskal-Wallis妫€楠岋紙鏁版嵁涓嶆弧瓒虫鎬佸垎甯冩椂浣跨敤锛?
**涓ょ被閿欒锛?*
- 绗竴绫婚敊璇紙伪閿欒锛夛細鎷掔粷浜嗘纭殑鍘熷亣璁撅紙鍋囬槼鎬э級
- 绗簩绫婚敊璇紙尾閿欒锛夛細鎺ュ彈浜嗛敊璇殑鍘熷亣璁撅紙鍋囬槾鎬э級
- 缁熻鍔熸晥锛?-尾锛夛細姝ｇ‘鎷掔粷閿欒鍘熷亣璁剧殑姒傜巼

### 甯哥敤妫€楠岀粺璁￠噺鍏紡

| 妫€楠屾柟娉?| 妫€楠岀粺璁￠噺 | 鍏紡 | 鐢ㄩ€?|
|---------|-----------|------|------|
| **鍗曟牱鏈?t 妫€楠?* | $t$ | $t = \dfrac{\bar{x} - \mu_0}{s/\sqrt{n}}$ | 鏍锋湰鍧囧€间笌宸茬煡鎬讳綋鍧囧€兼瘮杈?|
| **鐙珛鏍锋湰 t 妫€楠?* | $t$ | $t = \dfrac{\bar{x}_1 - \bar{x}_2}{s_p\sqrt{\frac{1}{n_1}+\frac{1}{n_2}}}$ | 涓ょ粍鐙珛鏍锋湰鍧囧€兼瘮杈?|
| **閰嶅 t 妫€楠?* | $t$ | $t = \dfrac{\bar{d}}{s_d/\sqrt{n}}$ | 閰嶅璁捐鏁版嵁宸€兼瘮杈?|
| **鍗曞洜绱?ANOVA** | $F$ | $F = \dfrac{MS_{\text{between}}}{MS_{\text{within}}}$ | 澶氱粍鍧囧€兼瘮杈?|
| **鍗℃柟妫€楠?* | $\chi^2$ | $\chi^2 = \sum \dfrac{(O_{ij} - E_{ij})^2}{E_{ij}}$ | 鍒嗙被鍙橀噺鍏宠仈鎬ф楠?|
| **F 妫€楠岋紙鏂瑰樊榻愭€э級** | $F$ | $F = \dfrac{s_1^2}{s_2^2}$ | 涓ょ粍鏂瑰樊鏄惁鐩哥瓑 |

### 鍗曞洜绱?ANOVA 鍒嗚В

| 鍙樺紓鏉ユ簮 | 骞虫柟鍜?(SS) | 鑷敱搴?(df) | 鍧囨柟 (MS) | F 鍊?|
|---------|------------|------------|-----------|------|
| **缁勯棿** | $SS_{\text{tr}} = \sum_{i=1}^{k} n_i(\bar{x}_i - \bar{\bar{x}})^2$ | $k-1$ | $MS_{\text{tr}} = \dfrac{SS_{\text{tr}}}{k-1}$ | $F = \dfrac{MS_{\text{tr}}}{MS_{\text{e}}}$ |
| **缁勫唴锛堣宸級** | $SS_{\text{e}} = \sum_{i=1}^{k}\sum_{j=1}^{n_i}(x_{ij} - \bar{x}_i)^2$ | $N - k$ | $MS_{\text{e}} = \dfrac{SS_{\text{e}}}{N-k}$ | |
| **鎬诲彉寮?* | $SS_{\text{tot}} = \sum_{i=1}^{k}\sum_{j=1}^{n_i}(x_{ij} - \bar{\bar{x}})^2$ | $N-1$ | | |

### 缃俊鍖洪棿

缃俊鍖洪棿鎻愪緵鍙傛暟浼拌鐨勪笉纭畾鎬ч噺鍖栥€?
**鍧囧€肩殑缃俊鍖洪棿锛?*
$$\bar{x} \pm t_{\alpha/2, df} \times \frac{s}{\sqrt{n}}$$

**姣斾緥鐨勭疆淇″尯闂达細**
$$\hat{p} \pm z_{\alpha/2} \times \sqrt{\frac{\hat{p}(1-\hat{p})}{n}}$$

**褰卞搷缃俊鍖洪棿瀹藉害鐨勫洜绱狅細**
- 鏍锋湰閲忥細鏍锋湰閲忚秺澶э紝鍖洪棿瓒婄獎
- 鍙樺紓绋嬪害锛氬彉寮傝秺澶э紝鍖洪棿瓒婂
- 缃俊姘村钩锛氱疆淇℃按骞宠秺楂橈紝鍖洪棿瓒婂

## 甯哥敤瀹為獙璁捐

### 瀹屽叏闅忔満璁捐

瀹屽叏闅忔満璁捐锛圕ompletely Randomized Design, CRD锛夋槸鏈€绠€鍗曠殑瀹為獙璁捐銆?
**鐗圭偣锛?*
- 璇曢獙鍗曚綅闅忔満鍒嗛厤鍒板悇澶勭悊缁?- 鍚勫鐞嗙粍鏍锋湰閲忓彲浠ョ浉绛夋垨涓嶇瓑
- 閫傜敤浜庡疄楠屾潯浠跺潎鍖€鐨勬儏鍐?
**缁熻妯″瀷锛?*
$$y_{ij} = \mu + \tau_i + \varepsilon_{ij}$$

鍏朵腑锛?y_{ij}$涓鸿娴嬪€硷紝$\mu$涓烘€讳綋鍧囧€硷紝$\tau_i$涓哄鐞嗘晥搴旓紝$\varepsilon_{ij}$涓洪殢鏈鸿宸€?
### 闅忔満鍖虹粍璁捐

闅忔満鍖虹粍璁捐锛圧andomized Block Design, RBD锛夐€氳繃鍖虹粍鎺у埗宸茬煡鍙樺紓鏉ユ簮銆?
**璁捐鍘熷垯锛?*
- 鍚屼竴鍖虹粍鍐呰瘯楠屽崟浣嶅敖鍙兘鐩镐技
- 鍖虹粍闂村厑璁稿瓨鍦ㄥ樊寮?- 姣忎釜鍖虹粍鍐呭悇澶勭悊闅忔満鎺掑垪

**浼樺娍锛?*
- 鍑忓皯璇樊鏂瑰樊锛屾彁楂樻楠屽姛鏁?- 鍙互鍒嗘瀽鍖虹粍鏁堝簲
- 閫傜敤浜庡疄楠屾潗鏂欏紓璐ㄦ€ц緝澶х殑鎯呭喌

### 鏋愬洜璁捐

鏋愬洜璁捐锛團actorial Design锛夊悓鏃剁爺绌跺涓洜绱犵殑鏁堝簲鍙婂叾浜や簰浣滅敤銆?
**璁捐绫诲瀷锛?*
- 2脳2鏋愬洜璁捐锛氫袱涓洜绱狅紝鍚勪袱涓按骞?- 3脳3鏋愬洜璁捐锛氫袱涓洜绱狅紝鍚勪笁涓按骞?- 澶氬洜绱犳瀽鍥犺璁★細涓変釜鍙婁互涓婂洜绱?
**鍙垎鏋愮殑鏁堝簲锛?*
- 涓绘晥搴旓紙Main Effect锛夛細鍚勫洜绱犵殑鐙珛鏁堝簲
- 浜や簰鏁堝簲锛圛nteraction Effect锛夛細鍥犵礌闂寸殑鑱斿悎鏁堝簲

**搴旂敤瀹炰緥锛?*
- 鑲ユ枡脳鍝佺脳瀵嗗害鐨勪笁鍥犵礌璇曢獙
- 鑽墿脳鍓傞噺脳缁欒嵂鏃堕棿鐨勪复搴婅瘯楠?
## 鐢熷瓨鍒嗘瀽

鐢熷瓨鍒嗘瀽鏄爺绌朵簨浠跺彂鐢熸椂闂存暟鎹殑缁熻鏂规硶銆?
### Kaplan-Meier鏇茬嚎

Kaplan-Meier鏇茬嚎锛堜箻绉瀬闄愭硶锛夋槸闈炲弬鏁版柟娉曪紝鐢ㄤ簬浼拌鐢熷瓨鍑芥暟銆?
**璁＄畻鍏紡锛?*
$$S(t) = \prod_{t_i \leq t} \left(1 - \frac{d_i}{n_i}\right)$$

鍏朵腑锛?d_i$涓烘椂闂?t_i$鐨勪簨浠舵暟锛?n_i$涓烘椂闂?t_i$鐨勯闄╀汉鏁般€?
**鐗圭偣锛?*
- 鍙互澶勭悊鍒犲け鏁版嵁
- 鎻愪緵鐢熷瓨姒傜巼鐨勯樁姊嚱鏁颁及璁?- 鍙粯鍒剁敓瀛樻洸绾胯繘琛岀粍闂存瘮杈?
### Cox鍥炲綊

Cox姣斾緥椋庨櫓妯″瀷鏄崐鍙傛暟鏂规硶锛岀敤浜庡垎鏋愬涓洜绱犲鐢熷瓨鏃堕棿鐨勫奖鍝嶃€?
**妯″瀷褰㈠紡锛?*
$$h(t|X) = h_0(t) \exp(\beta_1 X_1 + \beta_2 X_2 + \cdots + \beta_p X_p)$$

鍏朵腑锛?h_0(t)$涓哄熀鍑嗛闄╁嚱鏁帮紝$\beta_i$涓哄洖褰掔郴鏁帮紝$X_i$涓哄崗鍙橀噺銆?
**椋庨櫓姣旓紙HR锛夛細**
- HR > 1锛氶闄╁鍔?- HR = 1锛氭棤褰卞搷
- HR < 1锛氶闄╅檷浣?
**姣斾緥椋庨櫓鍋囪妫€楠岋細**
- Schoenfeld娈嬪樊妫€楠?- 瀵规暟璐熷鏁扮敓瀛樻洸绾垮浘
- 娈嬪樊闅忔椂闂村彉鍖栧浘

### 鍏朵粬鐢熷瓨鍒嗘瀽鏂规硶

- **Log-rank妫€楠?*锛氭瘮杈冧袱缁勬垨澶氱粍鐢熷瓨鏇茬嚎
- **鍔犻€熷け鏁堟椂闂存ā鍨嬶紙AFT锛?*锛氬弬鏁版柟娉?- **绔炰簤椋庨櫓妯″瀷**锛氬鐞嗗绉嶄簨浠剁被鍨?
## 涓村簥璇曢獙缁熻

### 涓村簥璇曢獙璁捐绫诲瀷

**鎸夎璁″垎绫伙細**
- 骞宠璁捐锛氬鐓х粍鍜屽鐞嗙粍鍚屾椂杩涜
- 浜ゅ弶璁捐锛氬彈璇曡€呭厛鍚庢帴鍙椾笉鍚屽鐞?- 鏋愬洜璁捐锛氬悓鏃惰瘎浠峰涓共棰勬帾鏂?
**鎸夌洸娉曞垎绫伙細**
- 鍗曠洸锛氫粎鍙楄瘯鑰呬笉鐭ラ亾鍒嗙粍
- 鍙岀洸锛氬彈璇曡€呭拰鐮旂┒鑰呴兘涓嶇煡閬撳垎缁?- 涓夌洸锛氬彈璇曡€呫€佺爺绌惰€呭拰鏁版嵁鍒嗘瀽鑰呴兘涓嶇煡閬撳垎缁?
### 鏍锋湰閲忚绠?
**鍧囧€兼瘮杈冪殑鏍锋湰閲忥細**
$$n = \frac{(Z_{\alpha/2} + Z_{\beta})^2 \times 2\sigma^2}{\delta^2}$$

**姣斾緥姣旇緝鐨勬牱鏈噺锛?*
$$n = \frac{(Z_{\alpha/2} + Z_{\beta})^2 \times [p_1(1-p_1) + p_2(1-p_2)]}{(p_1 - p_2)^2}$$

### 閫傚簲鎬ц璁?
- 鏍锋湰閲忛噸浼?- 鍓傞噺鎺㈢储
- 鏃犵紳璁捐锛圛I/III鏈熸棤缂濓級
- 瀵岄泦璁捐

## R璇█瀹炵幇

### 鍩虹缁熻鍒嗘瀽

```r
# 鎻忚堪缁熻
summary(data)
sd(data$variable)
var(data$variable)

# t妫€楠?t.test(group1, group2, var.equal = TRUE)

# 鏂瑰樊鍒嗘瀽
anova_model <- aov(response ~ factor1 * factor2, data = data)
summary(anova_model)

# 鍗℃柟妫€楠?chisq.test(table(data$var1, data$var2))
```

### 鐢熷瓨鍒嗘瀽

```r
library(survival)
library(survminer)

# 鍒涘缓鐢熷瓨瀵硅薄
surv_obj <- Surv(time = data$time, event = data$status)

# Kaplan-Meier浼拌
km_fit <- survfit(surv_obj ~ group, data = data)
ggsurvplot(km_fit, data = data, pval = TRUE)

# Cox鍥炲綊
cox_model <- coxph(Surv(time, status) ~ age + sex + treatment, data = data)
summary(cox_model)

# 姣斾緥椋庨櫓鍋囪妫€楠?cox.zph(cox_model)
```

### 鏍锋湰閲忚绠?
```r
library(pwr)

# t妫€楠屾牱鏈噺
pwr.t.test(n = NULL, d = 0.5, sig.level = 0.05, power = 0.8, 
           type = "two.sample")

# 鏂瑰樊鍒嗘瀽鏍锋湰閲?pwr.anova.test(k = 3, f = 0.25, sig.level = 0.05, power = 0.8)

# 鐩稿叧鍒嗘瀽鏍锋湰閲?pwr.r.test(n = NULL, r = 0.3, sig.level = 0.05, power = 0.8)
```

## 鍙傝€冭祫婧?
- Zar JH. *Biostatistical Analysis* (5th ed.)
- Rosner B. *Fundamentals of Biostatistics*
- Kleinbaum DG, Klein M. *Survival Analysis: A Self-Learning Text*
- R Core Team. *R: A Language and Environment for Statistical Computing*

## 鐩稿叧鏉＄洰

[[Probability]], [[07_InterdisciplinarySciences/DataScience/INDEX|DataScience]], [[05_ComputerScience/ArtificialIntelligence/MachineLearning/INDEX|MachineLearning]], StatisticalModeling
