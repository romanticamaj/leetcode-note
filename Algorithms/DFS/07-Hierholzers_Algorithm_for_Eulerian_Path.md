# 心法: Hierholzer’s Algorithm for Eulerian Path

Hierholzer's Algorithm 是一種優雅且高效的演算法，專門用於在圖中尋找尤拉路徑 (Eulerian Path) 或尤拉迴路 (Eulerian Circuit)。其核心思想是透過深度優先搜尋 (DFS) 來遍歷所有邊，並巧妙地利用後序處理 (Post-order) 的特性來建構最終的路徑。

## 1. 問題定義

- **尤拉路徑 (Eulerian Path)**: 一條通過圖中**每一條邊**恰好一次的路徑。
- **尤拉迴路 (Eulerian Circuit)**: 一條起點和終點相同的尤拉路徑。

這類問題的經典應用是「一筆畫問題」，例如 LeetCode 上的 "Reconstruct Itinerary" (重構行程)，要求從一個機場出發，走完所有航線恰好一次。

## 2. 演算法核心概念

Hierholzer's Algorithm 的運作方式可以理解為一個不斷深入探索，直到「碰壁」再回溯記錄路徑的過程。

1. **從起點開始**: 選擇一個有效的起點進行 DFS。
2. **貪婪地消耗邊**: 沿著任意一條尚未走訪的出邊 (outgoing edge) 繼續深入。每走過一條邊，就將其「用掉」（例如從鄰接表中移除），以確保不會重複走。
3. **碰壁時記錄**: 當到達一個沒有任何未用出邊的節點時（即「碰壁」），意味著所有從該節點出發的路徑都已被探索完畢。此時，將這個節點加入到我們的路徑中。
4. **回溯與縫合**: 記錄完畢後，DFS 會自然地回溯到上一個節點，並嘗試走訪該節點的其他未用出邊，形成新的探索分支。
5. **反轉路徑**: 當所有邊都被走訪完畢後，將記錄下的路徑反轉，即為最終的尤拉路徑。

## 3. Post-ordering 的重要性

這個演算法最精妙之處在於第 3 步：**碰壁時才記錄節點**。這正是**後序處理 (Post-order Processing)** 的完美體現，確保了路徑的連續性。

```cpp
void dfs(GraphType& graph, const string& current, vector<string>& path) {
    // 1. 轉移狀態：走訪所有可達的子路徑
    while (!graph[current].empty()) {
        const auto node = graph[current].top(); graph[current].pop();
        dfs(graph, node, path);
    }
    // 2. 處理當前狀態：當所有子路徑都走完後，才將當前節點加入最終路徑
    path.push_back(current);
}
```

**為什麼必須是 Post-order？**

想像一下，如果我們在進入節點時就記錄路徑（Pre-order），會發生什麼問題。假設行程為 `A->C`, `C->A`, `A->B`，且從 A 開始，鄰居的選擇順序為 `B` 優先於 `C`。

- **Pre-order 的問題**:

  1. DFS 進入 A，記錄 `A`。路徑: `[A]`
  2. 優先選擇 `A->B`。DFS 進入 B，記錄 `B`。路徑: `[A, B]`
  3. B 沒有出邊，從 B 回溯到 A。
  4. 從 A 選擇剩下的 `A->C`。DFS 進入 C，記錄 `C`。路徑: `[A, B, C]`
  5. 從 C 走 `C->A`。DFS 進入 A，記錄 `A`。路徑: `[A, B, C, A]`
  6. 演算法結束，得到錯誤的路徑 `[A, B, C, A]`。問題在於 Pre-order 過早地「承諾」了路徑順序，導致無法正確地將 `A->C->A` 這個迴路插入到最終行程中。

- **Post-order 的正確性**:
  1. 從 A 出發，優先走 `A->B`。
  2. B 沒有出邊，碰壁。將 `B` 加入 path。`path: [B]`
  3. 回溯到 A，走下一個鄰居 `A->C`。
  4. 從 C 出發，走 `C->A`。
  5. A 沒有未走過的鄰居了，碰壁。將 `A` 加入 path。`path: [B, A]`
  6. 回溯到 C，C 的出邊已盡，將 `C` 加入 path。`path: [B, A, C]`
  7. 回溯到最初的 A，A 的出邊已盡，將 `A` 加入 path。`path: [B, A, C, A]`
  8. 反轉路徑得到 `[A, C, A, B]`，這才是正確的尤拉路徑。

Post-order 保證了**只有當一個節點的所有分支路徑都被完整探索並「縫合」到最終路徑後，這個節點本身才會被加入**。這確保了演算法不會因過早進入一個迴路而錯過其他路徑。

## 4. 演算法正確性與複雜度

- **正確性**: 在一個存在尤拉路徑的圖中，除了起點和終點，每個節點的入度和出度都相等。這保證了只要你進入一個中間節點，就一定有路可以離開。DFS 的貪婪走訪會找到一條路徑直到碰壁，然後 Post-order 的回溯機制會確保所有旁支的迴路都被正確地插入到主路徑中。
- **時間複雜度**: `O(E * logE)` 或 `O(E)`。
  - 若鄰接點需要按字典序訪問（如 LeetCode 332），使用最小堆 (`priority_queue`) 儲存，瓶頸在於建圖時的 `E` 次插入，總複雜度為 `O(E * logE)`。
  - 若無排序需求，使用 `vector` 儲存並從尾部 `pop_back`，則可以達到 `O(E)`。
- **空間複雜度**: `O(V + E)`，用於儲存圖的鄰接表和遞迴堆疊的深度。

## 5. 範例程式碼

```cpp
class Solution {
    // 使用優先佇列是為了滿足特定問題（如 LeetCode 332）的「字典序最小」要求。
    // 若無此要求，使用 std::vector 並從尾部 pop_back 會更高效。
    using NeighborType = priority_queue<string, vector<string>, std::greater<string>>;
    using GraphType = unordered_map<string, NeighborType>;

public:
    vector<string> findItinerary(vector<vector<string>>& tickets) {
        GraphType graph;
        for (auto& ticket: tickets) {
            graph[ticket[0]].push(ticket[1]);
        }

        vector<string> path;
        dfs(graph, "JFK", path);
        reverse(begin(path), end(path));
        return path;
    }

    void dfs(GraphType& graph, const string& current, vector<string>& path) {
        while (!graph[current].empty()) {
            const auto node = graph[current].top(); graph[current].pop();
            dfs(graph, node, path);
        }
        path.push_back(current);
    }
};
```
