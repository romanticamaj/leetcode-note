# 位元操作 (Bit Manipulation) Playbook

位元操作是一種直接在位元層級上處理資料的技術。它不僅速度極快，而且在解決特定類型的問題時非常節省空間，例如處理狀態壓縮、集合運算或硬體層級的控制。

## TL;DR (總結)

- **`&` (AND)**: 檢查/取得位元 (Check/Get Bit) - `(x & mask)`
- **`|` (OR)**: 設定位元 (Set Bit) - `(x | mask)`
- **`^` (XOR)**: 翻轉位元 (Flip Bit) - `(x ^ mask)`

## 核心概念：位元遮罩 (Bitmask)

在許多情況下，我們只關心一個數字中的特定幾個位元，而不是全部。為了達到這個目的，我們使用**位元遮罩**（也簡稱為 **mask**）。一個 mask 通常是一個整數，其中一個或多個位元被設定為 1，用來對其他數字進行位元層級的操作。

舉例來說，假設我們想操作數字 `x` 的第 2 個位元（從右邊 0 開始索引，即代表十進位 4 的位元）。

我們可以建立一個 mask，將整數 `1` 向左移動兩位，得到 `100`（二進位）。現在，`x` 和這個 `mask` 之間的任何位元運算都只會「作用」在第 2 個位元上。

```cpp
int x = 13; // 二進位: 1101
int mask = 1 << 2; // 二進位: 0100
```

### 檢查位元 (Check Bit) 與取得位元 (Get Bit) - `&` 運算子

`&` 運算子有兩個重要用途：檢查位元狀態和取得特定位元。

#### 檢查位元 (Check Bit)

如果我們想檢查 `x` 的第 2 個位元是否為 1，我們可以使用 `&` (AND) 運算子。

`mask & x` 的結果只會在 `x` 的第 2 個位元為 1 時才不為零。

- **`&` (AND)**: `1 & 1 = 1`, `1 & 0 = 0`, `0 & 0 = 0`。

```cpp
// x = 1101, mask = 0100
//   1101 (x)
// & 0100 (mask)
// ------
//   0100 (結果為 4，非零)
bool is_bit_set = (x & mask) != 0; // true
```

#### 取得位元 (Get Bit)

除了檢查，`&` 也可以用來提取（isolate）特定位元的值：

```cpp
// 取得第 i 個位元的值 (0 或 1)
int get_bit = (x >> i) & 1;

// 或者，取得多個位元並保持其位置
int bits = x & mask;  // 保留 mask 為 1 的位元，其餘清零
```

**口訣：`& mask` 用於確認位元的真實性 (check) 或提取位元值 (get)。**

### 設定位元 (Set Bit) - `|` 運算子

如果我們想將 `x` 的第 2 個位元設定為 1（無論它原來是什麼），我們可以使用 `|` (OR) 運算子。

- **`|` (OR)**: `1 | 1 = 1`, `1 | 0 = 1`, `0 | 0 = 0`。

```cpp
// x = 1001 (9), mask = 0100
//   1001 (x)
// | 0100 (mask)
// ------
//   1101 (結果為 13)
int result = x | mask;
```

**口訣：`| mask` 用於將位元設為真 (make it true)。**

### 翻轉位元 (Flip Bit) - `^` 運算子

如果我們想翻轉 `x` 的第 2 個位元（1 變 0，0 變 1），我們可以使用 `^` (XOR) 運算子。

- **`^` (XOR)**: `1 ^ 1 = 0`, `1 ^ 0 = 1`, `0 ^ 0 = 0`。

一個簡單的思考方式是：

- `x XOR 0`：`x` 不變。
- `x XOR 1`：`x` 被翻轉。

```cpp
// 情況 1: x = 1101, mask = 0100
//   1101 (x)
// ^ 0100 (mask)
// ------
//   1001 (結果為 9，第 2 位元從 1 變 0)

// 情況 2: x = 1001, mask = 0100
//   1001 (x)
// ^ 0100 (mask)
// ------
//   1101 (結果為 13，第 2 位元從 0 變 1)
```

**口訣：`^ mask` 用於翻轉 (flip) 位元。**

## C++ STL 中的位元運算

C++ 在 `<functional>` 標頭中提供了對應位元運算的函式物件，如 `std::bit_and`, `std::bit_or`, `std::bit_xor`。這些可以方便地與 STL 演算法（如 `std::accumulate`）結合使用。

### ⚠️ 重要警告：運算子優先順序 (Operator Precedence)

在 C++ 中，位元運算子 (`&`, `|`, `^`) 的優先順序**非常低**，甚至低於加減法和比較運算子（如 `==`, `!=`, `<`, `>`）。

這是一個極其常見的錯誤來源。例如，`x & mask != 0` 會被解析為 `x & (mask != 0)`，這幾乎肯定不是你想要的結果。

**最佳實踐：**
為了避免非預期的行為並確保程式碼的清晰度，**永遠**使用括號 `()` 將位元運算式完整地括起來。

```cpp
// 錯誤示範
if (x & mask != 0) { /* ... */ } // 編譯器會先計算 mask != 0，結果通常是 1 或 0

// 正確示範
if ((x & mask) != 0) { /* ... */ }
```

### `std::accumulate` 搭配位元運算

`std::accumulate` 可以對一個範圍內的元素進行累加或其他二元操作。當我們需要對一個集合中的所有數字執行位元運算時，這非常有用。

#### 範例：找出陣列中唯一出現的數字

一個經典問題是：在一個陣列中，除了一個數字外，其他所有數字都出現了兩次。找出那個唯一的數字。

這個問題可以透過 `XOR` 的特性完美解決：`a ^ a = 0` 且 `a ^ 0 = a`。
將所有數字進行 `XOR` 運算，成對的數字會抵銷為 0，最後剩下的就是那個唯一的數字。

```cpp
#include <vector>
#include <numeric> // For std::accumulate
#include <functional> // For std::bit_xor

int singleNumber(const std::vector<int>& nums) {
    // 使用 std::accumulate 和 std::bit_xor 找出唯一數字
    // 初始值為 0，因為 x ^ 0 = x
    return std::accumulate(nums.begin(), nums.end(), 0, std::bit_xor<int>());
}

// 使用範例:
// std::vector<int> v = {4, 1, 2, 1, 2};
// singleNumber(v) 會返回 4
```

#### 範例：計算所有元素的位元 AND/OR

同樣地，我們也可以計算一個範圍內所有元素的 `AND` 或 `OR` 結果。

```cpp
#include <vector>
#include <numeric>
#include <functional>

// 計算所有元素的位元 AND
int and_all(const std::vector<int>& nums) {
    if (nums.empty()) return 0;
    // 注意：初始值設為 ~0 (所有位元為 1)，因為 x & 1 = x
    return std::accumulate(nums.begin(), nums.end(), ~0, std::bit_and<int>());
}

// 計算所有元素的位元 OR
int or_all(const std::vector<int>& nums) {
    if (nums.empty()) return 0;
    // 初始值為 0，因為 x | 0 = x
    return std::accumulate(nums.begin(), nums.end(), 0, std::bit_or<int>());
}
```

這種結合 STL 演算法的方式讓程式碼更簡潔、易讀，並能清晰地表達意圖。
