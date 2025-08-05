# C++ 排序演算法比較：`std::sort`, `std::stable_sort`, 與 `container.sort()`

在 C++ 中，排序是基礎且頻繁的操作。標準庫提供了多種排序工具，主要包括通用的 `std::sort`、保證穩定性的 `std::stable_sort`，以及特定容器（如 `std::list`）的成員函式 `sort()`。理解它們的差異對於撰寫高效且正確的程式碼至關重要。

---

## 1. `std::sort` (`<algorithm>` 標頭檔)

`std::sort` 是 C++ 中最常用、最高效的通用排序演算法。

- **適用容器**:

  - 任何提供**隨機存取迭代器 (Random Access Iterator)** 的序列容器。
  - 主要包括：`std::vector`、`std::deque`、`std::array` 以及 C-style 陣列。
  - **不適用**於 `std::list` 或 `std::forward_list`，因其迭代器類型不符。

- **演算法與複雜度**:

  - **底層實現**: 通常為 **Introsort**（內省排序），它結合了快速排序、堆積排序和插入排序的優點，以在最壞情況下仍保持 O(N log N) 的時間複雜度。
  - **時間複雜度**: **O(N log N)** (平均與最壞情況)。
  - **空間複雜度**: **O(log N)**，主要來自遞迴呼叫堆疊。

- **穩定性 (Stability)**:

  - **不保證穩定**。`std::sort` 為了追求極致的效能，可能會改變相等元素的相對順序。

- **用法**:
  - `std::sort(begin, end)`：預設使用 `operator<` 進行升序排序。
  - `std::sort(begin, end, comparator)`：可傳入自定義比較器（如 Lambda 或函式物件）。

```cpp
#include <vector>
#include <algorithm>
#include <functional> // for std::greater

// 1. 預設升序排序
std::vector<int> v = {3, 1, 4, 1, 5, 9};
std::sort(v.begin(), v.end()); // v is now {1, 1, 3, 4, 5, 9}

// 2. 使用 Lambda 進行降序排序
std::sort(v.begin(), v.end(), [](int a, int b) {
    return a > b;
}); // v is now {9, 5, 4, 3, 1, 1}
```

---

## 2. `std::stable_sort` (`<algorithm>` 標頭檔)

當需要**保持相等元素原始相對順序**時，`std::stable_sort` 是首選。

- **適用容器**:

  - 與 `std::sort` 相同，適用於提供**隨機存取迭代器**的容器。

- **演算法與複雜度**:

  - **底層實現**: 通常為**合併排序 (Merge Sort)** 或其變體（如 Timsort）。
  - **時間複雜度**:
    - 在有足夠額外記憶體的情況下，可達到 **O(N log N)**。
    - 若記憶體不足，時間複雜度可能退化為 **O(N (log N)²)**。
  - **空間複雜度**:
    - 理想情況下為 **O(N)**，用於合併操作。若記憶體受限，則可能為 **O(log N)**。

- **穩定性 (Stability)**:

  - **保證穩定**。這是它與 `std::sort` 最核心的區別。

- **用法**:
  - 與 `std::sort` 完全相同。

```cpp
struct Item {
    int key;
    std::string value;
};

std::vector<Item> items = {{2, "B"}, {1, "A"}, {2, "C"}};

// 使用 stable_sort 按 key 排序
std::stable_sort(items.begin(), items.end(), [](const Item& a, const Item& b) {
    return a.key < b.key;
});
// items is now: {{1, "A"}, {2, "B"}, {2, "C"}}
// 注意：{2, "B"} 仍然在 {2, "C"} 之前，保持了原始順序。
```

---

## 3. `container.sort()` (容器成員函式)

某些不支援隨機存取的容器，會提供自己的成員函式 `sort()`，最典型的例子是 `std::list`。

- **適用容器**:

  - `std::list`
  - `std::forward_list`

- **演算法與複雜度**:

  - **底層實現**: 通常為**合併排序 (Merge Sort)**，因其不要求隨機存取，非常適合鏈結串列。
  - **時間複雜度**: **O(N log N)**。
  - **空間複雜度**: **O(1)**。這是其最大優勢，因為它直接重新連接節點指標，無需額外儲存空間。

- **穩定性 (Stability)**:

  - **保證穩定**。`std::list::sort` 的行為類似於 `std::stable_sort`。

- **用法**:
  - `l.sort()`：預設升序。
  - `l.sort(comparator)`：使用自定義比較器。

```cpp
#include <list>
std::list<int> l = {3, 1, 4, 1, 5, 9};
l.sort(); // l is now {1, 1, 3, 4, 5, 9}
```

---

## 4. 總結與選擇心法

| 特性           | `std::sort`                  | `std::stable_sort`           | `container.sort()` (`list`) |
| :------------- | :--------------------------- | :--------------------------- | :-------------------------- |
| **適用性**     | 隨機存取 (`vector`, `deque`) | 隨機存取 (`vector`, `deque`) | 特定容器 (`list`)           |
| **穩定性**     | **不保證**                   | **保證**                     | **保證**                    |
| **時間複雜度** | O(N log N)                   | O(N log N) ~ O(N(log N)²)    | O(N log N)                  |
| **空間複雜度** | O(log N)                     | O(N) 或 O(log N)             | **O(1)**                    |
| **底層演算法** | Introsort                    | Merge Sort / Timsort         | Merge Sort                  |

### 選擇心法

1. **預設選擇 `std::sort`**：對於 `std::vector`、`std::deque` 等容器，如果不需要穩定性，`std::sort` 通常是效能最佳的選擇。
2. **需要穩定性時，選擇 `std::stable_sort`**：當你需要保持相等元素的原始順序時（例如，按多個欄位排序），請使用 `std::stable_sort`。請注意它可能需要更多的記憶體。
3. **使用 `std::list` 時，必須用 `list::sort()`**：這是唯一適用於 `std::list` 的高效排序方法。如果你發現自己在 `list` 上頻繁排序，應重新評估 `list` 是否為當前場景的最佳資料結構。
