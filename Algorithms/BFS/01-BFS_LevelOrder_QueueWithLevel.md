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

---

## 💡 核心觀念延伸：Level 的兩種語義

在 BFS 的脈絡下，「level」這個詞可以有兩種不同的詮釋，這對於理解演算法的變體至關重要：

1. **Level as Distance (0-based): 距離**
   - **意涵**: `level` 代表的是從源點 `start` 到當前節點 `node` 的**最短路徑長度**（在無權重圖中，即最少邊數）。
   - **計數方式**: 源點的 `level` 為 0，其鄰居為 1，依此類推。這就是典型的 0-based indexing。
   - **關聯演算法**: 這種觀點下的 BFS 與 **Dijkstra 演算法** 有著深刻的聯繫。如果我們將 BFS 的 queue 換成一個 `min-priority-queue`，並將 `level` 視為 `distance`，再引入**鬆弛 (Relaxation)** 的概念來更新距離，那麼演算法就自然地演變為 Dijkstra，能夠處理帶有非負權重的圖。

2. **Level as Processing Layer (1-based): 處理層**
   - **意涵**: `level` 代表的是 BFS 處理節點的**第幾輪**或**第幾層**。
   - **計數方式**: 這種觀點通常透過一個在 `while` 迴圈外的獨立計數器來實現。計數器的**初始值**決定了計數是 0-based 還是 1-based。例如，若 `level` 初始化為 1，則源點是第 1 層，其鄰居是第 2 層。
   - **應用場景**: 當我們關心的是「處理到第幾批節點」時，這種觀點更為直觀。傳統的 `for` 迴圈層序遍歷範式，就是透過 `levelSize` 鎖定當前批次，並在處理完畢後遞增外部的 `level` 計數器來實現此概念。
