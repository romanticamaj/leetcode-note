# 閉區間三路搜尋與插入點：舊版對照

> ⚠️ **已被取代**：標準寫法見 [00-Binary_Search_Standard_Template.md](00-Binary_Search_Standard_Template.md)（半開區間 + 找第一個 true）。本篇的閉區間三路比較寫法保留作對照，不要背。

本文件提供一個二分搜尋法的標準範本，並直觀地解釋為何當找不到目標時，迴圈不變數 (loop invariant) 能幫助我們找到正確的插入點。

## 二分搜尋法的核心原則

1. **已排序的輸入**：陣列或集合必須是已排序的。
2. **搜尋範圍**：搜尋範圍為 `[0, nums.size() - 1]`，即包含陣列的第一個元素到最後一個元素。
3. **無重複元素**：在此基本範本中，我們假設沒有重複的元素。
4. **中點計算**：`mid = left + (right - left) / 2`。
   - 如果子陣列長度 (`right - left + 1`) 是奇數，`mid` 會是正中央的元素。
   - 如果子陣列長度是偶數，`mid` 會是中間兩個元素中偏左的那一個。
5. **迴圈條件**：搜尋會持續進行，只要 `while (left <= right)`。
6. **縮小搜尋範圍**：
   - 如果 `nums[mid] == target`，表示找到元素。
   - 如果 `nums[mid] > target`，目標必定在左半邊，所以我們捨棄右半邊：`right = mid - 1`。
   - 如果 `nums[mid] < target`，目標必定在右半邊，所以我們捨棄左半邊：`left = mid + 1`。
7. **插入點**：如果迴圈結束 (`left > right`)，`left` 的索引值就是 `target` 應該被插入的正確位置。

## C++ 二分搜尋法範本

這個範本會尋找目標值的索引。如果找不到目標，它會回傳目標應該被插入以維持排序順序的索引位置。

```cpp
int binarySearch(const std::vector<int>& nums, int target) {
    int left = 0;
    int right = nums.size() - 1; // 設定區間 [0, size() - 1]

    while (left <= right) { // left 指向 target 位置，left 最後一個可能是 right，所以需判斷 left == right
        int mid = left + (right - left) / 2;

        if (nums[mid] == target) {
            return mid; // 找到目標
        } else if (nums[mid] > target) {
            right = mid - 1; // 在左半部搜尋
        } else {
            left = mid + 1; // 在右半部搜尋
        }
    }

    // 找不到目標，`left` 即為插入點。
    return left;
}
```

## 對於插入點 (`left`) 的直觀看法

當 `while (left <= right)` 迴圈結束時，代表 `left > right`，此時的陣列狀態可以被理解為：

```
... [所有小於 target 的元素] ... [right] [left] ... [所有大於 target 的元素] ...
```

- **`right` 指標**: 指向的是「小於 `target` 的元素」這個區塊的 **最右邊界**。
- **`left` 指標**: 指向的是「大於 `target` 的元素」這個區塊的 **最左邊界**。

在迴圈的每一步，我們都在維護這個規則：

- 如果 `nums[mid] < target`，我們知道 `mid` 以及它左邊的所有元素都太小了，所以我們移動 `left = mid + 1`，將 `left` 指標推向右邊。
- 如果 `nums[mid] > target`，我們知道 `mid` 以及它右邊的所有元素都太大了，所以我們移動 `right = mid - 1`，將 `right` 指標拉向左邊。

當迴圈終止時，`left` 和 `right` 指標交錯而過，`left` 正好停在第一個大於 `target` 的元素應該在的位置。因此，如果 `target` 不存在於陣列中，`left` 就是它最理想的插入點，可以確保插入後陣列依然保持排序。
