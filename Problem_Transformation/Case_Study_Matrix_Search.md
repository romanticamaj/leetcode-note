# 問題轉換案例：將兩次二分搜索優化為一次

## LeetCode 74: 搜索二維矩陣

```
給你一個滿足下述兩個條件的 m x n 整數矩陣 matrix：
- 每行中的整數從左到右按非遞減順序排列。
- 每行的第一個整數大於前一行的最後一個整數。

給你一個整數 target，如果 target 在矩陣中，返回 true；否則，返回 false。
```

## 從「優化算法」角度出發

### 初始思路與挑戰

一開始，我們可能會想到使用兩次 `upper_bound` 來解決這個問題：

1. **第一次 `upper_bound`**：在第一列上查找，確定 `target` 可能在哪一行。
2. **第二次 `upper_bound`**：在確定的一行中查找 `target`。

這種方法的挑戰在於需要處理 `column span` 的資料，邏輯較為複雜，容易出錯。

### 核心優化動機

**“如何將兩次二分搜索降為一次？”**

這個問題是優化算法的出發點。我們希望找到一種方法，避免兩次獨立的搜索，從而簡化邏輯並提高效率。

## 問題轉換：最佳解

### 關鍵洞察

由於矩陣的特殊排序性質（每行有序且下一行的第一個元素大於上一行的最後一個元素），整個矩陣可以被視為一個邏輯上的一維有序數組。

### 轉換策略

這就是問題轉換的核心思想。我們建立二維坐標 `(i, j)` 和一維索引 `index` 之間的映射：

- **`index = i * n + j`**
- **`i = index / n, j = index % n`**

搜索空間也從二維變為一維：

- **`[0, m*n-1]`**

### 優化實現

```cpp
bool searchMatrix(vector<vector<int>>& matrix, int target) {
    if (matrix.empty() || matrix[0].empty()) return false;

    int m = matrix.size();
    int n = matrix[0].size();
    int left = 0;
    int right = m * n - 1; // 搜索空間: [0, m*n-1]

    while (left <= right) {
        int mid = left + (right - left) / 2;
        // 關鍵轉換：將一維索引映射到二維坐標
        int midValue = matrix[mid / n][mid % n]; // i = mid / n, j = mid % n

        if (midValue == target) {
            return true;
        } else if (midValue < target) {
            left = mid + 1;
        } else {
            right = mid - 1;
        }
    }

    return false;
}
```

### 優化效益

| 優化前                 | 優化後           |
| ---------------------- | ---------------- |
| 兩次 `upper_bound`     | 一次標準二分搜索 |
| 需要處理 `column span` | 無需處理行邊界   |
| 邏輯複雜               | 邏輯清晰         |

### 總結

這個案例是一個很好的例子，展示了如何從「優化算法」的角度出發，通過問題轉換找到更優雅的解決方案。關鍵在於：

1. **以優化為目標**：明確希望將兩次搜索降為一次。
2. **識別底層結構**：發現二維矩陣本質上是一維有序數組。
3. **建立數學映射**：使用 `index = i * n + j` 作為轉換工具。

最終，我們得到了一個不僅代碼更簡潔，而且邏輯更清晰、更不容易出錯的優化解。
