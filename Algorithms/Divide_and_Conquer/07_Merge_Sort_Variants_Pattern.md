# Merge Sort Variants Pattern (Combine-centric D&C) 心法

## 🧠 核心哲學

Merge Sort 不只是排序演算法，更是 **Combine-centric Divide and Conquer** 的最佳範例。當我們將思維從「排序」轉換到「利用 merge 特性做統計」時，就能解決需要統計滿足 `i < j` 條件的 Pair 數量問題。

**關鍵洞察**：**Divide 負責產生 Pair，Combine 負責統計**。

- Brute force: O(n²) 枚舉所有配對
- Merge Sort Pattern: O(n log n) - Divide 自動產生有序配對 + Combine 利用 sorted 特性高效統計

---

## 核心概念

### 1️⃣ 透過 Divide 產生 Index Pair

**Merge Sort 的天然優勢**：

- Divide 分為左半 `[left, mid]` 和右半 `[mid+1, right]`
- 遞迴處理後，左右半**內部已排序**
- Combine 時，左半任一元素 vs 右半任一元素，**自動滿足 i < j**

```
[left, ..., mid] [mid+1, ..., right]
    索引 i           索引 j

自動保證：i ≤ mid < mid+1 ≤ j  →  i < j
```

**擴展**：若需要 `i ≤ j`，在 base case 處理即可。

### 2️⃣ 利用 Sorted 特性達成 O(n) Combine

**Inflection Point（轉折點）概念**：

```
左半： [a₁, a₂, a₃, ...]  (sorted)
右半： [b₁, b₂, b₃, ...]  (sorted)

對於 a₁，找到右半第一個不滿足條件的 bⱼ
     → [b₁, ..., bⱼ₋₁] 都滿足條件
```

**關鍵技巧**：Two-pointer technique

- 左指針移到 a₂ 時，右指針**不需重置**，可從上次位置繼續
- 保證整體掃描 O(n)

### 3️⃣ 統計時機：Combine 而非 Divide

**設計原則**：

- ❌ Divide 階段：子區間尚未排序，無法高效利用特性
- ✅ Combine 階段：左右子區間已排序，可高效找 inflection point

**統計類型**：

1. **區間內統計**：遞迴處理左半、右半（子問題）
2. **跨區間統計**：Merge 時處理（當前層）

---

## 🧩 核心設計模式

```
Phase 1: Divide
  → 遞迴處理左半、右半

Phase 2: Count (利用 sorted 特性)
  → Two-pointer 找 inflection points
  → 統計跨區間滿足條件的配對數

Phase 3: Merge
  → 維持 sorted 性質（必要！）
```

**設計要點**：

- **計數時機**：Count before merge（需比較原始值）或 Count during merge
- **條件類型**：Simple comparison 或 Range condition（需 prefix sum）
- **Index tracking**：若結果需對應原始位置，使用 index array 追蹤

---

## 📚 LeetCode 學習路徑

### 推薦練習順序

```
1️⃣ LC 327. Count of Range Sum 📙
   → 最難但最重要
   → Prefix Sum + Merge Sort 雙重技巧
   → 需找兩個 inflection points

2️⃣ LC 315. Count of Smaller Numbers After Self 📕
   → 327 簡化版 + Index Mapping
   → 學習位置追蹤技巧

3️⃣ LC 493. Reverse Pairs 📕
   → 最簡化版本
   → 鞏固基本 Pattern
```

**關鍵心法**：

- 327 是「老大」，攻克它後其他題目迎刃而解
- 三題核心思想一致，只是條件複雜度不同
- 先理解 pattern 再做題，不要被難度嚇到
