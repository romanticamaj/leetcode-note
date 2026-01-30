# 🎯 Sliding Window Frequency Matching - 練習路徑

這類題目結合 Sliding Window 與 Hash Map Frequency Counting，核心技巧是**用 `matchedCount` 追蹤有多少字元的頻率已經匹配**，避免每次都 O(26) 或 O(k) 比較整個頻率表。

詳細心法請參考：[Frequency_Matching_Counting_Invariant.md](../../Data_Structures/Hash_Tables/Frequency_Matching_Counting_Invariant.md)

---

## 🧠 核心技巧

### Naive Approach vs Optimized Approach

| 方法      | 比較頻率                       | 時間複雜度   |
| --------- | ------------------------------ | ------------ |
| Naive     | 每次滑動都比較整個頻率表       | O((n-m) × k) |
| Optimized | 維護 `matchedCount`，O(1) 更新 | O(n)         |

### 關鍵 Invariant

```
matchedCount = 字元頻率完全匹配的數量
當 matchedCount == 字元種類數 → 找到 permutation/anagram
```

---

## 🏁 目標題總覽

| 題號   | 題目名稱                                       | Pattern 特徵                         | 難度   |
| ------ | ---------------------------------------------- | ------------------------------------ | ------ |
| LC 567 | Permutation in String                          | Fixed window + frequency matching    | ⭐⭐   |
| LC 438 | Find All Anagrams in a String                  | 同上，但收集所有起始位置             | ⭐⭐   |
| LC 76  | Minimum Window Substring                       | Variable window + frequency matching | ⭐⭐⭐ |
| LC 30  | Substring with Concatenation of All Words      | Fixed window + word-level matching   | ⭐⭐⭐ |
| LC 424 | Longest Repeating Character Replacement        | Variable window + maxFreq tracking   | ⭐⭐   |
| LC 3   | Longest Substring Without Repeating Characters | Variable window + unique constraint  | ⭐⭐   |
| LC 904 | Fruit Into Baskets                             | Variable window + distinct count ≤ 2 | ⭐⭐   |
| LC 992 | Subarrays with K Different Integers            | exactly(k) = atMost(k) - atMost(k-1) | ⭐⭐⭐ |

---

## 🧭 練習路徑（依 Pattern 變體）

### 1️⃣ Fixed Window + Exact Frequency Matching

**核心概念**：窗口大小固定，檢查窗口內字元頻率是否完全匹配目標

- 📙 **LC 567. Permutation in String** ← 入門：判斷是否存在 permutation
  - 固定窗口大小 = `s1.length()`
  - `matchedCount == 26` 時找到答案

- 📙 **LC 438. Find All Anagrams in a String** ← 同上，收集所有位置
  - 與 LC 567 幾乎相同，差別在於收集所有起始 index

- 📕 **LC 30. Substring with Concatenation of All Words** ← 進階：word-level matching
  - 窗口大小 = `words.length × word[0].length`
  - 用 `unordered_map<string, int>` 追蹤 word 頻率

### 2️⃣ Variable Window + Frequency Constraint

**核心概念**：窗口大小可變，找最小/最長滿足頻率條件的窗口

- 📕 **LC 76. Minimum Window Substring** ← 經典：找最小覆蓋子串
  - Variable window，expand until valid，then shrink
  - `matchedCount == required 字元種類數` 時窗口有效
  - 縮小時更新最小長度

- 📙 **LC 424. Longest Repeating Character Replacement** ← 變體：maxFreq tracking
  - Invariant: `windowLen - maxFreq ≤ k`
  - 不需完整頻率匹配，只追蹤 maxFreq

### 3️⃣ Variable Window + Distinct Count Constraint

**核心概念**：限制窗口內不同字元的數量

- 📙 **LC 3. Longest Substring Without Repeating Characters** ← 入門：所有字元唯一
  - Invariant: `frequency[c] ≤ 1` for all c in window

- 📙 **LC 904. Fruit Into Baskets** ← 變體：最多 2 種不同元素
  - Invariant: `distinctCount ≤ 2`

- 📕 **LC 992. Subarrays with K Different Integers** ← 進階：exactly K 種
  - 技巧：`exactly(k) = atMost(k) - atMost(k-1)`
  - 將 "exactly" 轉換為 "at most" 問題

---

## 🔑 Pattern 識別關鍵字

遇到以下關鍵字，考慮 Sliding Window + Frequency Matching：

- ✅ "permutation" / "anagram"
- ✅ "substring containing all characters"
- ✅ "minimum/maximum window"
- ✅ "at most K distinct"
- ✅ "exactly K different"
- ✅ "character frequency"
- ✅ "contiguous substring"

---

## ✅ 建議練習順序

### 階段 1：Fixed Window Matching（1 天）

1. **LC 567** → 基礎 matchedCount 技巧
2. **LC 438** → 同樣技巧，練習收集結果

### 階段 2：Variable Window Matching（1-2 天）

3. **LC 76** → 經典 minimum window，學會 expand-then-shrink
4. **LC 424** → maxFreq 變體，理解不同的 invariant 設計

### 階段 3：Distinct Count Constraint（1-2 天）

5. **LC 3** → 基礎 unique constraint
6. **LC 904** → K=2 的 distinct 限制
7. **LC 992** → exactly K 的轉換技巧

### 可選進階題

- **LC 30** → word-level matching，較繁瑣但概念相同

---

## 💡 關鍵心法總結

1. **matchedCount 追蹤** → 避免 O(k) 頻率比較，達到 O(1) 判斷
2. **更新順序** → 先檢查舊狀態，再更新頻率，再檢查新狀態
3. **Invariant 設計** → 明確定義「什麼時候 matchedCount 增減」
4. **Variable Window** → expand until valid, shrink while still valid

這份路徑涵蓋了 Sliding Window + Frequency Matching 的所有核心變體，從最基礎的 Fixed Window Permutation 檢測到複雜的 Variable Window 最小覆蓋問題。
