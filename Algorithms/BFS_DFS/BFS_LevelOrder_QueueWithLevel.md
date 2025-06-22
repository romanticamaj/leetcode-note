# BFS Level Order 優化：Level in Queue

在許多使用 BFS 的題目中，會需要進行「層級遍歷」（Level Order Traversal）。經典做法通常會在每層開始前記錄 queue 的大小，並以 `for` loop 的方式逐一處理該層所有節點。

然而，這種做法可以進一步優化，使程式碼更簡潔、結構更清晰，方式是：**在 queue 中直接記錄每個節點的 level（層級）**。

---

## 🧱 傳統 BFS Level Order 範式

```cpp
queue<int> q;
vector<bool> visited(n, false);
int level = 0;

q.push(start);
visited[start] = true;

while (!q.empty()) {
    int levelSize = q.size();

    // 處理該 level（可選）
    process(q);

    for (int i = 0; i < levelSize; ++i) {
        int node = q.front(); q.pop();

        // 處理該層節點
        process(node, level);
        visited[node] = true;

        for (int neighbor : getNeighbors(node)) { // tree: left/right; graph: adjacency list
            if (!visited[neighbor]) {
                q.push(neighbor);
                visited[neighbor] = true;
            }
        }
    }

    ++level; // start from zero, update here, better style
}
```

- 優點：每層明確、清楚
- 缺點：多了一層 `for` loop，不夠彈性

---

## 🚀 優化：Queue 中附帶 level 資訊

```cpp
queue<pair<int, int>> q;
vector<bool> visited(n, false);

q.push({start, 0});
visited[start] = true;

while (!q.empty()) {
    auto [node, level] = q.front(); q.pop();

    // 直接處理節點與其層級
    process(node, level);

    for (int neighbor : getNeighbors(node)) { // tree: left/right; graph: adjacency list
        if (!visited[neighbor]) {
            q.push({neighbor, level + 1});
            visited[neighbor] = true;
        }
    }
}
```

- 優點：
  - 移除 `for` loop，BFS 更扁平、易於維護
  - 可快速判斷 node 是否位於目標層（如 `if (level == k)`)
  - 易於加入 early exit 或結果收集邏輯

---

## 🔁 備註：如何決定是否要優化？

- 當「**層級的概念會影響邏輯**」時 → 使用 queue+level 結構較直觀。
- 當需要早期結束、收集某層結果、或擴展為多層次狀態 BFS → 更應使用此優化方式。
