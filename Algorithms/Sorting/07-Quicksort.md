# 快速排序 (Quicksort)

## 1. 核心概念 (Concept & Partition)

快速排序是另一個基於**分治法 (Divide and Conquer)** 的高效排序演算法。其精神與合併排序相似，但策略相反：它將主要精力放在**分割 (Divide)** 階段，而**合併 (Combine)** 階段則微不足道。

其核心流程包含三個步驟：

1. **分割 (Divide)**：選取陣列中的一個元素作為**基準 (Pivot)**。然後，重新排列陣列，使得所有小於或等於基準的元素都在基準的左邊，所有大於基準的元素都在基準的右邊。這個過程稱為 **分割 (Partitioning)**。完成後，基準元素就位於其最終的排序位置。
2. **征服 (Conquer)**：遞迴地對基準左右兩邊的兩個子陣列進行快速排序。
3. **合併 (Combine)**：由於子陣列是原地排序的，當遞迴結束時，整個陣列就已經排序完成，無需任何合併操作。

## 2. CLRS 虛擬碼 (CLRS Pseudocode)

這是《演算法導論》(CLRS) 中的經典虛擬碼實現，它清晰地展示了演算法的結構。

### QUICKSORT

```
QUICKSORT(A, p, r)
1 if p < r
2     q = PARTITION(A, p, r)
3     QUICKSORT(A, p, q - 1)
4     QUICKSORT(A, q + 1, r)
```

### PARTITION

```
PARTITION(A, p, r)
1 x = A[r]
2 i = p - 1
3 for j = p to r - 1
4     if A[j] <= x
5         i = i + 1
6         exchange A[i] with A[j]
7 exchange A[i + 1] with A[r]
8 return i + 1
```

## 3. C++ 實作 (C++ Implementation)

此 C++ 實作採用了與 CLRS 相似的邏輯，以最後一個元素作為基準 (Pivot)，並使用了 C++ STL 風格的半開區間。

### 與 CLRS 版本的差異：區間表示法

值得注意的是，此 C++ 實作與 CLRS 虛擬碼在處理**區間 (Range)** 的方式上有所不同，這也是學術界與工程界常見的差異：

- **CLRS 版本**: 使用**閉區間 (Inclusive Range)** `[p, r]`，`r` 是區間內的最後一個有效元素的索引。
- **C++ 版本**: 遵循 C++ STL 的慣例，使用**半開區間 (Half-Open Range)** `[start, end)`，`end` 是區間結尾的**下一個位置**（不包含在區間內）。

這個差異導致了終止條件和基準選擇的細微不同（例如 `end - start > 1` vs `p < r`，以及 `pivot_val_idx = end - 1`），但核心的分治思想是一致的。

```cpp
class Solution {
public:
    vector<int> sortArray(vector<int>& nums) {
        quicksort(nums, 0, nums.size());
        return nums;
    }

private:
    // 對 [start, end) 區間進行排序
    void quicksort(vector<int>& nums, const int start, const int end) {
        // 只有當區間內至少有兩個元素時才需要排序
        if (end - start > 1) {
            int pivot_idx = partition(nums, start, end);
            quicksort(nums, start, pivot_idx);
            quicksort(nums, pivot_idx + 1, end);
        }
    }

    // 分割 [start, end) 區間，並返回基準的最終索引
    int partition(vector<int>& nums, const int start, const int end) {
        const int pivot_val_idx = end - 1; // 以最後一個元素為基準
        int k = start; // k 是「小於等於基準」區間的右側邊界 (one-past-the-end)

        // 遍歷除了基準之外的所有元素
        for (int i = start; i < pivot_val_idx; i++) {
            if (nums[i] <= nums[pivot_val_idx]) {
                swap(nums[k], nums[i]);
                k++; // 擴大「小於等於基準」的區間
            }
        }

        // 迴圈結束後，k 是第一個大於基準的元素的位置
        // 將基準與其交換，完成分割
        swap(nums[k], nums[pivot_val_idx]);

        return k; // 返回基準的最終位置
    }
};
```

## 4. 迴圈不變量 (Loop Invariant)

在 `partition` 函式的 `for` 迴圈中（以 `i` 為索引），維持著以下不變量，它清晰地描述了陣列的動態劃分狀態：

> 在每次迭代開始時：
>
> 1. 對於所有 `start <= m < k` 的索引 `m`，`nums[m] <= pivot`。
> 2. 對於所有 `k <= m < i` 的索引 `m`，`nums[m] > pivot`。

這將陣列 `nums[start...pivot_val_idx-1]` 劃分為三個邏輯區間：

1. `nums[start...k-1]`：**小於等於**基準值的元素。
2. `nums[k...i-1]`：**大於**基準值的元素。
3. `nums[i...pivot_val_idx-1]`：尚未檢視的元素。

- **初始化**：迴圈開始前，`i = k = start`。此時區間 1 和 2 都是空的，不變量顯然成立。
- **維持**：
  - 若 `nums[i] > pivot`，則僅遞增 `i`。這會將 `nums[i]` 納入區間 2，不變量得以維持。
  - 若 `nums[i] <= pivot`，則 `nums[k]` 與 `nums[i]` 交換，然後 `k` 和 `i` 同時遞增。這將 `nums[i]` 放入了區間 1 的末尾，同時擴大了區間 1 和 2，不變量得以維持。
- **終止**：迴圈結束時 `i = pivot_val_idx`。此時 `nums[start...k-1]` 都是小於等於基準的元素。最後將基準 `nums[pivot_val_idx]` 與 `nums[k]` 交換，就將基準放到了正確的位置 `k`，並返回此索引。

## 5. 穩定性 (Stability)

快速排序是**不穩定 (Unstable)** 的。
在分割過程中，與基準相隔較遠的元素可能會被交換，這很容易打亂相等元素的原始相對順序。例如，在 `[5a, 2, 5b]` 中，若以 `5b` 為基準，`5a` 會被交換到 `5b` 的右側，破壞了穩定性。

## 6. 時間複雜度 (Time Complexity)

- **最差情況 (Worst Case): O(n²)**
  - 發生在每次分割都極不均衡時，例如對一個已經排序好的陣列進行排序，每次都選到最大或最小的元素作為基準。遞迴樹會退化成一條鏈，深度為 `n`。
- **最佳情況 (Best Case): O(n log n)**
  - 發生在每次分割都恰好將陣列對半分割時。遞迴樹的深度為 `log n`。
- **平均情況 (Average Case): O(n log n)**
  - 在 **隨機輸入** 下，快速排序的表現非常好。數學上可以證明其平均時間複雜度為 `O(n log n)`，且其常數因子較小，使其在實務中通常比其他 `O(n log n)` 演算法更快。

## 7. 深入探討：分割策略的影響 (Deep Dive: Partition Schemes)

分割策略是快速排序的核心，直接影響其效能。你所提供以及 CLRS 中的實作，都屬於 **Lomuto 分割方案 (Lomuto partition scheme)**。

- **Lomuto 分割方案**：
  - **特點**：較容易理解和實作。它總是將基準放在分割後區間的端點，並在一次遍歷後將基準交換到其最終的排序位置。
  - **缺點**：在處理有大量重複元素的陣列時，效能較差。

另一種非常著名的策略是 **Hoare 分割方案 (Hoare partition scheme)**。

- **Hoare 分割方案**：
  - **特點**：通常比 Lomuto 方案更有效率，平均進行的交換次數更少。它使用左右兩個指標同時向中間移動。
  - **缺點**：實作起來稍微複雜，且它**不會**將基準元素放在其最終的排序位置，僅保證其左邊的元素都比它小，右邊的都比它大。

不同的分割策略有各自的優劣，選擇哪一種取決於具體的應用場景。我們將在 `Algorithms/Partition/` 資料夾中對這些策略進行更詳細的介紹。
