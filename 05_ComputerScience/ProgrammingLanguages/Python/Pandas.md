# Pandas 快速指南

## 一、Series 与 DataFrame

```python
import pandas as pd
import numpy as np

# Series - 一维标签数组
s = pd.Series([1, 3, 5, np.nan, 6, 8])
s2 = pd.Series([10, 20, 30], index=["a", "b", "c"])

print(s2["a"])  # 10
print(s2[0])    # 10

# DataFrame - 二维表格
df = pd.DataFrame({
    "姓名": ["张三", "李四", "王五", "赵六"],
    "年龄": [25, 30, 35, 28],
    "城市": ["北京", "上海", "广州", "深圳"],
    "薪资": [15000, 20000, 18000, 22000]
})

# 从 NumPy 数组创建
df2 = pd.DataFrame(
    np.random.randn(4, 3),
    columns=["A", "B", "C"],
    index=pd.date_range("2024-01-01", periods=4)
)
```

## 二、数据读写

```python
# CSV
df.to_csv("data.csv", index=False, encoding="utf-8-sig")
df = pd.read_csv("data.csv", encoding="utf-8")

# Excel
df.to_excel("data.xlsx", sheet_name="Sheet1", index=False)
df = pd.read_excel("data.xlsx", sheet_name="Sheet1")

# JSON
df.to_json("data.json", orient="records", force_ascii=False)
df = pd.read_json("data.json")

# SQL
from sqlalchemy import create_engine
engine = create_engine("sqlite:///database.db")
df.to_sql("users", engine, if_exists="replace", index=False)
df = pd.read_sql("SELECT * FROM users", engine)

# 剪贴板
df.to_clipboard()
df = pd.read_clipboard()

# Parquet (高效列式存储)
df.to_parquet("data.parquet")
df = pd.read_parquet("data.parquet")
```

## 三、数据查看

```python
df = pd.DataFrame({
    "姓名": ["张三", "李四", "王五", "赵六", "陈七"],
    "年龄": [25, 30, 35, 28, None],
    "城市": ["北京", "上海", "广州", "深圳", "北京"],
    "薪资": [15000, 20000, 18000, 22000, 16000],
    "入职日期": pd.to_datetime(["2020-01-15", "2019-03-20", "2021-06-01", "2022-11-10", "2023-02-28"])
})

df.head(3)          # 前3行
df.tail(2)          # 后2行
df.sample(2)        # 随机2行
df.info()           # 列信息、非空数、数据类型
df.describe()       # 数值列统计摘要
df.describe(include="object")  # 对象列统计
df.shape            # (5, 5)
df.columns          # 列名
df.dtypes           # 数据类型
df.index            # 行索引
df.values           # 底层 NumPy 数组
```

## 四、数据选择

```python
# 列选择
df["姓名"]             # 单列 -> Series
df"姓名", "薪资"   # 多列 -> DataFrame

# 行选择 (位置)
df[0:3]               # 前3行 (切片)

# loc - 标签索引
df.loc[0]                     # 第0行
df.loc0, 2, 4             # 第0,2,4行
df.loc[0:2, "姓名":"城市"]    # 行切片 + 列切片
df.loc[df["年龄"] > 28]       # 条件选择

# iloc - 位置索引
df.iloc[0]            # 第0行
df.iloc[1:3, 0:2]    # 第1-2行, 第0-1列
df.iloc[:, [0, 3]]   # 所有行, 第0和3列

# at / iat - 快速标量访问
df.at[0, "姓名"]     # '张三'
df.iat[0, 0]         # '张三'

# 布尔选择
df[df["薪资"] > 17000]
df[(df["薪资"] > 15000) & (df["城市"] == "北京")]
df[df["城市"].isin(["北京", "上海"])]
df[df["姓名"].str.contains("张")]

# query
df.query("薪资 > 17000")
df.query("城市 == '北京' and 年龄 > 25")
```

## 五、缺失值处理

```python
# 检查缺失
df.isna()              # 每个元素是否NaN
df.isna().sum()        # 每列缺失数量
df.isna().any(axis=1)  # 有缺失的行
df.isna().sum().sum()  # 总缺失数

# 删除缺失
df.dropna()              # 删除任何有缺失的行
df.dropna(how="all")     # 删除全部缺失的行
df.dropna(thresh=3)      # 至少有3个非空值才保留
df.dropna(axis=1)        # 删除有缺失的列
df.dropna(subset=["年龄"])  # 只在特定列检查

# 填充缺失
df.fillna(0)                       # 填充0
df.fillna(method="ffill")          # 前向填充
df.fillna(method="bfill")          # 后向填充
df.fillna(df.mean())               # 用均值填充
df.fillna(df.median())             # 用中位数填充
df["年龄"].fillna(df["年龄"].mode()[0])  # 用众数填充
df.interpolate()                   # 插值填充

# 缺失值标记
df["年龄缺失"] = df["年龄"].isna()
```

## 六、数据操作

```python
# 添加列
df["年薪"] = df["薪资"] * 13
df["级别"] = pd.cut(df["薪资"], bins=[0, 10000, 20000, 30000], labels=["初级", "中级", "高级"])
df["年龄段"] = pd.qcut(df["年龄"], q=3, labels=["青年", "中年", "壮年"])

# 修改列
df.rename(columns={"姓名": "name", "年龄": "age"}, inplace=True)
df.columns = [c.upper() for c in df.columns]

# 删除列/行
df.drop("年薪", axis=1, inplace=True)
df.drop(0, axis=0, inplace=True)

# 排序
df.sort_values("薪资", ascending=False)
df.sort_values(["城市", "薪资"], ascending=[True, False])

# 排名
df["薪资排名"] = df["薪资"].rank(ascending=False)
```

## 七、分组与聚合

```python
df = pd.DataFrame({
    "部门": ["技术", "技术", "市场", "市场", "技术", "市场"],
    "姓名": ["张三", "李四", "王五", "赵六", "陈七", "刘八"],
    "薪资": [15000, 20000, 18000, 22000, 16000, 19000],
    "绩效": [85, 92, 78, 95, 88, 82]
})

# 分组聚合
df.groupby("部门")["薪资"].mean()
df.groupby("部门").agg({"薪资": ["mean", "sum", "count", "std"]})

# 多级聚合
df.groupby("部门").agg(
    平均薪资=("薪资", "mean"),
    最高薪资=("薪资", "max"),
    平均绩效=("绩效", "mean"),
    人数=("姓名", "count")
)

# transform - 保持原形状
df["部门平均薪资"] = df.groupby("部门")["薪资"].transform("mean")
df["薪资偏差"] = df["薪资"] - df["部门平均薪资"]

# filter - 过滤组
df.groupby("部门").filter(lambda x: x["薪资"].mean() > 17000)

# apply - 自定义函数
df.groupby("部门")["薪资"].apply(lambda x: x.max() - x.min())

# 多级分组
df.groupby(["部门", "城市"]).agg({"薪资": "mean"})
```

## 八、合并与连接

```python
# concat - 简单拼接
df1 = pd.DataFrame({"A": [1, 2], "B": [3, 4]})
df2 = pd.DataFrame({"A": [5, 6], "B": [7, 8]})
pd.concat([df1, df2], axis=0)  # 垂直拼接
pd.concat([df1, df2], axis=1)  # 水平拼接
pd.concat([df1, df2], ignore_index=True)  # 重置索引

# merge - SQL风格合并
left = pd.DataFrame({
    "id": [1, 2, 3],
    "姓名": ["张三", "李四", "王五"]
})
right = pd.DataFrame({
    "id": [1, 2, 4],
    "薪资": [15000, 20000, 18000]
})

pd.merge(left, right, on="id")                 # 内连接
pd.merge(left, right, on="id", how="left")     # 左连接
pd.merge(left, right, on="id", how="right")    # 右连接
pd.merge(left, right, on="id", how="outer")    # 外连接

# 多键合并
pd.merge(left, right, on=["key1", "key2"])

# join - 索引连接
left.join(right, lsuffix="_left", rsuffix="_right")
```

## 九、apply / map / applymap

```python
# apply - 对DataFrame的行/列应用函数
df = pd.DataFrame({"A": [1, 2, 3], "B": [4, 5, 6]})

df.apply(np.sum, axis=0)      # 列求和
df.apply(np.sum, axis=1)      # 行求和
df.apply(lambda x: x.max() - x.min(), axis=0)

# map - 对Series应用映射或函数
df["A"].map({1: "一", 2: "二", 3: "三"})
df["A"].map(lambda x: x ** 2)

# applymap - 对DataFrame每个元素应用函数
df.applymap(lambda x: f"{x:.2f}")

# 向量化字符串操作
df["姓名"].str.upper()
df["姓名"].str.contains("张")
df["姓名"].str.extract(r"(\w+)")
```

## 十、数据透视表

```python
df = pd.DataFrame({
    "部门": ["技术", "技术", "市场", "市场", "技术", "市场"],
    "城市": ["北京", "上海", "北京", "上海", "北京", "上海"],
    "季度": ["Q1", "Q1", "Q1", "Q1", "Q2", "Q2"],
    "薪资": [15000, 20000, 18000, 22000, 16000, 19000]
})

# pivot_table
pivot = pd.pivot_table(
    df,
    values="薪资",
    index="部门",
    columns="城市",
    aggfunc="mean",
    fill_value=0,
    margins=True  # 显示总计
)

# 多级透视
pd.pivot_table(
    df,
    values="薪资",
    index=["部门", "季度"],
    columns="城市",
    aggfunc=["mean", "sum"]
)

# stack / unstack
stacked = df.set_index(["部门", "城市"]).stack()
unstacked = stacked.unstack()
```

## 十一、时间序列

```python
# 创建时间索引
dates = pd.date_range("2024-01-01", periods=10, freq="D")
ts = pd.Series(np.random.randn(10), index=dates)

# 频率
pd.date_range("2024-01-01", periods=12, freq="M")   # 月末
pd.date_range("2024-01-01", periods=12, freq="MS")  # 月初
pd.date_range("2024-01-01", periods=4, freq="Q")    # 季度末
pd.date_range("2024-01-01", periods=3, freq="Y")    # 年末
pd.date_range("2024-01-01", periods=6, freq="2H")   # 每2小时

# 时间索引操作
ts["2024"]
ts["2024-01"]
ts["2024-01-01":"2024-01-05"]

# 重采样
ts.resample("W").mean()       # 周均值
ts.resample("M").sum()        # 月总和
ts.resample("Q").ohlc()       # 季度OHLC

# 移动窗口
ts.rolling(window=3).mean()
ts.rolling(window=3, min_periods=1).mean()
ts.ewm(span=3).mean()         # 指数加权移动平均

# 移位
ts.shift(1)        # 向后移1期
ts.diff()          # 差分
ts.pct_change()    # 百分比变化
```

## 十二、绘图

```python
import matplotlib.pyplot as plt

# 开启中文支持
plt.rcParams["font.sans-serif"] = ["SimHei"]
plt.rcParams["axes.unicode_minus"] = False

# Series 绘图
ts = pd.Series(np.random.randn(100), index=pd.date_range("2024-01-01", periods=100))
ts.plot(title="时间序列图")
plt.show()

# DataFrame 绘图
df = pd.DataFrame(np.random.randn(100, 3), columns=["A", "B", "C"])
df.plot()                # 折线图
df.plot(kind="bar")      # 柱状图
df.plot(kind="hist")     # 直方图
df.plot(kind="scatter", x="A", y="B")  # 散点图
df.plot(kind="box")      # 箱线图
df.plot(kind="kde")      # 核密度图
df.plot(kind="area")     # 面积图

# 子图
df.plot(subplots=True, layout=(2, 2), figsize=(12, 8))

# 保存
plt.savefig("plot.png", dpi=300, bbox_inches="tight")
```

## 十三、实用示例

```python
# 1. 数据清洗管道
def clean_data(df):
    df = df.copy()
    df.columns = df.columns.str.strip().str.lower()
    df = df.drop_duplicates()
    df = df.fillna(method="ffill")
    date_cols = df.select_dtypes(include=["datetime64"]).columns
    for col in date_cols:
        df[f"{col}_year"] = df[col].dt.year
        df[f"{col}_month"] = df[col].dt.month
    return df

# 2. 异常值检测 (IQR)
def detect_outliers(df, column):
    Q1 = df[column].quantile(0.25)
    Q3 = df[column].quantile(0.75)
    IQR = Q3 - Q1
    lower = Q1 - 1.5 * IQR
    upper = Q3 + 1.5 * IQR
    return df[(df[column] < lower) | (df[column] > upper)]

# 3. 数据分箱
df["年龄分组"] = pd.cut(df["年龄"], bins=[0, 18, 35, 50, 100], labels=["少年", "青年", "中年", "老年"])

# 4. 随机抽样
train = df.sample(frac=0.8, random_state=42)
test = df.drop(train.index)

# 5. 特征工程
df["入职年限"] = (pd.Timestamp.now() - df["入职日期"]).dt.days / 365
df["姓名首字"] = df["姓名"].str[0]
```

> Pandas 是 Python 数据分析的核心库。建议重点掌握: 数据选择(loc/iloc)、分组聚合(groupby)、合并(merge)、缺失值处理、时间序列。配合 NumPy 和 Matplotlib 可完成绝大部分数据分析任务。
