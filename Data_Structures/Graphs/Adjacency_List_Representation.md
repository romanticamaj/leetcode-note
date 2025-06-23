# 圖的表示法 (2): 鄰接列表

**鄰接列表 (Adjacency List)** 是表示圖**最常用、最高效**的方法，也是解決大多數圖論問題的**面試首選**。

它的核心思想是為圖中的每一個節點 `u` 維護一個列表或集合，其中包含所有與 `u` 相鄰的節點 `v`。這可以看作是一個從節點到其鄰居列表的映射。

在 LeetCode 等平台上，題目通常會以**邊列表 (`std::vector<std::vector<int>>`)** 的形式給定圖的邊，我們的第一步幾乎總是將這個輸入轉換為高效的鄰接列表，以便後續處理。

## tl;dr: 面試常用結構

- **`std::unordered_map<int, std::unordered_set<int>>`**: **最常用**。儲存節點到其**唯一**鄰居的映射。不允許重複邊。
- **`std::unordered_map<int, std::vector<int>>`**: 儲存節點到其鄰居的映射。**允許重複邊** (平行邊)。
- **`std::unordered_map<int, std::unordered_map<int, int>>`**: **最強大**。儲存節點到鄰居的映射，並為每條邊附加額外資訊（如權重、方向標記等）。
- **`std::vector<std::vector<int>>`**: **最高效 (無權重)**。節點為 `0..n-1` 時使用。
- **`std::vector<std::vector<std::pair<int, int>>>`**: **最高效 (有權重)**。節點為 `0..n-1` 時使用。

---

## C++ 高效實現：`unordered_map`

## 方法 1: `unordered_map` (靈活性高)

這是最通用的方法，適用於任何整數節點 ID。

- **`unordered_map<int, vector<int>>`**: 允許重複邊。
- **`unordered_map<int, unordered_set<int>>`**: 自動處理重複邊。
- **`unordered_map<int, unordered_map<int, int>>`**: 儲存權重或額外資訊。

## 方法 2: `vector` (效能最佳)

當題目保證節點是從 `0` 到 `n-1` 編號時，使用 `vector` 作為鄰接列表的底層容器是最高效的。

- **`vector<vector<int>>`**: 節點 `u` 的鄰居儲存在 `adj[u]`。
- **`vector<vector<pair<int, int>>>`**: 儲存帶權重的邊，`adj[u]` 包含 `pair{neighbor, weight}`。

### 處理有向圖 vs. 無向圖

#### `unordered_map` (或 `map`)

- **有向圖 (Directed)**: 添加邊 `u -> v` 時，只需在 `u` 的鄰居 map 中加入 `v`。
  ```cpp
  // adj 的類型: unordered_map<int, unordered_map<int, int>>
  // 儲存權重為 w
  adj[u][v] = w;
  ```
- **無向圖 (Undirected)**: 添加邊 `(u, v)` 時，需要雙向操作。
  ```cpp
  // adj 的類型: unordered_map<int, unordered_map<int, int>>
  adj[u][v] = 1; // 或者儲存權重
  adj[v][u] = 1; // 或者儲存權重
  ```

#### `vector`

- **有向圖 (Directed)**: 添加邊 `u -> v` 時，只需將 `{v, weight}` 加入 `u` 的鄰居列表。
  ```cpp
  // adj 的類型: vector<vector<pair<int, int>>>
  adj[u].push_back({v, weight});
  ```
- **無向圖 (Undirected)**: 添加邊 `(u, v)` 時，需要雙向操作。
  ```cpp
  // adj 的類型: vector<vector<pair<int, int>>>
  adj[u].push_back({v, weight});
  adj[v].push_back({u, weight}); // 注意權重
  ```

---

## 如何遍歷鄰居

這是鄰接列表最核心的操作，例如在 BFS 或 DFS 中。

### 使用 `unordered_map` 的情況

```cpp
// adj 的類型: std::unordered_map<int, std::unordered_map<int, int>>
void DFS_on_map(int u, std::unordered_map<int, std::unordered_map<int, int>>& adj) {
    if (!adj.contains(u)) { // C++20
        return;
    }

    // C++17 Structured Binding
    for (const auto& [neighbor, weight] : adj.at(u)) {
        // 遞迴呼叫 DFS(neighbor, ...);
    }
}
```

### 使用 `vector` 的情況

```cpp
// adj 的類型: std::vector<std::vector<std::pair<int, int>>>
void DFS_on_vector(int u, std::vector<std::vector<std::pair<int, int>>>& adj) {
    if (u < 0 || u >= adj.size()) {
        return;
    }

    // C++17 Structured Binding
    for (const auto& [neighbor, weight] : adj[u]) {
        // 遞迴呼叫 DFS(neighbor, ...);
    }
}
```

## 結論

| 表示法       | 結構                          | 邊查找效率 | 鄰居查找效率 |
| :----------- | :---------------------------- | :--------- | :----------- |
| 邊集合       | `unordered_set<pair>`         | O(1)       | O(E)         |
| **鄰接列表** | **`unordered_map<int, ...>`** | **O(1)**   | **O(1)**     |

鄰接列表，特別是使用 `unordered_map` 實現的版本，是解決幾乎所有圖論問題的黃金標準，兼具了頂級的效能和靈活性。
