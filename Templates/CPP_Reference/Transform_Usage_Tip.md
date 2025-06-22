# C++ 使用 std::transform

---

## `std::transform`：輸出容器空間問題

### 核心心法

在使用 `std::transform` 時，必須確保**輸出容器（output container）有足夠的空間**來存放結果。`std::transform` 本身**不會**自動為輸出容器分配記憶體。

### ❌ 錯誤用法（Undefined Behavior）

如果你傳遞一個空的 `vector` 作為輸出目標，會導致未定義行為（通常是段錯誤），因為 `std::transform` 會試圖寫入無效的記憶體位置。

```cpp
#include <vector>
#include <algorithm>

std::vector<int> input = {1, 2, 3, 4, 5};
std::vector<int> output; // 錯誤：output 是空的！

// 這會導致未定義行為
std::transform(input.begin(), input.end(), output.begin(), [](int x) {
    return x * 2;
});
```

### ✅ 正確用法

#### 方法一：預先調整輸出容器大小

在呼叫 `std::transform` 之前，先 `resize` 輸出容器。

```cpp
std::vector<int> input = {1, 2, 3, 4, 5};
std::vector<int> output;
output.resize(input.size()); // 正確：預先分配空間

std::transform(input.begin(), input.end(), output.begin(), [](int x) {
    return x * 2;
});
```

#### 方法二：使用 `std::back_inserter`

這是更現代、更推薦的做法。`std::back_inserter` 會在內部呼叫容器的 `push_back` 方法，動態地將元素加入容器中，無需預先分配空間。

```cpp
#include <vector>
#include <algorithm>
#include <iterator> // 需要包含 <iterator>

std::vector<int> input = {1, 2, 3, 4, 5};
std::vector<int> output; // output 可以是空的

// 正確：使用 back_inserter 自動擴展容器
std::transform(input.begin(), input.end(), std::back_inserter(output), [](int x) {
    return x * 2;
});
```

### 總結

- **陷阱**：`std::transform` 不會幫你 `resize` 輸出容器。
- **解法**：
  1.  手動 `resize`。
  2.  使用 `std::back_inserter`（推薦）。
