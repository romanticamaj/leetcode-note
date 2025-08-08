# 堆積排序 (Heap Sort)

## 1. 核心概念與分區 (Concept & Partition)

堆積排序可視為**選擇排序的優化版本**。其核心區別在於「尋找最大值」的效率：

- **選擇排序**：透過線性掃描 (`O(n)`) 尋找最大元素。
- **堆積排序**：利用**最大堆積 (Max-Heap)** 結構，能在 `O(1)` 時間內取得最大元素（根節點），並在 `O(log n)` 時間內完成堆積的修復。

演算法利用陣列本身來模擬堆積，並將其邏輯上劃分為兩個動態區間：

1. **最大堆積區間 (Max-Heap Partition)**：位於陣列**前端**，始終滿足最大堆積的性質。
2. **已排序區間 (Sorted Partition)**：位於陣列**後端**，範圍不斷擴大。

為了得到一個非遞減（升序）的陣列，演算法重複地將堆積中的最大元素交換到已排序區間的頂端，此策略與最大堆積的特性完美契合。

## 2. 實作策略與程式碼 (Implementation & Code)

標準的堆積排序採用**原地 (in-place)** 的 **Bottom-up** 方法，包含兩個核心階段：

1. **建堆 (Build Heap)**：`makeHeap` 函式將整個無序陣列轉換成一個最大堆積。
2. **排序 (Sort Down)**：`sortHeap` 函式重複地將堆積的根節點（最大值）與堆積的最後一個元素交換，然後縮小堆積範圍並修復其結構。

### C++ 實作範例

```cpp
#include <vector>
#include <algorithm> // 用於 std::swap

class Solution {
public:
    std::vector<int> sortArray(std::vector<int>& nums) {
        makeHeap(nums);
        sortHeap(nums);
        return nums;
    }

private:
    // 將無序陣列轉換成最大堆積 (Bottom-up)，時間複雜度 O(n)
    void makeHeap(std::vector<int>& nums) {
        // 從最後一個非葉子節點開始，向前逐一進行 heapify
        // n / 2 表示中間點，- 1 表示 0-indexed
        for (int i = nums.size() / 2 - 1; i >= 0; i--) {
            maxHeapify(nums, nums.size(), i);
        }
    }

    // 排序階段，重複 n-1 次 "交換-修復" 操作
    void sortHeap(std::vector<int>& nums) {
        for (int i = nums.size() - 1; i >= 1; i--) { // sorted location
            std::swap(nums[0], nums[i]); // take max out
            maxHeapify(nums, i, 0); // 縮小堆積大小 (heapSize = i)，並從根節點開始修復
        }
    }

    // 維護最大堆積性質的核心函式 (Sift-down)
    void maxHeapify(std::vector<int>& nums, const int heapSize, int i) {
        int largest = i;
        int left = 2 * i + 1;
        int right = 2 * i + 2;

        if (left < heapSize && nums[left] > nums[largest]) {
            largest = left;
        }
        if (right < heapSize && nums[right] > nums[largest]) {
            largest = right;
        }

        if (largest != i) {
            std::swap(nums[i], nums[largest]);
            maxHeapify(nums, heapSize, largest); // recursively heapify
        }
    }
};
```

## 3. 迴圈不變量 (Loop Invariant)

在 `sortHeap` 函式的 `for` 迴圈中，維持著以下不變量：

> 在每次迭代開始時（以 `i` 為索引）：
>
> 1. 子陣列 `nums[i+1...n-1]` 包含 `n-1-i` 個已排序的最大元素。
> 2. 子陣列 `nums[0...i]` 形成一個有效的最大堆積。

- **初始化**：`i = n-1` 時，已排序區間為空，`nums[0...n-1]` 是一個最大堆積（由 `makeHeap` 保證）。
- **維持**：迴圈中，`nums[0]`（最大值）與 `nums[i]` 交換，使已排序區間擴大。然後對 `nums[0...i-1]` 呼叫 `maxHeapify`，使其在下次迭代前恢復為最大堆積。
- **終止**：`i` 遞減至 `0` 時，整個陣列排序完成。

## 4. 屬性 (Properties)

- **穩定性 (Stability)**：堆積排序是**不穩定 (Unstable)** 的。交換操作可能改變相等元素的原始相對順序。
- **原地性 (In-Place)**：堆積排序是**原地 (in-place)** 的，僅需常數級別的額外空間。

## 5. 複雜度與實務考量 (Complexity & Practical Considerations)

### 複雜度分析

- **時間複雜度: O(n log n)**

  - `makeHeap` 階段為 `O(n)`。
  - `sortHeap` 階段包含 `n-1` 次 `O(log n)` 的 `maxHeapify` 操作，總共為 `O(n log n)`。
  - 整體時間複雜度為 `O(n log n)`。

- **空間複雜度: O(1)**

### 實務考量：快取局部性 (Cache Locality)

儘管堆積排序有著優秀的理論複雜度，但在實務中，其效能常不如合併排序或快速排序。主要原因是**糟糕的快取局部性 (Poor Cache Locality)**。

`maxHeapify` 操作在存取父節點 `i` 及其子節點 `2i+1`、`2i+2` 時，記憶體位置可能相距甚遠。這種跳躍式的記憶體存取模式易導致**快取未命中 (Cache Misses)**，從而影響實際運作效能。相比之下，對快取更友好的演算法（如合併排序）通常表現更佳。
