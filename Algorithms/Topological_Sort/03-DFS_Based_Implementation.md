# 基於 DFS 的拓撲排序

深度優先搜尋 (DFS) 是實現拓撲排序的另一種經典方法。此方法的正確性，完全建立在 DFS 後序遍歷 (post-order traversal) 的性質之上。

## 1. 核心概念

此演算法的核心思想，源於對 DFS 遞迴結束時機的洞察：**當一個頂點 `u` 的深度優先搜尋遞迴結束時 (即到達 post-order 位置)，代表所有從 `u` 出發可達的後代頂點，都已經被完整地訪問過。**

因此，如果我們記錄下所有頂點完成其 DFS 探索的順序，並將這個順序反轉，就能確保對於圖中任何一條邊 `u -> v`，`u` 必定在 `v` 之前。這恰好滿足了拓撲排序的定義。

更簡潔地說：**一個頂點的所有依賴項（它所指向的頂點），總是在它自身之前完成 DFS 遞迴。因此，「完成順序」的倒序，就是「依賴順序」。** 這個概念與 Hierholzer's Algorithm 透過 post-ordering 尋找尤拉路徑的思路有共通之處。

## 2. CLRS 經典演算法

在經典教科書《Introduction to Algorithms》(CLRS) 中，DFS 拓撲排序的演算法被描述為一個簡潔的三步驟流程：

```
TOPOLOGICAL-SORT(G)
1 call DFS(G) to compute finishing times v.f for each vertex v
2 as each vertex is finished, insert it onto the front of a linked list
3 return the linked list of vertices
```

這段偽代碼完美地體現了核心概念：

- **第 1 步:** 呼叫 `DFS(G)`，其主要目的是遍歷所有節點並確定它們的「完成時間」(finishing times)。一個節點的完成時間，就是它在 DFS 遞迴中被標記為 `BLACK` (已完全訪問) 的時刻。
- **第 2 步:** 「as each vertex is finished」指的正是 DFS 中的後序位置。每當一個頂點完成探索（即將從遞迴中返回），就將它插入到一個鏈結串列的最前端。
- **第 3 步:** 返回這個鏈結串列。由於每個節點都是在其所有後代都完成後，才被插入到串列的前端，因此這個串列自然地形成了拓撲排序的結果，無需額外反轉。

## 3. 演算法流程與關鍵資料結構

### 演算法流程

1. **初始化 (Initialization):**

   - 建立一個空的列表 `sortedOrder`，用於儲存最終的排序結果。
   - 建立一個狀態陣列 `colors`，以追蹤每個頂點的訪問狀態，這對於環偵測至關重要。

2. **遍歷所有頂點 (Iterate All Vertices):**
   迭代圖中的每一個頂點。如果某個頂點尚未被訪問 (WHITE)，則從該頂點開始進行深度優先搜尋。這確保了即使圖是不連通的，所有頂點也能被處理。

3. **深度優先搜尋 (DFS):**
   對於頂點 `u` 的遞迴函式 `dfs(u)`：
   - a. 將 `u` 的狀態標記為「正在訪問中」(GRAY)。此標記的目的是為了偵測環路。
   - b. 遍歷 `u` 的所有鄰居頂點 `v`：
     - i. 如果 `v` 尚未被訪問 (WHITE)，則對 `v` 進行遞迴呼叫 `dfs(v)`。若遞迴呼叫返回 `false`，表示在更深層的路徑中發現了環，立即中斷並返回 `false`。
     - ii. 如果 `v` 的狀態為「正在訪問中」(GRAY)，表示我們遇到了一條**反向邊 (back edge)**，即從當前節點指向其遞迴堆疊上的某個祖先節點。這證明圖中有環，無法進行拓撲排序，應立即返回 `false`。
   - c. 當 `u` 的所有鄰居都已被成功訪問後 (所有遞迴呼叫均返回 `true`)，將 `u` 的狀態標記為「已完全訪問」(BLACK)。
   - d. **在後序位置 (Post-order Position)，將 `u` 加入 `sortedOrder` 列表。**
   - e. 返回 `true`，表示從 `u` 出發的路徑沒有發現環。

### 關鍵資料結構

1. **鄰接串列 (Adjacency List):** `std::vector<std::vector<int>> graph`
2. **狀態陣列 (State Array):** `std::vector<int> colors` (WHITE, GRAY, BLACK)
3. **結果列表 (Result List):** `std::vector<int> sortedOrder`

## 4. 實作 (Implementation)

### 實作一：Pruning-on-Push (CLRS 核心邏輯)

這個版本最直接地體現了 CLRS 的環偵測邏輯。它在遍歷鄰居節點時，才檢查其狀態，並只對 `WHITE` 狀態的鄰居發起新的遞迴呼叫。這種策略可視為 "Pruning-on-Push"。

這個版本更為簡潔，因為它只專注於環偵測的核心：**DFS 路徑上是否遇到了已在遞迴堆疊中的節點 (GRAY)？** 對於 `BLACK` 節點的判斷在此處是多餘的，因為一個已完成探索的 `BLACK` 節點不可能再次出現在當前的 DFS 路徑上（否則就意味著存在一個指向祖先的邊，那它在完成前就會被 `GRAY` 狀態捕獲）。

```cpp
class TopologicalSort {
private:
    const int WHITE = 0, GRAY = 1, BLACK = 2;
    std::vector<int> colors;
    std::vector<int> sortedOrder;

    bool dfs(const std::vector<std::vector<int>>& graph, int u) {
        colors[u] = GRAY;

        for (int v : graph[u]) {
            if (colors[v] == WHITE) {
                if (!dfs(graph, v)) return false;
            } else if (colors[v] == GRAY) {
                return false; // 發現反向邊，檢測到環
            }
        }

        colors[u] = BLACK;
        sortedOrder.push_back(u);
        return true;
    }
    // ... 主函式 findOrder 與下一個版本相同 ...
};
```

### 實作二：Pruning-on-Entry

這個版本在進入 `dfs` 函式時，就立即檢查當前頂點的顏色。此作法的好處是**判斷條件集中**，使得 `for` 迴圈內的遞迴呼叫非常簡單，可以 **無條件地對所有鄰居進行呼叫**，將狀態判斷的邏輯統一放在遞迴函式的入口處。

> `if (colors[u] == BLACK) return true;`

此版本多了一個對 `BLACK` 狀態的判斷。在一個稠密圖中，一個已被完全探索的節點（及其整個分支）可能會被多次作為其他節點的鄰居訪問到。這個檢查可以讓 `dfs` 呼叫立即返回，避免了不必要的鄰居迴圈，從而減少函式呼叫的開銷。

```cpp
#include <vector>
#include <algorithm>

class TopologicalSortWithOptimization {
private:
    const int WHITE = 0; // 未訪問
    const int GRAY = 1;  // 正在訪問 (已在遞迴堆疊中)
    const int BLACK = 2; // 已完全訪問

    std::vector<int> colors;
    std::vector<int> sortedOrder;

    bool dfs(const std::vector<std::vector<int>>& graph, int u) {
        // Pruning-on-Entry: 進入函式時立即檢查
        if (colors[u] == GRAY) return false; // 遇到環
        if (colors[u] == BLACK) return true; // 已訪問過的分支，無需重複探索

        colors[u] = GRAY; // 標記為正在訪問

        for (int v : graph[u]) {
            if (!dfs(graph, v)) {
                return false; // 在後續路徑中發現環，提前終止
            }
        }

        colors[u] = BLACK; // 標記為已完全訪問
        sortedOrder.push_back(u); // 在後序位置加入結果

        return true;
    }

public:
    std::vector<int> findOrder(int numVertices, const std::vector<std::vector<int>>& edges) {
        if (numVertices < 0) return {};

        // 1. 建立鄰接串列來表示圖
        std::vector<std::vector<int>> graph(numVertices);
        for (const auto& edge : edges) {
            graph[edge[1]].push_back(edge[0]);
        }

        colors.assign(numVertices, WHITE);
        sortedOrder.clear();
        sortedOrder.reserve(numVertices);

        // 2. 對所有尚未訪問的頂點執行 DFS
        for (int i = 0; i < numVertices; ++i) {
            if (colors[i] == WHITE) {
                if (!dfs(graph, i)) {
                    return {}; // 檢測到環，返回空向量
                }
            }
        }

        // 3. 將後序遍歷的結果反轉，得到拓撲排序
        std::reverse(sortedOrder.begin(), sortedOrder.end());
        return sortedOrder;
    }
};
```

## 5. 正確性證明 (Proof of Correctness)

DFS 拓撲排序的正確性，可透過證明以下引理來確立：

> **引理：** 在有向無環圖 (DAG) 中，對於任意邊 `(u, v)`，在 DFS 結束後，`u` 的完成時間 (finish time) 必定晚於 `v` 的完成時間。

- **完成時間 (Finish Time):** 一個頂點 `u` 被標記為 `BLACK` 的時間點。
- **證明 (反證法):**
  1. 假設存在一條邊 `(u, v)`，但 `u` 的完成時間卻早於 `v`。
  2. 當 DFS 訪問到 `u` 時，`v` 必定還未被訪問（`WHITE` 狀態）。因為如果 `v` 已被訪問 (無論 `GRAY` 或 `BLACK`)，`u` 就不可能比 `v` 更早完成。
  3. 因此，`dfs(u)` 會在其迴圈中呼叫 `dfs(v)`。這意味著 `v` 成為 `u` 在 DFS 樹中的後代。
  4. 根據遞迴的性質，`dfs(v)` 必須在 `dfs(u)` 之前完成。所以 `v` 的完成時間必定早於 `u` 的完成時間。
  5. 這與我們最初的假設「`u` 的完成時間早於 `v`」產生矛盾。
  6. 因此，假設不成立。對於任何邊 `(u, v)`，`u` 的完成時間必定晚於 `v`。

由於演算法將頂點按照完成時間的順序（`push_back` 的順序）儲存，並在最後反轉，這就確保了對於任何邊 `(u, v)`，`u` 都會出現在 `v` 之前，完全符合拓撲排序的定義。

## 6. 時間與空間複雜度分析

- **時間複雜度 (Time Complexity):** `O(V + E)`

  - 建立鄰接串列需要 `O(E)` 的時間。
  - DFS 演算法會訪問每個頂點和每條邊各一次，因此成本為 `O(V + E)`。
  - 最終反轉結果列表的成本為 `O(V)`。
  - 總和為 `O(V + E)`。

- **空間複雜度 (Space Complexity):** `O(V + E)`
  - 儲存鄰接串列 `graph` 需要 `O(V + E)` 的空間。
  - `colors` 狀態陣列需要 `O(V)` 的空間。
  - 遞迴呼叫堆疊 (recursion stack) 在最壞情況下（例如，一個鏈狀圖）其深度可達 `O(V)`。
  - 總和為 `O(V + E)`。
