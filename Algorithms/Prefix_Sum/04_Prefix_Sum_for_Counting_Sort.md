# 心法：使用前綴和實現計數排序 (Counting Sort)

計數排序 (Counting Sort) 是一個非比較排序演算法，其核心思想是統計每個元素出現的次數，然後利用這些次數計算出每個元素在排序後陣列中的最終位置。前綴和 (Prefix Sum) 在這個計算過程中扮演了關鍵角色。

## 核心步驟

1. **計數 (Counting)**：統計輸入陣列中每個唯一元素出現的頻率。
2. **計算前綴和 (Prefix Sum)**：將計數陣列轉換為前綴和陣列。此時，前綴和陣列 `P[x]` 的值代表「小於或等於 `x` 的元素總個數」。
3. **放置 (Placement)**：遍歷原始陣列，根據前綴和陣列找到每個元素應放置的正確位置，並將其放入結果陣列中。為了保持排序的**穩定性 (Stability)**，通常會**反向遍歷**原始陣列。

---

## 關鍵心法與注意事項

### 1. 資料結構選擇：為何使用 `std::map`？

在實現計數排序時，我們需要一個資料結構來儲存元素的頻率。雖然 `unordered_map` 查詢效率高，但在這裡**必須使用 `std::map`**。

- **原因**：`std::map` 是一個基於紅黑樹的有序容器，它會自動根據鍵 (key) 的大小進行排序。當我們遍歷 `map` 來計算前綴和時，能夠保證是**從最小的元素遍歷到最大的元素**。這個有序性是計算正確前綴和的基礎。如果使用 `unordered_map`，遍歷順序是未定義的，計算出的前綴和將是無意義的。

```cpp
#include <map>
#include <vector>
#include <iostream>

void counting_sort_with_map(std::vector<int>& arr) {
    if (arr.empty()) return;

    // 步驟 1: 使用 std::map 進行計數，確保鍵有序
    std::map<int, int> counts;
    for (int x : arr) {
        counts[x]++;
    }

    // 步驟 2: 在 map 上原地計算前綴和
    int total = 0;
    for (auto& pair : counts) {
        total += pair.second;
        pair.second = total;
    }
    // 此時，counts[x] 的值變為「小於等於 x 的元素總數」

    // 步驟 3: 根據前綴和放置元素
    std::vector<int> sorted_arr(arr.size());
    for (int i = arr.size() - 1; i >= 0; --i) {
        int val = arr[i];

        // 此時 counts[val] 代表 val 這個元素在排序後陣列中的「結束位置+1」(1-based)
        // 我們可以把它看作是下一個可用位置的 index
        int& next_pos_idx = counts[val];
        sorted_arr[next_pos_idx - 1] = val; // 核心：1-based 索引轉換

        next_pos_idx--; // 更新位置，為下一個相同元素準備
    }

    arr = sorted_arr;
}
```

### 2. 索引轉換：從「個數」到「0-based Index」

這是實現中最容易出錯的地方。

- **前綴和的意義**：計算完前綴和後，`counts[x]` 的值代表「小於或等於 `x` 的元素總共有幾個」。例如，如果 `counts[10] = 5`，意味著小於等於 10 的元素有 5 個。
- **1-based 索引**：這 5 個元素在排序後的陣列中，將佔據第 1 到第 5 個位置。因此，`counts[x]` 的值天然對應的是一個 **1-based** 的結束位置。
- **轉換為 0-based Index**：在 C++ 中，陣列索引是 0-based 的。要將一個值為 `val` 的元素放入正確的位置，其索引應該是 `counts[val] - 1`。

**錯誤的寫法**：
`sorted_arr[counts[val]] = val;` // 會導致 out-of-bounds 錯誤

**正確的寫法**：
`sorted_arr[counts[val] - 1] = val;`

在放置完一個元素後，記得將 `counts[val]` 的值減一，這樣當下一個同樣值的元素出現時，它會被放置在前一個元素的左邊。

**反向遍歷**確保了原始陣列中排在後面的相同元素會先被放入結果陣列的右側，從而保證了排序的**穩定性 (Stability)**。若不在乎穩定性，正向遍歷也可以得到正確的排序結果。
