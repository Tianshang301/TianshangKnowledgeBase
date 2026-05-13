# 寰Н鍒嗚瑙?
## 涓€銆佹瀬闄?(Limits)

### 蔚-未 瀹氫箟

鍑芥暟 $f(x)$ 鍦?$x \to a$ 鏃剁殑鏋侀檺涓?$L$锛岃浣?$\lim_{x \to a} f(x) = L$锛屽鏋滃浠绘剰 $\varepsilon > 0$锛屽瓨鍦?$\delta > 0$锛屼娇寰楀綋 $0 < |x - a| < \delta$ 鏃讹紝鏈?$|f(x) - L| < \varepsilon$銆?
$$\forall \varepsilon > 0, \ \exists \delta > 0 \ \text{s.t.} \ 0 < |x-a| < \delta \implies |f(x)-L| < \varepsilon$$

### 鏋侀檺娉曞垯

鑻?$\lim_{x \to a} f(x) = L$锛?\lim_{x \to a} g(x) = M$锛屽垯锛?
$$\lim_{x \to a} [f(x) \pm g(x)] = L \pm M$$
$$\lim_{x \to a} [f(x)g(x)] = LM$$
$$\lim_{x \to a} \frac{f(x)}{g(x)} = \frac{L}{M}, \ (M \neq 0)$$
$$\lim_{x \to a} [f(x)]^n = L^n, \ n \in \mathbb{Z}^+$$

### 澶归€煎畾鐞?(Squeeze Theorem)

鑻ュ湪 $a$ 鐨勬煇鍘诲績閭诲煙鍐呮湁 $g(x) \leq f(x) \leq h(x)$锛屼笖 $\lim_{x \to a} g(x) = \lim_{x \to a} h(x) = L$锛屽垯 $\lim_{x \to a} f(x) = L$銆?
**閲嶈鏋侀檺锛?*

$$\lim_{x \to 0} \frac{\sin x}{x} = 1, \quad \lim_{x \to 0} \frac{1 - \cos x}{x} = 0, \quad \lim_{x \to \infty} \left(1 + \frac{1}{x}\right)^x = e$$

## 浜屻€佽繛缁€?(Continuity)

### 瀹氫箟

$f(x)$ 鍦?$x = a$ 澶勮繛缁綋涓斾粎褰擄細

$$\lim_{x \to a} f(x) = f(a)$$

### 闂存柇鐐圭被鍨?
- **鍙幓闂存柇鐐?*锛?\lim_{x \to a} f(x)$ 瀛樺湪浣?$\neq f(a)$ 鎴?$f(a)$ 鏈畾涔?- **璺宠穬闂存柇鐐?*锛氬乏鍙虫瀬闄愬瓨鍦ㄤ絾涓嶇浉绛?- **鏃犵┓闂存柇鐐?*锛?\lim_{x \to a} f(x) = \pm \infty$
- **鎸崱闂存柇鐐?*锛氭瀬闄愪笉瀛樺湪锛堝 $\sin(1/x)$ 鍦?$x=0$锛?
### 浠嬪€煎畾鐞?(Intermediate Value Theorem)

鑻?$f$ 鍦?$[a,b]$ 涓婅繛缁紝$f(a) \neq f(b)$锛屽垯瀵?$f(a)$ 鍜?$f(b)$ 涔嬮棿鐨勪换鎰忓€?$k$锛屽瓨鍦?$c \in (a,b)$ 浣垮緱 $f(c) = k$銆?
## 涓夈€佸鏁?(Derivatives)

### 瀹氫箟

$$f'(x) = \lim_{h \to 0} \frac{f(x+h) - f(x)}{h}$$

### 姹傚娉曞垯

| 娉曞垯 | 鍏紡 |
|:---|:---|
| 甯告暟鍊?| $(cf)' = cf'$ |
| 鍜屽樊 | $(f \pm g)' = f' \pm g'$ |
| 涔樼Н | $(fg)' = f'g + fg'$ |
| 鍟?| $\left(\frac{f}{g}\right)' = \frac{f'g - fg'}{g^2}$ |
| 閾惧紡 | $\frac{d}{dx} f(g(x)) = f'(g(x)) g'(x)$ |
| 鍙嶅嚱鏁?| $(f^{-1})'(x) = \frac{1}{f'(f^{-1}(x))}$ |
| 闅愬嚱鏁?| 瀵?$F(x,y)=0$ 涓よ竟姹傚锛?y$ 瑙嗕负 $y(x)$ |

### 甯哥敤瀵兼暟鍏紡

$$\frac{d}{dx} x^n = nx^{n-1}, \quad \frac{d}{dx} e^x = e^x, \quad \frac{d}{dx} \ln x = \frac{1}{x}$$
$$\frac{d}{dx} \sin x = \cos x, \quad \frac{d}{dx} \cos x = -\sin x, \quad \frac{d}{dx} \tan x = \sec^2 x$$
$$\frac{d}{dx} \arcsin x = \frac{1}{\sqrt{1-x^2}}, \quad \frac{d}{dx} \arctan x = \frac{1}{1+x^2}$$

## 鍥涖€佸鏁扮殑搴旂敤

### 鏋佸€煎畾鐞?(Extreme Value Theorem)

鑻?$f$ 鍦?$[a,b]$ 涓婅繛缁紝鍒?$f$ 鍦?$[a,b]$ 涓婂彇寰楁渶澶у€煎拰鏈€灏忓€笺€?
### 涓€煎畾鐞?(Mean Value Theorem)

鑻?$f$ 鍦?$[a,b]$ 涓婅繛缁紝鍦?$(a,b)$ 鍐呭彲瀵硷紝鍒欏瓨鍦?$c \in (a,b)$ 浣垮緱锛?
$$f'(c) = \frac{f(b) - f(a)}{b - a}$$

**缃楀皵瀹氱悊锛?* 鑻?$f(a) = f(b)$锛屽垯瀛樺湪 $c \in (a,b)$ 浣垮緱 $f'(c) = 0$銆?
### Taylor瀹氱悊锛堝甫浣欓」锛?
$$f(x) = \sum_{k=0}^n \frac{f^{(k)}(a)}{k!}(x-a)^k + R_n(x)$$

**Lagrange浣欓」**锛?$$R_n(x) = \frac{f^{(n+1)}(\xi)}{(n+1)!}(x-a)^{n+1}, \quad \xi \in (a, x)$$

### 娲涘繀杈炬硶鍒?(L'H么pital's Rule)

鑻?$\lim_{x \to a} \frac{f(x)}{g(x)}$ 涓?$\frac{0}{0}$ 鎴?$\frac{\infty}{\infty}$ 鍨嬶紝涓?$\lim_{x \to a} \frac{f'(x)}{g'(x)}$ 瀛樺湪锛屽垯锛?
$$\lim_{x \to a} \frac{f(x)}{g(x)} = \lim_{x \to a} \frac{f'(x)}{g'(x)}$$

### 鏇茬嚎缁樺埗

- **涓寸晫鐐?*锛?f'(x) = 0$ 鎴?$f'(x)$ 涓嶅瓨鍦?- **鎷愮偣**锛?f''(x) = 0$ 涓斿乏鍙冲嚬鍑告€ф敼鍙?- **娓愯繎绾?*锛氭按骞虫笎杩戠嚎 $\lim_{x \to \pm\infty} f(x) = L$锛涘瀭鐩存笎杩戠嚎 $\lim_{x \to a} f(x) = \pm\infty$

## 浜斻€佺Н鍒?(Integrals)

### 榛庢浖鍜?(Riemann Sum)

$$\int_a^b f(x) \, dx = \lim_{n \to \infty} \sum_{i=1}^n f(x_i^*) \Delta x, \quad \Delta x = \frac{b-a}{n}$$

### 寰Н鍒嗗熀鏈畾鐞?(Fundamental Theorem of Calculus)

**FTC Part 1锛?* 鑻?$F(x) = \int_a^x f(t) \, dt$锛屽垯 $F'(x) = f(x)$銆?
$$\frac{d}{dx} \int_a^x f(t) \, dt = f(x)$$

**FTC Part 2锛?* 鑻?$F' = f$锛屽垯锛?
$$\int_a^b f(x) \, dx = F(b) - F(a)$$

### 鍩烘湰绉垎琛?
| 鍑芥暟 | 鍘熷嚱鏁?|
|:---|:---|
| $x^n$ | $\frac{x^{n+1}}{n+1}+C,\ n\neq -1$ |
| $1/x$ | $\ln\|x\|+C$ |
| $e^x$ | $e^x+C$ |
| $a^x$ | $a^x/\ln a+C$ |
| $\sin x$ | $-\cos x+C$ |
| $\cos x$ | $\sin x+C$ |
| $\sec^2 x$ | $\tan x+C$ |
| $\frac{1}{\sqrt{1-x^2}}$ | $\arcsin x+C$ |
| $\frac{1}{1+x^2}$ | $\arctan x+C$ |

### 绉垎鎶€宸?
**鎹㈠厓娉曪細**
$$\int f(g(x)) g'(x) \, dx = \int f(u) \, du, \ u = g(x)$$

**鍒嗛儴绉垎娉曪細**
$$\int u \, dv = uv - \int v \, du$$

**閮ㄥ垎鍒嗗紡鍒嗚В锛?* 灏嗘湁鐞嗗嚱鏁板垎瑙ｄ负绠€鍗曞垎寮忎箣鍜屽啀绉垎銆?
**涓夎鎹㈠厓锛?*
- $\sqrt{a^2 - x^2}$锛氫护 $x = a\sin\theta$
- $\sqrt{a^2 + x^2}$锛氫护 $x = a\tan\theta$
- $\sqrt{x^2 - a^2}$锛氫护 $x = a\sec\theta$

## 鍏€佸弽甯哥Н鍒?(Improper Integrals)

**鏃犵┓闄愶細** $\int_a^\infty f(x) \, dx = \lim_{b \to \infty} \int_a^b f(x) \, dx$

**鏃犵晫鍑芥暟锛?* $\int_a^b f(x) \, dx = \lim_{c \to a^+} \int_c^b f(x) \, dx$锛?x=a$ 涓虹憰鐐癸級

## 涓冦€佺Н鍒嗙殑搴旂敤

**闈㈢Н锛?* $A = \int_a^b [f(x) - g(x)] \, dx$

**浣撶Н锛堝渾鐩樻硶锛夛細** $V = \pi \int_a^b [R(x)]^2 \, dx$

**浣撶Н锛堝３娉曪級锛?* $V = 2\pi \int_a^b x f(x) \, dx$

**寮ч暱锛?* $s = \int_a^b \sqrt{1 + [f'(x)]^2} \, dx$

**鏃嬭浆鏇查潰闈㈢Н锛?* $S = 2\pi \int_a^b f(x) \sqrt{1 + [f'(x)]^2} \, dx$

## 鐩稿叧鏉＄洰

[[02_NaturalSciences/Mathematics/Algebra/INDEX|Algebra]], [[02_NaturalSciences/Mathematics/DifferentialEquations/INDEX|DifferentialEquations]], [[02_NaturalSciences/Mathematics/Geometry/INDEX|Geometry]], RealAnalysis
