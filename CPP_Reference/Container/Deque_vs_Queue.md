# C++ `deque` vs `queue` 完整比較與使用指南

## `deque` 是什麼？

`std::deque`（double-ended queue）是 C++ STL 中一種支援**雙端插入與刪除**的容器。與 `vector` 類似，它支援隨機存取，但在兩端插入/刪除的效率更高。

### 特性總覽

| 特性          | `deque`                                                    |
| ------------- | ---------------------------------------------------------- |
| 雙端操作      | 支援 `push_front` / `pop_front` / `push_back` / `pop_back` |
| 隨機存取      | 支援 `operator[]`、`at()`                                  |
| 動態擴容      | 是                                                         |
| 內部實作      | 分段連續記憶體（非單一連續）                               |
| 插入刪除效率  | 前後皆為 O(1)（均攤）                                      |
| 中間插入刪除  | O(n)（需要移動後續元素）                                   |
| 前端/尾端操作 | 可用 `front()` / `back()` 讀取兩端元素                     |
| 空間配置      | 多段記憶體區塊                                             |

---

### 記憶體配置與內部結構

- `deque` 並不像 `vector` 使用單一連續記憶體，而是使用**分段記憶體區塊（chunked memory blocks）**。
- STL `deque` 內部維護一個指向多個固定大小區塊的指標陣列（map of blocks），每個區塊大小通常為 512 bytes 或數個元素。
- 這種設計讓 `deque` 可以在前端與尾端都進行 O(1) 的插入與刪除，因為只需在區塊邊界擴展或回收。

### iterator 特性

- `deque` 的 iterator 是 **RandomAccessIterator**，與 `vector` 相同，可支援 `+`, `-`, `[]`, `distance()` 等操作。
- 但由於記憶體非連續，`&deque[i+1] == &deque[i] + 1` 不一定成立。
  不過其 iterator 仍完全支援 `++`, `--`, `+n`, `-n`, `[]` 等 RandomAccess 操作，行為與 `vector` 相同，只是底層位置不連續。
- 若你需要與底層記憶體位置有關的操作（如 `memcpy`），`deque` 不適合。

### 注意事項

- `deque` 的 iterator 在以下情況會失效（invalidated）：
  - 插入或刪除導致區塊重組（尤其是 `push_front` / `pop_front`）
  - `clear()` 或 `resize()` 操作
- 相比之下，`vector` 的 iterator 只有在 reallocation 時才會失效（通常是 `push_back` 導致容量擴張）

---

## `queue` 是什麼？

`std::queue` 是一種**封裝容器（container adaptor）**，預設以 `deque` 為底層實作，提供**單端進、單端出**的 FIFO 結構。

### 特性總覽

| 特性           | `queue`                          |
| -------------- | -------------------------------- |
| 操作限制       | 只能 `push` 到尾端、`pop` 從前端 |
| 不支援隨機存取 | 無 `[]`，不提供 iterator 介面    |
| 底層容器       | 預設為 `deque`，可改為 `list`    |
| 適用場景       | 僅需 FIFO 行為的情境             |

---

## `deque` vs `queue` 比較表

| 功能/特性     | `deque`                               | `queue`                  |
| ------------- | ------------------------------------- | ------------------------ |
| 雙端操作      | ✅ `push_front` / `pop_front`         | ❌ 僅支援尾 push、頭 pop |
| 隨機存取      | ✅ `[]`, `at()`                       | ❌                       |
| iterator 支援 | ✅                                    | ❌                       |
| 彈性          | ✅ 高（可當作雙端佇列、stack、queue） | ❌ 僅限 FIFO             |
| 使用場景      | BFS、滑動窗口、雙端處理等             | 純 FIFO 隊列             |

---

---

## `deque` vs `queue` API 與時間複雜度比較

| 操作類型     | `deque` API          | 時間複雜度 | `queue` API | 時間複雜度 | 備註                                |
| ------------ | -------------------- | ---------- | ----------- | ---------- | ----------------------------------- |
| 插入尾端     | `push_back(val)`     | O(1)       | `push(val)` | O(1)       | `queue` 實際呼叫 `deque::push_back` |
| 插入前端     | `push_front(val)`    | O(1)       | ❌          | -          | `queue` 不支援                      |
| 移除尾端     | `pop_back()`         | O(1)       | ❌          | -          | `queue` 不支援                      |
| 移除前端     | `pop_front()`        | O(1)       | `pop()`     | O(1)       | `queue` 實際呼叫 `deque::pop_front` |
| 讀取尾端     | `back()`             | O(1)       | `back()`    | O(1)       | 兩者皆支援                          |
| 讀取前端     | `front()`            | O(1)       | `front()`   | O(1)       | 兩者皆支援                          |
| 隨機存取     | `operator[]`, `at()` | O(1)       | ❌          | -          | `queue` 不支援                      |
| 判斷是否為空 | `empty()`            | O(1)       | `empty()`   | O(1)       | 兩者皆支援                          |
| 取得大小     | `size()`             | O(1)       | `size()`    | O(1)       | 兩者皆支援                          |
| 清空         | `clear()`            | O(n)       | ❌          | -          | `queue` 無提供 clear()              |

這張表格幫助你快速比較 `deque` 與 `queue` 在 API 支援與時間複雜度上的差異，並理解 `queue` 是如何封裝 `deque` 的子集功能。

## `deque` 的常見用法

### 1. 雙端佇列

```cpp
deque<int> dq;
dq.push_back(1);
dq.push_front(2);
dq.pop_back();
dq.pop_front();
```

### 2. 單調佇列（Monotonic Queue）

```cpp
deque<int> mono;
while (!mono.empty() && mono.back() < current)
    mono.pop_back();
mono.push_back(current);
```

### 3. 滑動窗口最大值

```cpp
vector<int> maxSlidingWindow(vector<int>& nums, int k) {
    deque<int> dq;
    vector<int> res;
    for (int i = 0; i < nums.size(); ++i) {
        if (!dq.empty() && dq.front() <= i - k)
            dq.pop_front();
        while (!dq.empty() && nums[dq.back()] < nums[i])
            dq.pop_back();
        dq.push_back(i);
        if (i >= k - 1)
            res.push_back(nums[dq.front()]);
    }
    return res;
}
```

---

## 什麼時候選擇 `deque`？

- 需要雙端操作（如 BFS、滑動窗口）
- 需要隨機存取（比 `list` 更快）
- 不需要頻繁中間插入（否則 `list` 更適合）

---

## 小結

- `deque` 是功能強大的雙端容器，適合大多數需要彈性佇列操作的場景
- `queue` 是簡化版的 FIFO 封裝，適合只需要基本佇列行為的情境
- 若你需要更多控制與效率，`deque` 幾乎總是更好的選擇
