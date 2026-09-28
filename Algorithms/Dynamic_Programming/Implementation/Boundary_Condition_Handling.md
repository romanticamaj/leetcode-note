# DP 邊界處理的設計模式與心法

在動態規劃中，如何處理邊界索引不僅是技術問題，更是一種設計哲學的體現。優雅的邊界處理能顯著提升程式碼的簡潔性、可讀性與穩健性。本文件旨在探討處理邊界的核心策略與通用模式。

---

## 核心挑戰：邊界處理的兩種設計哲學

所有邊界處理的技巧，都源於兩種基本哲學的權衡：

1. **寬鬆呼叫，入口防禦 (Loose Calls, Strict Entry):**

   - **哲學：** 信任但驗證。在進行狀態轉移（遞迴呼叫）時，不預先檢查索引的合法性，而是將驗證的責任完全交給被呼叫函式的「入口」。
   - **體現：** 主要用於 Top-Down DP。

2. **嚴格呼叫，邏輯內嵌 (Strict Calls, Embedded Logic):**
   - **哲學：** 永不犯錯。在進行狀態轉移（迭代計算）之前，就透過各種技巧確保所有存取都是合法的，將邊界處理邏輯內嵌到核心計算中。
   - **體現：** 主要用於 Bottom-Up DP。

---

## Top-Down 模式：入口剪枝 (Pruning on Entry)

這是 Top-Down DP 最自然、最常用的邊界處理模式。其核心是**保持遞迴呼叫的簡潔性**。

**通用模式：**

> 在遞迴函式的最開頭，立刻檢查所有無效狀態（如索引越界）。若狀態無效，則回傳一個對當前問題無害的「中性值」。

- **對於最小值問題 (min-cost):** 回傳 `infinity`。
- **對於最大值問題 (max-profit):** 回傳 `-infinity` 或 `0`。
- **對於計數問題 (counting):** 回傳 `0`。
- **對於可行性問題 (feasibility):** 回傳 `false`。

**偽代碼範例：**

```cpp
// C++ 偽代碼範例
// T: 回傳類型, Args...: 狀態參數
template<typename T, typename... Args>
T solve(Args... state_params) {
    // 1. 入口處統一防禦
    if (is_invalid(state_params...)) {
        return NEUTRAL_VALUE; // 例如：infinity, 0, false
    }
    // 處理基礎案例
    if (is_base_case(state_params...)) {
        return BASE_VALUE;
    }
    // 檢查快取
    if (cache.count({state_params...})) {
        return cache[{state_params...}];
    }

    // 2. 遞迴呼叫本身保持乾淨
    T result = combine(
        solve<T>(next_state_A...),
        solve<T>(next_state_B...),
        // ...
    );

    // 儲存結果並回傳
    return cache[{state_params...}] = result;
}
```

**優點：**

- **邏輯清晰：** 核心的遞迴關係 `combine(...)` 非常純粹，不受邊界判斷干擾。
- **易於除錯：** 所有邊界問題都在一個地方處理。

---

## Bottom-Up 模式：三種邊界防護技巧

Bottom-Up 方法沒有統一的遞迴入口，因此必須在迭代邏輯中處理邊界。

### 技巧 1：索引鉗制 (Index Clamping)

**通用模式：**

> 當轉移依賴的邊界外狀態，其值可以安全地由最接近的邊界內狀態替代時，使用 `min()` 和 `max()` 將索引「鉗制」在合法範圍內。

**適用場景：**

- 網格問題中，當越界的路徑可以視為從邊界格子出發時。
- 當邊界值本身就是一個有效的「預設」選項時。

**偽代碼範例：**

```cpp
// C++ 偽代碼範例
// dp[i][j] 依賴 dp[i-1][j-1], dp[i-1][j], dp[i-1][j+1]
for (int i = 1; i < m; ++i) {
    for (int j = 0; j < n; ++j) {
        // 使用 std::max 和 std::min 進行索引鉗制
        int prev_j_left = std::max(0, j - 1);
        int prev_j_right = std::min(n - 1, j + 1);

        auto val_left = dp[i - 1][prev_j_left];
        auto val_center = dp[i - 1][j];
        auto val_right = dp[i - 1][prev_j_right];

        dp[i][j] = combine(val_left, val_center, val_right) + value[i][j];
    }
}
```

### 技巧 2：哨兵填充 (Sentinel Padding)

**通用模式：**

> 擴展 DP 表格，在周圍建立一圈「哨兵」，預先填入中性值（如 `infinity` 或 `0`）。這樣，核心迴圈的索引計算就無需任何邊界檢查。

**適用場景：**

- 轉移關係複雜，涉及多個方向的索引存取。
- 希望核心計算邏輯達到極致純粹與簡潔。

**偽代碼範例：**

```cpp
// C++ 偽代碼範例
// 表格大小為 (m+2) x (n+2)，周圍填充一圈哨兵
// NEUTRAL_VALUE 可能是 infinity 或 0
std::vector<std::vector<int>> dp(m + 2, std::vector<int>(n + 2, NEUTRAL_VALUE));

// 初始化非哨兵區域 (如果需要)
// ...

// 核心迴圈無需任何邊界檢查，索引從 1 開始
for (int i = 1; i <= m; ++i) {
    for (int j = 1; j <= n; ++j) {
        // 所有索引 (如 i-1, j-1, j+1) 都在 dp 表的合法範圍內
        auto val_up_left = dp[i - 1][j - 1];
        auto val_up = dp[i - 1][j];
        auto val_up_right = dp[i - 1][j + 1];

        // 注意 value 陣列的索引需要 -1 來對應原始座標
        dp[i][j] = combine(val_up_left, val_up, val_up_right) + value[i - 1][j - 1];
    }
}
```

### 技巧 3：明確的條件判斷 (Explicit `if-else`)

**通用模式：**

> 當邊界條件的邏輯非常特殊，無法用鉗制或哨兵一概而論時，回歸最原始的 `if-else` 判斷。

**適用場景：**

- 邊界上的轉移規則與內部完全不同。
- 問題的約束導致邊界行為複雜。

**偽代碼範例：**

```cpp
for (int i = 0; i < m; ++i) {
    for (int j = 0; j < n; ++j) {
        if (i == 0 && j == 0) {
            dp[i][j] = value[i][j]; // 處理起點
            continue;
        }

        auto val_up = (i > 0) ? dp[i - 1][j] : NEUTRAL_VALUE;
        auto val_left = (j > 0) ? dp[i][j - 1] : NEUTRAL_VALUE;

        dp[i][j] = combine(val_up, val_left) + value[i][j];
    }
}
```

---

## 策略比較與實戰心法

| 策略                      | 最適用場景                         | 優點                     | 缺點                       |
| ------------------------- | ---------------------------------- | ------------------------ | -------------------------- |
| **入口剪枝 (Top-Down)**   | 狀態空間稀疏，或遞迴思考更自然時   | 邏輯清晰，易於實現       | 遞迴深度可能導致堆疊溢位   |
| **索引鉗制 (Bottom-Up)**  | 邊界值可安全重複使用時             | 程式碼簡潔，無額外空間   | 需要思考鉗制後的語意正確性 |
| **哨兵填充 (Bottom-Up)**  | 轉移關係複雜，希望核心邏輯最純粹時 | 核心邏輯最乾淨，不易出錯 | 額外空間，索引映射需小心   |
| **明確 `if` (Bottom-Up)** | 邊界情況非常特殊，無法一概而論時   | 直觀，能處理複雜邊界邏輯 | 程式碼冗長，易出錯         |

**最終心法：**

> **Top-Down** 傾向於用 **入口剪枝** 將複雜性隔離在函式開頭，保持核心邏輯的純粹。**Bottom-Up** 則提供一個工具箱（`if`、鉗制、哨兵），讓你根據問題的特性，在 **程式碼簡潔性** 與 **邏輯直觀性** 之間做出權衡。對於大多數競賽問題，**索引鉗制** 和 **哨兵填充** 是最能體現實力且不易出錯的優雅技巧。

> 字串 / 雙序列 DP 裡「`i` 是長度還是 index」、「`i == m` 算不算越界」的混淆，見 [Index_as_Cut.md](../../../Data_Structures/Arrays_and_Strings/Index_as_Cut.md)：`i` 是切點，`i == m` 是合法的空剩餘狀態。
