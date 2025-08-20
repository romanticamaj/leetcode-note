# 加權並查集與路徑壓縮 (Weighted Union-Find with Path Compression)

本指南旨在說明一個清晰、具體的加權並查集（Weighted Union-Find）實作。此結構透過「權重」來記錄集合內元素之間的相對關係（在此範例中為比率），是解決 LeetCode 399. Evaluate Division 等問題的強力工具。

## 1. 核心概念與公式

加權並查集在標準並查集的基礎上，為每個節點增加一個 `weight` 屬性。`weight[i]` 記錄節點 `i` 到其父節點 `parent[i]` 的相對關係。在「Evaluate Division」問題中，這個關係是除法比率：`weight[i] = i / parent[i]`。

### 路徑壓縮中的權重更新

在 `find` 操作進行路徑壓縮時，節點 `i` 的父節點會直接指向根節點 `root`。其權重也必須更新：

- **舊關係**: `weight[i] = i / parent[i]` 和 `weight[parent[i]] = parent[i] / root`
- **新關係**: `weight[i]_new = i / root = (i / parent[i]) * (parent[i] / root) = weight[i] * weight[parent[i]]`
  因此，權重更新規則為 **`weight[i] *= weight[parent[i]]`**。

### 合併時的權重更新

當我們根據 `a / b = v` 合併兩個集合時，若決定將 `a` 的根 `root_a` 合併到 `b` 的根 `root_b` (`parent[root_a] = root_b`)，我們需要計算 `weight[root_a]` 的新值，即 `root_a / root_b`。

- **已知**: `a / b = v`
- **壓縮後**: `weight[a] = a / root_a` => `root_a = a / weight[a]`
- **壓縮後**: `weight[b] = b / root_b` => `root_b = b / weight[b]`

**推導 `root_a / root_b`**:
`root_a / root_b = (a / weight[a]) / (b / weight[b]) = (a / b) * (weight[b] / weight[a]) = v * weight[b] / weight[a]`

這就是 `union` 操作中權重計算的核心。

## 2. C++ 實作 (for LeetCode 399)

這是一個專為 LeetCode 399 設計的、清晰易懂的 C++ 實作。
**注意**: `contains` 是 C++20 的特性。如果使用舊版編譯器，需改用 `find(key) != map.end()`。

```cpp
#include <string>
#include <unordered_map>
#include <vector>
#include <optional>

class WeightedUnionFind {
public:
    // 尋找節點的根，並在過程中進行路徑壓縮與權重更新
    std::string find(const std::string& s) {
        // 如果節點不存在，則初始化
        if (!parent.contains(s)) {
            parent[s] = s;
            weight[s] = 1.0;
            return s;
        }

        // 如果節點是根，直接返回
        if (parent[s] == s) {
            return s;
        }

        // 遞歸尋找根，並進行路徑壓縮
        std::string root = find(parent[s]);

        // 更新權重：s/root = (s/original_parent) * (original_parent/root)
        weight[s] = weight[s] * weight[parent[s]];

        return parent[s] = root;
    }

    // 根據 a / b = value 合併兩個集合
    void unite(const std::string& a, const std::string& b, double value) {
        std::string root_a = find(a);
        std::string root_b = find(b);

        if (root_a != root_b) {
            // 將 a 的樹合併到 b 的樹
            parent[root_a] = root_b;
            // 更新 root_a 的權重: weight[root_a] = root_a / root_b
            // 推導: root_a/root_b = (a/b) * (weight_b/weight_a) = value * weight[b] / weight[a]
            weight[root_a] = value * weight[b] / weight[a];
        }
    }

    // 查詢 a / b 的結果
    std::optional<double> query(const std::string& a, const std::string& b) {
        // 檢查節點是否存在於並查集中
        if (!parent.contains(a) || !parent.contains(b)) {
            return std::nullopt;
        }

        std::string root_a = find(a);
        std::string root_b = find(b);

        if (root_a != root_b) {
            return std::nullopt; // 不在同一集合，無法計算
        }

        // a/b = (a/root_a) / (b/root_b) = weight[a] / weight[b]
        return weight[a] / weight[b];
    }

private:
    // parent[s] 儲存節點 s 的父節點
    std::unordered_map<std::string, std::string> parent;
    // weight[s] 儲存比率 s / parent[s]
    std::unordered_map<std::string, double> weight;
};
```

## 3. 時間複雜度分析

經典的並查集分析指出，當 **同時使用路徑壓縮和按大小/秩合併** 時，操作的均攤時間複雜度可以達到 O(α(n))（幾乎是常數時間）。

然而，在當前的「加權並查集」實作中，我們 **只使用了路徑壓縮**。我們沒有使用「按大小/秩合併」，因為合併的方向是由數學關係決定的，而不是由集合的大小或秩決定的。

因此，其時間複雜度分析有所不同：

- **單次操作最壞情況 (Worst Case)**：如果樹的結構退化成一個鏈表，單次的 `find` 操作可能需要 O(N) 的時間。
- **均攤時間複雜度 (Amortized Analysis)**：對於一個包含 `m` 次操作的序列，僅使用路徑壓縮的總時間複雜度為 O(m log N)。因此，單次操作的均攤時間可以視為 **O(log N)**。

**對於 LeetCode 面試**：

- **精確回答**：應說明此特定實作（僅路徑壓縮）的均攤時間複雜度為 O(log N)。可以補充說明，如果能結合按大小/秩合併，則可優化至 O(α(n))。
- **「Evaluate Division」的總時間**：
  - 建立並查集結構（`E` 個方程式）：O(E \* log N)，其中 `N` 是唯一變數的數量。
  - 回答查詢（`Q` 個查詢）：O(Q \* log N)。
  - **整體複雜度**：**O((E + Q) \* log N)**。

雖然不如 O(α(n)) 理想，但 O(log N) 的均攤效率在絕大多數情況下仍然非常高效，並且是此類問題的正確解法。
