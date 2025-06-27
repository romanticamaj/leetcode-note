# DFS 優化心法：「單行」DFS 模式 (The "One-Liner" DFS Pattern)

在圖的深度優先搜索 (DFS) 中，尤其是格狀圖 (Grid) 問題，我們常常可以將一個分散、多檢查點的遞迴函數，重構成一個更為緊湊、優雅的形式。這個模式的核心思想是**將所有檢查點從「呼叫前」轉移到「進入後」**，從而簡化呼叫點的邏輯。

我們將此模式命名為 **「單行 DFS 模式 (One-Liner DFS Pattern)」**，其核心技巧是：**「先呼後判，入內即標，單行聚合 (Call First, Filter Inside; Mark on Entry, Aggregate in One Line)」**。

---

## 1. 兩種風格的對比

### 風格一：呼叫前檢查 (Pre-call Validation) - 傳統寫法

在遞迴呼叫 `dfs()` **之前**，先檢查所有條件（邊界、訪問過、合法性），確保傳入的參數絕對合法。

```cpp
// 傳統寫法：在呼叫點進行大量檢查
ResultType dfs_verbose(Node current, VisitedSet& visited) {
    // 假設 current 傳進來時一定是合法的

    // 1. 處理當前節點
    ResultType result = process(current);
    // (註：current 節點應由其呼叫者標記為 visited)

    // 2. 遍歷並檢查鄰居
    for (Node neighbor : get_neighbors(current)) {
        // 在呼叫前進行所有檢查
        if (is_valid(neighbor) && !visited.contains(neighbor)) {
            // 3. 標記鄰居並進行遞迴呼叫
            visited.insert(neighbor);
            result = aggregate(result, dfs_verbose(neighbor, visited));
        }
    }
    return result;
}
```

- **問題**: 邊界檢查邏輯分散在呼叫者和被呼叫者處，程式碼冗長。

### 風格二：「單行」DFS 模式 (One-Liner DFS Pattern) - 重構後

我們**無條件地**進行遞迴呼叫，然後在 `dfs()` 函數的**最開頭**統一處理所有**終止條件 (Terminating Conditions)**，包括無效情況和成功的 base case。

```cpp
// 重構後：應用「單行 DFS 模式」
ResultType dfs_one_liner(Node current, VisitedSet& visited) {
    // 1. 進入後篩選 (Filter Inside)：處理所有無效情況
    if (!is_valid(current) || visited.contains(current)) {
        return base_case_for_invalid; // e.g., 0, empty list
    }

    // 2. 終止性 Base Case：處理滿足目標的成功情況
    if (is_target_or_goal(current)) {
        return base_case_for_success; // e.g., 1, list with current node
    }

    // 3. 入內即標 (Mark on Entry)
    visited.insert(current);

    // 4. 聚合與遞迴 (Aggregate in One Line)
    // 將當前節點的貢獻與所有子問題（鄰居）的結果，以單行返回語句聚合起來。
    return process(current) +
           dfs_one_liner(neighbor1, visited) +
           dfs_one_liner(neighbor2, visited) +
           // ...
           dfs_one_liner(neighborN, visited);

    /*
    // 對於鄰居數量可變的一般圖，其概念相同，只是用迴圈來實現：
    ResultType result = process(current); // 當前節點的貢獻
    for (Node neighbor : get_neighbors(current)) {
        result = aggregate(result, dfs_one_liner(neighbor, visited));
    }
    return result;
    */
}
```

- **優點**: 程式碼極度簡潔，遞迴關係一目了然，責任單一。

---

## 2. 核心重構技巧 (Key Refactoring Takeaways)

### 技巧一：先呼後判 (Call First, Filter Inside)

- **核心**: 將邊界與合法性檢查，從**呼叫點 (caller)** 的 `if` 判斷，轉移到**遞迴函數開頭**的守衛條款。
- **效果**: 呼叫點的邏輯被大幅簡化，所有關於「節點是否有效」的責任都統一由遞迴函數自身承擔。

### 技巧二：入內即標 (Mark on Entry)

- **核心**: 在守衛條款之後，立刻將當前節點標記為已訪問。這是為了防止從其他路徑再次訪問到同一個節點，從而避免無限循環。
- **實作**:
  - **原地標記 (In-place Marking)**: 直接修改輸入的 `grid` 來標記（例如，將 `1` 改為 `0` 或 `#`）。這是**空間最優**的做法 `O(1)`，但會修改輸入。
  - **傳遞 `visited` 集合**: 如果不允許修改輸入，則仍需傳遞 `visited` 集合，但標記的動作應在函數開頭完成。

### 技巧三：單行聚合 (One-line Aggregation)

- **核心**: 利用 `return` 語句，將「當前節點的貢獻」與「所有鄰居（子問題）的貢獻」在一行內清晰地表達出來。
- **效果**: 使遞迴的聚合關係（例如求和、計數）變得非常明確，避免了使用臨時變數來累加。

---

## ✅ 總結與檢查清單

「單行 DFS 模式」是一種提升程式碼品質的有效方法。下次進行 DFS 設計時，可以依循此清單：

- [ ] **邊界條件是否已移至 DFS 開頭？** (先呼後判)
- [ ] **是否在處理節點邏輯前就標記 `visited`？** (入內即標)
- [ ] **是否可以用一行 `return` 來表達貢獻值的聚合？** (單行聚合)
- [ ] **是否可以/應該使用「原地標記」來優化空間？**

通過實踐這些技巧，可以將原本分散的邏輯檢查點，收斂成一個高度簡潔且表達力強的遞迴實現。
