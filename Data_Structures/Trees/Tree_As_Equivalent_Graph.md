# 將 Tree 問題轉換為等價 Graph 解法

在許多需要「任意節點之間」搜尋的 Tree 題目中，若能將 Tree 視為一個 Undirected Graph，便能使用標準的 BFS / DFS 進行遍歷與距離計算。

---

## 🌳 Tree 本質上是 Graph 的子集

- Tree 是一種特殊的 Graph：**無環、連通、N 個節點有 N-1 條邊**
- 但 Tree 的實作通常是單向的（只有 left/right），無法往回走

---

## ✅ 解法一：顯式轉換為 Graph

### 步驟

1. 使用 DFS 或 BFS 遍歷整棵樹
2. 將每個節點與其子節點建立雙向邊
3. 建立 `unordered_map<TreeNode*, unordered_set<TreeNode*>>` 作為 adjacency list

### 範例程式碼

```cpp
unordered_map<TreeNode*, unordered_set<TreeNode*>> adjList;

void createList(TreeNode* root, TreeNode* parent) {
    if (root == nullptr) return;

    if (parent) adjList[root].insert(parent);
    if (root->left) adjList[root].insert(root->left);
    if (root->right) adjList[root].insert(root->right);

    createList(root->left, root);
    createList(root->right, root);
}
```

---

## ✅ 解法二：額外記錄 parent，讓 Tree 變成 Undirected Graph

### 概念

- Tree 本身只有 left/right，無法往上走
- 若額外記錄每個節點的 parent，就能往上走
- 加上 parent 後，Tree 就變成一個 Undirected Graph

### 實作方式

```cpp
unordered_map<TreeNode*, TreeNode*> parentMap;

void recordParent(TreeNode* root, TreeNode* parent) {
    if (root == nullptr) return;

    parentMap[root] = parent;

    recordParent(node->left, root);
    recordParent(node->right, root);
}
```

### 使用方式

- 在 BFS / DFS 中，除了走 left/right，也可以走 parent
- 需要搭配 `unordered_set<TreeNode*> visited` 避免重複

---

## 🧠 小結

- Tree 是 Graph 的一種，但實作上常缺乏「往上」的能力
- 只要補上 parent，或轉成 adjacency list，就能當作 Graph 使用
