# 贝叶斯统��?
## 一、贝叶斯推断基础

### 贝叶斯定��?
$$p(\theta \mid y) = \frac{p(y \mid \theta) p(\theta)}{p(y)} = \frac{p(y \mid \theta) p(\theta)}{\int p(y \mid \theta) p(\theta) \, d\theta}$$

- $p(\theta)$：先验分��?(Prior)
- $p(y \mid \theta)$：似��?(Likelihood)
- $p(\theta \mid y)$：后验分��?(Posterior)
- $p(y)$：边际似��?(Evidence)

### 共轭先验

| 似然 | 共轭先验 | 后验 |
|------|----------|------|
| Bernoulli$(p)$ | Beta$(\alpha, \beta)$ | Beta$(\alpha + \sum y_i, \beta + n - \sum y_i)$ |
| Poisson$(\lambda)$ | Gamma$(\alpha, \beta)$ | Gamma$(\alpha + \sum y_i, \beta + n)$ |
| Normal$(\mu, \sigma^2)$��?\sigma^2$ 已知��?| Normal$(\mu_0, \sigma_0^2)$ | Normal$(\frac{\mu_0/\sigma_0^2 + n\bar{y}/\sigma^2}{1/\sigma_0^2 + n/\sigma^2}, \frac{1}{1/\sigma_0^2 + n/\sigma^2})$ |

### 贝叶��?vs 频率学派

| 方面 | 频率学派 | 贝叶��?|
|------|---------|--------|
| 参数 $\theta$ | 固定未知常数 | 随机变量 |
| 概率含义 | 长期频率 | 信念程度 |
| 推断依据 | 似然 | 后验分布 |
| 区间估计 | 置信区间 | 可信区间 |

## 二、贝叶斯线性回��?
### 模型

$$y \sim N(X\beta, \sigma^2 I)$$
$$\beta \sim N(0, \tau^2 I)$$

### 后验

$$\beta \mid y \sim N\left( \frac{1}{\sigma^2} \Sigma X^T y, \ \Sigma \right)$$

其中 $\Sigma = \left( \frac{1}{\sigma^2} X^T X + \frac{1}{\tau^2} I \right)^{-1}$

贝叶斯线性回归的 MAP 估计等价��?Ridge 回归��?
## 三、可信区��?vs 置信区间

- **Credible Interval**��?P(\theta \in [a,b] \mid y) = 1 - \alpha$，参数是随机的，区间固定
- **Confidence Interval**��?P(\text{区间包含 } \theta) = 1 - \alpha$，参数固定，区间随机

## 四、马尔可夫链蒙特卡洛 (MCMC)

### 为什么需��?MCMC

当后验分布无闭式解时，用采样近似后验��?
### Metropolis-Hastings 算法

1. 从当前状��?$\theta^{(t)}$ 开��?2. 从提议分��?$q(\theta^* \mid \theta^{(t)})$ 采样候��?$\theta^*$
3. 计算接受概率��?
$$\alpha = \min\left(1, \frac{p(\theta^* \mid y) q(\theta^{(t)} \mid \theta^*)}{p(\theta^{(t)} \mid y) q(\theta^* \mid \theta^{(t)})}\right)$$

4. 以概��?$\alpha$ 接受 $\theta^{(t+1)} = \theta^*$，否��?$\theta^{(t+1)} = \theta^{(t)}$

### Gibbs 采样

每次从一个条件后验分布中采样��?
$$\theta_1^{(t+1)} \sim p(\theta_1 \mid \theta_2^{(t)}, \theta_3^{(t)}, \dots, y)$$
$$\theta_2^{(t+1)} \sim p(\theta_2 \mid \theta_1^{(t+1)}, \theta_3^{(t)}, \dots, y)$$
$$\vdots$$

```python
import numpy as np
import pymc as pm

# PyMC 示例：贝叶斯线性回��?data = np.random.randn(100)
y = 2 * data + 1 + np.random.randn(100) * 0.5

with pm.Model():
    # 先验
    alpha = pm.Normal('alpha', mu=0, sigma=10)
    beta = pm.Normal('beta', mu=0, sigma=10)
    sigma = pm.HalfNormal('sigma', sigma=1)
    
    # 似然
    mu = alpha + beta * data
    y_obs = pm.Normal('y_obs', mu=mu, sigma=sigma, observed=y)
    
    # MCMC 采样
    trace = pm.sample(1000, tune=500)
    
    # 后验摘要
    print(pm.summary(trace))
```

## 五、贝叶斯计算工具

### PyMC

- ��?Python 实现的概率编程框��?- 支持自动 MCMC（NUTS 采样器）
- 适合中小规模模型

### Stan

- 独立的概率编程语言
- 使用 HMC/NUTS 高效采样
- Python 接口：PyStan（CmdStanPy��?- 适合复杂模型

## 六、应��?
- **A/B 测试**：贝叶斯方法提供 $P(\text{A 优于 B})$ 的直接概��?- **贝叶斯分层模��?*：处理分组数据（如不同学校的考试成绩��?- **贝叶斯优��?*：超参数调优（Gaussian Process + acquisition function��?- **贝叶斯时间序��?*：结构时间序列模��?

## 相关条目

[[02_NaturalSciences/Mathematics/MathematicalAnalysis/INDEX|MathematicalAnalysis]], [[07_InterdisciplinarySciences/DataScience/INDEX|DataScience]], [[02_NaturalSciences/Mathematics/Algebra/INDEX|Algebra]], StatisticalInference
