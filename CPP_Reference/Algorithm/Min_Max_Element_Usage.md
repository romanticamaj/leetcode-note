# C++ STL 心法：`min_element` 與 `max_element` 使用指南

在 C++ STL 的 `<algorithm>` 頭文件中，`min_element` 和 `max_element` 是兩個非常實用的函式，用於在給定範圍內尋找最小和最大的元素。

---

## 核心概念：返回迭代器

最重要的一點是：這兩個函式返回的**不是值 (value)，而是指向目標元素的迭代器 (iterator)**。

- `std::min_element(begin, end)`: 返回指向範圍 `[begin, end)` 中最小元素的迭代器。
- `std::max_element(begin, end)`: 返回指向範圍 `[begin, end)` 中最大元素的迭代器。

如果有多個同樣小（或大）的元素，函式會返回**第一個**出現的該元素的迭代器。

---

## 基本用法

### 1. 取得最小值/最大值

要取得實際的值，需要對返回的迭代器進行**解引用 (dereference)**，即在前面加上 `*`。

```cpp
#include <iostream>
#include <vector>
#include <algorithm>

int main() {
    std::vector<int> v = {3, 1, 4, 1, 5, 9, 2, 6};

    auto it_min = std::min_element(v.begin(), v.end());
    auto it_max = std::max_element(v.begin(), v.end());

    // 使用 * 解引用來取得值
    std::cout << "Min value: " << *it_min << std::endl; // 輸出: 1
    std::cout << "Max value: " << *it_max << std::endl; // 輸出: 9
}
```

### 2. 取得索引

如果需要知道最小/最大元素的位置，可以使用 `std::distance` 或迭代器減法。

```cpp
// 接續上例
size_t index_min = std::distance(v.begin(), it_min);
size_t index_max = it_max - v.begin(); // 對於 vector 更簡潔

std::cout << "Min element is at index: " << index_min << std::endl; // 輸出: 1 (第一個 1 的位置)
std::cout << "Max element is at index: " << index_max << std::endl; // 輸出: 5
```

### 3. 處理空容器

如果傳入的範圍是空的（例如，`v.begin() == v.end()`），這兩個函式會返回 `end` 迭代器。在使用結果前進行檢查是一個好習慣。

```cpp
if (it_min != v.end()) {
    // 安全地使用 it_min
}
```

---

## 使用自訂比較函式

`min_element` 和 `max_element` 都有一個可選的第三個參數，允許你傳入一個自訂的比較函式（或 Lambda 表達式），這在處理複雜資料結構或自訂排序規則時非常有用。

**比較函式的要求：**
它必須是一個二元謂詞 (Binary Predicate)，接受兩個參數並返回 `bool`。其語義應該是 `bool cmp(const Type& a, const Type& b)`，如果 `a` “小於” `b`，則返回 `true`。

### 範例：根據絕對值尋找元素

```cpp
#include <cmath>

int main() {
    std::vector<int> v = {-10, 3, -5, 8, 2};

    // 尋找絕對值最小的元素
    auto it_min_abs = std::min_element(v.begin(), v.end(),
        [](int a, int b) {
            return std::abs(a) < std::abs(b);
        });

    // 尋找絕對值最大的元素
    auto it_max_abs = std::max_element(v.begin(), v.end(),
        [](int a, int b) {
            return std::abs(a) < std::abs(b);
        });

    std::cout << "Min absolute value element: " << *it_min_abs << std::endl; // 輸出: 2
    std::cout << "Max absolute value element: " << *it_max_abs << std::endl; // 輸出: -10
}
```

---

## 一次性取得兩者：`std::minmax_element`

如果你需要同時找到最小值和最大值，使用 `std::minmax_element` 會比分別呼叫 `min_element` 和 `max_element` 更高效，因為它只需要遍歷一次序列。

- **返回值：** `std::pair<ForwardIt, ForwardIt>`，其中 `pair.first` 是指向最小值的迭代器，`pair.second` 是指向最大值的迭代器。

```cpp
int main() {
    std::vector<int> v = {3, 1, 4, 1, 5, 9, 2, 6};

    auto pair_it = std::minmax_element(v.begin(), v.end());

    std::cout << "Min value: " << *pair_it.first << std::endl;  // 輸出: 1
    std::cout << "Max value: " << *pair_it.second << std::endl; // 輸出: 9
}
```
