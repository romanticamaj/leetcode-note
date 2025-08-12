# Ultimate Design: Path Compression + Union by Rank

將「按秩合併」和「路徑壓縮」兩個優化結合起來，我們可以得到一個效率極高的 Disjoint Set 最終版本。這也是在解決實際問題時，最推薦理解和記憶的模板。

## 1. 核心概念

- **`find` 操作**: 使用「路徑壓縮」優化。在查找根節點的同時，將路徑上的所有節點直接連接到根上，壓平查詢樹。
- **`union` 操作**: 使用「按秩合併」優化。在合併時，總是將較矮的樹（rank 較小）連接到較高的樹（rank 較大）上，以抑制樹高的增長。

**注意**: 當同時使用這兩種優化時，`rank` 陣列記錄的就不再是精確的樹高，而是一個「高度的上界」。因為路徑壓縮會改變樹的結構，但我們為了效率，不去更新 `rank` 值。儘管如此，這個 `rank` 值仍然是「按秩合併」策略的一個有效指標。

## 2. 實作 (推薦模板)

這段程式碼整合了兩種優化，並加入了計算連通分量數量的功能，非常適用於 LeetCode 問題。

```cpp
class DisjointSet {
public:
    DisjointSet(const int n): parent(n), rank(n, 1), connectedCount(n) {
        for (int i = 0; i < n; i++) parent[i] = i;
    }

    int find(const int x) {
        if (x == parent[x]) return x;

        // Some ranks may become obsolete so they are not updated
        return parent[x] = find(parent[x]); // path compression
    }

    void unionSet(const int x, const int y) {
        const int rootX = find(x);
        const int rootY = find(y);

        if (rootX != rootY) {
            if (rank[rootX] > rank[rootY]) {
                parent[rootY] = rootX; // 選高的當 parent node
            } else if (rank[rootX] < rank[rootY]) {
                parent[rootX] = rootY; // 選高的當 parent node
            } else {
                parent[rootY] = rootX; // 任選一個當 parent node
                rank[rootX]++; // 更新 rank
            }

            connectedCount--;
        }
    }

    bool connected(const int x, const int y) {
        return find(x) == find(y);
    }

    int size() const { return connectedCount; }

private:
    vector<int> parent;
    vector<int> rank;

    int connectedCount;
};
```

## 3. 複雜度分析

結合了兩種優化的 Disjoint Set，其操作的均攤時間複雜度 (Amortized Time Complexity) 非常接近常數時間。

- **`find` / `union` / `connected`**: `O(α(N))`
  - `α(N)` 是**反阿克曼函數 (Inverse Ackermann Function)**。這個函數的增長速度極其緩慢，對於任何在現實世界中可能出現的 `N` 值，`α(N)` 的值都不會超過 5。
  - 因此，在實務上，我們可以將 `O(α(N))` 視為**均攤 O(1)**。
