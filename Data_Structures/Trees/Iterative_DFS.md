# Iterative DFS in Binary Trees

---

## 📌 為什麼使用 Iterative DFS？

雖然 DFS 在 binary tree 中常以遞迴實作，但在以下情境中，使用 **iterative DFS（使用 stack）** 更具優勢：

- 避免遞迴過深造成 stack overflow
- 更容易控制 traversal 順序（如 pre-order, in-order, post-order）
- 可與 BFS 結構對照學習

---

## 🧠 核心結構

```cpp
std::stack<TreeNode*> s;
s.push(root);

while (!s.empty()) {
    TreeNode* node = s.top();
    s.pop();

    // 處理當前節點
    ...

    // 根據 traversal 順序決定 push 順序
    if (node->right) s.push(node->right);
    if (node->left)  s.push(node->left);
}
```

---

## ✅ 適用於

- Pre-order traversal（根 → 左 → 右）
- 模擬 DFS 的遞迴邏輯
- 題目要求 iterative 解法

---

## 📘 延伸閱讀

- [DFS vs BFS](../../Algorithms/Traversal_Strategies/DFS_vs_BFS.md)
- [DFS for Level Order Traversal](../../Algorithms/Traversal_Strategies/DFS_for_Level_Order_Traversal.md)
- [DFS Tree vs Graph](../../Algorithms/BFS_DFS/DFS_Tree_vs_Graph.md)

---

本頁將持續補充各種 iterative DFS 的範例與變形。