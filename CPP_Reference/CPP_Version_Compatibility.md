# C++ 版本相容性速查：以 C++14 為基準

面試環境若指定 C++14，先選能在 C++14 編譯的寫法。**API 與語法都要檢查最低標準版本**；C++14 可用不代表它是在 C++14 才加入。

本表聚焦刷題常見功能，不是完整標準清單。表中的最低版本指列出的基本用法；同名 API 的其他 overload 可能需要較新版本。

## C++14 已可用的常用功能

| 功能 | 最低標準 | 備註 |
|:---|:---:|:---|
| `vector`、`deque`、`queue`、`priority_queue`、`map`、`set` 的基本操作 | C++98 | `push`／`pop`、`front`／`top` 等依容器而定 |
| `sort`、`lower_bound`、`upper_bound`、`accumulate` 的 iterator 基本版 | C++98 | 不是 ranges 或 execution policy overload |
| `unordered_map`／`unordered_set`、`array` | C++11 | `find`／`count` 可用；`contains` 不可用 |
| `auto`、range-based for、具名型別參數的 lambda | C++11 | 例如 `[](int a, int b) { return a < b; }` |
| `emplace`／`emplace_back`、`to_string` | C++11 | 注意選對容器支援的 member |
| Generic lambda、`greater<>`／`less<>` | C++14 | 例如 `[](const auto& a, const auto& b) { return a < b; }` |
| `make_unique` | C++14 | `<memory>` |

## 較新功能與 C++14 替代寫法

| 功能／語法 | 最低標準 | C++14 寫法 |
|:---|:---:|:---|
| Structured bindings：`auto [a, b] = p` | C++17 | `p.first`／`p.second`；迭代 map 時用 `entry.first`／`entry.second` |
| `if (auto it = m.find(key); it != m.end())` | C++17 | 先在前一行宣告 `it`，再寫 `if` |
| `map`／`unordered_map` 的 `try_emplace` | C++17 | 視需求用 `find` 後再 `emplace`；避免缺 key 時不必要的值建構須自行安排 |
| `map`／`unordered_map` 的 `insert_or_assign` | C++17 | 值可預設建構時可用 `m[key] = value`；否則 `find` 後更新或插入 |
| `clamp(x, lo, hi)` | C++17 | 同型別且 `lo <= hi` 時，取值用 `min(max(x, lo), hi)` |
| `gcd`／`lcm` | C++17 | 自寫 Euclidean algorithm；LCM 先除再乘，仍須確認不溢位 |
| `reduce` | C++17 | 循序累加通常用 `accumulate`，兩者運算順序語義不同，見[既有比較](Algorithm/Accumulate_vs_Reduce.md) |
| `map`／`set`／`unordered_map`／`unordered_set` 的 `contains` | C++20 | `c.find(key) != c.end()`；只查存在也可 `c.count(key) > 0` |
| `string::starts_with`／`ends_with` | C++20 | 檢查長度後，用 `compare` 比較前綴／後綴 |
| `std::erase`／`std::erase_if`（以 vector 為例） | C++20 | `v.erase(remove(...), v.end())`／`v.erase(remove_if(...), v.end())` |
| `string::contains` | C++23 | `s.find(pattern) != string::npos` |

**注意：容器的 `contains` 是 C++20，字串的 `contains` 是 C++23。** `vector` 也沒有 `contains` member。

## 存在性查詢：C++14 的標準寫法

```cpp
#include <unordered_map>

std::unordered_map<int, int> counting;
int key = 5;

// 只查 key 是否存在，不會插入。
bool exists = counting.find(key) != counting.end();
bool missing = counting.find(key) == counting.end();

// 同時需要 value：保留 iterator，避免再次查詢。
auto it = counting.find(key);
if (it != counting.end()) {
    int frequency = it->second;
    // 使用 frequency
}
```

查詢存在性不要改成 `counting[key]`：缺 key 時會插入預設值。對 frequency map 而言，**key 存在**與 **frequency > 0** 是不同問題；只有維持「零頻率就 erase」時，存在性才能代表仍有元素。

239 的原始程式只需將清理條件改成以下寫法，即可避開 C++20 的 `contains`：

```cpp
while (!pq.empty() && counting.find(pq.top()) == counting.end()) {
    pq.pop();
}
```

253 的 `for (auto [time, count] : counting)` 則需要 C++17；C++14 可寫：

```cpp
for (const auto& entry : counting) {
    meetingRoom += entry.second;
    minRoom = std::max(minRoom, meetingRoom);
}
```

## 使用與維護方式

- 以 **C++14 可用的基本寫法**作為查閱起點；較新 API／語法在程式碼旁標註最低版本。
- 範例內混用較新語法時，要一起標記；只換掉 API 不一定就能以 C++14 編譯。
- 編譯時指定 `-std=c++14 -pedantic-errors`，避免把編譯器接受的 extension 誤認為標準功能；標準庫也需支援所用版本。
- 容器操作見[常用容器 API](Container/Common_Container_APIs.md)，演算法見[常用演算法與工具](Algorithm/Common_Algorithms_and_Utilities.md)。

## 版本來源

- [Microsoft C++ 標準相容性表](https://learn.microsoft.com/en-us/cpp/overview/visual-cpp-language-conformance?view=msvc-170)：依 C++14／17／20／23 分類語言與標準庫功能；表中 Visual Studio 發行版本不等於 C++ 標準版本。
- [Microsoft unordered_map 文件](https://learn.microsoft.com/en-us/cpp/standard-library/unordered-map-class?view=msvc-170)：`contains`、`find`、`count` 的介面與版本標記。
