# Bottom-Up Divide and Conquer 解題策略

## 🧠 核心哲學

Bottom-up 分治法從最小的子問題開始，逐層向上建構解答。關鍵在於使用 **長度 (interval/size)** 作為狀態控制變數，系統性地管理子問題的規模。

## 子問題定義模型

### 狀態表示

```cpp
struct SubProblem {
    int start;     // 起始位置
    int length;    // 子問題長度/區間大小
    int end() { return start + length; }
};
```

### 核心迭代模式

```cpp
template<typename T>
void bottomUpDivideConquer(vector<T>& data) {
    int n = data.size();

    // 外層：控制子問題規模（指數成長）
    for (int interval = 1; interval < n; interval *= 2) {

        // 內層：遍歷所有該規模的子問題對
        for (int start = 0; start < n - interval; start += interval * 2) {
            int mid = start + interval;
            int end = min(start + interval * 2, n);

            // 合併相鄰的兩個長度為 interval 的子問題
            combine(data, start, mid, end);
        }
    }
}
```

## 🧩 設計模式

### 1. 長度狀態控制

```cpp
// 狀態演進：1 → 2 → 4 → 8 → ... → n
int interval = 1;
while (interval < n) {
    // 處理長度為 interval 的所有子問題
    processSubProblems(interval);
    interval *= 2;  // 指數成長
}
```

**討論**: 為什麼是 interval < n ? （不用考慮等於）

考慮 n == 1、interval == 1，不用進去 recurrence

**注意**: interval *= 2，必須兩倍擴展，才會是 O(nlogn) 的 Divide and Conquer

### 2. 配對合併策略

```cpp
// 每次迭代將相鄰的子問題配對
for (int i = 0; i < n - interval; i += interval * 2) {
    // 子問題 1: [i, i + interval)
    // 子問題 2: [i + interval, i + interval * 2)
    SubProblem left(i, interval);
    SubProblem right(i + interval, interval);

    // 合併成更大的子問題
    mergeSubProblems(left, right);
}
```

### 3. 邊界處理

```cpp
// 優雅處理最後一個不完整的子問題
int end = min(start + interval * 2, n);

// 或使用條件判斷
if (start + interval < n) {
    // 存在第二個子問題
    processEvenPair(start, interval);
} else {
    // 只有一個子問題（奇數情況）
    processOddSingle(start);
}
```

## 複雜度分析

### 時間複雜度

- 迭代層數：`O(log n)` - interval 指數成長
- 每層工作：`O(n)` - 處理所有元素
- 總複雜度：`O(n log n)`

### 空間複雜度

- 迭代實現：`O(1)` - 只需控制變數
- 輔助空間：依具體問題而定

## ✅ 關鍵設計要點

- **狀態定義**：使用 `(start, length)` 或 `(start, end)` 定義子問題
- **規模控制**：interval 從 1 開始，指數成長 (×2)
- **配對策略**：每次處理相鄰的等長子問題對
- **邊界處理**：最後的不完整子問題需特殊處理
- **迭代優勢**：避免遞迴開銷，空間效率更高

## 與 Top-Down 的對比

| 特性       | Bottom-Up        | Top-Down          |
| ---------- | ---------------- | ----------------- |
| 實現方式   | 迭代             | 遞迴              |
| 空間開銷   | O(1)             | O(log n) 呼叫堆疊 |
| 快取局部性 | 較好（連續存取） | 較差（跳躍存取）  |
| 直觀性     | 較低             | 較高              |
| 邊界處理   | 需要明確處理     | 自然終止          |
