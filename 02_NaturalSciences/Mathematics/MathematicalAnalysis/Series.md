# 绾ф暟璇﹁В

## 涓€銆佹暟鍒?(Sequences)

### 鏋侀檺

鏁板垪 $\{a_n\}$ 鏀舵暃浜?$L$锛岃浣?$\lim_{n \to \infty} a_n = L$锛屽鏋滃浠绘剰 $\varepsilon > 0$锛屽瓨鍦?$N \in \mathbb{N}$锛屼娇寰楀綋 $n > N$ 鏃舵湁 $|a_n - L| < \varepsilon$銆?
### 鍗曡皟鏀舵暃瀹氱悊

鍗曡皟鏈夌晫鏁板垪蹇呮敹鏁涖€?
## 浜屻€佺骇鏁?(Series)

### 閮ㄥ垎鍜屼笌鏀舵暃

绾ф暟 $\sum_{n=1}^\infty a_n$ 鏀舵暃褰撲笖浠呭綋閮ㄥ垎鍜屽簭鍒?$\{S_n\}$ 鏀舵暃锛屽叾涓細

$$S_n = \sum_{k=1}^n a_k$$

**鍑犱綍绾ф暟锛?* $\sum_{n=0}^\infty ar^n = \frac{a}{1-r}$锛屽綋 $|r| < 1$ 鏃舵敹鏁涖€?
**$p$-绾ф暟锛?* $\sum_{n=1}^\infty \frac{1}{n^p}$ 褰?$p > 1$ 鏃舵敹鏁涳紝$p \leq 1$ 鏃跺彂鏁ｃ€?
## 涓夈€佹敹鏁涙€у垽鍒硶

### 鍙戞暎鎬ф楠?
鑻?$\lim_{n \to \infty} a_n \neq 0$锛屽垯 $\sum a_n$ 鍙戞暎銆?
### 鏀舵暃鎬у垽鍒硶姹囨€?
| 鍒ゅ埆娉?| 鏉′欢 | 缁撹 |
|:---|:---|:---|
| 鍙戞暎妫€楠?| $\lim a_n \neq 0$ | 鍙戞暎 |
| 绉垎娉?| $f$ 杩炵画姝ｉ€掑噺锛?\int f$ 鏀舵暃 | 鏀舵暃 |
| 姣旇緝娉?| $0 \le a_n \le b_n$锛?\sum b_n$ 鏀舵暃 | $\sum a_n$ 鏀舵暃 |
| 姣斿€兼硶 | $\lim \|a_{n+1}/a_n\| = L$ | $L<1$鏀舵暃,$L>1$鍙戞暎 |
| 鏍瑰€兼硶 | $\lim \sqrt[n]{\|a_n\|} = L$ | $L<1$鏀舵暃,$L>1$鍙戞暎 |
| 浜ら敊绾ф暟 | $b_n$ 閫掑噺 $\to 0$ | 鏀舵暃 |
| 鏋侀檺姣旇緝 | $\lim a_n/b_n = c>0$ | 鍚屾暃鏁?|

### 绉垎鍒ゅ埆娉?
鑻?$f$ 鍦?$[1, \infty)$ 涓婅繛缁€佹銆侀€掑噺锛屽垯 $\sum_{n=1}^\infty f(n)$ 涓?$\int_1^\infty f(x) \, dx$ 鍚屾暃鏁ｃ€?
### 姣旇緝鍒ゅ埆娉?
鑻?$0 \leq a_n \leq b_n$ 涓?$\sum b_n$ 鏀舵暃锛屽垯 $\sum a_n$ 鏀舵暃锛涜嫢 $\sum a_n$ 鍙戞暎锛屽垯 $\sum b_n$ 鍙戞暎銆?
### 鏋侀檺姣旇緝鍒ゅ埆娉?
鑻?$\lim_{n \to \infty} \frac{a_n}{b_n} = c > 0$锛屽垯 $\sum a_n$ 涓?$\sum b_n$ 鍚屾暃鏁ｃ€?
### 姣斿€煎垽鍒硶 (Ratio Test)

$$\lim_{n \to \infty} \left|\frac{a_{n+1}}{a_n}\right| = L$$
- $L < 1$锛氱粷瀵规敹鏁?- $L > 1$锛氬彂鏁?- $L = 1$锛氭棤娉曞垽瀹?
### 鏍瑰€煎垽鍒硶 (Root Test)

$$\lim_{n \to \infty} \sqrt[n]{|a_n|} = L$$
- $L < 1$锛氱粷瀵规敹鏁?- $L > 1$锛氬彂鏁?- $L = 1$锛氭棤娉曞垽瀹?
### 浜ら敊绾ф暟鍒ゅ埆娉?(Alternating Series Test)

鑻?$b_n$ 鍗曡皟閫掑噺瓒嬩簬 0锛屽垯浜ら敊绾ф暟 $\sum (-1)^{n-1} b_n$ 鏀舵暃銆?
## 鍥涖€佺粷瀵规敹鏁涗笌鏉′欢鏀舵暃

- **缁濆鏀舵暃**锛?\sum |a_n|$ 鏀舵暃
- **鏉′欢鏀舵暃**锛?\sum a_n$ 鏀舵暃浣?$\sum |a_n|$ 鍙戞暎

## 浜斻€佸箓绾ф暟 (Power Series)

### 褰㈠紡

$$\sum_{n=0}^\infty c_n (x - a)^n$$

### 鏀舵暃鍗婂緞涓庢敹鏁涘尯闂?
鏀舵暃鍗婂緞 $R$ 鐢辨牴鍊兼硶鎴栨瘮鍊兼硶姹傚緱锛?
$$\frac{1}{R} = \limsup_{n \to \infty} \sqrt[n]{|c_n|} \quad \text{鎴杴 \quad \frac{1}{R} = \lim_{n \to \infty} \left|\frac{c_{n+1}}{c_n}\right|$$

鏀舵暃鍖洪棿闇€妫€鏌ョ鐐?$x = a \pm R$ 澶勭殑鏀舵暃鎬с€?
### 閫愰」姹傚涓庣Н鍒?
鍦ㄦ敹鏁涘尯闂村唴锛?$$\frac{d}{dx} \sum_{n=0}^\infty c_n (x-a)^n = \sum_{n=1}^\infty n c_n (x-a)^{n-1}$$
$$\int \sum_{n=0}^\infty c_n (x-a)^n \, dx = \sum_{n=0}^\infty \frac{c_n}{n+1} (x-a)^{n+1} + C$$

## 鍏€佹嘲鍕掔骇鏁颁笌楹﹀厠鍔虫灄绾ф暟

### 娉板嫆绾ф暟

$$f(x) = \sum_{n=0}^\infty \frac{f^{(n)}(a)}{n!} (x - a)^n$$

### 楹﹀厠鍔虫灄绾ф暟

$$f(x) = \sum_{n=0}^\infty \frac{f^{(n)}(0)}{n!} x^n$$

### 甯歌灞曞紑

$$e^x = \sum_{n=0}^\infty \frac{x^n}{n!} = 1 + x + \frac{x^2}{2!} + \frac{x^3}{3!} + \cdots, \quad x \in \mathbb{R}$$

$$\sin x = \sum_{n=0}^\infty \frac{(-1)^n x^{2n+1}}{(2n+1)!} = x - \frac{x^3}{3!} + \frac{x^5}{5!} - \cdots, \quad x \in \mathbb{R}$$

$$\cos x = \sum_{n=0}^\infty \frac{(-1)^n x^{2n}}{(2n)!} = 1 - \frac{x^2}{2!} + \frac{x^4}{4!} - \cdots, \quad x \in \mathbb{R}$$

$$\ln(1+x) = \sum_{n=1}^\infty \frac{(-1)^{n-1} x^n}{n} = x - \frac{x^2}{2} + \frac{x^3}{3} - \cdots, \quad -1 < x \leq 1$$

$$(1+x)^\alpha = \sum_{n=0}^\infty \binom{\alpha}{n} x^n = 1 + \alpha x + \frac{\alpha(\alpha-1)}{2!} x^2 + \cdots, \quad |x| < 1$$

## 涓冦€佸倕閲屽彾绾ф暟 (Fourier Series)

### 姝ｄ氦鍑芥暟绯?
鍑芥暟绯?$\{1, \cos(nx), \sin(nx)\}_{n=1}^\infty$ 鍦?$[-\pi, \pi]$ 涓婃浜ゃ€?
### 鍌呴噷鍙剁郴鏁?
$$f(x) \sim \frac{a_0}{2} + \sum_{n=1}^\infty \left( a_n \cos(nx) + b_n \sin(nx) \right)$$

$$a_0 = \frac{1}{\pi} \int_{-\pi}^{\pi} f(x) \, dx$$
$$a_n = \frac{1}{\pi} \int_{-\pi}^{\pi} f(x) \cos(nx) \, dx, \ n \geq 1$$
$$b_n = \frac{1}{\pi} \int_{-\pi}^{\pi} f(x) \sin(nx) \, dx, \ n \geq 1$$

### 鏀舵暃鎬э紙鐙勫埄鍏嬮浄鏉′欢锛?
鑻?$f$ 鍦?$[-\pi, \pi]$ 涓婂垎娈佃繛缁笖鍒嗘鍏夋粦锛屽垯鍌呴噷鍙剁骇鏁板湪杩炵画鐐瑰鏀舵暃鍒?$f(x)$锛屽湪璺宠穬闂存柇鐐瑰鏀舵暃鍒板乏鍙虫瀬闄愮殑骞冲潎鍊笺€?
### 澶嶆暟褰㈠紡

$$f(x) = \sum_{n=-\infty}^\infty c_n e^{inx}, \quad c_n = \frac{1}{2\pi} \int_{-\pi}^{\pi} f(x) e^{-inx} \, dx$$

### Parseval瀹氱悊

$$\frac{1}{2\pi} \int_{-\pi}^{\pi} |f(x)|^2 dx = \sum_{n=-\infty}^{\infty} |c_n|^2 = \frac{a_0^2}{4} + \frac{1}{2}\sum_{n=1}^{\infty} (a_n^2 + b_n^2)$$

### Cauchy涔樼Н

涓や釜绾ф暟鐨勪箻绉細
$$\left(\sum_{n=0}^{\infty} a_n\right) \left(\sum_{n=0}^{\infty} b_n\right) = \sum_{n=0}^{\infty} c_n, \quad c_n = \sum_{k=0}^{n} a_k b_{n-k}$$

## 鐩稿叧鏉＄洰

[[02_NaturalSciences/Mathematics/Algebra/INDEX|Algebra]], [[02_NaturalSciences/Mathematics/DifferentialEquations/INDEX|DifferentialEquations]], [[02_NaturalSciences/Mathematics/Geometry/INDEX|Geometry]], RealAnalysis
