# 最大併發區間 解題心法 / Maximum Concurrent Intervals

## 🧠 核心哲學

當問題問「需要多少資源才能處理所有區間」或「最多同時發生幾個事件」時，這是**資源分配模擬問題**，而非合併區間問題。

**心智模型**: 會議室管理系統

- 會議開始 → 分配資源
- 會議結束 → 釋放資源
- 追蹤峰值 → 同時進行的最大會議數

**核心洞察**: Min Heap 動態維護活躍區間集合

```cpp
// Min Heap 存儲所有活躍區間的結束時間
priority_queue<int, vector<int>, greater<int>> minHeap;

// Invariant: 堆中元素 = 已開始但未結束的區間
// heap.size() = 當前需要的資源數量
```

## 🧩 標準模板

```cpp
// Step 1: 按開始時間排序（掃描線的時間軸）
sort(intervals.begin(), intervals.end());

// Step 2: Min Heap 追蹤活躍區間的結束時間
priority_queue<int, vector<int>, greater<int>> heap;
int maxConcurrent = 0;

// Step 3: 按時間順序處理每個區間
for (auto& interval : intervals) {
    int start = interval[0], end = interval[1];
    
    // 釋放所有已結束的區間（掃描線推進）
    while (!heap.empty() && heap.top() <= start)
        heap.pop();
    
    // 當前區間開始，佔用新資源
    heap.push(end);
    
    // 記錄峰值（最大併發數）
    maxConcurrent = max(maxConcurrent, (int)heap.size());
}

return maxConcurrent;
```

**複雜度**: 時間 O(n log n)，空間 O(n)

**Heap Invariant（不變性）**:

- 堆僅包含「已開始但未結束」的區間
- [`heap.top()`](heap.top():int) = 最早結束的區間
- [`heap.size()`](heap.size():size_t) = 當前時刻需要的資源數

## 🔍 兩種實作策略比較

### 策略 A: 動態追蹤當前併發（推薦）✅

```cpp
for (auto& interval : intervals) {
    // 釋放所有已結束的區間
    while (!heap.empty() && heap.top() <= interval[0])
        heap.pop();
    
    heap.push(interval[1]);
    maxConcurrent = max(maxConcurrent, (int)heap.size());
}
return maxConcurrent;
```

**Heap Invariant**: [`heap.size()`](heap.size():size_t) 始終等於當前併發數

**優勢**:

- Invariant 明確：任何時刻堆大小都有清晰意義
- 符合真實場景：完整模擬資源分配過程
- 易於擴展：可追蹤峰值發生時刻等額外信息
- 易於除錯：每步的堆狀態都有明確語義

### 策略 B: 累積資源計數

```cpp
for (int i = 1; i < intervals.length; i++) {
    // 僅釋放一個最早結束的區間
    if (intervals[i][0] >= heap.peek())
        heap.poll();
    
    heap.push(intervals[i][1]);
}
return heap.size(); // 最終堆大小即為答案
```

**Heap Invariant**: [`heap.size()`](heap.size():size_t) 等於累積分配的資源總數

**劣勢**:

- Invariant 模糊：過程中堆大小無明確意義
- 需額外證明：為何「僅釋放一個」是正確的
- 不符合直覺：未完整模擬真實資源管理
- 難以擴展：無法追蹤中間狀態

**執行對比** (`intervals = [[0,30],[5,10],[15,20]]`):

| 時刻 | 策略 A (動態追蹤) | 策略 B (累積計數) |
|------|------------------|------------------|
| [0,30] | heap=[30], max=1 | heap=[30], size=1 |
| [5,10] | heap=[10,30], max=2 ✅ | heap=[10,30], size=2 |
| [15,20] | heap=[20,30], max=2 | heap=[20,30], size=2 ✅ |

**建議**: 使用策略 A，因為程式碼意圖清晰、不變性明確、易於維護與擴展。

## 適用場景

| 問題類型 | 描述 | LeetCode |
|---------|------|---------|
| Meeting Rooms | 需要多少會議室 | 253 |
| CPU Scheduling | 需要多少 CPU 核心 | - |
| Parking Allocation | 停車場需要多少車位 | - |
| Event Overlap | 最多同時發生幾個事件 | - |

**識別關鍵字**:

- "minimum number of resources"
- "maximum concurrent events"
- "how many rooms/servers/cores needed"

## Interval 問題分類

| Pattern | 問題描述 | 算法 | 返回值 | LeetCode |
|---------|---------|------|--------|---------|
| Merge Intervals | 合併重疊區間 | Sort + Greedy | 區間列表 | 56 |
| Maximum Concurrent | 資源分配 | Sweep Line + Heap | int | 253 |
| Interval Scheduling | 最多不重疊活動 | Sort + Greedy | int | 435 |

## ⏱️ 複雜度分析

| 操作 | 時間 | 空間 | 說明 |
|-----|------|------|------|
| 排序 | O(n log n) | O(1) ~ O(n) | 依排序算法而定 |
| Heap 操作 | O(n log n) | O(n) | 每區間 push/pop 各一次 |
| **總計** | **O(n log n)** | **O(n)** | 瓶頸在排序 |

## ✅ 核心要點

- [ ] 按開始時間排序是必要前提，作為掃描線的時間軸
- [ ] Min Heap 維護活躍區間的結束時間
- [ ] 堆大小表示當前資源需求
- [ ] 處理新區間前必須釋放已結束資源
- [ ] 堆頂始終是最早結束的區間，便於快速釋放
- [ ] 與 Merge Intervals 概念完全不同
- [ ] 這是模擬算法 (Simulation Algorithm)，不涉及選擇決策
