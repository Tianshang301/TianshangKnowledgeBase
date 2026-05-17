---
aliases: [MATLAB数值计算与仿真]
tags: ['ProgrammingLanguages', 'MATLAB', '数值计算']
---

# MATLAB 数值计算与仿真

## 一、MATLAB 环境概述

MATLAB（Matrix Laboratory）由 MathWorks 开发，是数值计算和仿真的行业标准工具。

核心特性：

| 特性 | 说明 |
|------|------|
| 数据类型 | 默认矩阵 (double)，支持多种数值类型 |
| 脚本语言 | 解释执行，支持 JIT 加速 |
| 图形系统 | 内置 2D/3D 可视化，支持交互式绘图 |
| 工具箱 | 30+ 领域工具箱（信号处理、控制、优化等） |
| Simulink | 基于模型的仿真设计环境 |
| 代码生成 | MATLAB Coder / Embedded Coder |

## 二、矩阵运算基础

矩阵创建与操作：

```matlab
% 矩阵创建
A = [1 2 3; 4 5 6; 7 8 9]   % 3x3矩阵
B = eye(3)                     % 单位矩阵
C = zeros(3, 4)                % 全零矩阵
D = ones(2, 5)                 % 全1矩阵
E = rand(3)                    % 随机矩阵[0,1]
F = linspace(0, 1, 100)        % 等间隔向量

% 矩阵运算
A_transpose = A'                % 转置
A_inv = inv(A)                  % 逆矩阵
A_det = det(A)                  % 行列式
A_eig = eig(A)                  % 特征值
[A_vec, A_val] = eig(A)         % 特征向量和特征值
A_svd = svd(A)                  % 奇异值分解

% 逐元素运算
A .* B                          % 点乘
A ./ B                          % 点除
A .^ 2                          % 逐元素平方
```

线性方程组求解：

$$
Ax = b \quad \Rightarrow \quad x = A^{-1}b
$$

```matlab
A = [3 2 -1; 2 -2 4; -1 0.5 -1];
b = [1; -2; 0];

x = A \ b           % 使用反斜杠运算符（推荐）
% x = [-1; 2; -2]

% 验证
residual = norm(A*x - b)
```

## 三、数值分析与优化

数值积分：

```matlab
% 定积分计算
f = @(x) exp(-x.^2) .* sin(x);

% 自适应Simpson积分
Q = integral(f, 0, 10)

% 二重积分
g = @(x, y) x.^2 + y.^2;
Q2 = integral2(g, -1, 1, -1, 1)

% 三重积分
h = @(x, y, z) x + y + z;
Q3 = integral3(h, 0, 1, 0, 1, 0, 1)
```

微分方程求解：

```matlab
% 常微分方程 dy/dt = -2y + cos(t), y(0) = 1
odefun = @(t, y) -2*y + cos(t);
[t, y] = ode45(odefun, [0 10], 1);

% 绘图
plot(t, y, 'b-', 'LineWidth', 2)
xlabel('Time (s)')
ylabel('y(t)')
title('ODE Solution')
grid on

% 二阶ODE: 弹簧-阻尼系统
% m*d2x/dt2 + c*dx/dt + k*x = 0
m = 1; c = 0.5; k = 10;
spring_system = @(t, x) [x(2); -c/m*x(2) - k/m*x(1)];
[t, x] = ode45(spring_system, [0 20], [1; 0]);

figure
plot(t, x(:,1), 'r-', t, x(:,2), 'b--')
legend('Position', 'Velocity')
```

优化问题：

```matlab
% 无约束优化 最小化 Rosenbrock 函数
% f(x) = 100*(x2 - x1^2)^2 + (1 - x1)^2

fun = @(x) 100*(x(2) - x(1)^2)^2 + (1 - x(1))^2;
x0 = [0; 0];  % 初始点
[x_opt, fval] = fminunc(fun, x0)
% x_opt: [1; 1], fval: ~0

% 有约束优化
% min f(x) = -x1*x2
% subject to: x1 + x2 <= 10, x1 >= 0, x2 >= 0
f = @(x) -x(1)*x(2);
A = [1 1];
b = 10;
lb = [0; 0];
[x_opt, fval] = fmincon(f, [1; 1], A, b, [], [], lb, [])
```

## 四、信号处理

```matlab
% 信号生成
fs = 1000;                    % 采样频率 1kHz
t = 0:1/fs:1-1/fs;           % 时间向量

% 复合信号: 50Hz + 120Hz + 噪声
f1 = 50; f2 = 120;
signal = sin(2*pi*f1*t) + 2*sin(2*pi*f2*t) + randn(size(t))*0.5;

% FFT分析
N = length(signal);
Y = fft(signal);
f = fs*(0:(N/2))/N;
P2 = abs(Y/N);
P1 = P2(1:N/2+1);
P1(2:end-1) = 2*P1(2:end-1);

figure
plot(f, P1)
xlabel('Frequency (Hz)')
ylabel('|P1(f)|')
title('Single-Sided Amplitude Spectrum')
xlim([0 200])

% 滤波器设计
[b, a] = butter(4, 100/(fs/2), 'low');  % 4阶低通，截止100Hz
filtered_signal = filtfilt(b, a, signal);

% FIR滤波器
fir_coeff = fir1(30, 0.2);  % 30阶低通
filtered_fir = filter(fir_coeff, 1, signal);
```

$$
X[k] = \sum_{n=0}^{N-1} x[n] e^{-j2\pi kn/N}
$$

## 五、控制系统设计与仿真

```matlab
% 传递函数 G(s) = 1/(s^2 + 2s + 1)
s = tf('s');
G = 1/(s^2 + 2*s + 1);

% 阶跃响应
figure
step(G)
title('Step Response')
grid on

% 波特图
figure
bode(G)
grid on

% PID控制器设计
Kp = 2; Ki = 1; Kd = 0.5;
C = pid(Kp, Ki, Kd);

% 闭环系统
T = feedback(C*G, 1);

figure
step(T)
title('Closed-Loop Step Response with PID')

% 根轨迹
figure
rlocus(G)
title('Root Locus')
```

## 六、Simulink 仿真

Simulink 是基于模型的图形化仿真环境。

基本建模步骤：

```matlab
% 创建Simulink模型
new_system('my_model')
open_system('my_model')

% 通过命令行添加模块
add_block('simulink/Sources/Sine Wave', 'my_model/Sine')
add_block('simulink/Math Operations/Gain', 'my_model/Gain')
add_block('simulink/Sinks/Scope', 'my_model/Scope')
add_block('simulink/Continuous/Integrator', 'my_model/Integrator')

% 连接模块
add_line('my_model', 'Sine/1', 'Gain/1')
add_line('my_model', 'Gain/1', 'Integrator/1')
add_line('my_model', 'Integrator/1', 'Scope/1')

% 设置参数
set_param('my_model/Gain', 'Gain', '2.5')

% 运行仿真
sim('my_model')
```

常用仿真模块：

| 模块库 | 模块 | 用途 |
|--------|------|------|
| Sources | Step, Sine Wave, Pulse Generator | 信号源 |
| Continuous | Transfer Fcn, Integrator, PID Controller | 连续系统 |
| Math Operations | Gain, Sum, Product | 数学运算 |
| Sinks | Scope, To Workspace, Display | 数据显示 |
| Discontinuities | Saturation, Dead Zone, Relay | 非线性 |
| Signal Routing | Mux, Demux, Switch | 信号路由 |

## 七、数据可视化

2D 绘图：

```matlab
x = linspace(0, 2*pi, 100);
y1 = sin(x);
y2 = cos(x);
y3 = sin(2*x);

figure
plot(x, y1, 'r-', 'LineWidth', 2); hold on
plot(x, y2, 'b--', 'LineWidth', 2);
plot(x, y3, 'g:', 'LineWidth', 2);
hold off

xlabel('x')
ylabel('y')
title('Trigonometric Functions')
legend('sin(x)', 'cos(x)', 'sin(2x)')
grid on

% 子图
figure
subplot(2, 1, 1)
plot(x, y1)
title('sin(x)')

subplot(2, 1, 2)
plot(x, y2)
title('cos(x)')
```

3D 绘图：

```matlab
% 3D曲面
[X, Y] = meshgrid(-3:0.1:3, -3:0.1:3);
Z = peaks(X, Y);

figure
surf(X, Y, Z)
xlabel('X'), ylabel('Y'), zlabel('Z')
title('3D Surface')
colorbar
shading interp

% 等高线
figure
contour(X, Y, Z, 20)
xlabel('X'), ylabel('Y')
title('Contour Plot')
```

## 八、性能优化

```matlab
% 预分配数组（重要！）
N = 10000;

% 慢 动态增长
tic
x = [];
for i = 1:N
    x = [x, i^2];
end
toc

% 快 预分配
tic
x = zeros(1, N);
for i = 1:N
    x(i) = i^2;
end
toc

% 最快 向量化
tic
x = (1:N).^2;
toc

% 使用profiler分析性能
profile on
% 运行代码
profile viewer
```

向量化与循环速度对比：

| 操作 | 循环时间 | 向量化时间 | 加速比 |
|------|----------|-----------|--------|
| 求和 | 0.15s | 0.001s | 150x |
| 矩阵乘法 | 1.2s | 0.005s | 240x |
| 条件筛选 | 0.3s | 0.002s | 150x |
| 逐元素运算 | 0.08s | 0.0005s | 160x |

## 参考资料

1. MathWorks MATLAB 文档：https://www.mathworks.com/help/matlab
2. 《MATLAB 数值分析》 Cleve Moler 著
3. 《精通 MATLAB》 Stephen J. Chapman 著
4. MATLAB 官方示例：https://www.mathworks.com/examples
5. MATLAB Central 文件交换：https://www.mathworks.com/matlabcentral
6. 《Simulink 仿真及代码生成技术》书籍
7. Cleve's Corner 博客
