# Dijkstra 演算法深度解析：從理論到 C++ 實踐

Dijkstra 演算法是圖論中解決「單源最短路徑問題」(Single-Source Shortest Path, SSSP) 的經典演算法，其核心應用場景是**帶有非負權重 (non-negative weights) 的圖**。

本文將遵循從經典理論到現代 C++ 實踐的思路，深入探討 Dijkstra 演算法，幫助讀者建立一個完整且清晰的知識體系。

---

## tl;dr - 重點摘要

1. **理論核心 (CLRS)**: 演算法維護一個包含**所有**節點的優先佇列，並依賴 `DECREASE-KEY` 操作來更新節點距離。這在理論上很完美，但在標準 C++ 中難以高效實現。
2. **C++ 實踐**: 我們不使用 `DECREASE-KEY`，而是採用「**惰性刪除 (Lazy Deletion)**」策略：當發現更短路徑時，不更新舊記錄，而是直接將 `(新距離, 節點)` **插入**優先佇列。
3. **關鍵優化**: 為了處理「惰性刪除」產生的重複節點，我們在從佇列取出節點時，必須進行「**提前剪枝**」：`if (d > dist[u]) continue;`。這個檢查會忽略所有過時的、較長的路徑記錄。
4. **實現流程**:
   - 維護 `dist` 陣列，初始化為無限大。
   - 將 `(0, start_node)` 推入優先佇列。
   - 迴圈直到佇列為空，每次取出距離最小的節點，進行剪枝檢查，然後對其鄰居執行「鬆弛 (Relaxation)」操作。

---

## 1. 經典演算法 (教科書版本)

在經典演算法教科書如 _Introduction to Algorithms_ (CLRS) 中，Dijkstra 的虛擬碼通常假設優先佇列支援一個 `DECREASE-KEY` 操作。

### CLRS 虛擬碼解析

```
DIJKSTRA(G, w, s)
1  INITIALIZE-SINGLE-SOURCE(G, s)  // 將所有節點距離設為 ∞，起點設為 0
2  S = ∅                           // S 是已確定最短路徑的節點集合
3  Q = G.V                         // Q 是一個包含所有節點的優先佇列
4  while Q ≠ ∅
5      u = EXTRACT-MIN(Q)          // 取出距離最近的節點
6      S = S ∪ {u}
7      for each vertex v ∈ G.Adj[u]
8          RELAX(u, v, w)          // 鬆弛操作，內部隱含 DECREASE-KEY
```

這個版本的核心在於：

- **積極初始化 (Eager Initialization)**: 一開始就把所有節點放入優先佇列 `Q`。
- **依賴 `DECREASE-KEY`**: `RELAX` 操作在更新節點距離時，會直接在 `Q` 中**更新**該節點的優先級。

---

## 2. C++ 實作框架 (實用版本)

由於標準 C++ 的 `std::priority_queue` 不提供高效的 `DECREASE-KEY` 方法，我們採用了更符合其 API 的「惰性刪除」策略。

### C++ 程式碼

```cpp
#include <iostream>
#include <vector>
#include <queue>
#include <limits>

const int INF = std::numeric_limits<int>::max();
using Graph = std::vector<std::vector<std::pair<int, int>>>;

void dijkstra(int start_node, int num_nodes, const Graph& adj) {
    std::vector<int> dist(num_nodes, INF);
    std::priority_queue<std::pair<int, int>,
                        std::vector<std::pair<int, int>>,
                        std::greater<std::pair<int, int>>> pq;

    // 懶惰初始化 (Lazy Initialization): 只放入起點
    dist[start_node] = 0;
    pq.push({0, start_node});

    while (!pq.empty()) {
        int [d, u] = pq.top(); pq.pop();

        // 關鍵優化：提前剪枝 (處理惰性刪除的後果)
        if (d > dist[u]) continue; // 一定是大於，若等於的話，第一個 node 就沒辦法處理

        for (const auto& [v, weight] : adj[u]) {
            // 鬆弛操作 (Relaxation)
            if (dist[u] + weight < dist[v]) {
                dist[v] = dist[u] + weight;

                // 不更新，直接插入新記錄
                pq.push({dist[v], v});
            }
        }
    }
    // ... (輸出結果)
}
```

---

## 3. 深入探討：理論與實踐的橋樑

### 關鍵差異 1: `DECREASE-KEY` vs. 「惰性刪除」

| 特性 (Feature) | CLRS 理論版本 (`DECREASE-KEY`)     | C++ `std::priority_queue` 實作 (Lazy Deletion) |
| :------------- | :--------------------------------- | :--------------------------------------------- |
| **佇列內容**   | 每個節點**永遠只有一個副本**。     | 可能存在同一個節點的**多個副本**。             |
| **更新方式**   | 直接在佇列中**更新**元素的優先級。 | **不更新**舊元素，而是**插入**一個新元素。     |
| **處理冗餘**   | 無冗餘資料。                       | 依賴「提前剪枝」來**忽略**冗餘資料。           |

**為什麼 C++ 採用「惰性刪除」？**
因為 `std::priority_queue` API 簡單，不提供 `DECREASE-KEY`。而「惰性刪除」的實作非常直觀，且在保持 `O(E log V)` 時間複雜度的前提下，已經足夠高效。

### 關鍵差異 2: 佇列初始化與 `S` 集合

- **`S = S ∪ {u}` 的作用**:
  在理論中，`S` 是**已確定最短路徑的節點集合**，是演算法正確性證明的核心。在 C++ 實作中，我們**不需要**明確的 `S` 集合。一個節點 `u` 在**首次**被從優先佇列取出並通過剪枝檢查時，就等同於被加入了 `S`。

- **佇列初始化策略**:
  - **CLRS (Eager)**: 一開始將所有節點放入佇列，依賴 `DECREASE-KEY`。
  - **C++ (Lazy)**: 一開始只放起點，後續只放入被鬆弛過的節點。這種方式更高效，因為它避免了處理大量距離仍為無限大的無關節點，特別是在圖不連通或稀疏時。

總結來說，我們在 C++ 中看到的實作，是用**更簡單的資料結構 (`std::priority_queue`)** 和一個**巧妙的剪枝技巧**，來模擬理論上更複雜的 `DECREASE-KEY` 操作，並在實踐中達到了同樣優秀的時間複雜度。
