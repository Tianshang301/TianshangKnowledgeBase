# 鐢靛瓙涔﹁祫婧愪笌绠＄悊鎸囧崡

## 涓€銆佺數瀛愪功鏍煎紡

### 1.1 涓绘祦鏍煎紡瀵规瘮

| 鏍煎紡 | 鍏ㄧО | 寮€鍙戣€?| 鐗堝紡 | DRM 鏀寔 | 閫傜敤骞冲彴 |
|------|------|--------|:----:|:--------:|---------|
| EPUB | Electronic Publication | IDPF | 閲嶆帓 | Adobe ADEPT | 閫氱敤锛堥櫎 Kindle锛?|
| MOBI | Mobipocket | Amazon | 閲嶆帓 | Kindle DRM | Kindle 鏃ц澶?|
| AZW3 | Kindle Format 8 | Amazon | 閲嶆帓 | Kindle DRM | Kindle 鏂拌澶?|
| PDF | Portable Document Format | Adobe | 鍥哄畾 | 澶氱 | 閫氱敤 |
| DJVU | DjVu | AT&T | 鍥哄畾 | 鏋佸皯 | 鎵弿鐗堝浘涔?|

**鐗圭偣璇﹁В**锛?
- **EPUB**锛氬紑鏀炬爣鍑嗭紙ISO 24698锛夛紝鍩轰簬 XHTML + CSS锛屾敮鎸佽嚜閫傚簲鎺掔増锛屾槸鐩墠鏈€骞挎硾鏀寔鐨勬牸寮?- **AZW3/KF8**锛欰mazon 涓撴湁鏍煎紡锛屾敮鎸?HTML5 + CSS3锛孠indle 璁惧鐨勬渶浣抽€夋嫨
- **PDF**锛氬浐瀹氶〉闈㈢殑鎺掔増淇濈湡搴﹂珮锛屼絾灏忓睆骞曢槄璇讳綋楠屽樊锛岄€傚悎 A4 瀛︽湳璁烘枃
- **DJVU**锛氫笓闂ㄩ拡瀵规壂鎻忔枃妗ｄ紭鍖栫殑鏍煎紡锛屽帇缂╃巼绾︿负 JPEG 鐨?5鈥?0 鍊?
### 1.2 鏍煎紡杞崲

$$ \text{Source} \xrightarrow{\text{Pandoc/Calibre}} \text{Target} $$

| 杞崲宸ュ叿 | 鏀寔鐨勬牸寮?| 鐗圭偣 |
|---------|-----------|------|
| Pandoc | 30+ 鏍煎紡 | 鍛戒护琛屻€佺簿纭帶鍒躲€佸鏈閫?|
| Calibre | 20+ 鏍煎紡 | GUI + 鍛戒护琛屻€佹壒閲忚浆鎹€佸厓鏁版嵁绠＄悊 |
| Kindle Previewer | MOBI/AZW3 | Amazon 瀹樻柟銆佹ā鎷?Kindle 璁惧 |
| Online Convert | 澶氭牸寮?| 娴忚鍣ㄦ搷浣溿€佹棤闇€瀹夎 |

## 浜屻€佺數瀛愪功鍒涘缓娴佺▼

### 2.1 鍐欎綔涓庤浆鎹?
**鎺ㄨ崘宸ヤ綔娴?*锛?
```
Markdown/LaTeX 婧愭枃浠?        鈫? Pandoc
     EPUB/PDF
        鈫? Calibre
     MOBI/AZW3
```

```markdown
% 浣跨敤 Pandoc 灏?Markdown 杞崲涓?EPUB
pandoc book.md -o book.epub --metadata title="涔﹀悕" --metadata author="浣滆€?
```

### 2.2 鍏冩暟鎹鐞?
EPUB 鍏冩暟鎹娇鐢?OPF 鏂囦欢瀹氫箟锛屽叧閿瓧娈碉細

| 瀛楁 | 鎻忚堪 | Dublin Core 鏄犲皠 |
|------|------|-----------------|
| title | 涔﹀悕 | dc:title |
| creator | 浣滆€?| dc:creator |
| publisher | 鍑虹増绀?| dc:publisher |
| identifier | 鍞竴鏍囪瘑锛圛SBN/DOI锛?| dc:identifier |
| language | 璇█浠ｇ爜锛坺h, en锛?| dc:language |
| date | 鍑虹増鏃ユ湡 | dc:date |
| subject | 鍒嗙被涓婚 | dc:subject |
| rights | 鐗堟潈澹版槑 | dc:rights |

### 2.3 CSS 鏍煎紡鍖?
```css
/* EPUB 鏍峰紡绀轰緥 */
body {
  font-family: "Noto Serif", "Source Han Serif", serif;
  line-height: 1.8;
  margin: 5%;
}
h1 { text-align: center; font-size: 1.6em; }
h2 { font-size: 1.3em; margin-top: 1.5em; }
p { text-indent: 2em; }
img { max-width: 100%; height: auto; }
```

## 涓夈€侀槄璇昏澶囦笌杞欢

### 3.1 纭欢璁惧

| 璁惧 | 灞忓箷鎶€鏈?| 灞忓箷灏哄 | 浼樼偣 | 缂虹偣 |
|------|---------|:--------:|------|------|
| Kindle | E-ink | 6"鈥?0" | 鎶ょ溂銆佺画鑸暱 | 鏍煎紡灏侀棴 |
| Kobo | E-ink | 6"鈥?" | EPUB 鍘熺敓銆佸紑鏀?| 涓枃鐢熸€佸急 |
| Remarkable | E-ink | 10.3" | 鎵嬪啓绗旇 | 浠锋牸楂?|
| iPad | LCD/OLED | 8"鈥?3" | 褰╄壊銆丄pp 涓板瘜 | 浼ょ溂銆侀噸 |
| 鏂囩煶 Boox | E-ink | 6"鈥?3.3" | Android 寮€鏀?| 浠锋牸楂?|

### 3.2 闃呰杞欢

| 杞欢 | 骞冲彴 | 鐗硅壊鍔熻兘 |
|------|------|---------|
| Kindle App | iOS/Android/PC | Whispersync 鍚屾 |
| Google Play Books | iOS/Android/Web | 浜戝瓨鍌ㄣ€丳DF 涓婁紶 |
| Apple Books | iOS/macOS | 缇庤銆乮Cloud 鍚屾 |
| Adobe Digital Editions | PC | EPUB/PDF + ADEPT DRM |
| 寰俊璇讳功 | iOS/Android | 绀句氦闃呰銆佷腑鏂囩敓鎬?|
| Marvin 3 | iOS | 鑷畾涔夊己銆佺粺璁″姛鑳?|
| Moon+ Reader | Android | TTS銆佹墜鍔裤€佹牸寮忔敮鎸佸箍 |

## 鍥涖€佹暟瀛楃増鏉冪鐞嗭紙DRM锛?
### 4.1 DRM 鏂规瀵规瘮

| DRM 鏂规 | 鎻愪緵鍟?| 鍔犲瘑鏂规硶 | 璁惧闄愬埗 |
|---------|--------|---------|:--------:|
| Kindle DRM | Amazon | 涓撴湁鍔犲瘑 | 6 鍙拌澶?|
| Adobe ADEPT | Adobe | AES-256 | 6 鍙拌澶?|
| Apple FairPlay | Apple | 涓撴湁鍔犲瘑 | 鐢熸€佸唴 |
| Marlin DRM | Marlin Trust | 寮€鏀炬爣鍑?| 鐏垫椿 |
| LCP | Readium | AES-256 | 鐏垫椿 |

### 4.2 DRM 鐨勫埄寮?
| 缁村害 | 鏀寔 DRM | 鏃?DRM |
|------|---------|--------|
| 鐗堟潈淇濇姢 | 寮?| 鏃?|
| 鐢ㄦ埛渚垮埄鎬?| 鍙楅檺 | 鑷敱浣跨敤 |
| 鏍煎紡杞崲 | 涓嶅厑璁?| 鍏佽 |
| 璺ㄥ钩鍙板叡浜?| 鍙楅檺 | 鑷敱 |
| 闀挎湡淇濆瓨 | 鍗遍櫓锛堟湇鍔″櫒鍏抽棴锛?| 瀹夊叏 |

## 浜斻€佸紑鏀捐幏鍙栫數瀛愪功

### 5.1 涓昏璧勬簮

| 璧勬簮搴?| 瑙勬ā | 鍐呭绫诲瀷 | 璁块棶鏂瑰紡 |
|--------|:----:|---------|---------|
| Project Gutenberg | 70,000+ | 鍏増鏂囧浣滃搧 | 鍏嶈垂涓嬭浇 |
| Internet Archive | 10,000,000+ | 涔︾睄/闊抽/瑙嗛 | 鍊熼槄+涓嬭浇 |
| Open Library | 1,000,000+ | 鐜颁唬涔︾睄 | 鍊熼槄 |
| OAPEN | 20,000+ | 瀛︽湳寮€鏀惧浘涔?| 鍏嶈垂闃呰 |
| DOAB | 50,000+ | 鍚岃璇勫瀛︽湳鍥句功 | 鍏嶈垂涓嬭浇 |
| 鍥藉澶у笀 | 100,000+ | 涓浗鍙ょ睄 | 鍦ㄧ嚎闃呰 |

### 5.2 Project Gutenberg 浣跨敤

Distributed Proofreaders 蹇楁効鑰呭崗浣滃钩鍙帮紝鍥句功缁忚繃 OCR 鈫?鏍″ 鈫?鏍煎紡鍖?鈫?鍙戝竷娴佺▼銆傛敮鎸?EPUB銆並indle銆丠TML銆佺函鏂囨湰鏍煎紡銆?
## 鍏€佺數瀛愪功鍙戣

### 6.1 鑷嚭鐗堝钩鍙板姣?
| 骞冲彴 | 鍒嗘垚妯″紡 | 鐙瑕佹眰 | 鏍煎紡瑕佹眰 | DRM 閫夐」 |
|------|---------|:--------:|---------|:--------:|
| Amazon KDP | 35%鈥?0% | KDP Select | MOBI/EPUB | 鍙€?|
| Google Play Books | 52%鈥?0% | 鏃?| EPUB/PDF | 鍙€?|
| Apple Books | 70% | 鏃?| EPUB | 鍙€?|
| Smashwords | 60%鈥?0% | 鏃?| EPUB锛堥€氳繃 Meatgrinder锛?| 鍙€?|
| 璞嗙摚闃呰 | 50%鈥?0% | 鏃?| EPUB | 鏃?|

### 6.2 鑷嚭鐗?vs 浼犵粺鍑虹増

| 缁村害 | 鑷嚭鐗?| 浼犵粺鍑虹増 |
|------|--------|---------|
| 鎺у埗鏉?| 瀹屽叏鑷富 | 鍑虹増绀句富瀵?|
| 鍛ㄦ湡 | 鏁板ぉ鈥撴暟鍛?| 6 涓湀鈥? 骞?|
| 缂栬緫鏀寔 | 鑷垂/澶栧寘 | 涓撲笟缂栬緫 |
| 鍙戣娓犻亾 | 鏈夐檺 | 鍏ㄩ潰 |
| 鐗堢◣鐜?| 35%鈥?0% | 5%鈥?5% |
| 鍓嶆湡鎶曞叆 | 缂栨牎/灏侀潰璁捐 | 鏃?|
| 鍝佺墝鑳屼功 | 鏃?| 鏈?|

## 涓冦€佸鏈數瀛愪功

| 骞冲彴 | 瀛︾瑕嗙洊 | 璁块棶妯″紡 | 鐗圭偣 |
|------|---------|---------|------|
| SpringerLink | STEM | 鏈烘瀯璁㈤槄/璐拱 | Lecture Notes 绯诲垪 |
| Cambridge Core | 鍏ㄥ绉?| 鏈烘瀯璁㈤槄 | 鍓戞ˉ澶у鍑虹増绀?|
| Oxford Scholarship Online | 浜烘枃绀剧 | 鏈烘瀯璁㈤槄 | 涓撻鍚堥泦 |
| JSTOR | 浜烘枃绀剧 | 鏈烘瀯璁㈤槄 | 杩囧垔 + 鐢靛瓙涔?|
| 涓浗鐭ョ綉锛圕NKI锛?| 鍏ㄥ绉?| 鎸夐〉浠樿垂 | 涓枃纭曞崥璁烘枃 |
| 璇荤 | 鍏ㄥ绉?| 鏈烘瀯璁㈤槄 | 涓枃鍥句功鎼滅储 |

## 鍏€佺數瀛愪功搴撶鐞?
### 8.1 Calibre 绠＄悊

Calibre 鏄紑婧愮殑鐢靛瓙涔︾鐞嗙憺澹啗鍒€锛?
| 鍔熻兘 | 鎻忚堪 |
|------|------|
| 鏍煎紡杞崲 | 鏀寔 20+ 鏍煎紡浜掕浆 |
| 鍏冩暟鎹紪杈?| 鑷姩鎶撳彇璞嗙摚/Amazon/Google 淇℃伅 |
| 鏍囩绠＄悊 | 鑷畾涔夋爣绛?鍒嗙被 |
| 鍐呭鏈嶅姟鍣?| 灞€鍩熺綉鏃犵嚎璁块棶 |
| 鏂伴椈涓嬭浇 | 鑷姩鎶撳彇 RSS 杞崲涓虹數瀛愪功 |
| 鎵归噺鎿嶄綔 | 鎵归噺杞崲/缂栬緫/閲嶅懡鍚?|

### 8.2 鍏冩暟鎹紪杈戝缓璁?
- 缁熶竴涔﹀悕鍜屼綔鑰呮牸寮忥紙濮? 鍚嶏級
- 娣诲姞鏍囩锛歚#缂栫▼`, `#Python`, `#鏁版嵁绉戝`
- 濉啓 ISBN 渚夸簬妫€绱?- 娣诲姞灏侀潰鍥惧儚锛堢粺涓€灏哄锛?- 璁剧疆璇█鏍囩锛坺h, en, ja锛?
## 涔濄€佹棤闅滅璁块棶

| 鏃犻殰纰嶇壒鎬?| 璇存槑 | EPUB3 鏀寔 |
|-----------|------|:----------:|
| 灞忓箷闃呰鍣ㄥ吋瀹?| NVDA, VoiceOver, TalkBack | 鉁?|
| 鏂囧瓧閲嶆帓 | 鑷畾涔夊瓧浣?澶у皬/闂磋窛 | 鉁?|
| 楂樺姣斿害妯″紡 | 閫傚簲瑙嗗姏闅滅 | 鉁?|
| 鏇夸唬鏂囨湰锛圓lt Text锛?| 鍥惧儚鎻忚堪 | 鉁?|
| 濯掍綋鏇夸唬 | 闊抽鎻忚堪瑙嗛 | 鉁?|
| 椤甸潰瀵艰埅 | 鏍囬/涔︾/椤电爜 | 鉁?|
| 璇煶鍚堟垚锛圱TS锛?| 鏂囨湰鏈楄 | 鉁?|

WCAG 2.1 AA 鏄數瀛愪功鏃犻殰纰嶇殑鍩烘湰鏍囧噯锛孍PUB3 瀵硅鏍囧噯鎻愪緵浜嗚壇濂芥敮鎸併€?
## 鍙傝€冭祫婧?
- 涓浗鐨功缃? (2024). *鏁板瓧鍑虹増浜т笟骞村害鎶ュ憡*.
- Project Gutenberg: https://www.gutenberg.org
- Calibre 瀹樻柟: https://calibre-ebook.com
- Pandoc 鏂囨。: https://pandoc.org/MANUAL.html
- IDPF EPUB 瑙勮寖: https://www.w3.org/publishing/epub3
- Open Access Publishing in European Networks: https://www.oapen.org

## 鐩稿叧鏉＄洰

DigitalLibrary, [[NoteTaking]], [[KnowledgeManagement]], EPUB
