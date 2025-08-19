# 心法：從並查集還原連通分量 (Reconstructing Connected Components)

在使用並查集 (Disjoint Set) 處理完所有邊的 `union` 操作後，我們得到了一個隱含的森林結構，其中 `parent` 陣列記錄了每個節點的父節點。然而，在很多題目中，我們不僅需要知道兩個節點是否連通，還需要**明確地列出每個連通分量 (Connected Component) 中的所有成員**。

本篇將介紹如何從一個成熟的並查集結構中，高效地還原並建構出所有的連通分量。

---

## 1. 核心思想：以根為名，聚集成群

並查集經過路徑壓縮優化後，有一個非常重要的特性：

> **在同一個連通分量中的所有節點，其最終的根節點 (root) 都是相同的。**

這個特性為我們提供了分組的依據。我們可以遍歷每一個節點，找到它所屬的根，然後將其歸類到以該根為「代表」的群組中。

---

## 2. 實作策略：使用雜湊表進行分組

最高效且直觀的實作方式是使用一個**雜湊表 (Hash Map)**。

- **資料結構**: `std::unordered_map<int, std::vector<int>>`
- **鍵 (Key)**: 連通分量的**根節點** `root`。
- **值 (Value)**: 一個**列表 (vector)**，儲存所有根為 `root` 的節點。

### 演算法步驟

1. **初始化**: 創建一個空的 `unordered_map<int, vector<int>> components;`。
2. **遍歷節點**: 對於圖中的每一個節點 `i`（從 `0` 到 `n-1`）：
   a. 使用 `find(i)` 操作找到節點 `i` 的根 `root`。
   b. 將節點 `i` 加入到以 `root` 為鍵的列表中：`components[root].push_back(i);`。
3. **完成**: 遍歷結束後，`components` 這個 map 中就儲存了所有連通分量。`map` 的大小就是連通分量的數量，每個 `value` (vector) 就是一個連通分量的完整成員列表。

> **💡 重要性質**: 由於我們的遍歷是從 `i = 0` 到 `n-1`，是嚴格遞增的，因此 `push_back` 到每個 `vector` 中的節點順序也將是**嚴格遞增**的。這意味著最終得到的每個連通分量列表，其成員都已**自動排序**，無需額外處理。

---

## 3. C++ 程式碼範例

假設我們已經有一個完整實現的 `DSU` 類，包含了路徑壓縮和按秩合併/按大小合併的優化。其標準實作可參考：

- [`06-Optimized_Implementation_and_Analysis.md`](./06-Optimized_Implementation_and_Analysis.md)

以下函數展示了如何基於一個 `dsu` 物件來還原所有連通分量。

```cpp
#include <vector>
#include <unordered_map>

// 核心還原函數
// 參數 n: 節點總數
// 參數 dsu: 一個已經處理完所有 union 操作的 DSU 物件
std::unordered_map<int, std::vector<int>> get_connected_components(int n, DSU& dsu) {
    std::unordered_map<int, std::vector<int>> components;

    for (int i = 0; i < n; ++i) {
        int root = dsu.find(i);
        components[root].push_back(i);
    }

    return components;
}

/*
// 使用範例
int n = 10;
DSU dsu(n); // 假設 DSU 類已在別處定義

// 執行一系列的 union 操作
dsu.unite(0, 1);
dsu.unite(1, 2);
dsu.unite(3, 4);
dsu.unite(5, 6);
dsu.unite(6, 7);
dsu.unite(8, 9);

// 還原所有連通分量
auto all_components = get_connected_components(n, dsu);

// all_components 的結果將會類似：
// {
//   2: [0, 1, 2],  // 假設 2 是此分量的根
//   4: [3, 4],     // 假設 4 是此分量的根
//   7: [5, 6, 7],  // 假設 7 是此分量的根
//   9: [8, 9]      // 假設 9 是此分量的根
// }
// (根的具體值取決於 unite 的實現細節，但分組結果是確定的)
*/
```

---

## 4. 複雜度分析

- **時間複雜度**: `O(N * α(N))`

  - 我們需要遍歷 `N` 個節點。
  - 對於每個節點，我們執行一次 `find` 操作，其攤銷時間複雜度為 `α(N)`（反阿克曼函數，幾乎為常數）。
  - 因此，總時間複雜度為 `O(N * α(N))`。

- **空間複雜度**: `O(N)`
  - 雜湊表需要儲存 `N` 個節點，無論它們被分到多少個組中，總數都是 `N`。

這個方法在時間和空間上都非常高效，是處理並查集後續分析的標準模式。
