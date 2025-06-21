# DFS 在 Tree 與 Graph 中的結構比較與觀察

---

## 🧠 核心觀察

DFS（深度優先搜尋）在樹與圖中雖然應用場景不同，但其遞迴結構本質上非常相似。以下是從 LeetCode 547 題的 DFS 實作中歸納出的幾個關鍵觀察：

---

## 🔍 DFS 結構對比

| 元素         | Tree 中的 DFS                  | Graph 中的 DFS                          |
| ------------ | ------------------------------ | --------------------------------------- |
| 起始點       | 一定是 root                    | 需自行選擇起點（通常為每個未訪節點）    |
| base case    | 通常為 null 或是滿足條件的位置 | 通常為 visited[node] 為 true            |
| 拜訪當前節點 | 設定值 / 操作結構 / 累積結果等 | `visited[node] = true`                  |
| 遞迴條件     | left/right 子節點存在          | `isConnected[node][i] == 1`             |
| 遞迴次數     | 最多兩次（left, right）        | 視鄰接節點數量而定（可為 0~n-1）        |
| 結構         | 嚴格樹狀（無環）               | 可有環，需特別處理 visited              |
| 呼叫方式     | `dfs(root->left)`              | `dfs(i)` for all `isConnected[node][i]` |

---

## 🧪 LeetCode 547 範例程式碼

```cpp
class Solution {
public:
    int findCircleNum(vector<vector<int>>& isConnected) {
        std::vector<bool> visited(isConnected.size(), false);
        int provinceCount = 0;

        // Iterate through all nodes to ensure all components are covered
        for (int i = 0; i < isConnected.size(); ++i) {
            if (visited[i]) continue;

            dfs(isConnected, i, visited);
            provinceCount++;
        }

        return provinceCount;
    }

    void dfs(const vector<vector<int>>& isConnected, const int node, vector<bool>& visited) {
        // Base case: skip already visited elements
        if (visited[node]) return;

        // Mark the current element as visited
        visited[node] = true;

        // Explore all related elements
        // If a connection exists and the element hasn't been visited, recurse
        for (int i = 0; i < isConnected.size(); ++i) {
            if (isConnected[node][i]) {
                dfs(isConnected, i, visited);
            }
        }
    }
};
```

---

## 🧩 結構對應說明

| DFS 元素     | 程式碼對應行為                        |
| ------------ | ------------------------------------- |
| base case    | `if (visited[node]) return;`          |
| 拜訪當前節點 | `visited[node] = true;`               |
| 遞迴條件     | `if (isConnected[node][i])`           |
| 遞迴呼叫     | `dfs(isConnected, i, visited);`       |
| 起始點選擇   | `for (int i = 0; i < n; ++i)` loop 中 |

---

## 🧠 結論

- DFS 的遞迴結構在 tree 與 graph 中幾乎一致，差別在於：

  - **是否需要 visited 陣列**（graph 必須）
  - **遞迴次數是否固定**（tree 為 2，graph 為鄰接數）
  - **起始點是否唯一**（tree 為 root，graph 需遍歷所有 component）

- 若你已熟悉 binary tree 的 DFS，轉換到 graph 的 DFS 只需多加注意 visited 與起點選擇邏輯，即可無痛遷移。

這種結構對應的理解，有助於你在面對不同資料結構時快速建立遞迴邏輯。
