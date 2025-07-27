# Difference Array 演算法心法 (基於半開區間 `[left, right)`)

## 核心概念

差分陣列 (Difference Array) 是一種高效處理區間事件 (interval-based problems) 的演算法技巧。其核心思想是 **將對一個連續區間的操作，轉化為對其兩個端點的離散操作**，從而將單次區間更新的複雜度從 O(L) (L 為區間長度) 降至 O(1) 或 O(log N)。

本文統一採用在程式設計競賽和 C++ 標準庫中廣泛使用的 **半開區間 `[left, right)`** 作為標準定義。這表示一個事件的影響範圍包含 `left` 端點，但不包含 `right` 端點。

- **事件起點 (Pickup):** 在區間的左端點 `left`，我們記錄一個 `+value` 的變化。
- **事件終點 (Dropoff):** 在區間的右端點 `right`，我們記錄一個 `-value` 的變化，以抵銷先前 `+value` 的效果。

當我們沿著時間軸（或座標軸）從頭到尾遍歷所有事件端點，並使用一個 `running sum` 累計所有變化量時，這個 `running sum` 在任意點 `i` 的值，即代表了該點的瞬時狀態總和。

## 實作方法比較

根據問題中座標軸的範圍和事件的疏密程度，有三種主要的實作方法：

| 方法                                  | 適用場景                                 | 優點                           | 缺點                             | 時間複雜度 (Build + Walk)     |
| ------------------------------------- | ---------------------------------------- | ------------------------------ | -------------------------------- | ----------------------------- |
| 1. `std::map<int, int>`               | **稀疏、大範圍**的座標 (e.g., 1 to 10^9) | 寫法簡潔、自動排序、空間效率高 | 單次操作有對數時間 `logM` 的開銷 | `O(N log M + M)`              |
| 2. `std::vector<int>`                 | **密集、小範圍**的座標 (e.g., 0 to 1000) | 訪問速度最快 (O(1))            | 座標範圍大時會消耗巨量記憶體     | `O(Range + N)`                |
| 3. `std::vector<std::pair<int, int>>` | 介於兩者之間，或不希望使用 `map` 的場合  | 遍歷階段比 `map` 快            | 需要額外的手動排序步驟           | `O(N log N + N)` (排序是瓶頸) |

_註：N = 區間數量, M = 獨立端點數量, Range = 座標最大範圍_

---

## C++ 泛用模板

此模板以 `std::map` 為基礎，因其最具通用性。程式碼結構清晰地分為 **Build (建構差分)** 和 **Walk (遍歷求和)** 兩個核心階段。

```cpp
#include <iostream>
#include <vector>
#include <map>
#include <algorithm>

// 泛用模板，適用於需要計算區間疊加效果的問題
// 例如：計算最大重疊數、判斷是否超載、或計算每個點的最終狀態值
void differenceArrayExample(const std::vector<std::vector<int>>& intervals) {

    // === 1. Build: 建構差分映射表 ===
    // key: 時間點 (座標)
    // value: 該時間點的淨變化量
    std::map<int, int> diff;
    for (const auto& interval : intervals) {
        int left = interval[0];
        int right = interval[1];
        int value = interval[2];

        // 在左端點增加 value
        diff[left] += value;
        // 在右端點減少 value，以符合 [left, right) 的半開區間定義
        diff[right] -= value;
    }

    // === 2. Walk: 遍歷映射表以計算 running sum ===
    int running_sum = 0;
    int max_value = 0;

    // std::map 的遍歷會自動按 key (時間點) 從小到大排序
    for (const auto& [time, change] : diff) {
        // 累加當前時間點的變化量
        running_sum += change;

        // 在此處可以根據具體問題進行操作
        // 例如：更新最大值、檢查是否超過 capacity 等
        max_value = std::max(max_value, running_sum);
    }

    std::cout << "The maximum running sum is: " << max_value << std::endl;
}
```

### 其他方法的實現

#### 2. `std::vector<int>` 作法

```cpp
// 適用於座標範圍已知且不大的情況, e.g., 0 <= time <= 1000
const int MAX_TIME = 1001;
std::vector<int> diff_vec(MAX_TIME + 1, 0);

for (const auto& interval : intervals) {
    // 確保索引不越界
    if (interval[0] < MAX_TIME) diff_vec[interval[0]] += interval[2];
    if (interval[1] < MAX_TIME) diff_vec[interval[1]] -= interval[2];
}

int running_sum = 0;
for (int i = 0; i < MAX_TIME; ++i) {
    running_sum += diff_vec[i];
    // 在此處對 running_sum 進行操作
}
```

#### 3. `std::vector<std::pair<int, int>>` 作法

```cpp
std::vector<std::pair<int, int>> diff_pairs;
for (const auto& interval : intervals) {
    diff_pairs.push_back({interval[0], interval[2]});
    diff_pairs.push_back({interval[1], -interval[2]});
}

// 必須手動對時間點進行排序
std::sort(diff_pairs.begin(), diff_pairs.end());

int running_sum = 0;
for (const auto& [time, change] : diff_pairs) {
    running_sum += change;
    // 在此處對 running_sum 進行操作
}
```
