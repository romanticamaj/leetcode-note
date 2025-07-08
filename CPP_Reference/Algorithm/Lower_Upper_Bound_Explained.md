# C++ STL 心法：深入理解 `lower_bound` 與 `upper_bound`

在 C++ STL 中，`lower_bound` 和 `upper_bound` 是非常有用的二分搜尋演算法，主要用於在**已排序**的序列中快速查找。然而，它們的命名和行為常常會讓初學者感到困惑。

---

## 核心概念：尋找插入點

理解這兩個函式的關鍵在於，不要把它們想成是「尋找元素」，而是「**尋找一個合適的插入點**」，使得插入新元素後序列仍然保持有序。

- `lower_bound(key)`：尋找第一個**可以**插入 `key` 而不破壞排序的位置。這個位置上的現有元素的值必然 **大於或等於 (>=)** `key`。
- `upper_bound(key)`：尋找最後一個**可以**插入 `key` 而不破壞排序的位置。這個位置上的現有元素的值必然 **嚴格大於 (>)** `key`。

**一個簡單的記憶法**：

- `lower_bound` 包含「等於」的情況 (`>=`)，是**閉區間**的下界。
- `upper_bound` 不包含「等於」的情況 (`>`)，是**開區間**的上界。

---

## 在不同容器上的應用

### 1. 用於序列容器 (如 `std::vector`)

對於 `std::vector`、`std::deque` 等已排序的序列容器，我們使用 `<algorithm>` 頭文件中的 `std::lower_bound` 和 `std::upper_bound`。

#### 基本用法

```cpp
#include <iostream>
#include <vector>
#include <algorithm>
#include <iterator> // For std::distance

int main() {
    std::vector<int> v = {10, 20, 30, 30, 30, 40, 50};

    // 尋找 >= 30 的第一個元素
    auto it_lower = std::lower_bound(v.begin(), v.end(), 30);
    // it_lower 指向索引 2 的 30

    // 尋找 > 30 的第一個元素
    auto it_upper = std::upper_bound(v.begin(), v.end(), 30);
    // it_upper 指向索引 5 的 40
}
```

#### 如何取得索引

`lower_bound` 和 `upper_bound` 返回的是**迭代器 (iterator)**。如果需要將其轉換為整數索引，有兩種主要方法：

1. **迭代器減法 (推薦，僅限隨機存取迭代器)**

   - 對於 `std::vector`、`std::deque` 等提供**隨機存取迭代器**的容器，可直接用返回的迭代器減去起始迭代器。
   - **用法：** `size_t index = it - container.begin();`

2. **`std::distance` (通用方法)**
   - 這是最標準的方法，適用於所有類型的迭代器。
   - **用法：** `size_t index = std::distance(container.begin(), it);`

對於 `std::vector`，迭代器減法更簡潔。但若編寫通用模板程式碼，`std::distance` 更安全。

---

### 2. 用於關聯式容器 (如 `std::map`)

對於 `std::map`、`std::set` 等本身已有序的容器，應使用其**成員函式** `lower_bound` 和 `upper_bound`，效率更高。

#### 基本用法

```cpp
#include <iostream>
#include <map>

int main() {
    std::map<std::string, int> m = {
        {"apple", 10}, {"banana", 20}, {"cherry", 30}, {"date", 40}
    };

    // 尋找鍵 >= "banana" 的第一個元素
    auto it_lower = m.lower_bound("banana"); // it_lower 指向 {"banana", 20}

    // 尋找鍵 > "banana" 的第一個元素
    auto it_upper = m.upper_bound("banana"); // it_upper 指向 {"cherry", 30}

    std::cout << "Lower bound of 'banana': " << it_lower->first << std::endl;
    std::cout << "Upper bound of 'banana': " << it_upper->first << std::endl;
}
```

#### 關於「索引」的討論

**關聯式容器沒有數字索引。**

- **內部結構：** `std::map` 等容器內部通常是紅黑樹，根據**鍵 (key)** 來排序，而非 `0, 1, 2, ...` 的線性位置。
- **迭代器類型：** 其迭代器是**雙向迭代器**，不支持 `O(1)` 的指針運算（如 `it - begin()`）。
- **`std::distance` 的效能陷阱：** 雖然仍可使用 `std::distance(m.begin(), it)`，但其時間複雜度是 **`O(n)`**，因為它必須從頭遍歷來計算距離。這會完全抵消二分搜尋 `O(log n)` 的效率優勢。

**結論：** 對於 `std::map` 或 `std::set`，我們應該直接使用返回的**迭代器**進行操作，而不是試圖將其轉換成一個沒有意義且低效的數字“索引”。

---

## 實用技巧

### 1. 計算重複元素個數

利用 `lower_bound` 和 `upper_bound` 返回的迭代器，可以高效計算出等於某個值的元素數量。

```cpp
// v = {10, 20, 30, 30, 30, 40, 50};
auto it_lower = std::lower_bound(v.begin(), v.end(), 30); // 指向第一個 30
auto it_upper = std::upper_bound(v.begin(), v.end(), 30); // 指向 40
auto count = std::distance(it_lower, it_upper); // count is 3
```

### 2. 遍歷一個範圍內的元素

這是最強大的應用之一，可以高效地遍歷一個特定範圍內的所有元素。

```cpp
void print_range(const std::map<std::string, int>& m, const std::string& start_key, const std::string& end_key) {
    auto it_start = m.lower_bound(start_key); // 範圍起點 (>= start_key)
    auto it_end = m.upper_bound(end_key);     // 範圍終點 (> end_key)

    for (auto it = it_start; it != it_end; ++it) {
        std::cout << "  " << it->first << ": " << it->second << std::endl;
    }
}
```

這個技巧在處理日誌、時間序列資料或任何需要範圍查詢的場景中都非常有用。
