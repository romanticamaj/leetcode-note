# BFS 在 Tree 與 Graph 中的結構比較與觀察

---

## 🧠 核心觀察

BFS（廣度優先搜尋）在樹與圖中雖然應用場景不同，但其 queue-based 結構與操作流程高度相似。以下是從 LeetCode 547 題的 BFS 實作中歸納出的幾個關鍵觀察：

---

## 🔍 BFS 結構對比

| 元素                    | Tree 中的 BFS（Level Order）    | Graph 中的 BFS                        |
| ----------------------- | ------------------------------- | ------------------------------------- |
| 起始點                  | 一定是 root                     | 需自行選擇起點（通常為每個未訪節點）  |
| queue 初始內容          | root                            | 任一未 visited 的節點                 |
| while 條件              | `!q.empty()`                    | `!q.empty()`                          |
| 拿出當前節點            | `q.front(); q.pop();`           | `q.front(); q.pop();`                 |
| 加入鄰接節點條件        | left/right 存在                 | `isConnected[node][i] && !visited[i]` |
| visited 處理            | 不一定需要（若為 perfect tree） | 必須使用 visited 陣列                 |
| 結構                    | 嚴格樹狀（無環）                | 可有環，需特別處理 visited            |
| 層級處理（level order） | 可用 size() 控制層級            | 若需算距離也可用 size() 控制層級      |

---

## 🧪 LeetCode 547 範例程式碼（Graph BFS）

```cpp
class Solution {
public:
    int findCircleNum(vector<vector<int>>& isConnected) {
        std::vector<bool> visited(isConnected.size(), false);
        int count = 0;

        // Iterate through all nodes to ensure all components are covered
        for (int i = 0; i < isConnected.size(); ++i) {
            if (!visited[i]) {
                bfs(isConnected, i, visited);
                count++;
            }
        }

        return count;
    }

    void bfs(const vector<vector<int>>& isConnected, const int node, vector<bool> &visited) {
        std::queue<int> q;

        // Initialize the queue with the starting element
        q.push(node);

        while (!q.empty()) {
            // Retrieve the next element from the queue for processing
            const int current = q.front();
            q.pop();

            // Perform the core operation on the current element
            visited[current] = true;

            // Explore all candidates related to the current element
            // If a candidate satisfies the connection condition and hasn't been processed, enqueue it
            for (int i = 0; i < isConnected.size(); ++i) {
                if (isConnected[current][i] && !visited[i]) {
                    q.push(i);
                }
            }
        }
    }
};
```

---

## 🧩 結構對應說明

| BFS 元素     | 程式碼對應行為                               |
| ------------ | -------------------------------------------- |
| 起始點選擇   | `for (int i = 0; i < n; ++i)` loop 中        |
| queue 初始化 | `q.push(node);`                              |
| while 條件   | `while (!q.empty())`                         |
| 拿出當前節點 | `vertex = q.front(); q.pop();`               |
| 加入鄰接節點 | `if (isConnected[vertex][i] && !visited[i])` |
| visited 處理 | `visited[vertex] = true;`                    |

---

## 🧠 結論

- BFS 的 queue 結構與流程在 tree 與 graph 中幾乎一致，差別在於：

  - **是否需要 visited 陣列**（graph 必須）
  - **鄰接節點的取得方式**（tree 為 left/right，graph 為鄰接矩陣或 list）
  - **起始點是否唯一**（tree 為 root，graph 需遍歷所有 component）

- 若你已熟悉 binary tree 的 BFS，轉換到 graph 的 BFS 只需多加注意 visited 與起點選擇邏輯，即可無痛遷移。

這種結構對應的理解，有助於你在面試與實作中快速建立 BFS 解法。

---

## 🧪 延伸補充：為何建議「加入 queue 時就標記 visited」

若你在「取出 queue 時」才標記 visited，可能會發生以下情況：

- 某節點 A 的鄰居 C 尚未被 visited，因此被加入 queue。
- 另一節點 B 也有鄰居 C，且 B 也在 queue 中。
- 此時 C 尚未被 pop，因此仍未被標記 visited，導致 B 也將 C 加入 queue。

這會導致 C 被重複加入 queue，造成空間浪費與重複處理。

### ✅ 正確做法：加入 queue 時就標記 visited（Mark-on-Push）

這樣可以保證每個節點最多只會被加入 queue 一次。

### 🔁 比較程式碼

**❌ 取出時標記（Mark-on-Pop）**

```cpp
while (!q.empty()) {
    const int cur = q.front();
    q.pop();

    // BFS basic: operate on current node
    // Here: Mark-on-Pop
    visited[cur] = true;

    for (int nei : graph[cur]) {
        if (!visited[nei]) {
            q.push(nei);
        }
    }
}
```

**✅ 加入時標記（Mark-on-Push）**

```cpp
// Mark-on-Push, for graph to optimize
visited[start] = true;
q.push(start);

while (!q.empty()) {
    const int cur = q.front();
    q.pop();

    for (int nei : graph[cur]) {
        if (!visited[nei]) {
            // Mark-on-Push, for graph to optimize
            visited[nei] = true;
            q.push(nei);
        }
    }
}
```
