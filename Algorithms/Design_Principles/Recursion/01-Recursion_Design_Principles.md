# 遞迴設計心法：萬用邏輯架構與實戰準則

---

## 🧠 遞迴的四大核心心法

### 1. Base Case ≠ 單純停止，而是**含有意義的最小單位**

- Base case 是你要處理的「最小問題」或「終止條件」。
- 它應該具備**明確的結構意義或答案特性**，不是單純為了停止遞迴。
- 在遇到 base case 時，往往已經足以：
  - 給出最終解答的一部分
  - 完成局部操作（例如建立節點、回傳總和、或傳回空容器）

---

### 2. 遞迴的呼叫位置 = **主動操作點**

遞迴函式的核心不只是呼叫自己，更重要的是在「呼叫前」與「呼叫後」對當前狀態進行處理。

- **呼叫前的處理 (Pre-order Logic):**

  - 在進入下一層遞迴之前，針對**目前節點**的狀態進行處理。
  - 這是執行「前序」邏輯的地方，例如：
    - 標記節點為已訪問 (`visited[node] = true`)
    - 將當前節點值加入路徑中 (`path.push_back(node->val)`)
    - 根據當前狀態進行剪枝 (Pruning) 判斷

- **呼叫後的處理 (Post-order Logic):**
  - 當遞迴呼叫從子問題返回後，這個位置就是**主動操作點**。
  - 呼叫遞迴不只是丟出去算，而是要**接收回傳值（有意義）**並**基於回傳值進行操作**。
  - 在這裡，你可以而且應該做：
    - **合併與建構**：合併子問題的結果 (e.g., `left_sum + right_sum + current_val`)，或連接資料結構。
    - **決策性更新**：更新全域狀態（如最大深度、節點總數）。
    - **回溯**：清理當前層級的狀態，為其他分支做準備 (`path.pop_back()`)。

---

### 3. 回傳值需設計成可串接、可堆疊、可理解

- 所有遞迴層級應保持一致回傳意義與型態。
  - 「可串接」：每一層回傳的值能被上層接住並進一步處理（如合併、加總、建構）。
  - 「可堆疊」：多層遞迴的回傳值能自然堆疊成一個整體（如陣列、樹、字串）。
  - 「可理解」：回傳值的語意清楚，能代表該層遞迴的處理結果。
- 若不回傳任何東西，就應明確設計為 in-place mutation 或副作用模式。
- 為了維持邏輯完整性，非 base case 通常也需：
  - 回傳處理後的狀態（如部分解、結構、節點）
  - 將遞迴的意圖往上傳遞

---

### 4. 剪枝 (Pruning) 是「預測性」的 Base Case，提早過濾無效路徑

如果說 `Base Case` 是遞迴的「終點站」，那麼 `Pruning` (剪枝) 就是在列車到達終點前，預先判斷「這條路線是否還有希望」的智慧檢查哨。它和 `Base Case` 共同構成了遞迴的終止防線。

- **`Base Case` vs. `Pruning`**
  - **`Base Case`**：處理**已完成**的最小問題單元 (e.g., `path.size() == k`)。它是遞迴的最終邊界。
  - **`Pruning`**：處理**未完成**但**已無望**的路徑 (e.g., `current_sum > target`)。它是一種預測性的、提早觸發的終止條件。

一個設計良好的剪枝，能將驗證邏輯從終點 (`Base Case`) 分散到過程中的每一步。當遞迴真正到達 `Base Case` 時，我們幾乎可以確信它是一個有效解，從而讓 `Base Case` 的邏輯變得極簡。

#### 設計的演進三階段

1. **標準回溯 (Backtracking with Pruning)**：

   - 在 `for` 迴圈中，明確檢查每個候選者是否 `promising`，決定是否要 `explore`。這是最典型、最清晰的剪枝應用。

2. **入口處檢查 (Pruning as an Entry Check)**：

   - 將剪枝條件移至遞迴函式的入口處，與 `Base Case` 並列。
   - `if (is_invalid_state) return;` 成為函式的第一道防線，讓後續邏輯更專注於核心任務。

3. **防禦性遞迴 (Defensive Recursion / One-liner)**：
   - 極致簡化下，剪枝與邊界檢查 (`Base Case` 的一部分) 合而為一，成為函式呼叫的單一屏障。
   - 例如：`if (index < 0 || visited[index] || current_sum > target) return;` 這種寫法將所有無效情況一次性過濾，程式碼更為緊湊。

---

## 🧩 心法速查表

| 編號 | 心法內容                     | 關鍵行為                                                                    |
| ---- | ---------------------------- | --------------------------------------------------------------------------- |
| 1    | Base case 有其邊界意義       | 是答案的一部分，而非僅為終止條件                                            |
| 2    | 在遞迴呼叫前後處理狀態       | 前序 (Pre-order) 處理當前狀態，後序 (Post-order) 作為「主動操作點」合併結果 |
| 3    | 回傳值需語意統一、邏輯可串接 | 維持 call stack 邏輯與意圖一致                                              |
| 4    | 剪枝是「預測性」的 Base Case | 預測性地終止無望路徑，簡化 Base Case 驗證                                   |

---

## 🔧 遞迴設計模板

這是一個整合性的「超級模板」，它透過註解說明如何根據問題特性，調整為不同的遞迴模式。

```cpp
// ReturnType:
// - void: 回溯法，透過 &results 收集解。
// - T: 分治法或結構遞迴，回傳當前子問題的解。
ReturnType solve(State& current_state, /* &results, */ ...) {
    // --- 1. 終止與邊界檢查 ---

    // Pruning (入口剪枝): 根據當前「狀態」判斷是否繼續。
    if (isStateInvalidOrHopeless(current_state)) {
        return ...; // 返回失敗/無效值 (e.g., 0, false, nullptr)
    }

    // Base Case: 到達遞迴終點。
    if (isBaseCase(current_state)) {
        // 模式 A (回溯法): 收集一個完整解。
        // results.add(buildSolution(current_state)); return;

        // 模式 B (分治法): 返回最小單元的解。
        // return solveDirectly(current_state);
    }

    // --- 2. 核心遞迴邏輯 ---

    // Pre-order Logic: 在探索子問題前，處理當前節點/狀態。
    processCurrentNode(current_state);
    // e.g., auto combined_solution = initial_value;

    // 核心探索迴圈:
    // - 對於「回溯法」，這是遍歷所有「候選者 (candidates)」。
    // - 對於「分治法/結構遞迴」，這是遍歷固定的「子問題 (subproblems)」，如樹的左右子節點。
    for (auto& choice : generateChoicesOrSubproblems(current_state)) {

        // Pruning (候選者剪枝): 檢查單一「選擇」是否合法。
        if (!isChoicePromising(choice, current_state)) {
            continue;
        }

        // --- 準備遞迴 ---
        // 模式 A (回溯法): 修改共享狀態，遞迴後還原。
        updateState(current_state, choice); // Choose
        auto sub_solution = solve(current_state, ...); // 傳入「被修改後」的 state 作為 next_state
        restoreState(current_state, choice); // Unchoose

        // 模式 B (分治法): 直接將 choice (子問題) 作為 next_state 傳入。
        auto sub_solution = solve(choice, ...);

        // Post-order Logic: 處理子問題的回傳結果。
        // - 回溯法: 通常無事可做。
        // - 分治法: 合併子問題的解到當前層級。
        //   e.g., combined_solution = combine(combined_solution, sub_solution);
        processSubSolution(sub_solution);
    }

    // --- 3. 返回最終結果 ---
    // - 回溯法: 通常是 void，無返回值。
    // - 分治法: 返回當前層級合併後的完整解。
    //   return combined_solution;
    return ...;
}
```

---

## 📘 結語

不論是樹、陣列、字串或動態規劃，遞迴設計的精髓不在「反覆呼叫自己」，而在於：

> **每一層呼叫都要有其意義，每一次回傳都要能被接住並傳遞整體邏輯。**

這四個心法將幫助你建立出可維護、可擴展、可 debug 的遞迴程式架構。
