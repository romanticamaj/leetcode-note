# C++ STL 心法：深入理解 `lower_bound` 與 `upper_bound`

在 C++ STL 中，`lower_bound` 和 `upper_bound` 是非常有用的二分搜尋演算法，主要用於在**已排序**的序列中快速查找元素。然而，它們的命名和行為常常會讓初學者感到困惑。

## 核心概念：尋找插入點

理解這兩個函式的關鍵在於，不要把它們想成是「尋找元素」，而是「**尋找一個合適的插入點**」，使得插入新元素後序列仍然保持有序。

- `lower_bound(key)`：尋找第一個**可以**插入 `key` 而不破壞排序的位置。這個位置上的現有元素的值必然 **大於或等於 (>=)** `key`。
- `upper_bound(key)`：尋找最後一個**可以**插入 `key` 而不破壞排序的位置。這個位置上的現有元素的值必然 **嚴格大於 (>)** `key`。

### 為什麼這樣命名？

這個命名源於數學中區間的概念：

- **Lower Bound (下界)**：在一個集合中，所有大於或等於某個數 `x` 的元素中，最小的那一個。`lower_bound` 回傳的正是這個「下界」元素的迭代器。
- **Upper Bound (上界)**：在一個集合中，所有嚴格大於某個數 `x` 的元素中，最小的那一個。`upper_bound` 回傳的正是這個「上界」元素的迭代器。

**一個簡單的記憶法**：

- `lower_bound` 包含「等於」的情況 (`>=`)。
- `upper_bound` 不包含「等於」的情況 (`>`)。

---

## `std::map` 和 `std::vector` 中的應用

這兩個函式在 `std::vector`（或任何提供隨機存取迭代器的已排序序列）和 `std::map`（或 `std::set`）中都可以使用，但用法略有不同。

### 1. 在 `std::vector`（已排序）上使用

需要傳入迭代器範圍 `(begin, end)`。

```cpp
#include <iostream>
#include <vector>
#include <algorithm>

int main() {
    std::vector<int> v = {10, 20, 30, 30, 30, 40, 50};

    // 尋找 >= 30 的第一個元素
    auto it_lower = std::lower_bound(v.begin(), v.end(), 30);
    // it_lower 指向索引 2 的 30

    // 尋找 > 30 的第一個元素
    auto it_upper = std::upper_bound(v.begin(), v.end(), 30);
    // it_upper 指向索引 5 的 40

    std::cout << "First element >= 30 is at index: " << std::distance(v.begin(), it_lower) << std::endl;
    std::cout << "First element > 30 is at index: " << std::distance(v.begin(), it_upper) << std::endl;

    // 計算等於 30 的元素個數
    std::cout << "Count of 30s: " << std::distance(it_lower, it_upper) << std::endl;
}
```

### 2. 在 `std::map` 上使用

`std::map` 本身就是有序的，所以可以直接呼叫其成員函式，效率更高。

```cpp
#include <iostream>
#include <map>

int main() {
    std::map<std::string, int> m = {
        {"apple", 10},
        {"banana", 20},
        {"cherry", 30},
        {"date", 40}
    };

    // 尋找鍵 >= "banana" 的第一個元素
    auto it_lower = m.lower_bound("banana");
    // it_lower 指向 {"banana", 20}

    // 尋找鍵 > "banana" 的第一個元素
    auto it_upper = m.upper_bound("banana");
    // it_upper 指向 {"cherry", 30}

    std::cout << "Lower bound of 'banana': " << it_lower->first << std::endl;
    std::cout << "Upper bound of 'banana': " << it_upper->first << std::endl;
}
```

---

## 實用技巧：遍歷一個範圍內的元素

`lower_bound` 和 `upper_bound` 最強大的應用之一，就是**高效地遍歷一個特定範圍內的所有元素**。

假設你想遍歷 `map` 中所有鍵在 `[start_key, end_key]` 範圍內的元素。

```cpp
void print_range(const std::map<std::string, int>& m, const std::string& start_key, const std::string& end_key) {
    // 找到範圍的起始點 (>= start_key)
    auto it_start = m.lower_bound(start_key);

    // 找到範圍的結束點 (> end_key)
    auto it_end = m.upper_bound(end_key);

    std::cout << "Elements in range [" << start_key << ", " << end_key << "]:" << std::endl;

    // 從起始點遍歷到結束點
    for (auto it = it_start; it != it_end; ++it) {
        std::cout << "  " << it->first << ": " << it->second << std::endl;
    }
}

int main() {
    std::map<std::string, int> m = {
        {"a", 1}, {"b", 2}, {"c", 3}, {"d", 4}, {"e", 5}, {"f", 6}
    };
    print_range(m, "b", "e");
    // 輸出:
    // b: 2
    // c: 3
    // d: 4
    // e: 5
}
```

這個技巧利用了 `lower_bound` 找到範圍的起點，`upper_bound` 找到範圍的終點（不包含），從而可以高效地對一個子集進行操作，而無需遍歷整個容器。這在處理日誌、時間序列資料或任何需要範圍查詢的場景中都非常有用。
