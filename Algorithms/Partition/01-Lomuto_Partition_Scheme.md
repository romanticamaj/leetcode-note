# Lomuto 分割方案 (Lomuto Partition Scheme)

## 1. 核心概念

Lomuto 分割方案是一種相對直觀的分割演算法，常用於快速排序中。其核心思想是選定陣列的**最後一個元素**作為**基準 (Pivot)**，然後透過一次線性掃描，將陣列重新排列為兩個部分：

1. 所有小於或等於基準的元素。
2. 所有大於基準的元素。

完成後，再將基準元素放置到這兩個部分的交界處，使其到達最終的排序位置。

## 2. 演算法流程與程式碼

演算法維護一個指標 `k`，這個指標可以看作是「小於等於基準」這個區間的右側邊界 (one-past-the-end)。

1. **初始化**：`k` 指向區間的起始位置 `start`。
2. **遍歷**：使用另一個指標 `i` 從 `start` 遍歷到基準之前的位置 (`end - 2`)。
3. **交換**：
   - 如果 `nums[i]` 小於或等於基準 `nums[end - 1]`，則表示 `nums[i]` 應該屬於左側分區。此時，將 `nums[i]` 與 `nums[k]` 交換，並將 `k` 向右移動一位，以擴大左側分區的範圍。
   - 如果 `nums[i]` 大於基準，則 `i` 繼續前進，`k` 保持不動。
4. **放置基準**：遍歷結束後，`k` 指向的位置是第一個大於基準的元素。將基準（位於 `end - 1`）與 `nums[k]` 交換，這樣基準就恰好位於兩個分區之間。
5. **返回**：返回 `k` 作為基準的最終索引。

### C++ 實作 (半開區間 `[start, end)`)

```cpp
#include <vector>
#include <algorithm> // for std::swap

/**
 * @brief 使用 Lomuto 分割方案對 nums 的 [start, end) 區間進行分割
 * @param nums 欲分割的陣列
 * @param start 區間起始索引 (包含)
 * @param end 區間結束索引 (不包含)
 * @return int 基準 (pivot) 的最終索引
 */
int partition(std::vector<int>& nums, const int start, const int end) {
    // 選擇最後一個元素作為基準
    const int pivot_val_idx = end - 1;

    // k 是「小於等於基準」區間的右側邊界 (one-past-the-end)
    // 也可以理解為下一個小於等於基準的元素應該被放置的位置
    int k = start;

    // 遍歷除了基準之外的所有元素
    for (int i = start; i < pivot_val_idx; i++) {
        if (nums[i] <= nums[pivot_val_idx]) {
            std::swap(nums[k], nums[i]);
            k++; // 擴大「小於等於基準」的區間
        }
    }

    // 迴圈結束後，k 是第一個大於基準的元素的位置
    // 將基準與其交換，完成分割
    std::swap(nums[k], nums[pivot_val_idx]);

    return k; // 返回基準的最終位置
}
```

## 3. 迴圈不變量 (Loop Invariant)

在 `for` 迴圈中，維持著以下不變量：

> 在每次迭代開始時：
>
> 1. 對於所有 `start <= m < k` 的索引 `m`，`nums[m] <= pivot`。
> 2. 對於所有 `k <= m < i` 的索引 `m`，`nums[m] > pivot`。

這個不變量清晰地將陣列劃分為三個邏輯區間：`[<= pivot]`, `[> pivot]`, `[尚未檢視]`。

## 4. 特性分析

- **優點**：
  - 邏輯清晰，易於理解和實作。
  - 總能將基準元素放置到其最終的排序位置。
- **缺點**：
  - 在處理包含大量重複元素的陣列時，效能不佳。如果許多元素都等於基準，它們都會被交換到左側分區，可能導致分割非常不均衡。
  - 與 Hoare 分割方案相比，通常需要進行更多的交換操作。
