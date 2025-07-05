# 二分搜尋法範本與插入點解釋

本文件提供一個二分搜尋法的標準範本，並直觀地解釋為何當找不到目標時，迴圈不變數 (loop invariant) 能幫助我們找到正確的插入點。

## 二分搜尋法的核心原則

1. **已排序的輸入**：陣列或集合必須是已排序的。
2. **無重複元素**：在此基本範本中，我們假設沒有重複的元素。
3. **中點計算**：`mid = left + (right - left) / 2`。
   - 如果子陣列長度 (`right - left + 1`) 是奇數，`mid` 會是正中央的元素。
   - 如果子陣列長度是偶數，`mid` 會是中間兩個元素中偏左的那一個。
4. **迴圈條件**：搜尋會持續進行，只要 `while (left <= right)`。
5. **縮小搜尋範圍**：
   - 如果 `nums[mid] == target`，表示找到元素。
   - 如果 `nums[mid] > target`，目標必定在左半邊，所以我們捨棄右半邊：`right = mid - 1`。
   - 如果 `nums[mid] < target`，目標必定在右半邊，所以我們捨棄左半邊：`left = mid + 1`。
6. **插入點**：如果迴圈結束 (`left > right`)，`left` 的索引值就是 `target` 應該被插入的正確位置。

## C++ 二分搜尋法範本

這個範本會尋找目標值的索引。如果找不到目標，它會回傳目標應該被插入以維持排序順序的索引位置。

```cpp
int binarySearch(const std::vector<int>& nums, int target) {
    int left = 0;
    int right = nums.size() - 1;

    while (left <= right) {
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

要理解為什麼 `left` 會成為插入點，關鍵在於觀察 `while (left <= right)` 迴圈終止時 `left` 和 `right` 指標的狀態。

迴圈在 `left > right` 時終止。這個條件也可以寫成 `left = right + 1`。

讓我們分析最後一步之前的指標狀態：

1. **搜尋空間縮小**：每一次迭代，二分搜尋演算法都會排除掉目標不可能存在的那一半陣列。
2. **`left` 和 `right` 指標收斂**：最終，`left` 和 `right` 會指向相鄰的元素或同一個元素。
3. **最後的比較**：考慮 `left == right` 的最後一次迭代。此時搜尋空間已經縮小到位於索引 `mid = left = right` 的單一元素。
   - **情況 A: `nums[mid] < target`**：
     - 我們知道 `target` 必定在 `mid` 的右邊。
     - 程式碼執行 `left = mid + 1`。
     - 現在，`left` 是 `mid + 1`，而 `right` 仍然是 `mid`。迴圈因為 `left > right` 而終止。
     - 插入點是 `left`，正好是 `mid` 之後的一個位置。這是正確的，因為 `nums[mid]` 比 `target` 小。
   - **情況 B: `nums[mid] > target`**：
     - 我們知道 `target` 必定在 `mid` 的左邊。
     - 程式碼執行 `right = mid - 1`。
     - 現在，`right` 是 `mid - 1`，而 `left` 仍然是 `mid`。迴圈因為 `left > right` 而終止。
     - 插入點是 `left` (值仍然是 `mid`)。這也是正確的。`target` 應該被插入在 `mid` 的位置，將 `nums[mid]` 及所有後續元素向右推移一個位置。