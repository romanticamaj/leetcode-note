# Swap 作為通用 Backtracking 狀態操作心法

`swap` 技巧是回溯法中一種極致的空間優化，它用「隱性的分區管理」替代了「顯性的狀態標記」。理解其本質，能讓我們在處理排列組合等問題時，寫出更優雅、更高效的程式碼。

---

## 1. `swap` 技巧的核心思想

### 本質：一步到位的狀態轉換

> **Swap 是一種在固定位置與候選元素交換，藉此「標記狀態 + 移除候選 + 原地建構」，並在回溯時透過再次 swap 來還原現場的技巧。**

很多 backtracking 都要同時做三件事：

1. **標記「這個元素被使用了」** (傳統方法：用 `used[]`)
2. **把它放到「已選集合」裡** (傳統方法：`path.push_back()`)
3. **讓下一層遞迴不再考慮它** (傳統方法：維護「剩餘候選」)

而 **`swap`** 將這三件事合而為一：把它交換到固定 `index`，等於「放入已選集合」，同時將其排除在「待選區間」之外。回溯時 `swap` 回去，完美地「撤銷選擇」。

### `swap` 的三重意義

1. **視覺上 (Partitioning)**：將陣列劃分為 `[0...index-1]` 的「已決策區」和 `[index...n-1]` 的「待決策區」。
2. **語意上 (Selection)**：`swap` 的動作，是將一個未決元素放到 `index` 位置，使其成為「已決定」的一部分。
3. **操作上 (Efficiency)**：`swap` 是 `O(1)` 操作，極大地節省了時間和空間。

---

## 2. 案例分析：從 `visited` 到 `swap` 的演進

要真正理解 `swap` 技巧，最好的方式是看它是如何從更直觀的 `visited` 陣列方法演進而來的。

### 兩種排列 (Permutation) 的實現回顧

#### 解法 A：使用 `visited` 陣列 (顯性標記)

- **核心思想**：使用 `visited` 陣列**標記**原陣列中哪些**索引**的元素已被使用。
- **空間複雜度**：`O(N)`

```cpp
/**
 * @brief 使用 visited 陣列生成排列
 * @param nums 原始的選擇列表
 * @param path 當前正在構建的排列路徑
 * @param visited 標記 nums 中對應索引的元素是否已被使用
 * @param results 儲存所有找到的完整排列
 */
void backtrack_visited(const vector<int>& nums, vector<int>& path, vector<bool>& visited, vector<vector<int>>& results) {
    // 終止條件：當前路徑的長度等於原始陣列長度，表示一個完整的排列已產生
    if (path.size() == nums.size()) {
        results.push_back(path);
        return;
    }

    // 遍歷所有可能的選擇（從頭開始掃描原始陣列）
    for (int i = 0; i < nums.size(); ++i) {
        // 如果當前索引的元素已經在路徑中，則跳過
        if (visited[i]) {
            continue;
        }

        // Choose: 做出選擇
        path.push_back(nums[i]); // 1. 將元素加入路徑
        visited[i] = true;       // 2. 標記為已使用

        // Explore: 繼續向下探索
        backtrack_visited(nums, path, visited, results);

        // Unchoose: 撤銷選擇 (回溯)
        visited[i] = false;      // 1. 取消標記
        path.pop_back();         // 2. 從路徑中移除元素
    }
}
```

#### 解法 B：使用 `swap` 技巧 (隱性分區)

- **核心思想**：直接在原陣列上操作，透過**交換**將「待選元素」放到當前要決定的位置上。
- **空間複雜度**：`O(1)`

```cpp
/**
 * @brief 使用 swap 技巧生成排列
 * @param nums 既是選擇列表，也是當前正在構建的排列
 * @param index 當前要決定的位置 (也是「已決策區」和「待決策區」的分界)
 * @param results 儲存所有找到的完整排列
 */
void backtrack_swap(vector<int>& nums, int index, vector<vector<int>>& results) {
    // 終止條件：當要決定的位置越界時，表示一個完整的排列已在 nums 中形成
    if (index == nums.size()) {
        results.push_back(nums);
        return;
    }

    // 遍歷「待決策區」[index, n-1]，為 index 位置選擇一個元素
    for (int i = index; i < nums.size(); ++i) {
        // Choose: 將第 i 個元素換到 index 位置，代表選擇它作為當前位置的數字
        swap(nums[index], nums[i]);

        // Explore: 處理下一個位置
        backtrack_swap(nums, index + 1, results);

        // Unchoose: 換回來，恢復陣列狀態，以便 for 迴圈下一次迭代
        swap(nums[index], nums[i]);
    }
}
```

### 思維過渡：從「標記」到「分區」

從 `visited` 版本進化到 `swap` 版本的關鍵，是將思維模式從 **「標記已用元素」** 轉換為 **「對陣列進行分區」**。

- **`visited` 版本的思維**：`nums` 陣列不變，我們用一個外部的 `visited` 帳本來記錄用過了誰。`for` 迴圈每次都從頭掃描，問：「第 `i` 個元素用過了嗎？」
- **`swap` 版本的思維**：沒有額外的帳本。`index` 變數將 `nums` 陣列劃分為「已決策區」`[0, index-1]` 和「待決策區」`[index, n-1]`。`for` 迴圈的迭代是在做一個動作：
  > 「從『待決策區』中，挑選第 `i` 個元素，把它**交換**到『當前決策點』(`index`) 上，然後去處理下一個決策點 `index + 1`。」

### 為什麼這不是組合 (Combination)

在**組合**問題中，`for (int i = start_index; ...)` 的目的是**防止向後看**，因為 `[1, 2]` 和 `[2, 1]` 是同一個解。

但在**`swap` 排列**中，`swap` 操作**徹底改變了陣列的狀態**。假設 `nums = [1, 2, 3]`，在 `index=0` 時，當 `i=1`，`swap(nums[0], nums[1])` 使陣列變為 `[2, 1, 3]`。在下一層遞迴中，元素 `1` 位於「待決策區」，**它仍然是可選的**。這證明了它並不是「不向後看」，而是透過動態地維護「待決策」集合來確保所有排列都能被生成。

---

## 3. 決策指南與適用場景

### 與其他方法的比較

| 方法          | 特點                    | 空間複雜度 (額外) |
| :------------ | :---------------------- | :---------------- |
| call by value | 簡單，但每層複製容器    | `O(N^2)`          |
| `used[]`      | 額外 array 追蹤使用情況 | `O(N)`            |
| `swap`        | 原地操作，最節省空間    | `O(1)`            |

### `swap` 適用的場景

凡是需要：

- 把元素「移出候選集合」。
- 同時「在原集合中標記位置」。
- 在回溯時「完全還原現場」。

都可以考慮 `swap`。
例如：**全排列 (Permutations)**、**N 皇后 (N-Queens)**、**Next Permutation**。

---

## 4. 總結與練習

### 心法口訣

**「swap = 放置 + 標記/移除 + 還原」**

讓我們用一個例子來詳細拆解這個過程。假設 `nums = [1, 2, 3]`，當前遞迴在 `index = 0`，`for` 迴圈進行到 `i = 1`。

1. **放置 (Placement)**

   - **動作**：執行 `swap(nums[0], nums[1])`，`nums` 變為 `[2, 1, 3]`。
   - **意義**：將「待決策區」的元素 `2` **放置**到了「當前決策點」`index = 0` 上。

2. **標記 (Marking) & 移除 (Removal)**

   - **動作**：遞迴呼叫 `backtrack_swap(nums, index + 1, ...)`。
   - **意義**：透過將 `index` 向前推進，我們隱性地**標記**了 `2` 為已用，並將其從下一層的「待決策區」中**移除**。

3. **還原 (Restoration)**
   - **動作**：遞迴返回後，執行第二次 `swap(nums[0], nums[1])`，`nums` 恢復為 `[1, 2, 3]`。
   - **意義**：將狀態**還原**，以便 `for` 迴圈的下一次迭代可以從乾淨的狀態開始。

### 鞏固練習

試著問自己：

> **能否透過 swap + index，原地管理「待決策」的候選元素？**

如果可以，就能用這種 in-place 狀態管理技巧來優化空間。
