# DP 的直觀解法：從遞迴關係式到迭代實現

對於有經驗的開發者來說，有時並不需要完整地走完「從回溯到 DP」的每一步。當問題的「最優子結構」特性非常明顯時，我們可以憑直覺快速建立遞迴關係式，並直接跳轉到高效的 Bottom-Up 實現。

本文件旨在闡述這條捷徑的思維過程。

---

## 步驟一：定義狀態與選擇 (State & Choices)

忘掉程式碼，專注於問題的核心。首先，定義子問題的「狀態」，然後分析在該狀態下的「選擇」。

- **定義狀態 (State):** `dp[i]` 的物理意義是什麼？它通常代表「考慮到第 `i` 個元素為止的最優解」。
- **分析選擇 (Choices):** 對於狀態 `dp[i]`，你有哪幾種決策可以做？
  - **例子 (House Robber):**
    - **狀態:** `dp[i]` = 考慮到第 `i` 間房子的最高金額。
    - **選擇:**
      1. **搶 `i`:** 收益為 `nums[i]` + `dp[i-2]` (不能搶 `i-1`)。
      2. **不搶 `i`:** 收益為 `dp[i-1]`。

## 步驟二：建立遞迴關係式 (Recurrence Relation)

將「狀態」和「選擇」的分析轉化為一個數學公式，即狀態轉移方程式。

1. **聚合結果 (Aggregate the Outcomes):** 如何從所有選擇的結果中，得到當前狀態的最優解？通常是取最大值、最小值或求和。

   - **範例 (House Robber):** 為了獲得最高金額，我們在「搶」和「不搶」的結果中取最大值。
     `dp[i] = max(dp[i-2] + nums[i], dp[i-1])`

2. **泛化公式 (General Formula):** 這個過程可以被抽象為一個更通用的模型：

   ```cpp
   dp[state] = combine({ calculate(dp[prev_state_c], cost(c)) for c in choices_at_state })
   ```

   - **`dp[state]`**: 當前狀態的最優解。
   - **`combine`**: 聚合函數 (`max`, `min`, `sum`)，用於在所有選擇中做出最終決策。
   - **`calculate`**: 價值計算函數 (`+`, `*` ...)，用於計算單一選擇的結果。
   - **`dp[prev_state_c]`**: 做出某個決策後，所依賴的「前置狀態」的解。
   - **`cost(c)`**: 做出該決策本身的成本或收益。
   - **`choices_at_state`**: 在當前狀態下的所有可能決策。

## 步驟三：確定基礎案例 (Base Cases)

遞迴必須有終點。基礎案例是遞迴關係式無法再分解、可以直接得知的初始值。

- **思考:** 遞迴公式在 `i` 多小的時候會失效或沒有意義？
- **例子 (House Robber):**
  - `dp[0] = nums[0]`
  - `dp[1] = max(nums[0], nums[1])`

## 步驟四：實現與路徑重建

有了遞迴關係和基礎案例，就可以直接編寫 Bottom-Up 代碼，並視需要重建解路徑。

### 1. Bottom-Up 實現 (計算最優值)

從基礎案例開始，迭代計算直到目標狀態。

```cpp
// 泛化模板
vector<T> dp(n); // solution at n - 1, size n is needed
// 1. 初始化 Base Cases
dp[0] = base_val_0;
dp[1] = base_val_1;
// 2. 迭代計算
for (int i = 2; i < n; ++i) {
    dp[i] = f(dp[i-1], dp[i-2], ...); // 應用遞迴關係式
}
// 3. 返回結果
return dp[n-1];
```

### 2. 重建解路徑 (Reconstructing the Solution)

DP 表儲存了決策路徑。我們可以從最終狀態反向追溯，找出是哪個選擇導致了最優解。

- **邏輯:** 檢查 `dp[i]` 的值是由哪個子問題的解轉移而來的。
- **例子 (House Robber):**

  ```cpp
  vector<int> path;
  for (int i = n - 1; i >= 0; ) {
      if (i > 0 && dp[i] == dp[i-1]) {
          // 決策：不搶第 i 間
          i--;
      } else {
          // 決策：搶第 i 間
          path.push_back(nums[i]);
          i -= 2;
      }
  }
  reverse(path.begin(), path.end());
  return path;
  ```

---

## 總結

> **直觀解法的精髓在於：**
> **1. 識別最優子結構 -> 2. 寫下遞迴關係式 -> 3. 確定 Base Case -> 4. 直接翻譯成 Bottom-Up 迭代。**

這條路徑省略了顯式地編寫遞迴和 Memoization 的過程，讓你能夠更快地從問題的核心邏輯跳轉到高效的程式碼實現。
