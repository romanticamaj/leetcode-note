# Node-Based vs Edge-Based Implementation

## 核心觀察：兩者都輸出 Edge List

兩種實現模式本質上都是輸出 edge list，只是表現形式不同：

- **Node-Based**: 輸出節點序列 `[A, B, C, D]` → 隱含邊 `A→B, B→C, C→D`
- **Edge-Based**: 輸出邊標識 `["A→B", "B→C", "C→D"]` → 明確的邊序列

## Node-Based Implementation

### 特徵

- **Input**: 通常是 edge list，需建構鄰接表
- **收集內容**: 節點序列
- **收集時機**: 所有出邊處理完後
- **輸出意義**: 節點作為「邊的終點」

### 實現方式

```cpp
class NodeBasedHierholzer {
    vector<int> path;
    vector<vector<int>> adj;

public:
    vector<int> findEulerPath(vector<pair<int,int>>& edges) {
        // Input: edge list → 建構鄰接表
        buildAdjacencyList(edges);

        // DFS with node collection
        dfs(startNode);

        // 反轉得到正確路徑
        reverse(path.begin(), path.end());
        return path;
    }

private:
    void dfs(int node) {
        // 處理所有出邊
        while (!adj[node].empty()) {
            int next = adj[node].back();
            adj[node].pop_back();  // 移除邊 = 標記已訪問
            dfs(next);
        }

        // Post-order: 收集節點（作為某條邊的終點）
        path.push_back(node);
    }
};
```

### 為什麼在所有邊處理完後收集？

```cpp
// 節點 A 有出邊 A→B, A→C
dfs(A) {
    // 處理 A→B
    dfs(B);
    // 處理 A→C
    dfs(C);

    // 此時 A 的所有出邊都處理完
    // A 成為「最後進入它的邊」的終點
    collect(A);
}
```

節點代表了「所有入邊的匯集點」，必須等所有出邊處理完才能確定其在路徑中的位置。

### Visited 標記策略

| 策略            | 實現方式               | 優點                 |
| --------------- | ---------------------- | -------------------- |
| 動態修改鄰接表  | `adj[node].pop_back()` | 空間效率高，直接修改 |
| Out-degree 計數 | `outDegree[node]--`    | 保留原圖結構         |
| 鄰接矩陣遞減    | `matrix[u][v]--`       | 支援重邊             |

## Edge-Based Implementation

### 特徵

- **Input**: 可以是 edge list 或需要邊資訊的結構
- **收集內容**: 邊的標識或資訊
- **收集時機**: 每條邊處理完立即收集
- **輸出意義**: 明確的邊序列

### 實現方式

```cpp
class EdgeBasedHierholzer {
    unordered_set<string> visitedEdges;
    vector<string> edgePath;
    unordered_map<string, vector<pair<string, string>>> adj;

public:
    vector<string> findEulerPath(vector<pair<string, string>>& edges) {
        // Input: edge list → 建構帶邊資訊的鄰接表
        for (auto& [from, to] : edges) {
            string edgeId = from + "->" + to;
            adj[from].push_back({to, edgeId});
        }

        dfs(startNode);
        reverse(edgePath.begin(), edgePath.end());
        return edgePath;
    }

private:
    void dfs(const string& node) {
        while (!adj[node].empty()) {
            auto [next, edgeId] = adj[node].back();
            adj[node].pop_back();

            // 邊可能需要額外檢查（如處理重邊）
            if (!visitedEdges.count(edgeId)) {
                visitedEdges.insert(edgeId);

                // 遞迴處理下一個節點
                dfs(next);

                // Post-order: 立即收集這條邊
                edgePath.push_back(edgeId);
            }
        }
    }
};
```

### 為什麼每條邊處理完就收集？

```cpp
// 處理邊 A→B
processEdge(A→B) {
    markVisited(A→B);
    dfs(B);  // 探索 B 的所有後續路徑

    // 此時邊 A→B 及其後續路徑都處理完
    // 邊是獨立的資訊單元，可以立即收集
    collect(A→B);
}
```

每條邊是獨立的資訊單元，一旦該邊及其後續路徑都探索完就可以收集。

### Visited 標記策略

| 策略         | 實現方式                      | 適用場景       |
| ------------ | ----------------------------- | -------------- |
| HashSet 記錄 | `visitedEdges.insert(edgeId)` | 邊有唯一 ID    |
| Map 計數     | `edgeCount[edgeId]--`         | 處理重邊       |
| 邊屬性標記   | `edge.visited = true`         | 邊物件包含狀態 |

## 關鍵差異分析

### 收集時機的本質差異

| 層面         | Node-Based           | Edge-Based     |
| ------------ | -------------------- | -------------- |
| **資訊載體** | 節點（隱含所有入邊） | 邊（獨立單元） |
| **收集時機** | 所有出邊處理完       | 單條邊處理完   |
| **收集內容** | 節點作為終點         | 邊的完整資訊   |
| **輸出形式** | 節點序列             | 邊序列         |

### 統一理解框架

```cpp
void hierholzer(current) {
    for (edge : unvisited_edges_from(current)) {
        mark_visited(edge);
        hierholzer(edge.target);

        // Edge-Based: 在這裡收集邊
        // collect(edge);
    }

    // Node-Based: 在這裡收集節點(作為某條邊的終點)
    // collect(current);
}
```

## 選擇指南

### 使用 Node-Based 的場景

- 一般圖遍歷問題
- 只需要節點順序
- 輸入已是鄰接表形式
- 空間效率要求高

### 使用 Edge-Based 的場景

- 邊有特殊意義（如 De Bruijn Graph）
- 需要邊的詳細資訊
- 需要處理複雜的重邊情況
- 輸出需要明確的邊序列

## 實現要點總結

### 共同要點

- 都使用 Post-order Collection
- 都需要最後反轉結果
- 都要確保每條邊只訪問一次

### Node-Based 要點

- 建構鄰接表（從 edge list）
- 動態修改結構標記訪問
- 收集節點序列

### Edge-Based 要點

- 維護邊的唯一標識
- 可能需要額外的訪問檢查
- 收集邊的資訊

## ✅ 實現檢查清單

- [ ] 識別問題需要節點序列還是邊序列
- [ ] 選擇合適的實現模式
- [ ] 正確處理 Input（edge list vs adjacency list）
- [ ] 實現適當的 visited 標記機制
- [ ] Post-order 收集（但時機不同）
- [ ] 記得反轉最終結果
