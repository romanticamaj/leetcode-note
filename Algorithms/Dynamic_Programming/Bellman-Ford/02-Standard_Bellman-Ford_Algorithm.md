# 標準 Bellman-Ford 最短路徑演算法

基於動態規劃的方法為 Bellman-Ford 提供了堅實的理論基礎，但標準的 Bellman-Ford 演算法通常以更直接的迭代過程呈現。此版本捨棄了明確的「邊數」狀態（`k`），而是專注於重複地鬆弛所有邊，直到最短路徑的距離收斂為止。

---

## 1. 核心概念：迭代鬆弛

標準 Bellman-Ford 演算法的運作方式非常直觀：

1. **初始化 (Initialization)**: 將源點 `s` 的距離設為 0，所有其他頂點的距離設為無限大。
2. **迭代鬆弛 (Iterative Relaxation)**: 重複地對圖中的**每一條邊**進行鬆弛操作。這個過程總共執行 `V-1` 次。

每一次完整地遍歷圖中所有的邊並進行鬆弛，我們稱之為一輪 (a round or a pass)。經過 `V-1` 輪後，如果圖中沒有負權重環，演算法保證能找到所有從源點出發的最短路徑。

### 與 DP 版本的關係

- **DP 版本**: 第 `k` 次迭代計算的是**至多 `k` 條邊**的最短路徑。
- **標準版本**: 第 `k` 輪迭代**不能保證**找到的是恰好 `k` 條邊的最短路徑。因為邊的鬆弛順序是任意的，可能在一輪內，一條路徑上的多個邊被連續鬆弛，從而提前更新了距離。例如，如果邊 `(s, a)`, `(a, b)`, `(b, c)` 按順序被處理，那麼在第一輪迭代中就能找到長度為 3 的路徑 `s->a->b->c`。

然而，經過 `V-1` 輪完整的迭代後，其最終結果與 DP 版本是等價的，因為任何不含環的最短路徑最多只有 `V-1` 條邊。

### 提早終止優化 (Early Termination)

一個關鍵的優化是：如果在某一輪完整的迭代中，**沒有任何頂點的 `dist` 值被成功更新**，這意味著所有的最短路徑都已經找到，演算法可以提早終止，無需執行完剩下的輪次。

---

## 2. C++ 實作說明

以下是標準 Bellman-Ford 演算法的 C++ 實作，包含了提早終止的優化。

```cpp
#include <vector>
#include <limits>
#include <iostream>

const int INF = std::numeric_limits<int>::max();

// 如果找到最短路徑則返回 true，如果檢測到負循環則返回 false。
// 距離儲存在 `dist` 向量中。
bool bellman_ford(int n, const std::vector<std::vector<int>>& edges, int src, std::vector<int>& dist) {
    dist.assign(n, INF);
    dist[src] = 0;

    // 重複鬆弛邊 V-1 次
    for (int i = 1; i <= n - 1; ++i) {
        bool updated = false;

        for (const auto& edge : edges) {
            int u = edge[0];
            int v = edge[1];
            int weight = edge[2];

            if (dist[u] != INF && dist[u] + weight < dist[v]) {
                dist[v] = dist[u] + weight;
                updated = true;
            }
        }

        if (!updated) break; // 提早終止優化
    }

    // 再進行一輪鬆弛以檢測負循環。
    for (const auto& edge : edges) {
        int u = edge[0];
        int v = edge[1];
        int weight = edge[2];

        if (dist[u] != INF && dist[u] + weight < dist[v]) {
            // 如果仍然可以鬆弛，則存在負循環。
            return false;
        }
    }

    return true;
}
```

---

## 3. 正確性說明

演算法的正確性依賴於**路徑鬆弛屬性 (Path-relaxation property)**。

**引理**: 假設 `p = <v0, v1, ..., vk>` 是一條從源點 `s=v0` 到 `vk` 的最短路徑。如果我們按照 `(v0, v1)`, `(v1, v2)`, ..., `(vk-1, vk)` 的順序對邊進行鬆弛，那麼 `dist[vk]` 將會等於實際最短路徑 `δ(s, vk)`，且這個值在此之後不會再改變。

**證明**:

- 鬆弛 `(v0, v1)` 後，`dist[v1] = δ(s, v1)`。
- 接著鬆弛 `(v1, v2)`，由於 `dist[v1]` 已達最優，`dist[v2]` 也會被更新為 `dist[v1] + w(v1, v2) = δ(s, v2)`。
- 這個過程依序進行，最終 `dist[vk]` 會被正確計算。

Bellman-Ford 演算法透過 `V-1` 輪迭代來確保這個過程的發生。在第 `i` 輪迭代後，演算法保證找到了所有**邊數不超過 `i`** 的最短路徑。由於任何不含負權重環的最短路徑最多有 `V-1` 條邊，因此經過 `V-1` 輪迭代後，所有頂點的 `dist` 值都已收斂到其最終的最短路徑值。

---

## 4. 複雜度分析

- **`V`**: 圖中的頂點數 (vertices)
- **`E`**: 圖中的邊數 (edges)

### 時間複雜度 (Time Complexity): `O(V * E)`

- 演算法的主體是一個雙層迴圈。
- 外層迴圈最多執行 `V-1` 次。
- 內層迴圈遍歷圖中所有的 `E` 條邊，對每一條邊進行一次鬆弛操作。
- 因此，總的時間複雜度為 `O((V-1) * E) = O(V * E)`。
- 提早終止的優化在平均情況下可能提升效能，但最壞情況下的複雜度依然是 `O(V * E)`。

### 空間複雜度 (Space Complexity): `O(V)`

- 我們需要一個 `dist` 陣列來儲存從源點到每個頂點的最短距離，其大小為 `V`。
- 因此，空間複雜度為 `O(V)`。
