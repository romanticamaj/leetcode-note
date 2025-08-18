# 心法：將 Dijkstra 視為一個通用的貪婪搜尋框架

Dijkstra 演算法的精髓遠不止於計算 `A` 點到 `B` 點的最短距離。若將其核心思想抽象化，它可以被視為一個強大的、可客製化的**通用貪婪搜尋框架**。理解這一點，是將 Dijkstra 應用於更廣泛最佳化問題的關鍵。

這個框架的威力在於，我們可以**重新定義**演算法的兩個核心要素：

1. **成本 (Cost)**：傳統意義上的 `distance`，即路徑權重之和。
2. **鬆弛 (Relaxation)**：如何根據舊路徑的成本和新邊的權重，來計算新路徑成本的規則。

---

## 1. 抽象化 Dijkstra 的核心組件

一個通用的 Dijkstra 框架包含以下組件：

| 組件          | 標準 Dijkstra                 | 泛化概念                                     |
| :------------ | :---------------------------- | :------------------------------------------- |
| **目標**      | 最小化**路徑權重總和**        | 最小化（或最大化）某個**目標成本函數**       |
| **狀態/成本** | `distance` (一個整數或浮點數) | `cost` (任何可比較的值)                      |
| **鬆弛操作**  | `dist[u] + weight`            | `aggregate(cost[u], weight)`                 |
| **優先佇列**  | `min-priority-queue`          | `min-priority-queue` 或 `max-priority-queue` |

**`aggregate(cost, weight)`** 是一個聚合函數，它定義了如何結合當前路徑的成本 `cost` 和新遇到的邊 `weight` 來產生一條新路徑的成本。

---

## 2. 重新定義「成本」與「鬆弛」

Dijkstra 演算法之所以能保證找到最佳解，是基於其**貪婪選擇性質**，而這個性質成立的前提是路徑成本的計算滿足**最佳子結構**與**無負權環**的特性。只要我們定義的「成本」和「鬆弛」不破壞這個基礎，就可以安全地套用此框架。

### 範例 1：標準最短路徑 (Standard Shortest Path)

這是我們最熟悉的形式。

- **成本 `cost`**: 從起點到當前節點的路徑權重**總和**。
- **聚合函數 `aggregate`**: `new_cost = old_cost + edge_weight` (加法)。
- **目標**: 最小化 `cost`。

### 範例 2：瓶頸最短路徑 (Bottleneck Shortest Path / Minimax Path)

目標是找到一條路徑，使其上的**最大邊權**在所有可能路徑中最小。

- **成本 `cost`**: 從起點到當前節點的路徑上，所經過的**最大邊權**。
- **聚合函數 `aggregate`**: `new_cost = max(old_cost, edge_weight)` (取最大值)。
- **目標**: 最小化 `cost`。

### 範例 3：最高機率路徑 (Most Probable Path)

假設邊權代表節點間的通行**成功機率** (0 到 1 之間)。目標是找到一條從起點到終點**總成功機率最高**的路徑。

- **成本 `cost`**: 從起點到當前節點的**總成功機率**。
- **聚合函數 `aggregate`**: `new_cost = old_cost * edge_probability` (乘法)。
- **目標**: **最大化** `cost`。
- **實現細節**: 由於我們要找最大值，應使用**最大優先佇列 (max-priority-queue)**。

---

## 3. 泛用程式碼框架

這個 C++ 框架展示了如何將「成本」和「鬆弛」邏輯模組化。

```cpp
#include <vector>
#include <queue>
#include <functional> // For std::function

// 定義成本類型，可以是 int, double, or even a custom struct
using CostType = double;

// 定義聚合函數的簽名
using AggregationFunc = std::function<CostType(CostType, double)>;

// adj: 鄰接串列, adj[u] = { {v1, w1}, {v2, w2}, ... }
// num_nodes: 節點總數
// start_node: 起點
// initial_cost: 起點的初始成本
// worst_cost: 代表無限大或極差成本的值
// aggregate: 用於計算新成本的函數
// compare: 用於優先佇列的比較器 (std::less for max-heap, std::greater for min-heap)
template<typename Compare>
vector<CostType> generalizedDijkstra(
    const vector<vector<pair<int, double>>>& adj,
    int num_nodes,
    int start_node,
    CostType initial_cost,
    CostType worst_cost,
    AggregationFunc aggregate,
    Compare compare
) {
    vector<CostType> costs(num_nodes, worst_cost);
    priority_queue<pair<CostType, int>, vector<pair<CostType, int>>, Compare> pq(compare);

    costs[start_node] = initial_cost;
    pq.push({initial_cost, start_node});

    while (!pq.empty()) {
        auto [current_cost, u] = pq.top(); pq.pop();

        // 根據目標是最大化還是最小化，剪枝條件可能需要調整
        // 對於最小化問題，使用 >
        // 對於最大化問題，使用 <
        if (compare(costs[u], current_cost)) {
             continue;
        }

        for (const auto& edge : adj[u]) {
            int v = edge.first;
            double weight = edge.second;

            // 使用傳入的聚合函數計算新成本
            CostType new_cost = aggregate(current_cost, weight);

            // 根據目標，比較新舊成本
            if (compare(new_cost, costs[v])) {
                costs[v] = new_cost;
                pq.push({new_cost, v});
            }
        }
    }
    return costs;
}

// --- 如何使用 ---
// 1. 標準 Dijkstra
// auto costs = generalizedDijkstra(adj, n, start, 0.0, INF,
//     [](double a, double b) { return a + b; },
//     std::greater<pair<CostType, int>>());

// 2. Minimax Path
// auto costs = generalizedDijkstra(adj, n, start, 0.0, INF,
//     [](double a, double b) { return std::max(a, b); },
//     std::greater<pair<CostType, int>>());

// 3. Most Probable Path
// auto costs = generalizedDijkstra(adj, n, start, 1.0, 0.0,
//     [](double a, double b) { return a * b; },
//     std::less<pair<CostType, int>>());
```

---

## 4. 結論：Dijkstra 的思想核心

將 Dijkstra 視為一個通用框架，能幫助我們跳出「求最短路徑和」的思維定勢。當遇到圖論最佳化問題時，可以先問自己：

1. **目標是什麼？** 我要最小化還是最大化哪個值？
2. **成本是什麼？** 這個值是如何定義的？它只跟路徑有關嗎？
3. **成本如何傳遞？** 當我從節點 `u` 走到 `v` 時，新的成本 `cost[v]` 如何由 `cost[u]` 和邊權 `w(u,v)` 計算出來？

只要問題的結構符合貪婪選擇的原則，我們就可以透過客製化「成本」與「鬆弛」這兩個核心，來設計出高效且優雅的解決方案。
