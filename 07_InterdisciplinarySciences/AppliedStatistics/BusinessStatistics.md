# 鍟嗕笟缁熻

## 姒傝堪

鍟嗕笟缁熻鏄粺璁″鍦ㄥ晢涓氬喅绛栦腑鐨勫簲鐢紝娑电洊鏁版嵁鏀堕泦銆佸垎鏋愬拰瑙ｉ噴锛屽府鍔╃鐞嗚€呭熀浜庤瘉鎹仛鍑虹瀛﹀喅绛栥€傚畠铻嶅悎鎻忚堪缁熻銆佹帹鏂粺璁″拰棰勬祴鍒嗘瀽锛屾槸鐜颁唬鍟嗕笟鏅鸿兘鐨勬牳蹇冨伐鍏枫€?
## 鎻忚堪缁熻

### 闆嗕腑瓒嬪娍搴﹂噺

**鍧囧€硷紙Mean锛夛細**
$$\bar{x} = \frac{1}{n}\sum_{i=1}^{n}x_i$$

- 浼樼偣锛氬埄鐢ㄦ墍鏈夋暟鎹俊鎭?- 缂虹偣锛氬彈鏋佺鍊煎奖鍝嶅ぇ

**涓綅鏁帮紙Median锛夛細**
- 灏嗘暟鎹粠灏忓埌澶ф帓鍒楀悗浣嶄簬涓棿鐨勫€?- 瀵瑰紓甯稿€肩ǔ鍋?- 閫傜敤浜庡亸鎬佸垎甯冩暟鎹?
**浼楁暟锛圡ode锛夛細**
- 鍑虹幇棰戠巼鏈€楂樼殑鍊?- 閫傜敤浜庡垎绫绘暟鎹?- 鍙兘瀛樺湪澶氫釜浼楁暟

### 绂绘暎绋嬪害搴﹂噺

**鏍囧噯宸紙Standard Deviation锛夛細**
$$s = \sqrt{\frac{1}{n-1}\sum_{i=1}^{n}(x_i - \bar{x})^2}$$

**鏂瑰樊锛圴ariance锛夛細**
$$s^2 = \frac{1}{n-1}\sum_{i=1}^{n}(x_i - \bar{x})^2$$

**鍙樺紓绯绘暟锛圕V锛夛細**
$$CV = \frac{s}{\bar{x}} \times 100\%$$

鐢ㄤ簬姣旇緝涓嶅悓閲忕翰鏁版嵁鐨勭鏁ｇ▼搴︺€?
### 鍒嗗竷褰㈡€佸害閲?
**鍋忓害锛圫kewness锛夛細**
$$SK = \frac{1}{n}\sum_{i=1}^{n}\left(\frac{x_i - \bar{x}}{s}\right)^3$$

- SK > 0锛氬彸鍋忓垎甯?- SK = 0锛氬绉板垎甯?- SK < 0锛氬乏鍋忓垎甯?
**宄板害锛圞urtosis锛夛細**
$$K = \frac{1}{n}\sum_{i=1}^{n}\left(\frac{x_i - \bar{x}}{s}\right)^4$$

- K > 3锛氬皷宄板垎甯?- K = 3锛氭鎬佸垎甯?- K < 3锛氬钩宄板垎甯?
## 姒傜巼鍒嗗竷搴旂敤

### 甯哥敤绂绘暎鍒嗗竷

**浜岄」鍒嗗竷锛圔inomial Distribution锛夛細**
$$P(X = k) = \binom{n}{k}p^k(1-p)^{n-k}$$

搴旂敤锛氳川閲忔楠屼腑鐨勪笉鍚堟牸鍝佹暟銆佸競鍦鸿皟鐮斾腑鐨勬垚鍔熸鏁?
**娉婃澗鍒嗗竷锛圥oisson Distribution锛夛細**
$$P(X = k) = \frac{\lambda^k e^{-\lambda}}{k!}$$

搴旂敤锛氬崟浣嶆椂闂村唴鐨勯【瀹㈠埌杈炬暟銆佺己闄锋暟

### 甯哥敤杩炵画鍒嗗竷

**姝ｆ€佸垎甯冿紙Normal Distribution锛夛細**
$$f(x) = \frac{1}{\sigma\sqrt{2\pi}}e^{-\frac{(x-\mu)^2}{2\sigma^2}}$$

搴旂敤锛氫骇鍝佸昂瀵搞€佹祴閲忚宸€佽偂绁ㄦ敹鐩婄巼

**鎸囨暟鍒嗗竷锛圗xponential Distribution锛夛細**
$$f(x) = \lambda e^{-\lambda x}$$

搴旂敤锛氳澶囧鍛姐€佹湇鍔℃椂闂?
## 鍥炲綊鍒嗘瀽鍦ㄥ晢涓氫腑鐨勫簲鐢?
### 绠€鍗曠嚎鎬у洖褰?
**妯″瀷锛?*
$$y = \beta_0 + \beta_1 x + \varepsilon$$

**鍟嗕笟搴旂敤锛?*
- 骞垮憡鏀嚭涓庨攢鍞鐨勫叧绯?- 浠锋牸涓庨渶姹傞噺鐨勫叧绯?- 鍛樺伐鍩硅鏃堕棿涓庣敓浜у姏鐨勫叧绯?
### 澶氬厓鍥炲綊鍒嗘瀽

**妯″瀷锛?*
$$y = \beta_0 + \beta_1 x_1 + \beta_2 x_2 + \cdots + \beta_p x_p + \varepsilon$$

**搴旂敤鍦烘櫙锛?*
- 鎴夸环棰勬祴锛堥潰绉€佹埧榫勩€佸湴娈碉級
- 瀹㈡埛浠峰€奸娴嬶紙娑堣垂棰戞銆佸鍗曚环銆佷細鍛樻椂闀匡級
- 閿€鍞娴嬶紙瀛ｈ妭銆佷績閿€銆佺珵鍝佷环鏍硷級

### 鍥炲綊璇婃柇

- **澶氶噸鍏辩嚎鎬?*锛氭柟宸啫鑳€鍥犲瓙锛圴IF锛?- **寮傛柟宸€?*锛氭畫宸浘鍒嗘瀽
- **鑷浉鍏虫€?*锛欴urbin-Watson妫€楠?- **妯″瀷鎷熷悎浼樺害**锛歊虏銆佽皟鏁碦虏

## A/B娴嬭瘯

### 鍩烘湰鍘熺悊

A/B娴嬭瘯鏄瘮杈冧袱涓増鏈殑缁熻瀹為獙鏂规硶锛岀敤浜庣‘瀹氬摢涓増鏈〃鐜版洿濂姐€?
**瀹炴柦姝ラ锛?*
1. 鏄庣‘娴嬭瘯鐩爣锛堣浆鍖栫巼銆佺偣鍑荤巼绛夛級
2. 纭畾鏍锋湰閲忓拰娴嬭瘯鏃堕暱
3. 闅忔満鍒嗛厤鐢ㄦ埛鍒板鐓х粍鍜屽疄楠岀粍
4. 鏀堕泦鏁版嵁骞惰繘琛岀粺璁″垎鏋?5. 鍋氬嚭鍐崇瓥骞跺疄鏂?
### 鏍锋湰閲忚绠?
$$n = \frac{(Z_{\alpha/2} + Z_{\beta})^2 \times [p_1(1-p_1) + p_2(1-p_2)]}{(p_1 - p_2)^2}$$

### 甯歌闂

- **鏂板鏁堝簲**锛氱敤鎴峰鏂扮増鏈殑鏂伴矞鎰?- **骞稿瓨鑰呭亸宸?*锛氬彧鍒嗘瀽瀹屾垚娴嬭瘯鐨勭敤鎴?- **澶氶噸姣旇緝**锛氬悓鏃舵祴璇曞涓彉閲?- **娴嬭瘯鏃堕暱涓嶈冻**锛氭湭瑕嗙洊瀹屾暣鐨勪笟鍔″懆鏈?
## 鏃堕棿搴忓垪鍒嗘瀽

### 鏃堕棿搴忓垪鎴愬垎

**瓒嬪娍锛圱rend锛夛細**
- 闀挎湡涓婂崌鎴栦笅闄嶇殑鍙樺姩
- 绾挎€ц秼鍔裤€侀潪绾挎€ц秼鍔?
**瀛ｈ妭鎬э紙Seasonality锛夛細**
- 鍥哄畾鍛ㄦ湡鐨勯噸澶嶆尝鍔?- 鏃ャ€佸懆銆佹湀銆佸搴︺€佸勾

**寰幆锛圕yclical锛夛細**
- 闈炲浐瀹氬懆鏈熺殑娉㈠姩
- 閫氬父涓庣粡娴庡懆鏈熺浉鍏?
**涓嶈鍒欏彉鍔紙Irregular锛夛細**
- 闅忔満娉㈠姩
- 鏃犳硶棰勬祴鐨勬垚鍒?
### 甯哥敤棰勬祴鏂规硶

**绉诲姩骞冲潎娉曪細**
$$\hat{y}_{t+1} = \frac{1}{k}\sum_{i=0}^{k-1}y_{t-i}$$

**鎸囨暟骞虫粦娉曪細**
$$\hat{y}_{t+1} = \alpha y_t + (1-\alpha)\hat{y}_t$$

**ARIMA妯″瀷锛?*
- 鑷洖褰掞紙AR锛夛細褰撳墠鍊间緷璧栦簬杩囧幓鍊?- 绉诲姩骞冲潎锛圡A锛夛細褰撳墠鍊间緷璧栦簬杩囧幓璇樊
- 宸垎锛圛锛夛細浣垮簭鍒楀钩绋?
## Excel鏁版嵁鍒嗘瀽宸ュ叿

### 鍐呯疆鍒嗘瀽宸ュ叿

- **鎻忚堪缁熻**锛氫竴閿敓鎴愬潎鍊笺€佹爣鍑嗗樊绛夌粺璁￠噺
- **鐩存柟鍥?*锛氭暟鎹垎甯冨彲瑙嗗寲
- **鐩稿叧绯绘暟**锛氬彉閲忛棿鐩稿叧鎬у垎鏋?- **鍥炲綊鍒嗘瀽**锛氱嚎鎬у洖褰掑缓妯?- **绉诲姩骞冲潎**锛氭椂闂村簭鍒楀钩婊?
### 甯哥敤鍑芥暟

```
=AVERAGE()        # 鍧囧€?=STDEV.S()        # 鏍囧噯宸?=CORREL()         # 鐩稿叧绯绘暟
=LINEST()         # 绾挎€у洖褰?=TREND()          # 瓒嬪娍棰勬祴
=FORECAST()       # 棰勬祴鍊?```

## Python鏁版嵁鍒嗘瀽宸ュ叿

### pandas鏁版嵁澶勭悊

```python
import pandas as pd
import numpy as np

# 鏁版嵁璇诲彇
df = pd.read_csv('data.csv')

# 鎻忚堪缁熻
df.describe()

# 鍒嗙粍缁熻
df.groupby('category')['sales'].agg(['mean', 'std', 'sum'])

# 鏁版嵁閫忚琛?pd.pivot_table(df, values='sales', index='region', 
               columns='product', aggfunc='sum')
```

### 鏁版嵁鍙鍖?
```python
import matplotlib.pyplot as plt
import seaborn as sns

# 鎶樼嚎鍥?plt.figure(figsize=(10, 6))
plt.plot(df['date'], df['sales'])
plt.title('Sales Trend')
plt.show()

# 绠辩嚎鍥?sns.boxplot(x='category', y='price', data=df)
plt.show()
```

### 缁熻鍒嗘瀽

```python
from scipy import stats
from sklearn.linear_model import LinearRegression

# 鍋囪妫€楠?stats.ttest_ind(group1, group2)

# 鍥炲綊鍒嗘瀽
model = LinearRegression()
model.fit(X, y)
print(f'R虏: {model.score(X, y)}')
```

## 鍟嗕笟缁熻搴旂敤妗堜緥

### 閿€鍞垎鏋?
- 閿€鍞秼鍔垮垎鏋?- 浜у搧鐩稿叧鎬у垎鏋?- 瀹㈡埛缁嗗垎锛圧FM妯″瀷锛?- 閿€鍞娴?
### 璐ㄩ噺鎺у埗

- 鎺у埗鍥撅紙X-bar鍥俱€丷鍥撅級
- 杩囩▼鑳藉姏鍒嗘瀽锛圕p銆丆pk锛?- 缂洪櫡鐜囧垎鏋?- 鍏タ鏍肩帥绠＄悊

### 甯傚満璋冪爺

- 闂嵎璁捐涓庢娊鏍?- 婊℃剰搴﹀垎鏋?- 甯傚満浠介浼拌
- 鍝佺墝鍋忓ソ鐮旂┒

## 鍙傝€冭祫婧?
- Anderson DR, et al. *Statistics for Business and Economics*
- Levine DM, et al. *Business Statistics: A First Course*
- McKinney W. *Python for Data Analysis*
- 鎴寸淮 R. 瀹夊痉妫? 銆婂晢鍔′笌缁忔祹缁熻銆?

## 鐩稿叧鏉＄洰

[[Probability]], [[07_InterdisciplinarySciences/DataScience/INDEX|DataScience]], [[05_ComputerScience/ArtificialIntelligence/MachineLearning/INDEX|MachineLearning]], StatisticalModeling
