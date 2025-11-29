# 掃描線算法 解題心法 / Sweep Line Algorithm

## 🧠 核心哲學

將複雜的時間/空間問題轉換為「按事件順序處理」的問題，通過模擬掃描線從左到右（或從上到下）移動，動態維護狀態並記錄關鍵指標。

**心智模型**: 想像一條垂直線掃過問題空間

- 在關鍵**事件點**更新狀態
- 追蹤過程中的**峰值**或**累積值**
- 不做「選擇」決策，只做**狀態模擬**

## 核心概念：Event-Driven State Tracking

### 什麼是掃描線？

掃描線是一條想像中的線，按順序掃過所有重要位置（事件點）：

- **時間軸問題**: 掃描線 = 當前時間點
- **幾何問題**: 掃描線 = 垂直或水平線的位置

### 事件點 (Event Points)

將連續問題離散化為關鍵事件：

```cpp
struct Event {
    int position;     // 事件發生位置（時間/坐標）
    int type;         // 事件類型（START/END/POINT）
    // ... 其他相關資料
};
```

**關鍵**: 必須**排序**事件點，按位置順序處理

## 通用模板

```cpp
// Step 1: 提取事件點
vector<Event> events;
for (auto& item : input) {
    events.push_back({item.start, START, item});
    events.push_back({item.end, END, item});
}

// Step 2: 排序事件
sort(events.begin(), events.end());

// Step 3: 掃描線處理
State currentState;  // 當前狀態
Result answer;       // 最終答案

for (auto& event : events) {
    // 根據事件類型更新狀態
    currentState.update(event);

    // 記錄/更新答案
    answer = computeAnswer(currentState);
}

return answer;
```

## 🧩 典型應用場景

### 1. 區間問題 (Interval Problems)

**特徵**: 多個區間，需要處理重疊、併發或覆蓋

| 問題         | 事件點        | 狀態                    | 答案       | LeetCode |
| ------------ | ------------- | ----------------------- | ---------- | -------- |
| 最大併發數   | 區間開始/結束 | 活躍區間集合 (Min Heap) | 最大堆大小 | 253      |
| 區間重疊檢測 | 區間開始/結束 | 當前重疊數              | 是否 > 1   | -        |
| 天際線       | 建築開始/結束 | 活躍高度集合            | 高度變化點 | 218      |

**範例**: Maximum Concurrent Intervals

```cpp
sort(intervals.begin(), intervals.end());
priority_queue<int, vector<int>, greater<int>> heap;  // Min heap
int maxConcurrent = 0;

for (auto& [start, end] : intervals) {
    // 釋放已結束的區間
    while (!heap.empty() && heap.top() <= start)
        heap.pop();

    // 新區間開始
    heap.push(end);
    maxConcurrent = max(maxConcurrent, (int)heap.size());
}
```

### 2. 幾何問題 (Geometric Problems)

**特徵**: 矩形、線段的重疊面積或輪廓

**範例**: 矩形面積並集

- 事件點 = 矩形的左邊界/右邊界
- 狀態 = 當前 Y 軸的活躍線段
- 答案 = 累積面積

## ⏱️ 複雜度分析

| Operation | Time           | Space    | Notes          |
| --------- | -------------- | -------- | -------------- |
| 提取事件  | O(n)           | O(n)     | n = 輸入元素數 |
| 排序事件  | O(n log n)     | O(log n) | 主要瓶頸       |
| 狀態維護  | O(n log n)     | O(n)     | 若用 heap/set  |
| **Total** | **O(n log n)** | **O(n)** |                |

## Sweep Line vs 其他技術

| 特徵               | Sweep Line      | Greedy            | DP                  |
| ------------------ | --------------- | ----------------- | ------------------- |
| **有選擇決策**     | ❌ 否           | ✅ 是             | ✅ 是               |
| **需要證明正確性** | ❌ 否           | ✅ 是（交換論證） | ✅ 是（最優子結構） |
| **本質**           | 狀態模擬        | 局部最優選擇      | 全局最優求解        |
| **關鍵操作**       | 排序 + 狀態更新 | 排序 + 貪婪選擇   | 狀態轉移            |

**關鍵區別**:

- Sweep Line 處理**所有**輸入，沒有「選或不選」
- Greedy 在候選項中**選擇**最優解
- DP 探索**多個**可能性並選最優

## ✅ 識別檢查點

使用 Sweep Line 當問題符合：

- [ ] 涉及**多個區間**或**幾何形狀**
- [ ] 需要處理「重疊」「併發」「覆蓋」
- [ ] 可以將問題分解為**離散事件點**
- [ ] 狀態隨時間/位置**連續變化**
- [ ] **不需要**做「選或不選」的決策
- [ ] 需要追蹤「某個時刻的狀態」或「峰值」

## 常見錯誤

❌ **誤用 Greedy 思維**

- Sweep Line 不是在「選擇」，是在「模擬」
- 所有輸入都必須處理，沒有篩選

❌ **忘記排序事件**

- 掃描線必須按順序移動
- 排序是算法的必要前提

❌ **狀態維護錯誤**

- 必須正確更新狀態（新增/移除）
- 狀態的不變性 (invariant) 要清晰

## 進階技巧

**事件排序的細節**:

```cpp
// 當事件位置相同時，處理順序很重要
sort(events.begin(), events.end(), [](auto& a, auto& b) {
    if (a.position != b.position)
        return a.position < b.position;
    // 同位置：通常先處理 END 事件，再處理 START
    return a.type < b.type;  // END < START
});
```

**狀態容器選擇**:

- **計數器**: 簡單的併發數 → `int count`
- **Min Heap**: 追蹤最早結束時間 → `priority_queue`
- **Max Heap/Multiset**: 追蹤當前最大值 → 天際線問題
