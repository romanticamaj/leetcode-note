# State-Space BFS

## tl;dr

BFS 遍歷的是一個「狀態空間」，而不僅僅是物理位置。佇列中的每個節點都代表一個獨特的 `(位置, 狀態)`。

也可稱作 BFS with State Tracking

- **High-Dimensional `visited`**: `visited` 集合必須記錄完整的狀態，以防止對同一狀態的重複探索。
- **State as a Node**: 將每個 `(位置, 狀態)` 組合視為圖中的一個獨立節點。剪枝不能僅基於位置。
- **State-Conditioned Queuing**: 只有當一個新狀態比同一位置上先前記錄的狀態「更優」（例如，剩餘資源更多）時，才應將其加入佇列。

---

## 🧠 問題背景：何時需要「State-Space BFS」？

當你遇到以下任一情況，就需要將標準 BFS 升級為「State-Space BFS」：

- **條件式移動**: 格子的可走性取決於「當前狀態」（如：持有鑰匙、剩餘生命值）。
- **狀態影響決策**: 當前狀態會改變後續的移動能力或結果（如：消耗資源後才能通過）。
- **高維最短路**: 尋找最短路徑，但不能單純用 `visited[r][c]` 來判斷是否已訪問。

---

## ✅ Step 1: 狀態建模 (State Modeling)

傳統 BFS 的佇列中儲存的是 `(r, c)`，但在 State-Space BFS 中，你處理的是一個更豐富的結構：

```cpp
// 狀態的抽象表示
struct State {
    int r, c;
    int remaining_k; // 範例：剩餘可破壞障礙物的次數
    int keys_mask;   // 範例：已持有的鑰匙集合 (位元遮罩)
};
```

BFS 的核心單位從「位置」變成了「狀態」。

---

## ✅ Step 2: Visited 陣列的對應設計

因為狀態是多維的，`visited` 的設計也必須能對應整個狀態空間，以防止重複且無效的探索。

### ✦ 方法一：完整狀態空間建模 (3D Grid Analogy)

你可以將 `(r, c, state)` 想像成一個三維空間。`r` 和 `c` 是平面上的座標，而 `state` 是 Z 軸（深度）。

- **2D Grid**: 是一個平面。
- **3D State-Space**: 像是將多個平面疊加起來，每一層代表一個不同的狀態 `k`。

因此，`visited` 陣列也從二維變成了三維，`visited[r][c][k]` 的意義就是「在狀態 `k` 下，是否訪問過 `(r, c)` 這個位置」。

```cpp
// 範例：visited[r][c][k]
vector<vector<vector<bool>>> visited(m, vector<vector<bool>>(n, vector<bool>(k + 1, false)));
```

### ✦ 方法二：記錄該位置的最佳狀態 (空間優化)

當狀態是數值且有「優劣」之分時（如剩餘步數、生命值），可以用一個二維陣列來記錄到達某位置時的「最佳狀態」。

```cpp
// 範例：visited[r][c] 記錄到達 (r,c) 的最佳狀態 (e.g., 剩餘步數)
vector<vector<int>> visited(m, vector<int>(n, -1));

// 條件式入隊
if (state > visited[nr][nc]) {
    new_state = update(state); // e.g., 減少步數, 增加武器

    visited[nr][nc] = new_state;
    queue.push({nr, nc, new_state});
}
```

這兩種方法的本質都是：

> **對每個 `(位置, 狀態)` 進行去重，避免冗餘探索。**

---

## ✅ Step 3: 為什麼 BFS 仍能保證最短距離？

BFS 的最短路保證在狀態空間中依然成立：

> **第一次訪問某個 `(位置, 狀態)` 的組合，其步數必定是到達該狀態的最短距離。**

這是因為 BFS 嚴格按照層級（level）順序進行擴展。只要你確保每個 `(位置, 狀態)` 只入隊一次，那麼當你第一次從佇列中取出目標狀態時，其所在的層級就是最短步數。

---

## ✅ Step 4: 正確的剪枝觀念

| 錯誤觀念                         | 正確觀念                                       |
| :------------------------------- | :--------------------------------------------- |
| 「這個**位置**來過了，不用再走」 | 「如果**狀態**不同，這是一條全新的路」         |
| 「`visited` 應以**座標**為準」   | 「`visited` 應以**完整狀態**為 Key」           |
| 「能走就全部放進 queue」         | 「只有當新狀態比舊狀態**更有潛力**時，才入隊」 |

**內心提問法**:

> 「我現在以**這個狀態**來到這個位置，比上次的狀態更強嗎？如果是，那這條路就值得繼續探索。」

---

## 🛠️ 通用演算法結構 (空間優化版)

```cpp
// visited[r][c] = 到達 (r,c) 時的最佳狀態 (e.g., 剩餘 k)
vector<vector<int>> visited(m, vector<int>(n, -1));
queue<State> q; // State: {r, c, state_value}

// 初始化
q.push({0, 0, initial_state});
visited[0][0] = initial_state;

int distance = 0;
while (!q.empty()) {
    int level_size = q.size();

    while (level_size--) {
        auto [r, c, state] = q.front();
        q.pop();

        if (r == m - 1 && c == n - 1) { // ending point found or meet specific condition
            return distance;
        }

        for (auto& dir : directions) {
            int nr = r + dir.first;
            int nc = c + dir.second;

            if (is_out_of_bounds(nr, nc)) continue;

            // 剪枝：如果新狀態無效，或不如之前到達該點的狀態，則跳過
            if (state < 0 || visited[nr][nc] >= state) continue;

            // 根據當前狀態計算新狀態, Marked-On-Push
            auto new_state = calculate_new_state(state, grid[nr][nc]);

            visited[nr][nc] = new_state;
            q.push({nr, nc, new_state});
        }
    }
    distance++;
}
return -1; // 無法到達
```

---

## 📘 延伸練習題目

| 題目編號                                                 | 狀態空間設計                    |
| :------------------------------------------------------- | :------------------------------ |
| 1293. Shortest Path in a Grid with Obstacles Elimination | `(r, c, remaining_k)`           |
| 864. Shortest Path to Get All Keys                       | `(r, c, keys_mask)`             |
| 847. Shortest Path Visiting All Nodes                    | `(current_node, visited_mask)`  |
| 773. Sliding Puzzle                                      | `(board_string, zero_position)` |

---

## ✅ 結語

當你遇到「帶有條件的最短路徑」問題時，就應該啟動這套心法：

> **State-Space BFS → 狀態空間建模 → 高維 visited → 條件式入隊**

這是處理所有「條件型路徑搜尋」問題的萬用套路。
