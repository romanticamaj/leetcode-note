# Divide and Conquer vs Dynamic Programming 比較分析

## 🧠 核心差異

兩者都將問題分解為子問題，但處理方式根本不同：

- **Divide and Conquer**：子問題**獨立**，直接遞迴求解
- **Dynamic Programming**：子問題**重疊**，記憶化避免重複計算

## 關鍵特徵對比

### 1. 子問題重疊性

#### Divide and Conquer：無重疊

```cpp
// MergeSort：左右子數組完全獨立
void mergeSort(arr, left, right) {
    int mid = (left + right) / 2;
    mergeSort(arr, left, mid);    // 獨立子問題 1
    mergeSort(arr, mid+1, right);  // 獨立子問題 2
    merge(arr, left, mid, right);
}
```

#### Dynamic Programming：有重疊

```cpp
// Fibonacci：子問題大量重疊
int fib(n) {
    if (n <= 1) return n;
    return fib(n-1) + fib(n-2);  // fib(n-2) 被多次計算
}

// DP 解法：記憶化
int fibDP(n, memo) {
    if (memo[n] != -1) return memo[n];  // 避免重複計算
    memo[n] = fibDP(n-1, memo) + fibDP(n-2, memo);
    return memo[n];
}
```

### 2. 問題分割方式

| 特性     | Divide and Conquer      | Dynamic Programming          |
| -------- | ----------------------- | ---------------------------- |
| 分割模式 | 通常等分（n/2, n/3）    | 減少固定量（n-1, n-k）       |
| 子問題數 | 通常固定（2 個、3 個）  | 可變（取決於狀態轉移）       |
| 遞迴結構 | T(n) = a\*T(n/b) + f(n) | T(n) = T(n-1) + T(n-2) + ... |

### 3. 最優子結構 vs 分治結構

#### Divide and Conquer：分治結構

```cpp
// QuickSort：不需要「最優」，只需要正確分割
int partition(arr, left, right) {
    // 任何正確的分割都可行
    // 不需要保證子問題的「最優性」
}
```

#### Dynamic Programming：最優子結構

```cpp
// 最短路徑：子問題必須是最優的
dp[i][j] = min(
    dp[i-1][j] + cost,   // 必須是到 (i-1,j) 的最短路
    dp[i][j-1] + cost    // 必須是到 (i,j-1) 的最短路
);
```

## 🧩 算法選擇決策樹

```
問題可以分解為子問題？
    ├─ 否 → 其他算法
    └─ 是
        └─ 子問題是否重疊？
            ├─ 否（獨立子問題）
            │   └─ Divide and Conquer
            │       ├─ 主要工作在分割 → Divide-centric
            │       └─ 主要工作在合併 → Combine-centric
            └─ 是（重疊子問題）
                └─ Dynamic Programming
                    ├─ 有最優子結構 → 標準 DP
                    └─ 無最優子結構 → 記憶化搜索
```

## 典型問題分類

### Divide and Conquer 適用

- **排序**：MergeSort, QuickSort
- **搜索**：Binary Search, Find K-th element
- **幾何**：Closest Pair, Convex Hull
- **數學**：Fast Power, Karatsuba Multiplication

### Dynamic Programming 適用

- **優化問題**：背包、最短路徑
- **計數問題**：組合數、路徑計數
- **決策問題**：股票買賣、遊戲策略
- **字符串**：編輯距離、最長公共子序列

## ⚠️ 常見誤區

### 1. 強行使用分治解決有重疊的問題

```cpp
// 錯誤：用分治解 0-1 背包
int knapsack(items, capacity) {
    // 子問題 capacity-w[i] 會被重複計算
    return max(
        knapsack(items-1, capacity),
        knapsack(items-1, capacity-w[i]) + v[i]
    );
}
```

### 2. 對獨立子問題使用 DP

```cpp
// 過度設計：MergeSort 不需要記憶化
unordered_map<pair<int,int>, void> memo;  // 無意義
void mergeSort(arr, left, right) {
    // 每個 [left, right] 區間只會處理一次
}
```

## ✅ 選擇指南

| 使用 Divide and Conquer     | 使用 Dynamic Programming |
| --------------------------- | ------------------------ |
| ✓ 子問題完全獨立            | ✓ 子問題有重疊           |
| ✓ 分割後規模顯著縮小（n/2） | ✓ 規模逐步縮小（n-1）    |
| ✓ 不需要記憶化              | ✓ 需要記憶化避免重複     |
| ✓ 只需要正確性              | ✓ 需要最優性             |
| ✓ 空間要求嚴格              | ✓ 可以犧牲空間換時間     |
