# 2. Three Sum (三數之和)

## 1. 問題定義

`Three Sum` 是 `Two Sum` 問題的延伸，要求在一個整數數組中，找出所有總和為零 (`a + b + c = 0`) 且不重複的三元組 (triplets)。

---

## 2. 從暴力法到 O(n²)

一個直觀的暴力解法是使用三層迴圈，遍歷所有可能的三元組組合，時間複雜度為 O(n³)，這在大部分情況下是無法接受的。

為了優化，我們可以將其降維。如果我們先固定一個元素 `a`，問題就變成在剩餘的數組中尋找一對和為 `-a` 的元素 (2-Sum 問題)。這可以將時間複雜度降至 O(n²)。

### 理論上的 O(n²) 解法

- **基於雜湊表**: 遍歷每對 `(S[i], S[j])`，然後在 O(1) 時間內查找補數 `-(S[i] + S[j])` 是否存在於預先填充的雜湊表中。
- **基於排序與雙指針**: 先對數組排序 (O(n log n))。然後，固定一個元素 `a`，在剩餘的排序子數組上使用雙指針，可在 O(n) 時間內找到配對。總體為 O(n²)。

---

## 3. LeetCode 實戰：處理重複項

經典的理論解法通常假設元素唯一。然而，LeetCode 的核心挑戰在於：

1. 輸入數組可能包含**重複數字**。
2. 輸出結果不能包含**重複三元組**。

為此，我們需要一個更穩健的策略。

### 通用策略：排序 + 降維打擊 + 去重

1. **排序 (Sort)**：對整個數組進行排序是解決去重問題的基礎。
2. **降維 (Reduce to 2-Sum)**：遍歷排序後的數組，每次固定一個元素 `nums[k]`。
3. **高效去重 (Duplicate Prevention)**：在遍歷 `k` 和解決 2-Sum 子問題時，跳過所有重複的元素。

---

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
                    ans.push_back({nums[k], nums[left--], nums[right++]});
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

---

### 解法二: 排序 + 滾動雜湊表

此方法同樣利用排序來處理重複問題，但在 2-Sum 部分改用雜湊表，以空間換取可能的查找效率。

#### C++ 實現

```cpp
class Solution {
    vector<vector<int>> ans;
public:
    vector<vector<int>> threeSum(vector<int>& nums) {
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

- **時間複雜度**: O(n log n) + O(n²) = **O(n²)**
- **空間複雜度**: O(log n) + O(n) = **O(n)**，`HashSet` 在內層循環最壞情況下需要 O(n) 空間。
