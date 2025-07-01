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

---

## 常見陷阱 (Pitfall)

在自訂 `priority_queue` 的比較器時，一個常見的錯誤是忘記提供第二個模板參數，也就是底層容器的型別。

**錯誤寫法：**

```cpp
// 這段程式碼無法編譯
std::priority_queue<int, std::greater<int>> minHeap;
```

**原因**：
`std::priority_queue` 的模板定義如下：

```cpp
template<
    class T,
    class Container = std::vector<T>,
    class Compare = std::less<typename Container::value_type>
> class priority_queue;
```

第二個參數 `Container` 和第三個參數 `Compare` 都有預設值。如果你想提供自訂的 `Compare`（第三個參數），就必須先明確指定 `Container`（第二個參數），即使你只是想使用預設的 `std::vector<T>`。

**正確寫法：**

```cpp
// 必須明確提供容器型別
std::priority_queue<int, std::vector<int>, std::greater<int>> minHeap;
```

---

## 小技巧：用負號實現 Min-Heap

在處理數值型別時，有一個非常巧妙的技巧可以快速實現 Min-Heap，而無需自訂比較器：**將存入的元素變為負數**。

`std::priority_queue` 預設是 Max-Heap，它會將最大的元素放在頂部。如果我們將所有數字都變成負數，那麼原本最小的數字（例如 `1`）就會變成最大的負數（`-1`），從而被 Max-Heap 放在頂部。

**實現方式：**

- **插入 (`push`)**：將 `value` 以 `-value` 的形式存入。
- **讀取 (`top`)**：取出堆頂元素後，再將其變回正數 (`-heap.top()`)。

**範例：**

```cpp
#include <queue>
#include <iostream>

int main() {
    // 使用預設的 Max-Heap 來模擬 Min-Heap
    std::priority_queue<int> minHeap_sim;

    minHeap_sim.push(-3); // 存入 -3
    minHeap_sim.push(-1); // 存入 -1
    minHeap_sim.push(-4); // 存入 -4

    // 此時堆頂是 -1 (最大的負數)
    std::cout << "Simulated minHeap.top() = " << -minHeap_sim.top() << std::endl; // 輸出 1

    return 0;
}
```

這個技巧非常簡潔，在競賽中可以節省大量時間，但請注意它只適用於數值型別。
