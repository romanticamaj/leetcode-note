# 整數溢位防範心法 (Arithmetic Overflow Prevention Playbook)

在 C++ 等語言中，整數溢位 (Integer Overflow) 是一種未定義行為 (Undefined Behavior)，可能導致程式崩潰、安全漏洞或難以追蹤的邏輯錯誤。培養對溢位的「敏感度」是寫出健壯程式碼的關鍵。

本心法旨在建立一個系統性的框架，幫助開發者在撰寫程式碼時，主動識別並規避潛在的溢位風險。

---

## 核心原則

1. **預測 (Anticipate)**: 在寫下任何算術運算前，先思考運算元的可能最大值與最小值。問自己：「這個運算的結果是否可能超出當前資料型別的表示範圍？」
2. **提升 (Promote)**: 當運算結果可能超出範圍時，在運算發生前，將運算元提升到一個更大的資料型別（例如，從 `int` 提升到 `long long`）。
3. **重排 (Rearrange)**: 改變運算順序以避免產生巨大的中間值。有時，先做除法或減法可以有效縮小數值規模。
4. **限制 (Constrain)**: 在每一步運算後，使用模數運算 (`%`) 或上下限 (`min`, `max`) 將結果限制在一個已知的安全範圍內。

---

## 常見溢位場景與應對策略

### 場景一：乘法溢位 (Multiplication Overflow)

- **識別**: `a * b`，其中 `a` 和 `b` 都是 `int`，但其乘積可能超過 `INT_MAX` (約 `2 * 10^9`)。這在計算面積、排列組合或 DP 轉移式中非常常見。
- **心法**: **「先提升，再相乘」 (Promote then Multiply)**
- **策略**: 使用 `1LL` 字面值將其中一個運算元強制轉換為 `long long`，從而使整個乘法運算在 64 位元精度下進行。
- **範例**:

  ```cpp
  int a = 100000;
  int b = 100000;
  // long long result = a * b; // 錯誤！a * b 會先在 int 內溢位，再賦值給 result
  long long result = 1LL * a * b; // 正確！
  ```

### 場景二：加法溢位 (Addition Overflow)

- **識別**: `a + b`，其中 `a` 和 `b` 的值都很大，其和可能超過 `INT_MAX`。
- **心法**: **「先減後加，化大為小」 (Subtract then Add, Reduce the Scale)**
- **策略**: 重新排列數學表達式，用減法來避免直接對兩個大數求和。
- **範例 (Binary Search)**:
  - `int mid = (left + right) / 2;` // **不安全**：`left + right` 可能溢位。
  - `int mid = left + (right - left) / 2;` // **安全**：`right - left` 範圍較小。
- **策略 (安全檢查)**: 在執行加法前，先檢查是否會溢位。
  - `if (a > INT_MAX - b)` // **安全**：等價於 `a + b > INT_MAX`，但避免了溢位。

### 場景三：累計溢位 (Cumulative Overflow)

- **識別**: 在迴圈中對一個變數進行累加或累乘，即使單次操作安全，多次累積後也可能溢位。
- **心法**: **「容器要夠大」 (Use a Big Enough Container)**
- **策略**: 用於累計的變數（容器）必須使用能容納**最終結果**的資料型別，而不是單個元素的型別。
- **範例 (計算總和)**:

```cpp
  vector<int> nums = {INT_MAX, INT_MAX};
  // int sum = 0; // 錯誤：sum 會在第二次迭代時溢位
  long long sum = 0; // 正確
  for (int num : nums) {
      sum += num;
  }
```

- **範例 (前綴和 Prefix Sum)**:

```cpp
  vector<int> nums(100000, 100000); // 10^5 個元素，每個都是 10^5
  // vector<int> prefix(nums.size() + 1, 0); // ❌ 錯誤：最終總和 = 10^10，遠超 INT_MAX
  vector<long long> prefix(nums.size() + 1, 0); // ✅ 正確
  for (int i = 0; i < nums.size(); i++) {
      prefix[i + 1] = prefix[i] + nums[i];
  }
```

> 💡 **LeetCode 經驗**: 在 Prefix Sum、Subarray Sum、Running Sum 等問題中，這是最常見的溢位場景。詳見：[`Prefix_Sum/01_Prefix_Sum_Intro.md`](../Prefix_Sum/01_Prefix_Sum_Intro.md:62)

### 場景四：減法下溢 (Subtraction Underflow)

- **識別**: `a - b`，當 `a` 遠小於 `b` 時。在無號整數中，這會導致數值「繞回」(wrap around)；在模數算術中，可能產生負數，導致後續 `%` 運算結果不符預期。
- **心法**: **「加模再減，保持正數」 (Add MOD then Subtract, Stay Positive)**
- **策略**: 在取模的場景下，為了避免結果為負，先加上一個 `MOD`。
- **範例**:

  ```cpp
  // 假設 a < b
  // int result = (a - b) % MOD; // 可能為負
  int result = (a - b + MOD) % MOD; // 正確，保證結果在 [0, MOD-1]
  ```

### 場景五：除法溢位 (Division Overflow) - _特殊邊界_

- **識別**: 這是 C++ 中一個非常特殊的邊界情況：`INT_MIN / -1`。
- **原因**: `INT_MIN` 是 `-2,147,483,648`。除以 `-1` 後的結果是 `+2,147,483,648`，這個數超出了 `INT_MAX` (`2,147,483,647`) 的表示範圍。
- **心法**: **「邊界檢查，特殊處理」 (Check Boundaries, Handle Specially)**
- **策略**: 如果演算法的輸入允許 `dividend` 為 `INT_MIN` 且 `divisor` 為 `-1`，則必須加入明確的邊界條件判斷。
- **範例 (LeetCode 29. Divide Two Integers)**:

  ```cpp
  if (dividend == INT_MIN && divisor == -1) {
      return INT_MAX;
  }
  ```

### 場景六：取負號溢位 (Negation Overflow) - _特殊邊界_

- **識別**: 對一個整數型別的最小值取負號，例如 `-INT_MIN`。
- **原因**: 在二的補數表示法中，負數的表示範圍比正數多一。例如，`int` 的範圍通常是 `[-2147483648, 2147483647]`。`-INT_MIN` 的結果是 `+2147483648`，這超出了 `INT_MAX` 的範圍。
- **心法**: **「型別提升，再取負號」 (Promote then Negate)**
- **策略**: 在對 `INT_MIN` 這類值進行操作前，先將其轉換為更大的型別，如 `long long`。
- **範例 (LeetCode 50. Pow(x, n))**:

  ```cpp
  // 假設 n 是 int 型別
  if (n < 0) {
      // long long n_ll = -n; // 錯誤！如果 n 是 INT_MIN，這裡就會溢位
      long long n_ll = n;
      n_ll = -n_ll; // 正確！先提升型別，再取負號
      x = 1 / x;
      // ...
  }
  ```

---

## 總結檢查清單

在進行算術運算時，快速進行以下心智檢查：

- [ ] **乘法**: 結果是否可能 > `10^9`？ -> `1LL`
- [ ] **加法**: 兩數相加是否可能 > `10^9`？ -> `left + (right - left) / 2`
- [ ] **累加**: 迴圈總和是否可能 > `10^9`？ -> 累加器用 `long long`
- [ ] **減法 (取模)**: 是否可能為負？ -> `(a - b + MOD) % MOD`
- [ ] **除法**: 是否可能遇到 `INT_MIN / -1`？ -> 增加邊界判斷
- [ ] **取負號**: 是否可能遇到 `INT_MIN`？ -> 先轉 `long long`
