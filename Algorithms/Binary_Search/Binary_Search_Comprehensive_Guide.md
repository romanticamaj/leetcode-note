# 🟢 二分搜尋全面心法整理

二分搜尋法的精髓在於其 **搜尋區間 (Search Space)** 的定義與 **收斂方式 (Convergence)**。不同的設定組合適用於不同的情境。

## 🚀 設計二分搜尋的五大考量

設計任何二分搜尋演算法時，都必須仔細考量並搭配以下五個核心元素：

1. **搜尋空間 (Search Space)**: 定義 `left` 和 `right` 指標的初始範圍。

   - `[0, size-1]` (搜尋元素): 用於在陣列內部尋找特定元素。
   - `[0, size]` (搜尋插入點): 用於尋找一個插入位置，包含「插入在所有元素之後」的可能。

2. **目標指標 (Target Pointer)**: 通常是 `left`，代表迴圈結束時我們想要的答案。

3. **修剪指標 (Pruning Pointer)**: 通常是 `right`，用來縮小搜尋空間的右邊界。

4. **迴圈條件 (While Condition)**: 決定搜尋何時終止。

   - `left <= right`: 搭配 `[0, size-1]` 空間，當 `left > right` 時區間為空。
   - `left < right`: 搭配 `[0, size]` 空間，當 `left == right` 時收斂至單點。

5. **收斂策略 (Convergence Strategy)**: 根據 `mid` 與 `target` 的關係，決定如何移動指標。
   - **基本型 (找特定值)**: `left = mid + 1` 或 `right = mid - 1`
   - **`lower_bound` (往左找)**: `right = mid`
   - **`upper_bound` (往右找)**: `left = mid + 1`

## 🧠 核心口訣

- **`lower_bound` (找第一個 `>=`)**: 關鍵是 **往左找**。當 `mid` 滿足條件 (`>= target`) 時，`right` 指標要盡量往左靠，所以設為 `mid`。
- **`upper_bound` (找第一個 `>`)**: 關鍵是 **往右找**。當 `mid` 不滿足條件 (`<= target`) 時，`left` 指標要盡量往右跳，所以設為 `mid + 1`。

---

## 📘 範本一：基本型 (尋找特定值)

### 🎯 適用情境

- 陣列中 **沒有重複元素**。
- 目標是尋找 **目標值是否存在** 或其 **精確的索引**。
- 這是最經典、最直觀的版本。

### 🛠️ 配套設定

| 設定         | 值                                   | 說明                       |
| :----------- | :----------------------------------- | :------------------------- |
| **搜尋空間** | `[0, size-1]`                        | `right` 指向最後一個元素。 |
| **迴圈條件** | `left <= right`                      | 只要區間有效就繼續。       |
| **收斂邏輯** | `left = mid + 1` / `right = mid - 1` | 每次都排除 `mid`。         |

### ⚙️ 程式碼邏輯

```cpp
while (left <= right) {
    int mid = left + (right - left) / 2;
    if (arr[mid] == target) {
        return mid; // 找到，直接返回
    } else if (arr[mid] > target) {
        right = mid - 1; // 往左半部找
    } else {
        left = mid + 1; // 往右半部找
    }
}
// 沒找到，left 是插入點
return left;
```

### 🏁 最終狀態

- **退出時**: `left > right`，搜尋區間為空。
- **區間示意**: `[... right] [left ...]`
- **`left` 的意義**: 如果找不到 `target`，`left` 的位置是第一個大於 `target` 的元素索引，也就是 `target` 的插入點。

---

## 📗 範本二：Lower Bound (找第一個 `>= target`)

### 🎯 適用情境

- 陣列中 **可能有重複元素**。
- 目標是尋找第一個 **大於或等於** `target` 的元素位置。
- 等同於 C++ STL 的 `std::lower_bound`。

### 🛠️ 配套設定

| 設定         | 值             | 說明                                                                                          |
| :----------- | :------------- | :-------------------------------------------------------------------------------------------- |
| **搜尋空間** | `[0, size]`    | `right` 設為 `size`，將 `size` 納入答案的可能範圍。                                           |
| **迴圈條件** | `left < right` | 當 `left == right` 時，區間收斂至一點。                                                       |
| **收斂邏輯** | `right = mid`  | **向左收斂**。當 `arr[mid] >= target`，`mid` 可能是答案，但我們嘗試在左邊找尋更早出現的答案。 |

### ⚙️ 程式碼邏輯

```cpp
while (left < right) {
    int mid = left + (right - left) / 2;
    if (arr[mid] >= target) {
        right = mid; // mid 可能是答案，試著往左邊找更好的
    } else {
        left = mid + 1; // mid 太小，一定不是答案，往右找
    }
}
return left;
```

### 🏁 最終狀態

- **退出時**: `left == right`。
- **`left` 的意義**: 第一個大於或等於 `target` 的元素索引。如果所有元素都小於 `target`，則 `left` 會是 `size`。

---

## 📙 範本三：Upper Bound (找第一個 `> target`)

### 🎯 適用情境

- 陣列中 **可能有重複元素**。
- 目標是尋找第一個 **嚴格大於** `target` 的元素位置。
- 等同於 C++ STL 的 `std::upper_bound`。

### 🛠️ 配套設定

| 設定         | 值               | 說明                                                                          |
| :----------- | :--------------- | :---------------------------------------------------------------------------- |
| **搜尋空間** | `[0, size]`      | 同 `lower_bound`。                                                            |
| **迴圈條件** | `left < right`   | 同 `lower_bound`。                                                            |
| **收斂邏輯** | `left = mid + 1` | **向右收斂**。當 `arr[mid] <= target`，`mid` 肯定不是答案，我們需要往右邊找。 |

### ⚙️ 程式碼邏輯

```cpp
while (left < right) {
    int mid = left + (right - left) / 2;
    if (arr[mid] > target) {
        right = mid; // mid 可能是答案，但試著往左邊找更好的
    } else {
        left = mid + 1; // mid 不夠大，一定不是答案，往右找
    }
}
return left;
```

### 🏁 最終狀態

- **退出時**: `left == right`。
- **`left` 的意義**: 第一個嚴格大於 `target` 的元素索引。如果所有元素都小於或等於 `target`，則 `left` 會是 `size`。

---

## 🎯 範例：`[1,1,1,1,1]`, `target=1`

這個例子最能體現 `lower_bound` 和 `upper_bound` 的行為差異：

- **`lower_bound`**:
  - 因為 `arr[mid] >= 1` 始終成立，會不斷執行 `right = mid`，將搜尋邊界持續向左壓縮。
  - 最終 `left` 會收斂到 `0`。
- **`upper_bound`**:
  - 因為 `arr[mid] > 1` 始終不成立 (`1 > 1` 為 false)，會不斷執行 `left = mid + 1`，將搜尋邊界持續向右推進。
  - 最終 `left` 會收斂到 `5` (`size`)。

---

## 🟥 關鍵陷阱：為何 `lower/upper_bound` 的 `right` 不能設為 `size - 1`？

一個常見的誤解是試圖將 `lower/upper_bound` 的邏輯套用在 `[0, size-1]` 的搜尋空間上。這會導致在邊界情況下出錯。

### 🧠 核心理由

> **`right` 初始化為 `size` 是為了讓 `left` 指標（即最終答案）有機會移動到 `size` 這個位置。**
>
> 如果 `target` 比所有元素都大，`lower_bound` 和 `upper_bound` 都需要能夠回傳 `size` 作為正確的插入點。如果 `right` 被限制在 `size-1`，`left` 將永遠無法合法地達到 `size`，導致無法處理這種邊界情況。

### 🧭 具體錯誤範例

假設 `nums = [2, 4, 6]`, `target = 7`，並使用 `lower_bound` 的邏輯但錯誤的邊界設定：

```cpp
// 錯誤的設定
int left = 0;
int right = nums.size() - 1; // right = 2

while (left < right) { // 迴圈條件
    int mid = left + (right - left) / 2;
    if (nums[mid] >= 7) {
        right = mid;
    } else {
        left = mid + 1;
    }
}
return left;
```

**收斂過程**:

1. `left=0, right=2` -> `mid=1`. `nums[1]` (4) < 7. `left` 變為 `2`.
2. `left=2, right=2`. `left < right` 條件不滿足，迴圈終止。

**結果**: 函式回傳 `left = 2`。但正確的插入點應該是索引 `3`。這個模型失敗了。

### 🟢 正確的配套

**規則很簡單：搜尋空間的定義必須和迴圈條件配套使用。**

- 如果你使用 `while (left < right)`，請搭配 `right = size`。
- 如果你使用 `while (left <= right)`，請搭配 `right = size - 1`。

---

## 🏆 總結：心法對照表

| 用途              | 搜尋空間      | `while` 條件    | 收斂狀態        | 結果語意                           |
| :---------------- | :------------ | :-------------- | :-------------- | :--------------------------------- |
| **找特定值**      | `[0, size-1]` | `left <= right` | `left > right`  | `left` = 插入點 或 第一個 > target |
| **`lower_bound`** | `[0, size]`   | `left < right`  | `left == right` | `left` = 第一個 `>= target`        |
| **`upper_bound`** | `[0, size]`   | `left < right`  | `left == right` | `left` = 第一個 `> target`         |
