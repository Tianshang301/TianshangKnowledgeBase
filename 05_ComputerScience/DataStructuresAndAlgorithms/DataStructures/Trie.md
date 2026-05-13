# 字典树 (Trie)

## 基本概念

字典树（Trie，也称前缀树/prefix tree）是一种多叉树结构，用于高效存储和检索**字符串集合**。每个节点表示一个字符，从根到叶子的路径组成一个字符串。

```
          root
         / | \
        a  b  c
       /   |   \
      p    a    a
     /     |     \
    p      t      t
   /       |
  l        s
 /
e

包含单词: "app", "apple", "bat", "bats", "cat"
```

## 节点结构

```python
class TrieNode:
    def __init__(self):
        self.children = {}    # 字符 -> TrieNode
        self.is_end = False   # 是否是单词结尾
        self.count = 0        # 经过此节点的单词数（可选）
        self.word_count = 0   # 以此节点为结尾的单词数（可选）
```

## 基本实现

```python
class Trie:
    def __init__(self):
        self.root = TrieNode()
    
    def insert(self, word):
        """插入单词"""
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
            node.count += 1
        node.is_end = True
        node.word_count += 1
    
    def search(self, word):
        """精确搜索单词是否存在"""
        node = self._find(word)
        return node is not None and node.is_end
    
    def starts_with(self, prefix):
        """是否存在以 prefix 为前缀的单词"""
        return self._find(prefix) is not None
    
    def _find(self, prefix):
        """查找前缀的最后一个节点"""
        node = self.root
        for char in prefix:
            if char not in node.children:
                return None
            node = node.children[char]
        return node
    
    def delete(self, word):
        """删除单词"""
        if not self.search(word):
            return
        
        node = self.root
        nodes_stack = [(node, None, None)]  # (node, char, parent)
        node = self.root
        for char in word:
            nodes_stack.append((node.children[char], char, node))
            node = node.children[char]
        
        node.is_end = False
        node.word_count -= 1
        
        # 向上清理无用节点
        for node, char, parent in reversed(nodes_stack):
            node.count -= 1
            if node.count == 0 and not node.is_end:
                if parent:
                    del parent.children[char]
    
    def count_words_with_prefix(self, prefix):
        """统计有多少单词以 prefix 为前缀"""
        node = self._find(prefix)
        return node.count if node else 0
```

## 数组优化 (C++)

C++ 中常用数组实现 Trie 以节省内存：

```cpp
class Trie {
private:
    static const int ALPHABET_SIZE = 26;
    vector<vector<int>> next;
    vector<bool> is_end;
    
public:
    Trie() {
        next.push_back(vector<int>(ALPHABET_SIZE, -1));
        is_end.push_back(false);
    }
    
    void insert(string word) {
        int node = 0;
        for (char c : word) {
            int idx = c - 'a';
            if (next[node][idx] == -1) {
                next[node][idx] = next.size();
                next.push_back(vector<int>(ALPHABET_SIZE, -1));
                is_end.push_back(false);
            }
            node = next[node][idx];
        }
        is_end[node] = true;
    }
    
    bool search(string word) {
        int node = 0;
        for (char c : word) {
            int idx = c - 'a';
            if (next[node][idx] == -1) return false;
            node = next[node][idx];
        }
        return is_end[node];
    }
    
    bool startsWith(string prefix) {
        int node = 0;
        for (char c : prefix) {
            int idx = c - 'a';
            if (next[node][idx] == -1) return false;
            node = next[node][idx];
        }
        return true;
    }
};
```

## 时间复杂度

| 操作 | 时间复杂度 |
|-----|-----------|
| 插入 (insert) | O(L) — L 为字符串长度 |
| 搜索 (search) | O(L) |
| 前缀搜索 (startsWith) | O(L) |
| 删除 (delete) | O(L) |
| 空间 | O(N × L) 最差 |

对比哈希表：
- 哈希表也支持 O(L) 搜索，但不支持前缀匹配
- Trie 在搜索前缀时比哈希表更高效
- Trie 没有哈希冲突问题

## 内存优化

```python
class TrieNodeCompressed:
    """压缩节点：减少内存占用"""
    __slots__ = ('children', 'is_end')
    
    def __init__(self):
        self.children = {}
        self.is_end = False
```

或使用字典映射替代数组：

```python
class TrieNodeDict:
    """仅存储非空子节点"""
    def __init__(self):
        self.children = {}  # char -> TrieNodeDict
        self.is_end = False
```

## 应用场景

### 1. 自动补全 (Autocomplete)

```python
class AutocompleteSystem:
    def __init__(self):
        self.trie = Trie()
    
    def insert(self, word):
        self.trie.insert(word)
    
    def autocomplete(self, prefix, limit=10):
        """根据前缀返回所有可能的完整单词"""
        node = self.trie._find(prefix)
        if not node:
            return []
        
        results = []
        self._dfs(node, list(prefix), results)
        return results[:limit]
    
    def _dfs(self, node, path, results):
        if node.is_end:
            results.append(''.join(path))
        for char in sorted(node.children.keys()):
            path.append(char)
            self._dfs(node.children[char], path, results)
            path.pop()
```

### 2. 单词搜索 II (LeetCode 212)

```python
def find_words(board, words):
    """在二维网格中搜索单词（Trie + DFS）"""
    trie = Trie()
    for word in words:
        trie.insert(word)
    
    m, n = len(board), len(board[0])
    result = set()
    visited = [[False] * n for _ in range(m)]
    
    def dfs(i, j, node, path):
        if node.is_end:
            result.add(path)
            # 可选：标记已找到，避免重复
            node.is_end = False
        
        if not (0 <= i < m and 0 <= j < n) or visited[i][j]:
            return
        
        char = board[i][j]
        if char not in node.children:
            return
        
        visited[i][j] = True
        for di, dj in [(0,1), (1,0), (0,-1), (-1,0)]:
            dfs(i + di, j + dj, node.children[char], path + char)
        visited[i][j] = False
    
    for i in range(m):
        for j in range(n):
            dfs(i, j, trie.root, "")
    
    return list(result)
```

### 3. 拼写检查

```python
class SpellChecker:
    def __init__(self):
        self.trie = Trie()
    
    def add_word(self, word):
        self.trie.insert(word)
    
    def suggest(self, word, max_distance=2):
        """返回编辑距离在 max_distance 以内的单词建议"""
        suggestions = []
        self._dfs_suggest(self.trie.root, word, 0, [], suggestions, max_distance)
        return suggestions
    
    def _dfs_suggest(self, node, word, idx, path, suggestions, max_dist):
        if node.is_end and len(word) - idx <= max_dist:
            suggestions.append(''.join(path))
            return
        
        if idx >= len(word):
            if node.is_end:
                suggestions.append(''.join(path))
            return
        
        for char, child in node.children.items():
            cost = 0 if char == word[idx] else 1
            if cost <= max_dist:
                path.append(char)
                self._dfs_suggest(child, word, idx + 1, path, suggestions, max_dist - cost)
                path.pop()
```

### 4. IP 路由 (最长前缀匹配)

```python
class IPTrie:
    """IP 路由表 — 最长前缀匹配"""
    class IPNode:
        def __init__(self):
            self.children = [None, None]
            self.next_hop = None
    
    def __init__(self):
        self.root = self.IPNode()
    
    def insert(self, ip_prefix, next_hop):
        """插入路由表项，如 "192.168.1.0/24" """
        mask_len = int(ip_prefix.split('/')[1])
        ip_int = self._ip_to_int(ip_prefix)
        
        node = self.root
        for i in range(32 - mask_len, 32):
            bit = (ip_int >> (31 - i)) & 1
            if not node.children[bit]:
                node.children[bit] = self.IPNode()
            node = node.children[bit]
        node.next_hop = next_hop
    
    def lookup(self, ip):
        """查找最匹配的路由"""
        ip_int = self._ip_to_int(ip)
        node = self.root
        result = None
        
        for i in range(32):
            bit = (ip_int >> (31 - i)) & 1
            if node.children[bit]:
                node = node.children[bit]
                if node.next_hop:
                    result = node.next_hop
            else:
                break
        
        return result
    
    def _ip_to_int(self, ip):
        parts = ip.split('/')[0].split('.')
        return (int(parts[0]) << 24) + (int(parts[1]) << 16) + \
               (int(parts[2]) << 8) + int(parts[3])
```

### 5. 最大异或对 (LeetCode 421)

```python
def find_maximum_xor(nums):
    """数组中两数最大异或值"""
    # 构建二进制 Trie
    class BinaryTrieNode:
        def __init__(self):
            self.children = [None, None]
    
    root = BinaryTrieNode()
    
    # 插入数字的二进制表示
    for num in nums:
        node = root
        for i in range(31, -1, -1):
            bit = (num >> i) & 1
            if not node.children[bit]:
                node.children[bit] = BinaryTrieNode()
            node = node.children[bit]
    
    # 查询最大异或
    max_xor = 0
    for num in nums:
        node = root
        xor_val = 0
        for i in range(31, -1, -1):
            bit = (num >> i) & 1
            # 优先选择相反位
            opposite = 1 - bit
            if node.children[opposite]:
                xor_val |= (1 << i)
                node = node.children[opposite]
            else:
                node = node.children[bit]
        max_xor = max(max_xor, xor_val)
    
    return max_xor
```

## 练习

| 题目 | 难度 | 核心技巧 |
|------|------|---------|
| LeetCode 208. 实现 Trie | 🟡 中等 | 基础实现 |
| LeetCode 211. 添加与搜索单词 | 🟡 中等 | Trie + DFS |
| LeetCode 212. 单词搜索 II | 🔴 困难 | Trie + 回溯 |
| LeetCode 421. 最大异或对 | 🟡 中等 | 二进制 Trie |
| LeetCode 648. 单词替换 | 🟡 中等 | Trie 前缀匹配 |
| LeetCode 677. 键值映射 | 🟡 中等 | Trie + 求和 |
| LeetCode 720. 词典中最长单词 | 🟢 简单 | Trie + DFS |
| LeetCode 745. 前缀和后缀搜索 | 🔴 困难 | 双 Trie |
| LeetCode 676. 实现魔法字典 | 🟡 中等 | Trie + 搜索 |

## 相关条目

- [[HashTable]]
- [[Tree]]
- [[StringAlgorithms]]
- [[BinarySearchTree]]
- [[SegmentTree]]
