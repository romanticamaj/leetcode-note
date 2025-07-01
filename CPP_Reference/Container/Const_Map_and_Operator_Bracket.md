# C++ 容器陷阱：`const` map/unordered_map 與 `operator[]`

在 C++ 中，一個常見且容易讓人困惑的編譯錯誤，是嘗試使用 `operator[]`（中括號運算子）來存取一個被 `const` 修飾的 `std::map` 或 `std::unordered_map`。

## 問題場景

當你將一個 `map` 或 `unordered_map` 以 `const` 引用傳遞給一個函式，並試圖用 `[]` 來存取其元素時，就會觸發這個問題。

```cpp
// 錯誤範例
void processGraph(const std::unordered_map<std::string, std::unordered_map<std::string, double>>& graph) {
    std::string current = "A";
    // ...
    // 下面這行會導致編譯錯誤
    for (auto const& [neighbor, weight] : graph[current]) {
        // ...
    }
}
```

**常見錯誤訊息**: `no viable overloaded operator[] for type 'const ...'`

## 核心原因：`operator[]` 的非 `const` 設計

這個錯誤的根本原因在於 `std::map` 和 `std::unordered_map` 的 `operator[]` 被設計為一個**非 `const`** 的成員函式。

`operator[]` 的行為模式是「**存取或插入 (access or insert)**」：

1. 如果鍵 (key) **存在**，它會回傳對應值 (value) 的引用。
2. 如果鍵 (key) **不存在**，它會**插入**一個新的鍵值對，其中值是預設建構的（例如，`int` 為 `0`），然後回傳這個新值的引用。

正是這個「如果不存在就插入」的副作用，意味著 `operator[]` 有**可能修改**容器。這個潛在的修改行為與 `const` 的承諾（保證不修改物件）是完全衝突的。因此，C++ 標準禁止對 `const` 的 map 使用 `operator[]`。

## ✅ 正確做法：使用 `const` 安全的存取方法

當你需要從一個 `const` 的 map 中讀取資料時，必須使用保證不會修改容器的方法。

### 方法一：使用 `.at()` (個人推薦)

`.at()` 成員函數會回傳鍵對應的值的 `const` 引用。它的優點是**意圖清晰**：你就是想存取這個鍵，並預期它一定存在。如果鍵不存在，它會拋出一個 `std::out_of_range` 例外，這在開發和除錯階段能立即暴露問題，防止潛在的邏輯錯誤。

```cpp
// 正確範例
void processGraph(const std::unordered_map<std::string, std::unordered_map<std::string, double>>& graph) {
    std::string current = "A";
    try {
        const auto& neighbors = graph.at(current);
        for (auto const& [neighbor, weight] : neighbors) {
            // ...
        }
    } catch (const std::out_of_range& e) {
        // 處理 'current' 節點不存在於圖中的情況
        // 例如，記錄錯誤日誌或直接返回
    }
}
```

### 方法二：使用 `.find()`

`.find()` 會回傳一個指向鍵值對的迭代器。如果鍵不存在，它會回傳指向容器 `end()` 的迭代器。這個方法**不會**拋出例外，因此在「不確定鍵是否存在，且不存在是正常情況」的場景下非常適用。

```cpp
// 正確範例
void processGraph(const std::unordered_map<std::string, std::unordered_map<std::string, double>>& graph) {
    std::string current = "A";
    auto it = graph.find(current);

    if (it != graph.end()) {
        // it->first 是鍵 (current)
        // it->second 是值 (鄰居 map)
        for (auto const& [neighbor, weight] : it->second) {
            // ...
        }
    } else {
        // 處理 'current' 節點不存在於圖中的情況
    }
}
```

## 總結對照表

| 方法 | `const` 安全性 | 鍵不存在時的行為 | 適用場景 |
| :--- | :--- | :--- | :--- |
| `operator[]` | ❌ 否 | 插入預設值 | 非 `const` map，且希望鍵不存在時自動插入 |
| `.at()` | ✅ 是 | 拋出 `std::out_of_range` | `const` map，且你**預期鍵應該存在**時（Fail-fast） |
| `.find()` | ✅ 是 | 回傳 `end()` 迭代器 | `const` map，且鍵**可能不存在**是正常邏輯 |

**心法**：當處理 `const` map 或 `const` unordered_map 時，**永遠用 `.find()` 或 `.at()` 取代 `[]` 來存取元素**。
