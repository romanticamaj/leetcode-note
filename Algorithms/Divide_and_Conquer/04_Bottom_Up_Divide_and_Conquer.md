# Bottom-Up Divide and Conquer 解題策略

## 🧠 核心哲學

Bottom-up 分治法從最小的子問題開始，逐層向上建構解答。關鍵在於使用 **子問題長度 (interval)** 作為狀態控制變數，系統性地管理子問題的規模。

## 子問題定義模型

### 狀態表示

```cpp
struct SubProblem {
    int start;     // 起始位置
    int length;    // 子問題長度/區間大小
    int end() { return start + length; } // 不包含, 但可作為下一個子問題起點
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
        // 條件寫成 start + interval < n：意思是「右半塊還存在嗎」
        for (int start = 0; start + interval < n; start += interval * 2) {
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
for (int i = 0; i + interval < n; i += interval * 2) {
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

## 🔑 起手式：為什麼用「半塊大小」當迴圈變數

`interval` 代表的是**被合併的兩塊各自的大小**（半塊），不是合併後的大小。

### 迴圈不變量

> **進入 `interval = w` 這一輪時，所有長度為 `w` 的區塊都已經處理好了。**

因此 `interval` 從 **1** 開始不需要特例 — 長度 1 的區塊天生就是已解決的。若改用「合併後長度從 2 開始」當心智模型，反而要多解釋「長度 1 去哪了」。

### 兩個迴圈條件的意思（不用背）

| 條件 | 意思 |
| :--- | :--- |
| `interval < n` | 還有東西沒合併完（`interval >= n` 表示整個陣列已是一塊） |
| `i + interval < n` | **右半塊存在嗎** — 不存在就沒得合，留到下一輪 |

內層條件是最容易寫錯的地方：**不是 `i < n`**。這一輪要合併 `[i, i+interval)` 與 `[i+interval, i+2*interval)`，右半不存在就整塊跳過。

寫成 `i + interval < n` 而不是等價的 `i < n - interval`：前者直接讀作「**右半塊的起點還在範圍內嗎**」，後者要先在腦中移項。（另外若索引型別是 `size_t`，`n - interval` 還有下溢風險。）

### 對照：用「合併後大小」參數化會變醜

```cpp
// ✅ A：interval = 半塊
for (int interval = 1; interval < n; interval *= 2)
    for (int i = 0; i + interval < n; i += 2 * interval)
        combine(i, i + interval, min(i + 2 * interval, n));
//               ^^^^^^^^^^^^^^ mid 直接就是 i + interval

// ❌ B：size = 合併後大小
for (int size = 2; size / 2 < n; size *= 2)
    for (int i = 0; i + size / 2 < n; i += size)
        combine(i, i + size / 2, min(i + size, n));
//               ^^^^^^^^^^^^^ /2 出現三次
```

B 不是不能寫，而是 `mid = i + 半塊`，真正需要的量本來就是半塊；用合併後大小當變數，每個表達式都得再除回去。

---

## 與 Top-Down 的對比

| 特性       | Bottom-Up        | Top-Down          |
| ---------- | ---------------- | ----------------- |
| 實現方式   | 迭代             | 遞迴              |
| 空間開銷   | O(1)             | O(log n) 呼叫堆疊 |
| 快取局部性 | 較好（連續存取） | 較差（跳躍存取）  |
| 直觀性     | 較低             | 較高              |
| 邊界處理   | 需要明確處理     | 自然終止          |
