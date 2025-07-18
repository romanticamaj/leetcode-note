# DP 的優雅邊界處理：哨兵值與索引鉗制 (Sentinel Value & Index Clamping)

在設計 Bottom-Up DP 解法時，狀態轉移方程（如 `dp[i] = f(dp[i+k], dp[i-m])`）常常會遇到索引超出 `dp` 陣列範圍的問題（例如 `i+k >= n` 或 `i-m < 0`）。傳統的處理方式是使用 `if` 條件判斷，但這會讓程式碼顯得冗長。

本文件介紹一種更為優雅的技巧：透過設定「哨兵值」並結合「索引鉗制」，來統一邊界內外的處理邏輯。

---

## 核心問題：惱人的邊界檢查

假設我們的狀態轉移需要存取 `dp[i + k]`，一個直接的寫法會是：

```cpp
// 傳統的邊界檢查
long long future_val;
if (i + k >= n) {
    future_val = 0; // 越界，對應到 Base Case 的預設值
} else {
    future_val = dp[i + k];
}
dp[i] = calculate(..., future_val);
```

這段程式碼雖然功能正確，但 `if-else` 結構打斷了核心計算邏輯的流暢性。當轉移關係更複雜時，程式碼會變得更加混亂。

---

## 優雅解法：哨兵值 + `min`/`max` 鉗制

這個技巧包含兩個相輔相成的步驟：

### 1. 擴展 DP 陣列以建立「哨兵」

我們故意將 `dp` 陣列的大小擴展一個單位，並在這個額外的位置上儲存對應於「越界」情況的基礎案例值（通常是 `0`）。

- **對於上界 (`>= n`)：**
  將陣列大小設為 `n+1`，即 `vector<T> dp(n + 1, ...)`。`dp[n]` 這個位置就成為了我們的**哨兵 (Sentinel)**。我們將其初始化為越界時應有的值，例如 `0LL`。

- **對於下界 (`< 0`)：**
  雖然較少見（通常由迴圈起始點控制），但同樣的邏輯也適用。可以透過 1-based 索引來建立 `dp[0]` 作為下界的哨兵。

### 2. 使用 `min()` 或 `max()` 鉗制索引

在存取 `dp` 陣列時，我們不再使用 `if` 判斷，而是用 `min()` 或 `max()` 函式將索引「鉗制」在合法範圍內。

- **鉗制上界：**
  用 `min(n, i + k)` 來取代 `i + k`。

  - 如果 `i + k < n`，`min` 會返回 `i + k`，正常存取。
  - 如果 `i + k >= n`，`min` 會返回 `n`，存取會被巧妙地導向我們設定好的哨兵 `dp[n]`，其值正好是我們想要的 `0`。

- **鉗制下界：**
  用 `max(0, i - m)` 來取代 `i - m`。
  - 如果 `i - m >= 0`，`max` 會返回 `i - m`，正常存取。
  - 如果 `i - m < 0`，`max` 會返回 `0`，存取會被導向哨兵 `dp[0]`。

### 範例：Brainpower 問題的應用

讓我們用這個技巧來重構 Brainpower 問題的程式碼。

- **原轉移方程：** `dp[i] = max(dp[i + 1], points[i] + dp[i + brainpower + 1])`
- **問題：** `i + brainpower + 1` 可能會超過 `n`。

**重構後的程式碼：**

```cpp
long long mostPoints(vector<vector<int>>& questions) {
    int n = questions.size();

    // 1. 建立一個大小為 n+1 的 dp 陣列，dp[n] 作為哨兵，其值為 0。
    vector<long long> dp(n + 1, 0LL);

    for (int i = n - 1; i >= 0; i--) {
        int points = questions[i][0];
        int brainpower = questions[i][1];

        // 2. 使用 min(n, ...) 來鉗制索引
        long long future_idx = min(n, i + brainpower + 1);

        long long solve_it = points + dp[future_idx];
        long long skip_it = dp[i + 1]; // i+1 永遠不會超過 n

        dp[i] = max(solve_it, skip_it);
    }

    return dp[0];
}
```

透過這個技巧，我們移除了 `if-else` 判斷，使得核心的 `dp[i] = max(...)` 邏輯更加純粹和清晰。

---

## 總結心法

> **當 DP 轉移需要存取潛在的越界索引時，考慮建立一個「哨兵節點」來儲存基礎案例值。然後，使用 `min()` 或 `max()` 將索引鉗制在 `[0, n]` 範圍內，從而將邊界檢查優雅地融入到狀態轉移方程中。**
