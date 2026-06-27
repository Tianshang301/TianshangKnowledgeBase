---
aliases: [NumPy]
tags: ['ProgrammingLanguages', 'Python', 'NumPy']
created: 2026-05-16
updated: 2026-05-13
---

# NumPy 快速指南

## 一、ndarray 创建

```python
import numpy as np

# 从列表创建
a = np.array([1, 2, 3, 4, 5])
b = np.array([[1, 2, 3], [4, 5, 6]])  # 2x3 矩阵
c = np.array([1, 2, 3], dtype=np.float32)

# 特殊数组
zeros = np.zeros((3, 4))        # 3x4 全零矩阵
ones = np.ones((2, 3))          # 2x3 全一矩阵
eye = np.eye(5)                 # 5x5 单位矩阵
full = np.full((3, 3), 7)       # 3x3 全7矩阵
empty = np.empty((2, 2))        # 未初始化 (垃圾值)

# 序列
arange = np.arange(10)          # [0 1 2 ... 9]
arange2 = np.arange(2, 10, 2)   # [2 4 6 8]
linspace = np.linspace(0, 1, 5) # [0. 0.25 0.5 0.75 1.]
logspace = np.logspace(0, 2, 5) # 对数等间距

# 随机数组
np.random.seed(42)  # 设置种子
rand = np.random.rand(3, 3)         # [0,1) 均匀分布
randn = np.random.randn(3, 3)       # 标准正态分布
randint = np.random.randint(0, 10, (3, 3))  # [0,10) 随机整数
uniform = np.random.uniform(-1, 1, (2, 3))  # [-1,1) 均匀
normal = np.random.normal(0, 1, (3, 3))     # N(0,1) 正态
```

## 二、数组属性

```python
a = np.array([[1, 2, 3], [4, 5, 6]], dtype=np.float64)

a.shape       # (2, 3) - 形状
a.ndim        # 2 - 维度数
a.size        # 6 - 元素总数
a.dtype       # float64 - 数据类型
a.itemsize    # 8 - 每个元素字节数
a.nbytes      # 48 - 总字节数
a.T           # 转置 (3x2)
a.real        # 实部
a.imag        # 虚部 (复数时)
a.flat        # 扁平迭代器
```

## 三、索引与切片

```python
a = np.array([[1, 2, 3, 4],
              [5, 6, 7, 8],
              [9, 10, 11, 12]])

# 基本索引
a[0, 1]       # 2
a[1]          # [5, 6, 7, 8]
a[-1, -1]     # 12

# 切片
a[:2, 1:3]    # [[2, 3], [6, 7]]
a[:, ::2]     # [[1, 3], [5, 7], [9, 11]]
a[::2]        # [[1,2,3,4], [9,10,11,12]]

# 布尔索引
mask = a > 5
print(a[mask])  # [6 7 8 9 10 11 12]
a[a % 2 == 0]  # 所有偶数

# 花式索引 (fancy indexing)
indices = [0, 2]
print(a[indices])  # 第0行和第2行
print(a[:, [0, -1]])  # 所有行的第0列和最后一列

# where
cond = np.where(a > 5, a, 0)  # 大于5的保留, 否则0
```

## 四、广播 (Broadcasting)

```python
# 广播规则: 从后往前对齐, 维度相同或其中一个为1

a = np.array([[1, 2, 3],
              [4, 5, 6]])  # (2, 3)
b = np.array([10, 20, 30])  # (3,) -> 广播为 (2, 3)
print(a + b)
# [[11 22 33]
#  [14 25 36]]

c = np.array([[1], [2], [3]])  # (3, 1)
d = np.array(10, 20, 30)   # (1, 3) -> 广播为 (3, 3)
print(c + d)
# [[11 21 31]
#  [12 22 32]
#  [13 23 33]]

# 标量广播
print(a * 10)  # 每个元素乘以10

# 常见错误: 形状不兼容
# a = np.ones((3, 2))
# b = np.ones((2, 3))
# a + b  # ValueError!
```

## 五、通用函数 (ufunc)

```python
a = np.array([1, 2, 3, 4, 5])

# 数学运算
np.add(a, 10)       # [11 12 13 14 15]
np.subtract(a, 1)   # [0 1 2 3 4]
np.multiply(a, 2)   # [2 4 6 8 10]
np.divide(a, 2)     # [0.5 1. 1.5 2. 2.5]
np.power(a, 2)      # [1 4 9 16 25]
np.sqrt(a)          # 平方根
np.square(a)        # 平方
np.abs([-1, -2, 3]) # [1 2 3]

# 三角函数
np.sin(np.pi/2)     # 1.0
np.cos(0)           # 1.0
np.tan(np.pi/4)     # ~1.0
np.arcsin(1)        # π/2

# 指数对数
np.exp([0, 1, 2])   # [1. 2.718 7.389]
np.log([1, e, e**2])  # [0 1 2]
np.log10([1, 10, 100]) # [0 1 2]

# 舍入
np.round([1.234, 2.567], 1)  # [1.2 2.6]
np.floor([1.5, 2.7])  # [1. 2.]
np.ceil([1.5, 2.1])   # [2. 3.]

# 统计
a = np.array([[1, 2, 3],
              [4, 5, 6]])

np.sum(a)             # 21
np.mean(a)            # 3.5
np.std(a)             # 1.707... 标准差
np.var(a)             # 2.916... 方差
np.min(a)             # 1
np.max(a)             # 6
np.argmin(a)          # 0 (扁平索引)
np.argmax(a)          # 5 (扁平索引)
np.median(a)          # 3.5

# 按轴统计
np.sum(a, axis=0)     # [5 7 9] 列和
np.sum(a, axis=1)     # [6 15] 行和
np.mean(a, axis=0)    # [2.5 3.5 4.5]
np.cumsum(a)          # 累积和 [1 3 6 10 15 21]
```

## 六、数组操作

```python
a = np.array([[1, 2, 3],
              [4, 5, 6]])

# 重塑
a.reshape(3, 2)       # [[1,2],[3,4],[5,6]]
a.reshape(-1)         # [1 2 3 4 5 6] 扁平化
a.flatten()           # 返回新数组 (复制)
a.ravel()             # 返回视图 (可能共享内存)
np.resize(a, (3, 3))  # 调整大小 (可填充重复)

# 转置
a.T                   # [[1,4],[2,5],[3,6]]
np.transpose(a)       # 同上

# 拼接
b = np.array(7, 8, 9)
np.concatenate([a, b], axis=0)  # 垂直拼接
np.vstack([a, b])               # 垂直栈
np.hstack([a, a])               # 水平栈: [[1,2,3,1,2,3],[4,5,6,4,5,6]]
np.stack([a, a], axis=0)        # 新轴堆叠 (2,2,3)

# 分割
np.split(a, 3, axis=1)    # 水平分割3份
np.hsplit(a, 3)           # 同上
np.vsplit(a, 2)           # 垂直分割

# 添加/删除维度
a[np.newaxis, :]          # (1, 2, 3) 增加新轴
np.expand_dims(a, axis=0) # 同上
np.squeeze(np.array([1]))  # 去除长度为1的维度
```

## 七、线性代数

```python
# 矩阵乘法
A = np.array([[1, 2], [3, 4]])
B = np.array([[5, 6], [7, 8]])

np.dot(A, B)          # 点积 [[19 22][43 50]]
A @ B                 # 同上 (@运算符)
np.matmul(A, B)       # 同上

# 向量点积
v1 = np.array([1, 2, 3])
v2 = np.array([4, 5, 6])
np.dot(v1, v2)        # 32
np.inner(v1, v2)      # 32
np.outer(v1, v2)      # 外积 (3x3)

# 行列式
np.linalg.det(A)      # -2.0

# 逆矩阵
np.linalg.inv(A)      # [[-2., 1.],[1.5, -0.5]]

# 特征值分解
eigenvalues, eigenvectors = np.linalg.eig(A)
print(eigenvalues)    # [-0.372...  5.372...]
print(eigenvectors)   # 特征向量矩阵

# SVD 分解
U, S, Vt = np.linalg.svd(A)
print(U.shape, S.shape, Vt.shape)  # (2,2) (2,) (2,2)

# 解线性方程组 Ax = b
A = np.array([[3, 1], [1, 2]])
b = np.array([9, 8])
x = np.linalg.solve(A, b)
print(x)  # [2. 3.]

# 范数
np.linalg.norm([3, 4])         # 5.0 (L2范数)
np.linalg.norm([3, 4], ord=1)  # 7.0 (L1范数)

# QR 分解
Q, R = np.linalg.qr(A)

# Cholesky 分解
L = np.linalg.cholesky(np.array([[4, 2], [2, 3]]))
```

## 八、随机模块

```python
rng = np.random.default_rng(42)  # 新式随机接口 (推荐)

# 分布
rng.random((3, 3))          # [0,1) 均匀
rng.normal(0, 1, (3, 3))    # N(0,1) 正态
rng.uniform(-1, 1, (3, 3))  # [-1,1) 均匀
rng.poisson(lam=3, size=10) # 泊松分布
rng.binomial(n=10, p=0.5, size=10)  # 二项分布
rng.exponential(scale=1.0, size=10)  # 指数分布
rng.gamma(shape=2, scale=2, size=10) # Gamma 分布

# 旧式接口 (兼容)
np.random.seed(42)
np.random.rand(3, 3)
np.random.randn(3, 3)
np.random.randint(0, 10, (3, 3))

# 随机操作
arr = np.arange(10)
rng.shuffle(arr)            # 原地打乱
rng.permutation(10)         # 随机排列 (返回新数组)
rng.choice([1,2,3,4,5], size=3, replace=False)  # 无放回抽样
rng.choice([1,2,3,4,5], size=10, replace=True)  # 有放回抽样
```

## 九、实用技巧

```python
# 1. 条件替换
a = np.array([1, 2, 3, 4, 5])
np.where(a > 3, 100, a)  # [1 2 3 100 100]

# 2. 唯一值与计数
np.unique([1, 2, 2, 3, 3, 3], return_counts=True)
# (array([1, 2, 3]), array([1, 2, 3]))

# 3. 集合操作
np.intersect1d([1,2,3], [2,3,4])  # [2 3]
np.union1d([1,2,3], [2,3,4])      # [1 2 3 4]
np.setdiff1d([1,2,3], [2,3,4])    # [1]
np.setxor1d([1,2,3], [2,3,4])     # [1 4]

# 4. 排序
a = np.array([[3, 1, 2], [6, 4, 5]])
np.sort(a)             # 每行排序
np.sort(a, axis=0)     # 每列排序
np.argsort(a)          # 排序索引
np.lexsort(([1, 2, 3], [3, 1, 2]))  # 多级排序

# 5. 向量化 (比循环快100倍)
def slow_loop(n):
    result = []
    for i in range(n):
        result.append(i ** 2)
    return np.array(result)

def fast_vectorized(n):
    return np.arange(n) ** 2

# 6. 内存映射 (处理超大文件)
# mmap = np.memmap('large.dat', dtype='float32', mode='readwrite', shape=(10000, 10000))

# 7. 保存与加载
np.save("array.npy", a)     # 二进制
np.savetxt("array.csv", a, delimiter=",")  # 文本
loaded = np.load("array.npy")
```

> NumPy 是 Python 科学计算的基石。核心要点: 使用向量化操作替代循环、理解广播机制、善用切片和索引。熟练掌握 NumPy 是学习 Pandas、Scikit-learn 和深度学习框架的基础。
