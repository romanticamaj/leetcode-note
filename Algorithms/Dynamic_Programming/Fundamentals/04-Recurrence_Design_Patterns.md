# DP 遞迴關係的三大設計模式

當問題的最優子結構特性非常明顯時，我們可以跳過完整的從回溯到 DP 的推導，憑直覺快速建立遞迴關係式，並直接開發出高效的 Bottom-Up 解法。

本文件旨在闡述此過程中，三種最常見的遞迴關係設計模式。

---

## 核心步驟

一個完整的遞迴模型包含三個核心部分：狀態定義、狀態轉移、以及基礎案例。

### 1. 定義狀態 (Define the State)

這是描述子問題的第一步。用最簡潔的方式定義 `dp[i]` 的物理意義。它通常代表：

- **對於最優化問題：** 「考慮到第 `i` 個元素為止的最優解值（最大/最小）」。
- **對於計數問題：** 「處理到第 `i` 個元素為止的方法總數」。

### 2. 建立狀態轉移 (Formulate the Recurrence Relation)

分析當前狀態 `dp[i]` 是如何由一個或多個「前置狀態」轉移而來的。這裡存在三種核心模式：

#### 模式一：固定窗口依賴 (Fixed Window Dependency)

`dp[i]` 的計算只依賴於固定的、常數個數的前置狀態。

- **特徵：** 狀態轉移只涉及 `dp[i-1]`, `dp[i-2]` 等少量前置狀態。
- **適用場景：** 問題的決策只與緊鄰的幾個狀態有關。
- **範例：**
  - **Fibonacci / Climbing Stairs:** `dp[i] = dp[i-1] + dp[i-2]`
  - **House Robber:** `dp[i] = max(dp[i-1], dp[i-2] + nums[i])`

#### 模式二：動態範圍依賴 (Dynamic Range Dependency)

`dp[i]` 的計算需要**迭代一個變動範圍內的所有可能前置狀態**，從中找出最優解。這也常被稱為「全歷史依賴」。

- **核心思想：** 遞迴關係本身包含一個迭代過程 (Iteration in the recurrence relation)。
- **特徵：** 狀態轉移方程通常寫成 `dp[i] = min/max(f(dp[j]))` for `j` in a specific range。這在實現中自然會形成**巢狀迴圈**，導致 `O(N^2)` 的複雜度。
- **範例：**
  - **Longest Increasing Subsequence:** `dp[i] = 1 + max(dp[j])` for all `j < i` where `nums[j] < nums[i]`。

#### 模式三：狀態機依賴 (State Machine Dependency)

當問題的決策會產生幾種固定的後續狀態，且這些狀態之間存在明確的轉移關係時，我們可以將其模型化為一個狀態機。

- **核心思想：** 為每個「狀態」定義一個專屬的遞迴關係，讓它們互相更新。這可以看作是多個遞迴關係的耦合。
- **範例 (骨牌密鋪):**
  - `f[i]`: 鋪滿 `2xi` 區域的方法數。
  - `g[i]`: 鋪滿 `2xi` 區域但有一格突出的方法數。
  - `f(i)` 的計算會同時依賴 `f` 和 `g` 的前序狀態。

### 3. 確定基礎案例 (Determine Base Cases)

遞迴模型需要一個終點。基礎案例是模型中無法再分解、可以直接得知的初始值。它們是遞迴關係的「錨點」，無需依賴任何其他 `dp` 狀態。

---

## 優化與實現

### 「動態範圍依賴」的優化

模式二的 `O(N^2)` 複雜度瓶頸在於內層的線性掃描。優化的核心是將 `O(N)` 的掃描替換為 `O(1)` 的高效查詢。

- **技巧：使用 Hash Map (Unordered Map) 進行 `O(1)` 查詢**
  - **用途：** 當你需要快速判斷某個「值」是否存在於歷史狀態中，或需要取得其關聯的 DP 結果時。
  - **範例 (Longest Consecutive Sequence):** `dp[x] = 1 + dp[x-1]` 的轉移，可以透過 `unordered_map` 將對 `x-1` 的查找從 `O(N)` 降至 `O(1)`。
  - **結論：** 當你發現巢狀迴圈是在進行「搜索」時，思考是否能用 Hash Map 取代搜索，這是通往 `O(N)` 解的關鍵。

### Bottom-Up 實現模板

#### 模式一：固定窗口依賴

```cpp
vector<ResultType> dp(n);
dp[0] = base_val_0;
// ... init other base cases ...
for (int i = ...; i < n; ++i) {
    dp[i] = f(dp[i-1], dp[i-2], ...);
}
```

#### 模式二：動態範圍依賴

```cpp
vector<ResultType> dp(n, initial_val);
for (int i = 0; i < n; ++i) {
    for (int j = 0; j < i; ++j) { // 這個迴圈是優化的目標
        if (is_valid_transition(i, j)) {
            dp[i] = aggregate(dp[i], ...);
        }
    }
}
```

#### 模式三：狀態機依賴

```cpp
vector<ResultType> dp_f(n), dp_g(n);
dp_f[0] = base_f;
dp_g[0] = base_g;
// ... init other base cases ...
for (int i = ...; i < n; ++i) {
    dp_f[i] = f(dp_f[i-1], dp_g[i-1], ...);
    dp_g[i] = g(dp_f[i-1], dp_g[i-1], ...);
}
```
