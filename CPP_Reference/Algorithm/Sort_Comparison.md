# C++ Sorting: `std::sort` vs. Container's `sort()`

在 C++ 中，排序是常見操作。主要有兩種方式：通用的 `std::sort` 演算法，以及某些容器（如 `std::list`）提供的成員函式 `sort()`。兩者在效能、用法和適用性上有顯著差異。

---

## 1. `std::sort` (`<algorithm>` 標頭檔)

`std::sort` 是一個通用的、高效能的排序演算法。

- **適用容器**:

  - 任何提供**隨機存取迭代器 (RandomAccessIterator)** 的序列容器。
  - 主要包括：`std::vector`、`std::deque`、`std::array` 以及 C-style 陣列。
  - **不適用**於 `std::list`、`std::forward_list`（因為它們只有雙向或單向迭代器），也不適用於 `std::map`、`std::set`（因為它們內部已有序）。

- **時間複雜度**:

  - **平均**: O(N log N)。
  - **最壞**: O(N log N)。
  - C++ 標準庫通常使用 **Introsort**（內省排序），它結合了快速排序、堆積排序和插入排序的優點，以保證在各種情況下都有高效能。

- **空間複雜度**:

  - **O(log N)**。
  - 這是 Introsort 遞迴呼叫堆疊所需的空間。

- **用法**:
  - `std::sort` 是一個非成員函式，需要傳入指向序列頭尾的迭代器。
  - **預設排序**：使用 `operator<`，結果為升序（小到大）。
  - **自定義排序**：可傳入第三個參數作為比較器，且此參數必須是物件 (與容器不同，容器是帶入型別)。

```cpp
#include <iostream>
#include <vector>
#include <algorithm>
#include <functional> // for std::greater

int main() {
    std::vector<int> v = {3, 1, 4, 1, 5, 9};

    // 1. 預設升序排序
    std::sort(v.begin(), v.end());
    // v 現在是 {1, 1, 3, 4, 5, 9}

    // 2. 使用 std::greater 進行降序排序
    std::sort(v.begin(), v.end(), std::greater<int>());
    // v 現在是 {9, 5, 4, 3, 1, 1}

    // 3. 使用 Lambda 進行自定義排序 (例如，按絕對值大小)
    std::vector<int> v2 = {-5, 3, -1, 4};
    std::sort(v2.begin(), v2.end(), [](int a, int b) {
        return std::abs(a) < std::abs(b);
    });
    // v2 現在是 {-1, 3, 4, -5}
}
```

---

## 2. `container.sort()` (容器成員函式)

某些不支援隨機存取的容器，會提供自己的成員函式 `sort()`。最典型的例子是 `std::list`。

- **適用容器**:

  - `std::list`
  - `std::forward_list`

- **時間複雜度**:

  - **O(N log N)**。
  - `std::list::sort()` 通常使用**合併排序 (Merge Sort)**，因為合併排序不需要隨機存取，且對鏈結串列這種資料結構特別高效。

- **空間複雜度**:

  - **O(1)** 或 **O(log N)**，取決於實作。
  - 對於鏈結串列，合併排序可以透過重新連接節點指標來完成，因此通常可以達到 O(1) 的額外空間，遠優於 `std::sort`。

- **用法**:
  - `sort()` 是容器的成員函式，直接在物件上呼叫。
  - **預設排序**：同樣使用 `operator<`，結果為升序。
  - **自定義排序**：可傳入一個比較器作為參數，且此參數必須是物件。

```cpp
#include <iostream>
#include <list>
#include <functional> // for std::greater

int main() {
    std::list<int> l = {3, 1, 4, 1, 5, 9};

    // 1. 預設升序排序
    l.sort();
    // l 現在是 {1, 1, 3, 4, 5, 9}

    // 2. 使用 std::greater 進行降序排序
    l.sort(std::greater<int>());
    // l 現在是 {9, 5, 4, 3, 1, 1}

    // 3. 使用 Lambda 進行自定義排序
    std::list<int> l2 = {-5, 3, -1, 4};
    l2.sort([](int a, int b) {
        return std::abs(a) < std::abs(b);
    });
    // l2 現在是 {-1, 3, 4, -5}
}
```

---

## 3. 總結與比較

| 特性           | `std::sort` (`<algorithm>`)                 | `container.sort()` (e.g., `std::list::sort`) |
| :------------- | :------------------------------------------ | :------------------------------------------- |
| **適用性**     | 隨機存取迭代器 (`vector`, `deque`, `array`) | 特定容器的成員 (`list`, `forward_list`)      |
| **底層演算法** | Introsort (混合式)                          | Merge Sort (通常)                            |
| **時間複雜度** | O(N log N)                                  | O(N log N)                                   |
| **空間複雜度** | O(log N)                                    | O(1) 或 O(log N) (通常更優)                  |
| **呼叫方式**   | `std::sort(v.begin(), v.end());`            | `l.sort();`                                  |
| **優點**       | 通用性強，對快取友好 (cache-friendly)       | 針對特定容器高度優化，空間效率極高           |

### 選擇心法

- 如果你的資料儲存在 `vector`、`deque` 或陣列中，**永遠使用 `std::sort`**。
- 如果你的資料儲存在 `list` 中，**必須使用 `list::sort()`**，因為 `std::sort` 無法在其上工作。這也是 `list` 提供自己版本的原因。
- 如果你發現自己需要在 `list` 上頻繁排序，可能需要重新評估是否 `list` 是適合該場景的資料結構。
