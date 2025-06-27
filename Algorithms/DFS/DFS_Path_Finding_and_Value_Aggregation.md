# DFS 心法：路徑查找與值的聚合 (Path Finding and Value Aggregation)

當使用 DFS 在圖中不僅僅是為了遍歷，而是為了**查找一條從起點到終點的路徑**並**計算路徑上的聚合值**（如乘積、總和等）時，遞迴的設計需要遵循特定的模式。

---

## 1. 核心思想：遞迴的雙重角色

在這種模式下，DFS 遞迴函數同時扮演兩個角色：

1. **信號員 (Signaler)**: 它的回傳值首先是一個「信號」，告訴上一層呼叫者「我是否找到了通往終點的路徑？」。
2. **計算員 (Calculator)**: 如果找到了路徑，回傳值中還攜帶了「從我當前位置到終點的計算結果」。

### 案例：LeetCode 399. Evaluate Division

- **問題**: 計算 `a / b` 的值，本質是查找從 `a` 到 `b` 的路徑，並將路徑上所有邊的權重相乘。
- **信號**:
  - 回傳 `-1.0` 代表「此路不通 (Not Found)」。
  - 回傳任何非 `-1.0` 的值代表「路已找到 (Found)」。
- **計算**:
  - 如果 `current == end` (到達終點)，回傳 `1.0` 作為乘法的中性元素。
  - 如果從鄰居 `neighbor` 找到了路徑 (非 `-1.0` 的回傳值)，則將當前邊的權重 `weight` 與 `neighbor` 回傳的結果相乘，得到從 `current` 到終點的結果。

---

## 2. 遞迴設計的關鍵原則 (Key Principles of Recursive Design)

### Principle 1: Base Case 必須回傳「初始值」與「信號」

- **Base Case (遞迴終止條件)**: 當 `current == end` 時，你已經在終點了。
- **回傳設計**:

  - **信號**: 你已經「找到」了路徑。
  - **初始值**: 為了讓上一層能進行計算，你需要回傳一個「中性元素」。對於乘法，它是 `1.0`；對於加法，它是 `0.0`。

  ```cpp
  // Base Case: 到達終點
  if (current == end) {
      return 1.0; // 信號：找到了！ 初始值：1.0
  }
  ```

### Principle 2: 呼叫點必須分離「信號判斷」與「結果計算」

- 在遍歷鄰居的迴圈中，當你呼叫遞迴函數後，不能直接使用其回傳值。
- **第一步：檢查信號**。先判斷回傳值是否為「Not Found」的信號（如 `-1.0`）。
- **第二步：結合當前狀態**。如果信號是「Found」，才將回傳的結果與當前節點的狀態（如邊的權重）結合。

  ```cpp
  // 抽象化的遞迴呼叫點
  for (auto& edge : graph.get_neighbors(current)) {
      Node neighbor = edge.get_neighbor();

      if (!visited.contains(neighbor)) {
          visited.insert(neighbor);

          // 遞迴呼叫，傳遞上下文
          ReturnType result_from_neighbor = dfs(neighbor, target, visited);

          // 1. 檢查信號 (Signal Check)
          if (result_from_neighbor.is_found()) {

              // 2. 結合當前狀態 (Combine with Current State)
              //    'edge.get_property()' 可能是權重、類型等
              return combine(result_from_neighbor, edge.get_property());
          }
      }
  }
  ```

### Principle 3: 理解鄰居遍歷的兩種視角

在設計遞迴時，要清楚你是在處理以下哪種情況：

1. **單一路徑查找 (Single Path Finding)**:

   - **目標**: 只要找到**任何一條**通往終點的路徑即可。
   - **行為**: 一旦某個鄰居的遞迴呼叫回傳了「Found」信號，就**立即停止搜索**其他鄰居，並將結果層層傳回。

   ```cpp
   // 抽象化的單一路徑查找
   if (result_from_neighbor.is_found()) {
       // 結合結果並立即回傳，不再搜索其他鄰居
       return combine(result_from_neighbor, edge.get_property());
   }
   ```

2. **多路徑結果聚合 (Multi-Path Aggregation)**:

   - **目標**: 需要遍歷**所有**鄰居，並將它們的結果聚合起來（例如：計算所有可能路徑的數量、找到所有路徑中的最短/最長路徑）。
   - **行為**: 你需要一個局部變數來累積所有鄰居回傳的結果，直到迴圈結束才回傳總的聚合結果。
   - **範例**: 尋找圖中所有從 A 到 B 的路徑數量。

   ```cpp
   // 抽象化的多路徑聚合
   ResultType aggregated_result = initial_value;
   for (auto& edge : graph.get_neighbors(current)) {
       Node neighbor = edge.get_neighbor();

       // 取得來自一個分支的結果
       ReturnType result_from_neighbor = dfs(neighbor, target, visited);

       // 將該分支結果聚合到總結果中
       aggregated_result = aggregate(aggregated_result, result_from_neighbor);
   }
   return aggregated_result;
   ```

---

## 3. 應用於樹 (Application to Trees)

這些原則同樣適用於樹的遍歷，但有兩個關鍵的簡化：

1. **鄰居即子節點 (Neighbors are Children)**:

   - 在圖中，你需要一個鄰接表來找到 `neighbors`。
   - 在樹中，鄰居就是明確的 `left` 和 `right` 子節點。

2. **無需 `visited` 集合 (No `visited` Set Needed)**:
   - 樹是無環圖 (acyclic graph)，從父節點往下走，絕不會回到訪問過的節點。
   - 因此，在樹的 DFS 中，你不需要 `visited` 集合來防止無限循環。

---

## ✅ 總結

將 DFS 用於圖的路徑查找與值聚合問題時，成功的關鍵在於將遞迴函數的回傳值設計成一個**同時包含「狀態信號」和「計算結果」的複合資訊**。通過在呼叫點正確地解析這個回傳值，你就能優雅地解決這類複雜的遞迴問題。

對於樹，這個模式同樣適用，但可以省去 `visited` 集合的開銷。
