# 雙向約束分解 / Bidirectional Constraint Decomposition

## 🧠 核心哲學

當問題涉及局部雙向依賴時，將其分解為兩個獨立的單向約束，分別求解後合併。

這是一個**設計原則**，可與 Greedy、DP 等多種演算法結合。

## 核心概念：設計原則而非算法

**問題特徵**：

```
element[i] 必須同時滿足：
  - 與左鄰居的關係 R_left(i, i-1)
  - 與右鄰居的關係 R_right(i, i+1)
```

**設計原則**：

```
Step 1: 分解 - 化雙向為兩個單向
Step 2: 求解 - 獨立求解每個方向
Step 3: 重組 - merge(left, right)
```

**為何是設計原則？**

- 提供問題轉換框架
- 不限定實現方法
- 可與多種演算法結合

## 通用模板 / General Template

```cpp
template<typename T, typename Algorithm>
vector<T> bidirectionalDecomposition(
    const vector<T>& input, Algorithm solver) {

    // Step 1 & 2: 獨立求解兩個方向
    vector<T> left = solver.solveLeftToRight(input);
    vector<T> right = solver.solveRightToLeft(input);

    // Step 3: 重組
    vector<T> result(input.size());
    for (int i = 0; i < input.size(); i++) {
        result[i] = merge(left[i], right[i]);
    }
    return result;
}
```

**合併操作選擇**：

| 約束類型        | 操作       | 理由       |
| --------------- | ---------- | ---------- |
| AND（同時滿足） | `max(L,R)` | 取更嚴格的 |
| OR（任一即可）  | `min(L,R)` | 取代價小的 |
| 獨立貢獻        | `L + R`    | 累加貢獻   |

## 🧩 設計模式 / Implementation Patterns

### Pattern 1: Greedy + Bidirectional

```cpp
// Greedy 求解器（Kadane-like）
left[i] = condition(i) ? left[i-1] + 1 : baseValue;
right[i] = condition(i) ? right[i+1] + 1 : baseValue;
result[i] = max(left[i], right[i]);
```

**在 Greedy 框架中**：這是第三種實現模式（補充排序/堆驅動）

### Pattern 2: DP + Bidirectional

```cpp
// DP 狀態遞推
left[i] = dpTransition(left[i-1], input[i]);
right[i] = dpTransition(right[i+1], input[i]);
result[i] = merge(left[i], right[i]);
```

**與 State Decomposition**：方向分解的具體應用

## 適用場景 / Use Cases

**識別特徵**：

- [ ] 局部雙向依賴（i 依賴 i±1）
- [ ] 約束可分解為獨立方向
- [ ] 單次掃描無法同時滿足
- [ ] 有合適的 merge 操作

**典型問題**：

- **Greedy+雙向**：LeetCode 135, 845, 1671
- **DP+雙向**：LeetCode 42, 238, 1493
- **Hybrid**：LeetCode 1402, 1326

## ⏱️ 複雜度分析

| 操作     | Time | Space |
| -------- | ---- | ----- |
| Two-Pass | O(n) | O(n)  |
| 優化版本 | O(n) | O(1)  |

## 雙視角理解 / Dual Perspectives

### Greedy 視角

```
雙向約束 → 分解 → 左右各用 Greedy → 合併
證明：Exchange Argument / 下界論證
```

### DP 視角

```
耦合狀態 → 解耦 → 左右各用 DP → 重組
證明：最優子結構 + 重組保持性
```

### 統一視角

| 角度 | Greedy   | DP           | 設計原則     |
| ---- | -------- | ------------ | ------------ |
| 本質 | 雙向約束 | 雙向耦合狀態 | 局部雙向依賴 |
| 分解 | 約束分解 | 狀態解耦     | 問題降維     |
| 求解 | 局部貪婪 | 狀態遞推     | 基底演算法   |
| 合併 | 貪婪選擇 | 狀態重組     | merge()      |

**深層統一**：同一問題的不同理解層次

## 設計決策指南 / Design Guide

**何時使用？**

- ✅ 明確的雙向局部依賴
- ✅ 約束可獨立分解
- ✅ merge 保持正確性

**選擇基底演算法**：

- **Greedy**：局部最優 → 全局最優
- **DP**：最優子結構清晰
- **Hybrid**：兩方向性質不同

**vs 其他方法**：

- 單次掃描：若可解則不需分解
- 排序驅動：若有天然順序
- 雙指針：若可兩端向中間

## ✅ 關鍵要點 / Key Points

- [ ] 這是**設計原則**，可與多種演算法結合
- [ ] 核心是化雙向為兩個單向子問題
- [ ] Greedy 框架的第三種實現模式
- [ ] DP 中 State Decomposition 的方向分解應用
- [ ] merge 操作決定正確性（AND→max, OR→min）
- [ ] 兩方向獨立求解（可並行）
- [ ] 理解 Greedy 和 DP 雙視角的統一性
- [ ] 用 O(n) 空間換 O(n) 時間
