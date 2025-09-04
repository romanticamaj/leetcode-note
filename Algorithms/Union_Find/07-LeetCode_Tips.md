# Union-Find 解題技巧

## 1. 熟記模板

Disjoint Set 的程式碼高度模組化。強烈建議理解並熟記「按秩合併」與「路徑壓縮」結合的最佳化模板。在面試或解題時，能夠快速、準確地寫出這個模板是成功的一半。

## 2. 適用場景

當題目涉及以下概念時，可以高度懷疑是 Union-Find 的應用場景：

- **動態連通性 (Dynamic Connectivity)**: 需要不斷地合併集合，並查詢兩點的連通狀態。
- **判斷環的存在**: 在遍歷邊的過程中，若一條邊的兩個端點在 `union` 之前就已經 `connected`，則加入這條邊必然會形成環。
- **計算連通分量 (Connected Components)**: 可以透過一個 `count` 變數來追蹤。每成功 `union` 一次，`count` 就減一。

## 3. 節點表示

Union-Find 最適合處理的節點是已經被編號為 `0` 到 `n-1` 的整數。如果題目給的節點是其他形式（如座標 `(x, y)`、字串等），需要先將其**映射**到 `0` 到 `n-1` 的整數 ID，才能使用 `parent` 陣列。

## 4. 兩種 Union 策略

在處理邊列表時，有兩種常見的策略：

1. **先檢查再合併 (Check then Union)**:

   - `if (!disjointSet.connected(x, y)) { disjointSet.unionSet(x, y); }`
   - 這種寫法在邏輯上更清晰，適用於需要根據「是否已連通」來做不同決策的場景（例如判斷環）。

2. **無條件合併 (Unconditional Union)**:

   - `disjointSet.unionSet(x, y);`
   - 這種寫法更簡潔，因為 `union` 函式內部已經包含了 `find` 和 `rootX != rootY` 的檢查。適用於只關心最終連通狀態，而不在乎合併過程的場景。

3. **帶有回傳值的合併 (Union with Return Value)**:

   - 這是一種更強大、更推薦的實作模式。讓 `unionSet` 函式回傳一個布林值，表示這次操作是否**真正**發生了合併。
   - **實作**:

   ```cpp
      bool unionSet(int x, int y) {
         int rootX = find(x);
         int rootY = find(y);
         if (rootX != rootY) {
               // ... 合併邏輯 ...
               return true; // 真正發生了合併
         }
         return false; // 原本就已連通
      }
   ```

- **優點**: 呼叫端可以根據回傳值來執行相應操作，讓程式碼更優雅。
  - **計算連通分量**: `if (disjointSet.unionSet(x, y)) { count--; }`
  - **判斷環**: `if (!disjointSet.unionSet(x, y)) { return true; } // 發現環`
  - **提早返回**: 在某些問題中（如 Kruskal 演算法），一旦所有節點都已連通（`count == 1`），就可以提早結束迴圈。

總之，如果題目給的是一個邊列表，又要判斷圖的連通性相關屬性（如環、連通分量數），Union-Find 是一個非常強大的工具。
