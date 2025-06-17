# C++ Deque 與 Queue 的比較

## 基本概念

### Queue（隊列）

Queue 是一種先進先出（FIFO: First-In-First-Out）的數據結構，只允許在一端（隊尾）添加元素，在另一端（隊首）移除元素。在 C++ 標準庫中，`std::queue` 是一個 container adapter（容器適配器），默認基於 `std::deque` 實現。

### Deque（雙端隊列）

Deque（Double-ended queue，雙端隊列）是一種可以在兩端進行插入和刪除操作的序列容器。在 C++ 標準庫中，`std::deque` 是一個獨立的容器類。

## Deque 與 Queue 的主要差異

| Feature | std::deque | std::queue |
|---------|------------|------------|
| Type | Container | Adapter |
| Implementation | Independent | Based on deque |
| Access | Random access | Front only |
| Insertion | Both ends & middle | Back only |
| Deletion | Both ends & middle | Front only |
| Iterators | Yes | No |
| Resizing | Dynamic | From base container |

## Deque 的特點

### 1. 雙端操作

Deque 允許在容器的兩端高效地進行插入和刪除操作：

```cpp
std::deque<int> dq;
dq.push_front(1);  // 在前端添加元素
dq.push_back(2);   // 在後端添加元素
dq.pop_front();    // 從前端移除元素
dq.pop_back();     // 從後端移除元素
```

### 2. 隨機訪問

Deque 支持隨機訪問，可以使用索引直接訪問任意位置的元素：

```cpp
std::deque<int> dq = {1, 2, 3, 4, 5};
int third = dq[2];  // 訪問索引為 2 的元素（值為 3）
dq[1] = 10;         // 修改索引為 1 的元素
```

### 3. 動態內存分配

Deque 使用多個內存塊來存儲元素，而不是一個連續的內存塊：
- 不需要像 vector 那樣在擴容時複製所有元素
- 在兩端添加元素時通常不需要重新分配內存
- 內存使用可能比 vector 更高，因為需要維護多個內存塊的引用

### 4. 中間插入和刪除

Deque 支持在容器中間插入和刪除元素，但效率低於在兩端操作：

```cpp
std::deque<int> dq = {1, 2, 3, 4, 5};
dq.insert(dq.begin() + 2, 10);  // 在索引為 2 的位置插入元素 10
dq.erase(dq.begin() + 1);       // 刪除索引為 1 的元素
```

### 5. 不保證迭代器和引用的穩定性

與 vector 類似，當 deque 進行插入或刪除操作時，可能會使現有的迭代器和引用失效。

### 6. 時間複雜度分析

Deque 的各種操作時間複雜度如下：

| 操作 | 時間複雜度 | 說明 |
|------|------------|------|
| 隨機訪問 | O(1) | 通過索引直接訪問元素 |
| 在兩端插入/刪除 | O(1) | push_front, push_back, pop_front, pop_back 操作 |
| 在中間插入/刪除 | O(n) | 需要移動元素以維持連續性 |
| 查找元素 | O(n) | 需要線性搜索 |

#### 為什麼 deque 在中間插入/刪除需要 O(n) 時間？

雖然 deque 支持在中間位置插入和刪除元素，但這些操作的時間複雜度為 O(n)，原因如下：

1. **元素移動**：當在 deque 的中間插入一個元素時，需要將插入點後面的所有元素向後移動一個位置來騰出空間。同樣，當刪除中間的元素時，需要將刪除點後面的所有元素向前移動一個位置來填補空缺。

2. **分段內存結構**：雖然 deque 使用分段連續內存塊而非單一連續內存（如 vector），但這只影響實現細節和常數因子，不改變漸進時間複雜度。

3. **最壞情況分析**：
   - 最壞情況下，如果插入/刪除發生在 deque 的中間位置，大約需要移動一半的元素
   - 如果 deque 包含 n 個元素，則需要移動約 n/2 個元素，這仍然是 O(n) 的操作

4. **與 vector 的比較**：
   - vector 在中間插入/刪除也是 O(n) 的操作
   - deque 的分段內存結構可能使得這些操作在實際執行時比 vector 更高效（常數因子更小），特別是當需要重新分配內存時
   - 然而，從漸進分析的角度來看，兩者都是 O(n) 的操作

5. **替代方案**：
   - 如果應用程序需要頻繁在容器中間進行插入和刪除操作，可能應該考慮使用 `std::list`（雙向鏈表）
   - `std::list` 提供 O(1) 的中間插入和刪除操作（假設已有指向插入/刪除位置的迭代器）
   - 但 `std::list` 不支持隨機訪問，查找特定位置需要 O(n) 時間

## 使用場景

### 適合使用 Queue 的情況

- 需要嚴格的 FIFO（先進先出）操作
- 只需要訪問隊首元素
- 不需要隨機訪問或迭代容器中的元素
- 典型應用：任務隊列、消息緩衝區、廣度優先搜索（BFS）

### Queue 在算法問題中的應用

在算法問題中，queue 的使用頻率低於 stack，且相關問題通常更具挑戰性。Queue 最主要的應用是實現廣度優先搜索（BFS）算法，這是一種用於圖和樹遍歷的重要算法。除了 BFS 外，與 stack 不同，很少有問題的核心焦點是 queue 本身。

BFS 的典型應用包括：
- 最短路徑問題（如迷宮最短路徑）
- 層序遍歷（如二叉樹的層序遍歷）
- 連通性問題（如找出圖中的所有連通分量）
- 拓撲排序的某些實現

### 適合使用 Deque 的情況

- 需要在兩端高效地進行插入和刪除操作
- 需要 `隨機訪問` 元素
- 需要在 `中間插入或刪除` 元素
- 需要迭代容器中的元素
- 典型應用：滑動窗口問題、雙端隊列算法、需要頻繁在兩端操作的數據處理

## 代碼示例

### Queue 基本操作

```cpp
#include <queue>
#include <iostream>

int main() {
    std::queue<int> q;
    
    // 添加元素
    q.push(1);
    q.push(2);
    q.push(3);
    
    // 訪問隊首元素
    std::cout << "Front: " << q.front() << std::endl;  // 輸出: 1
    
    // 移除隊首元素
    q.pop();
    std::cout << "New front: " << q.front() << std::endl;  // 輸出: 2
    
    // 檢查隊列大小
    std::cout << "Size: " << q.size() << std::endl;  // 輸出: 2
    
    // 檢查隊列是否為空
    std::cout << "Empty: " << (q.empty() ? "Yes" : "No") << std::endl;  // 輸出: No
    
    return 0;
}
```

### Deque 基本操作

```cpp
#include <deque>
#include <iostream>

int main() {
    std::deque<int> dq;
    
    // 在兩端添加元素
    dq.push_front(1);
    dq.push_back(2);
    dq.push_front(0);
    dq.push_back(3);
    
    // 現在 dq 包含: {0, 1, 2, 3}
    
    // 隨機訪問
    std::cout << "Element at index 2: " << dq[2] << std::endl;  // 輸出: 2
    
    // 修改元素
    dq[1] = 10;
    // 現在 dq 包含: {0, 10, 2, 3}
    
    // 在中間插入元素
    dq.insert(dq.begin() + 2, 15);
    // 現在 dq 包含: {0, 10, 15, 2, 3}
    
    // 從兩端移除元素
    dq.pop_front();
    dq.pop_back();
    // 現在 dq 包含: {10, 15, 2}
    
    // 迭代遍歷
    std::cout << "Deque contents: ";
    for (int x : dq) {
        std::cout << x << " ";
    }
    std::cout << std::endl;  // 輸出: Deque contents: 10 15 2
    
    return 0;
}
```

## 總結

- **Queue** 是一個 container adapter，提供嚴格的 FIFO 操作，限制了元素的訪問和修改方式，適用於需要簡單隊列操作的場景。
- **Deque** 是一個功能更強大的容器，支持雙端操作和隨機訪問，提供了更大的靈活性，但可能有更高的內存開銷。

選擇使用哪一個取決於具體的需求：如果只需要標準的隊列操作，使用 `std::queue` 可能更簡單明了；如果需要更靈活的操作，如雙端插入/刪除或隨機訪問，則應選擇 `std::deque`。