# 遞迴設計心法：狀態、邊界與遞迴關係

---

## 核心思想：將問題視為狀態的轉移

遞迴的本質是將一個大問題分解為一個或多個結構相同、規模更小的子問題。設計遞迴函式的關鍵，在於精準定義**狀態 (State)**、**終止邊界 (Base Case)**，以及**遞迴關係 (Recurrence Relation)**。

---

## 1. 狀態設計：定義遞迴函式的簽名

狀態是解決當前子問題所需的所有資訊。一個設計良好的狀態，會讓遞迴函式的職責單一且清晰。

### 關鍵工具 1：函式參數 (Parameters)

這是定義狀態最直接的方式。參數明確地傳遞了每一層遞迴所需的上下文。

- **範例**: `int fib(int n)`，狀態就是 `n`。
- **範例**: `TreeNode* searchBST(TreeNode* root, int val)`，狀態是 `root` 和 `val`。

### 關鍵工具 2：可視範圍內的外部資訊

除了參數，當前遞迴層級能「看見」的外部資訊也是其狀態的一部分。

- **連結結構**: 在樹或鏈結串列中，`node->next` 或 `node->left` 提供了訪問相鄰狀態的能力。
- **共享參考**: 透過指標或參考傳遞的外部容器（如 `results` 陣列、`visited` 集合），它們的當前內容也是遞迴狀態的一部分。

### 關鍵工具 3：External State（外部狀態）

當多個遞迴呼叫需要共享或累積資訊時，可使用外部狀態（類成員變數或靜態變數）。這在分治算法中特別有用。

- **全局計數器**: `int counter = 0;` 用於按遞迴順序編號
- **累加器**: `int total = 0;` 用於累積子問題結果
- **資源指標**: `int* current` 用於追蹤資源消費

**使用場景**：

- **構造型分治**: 按遍歷順序編號/標記節點（如 DFS 編號）
- **線性資源消費**: 按特定順序分配編號、ID
- **遞迴順序決定處理順序**: 利用 DFS 自然順序管理狀態

**設計原則**：

- 遞迴順序必須與期望的處理順序一致
- 適用於結果依賴遍歷順序的場景
- 可避免顯式計算資源區間

💡 詳見 [分治結果累積策略](../../Divide_and_Conquer/Linear_Resource_Consumption_Pattern.md)

> **心法**: 設計遞迴時，首要任務是問自己：「要解決當前的子問題，我需要哪些資訊？」這些資訊共同構成了函式的狀態（即函式簽名）。

---

## 2. 遞迴關係：定義問題如何分解

遞迴關係描述了如何利用**當前狀態**和**子問題的解**來建構當前問題的解。這是演算法的核心邏輯。

### 關鍵工具 1：當前狀態的處理 (Pre-order Logic)

在發起遞迴呼叫（解決子問題）之前，我們可以利用當前狀態進行操作。

- **操作**: 標記訪問、路徑紀錄、預先計算。
- **位置**: `遞迴呼叫之前` 的程式碼區塊。

### 關鍵工具 2：子問題回傳值的處理 (Post-order Logic)

當遞迴呼叫返回時，它帶回了子問題的解。這是我們合併、決策、建構的**主動操作點**。

- **操作**:
  - **合併與建構**: `left_sum + right_sum + current_val`。
  - **決策與更新**: `max(left_depth, right_depth) + 1`。
  - **回溯清理**: `path.pop_back()`，為探索其他分支還原狀態。
- **位置**: `遞迴呼叫之後` 的程式碼區塊。

> **心法**: 思考遞迴關係時，問自己：「如果我已經拿到了子問題的答案，我該如何利用它和『當前狀態』的資訊，來計算出當前問題的答案？」

### 關鍵工具 3：Return Value 設計模式 — Sentinel vs. External State

當遞迴需要同時傳遞**計算結果**和**狀態標記**（如成功/失敗）時，有兩種主要設計策略：使用特殊值編碼（Sentinel Value）或外部狀態變數（External State）。

#### 設計策略對比

**方法 A: Sentinel Value（推薦）**
- 用特殊值（如 `-1`, `nullptr`, `INT_MIN`）編碼失敗狀態
- **優勢**:
  - Pure function、無副作用
  - 支援真正的 early termination
  - 邏輯內聚、易於測試
- **適用**: Tree DP、單一 boolean 判斷、需要提早終止的場景
- **典型應用**: Height Balanced Tree 驗證、路徑存在性檢查

**方法 B: External State**
- 用 global 變數或可修改參數（如 `bool& isValid`）記錄狀態
- **優勢**: 適合需要累積多個指標的場景
- **劣勢**:
  - 有副作用、較難測試
  - 即使檢測到失敗，仍需遍歷全部節點（無法真正 early termination）
- **適用**: 必須遍歷全部的統計場景、多指標累積

#### 設計原則

1. **優先使用回傳值編碼**：當只需單一 boolean 判斷時
2. **選擇合適的特殊值**：
   - 高度/長度問題：`-1` （正常值 ≥ 0）
   - 指標問題：`nullptr`
   - 數值問題：`INT_MIN`, `INT_MAX`, `NaN`
3. **保持語義清晰**：特殊值的意義應該直觀且一致
4. **配合提早終止**：檢測到特殊值後立即返回，避免無謂計算

> **心法**: 回傳值不僅僅是「答案」，它可以同時編碼**計算結果**和**執行狀態**。透過巧妙的編碼設計，能讓遞迴函式更純粹、更高效。

---

## 3. 終止邊界：定義最小問題單元

終止邊界（Base Case）是遞迴的出口，它定義了無需進一步分解、可以直接求解的最小問題。

### Base Case vs. 剪枝 (Pruning)

- **Base Case**: **問題的終點**。它是一個有意義的、可直接求解的最小單元。

  - **範例**: `if (n <= 1) return n;`
  - **範例**: `if (root == nullptr) return;`

- **剪枝 (Pruning)**: **無效路徑的提早終止**。它是一種預測性的檢查，用於過濾掉不可能產生有效解的遞迴路徑。
  - **範例**: `if (current_sum > target) return;`
  - **範例**: `if (visited[node]) return;`

一個設計良好的剪枝，能大幅減少不必要的計算，讓遞迴能更快地收斂到有效的 Base Case。

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

## 結語

設計優雅的遞迴程式，其精髓在於清晰地定義**狀態**、**遞迴關係**和**終止邊界**。每一層遞迴呼叫都應有其明確的計算意義，每一次回傳都應服務於更高層級的邏輯建構。
