# Kahn 演算法 (基於 BFS 的拓撲排序)

Kahn 演算法是一種高效、非遞迴的拓撲排序方法，適用於有向無環圖 (Directed Acyclic Graph, DAG)。其運作原理是透過迭代處理圖中所有入度 (in-degree) 為零的頂點。

## 1. 核心概念

本演算法的基礎在於一個關鍵觀察：**任何有向無環圖中，必定至少存在一個入度為 0 的頂點**。這些頂點沒有任何前置依賴，因此可作為拓撲排序的起點。

演算法從所有入度為 0 的頂點出發，將它們放入一個佇列。接著，演算法進入一個迴圈，持續從佇列中提取頂點並將其加入最終的排序結果。每當一個頂點被處理，我們可以想像它及其所有對外的邊都從圖中被「移除」。這個動作會使其所有鄰居節點的入度減一。若某個鄰居節點的入度因此變為 0，代表其所有前置依賴均已滿足，便可將其加入佇列，等待後續處理。此過程不斷重複，直到佇列清空。

## 2. 演算法流程與關鍵資料結構

## 演算法流程

1. **建立圖並計算入度 (Graph Construction & In-degree Calculation):**
   遍歷輸入的邊列表，建立鄰接串列以表示圖的結構，並同時使用一個陣列來統計每個頂點的初始入度。

2. **初始化佇列 (Queue Initialization):**
   遍歷所有頂點，找出入度為 0 的頂點，並將它們全部加入一個佇列中。這些頂點是拓撲排序的起始集合。

3. **迭代處理 (Iterative Processing):**
   當佇列不為空時，重複執行以下步驟：
   a. 從佇列的前端取出一個頂點 `u`。
   b. 將 `u` 添加到最終的拓撲排序結果列表中。
   c. 遍歷 `u` 的所有鄰居頂點 `v`：
   i. 將 `v` 的入度減 1 (代表 `u` 這個依賴已被滿足)。
   ii. 如果 `v` 的入度變為 0，表示 `v` 的所有前置依賴都已處理完畢，因此將 `v` 加入佇列。

4. **結果驗證 (Result Validation):**
   迴圈結束後，檢查結果列表中的頂點數量是否等於圖的總頂點數。若相等，則排序成功；若不相等，則表示圖中存在環路 (cycle)，無法完成拓撲排序。

## 關鍵資料結構

1. **鄰接串列 (Adjacency List):**

   - **用途:** 儲存圖的結構，讓我們在處理完一個頂點後，能高效地存取其所有後繼鄰居。
   - **實作:** `std::vector<std::vector<int>> graph`

2. **入度陣列 (In-degree Array):**

   - **用途:** 記錄每個頂點的入度。這是判斷一個頂點是否滿足所有前置依賴、能否被加入佇列的關鍵依據。
   - **實作:** `std::vector<int> indegree`

3. **佇列 (Queue):**
   - **用途:** 存放所有入度為 0、等待被處理的頂點。佇列的先進先出 (FIFO) 特性確保了處理的層次順序。
   - **實作:** `std::queue<int> q`

## 3. C++ 實作參考

```cpp
#include <vector>
#include <queue>
#include <vector>

class TopologicalSort {
public:
    /**
     * @brief 使用 Kahn 演算法執行拓撲排序
     * @param numVertices 圖中的頂點總數
     * @param edges 一個二維向量，其中每個元素 {u, v} 代表一條從 u 到 v 的邊
     * @return 如果圖為有向無環圖，則返回拓撲排序結果；否則返回空向量。
     */
    std::vector<int> run(int numVertices, const std::vector<std::vector<int>>& edges) {
        // 1. 建立圖結構並計算每個節點的入度
        std::vector<std::vector<int>> graph(numVertices);
        std::vector<int> indegree(numVertices, 0);

        for (const auto& edge : edges) {
            int u = edge[1]; // 邊的起點 (前置依賴)
            int v = edge[0]; // 邊的終點
            graph[u].push_back(v);
            indegree[v]++;
        }

        // 2. 將所有入度為 0 的頂點加入佇列
        std::queue<int> q;
        for (int i = 0; i < numVertices; ++i) {
            if (indegree[i] == 0) {
                q.push(i);
            }
        }

        std::vector<int> sortedOrder;

        // 3. 迭代處理佇列中的頂點
        while (!q.empty()) {
            const int u = q.front(); q.pop();

            sortedOrder.push_back(u);

            // 更新其鄰居的入度
            for (int v : graph[u]) {
                indegree[v]--;

                if (indegree[v] == 0) { // 入度為 0，加入佇列
                    q.push(v);
                }
            }
        }

        // 4. 驗證結果：如果排序後的頂點數不等於總頂點數，表示圖中有環
        if (sortedOrder.size() != numVertices) {
            return {};
        }

        return sortedOrder;
    }
};
```

## 4. Loop Invariant 分析

Kahn 演算法中 `while` 迴圈的 **Loop Invariant (迴圈不變性)** 是確保演算法正確性的基石，其定義如下：

> **在每一次 `while` 迴圈迭代開始時，佇列 `q` 中儲存了「在當前剩餘圖中」所有入度為 0 的頂點。**

- **初始化 (Initialization):** 迴圈開始前，透過遍歷所有頂點，將初始入度為 0 的頂點全部放入佇列。此時，不變性成立。
- **維持 (Maintenance):** 在一次迭代中，演算法從佇列取出一個頂點 `u`。這個操作可視為將 `u` 從圖中移除。接著，演算法將 `u` 的所有鄰居 `v` 的入度減 1。只有當 `v` 的入度恰好變為 0 時，才將其加入佇列。這精準地確保了在下一次迭代開始時，佇列中新增的成員都滿足在「新的剩餘圖」中入度為 0 的條件，因此不變性得以保持。
- **終止 (Termination):** 當迴圈終止時，佇列為空。這意味著剩餘的圖中已不存在任何入度為 0 的頂點。如果此時所有頂點都已包含在 `sortedOrder` 中，則我們已成功找到一個拓撲排序。反之，如果圖中仍有頂點未被處理，這些頂點必然相互依賴，構成一個或多個環。

## 5. 時間與空間複雜度分析

- **時間複雜度 (Time Complexity):** `O(V + E)`

  - 建立鄰接串列與計算所有頂點的入度，需要遍歷所有邊，成本為 `O(E)`。
  - 初始化佇列，需要遍歷所有頂點，成本為 `O(V)`。
  - 主迴圈中，每個頂點最多只會入隊和出隊一次，總成本為 `O(V)`。在處理每個頂點時，我們會遍歷其所有對外的邊，因此所有邊最多只會被訪問一次，總成本為 `O(E)`。
  - 綜合起來，總時間複雜度為 `O(V + E)`。

- **空間複雜度 (Space Complexity):** `O(V + E)`
  - 儲存鄰接串列 `graph` 需要 `O(V + E)` 的空間。
  - `indegree` 陣列需要 `O(V)` 的空間。
  - 佇列 `q` 在最壞情況下（例如，一個星形圖的中心指向所有其他節點）可能需要儲存 `O(V)` 個頂點。
  - 綜合起來，總空間複雜度為 `O(V + E)`。
