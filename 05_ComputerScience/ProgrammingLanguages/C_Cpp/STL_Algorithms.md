# C++ STL 算法

## 非修改算法

### find / find_if / find_if_not

```cpp
#include <algorithm>
#include <vector>

vector<int> vec = {1, 2, 3, 4, 5};

auto it = find(vec.begin(), vec.end(), 3);
if (it != vec.end()) {
    cout << "找到: " << *it;  // 3
}

// 条件查找
auto it2 = find_if(vec.begin(), vec.end(), [](int x) {
    return x > 3;
});  // 4

auto it3 = find_if_not(vec.begin(), vec.end(), [](int x) {
    return x < 4;
});  // 4
```

### count / count_if

```cpp
vector<int> vec = {1, 2, 2, 3, 2, 4};

int cnt = count(vec.begin(), vec.end(), 2);      // 3
int cnt2 = count_if(vec.begin(), vec.end(),
    [](int x) { return x % 2 == 0; });           // 3
```

### for_each

```cpp
vector<int> vec = {1, 2, 3, 4, 5};

for_each(vec.begin(), vec.end(), [](int& x) {
    x *= 2;
});  // vec = {2, 4, 6, 8, 10}

int sum = 0;
for_each(vec.begin(), vec.end(), [&sum](int x) {
    sum += x;
});  // sum = 30
```

### all_of / any_of / none_of

```cpp
vector<int> vec = {2, 4, 6, 8, 10};

bool allEven = all_of(vec.begin(), vec.end(),
    [](int x) { return x % 2 == 0; });     // true

bool anyOdd = any_of(vec.begin(), vec.end(),
    [](int x) { return x % 2 != 0; });     // false

bool noneNegative = none_of(vec.begin(), vec.end(),
    [](int x) { return x < 0; });          // true
```

## 修改算法

### copy / copy_if

```cpp
vector<int> src = {1, 2, 3, 4, 5};
vector<int> dest(5);

copy(src.begin(), src.end(), dest.begin());

// 条件复制
vector<int> evens;
copy_if(src.begin(), src.end(),
    back_inserter(evens), [](int x) {
        return x % 2 == 0;
    });  // evens = {2, 4}

// n 个元素复制
copy_n(src.begin(), 3, dest.begin());  // {1, 2, 3, ?, ?}
```

### transform

```cpp
vector<int> vec = {1, 2, 3, 4, 5};
vector<int> result(5);

// 一元转换
transform(vec.begin(), vec.end(), result.begin(),
    [](int x) { return x * x; });  // {1, 4, 9, 16, 25}

// 二元转换
vector<int> a = {1, 2, 3}, b = {4, 5, 6}, c(3);
transform(a.begin(), a.end(), b.begin(), c.begin(),
    [](int x, int y) { return x + y; });  // {5, 7, 9}
```

### replace / replace_if

```cpp
vector<int> vec = {1, 2, 3, 2, 4, 2};

replace(vec.begin(), vec.end(), 2, 99);
// {1, 99, 3, 99, 4, 99}

replace_if(vec.begin(), vec.end(),
    [](int x) { return x > 3; }, 0);
```

### fill / fill_n

```cpp
vector<int> vec(5);
fill(vec.begin(), vec.end(), 42);         // {42, 42, 42, 42, 42}
fill_n(vec.begin(), 3, 0);                // {0, 0, 0, 42, 42}
```

### remove / remove_if

注意：remove 并不会删除元素，而是将符合条件的元素移到末尾，返回新的 logical end。

```cpp
vector<int> vec = {1, 2, 3, 2, 4, 2};

auto newEnd = remove(vec.begin(), vec.end(), 2);
vec.erase(newEnd, vec.end());               // erase-remove idiom
// vec = {1, 3, 4}

// remove_if + erase
vec.erase(
    remove_if(vec.begin(), vec.end(),
        [](int x) { return x % 2 == 0; }),
    vec.end()
);
```

### unique

去除连续重复元素。

```cpp
vector<int> vec = {1, 1, 2, 2, 3, 1, 1};

auto newEnd = unique(vec.begin(), vec.end());
vec.erase(newEnd, vec.end());
// {1, 2, 3, 1} （只去除连续重复）

// 先排序再 unique 去重
sort(vec.begin(), vec.end());
vec.erase(unique(vec.begin(), vec.end()), vec.end());
```

## 排序算法

### sort / stable_sort

```cpp
vector<int> vec = {5, 2, 8, 1, 9, 3};

sort(vec.begin(), vec.end());                // 升序 {1, 2, 3, 5, 8, 9}
sort(vec.begin(), vec.end(), greater<int>()); // 降序
sort(vec.begin(), vec.end(), [](int a, int b) {
    return a > b;
});

// stable_sort：保持相等元素的相对顺序
struct Student {
    string name;
    int grade;
};
stable_sort(students.begin(), students.end(),
    [](const Student& a, const Student& b) {
        return a.grade > b.grade;
    });
```

### partial_sort

```cpp
vector<int> vec = {5, 2, 8, 1, 9, 3, 7, 4, 6};

// 将最小的 4 个元素排序放在前面
partial_sort(vec.begin(), vec.begin() + 4, vec.end());
// {1, 2, 3, 4, ?, ?, ?, ?, ?}

// 获取前 3 名
partial_sort(vec.begin(), vec.begin() + 3, vec.end(), greater<int>());
// {9, 8, 7, ?, ?, ?, ?, ?, ?}
```

### nth_element

将第 n 个元素放在正确位置，左侧都不大于它，右侧都不小于它。

```cpp
vector<int> vec = {5, 2, 8, 1, 9, 3, 7, 4, 6};

nth_element(vec.begin(), vec.begin() + 4, vec.end());
// vec[4] 是第 5 小的元素（排序后的正确位置）
// 左侧 4 个都 <= vec[4]，右侧都 >= vec[4]

// 查找中位数
nth_element(vec.begin(), vec.begin() + vec.size()/2, vec.end());
int median = vec[vec.size()/2];
```

## 二分查找（需有序容器）

### binary_search

```cpp
vector<int> vec = {1, 2, 3, 4, 5, 6, 7};

bool found = binary_search(vec.begin(), vec.end(), 4);  // true
bool found2 = binary_search(vec.begin(), vec.end(), 8); // false
```

### lower_bound / upper_bound

```cpp
vector<int> vec = {1, 2, 2, 2, 3, 4, 5};

auto lower = lower_bound(vec.begin(), vec.end(), 2);
// 第一个 >= 2 的位置（index 1）

auto upper = upper_bound(vec.begin(), vec.end(), 2);
// 第一个 > 2 的位置（index 4）

// 等于 2 的范围
auto [low, up] = equal_range(vec.begin(), vec.end(), 2);
// [low, up) 包含所有 2

// 实际应用：统计某个值的出现次数
int count = upper - lower;  // 3
```

### equal_range

```cpp
auto range = equal_range(vec.begin(), vec.end(), 2);
// 等价于 make_pair(lower_bound(...), upper_bound(...))

for (auto it = range.first; it != range.second; ++it) {
    cout << *it << " ";  // 2 2 2
}
```

## 数值算法

### accumulate

```cpp
#include <numeric>

vector<int> vec = {1, 2, 3, 4, 5};

int sum = accumulate(vec.begin(), vec.end(), 0);     // 15
int product = accumulate(vec.begin(), vec.end(), 1,
    multiplies<int>());                                // 120
string concat = accumulate(vec.begin(), vec.end(),
    string(""), [](string& s, int x) {
        return s + to_string(x);
    });  // "12345"
```

### inner_product

```cpp
vector<int> a = {1, 2, 3};
vector<int> b = {4, 5, 6};

int dot = inner_product(a.begin(), a.end(), b.begin(), 0);
// 1*4 + 2*5 + 3*6 = 32
```

### partial_sum / adjacent_difference

```cpp
vector<int> vec = {1, 2, 3, 4, 5};
vector<int> result(5);

partial_sum(vec.begin(), vec.end(), result.begin());
// {1, 1+2=3, 3+3=6, 6+4=10, 10+5=15}

adjacent_difference(vec.begin(), vec.end(), result.begin());
// {1, 2-1=1, 3-2=1, 4-3=1, 5-4=1}
```

## 最小/最大算法

```cpp
int a = 10, b = 20;
int m = min(a, b);            // 10
int M = max(a, b);            // 20
auto [minVal, maxVal] = minmax(a, b);  // {10, 20}

vector<int> vec = {5, 2, 8, 1, 9, 3};

auto minIt = min_element(vec.begin(), vec.end());  // 指向 1
auto maxIt = max_element(vec.begin(), vec.end());  // 指向 9

auto [minIt2, maxIt2] = minmax_element(vec.begin(), vec.end());

// clamp（C++17）
int clamped = clamp(value, low, high);  // 将值限制在 [low, high]
```

## Lambda 表达式

```cpp
// 基本语法
[capture](parameters) -> return_type { body }

// 值捕获
int x = 10;
auto lambda = [x](int y) { return x + y; };
cout << lambda(5);  // 15

// 引用捕获
auto lambda2 = [&x](int y) { x += y; };
lambda2(5);
cout << x;  // 15

// 全部值捕获
auto byValue = [=]() { /* 捕获所有外部变量副本 */ };

// 全部引用捕获
auto byRef = [&]() { /* 捕获所有外部变量引用 */ };

// 混合捕获
auto mixed = [=, &x]() { /* x 引用捕获，其余值捕获 */ };

// 泛型 lambda（C++14）
auto generic = [](auto a, auto b) { return a + b; };

// 可变 lambda（可修改捕获的值）
int count = 0;
auto counter = [count]() mutable { return ++count; };
cout << counter();  // 1
cout << counter();  // 2（每次调用修改的是 lambda 内部的副本）

// 算法中使用
sort(vec.begin(), vec.end(),
    [](int a, int b) { return a > b; });

auto it = find_if(vec.begin(), vec.end(),
    [threshold](int x) { return x > threshold; });
```
