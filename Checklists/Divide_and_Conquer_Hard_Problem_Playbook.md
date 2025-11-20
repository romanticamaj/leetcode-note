# 🎯 Divide and Conquer - Hard 題終極練習路徑（按目標題分類）

以下是將所有經典 Hard 題目依照「終極目標題」分類，並為每題設計對應的練習路徑與技巧說明。

---

## 🏁 終極目標 Hard 題（按技巧分類）

| 題號    | 題目名稱                            | 技巧類型                | 難度   | 面試頻率 |
| ------- | ----------------------------------- | ----------------------- | ------ | -------- |
| LC 4    | Median of Two Sorted Arrays         | Binary Search + D&C     | ⭐⭐⭐ | 🔥🔥🔥   |
| LC 218  | The Skyline Problem                 | Recursive Merging       | ⭐⭐⭐ | 🔥🔥🔥   |
| LC 315  | Count of Smaller Numbers After Self | Merge Sort Variant      | ⭐⭐   | 🔥🔥     |
| LC 410  | Split Array Largest Sum             | Binary Search on Answer | ⭐⭐   | 🔥🔥     |
| LC 23   | Merge k Sorted Lists                | Recursive Merging       | ⭐     | 🔥🔥     |
| LC 973  | K Closest Points to Origin          | QuickSelect             | ⭐     | 🔥       |
| LC 312  | Burst Balloons                      | Interval DP (D&C)       | ⭐⭐⭐ | 🔥       |
| LC 1000 | Minimum Cost to Merge Stones        | Interval DP (D&C)       | ⭐⭐⭐ | 🔥       |

---

## 🧭 練習路徑總覽（依技巧類型）

---

### 1️⃣ Binary Search on Answer + D&C

**終極目標**：

- LC 4. Median of Two Sorted Arrays
- LC 410. Split Array Largest Sum
- LC 1231. Divide Chocolate
- LC 774. Minimize Max Distance to Gas Station

**練習路徑**：

- 📙 LC 875. Koko Eating Bananas ← 入門 check 函數設計
- 📙 LC 1283. Find the Smallest Divisor
- 📙 LC 1011. Capacity To Ship Packages
- 📕 LC 410 / 1231 / 774
- 📕 LC 4 ← 最後挑戰，需理解 partition + binary search

---

### 2️⃣ Merge Sort Variants（Combine-centric D&C）

**終極目標**：

- LC 315. Count of Smaller Numbers After Self
- LC 493. Reverse Pairs

**練習路徑**：

- 📙 LC 327. Count of Range Sum ← merge 時統計跨區間條件
- 📕 LC 315
- 📕 LC 493

---

### 3️⃣ Recursive Merging（Divide-centric D&C）

**終極目標**：

- LC 218. The Skyline Problem
- LC 23. Merge k Sorted Lists

**練習路徑**：

- 📘 LC 21. Merge Two Sorted Lists ← 合併邏輯基礎
- 📕 LC 23 ← 用 D&C 解法
- 📕 LC 218 ← 合併建築輪廓線，經典難題

---

### 4️⃣ QuickSelect / Partition-based

**終極目標**：

- LC 973. K Closest Points to Origin
- LC 347. Top K Frequent Elements

**練習路徑**：

- 📙 LC 215. Kth Largest Element ← QuickSelect 標準實作
- 📕 LC 973
- 📕 LC 347

---

### 5️⃣ Interval DP（Bottom-up Divide and Conquer）

**終極目標**：

- LC 312. Burst Balloons
- LC 1000. Minimum Cost to Merge Stones

**練習路徑**：

- 📙 LC 1039. Minimum Score Triangulation
- 📙 LC 1130. Minimum Cost Tree From Leaf Values
- 📕 LC 312
- 📕 LC 1000

---

## ✅ 建議練習順序（按週分階段）

### Week 1-2: 建立核心技巧肌肉記憶

- LC 875, LC 1283, LC 1011 → Binary Search on Answer
- LC 327 → Merge Sort Variants
- LC 21 → Recursive Merging
- LC 215 → QuickSelect

### Week 3-4: 挑戰 Hard 題

- LC 410, LC 315, LC 23, LC 973

### Week 5+: 經典難題與終極挑戰

- LC 218 (Skyline)
- LC 312, LC 1000 (Interval DP)
- LC 4 (Median of Two Sorted Arrays)

---

這份路徑涵蓋了所有 Divide and Conquer 的經典技巧與面試高頻題，並依照終極目標題反推練習順序，幫助你系統性建立解題肌肉記憶。
