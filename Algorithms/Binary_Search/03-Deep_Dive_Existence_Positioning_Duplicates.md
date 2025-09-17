# 二分搜尋實現分析：存在性、定位與重複值的深度探討

本文檔旨在深度分析不同的二分搜尋實現模式，重點剖析**搜索區間**與**循環終止條件**的選擇，如何影響算法在處理**存在性查找**、**精確位置定位**（如 `lower_bound`、`upper_bound`）以及**重複值**等場景下的行為與正確性。

---

## 核心模式比較

二分搜尋主要有兩種核心實現模式，它們的選擇取決於你的主要目標：

1. **模式一 (`while (left <= right)`)**: 主要用於**存在性檢查**。目標是快速判斷一個元素是否存在，如果存在，返回其任意一個位置。
2. **模式二 (`while (left < right)`)**: 主要用於**精確邊界定位**。目標是找到一個精確的插入點，如 `lower_bound`（第一個大於或等於目標的位置）或 `upper_bound`（第一個嚴格大於目標的位置）。

接下來，我們將深入探討這兩種模式的細節與應用。

---

## 模式一：標準存在性搜索 (`while (left <= right)`)

此為最常見的二分搜尋模式，其主要目標是高效判斷特定元素是否存在於一個已排序的陣列中。

- **搜索區間:** `[0, size - 1]` (閉區間)
- **循環條件:** `while (left <= right)`
- **核心邏輯:** 只要搜索區間有效（`left` 不大於 `right`），循環便持續進行。
- **區間收縮:** `right = mid - 1` 與 `left = mid + 1`
  - **原因:** 當 `nums[mid]` 不等於 `target` 時，`mid` 這個索引**絕對不可能是答案**。因此，我們可以安全地將其從搜索區間中徹底排除(-1 或 +1 離開 `mid`)，保證循環必定會終止。

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
    // 未找到目標。此時 `left` 的值即為 `target` 的插入點。
    return -1;
}
```

- **結論:** 此模式非常穩健，是檢查元素**存在性**的理想選擇。若 `target` 重複，它會返回任意一個匹配項。

---

## 模式二：精確邊界定位 (`while (left < right)`)

此模式通常用於實現 `lower_bound` 或 `upper_bound`，其目標是找到一個精確的插入點。

### 關鍵設計選擇

1. **搜索區間: `[0, size]`**: `right` 必須初始化為 `size`，因為插入點可能在所有元素之後。
2. **循環條件: `while (left < right)`**: 循環在 `left == right` 時終止，將範圍縮小到單一的確定位置。
3. **區間收縮: `right = mid`**: 當 `nums[mid]` 可能是答案時（例如在 `lower_bound` 中），我們不能排除 `mid`，只能將右邊界縮小到 `mid`。這保證了不會錯過邊界上的答案。

### `lower_bound` 實現 (尋找第一個 >= target 的位置)

```cpp
int lower_bound_search(const vector<int>& nums, int target) {
    int left = 0;
    int right = nums.size();

    while (left < right) {
        int mid = left + (right - left) / 2;

        if (nums[mid] >= target) {
          right = mid;
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
    int right = nums.size();

    while (left < right) {
        int mid = left + (right - left) / 2;

        if (nums[mid] > target) {
            right = mid;
        } else {
            left = mid + 1;
        }
    }

    return left;
}
```

---

## 應用與進階探討

### 組合應用：尋找元素的起始與結束範圍

`lower_bound` 和 `upper_bound` 的真正威力在於它們的組合，這能讓我們在 `O(log n)` 時間內解決複雜的範圍查詢問題。

#### 步驟一：使用 `lower_bound` 尋找起始位置

`lower_bound` 返回**第一個** `>= target` 的位置。找到後，我們必須進行一次**關鍵檢查**來確認 `target` 是否真的存在。

```cpp
// 執行 lower_bound 後，得到 left...

// 關鍵檢查：
// 1. 檢查 left 是否越界 (當 target 比所有元素都大時)
// 2. 檢查該位置的值是否真的是 target
if (left == nums.size() || nums[left] != target) {
    // target 不存在
    return -1;
}
// 如果檢查通過，left 就是 target 的起始位置
return left;
```

#### 步驟二：使用 `upper_bound` 尋找結束位置

`upper_bound` 返回第一個 `> target` 的位置。這個結果有多種用途：

- 用途 A：尋找 `target` 的**最後一個**出現位置

  ```cpp
  // 執行 upper_bound 後，得到 left...
  // target 的最後一個位置是 left 的前一個位置
  int last_pos = left - 1;

  // 關鍵檢查：
  // 1. 檢查索引是否有效 (當 target 比所有元素都小時)
  // 2. 檢查該位置的值是否真的是 target
  if (last_pos < 0 || nums[last_pos] != target) {
      // target 不存在
      return -1;
  }
  return last_pos;
  ```

- 用途 B：尋找 `> target` 的**第一個**元素位置

  ```cpp
  // 執行 upper_bound 後，得到 left...
  return left;
  ```

### 邊界案例分析：空陣列的優雅處理

一個設計良好的模式二實現，其循環後的檢查邏輯已經能**完美地處理空陣列**，無需額外的 `if (nums.empty())` 檢查。

- **`lower_bound` 處理空陣列：** `left` 和 `right` 均為 `0`，循環不執行。後續檢查 `left == nums.size()` (`0 == 0`) 為 `true`，正確返回 `-1`。
- **`upper_bound` (尋找結束位置) 處理空陣列：** `left` 和 `right` 均為 `0`，循環不執行。`last_pos` 變為 `-1`。後續檢查 `last_pos < 0` 為 `true`，正確返回 `-1`。

### 重複值的影響

兩種模式都能處理重複值，因為它們的目標不同：

- **模式一** 的不變性是「`target` 若存在，必在 `[left, right]` 內」，它尋找**任意匹配**。
- **模式二** 的不變性是「`left` 左邊的元素都 `< target`，`right` 右邊的元素都 `>= target`（以 `lower_bound` 為例）」，它尋找**精確邊界**。

---

## 總結與決策指南

| 特性 / 場景    | 模式一 (標準搜索)                                      | 模式二 (`lower_bound` / `upper_bound`)                                            |
| :------------- | :----------------------------------------------------- | :-------------------------------------------------------------------------------- |
| **主要目標**   | **存在性檢查** (Find any)                              | **精確邊界定位** (Find first `>=` or `>`)                                         |
| **搜索區間**   | `[0, size - 1]`                                        | `[0, size]`                                                                       |
| **區間收縮**   | `l=m+1`, `r=m-1`                                       | `l=m+1`, `r=m`                                                                    |
| **確認存在性** | **直接** (返回非 -1 值)                                | **間接** (需在返回後額外檢查)                                                     |
| **優點**       | 程式碼最直觀，直接回答“在不在”                         | 精確找到邊界，可用於計數和範圍查詢                                                |
| **缺點**       | 無法區分重複元素的位置                                 | 需額外步驟確認存在性                                                              |
| **適用情境**   | - 確認一個元素是否存在<br>- 陣列中無重複值時的簡單查找 | - 尋找第一個/最後一個出現的位置<br>- 計算等於 `target` 的元素數量 (`upper-lower`) |
