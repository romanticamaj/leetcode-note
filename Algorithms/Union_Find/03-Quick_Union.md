# Design 2: Quick Union

Quick Union 是對 Quick Find 的一種改進，它優化了 `union` 操作，但犧牲了 `find` 操作的效率。

## 1. 核心概念

- **資料結構**: 同樣使用一個整數陣列 `parent`，但 `parent[i]` 儲存的是元素 `i` 的**父節點**。這形成了一個或多個樹狀結構。
- **根節點**: 一個集合的根節點是其 `parent` 指向自己的那個節點，即 `parent[i] == i`。
- **初始化**: `parent[i] = i`，初始時每個元素都是一棵只有單一節點的樹。

## 2. 實作

```cpp
class QuickUnion {
private:
    vector<int> parent;

public:
    QuickUnion(int n) : parent(n) {
        for (int i = 0; i < n; ++i) {
            parent[i] = i;
        }
    }

    // 找到 x 的根節點
    int find(int x) {
        while (x != parent[x]) { // O(n)
            x = parent[x];
        }
        return x;
    }

    // 將 x 和 y 的集合合併
    void unionSet(int x, int y) { // O(n)
        int rootX = find(x);
        int rootY = find(y);
        if (rootX != rootY) { // O(1)
            // 只需改變一個根節點的 parent
            parent[rootX] = rootY;
        }
    }

    // 檢查 x 和 y 是否連通
    bool connected(int x, int y) {
        return find(x) == find(y);
    }
};
```

## 3. 複雜度分析

- **`find(x)`**: `O(N)`

  - 在最壞的情況下，樹可能退化成一條鏈（skewed tree），此時尋找根節點需要遍歷所有 N 個節點。

- **`union(x, y)`**: `O(N)`

  - `union` 操作本身很快，只需要改變一個指標。但它依賴於兩次 `find` 操作，所以其複雜度由 `find` 決定。

- **`connected(x, y)`**: `O(N)`
  - 同樣，由 `find` 操作的複雜度決定。

## 4. 為何 Quick Union 更高效？

雖然在最壞情況下，Quick Union 的 `find` 和 `union` 都是 `O(N)`，看起來沒有比 Quick Find 好。但 Quick Union 的**潛力**在於，它的樹狀結構為後續的優化（按秩合併、路徑壓縮）提供了可能。

- **Quick Find**: `union` 操作的 `O(N)` 是「硬性」的，每次都必須遍歷整個陣列，無法優化。
- **Quick Union**: `union` 的 `O(N)` 來自於 `find`，是「彈性」的。只要我們能優化 `find` 的效率（即降低樹的高度），就能同時優化 `union`。

因此，Quick Union 雖然本身不完美，但它是一個通往更高效演算法的關鍵墊腳石。
