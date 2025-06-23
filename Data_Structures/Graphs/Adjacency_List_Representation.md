# 圖的表示法 (2): 鄰接列表

**鄰接列表 (Adjacency List)** 是表示圖**最常用、最高效**的方法，也是解決大多數圖論問題的**面試首選**。

它的核心思想是為圖中的每一個節點 `u` 維護一個列表或集合，其中包含所有與 `u` 相鄰的節點 `v`。這可以看作是一個從節點到其鄰居列表的映射。

在 LeetCode 等平台上，題目通常會以**邊列表 (`std::vector<std::vector<int>>`)** 的形式給定圖的邊，我們的第一步幾乎總是將這個輸入轉換為高效的鄰接列表，以便後續處理。

## tl;dr: 面試常用結構

- **`std::unordered_map<int, std::unordered_set<int>>`**: **最常用**。儲存節點到其**唯一**鄰居的映射。不允許重複邊。
- **`std::unordered_map<int, std::vector<int>>`**: 儲存節點到其鄰居的映射。**允許重複邊** (平行邊)。
- **`std::unordered_map<int, std::unordered_map<int, int>>`**: **最強大**。儲存節點到鄰居的映射，並為每條邊附加額外資訊（如權重、方向標記等）。

---

## C++ 高效實現：`unordered_map`

在 C++ 中，實現鄰接列表最快、最靈活的方式是使用 `std::unordered_map`，它提供了平均 O(1) 的查找效率。

### 基本結構：`unordered_map<int, unordered_set<int>>`

- **外層 Map**: `unordered_map<int, ...>` 將每個節點 `u` 映射到它的鄰居集合。
- **內層 Set**: `...unordered_set<int>>` 儲存 `u` 的所有鄰居，並允許在 O(1) 時間內判斷某個鄰居是否存在。

### 處理有向圖 vs. 無向圖

- **有向圖 (Directed)**: 添加邊 `u -> v` 時，只需將 `v` 加入 `u` 的鄰居集合。`adj[u].insert(v);`
- **無向圖 (Undirected)**: 添加邊 `(u, v)` 時，需要雙向操作：將 `v` 加入 `u` 的鄰居集合，**同時**將 `u` 加入 `v` 的鄰居集合。`adj[u].insert(v); adj[v].insert(u);`

### 程式碼範例

```cpp
class Graph {
private:
    std::unordered_map<int, std::unordered_set<int>> adj;

public:
    // 添加一條有向邊 u -> v
    void addDirectedEdge(int u, int v) {
        adj[u].insert(v);
    }

    // 添加一條無向邊
    void addUndirectedEdge(int u, int v) {
        adj[u].insert(v);
        adj[v].insert(u);
    }

    // 檢查邊 u -> v 是否存在 (平均 O(1) 時間)
    bool hasEdge(int u, int v) {
        if (adj.contains(u)) { // C++20
            return adj.at(u).contains(v);
        }
        return false;
        // C++11/14/17: return adj.count(u) && adj.at(u).count(v);
    }
};
```

---

## 進階變形：儲存額外資訊 (如權重或方向)

鄰接列表的真正威力在於其靈活性。我們可以輕易地修改內層的集合來儲存更多資訊。

### 範例：儲存加權邊

只需將內層的 `unordered_set<int>` 改為 `unordered_map<int, int>`，其中第二個 `int` 用於儲存權重。

- **結構**: `std::unordered_map<int, std::unordered_map<int, int>>`
- `adj[u][v] = weight`

```cpp
class WeightedGraph {
private:
    std::unordered_map<int, std::unordered_map<int, int>> adj;

public:
    // 添加一條帶權重的有向邊 u -> v
    void addWeightedEdge(int u, int v, int weight) {
        adj[u][v] = weight;
    }

    int getWeight(int u, int v) {
        if (hasEdge(u, v)) {
            return adj.at(u).at(v);
        }
        return -1; // Or throw an exception
    }

    bool hasEdge(int u, int v) {
        return adj.contains(u) && adj.at(u).contains(v);
    }
};
```

### 範例：同時處理無向連接與有向資訊

這是一個常見的面試變形：圖中的邊是雙向的，但你需要知道原始的有向資訊。

- **結構**: `std::unordered_map<int, std::unordered_map<int, int>>`
- `adj[u][v] = 1` 表示原始邊是 `u -> v`
- `adj[v][u] = -1` 表示 `v` 是 `u` 的一個反向鄰居

```cpp
class BidirectionalGraph {
private:
    std::unordered_map<int, std::unordered_map<int, int>> adj;

public:
    void addDirectedEdge(int u, int v) {
        adj[u][v] = 1;  // 正向邊
        adj[v][u] = -1; // 反向邊
    }

    bool hasOutgoingEdge(int u, int v) {
        return adj.contains(u) && adj.at(u).contains(v) && adj.at(u).at(v) == 1;
    }
};
```

## 結論

| 表示法       | 結構                          | 邊查找效率 | 鄰居查找效率 |
| :----------- | :---------------------------- | :--------- | :----------- |
| 邊集合       | `unordered_set<pair>`         | O(1)       | O(E)         |
| **鄰接列表** | **`unordered_map<int, ...>`** | **O(1)**   | **O(1)**     |

鄰接列表，特別是使用 `unordered_map` 實現的版本，是解決幾乎所有圖論問題的黃金標準，兼具了頂級的效能和靈活性。
