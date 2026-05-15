# C++ STL 容器

## 序列容器（Sequence Containers）

### vector

动态数组，连续内存。

```cpp
#include <vector>

vector<int> vec;
vector<int> vec2(10, 0);        // 10 个 0
vector<int> vec3 = {1, 2, 3, 4, 5};

// 插入
vec.push_back(1);               // 末尾添加
vec.emplace_back(2);            // 原地构造，更高效
vec.insert(vec.begin() + 1, 99); // 指定位置插入
vec.insert(vec.end(), {10, 20});

// 访问
vec[0];                         // 不检查边界
vec.at(0);                      // 检查边界，越界抛出 out_of_range
vec.front();                    // 第一个元素
vec.back();                     // 最后一个元素

// 删除
vec.pop_back();                 // 删除末尾
vec.erase(vec.begin());         // 删除指定位置
vec.erase(vec.begin(), vec.begin() + 2); // 删除区间
vec.clear();                    // 清空

// 容量
vec.size();                     // 元素个数
vec.capacity();                 // 容量
vec.reserve(100);               // 预留空间
vec.shrink_to_fit();            // 缩减容量到 size

// 遍历
for (size_t i = 0; i < vec.size(); i++) {}
for (int v : vec) {}
for (auto it = vec.begin(); it != vec.end(); ++it) {}
```

### deque（双端队列）

```cpp
deque<int> dq = {1, 2, 3};

dq.push_front(0);               // 前端插入 O(1)
dq.push_back(4);                // 后端插入 O(1)
dq.pop_front();                 // 前端删除
dq.pop_back();                  // 后端删除
```

### list（双向链表）

```cpp
list<int> lst = {1, 2, 3, 4, 5};

lst.push_front(0);
lst.push_back(6);
lst.pop_front();
lst.pop_back();

// 特有操作
lst.sort();                     // 排序
lst.unique();                   // 去重（连续重复）
lst.reverse();                  // 反转
lst.merge(other);               // 合并（需已排序）
lst.splice(it, other);          // 移动元素
lst.remove(3);                  // 删除所有值为 3 的元素
lst.remove_if([](int x) { return x % 2 == 0; });
```

### forward_list（单链表，C++11）

```cpp
forward_list<int> fl = {1, 2, 3, 4};

fl.push_front(0);
fl.pop_front();
fl.insert_after(fl.before_begin(), -1);
fl.sort();
fl.unique();
```

### array（定长数组，C++11）

```cpp
array<int, 5> arr = {1, 2, 3, 4, 5};

arr[0];                         // 不检查边界
arr.at(0);                      // 检查边界
arr.front();
arr.back();
arr.size();                     // 编译期常量

// 支持范围 for
for (int v : arr) {}
```

### basic_string（字符串）

```cpp
string s = "Hello";
s += " World";
s.append("!");

s.insert(5, ",");
s.erase(5, 1);
s.replace(0, 5, "Hi");
s.substr(0, 5);
s.find("World");
s.rfind('o');
s.compare("Hello");
```

## 关联容器（Associative Containers）

基于红黑树实现，有序，查找 O(log n)。

### set

```cpp
set<int> s = {3, 1, 4, 1, 5, 9};  // {1, 3, 4, 5, 9}

s.insert(2);
s.emplace(6);
s.erase(3);
s.erase(s.find(4));

s.contains(5);                      // C++20
s.count(1);                         // 0 或 1
s.find(2);                          // 返回迭代器
s.lower_bound(3);                   // >= 3 的第一个元素
s.upper_bound(3);                   // > 3 的第一个元素
s.equal_range(3);                   // [lower, upper) 范围
```

### multiset

```cpp
multiset<int> ms = {1, 2, 2, 3, 3, 3};

ms.count(3);                        // 3
ms.erase(3);                        // 删除所有 3
ms.erase(ms.find(2));               // 只删除一个 2
```

### map

```cpp
map<string, int> mp;

mp["Alice"] = 25;                   // 插入
mp["Bob"] = 30;
mp.insert({"Charlie", 35});
mp.emplace("David", 40);

// 访问
int age = mp["Alice"];              // 如果 key 不存在，会创建默认值
int age2 = mp.at("Alice");          // 不存在则抛出 out_of_range
auto it = mp.find("Eve");
if (it != mp.end()) {
    cout << it->first << it->second;
}

// 遍历
for (const auto& [key, value] : mp) {  // C++17
    cout << key << ": " << value << endl;
}

// 查询
mp.contains("Alice");               // C++20
mp.count("Alice");                  // 0 或 1
mp.lower_bound("B");
mp.upper_bound("C");
```

### multimap

```cpp
multimap<string, int> mmp;

mmp.insert({"key", 1});
mmp.insert({"key", 2});
mmp.insert({"key", 3});

auto range = mmp.equal_range("key");
for (auto it = range.first; it != range.second; ++it) {
    cout << it->second << " ";       // 1 2 3
}
```

## 无序容器（Unordered Containers）

基于哈希表，无序，平均 O(1)。

### unordered_set

```cpp
unordered_set<int> us = {3, 1, 4, 1, 5};

us.insert(2);
us.erase(1);
us.contains(3);                      // O(1) 平均

// 自定义哈希
struct Person {
    string name;
    int age;
    bool operator==(const Person& o) const {
        return name == o.name && age == o.age;
    }
};

struct PersonHash {
    size_t operator()(const Person& p) const {
        return hash<string>()(p.name) ^ hash<int>()(p.age);
    }
};

unordered_set<Person, PersonHash> people;
```

### unordered_map

```cpp
unordered_map<string, int> scores;
scores["Alice"] = 95;
scores["Bob"] = 87;

// 自定义哈希
unordered_map<string, int, CustomHash> custom;
```

## 容器适配器（Container Adaptors）

### stack

```cpp
stack<int> stk;
stk.push(1);
stk.push(2);
stk.top();          // 2
stk.pop();          // 无返回值
stk.size();
stk.empty();
```

### queue

```cpp
queue<int> q;
q.push(1);
q.push(2);
q.front();          // 1
q.back();           // 2
q.pop();            // 移除 front
```

### priority_queue

默认大顶堆（最大堆）。

```cpp
// 大顶堆
priority_queue<int> pq;
pq.push(3);
pq.push(1);
pq.push(5);
pq.top();           // 5

// 小顶堆
priority_queue<int, vector<int>, greater<int>> minHeap;

// 自定义
struct Task {
    int priority;
    string name;
    bool operator<(const Task& o) const {
        return priority < o.priority;  // 大顶堆
    }
};
priority_queue<Task> taskQueue;
```

## 时间复杂度表

| 容器 | 查找 | 插入 | 删除 | 随机访问 | 末尾操作 |
|------|------|------|------|---------|---------|
| vector | O(1) | O(n) | O(n) | O(1) | O(1) 均摊 |
| deque | O(1) | O(n) | O(n) | O(1) | 两端 O(1) |
| list | O(n) | O(1) | O(1) | O(n) | 两端 O(1) |
| forward_list | O(n) | O(1) | O(1) | O(n) | 前端 O(1) |
| set/map | O(log n) | O(log n) | O(log n) | - | - |
| multiset/multimap | O(log n) | O(log n) | O(log n) | - | - |
| unordered_set/map | O(1) 平均 | O(1) 平均 | O(1) 平均 | - | - |
| priority_queue | O(1) top | O(log n) | O(log n) | - | - |
| stack/queue | O(1) top | O(1) | O(1) | - | - |

## 迭代器类别

```
Input Iterator             （istream_iterator）
  └── Forward Iterator     （forward_list, unordered_set）
        ├── Bidirectional Iterator（list, set, map）
        │     └── Random Access Iterator（vector, deque, array, string）
        └── Output Iterator（ostream_iterator）
```

```cpp
vector<int> vec = {1, 2, 3, 4, 5};

// 不同迭代器
auto it1 = vec.begin();             // iterator
auto it2 = vec.cbegin();            // const_iterator
auto it3 = vec.rbegin();            // reverse_iterator
auto it4 = vec.crbegin();           // const_reverse_iterator

// 随机访问迭代器支持
it1 + 3;
it1 - 2;
it1[2];
it1 < it1 + 2;
```
