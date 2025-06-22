# 格狀圖（Lattice Graph / Grid Graph）

---

## 1. 定義

**格狀圖**（或稱網格圖）是一種特殊的圖，其節點（vertices）被排列在一個二維或更高維度的網格中。在二維格狀圖中，每個節點的鄰居通常是其上、下、左、右的四個節點（有時也包括對角線的八個節點）。

### 關鍵特性

- **結構化**：節點位置固定，鄰居關係明確。
- **隱式圖**：通常不會明確給出圖的結構（如鄰接表），而是透過一個二維矩陣（matrix）或網格（grid）來表示。你需要自行根據規則（如上下左右移動）來確定邊。
- **權重**：邊可以有權重，例如，矩陣中的值可以代表移動到該格的成本。

---

## 2. 應用

格狀圖在演算法問題中非常常見，特別是：

- **路徑尋找**：在迷宮或地圖中找最短路徑（如 Dijkstra、A\*）。
- **狀態空間搜索**：當問題的狀態可以用網格座標表示時。
- **動態規劃**：許多 DP 問題的狀態轉移可以在格狀圖上視覺化。
- **圖像處理**：像素可以被視為格狀圖的節點。

---

## 3. C++ 實作

在 C++ 中，格狀圖通常用 `vector<vector<int>>` 來表示。遍歷時，我們需要一個方向陣列來簡化移動邏輯。

```cpp
#include <iostream>
#include <vector>
#include <queue>

// 代表格狀圖
using Grid = std::vector<std::vector<int>>;

// 4 個方向：上、下、左、右
int dr[] = {-1, 1, 0, 0};
int dc[] = {0, 0, -1, 1};

// (有時需要 8 個方向，加上對角線)
// int dr8[] = {-1, -1, -1, 0, 0, 1, 1, 1};
// int dc8[] = {-1, 0, 1, -1, 1, -1, 0, 1};

void bfs(Grid& grid, int start_r, int start_c) {
    int rows = grid.size();
    if (rows == 0) return;
    int cols = grid[0].size();

    std::vector<std::vector<bool>> visited(rows, std::vector<bool>(cols, false));
    std::queue<std::pair<int, int>> q;

    q.push({start_r, start_c});
    visited[start_r][start_c] = true;

    while (!q.empty()) {
        std::pair<int, int> curr = q.front();
        q.pop();
        int r = curr.first;
        int c = curr.second;

        std::cout << "Visiting (" << r << ", " << c << ")" << std::endl;

        // 探索 4 個方向的鄰居
        for (int i = 0; i < 4; ++i) {
            int nr = r + dr[i];
            int nc = c + dc[i];

            // 檢查邊界條件與是否已訪問
            if (nr >= 0 && nr < rows && nc >= 0 && nc < cols && !visited[nr][nc]) {
                visited[nr][nc] = true;
                q.push({nr, nc});
            }
        }
    }
}

int main() {
    Grid grid = {
        {1, 1, 0, 1},
        {1, 0, 1, 1},
        {1, 1, 1, 0},
        {0, 1, 1, 1}
    };
    bfs(grid, 0, 0);
    return 0;
}
```

---

## 4. LeetCode 上的辨識與使用

### 如何辨識？

- **輸入是二維陣列/矩陣**：`vector<vector<char>>`、`vector<vector<int>>`。
- **問題描述涉及「網格」、「迷宮」、「島嶼」、「矩陣」**。
- **移動規則被定義**：例如「只能上下左右移動」、「可以走對角線」。

### 常見題型

| 題型             | LeetCode 範例                                                                                         | 解法                         |
| ---------------- | ----------------------------------------------------------------------------------------------------- | ---------------------------- |
| **島嶼數量**     | [200. Number of Islands](https://leetcode.com/problems/number-of-islands/)                            | DFS/BFS 遍歷，計算連通塊數量 |
| **最短路徑**     | [1091. Shortest Path in Binary Matrix](https://leetcode.com/problems/shortest-path-in-binary-matrix/) | BFS（因為邊權重為 1）        |
| **尋找特定路徑** | [79. Word Search](https://leetcode.com/problems/word-search/)                                         | Backtracking (DFS)           |
| **成本最小路徑** | [64. Minimum Path Sum](https://leetcode.com/problems/minimum-path-sum/)                               | 動態規劃                     |

### 解題步驟

1. **確認圖的類型**：是二進位矩陣（0/1）還是有權重？移動方向是 4 個還是 8 個？
2. **選擇演算法**：
   - 找**連通塊**（島嶼） → DFS/BFS
   - 找**最短路徑**（無權重） → BFS
   - 找**最短路徑**（有權重） → Dijkstra
   - 找**所有可能路徑**或**是否存在路徑** → Backtracking/DFS
3. **定義 `visited` 陣列**：`vector<vector<bool>>` 是必需的，以避免重複訪問。
4. **使用方向陣列**：`dr`, `dc` 可以讓你的程式碼更簡潔。
5. **處理邊界條件**：在探索鄰居時，務必檢查是否超出網格範圍。
