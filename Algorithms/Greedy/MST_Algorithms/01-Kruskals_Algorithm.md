# Kruskal's Algorithm for Minimum Spanning Tree

---

## 1. 核心設計概念

Kruskal 演算法採用**以邊為中心**的貪婪策略來建構最小生成樹 (MST)。其核心思想非常直觀：

> **在不形成環路 (Cycle) 的前提下，持續選擇圖中權重最小的邊。**

這個過程就像是從一盤散落的節點開始，不斷用最短的繩子將兩個尚未連通的節點群體連接起來，直到所有節點都連通為止。演算法的正確性由 **Cut Property** 保證。

### 核心元件

1. **Greedy Strategy**: 演算法的每一步都做出局部最優選擇（選擇當前可用的最輕邊）。
2. **Cycle Detection**: 必須有一個高效的機制來判斷加入一條新邊是否會形成環路。
3. **Edge-centric**: 整個演算法是圍繞著一個全局的、排序好的邊列表來進行的。

---

## 2. Data Structure

為了高效地實現 Kruskal 演算法，需要兩個關鍵的資料結構：

1. **優先佇列 (Min-Heap)**:
   - **用途**: 用於儲存圖中所有的邊，並能以 `O(log E)` 的效率提取出當前權重最小的邊。
   - **結構**: 佇列中的元素通常是一個 `tuple<int, int, int>`，分別代表 `(weight, u, v)`。對於二維座標點，`u` 和 `v` 可以是它們在原陣列中的索引。

2. **並查集 (Disjoint Set Union, DSU)**:
   - **用途**: 這是 Kruskal 演算法的精髓所在，用於高效地**偵測環路**。它能以近乎 `O(1)` 的均攤時間複雜度完成兩件事：
     - `find(u)`: 查找節點 `u` 所在的集合的代表元素。
     - `union(u, v)`: 合併 `u` 和 `v` 所在的兩個集合。
   - **環路偵測原理**: 在考慮加入一條邊 `(u, v)` 之前，如果 `find(u) == find(v)`，代表 `u` 和 `v` 早已透過其他邊連通。此時若再加入 `(u, v)`，必然會形成一條環路。

---

## 3. C++ 實作 (LeetCode 1584. Min Cost to Connect All Points)

這個範例完美地展示了 Kruskal 演算法的應用。題目要求連接所有點的最小成本，這是一個典型的 MST 問題。圖是**稠密的 (Dense)**，因為任意兩點之間都存在一條邊。

```cpp
class Solution {
public:
    int minCostConnectPoints(vector<vector<int>>& points) {
        const int n = points.size();

        // 1. 建構優先佇列，儲存所有可能的邊
        // 對於稠密圖，邊的數量是 O(n^2)
        priority_queue<tuple<int, int, int>, vector<tuple<int, int, int>>, std::greater<tuple<int, int, int>>> q;
        //// 格式: {weight, index_of_point1, index_of_point2}

        for (int i = 0; i < n; i++) {
            for (int j = i + 1; j < n; j++) {
                const int weight = abs(points[i][0] - points[j][0]) + abs(points[i][1] - points[j][1]);
                q.push({weight, i, j});
            }
        }

        // 2. 建構並查集
        DisjointSet disjointSet(n);

        int edgeCount = 0;
        int minCost = 0;

        // 3. 貪婪策略 + 環路偵測
        while (edgeCount < n - 1) {
            const auto [weight, i, j] = q.top(); q.pop();

            // 如果 i 和 j 已連通，加入此邊會形成環路，跳過
            if (disjointSet.connected(i, j)) continue;

            // 安全邊，選擇此邊
            disjointSet.unionSet(i, j); // 將 i 和 j 的集合合併
            minCost += weight;
            edgeCount++;
        }

        return minCost;
    }

private:
    class DisjointSet {
    private:
        vector<int> parent;
        vector<int> rank;

    public:
        DisjointSet(const int n) : parent(n), rank(n, 1) {
            for (int i = 0; i < n; i++) parent[i] = i;
        }

        int find(const int x) {
            if (x == parent[x]) return x;
            return parent[x] = find(parent[x]); // Path Compression
        }

        void unionSet(const int x, const int y) {
            const int rootX = find(x);
            const int rootY = find(y);

            if (rootX != rootY) {
                // Union by Rank
                if (rank[rootX] > rank[rootY]) {
                    parent[rootY] = rootX;
                } else if (rank[rootX] < rank[rootY]) {
                    parent[rootX] = rootY;
                } else {
                    parent[rootY] = rootX;
                    rank[rootX]++;
                }
            }
        }

        bool connected(const int x, const int y) {
            return find(x) == find(y);
        }
    };
};
```

---

## 4. 複雜度分析

假設圖中有 `V` 個頂點和 `E` 條邊。

### 時間複雜度

主要瓶頸在於對邊的排序(Sorting or Priority Queue)。

- **通用情況**: `O(E log E)`
- **稠密圖**: `O(V^2 log V)`

說明如下：

- **建構優先佇列**:
  - 對於**稀疏圖 (Sparse Graph)**，`E` 遠小於 `V^2`，需要 `O(E)` 的時間。
  - 對於**稠密圖 (Dense Graph)**，如本例，`E` 約等於 `V^2 / 2`，需要 `O(V^2)` 的時間。
- **排序/提取**:
  - 從優先佇列中提取 `V-1` 條邊，總時間為 `O(E log E)`。在稠密圖中，這變為 `O(V^2 log(V^2)) = O(V^2 * 2 log V) = O(V^2 log V)`。
- **並查集操作**:
  - `V-1` 次 `union` 和約 `2*E` 次 `find`。使用優化後，總時間約為 `O(E * α(V))`，其中 `α(V)` 是反阿克曼函數，可視為常數。

### 空間複雜度

- **通用情況**: `O(V + E)`
- **稠密圖**: `O(V^2)`

說明如下：

- **優先佇列**: `O(E)`，稠密圖中為 `O(V^2)`。
- **並查集**: `O(V)`。
