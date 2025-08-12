# Design 1: Quick Find

Quick Find 是 Disjoint Set 最直觀的一種實現方式。

## 1. 核心概念

- **資料結構**: 使用一個整數陣列 `parent`（或 `root`），其中 `parent[i]` **直接儲存**元素 `i` 所在集合的根節點。
- **初始化**: `parent[i] = i`，表示初始時，每個元素都是一個獨立的集合，且根節點就是它自己。

## 2. 實作

```cpp
class QuickFind {
private:
    vector<int> parent;

public:
    QuickFind(int n) : parent(n) {
        for (int i = 0; i < n; ++i) {
            parent[i] = i;
        }
    }

    // 找到 x 的根節點
    int find(int x) {
        return parent[x]; // O(1)
    }

    // 將 x 和 y 的集合合併
    void unionSet(int x, int y) {
        int rootX = find(x);
        int rootY = find(y);
        if (rootX != rootY) {
            // 將所有 rootX 的成員的根節點都改為 rootY
            for (int i = 0; i < parent.size(); ++i) { // O(n)
                if (parent[i] == rootX) {
                    parent[i] = rootY;
                }
            }
        }
    }

    // 檢查 x 和 y 是否連通
    bool connected(int x, int y) {
        return find(x) == find(y);
    }
};
```

## 3. 複雜度分析

- **`find(x)`**: `O(1)`

  - 因為我們直接儲存了根節點，所以查找操作只需要一次陣列存取。

- **`union(x, y)`**: `O(N)`

  - 這是 Quick Find 的主要瓶頸。為了合併兩個集合，我們需要遍歷整個 `parent` 陣列，將其中一個集合的所有成員的根節點更新為另一個集合的根節點。

- **`connected(x, y)`**: `O(1)`
  - 因為它內部只呼叫了兩次 `find` 操作。

**結論**: Quick Find 的 `find` 操作非常快，但 `union` 操作非常慢，導致整體效率不佳，尤其是在 `union` 操作頻繁的場景下。
