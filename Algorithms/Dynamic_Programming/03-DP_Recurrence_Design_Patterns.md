# DP 的直觀解法：遞迴關係的設計模式

當問題的最優子結構特性非常明顯時，我們可以跳過完整的從回溯到 DP 的推導，憑直覺快速建立遞迴關係式，並直接開發出高效的 Bottom-Up 解法。

本文件旨在闡述此過程中，兩種最常見的遞迴關係設計模式。

---

## 第一步：定義最優子結構 (Define the Optimal Substructure)

忘掉程式碼，專注於問題的數學模型。一個完整的遞迴模型（即最優子結構的體現）包含兩個核心部分：狀態定義和狀態轉移。

### 1.1 定義狀態 (Define the State)

這是描述子問題的第一步。用最簡潔的方式定義 `dp[i]` 的物理意義。它通常代表：

- **對於最優化問題：** 「考慮到第 `i` 個元素為止的最優解值（最大/最小）」。
- **對於計數問題：** 「處理到第 `i` 個元素為止的方法總數」。

### 1.2 建立狀態轉移 (Formulate the Recurrence Relation)

分析當前狀態 `dp[i]` 是如何由一個或多個「前置狀態」轉移而來的。這裡存在兩種核心模式：

#### 模式一：固定窗口依賴 (Fixed Window Dependency)

在這種模式下，`dp[i]` 的計算只依賴於固定的、常數個數的前置狀態。

- **特徵：** 狀態轉移只涉及 `dp[i-1]`, `dp[i-2]` 等少量前置狀態。
- **適用場景：** 問題的決策只與緊鄰的幾個狀態有關。
- **範例遞迴關係：**
  - **Fibonacci / Climbing Stairs:** `dp[i] = dp[i-1] + dp[i-2]`
  - **House Robber:** `dp[i] = max(dp[i-1], dp[i-2] + nums[i])`

#### 模式二：動態範圍依賴 (Dynamic Range Dependency) / 全歷史依賴

與固定依賴不同，此模式的遞迴關係是**動態的**。`dp[i]` 的計算不再是從固定的幾個選項中選擇，而是需要**迭代一個變動範圍內的所有可能選項**，從中找出最優解。這也常被稱為「全歷史依賴」，因為選擇範圍可能涵蓋所有 `j < i` 的狀態。

- **核心思想：** 遞迴關係本身包含一個迭代過程 (Iteration in the recurrence relation)。
- **特徵：** 狀態轉移方程通常寫成 `dp[i] = min/max(f(dp[j]))` for `j` in a specific range, e.g., `i-k <= j < i`。
- **適用場景：** 問題的決策依賴於一個可變長度的歷史區間。
- **範例：**
  - **Climbing Stairs (k steps):** 如果一次可以爬 `1` 到 `k` 階，則 `dp[i] = sum(dp[j])` for `i-k <= j < i` (計數問題)。
  - **Min Cost Climbing Stairs (k steps):** `dp[i] = min(dp[j] + cost[j])` for `i-k <= j < i` (最優化問題)。
  - **Longest Increasing Subsequence:** `dp[i] = 1 + max(dp[j])` for all `j < i` where `nums[j] < nums[i]`。

這種模式在 Bottom-Up 實現中，自然地會形成一個**巢狀迴圈**，外層迴圈計算 `dp[i]`，內層迴圈則實現遞迴關係中的迭代，以遍歷所有可能的決策選項。

---

## 第二步：確定基礎案例 (Determine Base Cases)

遞迴模型需要一個終點。基礎案例是模型中無法再分解、可以直接得知的初始值。

- **通用原則:** 基礎案例是遞迴關係的「錨點」。它們是問題規模小到其解可以直接從題目條件中得知，而**無需依賴任何其他 `dp` 狀態**的子問題。

---

## 第三步：迭代實現 (Bottom-Up Implementation)

有了遞迴模型和基礎案例，就可以將其翻譯為高效的 Bottom-Up 程式碼。

### 實現模式一：固定窗口依賴

```cpp
// 泛化模板
vector<ResultType> dp(n);
// 1. 初始化 Base Cases
dp[0] = base_val_0;
if (n > 1) dp[1] = base_val_1;

// 2. 迭代計算
for (int i = 2; i < n; ++i) {
    dp[i] = f(dp[i-1], dp[i-2], ...);
}
return dp[n-1];
```

### 實現模式二：動態範圍依賴 (全歷史依賴)

```cpp
// 泛化模板
vector<ResultType> dp(n, initial_base_value); // 設定初始解
for (int i = 0; i < n; ++i) {
    for (int j = 0; j < i; ++j) { // 遍歷歷史
        if (is_valid_transition(i, j)) {
            dp[i] = aggregate(dp[i], calculate_new_value(dp[j]));
        }
    }
}
return final_result(dp);
```
