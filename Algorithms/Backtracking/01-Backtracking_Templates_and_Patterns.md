# 心法：回溯算法的通用模板與模式

## tl;dr: 核心思想

回溯法 (Backtracking) 是一種透過**遞迴**來系統性地探索問題所有可能解的演算法。其精髓在於「**智能的窮舉**」：它在探索過程中，一旦發現當前路徑不可能導向一個有效解，就會立即**放棄 (Pruning)** 這條路徑，並**退回 (Backtrack)** 到上一步，嘗試其他選擇。

---

## 1. 通用回溯模板與視角

### 基本模板

幾乎所有的回溯問題都可以用以下這個「選擇、探索、撤銷」的遞迴模板來解決。

```cpp
/**
 * @brief 通用回溯函式
 * @param path 當前正在構建的路徑 (狀態)
 * @param choices 所有可用的選擇
 * @param results 儲存所有找到的有效解
 */
void backtrack(const Choices& choices, State& path, Results& results) {
    // --- 收集解的兩種時機 (根據問題選擇一種) ---

    // 時機 A：解在葉節點 (例如：組合、排列)
    // 當前路徑已構成一個完整解
    if (is_solution(path)) {
        results.add(path);
        return; // 找到葉節點解後，通常可以直接返回
    }

    // 時機 B：解在所有節點 (例如：子集)
    // 每個中間路徑都是一個合法的解
    results.add(path); // 會在迴圈前加入

    // --- (以上二選一，或都不選，取決於問題定義) ---

    // 遍歷所有可能的選擇
    for (const auto& choice : get_available_choices(choices, path)) {
        // (可選) 剪枝：若當前選擇不合法，則跳過
        if (!is_valid(choice, path)) {
            continue;
        }

        // 核心三部曲
        make_choice(choice, path);      // 1. Choose
        backtrack(choices, path, results); // 2. Explore
        unmake_choice(choice, path);    // 3. Unchoose
    }
}
```

### 決策樹視角 (The Decision Tree Analogy)

你可以將整個回溯過程想像成在一個「決策樹」上進行深度優先搜索 (DFS)。

- **節點 (Node)**：每一次對 `backtrack` 函式的呼叫。(同 State-Space Tree，對應當前的 `State`)
- **路徑 (Path)**：從根節點到當前節點的路徑，代表一個正在構建中的部分解。
- **向下探索 (Explore)**：遞迴呼叫 `backtrack`，深入下一層。
- **向上回溯 (Unchoose)**：撤銷選擇，從遞迴中返回，回到父節點。

---

## 2. 關鍵模式：根據「解」在決策樹的位置區分

我們可以根據「有效解」存在於決策樹的哪個位置，來對回溯問題進行分類。

### 模式 A：解在葉節點 (Solutions are at the Leaf Nodes)

在這類問題中，一個部分解 `path` 只有在它無法再繼續延伸時（即到達決策樹的葉節點），才是一個完整解。這通常意味著 `path` 達到了特定長度或滿足了某個終止條件。

#### 子模式 A.1：組合 (Combinations)

- **實現關鍵**：**防止「向後看」**。透過傳遞 `index` 索引，並在遞迴中呼叫 `i + 1`，來強制選擇的順序性，從而避免產生重複的組合（如 `[1, 2]` 和 `[2, 1]`）。

```cpp
void generateCombinations(const ChoicesType& choices, const int k, const int index, PathType& path, ResultsType& results) {
    // 終止條件：當前組合的長度已達到 k
    if (path.size() == k) {
        results.push_back(path);
        return;
    }

    // 從 index 開始遍歷，避免重複
    for (int i = index; i < choices.size(); ++i) {
        path.push_back(choices[i]);

        // 關鍵：傳入 i + 1，下一輪選擇只能從 i 的右邊開始
        generateCombinations(choices, k, i + 1, path, results);

        path.pop_back(); // 回溯
    }
}
```

#### 子模式 A.2：排列 (Permutations)

- **實現關鍵**：**允許「任意看」，但要避免「重複用」**。需要一個 `visited` 陣列來追蹤哪些元素已在當前路徑中。

```cpp
void generatePermutations(const ChoicesType& choices, VisitedType& visited, PathType& path, ResultsType& results) {
    // 終止條件：當前排列的長度等於總元素數
    if (path.size() == choices.size()) {
        results.push_back(path);
        return;
    }

    // 每次都從頭掃描，但用 visited 陣列跳過已用過的元素
    for (int i = 0; i < choices.size(); ++i) {
        if (visited[i]) continue; // 不重複選取

        path.push_back(choices[i]);
        visited[i] = true;

        generatePermutations(path, choices, visited, results);

        visited[i] = false;
        path.pop_back();
    }
}
```

> **進階技巧**：對於排列問題，還有一種更高效、空間複雜度為 O(1) 的**原地交換 (In-place Swap)** 技巧，它透過直接修改輸入陣列來管理狀態，無需額外的 `visited` 陣列。詳細解釋請參閱：[`Swap_as_In_Place_State_Management.md`](./Swap_as_In_Place_State_Management.md)。

### 模式 B：解在所有節點 (Solutions are at Every Node)

在這類問題中（最經典的是**所有子集 Power Set**），決策樹上的**每一個節點**本身就代表一個有效的解。

- **實現關鍵**：將「收集解」的動作放在遞迴函式的**入口處**，概念上等同於 DFS 遍歷中的 `visit(node)` 操作。

```cpp
void generateSubsets(const ChoicesType& choices, const int index, PathType& path, ResultsType& results) {
    // 關鍵：在遞迴入口，立即將當前路徑視為一個解並收集
    results.push_back(path);

    // 遍歷後續選擇，構建更長的子集
    for (int i = index; i < choices.size(); ++i) {
        path.push_back(choices[i]);

        generateSubsets(choices, i + 1, path, results); // 不重複選取

        path.pop_back();
    }
}
```

> **隱式終止條件**：你可能會注意到 `generateSubsets` 函式沒有像 模式 A 那樣的顯式 `if` 終止條件。這是因為遞迴的終止是**隱式**地由 `for` 迴圈處理的。當 `index` 索引越過 `choices` 的邊界時，`for (int i = index; ...)` 迴圈將不會執行，遞迴自然終止並返回。

---

## 3. 通用優化技巧：約束剪枝 (Constraint-Based Pruning)

剪枝是一個**正交**於上述模式的概念，它可以應用於任何一種模式中，其目標是在「做出選擇」之前，增加一個基於**問題特定約束**的判斷 (`is_valid`)，提前砍掉無效的決策分支。

> 💡 `is_valid_choice` 該寫什麼條件，不需要猜——**先寫下不變量，guard 從「加完之後不變量還成立嗎」倒推**，終止條件則是「不變量飽和」。見 [07-Guards_from_Invariants.md](07-Guards_from_Invariants.md)。

```cpp
void solveWithConstraints(State& state, ...) {
    // ... (根據問題，可能在入口或終止條件處收集解)

    for (const auto& choice : get_available_choices(state)) {
        // 剪枝：在深入探索前，判斷此選擇是否會違反問題的約束
        if (!is_valid_choice(state, choice)) continue;

        make_choice(state, choice);

        solveWithConstraints(state, ...);

        unmake_choice(state, choice);
    }
}
```

---

## 4. 關鍵心法：從解題經驗總結 (Key Takeaways from Experience)

### 4.1 狀態設計是核心 (State Design is Key)

回溯法的成敗往往取決於**狀態 (State)** 的設計。一個好的狀態設計應該能精確地捕捉解決問題所需的所有資訊，例如：

- 當前構建的路徑 (`path`)
- 哪些元素已被使用 (`visited` map)
- 當前遞迴的深度或索引 (`index`)
- 其他與問題約束相關的變數（如 `currentSum`）

### 4.2 剪枝優化的關鍵：O(1) 的 `promising` 檢查

回溯法的效能優化主要來自於**剪枝 (Pruning)**。最有效的剪枝策略是設計一個 `promising()` 或 `is_valid()` 檢查，其時間複雜度應為 **O(1)**。

- **提前思考 `used` 集合**：在開始寫程式碼前，就應該規劃好如何追蹤「已使用」的元素或狀態。這通常是透過一個 hash map/set (`unordered_map`, `unordered_set`) 或布林陣列 (`vector<bool>`) 來實現。
- **簡潔的程式碼**：一個設計良好的 `used` 集合不僅能帶來 O(1) 的檢查效率，通常也會讓剪枝部分的邏輯變得非常簡潔明瞭。

### 4.3 狀態壓縮：用位元運算優化 `used` 集合

當可選元素的數量不多時（例如 N <= 20），可以用**位元運算 (Bit Manipulation)** 來優化空間使用和存取速度。

- **用一個整數代表 `used` 集合**：一個 32 位元的整數可以表示一個大小為 32 的布林陣列。整數的第 `i` 位元為 1 代表第 `i` 個元素已被使用，為 0 則代表尚未使用。
- **操作**：
  - 檢查第 `i` 個元素是否已用：`(mask & (1 << i)) != 0`
  - 標記第 `i` 個元素為已用：`mask |= (1 << i)`
  - 取消標記：`mask &= ~(1 << i)`

這種方法稱為**狀態壓縮 (State Compression)**，能極大地提升效能，特別是在狀態空間龐大的問題中。

### 4.4 State Transition Constraints 的陣列編碼

當問題涉及**狀態轉換的限制條件**（例如：從狀態 A 能否跳到狀態 B），將規則**預先編碼到陣列**中，使 `is_valid()` 檢查達到 O(1)。

**核心技巧：Constraint Matrix**

```cpp
// 預處理：編碼「從 from 到 to 需要什麼條件」
vector<vector<int>> skip(10, vector<int>(10, 0));
skip[1][3] = skip[3][1] = 2;  // 1↔3 需經過 2
skip[1][7] = skip[7][1] = 4;  // 1↔7 需經過 4
skip[1][9] = skip[9][1] = 5;  // 1↔9 需經過 5
// ...

// 使用：O(1) 的 promising 檢查
for (int to = 1; to <= 9; to++) {
    if (used[to]) continue;

    int skipNumber = skip[from][to];
    if (skipNumber != 0 && !used[skipNumber]) continue;  // 違反限制

    // 這是有效的移動
}
```

**優勢**：O(1) 查詢、規則與邏輯分離、易維護

**適用場景**：圖/網格移動限制、狀態機轉換規則、遊戲規則編碼

> **心法**：State transition 的限制條件可以用陣列來表示，避免複雜的 if-else 判斷。
