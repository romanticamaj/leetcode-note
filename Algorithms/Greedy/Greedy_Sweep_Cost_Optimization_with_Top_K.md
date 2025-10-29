# Greedy Sweep Cost Optimization with Top-K

## 🧠 核心哲學

沿 **multiplier 維度掃描**（Sweep），每步維護 **Top-K minimized sum**，追蹤全域最小 cost（非單調乘積 → 最小值可在**任何時刻**出現）。

**Sweep + Greedy 的關聯**: 排序 → 順序處理 → 動態維護最優狀態

## 核心概念

```
cost = pivot1 × sum(pivot2)
        ↑         ↓
    單調遞增   可優化遞減
```

**非單調乘積** → 最小值不在終點，需全程追蹤

## 通用模板

```cpp
double solve(vector<Item>& items, int k) {
    // Step 1: 建立 Min Heap (依 pivot1 遞增排序)
    MinHeap<pivot1, pivot2> sortedByMultiplier;
    for (auto& item : items)
        sortedByMultiplier.push({item.pivot1, item.pivot2});

    // Step 2: 維護 Top-K Max Heap (最小化 sum(pivot2))
    MaxHeap<pivot2> topK;
    int totalPivot2 = 0;
    double globalMin = INFINITY;

    // Step 3: 依序處理，每個 size==k 時更新全域最小值
    while (!sortedByMultiplier.empty()) {
        auto [multiplier, component] = sortedByMultiplier.top();
        sortedByMultiplier.pop();

        accumulate(totalPivot2, component);
        topK.push(component);

        // 維護恰好 k 個元素
        if (topK.size() > k) {
            eliminate(totalPivot2, topK.top());
            topK.pop();
        }

        // 追蹤全域最小值
        if (topK.size() == k) {
            globalMin = min(globalMin, multiplier * totalPivot2);
        }
    }
    return globalMin;
}
```

## 🧩 關鍵設計決策

### 1. Pivot 設計：Sweep 軸 vs 優化目標

**Pivot1 (Multiplier)**: **Sweep 的掃描軸**

- 類似 Sweep Line 的 x 軸或時間軸
- 必須可排序（單調性），沿此軸依序處理
- 每個 pivot1 值是一個「事件點」，觸發狀態更新
- 所選項目共用同一 multiplier（當前掃描位置）

**Pivot2 (Component)**: **動態維護的優化目標**

- 在每個掃描位置，維護 Top-K 最小 sum
- 類似 Sweep Line 在每個事件點更新「活躍集合」
- 累積總和影響最終 cost

### 2. 為何不用逐一替換？

❌ `if (newMultiplier × newSum < currentCost) replace()`

- 這樣只考慮到單項替換，但是最優解可能需同時替換多項

✅ `維護每個 multiplier 下的 Top-K minimum sum`

- 自動處理多項目替換，保證該 multiplier 下的最優組合

### 3. 為何要全程追蹤？

| Step | Multiplier | Sum | Cost    | 說明                           |
| ---- | ---------- | --- | ------- | ------------------------------ |
| 1    | 2.0        | 100 | 200     | 低 multiplier，高 sum          |
| 2    | 4.0        | 50  | **200** | 高 multiplier，低 sum - 平手！ |
| 3    | 5.0        | 45  | 225     | 最低 sum，但 multiplier 過高   |

**非單調性** → 無法預測最小值位置 → 每個 size==k 都要檢查

### 4. 當前項被踢出仍要計算？

**發生什麼**:

```
處理 item i (假設 pivot2[i] 最大):
  push pivot2[i] → sum 增加
  pop pivot2[i]  → sum 回退（狀態不變）

計算: pivot1[i] × sum_舊 = ?
```

**這代表什麼意義**:
「維持上一輪的 k 人組合，但被迫用當前更高的 multiplier (pivot1[i]) 支付」

**為什麼正確**:

- Pivot1 遞增 → pivot1[i] ≥ pivot1[舊組合]
- Sum 不變 → sum\*舊
- Cost 增加 → pivot1[i] × sum*舊 ≥ cost*舊
- 不會更新 global min，但**正確反映 multiplier 拉高的效應**

**Sum 非單調**:

- Push 小 pivot2 → sum ↓
- Push 大 pivot2 立即 pop → sum 不變

## 適用場景

**識別特徵**:

- [ ] Cost = multiplier × sum 結構
- [ ] Multiplier 可排序（單調性）
- [ ] Sum 可透過 Top-K selection 最小化
- [ ] 固定選擇 k 個項目

**應用題目**: LeetCode 857 (Minimum Cost to Hire K Workers)

## ⏱️ 複雜度

| 操作        | 時間       | 空間 |
| ----------- | ---------- | ---- |
| 建立 + 處理 | O(n log n) | O(n) |
| Top-K 維護  | O(n log k) | O(k) |

## ✅ 實作檢查清單

- [ ] 識別 pivot1 (multiplier) 與 pivot2 (sum component)
- [ ] 建立 Min Heap 依 pivot1 排序
- [ ] 用 Max Heap 維護 Top-K 最小 sum(pivot2)
- [ ] 在**每個** size==k 時更新 global min
- [ ] 即使當前項被踢出也要計算（安全的上界）
