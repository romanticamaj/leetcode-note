# Kadane's Pattern DP

## 🧠 核心哲學

定義 `dp[i]` 必須包含位置 `i` 的元素，不包含則為 0 或 invalid。

這是 **Kadane's Algorithm 的底層模式**，將「必須包含當前元素」推廣到各種 DP 問題。

強制包含的要求使得：

1. 子序列可透過串接延續
2. dp 值可用於結構導航
3. 可跳躍至配對元素位置

## Kadane's Pattern 的本質

```cpp
// Kadane's 經典形式
dp[i] = max(nums[i], dp[i-1] + nums[i])
//      重置        延續累積
//      ↑ 不包含前項 → 從 i 重新開始
//      ↑ 但必須包含 nums[i]

// 空間優化版（滾動變數）
current = max(nums[i], current + nums[i])
```

**關鍵理解**：

- **Kadane's Pattern** = `dp[i]` 必須包含位置 `i` 的元素
- **Kadane's Algorithm** = 連續子陣列問題的 O(1) 空間實現
- 其他問題（如 LC 32）同樣遵循此 pattern，但需完整 dp 陣列

詳見：[Kadane_Algorithm.md](./Kadane_Algorithm.md)

## 核心技巧：用 dp 值導航結構

**定義**: `dp[i] = s[i] 結尾且必須包含 s[i] 的最優解`

若 `s[i]` 不在解中 → `dp[i] = 0`

```cpp
// 關鍵：透過 dp 值跳過已處理的部分
int match_pos = i - 1 - dp[i-1];  // 跳過已配對的區段
if (s[match_pos] matches s[i]) {
    dp[i] = dp[match_pos-1] + 2 + dp[i-1];  // 串接三段
}
```

## 🧩 實例：LeetCode 32 Longest Valid Parentheses

**State**: `dp[i] = s[i] 結尾的最長合法括號長度，且必須包含 s[i]`

**Recurrence**:

- **Case 1**: `s[i] == '('` → `dp[i] = 0`（左括號無法作為合法括號的結尾）

- **Case 2**: `s[i] == ')'` → 檢查能否配對：

  - **Subcase 2a**: `s[i-1] == '('` → 直接配對 `"()"`

    - `dp[i] = dp[i-2] + 2`（串接前段 + 新配對）

  - **Subcase 2b**: `s[i-1] == ')'` → 用 `dp[i-1]` 跳過已配對部分
    - 計算左括號位置：`j = i - 1 - dp[i-1]`
    - 若 `j >= 0` 且 `s[j] == '('` → 可配對
    - `dp[i] = dp[j-1] + 2 + dp[i-1]`
      - `dp[j-1]`: 左括號前段
      - `2`: 新配對的左右括號
      - `dp[i-1]`: 已經配對的中段

**關鍵技巧**: 用 `dp[i-1]` 的值直接跳過已配對的區段，O(1) 定位到應該配對的左括號位置

## 對比：Optional Inclusion State

| Aspect   | Kadane's Pattern | Optional (傳統 LIS)     |
| -------- | ---------------- | ----------------------- |
| 定義     | dp[i] 必含 s[i]  | dp[i] = 前 i 元素最優解 |
| 不符條件 | dp[i] = 0        | dp[i] = dp[i-1]         |
| 導航     | 可用 dp 值跳躍   | 需額外信息              |
| 串接     | 直接加總 dp 值   | 需比較取 max            |

## 適用場景

- **配對結構問題**: 括號、標籤配對
- **必須使用當前元素**: 結尾位置有意義
- **需要結構導航**: 用 dp 值定位配對元素
- **區段串接**: 多段合法子序列合併

## ⏱️ 複雜度

| Aspect | Complexity | Note                           |
| ------ | ---------- | ------------------------------ |
| Time   | O(n)       | 單次遍歷，透過 dp 值 O(1) 導航 |
| Space  | O(n)       | dp 陣列                        |

## ✅ 關鍵要點

- [ ] **State 必須包含當前元素** - 這是能串接的關鍵
- [ ] **用 dp 值導航** - `i - dp[i-1]` 跳至配對位置
- [ ] **三段串接公式** - `dp[before] + 2 + dp[middle]`
- [ ] **不符條件設為 0** - 中斷而非繼承前值
