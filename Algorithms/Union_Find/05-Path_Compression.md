# Design 4: Path Compression Optimization

「路徑壓縮」是針對 `find` 操作的強力優化。它的核心思想是，在我們辛苦地沿著一條路徑找到根節點後，我們應該「順手」做一些事，讓下一次對同路徑上任何節點的 `find` 操作變得更快。

## 1. 核心概念

- **問題**: 在沒有優化的 Quick Union 中，`find(x)` 操作需要從 `x` 開始，一步步向上走到根。如果這條路徑很長，且我們頻繁地對路徑上的節點（如 `x` 或其父節點）進行 `find`，我們會重複走很多冤枉路。
- **解決方案**: 在 `find(x)` 的過程中，當我們找到最終的根節點 `root` 後，我們再次遍歷從 `x` 到 `root` 的這條路徑，將路徑上**所有節點的 `parent` 指標直接指向 `root`**。
- **效果**: 這會極大地「壓平」樹的結構，使得下次對這些節點的 `find` 操作幾乎是 `O(1)` 的。

## 2. 實作

路徑壓縮最優雅的實現方式是使用**遞迴**。

```cpp
class PathCompression {
private:
    vector<int> parent;

public:
    PathCompression(int n) : parent(n) {
        for (int i = 0; i < n; ++i) {
            parent[i] = i;
        }
    }

    // 找到 x 的根節點，並進行路徑壓縮
    int find(int x) {
        // 如果 x 就是根節點，直接返回
        if (x == parent[x]) {
            return x;
        }
        // 遞迴地向上尋找根節點
        // 在回溯的過程中，將路徑上所有節點的 parent 都設為最終找到的根節點
        return parent[x] = find(parent[x]);
    }

    // union 和 connected 保持不變，因為它們的效率提升完全來自於 find 的優化
    void unionSet(int x, int y) {
        int rootX = find(x);
        int rootY = find(y);
        if (rootX != rootY) {
            parent[rootX] = rootY;
        }
    }

    bool connected(int x, int y) {
        return find(x) == find(y);
    }
};
```

## 3. 複雜度分析

單獨使用路徑壓縮時，`find` 操作的平均時間複雜度可以被證明是 `O(logN)`。

- **`find(x)`**: 平均 `O(logN)`
- **`union(x, y)`**: 平均 `O(logN)`
- **`connected(x, y)`**: 平均 `O(logN)`

雖然單獨使用路徑壓縮已經非常高效，但它與「按秩合併」結合時，能達到近乎常數時間的驚人效率。
