# 演算法的時序模式 (Temporal Patterns in Algorithms)

## 核心思想：狀態處理與狀態轉移的相對順序

任何遞迴或迭代的演算法，其核心都可以被抽象為兩個基本操作的序列：

1. **處理當前狀態 (Process Current State):** 對當前的狀態（節點、索引、子問題）進行計算、更新、或產生結果。
2. **轉移到下一狀態 (Transition to Next State):** 透過遞迴呼叫或迭代更新，移動到下一個狀態。

這兩個操作的**相對執行順序**，決定了演算法的根本行為模式。這個觀點超越了特定的資料結構（如樹），適用於從一維陣列到多維 DP 的所有問題。我們可以將這些順序歸納為三種「時序模式」。

---

## 遞迴中的時序模式 (Temporal Patterns in Recursion)

### 模式一：前序處理 (Pre-order Processing): 先處理，後探索

**本質：**
自頂向下傳遞資訊 (Top-Down Information Passing)。在探索子問題之前，先處理當前狀態。這意味著當前狀態的處理結果會影響或作為參數傳遞給子問題的求解過程。

**適用場景與泛化應用：**

- **回溯法 (Backtracking):** 先在當前路徑上做出選擇 (`process`)，然後基於此選擇繼續向下探索 (`recurse`)。這是最典型的應用。
- **前綴計算 (Prefix Calculation):** 在 DFS 中，將父節點的計算結果（如路徑和）傳遞給子節點，子節點基於此結果繼續計算。
- **拓撲排序 (Topological Sort - Kahn's Algorithm):** 雖然是迭代，但其思想是前序的。處理一個入度為 0 的節點 (`process`)，然後更新其鄰居的入度，將新的入度為 0 的節點加入佇列 (`transition`)。

**泛化 C++ 元模板:**

```cpp
// State: 代表當前狀態，可以是單一索引(int i)、多維座標(int i, int j)、或更複雜的結構。
// Context: 演算法過程中需要傳遞的上下文，如當前路徑、結果集合等。
void pre_order_process(State& current_state, Context& context) {
    // 1. 處理當前狀態 (Process Current State)
    //    例如：將當前節點加入路徑、檢查是否滿足剪枝條件等。
    process(current_state, context);

    // 2. 轉移到下一狀態 (Transition to Next State)
    //    為每個可能的下一步生成新狀態並遞迴。
    for (State next_state : generate_next_states(current_state)) {
        pre_order_process(next_state, context);
    }

    // (可選) 回溯：如果 process 改變了共享狀態，此處需要復原。
    backtrack(current_state, context);
}
```

### 模式二：後序處理 (Post-order Processing): 先探索，後整合

**本質：**
自底向上整合結果 (Bottom-Up Result Aggregation)。必須先得到所有子問題的解，才能計算或處理當前狀態。

**適用場景與泛化應用：**

- **動態規劃 (Top-Down DP):** `dp(state)` 的解依賴於 `dp(sub_state)` 的解，必須先遞迴求得子問題的解。
- **分治法 (Divide and Conquer):** 如合併排序，先遞迴處理左右兩半 (`recurse`)，再進行合併 (`process`)。
- **表達式樹求值 (Expression Tree Evaluation):** 必須先計算左右子樹的值，才能計算當前運算符節點的值。
- **聚合計算 (Aggregation):** 如計算樹的高度或節點總和，需要先知道所有子樹的結果才能整合。

**泛化 C++ 元模板:**

```cpp
// ReturnType: 子問題解的類型。
// State: 同上。
ReturnType post_order_process(State& current_state) {
    // 基礎案例：遞迴的終點。
    if (is_base_case(current_state)) {
        return base_value;
    }
    // 記憶化：避免重複計算。
    if (memo.count(current_state)) {
        return memo[current_state];
    }

    // 1. 轉移到下一狀態 (Transition to Next State)
    //    先遞迴地解決所有子問題。
    vector<ReturnType> sub_results;
    for (State next_state : generate_next_states(current_state)) {
        sub_results.push_back(post_order_process(next_state));
    }

    // 2. 處理當前狀態 (Process Current State)
    //    利用所有子問題的解來計算當前狀態的解。
    ReturnType current_result = combine(current_state, sub_results);

    return memo[current_state] = current_result;
}
```

### 模式三：中序處理 (In-order Processing): 探索、處理、再探索

**本質：**
在多個子問題的探索之間進行處理。通常與具有線性或有序特性的結構相關。

**適用場景與泛化應用：**

- **二元搜尋樹 (BST):** `recurse(left) -> process(node) -> recurse(right)` 是其最經典的應用，用於按序輸出節點。
- **將 BST 扁平化為有序鏈表:** 透過中序遍歷，在 `process` 階段重新連接節點指針。
- **泛化應用：** 當一個狀態的處理需要「左邊」或「前序」子問題的結果，且其處理結果又會影響「右邊」或「後續」子問題時。

---

## 迭代中的時序模式 (Temporal Patterns in Iteration)

- **前序處理 (Pre-order):**

  - **體現：** 標準的 `for` 或 `while` 迴圈。
  - **範例：** `for (int i = 0; i < n; ++i)`。在每次迭代中，先處理當前狀態 `i`，然後透過 `i++` 轉移到下一狀態。

- **後序處理 (Post-order):**
  - **體現：** DP 的表格法 (Tabulation)。
  - **範例：** `for (int i = n-1; i >= 0; --i)`。從後往前填表，正是為了滿足「先有子問題解」的後序依賴關係。
  - **體現：** 使用顯式堆疊 (explicit stack) 模擬遞迴，是實現迭代式後序遍歷的標準技巧。

---

## 總結心法：如何選擇模式？

選擇哪種時序模式，取決於**資訊流動的方向**：

> - 如果問題的解決需要將父層級的資訊（如路徑、約束、狀態）**向下傳遞**給子層級，則應優先考慮 **前序處理 (Pre-order)**。
> - 如果問題的解決需要將子層級的計算結果**向上整合**，用以建構父層級的解，則應優先考慮 **後序處理 (Post-order)**。
