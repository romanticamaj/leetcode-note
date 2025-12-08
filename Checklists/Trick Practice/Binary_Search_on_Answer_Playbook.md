# 🔍 Binary Search on Answer 題型整理

這類題目雖然使用 Binary Search，但不是在 array 上找元素，而是在「答案空間」上進行二分，透過 check 函數來判斷某個 candidate 是否可行。

---

## 🎯 終極目標題

- LC 410. Split Array Largest Sum
- LC 1231. Divide Chocolate
- LC 774. Minimize Max Distance to Gas Station
- LC 4. Median of Two Sorted Arrays

---

## 🧪 練習路徑

### ✅ 推薦學習順序

1. **Binary Search Fundamentals**

   - LC 704. Binary Search
   - LC 35. Search Insert Position
   - LC 69. Sqrt(x)

2. **Binary Search on Answer**

   - 📙 LC 875. Koko Eating Bananas ← 入門 check 函數設計
   - 📙 LC 1283. Find the Smallest Divisor
   - 📙 LC 1011. Capacity To Ship Packages

3. **Partition 類型題目**

   - LC 153. Find Minimum in Rotated Sorted Array
   - LC 33. Search in Rotated Sorted Array

4. **Two Array Binary Search**

   - LC 378. Kth Smallest Element in a Sorted Matrix
   - LC 668. Kth Smallest Number in Multiplication Table

5. **最終挑戰**
   - 📕 LC 410 / 1231 / 774
   - 📕 LC 4 ← 最後挑戰，需理解 partition + binary search

---

## 🧠 技巧重點

- 明確界定「答案空間」的上下界
- 設計單調性 check 函數
- 注意整數除法、上界下界更新方式
- LC 4 題型需額外理解 partition + binary search 的結合技巧（建議延後）
