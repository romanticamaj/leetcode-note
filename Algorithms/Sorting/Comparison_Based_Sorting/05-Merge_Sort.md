# 合併排序 (Merge Sort)

## 1. 核心概念與分區 (Concept & Partition)

合併排序是**分治法 (Divide and Conquer)** 的一個典型應用。其核心思想是將一個陣列遞迴地拆解成更小的子陣列，直到每個子陣列只包含一個元素（此時可視為已排序）。接著，再將這些已排序的子陣列兩兩合併，最終組合成一個完全排序的陣列。

與快速排序 (Quicksort) 不同，合併排序的主要工作發生在「征服 (Conquer)」階段，也就是合併已排序子陣列的過程，而「分割 (Divide)」階段則相對簡單。

演算法在邏輯上將陣列劃分為待排序的子區間，並透過一個外部的快取空間來輔助合併操作。

## 2. 實作策略與程式碼 (Implementation & Code)

合併排序主要有兩種實作策略：由上而下 (Top-Down) 的遞迴法和由下而上 (Bottom-Up) 的迭代法。

### 2.1 由上而下 (Top-Down) - 遞迴法

這是最直觀的實作方式，透過遞迴呼叫將陣列不斷對半分割，直到達到基礎情況（子陣列大小為 0 或 1），然後再逐層合併。

#### C++ 實作範例

```cpp
class Solution {
public:
    vector<int> sortArray(vector<int>& nums) {
        vector<int> cache(nums.size());
        mergesort(nums, 0, nums.size(), cache);
        return nums;
    }

    // 排序 [start, end) 區間
    void mergesort(vector<int>& nums, const int start, const int end, vector<int>& cache) {
        if (start >= end) return;
        if (end - start <= 1) return; // 基礎情況：大小為 0 或 1 的陣列已排序

        const int mid = start + (end - start) / 2;

        mergesort(nums, start, mid, cache);
        mergesort(nums, mid, end, cache);

        // --- 合併階段 ---
        // 先將左右兩個已排序的子陣列複製到 cache 中
        for (int i = start; i < end; ++i) {
            cache[i] = nums[i];
        }

        int left = start;  // 左子陣列的指標
        int right = mid;   // 右子陣列的指標
        int k = start;     // 原 nums 陣列的寫入指標

        while (left < mid && right < end) {
            // 為了維持穩定性，使用 <=
            if (cache[left] <= cache[right]) {
                nums[k++] = cache[left++];
            } else {
                nums[k++] = cache[right++];
            }
        }

        // 將剩餘的元素複製回去
        while (left < mid) nums[k++] = cache[left++];
        while (right < end) nums[k++] = cache[right++];
    }
};
```

#### Takeaways

1. **快取一次性建立**：在排序開始前，一次性建立一個與原陣列等大的 `cache`，避免在遞迴中反覆配置記憶體。
2. **合併前複製**：在合併兩個子陣列前，必須先將它們的內容複製到 `cache`。這是因為合併時需要讀取原始、未被覆蓋的數值，同時又要寫入回原 `nums` 陣列。
3. **三指標合併**：使用 `left`, `right`, `k` 三個指標，分別指向左子陣列、右子陣列和目標寫入位置，高效地完成合併。

### 2.2 由下而上 (Bottom-Up) - 迭代法

此方法不使用遞迴，而是透過迭代完成。它從最小的子陣列（大小為 1）開始，兩兩合併成大小為 2 的已排序子陣列，然後再合併成大小為 4，以此類推，直到整個陣列排序完成。

#### C++ 實作範例

```cpp
class Solution {
public:
    vector<int> sortArray(vector<int>& nums) {
        const int n = nums.size();
        vector<int> cache(n);

        for (int size = 1; size < n; size *= 2) { // size 代表當前要合併的子陣列大小
            for (int i = 0; i < n; i += (2 * size)) { // 每次跳 2*size，處理一組相鄰的子陣列
                const int start = i;
                const int mid = std::min(start + size, n); // 優雅處理邊界
                const int end = std::min(start + 2 * size, n); // 優雅處理邊界

                int left = start;
                int right = mid;
                int k = start;

                // 將 nums 的內容合併到 cache
                while (left < mid && right < end) {
                    if (nums[left] <= nums[right])
                        cache[k++] = nums[left++];
                    else
                        cache[k++] = nums[right++];
                }
                while (left < mid) cache[k++] = nums[left++];
                while (right < end) cache[k++] = nums[right++];
            }
            // 每一輪合併的結果都在 cache 中，將其與 nums 交換，
            // 以便下一輪迭代能從已部分排序的 nums 開始
            swap(nums, cache);
        }

        return nums;
    }
};
```

#### Takeaways

1. **迭代決定大小**：外層迴圈 `size` (1, 2, 4, ...) 決定了當前合併的子陣列大小。
2. **成對選取**：內層迴圈 `i` 負責遍歷陣列，每次選取一對相鄰的子陣列進行合併。
3. **邊界處理**：使用 `std::min` 來計算 `mid` 和 `end`，可以優雅地處理陣列尾端長度不足 `2*size` 的情況。
4. **雙緩衝區交換 (Double Buffering)**：`swap(nums, cache)` 是關鍵。每一輪迭代都從 `nums` 讀取，將合併結果寫入 `cache`。然後交換兩者，讓下一輪迭代的 `nums` 是上一輪的排序結果，避免了額外的 `O(n)` 複製操作。

## 3. 迴圈不變量 (Loop Invariant)

### Top-Down (遞迴法)

對於 `mergesort` 函式中的合併階段（`while` 迴圈），可以定義一個不變量。

> 在每次 `while (left < mid && right < end)` 迴圈開始時：
>
> 1. `nums[start...k-1]` 包含 `k - start` 個來自左右子陣列的最小元素，且它們是已排序的。
> 2. `cache[left...mid-1]` 和 `cache[right...end-1]` 分別是尚未被複製回 `nums` 的剩餘元素。

- **初始化**：`k = start` 時，`nums[start...start-1]` 是一個空區間，條件成立。
- **維持**：迴圈中，會從 `cache[left]` 和 `cache[right]` 中選出較小者放入 `nums[k]`，然後遞增 `k` 和對應的 `left` 或 `right` 指標。這確保了 `nums[start...k-1]` 始終是已排序的。
- **終止**：當 `left == mid` 或 `right == end` 時，迴圈終止。此時，一個子陣列已被完全複製。後續的兩個 `while` 迴圈會將另一個子陣列的剩餘元素複製過去，完成整個 `[start, end)` 區間的合併。

### Bottom-Up (迭代法)

對於 **Bottom-Up** 迭代法的外層 `for` 迴圈（以 `size` 為變數），維持著以下不變量：

> 在每次 `size` 迴圈開始時：
>
> 陣列 `nums` 由一系列長度為 `size` 的已排序子陣列組成（最後一個子陣列長度可能小於 `size`）。

- **初始化**：`size = 1` 時，陣列中的每個元素可視為一個長度為 1 的已排序子陣列，不變量成立。
- **維持**：內層迴圈將相鄰的兩個長度為 `size` 的已排序子陣列合併成一個長度為 `2*size` 的已排序子陣列。當內層迴圈結束時，整個陣列變為由一系列長度為 `2*size` 的已排序子陣列組成。
- **終止**：當 `size` 增長到大於或等於 `n` 時，迴圈終止，此時整個陣列已合併為一個單一的已排序陣列。

## 4. 屬性 (Properties)

- **穩定性 (Stability)**：合併排序是**穩定 (Stable)** 的。在合併過程中，如果遇到相等的元素，總是先取左邊子陣列的元素 (`cache[left] <= cache[right]`)，從而保證了它們的原始相對順序。
- **原地性 (In-Place)**：合併排序**不是原地 (not in-place)** 的，它需要 `O(n)` 的額外空間來建立快取陣列。

## 5. 複雜度與實務考量 (Complexity & Practical Considerations)

### 複雜度分析

- **時間複雜度: O(n log n)**

  - 無論是最佳、平均還是最差情況，時間複雜度都是 `O(n log n)`。
  - `log n` 來自遞迴的深度或迭代的輪數。
  - `n` 來自每一層或每一輪合併操作所需的線性時間。

- **空間複雜度: O(n)**
  - 需要一個與原陣列等大的輔助陣列 (`cache`)。

### 實務考量

- **外部排序 (External Sorting)**：合併排序非常適合處理無法完全載入記憶體的超大型資料。它可以分塊讀取資料、排序後寫回磁碟，再合併這些已排序的區塊。
- **效能穩定**：其 `O(n log n)` 的最差情況時間複雜度保證了效能的穩定性，不會像快速排序那樣在特定情況下退化到 `O(n^2)`。
- **快取局部性 (Cache Locality)**：合併排序（特別是迭代版本）具有良好的快取局部性，因為它主要進行循序的記憶體讀寫，這通常使其在實務中比堆積排序等跳躍式存取的演算法更快。
- **`std::stable_sort`**：C++ 標準庫中的 `std::stable_sort` 通常採用合併排序或其變種（如 Timsort），以同時保證穩定性和 `O(n log n)` 的效能。
