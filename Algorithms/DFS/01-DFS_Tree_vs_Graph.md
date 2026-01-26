# DFS 策略：從 Tree 到 Graph 的演進與對比

## 核心思想：DFS 的遞迴本質

深度優先搜尋（DFS）無論應用於樹（Tree）或圖（Graph），其核心都是一個遞迴的探索過程。掌握其在不同資料結構下的實現差異，是精通圖論遍歷的基石。

- **樹 (Tree)**: 結構層次分明，無環路，具有唯一的根節點。DFS 主要用於節點遍歷、路徑查找與操作。
- **圖 (Graph)**: 結構複雜，可能包含環路，且可能由多個不連通的元件組成。DFS 必須依賴 `visited` 狀態追蹤來避免無限循環和重複探索。

---

## Graph DFS 的設計演進

為了深入理解，我們可以從一個基礎的 Tree DFS 模式開始，逐步演化為一個健壯且高效的 Graph DFS。

### 版本 1：拜訪檢查加標記遞迴模式

此版本直接套用樹的遍歷邏輯，在函式入口處檢查節點是否已訪問，如同在樹中檢查節點是否為 `nullptr`。

```cpp
// DFS 核心遞迴函式 - 版本 1 (基礎)
void dfs_v1(int u, const std::vector<std::vector<int>>& adj, std::vector<bool>& visited) {
    // 1. Pruning-on-Entry: 在函式入口處剪枝
    if (visited[u]) return;

    // 2. Mark-on-Process: 進入處理流程時標記
    visited[u] = true;
    // Process node u...

    // 3. 遍歷所有鄰居並直接遞迴
    for (int v : adj[u]) {
        dfs_v1(v, adj, visited);
    }
}
```

- **評析**: 此版本邏輯正確，但效率欠佳。即使鄰居 `v` 已被訪問，仍會產生一次不必要的 `dfs_v1(v)` 函式呼叫。

### 版本 2：拜訪即標記遞迴模式

此版本將 `visited` 檢查的責任從「被呼叫者」轉移到「呼叫者」，在遞迴呼叫前進行剪枝，避免了無效的函式呼叫。

```cpp
// DFS 核心遞迴函式 - 版本 2
void dfs_v2(int u, const std::vector<std::vector<int>>& adj, std::vector<bool>& visited) {
    // 1. Mark-on-Process: 進入處理流程時標記
    visited[u] = true;
    // Process node u... (such as label as gray)

    // 2. 遍歷所有鄰居
    for (int v : adj[u]) {
        // 3. Pruning-before-Push: 在發起遞迴呼叫前剪枝
        if (!visited[v]) {
            dfs_v2(v, adj, visited);
        }
    }

    // Process node u... (such as label as black)
}
```

- **評析**: 這是標準且高效的遞迴寫法，也是從 Tree DFS 思維到 Graph DFS 思維的關鍵轉變 (避免無效拜訪)。
- **應用**: 可延伸成 Node Coloring DFS (Cycle Detection, Topological Sort, etc.)

### 版本 3：經典且最高效遞迴模式

此版本將標記動作也提前至遞迴呼叫之前，在邏輯上與最高效的迭代版本完全對應，從根本上杜絕了任何重複排程的可能。

```cpp
// DFS 核心遞迴函式 - 版本 3 (經典且最高效)
void dfs_v3(int u, const std::vector<std::vector<int>>& adj, std::vector<bool>& visited) {
    // 處理節點 u
    // Process node u...

    // 遍歷所有鄰居
    for (int v : adj[u]) {
        // Pruning-before-Push + Mark-on-Push
        if (!visited[v]) {
            // 在遞迴呼叫前標記，確保節點只被排程一次
            visited[v] = true;
            dfs_v3(v, adj, visited);
        }
    }
}

// 主遍歷函式 - 需要為啟動點預先標記
void traverseGraph(const std::vector<std::vector<int>>& adj) {
    std::vector<bool> visited(adj.size(), false);
    for (int i = 0; i < adj.size(); ++i) {
        if (!visited[i]) {
            // 啟動點也需遵循 Mark-on-Push 策略
            visited[i] = true;
            dfs_v3(i, adj, visited);
        }
    }
}
```

- **評析**: 概念上最嚴謹的模式，是 `Mark-on-Push` + `Pruning-before-Push` 策略在遞迴中的直接體現。

---

## 關鍵決策：標記與剪枝的設計模式

為保證 `O(V+E)` 時間複雜度，DFS 依賴於**標記 (Marking)** 和 **剪枝 (Pruning)**。這兩者是獨立的設計選擇，其組合方式應根據演算法需求決定，而非綁定於遞迴或迭代實現。

### 1. 標記策略 (Marking Strategy)

**核心問題**：「節點是在**即將被處理時**標記，還是在**被排入待辦清單時**就標記？」

- **`Mark-on-Process` (處理時標記)**

  - **時機**: 當節點 `u` 的處理邏輯**正要開始**時才標記 `visited[u] = true`。
  - **語義**: `visited = true` 意為「此節點的處理已開始」。

- **`Mark-on-Push` (排程時標記)**
  - **時機**: 在將節點 `v` **排程**（遞迴呼叫或入隊）**之前**，就立即標記 `visited[v] = true`。
  - **語義**: `visited = true` 意為「此節點已在待辦清單中，未來將被處理」。

### 2. 剪枝策略 (Pruning Strategy)

**核心問題**：「在探索鄰居時，何時檢查 `visited` 狀態以避免重複工作？」

- **`Pruning-on-Entry` (入口處剪枝)**

  - **時機**: 在函式 `dfs(u)` 的**入口處**檢查 `if (visited[u]) return;`。
  - **特性**: 由**被呼叫者 (Callee)** 負責終止無效探索，但會產生額外函式呼叫。

- **`Pruning-before-Push` (排程前剪枝)**
  - **時機**: 在將節點 `v` **排程**（遞迴呼叫或入隊）**之前**，先檢查 `if (!visited[v])`。
  - **特性**: 由**呼叫者 (Caller)** 負責過濾，從源頭避免無效操作，是**最高效的剪枝方式**。

### 設計模式組合

1. **最高效模式 (通用首選)**

   - **組合**: `Mark-on-Push` + `Pruning-before-Push`
   - **流程**: 探索鄰居 `v` 時，檢查 `!visited[v]` (剪枝)，若通過則**立刻標記** `visited[v] = true` (標記)，然後才將 `v` 排程。
   - **評價**: **最高效的組合**，確保每個節點僅被排程一次，是**一般圖遍歷**的黃金標準。

2. **經典遞迴模式**

   - **組合**: `Mark-on-Process` + `Pruning-before-Push`
   - **流程**: 探索鄰居 `v` 時，檢查 `!visited[v]` (剪枝)，若通過則直接呼叫 `dfs(v)`。在 `dfs(v)` 入口處標記 `visited[v] = true` (標記)。
   - **評價**: 非常常見且高效，邏輯清晰地將「檢查」和「標記」分離在呼叫者和被呼叫者中。常用在 Node Coloring DFS 延伸演算法上。

3. **基礎模式 (效率較低)**
   - **組合**: `Mark-on-Process` + `Pruning-on-Entry`
   - **流程**: 直接對所有鄰居 `v` 呼叫 `dfs(v)`。在 `dfs(v)` 入口處檢查 `if (visited[v]) return;` (剪枝)，然後才標記。
   - **評價**: 邏輯正確但效率較低，因其對已訪問鄰居產生了多餘的函式呼叫。這種「信任被呼叫者自行剪枝」的模式，是實現簡潔 One-Liner DFS 的關鍵，犧牲少許性能換取極致簡潔性。

**結論**：標記與剪枝是可組合的工具。要實現最高效的 DFS，核心是採納 **`Pruning-before-Push`** 思想，並盡早標記（**`Mark-on-Push`**），從而杜絕任何不必要的操作。

---

## 實現策略：遞迴 vs. 迭代

### 遞迴 DFS (Recursive)

遞迴寫法簡潔，最能體現 DFS 的思想。前述的版本 1、2、3 均為遞迴實現。當採用 `Pruning-before-Push` 策略時（如版本 2 和 3），遞迴函式本身不再需要入口處的 `if (visited[u]) return;` 檢查。

### 迭代 DFS (Iterative)

當圖的深度極深時，為避免堆疊溢位 (Stack Overflow)，可手動管理一個 `std::stack`。迭代實現的黃金準則是採用**最高效模式**：`Mark-on-Push` + `Pruning-before-Push`。

```cpp
void dfs_iterative(const std::vector<std::vector<int>>& adj, int start_node) {
    std::vector<bool> visited(adj.size(), false);
    std::stack<int> s;

    // 遵循 Mark-on-Push，為起點預先標記
    visited[start_node] = true;
    s.push(start_node);

    while (!s.empty()) {
        int u = s.top();
        s.pop();

        // 處理節點 u ...

        for (int v : adj[u]) {
            // Pruning-before-Push + Mark-on-Push
            if (!visited[v]) {
                visited[v] = true;
                s.push(v);
            }
        }
    }
}
```
