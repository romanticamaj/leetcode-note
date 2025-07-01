# STL 容器轉換心法：以迭代器為橋樑

在 C++ 中，尤其是在需要快速實現演算法的 LeetCode 刷題場景，熟悉 STL 容器間的轉換技巧非常關鍵。由於各容器在資料結構與操作介面上的差異，標準庫並不提供容器間的直接轉換。

**核心心法**：**利用「迭代器 (Iterators)」作為通用橋樑**。

**重要原則**：若元素型別之間可隱式轉換，就可直接使用迭代器範圍初始化不同容器。

大多數 STL 容器都提供接受一對迭代器 `(first, last)` 的構造函式，用以從任意序列（來源容器不限）初始化新容器。這是最通用且高效的轉換方式。

---

## 案例：使用迭代器將 `std::vector<int>` 轉換為 `std::priority_queue<double>`

以下案例展示同時進行容器型別與元素型別的轉換：

**問題**：能否直接使用 `std::vector<int>` 的迭代器初始化 `std::priority_queue<double>`？
**答案**：可以，且這是最高效且最推薦的做法。

## 關鍵機制：為何此類轉換可行？

此類轉換成功的關鍵機制包括：

1. **迭代器抽象**：C++ STL 的核心設計理念是將容器與演算法解耦，而迭代器正是連接兩者的橋樑。迭代器提供了一個統一的介面，使得不同容器的元素可以被以相同的方式訪問。
2. **模板參數推導**：容器的建構函式通常是模板函式，它們不關心迭代器的具體型別，只關心迭代器是否滿足特定的概念要求（如 `InputIterator`）。
3. **逐元素構造**：當使用迭代器範圍初始化容器時，容器會逐一讀取迭代器指向的元素，然後嘗試用這些元素來構造自己的元素。
4. **隱式型別轉換**：C++ 允許某些型別之間進行隱式轉換，例如 `int` 到 `double`、`derived*` 到 `base*` 等。在容器構造過程中，這些轉換會自動發生。
5. **容器配接器的特殊性**：`priority_queue`、`stack`、`queue` 等容器配接器實際上是包裝了一個底層容器（通常是 `vector` 或 `deque`）。當你用迭代器初始化它們時，實際上是在初始化它們的底層容器。

### 正確心法：使用迭代器範圍直接初始化

直接使用 `vector<int>` 的迭代器來構造 `priority_queue<double>` **是完全可行的**。

```cpp
// 這段程式碼是正確且高效的
#include <iostream>
#include <vector>
#include <queue>

int main() {
    std::vector<int> vec = {1, 8, 5, 6, 3, 4, 0, 9, 7, 2};

    // 正確：直接使用 `vec` 的迭代器初始化 `pq`
    // C++ 的模板機制會處理從 int 到 double 的隱式型別轉換
    std::priority_queue<double> pq(vec.begin(), vec.end());

    // 驗證結果
    std::cout << "Priority Queue elements (descending order):" << std::endl;
    while (!pq.empty()) {
        std::cout << pq.top() << " ";
        pq.pop();
    }
    std::cout << std::endl;
    // 預期輸出: 9 8 7 6 5 4 3 2 1 0

    return 0;
}
```

**轉換過程的底層機制**：

1. `priority_queue<double>` 的建構函式接受一對迭代器 `(first, last)`。
2. 在內部，它會創建一個 `vector<double>`（其底層容器）。
3. 對於迭代器範圍 `[vec.begin(), vec.end()]` 中的每個元素（型別為 `int`）：
   - 讀取該 `int` 值
   - 將其隱式轉換為 `double`
   - 將轉換後的 `double` 值插入到底層的 `vector<double>` 中
4. 最後，使用這個填充好的 `vector<double>` 來構造 `priority_queue`。

### LeetCode 中的快速心法

在解題時，速度和簡潔性至關重要。

**首選永遠是迭代器直接構造**。

```cpp
std::vector<int> source_vec = {1, 8, 5, 6, 3, 4, 0, 9, 7, 2};

// 一行完成初始化，這是最快、最好的寫法
std::priority_queue<double> pq(source_vec.begin(), source_vec.end());
```

---

## 替代方案：當隱式轉換不可行時

雖然迭代器直接構造非常強大，但在某些情況下，你可能需要更明確的控制，或者當型別之間無法隱式轉換時（例如，從 `std::pair` 轉換為自訂 `struct`），就需要手動處理。

### 1. 使用迴圈手動插入

最基礎但萬無一失的方法。

```cpp
std::priority_queue<double> pq;
for (int val : source_vec) {
    pq.push(val); // int 會被隱式轉換為 double
}
```

### 2. 使用 `std::transform`

當轉換邏輯更複雜時，`std::transform` 是個強大的工具。你需要一個可以插入元素的迭代器，例如 `std::back_inserter`，並搭配一個臨時容器。

```cpp
#include <algorithm>
#include <iterator>

struct MyData { double d; };
std::vector<int> source_vec = {1, 5, 2};
std::vector<MyData> target_vec;

// 使用 transform 和 lambda 進行自訂轉換
std::transform(source_vec.begin(), source_vec.end(), std::back_inserter(target_vec),
    [](int val) { return MyData{static_cast<double>(val)}; });

// 現在可以用 target_vec 初始化其他容器...
```

---

## 通用轉換規則總結

1. **相同型別，不同容器**：直接使用迭代器建構。

   ```cpp
   std::vector<int> vec = {1, 2, 3};
   std::deque<int> deq(vec.begin(), vec.end()); // 合法
   ```

2. **不同型別，不同容器**：
   - **如果型別可隱式轉換** (如 `int` -> `double`)：**直接使用迭代器建構**。這是最高效的方法。
   - **如果型別需要自訂轉換** (如 `pair` -> `struct`)：使用 `std::transform` 搭配 lambda 函式，將結果存入一個臨時容器，再用該臨時容器進行初始化。

3. **`priority_queue` / `stack` / `queue` 的特殊性**：
   - 這些是**容器配接器 (Container Adaptors)**，它們底層依賴於一個序列容器（`priority_queue` 預設是 `std::vector`）。
   - 它們的建構函式也接受迭代器，這實際上是將迭代器範圍內的元素傳遞給底層容器來進行初始化，初始化過程中會處理型別轉換。

掌握了以迭代器為中心的轉換思想，你就能在各種容器之間游刃有餘地進行資料操作。
