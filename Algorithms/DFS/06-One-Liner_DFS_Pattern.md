# DFS 優化心法：「單行」DFS 模式 (The "One-Liner" DFS Pattern)

在圖的深度優先搜索 (DFS) 中，尤其是格狀圖 (Grid) 問題，我們常常可以將一個分散、多檢查點的遞迴函數，重構成一個更為緊湊、優雅的形式。這個模式的核心思想是**將所有檢查點從「呼叫前」轉移到「進入後」**，從而簡化呼叫點的邏輯。

我們將此模式命名為 **「單行 DFS 模式 (One-Liner DFS Pattern)」**，其核心技巧是：**「先呼後判，入內即標，單行聚合 (Call First, Filter Inside; Mark on Entry, Aggregate in One Line)」**。

---

## 1. 模式詳解：從傳統到 One-Liner

### 風格一：呼叫前檢查 (Pre-call Validation) - 傳統寫法

在遞迴呼叫 `dfs()` **之前**，先檢查所有條件（邊界、訪問過、合法性），確保傳入的參數絕對合法。這種寫法邏輯分散，呼叫點顯得臃腫。

```cpp
// 傳統寫法：在呼叫點進行大量檢查
void dfs_verbose(Node current, VisitedSet& visited) {
    // ... 處理 current 節點 ...
    // (註：current 節點應由其呼叫者標記為 visited)

    for (Node neighbor : get_neighbors(current)) {
        // 在呼叫前進行所有檢查
        if (is_valid(neighbor) && !visited.contains(neighbor)) {
            visited.insert(neighbor);
            dfs_verbose(neighbor, visited);
        }
    }
}
```

### 風格二：「單行」DFS 模式 (One-Liner DFS Pattern) - 重構後

我們**無條件地**進行遞迴呼叫，然後在 `dfs()` 函數的**最開頭**統一處理所有**終止條件 (Terminating Conditions)**，包括無效情況和成功的 base case。

```cpp
// 重構後：應用「單行 DFS 模式」
ResultType dfs_one_liner(Node current, VisitedSet& visited) {
    // 1. 進入後篩選 (Filter Inside)：處理所有無效情況
    if (!is_valid(current) || visited.contains(current)) {
        return base_case_for_invalid; // e.g., 0, false
    }

    // 2. 終止性 Base Case：處理滿足目標的成功情況
    if (is_goal(current)) {
        return base_case_for_success; // e.g., 1, true
    }

    // 3. 入內即標 (Mark on Entry)
    visited.insert(current);

    // 4. 聚合與遞迴 (Aggregate in One Line)
    // 將當前節點的貢獻與所有子問題（鄰居）的結果，以單行返回語句聚合起來。
    return process(current) +
           dfs_one_liner(neighbor1, visited) +
           dfs_one_liner(neighbor2, visited);
}
```

---

## 2. 核心重構步驟

### 步驟一：先呼後判 (Call First, Filter Inside)

- **核心**: 將邊界與合法性檢查，從**呼叫點 (caller)** 的 `if` 判斷，轉移到**遞迴函數開頭**的守衛條款。
- **效果**: 呼叫點的邏輯被大幅簡化，所有關於「節點是否有效」的責任都統一由遞迴函數自身承擔。

### 步驟二：入內即標 (Mark on Entry)

- **核心**: 在守衛條款之後，立刻將當前節點標記為已訪問。這是為了防止從其他路徑再次訪問到同一個節點，從而避免無限循環。
- **實作**:
  - **原地標記 (In-place Marking)**: 直接修改輸入的 `grid` 來標記（例如，將 `1` 改為 `#`）。這是**空間最優**的做法 `O(1)`，但會修改輸入。
  - **傳遞 `visited` 集合**: 如果不允許修改輸入，則仍需傳遞 `visited` 集合。

### 步驟三：單行聚合 (One-line Aggregation)

- **核心**: 利用 `return` 語句，將「當前節點的貢獻」與「所有鄰居（子問題）的貢獻」在一行內清晰地表達出來。
- **效果**: 使遞迴的聚合關係（例如求和、計數、`||` 邏輯）變得非常明確，避免了使用臨時變數。

---

## 3. 概念延伸：與 Backtracking 的關係

`One-Liner DFS` 模式不僅是程式碼風格的優化，它在本質上可以視為一種**高度特化**的 `Backtracking` 模式。

### 核心關聯：前置所有檢查點

- **`Backtracking`**: 通常在 `for` 迴圈內部，遞迴探索前，使用 `is_promising` 檢查來剪枝。
- **`One-Liner DFS`**: 將 `is_valid` 和 `is_promising` 的檢查**全部前置**到遞迴函式的入口處，作為守衛條款。

### One-Liner DFS 作為特化的 Backtracking

這種模式特別適用於：

1. **目標是「尋找存在性」**: 最常見的應用是判斷「是否存在」一條滿足條件的路徑，因此可以用 `||` (OR) 邏輯來聚合結果。只要任何一個分支成功，整個探索就成功。
2. **狀態恢復的簡化**: 在傳統 `Backtracking` 中，`Unchoose` 步驟（例如 `visited[i] = false`）是必要的，因為你需要探索所有可能的路徑。在尋找單一路徑的 `One-Liner DFS` 中，如果找到解就終止，`unmark_visited` 這一步有時可以省略，因為我們不再關心後續分支的狀態。

### 範例模板：Backtracking 視角

```cpp
bool dfs(State& state) {
    // 1. 前置檢查 (is_valid + is_promising)
    if (!is_valid(state) || !is_promising(state)) {
        return false; // 無效或無望，剪枝
    }

    // 2. 成功終止條件 (Base Case)
    if (is_goal(state)) {
        return true; // 找到解
    }

    // 3. 做出選擇 (Choose)
    state.mark_visited();

    // 4. 探索 (Explore) - 濃縮在一行
    bool found = dfs(next_state_1) || dfs(next_state_2);

    // 5. 撤銷選擇 (Unchoose) - 根據需要
    state.unmark_visited();

    return found;
}
```

### 總結心法

- **`One-Liner DFS` = 前置所有驗證 + 簡化遞迴聚合**
- **關鍵原則**：
  > 將所有能導致 `return false` 的情況（無效、無望）全部在遞迴入口處處理掉。
  > 將所有能導致 `return true` 的情況（找到目標）在 `base case` 處處理掉。

這使得遞迴的主體部分極度純粹，只專注於「擴展下一步」，從而實現程式碼的簡潔與清晰。

---

## ✅ 總結與檢查清單

下次進行 DFS 設計時，可以依循此清單：

- [ ] **邊界與合法性條件是否已移至 DFS 開頭？** (先呼後判)
- [ ] **是否在處理節點邏輯前就標記 `visited`？** (入內即標)
- [ ] **是否可以用一行 `return` 來表達貢獻值的聚合？** (單行聚合)
- [ ] **這是否是一個尋找存在性的問題，適合用 `||` 聚合？**
- [ ] **是否可以/應該使用「原地標記」來優化空間？**
