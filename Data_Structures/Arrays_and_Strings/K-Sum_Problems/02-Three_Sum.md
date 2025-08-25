# 2. Three Sum (三數之和)

3Sum 問題是 2Sum 問題的延伸，要求在一個數組中找出所有總和為零且不重複的三元組 (triplets)，這使其在算法設計上增加了額外的複雜度。

## 可達最佳運行時間 (BCR) 分析

在設計算法前，評估其理論上的最佳運行時間 (Best Conceivable Runtime, BCR) 是重要的第一步。

- **Two Sum (未排序)**: 使用雜湊表可在 O(n) 時間內找到解。
- **Two Sum II (已排序)**: 使用雙指針法同樣可在 O(n) 時間內完成。若對未排序數組先進行排序，總體時間複雜度為 O(n log n)。

鑑於 3Sum 問題比 2Sum 多了一個維度（需要尋找第三個數），一個直觀的推論是，在 O(n²) 的時間複雜度內求解是合理且高效的目標。

---

## 經典 O(n²) 算法理論

### 基於雜湊表的平均情況 O(n²) 解法

在整數計算模型中，一種平均情況下為 O(n²) 的解法是：

1. 將數組中的每個數字 `S[i]` 插入一個雜湊表。
2. 對於每對索引 `(i, j)`，檢查雜湊表中是否存在補數 `-(S[i] + S[j])`。

### 基於排序與雙指針的最壞情況 O(n²) 解法

在不允許使用雜湊的計算模型中（如純比較模型），可以透過以下算法達到最壞情況 O(n²) 的時間複雜度。此方法避免了對每對組合進行二分搜索的需要。(因為要使用雙指針，所以必須先排序)

**偽代碼：**

> **注意**: 以下偽代碼假設輸入數組中的元素是唯一的。

```
sort(S);
for i from 0 to n - 2 do
    a = S[i];
    start = i + 1;
    end = n - 1;
    while (start < end) do
        b = S[start];
        c = S[end];
        if (a + b + c == 0) then
            output a, b, c;
            // 找到一組解後，繼續尋找其他可能的組合
            start = start + 1;
            end = end - 1;
        else if (a + b + c > 0) then
            // 和太大，需減小總和
            end = end - 1;
        else
            // 和太小，需增大總和
            start = start + 1;
        end
    end
end
```

---

## LeetCode 實戰策略與 C++ 解決方案

在 LeetCode 的實戰中，我們需要處理輸入數組包含重複數字，且輸出結果不能包含重複三元組的邊界情況。

### 解法一: 排序 + 雙指針 (Sort + Two Pointers)

這是最經典且高效的解法，空間複雜度最優。

#### 核心策略

1. **排序 (Sort)**：對數組進行排序是所有後續操作的基礎，時間複雜度為 O(n log n)。
2. **固定一點 + 雙指針 (Fix one element + Two Pointers)**：遍歷數組，每次固定一個元素 `nums[k]`，然後在剩餘的 `[k+1, n-1]` 區間內使用雙指針法尋找和為 `-nums[k]` 的兩個元素。
3. **去重 (Duplicate Prevention)**：在固定 `k` 以及移動 `left`/`right` 指針時，必須跳過所有重複的元素，以確保最終結果的唯一性。

#### C++ 解決方案 (雙指針)

```cpp
class Solution {
public:
    vector<vector<int>> threeSum(vector<int>& nums) {
        vector<vector<int>> ans;
        const int n = nums.size();
        if (n < 3) return ans; // 長度不足，不可能有三元組

        // 1. 排序是雙指針法的基礎
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
                    ans.push_back({nums[k], nums[left++], nums[right--]});

                    // 3. 找到解後，對左右指針進行去重
                    while (left < right && nums[left] == nums[left - 1]) left++;
                    while (left < right && nums[right] == nums[right + 1]) right--;
                } else if (sum < 0) {
                    left++;
                } else {
                    right--;
                }
            }
        }
        return ans;
    }
};
```

### 解法二: 排序 + 滾動雜湊表 (Sort + Rolling Hash Map)

此方法同樣利用排序來處理重複問題，但在尋找 `twoSum` 的部分改用雜湊表。

#### 核心策略

1. **排序 (Sort)**: 同樣先對數組排序，以便於去重。
2. **固定一點 + 滾動雜湊表 (Fix one element + Rolling Hash Map)**: 遍歷數組固定 `nums[k]`，然後在 `[k+1, n-1]` 的範圍內，使用滾動雜湊表的方法尋找 `twoSum` 的解。
3. **去重 (Duplicate Prevention)**:
   - 外層循環透過 `if (k > 0 && nums[k] == nums[k - 1])` 來跳過重複的 `k`。
   - 內層循環在找到一個解後，需要手動跳過所有與 `nums[i]` 相等的後續元素，以避免因 `nums[i]` 重複而產生重複的三元組。

#### C++ 解決方案 (滾動雜湊表)

```cpp
class Solution {
    vector<vector<int>> ans;

public:
    vector<vector<int>> threeSum(vector<int>& nums) {
        const int n = nums.size();
        if (n < 3) return ans;

        std::sort(begin(nums), end(nums)); // 仍必須排序，確保 search space 可以達成無重覆

        for (int k = 0; k < n - 2; k++) {
            if (nums[k] > 0) break; // 優化：提前終止
            if (k > 0 && nums[k] == nums[k - 1]) continue; // 去重

            twoSumHashMap(nums, k);
        }

        return ans;
    }

    void twoSumHashMap(const vector<int>& nums, const int k) {
        const int n = nums.size();
        unordered_set<int> hashMap;

        int i = k + 1;

        while (i < n) {
            const int target = -nums[k] - nums[i];

            if (hashMap.contains(target)) {
                ans.push_back({nums[k], nums[i], target});

                // 關鍵：找到一個解後，必須跳過所有與當前 nums[i] 相等的後續元素
                while (i + 1 < n && nums[i + 1] == nums[i]) i++;
            }

            // 滾動雜湊表：將當前元素加入 set
            hashMap.insert(nums[i++]);
        }
    }
};
```

#### 算法思路總結

```
// Leetcode 提示:
// Two-Sum 的第二種思路是，在不改變數組的情況下，
// 我們能否使用額外的空間？例如使用雜湊表來加速查找？

// 算法流程 (排序 + 雜湊表):
// 1. 排序 -> 排序是為了方便消除重複項。
// 2. 邊建構邊查找 -> 對於每個固定的 <nums[k], k>，
//    在搜索空間 [k + 1, n - 1] 中查找補數 -nums[k] - nums[i]。
```
