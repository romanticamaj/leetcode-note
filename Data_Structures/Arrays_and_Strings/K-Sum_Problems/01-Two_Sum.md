# 1. Two Sum (兩數之和)

本文件旨在探討「兩數之和」(Two Sum) 問題，此問題要求在一個數組中，找出兩個其值相加等於一特定目標值的元素的索引。

---

## 解法一：暴力法 (Brute Force)

此為最直觀的解法，通過檢查數組中所有可能的元素對來尋找答案。

- **時間複雜度**: O(n²) - 透過雙層 `for` 迴圈遍歷所有組合。
- **空間複雜度**: O(1) - 無需額外儲存空間。

---

## 優化解法 (O(n) 時間複雜度)

### 解法二：滾動雜湊表 (Rolling Hash Map)

此解法為處理**未排序**數組時的最佳選擇，利用雜湊表 O(1) 的查找效率，將時間複雜度降至線性。

#### 關鍵技巧：滾動式建構與查找

此策略的核心在於單次遍歷中動態地維護一個雜湊表。在迭代過程中，我們並非預先填充所有元素，而是**先查詢當前元素的補數（complement）是否存在於表中，若不存在，再將當前元素及其索引加入表中**。這種滾動式更新的模式，不僅能確保在一次遍歷中找到解答，也巧妙地避免了使用同一元素兩次的問題。

#### C++ 解決方案 (雜湊表)

```cpp
class Solution {
public:
    vector<int> twoSum(vector<int>& nums, int target) {
        // 使用雜湊表儲存數字及其索引
        unordered_map<int, int> hashMap; // Key: 數字, Value: 索引

        for (int i = 0; i < nums.size(); ++i) {
            // 計算當前數字的補數
            const int complement = target - nums[i];

            // 在雜湊表中查找補數
            if (hashMap.contains(complement)) {
                // 如果找到，返回補數的索引和當前數字的索引
                return {i, hashMap[complement]};
            }

            // 如果未找到補數，將當前數字和索引存入雜湊表
            hashMap[nums[i]] = i;
        }

        // 根據題目假設，必有解，此處僅為滿足函數返回類型
        return {};
    }

    // TIME: O(n) - 單次遍歷數組
    // SPACE: O(n) - 雜湊表最壞情況下需要儲存 n 個元素
};
```

### 解法三：雙指針 (Two Pointers on Sorted Array)

當輸入數組**已排序**時（例如 LeetCode 167. Two Sum II），雙指針法提供了空間複雜度最優的 O(1) 解決方案。

#### C++ 解決方案 (雙指針)

```cpp
class Solution {
public:
    vector<int> twoSum(vector<int>& numbers, int target) {
        // 初始化左右指針
        int left = 0;
        int right = numbers.size() - 1;

        while (left < right) {
            const int sum = numbers[left] + numbers[right];

            if (sum == target) {
                return {left, right};
            } else if (sum < target) {
                // 和太小，移動左指針以增大和
                left++;
            } else {
                // 和太大，移動右指針以減小和
                right--;
            }
        }

        // 根據題目假設，必有解
        return {};
    }

    // time: O(n) - 單次遍歷
    // space: O(1) - 僅使用常數額外空間
};
```
