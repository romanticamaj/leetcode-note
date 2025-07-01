# C++ 最大值/最小值初始化技巧

在 C++ 程式設計中，特別是在演算法題目裡，當需要尋找一個集合中的最大值或最小值時，如何正確地初始化 `min_val` 和 `max_val` 變數至關重要。

---

## 問題描述

若將初始值設為一個固定的「魔術數字」（如 `0`, `-1`, `10000`），可能因為輸入數據的實際範圍而導致錯誤的結果。

**錯誤示例**：

```cpp
// 錯誤示例 - 初始值設定不當
int min_val = 10000; // 如果輸入陣列所有數都大於 10000，結果會是錯的
for (int x : nums) {
    min_val = min(min_val, x);
}
```

---

## 正確心法：使用 `std::numeric_limits`

最標準、最安全的方法是使用 `<limits>` 標頭檔中的 `std::numeric_limits` 來取得該型別的最大值或最小值，確保初始值在任何情況下都有效。

**正確示例**：

```cpp
#include <limits>

// 正確示例 - 使用 numeric_limits
int min_val = std::numeric_limits<int>::max(); // 初始化為 int 的最大值
int max_val = std::numeric_limits<int>::min(); // 初始化為 int 的最小值

for (int x : nums) {
    min_val = min(min_val, x);
    max_val = max(max_val, x);
}
```

---

## 為什麼要這樣做？

- **通用性**：適用於任何內建數值型別（`int`, `long long`, `double` 等）。
- **可讀性**：程式碼意圖清晰，一看就知道是在尋找最大/最小值。
- **安全性**：避免了因「魔術數字」選擇不當而導致的邊界錯誤。

---

## 結論

當你需要一個「無限大」或「無限小」的初始值時，`std::numeric_limits` 是最標準、最安全、最可讀的選擇。養成使用它的習慣，可以顯著提升程式碼的穩健性。
