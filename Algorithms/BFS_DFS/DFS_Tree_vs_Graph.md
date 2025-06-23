# DFS 在 Tree 與 Graph 中的結構比較與觀察

## 核心心法：DFS 的通用模式

DFS（深度優先搜尋）無論應用於樹還是圖，其核心都是一個遞迴過程。理解其在不同結構下的微小差異，是掌握圖論遍歷的關鍵。

- **樹 (Tree)**: 結構簡單，無環，有固定根節點。DFS 通常用於遍歷、節點操作、路徑查找等。
- **圖 (Graph)**: 結構複雜，可能有環，可能不連通。DFS 必須依賴 `visited` 集合來避免無限循環和重複訪問。

---

## 從 Tree DFS 到 Graph DFS 的演進

為了更好地理解，我們可以從一個類似 Tree DFS 的結構開始，逐步演化到最終的 Graph DFS。

### 版本 1：直接套用 Tree 的邏輯

這個版本非常直觀，它在函式入口處檢查 `visited`，就像在 Tree 中檢查 `node == nullptr` 一樣。

```cpp
// DFS 核心遞迴函式 - 版本 1 (類似 Tree)
void dfs(int u, const std::vector<std::vector<int>>& adj, std::vector<bool>& visited) {
    // 1. Base Case: 如果已訪問，直接返回
    if (visited[u]) return;

    // 2. Mark-on-Entry: 進入節點時立刻標記
    visited[u] = true;
    // Process node u...

    // 3. 遍歷所有鄰居並直接遞迴
    for (int v : adj[u]) {
        dfs(v, adj, visited);
    }
}

// 主遍歷函式 (保持不變)
void traverseGraph(const std::vector<std::vector<int>>& adj) {
    std::vector<bool> visited(adj.size(), false);
    for (int i = 0; i < adj.size(); ++i) {
        if (!visited[i]) {
            dfs(i, adj, visited);
        }
    }
}
```

這個版本是**正確的**，但不是最高效的。因為即使 `v` 已經被訪問過，我們仍然會為它產生一次不必要的函式呼叫，只是為了觸發第一行的 `if (visited[v]) return;`。

### 版本 2：優化 - 在呼叫前檢查 (最終版本)

這就是我們在前面看到的標準版本。它透過在遞迴呼叫**前**檢查 `!visited[v]`，避免了對已訪問節點的無效函式呼叫。

```cpp
// DFS 核心遞迴函式 - 版本 2 (優化後)
void dfs(int u, const std::vector<std::vector<int>>& adj, std::vector<bool>& visited) {
    // 1. Mark-on-Entry
    visited[u] = true;
    // Process node u...

    // 2. 遍歷所有鄰居
    for (int v : adj[u]) {
        // 3. 在呼叫前檢查，避免不必要的遞迴
        if (!visited[v]) {
            dfs(v, adj, visited);
        }
    }
}
```

這個小小的改動，將 `visited` 檢查從「被呼叫者」的責任轉移到了「呼叫者」的責任，是從 Tree DFS 思維到 Graph DFS 思維的一個關鍵轉變。

---

## 結構對比：Tree vs. Graph

| DFS 元素     | Tree 中的實現                          | Graph 中的實現                    | 關鍵差異                                |
| :----------- | :------------------------------------- | :-------------------------------- | :-------------------------------------- |
| **起點**     | 固定為 `root`                          | `for` 迴圈遍歷所有節點            | 圖可能不連通，需多個起點                |
| **終止條件** | `if (node == nullptr)`                 | 無 (由 `visited` 檢查隱含)        | 圖的終止依賴於 `visited` 狀態           |
| **遞迴條件** | `if (node->left)` / `if (node->right)` | `if (!visited[v])` (在呼叫前檢查) | 圖必須檢查 `visited` 狀態以防止無限循環 |
| **標記訪問** | 通常不需要                             | `visited[u] = true`               | 圖必須有 `visited` 集合來追蹤狀態       |
| **鄰居探索** | `dfs(node->left)`, `dfs(node->right)`  | `for (int v : adj[u])`            | 樹的鄰居固定 (left/right)，圖不固定     |

---

## 核心實踐：遞迴 vs. 迭代

### 遞迴 DFS (Recursive) - 首選方法

遞迴寫法簡潔，最能體現 DFS 的思想。上面的通用範例就是遞迴實現。

**重點**：因為在遞迴呼叫前已經檢查過 `!visited[v]`，所以遞迴函式 `dfs` 的第一行**不需要** `if (visited[u]) return;` 這種 base case。

### 迭代 DFS (Iterative) - 避免堆疊溢位

當圖的深度極深時，遞迴可能導致堆疊溢位。此時需要手動使用 `std::stack`。

#### 關鍵模式：Mark-on-Push

```cpp
void dfs_iterative(const std::vector<std::vector<int>>& adj, int start_node) {
    std::vector<bool> visited(adj.size(), false);
    std::stack<int> s;

    // 1. 標記起點並推入堆疊
    visited[start_node] = true;
    s.push(start_node);

    while (!s.empty()) {
        int u = s.top();
        s.pop();

        // 處理節點 u ...

        for (int v : adj[u]) {
            if (!visited[v]) {
                // 2. 在推入前標記 (Mark-on-Push)
                visited[v] = true;
                s.push(v);
            }
        }
    }
}
```

### 兩種模式的等價性

**遞迴的「Mark-on-Entry」與迭代的「Mark-on-Push」是完全等價的**。它們都遵循了「**在節點被排定要訪問時就立即標記**」的黃金準則，以防止同一個節點被重複排程，從而保證了 O(V+E) 的時間複雜度。
