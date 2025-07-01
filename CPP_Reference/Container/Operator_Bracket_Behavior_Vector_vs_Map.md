# C++ 容器陷阱：`vector` vs. `map` 的 `operator[]` 行為差異

在 C++ 中，`std::vector` 和 `std::map`（及其 `unordered` 版本）都支援 `operator[]`（中括號運算子），但其底層行為和使用約束截然不同。混淆這兩者的行為是初學者常見的錯誤來源。

## `std::vector` 的 `operator[]`：純粹的存取

- **行為**: 提供對**已存在**元素的直接、高效的存取。它**永遠不會**自動新增元素或改變 `vector` 的大小。
- **核心約束**: 使用 `[]` 存取一個**超出範圍 (out-of-bounds)** 的索引是**未定義行為 (Undefined Behavior)**。這意味著程式可能會立即崩潰，也可能在不相關的地方讀寫記憶體，導致難以追蹤的 bug。
- **使用前提**: 在使用 `vec[i] = value` 賦值前，你必須**自己確保**索引 `i` 是有效的（即 `0 <= i < vec.size()`）。這通常意味著需要先使用 `resize()` 或 `push_back()` 來分配足夠的空間。

```cpp
// ❌ 錯誤：對一個空的 vector 使用索引賦值
std::vector<int> vec;
vec[0] = 100; // 未定義行為！vec 的大小是 0，索引 0 無效。

// ✅ 正確做法 1：先指定大小
std::vector<int> vec_sized(10);
vec_sized[0] = 100; // 正確，因為索引 0 是合法的。

// ✅ 正確做法 2：使用 push_back
std::vector<int> vec_pushed;
vec_pushed.push_back(100); // 正確，新增一個元素並賦值。
```

## `std::map` / `std::unordered_map` 的 `operator[]`：存取或插入

- **行為**: 提供對鍵 (key) 所對應的值 (value) 的存取。
- **特殊功能 (副作用)**: 如果鍵**不存在**，`operator[]` 會**自動插入**一個新的鍵值對。這個新鍵值對的值部分會被**預設建構**（例如，`int` 為 `0`，`string` 為 `""`）。
- **`const` 限制**: 正因為有這個自動插入的副作用，`operator[]` 不能被用於 `const` 的 map。

```cpp
std::unordered_map<std::string, int> word_count;

// ✅ 正確：如果 "hello" 不存在，會自動新增 "hello" -> 0，然後再 ++ 變成 1。
word_count["hello"]++;

// ✅ 正確：可以直接賦值，即使 "world" 不存在。
word_count["world"] = 5;
```

## 總結心法

| 容器                              | `operator[]` 行為                 | 使用前提                            |
| :-------------------------------- | :-------------------------------- | :---------------------------------- |
| `std::vector`                     | **僅存取 (Access-only)**          | 索引必須在 `[0, size() - 1]` 範圍內 |
| `std::map` / `std::unordered_map` | **存取或插入 (Access-or-Insert)** | 無，若鍵不存在則自動插入            |

> **心法**: 對 `vector` 使用 `[]` 前，先問自己：「這個位置 (`index`) 真的存在嗎？」；對 `map` 使用 `[]` 前，則要意識到：「如果這個鍵 (`key`) 不存在，它會被自動建立。」
