# 計數排序 (Counting Sort)

## 1. 核心概念與分區 (Concept & Partition)

計數排序是一種**非比較排序 (Non-Comparison Sort)** 演算法，它不透過比較元素大小來排序，而是利用**鍵 (key)** 的特性。其核心思想是統計每個獨立鍵值出現的次數，然後利用這些次數來計算每個元素在最終排序後的位置。

**核心假設**：輸入的元素必須是**整數**，且這些整數的範圍 `k` (最大值 - 最小值) 不能過大。

演算法邏輯上使用一個**計數陣列 (Counting Array)**，可視為一個直方圖 (Histogram)，來完成分區與計數：

1. **計數 (Counting)**：遍歷輸入陣列，將每個元素的值作為索引，在計數陣列中對應的位置上記錄其出現次數。
2. **計算位置 (Calculating Positions)**：對計數陣列進行處理（通常是計算前綴和），使其能夠直接反映出每個元素在輸出陣列中的最終位置。
3. **放置 (Placing)**：遍歷輸入陣列，根據計數陣列提供的資訊，將每個元素放置到輸出陣列的正確位置上。

## 2. 實作策略與程式碼 (Implementation & Code)

計數排序的關鍵在於如何利用計數陣列來確定最終位置。以下介紹兩種常見的實作方式。

### 作法一：使用起始索引 (Starting Index Trick)

此方法將計數陣列從「頻率圖」轉換為「起始索引圖」。

1. **計數**：計算每個數字的出現頻率。
2. **轉換為起始索引**：透過一次遍歷，將計數陣列 `counting[i]` 的值更新為數字 `i` 在排序後陣列中的起始索引。
3. **放置**：遍歷原始陣列，根據起始索引圖將數字放入新陣列，並更新該數字的下一個可用起始索引。

#### C++ 實作範例

```cpp
class Solution {
public:
    vector<int> sortArray(vector<int>& nums) {
        // 處理 LeetCode 的邊界情況
        const int min_val = -5 * 1e4;
        const int max_val = 5 * 1e4;
        const int k = max_val - min_val;

        vector<int> counting(k + 1, 0);

        // 1. 計數，num - min_val 是為了處理負數，將其平移到 0 開始的索引
        for (auto num: nums) {
            counting[num - min_val]++;
        }

        // 2. 將計數陣列轉換為起始索引陣列
        int startingIndex = 0;
        for (int i = 0; i <= k; i++) {
            int count = counting[i];      // 保存當前數字的計數
            counting[i] = startingIndex;  // 更新為該數字的起始位置
            startingIndex += count;       // 為下一個數字計算起始位置
        }

        // 3. 根據起始索引，將元素放入 sorted 陣列
        // 正向遍歷，放置元素以維持穩定性
        vector<int> sorted(nums.size());
        for (auto num: nums) {
            int& place_idx = counting[num - min_val];
            sorted[place_idx] = num;
            place_idx++; // 更新該數字的下一個放置位置
        }

        return sorted;
    }
    // 時間複雜度: O(n + k)
    // 空間複雜度: O(k)
};
```

### 作法二：使用前綴和作為結尾索引 (Prefix Sum as End-Index)

此方法更接近 CLRS 教科書中的經典實現，它利用前綴和來確定每個元素在排序後的位置**上限**。

1. **計數**：同上。
2. **計算前綴和**：`counting[i]` 的值變為「小於或等於 `i` 的元素總數」。
3. **反向放置**：**從後向前**遍歷原始陣列，根據前綴和計算出的索引（需減一）放置元素，並更新計數。

#### C++ 實作範例

```cpp
class Solution {
public:
    vector<int> sortArray(vector<int>& nums) {
        if (nums.empty()) return {};

        const int min_val = *min_element(nums.begin(), nums.end());
        const int max_val = *max_element(nums.begin(), nums.end());
        const int k = max_val - min_val;
        vector<int> counting(k + 1, 0);

        // 1. 計數
        for (auto num: nums) {
            counting[num - min_val]++;
        }

        // 2. 計算前綴和，counting[i] 表示 <= i 的元素個數
        for (int i = 1; i <= k; i++) {
            counting[i] += counting[i - 1];
        }

        // 3. 反向遍歷，放置元素以維持穩定性
        vector<int> sorted(nums.size());
        for (int i = nums.size() - 1; i >= 0; i--) {
            int num = nums[i];
            int& count_idx = counting[num - min_val];
            sorted[count_idx - 1] = num; // -1 是因為前綴和是1-based計數，需轉為0-based索引
            count_idx--; // 將下一個相同元素的放置位置前移
        }

        return sorted;
    }
};
```

## 3. 穩定性與 CLRS 版本分析 (Stability & CLRS Version Analysis)

為什麼 CLRS 版本的計數排序在最後放置元素時，需要**從後向前**遍歷 (`for j = A.length downto 1`)？

**答案：這是為了保證排序的穩定性 (Stability)。**

穩定性是指當序列中存在相等元素時，排序後它們的原始相對順序保持不變。

#### CLRS 虛擬碼

為了方便討論，我們先看一下 CLRS 中的虛擬碼 (`A` 是輸入, `B` 是輸出, `k` 是最大值)。

```
COUNTING-SORT(A, B, k)
1  let C[0..k] be a new array
2  for i = 0 to k
3      C[i] = 0
4  for j = 1 to A.length
5      C[A[j]] = C[A[j]] + 1
6  // C[i] now contains the number of elements equal to i.
7  for i = 1 to k
8      C[i] = C[i] + C[i-1]
9  // C[i] now contains the number of elements less than or equal to i.
10 for j = A.length downto 1
11     B[C[A[j]]] = A[j]
12     C[A[j]] = C[A[j]] - 1
```

讓我們分析一下：

1. **前綴和的意義**：在計算完前綴和後（第 7-8 行），`C[i]` 的值代表「小於或等於 `i` 的元素」的總個數。這也意味著，值為 `i` 的元素在排序後的陣列中，其**最後一個**出現的位置應該是索引 `C[i] - 1` (如果從 0 開始計數) 或 `C[i]` (如果從 1 開始計數，如 CLRS)。

2. **從後向前遍歷 (維持穩定性)**：

   - 假設原始陣列中有兩個相等的元素 `A[x]` 和 `A[y]`，且 `x < y`。
   - 當我們從後向前遍歷時，會先處理 `A[y]`。我們將 `A[y]` 放置在 `sorted[C[A[y]] - 1]` 的位置，然後將 `C[A[y]]` 減一。
   - 接著處理 `A[x]`。此時 `C[A[x]]` 的值已經被 `A[y]` 的操作減了一，所以 `A[x]` 會被放置在 `A[y]` 的**前面一個**位置。
   - 因此，它們的原始相對順序 `x < y` 得以保持，排序是穩定的。

3. **如果從前向後遍歷 (會變得不穩定)**：
   - 如果從前向後遍歷，會先處理 `A[x]`。它會被放在 `sorted[C[A[x]] - 1]`。
   - 接著處理 `A[y]`，它會被放在 `A[x]` 的前面一個位置。
   - 這樣一來，它們的原始相對順序就被顛倒了，排序將變得不穩定。

## 4. 屬性 (Properties)

- **穩定性 (Stability)**：計數排序**可以是穩定的**，前提是採用類似 CLRS 的實現方式（從後向前放置元素）。
- **原地性 (In-Place)**：計數排序**不是原地 (not in-place)** 的，它需要一個大小為 `k` 的計數陣列和一個大小為 `n` 的輸出陣列。

## 5. 複雜度與實務考量 (Complexity & Practical Considerations)

### 複雜度分析

- **時間複雜度: O(n + k)**

  - `n` 是輸入陣列的大小。
  - `k` 是輸入元素的範圍 (`max - min + 1`)。
  - 演算法包含幾次線性掃描（計數、計算前綴和、放置），總時間與 `n` 和 `k` 的和成正比。

- **空間複雜度: O(n + k)**
  - 需要 `O(k)` 的空間來儲存計數陣列。
  - 需要 `O(n)` 的空間來儲存排序後的輸出陣列。

### 實務考量

- **適用場景**：當 `k` 的大小與 `n` 相當或更小時，計數排序非常高效，其線性時間複雜度優於任何基於比較的排序演算法 (如快速排序、合併排序的 `O(n log n)`)。
- **限制**：如果 `k` 非常大（例如，排序 64 位元整數），則計數陣列會過於龐大，導致空間複雜度不可接受。
- **基數排序 (Radix Sort)**：計數排序最常見的應用是作為**基數排序**的子程序，用來對數字的某一位進行排序。
