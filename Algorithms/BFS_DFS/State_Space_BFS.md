# 狀態空間 BFS (State-Space BFS)

## tl;dr

BFS 遍歷的是一個「狀態空間」，而不僅僅是物理位置。佇列中的每個節點都代表一個獨特的 `(位置, 狀態)`。

- **State as a Node**: 將每個 `(位置, 狀態)` 組合視為圖中的一個獨立節點。剪枝不能僅基於位置。
- **High-Dimensional `visited`**: `visited` 集合必須記錄完整的狀態，以防止對同一狀態的重複探索。
- **State-Conditioned Queuing**: 只有當一個新狀態合法且比同一位置上先前記錄的狀態「更優」（例如，剩餘資源更多）時，才應將其加入佇列。

---

## 🧠 問題背景：何時需要「State-Space BFS」？

當你遇到以下任一情況，就需要將標準 BFS 升級為「State-Space BFS」：

- **條件式移動**: 格子的可走性取決於「當前狀態」（如：持有鑰匙、剩餘生命值）。
- **狀態影響決策**: 當前狀態會改變後續的移動能力或結果（如：消耗資源後才能通過）。
- **高維最短路**: 尋找最短路徑，但不能單純用 `visited[r][c]` 來判斷是否已訪問。

### 核心矛盾：為何標準 BFS 不足？

讓我們以「消除障礙的最短路徑」為例來思考：

- **如果沒有障礙物限制**：最短路徑就是曼哈頓距離。
- **如果可消除障礙的配額（quota）大於曼哈頓距離**：最短路徑也必然是曼哈頓距離。
- **但現實是，quota 有限**：這意味著我們不能總是走直線，有時必須「繞路」以節省 quota。

這就產生了核心矛盾：為了找到全局最短路徑，我們必須探索所有可能的路徑，同時尊重 quota 的限制。因此，**保留 quota 資訊就變得至關重要**，因為它允許我們**以不同的狀態（quota）重新訪問同一個格子**。

---

## 🧠 題型本質：狀態空間擴張型 BFS

這類問題的核心特徵是：

> 最短路徑不僅取決於「節點位置」，還取決於「附加條件」。這些附加條件會改變你對「已走過」的定義，從而擴張了搜尋的狀態空間。

---

## ✅ 核心設計原則 (Core Design Principles)

### 1. 狀態空間擴張 (State Space Expansion)

- **傳統 BFS**: 狀態只考慮節點 `node`。
- **擴張後**: 狀態是 `(node, extra_condition)` 的組合，例如 `(node, remaining_k)` 或 `(node, incoming_edge_color)`。

> **泛化 takeaway**: 當「一個節點是否走過」的判斷標準，不再只有節點本身，而是需要附加額外條件時，就必須將這些條件納入 BFS 的狀態定義中。

### 2. Visited 維度對應狀態空間 (Visited Dimensions Match the State Space)

- `visited` 陣列必須能夠唯一識別一個完整的狀態。
- 如果狀態是 `(node, color)`，`visited` 就必須是 `visited[node][color]`。
- 如果狀態是 `(r, c, k)`，`visited` 就必須是 `visited[r][c][k]`。

> **泛化 takeaway**: `visited` 的維度必須與狀態空間的維度完全對應，否則會導致重複訪問（造成 TLE）或錯誤剪枝（找不到最佳解）。

### 3. Queue 必須攜帶完整狀態 (Queue Carries the Full State)

- 佇列中儲存的每個元素，都必須包含判斷下一步合法性所需的所有資訊。
- 如果下一步的移動需要知道「上一步的顏色」，那麼這個顏色資訊就必須被放進佇列。

> **泛化 takeaway**: 如果下一步的決策依賴於當前的某個特定狀態，那麼這個狀態就必須在佇列中傳遞。

### 4. 建圖時加入邊的屬性 (Graph Building with Edge Attributes)

- 在許多問題中，附加條件是「邊的性質」（例如：邊的顏色、權重、類型）。
- 在建圖時，應將這些屬性與邊本身綁定。

> **泛化 takeaway**: 考慮使用 `vector<pair<neighbor, attribute>>` 或 `struct Edge` 來建構鄰接串列，使圖的表達更清晰。

### 5. BFS 確保首次到達即為最短 (BFS Guarantees Shortest Path)

- 這個基本原則在擴張的狀態空間中依然成立。
- BFS 按層級擴張，保證了第一次抵達某個完整狀態 `(node, extra_condition)` 的路徑，就是到達該狀態的最短路徑。

---

## 🪜 通用策略模板

當題目要求「滿足特定條件的最短路徑」，且「狀態」不只取決於位置時，遵循以下步驟：

1. **設計狀態空間**：找出所有會影響決策的變數，將它們組合成一個完整的狀態，例如 `(node, extra_state)`。
2. **建構對應的 Visited 結構**：建立一個能夠唯一標識每個狀態的 `visited` 集合或多維陣列。
3. **設計 Queue 結構**：確保佇列中的元素攜帶了判斷下一步所需的所有狀態資訊。
4. **定義入隊條件**：在 BFS 擴展時，只有當新產生的狀態合法且未被訪問過時，才將其加入佇列並標記為已訪問。
5. **更新答案**：在 BFS 的過程中，根據題意在首次訪問節點或滿足終止條件時更新結果。

### 通用程式碼模板 (Generic Code Template)

這是一個結合了上述原則的通用 C++ 模板。實際應用時，需要根據具體問題來定義 `State` 結構、`visited` 的維度和 `is_valid_transition` 函數。

```cpp
// 1. 設計狀態空間 (Define the State)
struct State {
    // ... position info (e.g., r, c or node_id)
    // ... extra state info (e.g., remaining_k, mask, color)
};

// 2. 建構對應的 Visited 結構 (Define the Visited structure)
// e.g., vector<vector<vector<bool>>> visited(m, n, k+1, false);
// e.g., vector<vector<int>> visited(m, n, -1); // For state optimization
// e.g., set<tuple<int, int, int>> visited;

// 3. 設計 Queue 結構 (Define the Queue)
queue<State> q;

// 初始化 (Initialization)
q.push(initial_state);
mark_visited(initial_state);

int distance = 0;
while (!q.empty()) {
    int level_size = q.size();
    while (level_size--) {
        State current = q.front();
        q.pop();

        if (is_target(current)) {
            return distance;
        }

        // 遍歷所有可能的下一步 (Iterate through all possible next moves)
        for (auto& move : possible_moves) {
            State next = calculate_next_state(current, move);

            // 4. 定義入隊條件 (Define enqueuing condition)
            if (is_valid_transition(next) && !is_visited(next)) {
                mark_visited(next);
                q.push(next);
            }
        }
    }
    distance++;
}

return -1; // Target not reachable
```

---

## 🧩 類似題型範例

| 題目編號                                                 | 狀態空間設計 (State Space Design) | 核心挑戰                             |
| :------------------------------------------------------- | :-------------------------------- | :----------------------------------- |
| 1129. Shortest Path with Alternating Colors              | `(node, incoming_edge_color)`     | 邊的屬性 (顏色) 成為狀態的一部分     |
| 1293. Shortest Path in a Grid with Obstacles Elimination | `(r, c, remaining_k)`             | 資源消耗 (k) 成為狀態的一部分        |
| 864. Shortest Path to Get All Keys                       | `(r, c, keys_mask)`               | 狀態累積 (鑰匙) 改變可達性           |
| 847. Shortest Path Visiting All Nodes                    | `(current_node, visited_mask)`    | 訪問過的所有節點集合成為狀態的一部分 |
| 1368. Minimum Cost to Make at Least One Valid Path       | `(r, c)` (但用 0-1 BFS)           | 邊的權重不同，需用 Deque (0-1 BFS)   |
| 773. Sliding Puzzle                                      | `(board_string, zero_position)`   | 整個遊戲盤面成為狀態                 |
