# 🎯 Divide and Conquer - Hard 題終極練習路徑（按目標題分類）

以下是將所有經典 Hard 題目依照「終極目標題」分類，並為每題設計對應的練習路徑與技巧說明。

---

## 🏁 終極目標 Hard 題（按技巧分類）

| 題號    | 題目名稱                            | 技巧類型           | 難度   | 面試頻率 |
| ------- | ----------------------------------- | ------------------ | ------ | -------- |
| LC 218  | The Skyline Problem                 | Merge Sort Variant | ⭐⭐⭐ | 🔥🔥🔥   |
| LC 315  | Count of Smaller Numbers After Self | Merge Sort Variant | ⭐⭐   | 🔥🔥     |
| LC 23   | Merge k Sorted Lists                | Recursive Merging  | ⭐     | 🔥🔥     |
| LC 973  | K Closest Points to Origin          | QuickSelect        | ⭐     | 🔥       |
| LC 312  | Burst Balloons                      | Interval DP (D&C)  | ⭐⭐⭐ | 🔥       |
| LC 1000 | Minimum Cost to Merge Stones        | Interval DP (D&C)  | ⭐⭐⭐ | 🔥       |

---

## 🧭 練習路徑總覽（依技巧類型）

### 1️⃣ Merge Sort Variants（Combine-centric D&C）

**終極目標**：

- LC 315. Count of Smaller Numbers After Self
- LC 493. Reverse Pairs

**練習路徑**：

- 📙 LC 327. Count of Range Sum ← merge 時統計跨區間條件 (這題是最難的，Claude 建議的順序錯誤，但是先寫完這題，反而其他的都變簡單了)
- 📕 LC 315
- 📕 LC 493

---

### 2️⃣ Recursive Merging（Divide-centric D&C）

**終極目標**：

- LC 218. The Skyline Problem
- LC 23. Merge k Sorted Lists

**練習路徑**：

- 📘 LC 21. Merge Two Sorted Lists ← 合併邏輯基礎
- 📕 LC 23 ← 用 D&C 解法
- 📕 LC 218 ← 合併建築輪廓線，經典難題

---

### 3️⃣ QuickSelect / Partition-based

**終極目標**：

- LC 973. K Closest Points to Origin
- LC 347. Top K Frequent Elements

**練習路徑**：

- 📙 LC 215. Kth Largest Element ← QuickSelect 標準實作
- 📕 LC 973
- 📕 LC 347

---

### 4️⃣ Interval DP（Bottom-up Divide and Conquer）

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

- LC 327 → Merge Sort Variants
- LC 21 → Recursive Merging
- LC 215 → QuickSelect
- LC 1039, LC 1130 → Interval DP

### Week 3-4: 挑戰 Hard 題

- LC 315, LC 493 → Merge Sort Variants
- LC 23 → Recursive Merging
- LC 973, LC 347 → QuickSelect

### Week 5+: 經典難題與終極挑戰

- LC 218 (Skyline)
- LC 312, LC 1000 (Interval DP)

---

這份路徑涵蓋了所有 Divide and Conquer 的經典技巧與面試高頻題，並依照終極目標題反推練習順序，幫助你系統性建立解題肌肉記憶。
