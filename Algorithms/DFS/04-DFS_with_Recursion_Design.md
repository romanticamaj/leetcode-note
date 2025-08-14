# DFS 與遞迴設計：路徑查找與值的聚合

當使用 DFS 解決不僅僅是遍歷，而是需要**查找特定路徑**或**聚合路徑上的值**時，其本質是遞迴設計模式的直接應用。理解如何運用遞迴的「狀態」與「回傳值」，是解決這類問題的關鍵。

---

## 1. 核心思想：遞迴的狀態與回傳值

根據遞迴設計心法，我們需要利用兩個關鍵工具來解決問題：

1. **當前狀態 (Current State)**: 在遞迴函式中，我們能存取的所有資訊，包括函式參數（如 `current_node`）和外部可視變數（如 `visited` 集合）。
2. **子問題的回傳值 (Return Value from Subproblems)**: 當 `dfs(neighbor)` 呼叫返回時，它帶回了子問題的解。

在路徑查找與值聚合的場景下，**回傳值**的設計尤為重要。它通常需要扮演一個雙重角色：

- **信號員 (Signaler)**: 告知上一層呼叫者「我這個分支是否成功找到了通往終點的路徑？」
- **計算員 (Calculator)**: 如果找到了，回傳值還必須攜帶「從我當前位置到終點的計算結果」。

---

## 2. 遞迴設計模式：單一路徑查找

**目標**: 只要找到**任何一條**通往終點的路徑即可。

這種模式的設計完全體現了遞迴心法中的「狀態」與「回傳值」的運用。

### 設計步驟 (以 LeetCode 399. Evaluate Division 為例)

**問題**: 計算 `a / b` 的值，本質是查找從 `a` 到 `b` 的路徑，並將路徑上所有邊的權重相乘。

#### A. 定義狀態 (函式簽名)

要解決子問題「從 `current` 節點到 `end` 節點的路徑乘積是多少？」，我們需要以下資訊：

- `current`: 當前節點。
- `end`: 最終目標節點。
- `graph`: 圖的結構。
- `visited`: 訪問過的節點集合，防止環路。

```cpp
double dfs(string& current, string& end, ..., unordered_set<string>& visited);
```

#### B. 定義遞迴關係 (核心邏輯)

1. **Pre-order Logic (處理當前狀態)**:

   - 在探索鄰居前，將當前節點加入 `visited` 集合，標記為「處理中」。`visited.insert(current);`

2. **Post-order Logic (處理子問題回傳值)**:
   - 遍歷所有鄰居 `neighbor`，發起遞迴呼叫 `dfs(neighbor, ...)`。
   - 拿到回傳值 `result_from_neighbor` 後，**必須先檢查信號**。
   - **信號判斷**: 如果 `result_from_neighbor != -1.0` (代表「Found」信號)，則證明從 `neighbor` 到 `end` 的路徑存在。
   - **結果建構**: 此時，才將子問題的解與當前狀態（即 `current` 到 `neighbor` 的邊權重）結合：`result = result_from_neighbor * edge_weight`。
   - **立即返回**: 因為是單一路徑查找，一旦找到解，就沒有必要再探索其他鄰居，應立即將結果回傳。

#### C. 定義終止邊界 (Base Case)

- **成功邊界**: `if (current == end)`，到達終點。
  - **回傳值**: `1.0`。這個值同時扮演兩個角色：
    - **信號**: 非 `-1.0`，代表「Found」。
    - **計算初始值**: 作為乘法的中性元素，讓上一層可以 `* edge_weight`。
- **失敗邊界**: 遍歷完所有鄰居後，仍未收到「Found」信號。
  - **回傳值**: `-1.0`，作為明確的「Not Found」信號。

### 程式碼實現

```cpp
double dfs(string& current, string& end, ..., unordered_set<string>& visited) {
    // Base Case: 到達終點
    if (current == end) {
        return 1.0; // 回傳「Found」信號與計算初始值
    }

    // Pre-order Logic: 標記當前狀態
    visited.insert(current);

    // 遍歷子問題
    for (auto& [neighbor, weight] : graph[current]) {
        if (!visited.contains(neighbor)) {
            // 遞迴呼叫
            double result_from_neighbor = dfs(neighbor, end, ..., visited);

            // Post-order Logic: 處理子問題回傳值
            // 1. 檢查信號
            if (result_from_neighbor != -1.0) {
                // 2. 結合當前狀態並立即返回
                return result_from_neighbor * weight;
            }
        }
    }

    // 失敗邊界: 所有路徑都走不通
    return -1.0; // 回傳「Not Found」信號
}
```

---

## 3. 遞迴設計模式：多路徑結果聚合

**目標**: 需要遍歷**所有**從起點可達的路徑，並將它們的結果聚合起來（例如：計算所有可能路徑的數量）。

### 設計差異

- **Post-order Logic**: 不再是找到一個解就立即返回，而是需要一個**局部變數**來累積所有子問題的結果。
- **失敗邊界**: 即使一個分支是死路，它也可能回傳一個對聚合有意義的值（如 `0`），而不是一個「信號」。

### 範例：計算從 `start` 到 `end` 的所有路徑數量

```cpp
int countPaths(int current, int end, ..., unordered_set<int>& visited) {
    // Base Case: 到達終點，找到一條路徑
    if (current == end) {
        return 1; // 返回一個計數
    }

    // Pre-order Logic
    visited.insert(current);

    // Post-order Logic: 聚合所有子路徑的結果
    int total_paths = 0;
    for (int neighbor : graph[current]) {
        if (visited.find(neighbor) == visited.end()) {
            total_paths += countPaths(neighbor, end, ..., visited);
        }
    }

    // 回溯 (可選，取決於是否需要在不同分支中重用節點)
    visited.erase(current);

    return total_paths; // 返回當前節點出發的所有路徑總數
}
```

---

## ✅ 總結

將 DFS 應用於路徑查找與值聚合問題時，成功的關鍵在於遵循遞迴設計心法：

1. **定義狀態**: 確定函式需要哪些資訊。
2. **設計回傳值**: 讓回傳值清晰地表達「信號」與「計算結果」。
3. **處理遞迴關係**: 在 Pre-order 和 Post-order 位置執行正確的操作，特別是在 Post-order 位置解析子問題的回傳值。
4. **明確邊界**: 設計好成功與失敗的終止條件。
