# 心法：以 `std::vector` 為核心的回溯策略：原地建構 vs. 輔助空間

當我們使用 `std::vector` 來解決回溯問題時，最關鍵的設計抉擇往往歸結為一個問題：**我們能否在原始 `vector` 上「原地 (in-place)」建構出解，還是必須使用一個額外的 `vector` 作為「路徑 (path)」來輔助建構？**

這個決策深刻影響了演算法的空間複雜度、實作複雜性以及我們對問題的思考方式。

---

## 1. 排列 (Permutations) on `std::vector`

排列的本質是**重新排列 `vector` 中元素的順序**。這意味著解的結構與輸入 `vector` 息息相關，為原地操作提供了可能性。

### 1.1 全長排列 (k=n, 不重複): 原地 `swap` 的黃金標準

- **核心情境**：找出 `vector` 的所有全長排列 (e.g., LeetCode 46)。
- **能否 In-place?**：**可以**。這是 `swap` 技巧最經典、最高效的應用場景。
- **運作原理**：解與輸入是同構的（元素、長度均相同）。因此，我們可直接修改輸入 `vector`，用 `index` 指標將其劃分為 `[0, index-1]` (已定區) 和 `[index, n-1]` (待選區)。`swap` 操作的本質是在「待選區」中為當前 `index` 挑選一個元素，從而實現了狀態的轉換，且無需 `O(N)` 的 `visited` 陣列。

```cpp
void permute_full_inplace(vector<int>& nums, int index, vector<vector<int>>& results) {
    if (index == nums.size()) {
        results.push_back(nums); // 此時的 nums 本身就是一個完整的解
        return;
    }
    // 從「待選區」[index, n-1] 中選擇一個元素放到 index 位置
    for (int i = index; i < nums.size(); ++i) {
        swap(nums[index], nums[i]);
        permute_full_inplace(nums, index + 1, results);
        swap(nums[index], nums[i]); // 回溯，恢復狀態供下一輪迴圈使用
    }
}
```

### 1.2 k-長度排列 (k<n, 不重複): `swap` 的適應與權衡

當只需找出長度為 `k` 的排列時，情況變得更加微妙。

#### 策略 A: 適應性原地 `swap` (Adapted In-place)

- **核心思想**：`swap` 的狀態管理邏輯不變，但終止條件和解的收集方式需要調整。
- **能否 In-place?**：**狀態管理是 In-place 的**，省去了 `visited` 陣列的 `O(N)` 空間。但**收集解時仍需 `O(k)` 空間**來建立一個新的 `vector`。
- **運作原理**：當遞迴深度 `index` 達到 `k` 時，「已定區」`nums[0...k-1]` 就構成了一個有效的 k-排列。我們只需複製這部分前綴即可。

```cpp
void permute_k_inplace_adapted(vector<int>& nums, int index, int k, vector<vector<int>>& results) {
    if (index == k) {
        results.emplace_back(nums.begin(), nums.begin() + k); // 複製前 k 個元素作為解
        return;
    }
    for (int i = index; i < nums.size(); ++i) {
        swap(nums[index], nums[i]);
        permute_k_inplace_adapted(nums, index + 1, k, results);
        swap(nums[index], nums[i]);
    }
}
```

#### 策略 B: 輔助 `path` 向量 + `visited` 陣列

- **核心思想**：一個更傳統、概念上更直接的作法。`path` 向量專門負責建構解，`visited` 陣列專門負責追蹤狀態，職責分離。
- **權衡**：此方法需要 `O(N)` 的 `visited` 陣列和 `O(k)` 的 `path` 向量，空間開銷較大，但邏輯可能更清晰：`path` 的大小就是遞迴深度。

```cpp
void permute_k_aux_space(vector<int>& path, const vector<int>& nums, vector<bool>& visited, int k, vector<vector<int>>& results) {
    if (path.size() == k) {
        results.push_back(path);
        return;
    }
    for (int i = 0; i < nums.size(); ++i) {
        if (visited[i]) continue;
        visited[i] = true;
        path.push_back(nums[i]);
        permute_k_aux_space(path, nums, visited, k, results);
        path.pop_back();
        visited[i] = false;
    }
}
```

### 1.3 可重複排列: `swap` 模型的失效

- **核心思想：模型不匹配 (Model Mismatch)**
- **In-place 為何不可行**：`swap` 技巧的心智模型是**分割** `vector` 為「已定區」和不斷縮小的「待選區」。然而，「可重複選取」問題的本質是，**選擇池（candidates）永遠是完整的原始 `vector`**，它從不縮小。這兩種模型從根本上是**不相容**的。
- **`vector` 策略**：必須將「候選人池 (`nums`)」和「正在建構的路徑 (`path`)」明確分開。`path` 向量作為輔助空間，獨立地記錄當前的排列，而 `nums` 則作為一個永遠不變的、完整的候選人列表。

```cpp
void permute_k_with_replacement(vector<int>& path, const vector<int>& nums, int k, vector<vector<int>>& results) {
    if (path.size() == k) {
        results.push_back(path);
        return;
    }
    // 每次都從完整的候選者中選擇
    for (int i = 0; i < nums.size(); ++i) {
        path.push_back(nums[i]);
        permute_k_with_replacement(path, nums, k, results);
        path.pop_back();
    }
}
```

---

## 2. 組合 (Combinations) on `std::vector`

組合的本質是從 `vector` 中**挑選一部分元素**，順序無關。

### 2.1 普遍原則：組合問題無法 In-place

- **核心思想**：一個組合是原始 `vector` 的一個**子集**。解的長度、甚至元素都可能與輸入不同。你無法在原始 `vector` 內部建構出一個長度不一的子集而稱之為 "in-place"。
- **能否 In-place?**：**不可以**。所有組合問題都需要一個輔助的 `path` 向量來建構解。

### 2.2 核心策略：以 `start` 索引避免重複

既然必須使用輔助空間，組合問題的關鍵就變成了**如何高效地避免重複組合**（如 `[1,2]` 和 `[2,1]`）。`std::vector` 的循序存取特性完美地配合了 `start` 索引策略。

#### A. 不可重複取元素的組合 (e.g., Subsets, Combinations)

- **`vector` 策略**：遞迴時傳入 `i + 1`。這確保了下一個元素的選擇**永遠在當前元素的右邊**，從根本上杜絕了因順序不同而產生的重複解。

```cpp
// LeetCode 77. Combinations
void combine_k_unique(vector<int>& path, int k, int start, const vector<int>& nums, vector<vector<int>>& results) {
    if (path.size() == k) {
        results.push_back(path);
        return;
    }
    // 關鍵：從 start 開始，遞迴傳入 i + 1
    for (int i = start; i < nums.size(); ++i) {
        path.push_back(nums[i]);
        combine_k_unique(path, k, i + 1, nums, results);
        path.pop_back();
    }
}
```

#### B. 可重複取元素的組合

- **`vector` 策略**：遞迴時傳入 `i` 而不是 `i+1`。這允許演算法在下一層遞迴中**重新選擇當前元素**，從而實現了元素的重複使用。
- **通用模板**：下面的模板產生長度為 `k` 的、可重複元素的組合。這個模式可以輕易地修改，將終止條件從 `path.size() == k` 改為其他約束，例如 `target == 0`（如 LeetCode 39. Combination Sum）。

```cpp
// 通用模板：尋找長度為 k 的、可重複元素的組合
void combine_k_with_replacement(vector<int>& path, int k, int start, const vector<int>& nums, vector<vector<int>>& results) {
    // 終止條件：路徑長度已達到 k
    if (path.size() == k) {
        results.push_back(path);
        return;
    }

    // 剪枝：如果路徑長度加上剩餘可選的元素數量（即使全部重複選也無法湊夠k），則可以提前終止
    // 這裡的剪枝比較tricky，因為可以重複選，一個簡單的剪枝是 if (start >= nums.size()) return;
    // 但 for 迴圈本身會處理這種情況，所以可以省略。

    // 從 start 開始遍歷
    for (int i = start; i < nums.size(); ++i) {
        path.push_back(nums[i]);
        // 關鍵：遞迴時傳入 i，允許重複選取同一個數字
        combine_k_with_replacement(path, k, i, nums, results);
        path.pop_back(); // 回溯
    }
}
```

---

## 總結

最終，選擇何種策略取決於問題的內在約束。

| 問題類型                | 能否 In-place on `vector`? | `vector` 核心策略                                                |
| :---------------------- | :------------------------- | :--------------------------------------------------------------- |
| **全長排列 (不重複)**   | **是**                     | `swap(nums[index], nums[i])`                                     |
| **k-長度排列 (不重複)** | **狀態管理 In-place**      | `swap` + 複製前 k 個元素 (策略 A) 或 `path` + `visited` (策略 B) |
| **排列 (可重複)**       | 否                         | `path` 向量                                                      |
| **組合 (不重複)**       | 否                         | `path` 向量 + `start` 索引 (`i+1`)                               |
| **組合 (可重複)**       | 否                         | `path` 向量 + `start` 索引 (`i`)                                 |
