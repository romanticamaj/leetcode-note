# Design 3: Union by Rank Optimization

「按秩合併」是對 Quick Union 中 `union` 操作的第一個關鍵優化。它的目標是解決 Quick Union 可能產生「傾斜樹 (skewed tree)」的問題，從而避免 `find` 操作退化到 `O(N)` 的最壞情況。

## 1. 核心概念

- **問題**: 在樸素的 Quick Union 中，我們隨意地將一棵樹的根節點連接到另一棵樹的根節點。這可能導致一棵很高的樹被接到一棵很矮的樹下面，使得整棵樹的高度不必要地增加。
- **解決方案**: 引入一個「秩 (rank)」的概念來近似每棵樹的高度。在合併兩棵樹時，我們總是將**秩較小（較矮）的樹，合併到秩較大（較高）的樹下面**。
- **秩的定義**:
  - `rank[i]` 記錄了以 `i` 為根的樹的高度（或是一個高度的上界）。
  - 初始時，所有節點的 `rank` 都是 1。
- **合併規則**:
  1. 比較兩個根節點 `rootX` 和 `rootY` 的 `rank`。
  2. 將 `rank` 較小的樹的根指向 `rank` 較大的樹的根。
  3. 如果兩者的 `rank` 相等，則可以任選一個作為新的根，但**新的根的 `rank` 必須加一**。

## 2. 實作

```cpp
class UnionByRank {
private:
    vector<int> parent;
    vector<int> rank;

public:
    UnionByRank(int n) : parent(n), rank(n, 1) {
        for (int i = 0; i < n; ++i) {
            parent[i] = i;
        }
    }

    int find(int x) {
        while (x != parent[x]) { // O(logn)
            x = parent[x];
        }
        return x;
    }

    void unionSet(int x, int y) { // O(logn)
        int rootX = find(x);
        int rootY = find(y);
        if (rootX != rootY) { // 建構較好的樹狀結構: 選高的當 root node
            if (rank[rootX] > rank[rootY]) {
                parent[rootY] = rootX;
            } else if (rank[rootX] < rank[rootY]) {
                parent[rootX] = rootY;
            } else {
                parent[rootY] = rootX;
                rank[rootX]++; // 只有在 rank 相等時才增加
            }
        }
    }

    bool connected(int x, int y) {
        return find(x) == find(y);
    }
};
```

## 3. 複雜度分析

通過按秩合併，我們可以保證樹的高度最多為 `O(logN)`。

- **`find(x)`**: `O(logN)`

  - 因為樹的高度被限制在對數級別，所以查找路徑的長度也是對數級別。

- **`union(x, y)`**: `O(logN)`

  - 由 `find` 操作的複雜度決定。

- **`connected(x, y)`**: `O(logN)`
  - 同樣由 `find` 操作的複雜度決定。

**結論**: 按秩合併是一個非常有效的優化，它顯著改善了 Quick Union 的最壞情況性能，將其從線性級別降低到了對數級別。
