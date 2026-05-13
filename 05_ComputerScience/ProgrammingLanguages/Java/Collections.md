# Java 集合框架

## 集合层次结构

```
Iterable
  └── Collection
        ├── List（有序、可重复）
        ├── Set（无序、不可重复）
        └── Queue（队列）

Map（单独的接口）
  ├── HashMap
  ├── TreeMap
  └── ...
```

## List 接口

### ArrayList

基于动态数组实现。随机访问 O(1)，插入/删除 O(n)。

```java
List<String> list = new ArrayList<>();
list.add("Apple");
list.add("Banana");
list.add(1, "Orange");         // 指定位置插入
String fruit = list.get(0);    // 随机访问
list.set(1, "Grape");          // 修改
list.remove(0);                // 按索引删除
list.remove("Banana");         // 按对象删除

// 遍历
for (String s : list) { }
list.forEach(System.out::println);
list.stream().filter(s -> s.startsWith("A")).collect(Collectors.toList());
```

### LinkedList

基于双向链表实现。插入/删除 O(1)，随机访问 O(n)。同时也实现了 Deque。

```java
LinkedList<String> linkedList = new LinkedList<>();
linkedList.addFirst("First");     // 头部添加
linkedList.addLast("Last");       // 尾部添加
linkedList.getFirst();            // 获取头部
linkedList.getLast();             // 获取尾部
linkedList.removeFirst();         // 移除头部
linkedList.removeLast();          // 移除尾部
```

### ArrayList vs LinkedList

| 操作 | ArrayList | LinkedList |
|------|-----------|------------|
| get(int index) | O(1) | O(n) |
| add(E) | O(1) 均摊 | O(1) |
| add(int, E) | O(n) | O(1) |
| remove(int) | O(n) | O(1) |
| 内存开销 | 较小 | 较大（存储前后指针） |

## Set 接口

### HashSet

基于 HashMap 实现，无序，允许 null。

```java
Set<String> set = new HashSet<>();
set.add("Apple");
set.add("Banana");
set.add("Apple");        // 不会重复添加
set.contains("Apple");   // true
set.size();              // 2
set.remove("Banana");
```

### LinkedHashSet

维护插入顺序，基于 LinkedHashMap。

```java
Set<String> linkedSet = new LinkedHashSet<>();
linkedSet.add("C");
linkedSet.add("A");
linkedSet.add("B");
// 遍历顺序: C, A, B（与插入顺序一致）
```

### TreeSet

基于 TreeMap（红黑树），元素按自然顺序或 Comparator 排序。

```java
Set<Integer> treeSet = new TreeSet<>();
treeSet.add(3);
treeSet.add(1);
treeSet.add(2);
// 遍历顺序: 1, 2, 3（已排序）

// 自定义排序
Set<String> customSet = new TreeSet<>(Comparator.reverseOrder());
customSet.add("A");
customSet.add("B");  // 遍历顺序: B, A

// 范围查询
TreeSet<Integer> ts = new TreeSet<>(Set.of(1, 3, 5, 7, 9));
ts.first();           // 1
ts.last();            // 9
ts.lower(5);          // 3（小于5的最大元素）
ts.higher(5);         // 7（大于5的最小元素）
ts.subSet(3, 7);      // [3, 5]（3到7的子集）
```

## Queue / Deque

### LinkedList（Queue 实现）

```java
Queue<String> queue = new LinkedList<>();
queue.offer("A");          // 入队
queue.offer("B");
queue.poll();              // 出队 -> "A"
queue.peek();              // 查看队首 -> "B"
```

### ArrayDeque

循环数组实现，比 LinkedList 更高效。可用作栈或双端队列。

```java
Deque<String> stack = new ArrayDeque<>();
stack.push("A");           // 入栈
stack.push("B");
stack.pop();               // 出栈 -> "B"
stack.peek();              // 查看栈顶 -> "A"

Deque<String> deque = new ArrayDeque<>();
deque.addFirst("A");
deque.addLast("B");
deque.removeFirst();
deque.removeLast();
```

### PriorityQueue

基于堆（Heap）实现，默认小顶堆。

```java
Queue<Integer> pq = new PriorityQueue<>();
pq.offer(5);
pq.offer(1);
pq.offer(3);
pq.poll();    // 1（最小元素）

// 大顶堆
Queue<Integer> maxHeap = new PriorityQueue<>(Comparator.reverseOrder());
maxHeap.offer(5);
maxHeap.offer(1);
maxHeap.offer(3);
maxHeap.poll();    // 5

// 自定义对象
Queue<Task> taskQueue = new PriorityQueue<>(
    Comparator.comparingInt(Task::getPriority)
);
```

## Map 接口

### HashMap

基于数组+链表+红黑树实现。允许一个 null key 和多个 null value。

```java
Map<String, Integer> map = new HashMap<>();
map.put("Apple", 10);
map.put("Banana", 20);
map.put("Apple", 15);       // 覆盖旧值

int val = map.get("Apple");          // 15
int val2 = map.getOrDefault("Orange", 0);  // 0

map.containsKey("Apple");    // true
map.containsValue(15);      // true

// 遍历
for (Map.Entry<String, Integer> entry : map.entrySet()) {
    System.out.println(entry.getKey() + ": " + entry.getValue());
}
map.forEach((k, v) -> System.out.println(k + ": " + v));

// 并发安全
Map<String, Integer> syncMap = Collections.synchronizedMap(new HashMap<>());
```

#### HashMap 扩容机制

- 默认容量 16，负载因子 0.75
- 当 size > capacity * loadFactor 时，扩容为原来的 2 倍
- 树化：链表长度 > 8 且容量 >= 64 时转为红黑树

### LinkedHashMap

维护插入顺序或访问顺序。

```java
// 插入顺序
Map<String, Integer> insertionMap = new LinkedHashMap<>();
insertionMap.put("C", 3);
insertionMap.put("A", 1);
insertionMap.put("B", 2);
// 遍历: C, A, B

// 访问顺序（可用于 LRU 缓存）
Map<String, Integer> accessMap = new LinkedHashMap<>(16, 0.75f, true);
accessMap.put("A", 1);
accessMap.put("B", 2);
accessMap.put("C", 3);
accessMap.get("A");  // 此时 A 移至末尾
```

### TreeMap

基于红黑树，key 按自然顺序或 Comparator 排序。

```java
TreeMap<String, Integer> treeMap = new TreeMap<>();
treeMap.put("C", 3);
treeMap.put("A", 1);
treeMap.put("B", 2);
// 遍历顺序: A, B, C

treeMap.firstKey();      // "A"
treeMap.lastKey();       // "C"
treeMap.lowerKey("B");   // "A"
treeMap.higherKey("B");  // "C"
treeMap.subMap("A", "C"); // {"A"=1, "B"=2}
```

### ConcurrentHashMap

线程安全的 HashMap，采用分段锁或 CAS 机制。

```java
ConcurrentHashMap<String, Integer> concurrentMap = new ConcurrentHashMap<>();
concurrentMap.put("A", 1);
concurrentMap.putIfAbsent("A", 2);  // 不会覆盖，key 已存在
concurrentMap.computeIfAbsent("B", k -> computeValue(k));
```

## equals() 和 hashCode()

重写 equals 必须重写 hashCode。约定：
- equals 相等 → hashCode 必须相等
- hashCode 相等 → equals 不一定相等（哈希冲突）

```java
public class Person {
    private final String name;
    private final int age;

    public Person(String name, int age) {
        this.name = name;
        this.age = age;
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        Person person = (Person) o;
        return age == person.age && Objects.equals(name, person.name);
    }

    @Override
    public int hashCode() {
        return Objects.hash(name, age);
    }
}
```

## Collections 工具类

```java
List<String> list = new ArrayList<>();

Collections.addAll(list, "A", "B", "C");
Collections.sort(list);
Collections.sort(list, Comparator.reverseOrder());
Collections.binarySearch(list, "B");    // 二分搜索（需已排序）
Collections.shuffle(list);               // 随机打乱
Collections.reverse(list);               // 反转
Collections.fill(list, "X");             // 全部填充
Collections.copy(dest, src);             // 拷贝
Collections.swap(list, 0, 1);            // 交换
Collections.frequency(list, "A");        // 出现次数
Collections.max(list);                   // 最大值
Collections.min(list);                   // 最小值
Collections.unmodifiableList(list);      // 返回不可变视图
Collections.synchronizedList(list);      // 返回线程安全包装
```

## Comparable vs Comparator

### Comparable（内部比较器）

```java
public class Student implements Comparable<Student> {
    private final String name;
    private final int score;

    @Override
    public int compareTo(Student other) {
        return Integer.compare(this.score, other.score);
    }
}

// 使用
List<Student> students = ...;
Collections.sort(students);  // 按 score 升序
```

### Comparator（外部比较器）

```java
// 匿名类
Collections.sort(list, new Comparator<Student>() {
    @Override
    public int compare(Student a, Student b) {
        return a.getName().compareTo(b.getName());
    }
});

// Lambda
list.sort((a, b) -> a.getName().compareTo(b.getName()));

// Comparator 工具方法
list.sort(Comparator.comparing(Student::getName));
list.sort(Comparator.comparingInt(Student::getScore).reversed());
list.sort(Comparator.comparing(Student::getName)
        .thenComparingInt(Student::getScore));
```

## 快速参考表

| 集合类 | 底层结构 | 有序 | 线程安全 | 允许null | 时间复杂度 |
|--------|---------|------|---------|---------|-----------|
| ArrayList | 动态数组 | 插入顺序 | 否 | 是 | get/set O(1), add/remove O(n) |
| LinkedList | 双向链表 | 插入顺序 | 否 | 是 | get O(n), add/remove O(1) |
| HashSet | HashMap | 否 | 否 | 允许null | add/remove/contains O(1) |
| LinkedHashSet | LinkedHashMap | 插入顺序 | 否 | 允许null | add/remove/contains O(1) |
| TreeSet | TreeMap(红黑树) | 排序 | 否 | 不允许null | add/remove/contains O(log n) |
| HashMap | 数组+链表+红黑树 | 否 | 否 | 允许一个null key | get/put O(1) |
| LinkedHashMap | HashMap+双向链表 | 插入/访问顺序 | 否 | 允许一个null key | get/put O(1) |
| TreeMap | 红黑树 | 排序 | 否 | 不允许null | get/put O(log n) |
| ConcurrentHashMap | 数组+链表+红黑树+CAS | 否 | 是 | 不允许null | get/put O(1) |
| PriorityQueue | 堆 | 优先级顺序 | 否 | 不允许null | offer/poll O(log n) |
| ArrayDeque | 循环数组 | 插入顺序 | 否 | 不允许null | 两端操作 O(1) |
