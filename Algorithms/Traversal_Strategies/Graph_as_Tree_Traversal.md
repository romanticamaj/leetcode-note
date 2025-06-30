# 圖遍歷優化：當圖是樹時，省略 `visited` 集合

## 1. 核心觀察：圖的「樹」屬性

在圖論問題中，一個關鍵的隱藏條件是 **「一個有 N 個節點和 N-1 條邊的連通圖，必定是一棵樹」**。

這個特性意味著圖中**沒有迴圈 (cycle)**。因此，在進行深度優先搜索 (DFS) 或廣度優先搜索 (BFS) 時，我們不需要一個額外的 `visited` 集合來防止無限循環。我們只需要確保遍歷時不走回頭路即可。

這個優化技巧可以稱為 **「父節點排除法 (Parent Exclusion Trick)」**。

---

## 2. 實作模式：傳遞 `parent` 參數

核心實作方法是在遞迴函數或佇列中，多傳遞一個 `parent` 參數，用來記錄當前節點是從哪個節點訪問過來的。

### DFS 模式

在 DFS 中，遞迴函數簽名通常會從 `dfs(node, visited)` 變成 `dfs(node, parent)`。

```cpp
// graph: 圖的鄰接表
// node: 當前訪問的節點
// parent: 帶來我們到 `node` 的節點
int dfs(const vector<vector<int>>& graph, int node, int parent) {
    // 處理當前節點的邏輯...
    int count = 1; // 例如，計算節點數量

    for (int neighbor : graph[node]) {
        // 如果鄰居不是我們的父節點，就繼續深入
        if (neighbor != parent) {
            count += dfs(graph, neighbor, node);
        }
    }
    return count;
}

// 初始呼叫
// dfs(graph, 0, -1); // -1 作為一個虛擬的根節點父節點
```

### BFS 模式

在 BFS 中，佇列的元素從 `queue<int>` (只存節點) 變成 `queue<pair<int, int>>` (儲存 `node` 和其 `parent`)。

```cpp
int bfs(const vector<vector<int>>& graph, int startNode) {
    queue<pair<int, int>> q;
    q.push({startNode, -1}); // {節點, 父節點}

    int count = 0;
    while (!q.empty()) {
        auto [node, parent] = q.front();
        q.pop();
        count++;

        for (int neighbor : graph[node]) {
            if (neighbor != parent) {
                q.push({neighbor, node});
            }
        }
    }
    return count;
}
```

---

## 3. 應用範例：LeetCode 2368. Reachable Nodes With Restrictions

**題目分析**:
題目給定 `n` 個節點和 `n-1` 條邊，這是一個明確的信號，表示這個無向圖其實是一棵樹。因此，我們可以使用「父節點排除法」。

**程式碼**:

```cpp
class Solution {
public:
    int reachableNodes(int n, vector<vector<int>>& edges, vector<int>& restricted) {
        vector<vector<int>> graph(n);
        // 將 restricted 轉為 hash set 以達到 O(1) 的查詢效率
        unordered_set<int> invalidNodes(begin(restricted), end(restricted));

        // 建立鄰接表
        for (auto& edge: edges) {
            graph[edge[0]].push_back(edge[1]);
            graph[edge[1]].push_back(edge[0]);
        }

        // 從節點 0 開始，其父節點設為 -1
        return dfs(graph, 0, -1, invalidNodes);
    }

    int dfs(const vector<vector<int>>& graph, int node, int parent, const unordered_set<int>& invalidNodes) {
        // Base Case: 如果當前節點是被限制的，則此路不通，返回 0
        if (invalidNodes.count(node)) {
            return 0;
        }

        // 處理當前節點：計數為 1
        int count = 1;

        // 遞迴探索鄰居
        for (int neighbor : graph[node]) {
            // 只要鄰居不是父節點，就繼續深入
            if (neighbor != parent) {
                count += dfs(graph, neighbor, node, invalidNodes);
            }
        }
        return count;
    }
};
```

## 4. 總結

- **識別時機**: 當題目描述一個有 `N` 個節點和 `N-1` 條邊的**連通**圖時，可以斷定它是一棵樹。
- **優化**:
  - **空間**: 省略了 `visited` 集合所需的 `O(N)` 空間。
  - **時間**: 減少了對 `visited` 集合的插入和查詢操作，雖然時間複雜度級別不變，但常數時間會更小。
- **核心**: 將 `visited.count(node)` 的檢查，替換為 `neighbor != parent` 的檢查。

這個技巧雖然簡單，卻是識別問題本質並進行程式碼優化的重要體現。
