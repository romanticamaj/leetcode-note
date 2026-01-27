# Subset Sum Problem 實作指南

本文檔詳細說明如何用動態規劃解決 Subset Sum 問題，包括從 2D DP 到 1D 空間優化的完整推導。

---

## 1. 標準 Subset Sum 問題

### 問題描述

給定一個正整數陣列和目標和 `target`，判斷是否存在子集使得子集和等於 `target`。

### 1.1 定義狀態

**狀態定義：**

```
dp[i][s] = 使用前 i 個數字，能否湊出和為 s
```

**答案：** `dp[n][target]`

### 1.2 狀態轉移

對於第 i 個數字 `nums[i-1]`，有兩種選擇：

1. **不選：** `dp[i][s] = dp[i-1][s]`
2. **選：** `dp[i][s] = dp[i-1][s - nums[i-1]]` (若 s >= nums[i-1])

**轉移方程：**

```
dp[i][s] = dp[i-1][s] OR dp[i-1][s - nums[i-1]]
```

### 1.3 初始化

```cpp
dp[0][0] = true;  // 不選任何數字，和為 0
dp[0][s] = false; // 對於 s > 0，無法湊出
```

### 1.4 實作 (2D DP)

```cpp
bool canPartition(vector<int>& nums, int target) {
    int n = nums.size();
    vector<vector<bool>> dp(n + 1, vector<bool>(target + 1, false));

    // 初始化
    dp[0][0] = true;

    // 填表
    for (int i = 1; i <= n; i++) {
        for (int s = 0; s <= target; s++) {
            // 不選 nums[i-1]
            dp[i][s] = dp[i-1][s];

            // 選 nums[i-1]
            if (s >= nums[i-1]) {
                dp[i][s] = dp[i][s] || dp[i-1][s - nums[i-1]];
            }
        }
    }

    return dp[n][target];
}
```

**時間複雜度：** O(n × target)  
**空間複雜度：** O(n × target)

---

## 2. 空間優化：Rolling Array (1D DP)

### 核心觀察

狀態轉移只依賴於「前一行」的數據：

```
dp[i][s] 只依賴 dp[i-1][s] 和 dp[i-1][s - nums[i-1]]
```

因此可以用一維陣列滾動更新。

### 2.1 為什麼必須倒序遍歷？

**關鍵：** 避免重複選取同一個元素。

#### 正序遍歷的問題 (錯誤)

```cpp
for (int s = 0; s <= target; s++) {
    if (s >= nums[i])
        dp[s] = dp[s] || dp[s - nums[i]];
}
```

**問題分析：**

假設 `nums[i] = 5`，當更新 `dp[10]` 時：

```
dp[10] = dp[10] || dp[10 - 5]
       = dp[10] || dp[5]
```

但此時 `dp[5]` 已經在同一輪中被更新過（包含了 nums[i]），因此 `dp[10]` 會**重複使用** `nums[i]`。

#### 倒序遍歷的正確性 (正確)

```cpp
for (int s = target; s >= nums[i]; s--) {
    dp[s] = dp[s] || dp[s - nums[i]];
}
```

**正確性分析：**

當更新 `dp[10]` 時：

```
dp[10] = dp[10] || dp[10 - 5]
       = dp[10] || dp[5]
```

此時 `dp[5]` **尚未在本輪更新**，仍是「上一輪（即 i-1）」的值，因此保證了 `nums[i]` 只被使用一次。

### 2.2 實作 (1D DP)

```cpp
bool canPartition(vector<int>& nums, int target) {
    vector<bool> dp(target + 1, false);
    dp[0] = true;

    for (int num : nums) {
        for (int s = target; s >= num; s--) {
            dp[s] = dp[s] || dp[s - num];
        }
    }

    return dp[target];
}
```

**時間複雜度：** O(n × target)  
**空間複雜度：** O(target) ✅

---

## 3. 關鍵技巧總結

### 3.1 識別 Subset Sum 的信號

1. **選或不選**：每個元素只能用一次
2. **子集和**：需要湊出特定的和
3. **約束條件**：通常有 sum 的範圍限制

### 3.2 實作檢查清單

- [ ] 確認 Constraints（sum 的範圍）
- [ ] 檢查邊界條件（sum % 2, abs(target) > sum）
- [ ] 確定 DP 類型（判定型 bool / 計數型 int）
- [ ] **倒序遍歷** 內層迴圈（1D 優化）
- [ ] 正確初始化 `dp[0]`

### 3.3 常見錯誤

| 錯誤             | 後果             | 修正                    |
| ---------------- | ---------------- | ----------------------- |
| 正序遍歷         | 重複選取同一元素 | 改為倒序                |
| 忘記檢查 sum % 2 | 無解情況未處理   | 提前返回 0/false        |
| dp[0] 初始化錯誤 | 整個 DP 表失效   | 判定型: true, 計數型: 1 |

---

## 4.. 延伸閱讀

- **理論背景**: [`01-Subset_Sum_and_NP_Completeness.md`](01-Subset_Sum_and_NP_Completeness.md)
- **變形題整理**: [`../../../Checklists/Trick Practice/Knapsack_Variations_Playbook.md`](../../../Checklists/Trick%20Practice/Knapsack_Variations_Playbook.md)
- **狀態設計原則**: [`../State_Design/01-Essentials.md`](../State_Design/01-Essentials.md)
