# Kadane's Algorithm 心法 / Running State with Conditional Reset

## 🧠 核心哲學

將 O(n) 空間的 DP 優化為 O(1) 空間的滾動狀態，核心在於「何時延續累積，何時重置狀態」的貪婪決策。

Kadane 是 **DP 的空間優化形式**，通過 **Conditional Reset** 機制將記憶化陣列壓縮為單一滾動變數。

## 核心概念：從 DP 到 Kadane

```cpp
// 標準 DP（O(n) 空間）
dp[i] = max(nums[i], dp[i-1] + nums[i])

// Kadane（O(1) 空間）
current = max(nums[i], current + nums[i])
//        重置          延續累積
```

**核心問題**：延續好還是重置好？

- 延續會變差 → 重置（拋棄過去）
- 延續更優 → 累積（保留狀態）

## 通用模板 / General Template

```cpp
template<typename T>
T kadane(const vector<T>& nums) {
    T current = 0, best = INT_MIN;
    for (T x : nums) {
        current = max(x, current + x);  // 一行決策
        best = max(best, current);
    }
    return best;
}
```

**抽象模板**：

```cpp
for (x : input) {
    if (shouldReset(current, x))
        current = reset(x);
    else
        current = accumulate(current, x);
    best = updateBest(best, current);
}
```

## 🧩 設計模式 / Implementation Patterns

### Pattern 1: 和的累積（Maximum Subarray）

```cpp
current = max(nums[i], current + nums[i]);
// 等價於：if (current < 0) current = nums[i]; else current += nums[i];
```

**重置時機**：累積和 < 0

### Pattern 2: 長度追蹤（Increasing Subsequence）

```cpp
if (arr[i] > arr[i-1])
    length++;
else
    length = 1;
```

**重置時機**：條件中斷（不再遞增）

### Pattern 3: 雙向掃描（Bidirectional Constraints）

```cpp
// 左向掃描
for (int i = 1; i < n; i++)
    left[i] = condition(i) ? left[i-1] + 1 : baseValue;

// 右向掃描
for (int i = n-2; i >= 0; i--)
    right[i] = condition(i) ? right[i+1] + 1 : baseValue;

// 合併
result[i] = max(left[i], right[i]);
```

**關鍵**：兩個獨立的 Kadane 過程

**參考**：[Bidirectional Constraint Decomposition](../../Design_Principles/Bidirectional_Constraint_Decomposition.md)

## 適用場景 / Use Cases

**識別特徵**：

- 連續子段的最優性質
- 局部狀態可能「不值得延續」
- 可定義「重置條件」

**典型應用**：

- **基礎**：LeetCode 53, 121
- **長度追蹤**：LeetCode 674, 485
- **雙向掃描**：LeetCode 135, 845
- **2D/環形**：LeetCode 363, 918

## ⏱️ 複雜度分析

| 操作      | Time   | Space |
| --------- | ------ | ----- |
| 單次掃描  | O(n)   | O(1)  |
| 雙向掃描  | O(n)   | O(n)  |
| 2D Kadane | O(n²m) | O(m)  |

## 與其他模式的關聯

```
標準 DP (O(n) 空間)
    ↓ 狀態壓縮
Rolling Array
    ↓ 極致優化
Kadane (O(1) 空間)
    ↓ 延伸
雙向掃描變體 → Bidirectional Decomposition
```

**相關技巧**：

- **State Reduction**：維度壓縮
- **Conditional Reset**：條件重置決策
- **State Decomposition**：雙向掃描的理論基礎

## 🔗 Kadane 與 State Machine DP 的關係（LC 121 紀錄）

Kadane 是 **state machine DP 退化後的樣子**，不是另一種想法。以買賣股票為例：

```cpp
// State machine：兩個狀態 hold / cash
hold[i] = max(hold[i-1], -price[i]);            // 持有：繼續持有 or 今天買
cash[i] = max(cash[i-1], hold[i-1] + price[i]); // 空手：繼續空手 or 今天賣

// LC 121 只允許一次交易 → hold[i] 化簡為 -min(price[0..i])
// 代回 cash[i] 就是 price[i] - minSoFar，即 Kadane 形式
```

**關鍵**：

- State machine 不是從 121 想出來的，是從 **122（無限次交易）逼出來的**；121 是它的退化特例
- 單題 121 用 Kadane / min-tracking 即可；題目一加「交易次數 / 冷卻 / 手續費」，單變數就不夠，要升回 `hold / cash` 多狀態
- 設計方法見 [04-Recurrence_Design_Patterns.md 模式三：狀態機依賴](../Fundamentals/04-Recurrence_Design_Patterns.md) 與 [State_Decomposition.md Pattern 2：動作分解](./State_Decomposition.md)

## ✅ 關鍵要點 / Key Points

- [ ] Kadane 是 DP 的優化，不是獨立算法
- [ ] 核心是一行決策：`max(reset, accumulate)`
- [ ] 雙向掃描 = 兩個獨立 Kadane + 合併
- [ ] `best` 初始化為 `INT_MIN` 或 `nums[0]`
- [ ] 區分「當前狀態」與「全局最優」
- [ ] Running State 可延伸到多種 DP 設計
