# SPFA (Shortest Path Faster Algorithm)

SPFA (Shortest Path Faster Algorithm) 是 Bellman-Ford 演算法的一種優化。標準的 Bellman-Ford 演算法在其 `V-1` 輪的每一輪中都重複地鬆弛所有 `E` 條邊，而 SPFA 則採用了一種更有針對性的方法。它意識到，只有那些自身 `dist` 值剛被更新的節點，才有可能去鬆弛它們的鄰居。

---

## 1. 核心概念：佇列優化

SPFA 的核心思想是：**只有當一個節點 `u` 的最短路徑估計值 `dist[u]` 變小時，它才有可能去更新其鄰居節點 `v` 的距離 `dist[v]`**。

基於這個觀察，SPFA 使用一個佇列 (queue) 來維護那些「剛剛被成功鬆弛」的節點。演算法的流程如下：

1. **初始化**: 將源點 `s` 的距離設為 0，其他點設為無限大。將源點 `s` 加入佇列。
2. **迭代處理**: 當佇列不為空時，從佇列中取出一個頂點 `u`。
3. **鬆弛鄰居**: 對於 `u` 的每一個鄰居 `v`，進行鬆弛操作。
4. **入隊管理**: 如果 `v` 的距離 `dist[v]` 因為鬆弛而變小了，並且**`v` 當前不在佇列中**，則將 `v` 加入佇列。
5. **終止**: 當佇列為空時，演算法結束。

這個過程有點像 Dijkstra 或 BFS，但關鍵區別在於一個節點**可以多次入隊**。

### 為何需要佇列？

佇列中的節點代表了「有潛力去更新其他節點」的候選者。當 `dist[u]` 更新後，我們將 `u` 放入佇列，因為它現在可能提供一條通往其鄰居的更短路徑。這個過程會像漣漪一樣擴散開來，直到沒有節點可以再被更新為止。

---

## 2. C++ 實作說明

SPFA 的實作需要一個佇列和一個布林陣列 `in_queue` 來追蹤節點是否已在佇列中，以避免重複添加。

```cpp
#include <vector>
#include <queue>
#include <limits>

const int INF = std::numeric_limits<int>::max();

// 如果找到最短路徑則返回 true，如果檢測到負循環則返回 false。
bool spfa(int n, const std::vector<std::vector<int>>& edges, int src, std::vector<int>& dist) {
    dist.assign(n, INF);
    std::vector<bool> in_queue(n, false);
    std::vector<int> update_count(n, 0); // 用於檢測負循環
    std::queue<int> q;

    dist[src] = 0;
    q.push(src);
    in_queue[src] = true;
    update_count[src]++;

    while (!q.empty()) {
        int u = q.front(); q.pop();
        in_queue[u] = false;

        // 注意：此處直接遍歷邊列表，效率較低。建議先轉換為鄰接表。
        for (const auto& edge : edges) {
            if (edge[0] == u) {
                int v = edge[1];
                int weight = edge[2];

                if (dist[u] != INF && dist[u] + weight < dist[v]) {
                    dist[v] = dist[u] + weight;

                    if (!in_queue[v]) {
                        q.push(v);
                        in_queue[v] = true;
                        update_count[v]++;

                        // 負循環檢測
                        if (update_count[v] >= n) {
                            return false; // 一個節點被鬆弛了 n 次
                        }
                    }
                }
            }
        }
    }

    return true;
}
```

_註：遍歷邊列表的效率可以透過先將其轉換為鄰接串列來提高。_

### 負權重環檢測 (Negative Cycle Detection)

在 SPFA 中，如果一個節點入隊的次數達到了 `n` 次，就意味著存在一個從源點可達的負權重環。這是因為在一條不含環的最短路徑中，每個節點最多只會被鬆弛 `n-1` 次。

---

## 3. 正確性與複雜度分析

### 正確性

SPFA 的正確性與 Bellman-Ford 相同。只要圖中沒有負權重環，演算法最終會收斂，因為每個節點的 `dist` 值是單調遞減且有下界的。當佇列為空時，表示系統達到了穩定狀態，沒有任何邊可以再被鬆弛，此時 `dist` 陣列就儲存了最短路徑。

### 複雜度分析

- **`V`**: 圖中的頂點數 (vertices)
- **`E`**: 圖中的邊數 (edges)

#### 時間複雜度 (Time Complexity)

- **平均情況**: `O(E)` 或 `O(kE)`，其中 `k` 是一個小的常數。在隨機生成的稀疏圖中，SPFA 的表現通常非常好，接近線性時間，遠優於 Bellman-Ford。
- **最壞情況**: `O(V * E)`。在某些特殊構造的圖（例如，一個長鏈）上，SPFA 的行為會退化到與標準 Bellman-Ford 相同。節點會被反覆地推入和彈出佇列，導致每個節點平均入隊 `O(V)` 次，每次處理時遍歷其出邊。

因為其不穩定的最壞情況性能，SPFA 在競技程式設計中需謹慎使用，因為很容易被針對性的測試案例卡住。在沒有負權重邊的情況下，Dijkstra 演算法是更穩定且高效的選擇。

#### 空間複雜度 (Space Complexity): `O(V)`

- `dist` 陣列需要 `O(V)`。
- `in_queue` 陣列需要 `O(V)`。
- `update_count` 陣列需要 `O(V)`。
- 佇列 `q` 在最壞情況下可能儲存所有 `V` 個頂點，需要 `O(V)`。
- 總空間複雜度為 `O(V)`。
