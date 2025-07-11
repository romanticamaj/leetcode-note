# 心法：回溯算法的通用模板與模式

## tl;dr: 核心思想

回溯法 (Backtracking) 是一種透過**遞迴**來系統性地探索問題所有可能解的演算法。

其精髓在於「**智能的窮舉**」：它不像單純的暴力窮舉會產生所有可能性，而是在探索過程中，一旦發現當前路徑**不可能**導向一個有效解，就會立即**放棄 (Pruning)** 這條路徑，並**退回 (Backtrack)** 到上一步，嘗試其他選擇。

---

## 回溯法 vs. 窮舉搜索

- **窮舉搜索 (Exhaustive Search)**：產生**所有**的可能性，然後逐一檢查它們是否為有效解。
- **回溯法 (Backtracking)**：在生成可能性的過程中，透過「剪枝 (Pruning)」來提前放棄那些不可能導向有效解的路徑，從而只生成一個大大縮小的、更有希望的可能性子集。

---

## 通用回溯模板

幾乎所有的回溯問題都可以用以下這個遞迴模板來解決。理解這個模板的「選擇、探索、撤銷」循環是掌握回溯法的關鍵。

```cpp
/**
 * @brief 通用回溯函式
 * @param path - 引用傳遞，記錄當前已構建的路徑
 * @param choices - 可用的選擇列表
 * @param results - 引用傳遞，儲存所有找到的有效解
 */
void backtrack(vector<T>& path, const vector<T>& choices, vector<vector<T>>& results) {
    // 1. 終止條件：當前路徑已滿足題目要求的完整解條件
    if (is_solution(path)) {
        results.push_back(path); // 找到一個解，加入結果集
        return;                  // 返回上一層，繼續搜索其他可能
    }

    // 2. 遍歷所有可能的選擇
    for (const auto& choice : choices) {
        // (可選) 剪枝：若當前選擇不合法或不可能導向有效解，則跳過
        if (!is_valid(path, choice)) {
            continue;
        }

        // 3. 做出選擇 (Choose)
        path.push_back(choice);

        // 4. 繼續探索 (Explore)：帶著更新後的路徑，進入下一層決策
        backtrack(path, choices, results);

        // 5. 撤銷選擇 (Unchoose)：將狀態恢復，以便 for 迴圈的下一次迭代能嘗試其他選擇
        path.pop_back();
    }
}
```

### 模板核心三部曲：Choose, Explore, Unchoose

- **Choose (做出選擇)**：從當前的可用選項中選擇一個，並更新你正在構建的解（例如，將一個數字加入列表）。
- **Explore (繼續探索)**：基於新的狀態，遞迴呼叫 `backtrack` 函式，深入到決策樹的下一層。
- **Unchoose (撤銷選擇)**：當從遞迴呼叫返回時，**必須**將狀態恢復原狀。這是回溯的精髓，它允許你探索完全不同的路徑。

### 決策樹視角 (The Decision Tree Analogy)

你可以將整個回溯過程想像成在一個「決策樹」上進行深度優先搜索 (DFS)。

- **樹的節點 (Node)**：每一次對 `backtrack` 函式的呼叫，都代表你正處於決策樹上的一個節點。
- **樹的邊 (Edge)**：`for` 迴圈中的每一次迭代，都代表從當前節點延伸出的一條邊，通往一個子節點。
- **向下探索 (Moving to a Child)**：在迴圈中遞迴呼叫 `backtrack`，相當於沿著一條邊移動到子節點。
- **向上回溯 (Backtracking)**：撤銷選擇 (`unmake_choice`) 的那一步，就是「回溯」的體現，相當於從子節點返回到其父節點。
- **根到葉的路徑 (Path from Root to Leaf)**：
  - 樹的**根節點**代表一個空的候選解，也就是你最初呼叫 `backtrack` 時的狀態。
  - 從根節點到任意節點的路徑，代表一個正在構建中的部分候選解。
  - 樹的**葉節點**代表搜索的終點，也就是觸發了終止條件（base case）的完整解。

### 狀態管理考量 (State Management Considerations)

在應用通用模板時，有幾個關於狀態 (`State`) 和選擇 (`Choices`) 的常見管理方式：

- **路徑 (Path)**：通常用一個 `vector` 或 `string` 來記錄當前正在構建的解。
- **選擇集 (Choices)**：可以是輸入的陣列本身，或是根據當前狀態動態生成的選項。
- **傳遞方式**：將路徑 `state` 以引用 (`&`) 方式傳遞可以提高效率，但要確保在遞迴返回後正確地「撤銷選擇」。如果以值傳遞，則無需手動撤銷，因為每一層遞迴都有自己的副本，但空間和時間開銷較大。

---

## 關鍵模式與變體

### 核心差異：組合 (Combinations) vs. 排列 (Permutations)

在深入探討模板之前，必須先理解兩者的根本區別：

- **組合 (Combinations)**：**順序不重要**。`[1, 2]` 和 `[2, 1]` 是同一個組合。
- **排列 (Permutations)**：**順序很重要**。`[1, 2]` 和 `[2, 1]` 是兩個不同的排列。

這個根本差異，決定了我們在遞迴中如何處理「可選的下一步」。

### 模式一：子集 (Subsets) / 組合 (Combinations)

這類問題的目標是找出所有可能的元素組合，因為順序不重要，所以我們需要避免產生重複的組合。

**模式關鍵**：**防止「向後看」**。為了避免重複，我們人為地規定一個選擇順序。一旦我們選擇了索引為 `i` 的元素，下一輪的選擇**只能從 `i` 之後的元素開始**。這就自然地排除了 `[2, 1]` 這種情況的出現，因為在選擇 `2` 之後，我們不能再回頭選擇 `1`。

**模板變體**：在遞迴呼叫中傳遞當前選擇的索引 `i`，並讓下一層的循環從 `i + 1` 開始。

```cpp
void findCombinations(vector<int>& path, int start, const vector<int>& candidates, vector<vector<int>>& results) {
    // 終止條件 (例如，達到特定長度)
    if (path.size() == k) {
        results.push_back(path);
        return;
    }

    // 從 start 開始遍歷，避免重複組合
    for (int i = start; i < candidates.size(); ++i) {
        path.push_back(candidates[i]);
        // 關鍵：傳入 i + 1 而不是 start + 1
        // 這確保了下一層遞迴的選擇，只會從當前選擇的元素 *之後* 開始。
        // 例如，如果 candidates = [1,2,3,4]，當前選擇了 2 (i=1)，
        // 下一層就只會從 3 (i=2) 開始考慮，從而避免了 [2,1] 這種重複組合。
        findCombinations(path, i + 1, candidates, results);
        path.pop_back();
    }
}
```

### 模式二：排列 (Permutations)

這類問題的目標是找出所有可能的元素排列，因為順序很重要，所以我們需要能夠在任何位置選擇任何**尚未被使用過**的元素。

**模式關鍵**：**允許「任意看」**，但要**避免「重複用」**。在任何一個決策點，我們都可以從**所有**元素中進行選擇，只要這個元素在**當前的排列路徑**中還沒有被使用過。這就需要一個 `visited` 陣列或類似的機制來追蹤當前路徑的狀態。

**模板變體**：使用一個 `visited` 陣列或類似的機制來標記已使用的元素。

```cpp
/**
 * @brief 尋找排列 (Permutations)
 * @param path - 當前正在構建的排列
 * @param nums - 原始數字（選擇列表）
 * @param visited - 標記哪些索引的數字已被使用
 * @param results - 儲存所有排列結果
 */
void findPermutations(vector<int>& path, const vector<int>& nums, vector<bool>& visited, vector<vector<int>>& results) {
    // 終止條件：當前排列的長度等於原始陣列長度
    if (path.size() == nums.size()) {
        results.push_back(path);
        return;
    }

    // 每次都從頭開始遍歷**所有**數字，尋找一個「未使用」的數字
    for (int i = 0; i < nums.size(); ++i) {
        // 如果 nums[i] 已經在當前路徑中，則跳過
        if (visited[i]) {
            continue;
        }

        // Choose: 選擇 nums[i]，並標記為已使用
        path.push_back(nums[i]);
        visited[i] = true;

        // Explore: 繼續尋找下一個元素
        findPermutations(path, nums, visited, results);

        // Unchoose: 回溯，撤銷選擇，將狀態恢復
        visited[i] = false;
        path.pop_back();
    }
}
```

### 模式三：帶有約束條件的搜索 (Constraint-Based Pruning)

許多問題（如 N-皇后、數獨）都屬於此類。它們不僅要求找到解，還要求解必須滿足一系列複雜的約束。

**模式關鍵**：在「做出選擇」之前，先進行一次**剪枝判斷**。如果一個選擇會立即違反約束，就根本不考慮它。

**模板變體**：在循環內部、做出選擇之前，增加一個 `is_valid` 的檢查。

```cpp
/**
 * @brief 帶有約束剪枝的回溯模板
 * @param state - 代表問題的當前狀態，例如棋盤
 * @param choices - 當前狀態下的可用選擇
 * @param results - 儲存所有找到的解
 */
void solveWithConstraints(State& state, Choices& choices, Results& results) {
    // 終止條件：當前狀態已是一個完整解
    if (is_solution(state)) {
        results.push_back(state);
        return;
    }

    // 遍歷所有可能的選擇
    for (const auto& choice : get_available_choices(state, choices)) {
        // 剪枝：在做出選擇前，先判斷此選擇是否會違反問題的約束條件
        if (is_valid_choice(state, choice)) {

            // Choose: 應用選擇
            make_choice(state, choice);

            // Explore: 繼續探索
            solveWithConstraints(state, choices, results);

            // Unchoose: 撤銷選擇，恢復狀態
            unmake_choice(state, choice);
        }
    }
}
```
