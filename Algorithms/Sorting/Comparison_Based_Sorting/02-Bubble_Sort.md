# 氣泡排序 (Bubble Sort)

## 1. 核心概念 (Concept)

氣泡排序的核心思想是**重複地遍歷待排序序列，比較相鄰元素，若順序錯誤則交換**。此過程會將當前未排序區間內的最大元素「浮」至序列末端。

演算法將陣列邏輯上劃分為兩個動態區間：

1. **已排序區間 (Sorted Partition)**：位於陣列的**後端**，每輪遍歷後會增加一個已確定位置的最大值。
2. **未排序區間 (Unsorted Partition)**：位於陣列的**前端**，是演算法操作的主要範圍。

## 2. 範例程式碼 (C++)

### 基礎版本 (用於理解)

這個版本展示了氣泡排序最原始的雙層迴圈結構。

```cpp
#include <iostream>
#include <vector>
#include <algorithm> // 用於 std::swap

void bubbleSortBasic(std::vector<int>& arr) {
    int n = arr.size();
    // 外層迴圈控制總共需要比較的輪數
    for (int i = 0; i < n - 1; ++i) {
        // 優化版本會在此處宣告一個旗標，如：bool swapped = false;

        // 內層迴圈的邊界 (n - i - 1) 會隨著已排序區間的擴大而縮小
        for (int j = 0; j < n - i - 1; ++j) {
            if (arr[j] > arr[j + 1]) {
                std::swap(arr[j], arr[j + 1]);
                // 優化版本會在此處設定旗標為 true，表示發生了交換
                // swapped = true;
            }
        }

        // 優化版本會在此處檢查旗標。如果整輪都沒有發生交換，
        // 代表陣列已排序完成，即可提早終止迴圈。
        // if (!swapped) {
        //     break;
        // }
    }
}
```

### 優化版本 (LeetCode 適用)

此版本使用 `while` 迴圈搭配旗標，在陣列已有序時能提早終止，寫法簡潔，適合在解題時快速實現。

```cpp
#include <iostream>
#include <vector>
#include <algorithm> // 用於 std::swap

void bubbleSort(std::vector<int>& nums) {
    bool swapped = true;
    while (swapped) {
        swapped = false;
        for (int i = 0; i < nums.size() - 1; i++) {
            if (nums[i] > nums[i + 1]) {
                std::swap(nums[i], nums[i + 1]);
                swapped = true;
            }
        }
    }
}
```

## 3. 迴圈不變量 (Loop Invariant)

氣泡排序的外層 `for` 迴圈（以 `i` 為索引）維持著以下不變量：

> 在第 `i` 次迭代開始之前，陣列的末尾 `i` 個元素 (`arr[n-i...n-1]`) 包含了整個陣列中 `i` 個最大的元素，並且它們已經處於其最終的**已排序**位置。

- **初始化**：`i=0` 時，已排序區間為空，不變量成立。
- **維持**：在第 `i` 輪中，內層迴圈會將未排序區間的最大值移至 `arr[n-i-1]`，從而使已排序區間擴大為 `i+1` 個元素。
- **終止**：`i` 達到 `n-1` 時，`arr[0...n-1]` 全部有序。

## 4. 穩定性 (Stability)

氣泡排序是一種 **穩定 (Stable)** 的排序演算法。

因為交換僅發生在相鄰元素嚴格逆序 (`arr[j] > arr[j+1]`) 時。若兩個元素相等，演算法不會交換它們，從而保留其原始相對順序。

## 5. 複雜度分析 (Complexity Analysis)

- **時間複雜度 (Time Complexity)**

  - **最差/平均情況: O(n²)**：當輸入陣列逆序或隨機時。
  - **最佳情況: O(n)**：僅適用於**優化版本**。若輸入已排序，僅需遍歷一次即可提早終止。

- **空間複雜度 (Space Complexity): O(1)**
  - 氣泡排序是一種 **原地排序 (in-place)** 演算法，僅需常數級別的額外空間。
