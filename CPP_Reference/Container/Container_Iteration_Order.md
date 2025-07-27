# C++ STL 容器的遍歷順序與有序性詳解

在 C++ 中，能否預測容器（Container）的遍歷順序，是撰寫正確且高效程式碼的關鍵。不同的容器基於其底層資料結構，提供了不同的順序性保證。本文件將深入探討各個 STL 容器的元素儲存順序與 range-based for 迴圈的遍歷行為。

---

## 總覽：容器遍歷順序快速參考

下表總結了主要 STL 容器的有序性與遍歷行為：

| Container             | 元素有序性 (Element Order)            | Range-based for 順序                      |
| --------------------- | ------------------------------------- | ----------------------------------------- |
| `std::vector`         | 按插入順序儲存，索引穩定              | 按索引 0 到 N-1 順序遍歷                  |
| `std::deque`          | 按插入順序儲存 (雙端)，中間元素不移動 | 按 0 到 N-1 順序遍歷                      |
| `std::list`           | 按插入順序，雙向鏈表                  | 從 head 到 tail 順序                      |
| `std::forward_list`   | 按插入順序，單向鏈表                  | 從 head 往後                              |
| `std::array`          | 固定大小，按 index 順序               | 按 0 到 N-1                               |
| `std::set`            | 自動排序 (key ascending)              | 按 key 小到大                             |
| `std::multiset`       | 自動排序 (key ascending)              | 按 key 小到大                             |
| `std::unordered_set`  | 無特定順序 (hash bucket)              | unspecified (通常看似插入順序,但絕不保證) |
| `std::map`            | 自動排序 (key ascending)              | 按 key 小到大                             |
| `std::multimap`       | 自動排序 (key ascending)              | 按 key 小到大                             |
| `std::unordered_map`  | 無特定順序 (hash bucket)              | unspecified                               |
| `std::stack`          | 沒有 iterator，不能用 range-based for | 不支援                                    |
| `std::queue`          | 沒有 iterator，不能用 range-based for | 不支援                                    |
| `std::priority_queue` | 沒有 iterator，不能用 range-based for | 不支援                                    |

---

## 1. 序列式容器 (Sequence Containers)

這類容器的共同點是**元素排列順序取決於插入位置**，而非元素的值。

- **`std::vector`**:

  - **底層結構**：動態陣列，保證記憶體連續。
  - **有序性**：嚴格的插入順序。
  - **遍歷**：永遠從索引 `0` 到 `N-1`。
  - **遍歷複雜度 (Traversal Complexity)**：**O(N)**，其中 N 是容器中的元素數量。

- **`std::deque`**:

  - **底層結構**：分塊的記憶體陣列，支援高效的頭尾插入/刪除。
  - **有序性**：嚴格的插入順序。
  - **遍歷**：從頭（front）到尾（back）。
  - **遍歷複雜度 (Traversal Complexity)**：**O(N)**。

- **`std::list`**:

  - **底層結構**：雙向鏈結串列。
  - **有序性**：嚴格的插入順序。
  - **遍歷**：從 `head` 節點到 `tail` 節點。
  - **遍歷複雜度 (Traversal Complexity)**：**O(N)**。

- **`std::array`**:
  - **底層結構**：靜態陣列，大小在編譯期固定。
  - **有序性**：固定的索引順序。
  - **遍歷**：永遠從索引 `0` 到 `N-1`。
  - **遍歷複雜度 (Traversal Complexity)**：**O(N)**。

```cpp
// 序列式容器的遍歷順序符合直覺
std::vector<int> v = {3, 1, 2};
// 輸出: 3 1 2
for (int x : v) { std::cout << x << " "; }
```

---

## 2. 有序關聯式容器 (Ordered Associative Containers)

這類容器的元素會**根據鍵值自動排序**。

- **`std::set`, `std::multiset`, `std::map`, `std::multimap`**:
  - **底層結構**：通常是**紅黑樹 (Red-Black Tree)**，一種自平衡的二元搜尋樹。
  - **有序性**：元素（或鍵）永遠保持排序狀態（預設為升序）。
  - **遍歷**：遍歷順序是根據鍵值從小到大。對於 `map`，是遍歷 `std::pair`，並根據 `pair.first` (key) 排序。
  - **遍歷複雜度 (Traversal Complexity)**：**O(N)**。

```cpp
std::set<int> s = {7, 3, 5};
// 輸出: 3 5 7 (自動排序)
for (int x : s) { std::cout << x << " "; }

std::map<int, std::string> m = {{5, "A"}, {2, "B"}};
// 輸出: 2:B 5:A (按 key 排序)
for (const auto& [key, value] : m) { std::cout << key << ":" << value << " "; }
```

---

## 3. 無序關聯式容器 (Unordered Associative Containers)

這類容器提供快速的平均查找時間，但**不保證任何遍歷順序**。

- **`std::unordered_set`, `std::unordered_multiset`, `std::unordered_map`, `std::unordered_multimap`**:
  - **底層結構**：**雜湊表 (Hash Table)**。
  - **有序性**：**完全無序**。元素的儲存位置由其雜湊值決定。
  - **遍歷**：遍歷順序是不確定的，並且在不同編譯器、不同執行，甚至每次插入/刪除後都可能改變。**絕對不能依賴其遍歷順序**。
  - **遍歷複雜度 (Traversal Complexity)**：平均情況下為 **O(N)**，最壞情況（雜湊碰撞嚴重）可能退化到 **O(N^2)**，但在良好雜湊函數下極為罕見。實務上可視為 **O(N)**。

```cpp
std::unordered_set<int> us = {100, 2, 50};
// 輸出順序不固定，例如可能是 2 50 100 或 100 2 50
for (int x : us) { std::cout << x << " "; }
```

---

## 4. 容器配接器 (Container Adaptors)

這類容器是為了提供特定的介面（如 LIFO, FIFO）而設計的，它們**不提供直接遍歷的能力**。

- **`std::stack`, `std::queue`, `std::priority_queue`**:
  - **設計理念**：限制介面以符合其抽象概念（堆疊、佇列）。它們封裝了底層容器，並只暴露如 `push`, `pop`, `top` 等操作。
  - **遍歷**：不支援 range-based for 迴圈，因為它們沒有提供 `begin()` 和 `end()` 迭代器。若要遍歷，必須手動將元素逐一 `pop` 出，這會清空容器。

---

## 結論：Range-based for 的遍歷順序心法

在 `for (auto& element : container)` 迴圈中，`element` 的出現順序完全取決於容器的類型：

1. **遍歷順序可預測且穩定**：

   - **序列式容器 (`vector`, `deque`, `list`, `array`)**：遍歷順序**嚴格等於**元素的插入/索引順序。這是最直觀、最可靠的行為。
   - **有序關聯式容器 (`set`, `map`, etc.)**：遍歷順序**嚴格等於**元素的鍵值排序（預設為升序）。

2. **遍歷順序完全不可預測**：

   - **無序關聯式容器 (`unordered_set`, `unordered_map`, etc.)**：**絕對不要**依賴其遍歷順序。它由內部雜湊函數和實現細節決定，隨時可能改變。

3. **不支援 Range-based for**：
   - **容器配接器 (`stack`, `queue`, `priority_queue`)**：它們被設計為限制性介面，未提供遍歷所需的迭代器，因此不能直接與 range-based for 迴圈一起使用。
