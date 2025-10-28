# Expand Around Center 心法

## 🧠 核心哲學

將「檢查所有可能性」轉換為「枚舉中心點 + 向外擴展」：

- 枚舉 O(n) 個中心，每個向外擴展 → O(n²)
- 比區間枚舉 O(n²) × 檢查 O(n) = O(n³) 更優

## 核心概念：處理奇偶長度

### 為何需要兩種中心？

| 長度類型 | 中心     | 範例      | 初始位置     |
| -------- | -------- | --------- | ------------ |
| 奇數     | 單個字符 | "a**b**a" | `(i, i)`     |
| 偶數     | 兩字符間 | "abba"    | `(i, i + 1)` |

**標準做法**：每個位置枚舉兩次

- `expand(i, i)` - 奇數長度
- `expand(i, i + 1)` - 偶數長度

## 設計模式

### Pattern 1: 位置追蹤模式

```
global: longest, start, end

expand(left, right):
    while left >= 0 && right < n && s[left] == s[right]:
        left--, right++
    left++, right--  # 回退到有效位置

    if (right - left + 1) > longest:
        update(start, end)
```

### Pattern 2: 長度返回模式（推薦）

```
expand(left, right) -> length:
    while left >= 0 && right < n && s[left] == s[right]:
        left--, right++
    return right - (left + 1)  # 實際長度

main:
    for i in positions:
        len = max(expand(i, i), expand(i, i + 1))
        if len > end - start:  # 一樣長也更新（取後面的）
            start = i - (len - 1) / 2
            end = i + len / 2
```

**條件設計**：

- `len > end - start` ⟺ `len >= end - start + 1`（整數條件下）
- 語義：遇到一樣長的也更新 → 偏好**後面出現**的答案
- 若改用 `len > end - start + 1`：嚴格要求更長才更新 → 偏好**前面出現**的答案

**Pattern 2 優缺點**：

- ✅ 職責單一（expand 只算長度）
- ✅ 位置計算集中
- ✅ 易於測試
- ❌ `start/end` 計算公式較不直觀（需要數學推導）

## 位置計算公式

### 從中心 i 和長度 len 推導位置

**統一公式**（整數除法）：

- `start = i - (len-1) / 2`
- `end = i + len / 2`

**範例驗證**：

- 奇數：len=5, i=2 → start=0, end=4 → `[0,1,2,3,4]` ✓
- 偶數：len=4, i=1 → start=0, end=3 → `[0,1,2,3]` ✓

## 擴展函數細節

### 返回長度的技巧

**循環結束後狀態**：

- `left`, `right` 已越過有效範圍
- 實際範圍：`[left+1, right-1]`
- 長度公式：`right - left - 1`

### 邊界檢查順序

**必須先檢查邊界再比較字符**：

```
left >= 0 && right < n && s[left] == s[right]
```

避免越界訪問

## 複雜度

| 項目 | 複雜度 |
| ---- | ------ |
| 時間 | O(n²)  |
| 空間 | O(1)   |

## vs DP 對比

| 方法                 | 時間  | 空間  | 適用場景           |
| -------------------- | ----- | ----- | ------------------ |
| Expand Around Center | O(n²) | O(1)  | 只需找一個最優解   |
| DP                   | O(n²) | O(n²) | 需要所有子問題結果 |

## 適用場景識別

**核心特徵**：

- 連續子串問題
- 具對稱/中心擴展特性
- 可從小範圍向外驗證

**典型應用**：回文相關問題

## ✅ 關鍵要點

- [ ] 兩種中心：`(i,i)` 和 `(i,i+1)` 都要處理
- [ ] 返回長度：`right - left - 1`
- [ ] 位置公式：`start = i - (len-1)/2`, `end = i + len/2`
- [ ] 更新條件：`len > end - start`（一樣長也更新，偏好後面答案）
- [ ] 邊界優先：先檢查索引再比較字符
- [ ] 推薦模式：expand 返回長度，外部計算位置

## 相關問題

- LeetCode 5: Longest Palindromic Substring
- LeetCode 647: Palindromic Substrings
