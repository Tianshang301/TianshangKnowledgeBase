# 澶氬厓寰Н鍒嗚瑙?
## 涓€銆佸鍏冨嚱鏁?
### 鍋忓鏁?
$$f_x(x,y) = \frac{\partial f}{\partial x} = \lim_{h \to 0} \frac{f(x+h, y) - f(x, y)}{h}$$
$$f_y(x,y) = \frac{\partial f}{\partial y} = \lim_{h \to 0} \frac{f(x, y+h) - f(x, y)}{h}$$

### 鍏嬭幈缃楀畾鐞?(Clairaut's Theorem)

鑻?$f_{xy}$ 鍜?$f_{yx}$ 鍦ㄧ偣 $(a,b)$ 闄勮繎杩炵画锛屽垯锛?
$$\frac{\partial^2 f}{\partial x \partial y} = \frac{\partial^2 f}{\partial y \partial x}$$

### Hessian鐭╅樀

$$H_f = \begin{bmatrix} 
\frac{\partial^2 f}{\partial x_1^2} & \frac{\partial^2 f}{\partial x_1\partial x_2} & \cdots \\
\frac{\partial^2 f}{\partial x_2\partial x_1} & \frac{\partial^2 f}{\partial x_2^2} & \cdots \\
\vdots & \vdots & \ddots
\end{bmatrix}$$

$H_f$ 姝ｅ畾 $\implies$ 灞€閮ㄦ瀬灏忥紱$H_f$ 璐熷畾 $\implies$ 灞€閮ㄦ瀬澶с€?
### 澶氬厓Taylor灞曞紑

$$f(x) = f(a) + \nabla f(a)^T(x-a) + \frac{1}{2}(x-a)^T H_f(a)(x-a) + \cdots$$

### 姊害 (Gradient)

$$\nabla f = \left\langle \frac{\partial f}{\partial x}, \frac{\partial f}{\partial y}, \frac{\partial f}{\partial z} \right\rangle$$

姊害鏂瑰悜涓哄嚱鏁板闀挎渶蹇殑鏂瑰悜锛屽叾妯′负鏈€澶ф柟鍚戝鏁般€?
### 鏂瑰悜瀵兼暟

$$D_{\mathbf{u}} f = \nabla f \cdot \mathbf{u}$$

鍏朵腑 $\mathbf{u}$ 涓哄崟浣嶅悜閲忋€?
### 鍒囧钩闈?
瀵规洸闈?$z = f(x,y)$锛屽湪 $(x_0, y_0, z_0)$ 澶勭殑鍒囧钩闈负锛?
$$z - z_0 = f_x(x_0, y_0)(x - x_0) + f_y(x_0, y_0)(y - y_0)$$

## 浜屻€佹媺鏍兼湕鏃ヤ箻鏁版硶

姹?$f(x,y,z)$ 鍦ㄧ害鏉?$g(x,y,z) = 0$ 涓嬬殑鏋佸€硷細

$$\nabla f = \lambda \nabla g$$

鍗宠В鏂圭▼缁勶細
$$f_x = \lambda g_x, \quad f_y = \lambda g_y, \quad f_z = \lambda g_z, \quad g = 0$$

## 涓夈€佸閲嶇Н鍒?
### 浜岄噸绉垎

$$\iint_R f(x,y) \, dA = \iint_R f(x,y) \, dx \, dy$$

### 绱绉垎

$$\iint_R f(x,y) \, dA = \int_a^b \int_{g_1(x)}^{g_2(x)} f(x,y) \, dy \, dx = \int_c^d \int_{h_1(y)}^{h_2(y)} f(x,y) \, dx \, dy$$

### 鏋佸潗鏍囧彉鎹?
$$x = r\cos\theta, \quad y = r\sin\theta, \quad dA = r \, dr \, d\theta$$

$$\iint_R f(x,y) \, dA = \iint_S f(r\cos\theta, r\sin\theta) \, r \, dr \, d\theta$$

### 涓夐噸绉垎

$$\iiint_E f(x,y,z) \, dV$$

**鏌卞潗鏍囷細**
$$x = r\cos\theta, \ y = r\sin\theta, \ z = z, \ dV = r \, dr \, d\theta \, dz$$

**鐞冨潗鏍囷細**
$$x = \rho\sin\phi\cos\theta, \ y = \rho\sin\phi\sin\theta, \ z = \rho\cos\phi, \ dV = \rho^2\sin\phi \, d\rho \, d\phi \, d\theta$$

### 鍙橀噺鏇挎崲涓庨泤鍙瘮琛屽垪寮?
$$\iint_R f(x,y) \, dA = \iint_S f(x(u,v), y(u,v)) \, |J| \, du \, dv$$

鍏朵腑闆呭彲姣旇鍒楀紡锛?
$$J = \frac{\partial(x,y)}{\partial(u,v)} = \begin{vmatrix} \frac{\partial x}{\partial u} & \frac{\partial x}{\partial v} \\ \frac{\partial y}{\partial u} & \frac{\partial y}{\partial v} \end{vmatrix}$$

## 鍥涖€佸悜閲忓井绉垎

### 鍚戦噺鍦?
$$\mathbf{F}(x,y,z) = P\mathbf{i} + Q\mathbf{j} + R\mathbf{k}$$

### 鏁ｅ害 (Divergence)

$$\text{div} \ \mathbf{F} = \nabla \cdot \mathbf{F} = \frac{\partial P}{\partial x} + \frac{\partial Q}{\partial y} + \frac{\partial R}{\partial z}$$

### 鏃嬪害 (Curl)

$$\text{curl} \ \mathbf{F} = \nabla \times \mathbf{F} = \begin{vmatrix} \mathbf{i} & \mathbf{j} & \mathbf{k} \\ \frac{\partial}{\partial x} & \frac{\partial}{\partial y} & \frac{\partial}{\partial z} \\ P & Q & R \end{vmatrix}$$

### Laplace绠楀瓙

$$\Delta f = \nabla^2 f = \frac{\partial^2 f}{\partial x^2} + \frac{\partial^2 f}{\partial y^2} + \frac{\partial^2 f}{\partial z^2}$$

### 绾跨Н鍒?
$$\int_C \mathbf{F} \cdot d\mathbf{r} = \int_a^b \mathbf{F}(\mathbf{r}(t)) \cdot \mathbf{r}'(t) \, dt$$

鑻?$\mathbf{F} = \nabla f$锛堜繚瀹堝満锛夛紝鍒?$\int_C \mathbf{F} \cdot d\mathbf{r} = f(\mathbf{r}(b)) - f(\mathbf{r}(a))$銆?
### 鏍兼灄瀹氱悊 (Green's Theorem)

$$\oint_C P \, dx + Q \, dy = \iint_D \left( \frac{\partial Q}{\partial x} - \frac{\partial P}{\partial y} \right) \, dA$$

### 闈㈢Н鍒?
$$\iint_S \mathbf{F} \cdot d\mathbf{S} = \iint_D \mathbf{F} \cdot (\mathbf{r}_u \times \mathbf{r}_v) \, du \, dv$$

### 鏂墭鍏嬫柉瀹氱悊 (Stokes' Theorem)

$$\oint_C \mathbf{F} \cdot d\mathbf{r} = \iint_S (\nabla \times \mathbf{F}) \cdot d\mathbf{S}$$

### 鏁ｅ害瀹氱悊 (楂樻柉瀹氱悊)

$$\iint_S \mathbf{F} \cdot d\mathbf{S} = \iiint_E (\nabla \cdot \mathbf{F}) \, dV$$

## 浜斻€佸簲鐢?
- **鏇查潰闈㈢Н**锛?A(S) = \iint_D |\mathbf{r}_u \times \mathbf{r}_v| \, du \, dv$
- **閫氶噺**锛?\iint_S \mathbf{F} \cdot \mathbf{n} \, dS$锛堟暎搴﹀畾鐞嗚绠楋級
- **鐜噺**锛?\oint_C \mathbf{F} \cdot d\mathbf{r}$锛堟柉鎵樺厠鏂畾鐞嗚绠楋級

## 鐩稿叧鏉＄洰

[[02_NaturalSciences/Mathematics/Algebra/INDEX|Algebra]], [[02_NaturalSciences/Mathematics/DifferentialEquations/INDEX|DifferentialEquations]], [[02_NaturalSciences/Mathematics/Geometry/INDEX|Geometry]], RealAnalysis
