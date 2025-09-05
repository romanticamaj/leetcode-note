# Prim's Algorithm for Minimum Spanning Tree

---

## 1. 核心設計概念

Prim 演算法採用**以點為中心 (Vertex-centric)** 的貪婪策略來建構最小生成樹 (MST)。其核心思想是將圖中的節點分為兩組：

1. **Decided Set**: 已經包含在 MST 中的節點集合。
2. **Undecided Set**: 尚未被包含的節點集合。

> **演算法從一個起始點開始，將其納入 "Decided Set"。接著，將該節點所有向外連接的邊都加入一個全域的最小優先佇列 (Min-Heap)。此後，不斷從 Min-Heap 中提取權重最小的邊，如果該邊連接到一個 "Undecided Set" 中的節點，就將該節點納入 "Decided Set"，並將其所有新的對外連接邊也加入 Min-Heap。重複此過程，直到所有節點都屬於 "Decided Set"。**
>
> 在這個過程中，Min-Heap 中存放的所有邊，就代表了從 "Decided Set" 連接到 "Undecided Set" 的所有候選邊界 (Candidate Edges)。演算法的每一步都是在這些候選邊界中，選擇最輕的一條來擴張我們的 MST。

這個過程就像是在一個點上點火，然後火勢總是沿著最短的路徑蔓延到最近的未燃燒點。演算法的每一步都直接應用了 **Cut Property**。

---

## 2. Data Structure

1. **優先佇列 (Min-Heap)**:

   - **用途**: 作為 "Decided Set" 所有對外連接邊的容器。它能讓我們高效地找到連接 "Decided Set" 與 "Undecided Set" 的最輕邊。
   - **結構**: 佇列中的元素通常是一個 `pair<int, int>`，代表 `(weight, destination_vertex)`。

2. **訪問標記 (Visited Vector)**:
   - **用途**: 用於區分節點屬於 "Decided Set" 還是 "Undecided Set"。`visited[i] = true` 代表節點 `i` 已經在 MST 中。
   - **結構**: 一個大小為 `n` 的布林陣列。

---

## 3. 通用 C++ 實作

這個範例展示了一個通用的 Prim 演算法實作，它接受一個以鄰接串列表示的圖，並回傳最小生成樹的總成本。

```cpp
class PrimMST {
    using Edge = pair<int, int>; // {weight, destination_vertex}
    using PriorityQueue = priority_queue<Edge, vector<Edge>, greater<Edge>>;

public:
    int minCost(int n, const vector<vector<int>>& edges) {
        // 1. 根據邊列表建構鄰接串列圖
        vector<vector<Edge>> graph(n);
        for (const auto& edge : edges) {
            int u = edge[0], v = edge[1], weight = edge[2];
            graph[u].push_back({weight, v});
            graph[v].push_back({weight, u});
        }

        // 2. 建構 visited 陣列 (Decided Set) 和 min-heap
        vector<bool> visited(n, false);
        PriorityQueue q;

        // 3. 選擇節點 0 作為起點
        visited[0] = true;
        for (const auto& edge : graph[0]) {
            // edge: {weight, neighbor_node}
            q.push(edge);
        }

        int edgesUsed = 0;
        int minCost = 0;

        // 4. 貪婪策略：持續選取最輕的邊，直到連接 n-1 條邊
        while (!q.empty() && edgesUsed < n - 1) {
            // 從 heap 中取得連接 Decided Set 與 Undecided Set 的最輕邊
            auto [weight, u] = q.top(); q.pop();

            // 如果節點 u 已經在 Decided Set 中，跳過 (這是舊的、較長的邊)
            if (visited[u]) continue;

            // 選擇此邊與節點 u
            minCost += weight;
            edgesUsed++;
            visited[u] = true;

            // 5. 將新節點 u 的所有對外邊加入 min-heap
            for (const auto& edge : graph[u]) {
                if (!visited[edge.second]) q.push(edge);
            }
        }

        // 如果最終使用的邊少於 n-1，表示圖不連通
        return edgesUsed == n - 1 ? minCost : -1;
    }
};
```

---

## 4. 複雜度分析

假設圖中有 `V` 個頂點和 `E` 條邊。

### 時間複雜度

- **總體**: `O(E log E)` 或 `O(E log V)`

  - 最差情況 Pop E 條邊，每次 O(log E)

- **精確分析**:
  - **`push` 操作**: `pushEdges` 函數總共會被呼叫 `V` 次。在整個演算法的生命週期中，每一條邊最多會被從其兩個端點推入優先佇列一次。因此，`push` 操作的總數是 `O(E)`。
  - **`pop` 操作**: `while` 迴圈的目標是選出 `V-1` 條有效的邊來連接所有 `V` 個節點。然而，由於我們採用了「懶惰更新」策略（見下文），佇列中可能包含指向已訪問節點的「過期」邊。在最壞的情況下，我們可能需要 `pop` 掉接近 `O(E)` 條邊，才能找到那 `V-1` 條我們需要的有效邊。
  - **瓶頸**: 優先佇列的大小最多為 `O(E)`，因此每次 `push` 或 `pop` 操作的時間成本是 `O(log E)`。演算法的總時間由對優先佇列的操作主導。總操作次數是 `O(E)`（`push` 和 `pop`），因此總時間複雜度是 **`O(E log E)`**。
  - **關於 `O(E log V)`**: 因為在一個圖中，邊的數量 `E` 最多是 `O(V^2)`，所以 `log E` 的級別最高是 `log(V^2) = 2 * log V`。因此，`O(E log E)` 和 `O(E log V)` 在漸進意義上是等價的，後者更常用於與其他圖演算法進行比較。

### 空間複雜度

- **優先佇列**: 最壞情況下需要儲存 `O(E)` 條邊。
- **訪問標記**: `O(V)`。
- **總體**: `O(V + E)`。

### 實作細節：`DECREASE-KEY` vs. `push` + Lazy Deletion

> **CLRS 理論 vs. LeetCode 實作**
>
> 傳統的 Prim 演算法教科書版本，會使用一個支援 `DECREASE-KEY` 操作的優先佇列。當發現一條通往某個 `Undecided` 節點的更短路徑時，會去「更新」佇列中已有的那條邊的權重。這需要特殊的堆結構（如斐波那契堆）來達到最優理論複雜度 `O(E + V log V)`。
>
> 然而，在 C++ 的 `std::priority_queue` 或大多數標準庫的堆實現中，並沒有提供高效的 `DECREASE-KEY`。因此，本範例採用了更常見且方便的實作方式：**不更新，而是直接推入新的、權重更低的邊**。
>
> 這種方法的結果是正確的，因為權重較低的邊會被優先處理。權重較高的舊邊雖然還留在佇列中，但當輪到它們被 `pop` 出來時，其目標節點早已被 `visited`，所以會被 `if (visited[j]) continue;` 這行程式碼自然地忽略。這種「懶惰更新」的策略，使得優先佇列中最多可能有 `O(E)` 個元素，也是時間複雜度中 `log E` 項的來源。
