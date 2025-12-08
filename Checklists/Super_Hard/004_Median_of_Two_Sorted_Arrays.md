# 004. Median of Two Sorted Arrays

## 解題脈絡與練習路徑

### 1. Brute Force

- 合併兩陣列後取中位數，建立中位數定義直覺。
- **Time:** O(m + n), **Space:** O(m + n)

### 2. Two Pointers Merge Until Mid

- 不需完整合併，使用雙指針只走到中位數位置。
- **Time:** O(m + n), **Space:** O(1)

### 3. Recursive Find k-th Element

- 將問題轉化為尋找第 k 小元素，使用 Divide and Conquer 切除不可能區間。
- **Time:** O(log(m + n)), **Space:** O(log(m + n)) (recursion stack)

### 4. Optimal Binary Search on Partition

- 在較短陣列上 Binary Search 分割點，確保左右平衡且左邊最大 ≤ 右邊最小。
- **Time:** O(log(min(m, n))), **Space:** O(1)
