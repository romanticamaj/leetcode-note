# C++ STL: std::priority_queue 使用詳解

`std::priority_queue` 是 C++ STL 中一個非常有用的容器配接器，它提供常數時間複雜度的最大（或最小）元素查找。理解其內部機制對於高效使用至關重要。

## 基本用法：Max-Heap vs. Min-Heap

```cpp
// 預設是 max-heap (大根堆)
std::priority_queue<int> maxHeap;

// 使用 std::greater 來自訂比較函式，實現 min-heap (小根堆)
std::priority_queue<int, std::vector<int>, std::greater<int>> minHeap;
```

## 核心機制：`std::less` vs. `std::greater`

要理解為什麼 `std::greater` 會產生 min-heap，我們需要先了解 `std::less` 和 `std::greater` 的定義以及 `priority_queue` 的堆屬性。

在 C++ STL 中，`std::less` 和 `std::greater` 都是在 `<functional>` 裡定義的「比較函式物件」（functor），它們的行為大致如下：

```cpp
// 定義在 <functional> 裡的模板（簡化版）
template <class T>
struct less {
    bool operator()(const T& a, const T& b) const {
        return a < b;    // 如果 a < b 則回傳 true
    }
};

template <class T>
struct greater {
    bool operator()(const T& a, const T& b) const {
        return a > b;    // 如果 a > b 則回傳 true
    }
};
```

### 為什麼預設是「大根堆」（max-heap）

`std::priority_queue` 的操作與底層的堆演算法緊密相關：

- **初始化**：當使用迭代器範圍初始化時，`priority_queue` 會呼叫 `std::make_heap` 來將整個容器轉換為一個合法的堆。
- **插入 (`push`)**：每次 `push` 一個新元素時，它會被放到容器末端，然後呼叫 `std::push_heap` 將該元素「上浮」(sift-up) 到正確位置。
- **刪除 (`pop`)**：每次 `pop` 時，會先呼叫 `std::pop_heap` 將堆頂元素（最大或最小值）與容器末端元素交換，然後將末端元素移除。`pop_heap` 會將新的堆頂元素「下沉」(sift-down) 以維持堆屬性。

這些操作都圍繞著一個核心的堆屬性條件：

> 對於任意節點 `i`（根節點除外），其與父節點 `parent(i)` 的關係必須滿足：
> `!Compare(parent(i), i)`
>
> 換句話說，`Compare(parent, child)` 這個表達式必須回傳 `false`。

我們來分析兩種情況：

1. **`Compare = std::less<T>` (預設情況)**
   - `less(parent, child)` 等價於 `parent < child`。
   - 堆屬性要求 `parent < child` 為 `false`。
   - 這就意味著必須滿足 `parent >= child`。
   - 因此，父節點永遠大於或等於子節點，根節點自然是整個堆中的「最大值」，這就是 **大根堆 (max-heap)**。

2. **`Compare = std::greater<T>`**
   - `greater(parent, child)` 等價於 `parent > child`。
   - 堆屬性要求 `parent > child` 為 `false`。
   - 這就意味著必須滿足 `parent <= child`。
   - 因此，父節點永遠小於或等於子節點，根節點自然是整個堆中的「最小值」，這就是 **小根堆 (min-heap)**。

---

## 完整範例

```cpp
#include <queue>
#include <vector>
#include <iostream>
#include <functional>

int main() {
    // 1) 預設：Compare = std::less<int> → max-heap
    // std::priority_queue<int> 等同於
    // std::priority_queue<int, std::vector<int>, std::less<int>>
    std::priority_queue<int> maxHeap;
    maxHeap.push(3);
    maxHeap.push(1);
    maxHeap.push(4);
    std::cout << "maxHeap.top() = " << maxHeap.top() << std::endl;  // 輸出 4

    // 2) 使用 std::greater → min-heap
    std::priority_queue<
        int,
        std::vector<int>,
        std::greater<int>
    > minHeap;
    minHeap.push(3);
    minHeap.push(1);
    minHeap.push(4);
    std::cout << "minHeap.top() = " << minHeap.top() << std::endl;  // 輸出 1

    return 0;
}
```

---

### 小結

- **`std::less<T>`**：內部執行 `a < b`，在 `priority_queue` 中產生 **大根堆**，`top()` 是最大值。
- **`std::greater<T>`**：內部執行 `a > b`，在 `priority_queue` 中產生 **小根堆**，`top()` 是最小值。

這就是為什麼把第三個模板參數從 `std::less` 換成 `std::greater`，就能將 max-heap 變成 min-heap 的根本原因。
