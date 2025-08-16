# Bellman-Ford 的動態規劃基礎

Bellman-Ford 演算法的核心思想可以從動態規劃 (Dynamic Programming) 的角度來理解。它解決的是「單源最短路徑問題」，特別是能夠處理帶有負權重邊的圖。其 DP 模型的核心是**限制路徑上所包含的邊的數量**。

## 核心定理

> **定理**：在一個包含 `N` 個頂點且沒有負權重環的圖中，任意兩點之間的最短路徑最多包含 `N-1` 條邊。

這個定理是 Bellman-Ford 演算法及其所有變體能夠成立的基石。它告訴我們，尋找最短路徑的過程是有界的：我們只需要考慮長度不超過 `N-1` 的路徑即可。

---

## 1. 核心概念：以邊數為狀態的動態規劃

我們將最短路徑問題轉化為一個可以逐步求解的 DP 問題。

### DP 狀態設計

我們定義一個二維狀態 `DP[k][v]`，其意義為：

> **`DP[k][v]`**: 從源點 `s` 出發，**經過至多 `k` 條邊**，到達頂點 `v` 的最短路徑權重。

### DP 遞迴關係式 (Recurrence Relation)

為了計算 `DP[k][v]`，我們有兩種可能構成到達 `v` 的路徑：

1. **路徑不超過 `k-1` 條邊**: 這條路徑的最短權重已經由 `DP[k-1][v]` 給出。
2. **路徑恰好有 `k` 條邊**: 這意味著路徑的最後一步是從某個鄰居 `u` 走 `(u, v)` 這條邊過來的。這條路徑的權重就是 `DP[k-1][u] + w(u, v)`。

我們需要遍歷所有指向 `v` 的邊 `(u, v)`，找出能讓 `DP[k-1][u] + w(u, v)` 最小的那個 `u`。

綜合起來，遞迴關係式為：

**`DP[k][v] = min(DP[k-1][v], DP[k-1][u] + w(u, v))`** for all edges `(u, v)` incoming to `v`.

這個公式的本質就是 Bellman-Ford 演算法中的**鬆弛 (Relaxation)** 操作。

---

## 2. CLRS 虛擬碼與 C++ 實作

### CLRS 經典虛擬碼

CLRS 的 `BELLMAN-FORD` 虛擬碼沒有顯式地使用 DP 表，而是透過 `V-1` 次對所有邊的迭代鬆弛來隱含地建立這個過程。

```
INITIALIZE-SINGLE-SOURCE(G, s)
1 for each vertex v ∈ G.V
2     v.d = ∞
3     v.π = NIL
4 s.d = 0

RELAX(u, v, w)
1 if v.d > u.d + w(u, v)
2     v.d = u.d + w(u, v)
3     v.π = u

BELLMAN-FORD(G, w, s)
1 INITIALIZE-SINGLE-SOURCE(G, s)
2 for i = 1 to |G.V| - 1
3     for each edge (u, v) ∈ G.E
4         RELAX(u, v, w)
5 // Check for negative-weight cycles
6 for each edge (u, v) ∈ G.E
7     if v.d > u.d + w(u, v)
8         return FALSE
9 return TRUE
```

- `INITIALIZE-SINGLE-SOURCE` 初始化所有點的距離為無限大，源點為 0。
- `RELAX` 是核心鬆弛操作。
- 主迴圈 `for i = 1 to |G.V| - 1` 正對應了 DP 狀態中的 `k`，從 1 迭代到 `V-1`。第 `i` 次外層迴圈結束後，`v.d` 中儲存的就是從源點出發，經過至多 `i` 條邊到達 `v` 的最短路徑。

### C++ 實作：從 DP 角度出發

以下是將 DP 思想直接轉化為程式碼的三種版本。

#### a. Top-Down DP with Memoization (由上而下與記憶化)

這種方法使用遞迴來求解，並用一個 `memo` 表（即 `distances`）來儲存已計算過的子問題結果，避免重複計算。

```cpp
#include <vector>
#include <limits>

const int INF = std::numeric_limits<int>::max();

// 遞迴 DP 的輔助函式
void find_shortest_path_recursive(
    int target_node,
    int max_edges,
    const std::vector<std::vector<int>>& edges,
    std::vector<std::vector<int>>& memo) {

    // 基礎情況：如果此狀態的結果已被計算，直接返回。
    if (memo[max_edges][target_node] != INF) {
        return;
    }

    // 基礎情況：0 條邊的路徑。如果目標是源點，距離為 0，否則為無限大。
    // 這通常在主遞迴呼叫前透過初始化處理。

    // 遞迴步驟：透過計算至多 max_edges - 1 條邊的路徑，來求解至多 max_edges 條邊的路徑。
    find_shortest_path_recursive(target_node, max_edges - 1, edges, memo);

    // 至多 max_edges 條邊的路徑，其長度至少與至多 max_edges - 1 條邊的路徑一樣短。
    memo[max_edges][target_node] = memo[max_edges - 1][target_node];

    // 遍歷所有邊，尋找是否能透過某個鄰居 `u` 找到更短的路徑。
    for (const auto& edge : edges) {
        int u = edge[0];
        int v = edge[1];
        int weight = edge[2];

        if (v == target_node) {
            // 確保使用 `max_edges - 1` 條邊能到達鄰居 `u`。
            if (memo[max_edges - 1][u] != INF) {
                memo[max_edges][target_node] = std::min(
                    memo[max_edges][target_node], // 本質上是 memo[max_edges - 1][target_node]
                    memo[max_edges - 1][u] + weight
                );
            }
        }
    }
}

// 主函式
int bellman_ford_top_down(int n, const std::vector<std::vector<int>>& edges, int src, int dst, int k) {
    // memo[k][v]: 使用至多 k 條邊到達 v 的最短路徑。
    std::vector<std::vector<int>> memo(k + 1, std::vector<int>(n, INF));

    // 初始化 0 條邊的路徑。
    memo[0][src] = 0;

    // 遞迴地尋找使用至多 k 條邊到達 dst 的最短路徑。
    find_shortest_path_recursive(dst, k, edges, memo);

    return memo[k][dst] == INF ? -1 : memo[k][dst];
}
```

#### b. Bottom-Up DP with Tabulation (由下而上與表格法)

此版本直接使用迴圈迭代，從 `k=1` 開始，逐步建立 `dp_table`。

```cpp
#include <vector>
#include <limits>
#include <algorithm>

const int INF = std::numeric_limits<int>::max();

int bellman_ford_bottom_up(int n, const std::vector<std::vector<int>>& edges, int src, int dst, int k) {
    // dp_table[k][v]: 使用至多 k 條邊到達 v 的最短路徑。
    std::vector<std::vector<int>> dp_table(k + 1, std::vector<int>(n, INF));

    // 基礎情況：0 條邊的路徑。
    dp_table[0][src] = 0;

    // 根據允許的邊數進行迭代，從 1 到 k。
    for (int i = 1; i <= k; ++i) {
        // 用前一個狀態的結果初始化當前狀態。
        dp_table[i] = dp_table[i - 1];

        // 鬆弛所有邊。
        for (const auto& edge : edges) {
            int u = edge[0];
            int v = edge[1];
            int weight = edge[2];

            if (dp_table[i - 1][u] != INF) {
                dp_table[i][v] = std::min(dp_table[i][v], dp_table[i - 1][u] + weight);
            }
        }
    }

    return dp_table[k][dst] == INF ? -1 : dp_table[k][dst];
}
```

#### c. Bottom-Up DP with Space Optimization (空間優化)

我們觀察到計算 `DP[k]` 的狀態只依賴於 `DP[k-1]`。因此，我們可以用兩個一維陣列來代替二維 DP 表，將空間複雜度從 `O(k*V)` 優化到 `O(V)`。

```cpp
#include <vector>
#include <limits>
#include <algorithm>

const int INF = std::numeric_limits<int>::max();

int bellman_ford_space_optimized(int n, const std::vector<std::vector<int>>& edges, int src, int dst, int k) {
    std::vector<int> dist(n, INF);
    dist[src] = 0;

    // 根據允許的邊數進行迭代，從 1 到 k。
    for (int i = 1; i <= k; ++i) {
        // 建立前一個狀態（k-1 條邊）的快照。
        std::vector<int> prev_dist = dist;

        // 根據前一個狀態來鬆弛所有邊。
        for (const auto& edge : edges) {
            int u = edge[0];
            int v = edge[1];
            int weight = edge[2];

            // 重要：必須從快照 (prev_dist) 中讀取，以避免使用到當前迭代 (k 條邊) 的資訊。
            if (prev_dist[u] != INF) {
                dist[v] = std::min(dist[v], prev_dist[u] + weight);
            }
        }
    }

    return dist[dst] == INF ? -1 : dist[dst];
}
```

##### 為何需要 `prev_dist` 快照？

這個問題觸及了 DP 狀態轉移的核心。我們的 DP 定義是 `DP[k][v]`，代表使用**至多 `k` 條邊**到達 `v` 的最短路徑。這個狀態的計算**嚴格依賴**於前一個狀態 `DP[k-1]`。

- **如果使用快照 (`prev_dist`)**:
  在第 `i` 輪迴圈中，我們所有的鬆弛操作 `dist[v] = min(dist[v], prev_dist[u] + weight)` 都是讀取 `prev_dist` 的值。`prev_dist` 完整地保存了第 `i-1` 輪的結果。這確保了第 `i` 輪更新所產生的新路徑，其邊數恰好是在 `i-1` 條邊的路徑基礎上再增加一條，完美地符合了「至多 `i` 條邊」的定義。

- **如果不使用快照 (錯誤示範)**:
  假設我們這樣寫：
  ```cpp
  // 錯誤的寫法
  for (int i = 1; i <= k; ++i) {
      for (const auto& edge : edges) {
          int u = edge[0];
          int v = edge[1];
          int weight = edge[2];
          if (dist[u] != INF) {
              dist[v] = std::min(dist[v], dist[u] + weight);
          }
      }
  }
  ```
  考慮一個路徑 `s -> a -> b`。在第 `i` 輪的內層 `for` 迴圈中，如果邊 `(s, a)` 恰好在邊 `(a, b)` 之前被處理：
  1. `dist[a]` 會先被 `dist[s]` 更新。此時 `dist[a]` 代表的是一個**至多 `i` 條邊**的路徑。
  2. 接著處理邊 `(a, b)` 時，我們會用**剛剛在同一輪更新**的 `dist[a]` 去更新 `dist[b]`。
  3. 這導致 `dist[b]` 的值是基於一個 `i` 邊路徑 (`s` 到 `a`) 再加上一條邊 `(a, b)`，總共 `i+1` 條邊。
  
  這就破壞了我們「在第 `i` 輪只計算至多 `i` 條邊路徑」的狀態定義。演算法退化成了標準的 Bellman-Ford，失去了對邊數 `k` 的嚴格限制。因此，為了在空間優化的同時維持 DP 狀態的正確性，建立前一狀態的快照是**必須的**。

---

## 3. 正確性證明 (Correctness Proof)

此 DP 解法的正確性基於一個關鍵定理。

**定理**: 在一個包含 `V` 個頂點且**沒有負權重環**的圖中，任意兩點之間的最短路徑最多包含 `V-1` 條邊。

**證明 (反證法)**:
假設存在一條從 `s` 到 `v` 的最短路徑 `p`，它包含了 `V` 條或更多的邊。這意味著路徑上至少有 `V+1` 個頂點。根據鴿巢原理，路徑中必定至少有一個頂點被訪問了兩次，從而形成一個環。

- 如果這個環的權重為正，那麼移除這個環會得到一條更短的路徑，與 `p` 是最短路徑的假設矛盾。
- 如果這個環的權重為零，移除它會得到一條權重相同但邊數更少的路徑。
- 如果這個環的權重為負，我們就可以不斷地走這個環來無限減小路徑權重，這意味著不存在最短路徑，與問題前提（圖中無負權重環）矛盾。

因此，任何最短路徑的邊數都不會超過 `V-1`。我們的 DP 演算法迭代 `V-1` 次（或題目指定的 `k` 次），確保了在第 `i` 次迭代結束時，我們已經找到了所有使用至多 `i` 條邊的最短路徑。當 `i` 達到 `V-1` 時，我們就找到了全局的最短路徑。

---

## 4. 複雜度分析

- **`V`**: 圖中的頂點數 (vertices)
- **`E`**: 圖中的邊數 (edges)
- **`k`**: 允許的最大邊數

### 時間複雜度 (Time Complexity): `O(k * E)`

- **Top-Down**: 每個狀態 `(i, v)` for `0 <= i <= k` and `0 <= v < V` 只會被計算一次。在計算每個狀態時，我們最壞需要遍歷所有邊，因此是 `O(E)`。總時間為 `O(k * V * E)`，但更精確的分析是，遞迴的深度是 `k`，每層遞迴中遍歷所有邊，因此是 `O(k * E)`。
- **Bottom-Up**: 外層迴圈執行 `k` 次。內層迴圈遍歷所有 `E` 條邊進行鬆弛操作。因此，總時間複雜度為 `O(k * E)`。
- 如果問題是標準的 Bellman-Ford（找到全局最短路徑），則 `k = V-1`，時間複雜度為 `O(V * E)`。

### 空間複雜度 (Space Complexity)

- **Top-Down / Bottom-Up (Tabulation)**: `O(k * V)`
  - 需要一個 `k x V` 的二維陣列來儲存 DP 狀態。
- **Bottom-Up (Space Optimized)**: `O(V)`
  - 我們只需要兩個一維陣列（一個儲存當前狀態，一個儲存前一狀態），因此空間被優化到 `O(V)`。
