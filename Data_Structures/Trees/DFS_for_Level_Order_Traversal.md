# 使用 DFS + Preordering + Level 變數實作層序遍歷

雖然層序遍歷（Level Order Traversal）最直觀的實作方式是使用 BFS 搭配一個佇列（Queue），但我們也可以巧妙地利用 DFS 來達成相同的效果。

---

## 核心思想

這個技巧的核心在於，在 DFS 遍歷的過程中，額外傳遞一個 `level`（或 `depth`）參數，來記錄當前節點所在的層級。

1. **使用 Pre-order Traversal**：

   - 我們選擇前序遍歷（根 -> 左 -> 右），因為它保證了在處理任何子節點之前，會先訪問父節點。這也意味著我們會先訪問第 `L` 層的節點，然後才訪問第 `L+1` 層的節點。 (關鍵概念！！！)

2. **傳遞 `level` 參數**：

   - 在遞迴函式中，除了傳遞 `TreeNode* node`，我們還需要傳遞一個 `int level`。
   - 根節點的 `level` 為 0，每向下一層，`level` 就加 1。 (用 0 當初始值比較直觀)

3. **使用結果容器**：
   - 我們使用一個 `vector<vector<int>>` 來儲存最終的結果。
   - `result[i]` 將會儲存第 `i` 層的所有節點值。

---

## 演算法步驟

```cpp
void dfs(TreeNode* node, int level, vector<vector<int>>& result) {
    if (node == nullptr) {
        return;
    }

    // 1. 檢查是否需要為新層級建立一個新的 vector
    if (level >= result.size()) {
        result.push_back({}); // 為新層級新增一個空的 vector
    }

    // 2. 將當前節點的值加入對應層級的 vector 中 (Pre-order 操作)
    result[level].push_back(node->val);

    // 3. 遞迴訪問子節點，並將 level 加 1
    dfs(node->left, level + 1, result);
    dfs(node->right, level + 1, result);
}

vector<vector<int>> levelOrder(TreeNode* root) {
    vector<vector<int>> result;
    dfs(root, 0, result);
    return result;
}
```

---

## 與 BFS 方法的比較

| 特性               | DFS 實現                             | BFS 實現                           |
| ------------------ | ------------------------------------ | ---------------------------------- |
| **輔助空間複雜度** | O(H) (遞迴堆疊)                      | O(W) (佇列)                        |
| **總空間複雜度**   | O(H) + O(N)                          | O(W) + O(N)                        |
| **直觀性**         | 較不直觀，但展示了對遞迴的深入理解。 | 非常直觀，直接模擬層序遍歷的過程。 |
| **程式碼**         | 遞迴寫法通常更簡潔。                 | 迭代寫法，需要手動管理佇列。       |

_註：H 是樹高，W 是樹的最大寬度，N 是節點總數。_

**空間複雜度說明：**
`O(H)` 和 `O(W)` 是一般性的表達式，但在最差情況下，它們都可以達到 `O(N)`：

- **DFS (O(H))**: 在一個極度不平衡的「鏈狀樹」（skewed tree）中，樹高 `H` 會約等於節點總數 `N`，因此輔助空間複雜度為 `O(N)`。
- **BFS (O(W))**: 在一個「完美」或「完整」的二元樹中，最底層的節點數（即最大寬度 `W`）可能接近 `N/2`，因此輔助空間複雜度為 `O(N)`。

---

## 結論

雖然 BFS 是實現層序遍歷的標準方法，但使用 DFS 搭配 `level` 參數也是一個完全可行的替代方案。在某些情況下，例如當樹的結構非常寬而淺（如完美二元樹）時，DFS 的遞迴堆疊空間開銷（O(H) = O(log N)）會遠小於 BFS 佇列的空間開銷（O(W) = O(N)），此時 DFS 的空間效率更高。

在面試中，能夠提出並實現這種 DFS 的解法，可以很好地展示你對樹遍歷和遞迴的深刻理解。
