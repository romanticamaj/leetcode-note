# 分治結果累積策略

## 核心原則

**問題分類決定策略**：計算型 → Return-Based，構造型 → In-Place/External State

- **計算型**（返回數值）：max, sum, count
- **構造型**（構造結構）：數組、矩陣、樹

**關鍵**：構造型誤用 Return-Based 會有 O(n log n) vs O(n) 差距

---

## 策略對比

| 維度     | Return-Based | In-Place         | External State      |
| -------- | ------------ | ---------------- | ------------------- |
| 問題類型 | 計算型       | 構造型           | 構造型              |
| 狀態參數 | Range        | Range + Position | Range + Pos + State |
| Combine  | 顯式計算     | Base Case 寫入   | 遞迴順序隱式        |
| 推薦度   | ⚠️ 僅計算型  | ⭐⭐⭐           | ⭐⭐⭐              |

---

## Return-Based ⚠️ 僅計算型 (Counting)

```cpp
ValueType solve(Range range) {
    if (isBase(range))
        return computeBase(range);

    auto subs = split(range);
    vector<ValueType> results;

    for (auto& s : subs)
        results.push_back(solve(s));

    return calculate(results);  // max/min/sum (O(1))
}
```

---

## In-Place ⭐⭐⭐ 構造型首選

**設計原則**：

1. 位置參數告訴子問題「寫到哪裡」
2. Base Case 即 Combine（合併點前移）

```cpp
void solve(Range range, Result& result, Position pos) {
    if (isBase(range)) {
        result[pos] = computeValue(range);
        return;
    }

    auto subs = split(range);
    auto positions = calculatePositions(pos, subs);

    for (int i = 0; i < subs.size(); i++)
        solve(subs[i], result, positions[i]);
}
```

---

## External State ⭐⭐⭐ 遍歷順序相關

**核心洞察**：遞迴順序決定處理順序

### 模式 A：全局計數器

```cpp
class Solution {
    int counter = 0;

    void solve(Range r, Result& result, Pos pos) {
        if (isBase(r)) {
            result[pos] = counter++;
            return;
        }

        // 訪問順序決定全局計數器跳動順序
        solve(sub1, result, pos1);  // 先訪問 → 編號小
        solve(sub2, result, pos2);
    }
};
```

### 模式 B：顯式區間 (區域變數傳遞)

```cpp
void solve(Range r, int start, Result& result, Pos pos) {
    if (isBase(r)) {
        result[pos] = start;
        return;
    }

    int total = calculateTotal(r);
    int share = total / numChildren;

    for (int i = 0; i < numChildren; i++)
        solve(subRange[i], start + i * share, result, subPos[i]);
}
```

---

## 決策流程

```
計算型？ → Return-Based
  ↓ 否
構造型
  ├─ 依賴遍歷順序？ → External State
  └─ 位置可直接算？ → In-Place
```

---

## 關鍵要點

1. **計算型 vs 構造型** 決定策略
2. **Base Case 即 Combine**（In-Place 核心）
3. **遞迴順序決定處理順序**（External State 精髓）
4. **位置參數是關鍵**（告訴子問題寫哪裡）

---

## 相關

[State Design Across Recursive Paradigms](../Design_Principles/Recursion/State_Design_Across_Recursive_Paradigms.md)
