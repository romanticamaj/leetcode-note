# 深度優先搜索 (Depth-First Search, DFS)

## 基本概念

深度優先搜索是一種遍歷樹或圖的算法，它優先遍歷到樹的最深處，然後回溯。在二叉樹中，DFS 有三種主要變體：

- **前序遍歷 (Preorder Traversal)**: 根節點 → 左子樹 → 右子樹
- **中序遍歷 (Inorder Traversal)**: 左子樹 → 根節點 → 右子樹
- **後序遍歷 (Postorder Traversal)**: 左子樹 → 右子樹 → 根節點

## 實現方式

DFS 可以通過**遞歸**或**迭代**（使用 std::stack<TreeNode*>）來實現。

## DFS 的通用模板

DFS 在樹上的實現有一個通用的結構，幾乎適用於所有樹的 DFS 問題：


```cpp
// 通用 DFS 函數模板
ReturnType dfs(TreeNode* node) {
    // 1. 處理基本情況
    if (node == nullptr) {
        // 返回基本情況的結果
        return baseResult;
    }
    
    // 2. 對當前節點進行邏輯處理
    // ... 處理當前節點的邏輯 ...
    
    // 3. 遞歸調用子節點
    ReturnType leftResult = dfs(node->left);
    ReturnType rightResult = dfs(node->right);
    
    // 4. 根據子節點的結果計算當前節點的結果
    ReturnType result = combine(node->val, leftResult, rightResult);
    
    // 返回結果
    return result;
}
```

每個遞歸調用都是在解決同一個問題，只是輸入變成了當前節點為根的子樹。這種"自相似"的特性使得遞歸特別適合處理樹結構。

### 為什麼需要 if (node == nullptr) 作為終止條件呢？

檢查基本情況（如 `if (node == nullptr)`）不僅是為了終止遞歸，更是為了`避免空指針異常`。

如果不進行檢查，當遞歸到葉節點的子節點（null）時，嘗試訪問 `null->val` 或 `null->left` 等屬性會導致程序崩潰，因為 null 不具有這些屬性。

## DFS 的特性與優勢

1. **實現簡單**：特別是使用遞歸時，DFS 的實現非常簡潔
2. **空間效率**：對於窄而深的樹，DFS 的空間複雜度較低
3. **適合深度相關問題**：如查找樹的最大深度，確認路徑存在等

## DFS 的主要缺點

- 如果目標節點在樹的上層，但 DFS 先遍歷其他分支，可能會浪費大量時間
- 對於極度不平衡的樹，DFS 的空間複雜度可能達到 O(n)

## 最佳實踐

- 遞歸 DFS 適合大多數樹問題，代碼簡潔易理解
- 當樹非常深或遞歸可能導致棧溢出時，考慮使用 iterative DFS
- 對於需要按特定順序處理節點的問題，選擇適合的遍歷方式（前序/中序/後序）