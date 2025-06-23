# 圖的表示法 (1): 邊列表與邊集合

## tl;dr: 面試常用結構

- **`std::vector<std::pair<int, int>>`**: **最基本**。僅用於儲存，查找效率 O(E)。
- **`std::set<std::pair<int, int>>`**: **O(log E) 查找**。適用於需要排序或不方便寫雜湊的場景。
- **`std::set<std::vector<int>>`**: **C++20 限定**。處理帶權重邊 `(u, v, w)` 的簡潔方法。
- **`std::unordered_set<std::pair<int, int>, Hasher>`**: **平均 O(1) 查找**。面試中最常見的高效邊集合。

---

## 1. 邊列表 (Edge List) - 基礎概念

邊列表是表示圖最直觀的方式，它就是一個包含所有邊的簡單列表。

- **結構**: `std::vector<std::pair<int, int>>` 或 `std::vector<std::vector<int>>`
- **優點**: 實現簡單，O(E) 的空間複雜度對於稀疏圖很高效。
- **缺點**: 查找特定邊 `(u, v)` 需要遍歷整個列表，時間複雜度為 **O(E)**，在大多數應用中效率太低。

**常見格式**: 在 LeetCode 等平台上，題目最常以 `std::vector<std::vector<int>>` 的形式給定邊列表。

---

## 2. 邊集合 (Edge Set) - 高效查找

為了克服 O(E) 的查找瓶頸，我們可以將邊儲存在一個**集合 (Set)** 中。這將查找效率提升到對數時間或常數時間。

### 處理無向圖 vs. 有向圖

- **無向圖 (Undirected)**: 邊 `(u, v)` 和 `(v, u)` 是等價的。為了確保唯一性，我們必須**標準化**儲存的邊，例如，總是讓第一個元素小於第二個。`if (u > v) swap(u, v);`
- **有向圖 (Directed)**: 邊 `u -> v` 和 `v -> u` 是不同的。因此，我們**不需要**做任何標準化。

### 實現方式

#### 方法 A: `std::set` (O(log E) 查找)

`std::set` 是一個平衡二元搜尋樹。

**C++11/14/17: 使用 `std::pair`**
這是最常見的方法，因為 `std::pair` 預設就有比較運算子。

```cpp
// 使用 std::set<std::pair<int, int>> 處理無向圖
void check_edges_with_set_pair() {
    std::vector<std::pair<int, int>> edge_list = {{1, 2}, {3, 4}, {2, 1}};
    std::set<std::pair<int, int>> seen_edges;

    for (auto edge : edge_list) {
        if (edge.first > edge.second) std::swap(edge.first, edge.second); // 標準化
        seen_edges.insert(edge);
    }

    if (seen_edges.count({1, 2})) {
        std::cout << "Edge (1, 2) exists." << std::endl;
    }
}
```

**C++20: 直接使用 `std::vector`**
C++20 可以直接使用 `std::set<std::vector<int>>`，在處理帶權重的邊時特別方便。

```cpp
// 使用 std::set<std::vector<int>> 處理帶權重的無向邊
void check_weighted_edges_with_set_vector() {
    std::vector<std::vector<int>> edge_list = {{1, 2, 10}, {2, 1, 10}};
    std::set<std::vector<int>> seen_edges;

    for (auto edge : edge_list) {
        if (edge[0] > edge[1]) std::swap(edge[0], edge[1]); // 標準化
        seen_edges.insert(edge);
    }

    if (seen_edges.contains({1, 2, 10})) { // C++20
        std::cout << "Edge (1, 2) with weight 10 exists." << std::endl;
    }
}
```

#### 方法 B: `std::unordered_set` (平均 O(1) 查找)

`std::unordered_set` 是基於雜湊表，提供最快的平均查找速度。

```cpp
// 為 std::pair<int, int> 提供自訂的雜湊結構
struct PairHasher {
    std::size_t operator()(const std::pair<int, int>& p) const {
        auto hash1 = std::hash<int>{}(p.first);
        auto hash2 = std::hash<int>{}(p.second);
        return hash1 ^ (hash2 << 1);
    }
};

// 使用 std::unordered_set 處理無向圖
void check_edges_with_unordered_set() {
    std::vector<std::pair<int, int>> edge_list = {{1, 2}, {3, 4}, {2, 1}};
    std::unordered_set<std::pair<int, int>, PairHasher> seen_edges;

    for (auto edge : edge_list) {
        if (edge.first > edge.second) std::swap(edge.first, edge.second); // 標準化
        seen_edges.insert(edge);
    }

    if (seen_edges.contains({1, 2})) { // C++20
        std::cout << "Edge (1, 2) exists. (O(1) average lookup)" << std::endl;
    }
}
```

---

## 結論：邊集合的局限性

雖然邊集合完美地解決了**邊查找**的問題，但它仍然無法高效地回答「**節點 u 的所有鄰居是誰？**」這個問題。要同時解決這兩個問題，需要使用功能更強大的**鄰接列表**。

> **詳細內容請參考：[鄰接列表表示法](./Adjacency_List_Representation.md)**
