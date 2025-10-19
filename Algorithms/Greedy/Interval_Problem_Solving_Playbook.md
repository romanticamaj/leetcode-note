# Interval 問題解題心法 (Playbook)

Interval 問題在 LeetCode 和面試中很常見。它們通常涉及處理一組區間，並根據它們的重疊關係進行合併、刪除、插入或查詢。掌握處理這些問題的核心模式和策略至關重要。

## 1. 核心思想：排序是第一步

**幾乎所有的 Interval 問題都可以透過排序來簡化。**

- **排序依據：** 通常是按照區間的 **起始點 (start time)** 進行升序排序。如果起始點相同，有時需要根據 **結束點 (end time)** 排序，具體取決於問題。
- **為什麼排序有效？** 排序後，你只需要處理當前區間與前一個（或後一個）區間的關係，而不用考慮所有其他區間。這將問題從 O(n^2) 的複雜度降低到 O(n log n)（排序）+ O(n)（遍歷），整體為 **O(n log n)**。這是一種 **Greedy** 的思想。

## 2. 關鍵技巧：合併重疊區間 (Merging Overlapping Intervals)

這是最常見的模式。排序後，遍歷區間並決定是否將當前區間與前一個合併。

**通用 C++ 模板：**

這個模板的核心概念是，在遍歷排序後的區間時，我們不斷地檢查當前區間是否可以與 `merged` 列表中的 **最後一個區間** 合併。如果可以，我們就地擴展（expand）最後一個區間的 `end`；否則，就表示一個新的不重疊區間開始了。

```cpp
#include <vector>
#include <algorithm>

// 假設區間定義為 vector<int> {start, end}
vector<vector<int>> merge(vector<vector<int>>& intervals) {
    // 1. 對所有區間進行排序
    std::sort(intervals.begin(), intervals.end());

    vector<vector<int>> merged; // result

    // 2. 開始遍歷所有區間
    for (int i = 0; i < intervals.size(); ++i) {
        const int start = intervals[i][0];
        const int end = intervals[i][1];

        // 3. 檢查重疊：當前區間的 start 是否小於等於 merged 最後一個區間的 end
        if (!merged.empty() && start <= merged.back()[1]) {
            // 合併操作：
            // 從 merged list 的 back() 開始擴展 end (expand end from merged.back())
            // 更新 merged 最後一個區間的 end 為兩者 end 的最大值
            merged.back()[1] = max(merged.back()[1], end);
        } else {
            // 無重疊：直接將當前區間加入 merged 列表
            merged.push_back(intervals[i]);
        }
    }

    return merged;
}
```

**範例：** `[1,3], [2,6], [8,10], [15,18]`

- 排序後：不變。
- `merged = [[1,3]]`
- 當前 `[2,6]`：`2 <= 3` (重疊)，合併後 `merged = [[1,6]]`
- 當前 `[8,10]`：`8 > 6` (不重疊)，`merged = [[1,6], [8,10]]`

## 3. Interval 問題分類與對應算法

**重要**: 不是所有 Interval 問題都用 Greedy 解決！根據問題類型選擇正確的算法技術。

| 問題類型 | 問題描述 | 算法技術 | 是否為 Greedy | 文檔位置 | LeetCode |
|---------|---------|---------|--------------|---------|----------|
| **Interval Merging** | 合併重疊區間 | Sort + Linear Scan | ✅ | 本檔案第2節 | 56 |
| **Interval Scheduling** | 選最多不重疊區間 | Sort by End + Greedy | ✅ | 本檔案 | 435 |
| **Maximum Concurrent** | 計算最大併發數/需要多少資源 | Sweep Line + Min Heap | ❌ | [`../Sweep_Line/02-Maximum_Concurrent_Intervals.md`](../Sweep_Line/02-Maximum_Concurrent_Intervals.md) | 253 |
| **Interval Covering** | 用最少區間覆蓋範圍 | Sort + Greedy | ✅ | 待補充 | 1024 |

**識別技巧**:

- **Merging**: 關鍵字「merge」「combine」「overlap」→ 合併重疊區間
- **Scheduling**: 關鍵字「maximum number of」「non-overlapping」→ 選最多區間
- **Concurrent**: 關鍵字「minimum resources」「how many rooms/servers」→ Sweep Line
- **Covering**: 關鍵字「minimum intervals to cover」→ 貪心覆蓋
