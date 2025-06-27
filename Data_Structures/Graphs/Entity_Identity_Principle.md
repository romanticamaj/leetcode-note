# 心法：實體身份原則 (Entity Identity Principle)

## 1. 核心思想

> **物件的屬性不等於其身份。在圖的遍歷中，必須使用唯一的識別符 (Identifier) 來追蹤每個實體 (Entity)，而不是依賴其屬性。**

在圖論問題中，我們將現實世界的物件（如炸彈、城市、任務）抽象為圖的節點 (vertex)。一個常見且隱蔽的陷阱是，僅僅因為兩個物件擁有完全相同的屬性（如座標、值、顏色），就將它們在 `visited` 集合中視為同一個節點。

**實體身份原則**強調，即使屬性完全相同，每個物件在邏輯上也應該是獨立的、唯一的實體。因此，我們必須使用一個與該實體永久綁定的、唯一的**識別符**——最常見的就是它在輸入陣列中的**索引 (index)**——來進行識別和追蹤。

---

## 2. 動機與典型場景

當你遇到以下情況時，必須應用此原則：

- **同屬性的多個物件**: 如「引爆最多的炸彈」問題，多個炸彈可能位於完全相同的位置 `(x, y)` 且半徑 `r` 也相同，但它們是不同的實體，可以被獨立引爆。
- **棋盤上的多個同種棋子**: 兩個「兵」在同一個格子，它們是不同的棋子，可以被分別吃掉。
- **系統中的多個相同任務**: 多個內容相同的任務實例可能在等待佇列中，它們需要被獨立調度。

**反思問題**: 「我的 `visited` 集合，是用**屬性**（如座標 `pair`）來記錄，還是用**唯一識別符**（如 `int` 索引）來記錄？」如果答案是前者，就需要警惕是否違反了此原則。

---

## 3. 設計策略與實作

### Principle 1: 以唯一識別符為節點 (Node as Identifier)

在腦中將圖的節點直接對應到每個實體的唯一識別符（通常是其陣列索引）。節點 `i` 就代表 `input_array[i]` 這個獨一無二的實體。

### Principle 2: `visited` 結構基於識別符

- **推薦**: 使用一個大小為 `N` 的布林陣列或集合，其中 `N` 是實體的總數。
  ```cpp
  // N 是炸彈的總數
  vector<bool> visited(N, false);
  ```
- **錯誤**: 使用一個儲存屬性的集合。
  ```cpp
  // ❌ 錯誤的設計：無法區分同座標的炸彈
  set<vector<int>> visited_by_property;
  ```

### Principle 3: 遍歷與判斷基於識別符

在主迴圈和遞迴函數中，傳遞和操作的都應該是實體的**唯一識別符**。

```cpp
// 主迴圈：從每個實體 i 開始一次新的遍歷
for (int i = 0; i < all_entities.size(); ++i) {
    vector<bool> visited(all_entities.size(), false);
    visited[i] = true;
    // ...
    dfs(all_entities, i, visited); // 傳遞實體的唯一識別符 i
}

// DFS 函數
int dfs(const vector<Entity>& all_entities, const int currentId, vector<bool>& visited) {
    // ...
    for (int nextId = 0; nextId < all_entities.size(); ++nextId) {
        if (visited[nextId]) continue;

        // 判斷實體 currentId 和實體 nextId 之間的關係
        if (are_connected(all_entities, currentId, nextId)) {
            visited[nextId] = true;
            // ...
        }
    }
    // ...
}
```

---

## 4. 違反原則的後果

- **錯誤去重 (Incorrect Deduplication)**: 將多個獨立的實體誤判為同一個，導致遍歷提前終止。
- **計數錯誤 (Counting Errors)**: 在「引爆最多的炸彈」這類問題中，會嚴重低估可引爆的總數。
- **邏輯混亂 (Logic Corruption)**: `visited` 集合失去了其應有的「防止重複處理同一實體」的功能。

## ✅ 總結

**實體身份原則**是處理「同屬性、多實體」圖問題的基石。它提醒我們，圖的節點是邏輯上的抽象，其唯一性應由我們賦予的**唯一識別符**來保證，而不是其物理或描述性的**屬性**。
