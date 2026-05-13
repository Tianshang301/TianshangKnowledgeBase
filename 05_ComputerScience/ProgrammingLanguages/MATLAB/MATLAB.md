# MATLAB

## 一、MATLAB 环境

MATLAB（Matrix Laboratory）是 MathWorks 开发的高级数值计算和可视化环境。

| 组件 | 功能 |
|------|------|
| 命令窗口（Command Window） | 交互式执行命令 |
| 编辑器（Editor） | 编写脚本和函数 |
| 工作区（Workspace） | 查看和管理变量 |
| 当前文件夹（Current Folder） | 文件浏览 |
| 路径管理（Path） | 设置搜索路径 |
| 实时脚本（Live Script） | 交互式文档（`.mlx`） |

## 二、数据类型

| 类型 | 说明 | 示例 |
|------|------|------|
| `double` | 双精度浮点（默认） | `x = 3.14` |
| `single` | 单精度浮点 | `x = single(3.14)` |
| `int8/16/32/64` | 有符号整数 | `x = int32(42)` |
| `char` | 字符数组 | `s = 'hello'` |
| `string` | 字符串（R2017a+） | `s = "hello"` |
| `logical` | 逻辑值 | `flag = true` |
| `cell` | 异构数组 | `c = {1, 'text', [1 2 3]}` |
| `struct` | 结构体 | `s.name = 'Alice'; s.age = 20` |
| `table` | 表格数据 | `T = table(x, y)` |
| `categorical` | 分类数据 | `c = categorical({'A','B','A'})` |

## 三、矩阵运算

### 基本操作

```matlab
% 矩阵创建
A = [1 2 3; 4 5 6; 7 8 9];     % 3×3 矩阵
B = zeros(3, 4);                % 全零矩阵
C = ones(3);                    % 全 1 矩阵
D = eye(4);                     % 单位矩阵
E = rand(3, 4);                 % 均匀分布随机数
F = linspace(0, 1, 100);        % 线性等分向量

% 索引
A(2, 3)          % 第 2 行第 3 列
A(1:2, :)        % 前两行所有列
A(end, :)        % 最后一行
```

### 矩阵运算

| 运算 | 数学含义 | MATLAB 语法 |
|------|---------|------------|
| 矩阵乘法 | $A \times B$ | `A * B` |
| 逐元素乘法 | $A \odot B$ | `A .* B` |
| 转置 | $A^T$ | `A'` |
| 逆矩阵 | $A^{-1}$ | `inv(A)` |
| 行列式 | $\det(A)$ | `det(A)` |
| 特征值 | $\lambda$ | `eig(A)` |
| 奇异值分解 | $A = U\Sigma V^T$ | `svd(A)` |
| LU 分解 | $A = LU$ | `[L,U] = lu(A)` |
| QR 分解 | $A = QR$ | `[Q,R] = qr(A)` |

**特征值问题**：$A \vec{x} = \lambda \vec{x}$，其中 $\lambda$ 为特征值，$\vec{x}$ 为特征向量。

**奇异值分解**：$A = U \Sigma V^T$，$U$ 和 $V$ 是正交矩阵，$\Sigma$ 是对角矩阵。

```matlab
% 线性方程组求解：Ax = b
x = A \ b;       % 使用反斜杠运算符（推荐）
x = inv(A) * b;  % 效率较低
```

## 四、控制流

```matlab
% if/elseif/else
if x > 0
    disp('positive')
elseif x < 0
    disp('negative')
else
    disp('zero')
end

% for 循环
for i = 1:10
    disp(i^2)
end

% while 循环
while abs(x - x_old) > tol
    x_old = x;
    x = x_new(x_old);
end

% switch
switch day
    case 'Monday'
        disp('Weekday')
    case 'Saturday'
        disp('Weekend')
    otherwise
        disp('Other')
end
```

## 五、数据可视化

### 基本绘图

```matlab
% 2D 绘图
x = linspace(0, 2*pi, 100);
y1 = sin(x);
y2 = cos(x);

figure;                     % 创建新图形
plot(x, y1, 'r-', 'LineWidth', 2); hold on;
plot(x, y2, 'b--', 'LineWidth', 2);
xlabel('x'); ylabel('y');
title('正弦和余弦函数');
legend('sin(x)', 'cos(x)');
grid on;

% 子图
subplot(2, 2, 1); plot(x, y1);
subplot(2, 2, 2); bar(1:5, rand(1,5));
subplot(2, 2, 3); histogram(randn(1000,1));
subplot(2, 2, 4); scatter(x, y1 + 0.1*randn(size(x)));
```

### 3D 绘图

```matlab
% 曲面图
[X, Y] = meshgrid(-3:0.1:3);
Z = peaks(X, Y);
figure;
surf(X, Y, Z);
mesh(X, Y, Z);      % 网格图
contour(X, Y, Z);   % 等高线
```

## 六、函数定义

```matlab
% 标准函数
function [mean_val, std_val] = stats(x)
    n = length(x);
    mean_val = sum(x) / n;
    std_val = sqrt(sum((x - mean_val).^2) / (n - 1));
end

% 匿名函数
f = @(x) x.^2 + 2*x + 1;
f(3)                          % 输出 16

% 函数句柄
h = @my_func;
integral(h, 0, 1)             % 数值积分
```

## 七、文件 I/O

```matlab
% 保存和加载 MAT 文件
save('data.mat', 'x', 'y');
load('data.mat');

% 文本文件
data = load('data.txt');          % 纯数值
data = csvread('data.csv');       % CSV（旧）
data = readmatrix('data.csv');    % 推荐（R2019a+）
writematrix(data, 'output.csv');

% Excel
data = xlsread('data.xlsx');
T = readtable('data.xlsx');
writetable(T, 'output.xlsx');

% 低级 I/O
fid = fopen('data.txt', 'r');
line = fgetl(fid);
fprintf(fid, 'x = %6.2f\n', x);
fclose(fid);
```

## 八、优化工具箱

```matlab
% 无约束优化
f = @(x) x(1)^2 + x(2)^2 + x(1)*x(2);
x0 = [1, 1];
x_opt = fminunc(f, x0);

% 约束优化
A = []; b = [];
Aeq = [1, 1]; beq = 1;
lb = [0, 0]; ub = [];
f = @(x) -x(1)*x(2);
x_opt = fmincon(f, [0.5, 0.5], A, b, Aeq, beq, lb, ub);

% 线性规划
f = [-5, -4];          % 最大化 5x + 4y
A = [6, 4; 1, 2; -1, 0; 0, -1];
b = [24, 6, 0, 0];
x_opt = linprog(f, A, b);
```

## 九、统计与机器学习

```matlab
% 线性回归
mdl = fitlm(X, y);         % 线性模型
y_pred = predict(mdl, X_new);

% SVM 分类器
svm_mdl = fitcsvm(X, y, 'KernelFunction', 'rbf');

% K-means 聚类
[idx, C] = kmeans(X, 3);

% PCA 降维
[coeff, score, latent] = pca(X);

% 神经网络
net = feedforwardnet(10);
net = train(net, X, y);
```

## 十、Simulink 基础

Simulink 是 MATLAB 的图形化仿真环境：

- **模块库**：连续/离散系统、数学运算、信号路由、Sinks/Sources
- **求解器**：ode45（变步长）、ode23、离散求解器
- **子系统**：组织复杂模型的层次结构

### ODE 求解器对比

| 求解器 | 类型 | 精度 | 适用场景 |
|-------|------|------|---------|
| `ode45` | 变步长 (RK4/5) | 中高 | 通用首选，非刚性 |
| `ode23` | 变步长 (RK2/3) | 低 | 容忍误差较大时 |
| `ode113` | 变步长 (Adams) | 高 | 高精度要求 |
| `ode15s` | 变步长 (BDF) | 中 | **刚性**方程 |
| `ode23s` | 变步长 (Rosenbrock) | 低 | 刚性低精度 |
| `ode23t` | 梯形法 | 中 | 中等刚性 |
| `ode23tb` | TR-BDF2 | 中 | 刚性问题 |
| 离散求解器 | 定步长 | — | 纯离散系统 |

## 十一、信号处理

### FFT（快速傅里叶变换）

$$X(k) = \sum_{n=0}^{N-1} x(n) e^{-j2\pi kn/N}$$

```matlab
Fs = 1000;                    % 采样频率
t = 0:1/Fs:1;                 % 时间向量
x = sin(2*pi*50*t) + 0.5*sin(2*pi*120*t);
X = fft(x);
f = Fs*(0:(length(X)/2))/length(X);
P = abs(X/length(X));
P = P(1:length(X)/2+1);
plot(f, P);
```

### 滤波器设计

```matlab
% FIR 低通滤波器设计
fc = 100;                     % 截止频率
fs = 1000;                    % 采样频率
N = 50;                       % 滤波器阶数
b = fir1(N, fc/(fs/2));       % 设计滤波器
y = filter(b, 1, x);          % 滤波

% IIR 滤波器
[b, a] = butter(4, 0.2);      % 4 阶 Butterworth 低通
y = filter(b, a, x);
```

## 十二、图像处理

```matlab
img = imread('photo.jpg');        % 读取图像
imshow(img);                      % 显示图像
gray = rgb2gray(img);             % 转灰度
edges = edge(gray, 'canny');      % 边缘检测
filtered = imfilter(gray, fspecial('gaussian', [5 5], 2));  % 高斯滤波
```

## 十三、MATLAB vs Python

| 特性 | MATLAB | Python (NumPy/SciPy) |
|------|--------|---------------------|
| 许可证 | 商业付费 | 开源免费 |
| 矩阵语法 | 原生 | `numpy.array` |
| 可视化 | 内置强大 | Matplotlib |
| 工具箱 | 各领域专用工具箱 | 社区包 |
| 性能 | JIT 加速 | NumPy/Cython |
| 部署 | MATLAB Compiler | 自由部署 |
| 社区 | 学术/工业 | 广泛 |

## 相关条目

- NumericalComputing
- Simulation
- [[07_InterdisciplinarySciences/DataScience/INDEX|DataScience]]
- EngineeringSoftware

## 参考资源

- [MATLAB 官方文档](https://www.mathworks.com/help/matlab/)
- [MathWorks 学习中心](https://matlabacademy.mathworks.com/)
- 《精通 MATLAB》（Stephen J. Chapman）
- [MATLAB Answers](https://www.mathworks.com/matlabcentral/answers/)
- [File Exchange - 社区贡献代码](https://www.mathworks.com/matlabcentral/fileexchange/)
