# 基數排序 (Radix Sort)

## 1. 核心概念與分區 (Concept & Partition)

基數排序 (Radix Sort) 是一種高效的非比較排序演算法，其核心思想不是比較元素的大小，而是利用整數的**位數 (digit)** 來進行排序。它將多位數的排序問題，拆解成多次針對單一位數的排序問題。

最常見的實現是 **LSD (Least Significant Digit) Radix Sort**，其流程如下：

1. **確定迭代次數**：找到輸入陣列中的最大值，其位數 `d` 決定了總共需要進行幾輪排序。
2. **從最低位開始排序**：從個位數 (least significant digit) 開始，使用一個**穩定**的排序演算法（通常是計數排序）對所有元素進行排序。
3. **向高位迭代**：接著，對十位數、百位數... 直到最高位數 (most significant digit)，重複進行穩定的排序。
4. **完成**：當最高位的排序完成後，整個陣列也就完全有序了。

**關鍵前提**：每一輪的排序都**必須是穩定的**，這樣才能保證前一輪低位數的排序結果能在後一輪高位數的排序中得以保持。

### 從計數排序到基數排序的動機

計數排序雖然在特定條件下非常快，但它有兩個主要限制：

1. **對鍵的範圍 (k) 敏感**：當整數的最大值非常大時，計數排序需要一個同樣巨大的計數陣列，這會導致過高的記憶體開銷，使其失去吸引力。
2. **難以處理複雜鍵**：計數排序不適合直接處理字串這類鍵，因為字母表的規模可能非常大或不固定。

基數排序正是為了解決這些問題而生。它不直接對整個數值或字串進行計數，而是將其分解為更小的、範圍固定的單元（例如十進位的**位數**或字串的**字元**），然後對這些單元逐一進行穩定的計數排序。這使得它能夠在可控的記憶體開銷下，高效地處理大範圍的整數和字串排序。

### 處理負數

標準的基數排序僅適用於非負整數。若要處理包含負數的陣列，通用的策略是：

1. 將正數和負數分開。
2. 將負數全部轉為正數。
3. 分別對正數陣列和負數陣列進行基數排序。
4. 將已排序的負數陣列反轉，並還原其負號。
5. 最後將排序好的負數陣列與正數陣列合併。

## 2. 實作策略與程式碼 (Implementation & Code)

以下實作展示了如何使用計數排序作為子程序來實現基數排序，並包含了處理負數的邏輯。

```cpp
class Solution {
public:
    vector<int> sortArray(vector<int>& nums) {
        // 1. 分離正負數
        vector<int> nonnegatives;
        vector<int> negatives;
        for (auto num: nums) {
            if (num < 0) {
                negatives.push_back(-num); // 將負數轉為正數處理
            } else {
                nonnegatives.push_back(num);
            }
        }

        // 2. 分別對兩組數進行基數排序
        radixSort(nonnegatives);
        radixSort(negatives);

        // 3. 合併結果
        // 將排序好的負數陣列反轉並還原符號
        for (auto& num: negatives) {
            num = -num;
        }
        std::reverse(begin(negatives), end(negatives));

        // 將正數陣列附加到負數陣列後面
        negatives.insert(negatives.end(), nonnegatives.begin(), nonnegatives.end());

        return negatives;
    }

private:
    // 基數排序主體
    void radixSort(vector<int>& nums) {
        if (nums.empty()) return;

        // 找到最大值以決定迭代次數
        const int max_val = *max_element(nums.begin(), nums.end());

        // 從個位數開始，對每一位進行計數排序
        // ❗ 注意：placeValue 必須使用 long 以避免在處理最大整數時溢位
        // 例如，當 placeValue 為 1,000,000,000 時，下一次乘以 10 會超出 32 位元整數的範圍。
        for (long placeValue = 1; 1L * max_val / placeValue > 0; placeValue *= 10) {
            countingSort(nums, placeValue);
        }
    }

    // 針對特定位數的穩定計數排序
    void countingSort(vector<int>& nums, const long placeValue) {
        vector<int> counting(10, 0); // 數字範圍是 0-9

        // 計算當前位數的頻率 (0-9)
        for (auto num: nums) {
            counting[(num / placeValue) % 10]++;
        }

        // 計算前綴和，以確定每個數字的結尾位置
        for (int i = 1; i < 10; i++) {
            counting[i] += counting[i - 1];
        }

        // 從後向前遍歷，以保證穩定性
        vector<int> sorted(nums.size());
        for (int i = nums.size() - 1; i >= 0; i--) {
            const int digit = (nums[i] / placeValue) % 10;
            sorted[counting[digit]] = nums[i];
            counting[digit]--;
        }

        // 將排序好的結果放回原陣列
        swap(nums, sorted);
    }
};
```

## 3. 屬性 (Properties)

- **穩定性 (Stability)**：基數排序是**穩定**的。其穩定性完全依賴於其內部使用的排序演算法（在此為計數排序）是穩定的。
- **原地性 (In-Place)**：基數排序**不是原地**的，因為其子程序計數排序需要 `O(n + k)` 的額外空間。

## 4. 複雜度與實務考量 (Complexity & Practical Considerations)

### 複雜度分析

- **時間複雜度: O(d \* (n + k))**

  - `d` 是最大元素的位數。
  - `n` 是輸入陣列的大小。
  - `k` 是單一位數的範圍（基數，在此為 10）。
  - 由於 `k` 通常是一個小常數，時間複雜度常簡化為 **O(d \* n)**。

- **空間複雜度: O(n + k)**
  - 主要由計數排序的空間開銷決定，需要一個大小為 `n` 的臨時陣列和一個大小為 `k` 的計數陣列。

## 5. 挑戰性問題討論 (Discussion on Challenging Questions)

### Q1. 這個 Radix Sort 適合用在數值範圍很大，但元素數量很小的情境嗎？

不適合。
Radix Sort 的效率依賴於最大值的**位數 (d)**。若最大值非常大（例如 `2^31 - 1`，約 10 位數），演算法就需要執行 10 輪計數排序。如果此時元素數量 `n` 很小（例如只有 5 個），那麼執行 10 次 `O(n+k)` 的成本遠高於一次 `O(n log n)` 的比較排序。在這種情況下，`std::sort` 通常會快得多。

### Q2. 什麼情況下你會不選用 Radix Sort？

1. **數值範圍過大**：導致位數 `d` 過多，使得 `d*n` 的成本超過 `n log n`。
2. **元素數量太小**：如 Q1 所述，此時比較排序的總開銷更低。
3. **資料類型非整數**：標準的基數排序不適用於浮點數或字串（儘管有變體可以處理）。
4. **對 Cache 效率敏感的系統**：基數排序在每一輪都需要完整遍歷資料，可能會導致 Cache Miss，效能不如一些 Cache-friendly 的演算法。

### Q3. Radix Sort 可否做到 O(1) space？

不行。
基數排序的正確性依賴於其子排序演算法的**穩定性**。要實現穩定的計數排序，必然需要一個額外的陣列來暫存排序結果，因此空間複雜度至少是 `O(n + k)`。

### Q4. LeetCode 要求線性時間排序，但數值範圍很大 (k >> n)，該用 Counting Sort 還是 Radix Sort？

**答案：絕對應該選擇 Radix Sort。**

這是一個經典的權衡場景，完美展現了 Radix Sort 的設計動機。

- **Counting Sort 的困境**：
  - 時間複雜度為 `O(n + k)`。
  - 當 `k` 非常大而 `n` 很小時，複雜度由 `k` 主導，趨近於 `O(k)`。這不僅不是線性時間（相對於 `n`），而且由於需要建立一個巨大的計數陣列，會導致嚴重的時間和空間浪費。

- **Radix Sort 的優勢**：
  - 時間複雜度為 `O(d * (n + k'))`，其中 `k'` 是基數（例如 10），`d` 是最大值的位數。
  - 它巧妙地將一個巨大的 `k` 問題分解成 `d` 個 `k'` 極小的問題。
  - 對於一個 32 位元整數，最大值約為 `2*10^9`，所以 `d` 最多約為 10。
  - 因此，時間複雜度變為 `O(10 * (n + 10))`，實質上是 `O(n)`。

**結論**：在被要求線性時間排序，但數值範圍 `k` 遠大於元素數量 `n` 的情況下，Radix Sort 是唯一可行的選擇。它透過分位處理，將對 `k` 的依賴轉化為對 `d` 的依賴，從而實現了真正的（相對於 `n` 的）線性時間複雜度。
