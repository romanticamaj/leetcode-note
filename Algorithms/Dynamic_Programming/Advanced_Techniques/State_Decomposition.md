# 狀態空間分解 / State Space Decomposition

## 🧠 核心哲學

當 DP 狀態有多個耦合維度導致遞推困難時，將狀態空間分解為多個獨立子空間，分別優化後重組。

這是 DP 的**高級設計技巧**，用於處理多維耦合問題。

## 核心概念：Decomposition of State Space

**問題原型**：

```cpp
// 理想的遞推
dp[i] = f(dp[i-1], input[i])

// 實際困境
dp[i] = f(dp[i-1], dp[i+1], ...)  // 依賴未來信息！
```

**分解策略**：

```
原問題：狀態 S 耦合多個維度
    ↓ 分解
子問題 1-n：各維度獨立遞推
    ↓ 重組
最終解：merge(S₁, S₂, ..., Sₙ)
```

## 理論基礎 / Bertsekas Principle

**狀態空間表示**：

```
State = Dimension₁ × Dimension₂ × ... × Dimensionₙ
```

**分離性條件**：

- 目標函數可分解：`F = merge(F₁, F₂, ..., Fₙ)`
- 約束可分離：`C = C₁ ∧ C₂ ∧ ... ∧ Cₙ`

**核心定理**：若滿足分離性，則可獨立求解各維度，再重組為全局最優。

## 通用模板 / General Template

```cpp
template<typename T>
vector<T> stateDecomposition(const Input& input) {
    int n = input.size();

    // 定義 k 個子狀態空間
    vector<vector<T>> substates(K, vector<T>(n));

    // 獨立求解各子問題
    for (int k = 0; k < K; k++) {
        substates[k] = solveSubproblem(input, k);
    }

    // 重組
    vector<T> result(n);
    for (int i = 0; i < n; i++) {
        result[i] = merge(substates, i);
    }
    return result;
}
```

## 🧩 設計模式 / Implementation Patterns

### Pattern 1: 方向分解

```cpp
// 左向 DP
left[i] = optimal(left[i-1], input[i]);
// 右向 DP
right[i] = optimal(right[i+1], input[i]);
// 重組
result[i] = merge(left[i], right[i]);
```

**應用**：雙向依賴問題

**參考**：[Bidirectional Constraint Decomposition](../../Design_Principles/Bidirectional_Constraint_Decomposition.md)

### Pattern 2: 動作分解

```cpp
// 動作 A 的子狀態（如「持有」）
stateA[i] = transitionA(stateA[i-1], ...);
// 動作 B 的子狀態（如「不持有」）
stateB[i] = transitionB(stateB[i-1], ...);
// 重組（選最優）
result[i] = max(stateA[i], stateB[i]);
```

**應用**：狀態機 DP

### Pattern 3: 約束分解

```cpp
// 僅滿足約束 C₁
constrained1 = solveUnderC1(input);
// 僅滿足約束 C₂
constrained2 = solveUnderC2(input);
// 重組（同時滿足）
result[i] = max(constrained1[i], constrained2[i]);
```

**應用**：多重約束問題

## 分解決策框架 / Decision Framework

### Step 1: 識別耦合維度

- [ ] 依賴未來信息？
- [ ] 涉及多個子目標？
- [ ] 有多種互斥動作？

### Step 2: 評估可分離性

**獨立性測試**：各子狀態能否獨立遞推？

### Step 3: 選擇重組操作

| 約束類型 | 操作         | 理由       |
| -------- | ------------ | ---------- |
| AND      | `max(s₁,s₂)` | 取更嚴格的 |
| OR       | `min(s₁,s₂)` | 取代價小的 |
| 獨立貢獻 | `s₁+s₂`      | 累加       |
| 互斥選擇 | `max/min`    | 取最優     |

### Step 4: 證明正確性

1. 子問題最優性
2. 重組保持性
3. 完整性（涵蓋所有維度）

## 案例類型 / Case Studies

**方向分解**：LeetCode 135, 42, 238, 845s
**動作分解**：LeetCode 309, 714, 72, 123
**約束分解**：LeetCode 845, 1027, 1671

## ⏱️ 複雜度分析

| 分解類型 | Time  | Space |
| -------- | ----- | ----- |
| 雙向     | O(n)  | O(n)  |
| k 維     | O(kn) | O(kn) |

## DP vs Greedy 雙視角

| 角度   | DP                   | Greedy                 |
| ------ | -------------------- | ---------------------- |
| 本質   | 多維耦合狀態         | 多向約束               |
| 思路   | 狀態解耦 → DP → 重組 | 約束分解 → 掃描 → 合併 |
| 合併   | 狀態重組             | 貪婪選擇               |
| 正確性 | 最優子結構           | Exchange Argument      |

**統一性**：同一問題的不同理解層次

## 與其他技巧的關聯

```
Multi-dimensional DP
    ↓ 優化分支
State Decomposition (分解耦合維度)
    ↓ 特殊應用
Bidirectional Constraint (方向分解)
    ↓ 極致優化
Kadane (Running State)
```

## ✅ 關鍵要點 / Key Points

- [ ] 用於處理多維耦合的 DP 問題
- [ ] 核心是分解為獨立子空間，分別優化後重組
- [ ] 識別耦合維度是第一步
- [ ] 驗證獨立性是可行性前提
- [ ] 重組操作決定正確性
- [ ] 與 Greedy 約束分解有深層統一性
- [ ] Bertsekas 提供系統化理論框架
- [ ] Kadane 是單維分解的極致
