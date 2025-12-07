# 🎯 Kadane's Pattern DP - 練習路徑

Kadane's Pattern DP 核心是「`dp[i]` 必須包含位置 `i` 的元素」，不包含則為 0 或無效。

這是將 **Kadane's Algorithm 的思維模式** 推廣到各種 DP 問題的設計哲學。

這個強制要求使得子序列可透過串接延續，並能用 dp 值導航結構。

詳細心法請參考：[Kadanes_Pattern_DP.md](../Algorithms/Dynamic_Programming/Advanced_Techniques/Kadanes_Pattern_DP.md)

## 💡 Kadane's Pattern 的本質

```cpp
// Kadane's 經典形式
dp[i] = max(nums[i], dp[i-1] + nums[i])
//      重置        延續
//      ↑ 必須包含 nums[i]，但可選擇是否包含前項
```

- **Kadane's Pattern** = `dp[i]` 必須包含位置 `i` 的狀態定義
- **Kadane's Algorithm** = 連續子陣列問題的 O(1) 空間優化實現
- 其他問題（如 LC 32）同樣遵循此 pattern，但需完整 dp 陣列

---

## 🏁 目標題總覽

| 題號   | 題目名稱                            | Pattern 特徵             | 難度   |
| ------ | ----------------------------------- | ------------------------ | ------ |
| LC 32  | Longest Valid Parentheses           | 用 dp 值跳躍找配對       | ⭐⭐⭐ |
| LC 53  | Maximum Subarray                    | 連續子陣列，Kadane's     | ⭐⭐   |
| LC 300 | Longest Increasing Subsequence      | 子序列串接，經典 LIS     | ⭐⭐   |
| LC 152 | Maximum Product Subarray            | 追蹤 max/min，乘積特性   | ⭐⭐   |
| LC 718 | Maximum Length of Repeated Subarray | 2D 狀態，必須結尾於 i,j  | ⭐⭐   |
| LC 139 | Word Break                          | 字串必須結尾於 i         | ⭐⭐   |
| LC 5   | Longest Palindromic Substring       | 中心擴展 or 區間 DP      | ⭐⭐   |
| LC 413 | Arithmetic Slices                   | 等差數列，必須包含 i     | ⭐⭐   |
| LC 647 | Palindromic Substrings              | 計數版回文，必須包含中心 | ⭐⭐   |
| LC 91  | Decode Ways                         | 解碼必須結尾於 i         | ⭐⭐   |

---

## 🧭 練習路徑（依 Pattern 變體）

### 1️⃣ 基礎連續子陣列（Contiguous Subarray）

**核心概念**：`dp[i]` 必須包含 `nums[i]` 作結尾，連續性自然滿足

- 📙 **LC 53. Maximum Subarray** ← 入門：Kadane's algorithm，最基礎的 pattern

  - State: `dp[i] = 必須包含 nums[i] 的最大和`
  - Recurrence: `dp[i] = max(nums[i], dp[i-1] + nums[i])`

- 📙 **LC 152. Maximum Product Subarray** ← 進階：需追蹤 max 和 min（負負得正）

  - State: `max_dp[i], min_dp[i]` 必須包含 `nums[i]`
  - Key: 負數會翻轉 max/min

- 📙 **LC 413. Arithmetic Slices** ← 變體：等差數列計數
  - State: `dp[i] = 必須包含 nums[i] 的等差數列個數`

### 2️⃣ 子序列串接（Subsequence Chaining）

**核心概念**：可跳躍，需檢查所有可串接的前項

- 📙 **LC 300. Longest Increasing Subsequence** ← 經典：掃描前項找最長可串接

  - State: `dp[i] = 必須包含 nums[i] 的 LIS 長度`
  - Recurrence: `dp[i] = max(dp[j] + 1)` for all `j < i` where `nums[j] < nums[i]`
  - 優化：Binary Search + Patience Sorting

- 📙 **LC 646. Maximum Length of Pair Chain** ← LIS 變體：配對串接
  - 先排序，再用 LIS 思路

### 3️⃣ 配對結構導航（Matching Structure Navigation）

**核心概念**：用 `dp[i]` 值跳躍定位配對元素

- 📕 **LC 32. Longest Valid Parentheses** ← 終極：用 `i - dp[i-1]` 跳至左括號
  - State: `dp[i] = 必須包含 s[i] 的最長合法括號長度`
  - Key: 三段串接 `dp[j-1] + 2 + dp[i-1]`
  - Navigation: `j = i - 1 - dp[i-1]`

### 4️⃣ 字串分拆（String Breaking）

**核心概念**：必須結尾於位置 `i`，檢查往前的所有可能切點

- 📙 **LC 139. Word Break** ← 入門：結尾必須是合法單字

  - State: `dp[i] = s[0..i) 能否分拆`（i 是分拆結束位置）
  - Recurrence: `dp[i] = any(dp[j] && s[j..i) in dict)` for `j < i`

- 📙 **LC 91. Decode Ways** ← 變體：解碼方式計數
  - State: `dp[i] = 必須結尾於 i 的解碼方式數`

### 5️⃣ 2D 狀態必須包含（2D Kadane's Pattern）

**核心概念**：兩個序列同時必須包含當前位置

- 📙 **LC 718. Maximum Length of Repeated Subarray** ← 2D 連續子陣列

  - State: `dp[i][j] = 必須包含 A[i], B[j] 的最長公共子陣列`
  - Recurrence: `dp[i][j] = dp[i-1][j-1] + 1` if `A[i] == B[j]`

- 📙 **LC 1143. Longest Common Subsequence** ← 2D 子序列（對比：LCS 通常用 optional）
  - 可用 Kadane's Pattern 變體理解

### 6️⃣ 回文結構（Palindrome Structure）

**核心概念**：中心擴展或區間 DP，必須包含特定位置

- 📙 **LC 5. Longest Palindromic Substring** ← 中心擴展 or 區間 DP

  - Approach 1: 中心必須在 `i` 或 `i,i+1` 之間
  - Approach 2: `dp[i][j]` 表示 `s[i..j]` 是否回文

- 📙 **LC 647. Palindromic Substrings** ← 計數版，同樣概念

---

## ✅ 建議練習順序

### 階段 1：基礎肌肉記憶（1-2 天）

1. **LC 53** → 最基礎的 Kadane's，理解「必須包含」vs「可選包含」
2. **LC 300** → 經典 LIS，學會掃描前項找可串接者
3. **LC 139** → 字串分拆，練習「結尾必須合法」

### 階段 2：變體與進階（2-3 天）

4. **LC 152** → 需追蹤雙狀態（max/min）
5. **LC 718** → 2D 版本，兩序列同時包含
6. **LC 91** → 解碼計數，類似 Word Break

### 階段 3：結構導航終極挑戰（1-2 天）

7. **LC 32** → 用 dp 值跳躍，三段串接，最經典的技巧展示

### 可選進階題

- **LC 413, LC 646, LC 647, LC 5** → 根據興趣和時間選做

---

## 🔑 Pattern 識別關鍵字

遇到以下關鍵字，考慮 Kadane's Pattern DP：

- ✅ "以 i 結尾" / "ending at i"
- ✅ "包含 nums[i]" / "containing element at i"
- ✅ "連續子陣列" / "contiguous subarray"
- ✅ 子序列需要「串接」前項
- ✅ 配對結構（括號、標籤）
- ✅ 字串分拆必須完整消費到位置 i

---

## 💡 關鍵心法總結

1. **強制包含** → 不符條件直接設為 0，不繼承前值
2. **串接延續** → `dp[i]` 可直接加總，無需比較
3. **結構導航** → 用 `dp[i]` 值跳躍定位關鍵元素
4. **最終答案** → `max(dp)` 而非 `dp[n]`

這份路徑涵蓋了 Kadane's Pattern DP 的所有核心變體，從最基礎的 Maximum Subarray 到最經典的配對結構導航，幫助你系統性建立這個重要的 DP 思維模式。
