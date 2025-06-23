# 如何為 unordered 容器的複合鍵提供自訂雜湊 (Custom Hasher)

---

## 陷阱：`unordered_set` / `unordered_map` 與複合鍵 (Compound Keys)

### 問題描述

在 C++ 中，當你試圖使用 `std::pair`、`std::vector` 或其他自訂結構作為 `std::unordered_set` 或 `std::unordered_map` 的鍵時，程式碼將無法編譯。

```cpp
// 這段程式碼無法編譯！
// error: use of deleted function 'std::hash<std::pair<_T1, _T2>>::hash()'
std::unordered_set<std::pair<int, int>> mySet;
```

**根本原因**：
`std::unordered_set` 和 `std::unordered_map` 是基於雜湊表 (Hash Table) 的容器。要將一個元素存入其中，它們必須能夠計算該元素的雜湊值 (hash value)。

C++ 標準庫為所有基本類型（如 `int`, `double`, `string`）以及 `std::string` 等提供了 `std::hash` 的特化版本，但**沒有為 `std::pair`、`std::vector` 或 `std::tuple` 等複合類型提供預設的雜湊函數**。

編譯器不知道如何將一個 `std::pair<int, int>` 轉換成一個 `size_t` 類型的雜湊值，因此編譯失敗。

---

### 解決方案：提供自訂雜湊函數 (Custom Hasher)

要解決這個問題，我們必須手動為該複合類型提供一個雜湊函數。最標準、最靈活的方法是定義一個自訂的雜湊結構 (struct)。

#### 範例：為 `std::pair<int, int>` 實現雜湊

這是在圖論或幾何問題中非常常見的模式。

```cpp
#include <iostream>
#include <unordered_set>
#include <utility> // For std::pair

// 1. 定義一個自訂的雜湊結構
struct PairHasher {
    // 2. 在結構中重載 operator()
    std::size_t operator()(const std::pair<int, int>& p) const {
        // 3. 一個簡單有效的雜湊結合方式
        //    使用標準庫提供的對基本類型的雜湊函數
        auto hash1 = std::hash<int>{}(p.first);
        auto hash2 = std::hash<int>{}(p.second);

        // 將兩個雜湊值結合起來。簡單的 XOR 結合位移可以有效減少碰撞。
        return hash1 ^ (hash2 << 1);
    }
};

int main() {
    // 4. 在宣告 unordered_set 時，將自訂的 Hasher 作為第二個模板參數傳入
    std::unordered_set<std::pair<int, int>, PairHasher> seen_edges;

    seen_edges.insert({1, 2});
    seen_edges.insert({2, 3});

    if (seen_edges.count({1, 2})) {
        std::cout << "Edge (1, 2) exists." << std::endl;
    }
}
```

#### 關鍵 takeaways:

- **`std::set` vs `std::unordered_set`**: `std::set` 可以直接使用 `std::pair` 和 `std::vector`，因為它基於 `operator<`（比較），而這些類型預設支援比較。`std::unordered_set` 基於雜湊，需要額外的工作。
- **靈活性**: 同樣的方法也適用於 `std::vector` 或你自己的 `struct`，只需為它們實現對應的雜湊結構即可。
- **效能**: 提供一個好的雜湊函數對於維持 `unordered_set` 的 O(1) 平均時間複雜度至關重要。
