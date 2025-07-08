# 二分搜尋實現分析：存在性、定位與重複值的深度探討

本文檔旨在深度分析不同的二分搜尋實現模式，重點剖析**搜索區間**與**循環終止條件**的選擇，如何影響算法在處理**存在性查找**、**精確位置定位**（如 `lower_bound`、`upper_bound`）以及**重複值**等場景下的行為與正確性。

---

## 模式一：標準元素搜索 (`while (left <= right)`)

此為最常見的二分搜尋模式，其主要目標是高效判斷特定元素是否存在於一個已排序的陣列中。

- **搜索區間:** `[0, size - 1]` (閉區間)
- **循環條件:** `while (left <= right)`
- **核心邏輯:** 只要搜索區間有效（`left` 不大於 `right`），循環便持續進行。每次迭代都會從兩端縮小搜索範圍。
- **區間收縮:** `right = mid - 1` 與 `left = mid + 1`
  - **原因:** 此模式的設計基於一個前提：當 `nums[mid]` 不等於 `target` 時，`mid` 這個索引**絕對不可能是答案**。因此，我們可以安全地將其從搜索區間 `[left, right]` 中徹底排除。透過 `mid - 1` 和 `mid + 1`，我們確保每次循環都至少縮小一個元素的搜索空間，從而保證循環最終必定會終止。

### 程式碼分析

```cpp
int binary_search(const vector<int>& nums, int target) {
    int left = 0;
    int right = nums.size() - 1;

    while (left <= right) {
        int mid = left + (right - left) / 2;
        if (nums[mid] == target) {
            // 找到目標。若存在重複值，這可能是其中任何一個。
            return mid;
        } else if (nums[mid] < target) {
            left = mid + 1;
        } else {
            right = mid - 1;
        }
    }
    // 未找到目標。
    // 此時 `left` 的值即為 `target` 的插入點。
    return -1; // 或可返回 `left` 作為插入點。
}
```

- **處理重複值:** 若 `target` 在陣列中多次出現，此演算法保證能找到其中一個，但無法保證是哪一個（例如，第一個或最後一個）。
- **處理未找到的情況:** 當循環因 `left > right` 而終止時，`left` 變數的值將恰好是 `target` 應該被插入以維持陣列排序的位置。這是一個非常有用的附加特性。

**結論:** 此模式非常穩健，是檢查元素**存在性**的理想選擇。

---

## 模式二：精確插入點定位 (`while (left < right)`)

此模式通常用於實現 `lower_bound` 或 `upper_bound`，其目標是找到一個精確的插入點，而非僅僅匹配一個元素。在此模式下，搜索區間的選擇至關重要。

### 關鍵設計選擇

1. **正確的搜索區間: `[0, size]`**

   - **原因:** 插入點完全有可能在所有元素之後，即索引 `size` 的位置。若搜索區間只到 `size - 1`，當 `target` 大於所有元素時，將無法得到正確的結果。將 `right` 初始化為 `size`，可將此邊界情況納入考量。

2. **循環條件: `while (left < right)`**

   - **原因:** 此條件使循環在 `left == right` 時終止，最終將搜索範圍縮小到單一的確定位置。

3. **區間收縮: `right = mid`**
   - **原因:** 在 `lower_bound` / `upper_bound` 的邏輯中，當我們捨棄右半邊時，`nums[mid]` 本身**仍有可能是我們尋找的答案**（例如，在 `lower_bound` 中，它可能是第一個 `>= target` 的元素）。因此，我們不能將 `mid` 排除，而是將搜索區間縮小到 `[left, mid]`，保留 `mid` 作為潛在的候選答案。
   - **避免無限循環:** 正是因為循環條件是 `left < right`，`right = mid` 才不會導致無限循環。當 `left` 和 `right` 相鄰時（例如 `left=2, right=3`），`mid` 會等於 `left`（`mid=2`）。若此時更新 `right = mid`，區間會縮小；若更新 `left = mid + 1`，區間也會縮小。這保證了循環的終止。

### `lower_bound` 實現 (尋找第一個 >= target 的位置)

```cpp
int lower_bound_search(const vector<int>& nums, int target) {
    int left = 0;
    int right = nums.size(); // 搜索區間 [0, size]

    while (left < right) {
        int mid = left + (right - left) / 2;
        if (nums[mid] >= target) {
          right = mid; // mid 可能是答案，不能排除
        } else {
          left = mid + 1;
        }
    }
    return left;
}
```

### `upper_bound` 實現 (尋找第一個 > target 的位置)

```cpp
int upper_bound_search(const vector<int>& nums, int target) {
    int left = 0;
    int right = nums.size(); // 搜索區間 [0, size]

    while (left < right) {
        int mid = left + (right - left) / 2;
        if (nums[mid] <= target) {
            left = mid + 1; // 往右找 > target 的位置
        } else {
            right = mid; // mid 可能是答案，不能排除
        }
    }
    return left;
}
```

如果要跟 lower_bound_search 格式對齊，可改用以下判斷：

```cpp
if (nums[mid] > target) { // 尋找第一個 > target
    right = mid; // mid 可能是答案，不能排除
} else {
    left = mid + 1; // 往右找 > target 的位置
}
```

### 邊界情況：當 Target 不存在時

你提出的觀點完全正確，這正是模式二的強大之處。

1. **`target` 比陣列中所有元素都小:**
   - 在每次迭代中，條件 `nums[mid] < target` (lower_bound) 或 `nums[mid] <= target` (upper_bound) 始終為 `false`。
   - 因此，`right` 會不斷地被更新為 `mid` (`right = mid`)。
   - `left` 始終保持為 `0`。
   - 循環最終在 `left == right == 0` 時終止，返回 `0`，即陣列的第一個位置，完全正確。

2. **`target` 比陣列中所有元素都大:**
   - 在每次迭代中，條件 `nums[mid] < target` (lower_bound) 或 `nums[mid] <= target` (upper_bound) 始終為 `true`。
   - 因此，`left` 會不斷地被更新為 `mid + 1`。
   - 最終 `left` 會被推到 `size`。
   - 循環最終在 `left == right == size` 時終止，返回 `size`，即陣列末尾之後的位置，也完全正確。

這個行為保證了 `lower_bound` 和 `upper_bound` 模式對於任何 `target` 值都能返回一個語義上正確的插入點。

---

## 深度探討：重複值的影響

這兩種模式在有重複值的情況下都能正常工作，其根本原因在於它們各自維護的**不變性 (Invariant)** 不同。

- **模式一 (`left <= right`) 的不變性:** 如果 `target` 存在，它一定在閉區間 `[left, right]` 內。重複值不違反陣列的非遞減性，因此三向比較 (`<`, `==`, `>`) 依然能正確地縮小絕對不包含答案的範圍。

- **模式二 (`left < right`) 的不變性:** 此模式旨在尋找一個**邊界**。它將陣列依條件劃分為兩部分（例如，`< target` 和 `>= target`）。`lower_bound` 的任務就是找到這個分界點。重複值只是意味著滿足條件的部分更長，但分界點的位置依然是唯一的，演算法的二分決策 (`< target` vs. `>= target`) 始終有效。

**結論：** 兩種模式都能處理重複值，因為它們的目標不同：一個是找**任意匹配**，另一個是找**精確邊界**。

---

## 核心要點與決策

### 1. 標準 `while (left <= right)` 模式 (主要用於查找)

- **核心權衡：** 這個模式**直接回答“存在性”**。
- **找到目標時：** 如果 `nums[mid] == target`，你立即知道 `target` 存在，並得到它的一個索引。但這個索引**不是**一個通用的“插入點”（例如 `lower_bound`）。
- **未找到目標時：** 當循環結束時 (`left > right`)，`left` 的值就是正確的插入點。

### 2. `lower_bound` / `upper_bound` 模式 (主要用於定位)

- **核心權衡：** 這個模式**總是返回一個精確的插入點**，但需要**額外一步**來確認“存在性”。
- **如何確認存在性：** 調用 `lower_bound` 後，需檢查返回的索引 `idx` 是否在範圍內 (`idx < nums.size()`) 且 `nums[idx] == target`。

## 最終決策

- **如果你的首要目標是檢查元素是否存在**，並且不關心是哪個副本或精確的插入位置，**模式一**是最直接、最高效的。
- **如果你的目標是找到一個可用於插入、計數或定義範圍的精確邊界**，那麼**模式二**是必須的，即使這意味著可能需要額外進行一次檢查來確認存在性。
