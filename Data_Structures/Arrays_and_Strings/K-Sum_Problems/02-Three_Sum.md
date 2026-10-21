# 2. Three Sum (三數之和)

## 1. 問題定義

`Three Sum` 是 `Two Sum` 問題的延伸，要求在一個整數數組中，找出所有總和為零 (`a + b + c = 0`) 且不重複的三元組 (triplets)。

### 🧠 先釐清輸入、輸出與「不重複」的意思

1. **輸入未排序（unsorted）**：不能預設任何大小順序；未排序也不代表數值服從某種隨機分布。若後續需要有序性，排序是解法主動加入的前處理。
2. **輸出是三個值的組合，不是三個 index**：index 用來確保取用三個不同位置；答案是否相同，要比較 value triplet，且忽略排列順序。
3. **不重複限制的是輸出組合，不是組合內的值**：相同值可來自不同位置並形成合法答案；不能先把輸入的重複值全部刪掉。

**合法性看 index，輸出去重看 value。** 先釐清這兩層，才知道哪些選擇必須保留、哪些重複工作可以跳過。

## 2. 從暴力法到 O(n²)

先建立正確的暴力法：枚舉 `i < j < k`，檢查三個值的和。這個順序保證位置不同，並避免重複枚舉同一組位置的排列；但不同位置組合仍可能產生相同的 value triplet，因此輸出去重還要另外處理。最壞時間為 O(n³)。

**先有完整、正確的枚舉，才容易看見要改善哪一層搜尋。** 固定兩個值後，第三個值已由補數決定，可用查表取代線性枚舉；或固定一個值，把剩餘問題轉成 target 為其相反數的 Two Sum，再利用排序與雙指標做線性搜尋。固定一個值本身不會自動降到 O(n²)，還要讓每輪 Two Sum 降到 O(n)。

推導順序：**釐清題意 → 正確暴力枚舉 → 找搜尋瓶頸 → 替換搜尋方式 → 驗證去重不漏解**。見 [Brute Force 關鍵設計](../../../Algorithms/Brute_Force/README.md)。

### 理論上的 O(n²) 解法

- **基於雜湊表**: 遍歷每對 `(S[i], S[j])`，以預期 O(1) 查詢補數；還須保證補數來自合法位置，例如記錄最右 index 並確認它 `> j`，不能只檢查值存在。
- **基於排序與雙指針**: 先對數組排序 (O(n log n))。然後，固定一個元素 `a`，在剩餘的排序子數組上使用雙指針，可在 O(n) 時間內找到配對。總體為 O(n²)。

## 3. LeetCode 實戰：處理重複項

部分教材版本假設值互異，另一些只問是否存在，與 LC 15 的列舉版本不同（見 [歷史與教材比較](../../../Problem_History/LC_0015_3Sum.md)）。LeetCode 的核心挑戰在於：

1. 輸入數組可能包含**重複數字**。
2. 輸出結果不能包含**重複三元組**。

為此，我們需要一個更穩健的策略。

### 通用策略：排序 + 降維打擊 + 去重

1. **排序 (Sort)**：讓相同值相鄰，方便以跳過連續相同值的方式去重；這是此處採用的策略，不代表所有解法都必須排序。
2. **降維 (Reduce to 2-Sum)**：遍歷排序後的數組，每次固定一個元素 `nums[k]`。
3. **高效去重 (Duplicate Prevention)**：固定值避免重複處理；內層依搜尋方式決定去重時機，保留相同值來自不同位置的合法配對機會。

## 4. 實作方法：2-Sum 子問題的兩種解法

基於上述通用策略，核心差異在於如何解決降維後的 2-Sum 子問題。

### 解法一: 排序 + 雙指針 (最優空間解)

此為最經典的解法，它將 2-Sum 部分也用雙指針實現，達到了最優的空間複雜度。

#### C++ 實現

```cpp
class Solution {
public:
    vector<vector<int>> threeSum(vector<int>& nums) {
        vector<vector<int>> ans;
        const int n = nums.size();
        if (n < 3) return ans;

        // 1. 排序是雙指針法的基礎，同時可以去重複
        std::sort(begin(nums), end(nums));

        // 2. 固定一個點 k，然後使用雙指針
        for (int k = 0; k < n - 2; k++) {
            // 優化：如果固定的數大於 0，後續不可能有和為 0 的組合
            if (nums[k] > 0) break;
            // 去重：跳過重複的起始點
            if (k > 0 && nums[k] == nums[k - 1]) continue;

            int left = k + 1;
            int right = n - 1;

            while (left < right) {
                const int sum = nums[k] + nums[left] + nums[right];

                if (sum == 0) {
                    ans.push_back({nums[k], nums[left], nums[right]});
                    left++;
                    right--;
                    // 3. 找到解後，對左右指針進行去重
                    while (left < right && nums[left] == nums[left - 1]) left++;
                    while (left < right && nums[right] == nums[right + 1]) right--;
                } else if (sum < 0) {
                    left++; // 和太小，左指針右移
                } else {
                    right--; // 和太大，右指針左移
                }
            }
        }
        return ans;
    }
};
```

#### 複雜度分析

- **時間複雜度**: O(n log n) + O(n²) = **O(n²)**
- **空間複雜度**: **O(log n)** 或 O(n)，取決於排序算法的實現。

### 解法二: 排序 + 滾動雜湊表

此方法同樣利用排序來處理重複問題，但在 2-Sum 部分改用雜湊表，以空間換取可能的查找效率。

#### C++ 實現

```cpp
class Solution {
    vector<vector<int>> ans;
public:
    vector<vector<int>> threeSum(vector<int>& nums) {
        ans.clear();
        const int n = nums.size();
        if (n < 3) return ans;

        std::sort(begin(nums), end(nums));

        for (int k = 0; k < n - 2; k++) {
            if (nums[k] > 0) break;
            if (k > 0 && nums[k] == nums[k - 1]) continue;

            twoSumHashMap(nums, k);
        }
        return ans;
    }
private:
    void twoSumHashMap(const vector<int>& nums, const int k) {
        const int n = nums.size();
        unordered_set<int> hashMap;

        for (int i = k + 1; i < n; ++i) {
            const int complement = -nums[k] - nums[i];
            if (hashMap.count(complement)) {
                ans.push_back({nums[k], complement, nums[i]});
                while (i + 1 < n && nums[i + 1] == nums[i]) i++;
            }
            hashMap.insert(nums[i]);
        }
    }
};
```

#### 複雜度分析

- **時間複雜度**: 雜湊操作為預期 O(1)，整體為**預期 O(n²)**。
- **空間複雜度**: O(log n) + O(n) = **O(n)**，`HashSet` 在內層循環最壞情況下需要 O(n) 空間。
