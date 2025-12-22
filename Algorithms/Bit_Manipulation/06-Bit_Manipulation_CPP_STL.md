# C++ STL 中的位元運算

C++ 在 `<functional>` 標頭中提供了對應位元運算的函式物件，如 `std::bit_and`, `std::bit_or`, `std::bit_xor`。這些可以方便地與 STL 演算法（如 `std::accumulate`）結合使用。

## ⚠️ 重要警告：運算子優先順序 (Operator Precedence)

在 C++ 中，位元運算子 (`&`, `|`, `^`) 的優先順序**非常低**，甚至低於比較運算子（如 `==`, `!=`, `<`, `>`）。

這是一個極其常見的錯誤來源。例如，`x & mask != 0` 會被解析為 `x & (mask != 0)`，這幾乎肯定不是你想要的結果。

**最佳實踐：** **永遠**使用括號 `()` 將位元運算式完整地括起來。

```cpp
// 錯誤示範
if (x & mask != 0) { /* ... */ } // 編譯器會先計算 mask != 0

// 正確示範
if ((x & mask) != 0) { /* ... */ }
```

## `std::accumulate` 搭配位元運算

`std::accumulate` 可以對一個範圍內的元素進行累加或其他二元操作。

### 範例：找出陣列中唯一出現的數字

利用 XOR 特性：`a ^ a = 0` 且 `a ^ 0 = a`，成對數字會抵銷。

```cpp
#include <numeric>
#include <functional>

int singleNumber(const std::vector<int>& nums) {
    return std::accumulate(nums.begin(), nums.end(), 0, std::bit_xor<int>());
}
```

### 範例：計算所有元素的位元 AND/OR

```cpp
// 計算所有元素的位元 AND
// 注意：初始值設為 ~0 (所有位元為 1)
int and_all = std::accumulate(nums.begin(), nums.end(), ~0, std::bit_and<int>());

// 計算所有元素的位元 OR
// 初始值為 0
int or_all = std::accumulate(nums.begin(), nums.end(), 0, std::bit_or<int>());
```

## 內建函式：`__builtin_popcount`

GCC/Clang 提供內建函式來高效計算位元：

```cpp
int x = 0b11010110;

__builtin_popcount(x);      // 計算 1 的個數 → 5
__builtin_popcountll(x);    // long long 版本

__builtin_clz(x);           // Count Leading Zeros（前導 0 數量）
__builtin_ctz(x);           // Count Trailing Zeros（尾隨 0 數量）
__builtin_ffs(x);           // Find First Set（最低位 1 的位置，從 1 開始）
```

**注意：** `__builtin_clz(0)` 和 `__builtin_ctz(0)` 是未定義行為，使用前需檢查 `x != 0`。
