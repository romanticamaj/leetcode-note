# Counting DP 心法手冊：從可達性到路徑計數

計數型動態規劃 (Counting DP) 是 DP 的一個重要分支。它從「路徑可達性」問題（判斷是否存在解）延伸而來，專注於計算「總共有多少種有效路徑或方法」。這類問題的核心在於精巧的遞迴關係設計與防止重複計數。

---

## 1. 核心思想：從 `max/min` 到 `addition`

Counting DP 與最優化 DP (Optimization DP) 的根本區別在於其**遞迴關係的組合方式**。

- **Optimization DP**: 通常在多個決策的結果中取**最優值**。
  - `dp[i] = max(dp[i-1], dp[i-2] + value[i])`
- **Counting DP**: 將所有可能達成當前狀態的路徑數量進行**累加**。
  - `dp[i] = dp[i-1] + dp[i-2]`

這個轉變看似簡單，卻是思維模式的關鍵切換：我們不再關心哪條路徑「最好」，而是關心「總共有幾條路」可以到達這裡。

> **註記：** 許多計數問題的直覺解法是回溯法。當你發現回溯過程中存在大量**重疊子問題 (Overlapping Subproblems)** 時，就應該立即意識到這是一個可以轉換為 DP 的信號。

---

## 2. 遞迴與基礎案例設計

### 遞迴關係 (Recurrence Relation)

Counting DP 的遞迴關係設計與標準的回溯法非常相似，通常遵循「做出選擇，然後遞迴」的模式。對於當前狀態，分析所有可能的「上一步」或「下一個決策」，並將這些來源路徑的數量相加。

### 基礎案例 (Base Case)

與 Optimization DP 不同，Counting DP 的基礎案例通常不是一個中性的 `0`。

- **Optimization DP**: 對於越界的、無效的子問題，其「最優值貢獻」通常是 `0` 或 `-infinity`，不影響 `max/min` 運算。
- **Counting DP**: 基礎案例必須是一個有意義的**計數單位**，通常是 `1`。這代表「達成這個基礎狀態本身就算一種方法」。
  - 例如，在爬梯子問題中，`dp[0] = 1`，代表「停在第 0 階」本身就是一種有效的方法。如果設為 `0`，所有後續的累加都將是 `0`，導致結果錯誤。

---

## 3. 關鍵挑戰：組合問題的去重 (Handling Combinations)

這是 Counting DP 中最常見也最棘手的問題。當問題要求計算「組合」數量時（元素的順序無關），我們必須避免將 `[1, 2]` 和 `[2, 1]` 當作兩種不同的方法來計算。

### 核心策略：人為引入順序

防止重複的核心策略是**在迭代中引入一個不可逆的順序**。

- **狀態設計**: 為了實現這一點，狀態中**必須包含一個 `index`**，用來指明「當前決策只能從候選集合的第 `index` 個元素開始考慮」。
  - `dp(index, target)`: 計算使用 `candidates[index:]` 的元素湊成 `target` 的方法數。
- **迭代設計**: 在遞迴或迭代的實現中，這個 `index` 確保了我們的「選擇」永遠是向前看的，絕不回頭。
  - `solve(index, ...)` 的下一層遞迴呼叫會是 `solve(index, ...)` (選擇當前元素) 或 `solve(index + 1, ...)` (不選擇當前元素，考慮下一個)。

> **關鍵心法**: 對於組合計數問題，**迭代順序或 DP 表格的設計本身，就是防止重複的核心機制**。

### 特例：Amount-based Counting

對於某些「湊金額」類型的問題，如果我們將**候選者（例如硬幣面額）作為外層迴圈**，將**金額作為內層迴圈**，也可以達到去重的效果，而無需將 `index` 直接作為 DP 狀態的一部分。

```cpp
// LeetCode 518. Coin Change 2
// dp[j] = number of ways to make up amount j
vector<int> dp(amount + 1, 0);
dp[0] = 1; // Base case

for (int coin : coins) { // 將候選者作為外層迴圈
    for (int j = coin; j <= amount; ++j) { // 金額作為內層迴圈
        dp[j] += dp[j - coin];
    }
}
```

在這個設計中，`for (int coin : coins)` 的迭代順序隱含地強制了選擇的順序（先用完所有 1 元，再用 5 元...），從而避免了重複計數。

---

## 4. 經典案例

- LeetCode 91. Decode Ways
- LeetCode 276. Paint Fence
- LeetCode 518. Coin Change II
