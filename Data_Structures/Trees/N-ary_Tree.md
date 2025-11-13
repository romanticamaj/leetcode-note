# N-ary Tree 解題心法

## 🧠 核心哲學

N-ary Tree 的核心在於每個節點可以有任意數量的子節點，需要以 **動態集合** 思維處理子節點遍歷，而非固定的左右子樹模式。

## 核心概念：Children as Dynamic Collection

N-ary Tree 的每個節點維護一個 children 列表，關鍵在於將 children 視為可迭代的序列：

```cpp
struct Node {
    int val;
    vector<Node*> children;
};
```

---

## 關鍵應用模式：Trie = N-ary Tree + Linked List

N-ary Tree 最重要的應用是實現 **Trie (字典樹)**：

- **N-ary Tree 結構**：每個節點可以有多個子節點 (字符)
- **Linked List 特性**：children 以 linked structure 串接，動態擴展

```cpp
// Trie node = N-ary Tree node
struct TrieNode {
    unordered_map<char, TrieNode*> children;  // N-ary structure
    bool isEnd;
};
```

**常見實現變體**：

- **HashMap children**: 快速查找任意字符 `O(1)`
- **Array children[26]**: 固定字母表，空間換時間
- **Linked List children**: 節省空間，適合稀疏樹

---

## 🧩 遍歷模式 / Traversal Patterns

### Pattern 1: Preorder Traversal

**遞歸版本**：自然的自頂向下處理

```cpp
void preorder(Node* root) {
    if (!root) return;
    process(root->val);  // 先處理當前節點
    for (Node* child : root->children) {
        preorder(child);  // 再處理所有子節點
    }
}
```

**迭代版本**：使用 stack，注意 **reverse push** 保證左到右順序

```cpp
// 關鍵：reverse iteration 確保 leftmost child 最後 pop
for (int i = node->children.size() - 1; i >= 0; --i) {
    stack.push(node->children[i]);
}
```

### Pattern 2: Postorder Traversal

**遞歸版本**：自然的自底向上處理

```cpp
void postorder(Node* root) {
    if (!root) return;
    for (Node* child : root->children) {
        postorder(child);  // 先處理所有子節點
    }
    process(root->val);  // 最後處理當前節點
}
```

**迭代版本**：使用 **Visit Count Trick**

核心思想：追蹤每個節點已訪問的子節點數量

```cpp
struct StackNode {
    Node* node;
    int visited_children = 0;  // 已訪問子節點計數
};

// 邏輯：當 visited_children == children.size() 時才處理節點
```

### Visit Count Trick 設計要點

- **何時 push**: 當前子節點處理前
- **何時 increment**: 每處理完一個子節點
- **何時 process**: `visited_children == children.size()`

---

## N-ary Tree 轉換問題 / Transformation Problems

### Problem 1: Encode/Decode 成 Binary Tree

**核心概念：From the Right Side View**

將 N-ary Tree 轉換為 Binary Tree 的關鍵在於：

- **第一個子節點 → 左子樹**：N-ary node 的第一個 child 對應到 binary tree 的 left child
- **兄弟節點 → 右子樹**：N-ary node 的其他 children (兄弟關係) 串接成 binary tree 的 right child chain
- **Right Side View**：從右側觀察，每個節點的 rightmost child 形成 binary tree 的右鏈

**實現方式**：

- **DFS (遞歸)**：自然處理父子與兄弟關係
- **BFS (迭代)**：逐層轉換，維護兄弟鏈

---

### Problem 2: Serialization (序列化成字串)

將 N-ary Tree 序列化的挑戰：如何表示每個節點有多少個 children？

**常見解法**：

**解法 1: Null Separator for Children Lists**

使用 null 標記每個 children list 的結束：

1. **BFS Level Ordering**：逐層處理所有節點，每個節點依序輸出其 children values
2. **Children List as Sequence**：每個節點的 children 視為連續序列，用 null 分隔
3. **Queue nullptr Trick**：在 queue 中插入 nullptr，表示 children list 結束

**解法 2: 其他方法**

- **記錄 children count**：每個節點先記錄子節點數量
- **Parentheses matching**：使用括號配對表示層級結構
- **Level size encoding**：記錄每層節點數量

**實現方式**：

- **BFS (Level Order)**：適合 null separator 或 level size encoding
- **DFS (Post-order)**：適合 null separator 或 parentheses matching

## ✅ 關鍵要點 / Key Points

- [ ] **Trie = N-ary Tree + Linked List**: N-ary 結構 + children 的 linked structure
- [ ] **Children as sequence**: 將 children 視為可迭代序列，而非固定結構
- [ ] **Reverse push in stack**: 迭代遍歷時注意 reverse iteration 保證順序
- [ ] **Visit Count Trick**: Postorder 迭代的核心技巧
- [ ] **Right Side View for Binary Tree conversion**: 第一個 child → left, 兄弟 → right chain
- [ ] **Null separator for serialization**: 標記每個 children list 的結束邊界
- [ ] **Queue nullptr trick**: BFS 中優雅標記 children list 邊界
