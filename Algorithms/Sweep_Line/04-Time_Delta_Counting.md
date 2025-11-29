# Event Time as Key + Delta Counting 解題心法

## 🧠 核心哲學

將 interval 問題轉換為「時間點的狀態變化量」問題，用 **delta counting** 配合 **running sum** 追蹤狀態。

**心智模型**: 銀行帳戶餘額追蹤

- 存款事件 → `+amount`，提款事件 → `-amount`
- 當前餘額 → running sum of all deltas
- 最高餘額 → 追蹤過程中的峰值

**核心洞察**: 用 `map<time, delta>` 取代追蹤具體區間對象

```cpp
map<int, int> events;  // time -> delta
events[start] += 1;    // 區間開始: +1
events[end] -= 1;      // 區間結束: -1
```

## 🧩 標準模板

```cpp
int maxConcurrent(vector<vector<int>>& intervals) {
    map<int, int> events;  // 自動排序

    // Step 1: 建立事件（delta）+ 排序
    for (auto& interval : intervals) {
        events[interval[0]] += 1;   // 開始: +1
        events[interval[1]] -= 1;   // 結束: -1
    }

    // Step 2: Sweep line + Running sum
    int runningCount = 0, maxCount = 0;
    for (auto& [time, delta] : events) {
        runningCount += delta;
        maxCount = max(maxCount, runningCount);
    }

    return maxCount;
}
```

**複雜度**: 時間 O(n log n)，空間 O(k) (k 為不同時間點數量，最壞 O(n))

## 📊 核心概念：Delta vs Absolute State

### Absolute State (絕對狀態)

```cpp
// 直接追蹤「當前活躍的區間集合」
set<int> activeIntervals;
activeIntervals.insert(id);  // +區間
activeIntervals.erase(id);   // -區間
int count = activeIntervals.size();
```

### Delta State (變化量狀態)

```cpp
// 只追蹤「狀態變化了多少」
map<int, int> deltas;
deltas[start] += 1;   // 狀態 +1
deltas[end] -= 1;     // 狀態 -1
// 用 running sum 還原絕對狀態
```

**Delta 優勢**:

- Space efficient: 不需要存儲所有活躍區間
- Automatic merging: 相同時間點的事件自動合併（`events[time] += delta`）
- Conceptual clarity: 符合 Prefix Sum 的思維模式

## 🎯 適用場景

**適合使用**:

- 只需要知道「最大併發數」（不需要知道是哪些區間）
- 時間點可能重複（多個區間在同一時間開始/結束）
- 問題可以抽象為「狀態的增減」

**不適合使用**:

- 需要知道「是哪個區間」結束
- 需要根據區間的額外屬性做決策
- 區間有優先級或權重
- 需要動態調整區間

## 🔗 相關概念

**Prefix Sum 思想**: Delta Counting 本質是 Prefix Sum

```cpp
prefix[i] = prefix[i-1] + nums[i]
// 等價於
runningCount = runningCount + delta[time]
```

詳見: [Running State Pattern](../Prefix_Sum/02_Running_State_Pattern.md) | [Sweep Line Core Concepts](01-Sweep_Line_Core_Concepts.md)

## ✅ 檢查清單

- [ ] 用 `map<time, delta>` 儲存時間點的變化量
- [ ] 區間開始 `+1`，結束 `-1`（或 `+weight` / `-weight`）
- [ ] Map 自動排序，無需手動 sort
- [ ] Running sum 累加 delta 得到當前狀態
- [ ] 追蹤過程中的峰值作為答案
- [ ] 適合「只需數量不需具體對象」的場景

## 📝 通用模板

```cpp
map<int, int> events;  // time -> delta

// 建立事件
for (auto& interval : intervals) {
    events[interval.start] += weight;   // 狀態增加
    events[interval.end] -= weight;     // 狀態減少
}

// 掃描線 + 前綴和
int runningState = 0, answer = 0;
for (auto& [time, delta] : events) {
    runningState += delta;
    answer = max(answer, runningState);  // 或其他聚合邏輯
}
```
