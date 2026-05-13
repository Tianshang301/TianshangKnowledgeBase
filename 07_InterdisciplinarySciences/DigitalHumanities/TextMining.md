# 鏂囨湰鎸栨帢锛堟暟瀛椾汉鏂囷級

## 姒傝堪

鏂囨湰鎸栨帢鏄埄鐢ㄨ嚜鐒惰瑷€澶勭悊鍜屾満鍣ㄥ涔犳妧鏈粠澶ч噺鏂囨湰涓彁鍙栨湁浠峰€间俊鎭殑鏂规硶銆傚湪鏁板瓧浜烘枃棰嗗煙锛屾枃鏈寲鎺樹负鍘嗗彶鏂囩尞鐮旂┒銆佹枃瀛﹀垎鏋愩€佹枃鍖栭仐浜т繚鎶ょ瓑鎻愪緵浜嗘柊鐨勭爺绌惰寖寮忋€?
## 鏂囨湰棰勫鐞?
### 涓枃鍒嗚瘝

**鍒嗚瘝鏂规硶锛?*
- 鍩轰簬璇嶅吀锛氭渶澶у尮閰嶆硶銆侀€嗗悜鏈€澶у尮閰?- 鍩轰簬缁熻锛氶殣椹皵鍙か妯″瀷銆佹潯浠堕殢鏈哄満
- 鍩轰簬娣卞害瀛︿範锛欱iLSTM-CRF銆丅ERT

**甯哥敤宸ュ叿锛?*
- jieba锛歅ython涓枃鍒嗚瘝
- HanLP锛氬璇█NLP宸ュ叿
- pkuseg锛氬寳浜ぇ瀛﹀垎璇?
```python
import jieba

# 绮剧‘妯″紡
text = "鏁板瓧浜烘枃鏄法瀛︾鐨勭爺绌堕鍩?
words = jieba.lcut(text)

# 娣诲姞鑷畾涔夎瘝鍏?jieba.add_word("鏁板瓧浜烘枃")
```

### 鍘婚櫎鍋滅敤璇?
**鍋滅敤璇嶇被鍨嬶細**
- 璇皵璇嶏細鍟娿€佸憿銆佸悧
- 杩炶瘝锛氬拰銆佷笌銆佸強
- 浠嬭瘝锛氬湪銆佷粠銆佸悜
- 浠ｈ瘝锛氳繖銆侀偅銆佷粬

**鍋滅敤璇嶈〃锛?*
- 鍝堝伐澶у仠鐢ㄨ瘝琛?- 鐧惧害鍋滅敤璇嶈〃
- 鑷畾涔夊仠鐢ㄨ瘝琛?
```python
def remove_stopwords(words, stopwords):
    return [w for w in words if w not in stopwords and len(w) > 1]
```

### 璇嶆€ф爣娉?
**鏍囨敞闆嗭細**
- 鍚嶈瘝锛坣锛夈€佸姩璇嶏紙v锛夈€佸舰瀹硅瘝锛坅锛?- 鍓瘝锛坉锛夈€佷粙璇嶏紙p锛夈€佽繛璇嶏紙c锛?
**宸ュ叿锛?*
- jieba.posseg
- HanLP璇嶆€ф爣娉?- LTP璇嶆€ф爣娉?
## 璇嶉鍒嗘瀽

### 璇嶉缁熻

**鍩烘湰缁熻锛?*
- 璇嶉鍒楄〃
- 璇嶉鍒嗗竷
- TF-IDF鏉冮噸

**TF-IDF璁＄畻锛?*
$$TF-IDF(t,d) = TF(t,d) \times IDF(t)$$

$$IDF(t) = \log\frac{N}{DF(t)}$$

### 璇嶄簯

**鍒朵綔宸ュ叿锛?*
- WordCloud锛圥ython锛?- 寰瘝浜?- 鍥炬偊

**璁捐瑕佺偣锛?*
- 璇嶉鏄犲皠鍒板ぇ灏?- 棰滆壊閫夋嫨
- 褰㈢姸璁捐

```python
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# 鐢熸垚璇嶄簯
wc = WordCloud(font_path='simhei.ttf', 
               width=800, height=400,
               max_words=200)
wc.generate(text)

# 鏄剧ず璇嶄簯
plt.imshow(wc)
plt.axis('off')
plt.show()
```

### 璇嶉鍒嗘瀽搴旂敤

**鏂囩尞璁￠噺锛?*
- 鐮旂┒鐑偣鍒嗘瀽
- 瀛︾鍙戝睍瓒嬪娍
- 浣滆€呭叧閿瘝鍒嗘瀽

**鍘嗗彶鏂囩尞锛?*
- 鍘嗗彶鏈婕斿彉
- 姒傚康鍙茬爺绌?- 鏂囨湰椋庢牸鍒嗘瀽

## 涓婚妯″瀷

### LDA锛圠atent Dirichlet Allocation锛?
**鍩烘湰鍘熺悊锛?*
- 鏂囨。-涓婚-璇嶄笁灞傜粨鏋?- 姣忎釜鏂囨。鏄富棰樼殑娣峰悎
- 姣忎釜涓婚鏄瘝鐨勫垎甯?
**姒傜巼妯″瀷锛?*
$$P(w|d) = \sum_{k=1}^{K}P(w|z=k)P(z=k|d)$$

**鍙傛暟浼拌锛?*
- 鍙樺垎鎺ㄦ柇
- Gibbs閲囨牱
- 鍦ㄧ嚎瀛︿範

### LDA搴旂敤

**鍙傛暟璁剧疆锛?*
- 涓婚鏁癒锛氬洶鎯戝害銆佷竴鑷存€?- 瓒呭弬鏁帮細伪锛堟枃妗?涓婚锛夈€佄诧紙涓婚-璇嶏級

**缁撴灉瑙ｉ噴锛?*
- 涓婚璇嶅垪琛?- 鏂囨。-涓婚鍒嗗竷
- 涓婚鍙鍖?
```python
from gensim import corpora, models

# 鍒涘缓璇嶅吀鍜岃鏂欏簱
dictionary = corpora.Dictionary(texts)
corpus = [dictionary.doc2bow(text) for text in texts]

# 璁粌LDA妯″瀷
lda = models.LdaModel(corpus, num_topics=5, 
                       id2word=dictionary,
                       passes=15)

# 杈撳嚭涓婚
for topic in lda.print_topics():
    print(topic)
```

### 鍏朵粬涓婚妯″瀷

- **NMF**锛氶潪璐熺煩闃靛垎瑙?- **pLSA**锛氭鐜囨綔鍦ㄨ涔夊垎鏋?- **鍔ㄦ€佷富棰樻ā鍨?*锛氭椂搴忎富棰樻紨鍖?- **灞傛涓婚妯″瀷**锛氫富棰樺眰娆＄粨鏋?
## 鎯呮劅鍒嗘瀽

### 鎯呮劅璇嶅吀鏂规硶

**璇嶅吀鏋勫缓锛?*
- 鐭ョ綉HowNet鎯呮劅璇嶅吀
- 鍙版咕澶уNTUSD
- 澶ц繛鐞嗗伐澶у鎯呮劅璇嶆眹鏈綋

**鎯呮劅璁＄畻锛?*
$$Sentiment = \sum_{i=1}^{n}w_i \times score(word_i)$$

### 鏈哄櫒瀛︿範鏂规硶

**鐗瑰緛宸ョ▼锛?*
- 璇嶈妯″瀷
- TF-IDF
- 璇嶅祵鍏?
**甯哥敤绠楁硶锛?*
- 鏈寸礌璐濆彾鏂?- SVM
- 闅忔満妫灄
- 娣卞害瀛︿範锛圠STM銆丅ERT锛?
```python
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB

# 鐗瑰緛鎻愬彇
vectorizer = TfidfVectorizer()
X_train = vectorizer.fit_transform(train_texts)

# 璁粌妯″瀷
clf = MultinomialNB()
clf.fit(X_train, train_labels)

# 棰勬祴
X_test = vectorizer.transform(test_texts)
predictions = clf.predict(X_test)
```

### 娣卞害瀛︿範鎯呮劅鍒嗘瀽

**BERT寰皟锛?*
```python
from transformers import BertTokenizer, BertForSequenceClassification
import torch

# 鍔犺浇妯″瀷
tokenizer = BertTokenizer.from_pretrained('bert-base-chinese')
model = BertForSequenceClassification.from_pretrained('bert-base-chinese')

# 缂栫爜
inputs = tokenizer(text, return_tensors='pt', padding=True, truncation=True)
outputs = model(**inputs)
```

## 鍛藉悕瀹炰綋璇嗗埆锛圢ER锛?
### 瀹氫箟

璇嗗埆鏂囨湰涓殑浜哄悕銆佸湴鍚嶃€佹満鏋勫悕銆佹椂闂寸瓑瀹炰綋銆?
### 鏍囨敞浣撶郴

**BIO鏍囨敞锛?*
- B锛氬疄浣撳紑濮?- I锛氬疄浣撳唴閮?- O锛氶潪瀹炰綋

**绀轰緥锛?*
```
鍖椾含/nr 鏄?v 涓浗/ns 鐨?uj 棣栭兘/n
```

### NER鏂规硶

**鍩轰簬瑙勫垯锛?*
- 姝ｅ垯琛ㄨ揪寮?- 璇嶅吀鍖归厤
- 妯℃澘鍖归厤

**鍩轰簬缁熻锛?*
- HMM
- CRF
- BiLSTM-CRF

**鍩轰簬棰勮缁冩ā鍨嬶細**
- BERT-NER
- RoBERTa-NER

```python
from transformers import BertTokenizer, TokenClassificationPipeline

# 鍔犺浇NER妯″瀷
tokenizer = BertTokenizer.from_pretrained('bert-base-chinese')
pipeline = TokenClassificationPipeline(model=model, tokenizer=tokenizer)

# 璇嗗埆瀹炰綋
result = pipeline("鍖椾含澶у鏄腑鍥借憲鍚嶉珮绛夊搴?)
```

## 鏂囨湰鎸栨帢鍦ㄥ巻鍙叉枃鐚腑鐨勫簲鐢?
### 鍘嗗彶鏂囩尞鏁板瓧鍖?
**OCR鎶€鏈細**
- 鍙ょ睄鏂囧瓧璇嗗埆
- 鎵嬪啓浣撹瘑鍒?- 澶氬瓧浣撳鐞?
**鏁板瓧鍖栧伐鍏凤細**
- Tesseract OCR
- 鐧惧害OCR
- ABBYY FineReader

### 鍘嗗彶鏂囨湰鍒嗘瀽

**浜虹墿鍏崇郴缃戠粶锛?*
- 浜哄悕璇嗗埆
- 鍏崇郴鎶藉彇
- 绀句細缃戠粶鍒嗘瀽

**鍘嗗彶浜嬩欢鍒嗘瀽锛?*
- 浜嬩欢鎶藉彇
- 鏃堕棿绾挎瀯寤?- 鍥犳灉鍏崇郴鍒嗘瀽

**鎬濇兂鍙茬爺绌讹細**
- 姒傚康婕斿彉
- 鎬濇疆鍒嗘瀽
- 褰卞搷鍔涜瘎浼?
### 妗堜緥鐮旂┒

**銆婄孩妤兼ⅵ銆嬫枃鏈垎鏋愶細**
- 浜虹墿璇嶉
- 鎯呮劅鍒嗘瀽
- 椋庢牸鍒嗘瀽

**銆婂彶璁般€嬬爺绌讹細**
- 浜虹墿鍏崇郴缃戠粶
- 鏃堕棿鍒嗗竷
- 鍦扮悊鍒嗗竷

### 宸ュ叿骞冲彴

- **MARKUS**锛氬巻鍙叉枃鐚爣娉?- **DocuSky**锛氬彴婀炬暟浣嶄汉鏂?- **CBDB**锛氫腑鍥藉巻浠ｄ汉鐗╀紶璁版暟鎹簱
- **CTEXT**锛氫腑鍥藉摬瀛︿功鐢靛瓙鍖栬鍒?
## 鍙傝€冭祫婧?
- 銆婃暟瀛椾汉鏂囧璁恒€?- 銆婃枃鏈寲鎺樹笌鍒嗘瀽銆?- 銆奝ython鑷劧璇█澶勭悊銆?- 銆婃暟瀛椾汉鏂囩爺绌躲€嬫湡鍒?

## 鐩稿叧鏉＄洰

[[ComputationalLinguistics]], [[07_InterdisciplinarySciences/DataScience/INDEX|DataScience]], [[TextMining]], [[CulturalAnalytics]]
