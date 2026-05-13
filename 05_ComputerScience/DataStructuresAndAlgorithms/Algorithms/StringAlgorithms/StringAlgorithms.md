# String Algorithms - 字符串算法

## 一、字符串匹配

### 朴素匹配

```python
def naive_search(text, pattern):
    """O(nm) 暴力匹配"""
    n, m = len(text), len(pattern)
    for i in range(n - m + 1):
        j = 0
        while j < m and text[i + j] == pattern[j]:
            j += 1
        if j == m:
            return i
    return -1
```

时间复杂度：$O(nm)$，其中 $n$ 为文本长度，$m$ 为模式长度。

### KMP 算法

KMP（Knuth-Morris-Pratt）通过预处理模式串的前缀函数，避免回溯文本指针。

**前缀函数 $\pi[i]$**：

$$ \pi[i] = \max\{ k \mid 0 \leq k < i \text{ 且 } s[0..k-1] = s[i-k..i-1] \} $$

即 $\pi[i]$ 是子串 $s[0..i]$ 的最长相等真前缀和真后缀的长度。

**失配函数递推**：

$$ \pi[i] = \begin{cases}
\pi[i-1] + 1, & s[i] = s[\pi[i-1]] \\
0, & \text{否则且无更短匹配} \\
\pi[\pi[i-1]-1] + 1, & \text{回退后匹配}
\end{cases} $$

匹配过程失配时，$j = \pi[j-1]$，其中 $j$ 为当前模式串匹配位置。

```python
def compute_lps(pattern):
    """计算最长公共前后缀数组 (π)"""
    m = len(pattern)
    lps = [0] * m
    length = 0  # 当前最长公共前后缀长度
    i = 1

    while i < m:
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1
        elif length != 0:
            length = lps[length - 1]  # 回退
        else:
            lps[i] = 0
            i += 1

    return lps

def kmp_search(text, pattern):
    """KMP 字符串匹配"""
    n, m = len(text), len(pattern)
    if m == 0:
        return 0

    lps = compute_lps(pattern)
    i = j = 0  # i 是文本索引，j 是模式索引

    while i < n:
        if text[i] == pattern[j]:
            i += 1
            j += 1

        if j == m:
            return i - j  # 匹配成功
        elif i < n and text[i] != pattern[j]:
            if j != 0:
                j = lps[j - 1]  # 利用 π 回退
            else:
                i += 1

    return -1
```

| 步骤 | 操作 |
|------|------|
| 1 | 计算模式串的 $\pi$ 数组（$O(m)$） |
| 2 | 文本与模式匹配，失配时 $j = \pi[j-1]$ |
| 时间复杂度 | $O(n + m)$ |
| 空间复杂度 | $O(m)$ |

---

## 二、Rabin-Karp 算法

基于**滚动哈希**的字符串匹配算法。

### 滚动哈希

$$ h(s) = \sum_{i=0}^{m-1} s[i] \cdot p^{i} \bmod M $$

等价形式（高位在前）：$h = \sum_{i=0}^{m-1} c_i \cdot b^{m-1-i} \bmod M$，滚动更新时：$h = (h - c_0 \cdot b^{m-1}) \cdot b + c_m \bmod M$

```python
def rabin_karp(text, pattern, d=256, q=101):
    """Rabin-Karp 滚动哈希匹配"""
    n, m = len(text), len(pattern)
    if m > n:
        return -1

    h = pow(d, m - 1, q)  # d^(m-1) mod q
    p_hash = 0  # 模式串哈希
    t_hash = 0  # 文本窗口哈希

    for i in range(m):
        p_hash = (d * p_hash + ord(pattern[i])) % q
        t_hash = (d * t_hash + ord(text[i])) % q

    for i in range(n - m + 1):
        if p_hash == t_hash:
            if text[i:i + m] == pattern:  # 哈希碰撞检查
                return i

        if i < n - m:
            t_hash = (d * (t_hash - ord(text[i]) * h) + ord(text[i + m])) % q
            if t_hash < 0:
                t_hash += q

    return -1
```

| 特性 | 说明 |
|------|------|
| 平均时间复杂度 | $O(n + m)$ |
| 最坏时间复杂度 | $O(nm)$（哈希碰撞时） |
| 空间复杂度 | $O(1)$ |
| 优点 | 适合多模式匹配、二维匹配 |

---

## 三、Boyer-Moore 算法

从右向左匹配，利用两个启发式规则跳过尽可能多的字符。

### 坏字符规则（Bad Character Rule）

```
文本:  ...GCAATGCCTATGTG...
模式:   ATGTG
              ↑ 失配 (C vs T)
模式中 T 在位置 4，C 不在模式中 → 移动 4 位
```

### 好后缀规则（Good Suffix Rule）

```
文本:  ...CGTGCCTACCTTA...
模式:   CCTTA
         ↑ 失配 (G vs C)
"TTA" 是已匹配的后缀，查找模式中前一个 "TTA" → 移动对齐
```

```python
def boyer_moore(text, pattern):
    """Boyer-Moore 字符串匹配（简化版）"""
    n, m = len(text), len(pattern)
    if m == 0:
        return 0

    # 坏字符表
    bad_char = {c: m for c in set(text)}
    for i in range(m - 1):
        bad_char[pattern[i]] = m - 1 - i

    i = 0
    while i <= n - m:
        j = m - 1
        while j >= 0 and pattern[j] == text[i + j]:
            j -= 1
        if j < 0:
            return i
        shift = bad_char.get(text[i + j], m)
        i += max(1, shift - (m - 1 - j))

    return -1
```

| 特性 | 值 |
|------|----|
| 最坏时间复杂度 | $O(nm)$ |
| 平均时间复杂度 | $O(n/m)$ 或更优 |
| 空间复杂度 | $O(\Sigma)$（字母表大小） |

---

## 四、后缀数组与 LCP 数组

### 后缀数组构建

后缀数组 $SA$ 是字符串所有后缀按字典序排列的起始位置数组。

```text
字符串: "banana"
后缀:     排序后:
banana    a         → (5)
anana     ana       → (3)
nana      anana     → (1)
ana       banana    → (0)
na        na        → (4)
a         nana      → (2)

SA = [5, 3, 1, 0, 4, 2]
```

### DC3 / SA-IS 算法

- **DC3（Difference Cover Mod 3）**：$O(n)$ 时间
- **SA-IS**：$O(n)$ 时间，更简洁

### Kasai 算法（LCP 数组）

LCP 数组存储 $SA[i]$ 和 $SA[i-1]$ 的最长公共前缀长度。

```python
def kasai(s, sa):
    """计算 LCP 数组 — O(n)"""
    n = len(s)
    rank = [0] * n
    for i in range(n):
        rank[sa[i]] = i

    lcp = [0] * (n - 1)
    k = 0
    for i in range(n):
        if rank[i] == n - 1:
            k = 0
            continue
        j = sa[rank[i] + 1]
        while i + k < n and j + k < n and s[i + k] == s[j + k]:
            k += 1
        lcp[rank[i]] = k
        if k:
            k -= 1

    return lcp
```

| 应用 | 方法 |
|------|------|
| 最长重复子串 | max(LCP) |
| 最长公共子串 | 拼接+DC3+LCP+滑动窗口 |
| 不同子串数 | $\frac{n(n+1)}{2} - \sum LCP[i]$ |
| 子串出现次数 | 二分 LCP 区间 |

---

## 五、后缀树

后缀树是压缩后的前缀树（Trie），包含字符串所有后缀。

### Ukkonen 算法

Ukkonen 算法在 $O(n)$ 时间内在线构建后缀树。

```text
核心概念：
    - 隐式后缀树 → 通过扩展规则逐步构建
    - 活动点 (active_point) = (node, edge, length)
    - 后缀链接 (suffix_link) → 加速转移
    - 三规则：
        1. 延伸已有边
        2. 创建新叶节点
        3. 分裂边 + 创建内部节点
```

后缀树 vs 后缀数组：

| 特性 | 后缀树 | 后缀数组 |
|------|--------|---------|
| 构建时间 | $O(n)$ | $O(n)$ |
| 空间 | 较大（常数倍） | 紧凑（$n$ 整数） |
| 模式匹配 | $O(m)$ | $O(m \log n)$ |
| 使用难度 | 实现复杂 | 实现简单 |

---

## 六、Trie 字典树

```python
class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end = False

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word):
        node = self.root
        for c in word:
            if c not in node.children:
                node.children[c] = TrieNode()
            node = node.children[c]
        node.is_end = True

    def search(self, word):
        node = self.root
        for c in word:
            if c not in node.children:
                return False
            node = node.children[c]
        return node.is_end

    def starts_with(self, prefix):
        node = self.root
        for c in prefix:
            if c not in node.children:
                return False
            node = node.children[c]
        return True
```

### Aho-Corasick 自动机

多模式匹配算法，在 Trie 上添加 fail 指针自动机。

```python
class AhoCorasick:
    def __init__(self):
        self.children = [{}]
        self.fail = [0]
        self.output = [[]]

    def add_word(self, word, idx):
        node = 0
        for c in word:
            if c not in self.children[node]:
                self.children[node][c] = len(self.children)
                self.children.append({})
                self.fail.append(0)
                self.output.append([])
            node = self.children[node][c]
        self.output[node].append(idx)

    def build(self):
        """构建 fail 指针（BFS）"""
        from collections import deque
        q = deque()
        for c, v in self.children[0].items():
            q.append(v)
            self.fail[v] = 0
        while q:
            r = q.popleft()
            for c, u in self.children[r].items():
                q.append(u)
                f = self.fail[r]
                while f and c not in self.children[f]:
                    f = self.fail[f]
                self.fail[u] = self.children[f][c] if c in self.children[f] else 0
                self.output[u].extend(self.output[self.fail[u]])

    def search(self, text):
        """多模式匹配"""
        node = 0
        results = []
        for i, c in enumerate(text):
            while node and c not in self.children[node]:
                node = self.fail[node]
            node = self.children[node].get(c, 0)
            for idx in self.output[node]:
                results.append((i, idx))
        return results
```

| 特性 | 值 |
|------|----|
| 预处理 | $O(\sum |P_i|)$ |
| 匹配 | $O(n + \text{matches})$ |
| 适用 | 多关键词过滤、敏感词检测 |

---

## 七、Z-算法

Z-算法计算每个位置与字符串前缀的最长匹配长度。

$$ Z[i] = \max\{k \mid s[0..k-1] = s[i..i+k-1]\} $$

```python
def z_algorithm(s):
    """计算 Z 数组 — O(n)"""
    n = len(s)
    z = [0] * n
    l = r = 0

    for i in range(1, n):
        if i <= r:
            z[i] = min(r - i + 1, z[i - l])
        while i + z[i] < n and s[z[i]] == s[i + z[i]]:
            z[i] += 1
        if i + z[i] - 1 > r:
            l, r = i, i + z[i] - 1

    z[0] = n
    return z
```

```text
应用：
    - 字符串匹配：text 拼接到 pattern 后 → Z[i] == m
    - 最长回文前缀：s + '#' + reverse(s)
    - 字符串周期：n % (n - Z[n - 1]) == 0 → 周期 = n - Z[n-1]
```

---

## 八、Manacher 算法

Manacher 算法在线性时间内找出字符串的所有回文子串。

```python
def manacher(s):
    """最长回文子串 — O(n)"""
    # 插入分隔符
    t = '#' + '#'.join(s) + '#'
    n = len(t)
    p = [0] * n
    center = right = 0

    for i in range(n):
        if i < right:
            mirror = 2 * center - i
            p[i] = min(right - i, p[mirror])

        while i - p[i] - 1 >= 0 and i + p[i] + 1 < n and t[i - p[i] - 1] == t[i + p[i] + 1]:
            p[i] += 1

        if i + p[i] > right:
            center = i
            right = i + p[i]

    # 找到最大回文
    max_len = max(p)
    center_idx = p.index(max_len)
    start = (center_idx - max_len) // 2
    return s[start:start + max_len]
```

| 特性 | 值 |
|------|----|
| 时间复杂度 | $O(n)$ |
| 空间复杂度 | $O(n)$ |
| 结果 | 所有回文子串信息在 $p$ 数组中 |

---

## 九、字符串哈希

```python
class StringHasher:
    def __init__(self, s, base=131, mod=10**9 + 7):
        self.n = len(s)
        self.base = base
        self.mod = mod
        self.prefix = [0] * (self.n + 1)
        self.pow = [1] * (self.n + 1)

        for i, c in enumerate(s):
            self.prefix[i + 1] = (self.prefix[i] * base + ord(c)) % mod
            self.pow[i + 1] = (self.pow[i] * base) % mod

    def get_hash(self, l, r):
        """获取区间 [l, r) 的哈希值"""
        return (self.prefix[r] - self.prefix[l] * self.pow[r - l]) % self.mod
```

**双哈希**：使用两个模数降低碰撞概率。

| 应用 | 方法 |
|------|------|
| 子串比较 | 比较 hash(l1, r1) == hash(l2, r2) |
| 最长回文 | 正反哈希 + 二分 |
| 最长重复子串 | 哈希 + 二分长度 |
| 字符串匹配 | 计算 pattern 哈希，滑动文本窗口 |

---

## 十、编辑距离与最长公共子序列

### 编辑距离 (Levenshtein Distance)

$$ D[i][j] = \begin{cases}
0, & i = 0 \text{ 且 } j = 0 \\
i, & j = 0 \\
j, & i = 0 \\
D[i-1][j-1], & s_1[i] = s_2[j] \\
1 + \min(D[i-1][j], D[i][j-1], D[i-1][j-1]), & \text{其他}
\end{cases} $$

其中 $D[i][j]$ 表示 $s_1[1..i]$ 和 $s_2[1..j]$ 的最小编辑距离。

### 最长公共子序列 (Longest Common Subsequence)

$$ L[i][j] = \begin{cases}
0, & i = 0 \text{ 或 } j = 0 \\
L[i-1][j-1] + 1, & s_1[i] = s_2[j] \\
\max(L[i-1][j], L[i][j-1]), & \text{其他}
\end{cases} $$

详见 [动态规划笔记](../DynamicProgramming/DynamicProgramming.md)。

### 最长公共子串

```python
def longest_common_substring(s1, s2):
    """最长公共子串 — DP"""
    m, n = len(s1), len(s2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    max_len = 0
    end_pos = 0

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s1[i - 1] == s2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
                if dp[i][j] > max_len:
                    max_len = dp[i][j]
                    end_pos = i

    return s1[end_pos - max_len:end_pos]
```

### 正则表达式匹配

```python
def regex_match(s, p):
    """支持 '.' 和 '*' 的正则匹配"""
    m, n = len(s), len(p)
    dp = [[False] * (n + 1) for _ in range(m + 1)]
    dp[0][0] = True

    for j in range(2, n + 1):
        if p[j - 1] == '*':
            dp[0][j] = dp[0][j - 2]

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if p[j - 1] == '.' or p[j - 1] == s[i - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            elif p[j - 1] == '*':
                dp[i][j] = dp[i][j - 2]   # 匹配 0 次
                if p[j - 2] == '.' or p[j - 2] == s[i - 1]:
                    dp[i][j] = dp[i][j] or dp[i - 1][j]  # 匹配 ≥1 次

    return dp[m][n]
```

---

## 十一、算法速查表

| 算法 | 时间复杂度 | 空间复杂度 | 主要应用 |
|------|-----------|-----------|---------|
| 朴素匹配 | $O(nm)$ | $O(1)$ | 短模式串 |
| KMP | $O(n+m)$ | $O(m)$ | 单模式匹配 |
| Rabin-Karp | $O(n+m)$ 平均 | $O(1)$ | 多模式/滚动哈希 |
| Boyer-Moore | $O(n/m)$ 平均 | $O(\Sigma)$ | 长模式串 |
| 后缀数组 (DC3) | $O(n)$ | $O(n)$ | 多种字符串问题 |
| 后缀树 | $O(n)$ | $O(n)$ | 模式匹配、LCS |
| Trie | $O(\sum |P|)$ | $O(\sum |P|)$ | 前缀查询 |
| Aho-Corasick | $O(n+m+\text{matches})$ | $O(m)$ | 多模式匹配 |
| Z-算法 | $O(n)$ | $O(n)$ | 字符串匹配、周期 |
| Manacher | $O(n)$ | $O(n)$ | 回文子串 |

## 相关条目

- [[模式匹配与字符串处理]]
- [[BasicAlgorithms]]
- [[Trie]]
- [[Sorting]]
- [[Tree]]

## 参考资源

- Knuth, D. E., Morris, J. H., & Pratt, V. R. (1977). Fast Pattern Matching in Strings. SIAM Journal on Computing.
- Manacher, G. (1975). A New Linear-Time "On-Line" Algorithm for Finding the Smallest Initial Palindrome. JACM.
- Ukkonen, E. (1995). On-Line Construction of Suffix Trees. Algorithmica.
- Aho, A. V. & Corasick, M. J. (1975). Efficient String Matching: An Aid to Bibliographic Search. CACM.
- Gusfield, D. (1997). Algorithms on Strings, Trees, and Sequences. Cambridge University Press.
